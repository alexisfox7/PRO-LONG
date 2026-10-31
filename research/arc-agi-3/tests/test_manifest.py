import json
import subprocess
from types import SimpleNamespace

import pytest

from prolong_agent import manifest
from prolong_agent.experiment import parse_args


def test_manifest_records_resolved_experiment_and_excludes_credentials(tmp_path, monkeypatch):
    args = parse_args(["--backend", "claude-code", "--repetitions", "3"], suites=["all"])
    args.unexpected_secret = "do-not-save"
    monkeypatch.setenv("ANTHROPIC_API_KEY", "do-not-save")
    record = manifest.create_manifest(args, ["ls20-version"], "experiment", 2)
    manifest.write_manifest(tmp_path, record)
    saved = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert saved["configuration"]["model"] == "claude-opus-4-6"
    assert saved["configuration"]["repetitions"] == 3
    assert saved["run_id"] == "experiment-rep2"
    assert saved["game_ids"] == saved["missing_games"] == ["ls20-version"]
    assert saved["status"] == "running"
    assert saved["finished_at"] is None
    assert "do-not-save" not in json.dumps(saved)
    assert not (tmp_path / ".manifest.json.tmp").exists()


def test_failed_manifest_serialization_preserves_last_valid_file(tmp_path):
    manifest.write_manifest(tmp_path, {"status": "running"})
    with pytest.raises(TypeError):
        manifest.write_manifest(tmp_path, {"not_json": object()})
    assert json.loads((tmp_path / "manifest.json").read_text()) == {"status": "running"}


@pytest.mark.parametrize("failure", [FileNotFoundError(), subprocess.TimeoutExpired("docker", 5)])
def test_probes_are_bounded_and_optional(monkeypatch, failure):
    def fail(command, **kwargs):
        assert kwargs["timeout"] == 5
        raise failure

    monkeypatch.setattr(subprocess, "run", fail)
    assert manifest._probe(["docker", "version"]) is None


def test_provenance_records_image_ids_without_container_launches(tmp_path, monkeypatch):
    calls = []

    def probe(command, cwd=None):
        calls.append(command)
        if command[0:3] == ["git", "status", "--porcelain"]:
            return " M changed.py"
        return "snapshot"

    monkeypatch.setattr(manifest, "_probe", probe)
    monkeypatch.setattr(manifest.metadata, "distributions", lambda: [
        SimpleNamespace(metadata={"Name": "arc-agi"}, version="0.9.1"),
    ])
    saved = manifest.collect_provenance(tmp_path, "sandbox:tag", "proxy:tag")
    assert saved["git"] == {"revision": "snapshot", "dirty": True}
    assert saved["packages"] == {"arc-agi": "0.9.1"}
    assert saved["docker"]["images"]["sandbox"] == {"tag": "sandbox:tag", "id": "snapshot"}
    assert all("run" not in call and "pull" not in call for call in calls)


def test_unavailable_provenance_is_unknown_not_clean(tmp_path, monkeypatch):
    monkeypatch.setattr(manifest, "_probe", lambda *args, **kwargs: None)
    saved = manifest.collect_provenance(tmp_path, "sandbox", "proxy")
    assert saved["git"] == {"revision": None, "dirty": None}
    assert saved["docker"]["images"]["sandbox"]["id"] is None
