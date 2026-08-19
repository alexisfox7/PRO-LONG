"""CodexAgent: runs OpenAI Codex CLI inside Docker to produce action plans."""
from __future__ import annotations

import json
import logging
import os
import subprocess
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from prolong_agent.agent.base import BaseAgent
from prolong_agent.agent.codex_events import CodexEventParser
from prolong_agent.utils import sandbox_net

log = logging.getLogger(__name__)

_DEFAULT_REASONING_EFFORT = "none"


class CodexAgent(BaseAgent):
    """Run OpenAI Codex CLI inside Docker to produce game actions."""

    BACKEND_ID = "codex"

    _DOCKER_IMAGE = os.environ.get(
        "CODEX_DOCKER_IMAGE", "prolong-agent/codex-sandbox:latest"
    )

    def __init__(
        self,
        *,
        model: str = "gpt-5.5",
        reasoning_effort: str = _DEFAULT_REASONING_EFFORT,
        timeout: Optional[int] = None,
        grid_mode: str = "hex",
        run_label: str = "",
        log_window: Optional[int] = None,
        codex_home: Optional[str] = None,
        action_cap: int = 20,
    ) -> None:
        super().__init__(grid_mode, log_window, action_cap, workspace=".")
        self._model = model
        self._reasoning_effort = reasoning_effort
        self._timeout = timeout
        self._codex_temp: tempfile.TemporaryDirectory[str] | None = None
        codex_home = codex_home or os.environ.get("CODEX_HOME")
        if codex_home:
            self._codex_home = Path(codex_home).expanduser().resolve()
            if self._codex_home == (Path.home() / ".codex").resolve():
                raise ValueError("refusing to mount the global ~/.codex directory")
            self._codex_home.mkdir(parents=True, exist_ok=True)
        else:
            self._codex_temp = tempfile.TemporaryDirectory(prefix="prolong-codex-")
            self._codex_home = Path(self._codex_temp.name)
        self._call_count: dict[str, int] = {}
        self._session_ids: dict[str, str] = {}
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

    def _find_session_file(self, session_id: str) -> Optional[Path]:
        sessions_root = self._codex_home / "sessions"
        if not sessions_root.exists():
            return None
        matches = list(sessions_root.rglob(f"*{session_id}.jsonl"))
        return matches[0] if matches else None

    def _session_exists_on_disk(self, session_id: str) -> bool:
        return self._find_session_file(session_id) is not None

    def _build_codex_args(
        self, prompt: str, is_first: bool, session_id: Optional[str]
    ) -> list[str]:
        common_opts = [
            "--json",
            "--skip-git-repo-check",
            "--ignore-user-config",
            "--ignore-rules",
            "-o", "/workspace/last_message.txt",
            "-m", self._model,
            "-c", f'model_reasoning_effort="{self._reasoning_effort}"',
            "-c", "shell_environment_policy.ignore_default_excludes=false",
        ]
        if not is_first and session_id:
            return [
                "exec", "resume",
                *common_opts,
                "--dangerously-bypass-approvals-and-sandbox",
                session_id, prompt,
            ]
        return [
            "exec",
            *common_opts,
            "-s", "danger-full-access",
            prompt,
        ]

    def analyze(self, log_path: Path, action_num: int, retry_nudge: str = "",
                **kwargs) -> Optional[dict[str, Any]]:
        if not log_path.exists():
            return None

        path_key = str(log_path)
        is_first = path_key not in self._call_count
        self._call_count[path_key] = self._call_count.get(path_key, 0) + 1

        sandbox = self._get_sandbox(log_path)
        self._sync_history(log_path, sandbox)
        self._add_current_board(log_path, kwargs)

        available_actions = self._available_actions(kwargs)
        agents_md = sandbox / "AGENTS.md"
        if not agents_md.exists():
            agents_md.write_text(self._build_system_prompt(available_actions))

        self._clear_files(sandbox, "actions.json", "last_message.txt")

        prompt = self._build_prompt(log_path.name, is_first, action_num=action_num, **kwargs)
        if retry_nudge:
            prompt += f"\n\n{retry_nudge}"

        session_id = self._session_ids.get(path_key)

        if not is_first and session_id:
            if not self._session_exists_on_disk(session_id):
                log.warning(
                    "action=%d: codex session %s no longer exists on disk — "
                    "dropping stale id",
                    action_num, session_id,
                )
                self._session_ids.pop(path_key, None)
                session_id = None

        codex_args = self._build_codex_args(prompt, is_first, session_id)

        host_codex = self._codex_home
        # Secure by default: the agent runs on an --internal docker network
        # (no direct internet/host/metadata) and reaches the OpenAI API only
        # through the squid allowlist proxy. The container never talks to the
        # game server (the host-side runner does), so an LLM-only allowlist is
        # sufficient. Opt out with CODEX_DOCKER_NETWORK=host.
        _net = os.environ.get("CODEX_DOCKER_NETWORK", sandbox_net.INTERNAL_NETWORK)
        _proxy = os.environ.get("CODEX_EGRESS_PROXY",
                                "http://prolong-openai-proxy:3128"
                                if _net == sandbox_net.INTERNAL_NETWORK else "")
        if _net == sandbox_net.INTERNAL_NETWORK:
            sandbox_net.ensure_secure_network(
                "prolong-openai-proxy", "prolong-openai-proxy", "docker/openai-proxy")
        net_flags: list[str] = ["--network", _net] if _net else []
        if _proxy:
            for _v in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                       "http_proxy", "https_proxy", "all_proxy"):
                net_flags += ["-e", f"{_v}={_proxy}"]
            net_flags += ["-e", "NO_PROXY=localhost,127.0.0.1",
                          "-e", "no_proxy=localhost,127.0.0.1"]

        cmd = [
            "docker", "run", "--rm",
            "--user", "1000:1000",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges:true",
            "--pids-limit=256",
            *net_flags,
            "--memory=8g", "--cpus=4",
            "--tmpfs", "/tmp:rw,nosuid,nodev,size=256m",
            "-w", "/workspace",
            "-v", f"{os.path.realpath(sandbox)}:/workspace:rw",
            "-v", f"{os.path.realpath(host_codex)}:/home/sandbox/.codex:rw",
            "-e", "HOME=/home/sandbox",
            "-e", "CODEX_HOME=/home/sandbox/.codex",
        ]
        api_key = os.environ.get("CODEX_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
        auth_file = host_codex / "auth.json"
        if not api_key and not auth_file.exists():
            log.error("Set CODEX_API_KEY or use a dedicated CODEX_HOME containing auth.json")
            return None
        docker_env = os.environ.copy()
        if api_key:
            docker_env["CODEX_API_KEY"] = api_key
            cmd += ["-e", "CODEX_API_KEY"]
        cmd += [
            self._DOCKER_IMAGE,
            *codex_args,
        ]

        agent_log = log_path.parent / (log_path.stem + "_agent.txt")
        with open(agent_log, "a", encoding="utf-8") as f:
            f.write(f"\n--- action={action_num} | {datetime.now().strftime('%H:%M:%S')} | codex ---\n")
            if is_first or retry_nudge:
                f.write(f"[USER PROMPT]\n{prompt}\n\n")
            f.flush()

        log.info(
            "agent: model=%s, resume=%s, session=%s",
            self._model,
            not is_first and session_id is not None,
            session_id or "new",
        )

        call_started = time.monotonic()
        try:
            proc = subprocess.Popen(
                cmd,
                env=docker_env,
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

            with open(agent_log, "a", encoding="utf-8") as f:
                parser = CodexEventParser(f)
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
                self._session_ids[path_key] = parser.session_id
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

            hint, plan = self._split_response(text)

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
            agent_log = log_path.parent / (log_path.stem + "_agent.txt")
            with open(agent_log, "a", encoding="utf-8") as f:
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
        parser: CodexEventParser,
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
