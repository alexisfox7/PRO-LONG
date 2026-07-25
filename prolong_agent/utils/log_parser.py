"""Parse executed actions from a game logs.txt file for --resume replay."""
from __future__ import annotations

import json
import re
from pathlib import Path


_ACTION_HEADER_RE = re.compile(
    r"^Action\s+(\d+)\s*\|\s*Level\s+(\d+)\s*\|\s*Attempt\s+(\d+)"
)
_TOOL_CALL_RE = re.compile(r"^Tool Call:\s+([A-Z0-9_]+)\s*\((\{.*\})\)\s*$")


def parse_actions_from_log(log_path: Path) -> list[dict]:
    actions: list[dict] = []
    current_action_idx: int | None = None
    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.rstrip("\n")
            header = _ACTION_HEADER_RE.match(line)
            if header:
                idx = int(header.group(1))
                current_action_idx = idx if idx > 0 else None
                continue
            if current_action_idx is None:
                continue
            m = _TOOL_CALL_RE.match(line)
            if not m:
                continue
            name = m.group(1)
            try:
                data = json.loads(m.group(2)) if m.group(2).strip() != "{}" else {}
            except json.JSONDecodeError:
                data = {}
            actions.append({"index": current_action_idx, "name": name, "data": data})
            current_action_idx = None
    actions.sort(key=lambda a: a["index"])
    return [{"name": a["name"], "data": a["data"], "index": a["index"]} for a in actions]


def last_action_index(log_path: Path) -> int:
    last = 0
    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            m = _ACTION_HEADER_RE.match(raw.rstrip("\n"))
            if m:
                idx = int(m.group(1))
                if idx > last:
                    last = idx
    return last
