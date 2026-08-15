"""ClaudeCodeAgent: runs Claude Code CLI (-p) inside Docker for game analysis.

The first call creates a session via --session-id and later calls resume it
via --resume. Claude Code's native auto-compaction manages context growth.
Session data persists in cc_sessions/ on the host.

Auth: uses CLAUDE_CODE_OAUTH_TOKEN (Claude Max subscription) by default.
Pass use_api_key=True to use ANTHROPIC_API_KEY instead.
"""
from __future__ import annotations
from prolong_agent.utils import sandbox_net

import atexit
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from prolong_agent.agent.base import BaseAgent
from prolong_agent.agent.prompts import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_INPROMPT,
    INPROMPT_INITIAL_PROMPT,
    INPROMPT_RESUME_PROMPT,
    HEX_COLOR_MAP,
    ASCII_COLOR_MAP,
)

log = logging.getLogger(__name__)

from prolong_agent.agent.action_queue import VALID_ACTIONS as _VALID_ACTIONS

_DOCKER_IMAGE = os.environ.get("CLAUDE_DOCKER_IMAGE", "prolong-agent/claude-sandbox:latest")


class _ContainerPool:
    """Manages persistent Docker containers with /workspace bind-mounted."""

    def __init__(self, run_label: str = "", oauth_token: Optional[str] = None,
                 compact_pct: Optional[int] = None,
                 use_api_key: bool = False) -> None:
        self._run_label = run_label
        self._oauth_token = oauth_token
        self._compact_pct = compact_pct
        self._use_api_key = use_api_key
        self._containers: dict[str, dict] = {}
        self._lock = threading.Lock()

    def get(self, key: str, workspace_dir: str) -> str:
        with self._lock:
            if key in self._containers:
                info = self._containers[key]
                check = subprocess.run(
                    ["docker", "inspect", "-f", "{{.State.Running}}", info["name"]],
                    capture_output=True, text=True, timeout=5,
                )
                if check.returncode == 0 and "true" in check.stdout.lower():
                    return info["name"]
                log.warning("container %s died, recreating", info["name"])
                subprocess.run(["docker", "rm", "-f", info["name"]],
                               capture_output=True, timeout=10)
                del self._containers[key]
            return self._create(key, workspace_dir)

    def _create(self, key: str, workspace_dir: str) -> str:
        name = f"cc_{uuid.uuid4().hex[:12]}"

        env_flags: list[str] = []
        if self._use_api_key:
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
            if api_key:
                env_flags.extend(["-e", f"ANTHROPIC_API_KEY={api_key}"])
            else:
                log.warning("use_api_key=True but ANTHROPIC_API_KEY not set")
        else:
            oauth = self._oauth_token or os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
            if oauth:
                env_flags.extend(["-e", f"CLAUDE_CODE_OAUTH_TOKEN={oauth}"])
            else:
                for key_name in ("ANTHROPIC_API_KEY",):
                    val = os.environ.get(key_name)
                    if val:
                        env_flags.extend(["-e", f"{key_name}={val}"])

        label_flags = [
            "--label", "app=prolong-agent",
            "--label", "backend=claude-code",
            "--label", f"game={key}",
        ]
        if self._run_label:
            label_flags.extend(["--label", f"run={self._run_label}"])

        sessions_dir = Path(workspace_dir).parent / "cc_sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        # Secure by default: internal docker network + anthropic allowlist
        # proxy. Opt out with CLAUDE_DOCKER_NETWORK=host (or bridge: "").
        _net = os.environ.get("CLAUDE_DOCKER_NETWORK", sandbox_net.INTERNAL_NETWORK)
        _proxy = os.environ.get("CLAUDE_EGRESS_PROXY",
                                "http://prolong-anthropic-proxy:3128"
                                if _net == sandbox_net.INTERNAL_NETWORK else "")
        if _net == sandbox_net.INTERNAL_NETWORK:
            sandbox_net.ensure_secure_network(
                "prolong-anthropic-proxy", "prolong-anthropic-proxy", "docker/anthropic-proxy")
        net_flags: list[str] = ["--network", _net] if _net else []
        if _proxy:
            for _v in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                       "http_proxy", "https_proxy", "all_proxy"):
                net_flags += ["-e", f"{_v}={_proxy}"]
            net_flags += ["-e", "NO_PROXY=localhost,127.0.0.1",
                          "-e", "no_proxy=localhost,127.0.0.1"]

        cmd = [
            "docker", "run", "-d",
            "--name", name,
            "--entrypoint", "sleep",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges:true",
            "--memory=8g", "--cpus=4",
            "--tmpfs", "/tmp:rw,nosuid,size=256m",
            *net_flags,
            "-v", f"{os.path.realpath(workspace_dir)}:/workspace:rw",
            "-v", f"{os.path.realpath(sessions_dir)}:/home/sandbox/.claude:rw",
            "-e", "HOME=/home/sandbox",
            "-e", "DISABLE_AUTOUPDATER=1",
            "-e", "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1",
            *((["-e", f"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE={self._compact_pct}"]
               if self._compact_pct is not None else [])),
            *env_flags,
            *label_flags,
            _DOCKER_IMAGE,
            "infinity",
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
        self._containers[key] = {"name": name}
        log.info("claude-code container ready: %s", name)
        return name

    def cleanup(self) -> None:
        with self._lock:
            for info in self._containers.values():
                try:
                    subprocess.run(["docker", "stop", "-t", "3", info["name"]],
                                   capture_output=True, timeout=10)
                    subprocess.run(["docker", "rm", "-f", info["name"]],
                                   capture_output=True, timeout=10)
                except Exception as e:
                    log.warning("cleanup %s failed: %s", info["name"], e)
            self._containers.clear()


class _ClaudeCodeEventParser:
    """Parses stream-json (JSONL) events from ``claude -p --output-format stream-json --verbose``."""

    PHASE_WAITING = "waiting"
    PHASE_LLM = "llm"
    PHASE_TOOL_RUNNING = "tool_running"
    PHASE_DONE = "done"

    def __init__(self, f) -> None:
        self._f = f
        self.accumulated_text: str = ""
        self.session_id: Optional[str] = None

        self.total_cost_usd: float = 0.0
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.cache_read_tokens: int = 0
        self.cache_creation_tokens: int = 0

        self.terminal_error: Optional[str] = None

        self._lock = threading.Lock()
        self.last_event_ts: float = time.monotonic()
        self.phase: str = self.PHASE_WAITING
        self.current_tool: Optional[str] = None
        self.current_tool_started: Optional[float] = None
        self.tool_calls: list[tuple[str, float]] = []
        self.commands: list[str] = []
        self.step_count: int = 0
        self.compaction_count: int = 0
        self.cumulative_output_tokens: int = 0
        self.cumulative_tool_result_chars: int = 0

    def _write(self, label: str, content: str) -> None:
        if content:
            self._f.write(f"[{label}]\n{content}\n\n")
            self._f.flush()

    def _mark_event(self, new_phase: Optional[str] = None) -> None:
        with self._lock:
            self.last_event_ts = time.monotonic()
            if new_phase is not None:
                self.phase = new_phase

    def snapshot_state(self) -> tuple[str, float, Optional[str]]:
        now = time.monotonic()
        with self._lock:
            return self.phase, now - self.last_event_ts, self.current_tool

    def handle(self, event: dict) -> None:
        etype = event.get("type", "")

        if etype == "system":
            sid = event.get("session_id")
            if sid:
                self.session_id = sid
            subtype = event.get("subtype", "")
            if subtype == "compact_boundary":
                self.compaction_count += 1
                self._write("COMPACTION",
                    f"#{self.compaction_count} at step {self.step_count}, "
                    f"cumulative_out={self.cumulative_output_tokens}, "
                    f"tool_chars={self.cumulative_tool_result_chars}")
            self._mark_event(self.PHASE_LLM)

        elif etype == "assistant":
            msg = event.get("message", {}) or {}
            content_blocks = msg.get("content", []) or []
            for block in content_blocks:
                btype = block.get("type", "")
                if btype == "text":
                    text = block.get("text", "")
                    if text:
                        self.accumulated_text += text
                    self._mark_event(self.PHASE_LLM)
                elif btype == "tool_use":
                    name = block.get("name", "unknown")
                    inp = block.get("input", {})
                    with self._lock:
                        self.current_tool = name
                        self.current_tool_started = time.monotonic()
                    self._mark_event(self.PHASE_TOOL_RUNNING)
                    if isinstance(inp, dict):
                        inp_str = json.dumps(inp, indent=2)
                        cmd = inp.get("command") or inp.get("cmd") or ""
                        if isinstance(cmd, str) and cmd.strip():
                            self.commands.append(cmd.strip()[:200])
                    else:
                        inp_str = str(inp)
                    self._write(f"TOOL USE: {name}", inp_str[:2000])
                elif btype == "thinking":
                    self._mark_event(self.PHASE_LLM)

            self.step_count += 1
            out_tokens = (msg.get('usage', {}) or {}).get('output_tokens', 0)
            self.cumulative_output_tokens += out_tokens

        elif etype == "user":
            msg = event.get("message", {}) or {}
            content_blocks = msg.get("content", []) or []
            for block in content_blocks:
                btype = block.get("type", "")
                if btype == "tool_result":
                    content = block.get("content", "")
                    if isinstance(content, list):
                        content = "\n".join(
                            b.get("text", str(b)) if isinstance(b, dict) else str(b)
                            for b in content
                        )
                    content = str(content)
                    self.cumulative_tool_result_chars += len(content)
                    self._write("TOOL RESULT", content[:2000])
                    with self._lock:
                        if self.current_tool_started:
                            duration = time.monotonic() - self.current_tool_started
                        else:
                            duration = 0.0
                        tool_name = self.current_tool or "unknown"
                        self.current_tool = None
                        self.current_tool_started = None
                    self.tool_calls.append((tool_name, duration))
                    self._mark_event(self.PHASE_LLM)

        elif etype == "result":
            cost = event.get("total_cost_usd", 0.0)
            if isinstance(cost, (int, float)):
                self.total_cost_usd = cost
            usage = event.get("usage", {}) or {}
            self.input_tokens = usage.get("input_tokens", 0) or 0
            self.output_tokens = usage.get("output_tokens", 0) or 0
            self.cache_read_tokens = usage.get("cache_read_input_tokens", 0) or 0
            self.cache_creation_tokens = usage.get("cache_creation_input_tokens", 0) or 0
            sid = event.get("session_id")
            if sid:
                self.session_id = sid
            is_error = event.get("is_error", False)
            if is_error:
                self.terminal_error = event.get("subtype", "error")
            self._mark_event(self.PHASE_DONE)

        elif etype == "rate_limit_event":
            self._mark_event()

        else:
            self._mark_event()


class ClaudeCodeAgent(BaseAgent):
    """Runs Claude Code CLI (`claude -p`) inside Docker.

    Returns the same contract as CodexAgent:
        {"hint": str, "plan": str, "actions": list[dict], "cost": float} | None
    """

    BACKEND_ID = "claude-code"

    def __init__(
        self,
        *,
        model: str = "claude-opus-4-6",
        timeout: Optional[int] = None,
        use_api_key: bool = False,
        grid_mode: str = "hex",
        run_label: str = "",
        log_window: Optional[int] = None,
        effort: str = "high",
        oauth_token: Optional[str] = None,
        extra_system_prompt: Optional[str] = None,
        compact_pct: Optional[int] = None,
        action_cap: int = 15,
        user_prompt_prepend: Optional[str] = None,
        user_prompt_inject_every: Optional[int] = None,
    ) -> None:
        self._model = model
        self._timeout = timeout or 2400
        self._effort = effort
        self._oauth_token = oauth_token
        self._use_api_key = use_api_key
        self._grid_mode = grid_mode
        self._run_label = run_label
        self._log_window = log_window
        self._compact_pct = compact_pct
        self._action_cap = max(1, int(action_cap))
        self._user_prompt_prepend = (user_prompt_prepend or "").strip() or None
        self._user_prompt_inject_every = user_prompt_inject_every if user_prompt_inject_every and user_prompt_inject_every > 0 else None
        self._last_user_inject_bucket: dict[str, int] = {}
        self._extra_system_prompt = (extra_system_prompt or "").strip() or None
        self._call_count: dict[str, int] = {}
        self._session_ids: dict[str, str] = {}

        self.total_estimated_cost: float = 0.0
        self.total_calls: int = 0

        self._pool = _ContainerPool(run_label=run_label, oauth_token=oauth_token,
                                    compact_pct=compact_pct,
                                    use_api_key=use_api_key)
        atexit.register(self._pool.cleanup)

    def _session_args(self, path_key: str) -> tuple[list[str], str, bool]:
        session_id = self._session_ids.get(path_key)
        if session_id:
            return ["--resume", session_id], session_id, True
        session_id = str(uuid.uuid4())
        self._session_ids[path_key] = session_id
        return ["--session-id", session_id], session_id, False

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
        if self._grid_mode == "hex":
            sp += HEX_COLOR_MAP
        else:
            sp += ASCII_COLOR_MAP
        return sp

    def _build_prompt(self, log_name: str, is_first: bool, **kwargs) -> str:
        if self._log_window == -1:
            board_text = kwargs.get("board_text", "") or "(board unavailable)"
            if is_first:
                return INPROMPT_INITIAL_PROMPT.format(board=board_text)
            return INPROMPT_RESUME_PROMPT.format(
                score=kwargs.get("score", 0),
                action_num=kwargs.get("action_num", 0),
                level=kwargs.get("level", 1),
                last_actions=kwargs.get("last_actions", "none"),
                board=board_text,
            )
        log_path = f"/workspace/{log_name}"
        if self._log_window is None:
            log_desc = f"Read the full game log at {log_path}"
        elif self._log_window == 0:
            log_desc = f"Read {log_path} (current board only; no action history)."
        else:
            log_desc = f"Read {log_path} (last {self._log_window} actions)."

        if is_first:
            return (
                f"{log_desc}\n\nThis is the first analysis. Analyze the board "
                "state and write /workspace/actions.json with your first set of actions."
            )
        if self._log_window == 0:
            body = (
                "Compare the current board to your notes in the workspace. "
                "Focus on what changed and whether your previous plan made "
                "progress. Check /workspace/ for anything you saved previously. "
                "Update your briefing and write a new /workspace/actions.json."
            )
        else:
            body = (
                "Recent actions and boards are at the end of the log; what "
                "changed since the last call (new moves, score transitions, "
                "plan adherence) can be informative. Check /workspace/ for "
                "anything you saved previously, then write a new "
                "/workspace/actions.json."
            )
        return f"{log_desc}\n\n{body}"

    # -- Quota-exhaustion detection -----------------------------------------
    _QUOTA_RE = re.compile(
        r"(?:out of (?:extra )?usage|usage limit)"
        r".*?resets?\s+(\d{1,2}:\d{2}\s*(?:am|pm))\s*\(UTC\)",
        re.IGNORECASE | re.DOTALL,
    )

    @staticmethod
    def _parse_quota_reset(text):
        m = ClaudeCodeAgent._QUOTA_RE.search(text)
        if not m and "out of" in text.lower() and "usage" in text.lower():
            return 30 * 60
        if not m:
            return None
        from datetime import datetime, timezone, timedelta
        reset_str = m.group(1).strip()
        now_utc = datetime.now(timezone.utc)
        for fmt in ("%I:%M%p", "%I:%M %p"):
            try:
                reset_time = datetime.strptime(reset_str, fmt).replace(
                    year=now_utc.year, month=now_utc.month, day=now_utc.day,
                    tzinfo=timezone.utc,
                )
                break
            except ValueError:
                continue
        else:
            return 30 * 60
        if reset_time <= now_utc:
            reset_time += timedelta(days=1)
        wait = (reset_time - now_utc).total_seconds() + 60
        return min(wait, 6 * 3600)

    def analyze(self, log_path: Path, action_num: int, retry_nudge: str = "",
                **kwargs) -> Optional[dict[str, Any]]:
        if not log_path.exists():
            return None

        path_key = str(log_path)
        is_first = path_key not in self._call_count
        self._call_count[path_key] = self._call_count.get(path_key, 0) + 1

        sandbox = log_path.parent / "cc_sandbox"
        sandbox.mkdir(parents=True, exist_ok=True)
        container = self._pool.get(path_key, str(sandbox.resolve()))

        if self._log_window != -1:
            if self._log_window is not None:
                self._copy_truncated_log(log_path, sandbox / log_path.name,
                                         self._log_window)
            else:
                dest = sandbox / log_path.name
                prev_size = dest.stat().st_size if dest.exists() else 0
                with open(log_path, "rb") as fsrc, open(dest, "ab") as fdst:
                    fsrc.seek(prev_size)
                    shutil.copyfileobj(fsrc, fdst)
        if self._log_window == -1:
            board_file = log_path.parent / "current_board.txt"
            if board_file.exists():
                _bt = board_file.read_text(errors='replace')
                _board_match = re.search(r'\[CURRENT BOARD STATE\]\n(.*)',
                                         _bt, re.DOTALL)
                kwargs.setdefault('board_text',
                                  _board_match.group(1).rstrip() if _board_match else _bt)

        avail_actions_list = kwargs.get("available_actions_list")
        if not avail_actions_list:
            _avail_str = kwargs.get("available_actions", "")
            if _avail_str:
                avail_actions_list = [a.strip() for a in _avail_str.split(",") if a.strip()]
        claude_md = sandbox / "CLAUDE.md"
        claude_md.write_text(self._build_system_prompt(avail_actions_list))

        stale = sandbox / "actions.json"
        if stale.exists():
            stale.unlink()

        prompt = self._build_prompt(log_path.name, is_first,
                                    action_num=action_num, **kwargs)
        if retry_nudge:
            prompt += f"\n\n{retry_nudge}"

        injection_file = sandbox / ".first_turn_injection.txt"
        pending_sentinel = sandbox / ".pending_injection"
        if pending_sentinel.exists() and not injection_file.exists():
            import time as _time
            start = _time.time()
            deadline = start + 15 * 60
            log.info("pending analyst injection detected — waiting (max 15 min)")
            while pending_sentinel.exists() and not injection_file.exists() and _time.time() < deadline:
                _time.sleep(1.0)
            waited = _time.time() - start
            log.info("pending injection wait: %.1fs (injection_ready=%s)",
                     waited, injection_file.exists())
            pending_sentinel.unlink(missing_ok=True)
        if injection_file.exists():
            injection_text = injection_file.read_text().strip()
            if injection_text:
                prompt = injection_text + "\n\n" + prompt
                log.info("injected first-turn prompt (%d chars) from %s",
                         len(injection_text), injection_file.name)
            injection_file.unlink()

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

        cmd = [
            "docker", "exec", "-i",
            "-w", "/workspace",
            container,
            "claude", "-p", "-",
            "--model", self._model,
            "--permission-mode", "bypassPermissions",
            "--effort", self._effort,
            "--max-turns", "50",
            "--output-format", "stream-json",
            "--verbose",
            "--disallowedTools", "Agent,Task,TodoWrite,ToolSearch,WebSearch,WebFetch,mcp__*,NotebookEdit,AskUserQuestion,Skill,ScheduleWakeup,CronCreate,CronDelete,CronList,EnterPlanMode,ExitPlanMode,EnterWorktree,ExitWorktree",
        ]

        if self._extra_system_prompt:
            cmd.extend(["--append-system-prompt", self._extra_system_prompt])

        session_args, session_id, resuming = self._session_args(path_key)
        cmd.extend(session_args)

        analyzer_log = log_path.parent / (log_path.stem + "_analyzer.txt")
        mode_label = f"{'resume' if resuming else 'new'}={session_id}"
        with open(analyzer_log, "a", encoding="utf-8") as f:
            f.write(f"\n--- action={action_num} | "
                    f"{datetime.now().strftime('%H:%M:%S')} | claude-code ---\n")
            if is_first or retry_nudge:
                f.write(f"[USER PROMPT]\n{prompt}\n\n")
            f.flush()

        log.info("analyzer: model=%s, session=%s (claude -p stream-json)",
                 self._model, mode_label)

        call_started = time.monotonic()
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            try:
                proc.stdin.write(prompt)
                proc.stdin.close()
            except BrokenPipeError:
                pass

            stderr_lines: list[str] = []

            def drain_stderr() -> None:
                for line in proc.stderr:
                    stderr_lines.append(line.rstrip("\n"))

            stderr_thread = threading.Thread(target=drain_stderr, daemon=True)
            stderr_thread.start()

            with open(analyzer_log, "a", encoding="utf-8") as f:
                parser = _ClaudeCodeEventParser(f)
                deadline = time.monotonic() + self._timeout
                killed_after_done = False

                heartbeat_stop = threading.Event()

                def heartbeat() -> None:
                    while not heartbeat_stop.wait(30.0):
                        phase, since, tool = parser.snapshot_state()
                        elapsed = time.monotonic() - call_started
                        if since > 30.0:
                            if phase == parser.PHASE_TOOL_RUNNING:
                                reason = f"tool={tool} still running"
                            elif phase == parser.PHASE_LLM:
                                reason = "LLM generating (or stalled)"
                            elif phase == parser.PHASE_WAITING:
                                reason = "waiting for first event"
                            else:
                                reason = f"phase={phase}"
                            log.warning(
                                "HEARTBEAT action=%d: no event for %.0fs "
                                "(call_elapsed=%.0fs phase=%s) — %s",
                                action_num, since, elapsed, phase, reason,
                            )

                heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
                heartbeat_thread.start()

                try:
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        if time.monotonic() > deadline:
                            proc.kill()
                            f.write("[TIMEOUT]\n")
                            log.warning("timed out at action %d", action_num)
                            return None
                        line = line.rstrip("\n")
                        if not line.strip():
                            continue
                        try:
                            parser.handle(json.loads(line))
                        except json.JSONDecodeError:
                            f.write(f"[RAW] {line}\n")

                        if parser.phase == parser.PHASE_DONE:
                            log.info("action=%d result received — breaking readline loop", action_num)
                            killed_after_done = True
                            proc.kill()
                            break

                    proc.wait()
                    stderr_thread.join(timeout=5)
                finally:
                    heartbeat_stop.set()

                response_text = parser.accumulated_text.strip()
                f.write(f"[ASSISTANT]\n{response_text}\n\n")

                stderr_text = "\n".join(stderr_lines).strip()
                if stderr_text:
                    f.write(f"[STDERR]\n{stderr_text[:2000]}\n\n")

                call_duration = time.monotonic() - call_started

                self.total_estimated_cost += parser.total_cost_usd
                self.total_calls += 1

                tool_summary = ", ".join(
                    f"{name}({dur:.1f}s)" for name, dur in parser.tool_calls
                ) or "none"
                compact_str = f" compactions={parser.compaction_count}" if parser.compaction_count else ""
                f.write(
                    f"[TIMING] {call_duration:.1f}s rc={proc.returncode} "
                    f"cost=${parser.total_cost_usd:.4f} "
                    f"tokens(in={parser.input_tokens} out={parser.output_tokens} "
                    f"cache_read={parser.cache_read_tokens} "
                    f"cache_create={parser.cache_creation_tokens}) "
                    f"cumulative(out={parser.cumulative_output_tokens} "
                    f"tool_chars={parser.cumulative_tool_result_chars})"
                    f"{compact_str} "
                    f"tools=[{tool_summary}]\n\n"
                )

                log.info(
                    "action=%d claude-code: %.1fs, $%.4f, "
                    "in=%d out=%d cache_r=%d cache_w=%d, "
                    "compactions=%d, %d tool calls, "
                    "total_cost=$%.4f",
                    action_num, call_duration, parser.total_cost_usd,
                    parser.input_tokens, parser.output_tokens,
                    parser.cache_read_tokens, parser.cache_creation_tokens,
                    parser.compaction_count,
                    len(parser.tool_calls), self.total_estimated_cost,
                )

            if parser.session_id:
                self._session_ids[path_key] = parser.session_id
                try:
                    self._save_session_state(log_path, parser.session_id, action_num)
                except Exception as exc:
                    log.warning("failed to persist session_state.json: %s", exc)

            genuine_failure = (proc.returncode != 0 and not killed_after_done) or not response_text
            if genuine_failure:
                log.warning("action=%d: claude -p failed rc=%d stderr=%s",
                            action_num, proc.returncode,
                            stderr_text[:200] if stderr_text else "")
                return None

            _quota_wait = self._parse_quota_reset(response_text)
            if _quota_wait is not None:
                log.warning(
                    "QUOTA EXHAUSTED at action=%d -- sleeping %.0f min until reset",
                    action_num, _quota_wait / 60,
                )
                time.sleep(_quota_wait)
                log.info("quota sleep done -- retrying analyze() for action=%d", action_num)
                return self.analyze(log_path, action_num, retry_nudge=retry_nudge, **kwargs)

            actions = self._read_actions_json(container, action_num, log_path)

            hint = response_text
            plan = response_text
            if "\n[PLAN]\n" in response_text:
                hint, plan = response_text.split("\n[PLAN]\n", 1)
                hint, plan = hint.strip(), plan.strip()

            log.info("action=%d OK (%d chars, %d actions, %.1fs)",
                     action_num, len(response_text), len(actions),
                     call_duration)

            return {
                "hint": hint,
                "plan": plan,
                "actions": actions,
                "cost": self.total_estimated_cost,
                "meta": {
                    "output": response_text,
                    "input_tokens": parser.input_tokens,
                    "cached_tokens": parser.cache_read_tokens,
                    "output_tokens": parser.output_tokens,
                    "reasoning_tokens": 0,
                    "call_cost_usd": parser.total_cost_usd,
                    "commands": list(parser.commands),
                    "model": self._model,
                },
            }

        except Exception as e:
            log.error("claude-code agent error: %s", e, exc_info=True)
            return None
        finally:
            try:
                subprocess.run(
                    ["docker", "exec", container, "sh", "-c",
                     "pkill -9 -f 'python3|bash -c' 2>/dev/null || true"],
                    timeout=5, capture_output=True,
                )
            except Exception:
                pass

    def _read_actions_json(self, container: str, action_num: int,
                           log_path: Path) -> list[dict]:
        try:
            check = subprocess.run(
                ["docker", "exec", container, "test", "-f", "/workspace/actions.json"],
                capture_output=True, timeout=5,
            )
            if check.returncode != 0:
                log.debug("action=%d: no actions.json found", action_num)
                return []

            cat = subprocess.run(
                ["docker", "exec", container, "cat", "/workspace/actions.json"],
                capture_output=True, text=True, timeout=5,
            )
            if cat.returncode != 0 or not cat.stdout.strip():
                log.warning("actions.json empty or unreadable")
                return []

            alog = log_path.parent / (log_path.stem + "_analyzer.txt")
            with open(alog, "a", encoding="utf-8") as f:
                f.write(f"\n[ACTIONS.JSON]\n{cat.stdout}\n")

            cap = self._action_cap
            actions = self._parse_actions_json_text(cat.stdout, cap=cap)
            log.info("actions.json produced %d actions (cap=%d)", len(actions), cap)
            return actions

        except Exception as e:
            log.warning("actions.json read error: %s", e)
            return []
