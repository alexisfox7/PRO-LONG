"""Experiment configuration, with existing CLI flags taking precedence."""
from __future__ import annotations

import argparse
import hashlib
import tomllib
from pathlib import Path

DEFAULT_MODELS = {"codex": "gpt-5.5", "claude-code": "claude-opus-4-6"}


def _config_defaults(path: Path, parser: argparse.ArgumentParser) -> tuple[dict, str]:
    raw = path.read_bytes()
    document = tomllib.loads(raw.decode("utf-8"))
    if set(document) != {"experiment"} or not isinstance(document["experiment"], dict):
        raise ValueError("config must contain one [experiment] table")
    values = document["experiment"]
    # Reuse the CLI's types and choices so the two interfaces cannot drift.
    options = {}
    for action in parser._actions:
        if action.dest not in {"help", "config"}:
            options.setdefault(action.dest, action)
    for key, value in values.items():
        if key not in options:
            raise ValueError(f"unknown experiment setting: {key}")
        action = options[key]
        if key == "log_window" and value == "full":
            values[key] = None
            continue
        expected = bool if key == "use_api_key" else (action.type or str)
        if type(value) is not expected:
            raise ValueError(f"{key} must be {expected.__name__}")
        if action.choices is not None and value not in action.choices:
            raise ValueError(f"invalid {key}: {value!r}; choose from {list(action.choices)}")
    if "game" in values and "suite" in values:
        raise ValueError("configure either game or suite, not both")
    return values, hashlib.sha256(raw).hexdigest()


def parse_args(argv=None, *, suites):
    parser = argparse.ArgumentParser(description="Run ARC-AGI-3 Swarm evaluation.")
    parser.add_argument("--config", type=Path, help="TOML experiment file; explicit CLI flags override it")
    parser.add_argument("--agent", "-a", default="prolong_agent")
    parser.add_argument("--game", "-g", help="Comma-separated game names or IDs (e.g. ls20,ft09).")
    parser.add_argument("--suite", "-s", choices=list(suites))
    parser.add_argument("--tags", "-t", help="Comma-separated tags.")
    parser.add_argument("--max-actions", type=int, default=500)
    parser.add_argument("--operation-mode", default="online", choices=["normal", "online", "offline"])
    parser.add_argument("--model", "-m", help="Model name; defaults depend on backend")
    parser.add_argument("--retries", type=int, default=5, help="Agent attempts per retry round")
    parser.add_argument("--backend", default="codex", choices=list(DEFAULT_MODELS))
    parser.add_argument("--api-key", dest="use_api_key", action=argparse.BooleanOptionalAction,
                        default=False, help="Use ANTHROPIC_API_KEY instead of subscription authentication")
    parser.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--reasoning-effort", default="none",
                        choices=["none", "minimal", "low", "medium", "high", "xhigh"])
    parser.add_argument("--grid-mode", default="hex", choices=["ascii", "hex", "num"])
    history = parser.add_mutually_exclusive_group()
    history.add_argument("--log-window", type=int,
                         help="Last N action sections for N>0, or -1 for no log")
    history.add_argument("--full-history", dest="log_window", action="store_const", const=None,
                         help="Use full history, overriding a configured memory condition")
    parser.add_argument("--action-cap", type=int, default=20)
    parser.add_argument("--repetitions", type=int, default=1,
                        help="Independent suite runs, executed sequentially (default 1)")
    parser.add_argument("--note", default="", help="Short run description saved to run_info.txt")

    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument("--config", type=Path)
    bootstrap.add_argument("--game", "-g")
    bootstrap.add_argument("--suite", "-s")
    selected, _ = bootstrap.parse_known_args(argv)
    config_sha256 = None
    if selected.config:
        try:
            defaults, config_sha256 = _config_defaults(selected.config, parser)
        except (OSError, UnicodeError, ValueError) as error:
            parser.error(str(error))
        if selected.game is not None:
            defaults.pop("suite", None)
        if selected.suite is not None:
            defaults.pop("game", None)
        parser.set_defaults(**defaults)
    args = parser.parse_args(argv)
    for name in ("max_actions", "action_cap", "retries", "repetitions"):
        if getattr(args, name) < 1:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.log_window is not None and args.log_window != -1 and args.log_window < 1:
        parser.error("--log-window must be -1 or a positive integer")
    args.model = args.model or DEFAULT_MODELS[args.backend]
    args.config_sha256 = config_sha256
    return args
