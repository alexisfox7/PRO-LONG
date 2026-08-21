"""Shared ARC game-session state for queued and interactive runners."""

from __future__ import annotations

import json
import logging
import os
import shlex
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import requests
from arcengine import GameState as ArcGameState

from prolong_agent.agent.game_state import GameState
from prolong_agent.environment import BaseEnv
from prolong_agent.metrics.structures import AttemptMetrics, GameMetrics, LevelMetrics, Status
from prolong_agent.utils import action_metadata

log = logging.getLogger(__name__)

ROOT_URL = os.environ.get("ROOT_URL", "https://three.arcprize.org")
MAX_RETRIES = 5
INITIAL_BACKOFF = 1

ACTION_NAMES = {
    0: "RESET", 1: "ACTION1", 2: "ACTION2", 3: "ACTION3",
    4: "ACTION4", 5: "ACTION5", 6: "ACTION6", 7: "ACTION7",
}
_SECRET_OPTIONS = {"--claude-token"}


def _safe_command(argv: list[str]) -> str:
    redacted: list[str] = []
    hide_next = False
    for arg in argv:
        if hide_next:
            redacted.append("[REDACTED]")
            hide_next = False
        elif arg in _SECRET_OPTIONS:
            redacted.append(arg)
            hide_next = True
        elif any(arg.startswith(f"{option}=") for option in _SECRET_OPTIONS):
            redacted.append(f"{arg.split('=', 1)[0]}=[REDACTED]")
        else:
            redacted.append(arg)
    return shlex.join(redacted)


def run_with_retries(func: Callable, *args: Any, **kwargs: Any) -> Any:
    retries = 0
    backoff = INITIAL_BACKOFF
    while True:
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if retries >= MAX_RETRIES:
                log.error("Final attempt failed for %s after %d retries.", func.__name__, retries)
                raise
            log.warning("%s failed; retrying in %ds (%d/%d)",
                        func.__name__, backoff, retries + 1, MAX_RETRIES)
            time.sleep(backoff)
            retries += 1
            backoff *= 2


@dataclass(frozen=True)
class ActionOutcome:
    score_changed: bool
    state: ArcGameState
    exhausted: bool


class GameSessionController:
    """Own the live environment, private trace, action budget, and metrics."""

    def __init__(
        self,
        *,
        env: BaseEnv,
        game_id: str,
        agent_name: str,
        max_actions: int,
        run_index: int = 1,
        tags: list[str] | None = None,
        trace_path: Path | None = None,
        log_post_board: bool = False,
        grid_mode: str = "hex",
    ) -> None:
        self.env = env
        self.game_id = game_id
        self.max_actions = max_actions
        self.tags = tags
        self.trace_path = trace_path
        self.log_post_board = log_post_board
        self.grid_mode = grid_mode
        self.state = GameState(grid_mode=grid_mode)
        self.metrics = GameMetrics(
            game_id=game_id,
            agent_name=agent_name,
            run_index=run_index,
            start_time=time.time(),
        )
        self.metrics.status = Status.IN_PROGRESS
        self.level_num = 1
        self.level_metrics = LevelMetrics(level_number=1)
        self.attempt_num = 1
        self.attempt_metrics = AttemptMetrics(attempt_number=1)
        self.attempt_start = self.metrics.start_time
        self.total_actions = 0
        self.max_score = 0
        self.arc_score = 0
        self.arc_state = ArcGameState.NOT_PLAYED
        self.available_action_names: list[str] = ["RESET"]
        self.usage = {"calls": 0, "in": 0, "out": 0, "cache_read": 0, "cost": 0.0}
        self._last_action: dict[str, Any] = {}
        self._finalized = False

    @property
    def observation(self) -> dict[str, Any]:
        board = self.state.render_board(include_animation=False) or ""
        return {
            "game_id": self.game_id,
            "state": "PLAYING" if self.arc_state == ArcGameState.NOT_FINISHED else self.arc_state.name,
            "score": self.arc_score,
            "level": self.level_num,
            "action_num": self.total_actions,
            "max_actions": self.max_actions,
            "remaining_actions": max(0, self.max_actions - self.total_actions),
            "available_actions": list(self.available_action_names),
            "grid_mode": self.grid_mode,
            "board": board.splitlines(),
        }

    @property
    def exhausted(self) -> bool:
        return self.total_actions >= self.max_actions

    @property
    def won(self) -> bool:
        return self.arc_state == ArcGameState.WIN

    def start(self) -> dict[str, Any]:
        self.state.reset()
        if self.trace_path:
            self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        observation = run_with_retries(
            self.env.reset,
            task={"game_id": self.game_id, "max_actions": self.max_actions, "tags": self.tags},
        )
        self._record_observation(observation)
        self._record_run_info(observation)
        if self.trace_path:
            self.trace_path.write_text("")
            grid = self.state.render_board()
            if grid:
                with self.trace_path.open("a", encoding="utf-8") as output:
                    output.write(f"{'=' * 80}\n")
                    output.write(
                        f"Action 0 | Level 1 | Attempt 1 | INITIAL STATE | Score: {self.arc_score}\n\n"
                    )
                    output.write(f"[INITIAL BOARD STATE]\n{grid}\n\n")
        return self.observation

    def record_usage(self, meta: dict[str, Any] | None) -> dict[str, Any] | None:
        if not meta:
            return None
        meta = dict(meta)
        input_tokens = meta.get("input_tokens", 0) or 0
        output_tokens = meta.get("output_tokens", 0) or 0
        cached_tokens = meta.get("cached_tokens", 0) or 0
        if meta.get("cumulative", False):
            meta["input_tokens"] = max(0, input_tokens - self.usage["in"])
            meta["output_tokens"] = max(0, output_tokens - self.usage["out"])
            meta["cached_tokens"] = max(0, cached_tokens - self.usage["cache_read"])
            self.usage["in"] = input_tokens
            self.usage["out"] = output_tokens
            self.usage["cache_read"] = cached_tokens
        else:
            self.usage["in"] += input_tokens
            self.usage["out"] += output_tokens
            self.usage["cache_read"] += cached_tokens
        self.usage["calls"] += 1
        self.usage["cost"] += meta.get("call_cost_usd", 0.0) or 0.0
        return meta

    def execute_action(self, action: dict[str, Any]) -> ActionOutcome:
        if self.exhausted:
            raise RuntimeError("action budget exhausted")
        previous_score = self.arc_score
        action_result = self.state.record_action(action)
        self._last_action = action
        observation, _, _ = run_with_retries(self.env.step, action_result)
        self.total_actions += 1
        self.attempt_metrics.actions += 1
        self._record_observation(observation)
        self.metrics.highest_level_reached = max(
            self.metrics.highest_level_reached, self.level_num
        )
        self._log_action()

        score_changed = self.arc_score != previous_score
        if self.arc_score > self.max_score:
            self.max_score = self.arc_score

        if score_changed and self.arc_state not in (ArcGameState.WIN, ArcGameState.GAME_OVER):
            self._complete_level()
        elif self.arc_state == ArcGameState.GAME_OVER:
            self._complete_attempt_game_over()
        elif self.arc_state == ArcGameState.WIN:
            self._complete_win()

        return ActionOutcome(score_changed, self.arc_state, self.exhausted)

    def build_action_metadata(
        self,
        action: dict[str, Any],
        *,
        output: str,
        step: int,
        total: int,
        model: str = "",
    ) -> str:
        name = action.get("name", "?")
        data = action.get("data", {})
        action_text = (
            f"ACTION6({data.get('x', 0)},{data.get('y', 0)})" if name == "ACTION6" else name
        )
        payload = action_metadata.build(
            output=output,
            plan={"step": f"{step}/{total}", "action": action_text},
            aggregate={
                "agent_calls": self.usage["calls"],
                "actions": self.total_actions + 1,
                "input_tokens": self.usage["in"],
                "output_tokens": self.usage["out"],
                "cache_read_tokens": self.usage["cache_read"],
                "cost_usd": round(self.usage["cost"], 4),
            },
            model=model,
        )
        return json.dumps(payload, separators=(",", ":"))

    def set_stalled(self) -> None:
        self.metrics.status = Status.AGENT_STALLED

    def finalize(self) -> GameMetrics:
        if self._finalized:
            return self.metrics
        self._finalized = True
        now = time.time()
        self.metrics.end_time = now
        self.metrics.run_duration_seconds = now - self.metrics.start_time

        if self.attempt_metrics.status == Status.IN_PROGRESS:
            self.attempt_metrics.duration_seconds = now - self.attempt_start
            if self.metrics.status == Status.ERROR:
                self.attempt_metrics.status = Status.ERROR
            elif self.arc_state == ArcGameState.WIN:
                self.attempt_metrics.status = Status.COMPLETED
                self.metrics.status = Status.COMPLETED_RUN
            else:
                self.attempt_metrics.status = Status.TIMEOUT
                if self.metrics.status == Status.IN_PROGRESS:
                    self.metrics.status = Status.TIMEOUT

        if (
            not self.level_metrics.attempts
            or self.level_metrics.attempts[-1].attempt_number != self.attempt_metrics.attempt_number
        ):
            self.level_metrics.attempts.append(self.attempt_metrics)
        if self.level_metrics.status == Status.IN_PROGRESS:
            self.level_metrics.status = self.attempt_metrics.status
        self.metrics.level_metrics[self.level_num] = self.level_metrics
        self.metrics.run_total_actions = sum(
            level.total_actions for level in self.metrics.level_metrics.values()
        )
        self.metrics.total_game_overs_across_run = sum(
            level.total_game_overs for level in self.metrics.level_metrics.values()
        )
        self.metrics.total_state_changes_across_run = sum(
            level.total_state_changes for level in self.metrics.level_metrics.values()
        )
        self.metrics.final_score = self.max_score
        return self.metrics

    def _record_observation(self, observation: dict[str, Any]) -> None:
        self.state.record_env_update(observation)
        self.arc_state = ArcGameState[observation.get("state") or "NOT_PLAYED"]
        self.arc_score = observation.get("score", 0) or 0
        raw_actions = observation.get("available_actions", [])
        self.available_action_names = sorted(
            {ACTION_NAMES.get(value, f"ACTION{value}") for value in raw_actions} | {"RESET"}
        )

    def _record_run_info(self, observation: dict[str, Any]) -> None:
        guid = observation.get("guid")
        if not guid:
            return
        self.metrics.guid = guid
        self.metrics.replay_url = f"{ROOT_URL}/replay/{self.game_id}/{guid}"
        if not self.trace_path:
            return
        note = ""
        for index, arg in enumerate(sys.argv):
            if arg == "--note" and index + 1 < len(sys.argv):
                note = sys.argv[index + 1]
        info_path = self.trace_path.parent / "run_info.txt"
        info_path.write_text(
            (f"note: {note}\n" if note else "")
            + f"game_id: {self.game_id}\n"
            f"guid: {guid}\n"
            f"replay_url: {self.metrics.replay_url}\n"
            f"scorecard_id: {getattr(self.env, '_scorecard_id', 'unknown')}\n"
            f"command: {_safe_command([Path(sys.argv[0]).name, *sys.argv[1:]])}\n"
        )

    def _complete_level(self) -> None:
        self.attempt_metrics.duration_seconds = time.time() - self.attempt_start
        self.attempt_metrics.status = Status.COMPLETED
        self.level_metrics.attempts.append(self.attempt_metrics)
        self.level_metrics.status = Status.COMPLETED
        self.metrics.level_metrics[self.level_num] = self.level_metrics
        self.level_num += 1
        self.metrics.highest_level_reached = max(
            self.metrics.highest_level_reached, self.level_num
        )
        self.level_metrics = LevelMetrics(level_number=self.level_num)
        self.attempt_num = 1
        self.attempt_metrics = AttemptMetrics(attempt_number=1)
        self.attempt_start = time.time()

    def _complete_attempt_game_over(self) -> None:
        self.attempt_metrics.duration_seconds = time.time() - self.attempt_start
        self.attempt_metrics.status = Status.GAME_OVER
        self.attempt_metrics.game_overs += 1
        self.level_metrics.attempts.append(self.attempt_metrics)
        self.level_metrics.status = Status.GAME_OVER
        self.metrics.level_metrics[self.level_num] = self.level_metrics
        self.metrics.status = Status.TIMEOUT
        self.attempt_num += 1
        self.attempt_metrics = AttemptMetrics(attempt_number=self.attempt_num)
        self.attempt_start = time.time()

    def _complete_win(self) -> None:
        self.attempt_metrics.duration_seconds = time.time() - self.attempt_start
        self.attempt_metrics.status = Status.COMPLETED
        self.level_metrics.attempts.append(self.attempt_metrics)
        self.level_metrics.status = Status.COMPLETED
        self.metrics.level_metrics[self.level_num] = self.level_metrics
        self.metrics.status = Status.COMPLETED_RUN

    def _log_action(self) -> None:
        if not self.trace_path:
            return
        action = self._last_action
        with self.trace_path.open("a", encoding="utf-8") as output:
            output.write(f"\n{'=' * 80}\n")
            step = action.get("plan_step")
            plan = f" | Plan Step {step}" if step else ""
            output.write(
                f"Action {self.total_actions} | Level {self.level_num} | "
                f"Attempt {self.attempt_num}{plan} | Score: {self.arc_score}\n\n"
            )
            hint = self.state.consume_hint_block()
            if hint:
                output.write(f"{hint}\n")
            name = action.get("name", "?")
            data = action.get("data", {})
            output.write(
                f"Tool Call: {name}({json.dumps(data) if name == 'ACTION6' else '{}'})\n"
            )
            if self.log_post_board:
                grid = self.state.render_board()
                if grid:
                    output.write(f"[POST-ACTION BOARD STATE]\n{grid}\n\n")
