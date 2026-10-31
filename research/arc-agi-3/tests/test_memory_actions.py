import json

from prolong_agent.agent.base import BaseAgent


def test_action_parsing_rejects_invalid_entries_and_respects_batch_cap():
    actions = BaseAgent._parse_actions_json_text(json.dumps({"actions": [
        "ACTION1", "INVALID", {"action": "ACTION6", "x": 3, "y": 4}, "RESET",
    ]}), cap=3)
    assert actions == [
        {"name": "ACTION1", "data": {}},
        {"name": "ACTION6", "data": {"x": 3, "y": 4}},
    ]
    assert BaseAgent._parse_actions_json_text('{"actions":') == []
    assert BaseAgent._parse_actions_json_text('{"actions": "ACTION1"}') == []


def test_full_history_sync_appends_without_duplicating_prior_content(tmp_path):
    source = tmp_path / "logs.txt"
    source.write_text("first\n", encoding="utf-8")
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    agent = BaseAgent()
    agent._sync_history(source, sandbox)
    source.write_text("first\nsecond\n", encoding="utf-8")
    agent._sync_history(source, sandbox)
    agent._sync_history(source, sandbox)
    assert (sandbox / "logs.txt").read_text() == "first\nsecond\n"


def test_no_log_condition_does_not_copy_history(tmp_path):
    source = tmp_path / "logs.txt"
    source.write_text("private history", encoding="utf-8")
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    agent = BaseAgent(log_window=-1)
    agent._sync_history(source, sandbox)
    assert not (sandbox / "logs.txt").exists()
    assert "current board" in agent._build_prompt("logs.txt", True, board_text="current board")
