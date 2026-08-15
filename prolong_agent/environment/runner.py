"""Game loop that drives the action queue through an ARC-AGI-3 environment."""
from prolong_agent.utils import action_metadata as _am
import json
import logging
import os
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, Optional

import requests

try:
    import wandb
    _HAS_WANDB = True
except ImportError:
    _HAS_WANDB = False

from prolong_agent.agent import GameState, ActionQueue, QueueExhausted
from prolong_agent.environment import ArcAgi3Env
from arcengine import GameState as ArcGameState
from prolong_agent.metrics.structures import GameMetrics, LevelMetrics, AttemptMetrics, Status

log = logging.getLogger(__name__)

ROOT_URL = os.environ.get("ROOT_URL", "https://three.arcprize.org")
MAX_RETRIES = 5
INITIAL_BACKOFF = 1

_RETRY_NUDGE = (
    "Your previous response did not produce a valid /workspace/actions.json. "
    "Please write one with the shape {\"actions\": [...]}."
)


def _run_with_retries(func: Callable, *args: Any, **kwargs: Any) -> Any:
    retries = 0
    backoff = INITIAL_BACKOFF
    while True:
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if retries >= MAX_RETRIES:
                log.error("Final attempt failed for %s after %d retries.", func.__name__, retries)
                raise
            log.warning("%s: %s. Retrying in %ds (%d/%d)",
                        func.__name__, type(e).__name__, backoff, retries + 1, MAX_RETRIES)
            time.sleep(backoff)
            retries += 1
            backoff *= 2


class GameRunner:
    """Runs a game by orchestrating GameState, ActionQueue, and the analyzer agent."""

    def __init__(
        self,
        *,
        env: ArcAgi3Env,
        game_id: str,
        agent_name: str,
        max_actions_per_game: int,
        run_index: int = 1,
        tags: Optional[list[str]] = None,
        prompts_log_path: Optional[Path] = None,
        analyzer=None,
        log_post_board: bool = False,
        analyzer_retries: int = 5,
        agent_kwargs: Optional[dict] = None,
        stateless: bool = False,
    ) -> None:
        self.env = env
        self.game_id = game_id
        self.agent_name = agent_name
        self.max_actions_per_game = max_actions_per_game
        self.run_index = run_index
        self.tags = tags
        self.prompts_log_path = prompts_log_path
        self.analyzer = analyzer
        self.log_post_board = log_post_board
        self.analyzer_retries = analyzer_retries
        self.stateless = stateless
        self._level_start_action: int = 0
        self._state = GameState(**(agent_kwargs or {}))
        self._queue = ActionQueue()
        self._last_cost: float = 0.0
        self._last_analyzer_duration: float = 0.0
        self._cum = {"calls": 0, "in": 0, "out": 0, "cache_read": 0, "cost": 0.0, "actions": 0}
        self._recent_actions: list[str] = []
        self._last_logged_action: dict = {}

    def _next_action(self) -> dict:
        obs = self._state.last_observation or {}
        state = obs.get("state", "NOT_PLAYED")

        if state in ("NOT_PLAYED", "GAME_OVER") and self._state.last_executed_action != "RESET":
            return {"name": "RESET", "data": {}, "obs_text": "Game Over, starting new game.", "action_text": ""}

        use_queued = bool(self._queue and not self._queue.score_changed)
        if not use_queued:
            self._queue.score_changed = False

        if use_queued and self._queue:
            action = self._queue.pop()
            # Guard against double-RESET or RESET-after-WIN triggering full_reset.
            _reset_unsafe = action.get("name") == "RESET" and (
                self._state.last_executed_action == "RESET"
                or state == "WIN"
            )
            if _reset_unsafe:
                _reason = ("duplicate RESET" if self._state.last_executed_action == "RESET"
                           else f"RESET while state={state}")
                log.warning(
                    "inserting ACTION7 no-op before %s (%d queued remaining)",
                    _reason, len(self._queue),
                )
                self._queue.push_front(action)
                action = {
                    "name": "ACTION7",
                    "data": {},
                    "obs_text": "",
                    "action_text": f"[injected ACTION7 no-op before {_reason}]",
                }
            label = f"plan step {self._queue.plan_index}/{self._queue.plan_total}"
            action["obs_text"] = ""
            action["action_text"] = f"[queued {label}]"

            log.info("queue drain -> %s (%s, %d remaining)",
                     action.get("name"), label, len(self._queue))
            return action

        log.info("queue empty — need new plan from analyzer")
        raise QueueExhausted("Queue empty, no actions from analyzer")


    def _build_action_metadata(self, action_dict: dict, action_num: int) -> str:
        """ARC reasoning-field JSON for one action. Full stats on batch heads;
        light stub on queued drains so replay analysis has per-action data."""
        import json
        meta = action_dict.get("batch_meta")
        name = action_dict.get("name", "?")
        data = action_dict.get("data", {})
        act_str = (f"ACTION6({data.get('x',0)},{data.get('y',0)})"
                   if name == "ACTION6" else name)
        aggregate = {
            "analyzer_calls": self._cum["calls"],
            "actions": action_num + 1,
            "input_tokens": self._cum["in"],
            "output_tokens": self._cum["out"],
            "cache_read_tokens": self._cum["cache_read"],
            "cost_usd": round(self._cum["cost"], 4),
        }
        if meta and action_dict.get("batch_head"):
            hint = ""
            payload = _am.build(
                output=meta.get("output", ""),
                input_tokens=meta.get("input_tokens", 0),
                cached_tokens=meta.get("cached_tokens", 0),
                output_tokens=meta.get("output_tokens", 0),
                reasoning_tokens=meta.get("reasoning_tokens", 0),
                cost_usd=meta.get("call_cost_usd", 0.0),
                commands=meta.get("commands"),
                plan={"step": f"{self._queue.plan_index}/{self._queue.plan_total}",
                      "action": act_str},
                aggregate=aggregate,
                model=meta.get("model", ""),
            )
        else:
            payload = _am.build(
                output=f"queued plan step {self._queue.plan_index}/{self._queue.plan_total}: {act_str}",
                plan={"step": f"{self._queue.plan_index}/{self._queue.plan_total}",
                      "action": act_str},
                aggregate=aggregate,
            )
        try:
            return json.dumps(payload, separators=(",", ":"))
        except Exception:
            return f"Action: {name}"

    def run(self) -> GameMetrics:
        metrics = GameMetrics(
            game_id=self.game_id,
            agent_name=self.agent_name,
            run_index=self.run_index,
            start_time=time.time(),
        )
        metrics.status = Status.IN_PROGRESS

        level_num = 1
        level_metrics = LevelMetrics(level_number=level_num)
        attempt_num = 1
        attempt_metrics = AttemptMetrics(attempt_number=attempt_num)
        attempt_start = metrics.start_time

        max_score = 0
        total_actions = 0
        arc_state: ArcGameState | None = None
        arc_score = 0

        try:
            self._state.reset()
            self._queue.reset()

            observation = _run_with_retries(
                self.env.reset,
                task={"game_id": self.game_id, "max_actions": self.max_actions_per_game, "tags": self.tags},
            )
            arc_state = ArcGameState[observation.get("state") or "NOT_PLAYED"]
            arc_score = observation.get("score", 0) or 0

            guid = observation.get("guid")
            if guid and not metrics.guid:
                metrics.guid = guid
                metrics.replay_url = f"{ROOT_URL}/replay/{self.game_id}/{guid}"
                log.info("[%s Run %d] Replay URL: %s", self.game_id, self.run_index, metrics.replay_url)
                if self.prompts_log_path:
                    info_path = self.prompts_log_path.parent / "run_info.txt"
                    note = ""
                    for i, arg in enumerate(sys.argv):
                        if arg == "--note" and i + 1 < len(sys.argv):
                            note = sys.argv[i + 1]
                    info_path.write_text(
                        (f"note: {note}\n" if note else "")
                        + f"game_id: {self.game_id}\n"
                        f"guid: {guid}\n"
                        f"replay_url: {metrics.replay_url}\n"
                        f"scorecard_id: {getattr(self.env, '_scorecard_id', 'unknown')}\n"
                        f"command: {Path(sys.argv[0]).name} {' '.join(sys.argv[1:])}\n"
                    )

            self._state.record_env_update(observation=observation, reward=0.0, done=False)

            ACTION_NAMES = {1: "ACTION1", 2: "ACTION2", 3: "ACTION3", 4: "ACTION4",
                            5: "ACTION5", 6: "ACTION6", 7: "ACTION7", 0: "RESET"}
            raw_actions = observation.get("available_actions", [])
            self._available_action_names = sorted(
                {ACTION_NAMES.get(a, f"ACTION{a}") for a in raw_actions} | {"RESET"}
            )
            log.info("[%s] Available actions: %s", self.game_id, ", ".join(self._available_action_names))

            if self.prompts_log_path and self.prompts_log_path.stat().st_size == 0:
                grid = self._state.render_board()
                if grid:
                    with open(self.prompts_log_path, 'a', encoding='utf-8') as f:
                        f.write(f"{'='*80}\n")
                        f.write(f"Action 0 | Level {level_num} | Attempt {attempt_num} | INITIAL STATE | Score: {arc_score}\n\n")
                        f.write(f"[INITIAL BOARD STATE]\n{grid}\n\n")

            if self.prompts_log_path:
                board_path = self.prompts_log_path.parent / "current_board.txt"
                grid = self._state.render_board(include_animation=False)
                with open(board_path, 'w', encoding='utf-8') as f:
                    f.write(f"Score: {arc_score}\nAction: 0\n\n")
                    if grid:
                        f.write(f"[CURRENT BOARD STATE]\n{grid}\n")

            while total_actions < self.max_actions_per_game:
                try:
                    action_dict = self._next_action()
                except QueueExhausted:
                    log.info("queue exhausted at action %d — firing analyzer", total_actions)
                    loaded = False
                    stall_backoff = 30  # seconds between macro-retries
                    while not loaded:
                        for attempt in range(self.analyzer_retries):
                            nudge = _RETRY_NUDGE if attempt > 0 else ""
                            log.info("analyzer attempt %d/%d action=%d nudge=%s",
                                     attempt + 1, self.analyzer_retries, total_actions, bool(nudge))
                            if self._fire_analyzer(total_actions, arc_score, retry_nudge=nudge,
                                                   level_num=level_num):
                                loaded = True
                                break
                            log.warning("analyzer attempt %d/%d failed", attempt + 1, self.analyzer_retries)
                        if not loaded:
                            log.warning(
                                "all %d analyzer attempts failed at action %d — "
                                "sleeping %ds before retrying (will not close scorecard)",
                                self.analyzer_retries, total_actions, stall_backoff,
                            )
                            time.sleep(stall_backoff)
                            stall_backoff = min(stall_backoff * 2, 300)  # cap at 5 min
                    action_dict = self._next_action()

                action_dict["action_metadata"] = self._build_action_metadata(action_dict, total_actions)
                action_result = self._state.record_action(action_dict)
                self._last_logged_action = action_dict
                name = action_dict.get("name", "?")
                data = action_dict.get("data", {})
                if name == "ACTION6":
                    self._recent_actions.append(f"ACTION6({data.get('x',0)},{data.get('y',0)})")
                else:
                    self._recent_actions.append(name)
                observation, reward, done = _run_with_retries(self.env.step, action_result)

                total_actions += 1
                attempt_metrics.actions += 1

                prev_score = arc_score
                prev_max_score = max_score
                arc_state = ArcGameState[observation.get("state") or "NOT_PLAYED"]
                arc_score = observation.get("score", 0) or 0
                max_score = max(max_score, arc_score)
                metrics.highest_level_reached = max(metrics.highest_level_reached, level_num)

                self._state.record_env_update(observation=observation, reward=reward, done=done)
                self._queue.check_score(arc_score)

                self._log_action(total_actions, level_num, attempt_num, arc_score, arc_state)

                if _HAS_WANDB and wandb.run is not None:
                    wandb.log({
                        # Top-level metrics — show in the default workspace view.
                        "score": arc_score,
                        "level": level_num,
                        "action": total_actions,
                        "max_score_so_far": max_score,
                        # Game-prefixed mirrors for runs that compare across games.
                        f"{self.game_id}/score": arc_score,
                        f"{self.game_id}/level": level_num,
                        f"{self.game_id}/action": total_actions,
                        f"{self.game_id}/attempt": attempt_num,
                        f"{self.game_id}/queue_size": len(self._queue),
                        f"{self.game_id}/cost": self._last_cost,
                        f"{self.game_id}/analyzer_seconds": self._last_analyzer_duration,
                    }, step=total_actions)

                if self.log_post_board and self.prompts_log_path:
                    grid = self._state.render_board()
                    if grid:
                        for _log_attempt in range(3):
                            try:
                                with open(self.prompts_log_path, 'a', encoding='utf-8') as f:
                                    f.write(f"[POST-ACTION BOARD STATE]\n{grid}\n\n")
                                break
                            except PermissionError:
                                time.sleep(0.5)
                        else:
                            log.warning("failed to write board state after 3 retries (PermissionError)")

                if arc_score > prev_max_score and arc_state not in (ArcGameState.WIN, ArcGameState.GAME_OVER):
                    attempt_metrics.duration_seconds = time.time() - attempt_start
                    attempt_metrics.status = Status.COMPLETED
                    level_metrics.attempts.append(attempt_metrics)
                    level_metrics.status = Status.COMPLETED
                    metrics.level_metrics[level_num] = level_metrics

                    log.info("[%s Run %d] Level %d COMPLETED. Attempt %d actions: %d. Score: %d.",
                             self.game_id, self.run_index, level_num, attempt_num, attempt_metrics.actions, arc_score)

                    level_num += 1
                    self._level_start_action = total_actions
                    metrics.highest_level_reached = max(metrics.highest_level_reached, level_num)
                    level_metrics = LevelMetrics(level_number=level_num)
                    attempt_num = 1
                    attempt_metrics = AttemptMetrics(attempt_number=attempt_num)
                    attempt_start = time.time()

                    continue

                if arc_state == ArcGameState.GAME_OVER:
                    attempt_metrics.duration_seconds = time.time() - attempt_start
                    attempt_metrics.status = Status.GAME_OVER
                    attempt_metrics.game_overs += 1
                    level_metrics.attempts.append(attempt_metrics)
                    level_metrics.status = Status.GAME_OVER
                    metrics.level_metrics[level_num] = level_metrics
                    metrics.status = Status.TIMEOUT
                    log.warning("[%s Run %d] Game Over on Level %d, Attempt %d. Actions: %d.",
                                self.game_id, self.run_index, level_num, attempt_num, attempt_metrics.actions)
                    attempt_num += 1
                    attempt_metrics = AttemptMetrics(attempt_number=attempt_num)
                    attempt_start = time.time()

                if arc_state == ArcGameState.WIN:
                    attempt_metrics.duration_seconds = time.time() - attempt_start
                    attempt_metrics.status = Status.COMPLETED
                    level_metrics.attempts.append(attempt_metrics)
                    level_metrics.status = Status.COMPLETED
                    metrics.level_metrics[level_num] = level_metrics
                    metrics.status = Status.COMPLETED_RUN
                    log.info("[%s Run %d] Game COMPLETED! Level %d actions: %d. Score: %d",
                             self.game_id, self.run_index, level_num, attempt_metrics.actions, arc_score)
                    break

        except QueueExhausted as e:
            log.info("[%s Run %d] Episode ended (queue exhausted): %s", self.game_id, self.run_index, e)
            metrics.status = Status.QUEUE_EXHAUSTED

        except Exception as e:
            metrics.status = Status.ERROR
            metrics.error_message = str(e)
            attempt_metrics.status = Status.ERROR
            level_metrics.status = Status.ERROR
            log.error("[%s Run %d] Exception: %s", self.game_id, self.run_index, e, exc_info=True)

        finally:
            metrics.end_time = time.time()
            metrics.run_duration_seconds = metrics.end_time - metrics.start_time

            if attempt_metrics.status == Status.IN_PROGRESS:
                attempt_metrics.duration_seconds = metrics.end_time - attempt_start
                if metrics.status == Status.ERROR:
                    attempt_metrics.status = Status.ERROR
                elif arc_state == ArcGameState.WIN:
                    attempt_metrics.status = Status.COMPLETED
                    metrics.status = Status.COMPLETED_RUN
                else:
                    attempt_metrics.status = Status.TIMEOUT
                    if metrics.status == Status.IN_PROGRESS:
                        metrics.status = Status.TIMEOUT

            if (not level_metrics.attempts
                    or level_metrics.attempts[-1].attempt_number != attempt_metrics.attempt_number):
                level_metrics.attempts.append(attempt_metrics)
            if level_metrics.status == Status.IN_PROGRESS:
                level_metrics.status = attempt_metrics.status

            metrics.level_metrics[level_num] = level_metrics
            metrics.run_total_actions = sum(lm.total_actions for lm in metrics.level_metrics.values())
            metrics.total_game_overs_across_run = sum(lm.total_game_overs for lm in metrics.level_metrics.values())
            metrics.total_state_changes_across_run = sum(lm.total_state_changes for lm in metrics.level_metrics.values())
            metrics.final_score = max_score

            if metrics.guid and not metrics.replay_url:
                metrics.replay_url = f"{ROOT_URL}/replay/{self.game_id}/{metrics.guid}"

        return metrics

    def _fire_analyzer(self, action_num: int, arc_score: int, retry_nudge: str = "",
                       level_num: int = 1) -> bool:
        if not self.analyzer:
            return False
        if self.prompts_log_path and not self.log_post_board:
            grid = self._state.render_board()
            if grid:
                with open(self.prompts_log_path, 'a', encoding='utf-8') as f:
                    f.write(f"[POST-ACTION BOARD STATE]\n{grid}\n\n")

        if self.prompts_log_path:
            board_path = self.prompts_log_path.parent / "current_board.txt"
            grid = self._state.render_board(include_animation=False)
            with open(board_path, 'w', encoding='utf-8') as f:
                f.write(f"Score: {arc_score}\nAction: {action_num}\n\n")
                if grid:
                    f.write(f"[CURRENT BOARD STATE]\n{grid}\n")

        kwargs = {
            "score": arc_score,
            "level": level_num,
            "last_actions": ", ".join(self._recent_actions[-5:]) if self._recent_actions else "none",
            "available_actions_list": list(self._available_action_names),
            "available_actions": ", ".join(self._available_action_names),
        }

        t0 = time.time()
        result = self.analyzer(self.prompts_log_path, action_num, retry_nudge=retry_nudge, **kwargs)
        self._last_analyzer_duration = time.time() - t0
        if not result:
            log.warning("analyzer returned None at action %d (%.1fs)", action_num, self._last_analyzer_duration)
            return False

        self._last_cost = result.get("cost", self._last_cost)
        self._state.set_external_hint(result["hint"])
        self._state.set_persistent_hint(result["plan"])

        actions = result.get("actions", [])
        _meta = result.get("meta")
        if _meta:
            cum = _meta.get("cumulative", False)
            ci = _meta.get("input_tokens", 0) or 0
            co = _meta.get("output_tokens", 0) or 0
            cr = _meta.get("cached_tokens", 0) or 0
            if cum:  # codex reports cumulative; diff to per-call
                pi = self._cum["in"]; po = self._cum["out"]; pr = self._cum["cache_read"]
                _meta = dict(_meta,
                             input_tokens=max(0, ci - pi),
                             output_tokens=max(0, co - po),
                             cached_tokens=max(0, cr - pr))
                self._cum["in"], self._cum["out"], self._cum["cache_read"] = ci, co, cr
            else:
                self._cum["in"] += ci; self._cum["out"] += co; self._cum["cache_read"] += cr
            self._cum["calls"] += 1
            self._cum["cost"] += _meta.get("call_cost_usd", 0.0) or 0.0
        if actions:
            if self._queue.load(actions, batch_meta=_meta):
                log.info("analyzer at action %d: loaded %d actions", action_num, len(actions))
                return True
            log.warning("analyzer at action %d: queue rejected the actions", action_num)
            return False

        log.warning("analyzer at action %d: no actions from actions.json", action_num)
        return False

    def _log_action(self, action_num: int, level: int, attempt: int,
                    arc_score: int, arc_state: ArcGameState) -> None:
        if not self.prompts_log_path:
            return
        action_dict = self._last_logged_action or {}
        with open(self.prompts_log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            plan_info = f" | Plan Step {self._queue.plan_index}/{self._queue.plan_total}" if self._queue.plan_total > 0 else ""
            f.write(f"Action {action_num} | Level {level} | Attempt {attempt}{plan_info} | Score: {arc_score}\n\n")
            hint = self._state.consume_hint_block()
            if hint:
                if self.stateless:
                    # stateless ablation: keep the agent's [PLAN] for our records but
                    # do NOT carry it forward in logs.txt — the agent sees only the
                    # objective trace (boards/actions/scores) next turn.
                    plans = self.prompts_log_path.parent / "plans.txt"
                    with open(plans, 'a', encoding='utf-8') as pf:
                        pf.write(f"\n{'='*80}\nAction {action_num} | Level {level} | Score: {arc_score}{hint}\n")
                else:
                    f.write(f"{hint}\n")
            name = action_dict.get("name", "?")
            data = action_dict.get("data", {})
            if name == "ACTION6":
                f.write(f"Tool Call: {name}({json.dumps(data)})\n")
            else:
                f.write(f"Tool Call: {name}({{}})\n")
