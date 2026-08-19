# PRO-LONG: Programmatic Memory Enables Long-Horizon Reasoning

PRO-LONG is a minimal memory addition for LLM agents on long-horizon tasks. The harness appends every observation, action, and outcome to a single structured log.txt, and the agent retrieves and reasons over it programmatically (grep, Python). There are no subagents or specialized retrieval mechanisms, and the system prompt is about 30 lines.

On the full [ARC-AGI-3](https://three.arcprize.org/) public game set, PRO-LONG improves over the same coding agents without the log by 18 percentage points on average, matches or exceeds specialized harnesses at 4.2–5.8x fewer billed tokens, and reaches **97.4% best@2 with Fable 5 at a total cost of $1,750.**

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

### Memory conditions

The agent's access to game history is controlled by `--log-window`. These are the ablation conditions from the paper:

| Condition | Flags | History available |
|-----------|-------|-------------------|
| prolong | (default) | Full game log |
| lw25 | `--log-window 25` | Last 25 action sections of the log |
| no-log (in-prompt) | `--log-window -1` | No log file; the current board is added to the prompt |

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
