"""Run one scorecard across multiple games in parallel threads.

Usage:
    prolong-swarm --suite all --max-actions 500
    prolong-swarm --game ls20,ft09
"""
from __future__ import annotations

import logging
import os
import re
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import arc_agi
import requests
from arc_agi import OperationMode
from dotenv import load_dotenv

from prolong_agent.environment import ArcAgi3Env
from prolong_agent.environment.config import EVALUATION_GAMES
from prolong_agent.environment.runner import GameRunner
from prolong_agent.experiment import parse_args
from prolong_agent.manifest import (
    collect_provenance,
    create_manifest,
    utc_now,
    write_manifest,
)
from prolong_agent.metrics.reporting import (
    calculate_stats,
    generate_console_report,
    save_summary_report,
)
from prolong_agent.metrics.structures import GameMetrics, Status

log = logging.getLogger(__name__)

_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
load_dotenv(dotenv_path=_project_root / ".env", override=False)

ROOT_URL = os.environ.get("ROOT_URL", "https://arcprize.org")


class Swarm:
    """Manages a single scorecard and runs one agent per game in daemon threads."""

    def __init__(
        self,
        inner_agent_kwargs: dict[str, Any],
        arcade: arc_agi.Arcade,
        games: list[str],
        tags: list[str],
        max_actions: int = 500,
        agent=None,
        prompts_log_dir: Path | None = None,
        log_post_board: bool = True,
        agent_retries: int = 5,
        run_index: int = 1,
    ) -> None:
        self.inner_agent_kwargs = inner_agent_kwargs
        self._arcade = arcade
        self.games = games
        self.tags = tags
        self.max_actions = max_actions
        self.agent = agent
        self.prompts_log_dir = prompts_log_dir
        self.log_post_board = log_post_board
        self.agent_retries = agent_retries
        self.run_index = run_index

        self.card_id: str | None = None
        self.scorecard: Any = None
        self.results: dict[str, GameMetrics] = {}
        self._lock = threading.Lock()

    def run(self) -> dict[str, GameMetrics]:
        self.card_id = self._arcade.open_scorecard(tags=self.tags)
        log.info("Opened scorecard %s for %d game(s)", self.card_id, len(self.games))

        threads = [
            threading.Thread(target=self._run_game, args=(self.card_id, gid), daemon=True)
            for gid in self.games
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.scorecard = self._arcade.close_scorecard(self.card_id)
        log.info("Closed scorecard %s", self.card_id)
        return self.results

    def _run_game(self, card_id: str, game_id: str) -> None:
        env = None
        try:
            env = ArcAgi3Env.from_arcade(
                arcade=self._arcade, game_id=game_id,
                scorecard_id=card_id, max_actions=self.max_actions,
            )

            prompts_log_path = None
            if self.prompts_log_dir:
                game_dir = self.prompts_log_dir / game_id.split("-")[0]
                game_dir.mkdir(parents=True, exist_ok=True)
                prompts_log_path = game_dir / "logs.txt"
                prompts_log_path.write_text("")

            runner = GameRunner(
                env=env,
                game_id=game_id,
                agent_name=self.inner_agent_kwargs.get("name", "swarm_agent"),
                max_actions_per_game=self.max_actions,
                tags=self.tags,
                prompts_log_path=prompts_log_path,
                agent=self.agent,
                log_post_board=self.log_post_board,
                agent_retries=self.agent_retries,
                agent_kwargs=self.inner_agent_kwargs,
                run_index=self.run_index,
            )
            metrics = runner.run()

            with self._lock:
                self.results[game_id] = metrics

        except Exception as exc:
            log.exception("Game %s failed: %s", game_id, exc)
            with self._lock:
                self.results[game_id] = GameMetrics(
                    game_id=game_id,
                    agent_name=self.inner_agent_kwargs.get("name", "swarm_agent"),
                    run_index=self.run_index,
                    start_time=time.time(),
                    status=Status.ERROR,
                    error_message=str(exc),
                )
        finally:
            if env:
                try:
                    env.close()
                except Exception:
                    log.exception("Failed to close environment %s", game_id)


def _parse_args(argv=None):
    return parse_args(argv, suites=EVALUATION_GAMES)


def _resolve_games(args):
    known_games = {game for games in EVALUATION_GAMES.values() for game in games}
    short_names = {game.split("-")[0]: game for game in known_games}
    if args.game:
        requested = [game.strip() for game in args.game.split(",") if game.strip()]
        return [short_names.get(game, game) for game in requested]
    if args.suite:
        return EVALUATION_GAMES[args.suite]

    response = requests.get(
        f"{ROOT_URL}/api/games",
        headers={"X-API-Key": os.getenv("ARC_API_KEY", ""), "Accept": "application/json"},
        timeout=15,
    )
    response.raise_for_status()
    games = [game["game_id"] for game in response.json()]
    log.info("Fetched %d games from API", len(games))
    return games


def _create_agent(args, model):
    history = "full" if args.log_window is None else "no log" if args.log_window == -1 else f"last {args.log_window}"
    if args.backend == "codex":
        from prolong_agent.agent import CodexAgent
        agent = CodexAgent(
            model=model,
            reasoning_effort=args.reasoning_effort,
            grid_mode=args.grid_mode,
            run_label=args.note,
            log_window=args.log_window,
            action_cap=args.action_cap,
        )
        effort = args.reasoning_effort
    else:
        from prolong_agent.agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(
            model=model,
            use_api_key=args.use_api_key,
            grid_mode=args.grid_mode,
            run_label=args.note,
            log_window=args.log_window,
            effort=args.effort,
            action_cap=args.action_cap,
        )
        effort = args.effort
    log.info("Agent (backend=%s, model=%s, effort=%s, history=%s)",
             args.backend, model, effort, history)
    return agent


def _save_reports(swarm, args, run_dir):
    results_list = list(swarm.results.values())

    print(f"\nScorecard ID: {swarm.card_id}")
    print(f"Results:      {run_dir}")
    for m in sorted(results_list, key=lambda r: r.game_id):
        if m.replay_url:
            print(f"  Replay:     {m.replay_url}")

    if swarm.scorecard:
        scorecard_path = run_dir / "scorecard.json"
        scorecard_path.write_text(swarm.scorecard.model_dump_json(indent=2))
        log.info("Scorecard saved to %s", scorecard_path)

    if results_list:
        generate_console_report(results_list, "swarm", args.agent, 1, scorecard=swarm.scorecard)
        game_stats, overall = calculate_stats(results_list)
        summary_path = run_dir / "summary.txt"
        save_summary_report(
            str(summary_path), game_stats, overall, results_list,
            args.agent, "swarm", 1, scorecard=swarm.scorecard,
        )
        log.info("Summary saved to %s", summary_path)
    else:
        log.error("No results collected.")


def _run_repetition(args, games, experiment_id, repetition):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    label = re.sub(r"[^A-Za-z0-9_.-]+", "-", f"{args.agent}__{args.note}")[:100]
    run_dir = Path("evaluation_results") / f"{timestamp}_swarm_{label}_rep{repetition}_{experiment_id[:12]}"
    run_dir.mkdir(parents=True, exist_ok=False)
    manifest = create_manifest(args, games, experiment_id, repetition)
    write_manifest(run_dir, manifest)
    agent = swarm = None
    try:
        agent = _create_agent(args, args.model)
        proxy_image = "prolong-openai-proxy" if args.backend == "codex" else "prolong-anthropic-proxy"
        manifest["provenance"] = collect_provenance(_project_root, agent.docker_image, proxy_image)
        write_manifest(run_dir, manifest)
        tags = [tag.strip() for tag in (args.tags or "").split(",") if tag.strip()]
        tags.append(f"swarm-{args.agent}")
        arcade = arc_agi.Arcade(
            arc_api_key=os.getenv("ARC_API_KEY", ""), arc_base_url=ROOT_URL,
            operation_mode=OperationMode(args.operation_mode),
        )
        swarm = Swarm(
            inner_agent_kwargs={"name": args.agent, "grid_mode": args.grid_mode},
            arcade=arcade, games=games, tags=tags, max_actions=args.max_actions,
            agent=agent.analyze, prompts_log_dir=run_dir, log_post_board=True,
            agent_retries=args.retries, run_index=repetition,
        )
        errors = []

        def run():
            try:
                swarm.run()
            except BaseException as error:
                errors.append(error)

        runner = threading.Thread(target=run, daemon=True)
        runner.start()
        while runner.is_alive():
            runner.join(timeout=1)
        if errors:
            raise errors[0]
        _save_reports(swarm, args, run_dir)
        incomplete = {Status.ERROR, Status.PENDING, Status.IN_PROGRESS, Status.QUEUE_EXHAUSTED}
        if set(swarm.results) != set(games) or any(m.status in incomplete for m in swarm.results.values()):
            raise RuntimeError("One or more games failed or did not return a final result")
        manifest["status"] = "completed"
    except BaseException as error:
        manifest["status"] = "interrupted" if isinstance(error, KeyboardInterrupt) else "failed"
        manifest["error_type"] = type(error).__name__
        raise
    finally:
        try:
            if agent is not None:
                agent.close()
        except Exception as error:
            if manifest["status"] == "completed":
                manifest["status"] = "failed"
                manifest["error_type"] = type(error).__name__
                raise
            log.exception("Backend cleanup failed after evaluation stopped")
        finally:
            manifest["finished_at"] = utc_now()
            if swarm is not None:
                with swarm._lock:
                    manifest["game_statuses"] = {game: result.status.value for game, result in swarm.results.items()}
                manifest["scorecard_id"] = swarm.card_id
                manifest["missing_games"] = [game for game in games if game not in manifest["game_statuses"]]
            write_manifest(run_dir, manifest)
    return run_dir


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    logging.getLogger("arc_agi").propagate = False
    args = _parse_args()
    try:
        games = _resolve_games(args)
        if not games:
            raise ValueError("No games to run. Provide --game, --suite, or set ARC_API_KEY.")
        if len({game.split('-')[0] for game in games}) != len(games):
            raise ValueError("Games must have distinct short names; use --repetitions for repeated runs.")
        experiment_id = uuid.uuid4().hex
        for repetition in range(1, args.repetitions + 1):
            _run_repetition(args, games, experiment_id, repetition)
    except KeyboardInterrupt:
        log.warning("Evaluation interrupted; stopping remaining repetitions.")
        sys.exit(130)
    except Exception:
        log.exception("Evaluation failed; stopping remaining repetitions.")
        sys.exit(1)


if __name__ == "__main__":
    main()
