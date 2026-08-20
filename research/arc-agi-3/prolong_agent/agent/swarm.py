"""Run one scorecard across multiple games in parallel threads.

Usage:
    prolong_agent-swarm --suite all --max-actions 500
    prolong_agent-swarm --game ls20,ft09
"""
from __future__ import annotations

import argparse
import logging
import os
import signal
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import arc_agi
import requests
from arc_agi import OperationMode
from dotenv import load_dotenv

from prolong_agent.environment import ArcAgi3Env
from prolong_agent.environment.config import EVALUATION_GAMES
from prolong_agent.environment.runner import GameRunner
from prolong_agent.metrics.reporting import calculate_stats, generate_console_report, save_summary_report
from prolong_agent.metrics.structures import GameMetrics, Status

log = logging.getLogger(__name__)

_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
load_dotenv(dotenv_path=_project_root / ".env", override=False)

ROOT_URL = os.environ.get("ROOT_URL", "https://arcprize.org")
DEFAULT_MODELS = {
    "codex": "gpt-5.5",
    "claude-code": "claude-opus-4-6",
}


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
            )
            metrics = runner.run()

            with self._lock:
                self.results[game_id] = metrics

        except Exception as exc:
            log.error("Game %s failed: %s", game_id, exc, exc_info=True)
            with self._lock:
                self.results[game_id] = GameMetrics(
                    game_id=game_id,
                    agent_name=self.inner_agent_kwargs.get("name", "swarm_agent"),
                    start_time=time.time(),
                    status=Status.ERROR,
                    error_message=str(exc),
                )
        finally:
            if env:
                try:
                    env.close()
                except Exception:
                    pass


def _parse_args():
    parser = argparse.ArgumentParser(description="Run ARC-AGI-3 Swarm evaluation.")
    parser.add_argument("--agent", "-a", default="prolong_agent")
    parser.add_argument("--game", "-g", help="Comma-separated game names or IDs (e.g. ls20,ft09).")
    parser.add_argument("--suite", "-s", choices=list(EVALUATION_GAMES.keys()))
    parser.add_argument("--tags", "-t", help="Comma-separated tags.")
    parser.add_argument("--max-actions", type=int, default=500)
    parser.add_argument("--operation-mode", default="online", choices=["normal", "online", "offline"])
    parser.add_argument("--model", "-m", help="Model name; defaults depend on backend")
    parser.add_argument("--retries", type=int, default=5, help="Max agent retry attempts")
    parser.add_argument("--backend", default="codex", choices=["codex", "claude-code"])
    parser.add_argument("--api-key", dest="use_api_key", action="store_true",
                        help="Use ANTHROPIC_API_KEY instead of Claude Max authentication")
    parser.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"],
                        help="Claude Code effort level")
    parser.add_argument("--reasoning-effort", default="none",
                        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
                        help="Codex reasoning effort")
    parser.add_argument("--grid-mode", default="hex", choices=["ascii", "hex", "num"])
    parser.add_argument("--log-window", type=int,
                        help="History mode: full log by default, last N actions for N>0, or -1 for no log")
    parser.add_argument("--action-cap", type=int, default=20,
                        help="Max actions per agent plan (default 20)")
    parser.add_argument("--note", default="", help="Short run description saved to run_info.txt")
    args = parser.parse_args()
    if args.log_window is not None and args.log_window != -1 and args.log_window < 1:
        parser.error("--log-window must be -1 or a positive integer")
    return args


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


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    logging.getLogger("arc_agi").propagate = False

    args = _parse_args()
    model = args.model or DEFAULT_MODELS[args.backend]
    try:
        games = _resolve_games(args)
    except Exception as exc:
        log.error("Failed to fetch games from API: %s", exc)
        sys.exit(1)

    if not games:
        log.error("No games to run. Provide --game, --suite, or set ARC_API_KEY.")
        sys.exit(1)

    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    tags.append(f"swarm-{args.agent}")

    arcade = arc_agi.Arcade(
        arc_api_key=os.getenv("ARC_API_KEY", ""),
        arc_base_url=ROOT_URL,
        operation_mode=OperationMode(args.operation_mode),
    )

    agent = _create_agent(args, model)

    timestamp = datetime.now().strftime("%m%dT%H%M%S")
    note_slug = f"__{args.note.replace(' ', '-')}" if args.note else ""
    run_dir = Path("evaluation_results") / f"{timestamp}_swarm_{args.agent}{note_slug}"
    run_dir.mkdir(parents=True, exist_ok=True)

    inner_agent_kwargs: dict[str, Any] = {
        "name": args.agent,
        "grid_mode": args.grid_mode,
    }

    swarm = Swarm(
        inner_agent_kwargs=inner_agent_kwargs,
        arcade=arcade, games=games, tags=tags,
        max_actions=args.max_actions,
        agent=agent.analyze,
        prompts_log_dir=run_dir,
        log_post_board=True,
        agent_retries=args.retries,
    )

    runner = threading.Thread(target=swarm.run, daemon=True)
    runner.start()

    def sigint_handler(sig: int, frame: Any) -> None:
        print("[Swarm] SIGINT received — cleaning up...", flush=True)
        sys.exit(1)

    signal.signal(signal.SIGINT, sigint_handler)

    while runner.is_alive():
        runner.join(timeout=1)

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


if __name__ == "__main__":
    main()
