from __future__ import annotations

import io

from prolong_agent.agent.claude_events import ClaudeEventParser
from prolong_agent.agent.codex_events import CodexEventParser


def test_codex_parser_records_mcp_tool_calls():
    parser = CodexEventParser(io.StringIO())
    parser.handle({
        "type": "item.started",
        "item": {
            "type": "mcp_tool_call",
            "server": "prolong_game",
            "tool": "current_board",
            "arguments": {},
        },
    })
    assert parser.phase == parser.PHASE_TOOL_RUNNING
    parser.handle({
        "type": "item.completed",
        "item": {
            "type": "mcp_tool_call",
            "server": "prolong_game",
            "tool": "current_board",
            "result": {"state": "PLAYING"},
        },
    })
    assert parser.phase == parser.PHASE_POST_TOOL
    assert parser.tool_calls[0][0] == "prolong_game.current_board"


def test_claude_parser_records_both_mcp_tools_as_progress():
    parser = ClaudeEventParser(io.StringIO())
    for name in ("mcp__prolong_game__current_board", "mcp__prolong_game__submit_actions"):
        parser.handle({
            "type": "assistant",
            "message": {"content": [{"type": "tool_use", "name": name, "input": {}}]},
        })
        assert parser.phase == parser.PHASE_TOOL_RUNNING
        parser.handle({
            "type": "user",
            "message": {"content": [{"type": "tool_result", "content": "ok"}]},
        })
        assert parser.phase == parser.PHASE_LLM
    assert [name for name, _ in parser.tool_calls] == [
        "mcp__prolong_game__current_board",
        "mcp__prolong_game__submit_actions",
    ]
