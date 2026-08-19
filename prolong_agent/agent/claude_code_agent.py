"""ClaudeCodeAgent: runs Claude Code CLI (-p) inside Docker for game analysis.

The first call creates a session via --session-id and later calls resume it
via --resume. Claude Code's native auto-compaction manages context growth.
Session data persists in cc_sessions/ on the host.

Auth: uses CLAUDE_CODE_OAUTH_TOKEN (Claude Max subscription) by default.
Pass use_api_key=True to use ANTHROPIC_API_KEY instead.
"""
from __future__ import annotations

import atexit
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from prolong_agent.agent.base import BaseAgent
from prolong_agent.agent.claude_events import ClaudeEventParser
from prolong_agent.utils import sandbox_net

log = logging.getLogger(__name__)

_DOCKER_IMAGE = os.environ.get("CLAUDE_DOCKER_IMAGE", "prolong-agent/claude-sandbox:latest")


class _ContainerPool:
    """Manages persistent Docker containers with /workspace bind-mounted."""

    def __init__(self, run_label: str = "", use_api_key: bool = False) -> None:
        self._run_label = run_label
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
                env_flags.extend(["-e", "ANTHROPIC_API_KEY"])
            else:
                log.warning("use_api_key=True but ANTHROPIC_API_KEY not set")
        else:
            oauth = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
            if oauth:
                env_flags.extend(["-e", "CLAUDE_CODE_OAUTH_TOKEN"])
            else:
                for key_name in ("ANTHROPIC_API_KEY",):
                    val = os.environ.get(key_name)
                    if val:
                        env_flags.extend(["-e", key_name])

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
            "--user", "1000:1000",
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
        action_cap: int = 20,
    ) -> None:
        super().__init__(grid_mode, log_window, action_cap)
        self._model = model
        self._timeout = timeout or 2400
        self._effort = effort
        self._call_count: dict[str, int] = {}
        self._session_ids: dict[str, str] = {}

        self.total_estimated_cost: float = 0.0
        self.total_calls: int = 0

        self._pool = _ContainerPool(run_label=run_label, use_api_key=use_api_key)
        atexit.register(self._pool.cleanup)

    def _session_args(self, path_key: str) -> tuple[list[str], str, bool]:
        session_id = self._session_ids.get(path_key)
        if session_id:
            return ["--resume", session_id], session_id, True
        session_id = str(uuid.uuid4())
        self._session_ids[path_key] = session_id
        return ["--session-id", session_id], session_id, False

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

        self._sync_history(log_path, sandbox)
        self._add_current_board(log_path, kwargs)

        available_actions = self._available_actions(kwargs)
        claude_md = sandbox / "CLAUDE.md"
        claude_md.write_text(self._build_system_prompt(available_actions))

        self._clear_files(sandbox, "actions.json")

        prompt = self._build_prompt(log_path.name, is_first,
                                    action_num=action_num, **kwargs)
        if retry_nudge:
            prompt += f"\n\n{retry_nudge}"

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

        session_args, session_id, resuming = self._session_args(path_key)
        cmd.extend(session_args)

        agent_log = log_path.parent / (log_path.stem + "_agent.txt")
        mode_label = f"{'resume' if resuming else 'new'}={session_id}"
        with open(agent_log, "a", encoding="utf-8") as f:
            f.write(f"\n--- action={action_num} | "
                    f"{datetime.now().strftime('%H:%M:%S')} | claude-code ---\n")
            if is_first or retry_nudge:
                f.write(f"[USER PROMPT]\n{prompt}\n\n")
            f.flush()

        log.info("agent: model=%s, session=%s (claude -p stream-json)",
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

            with open(agent_log, "a", encoding="utf-8") as f:
                parser = ClaudeEventParser(f)
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

            hint, plan = self._split_response(response_text)

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

            agent_log = log_path.parent / (log_path.stem + "_agent.txt")
            with open(agent_log, "a", encoding="utf-8") as f:
                f.write(f"\n[ACTIONS.JSON]\n{cat.stdout}\n")

            cap = self._action_cap
            actions = self._parse_actions_json_text(cat.stdout, cap=cap)
            log.info("actions.json produced %d actions (cap=%d)", len(actions), cap)
            return actions

        except Exception as e:
            log.warning("actions.json read error: %s", e)
            return []
