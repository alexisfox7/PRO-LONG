# Experiment configurations

Run these presets from `research/arc-agi-3/` after following the
[setup guide](../README.md#setup). Each preset runs all 25 versioned games once.

| Preset | Backend / model | Actions per game | Memory |
|---|---|---:|---|
| [codex-500.toml](codex-500.toml) | Codex / GPT-5.5 | 500 | Full history |
| [codex-500-no-log.toml](codex-500-no-log.toml) | Codex / GPT-5.5 | 500 | No log |
| [claude-500.toml](claude-500.toml) | Claude Code / Opus 4.6 | 500 | Full history |
| [claude-2000.toml](claude-2000.toml) | Claude Code / Opus 4.6 | 2,000 | Full history |

All presets use high effort and batches of at most 20 actions. The 2,000-action
preset is a template for extended-budget experiments with Opus 4.6; it does not
reproduce the paper's Fable 5 result. Select the appropriate model identifier
for your provider and account when matching a particular paper experiment.

```bash
# Smoke test one game; CLI flags override the preset.
prolong-swarm --config configs/codex-500.toml --game ls20

# Five independent repetitions of the full suite.
prolong-swarm --config configs/codex-500.toml --repetitions 5

# Matched no-log condition.
prolong-swarm --config configs/codex-500-no-log.toml --repetitions 5
```

## Format and overrides

A file contains a single `[experiment]` table. Keys match CLI destination names
with underscores, such as `max_actions`, `reasoning_effort`, and `use_api_key`.
Values must have the correct TOML type; unknown settings and invalid choices
are rejected before evaluation. Store credentials in the environment, not here.

Settings resolve in this order: **CLI overrides → config → CLI defaults**.
Use either `suite = "all"` or `game = "ls20,ft09"` in a config. Explicit `--game`
replaces a configured suite, and explicit `--suite` replaces configured games.
Model identifiers remain explicit settings: when changing a preset's backend,
also set `--model` and the backend's effort flag.

| Memory setting in TOML | CLI override |
|---|---|
| `log_window = "full"` | `--full-history` |
| `log_window = 25` | `--log-window 25` |
| `log_window = -1` | `--log-window -1` |

Use `--api-key` or `--no-api-key` to override `use_api_key`. Omitting a config
preserves the existing CLI defaults, including Codex's `none` reasoning effort.

## Repetitions and provenance

`repetitions` defaults to 1. Repetitions run sequentially, with games concurrent
within each repetition. Each starts a fresh agent and scorecard and writes to
its own output directory. A failure or Ctrl+C stops the remaining repetitions;
the runner exits with code 1 or 130, respectively.

Each directory contains `manifest.json` with schema version 1, including:

- A shared experiment ID, a unique run ID, and a one-based repetition number.
- The resolved settings, full game version IDs, and input config SHA-256.
- UTC start/end times, run status, scorecard ID, game statuses, and missing games.
- Git revision and dirty state, installed Python package versions, and a snapshot
  of the Docker server version and local sandbox/proxy image IDs before execution.

Provenance probes are read-only and bounded. Unavailable values are `null`; early
backend setup failures may have no provenance snapshot. Image IDs describe the
local tags inspected at startup; images are not pinned or pulled by this step,
and the snapshot does not verify an already-running proxy container's image.
Agent CLI versions are not queried separately. Keep the images used for a run.

The manifest is written before backend setup and replaced atomically on updates.
Final statuses are `completed`, `failed`, or `interrupted`. `completed` means the
evaluation finished, including games that exhausted their action budget; consult
`game_statuses` and the scorecard for game outcomes. A process killed without
cleanup can leave status `running`, which must not be counted as completed.

This runner collects repetitions; it does not yet aggregate them into best@k
or regenerate paper figures. Check requested versus completed repetitions
before reporting results.
