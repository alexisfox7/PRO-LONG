# Release-logs format spec

Target: a public-ready tree of agent run logs. This spec is what the Claude-side
cohorts (`fable5_*`, `opus46_*`) already follow; replicate it exactly for the
codex/GPT-5.5 cohorts.

## Tree layout

```
release_logs/
  <model>/             # gpt55 | opus46 | fable5
    <cohort>/          # <condition>[_<replabel>]  e.g. prolong_exp3, inprompt_r2
      <game>/          # 4-char game id, no version hash   e.g. ka59
        rep<N>/        # chronological by original run timestamp, 1-based
          logs.txt           # PROLONG runs only — omit for in-prompt runs
          logs_analyzer.txt
          scorecard.json
          workspace/         # the agent's sandbox working dir, complete
```

## Per-run contents

| file | prolong | in-prompt | notes |
|---|---|---|---|
| `logs.txt` | yes | **NO** | full environment game log (board states per action) |
| `logs_analyzer.txt` | yes | yes | model-side transcript, headers sanitized (below) |
| `scorecard.json` | yes | yes | as written by the harness, untouched |
| `workspace/` | yes | yes | agent sandbox (actions.json, notes.md, CLAUDE.md/AGENTS.md, level snapshots) |

## Excluded entirely (never copy)

- `checkpoint.json`, `summary.txt`, `run_info.txt`, `card_session.json`
- raw CLI session transcripts (`cc_sessions/` on claude; codex equivalent = the
  codex session/rollout jsonl dirs)
- OS / build artifacts: `.DS_Store`, `__pycache__/`, `*.pyc`

## Inclusion criteria

Only runs whose original `summary.txt` says `COMPLETED_RUN` or `TIMEOUT`.
(Check BEFORE dropping summary.txt — it is used as the filter, then not copied.)
One dir per run; multiple qualifying runs of the same game become rep1, rep2, …
ordered by original run-dir timestamp.

## Sanitization (applied to every copied file)

1. **Token redaction** — replace credentials with `[REDACTED_TOKEN]`:
   - claude: `sk-ant-oat01-[A-Za-z0-9_-]+`
   - codex: redact OpenAI/codex credentials equivalently (`sk-[A-Za-z0-9_-]{20,}`,
     any `Bearer` tokens, and anything from auth.json)
2. **Analyzer header stripping** — in `logs_analyzer.txt`:
   `--- action=N | HH:MM:SS | <backend> ---`  →  `--- action=N ---`
   (regex: `s/^(--- action=[0-9]+) \| [0-9:]+ \| [a-z-]+ ---$/\1 ---/`)
3. **Telemetry stripping** — delete `[TIMING] ...` lines from
   `logs_analyzer.txt` (per-call latency/cost/token counts; harness-side, not
   part of the agent transcript): `sed -i '' '/\[TIMING\]/d'`
   **BEFORE stripping, extract them** (with their `--- action=N` headers) to
   `cost_data/<model>/<cohort>/` — the internal input for the token-cost
   pipeline. `cost_data/` lives beside `release_logs/` in staging and is NEVER
   published. (Originals on EC2 `evaluation_results/` and wandb also retain
   full telemetry; release copies are the only stripped ones.)
4. **No dates anywhere** — run dirs are `rep<N>` (no timestamps in names);
   verify no `YYYY-MM-DD` strings survive in any file content:
   `grep -rE "20[0-9]{2}-[0-9]{2}-[0-9]{2}" release_logs/` must be empty.
   Dates can leak inside transcripts organically (agent ran `stat`/`date`, API
   error JSON, agent note headers) — scrub with
   `sed -E 's/20[0-9]{2}-[0-9]{2}-[0-9]{2}/[DATE]/g'` on affected files.

## Verification checklist (run after building)

```
# 1. no credentials
grep -rE "sk-(ant|proj)?-?[A-Za-z0-9_-]{20,}" release_logs/ | grep -v REDACTED   # empty
# 2. no dates in contents
grep -rlE "20[0-9]{2}-[0-9]{2}-[0-9]{2}" release_logs/                            # empty
# 3. no timestamps/backends left in analyzer headers (anchored — agents quoting
#    game-log "--- Action N | Level ... ---" lines are fine and match looser regexes)
grep -rlE "^--- action=[0-9]+ \| [0-9:]+ \| " release_logs/ --include=logs_analyzer.txt  # empty
# 3b. no [TIMING] telemetry
grep -rl "\[TIMING\]" release_logs/ --include=logs_analyzer.txt                # empty
# 4. no excluded files
find release_logs \( -name checkpoint.json -o -name summary.txt -o -name run_info.txt \) # empty
# 5. in-prompt cohorts have no top-level logs.txt (agent-authored files named
#    logs.txt inside workspace/ are legitimate — stateless agents keep notes there)
find release_logs/*/*inprompt* -name logs.txt -not -path "*/workspace/*"         # empty
# 6. per-cohort run counts
for c in release_logs/*/*/; do echo "$c $(find $c -mindepth 2 -maxdepth 2 -type d | wc -l)"; done
```

## Existing cohorts (for naming consistency)

fable5/: prolong, inprompt, fable_online (official online runs; see below)
opus46/: prolong_r2, prolong_r3, inprompt_r2, inprompt_r3, inprompt_r4
gpt55/:  prolong_exp1..exp11, inprompt_exp1..exp5, lw25_exp1..exp5,
         stateless_exp1..exp4, inprompt_stateless_exp1/2,
         ladder_r_exp1, ladder_rg_exp1/2, nowrite_exp2 (tool-ladder ablation)

NOTE: tree reorganized 2026-07-04 into per-model subfolders (`release_logs/<model>/<cohort>/`).
The `.tgz` archives predating this (release_logs.tgz, opus46_logs.tgz, gpt55_logs.tgz)
contain the old flat `<model>_<cohort>` layout — re-tar before publishing.

## Caveat to carry into the repo README

`scorecard.json` in offline-mode runs contains a launch-time stub entry
(`state: NOT_FINISHED, score: 0`) alongside — or instead of — the finished
entry. Authoritative trajectories are `logs.txt` / `logs_analyzer.txt`;
official scores are computed by replaying through `arc_agi` v0.9.7
(`min(115,(baseline/actions)^2*100)` per level, level-index weighting, @500 cap).

## fable_online cohort (added 2026-07-19/20)

Official arcprize.org online runs (leaderboard submissions), same per-rep layout.
Unlike offline runs, `scorecard.json` here is the SERVER's close response — the
authoritative official score (the offline stub caveat above does not apply).
`card_session.json` (recovery cookies) is excluded as a credential-adjacent
run-state artifact.

## Codex-side notes (gpt55_* cohorts, built 2026-07-04)

Cohorts: `gpt55_prolong_exp1..exp9`, `gpt55_inprompt_exp1..exp5` — 14 × 25 games,
built from inst1 `evaluation_results*/` per this spec, with three documented
amendments:

1. **Workspace mapping** — codex runs store the sandbox as `codex_sandbox/`;
   copied to `workspace/` (contains `actions.json`, `AGENTS.md`, `last_message.txt`,
   agent-written notes/scripts). `session_state.json` / `current_board.txt` are
   run-state artifacts, not copied (same rationale as `checkpoint.json`).
2. **Inclusion criterion extended for 4 runs** whose harness died at finalize
   (no `summary.txt`) or ended `ERROR` after a substantive trajectory. Scoring
   replays `logs.txt` directly, so these runs back the reported numbers and are
   included: exp3/vc33 (148 acts), exp5/bp35 (845), exp5/ft09 (52),
   exp5/su15 (922, API dropped at finish). Dead stubs (<15 acts, score 0)
   remain excluded. These 4 have no `scorecard.json` (never written).
3. **Date scrub** — agent-echoed dates inside transcripts (the model catting
   env probes / its own session paths) are replaced with `XXXX-XX-XX` rather
   than dropped, preserving transcript readability. 14 files affected.

All six verification checks pass on the merged tree.
