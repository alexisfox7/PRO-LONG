"""Versioned run manifests and bounded, read-only provenance collection."""
from __future__ import annotations

import json
import platform
import subprocess
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

CONFIG_FIELDS = (
    "agent", "backend", "model", "game", "suite", "tags", "max_actions",
    "operation_mode", "retries", "use_api_key", "effort", "reasoning_effort",
    "grid_mode", "log_window", "action_cap", "repetitions", "note",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _probe(command: list[str], cwd: Path | None = None) -> str | None:
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def collect_provenance(project_root: Path, sandbox_image: str, proxy_image: str) -> dict:
    status = _probe(["git", "status", "--porcelain", "--untracked-files=normal"], project_root)
    return {
        "git": {
            "revision": _probe(["git", "rev-parse", "HEAD"], project_root),
            "dirty": None if status is None else bool(status),
        },
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": dict(sorted(
            (distribution.metadata["Name"], distribution.version)
            for distribution in metadata.distributions() if distribution.metadata["Name"]
        )),
        "docker": {
            "server_version": _probe(["docker", "version", "--format", "{{.Server.Version}}"]),
            "images": {
                role: {"tag": tag, "id": _probe(["docker", "image", "inspect", "--format", "{{.Id}}", tag])}
                for role, tag in (("sandbox", sandbox_image), ("proxy", proxy_image))
            },
        },
    }


def create_manifest(args, games: list[str], experiment_id: str, repetition: int) -> dict:
    return {
        "schema_version": 1,
        "experiment_id": experiment_id,
        "run_id": f"{experiment_id}-rep{repetition}",
        "repetition": repetition,
        "started_at": utc_now(),
        "finished_at": None,
        "status": "running",
        "source_config": None if args.config is None else {
            "path": str(args.config), "sha256": args.config_sha256,
        },
        # Persist known experiment fields only, never credentials or the environment.
        "configuration": {key: getattr(args, key) for key in CONFIG_FIELDS},
        "game_ids": list(games),
        "provenance": None,
        "scorecard_id": None,
        "game_statuses": {},
        "missing_games": list(games),
        "error_type": None,
    }


def write_manifest(run_dir: Path, manifest: dict) -> None:
    temporary = run_dir / ".manifest.json.tmp"
    temporary.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(run_dir / "manifest.json")
