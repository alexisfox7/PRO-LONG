"""Parse JSON events emitted by `codex exec --json`."""

import json
import logging
import threading
import time

log = logging.getLogger(__name__)


class CodexEventParser:
    PHASE_WAITING_API = "waiting_for_llm"
    PHASE_LLM_STREAMING = "llm_streaming"
    PHASE_TOOL_RUNNING = "tool_running"
    PHASE_POST_TOOL = "post_tool_wait"
    PHASE_DONE = "done"

    def __init__(self, output):
        self.output = output
        self.accumulated_text = ""
        self.session_id = None

        self.last_tokens_total = None
        self.last_tokens_input = None
        self.last_tokens_output = None
        self.last_tokens_cache_read = None
        self.last_tokens_cache_write = None

        self.overflow_error = None
        self.terminal_error = None

        self.lock = threading.Lock()
        self.last_event_ts = time.monotonic()
        self.phase = self.PHASE_WAITING_API
        self.current_tool = None
        self.current_tool_started = None

        self.step_count = 0
        self.tool_calls = []
        self.commands = []

    def _write(self, label, content):
        if content:
            self.output.write(f"[{label}]\n{content}\n\n")
            self.output.flush()

    def _mark_event(self, new_phase=None):
        now = time.monotonic()
        with self.lock:
            elapsed = now - self.last_event_ts
            self.last_event_ts = now
            if new_phase is not None:
                self.phase = new_phase
        return elapsed

    def snapshot_state(self):
        with self.lock:
            return self.phase, time.monotonic() - self.last_event_ts, self.current_tool

    def handle(self, event):
        event_type = event.get("type", "")

        if event_type == "thread.started":
            thread_id = event.get("thread_id")
            if thread_id and not self.session_id:
                self.session_id = thread_id
            self._mark_event(self.PHASE_LLM_STREAMING)

        elif event_type == "turn.started":
            self.step_count += 1
            gap = self._mark_event(self.PHASE_LLM_STREAMING)
            if gap > 15.0 and self.step_count > 1:
                log.warning(
                    "codex turn.started arrived after %.1fs wait (step=%d, phase was %s). "
                    "Likely LLM API latency or rate limit queueing.",
                    gap, self.step_count, self.PHASE_POST_TOOL,
                )

        elif event_type == "item.started":
            item = event.get("item", {}) or {}
            item_type = item.get("type", "")
            if item_type == "command_execution":
                command = item.get("command", "")
                with self.lock:
                    self.current_tool = "bash"
                    self.current_tool_started = time.monotonic()
                    self.phase = self.PHASE_TOOL_RUNNING
                self._mark_event(self.PHASE_TOOL_RUNNING)
                self._write("TOOL USE: bash", command[:2000])
                if isinstance(command, str) and command.strip():
                    self.commands.append(command.strip()[:200])
            elif item_type == "file_change":
                with self.lock:
                    self.current_tool = "apply_patch"
                    self.current_tool_started = time.monotonic()
                    self.phase = self.PHASE_TOOL_RUNNING
                self._mark_event(self.PHASE_TOOL_RUNNING)
                self._write("TOOL USE: apply_patch", json.dumps(item, indent=2)[:2000])

        elif event_type == "item.completed":
            item = event.get("item", {}) or {}
            item_type = item.get("type", "")
            if item_type == "agent_message":
                text = item.get("text", "") or ""
                if text:
                    self.accumulated_text += text
                    self._write("ASSISTANT", text)
                self._mark_event()
            elif item_type == "command_execution":
                result = item.get("aggregated_output", "") or item.get("output", "") or ""
                exit_code = item.get("exit_code")
                label = "TOOL ERROR" if isinstance(exit_code, int) and exit_code != 0 else "TOOL RESULT"
                self._write(label, str(result)[:4000])
                with self.lock:
                    duration = time.monotonic() - self.current_tool_started if self.current_tool_started else 0.0
                self.tool_calls.append((self.current_tool or "bash", duration))
                if duration > 10.0:
                    log.warning(
                        "slow codex tool '%s' took %.1fs (exit=%s, out=%d chars)",
                        self.current_tool or "bash", duration, exit_code, len(str(result)),
                    )
                with self.lock:
                    self.current_tool = None
                    self.current_tool_started = None
                    self.phase = self.PHASE_POST_TOOL
                self._mark_event(self.PHASE_POST_TOOL)
            elif item_type == "file_change":
                changes = item.get("changes", []) or []
                self._write("TOOL RESULT", f"{len(changes)} file change(s)")
                with self.lock:
                    duration = time.monotonic() - self.current_tool_started if self.current_tool_started else 0.0
                self.tool_calls.append(("apply_patch", duration))
                with self.lock:
                    self.current_tool = None
                    self.current_tool_started = None
                    self.phase = self.PHASE_POST_TOOL
                self._mark_event(self.PHASE_POST_TOOL)
            elif item_type == "reasoning":
                self._mark_event()

        elif event_type == "turn.completed":
            usage = event.get("usage", {}) or {}
            input_tokens = usage.get("input_tokens")
            output_tokens = usage.get("output_tokens")
            if input_tokens is not None and output_tokens is not None:
                self.last_tokens_input = input_tokens
                self.last_tokens_output = output_tokens
                self.last_tokens_total = input_tokens + output_tokens
                self.last_tokens_cache_read = usage.get("cached_input_tokens") or 0
                self.last_tokens_cache_write = 0
            self._mark_event(self.PHASE_DONE)

        elif event_type == "error":
            message = event.get("message", "") or event.get("error", "")
            if isinstance(message, dict):
                name = message.get("name", "UnknownError")
                text = message.get("message", str(message))
            else:
                name = "CodexError"
                text = str(message)
            self._write(f"ERROR: {name}", text)
            self.terminal_error = name
            lower_text = text.lower()
            lower_name = name.lower()
            is_overflow = (
                "overflow" in lower_name
                or "too long" in lower_text
                or ("context" in lower_text and any(word in lower_text for word in ("length", "limit", "window")))
                or ("maximum" in lower_text and "tokens" in lower_text)
            )
            if is_overflow:
                self.overflow_error = name
                self.session_id = None
                log.error(
                    "OVERFLOW from codex: %s: %s — model context window exceeded. "
                    "Codex has no native compaction; the session must be restarted.",
                    name, text,
                )
            else:
                log.error("codex error: %s: %s", name, text)
