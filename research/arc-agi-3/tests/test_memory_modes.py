from __future__ import annotations

import itertools

import pytest

from prolong_agent.agent.base import BaseAgent
from prolong_agent.agent.codex_agent import CodexAgent
from prolong_agent.agent.claude_code_agent import ClaudeCodeAgent
from prolong_agent.agent.memory import MemoryMode, resolve_memory_mode
from prolong_agent.agent.swarm import _parse_args


def test_memory_mode_resolution():
    assert resolve_memory_mode() == (MemoryMode.FULL_LOG, None)
    assert resolve_memory_mode(log_window=4) == (MemoryMode.WINDOWED_LOG, 4)
    assert resolve_memory_mode(in_prompt=True) == (MemoryMode.IN_PROMPT, None)
    assert resolve_memory_mode(no_log=True) == (MemoryMode.MCP_NO_LOG, None)


def test_log_window_minus_one_is_deprecated_in_prompt_alias():
    with pytest.warns(FutureWarning, match="--in-prompt"):
        assert resolve_memory_mode(log_window=-1) == (MemoryMode.IN_PROMPT, None)


@pytest.mark.parametrize(
    "values",
    [values for size in (2, 3) for values in itertools.combinations(
        ("no_log", "in_prompt", "log_window"), size
    )],
)
def test_conflicting_memory_flags_are_rejected(values):
    kwargs = {"no_log": False, "in_prompt": False, "log_window": None}
    for value in values:
        kwargs[value] = 2 if value == "log_window" else True
    with pytest.raises(ValueError, match="mutually exclusive"):
        resolve_memory_mode(**kwargs)


def test_cli_exposes_distinct_flags():
    assert _parse_args(["--no-log"]).memory_mode == MemoryMode.MCP_NO_LOG
    assert _parse_args(["--in-prompt"]).memory_mode == MemoryMode.IN_PROMPT


def test_no_log_prompts_are_state_free():
    agent = BaseAgent(memory_mode=MemoryMode.MCP_NO_LOG)
    prompts = [
        agent._build_system_prompt(),
        agent._build_prompt("secret.txt", True),
        agent._build_prompt("secret.txt", False),
    ]
    joined = "\n".join(prompts)
    assert "logs.txt" not in joined
    assert "Score:" not in joined
    assert "Action:" not in joined
    assert "000000" not in joined
    assert "secret.txt" not in joined


def test_interactive_workspace_removes_stale_logs_recursively(tmp_path):
    nested = tmp_path / "old" / "run"
    nested.mkdir(parents=True)
    (tmp_path / "logs.txt").write_text("state")
    (nested / "logs.txt").write_text("state")
    (tmp_path / "current_board.txt").write_text("board")
    (nested / "current_board.txt").write_text("board")
    (tmp_path / "actions.json").write_text("{}")

    BaseAgent._purge_interactive_game_artifacts(tmp_path)

    assert not list(tmp_path.rglob("logs.txt"))
    assert not (tmp_path / "current_board.txt").exists()
    assert not list(tmp_path.rglob("current_board.txt"))
    assert not (tmp_path / "actions.json").exists()


def test_codex_mcp_config_retains_user_config_isolation(tmp_path):
    agent = CodexAgent(
        codex_home=str(tmp_path / "codex-home"),
        memory_mode=MemoryMode.MCP_NO_LOG,
    )
    args = agent._build_codex_args(
        "state-free prompt",
        True,
        None,
        mcp_url="http://host.docker.internal:1234/mcp",
    )
    assert "--ignore-user-config" in args
    assert any("mcp_servers.prolong_game.url" in arg for arg in args)
    assert any("bearer_token_env_var" in arg for arg in args)


def test_claude_mcp_config_exposes_only_the_game_server():
    config = ClaudeCodeAgent._mcp_config("http://host.docker.internal:1234/mcp")
    assert set(config["mcpServers"]) == {"prolong_game"}
    game = config["mcpServers"]["prolong_game"]
    assert game["type"] == "http"
    assert game["headers"]["Authorization"] == "Bearer ${PROLONG_MCP_TOKEN}"
