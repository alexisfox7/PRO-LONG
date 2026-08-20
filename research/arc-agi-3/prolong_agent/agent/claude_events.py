"""Parse JSON events emitted by `claude -p --output-format stream-json`."""

import json
import threading
import time


class ClaudeEventParser:
    PHASE_WAITING = "waiting"
    PHASE_LLM = "llm"
    PHASE_TOOL_RUNNING = "tool_running"
    PHASE_DONE = "done"

    def __init__(self, output):
        self.output = output
        self.accumulated_text = ""
        self.session_id = None

        self.total_cost_usd = 0.0
        self.input_tokens = 0
        self.output_tokens = 0
        self.cache_read_tokens = 0
        self.cache_creation_tokens = 0
        self.terminal_error = None

        self.lock = threading.Lock()
        self.last_event_ts = time.monotonic()
        self.phase = self.PHASE_WAITING
        self.current_tool = None
        self.current_tool_started = None
        self.tool_calls = []
        self.commands = []
        self.step_count = 0
        self.compaction_count = 0
        self.cumulative_output_tokens = 0
        self.cumulative_tool_result_chars = 0

    def _write(self, label, content):
        if content:
            self.output.write(f"[{label}]\n{content}\n\n")
            self.output.flush()

    def _mark_event(self, new_phase=None):
        with self.lock:
            self.last_event_ts = time.monotonic()
            if new_phase is not None:
                self.phase = new_phase

    def snapshot_state(self):
        with self.lock:
            return self.phase, time.monotonic() - self.last_event_ts, self.current_tool

    def handle(self, event):
        event_type = event.get("type", "")

        if event_type == "system":
            session_id = event.get("session_id")
            if session_id:
                self.session_id = session_id
            if event.get("subtype", "") == "compact_boundary":
                self.compaction_count += 1
                self._write(
                    "COMPACTION",
                    f"#{self.compaction_count} at step {self.step_count}, "
                    f"cumulative_out={self.cumulative_output_tokens}, "
                    f"tool_chars={self.cumulative_tool_result_chars}",
                )
            self._mark_event(self.PHASE_LLM)

        elif event_type == "assistant":
            message = event.get("message", {}) or {}
            for block in message.get("content", []) or []:
                block_type = block.get("type", "")
                if block_type == "text":
                    text = block.get("text", "")
                    if text:
                        self.accumulated_text += text
                    self._mark_event(self.PHASE_LLM)
                elif block_type == "tool_use":
                    name = block.get("name", "unknown")
                    arguments = block.get("input", {})
                    with self.lock:
                        self.current_tool = name
                        self.current_tool_started = time.monotonic()
                    self._mark_event(self.PHASE_TOOL_RUNNING)
                    if isinstance(arguments, dict):
                        content = json.dumps(arguments, indent=2)
                        command = arguments.get("command") or arguments.get("cmd") or ""
                        if isinstance(command, str) and command.strip():
                            self.commands.append(command.strip()[:200])
                    else:
                        content = str(arguments)
                    self._write(f"TOOL USE: {name}", content[:2000])
                elif block_type == "thinking":
                    self._mark_event(self.PHASE_LLM)

            self.step_count += 1
            self.cumulative_output_tokens += (message.get("usage", {}) or {}).get("output_tokens", 0)

        elif event_type == "user":
            message = event.get("message", {}) or {}
            for block in message.get("content", []) or []:
                if block.get("type", "") != "tool_result":
                    continue
                content = block.get("content", "")
                if isinstance(content, list):
                    content = "\n".join(
                        item.get("text", str(item)) if isinstance(item, dict) else str(item)
                        for item in content
                    )
                content = str(content)
                self.cumulative_tool_result_chars += len(content)
                self._write("TOOL RESULT", content[:2000])
                with self.lock:
                    duration = time.monotonic() - self.current_tool_started if self.current_tool_started else 0.0
                    tool_name = self.current_tool or "unknown"
                    self.current_tool = None
                    self.current_tool_started = None
                self.tool_calls.append((tool_name, duration))
                self._mark_event(self.PHASE_LLM)

        elif event_type == "result":
            cost = event.get("total_cost_usd", 0.0)
            if isinstance(cost, (int, float)):
                self.total_cost_usd = cost
            usage = event.get("usage", {}) or {}
            self.input_tokens = usage.get("input_tokens", 0) or 0
            self.output_tokens = usage.get("output_tokens", 0) or 0
            self.cache_read_tokens = usage.get("cache_read_input_tokens", 0) or 0
            self.cache_creation_tokens = usage.get("cache_creation_input_tokens", 0) or 0
            session_id = event.get("session_id")
            if session_id:
                self.session_id = session_id
            if event.get("is_error", False):
                self.terminal_error = event.get("subtype", "error")
            self._mark_event(self.PHASE_DONE)

        else:
            self._mark_event()
