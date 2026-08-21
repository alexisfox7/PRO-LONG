"""Shared prompt, history, and action parsing for the agent backends."""

import json
import logging
import re
import shutil

from prolong_agent.agent.action_queue import VALID_ACTIONS
from prolong_agent.agent.prompts import (
    ASCII_COLOR_MAP,
    HEX_COLOR_MAP,
    INPROMPT_INITIAL_PROMPT,
    INPROMPT_RESUME_PROMPT,
    MCP_NO_LOG_INITIAL_PROMPT,
    MCP_NO_LOG_RESUME_PROMPT,
    MCP_NO_LOG_SYSTEM_PROMPT,
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_INPROMPT,
    format_actions_block,
)
from prolong_agent.agent.memory import MemoryMode

log = logging.getLogger(__name__)

DEFAULT_ACTIONS = [
    "ACTION1", "ACTION2", "ACTION3", "ACTION4",
    "ACTION5", "ACTION6", "ACTION7", "RESET",
]


class BaseAgent:
    _ACTION6_RE = re.compile(r'^ACTION6\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)$')

    def __init__(
        self,
        grid_mode="hex",
        log_window=None,
        action_cap=20,
        workspace="/workspace",
        memory_mode: MemoryMode | str | None = None,
    ):
        self._grid_mode = grid_mode
        self._log_window = log_window
        self._memory_mode = MemoryMode(memory_mode) if memory_mode else (
            MemoryMode.IN_PROMPT if log_window == -1
            else MemoryMode.WINDOWED_LOG if log_window is not None
            else MemoryMode.FULL_LOG
        )
        self._action_cap = max(1, int(action_cap))
        self._workspace = workspace

    def _workspace_text(self, text):
        if self._workspace == ".":
            return text.replace("/workspace/", "./").replace("/workspace", ".")
        return text

    def _build_system_prompt(self, available_actions=None):
        if self._memory_mode == MemoryMode.MCP_NO_LOG:
            return self._workspace_text(
                MCP_NO_LOG_SYSTEM_PROMPT.format(action_cap=self._action_cap)
                + (HEX_COLOR_MAP if self._grid_mode == "hex" else ASCII_COLOR_MAP)
            )
        template = SYSTEM_PROMPT_INPROMPT if self._memory_mode == MemoryMode.IN_PROMPT else SYSTEM_PROMPT
        available_actions = available_actions or DEFAULT_ACTIONS

        if self._log_window is None:
            history = "It contains the full game history."
        elif self._log_window > 0:
            history = f"It contains the last {self._log_window} action sections."
        else:
            history = ""

        has_history = self._log_window is None or (self._log_window or 0) > 0
        cross_turn = ""
        if has_history:
            cross_turn = (
                " Cross-turn parsing (diffs between distant boards, greps of a "
                "fixed cell across board sections) is tractable and can be useful "
                "for understanding mechanics, including long-horizon ones."
            )

        prompt = template.format(
            action_cap=self._action_cap,
            actions_section=format_actions_block(available_actions),
            log_window_desc=history,
            cross_turn_hint=cross_turn,
        )
        prompt += HEX_COLOR_MAP if self._grid_mode == "hex" else ASCII_COLOR_MAP
        return self._workspace_text(prompt)

    def _build_prompt(self, log_name, is_first, **values):
        if self._memory_mode == MemoryMode.MCP_NO_LOG:
            return self._workspace_text(
                MCP_NO_LOG_INITIAL_PROMPT if is_first else MCP_NO_LOG_RESUME_PROMPT
            )
        if self._memory_mode == MemoryMode.IN_PROMPT:
            board = values.get("board_text", "") or "(board unavailable)"
            if is_first:
                prompt = INPROMPT_INITIAL_PROMPT.format(board=board)
            else:
                prompt = INPROMPT_RESUME_PROMPT.format(
                    score=values.get("score", 0),
                    action_num=values.get("action_num", 0),
                    level=values.get("level", 1),
                    last_actions=values.get("last_actions", "none"),
                    board=board,
                )
            return self._workspace_text(prompt)

        log_path = f"{self._workspace}/{log_name}"
        if self._log_window is None:
            description = f"Read the full game log at {log_path}"
        else:
            description = f"Read {log_path} (last {self._log_window} actions)."

        if is_first:
            return (
                f"{description}\n\nThis is the first analysis. Analyze the board "
                f"state and write {self._workspace}/actions.json with your first set of actions."
            )
        body = (
            "Recent actions and boards are at the end of the log; what changed "
            "since the last call (new moves, score transitions, plan adherence) "
            f"can be informative. Check {self._workspace}/ for anything you saved "
            f"previously, then write a new {self._workspace}/actions.json."
        )
        return f"{description}\n\n{body}"

    def _sync_history(self, log_path, sandbox):
        if self._memory_mode in (MemoryMode.IN_PROMPT, MemoryMode.MCP_NO_LOG):
            return
        destination = sandbox / log_path.name
        if self._log_window is not None:
            self._copy_truncated_log(log_path, destination, self._log_window)
            return
        previous_size = destination.stat().st_size if destination.exists() else 0
        with open(log_path, "rb") as source, open(destination, "ab") as output:
            source.seek(previous_size)
            shutil.copyfileobj(source, output)

    def _add_current_board(self, log_path, values):
        if self._memory_mode != MemoryMode.IN_PROMPT or values.get("board_text"):
            return
        board_file = log_path.parent / "current_board.txt"
        if not board_file.exists():
            return
        board_text = board_file.read_text(errors="replace")
        match = re.search(r'\[CURRENT BOARD STATE\]\n(.*)', board_text, re.DOTALL)
        values["board_text"] = match.group(1).rstrip() if match else board_text

    @staticmethod
    def _available_actions(values):
        actions = values.get("available_actions_list")
        if actions:
            return actions
        text = values.get("available_actions", "")
        return [action.strip() for action in text.split(",") if action.strip()] or None

    @staticmethod
    def _clear_files(sandbox, *names):
        for name in names:
            path = sandbox / name
            if path.exists():
                try:
                    path.unlink()
                except OSError:
                    pass

    @staticmethod
    def _purge_interactive_game_artifacts(sandbox):
        """Remove state-bearing artifacts before every MCP-backed CLI call."""
        for filename in ("logs.txt", "current_board.txt"):
            for path in sandbox.rglob(filename):
                try:
                    path.unlink()
                except OSError:
                    pass
        BaseAgent._clear_files(sandbox, "actions.json", "last_message.txt")

    @staticmethod
    def _split_response(text):
        if "\n[PLAN]\n" not in text:
            return text, text
        hint, plan = text.split("\n[PLAN]\n", 1)
        return hint.strip(), plan.strip()

    @staticmethod
    def _copy_truncated_log(source, destination, window):
        text = source.read_text()
        parts = re.split(r'(?=={80}\n)', text)
        truncated = parts[0] + "".join(parts[-window:] if len(parts) > window else parts[1:])
        destination.write_text(truncated)

    @classmethod
    def _parse_actions_json_text(cls, raw, cap=20):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as error:
            log.warning("actions.json malformed: %s", error)
            return []
        entries = value.get("actions") if isinstance(value, dict) else value
        if not isinstance(entries, list):
            log.warning("actions.json: expected list under 'actions' (got %s)", type(entries).__name__)
            return []
        actions = []
        for entry in entries[:cap]:
            action = cls._parse_action_entry(entry)
            if action is not None:
                actions.append(action)
        return actions

    @classmethod
    def _parse_action_entry(cls, entry):
        if isinstance(entry, dict):
            name = entry.get("action", "")
            if name in VALID_ACTIONS:
                return {"name": name, "data": {key: value for key, value in entry.items() if key != "action"}}
            return None
        if isinstance(entry, str):
            entry = entry.strip()
            match = cls._ACTION6_RE.match(entry)
            if match:
                return {"name": "ACTION6", "data": {"x": int(match.group(1)), "y": int(match.group(2))}}
            if entry in VALID_ACTIONS:
                return {"name": entry, "data": {}}
            log.warning("actions.json: skipping unrecognized entry: %s", entry)
        return None
