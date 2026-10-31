import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import prolong_agent.agent as agents
from prolong_agent.agent import swarm


@pytest.fixture
def harness(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    control = SimpleNamespace(agents=[], environments=[], arcades=[], fail_at=None, win=True)

    class Agent:
        docker_image = "sandbox:test"

        def __init__(self, **kwargs):
            self.settings = kwargs
            self.calls = []
            self.closed = False
            control.agents.append(self)

        def analyze(self, log_path, action_num, **kwargs):
            self.calls.append((log_path, action_num))
            return {"hint": "", "plan": "", "actions": [{"name": "ACTION1", "data": {}}]}

        def close(self):
            self.closed = True
            if control.fail_at == "cleanup":
                raise RuntimeError("fake cleanup failed")

    class Environment:
        def __init__(self, **kwargs):
            self.settings = kwargs
            self.closed = False
            control.environments.append(self)

        def reset(self, task):
            if control.fail_at == "game":
                raise ValueError("fake game failed")
            self.task = task
            return {"state": "NOT_FINISHED", "score": 0, "frame": [[[0]]], "available_actions": [1]}

        def step(self, action):
            return {"state": "WIN" if control.win else "NOT_FINISHED", "score": 1, "frame": [[[1]]]}, 0, control.win

        def close(self):
            self.closed = True

    class Arcade:
        def __init__(self, **kwargs):
            self.settings = kwargs
            control.arcades.append(self)

        def open_scorecard(self, tags):
            if control.fail_at == "open":
                raise RuntimeError("fake scorecard failed")
            if control.fail_at == "interrupt":
                raise KeyboardInterrupt()
            return f"card-{len(control.arcades)}"

        def close_scorecard(self, card_id):
            if control.fail_at == "close":
                raise RuntimeError("fake scorecard failed")
            return SimpleNamespace(
                score=42.0, total_environments_completed=1, total_environments=1,
                total_levels_completed=1, total_levels=1, total_actions=1, environments=[],
                model_dump_json=lambda **kwargs: json.dumps({"card_id": card_id, "score": 42.0}),
            )

    monkeypatch.setattr(agents, "CodexAgent", Agent)
    monkeypatch.setattr(agents, "ClaudeCodeAgent", Agent)
    monkeypatch.setattr(swarm.arc_agi, "Arcade", Arcade)
    monkeypatch.setattr(swarm, "ArcAgi3Env", SimpleNamespace(from_arcade=Environment))
    monkeypatch.setattr(swarm, "collect_provenance", lambda *args: {"fixture": True})
    return control


def run(monkeypatch, *args):
    monkeypatch.setattr("sys.argv", ["prolong-swarm", *args])
    swarm.main()


def manifests():
    return sorted(
        [(path, json.loads(path.read_text(encoding="utf-8")))
         for path in Path("evaluation_results").glob("*/manifest.json")],
        key=lambda item: item[1]["repetition"],
    )


def test_repetitions_use_fresh_agents_scorecards_and_workspaces(harness, monkeypatch, tmp_path):
    config = tmp_path / "experiment.toml"
    config.write_text('[experiment]\nbackend="codex"\nsuite="all"\nreasoning_effort="high"\nmax_actions=500\n')
    run(monkeypatch, "--config", str(config), "--game", "ls20,ft09", "--max-actions", "2", "--repetitions", "2")
    records = manifests()
    assert len(records) == len(harness.agents) == len(harness.arcades) == 2
    assert len(harness.environments) == 4
    assert records[0][1]["experiment_id"] == records[1][1]["experiment_id"]
    assert records[0][1]["run_id"] != records[1][1]["run_id"]
    for repetition, (path, record) in enumerate(records, start=1):
        assert record["status"] == "completed"
        assert record["finished_at"] >= record["started_at"]
        assert record["missing_games"] == []
        assert record["scorecard_id"] == f"card-{repetition}"
        assert record["game_ids"] == ["ls20-9607627b", "ft09-0d8bbf25"]
        assert set(record["game_statuses"].values()) == {"COMPLETED_RUN"}
        assert record["configuration"]["max_actions"] == 2
        assert record["provenance"] == {"fixture": True}
        assert (path.parent / "scorecard.json").exists()
        assert f"Run {repetition:>2}:" in (path.parent / "summary.txt").read_text()
        agent = harness.agents[repetition - 1]
        assert agent.settings["reasoning_effort"] == "high"
        assert agent.closed
        assert {call[0].parent.parent for call in agent.calls} == {path.parent}
    assert all(env.closed and env.task["max_actions"] == 2 for env in harness.environments)


@pytest.mark.parametrize("stage,expected_status,exit_code", [
    ("open", "failed", 1), ("close", "failed", 1),
    ("game", "failed", 1), ("interrupt", "interrupted", 130),
    ("cleanup", "failed", 1),
])
def test_failures_and_interruptions_are_recorded_and_stop_repetitions(harness, monkeypatch, stage, expected_status, exit_code):
    harness.fail_at = stage
    with pytest.raises(SystemExit) as error:
        run(monkeypatch, "--game", "ls20", "--repetitions", "3")
    assert error.value.code == exit_code
    records = manifests()
    assert len(records) == len(harness.agents) == 1
    record = records[0][1]
    assert record["status"] == expected_status
    assert record["finished_at"] is not None
    assert record["error_type"] is not None
    assert harness.agents[0].closed
    if stage in {"open", "interrupt"}:
        assert record["missing_games"] == ["ls20-9607627b"]
    if stage == "game":
        assert record["game_statuses"] == {"ls20-9607627b": "ERROR"}


def test_action_budget_exhaustion_is_a_completed_evaluation(harness, monkeypatch):
    harness.win = False
    run(monkeypatch, "--game", "ls20", "--max-actions", "1")
    record = manifests()[0][1]
    assert record["status"] == "completed"
    assert record["game_statuses"] == {"ls20-9607627b": "TIMEOUT"}


def test_backend_setup_failure_still_has_manifest(harness, monkeypatch):
    def fail(*args):
        raise ValueError("setup failed")

    monkeypatch.setattr(swarm, "_create_agent", fail)
    with pytest.raises(SystemExit):
        run(monkeypatch, "--game", "ls20")
    record = manifests()[0][1]
    assert record["status"] == "failed"
    assert record["missing_games"] == ["ls20-9607627b"]
    assert record["provenance"] is None


def test_repeated_game_ids_cannot_overwrite_workspaces(harness, monkeypatch):
    with pytest.raises(SystemExit):
        run(monkeypatch, "--game", "ls20,ls20-9607627b")
    assert harness.agents == []
    assert manifests() == []


def test_user_labels_stay_within_results_directory(harness, monkeypatch):
    run(monkeypatch, "--game", "ls20", "--note", "../../outside\\name", "--agent", "../../agent")
    path, _ = manifests()[0]
    assert path.parent.parent == Path("evaluation_results")
