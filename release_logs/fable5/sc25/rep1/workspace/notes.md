# Game notes
## SCORE 4 (L4 done action 116, 29 actions). L5 layout: 3 queued rounds (purple diamond / yellow TL,TM,MM / magenta TM,MM,BM). Plug 4x4 rows 15-18 cols 35-38 in isolated plus-block. Battery top-right (cols 50-55 rows 10-14, opens down) behind maroon valve (rows 16-18) AND orange barrier (rows 20-22) in shaft cols 52-55. Magenta socket C>>C cols 15-18 rows 11-14 (top of left shaft). Orange socket C--C cols 3-6 rows 43-46 (left of bottom corridor rows 43-46, via qqqq neck rows 43-46 cols 7-10). Corridor rows 39-41 cols 11-28 with II pad; purple ""+G warp pad cols 28-31 rows 38-41; right shaft has G warp pad rows 34-39 cols 51-56. Left shaft has qq neck rows 31-34 interior cols 16-17.
## L5 plan: purple round (contract), yellow round (warp - observe destination), then position + magenta pulses (up to C>>C from left shaft; left to C--C from bottom corridor), then reach right pad/battery.
## MOVEMENT ROTATES PLUG AXIS to the movement direction (Down→vertical, Left/Right→horizontal). Fire pulses only after a move along the desired axis!
## PATTERN COLOR = ROUND EFFECT: purple '"' = contract plug (4x4→2x2); magenta 'C' = fire pulse along plug axis; yellow 'G' = warp toward battery (L2). Boxes stack = queued rounds top-first.
## L4 after purple round: plug 2x2 'f(' cols 31-32 rows 27-28. Sent: Down (→rows 29-30 bridge height) + magenta round TM,MM,BM → pulse left into C>>C socket → expect valve open. Then: Down×3, Right×~9 to battery interior (rows 35-38, cols 52-55).
## SCORE 3 (L1 a65, L2 a72, L3 a87). L3 recipe: rotate/move plug to aim axis, round → pulse fires along plug axis BOTH directions (4-wide), consumes socket → opens valve; then arrow-navigate plug to battery.
## L4: two pattern boxes (top: purple diamond TM/ML/MR/BM; below: magenta col TM/MM/BM) = likely 2 queued rounds. Plug v-axis cols 35-38 rows 19-22 in block (cols 27-46, rows 11-38). Left socket C>>C cols 7-10 rows 28-31, bridge rows 29-30. Right: green II marker cols 44-45 rows 28-29; valve >>> cols 47-49 rows 35-38; battery cols 51-56 interior rows 35-38 opening left. Grid: all gray, NO whites (?). Sent: Down×2 (plug→rows 27-30) + TM click probe.
## SCORE 2 (level 2 cleared action 72; level 1 at action 65).
## L2 recipe that worked: toggle target cells green (TL,TM,MM), celebration WARPED plug through neck to below battery, one Up docked. Total L2 = 7 actions.
## L3 MODEL: round completion fires a magenta PULSE from the plug's '(' side; pulse travels through '#' material and dissipates if it exits. Goal: aim pulse RIGHT along rows 23-24 bridge into magenta C>>C socket (cols 55-58) — presumably unlocks maroon >>>> valve (rows 34-36) so plug can descend shaft to battery. Blocked arrows ROTATE the plug (L1 sprite flips were rotations!). Plug faces: 'f'=butt, '('=pulse exit. Initial L3: '(' up.
## Cells re-arm (turn white) after each round — rounds repeatable.
## L3: plug rows 22-25 cols 35-38 in big block. Battery bottom-left rows 37-42 cols 22-26. Left shaft cols 27-30 with maroon >>>> rows 34-36 (valve?). Right socket: magenta CCCC with >> inside (cols 55-58 rows 22-25) — maybe adapter to fetch. Target: middle column TM,MM,BM (magenta). Clicks toggle; celebration warps plug.

## LEVEL 1 SOLVED (action 65, score 1). Full recipe knowledge in sections below.
## Winning formula: demo trigger (1st action consumed), complete click round(s) (white cells, reading order) to slim plug to 2x2, arrow-move plug into battery. Move distance = plug size; moves cost 2 drain, clicks 1, blocked/no-op free-ish.

## LEVEL 2 (vertical): plug 4x4 cols 31-34 rows 35-38 in bottom block; battery top rows 10-14 (opening at bottom, interior cols 31-34); narrow neck rows 27-30 interior cols 31-32 (2-wide). Target: TL,TM,MM (yellow). Plan: demo-trigger click TL, then TL,TM,MM round → 2x2 plug, then Up ×~12 through neck into battery.
## Grid cell centers unchanged: cols 25/30/35 x rows 50/55/60.
## L2 findings (actions 66-69): no demo this level; grid clicks TOGGLE green/white (double-click TL turned it off!). Completion likely = green set matches target set. Click costs 2 drain here?? (drain 10 after 4 clicks).
## L2 geometry: lower block rows 31-38 (cols 27-38), funnel rows 24-26 interior cols 31-34, NECK rows 27-30 interior cols 32-33 (PARITY: plug 31-34 halves are 31-32/33-34, neither = 32-33 — watch how caterpillar handles this), battery rows 10-14 interior cols 31-34 opening at bottom.
## Level-1 reinterpretation: rounds don't "erode" — they caterpillar-MOVE the plug 2 units toward the battery (contract/expand alternation).

## Level 1 layout (64x64, cols 62-63 are green 'II' sidebar)
- Top rows 17-22: bar structure — blue box (cols 12-16) + gray '#' bar (cols 17-38, thick rows 19-20, thin 21-22) + 'ff((' at 39-42. Hypothesis: step budget / timer bar.
- Left target box rows 50-59, cols 11-20: purple '"' pattern on '#' bg, 8x8 interior = 3x3 logical pattern. Target diamond: (r0,c1),(r1,c0),(r1,c2),(r2,c1).
- Right grid rows 47-63, cols 22-38: 3x3 cells, centers at cols {25,30,35} x rows {50,55,60}. Initial: white '$' at diamond positions, '#' gray elsewhere — SAME positions as purple target.

## Round 1 SOLVED (actions 2-5)
- Clicked demo sequence (30,50),(25,55),(35,55),(30,60) → each correct click turns cell green 'I' (stays). After final click: purple flash celebration, cells turn gray '#', top track (rows 19-22) extended +4 cols to col 42. Score still 0 → multiple rounds per level.
- Sidebar cols 62-63: green 'I' drains from top ~1 row/action (6 rows after 5 actions). 64-row budget → be efficient.
- Next-round demo does NOT auto-play; a click likely triggers it (as action 1 did).
- Correct-click feedback: cell stays green. Track likely must reach right side (~col 61?) → ~5 more rounds at +4 cols each.

## Round 2 (action 6+)
- Action 6: clicked TM(30,50) on gray grid → turned green immediately, NO demo. Same sequence repeats each round: TM(30,50), ML(25,55), MR(35,55), BM(30,60).
- Actions 7-13 queued: finish round 2 (ML,MR,BM) + full round 3 (TM,ML,MR,BM).
- Watch: if round 3 first click errs, sequences differ per round → re-learn from demo/error frames.

## Progress model (after R3, action 13)
- Rounds 1-3 done, all same sequence TM,ML,MR,BM. Success anim: plug flashes purple, cells gray, plug/fill shifts.
- Top display: battery box (cols 12-16) + track + blue plug. Plug erodes/moves LEFT ~2 cols/round: initial 39-42 → R1 39-40 → R2 37-40 → R3 37-38. Hypothesis: level ends when plug reaches battery (~col 17) ≈ 10 more rounds.
- Assembly also shifted UP 1 row after R2 (rows 17-22 → 16-21). Meaning unclear.
- Timer: sidebar drains ~1.3 rows/action (17/64 used after 13 actions). ~36 actions left ≈ 9 rounds. RACE IS TIGHT.
- Actions 14-25: rounds 4,5,6 batched. Then extrapolate plug speed; if too slow, probe alternatives (click battery/plug, different orders).

## CRISIS ANALYSIS after R6 (action 25, drain 38/64)
- Plug per settled: demo 39-42, R1 39-40, R2 37-40, R3 37-38, R4 35-38, R5 35-36, R6 33-36. = 2 cols per 2 rounds (1/round). Needs col 17 → 16+ more rounds; drain 6/round → need ~96, have 26. REPETITION IS DOOMED.
- Drain: exactly ~6 per 4-click round (1.5/action incl. celebration).
- Plan: probe battery(14,20), plug(34,20), pattern box(15,55) for hidden mechanics. Then likely RESET (fresh timer) and execute the fast path.
- If probes reveal nothing: consider that intended play = longer sequences (Simon growth) or timing-based clicks.

## Probe results (actions 26-28, drain unchanged at 38!)
- Battery click (14,20): RED error flash (all 9 cells 'n'), no drain, no penalty seen.
- Plug click (34,20): RED error flash, no drain.
- Pattern box click (15,55): diamond cells relit WHITE = back to initial idle state. No drain, no error.
- Drain model: grid click=1, round celebration=2, demo=2, non-grid probes=0. Remaining 26 ≈ 4 rounds → repetition still doomed.
- NEW HYPOTHESIS: diamond = D-pad. Try arrows: ACTION1(up)=TM, ACTION3(left)=ML, ACTION4(right)=MR, ACTION2(down)=BM. Maybe intended input, maybe free/faster. Testing demo order: 1,3,4,2.

## BREAKTHROUGH (actions 29-32)
- ACTION3 (Left) moves plug LEFT 4 cols, costs 2 drain. ACTION4 (Right) moves it right 4 (also 2 drain). ACTION1/2 (up/down): harmless sprite flip, 0 drain.
- Rounds were nearly pointless (1 col per 6 drain); arrows are 12x more efficient.
- Plug at 33-36, battery right edge col 16. 4 Left presses → docked. Drain 42/64, cost 8 → fine.
- LEVEL-2 LESSON: try arrow keys EARLY; UI elements (plug/track/battery) may be the real puzzle, side minigames may be decoys or optional.

## Blocked at col 23 (actions 33-39, drain 52/64)
- Left works only while lower track (rows 21-22, min col 23) supports plug. Plug 4-cols wide × 4 rows, stuck at 23-26. Upper track reaches col 17 but plug won't go up (Up = free no-op sprite flip).
- Blocked Left press still costs 2 drain. Remaining budget 12.
- Current test: free battery click + 1 Simon round → does round move plug 1 col past block?
- RESET PLAN if yes: reset (fresh 64): Left×4 (8 drain, plug 39→23) + ~6 rounds (36 drain) to cover cols 23→17 = ~44 total. Feasible.

## Endgame attempt 1 (drain 58/64 after action 44+round)
- Round at block: plug eroded 26→24 (edge stays 23). Rounds advance ~1 col/6 drain. 6 cols to go = 36 drain. Only 6 left → attempt doomed.
- Battery click (action 40): free, no effect.
- Probing: Down at block, then Left with 2-wide plug (cols 23-24). If Left moves it → arrows work for 2-wide plug, no reset needed... else RESET next call.
- RESET RECIPE (attempt 2): Left×4 (8 drain, 39→23) + ~6-8 rounds (36-48 drain) = 44-56 ≤ 64 ✓. Maybe leftover: check if rounds before Lefts change anything.

## 2x2 plug discovery (actions 45-46, drain 60/64)
- After round eroded plug to 2-wide: ACTION2 (Down) MOVED/clipped plug to 2x2 at cols 23-24 rows 21-22 (cost 2). Left on lower track still blocked (cost 0 this time?).
- Vertical moves DO work for small plug. Upper track rows 19-20 reaches col 17 → battery interior cols 13-16 rows 18-21.
- Now trying Up (to rows 19-20) + Left (23→19?). Timer will hit 64 → expect auto-reset; treat as data-gathering.
- Attempt-2 sketch: Left×4 (8) + 2 rounds (12, erode to 2-wide) + Down/Up maneuvers + Lefts along upper track. ~30 drain total. Verify move sizes.

## Upper track reached (actions 47-48, drain 64/64 FULL)
- Up moved 2x2 plug to rows 19-20 (upper track) ✓. Left moved it 2 cols (21-22). MOVE DISTANCE = PLUG WIDTH (4-wide moves 4, 2-wide moves 2).
- Timer now fully drained; attempt 1 still alive at action 48. Testing whether 64/64 causes reset on next action or is harmless. Plug needs ~3 more Lefts to dock (target cols ~13-16).

## ATTEMPT 2 (from action 50, drain 0)
- Timer expiry = level reset (attempt increments). Fresh: plug 39-42 4x4, drain 0.
- RECIPE: Left×4 (→23-26, 8dr) | click grid once (demo if idle, 2dr) | TM,ML,MR,BM round (6dr) → plug 2-wide 23-24 | Up (or Down+Up) → 2x2 rows 19-20 | Left×4 (23→15, dock in battery interior 13-16) | expect SCORE.
- Move distance = plug width. Costs: move 2dr, click 1dr, celebration 2dr, demo 2dr, errors/no-ops 0dr.
- Call 1 sent: Left×4 + first grid click (check: demo frames vs TM greening).

## Attempt 2 status (after action 55, drain 4)
- Action 51 (first Left of attempt): DEMO auto-replayed instead of moving. Lefts 52-54 moved plug 39→27 (4 cols each). Action 55 click TM = input registered (green), no demo needed.
- Queued (56-61): ML,MR,BM (finish round → plug erodes 2-wide, keeps LEFT half 27-28), Left×2 (→23-24), Up (test direct clip to rows 19-20; if no-op do Down,Up next).
- Then Left×4: 23→21→19→17→15 to dock. Expect score.

## Mechanics learned
- Action 1: click (30,50) → 21-frame animation. Cells flashed GREEN ('I') cumulatively at frames 2,7,12,17: top-mid(30,50), mid-left(25,55), mid-right(35,55), bottom-mid(30,60). Settled = identical to initial. Score 0.
- Hypothesis: Simon-says. Click triggers/replays demo sequence; must repeat: top-mid, mid-left, mid-right, bottom-mid.
- Action 2-5: clicking that exact sequence. Watch frames to see per-click feedback (green=correct? red=error?).
- Top bar unchanged after action 1 (not a per-action counter so far).

## Parsing tips
- Board = 64 lines after each action header line "[...BOARD STATE]".
- Grid cell value: board[ry][cx] for cx in [25,30,35], ry in [49.., 54.., 59..] (any row within cell band).

## L5 status @ action 146 (drain 34/64)
- Plug 2x2 on left pad center c29-30 r39-40. All 3 yellow warps landed on LEFT pad (origins: plus-block, c15-16 r43-44, pad itself). Right pad (G corners c52/55 r35/38, interior c53-54 r36-37) never a destination. Warp anim: plug blinks, vanishes 3 frames, reappears.
- DRAIN RE-CALIBRATION: each action ~1 drain row (sidebar 2-row blocks made it look like 2). Celebration adds ~+2. Budget = ~64 actions/attempt.
- Unexplained: green II 2x2 at c12-13 r40-41 (since level start, misaligned with plug parity — can never be covered). Hypothesis: pulse target that toggles warp destination to right pad.
- Grid note: 3x3 grid TM cell started GREEN at level init. Currently all clear.
- Purple pattern = TM,ML,MR,BM (4 cells). Yellow = TL,TM,MM. Magenta = TM,MM,BM.
- Current test: fire magenta from pad (axis should be horiz from last Left @137) -> pulse left along r39-40 hits II top row. Then yellow, then climb 12 if right pad. Fallback: purple re-fire (expand to 4x4?) then yellow, climb 6.
- Shaft valves both OPEN (rows 15-38 clear to battery interior r11-14 c51-54).

## L5 breakthrough @ action 149 (drain 38/64, 26 left)
- Magenta pulse from pad swept left rows 39-40, grazed II (12,40) -> NO effect. II likely decoration or needs something else.
- PAD SELECTION MECHANIC: outer corner markers = selected warp destination. Initial state: RIGHT pad had outer G corners (c50,55 x r34,39) = selected. At a120 (purple fire): right pad LOST outer corners, left pad GAINED purple outer corners (c27,32 x r37,42). All yellow warps since went to left pad.
- Hypothesis: purple round toggles/moves pad selection (also contracted plug 4x4->2x2 at a120). Test in flight: purple 4 clicks (TM,ML,MR,BM = (30,50),(25,55),(35,55),(30,60)) then yellow 3 clicks. If right pad re-selected -> warp lands right shaft -> climb (12 presses 2x2 from r36-37, or 6 presses if 4x4).
- Shaft is c51-54 (matches battery interior c51-54). Right pad inner slot 2x2 c52-53 r36-37.
- a117 was demo replay; grid TM cell was pre-lit at level start (purple needed only 3 clicks then).
- Click cost ~1 drain, celebration ~+1-2, moves ~1 (recalibrated).

## L5 @ action 156 (drain 48/64, 16 left) — attempt 1 dying, probing
- Purple re-fire (a150-153) = NO-OP: selection stayed on left pad, warp #4 (a156) landed left pad again. Purple is idempotent "select left/purple pad", not a toggle.
- Attempt 1 unfinishable (climb needs 12, only ~16 left and no right-pad route). Using remaining drain for probes:
  - Now: click II (12,40) and right pad interior (53,36) — test click-to-select.
  - If nothing: Left x9 to overlap plug onto II cell (12,40) (walkability + touch-trigger test).
- Attempt 2 route sketch (if a right-pad selector is found): demo, purple(3 clicks, TM pre-lit), yellow(3) -> left pad, Left x6, Up, magenta(3) [maroon socket], Down x3, Left, magenta(3) [orange socket], <trigger right-pad select>, yellow(3) -> right pad c52-53 r36-37, Up x12 -> dock. ~49 drain if trigger is cheap.

## L5 probes a157-158: board clicks are ERRORS
- Clicking II (12,40) and right pad (53,36): whole 3x3 grid flashes RED for 3 frames = error animation, 0 drain. Only the 3x3 grid cells are clickable.
- Next probe (in flight): Left x9 from pad -> plug to c11-12 r39-40, overlapping II cell (12,40). Tests II walkability + touch trigger. Watch pad corners each step.
- After: RESET, run attempt 2. Open sockets first, then whatever right-pad selector we find.

## L5 BREAKTHROUGH a159-167 (drain 46/64, 18 left)
- II BLOCK = ENERGY PICKUP: plug touched it at a166 -> timer REFILLED +8 rows (54->46). Consumed (gone from board). Green 2x2 = +8 energy.
- SIZE-MATCH WARP THEORY: outer pad corners indicate valid destination for current plug size. Plug 4x4 -> right pad outer slot c51-54 r35-38 (outer G corners shown only while plug was 4x4). Plug 2x2 -> left pad "" slot. Purple round = size toggle? (contracted at a120; re-fire on pad a153 no-op possibly because no room to expand at pad).
- ENDGAME IN FLIGHT (13 actions): purple 4 clicks (expand 2x2->4x4 at c11-14 r39-42, room verified), yellow 3 clicks (warp 4x4 -> right pad c51-54 r35-38), Up x6 (r35-38 -> r11-14 = battery interior, cols already aligned). Est 15-17 drain vs 18 left.
- If expansion fails: reset, attempt 2 recipe (~45 drain): demo, purple(3, TM prelit), yellow(3)->left pad, Leftx6, Up, magenta(3), Downx3, Left, magenta(3), Upx2+Leftx2 grab II (+8), position open area, purple(4) expand, yellow(3), Upx6 dock.

## LEVEL 5 CLEARED @ a180 (attempt 1, 64 actions on level). Score 5.
- Final: purple EXPAND 2x2->4x4 anchored TOP-LEFT (c11-12 r39-40 -> c11-14 r39-42), yellow warp 4x4 -> right pad outer 4x4 slot (c51-54 r35-38), Up x6 dock.
- CONFIRMED MECHANICS: purple round = size toggle 2x2<->4x4 (needs room, anchors top-left; no-op if no room). Yellow warp = size-matched: 4x4 -> 4x4 slot (6-apart G corners, interior 4x4), 2x2 -> "" purple-marked 2x2 slot (4-apart corners). Slot corner markers appear/disappear as plug size changes = destination indicator. II green 2x2 = +8 timer pickup on touch. Board clicks outside 3x3 grid = free error (red grid flash).
- Patterns (same in L6): purple=TM,ML,MR,BM; yellow=TL,TM,MM; magenta=TM,MM,BM. Clicks: TL(25,50) TM(30,50) TR(35,50) ML(25,55) MM(30,55) MR(35,55) BL(25,60) BM(30,60) BR(35,60).

## LEVEL 6 map (fresh, timer full, grid all clear)
- Battery c34-37 r9-12 interior, opens DOWN; shaft c34-37 r13-28 with ORANGE barrier r14-16; widens c30-37 r29-32; MIDDLE pad at bottom: G corners (30,33),(33,33),(30,36),(33,36) -> 2x2 slot c31-32 r34-35. Shaft complex ISOLATED - enter only by warping to middle pad.
- Plug 4x4 START c41-44 r21-24 under platform r17-20 c41-52; right side shaft c50-53 r21-28 -> wide c50-57 r29-32 -> c54-57 r33-35 -> RIGHT pad: outer G (53,36),(58,36),(53,41),(58,41) = 4x4 slot c54-57 r37-40; inner G (54,37),(57,37),(54,40),(57,40) = 2x2 slot c55-56 r38-39.
- Corridor r37-40: right pad <- c46-53 #### <- MAROON barrier c43-45 <- c42 # <- ORANGE socket C--C c38-41 r37-40. Orange socket pulse: horizontal along r37-40 from right pad area (needs maroon open? or pulse passes barriers - unknown).
- MAROON socket C>>C c18-21 r33-36, stem below: c17-20 r37-38, c17-18 r39-40, connects to LEFT pad: G (12,40),(15,40),(12,43),(15,43), "" 2x2 slot c13-14 r41-42. Left region is 2x2-only (no 4x4 room anywhere!).
- Solution sketch: purple contract -> yellow (destination? watch markers!) -> if left pad: Right x2, Up x2 to c17-18 r37-38, magenta (vert pulse -> maroon socket -> maroon barrier opens). Then need orange socket pulse from r37-40 corridor as 4x4 (right pad) then dock via middle pad as 2x2... EXPANSION ROOM missing in left region - open question. Maybe "" marker moves between 2x2 slots after events.
- In flight: purple 4 clicks only (contract + read marker changes to learn 2x2 destination). WATCH: does demo eat first action of new level (L5 did)?

## L6 progress @ a184 (drain 4/64)
- No demo consumption this level (a181 click registered). Purple fired a184: plug 2x2 at c41-42 r21-22 (top-left anchor).
- Marker confirmation: left pad gained outer "" corners (11,39),(16,39) = 2x2 warp destination. Right pad outer 4x4 G corners vanished (plug now 2x2). Middle pad unchanged (G 2x2 slot, not destination).
- Battery corrected: border c32-37 r8-12, interior c33-36 r9-11, shaft below c34-37 (orange barrier r14-16). Right shaft c49-52 r21-28.
- Left region: "" slot c13-14 r41-42; corridor c15-18 r41-42; stem c17-18 r39-40, c17-20 r37-38. Maroon socket C c18-21 r33-36 (interior >> c19-20 r34-35).
- In flight (10 actions): yellow (warp -> c13-14 r41-42), Right x2 -> c17-18 r41-42, Up x2 -> r37-38, magenta (vert pulse up c17-18 -> maroon socket -> maroon barrier c43-45 r37-40 opens).
- Phase 3 TODO: orange socket (C--C c38-41 r37-40) needs horizontal pulse along r37-40 from the right corridor; then dock via middle pad (2x2 slot c31-32 r34-35) — but 2x2 warp goes to LEFT pad ("" marker)... open question how to retarget middle pad. Watch markers after each round fire! Maybe "" moves when left pad's role is done, or when plug stands on "" slot the warp picks next slot... investigate.

## L6 @ a194 (drain 18/64): maroon OPEN, pickup found
- a187 warp -> left "" slot; a191 stem c17-18 r37-38; a194 magenta vert pulse consumed maroon socket -> maroon barrier c43-45 r37-40 OPEN (corridor r37-40 clear c41-52).
- Consumed socket left: II pickup (+8) at c17-18 r33-34, walkable #### c17-20 r33-36 = 4x4 expansion room!
- Left pad now shows full outer "" corners (11,39),(16,39),(11,44),(16,44) - still 2x2 destination.
- In flight (15): Up x2 (grab II, plug c17-18 r33-34), purple x4 (expand c17-20 r33-36), yellow x3 (4x4 warp -> right pad slot ~c54-57 r37-40), Left x3 (-> c42-45 r37-40), magenta x3 (horiz pulse left -> orange socket c37-40 r37-40 -> orange barrier r14-16 opens).
- REMAINING PUZZLE: dock = middle pad (2x2 slot c31-32 r34-35, isolated shaft complex). 2x2 warps go to "" marker = left pad. Hope: markers move after orange socket consumed (level guidance updates each phase). Else find expansion/room trick near corridor: contract at c42-43 r37-38, or park 4x4... watch markers next turn!

## L6 @ a209 (drain 26/64): ORANGE OPEN, dock phase
- a196 pickup +10 (drain 18->8). a200 expand ok. a203 warp -> right pad c53-56 r37-40. a209 orange socket consumed -> battery shaft r13-17 OPEN. New II pickup at c37-38 r37-38 (former socket).
- NEAREST-RULE DISPROVEN: a187 2x2 warp chose left pad though middle was nearest. "" marker = sole destination selector.
- In flight (5): Left (grab pickup, plug c37-40 r37-40), purple x4 (contract -> c37-38 r37-38). Then READ where "" appears: if middle pad -> yellow, climb ~14 (Up x2, Right x2, Up x10) to battery interior c33-36 r9-11. If left pad again -> need new idea (maybe re-expand loop misses something).

## L6 endgame @ a214 (drain 22/64)
- REINTERPRETATION CONFIRMED: G corners 3-apart = 4x4 zone corners. Active destination shown by OUTER RING (6-apart corners) that MOVES as objectives complete: a202 ring on right pad -> after orange socket consumed (a209) ring moved to MIDDLE zone c29-32 r33-36. Markers = guidance system.
- Middle zone = 4x4 slot, gateway to battery shaft c33-36 (aligned with battery interior c33-36 r9-12).
- IN FLIGHT (14): purple x4 (expand c37-40 r37-40), yellow x3 (warp -> middle c29-32 r33-36), Up, Right (align c33-36), Up x5 -> dock r9-12. Expect score 6.
