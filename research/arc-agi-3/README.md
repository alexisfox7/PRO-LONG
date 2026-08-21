# PRO-LONG research reproduction: ARC-AGI-3

This directory contains the Python research harness, scorecards, and release logs for the paper. For the coding-agent CLI, start at the [repository README](../../README.md).

PRO-LONG is a minimal memory addition for LLM agents on long-horizon tasks. The harness appends every observation, action, and outcome to a single structured log.txt, and the agent retrieves and reasons over it programmatically (grep, Python). There are no subagents or specialized retrieval mechanisms, and the system prompt is about 30 lines.

On the full [ARC-AGI-3](https://three.arcprize.org/) public game set, PRO-LONG improves over the same coding agents without the log by 18 percentage points on average, matches or exceeds specialized harnesses at 4.2–5.8x fewer billed tokens, and reaches **97.4% best@2 with Fable 5 at a total cost of $1,750.**

**Paper:** [arxiv.org/abs/2607.20064](https://arxiv.org/abs/2607.20064)

![Architecture](assets/prolong_architecture.png)

## Setup

Requires Python (3.12 recommended) and Docker.

```bash
git clone git@github.com:alexisfox7/PRO-LONG.git
cd PRO-LONG/research/arc-agi-3
python -m venv .venv
source .venv/bin/activate
pip install -e .

# codex backend
docker build -t prolong-agent/codex-sandbox:latest docker/codex-sandbox
docker build -t prolong-openai-proxy docker/openai-proxy

# claude-code backend
docker build -t prolong-agent/claude-sandbox:latest docker/claude-sandbox
docker build -t prolong-anthropic-proxy docker/anthropic-proxy
```

Create a `.env` file:

```
ARC_API_KEY=...
CODEX_API_KEY=...              # codex backend
CLAUDE_CODE_OAUTH_TOKEN=...    # claude-code backend (default)
ANTHROPIC_API_KEY=...           # claude-code backend with --api-key
```

The agent container only mounts the game workspace and, by default, has no network access except a proxy to the model API.

## Usage

```bash
prolong-swarm --suite all -m gpt-5.5 --max-actions 500
prolong-swarm --suite all --backend claude-code -m claude-opus-4-6
prolong-swarm --game ls20,ft09 -m gpt-5.5
prolong-swarm --suite all --no-log
```

Results are written to `evaluation_results/`.

### Key flags

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
| `--no-log` | off | Interactive MCP baseline with no game log in the agent workspace |
| `--in-prompt` | off | Existing current-board-in-prompt baseline |
| `--log-window N` | full log | Expose only the latest N action sections |

### Memory conditions

The harness has four explicit memory conditions:

| Condition | Flags | History available |
|-----------|-------|-------------------|
| full-log (PRO-LONG) | (default) | Full durable game log |
| windowed-log | `--log-window 25` | Last 25 action sections of the durable log |
| in-prompt | `--in-prompt` | Current board serialized into each prompt; no agent-visible log |
| mcp-no-log | `--no-log` | Live state and actions available only through authenticated MCP tools |

`--log-window -1` remains a deprecated alias for `--in-prompt`. The three
condition-selecting flags are mutually exclusive.

In the MCP no-log baseline, each game gets a short-lived, bearer-authenticated
[Streamable HTTP MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
endpoint with two tools: `current_board` and
`submit_actions`. Tool results enter the coding CLI's native resumed context,
but the runner does not expose an explicit durable game log, serialize an
observation into a prompt, or mount the private trace into the CLI workspace.
Normal coding tools and persistent helper files remain available. A private
host-side `logs.txt`, agent transcript, and usage record are retained for
evaluation and debugging. If a CLI process exits before the live game ends,
the runner resumes the same CLI session with a state-free prompt. In this
condition, `--retries` is the maximum number of consecutive resumed calls that
may execute zero actions before the run is marked `AGENT_STALLED`.

## Scorecards & logs

`scorecards/` contains the official online scorecards, including all 25 Fable 5 runs from the paper (`fable_online_scorecards.txt`); each can be verified on arcprize.org. `release_logs/` contains logs for the Fable 5 online runs: game logs, agent transcripts, and workspaces. Logs for the remaining ablations will be added.

## Architecture

```
prolong_agent/
├── agent/
│   ├── base.py               # base architecture
│   ├── codex_agent.py        # Codex CLI backend
│   ├── claude_code_agent.py  # Claude Code backend
│   ├── swarm.py              # CLI entry point
│   ├── memory.py             # explicit memory-condition resolution
│   ├── action_queue.py       # action execution
│   ├── game_state.py         # board/log formatting
│   └── prompts.py            # prompts (~30 lines)
├── environment/
│   ├── arcagi3.py            # ARC-AGI-3 API wrapper
│   ├── game_session.py       # shared state, metrics, trace, and action execution
│   ├── mcp_game.py           # authenticated per-game MCP tools
│   ├── runner.py             # queued and interactive per-game loops
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
