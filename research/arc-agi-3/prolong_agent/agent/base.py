"""BaseAgent: shared behavior across analyzer backends.

Concentrates code that was duplicated across CodexAgent and ClaudeCodeAgent:
  * actions.json parsing (agent writes an actions.json the runner reads).
  * Log-window truncation helper.
"""
from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from .action_queue import VALID_ACTIONS

log = logging.getLogger(__name__)


class BaseAgent(ABC):

    BACKEND_ID: str = "base"

    # ----- Log window truncation -------------------------------------

    _FRAME_BLOCK_RE = re.compile(
        r'^\[frame \d+/\d+\]\n(?:[^\n]*\n)+?(?=^\[frame \d+/\d+\]|^\[settled\]|^$)',
        re.MULTILINE,
    )

    @classmethod
    def _strip_animation_frames(cls, text: str) -> str:
        out = cls._FRAME_BLOCK_RE.sub("", text)
        out = re.sub(r'^\[settled\]\n', '', out, flags=re.MULTILINE)
        return out

    @staticmethod
    def _copy_truncated_log(src: Path, dest: Path, window: int) -> None:
        text = src.read_text()
        parts = re.split(r'(?=={80}\n)', text)
        if window == 0:
            truncated = parts[0] + (parts[-1] if len(parts) > 1 else "")
            truncated = BaseAgent._strip_animation_frames(truncated)
        else:
            truncated = parts[0] + "".join(
                parts[-window:] if len(parts) > window else parts[1:]
            )
        dest.write_text(truncated)

    # ----- actions.json parsing --------------------------------------

    _ACTION6_RE = re.compile(r'^ACTION6\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)$')

    @classmethod
    def _parse_actions_json_text(cls, raw: str, cap: int = 15) -> list[dict]:
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            log.warning("actions.json malformed: %s", e)
            return []
        entries = obj.get("actions") if isinstance(obj, dict) else obj
        if not isinstance(entries, list):
            log.warning(
                "actions.json: expected list under 'actions' (got %s)",
                type(entries).__name__,
            )
            return []
        actions: list[dict] = []
        for entry in entries[:cap]:
            parsed = cls._parse_action_entry(entry)
            if parsed is not None:
                actions.append(parsed)
        return actions

    @classmethod
    def _parse_action_entry(cls, entry: Any) -> Optional[dict]:
        if isinstance(entry, dict):
            name = entry.get("action", "")
            if name in VALID_ACTIONS:
                return {
                    "name": name,
                    "data": {k: v for k, v in entry.items() if k != "action"},
                }
            return None
        if isinstance(entry, str):
            s = entry.strip()
            m = cls._ACTION6_RE.match(s)
            if m:
                return {
                    "name": "ACTION6",
                    "data": {"x": int(m.group(1)), "y": int(m.group(2))},
                }
            if s in VALID_ACTIONS:
                return {"name": s, "data": {}}
            log.warning("actions.json: skipping unrecognized entry: %s", s)
        return None

    # ----- Abstract API ----------------------------------------------

    @abstractmethod
    def _build_system_prompt(self) -> str: ...

    @abstractmethod
    def _build_prompt(self, *args: Any, **kwargs: Any) -> str: ...

    @abstractmethod
    def analyze(self, log_path: Path, action_num: int,
                retry_nudge: str = "", **kwargs: Any) -> Optional[dict[str, Any]]: ...
