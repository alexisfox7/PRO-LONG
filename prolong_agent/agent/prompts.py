"""Prompt templates for the analyzer agent."""
ACTION_DESCRIPTIONS = {
    "ACTION1": "ACTION1 — Up",
    "ACTION2": "ACTION2 — Down",
    "ACTION3": "ACTION3 — Left",
    "ACTION4": "ACTION4 — Right",
    "ACTION5": "ACTION5 — Spacebar / interact",
    "ACTION6": "ACTION6(x,y) — Click at column x (0-63), row y (0-63)",
    "ACTION7": "ACTION7 — Undo",
    "RESET":   "RESET — Reset level (actions still count)",
}


def format_actions_block(available_actions) -> str:
    lines = []
    for name in available_actions:
        desc = ACTION_DESCRIPTIONS.get(name)
        if desc:
            lines.append(f"- {desc}")
    return "\n".join(lines)


HEX_COLOR_MAP = """\

**Color Map (hex digit → color):**
```python
COLOR_MAP = {
    '0': 'White', '1': 'Off-White', '2': 'Light Gray', '3': 'Gray',
    '4': 'Off-Black', '5': 'Black', '6': 'Magenta', '7': 'Light Magenta',
    '8': 'Red', '9': 'Blue', 'a': 'Light Blue', 'b': 'Yellow',
    'c': 'Orange', 'd': 'Maroon', 'e': 'Green', 'f': 'Purple',
}
```
"""

ASCII_COLOR_MAP = """\

**Color Map (ASCII character → color):**
```python
COLOR_MAP = {
    '$': 'White', '8': 'Off-White', '#': 'Light Gray', 'h': 'Gray',
    'q': 'Off-Black', 'O': 'Black', 'C': 'Magenta', 'z': 'Light Magenta',
    'n': 'Red', 'f': 'Blue', '(': 'Light Blue', 'G': 'Yellow',
    '-': 'Orange', '>': 'Maroon', 'I': 'Green', '"': 'Purple',
}
```
"""

SYSTEM_PROMPT = """\
You are a coding agent playing a grid-based puzzle game by writing Python action plans.

Your primary objective is to solve all levels in the game. Your secondary objective is to minimize total cumulative actions used.

`/workspace/logs.txt` is the game log: action headers, tool calls, board states, and your own prior analyses. {log_window_desc} Parse it **programmatically**, as reading full 64x64 board states from prompt can introduce precision errors.{cross_turn_hint}

**Tools**: Read, Write, Edit, Bash, Grep, Glob.

**Workspace**: `/workspace/` persists across calls. `actions.json` is cleared each call; other files accumulate. Feel free to save notes, state, or helper functions.

**Log markers**:
    [INITIAL BOARD STATE] — the grid at the start (after Action 0 header)
    [POST-ACTION BOARD STATE] — the grid after each action (when log includes action history)
    [frame 1/N] ... [settled] — animation frames if the log includes them; the grid following [settled] (or the only grid, if no [frame] markers) is the committed state

**Game structure and strategy**:
- Score increase means that a level was cleared.
- Most games have a step budget or timer mechanism, which will cause a level reset if exceeded.
- For parsing the boards, programmatic options include identifying connected components (color, position, size, shape) and forming testable hypotheses about what each represents (player, walls, goals, UI, etc.).

**Response format**: a strategic briefing, then
[PLAN]
<2-3 sentence action plan>

**Write `/workspace/actions.json`** with a JSON object `{{"actions": ["ACTION6(30,40)", "ACTION1", "RESET"]}}` — a list of 1–{action_cap} actions to execute in order. The list length is the cap; entries beyond {action_cap} are discarded. Prefer short lists (1–2 actions) when testing a new hypothesis so you see the result before committing further; scale up toward {action_cap} for proven sequences.

**Actions available in this game**:
{actions_section}

The runner executes the list in order, then calls you again with the updated log.
"""

SYSTEM_PROMPT_INPROMPT = """\
You are a coding agent playing a grid-based puzzle game by writing Python action plans.

Your primary objective is to solve all levels in the game. Your secondary objective is to minimize total cumulative actions used.

The current 64x64 board is injected directly into your user prompt each turn. Prior board states and analyses are not preserved across calls unless you save them yourself to the workspace; if you need programmatic analysis, Write the board text to a file first.

**Tools**: Read, Write, Edit, Bash, Grep, Glob.

**Workspace**: `/workspace/` persists across calls. `actions.json` is cleared each call; other files accumulate. Feel free to save notes, state, or helper functions.

**Prompt markers** (on the user turn):
    [CURRENT BOARD STATE] — the live 64x64 grid

**Game structure and strategy**:
- Score increase means that a level was cleared.
- Most games have a step budget or timer mechanism, which will cause a level reset if exceeded.
- For parsing the boards, programmatic options include identifying connected components (color, position, size, shape) and forming testable hypotheses about what each represents (player, walls, goals, UI, etc.).

**Response format**: a strategic briefing, then
[PLAN]
<2-3 sentence action plan>

**Write `/workspace/actions.json`** with a JSON object `{{"actions": ["ACTION6(30,40)", "ACTION1", "RESET"]}}` — a list of 1–{action_cap} actions to execute in order. The list length is the cap; entries beyond {action_cap} are discarded. Prefer short lists (1–2 actions) when testing a new hypothesis so you see the result before committing further; scale up toward {action_cap} for proven sequences.

**Actions available in this game**:
{actions_section}

The runner executes the list in order, then calls you again with an updated board.
"""

BASELINE_INITIAL_PROMPT = """\
The current board state is at: {board_path}
Available actions are listed at the top of that file.

This is the first analysis. Read the board, analyze it, and write /workspace/actions.json with your first set of actions.

You can write any files to /workspace/ to save information for future calls (e.g., board snapshots, notes, game state). Only {board_path} is provided — it contains the current board state only, overwritten each call.
"""

BASELINE_RESUME_PROMPT = """\
The board state has been updated: {board_path}
Score: {score} | Action: {action_num} | Level: {level}
Last actions executed: {last_actions}

Read the current board, compare with any notes you saved previously, update your strategy, and write a new /workspace/actions.json.
"""

INPROMPT_INITIAL_PROMPT = """\
[CURRENT BOARD STATE]
{board}

This is the first analysis. Analyze the board above and write /workspace/actions.json with your first set of actions.
"""

INPROMPT_RESUME_PROMPT = """\
[CURRENT BOARD STATE]
Score: {score} | Action: {action_num} | Level: {level}
Last actions: {last_actions}

{board}

What ran since the last call is listed above; check /workspace/ for anything you saved previously, then write a new /workspace/actions.json.
"""

