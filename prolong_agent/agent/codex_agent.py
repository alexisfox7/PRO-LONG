"""CodexAgent: runs OpenAI Codex CLI inside Docker to produce action plans."""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, IO, Optional

from prolong_agent.utils import sandbox_net

from prolong_agent.agent.action_queue import VALID_ACTIONS
from prolong_agent.agent.prompts import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_INPROMPT,
    INPROMPT_INITIAL_PROMPT,
    INPROMPT_RESUME_PROMPT,
    HEX_COLOR_MAP,
    ASCII_COLOR_MAP,
)

log = logging.getLogger(__name__)

_DEFAULT_REASONING_EFFORT = "none"


def _utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Stream parser for nd-JSON events from `codex exec --json`
# ---------------------------------------------------------------------------

class _CodexEventParser:

    PHASE_WAITING_API = "waiting_for_llm"
    PHASE_LLM_STREAMING = "llm_streaming"
    PHASE_TOOL_RUNNING = "tool_running"
    PHASE_POST_TOOL = "post_tool_wait"
    PHASE_DONE = "done"

    def __init__(self, f: IO[str]) -> None:
        self._f = f

        self.accumulated_text: str = ""
        self.session_id: Optional[str] = None

        self.last_tokens_total: Optional[int] = None
        self.last_tokens_input: Optional[int] = None
        self.last_tokens_output: Optional[int] = None
        self.last_tokens_cache_read: Optional[int] = None
        self.last_tokens_cache_write: Optional[int] = None

        self.overflow_error: Optional[str] = None
        self.terminal_error: Optional[str] = None

        self._lock = threading.Lock()
        self._start_ts: float = time.monotonic()
        self.last_event_ts: float = self._start_ts
        self.phase: str = self.PHASE_WAITING_API
        self.current_tool: Optional[str] = None
        self.current_tool_started: Optional[float] = None

        self.step_count: int = 0
        self.tool_calls: list[tuple[str, float]] = []
        self.commands: list[str] = []

    def _write(self, label: str, content: str) -> None:
        if content:
            self._f.write(f"[{label}]\n{content}\n\n")
            self._f.flush()

    def _mark_event(self, new_phase: Optional[str] = None) -> float:
        now = time.monotonic()
        with self._lock:
            elapsed = now - self.last_event_ts
            self.last_event_ts = now
            if new_phase is not None:
                self.phase = new_phase
        return elapsed

    def snapshot_state(self) -> tuple[str, float, Optional[str]]:
        now = time.monotonic()
        with self._lock:
            return self.phase, now - self.last_event_ts, self.current_tool

    def handle(self, event: dict) -> None:
        etype = event.get("type", "")

        if etype == "thread.started":
            tid = event.get("thread_id")
            if tid and not self.session_id:
                self.session_id = tid
            self._mark_event(self.PHASE_LLM_STREAMING)

        elif etype == "turn.started":
            self.step_count += 1
            gap = self._mark_event(self.PHASE_LLM_STREAMING)
            if gap > 15.0 and self.step_count > 1:
                log.warning(
                    "codex turn.started arrived after %.1fs wait (step=%d, phase was %s). "
                    "Likely LLM API latency or rate limit queueing.",
                    gap, self.step_count, self.PHASE_POST_TOOL,
                )

        elif etype == "item.started":
            item = event.get("item", {}) or {}
            itype = item.get("type", "")
            if itype == "command_execution":
                name = "bash"
                cmd = item.get("command", "")
                with self._lock:
                    self.current_tool = name
                    self.current_tool_started = time.monotonic()
                    self.phase = self.PHASE_TOOL_RUNNING
                self._mark_event(self.PHASE_TOOL_RUNNING)
                self._write(f"TOOL USE: {name}", cmd[:2000])
                if isinstance(cmd, str) and cmd.strip():
                    self.commands.append(cmd.strip()[:200])
            elif itype == "file_change":
                with self._lock:
                    self.current_tool = "apply_patch"
                    self.current_tool_started = time.monotonic()
                    self.phase = self.PHASE_TOOL_RUNNING
                self._mark_event(self.PHASE_TOOL_RUNNING)
                self._write("TOOL USE: apply_patch", json.dumps(item, indent=2)[:2000])

        elif etype == "item.completed":
            item = event.get("item", {}) or {}
            itype = item.get("type", "")
            if itype == "agent_message":
                text = item.get("text", "") or ""
                if text:
                    self.accumulated_text += text
                    self._write("ASSISTANT", text)
                self._mark_event()
            elif itype == "command_execution":
                cmd = item.get("command", "") or ""
                out = item.get("aggregated_output", "") or item.get("output", "") or ""
                exit_code = item.get("exit_code")
                is_error = isinstance(exit_code, int) and exit_code != 0
                label = "TOOL ERROR" if is_error else "TOOL RESULT"
                self._write(label, str(out)[:4000])
                with self._lock:
                    if self.current_tool_started:
                        duration = time.monotonic() - self.current_tool_started
                    else:
                        duration = 0.0
                self.tool_calls.append((self.current_tool or "bash", duration))
                if duration > 10.0:
                    log.warning(
                        "slow codex tool '%s' took %.1fs (exit=%s, out=%d chars)",
                        self.current_tool or "bash", duration, exit_code, len(str(out)),
                    )
                with self._lock:
                    self.current_tool = None
                    self.current_tool_started = None
                    self.phase = self.PHASE_POST_TOOL
                self._mark_event(self.PHASE_POST_TOOL)
            elif itype == "file_change":
                changes = item.get("changes", []) or []
                summary = f"{len(changes)} file change(s)"
                self._write("TOOL RESULT", summary)
                with self._lock:
                    if self.current_tool_started:
                        duration = time.monotonic() - self.current_tool_started
                    else:
                        duration = 0.0
                self.tool_calls.append(("apply_patch", duration))
                with self._lock:
                    self.current_tool = None
                    self.current_tool_started = None
                    self.phase = self.PHASE_POST_TOOL
                self._mark_event(self.PHASE_POST_TOOL)
            elif itype == "reasoning":
                self._mark_event()

        elif etype == "turn.completed":
            usage = event.get("usage", {}) or {}
            input_tokens = usage.get("input_tokens")
            cached = usage.get("cached_input_tokens")
            output_tokens = usage.get("output_tokens")
            if input_tokens is not None and output_tokens is not None:
                self.last_tokens_input = input_tokens
                self.last_tokens_output = output_tokens
                self.last_tokens_total = input_tokens + output_tokens
                self.last_tokens_cache_read = cached or 0
                self.last_tokens_cache_write = 0
            self._mark_event(self.PHASE_DONE)

        elif etype == "error":
            msg = event.get("message", "") or event.get("error", "")
            if isinstance(msg, dict):
                name = msg.get("name", "UnknownError")
                text = msg.get("message", str(msg))
            else:
                name = "CodexError"
                text = str(msg)
            self._write(f"ERROR: {name}", text)
            self.terminal_error = name
            lmsg = text.lower()
            lname = name.lower()
            is_overflow = (
                "overflow" in lname
                or "too long" in lmsg
                or ("context" in lmsg and ("length" in lmsg or "limit" in lmsg or "window" in lmsg))
                or ("maximum" in lmsg and "tokens" in lmsg)
            )
            if is_overflow:
                self.overflow_error = name
                log.error(
                    "OVERFLOW from codex: %s: %s — model context window "
                    "exceeded. Codex has no native compaction; the session "
                    "must be restarted.",
                    name, text,
                )
                self.session_id = None
            else:
                log.error("codex error: %s: %s", name, text)


class CodexAgent:
    """Analyzer that runs OpenAI Codex CLI inside Docker for each analyze() call."""

    BACKEND_ID = "codex"

    _DOCKER_IMAGE = os.environ.get(
        "CODEX_DOCKER_IMAGE", "rgb-agent/codex-sandbox:latest"
    )

    def __init__(
        self,
        *,
        model: str = "gpt-5.4",
        reasoning_effort: str = _DEFAULT_REASONING_EFFORT,
        timeout: Optional[int] = None,
        grid_mode: str = "hex",
        run_label: str = "",
        log_window: Optional[int] = None,
        codex_home: Optional[str] = None,
        session_mode: str = "resume",
        clear_every: int = 15,
        clear_every_actions: Optional[int] = None,
        action_cap: int = 15,
        extra_system_prompt: Optional[str] = None,
        user_prompt_prepend: Optional[str] = None,
        user_prompt_inject_every: Optional[int] = None,
        workspace: str = "persistent",
    ) -> None:
        if workspace not in {"persistent", "stateless"}:
            raise ValueError(f"workspace must be persistent/stateless, got {workspace!r}")
        self._workspace = workspace
        self._model = model
        self._reasoning_effort = reasoning_effort
        self._timeout = timeout
        self._grid_mode = grid_mode
        self._run_label = run_label
        self._log_window = log_window
        if session_mode not in {"resume", "fresh", "reprime", "clear", "summary"}:
            raise ValueError(f"session_mode must be resume/fresh/reprime/clear/summary, got {session_mode!r}")
        self._session_mode = session_mode
        self._clear_every = clear_every
        self._clear_every_actions = clear_every_actions
        self._last_clear_bucket: dict[str, int] = {}
        self._action_cap = max(1, int(action_cap))
        self._codex_home = (
            Path(codex_home).expanduser().resolve()
            if codex_home else Path(os.path.expanduser("~/.codex"))
        )
        self._call_count: dict[str, int] = {}
        self._session_ids: dict[str, str] = {}
        self._extra_system_prompt = (extra_system_prompt or "").strip() or None
        self._user_prompt_prepend = (user_prompt_prepend or "").strip() or None
        self._user_prompt_inject_every = user_prompt_inject_every if user_prompt_inject_every and user_prompt_inject_every > 0 else None
        self._last_user_inject_bucket: dict[str, int] = {}

        self.total_estimated_cost: float = 0.0
        self.total_calls: int = 0

        self._sandbox_lock = threading.Lock()

    def _get_sandbox(self, log_path: Path) -> Path:
        sandbox = log_path.parent / "codex_sandbox"
        with self._sandbox_lock:
            sandbox.mkdir(parents=True, exist_ok=True)
            try:
                os.chown(sandbox, 1000, 1000)
            except (PermissionError, OSError):
                pass
        return sandbox

    # --- Session persistence -----------------------------------------------

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

    def consume_clear_tombstone(self, log_path: Path) -> bool:
        if not hasattr(self, "_cleared_paths"):
            return False
        path_key = str(log_path)
        if path_key in self._cleared_paths:
            self._cleared_paths.discard(path_key)
            return True
        return False

    # --- Log truncation ----------------------------------------------------

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
            truncated = CodexAgent._strip_animation_frames(truncated)
        else:
            truncated = parts[0] + "".join(
                parts[-window:] if len(parts) > window else parts[1:]
            )
        dest.write_text(truncated)

    # --- actions.json parsing ----------------------------------------------

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
            log.warning("actions.json: expected list under 'actions' (got %s)",
                        type(entries).__name__)
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
                return {"name": name, "data": {k: v for k, v in entry.items() if k != "action"}}
            return None
        if isinstance(entry, str):
            s = entry.strip()
            m = cls._ACTION6_RE.match(s)
            if m:
                return {"name": "ACTION6", "data": {"x": int(m.group(1)), "y": int(m.group(2))}}
            if s in VALID_ACTIONS:
                return {"name": s, "data": {}}
            log.warning("actions.json: skipping unrecognized entry: %s", s)
        return None

    # --- Codex session management ------------------------------------------

    def _find_session_file(self, session_id: str) -> Optional[Path]:
        sessions_root = self._codex_home / "sessions"
        if not sessions_root.exists():
            return None
        matches = list(sessions_root.rglob(f"*{session_id}.jsonl"))
        return matches[0] if matches else None

    def _session_exists_on_disk(self, session_id: str) -> bool:
        return self._find_session_file(session_id) is not None

    def prime_session_from_disk(self, log_path: Path) -> Optional[str]:
        state = self._load_session_state(log_path)
        if not state:
            return None
        recorded = state.get("backend")
        if recorded and recorded != self.BACKEND_ID:
            log.warning("resume: session_state backend=%s mismatches — starting fresh", recorded)
            return None
        sid = state.get("session_id")
        if not sid:
            return None
        if not self._session_exists_on_disk(sid):
            log.warning(
                "resume: codex session %s not found under %s/sessions — starting fresh",
                sid, self._codex_home,
            )
            return None
        path_key = str(log_path)
        self._session_ids[path_key] = sid
        self._call_count[path_key] = state.get("last_action", 1) or 1
        log.info("resume: restored session %s for %s (last_action=%s)",
                 sid, log_path.name, state.get("last_action"))
        return sid

    @staticmethod
    def _truncate_logs_below_level(logs_path: Path, max_level_inclusive: int) -> tuple[int, int]:
        if not logs_path.exists():
            return (0, 0)
        text = logs_path.read_text()
        orig_bytes = logs_path.stat().st_size
        blocks = re.split(r'(?=^={80}\nAction \d+ \| Level \d+ \| Attempt \d+)',
                          text, flags=re.M)
        preamble = blocks[0] if blocks else ""
        kept = [preamble]
        for blk in blocks[1:]:
            m = re.match(r'^={80}\nAction \d+ \| Level (\d+)', blk)
            if m and int(m.group(1)) <= max_level_inclusive:
                kept.append(blk)
        logs_path.write_text("".join(kept))
        return (orig_bytes, logs_path.stat().st_size)

    def clear_session(self, log_path: Path, reason: str = "external") -> bool:
        path_key = str(log_path)
        had = path_key in self._session_ids
        self._session_ids.pop(path_key, None)
        if not hasattr(self, "_cleared_paths"):
            self._cleared_paths: set[str] = set()
        self._cleared_paths.add(path_key)
        log.info("clear_session: log=%s reason=%s had_session=%s", log_path.name, reason, had)
        eval_dir = log_path.parent

        sb = eval_dir / "codex_sandbox"
        wiped = 0
        if sb.exists():
            for f in list(sb.rglob("*")):
                if f.is_file() and f.name != "AGENTS.md":
                    try:
                        f.unlink()
                        wiped += 1
                    except OSError:
                        pass

        logs_path = eval_dir / "logs.txt"
        try:
            orig, new = self._truncate_logs_below_level(logs_path, max_level_inclusive=0)
            if orig > 0:
                log.info(
                    "clear_session: dropped all action history from logs.txt "
                    "(was %d bytes, now %d bytes — preamble only)",
                    orig, new,
                )
        except Exception as exc:
            log.warning("clear_session: logs.txt truncation failed: %s", exc)

        log.info(
            "clear_session: wiped %d sandbox file(s) for %s",
            wiped, log_path.name,
        )
        return had

    def _build_system_prompt(self, available_actions=None) -> str:
        from prolong_agent.agent.prompts import format_actions_block
        cap = self._action_cap
        tmpl = SYSTEM_PROMPT_INPROMPT if self._log_window == -1 else SYSTEM_PROMPT
        if not available_actions:
            available_actions = ["ACTION1", "ACTION2", "ACTION3", "ACTION4",
                                 "ACTION5", "ACTION6", "ACTION7", "RESET"]
        actions_section = format_actions_block(available_actions)
        multi_turn = self._log_window is None or (self._log_window or 0) > 0
        if self._log_window is None:
            log_window_desc = "It contains the full game history."
        elif self._log_window == 0:
            log_window_desc = "It contains only the most recent board state."
        elif self._log_window > 0:
            log_window_desc = f"It contains the last {self._log_window} action sections."
        else:
            log_window_desc = ""
        cross_turn_hint = (
            " Cross-turn parsing (diffs between distant boards, greps of a "
            "fixed cell across board sections) is tractable and can be useful "
            "for understanding mechanics, including long-horizon ones."
        ) if multi_turn else ""
        sp = tmpl.format(action_cap=cap, actions_section=actions_section,
                         log_window_desc=log_window_desc,
                         cross_turn_hint=cross_turn_hint)
        if self._workspace == "stateless":
            # minimal factual swap: workspace doesn't persist + log has no prior [PLAN]s
            sp = sp.replace(
                "**Workspace**: `/workspace/` persists across calls. `actions.json` is cleared "
                "each call; other files accumulate. Feel free to save notes, state, or helper functions.",
                "**Workspace**: `/workspace/` does not persist across calls (i.e., any notes, state, "
                "helper functions do not persist after actions are submitted) — only `logs.txt` carries over.")
            sp = sp.replace("board states, and your own prior analyses.", "board states.")
        if self._grid_mode == "hex":
            sp += HEX_COLOR_MAP
        else:
            sp += ASCII_COLOR_MAP
        # Rewrite /workspace/ to ./ — Codex runs with cwd == sandbox directory.
        sp = sp.replace("/workspace/", "./").replace("/workspace", ".")
        if self._extra_system_prompt:
            sp += "\n\n" + self._extra_system_prompt
        return sp

    def _build_prompt(self, log_name: str, is_first: bool, **kwargs) -> str:
        if self._log_window == -1:
            board_text = kwargs.get("board_text", "") or "(board unavailable)"
            if is_first:
                p = INPROMPT_INITIAL_PROMPT.format(board=board_text)
            else:
                p = INPROMPT_RESUME_PROMPT.format(
                    score=kwargs.get("score", 0),
                    action_num=kwargs.get("action_num", 0),
                    level=kwargs.get("level", 1),
                    last_actions=kwargs.get("last_actions", "none"),
                    board=board_text,
                )
            return p.replace("/workspace/", "./").replace("/workspace", ".")
        log_path_disp = f"./{log_name}"
        if self._log_window is None:
            log_desc = f"Read the full game log at {log_path_disp}"
        elif self._log_window == 0:
            log_desc = f"Read {log_path_disp} (current board only; no action history)."
        else:
            log_desc = f"Read {log_path_disp} (last {self._log_window} actions)."

        if is_first:
            return (
                f"{log_desc}\n\n"
                "This is the first analysis. Analyze the board state and write "
                "./actions.json with your first set of actions."
            )
        else:
            if self._log_window == 0:
                body = (
                    "Compare the current board to your notes in the workspace. "
                    "Focus on what changed and whether your previous plan made "
                    "progress. Check ./ for anything you saved previously. "
                    "Update your briefing and write a new ./actions.json."
                )
            else:
                body = (
                    "Recent actions and boards are at the end of the log; what "
                    "changed since the last call (new moves, score transitions, "
                    "plan adherence) can be informative. Check ./ for anything "
                    "you saved previously, then write a new ./actions.json."
                )
            return f"{log_desc}\n\n{body}"

    def analyze(self, log_path: Path, action_num: int, retry_nudge: str = "",
                **kwargs) -> Optional[dict[str, Any]]:
        if not log_path.exists():
            return None

        path_key = str(log_path)
        is_first = path_key not in self._call_count
        self._call_count[path_key] = self._call_count.get(path_key, 0) + 1

        sandbox = self._get_sandbox(log_path)

        if self._log_window == -1:
            pass
        elif self._log_window is not None:
            self._copy_truncated_log(log_path, sandbox / log_path.name, self._log_window)
        else:
            dest = sandbox / log_path.name
            prev_size = dest.stat().st_size if dest.exists() else 0
            with open(log_path, "rb") as fsrc, open(dest, "ab") as fdst:
                fsrc.seek(prev_size)
                shutil.copyfileobj(fsrc, fdst)

        if self._log_window == -1:
            board_file = log_path.parent / "current_board.txt"
            if board_file.exists():
                _bt = board_file.read_text(errors="replace")
                _board_match = re.search(r'\[CURRENT BOARD STATE\]\n(.*)', _bt, re.DOTALL)
                kwargs.setdefault(
                    "board_text",
                    _board_match.group(1).rstrip() if _board_match else _bt,
                )

        avail_actions_list = kwargs.get("available_actions_list")
        if not avail_actions_list:
            _avail_str = kwargs.get("available_actions", "")
            if _avail_str:
                avail_actions_list = [a.strip() for a in _avail_str.split(",") if a.strip()]
        agents_md = sandbox / "AGENTS.md"
        if not agents_md.exists():
            agents_md.write_text(self._build_system_prompt(avail_actions_list))

        if self._workspace == "stateless":
            # ablation: nothing the agent writes survives the turn boundary — only
            # logs.txt (objective trace) + AGENTS.md (static prompt) persist. Kills
            # self-authored memory files. NOT clear_session (keeps codex conversation
            # + canonical host log intact; within-turn scratch still allowed).
            keep = {"logs.txt", "AGENTS.md"}
            for f in list(sandbox.rglob("*")):
                if f.is_file() and f.name not in keep:
                    try:
                        f.unlink()
                    except OSError:
                        pass
        else:
            for stale in ("actions.json", "last_message.txt"):
                p = sandbox / stale
                if p.exists():
                    try:
                        p.unlink()
                    except OSError:
                        pass

        prompt = self._build_prompt(log_path.name, is_first, action_num=action_num, **kwargs)
        if retry_nudge:
            prompt += f"\n\n{retry_nudge}"

        injection_file = sandbox / ".first_turn_injection.txt"
        if injection_file.exists():
            injection_text = injection_file.read_text().strip()
            if injection_text:
                prompt = injection_text + "\n\n" + prompt
                log.info("injected first-turn prompt (%d chars) from %s",
                         len(injection_text), injection_file.name)

        if self._user_prompt_prepend:
            if self._user_prompt_inject_every:
                bucket = int(action_num) // self._user_prompt_inject_every
                last = self._last_user_inject_bucket.get(path_key, -1)
                if bucket > last:
                    prompt = self._user_prompt_prepend + "\n\n" + prompt
                    self._last_user_inject_bucket[path_key] = bucket
                    log.info("user-prompt injection fired (bucket %d, action_num=%d)", bucket, action_num)
            else:
                prompt = self._user_prompt_prepend + "\n\n" + prompt

        call_num = self._call_count[path_key]

        if self._clear_every_actions is not None:
            cur_bucket = action_num // self._clear_every_actions
            last_bucket = self._last_clear_bucket.get(path_key, 0)
            is_clear_trigger = (
                self._session_mode in {"clear", "summary"}
                and not is_first
                and cur_bucket > last_bucket
            )
            next_call_is_trigger = (
                self._session_mode == "summary"
                and not is_first
                and (action_num + 1) // self._clear_every_actions > cur_bucket
            )
            if is_clear_trigger:
                self._last_clear_bucket[path_key] = cur_bucket
        else:
            is_clear_trigger = (
                self._session_mode in {"clear", "summary"}
                and not is_first
                and call_num % self._clear_every == 0
            )
            next_call_is_trigger = (
                self._session_mode == "summary"
                and not is_first
                and (call_num + 1) % self._clear_every == 0
            )

        if self._session_mode == "fresh" or is_clear_trigger:
            session_id = None
        else:
            session_id = self._session_ids.get(path_key)

        if self._session_mode == "reprime" and not is_first and session_id:
            prompt = f"{self._build_system_prompt()}\n\n---\n\n{prompt}"

        if self._session_mode == "summary":
            if next_call_is_trigger:
                prompt += (
                    "\n\nIMPORTANT: this is the last call before a scheduled "
                    "session reset. In addition to writing actions.json, also write "
                    "SUMMARY.md in the current directory capturing: "
                    "(1) your current theory of the game mechanics, "
                    "(2) hypotheses you've already tested and what actually happened, "
                    "(3) open questions and what to try next. "
                    "The next analyzer call will start with a fresh conversation "
                    "and only this SUMMARY.md plus logs.txt will be visible to it."
                )
            if is_clear_trigger:
                prompt += (
                    "\n\nNOTE: SUMMARY.md in the current directory was written "
                    "by a prior analyzer session about what has been learned. "
                    "Read it first — it's your only link to prior reasoning."
                )
        elif self._session_mode == "clear" and is_clear_trigger:
            log.info("clear-mode reset at call %d (every %d)", call_num, self._clear_every)

        if not is_first and session_id:
            if not self._session_exists_on_disk(session_id):
                log.warning(
                    "action=%d: codex session %s no longer exists on disk — "
                    "dropping stale id",
                    action_num, session_id,
                )
                self._session_ids.pop(path_key, None)
                session_id = None

        common_opts = [
            "--json",
            "--skip-git-repo-check",
            "-o", "/workspace/last_message.txt",
            "-m", self._model,
            "-c", f'model_reasoning_effort="{self._reasoning_effort}"',
        ]
        if not is_first and session_id:
            codex_args = [
                "exec", "resume",
                *common_opts,
                "--dangerously-bypass-approvals-and-sandbox",
                session_id, prompt,
            ]
        else:
            codex_args = [
                "exec",
                *common_opts,
                "-s", "danger-full-access",
                prompt,
            ]

        host_codex = self._codex_home
        # Secure by default: the agent runs on an --internal docker network
        # (no direct internet/host/metadata) and reaches the OpenAI API only
        # through the squid allowlist proxy. The container never talks to the
        # game server (the host-side runner does), so an LLM-only allowlist is
        # sufficient. Opt out with CODEX_DOCKER_NETWORK=host.
        _net = os.environ.get("CODEX_DOCKER_NETWORK", sandbox_net.INTERNAL_NETWORK)
        _proxy = os.environ.get("CODEX_EGRESS_PROXY",
                                "http://rgb-openai-proxy:3128"
                                if _net == sandbox_net.INTERNAL_NETWORK else "")
        if _net == sandbox_net.INTERNAL_NETWORK:
            sandbox_net.ensure_secure_network(
                "rgb-openai-proxy", "rgb-openai-proxy", "docker/openai-proxy")
        net_flags: list[str] = ["--network", _net]
        if _proxy:
            for _v in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                       "http_proxy", "https_proxy", "all_proxy"):
                net_flags += ["-e", f"{_v}={_proxy}"]
            net_flags += ["-e", "NO_PROXY=localhost,127.0.0.1",
                          "-e", "no_proxy=localhost,127.0.0.1"]

        cmd = [
            "docker", "run", "--rm",
            "--user", "1000:1000",
            *net_flags,
            "--memory=8g", "--cpus=4",
            "-w", "/workspace",
            "-v", f"{os.path.realpath(sandbox)}:/workspace:rw",
            "-v", f"{os.path.realpath(host_codex)}:/home/sandbox/.codex:rw",
            "-e", "HOME=/home/sandbox",
        ]
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            log.error("OPENAI_API_KEY not set — codex requires it for authentication")
            return None
        cmd += ["-e", f"OPENAI_API_KEY={api_key}"]
        cmd += [
            self._DOCKER_IMAGE,
            *codex_args,
        ]

        analyzer_log = log_path.parent / (log_path.stem + "_analyzer.txt")
        with open(analyzer_log, "a", encoding="utf-8") as f:
            f.write(f"\n--- action={action_num} | {datetime.now().strftime('%H:%M:%S')} | codex ---\n")
            if is_first or retry_nudge:
                f.write(f"[USER PROMPT]\n{prompt}\n\n")
            f.flush()

        log.info(
            "analyzer: model=%s, resume=%s, session=%s",
            self._model,
            not is_first and session_id is not None,
            session_id or "new",
        )

        call_started = time.monotonic()
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            stderr_lines: list[str] = []

            def drain_stderr() -> None:
                for line in proc.stderr:
                    stderr_lines.append(line.rstrip("\n"))

            stderr_thread = threading.Thread(target=drain_stderr, daemon=True)
            stderr_thread.start()

            with open(analyzer_log, "a", encoding="utf-8") as f:
                parser = _CodexEventParser(f)
                deadline = time.monotonic() + self._timeout if self._timeout else None

                heartbeat_stop = threading.Event()

                def heartbeat() -> None:
                    last_logged_stall = 0.0
                    while not heartbeat_stop.wait(30.0):
                        phase, since, tool = parser.snapshot_state()
                        elapsed = time.monotonic() - call_started
                        if since > 30.0 and since - last_logged_stall > 15.0:
                            if phase == parser.PHASE_TOOL_RUNNING:
                                reason = f"tool={tool} still running"
                            elif phase == parser.PHASE_LLM_STREAMING:
                                reason = "LLM emitting tokens (or stalled mid-stream)"
                            elif phase == parser.PHASE_POST_TOOL:
                                reason = "awaiting next turn after tool result"
                            elif phase == parser.PHASE_WAITING_API:
                                reason = "initial request — waiting for thread.started (API latency)"
                            else:
                                reason = f"phase={phase}"
                            log.warning(
                                "HEARTBEAT action=%d: no event for %.0fs "
                                "(call_elapsed=%.0fs phase=%s) — %s",
                                action_num, since, elapsed, phase, reason,
                            )
                            last_logged_stall = since

                heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
                heartbeat_thread.start()

                try:
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        if deadline and time.monotonic() > deadline:
                            proc.kill()
                            f.write("[TIMEOUT]\n")
                            log.warning("timed out at action %d — clearing session", action_num)
                            self._session_ids.pop(path_key, None)
                            return None
                        line = line.rstrip("\n")
                        if not line.strip():
                            continue
                        try:
                            parser.handle(json.loads(line))
                        except json.JSONDecodeError:
                            f.write(f"[RAW] {line}\n")

                    proc.wait()
                    stderr_thread.join(timeout=5)
                finally:
                    heartbeat_stop.set()

            if parser.session_id:
                if self.consume_clear_tombstone(log_path):
                    log.info(
                        "action=%d: session writeback skipped — cleared mid-call (sid=%s)",
                        action_num, parser.session_id,
                    )
                else:
                    self._session_ids[path_key] = parser.session_id
                    try:
                        self._save_session_state(log_path, parser.session_id, action_num)
                    except Exception as exc:
                        log.warning("failed to persist session_state.json: %s", exc)
            elif not is_first:
                tail = " | ".join(
                    line for line in stderr_lines[-5:] if line.strip()
                )
                log.warning(
                    "action=%d: codex session dropped (no thread.started event, "
                    "rc=%s, stderr_tail=%r) — next call will start fresh and "
                    "lose accumulated reasoning.",
                    action_num, proc.returncode, tail,
                )
                self._session_ids.pop(path_key, None)

            self.total_calls += 1
            call_duration = time.monotonic() - call_started

            self._log_call_diagnostics(
                action_num=action_num,
                parser=parser,
                session_id=self._session_ids.get(path_key),
                call_duration=call_duration,
                stderr_tail=stderr_lines[-5:],
            )

            if parser.overflow_error:
                log.warning(
                    "action=%d: codex overflow (%s) — session reset, reasoning lost.",
                    action_num, parser.overflow_error,
                )
                return None

            text = parser.accumulated_text.strip()
            if not text:
                last_msg_file = sandbox / "last_message.txt"
                if last_msg_file.exists():
                    text = last_msg_file.read_text().strip()
            if not text:
                log.warning(
                    "action=%d: empty response from codex — clearing session "
                    "(terminal_error=%s, stderr_tail=%s)",
                    action_num, parser.terminal_error,
                    "; ".join(stderr_lines[-3:]) if stderr_lines else "",
                )
                self._session_ids.pop(path_key, None)
                return None

            # Read actions.json written by the agent.
            actions = self._read_actions_json(sandbox, action_num, log_path)

            hint = text
            plan = text
            if "\n[PLAN]\n" in text:
                hint, plan = text.split("\n[PLAN]\n", 1)
                hint, plan = hint.strip(), plan.strip()

            log.info(
                "action=%d OK (%d chars, %d actions)",
                action_num, len(text), len(actions),
            )
            return {
                "hint": hint,
                "plan": plan,
                "actions": actions,
                "cost": self.total_estimated_cost,
                "meta": {
                    "output": text,
                    "input_tokens": parser.last_tokens_input or 0,
                    "cached_tokens": parser.last_tokens_cache_read or 0,
                    "output_tokens": parser.last_tokens_output or 0,
                    "reasoning_tokens": 0,
                    "call_cost_usd": 0.0,
                    "commands": list(parser.commands),
                    "model": self._model,
                    "cumulative": True,
                },
            }

        except Exception as exc:
            log.error("codex error: %s — clearing session", exc, exc_info=True)
            self._session_ids.pop(path_key, None)
            return None

    def _read_actions_json(self, sandbox: Path, action_num: int,
                           log_path: Path) -> list[dict]:
        actions_path = sandbox / "actions.json"
        if not actions_path.exists():
            log.debug("action=%d: no actions.json found", action_num)
            return []
        try:
            raw = actions_path.read_text()
            alog = log_path.parent / (log_path.stem + "_analyzer.txt")
            with open(alog, "a", encoding="utf-8") as f:
                f.write(f"\n[ACTIONS.JSON]\n{raw}\n")
            cap = self._action_cap
            actions = self._parse_actions_json_text(raw, cap=cap)
            log.info("actions.json produced %d actions (cap=%d)",
                     len(actions), cap)
            return actions
        except Exception as exc:
            log.warning("actions.json read failed: %s", exc)
            return []

    def _log_call_diagnostics(
        self,
        *,
        action_num: int,
        parser: "_CodexEventParser",
        session_id: Optional[str],
        call_duration: Optional[float] = None,
        stderr_tail: Optional[list[str]] = None,
    ) -> None:
        et = parser.last_tokens_total
        ei = parser.last_tokens_input
        eo = parser.last_tokens_output
        ec = parser.last_tokens_cache_read

        tool_time_total = sum(d for _, d in parser.tool_calls)
        tool_counts: dict[str, int] = {}
        for name, _ in parser.tool_calls:
            tool_counts[name] = tool_counts.get(name, 0) + 1
        tools_summary = ",".join(f"{n}={c}" for n, c in sorted(tool_counts.items())) or "none"

        if call_duration is not None:
            llm_wait_approx = call_duration - tool_time_total
            timing_str = (
                f"timing=call:{call_duration:.1f}s/tools:{tool_time_total:.1f}s"
                f"/llm_approx:{llm_wait_approx:.1f}s turns={parser.step_count}"
            )
        else:
            timing_str = f"turns={parser.step_count}"

        log.info(
            "codex_stats action=%d session=%s step_tokens=%s/in=%s/out=%s/cache_read=%s "
            "%s tools=[%s]",
            action_num, (session_id or "?")[:20],
            et, ei, eo, ec,
            timing_str, tools_summary,
        )

        if stderr_tail:
            for line in stderr_tail:
                if line.strip():
                    log.debug("codex stderr: %s", line)
