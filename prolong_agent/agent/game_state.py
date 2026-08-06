"""GameState: grid processing and action recording for the game runner."""
from __future__ import annotations

import logging
from typing import Any

from arcengine import GameAction
from prolong_agent.utils.grid_utils import format_grid_ascii

log = logging.getLogger(__name__)


class GameState:
    """Tracks game state: last observation, grid rendering, and hint injection."""

    def __init__(self, *, grid_mode: str = "hex", **_: Any) -> None:
        self._grid_mode = grid_mode
        self.reset()

    def reset(self) -> None:
        self.last_observation: dict[str, Any] | None = None
        self.last_executed_action: str | None = None
        self._external_hint: str | None = None
        self._persistent_hint: str | None = None

    def set_external_hint(self, hint: str) -> None:
        """One-shot strategic hint injected into the log as [PLAN]."""
        self._external_hint = hint
        self._persistent_hint = None

    def set_persistent_hint(self, plan: str) -> None:
        """Plan that persists in the log until the next analysis."""
        self._persistent_hint = plan

    def process_frame(self, obs: dict) -> tuple[list[list[int]], str]:
        """Extract the settled grid from an observation and render it as text."""
        frame_3d = obs.get("frame", [])
        grid_raw = [list(row) for row in frame_3d[-1]] if frame_3d else []
        return grid_raw, format_grid_ascii(grid_raw, mode=self._grid_mode) if grid_raw else ""

    def render_board(self, include_animation: bool = True) -> str | None:
        """Render the current board. If include_animation is False, only the settled grid."""
        obs = self.last_observation or {}
        frame_3d = obs.get("frame", [])
        if not frame_3d:
            return None
        if len(frame_3d) == 1 or not include_animation:
            grid_raw = [list(row) for row in frame_3d[-1]]
            text = format_grid_ascii(grid_raw, mode=self._grid_mode)
            return text if text else None
        parts = []
        for i, layer in enumerate(frame_3d[:-1]):
            grid_raw = [list(row) for row in layer]
            parts.append(f"[frame {i+1}/{len(frame_3d)-1}]")
            parts.append(format_grid_ascii(grid_raw, mode=self._grid_mode))
        grid_raw = [list(row) for row in frame_3d[-1]]
        parts.append("[settled]")
        parts.append(format_grid_ascii(grid_raw, mode=self._grid_mode))
        return "\n".join(parts)

    def consume_hint_block(self) -> str:
        """Return and clear any pending [PLAN] block for the log."""
        if self._external_hint:
            block = f"\n[PLAN]\n{self._external_hint}\n"
            self._external_hint = None
            return block
        elif self._persistent_hint:
            return f"\n[PLAN]\n{self._persistent_hint}\n"
        return ""

    def record_env_update(self, observation: Any, reward: float, done: bool, info: dict = None) -> None:
        """Store the latest observation from the environment."""
        self.last_observation = observation

    def record_action(self, action_dict: dict) -> dict:
        """Convert an action dict to the GameAction payload for env.step()."""
        action_name = action_dict["name"]
        self.last_executed_action = action_name

        action = GameAction.from_name(action_name)
        reasoning = action_dict.get("action_metadata")
        if reasoning is None:
            reasoning = f"Action: {action_name}"
        result = {"action": action, "reasoning": reasoning}
        if action == GameAction.ACTION6:
            x_pos = max(0, min(63, int(action_dict["data"].get("x", 0))))
            y_pos = max(0, min(63, int(action_dict["data"].get("y", 0))))
            result["x"] = x_pos
            result["y"] = y_pos
        return result
