import hashlib
from pathlib import Path

import pytest

from prolong_agent.experiment import parse_args


def parse(argv):
    return parse_args(argv, suites=["all"])


def config(tmp_path, settings):
    path = tmp_path / "experiment.toml"
    path.write_text("[experiment]\n" + settings, encoding="utf-8")
    return path


def test_legacy_cli_defaults_and_backend_selection():
    args = parse([])
    assert (args.backend, args.model, args.reasoning_effort) == ("codex", "gpt-5.5", "none")
    assert (args.max_actions, args.action_cap, args.log_window, args.repetitions) == (500, 20, None, 1)
    assert parse(["--backend", "claude-code"]).model == "claude-opus-4-6"


def test_cli_overrides_config_including_boolean_and_full_history(tmp_path):
    path = config(tmp_path, 'backend="claude-code"\nmax_actions=2000\nlog_window=-1\nuse_api_key=true\nsuite="all"\n')
    args = parse(["--config", str(path), "--game", "ls20", "--max-actions", "500", "--full-history", "--no-api-key"])
    assert (args.backend, args.model) == ("claude-code", "claude-opus-4-6")
    assert (args.max_actions, args.log_window, args.use_api_key) == (500, None, False)
    assert (args.game, args.suite) == ("ls20", None)
    assert args.config_sha256 == hashlib.sha256(path.read_bytes()).hexdigest()


def test_cli_suite_replaces_configured_game(tmp_path):
    path = config(tmp_path, 'game="ls20"\n')
    args = parse(["--config", str(path), "--suite=all"])
    assert (args.game, args.suite) == (None, "all")


@pytest.mark.parametrize("settings", [
    "max_action=500", "max_actions=true", 'max_actions="500"', "max_actions=0",
    'backend="typo"', 'suite="missing"', 'reasoning_effort="invalid"',
    "use_api_key=1", "log_window=0", 'log_window="none"', "repetitions=-1",
    'game="ls20"\nsuite="all"', 'config="other.toml"',
])
def test_invalid_configs_fail_before_execution(tmp_path, settings):
    with pytest.raises(SystemExit) as error:
        parse(["--config", str(config(tmp_path, settings))])
    assert error.value.code == 2


@pytest.mark.parametrize("flag", ["--max-actions", "--action-cap", "--retries", "--repetitions"])
def test_nonpositive_cli_budgets_are_rejected(flag):
    with pytest.raises(SystemExit):
        parse([flag, "0"])


def test_unknown_config_table_is_rejected(tmp_path):
    path = tmp_path / "wrong.toml"
    path.write_text('[experiments]\nbackend="codex"', encoding="utf-8")
    with pytest.raises(SystemExit):
        parse(["--config", str(path)])


@pytest.mark.parametrize("name,budget,window,backend", [
    ("codex-500", 500, None, "codex"),
    ("codex-500-no-log", 500, -1, "codex"),
    ("claude-500", 500, None, "claude-code"),
    ("claude-2000", 2000, None, "claude-code"),
])
def test_shipped_presets(name, budget, window, backend):
    path = Path(__file__).parents[1] / "configs" / f"{name}.toml"
    args = parse(["--config", str(path)])
    assert (args.max_actions, args.log_window, args.backend) == (budget, window, backend)
    assert args.suite == "all"
    assert getattr(args, "reasoning_effort" if backend == "codex" else "effort") == "high"
