# PRO-LONG Harness for ARC-AGI-3

This guide covers the released Python harness for ARC-AGI-3, e.g., setup, evaluation,
memory conditions, and output files. For the method, benchmark results, and
figures, see the [research overview](../README.md). For our coding agent memory
tool, see the [tool guide](../../README.md#tool-guide).

[Setup](#setup) · [Evaluation](#evaluation) · [Options](#options) · [Outputs](#outputs) · [Scorecards and logs](#scorecards-and-logs)

## Setup

Requires **Python 3.12 or later**, Docker with Linux containers, and a POSIX shell. Run commands from `research/arc-agi-3/`. The `.python-version` file specifies Python 3.12.8.

```bash
git clone https://github.com/alexisfox7/PRO-LONG.git
cd PRO-LONG/research/arc-agi-3
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

The pip command uses the version ranges in `pyproject.toml`, not the exact versions in `uv.lock`. Save the installed package versions with your results.

### Docker images

Build the sandbox and proxy for the backend you use:

```bash
# codex backend
docker build -t prolong-agent/codex-sandbox:latest docker/codex-sandbox
docker build -t prolong-openai-proxy docker/openai-proxy

# claude-code backend
docker build -t prolong-agent/claude-sandbox:latest docker/claude-sandbox
docker build -t prolong-anthropic-proxy docker/anthropic-proxy
```

### Authentication

Create `.env` in this directory. Set `ARC_API_KEY` for online evaluation and
the credentials for your selected model backend:

```
ARC_API_KEY=...
CODEX_API_KEY=...             # Codex; OPENAI_API_KEY is also accepted
CLAUDE_CODE_OAUTH_TOKEN=...   # Claude Code subscription authentication
ANTHROPIC_API_KEY=...         # Claude Code API authentication; use --api-key
```

Only the credentials for the selected backend are needed. The default Claude
Code path prefers the OAuth token; `--api-key` selects Anthropic API-key
authentication. Codex can alternatively use a dedicated `CODEX_HOME` containing
`auth.json`; the harness refuses to mount the global `~/.codex` directory.

The host communicates with ARC-AGI-3. Agent containers mount the game workspace
and backend session storage, and use an internal Docker network with a
model-provider allowlist proxy. The harness starts the proxy automatically
after its image has been built.

## Evaluation

Start with one game to check the backend and output files:

```bash
prolong-swarm --game ls20 --backend codex -m gpt-5.5 --reasoning-effort high --max-actions 500 --note codex-single-game
```

Then run the fixed 25-game suite, or select games by comma-separated short names
or full IDs. The suite launches one worker per game concurrently.

```bash
# Codex, full history, high reasoning effort
prolong-swarm --suite all --backend codex -m gpt-5.5 --reasoning-effort high --max-actions 500 --note codex-full-rep1

# Claude Code, full history, high effort
prolong-swarm --suite all --backend claude-code -m claude-opus-4-6 --effort high --max-actions 500 --note claude-full-rep1

# Selected games; add --api-key for Anthropic API-key authentication
prolong-swarm --game ls20,ft09 --backend claude-code -m claude-opus-4-6 --effort high --api-key
```

Game versions for `--suite all` are fixed in
`prolong_agent/environment/config.py`. Without `--game` or `--suite`, the CLI
fetches the game list from the configured ARC API instead.

### Memory conditions

Keep the other settings fixed when comparing these conditions:

| Condition | Flags | History available |
|---|---|---|
| PRO-LONG | Omit `--log-window` | Full game log |
| Truncated history | `--log-window 25` | Last 25 action sections |
| No-log / in-prompt | `--log-window -1` | Current board in the prompt; no harness-provided log |

For example, the no-log counterpart to the Codex command above is:

```bash
prolong-swarm --suite all --backend codex -m gpt-5.5 --reasoning-effort high --max-actions 500 --log-window -1 --note codex-no-log-rep1
```

No-log still has coding tools and can write its own notes. Each command runs one episode per game; run it again with a different `--note` for another repetition. Use `--max-actions 2000` for the larger action budget.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--backend` | `codex` | `codex` (OpenAI Codex CLI) or `claude-code` (Claude Code CLI) |
| `--suite` | — | Game suite (`all` only) |
| `--game` | — | Comma-separated individual game names or full IDs |
| `--max-actions` | 500 | Max actions per game |
| `--action-cap` | 20 | Max actions returned by one agent call |
| `--model`, `-m` | Backend-specific | `gpt-5.5` for Codex; `claude-opus-4-6` for Claude Code |
| `--effort` | `high` | Effort level (claude-code backend) |
| `--reasoning-effort` | `none` | Reasoning effort (codex backend) |
| `--operation-mode` | `online` | `online` / `offline` / `normal` |
| `--grid-mode` | `hex` | Board encoding: `ascii`, `hex`, or `num` |
| `--log-window` | Full log | Positive action-window size, or `-1` for no-log |
| `--api-key` | Off | Select Anthropic API-key authentication for Claude Code |
| `--retries` | 5 | Agent attempts per retry round; failed rounds back off and repeat |
| `--note` | Empty | Run description, also included in the output directory name |
| `--tags` | Empty | Comma-separated scorecard tags |

Use `prolong-swarm --help` for all options. The paper uses high reasoning effort
unless otherwise specified; the Codex backend's default here is `none`, so the
examples set `--reasoning-effort high` explicitly. Offline mode changes the ARC
environment connection, not the model API connection.

### Runtime notes

- The Dockerfiles install unpinned coding-agent CLIs. Save the CLI versions and image IDs with your runs.
- `--retries` is not an overall failure limit: the current runner continues
  retry rounds indefinitely. Its process timeout checks also occur after
  blocking stdout reads; a silent child can prevent timely timeout handling.

## Outputs

Each invocation writes to
`evaluation_results/<timestamp>_swarm_<agent>__<note>/` relative to the current
directory; the note suffix is omitted when no note is supplied.

| File or directory | Contents |
|---|---|
| `scorecard.json` | Official efficiency scorecard, saved when returned by ARC |
| `summary.txt` | Aggregate and per-game metrics, including the returned scorecard |
| `<game>/logs.txt` | Structured observation, action, and outcome history |
| `<game>/logs_agent.txt` | Streamed agent transcript and call diagnostics |
| `<game>/current_board.txt` | Latest board snapshot |
| `<game>/run_info.txt` | Game, replay, scorecard, and invocation metadata when available |
| `<game>/codex_sandbox/` or `<game>/cc_sandbox/` | Agent workspace and generated `actions.json` |

The paper uses the efficiency score in `scorecard.json`. The CLI also prints the scorecard ID and available replay links.

## Scorecards and logs

The [scorecard directory](scorecards/) contains official online links, including
`fable_online_scorecards.txt`, which lists one run for each of the 25 Fable 5
games. The [release logs](https://github.com/alexisfox7/PRO-LONG/tree/main/research/arc-agi-3/release_logs)
contain game histories, transcripts, scorecards, and saved workspaces for those
runs. Released transcripts use the older name `logs_analyzer.txt`; new runs
use `logs_agent.txt`.

## Architecture

```
prolong_agent/
├── agent/
│   ├── base.py               # base architecture
│   ├── codex_agent.py        # Codex CLI backend
│   ├── claude_code_agent.py  # Claude Code backend
│   ├── swarm.py              # CLI entry point
│   ├── action_queue.py       # action execution
│   ├── game_state.py         # board/log formatting
│   └── prompts.py            # prompts (~30 lines)
├── environment/
│   ├── arcagi3.py            # ARC-AGI-3 API wrapper
│   ├── runner.py             # per-game loop
│   └── config.py
├── metrics/
└── utils/
```

This repo was formerly the Read-Grep-Bash (RGB) Agent, see our original [blog post](https://blog.alexisfox.dev/arcagi3) on the ARC-AGI-3 preview games.

## Citation

```bibtex
@misc{fox2026prolong,
  title={PRO-LONG: Programmatic Memory Enables Long-Horizon Reasoning},
  author={Fox, Alexis and Wang, Junlin and Rosu, Paul and Dhingra, Bhuwan},
  year={2026},
  eprint={2607.20064},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2607.20064},
}
```
