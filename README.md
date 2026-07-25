# PRO-LONG: Programmatic Memory Enables Long-Horizon Reasoning

PRO-LONG is a minimal memory addition for LLM agents on long-horizon tasks: the harness appends every observation, action, and outcome verbatim to a single structured log, and the agent retrieves and reasons over it programmatically (grep, Python) — no subagents, no retrieval infrastructure, a ~30-line prompt.

On the full [ARC-AGI-3](https://three.arcprize.org/) public game set, PRO-LONG improves over the same coding agents without the log by 18 percentage points on average, matches or exceeds specialized harnesses at 4.2–5.8x fewer billed tokens, and reaches **97.4% best@2 with Fable 5 at a total cost of $1,750**.

**Paper:** [arxiv.org/abs/2607.20064](https://arxiv.org/abs/2607.20064)

![Architecture](assets/prolong_architecture.png)

## Setup

Requires Python (3.12 recommended) and Docker.

```bash
git clone git@github.com:alexisfox7/PRO-LONG.git
cd PRO-LONG
python -m venv .venv
source .venv/bin/activate
pip install -e .

# build the agent sandbox image(s) for the backend(s) you use
docker build -t rgb-agent/codex-sandbox:latest docker/codex-sandbox
docker build -t rgb-agent/claude-sandbox:latest docker/claude-sandbox
```

Create a `.env` file:

```
ARC_API_KEY=...
ANTHROPIC_API_KEY=...   # claude-code backend
OPENAI_API_KEY=...      # codex backend
```

## Usage

```bash
rgb-swarm --suite all --max-actions 500                       # codex backend (default)
rgb-swarm --suite all --backend claude-code -m claude-opus-4-6
rgb-swarm --game ls20,ft09
```

### Key flags

| Flag | Default | Description |
|------|---------|-------------|
| `--backend` | `codex` | Agent backend: `codex` (OpenAI Codex CLI) or `claude-code` (Claude Code CLI) |
| `--suite` | — | Predefined game suites (e.g. `ls20`, `vc33`, `ft09`, or `all`) |
| `--game` | — | Comma-separated game names or IDs (alternative to `--suite`) |
| `--max-actions` | 500 | Max actions per game |
| `--model`, `-m` | `claude-opus-4-6` | Analyzer model |
| `--effort` | `high` | Effort level (claude-code backend) |
| `--reasoning-effort` | `none` | Reasoning effort (codex backend) |
| `--operation-mode` | `online` | `online` / `offline` / `normal` |

### Memory conditions

The analyzer's access to game history is controlled by `--log-window` (and `--workspace`). These are the ablation conditions from the paper:

| Condition | Flags | What the analyzer sees |
|-----------|-------|------------------------|
| prolong | (default) | Full game log, read from a file in its workspace |
| lw25 | `--log-window 25` | Last 25 action sections of the log |
| no-log (in-prompt) | `--log-window -1` | No log file; the current board is injected into the prompt (history limited to context) |
| stateless | `--workspace stateless` | Full log, but the workspace is wiped each call (no carried-over notes/files) |

Results are saved to `evaluation_results/`.

### Sandbox network lockdown (optional)

By default the agent container uses Docker bridge networking. For locked-down egress, build the allowlist proxy and set two env vars — the agent then runs on an internal Docker network and can reach only the LLM API through the proxy:

```bash
docker build -t rgb-anthropic-proxy docker/anthropic-proxy
docker network create --internal rgb-internal
export CLAUDE_DOCKER_NETWORK=rgb-internal
export CLAUDE_EGRESS_PROXY=http://rgb-anthropic-proxy:3128
```

## Scorecards & logs

Official online scorecards (verifiable on arcprize.org) are in [`scorecards/`](scorecards/), including all 25 Fable 5 runs behind the paper's headline result (`fable_online_scorecards.txt`). Full sanitized run logs (game logs, agent transcripts, and workspaces for every reported run) are being released separately; a link will be added here.

## Architecture

The analyzer agent (Codex CLI or Claude Code CLI) runs in a sandboxed Docker container, reads the game's log with read/grep/Python, and outputs a JSON action plan. The action queue drains these one per step with zero LLM calls. When the queue empties or the score changes, the analyzer re-fires.

```
rgb_agent/
├── agent/
│   ├── base.py               # Backend-agnostic analyzer interface
│   ├── codex_agent.py        # Codex CLI backend (Docker sandbox)
│   ├── claude_code_agent.py  # Claude Code CLI backend (Docker sandbox)
│   ├── swarm.py              # CLI entry; runs games in parallel on a scorecard
│   ├── action_queue.py       # Drains one action per step (batched plans + score-change flush)
│   ├── game_state.py         # Board/log formatting
│   └── prompts.py            # System + user prompts (~30 lines for PRO-LONG)
├── environment/
│   ├── arcagi3.py            # ARC-AGI-3 API wrapper (reset, step, scoring)
│   ├── runner.py             # Per-game orchestration loop
│   └── config.py
├── metrics/
└── utils/
```

> This repo was formerly the Read-Grep-Bash (RGB) Agent — see the original [blog post](https://blog.alexisfox.dev/arcagi3) on the ARC-AGI-3 preview games.

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
