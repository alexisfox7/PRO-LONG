"""BaseAgent: shared behavior across analyzer backends.

Concentrates code that was duplicated across CodexAgent and ClaudeCodeAgent:
  * Session state persistence (session_state.json next to logs.txt).
  * actions.json parsing (agent writes an actions.json the runner reads).
  * Log-window truncation helper.
"""
from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .action_queue import VALID_ACTIONS

log = logging.getLogger(__name__)


def _utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class BaseAgent(ABC):

    BACKEND_ID: str = "base"

    # ----- Session state persistence ---------------------------------

    @staticmethod
    def _session_state_path(log_path: Path) -> Path:
        return log_path.parent / "session_state.json"

    def _save_session_state(self, log_path: Path, session_id: str,
                            action_num: int) -> None:
        state_path = self._session_state_path(log_path)
        payload = {
            "backend": self.BACKEND_ID,
            "session_id": session_id,
            "last_action": action_num,
            "mtime": _utc_now_iso_z(),
        }
        tmp = state_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(payload, indent=2))
        tmp.replace(state_path)

    @classmethod
    def _load_session_state(cls, log_path: Path) -> Optional[dict]:
        state_path = cls._session_state_path(log_path)
        if not state_path.exists():
            return None
        try:
            return json.loads(state_path.read_text())
        except Exception as exc:
            log.warning("could not parse %s: %s", state_path, exc)
            return None

    def prime_session_from_disk(self, log_path: Path) -> Optional[str]:
        state = self._load_session_state(log_path)
        if not state:
            return None
        recorded = state.get("backend")
        if recorded and recorded != self.BACKEND_ID:
            log.warning(
                "resume: session_state backend=%s mismatches agent=%s — "
                "starting fresh", recorded, self.BACKEND_ID,
            )
            return None
        sid = state.get("session_id")
        if not sid:
            return None
        path_key = str(log_path)
        self._session_ids[path_key] = sid
        self._call_count[path_key] = state.get("last_action", 1) or 1
        log.info(
            "resume: restored %s session %s for %s (last_action=%s)",
            self.BACKEND_ID, sid, log_path.name, state.get("last_action"),
        )
        return sid

    # ----- External session reset ------------------------------------

    def clear_session(self, log_path: Path, reason: str = "external") -> bool:
        path_key = str(log_path)
        had = path_key in self._session_ids
        self._session_ids.pop(path_key, None)
        if not hasattr(self, "_cleared_paths"):
            self._cleared_paths: set[str] = set()
        self._cleared_paths.add(path_key)
        log.info("clear_session: backend=%s log=%s reason=%s had_session=%s",
                 self.BACKEND_ID, log_path.name, reason, had)
        return had

    def consume_clear_tombstone(self, log_path: Path) -> bool:
        if not hasattr(self, "_cleared_paths"):
            return False
        path_key = str(log_path)
        if path_key in self._cleared_paths:
            self._cleared_paths.discard(path_key)
            return True
        return False

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
