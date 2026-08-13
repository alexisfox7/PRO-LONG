# Game notes

## Level 1 initial layout
- Green piece: cols 28-32, rows 9-11 (5x3), h-strip left edge (col 27), maroon dot at (31,10)
- Yellow piece: cols 9-11, rows 28-35 (3x8), h-strip top (row 27), maroon dot at (10,34)
- Diamond targets (hollow, maroon): centers (52,10) for green, (10,52) for yellow
- Instruction boxes: green = horizontal mirror (C open-right -> open-left); yellow = vertical mirror. Could also be 180 rotation (ambiguous from shapes).
- Row 63: full gray bar — possible step budget/timer
- Colors: I=Green, G=Yellow, >=Maroon, h=Gray, #=LightGray, q=Off-Black, O=Black

## Hypotheses
1. Click piece to select, click destination to move; flip per instruction box applied.
2. Alternative: clicking piece launches it away from h-strip.

## Findings
- Call 1 result: clicks at (30,10) piece-interior and (52,10) diamond center did NOTHING to pieces.
  Only change: bottom bar row 63 depleted right-to-left: action1 cost 1 cell (63,63), action2 cost 2 cells (61-62,63). Bar = step budget, 64 cells, 61 left. Cost may escalate or vary by click validity.
- Hypothesis 1 (select then place) DEAD.
- Geometry: if green piece is horizontally flipped and placed spanning cols 51-55, its dot (offset 3->1) lands exactly on diamond center (52,10). Yellow flipped vertically spanning rows 51-58 puts dot at (10,52). So goal = flipped piece translated so dot fills diamond hole.

## Key insight (call 3)
- Instruction boxes = demo of REFLECTION across h mirror line: left pattern reflects across central h column (col 42) to right pattern (v -> 2m-v). Yellow box same, vertical.
- Hypothesis 3: clicking an empty cell in line with a piece places a mirror there; piece reflects across it.
- Yellow: mirror at row 43 -> piece rows 28-35 reflects to 51-58, dot 34->52 = diamond center EXACT.
- Green: parity problem — dot col 31 (odd) can never reach 52 (even) via integer-column reflection. m=41 gives dot at 51 (diamond left cell), m=42 gives 53. May need boundary mirror or different target interpretation.

## Actions taken
- Call 1: ACTION6(30,10), ACTION6(52,10) — no effect (budget -1, -2).
- Call 2: ACTION6(31,10) dot, ACTION6(27,10) h strip — no effect (budget -1, -1). Budget 59/64.
- Call 3: ACTION6(10,43), ACTION6(41,10) — NO EFFECT again. 6 clicks total, zero response. Budget 56/64 (costs: 1,2,1,1,1,2).
- Parity insight: green needs a 2-cell-wide mirror at cols 41-42 (v->83-v maps dot 31->52, piece 28-32 -> 51-55 exact diamond fit). Yellow needs 1-wide mirror at row 43. So mirrors are DRAWN/painted, maybe multi-cell, maybe via 2-click segment endpoints or select-piece-then-click.
- Call 4 battery: (9,43),(11,43) [segment endpoints for yellow mirror row 43], then (10,30) [select yellow piece], (10,43) [then mirror cell]. Diff each action to see which (if any) triggers painting/reflection.
- Call 4 result: ALL four still no-ops. 10 clicks, zero response. Budget 51/64. Coords confirmed x=col,y=row via log Tool Call lines.
- New theory: game only responds to the exactly-correct click ("answer cell"); wrong clicks silently cost budget.
- Call 5 battery (answer-cell candidates): (23,10) = green dot reflected across piece's own mirror col 27; (10,20) = yellow dot reflected across its mirror row 27; (10,52) = yellow diamond center (never tried; green's center (52,10) was tried+silent); (51,10) = a diamond '>' cell.
- Note: both diamond centers = piece_start+24 on the relevant axis (28->52).
- Call 5 result: all 4 silent again. 14 clicks, zero response. Budget 46/64. Cost-2 drains at actions 2,6,9,13 (roughly every 3.5 — likely time-based extra drain, ~1.3/action avg).
- KEY GEOMETRY (call 6): mirror-to-diamond distance = 25 for BOTH pieces (27->52). Mirror strip span (rows/cols 9-11) EXACTLY matches diamond span. Virtual-image theory: diamond reflected across mirror lands at (2,10) green / (10,2) yellow.
- Call 6 battery: (2,10), (10,2) [reflected diamond centers], then (52,10) twice consecutively [double-click test].
- Call 6 result: silent again ((2,10),(10,2),(52,10)x2). 18 clicks, zero response. Budget 41/64.
- All single-click reflection theories now DEAD: dot->diamond needs mirror 41.5 (green parity fail); yellow's clean candidates (10,43) etc all tried+silent. Double-click dead. Virtual images dead.
- Call 7: paired grab-drop test: (31,10)->(52,10) [green dot then diamond center], (10,34)->(10,52) [yellow pair].
- Call 7 result: dot->target pairs SILENT too. 22 clicks, zero response ever. Budget 36/64.
- Call 8: RESET (test intro-state/budget-restore), then (42,21) demo mirror center, (32,63) budget bar cell.
- Call 8 result: RESET REFILLS THE BUDGET BAR fully (only change). Demo mirror (42,21) and bar (32,63) clicks silent. Budget ~61/64 now. RESET is a safety valve — use before bar empties.
- Call 9 theories: (A) draw the missing reflection cell-by-cell in image regions [green cols 22-26 rows 9-11; yellow cols 9-11 rows 19-26]; (B) off-by-one indexing.
- Call 9 battery: (26,10),(22,9),(24,11) [green image cells], (10,26),(9,19) [yellow image cells], (10,42),(10,44) [off-by-one around mirror-row-43 candidate], (52,9) [diamond arm].
- Call 9 result: all 8 silent (image-region cells, off-by-one, arm (52,9)). Draw-theory ~dead. 33 actions, zero response.
- Call 10 battery (12): yellow mirror cells (10,27); green mirror ends (27,9),(27,11); image center (24,10); ALL remaining diamond arms (53,10),(52,11),(10,51),(9,52),(11,52),(10,53); demo panel interiors (39,21),(45,21).
- After this: only systematic sweeps remain. RESET refills budget so sweeps are affordable: ~18 clicks+RESET per call.
- BREAKTHROUGH call 10: demo panels are BUTTONS that move the associated piece 3 cells along its axis!
  - Green box left panel center (39,21): piece moved LEFT 3 (dot 31->28; cells at/past mirror col 27 clipped/hidden, restored when moving back).
  - Green box right panel center (45,21): piece moved RIGHT 3 (restored exactly).
  - Yellow box: top panel (24,38)=up 3 (assumed), bottom panel (24,44)=down 3 (assumed).
- Movement step=3 explains the reflection-parity dead end. Goal: dot onto diamond center.
  - Green: dot 31->52 = 7 presses of (45,21). Yellow: dot 34->52 = 6 presses of (24,44).
- Call 11: exactly those 13 presses. Watch for: step size deviation, obstacles, level-clear (Score 1) mid-batch.
- Note ~36/64 budget left before this batch; RESET refills if needed.

## LEVEL 1 SOLVED (action 58, Score 1)
- MECHANIC CONFIRMED: panel buttons STRETCH the piece by 3 cells per press along its axis (base anchored at the mirror h-strip); the maroon dot rides near the leading edge. Level clears when each dot lands on its diamond center (filled '+' of maroon appears).
- Toward-mirror panel (left/top) retracts by 3; away panel (right/bottom) extends by 3.
- Green box panels: (39,21) retract, (45,21) extend. Yellow box: (24,38) retract, (24,44) extend. (Level 1 coords; may shift per level.)
- Solution was 7 extends green + 6 extends yellow (dot 31->52, 34->52; step 3).
- WARNING: log board sections may include a "[frame 1/1]" line before the grid — offset by 1 when parsing.
- Call 12: probe ACTION6(0,0) to render Level 2 initial state.

## LEVEL 2 (Score 1, from action 59)
- 4-link telescoping arm: wall -> ORANGE (h col9 rows39-41, cols10-11, extends RIGHT) -> BLUE (h row41, cols12-14, rows39-40, extends UP) -> YELLOW (h col12 rows36-38, cols13-14, extends RIGHT) -> GREEN (h top row36 cols15-17, rows37-38, extends DOWN, dot (16,37), dot rides 1 behind leading edge, center column).
- Purple walls: bar rows9-11 cols33-56; left wall cols33-35 rows9-26; mid wall cols42-44 rows15-44. Gap over mid wall: rows12-14. Diamond center (53,31).
- Button boxes row54-60: orange cols3-15 (retract (6,57)/extend (12,57)), blue cols18-30 ((21,57)/(27,57)), yellow cols33-45 ((36,57)/(42,57)), green cols48-60 ((51,57)/(57,57)).
- Residue: 53-16=37 not mult of 3 -> plan relies on CLAMP at right board edge col 63 (yellow 8th extend partial +1). UNVERIFIED. If blocked press = no-op instead, need different residue-breaker.
- FULL PLAN: orange extend x8, blue extend x8, yellow extend x8 (clamp), yellow retract x3, green extend x6 -> dot (53,31).
- Call 13: phase 1+2 = 8x(12,57) + 8x(27,57). Verify: orange grows to cols10-35, blue tower at cols36-38 rows15-40, yellow rows12-14, green cols39-41 rows13-14.
- Call 13 result: PERFECT match. Dot at (40,13). Kinematic model confirmed; each press = full 3-cell move when unobstructed.
- Call 14 (endgame): 8x yellow-extend, 3x yellow-retract, 6x green-extend.

## LEVEL 2 SOLVED (action 92, Score 2)
- Final plus filled at center (52,31): my diamond-center read was 1 off (was actually 52,31) AND the blocked 8th yellow press was evidently a NO-OP — the two errors canceled. LESSONS:
  1. Blocked extend press = NO-OP (no partial clamp). Residue arguments must use exact geometry.
  2. Always verify diamond center programmatically, not by eye.
- Mechanics summary now solid: color-matched button boxes, left panel=retract 3, right panel=extend 3, blocked=no-op, dot rides 1 behind leading edge in center column, level clears when dot = diamond center.
- Call 15: probe (0,0) to render Level 3.

## LEVEL 3 (Score 2, action 93+)
- Links: magenta z (anchor top row3 cols48-50, extends DOWN, dot (49,4)); light-blue ( (anchor col6 rows27-29, extends RIGHT, dot (7,28)); red n (cols27-29 rows18-37, anchor h row38, extends UP, carries WIDE BAR 8-block cols27-50 rows15-17 on tip); blue f (anchor col32 rows36-38, extends LEFT, carries red's anchor); orange - (cols39-55 rows21-23, anchor col56, extends LEFT); green I (cols54-56 rows24-25, anchor row26, extends UP, carries orange's anchor).
- Free block: strip 8 cols36-38 rows21-38. Static: purple wall cols45-47 rows27-29, box frames rows45-51 & 54-60 (cols 7-19,26-38,45-57), floor row63.
- Diamonds: (43,28) for blue-( dot, (49,28) for magenta dot.
- Buttons: red L(10,48)/R(16,48); blue-( L(29,48)/R(35,48); orange L(48,48)/R(54,48); blue-f L(10,57)/R(16,57); magenta L(29,57)/R(35,57); green L(48,57)/R(54,57). L=retract, R=extend.
- OLD PLAN (push strip LEFT) FAILED: orange pushed strip only to cols 30-32 (2 of 5 presses worked, rest no-ops) — extended blue-f BODY (cols 21-29 rows 36-38) blocks it. RULE LEARNED: free blocks may cover ANCHORS (h cells) but NOT link bodies.
- DEADLOCK found: strip at cols 30-32 rows 27-29(ish) can never exit corridor (left=f-body/red, down=middle box frame cols 26-38 row 45, right needs (-link which red blocks). Only escape: RESET.
- Level-3 budget drain is LOW: ~0.33/action (vs ~1.3 on levels 1-2). 66-action plan fits easily post-RESET.
- REVISED PLAN (push strip RIGHT to cols 39-41, which has clear descent between frames at cols 26-38 and 45-57):
  A (this call, 15 actions): RESET; orange-ret x4 (48,48) -> orange cols 51-55; f-ext x5 (16,57) -> red cols 12-14, bar cols 12-35; red-ret x5 (10,48) -> red tip rows 33-37, bar rows 30-32 (bar cols 12-35 clears strip cols 36-38).
  B: (-ext x10 (35,48) tip->col 38 pushing strip to cols 39-41; (-ret x9 (29,48) tip back to 11.
  C: red-ext x5 (16,48) bar back to rows 15-17; f-ret x2 (10,57) red->cols 18-20, bar cols 18-41 (now OVER strip); red-ret x5 (10,48) bar descends pushing strip down cols 39-41 to floor (strip rows 33-50).
  D: (-ext x12 (35,48) dot->(43,28); z-ext x8 (35,57) dot->(49,28). Level clear.
- Call 17 (phase A) result: red at 12-14 tip 33, bar 12-35 rows 30-32 ✓; BUT orange retracts DRAGGED the strip (strip attached to orange tip!): strip 36-38 -> 45-47 over purple wall (3 retracts ok, 4th NO-OP: strip can't enter cols 48-50, diamond2 zone). Then on next effective action the wall-overlap was EXPELLED: strip snapped left to 42-44 dragging orange tip 48->45.
- NEW RULES: (a) free strip is adjacency-attached to orange tip: dragged on retract, pushed on extend; detaches only via perpendicular (vertical) movement. (b) strip may transiently cover purple wall but gets expelled next action. (c) bar renders over red body; bar always spans [red_left, red_left+23].
- CURRENT STATE: strip cols 42-44 rows 21-38 (covers diamond1); orange 45-55 tip 45; red cols 12-14 tip 33, bar 12-35 rows 30-32; f body 15-31; ( at 7-8 dot (7,28); z rows 3-5 dot (49,4). Cols 42-44 have clear descent gap (frames at cols 26-38 & 45-57).
- Call 17b result: red-ext x4 + f-ret x3 OK (bar rows 18-20 cols 21-44, red cols 21-23 tip 21). red-ret #1: bar descended ONTO strip top WITHOUT pushing it (overlap rendered); red-ret #2-4 NO-OP. orange-ret #1 (action 12): triggered EXPULSION of the bar overlap (bar+red reverted up 3 to rows 18-20/tip 21) AND dragged strip onto wall 45-47 (orange tip 48). orange-ret #2 no-op (strip-on-wall state blocks further drags).
- RULE: bar CANNOT push the strip vertically. Any illegal overlap (bar-on-strip, strip-on-wall) is transient and gets expelled during the next effective action, reverting the mover.
- SOLUTION INSIGHT: green I link carries orange's ANCHOR -> green-extend LIFTS orange body; strip glued to orange tip should lift too. Lift strip 12-15 rows -> strip band rows ~6-26 clears corridor rows 27-29, wall, and f rows 36-38. Then drag strip right past wall to cols 51-53 via orange-ret x3 (tip 54). Corridor then clear for both dots.
- Call 18 result: LIFT FAILED. green-ext #1 lifted orange to rows 18-20 but strip stayed (separation = ILLEGAL TRANSIENT); green-ext #2-5 refused; orange-ret #1 REVERTED the lift AND dragged strip onto wall 45-47 (tip 48); #2-3 refused.
- CONFIRMED RULES: strip CANNOT move vertically at all (bar push illegal, lift separation illegal). Strip glued to orange horizontally, confined to cols<=44 (wall) and >=~32 (f). Strip ALWAYS straddles corridor rows 27-29. Orange body always covers cols 48-50 rows 21-23 (tip cannot pass 48 due to glue+wall).
- THEREFORE the level is only solvable if LINK BODIES PASS UNDER free blocks (and likely under other link bodies) — moving-strip-into-link is blocked, but moving-link-under-strip is untested. Diamond1 (43,28) currently sits under strip cell; diamond2 (49,28) approach passes under orange rows 21-23.
- Call 19 batch (17): f-ext x1 (16,57) [triggers expulsion: strip->42-44, orange tip->45; red->18-20, bar->cols 18-41]; red-ret x4 (10,48) [tip 33, bar rows 30-32 cols 18-41, corridor cleared of red/bar]; (-ext x12 (35,48) [tip 8->44; presses 1-11 clear, press 12 enters strip cols 42-44 = PASS-UNDER TEST; dot->(43,28)].
- Call 19 result: ALL 17 executed. PASS-UNDER CONFIRMED: (-ext #12 committed (dot cell (40,28) became body; new body/dot at 42-44 hidden UNDER strip rendering). ( dot now at (43,28) = diamond1. RENDER ORDER: diamonds > strip > links.
- Call 20 result: PASS-UNDER IS FALSE — ('s 12th press was EXPELLED (dot back at (40,28), tip 41). z extended to rows 3-23, its push into orange rows 21-23 committed transiently (z renders over orange) then presses 7-8 refused = pending-illegal; z will revert to tip 20 on next effective action.
- BREAKTHROUGH MODEL FIX: the strip is ORANGE'S RIGID T-HEAD (like red's bar): sits at tip-3..tip-1 columns, rows 21-38, moves with orange in ALL directions. The failed green-lift was NOT a glue violation — the BAR (then at cols 21-44 rows 18-20) blocked the strip's rise at cols 42-44! Bar now at rows 30-32 cols 18-41 -> lift path clear.
- Diamond centers VERIFIED programmatically: (43,28) and (49,28).
- ENDGAME (22 actions): Call 21 (14): f-ext x1 (16,57) [harmless; triggers z expulsion to tip 20; red->15-17, bar->cols 15-38]; z-ret x5 (29,57) [tip 20->5, dot (49,4), clears cols 48-50 rows 6-20]; green-ext x4 (54,57) [lift orange+strip 12 rows: orange rows 9-11, strip rows 9-26 at cols 42-44]; orange-ret x3 (48,48) [tip 45->54, strip ->cols 51-53 rows 9-26, crossing wall cols legally since rows differ]; (-ext x1 (35,48) [tip 44, dot ->(43,28) DIAMOND1].
  Call 22 (8): z-ext x8 (35,57) [descend cols 48-50 rows 6-29, now fully clear; dot ->(49,28) DIAMOND2 -> LEVEL 3 CLEAR].
- Call 21 result: ALL 14 PERFECT. T-head model confirmed (strip lifted with orange each green press). Strip now cols 51-53 rows 9-26; orange 54-55 rows 9-11; z home rows 3-5; ( dot ON (43,28). Score still 2 (needs both diamonds).
- Call 22: z-ext x8 (35,57) -> dot (49,28) -> LEVEL 3 CLEAR (Score 3). Then probe (0,0) next call for Level 4.

## LEVEL 3 SOLVED (action ~183, Score 3)
- Final mechanics summary (CRITICAL for future levels):
  1. Links: anchor h strip, extend/retract 3/press via color-matched button boxes (L=retract toward anchor, R=extend). Dot rides 1 behind tip center.
  2. T-HEADS: perpendicular blocks attached rigidly just beyond a link's tip (red's 24x3 bar; orange's 3x18 strip). They move with the link in ALL directions (including when the link's anchor is carried by another link, e.g. green lifting orange). NOT free blocks.
  3. Collisions: blocked press = no-op. Sometimes an overlapping/separating move half-commits = ILLEGAL TRANSIENT state: same-piece presses refuse; next different-piece press applies its own effect AND reverts/expels the transient.
  4. Nothing passes under anything; render order (diamonds > blocks > links) can HIDE cells — parse diffs, don't trust visuals.
  5. Kinematic chains: link anchors ride other links' tips/T-heads.
- Solution route: park T-strip out of the corridor by LIFTING orange (green-ext x4) then retracting orange x3 (strip to cols 51-53 rows 9-26); ( ext to dot (43,28); z ext x8 to (49,28).
- Call 23: probe (0,0) to render Level 4.

## LEVEL 4 (Score 3, action 185+)
- Diamond (31,10). Yellow dot-link: cols 30-32, body rows 42-43, dot (31,43), anchor h row 44, extends UP. Path col 30-32 rows 11-41 EMPTY.
- 4 passive yellow 2x3 riders on carrier links: G1 on green I (cols 9-11 rows 18-19, anchor row 20, ext UP; G1 cols 10-11 rows 15-17 + its h col 9); G2 on orange (cols 18-20 rows 27-52 TALL, anchor row 53, ext UP; G2 cols 19-20 rows 24-26); G3 on f (cols 52-54 rows 15-16, anchor row 17; G3 cols 52-53 rows 12-14); G4 on red (cols 46-48 rows 21-22, anchor row 23; G4 cols 46-47 rows 18-20).
- Boxes: green L(6,48)/R(12,48); f L(52,48)/R(58,48); orange L(6,57)/R(12,57); yellow-dot L(28,54)/R(34,54); red L(52,57)/R(58,57).
- Call 24 result: ALL 5 yellow links extend on ONE button (same color = same control). Gs are 3-tall horizontal links extending toward center: G1 rows 15-17 ext RIGHT (tip 11+3k), G2 rows 24-26 ext RIGHT (tip 20+3k), G3 rows 12-14 ext LEFT (tip 52-3k), G4 rows 18-20 ext LEFT (tip 46-3k); dot at row 43-3k. Press 6: dot tip entered G2's band = PENDING-ILLEGAL (dot at (31,25) overlapping); presses 7-11 refused.
- PLAN: park Gs out of dot column band (cols 30-32 rows 9-43) at k=11: G1->rows 0-2 (green-ext x5), G3->rows 3-5 (f-ext x3), G4->rows 6-8 (red-ext x4), G2->rows 45-47 (orange-ret x7, MUST happen at k<=3 so G2 tip<=29 doesn't cross dot column during descent; hence yellow-ret x2 first). Then yellow-ext x8 (k=3->11): dot->(31,10). G2 will hit right button box (cols 49+) at k=10,11 — RISK: hoping blocked individual link stalls independently without blocking the others.
- Call 25 batch (14): green-ext x1 (12,48) [triggers expulsion of pending; also 1st lift], yellow-ret x2 (28,54), orange-ret x7 (6,57), green-ext x4 (12,48).
- VERIFY: expulsion revert semantics (dot only vs whole press 6); yellow-ret allowed after expulsion; G2 rows 45-47 cols 19-29; G1 rows 0-2 cols 10-20.
- Call 25 result: PERFECT. Expulsion fully reverted press 6 (k back to 5, all 5 links); yellow-ret worked post-expulsion (k=3, dot (31,34)); G2 at rows 45-47 cols 19-29; G1 at rows 0-2 cols 10-20. NOTE: expulsion reverts the ENTIRE multi-link press, and same-color retract IS allowed after expulsion.
- Call 26 result: ALL 15 executed; dot reached (31,10).

## LEVEL 4 SOLVED (action ~225, Score 4)
- KEY RULE LEARNED: same-color links all move on one button; a BLOCKED member link stalls INDEPENDENTLY (others continue). Pending-illegal overlap reverts the whole multi-link press.
- Solution: park gates in bands (G1 rows 0-2 via green x5, G3 rows 3-5 via f x3, G4 rows 6-8 via red x4, G2 rows 45-47 via orange-ret x7 at k<=3 after yellow-ret x2), then yellow-ext x8.
- Call 27: probe (0,0) for Level 5.

## LEVEL 5 (Score 4, action 226+)
- green1: body cols 10-11 rows 9-11, dot (10,10), anchor col 9 rides orange1 tip (orange1 cols 9-11, anchor row 6, ext DOWN, body 7-8).
- orange2: cols 42-44 rows 7-8 ext DOWN (same button as orange1) — will stall on f body (rows 30-32) at tip 29 after 7 presses.
- ( link: anchor col 21 rows 24-26, body to col 38, tip carries FILLED plus at (37,25) = pre-filled diamond, DO NOT TOUCH.
- f: rows 30-32 cols 33-56, anchor col 57 rides green2 tip (green2 cols 55-57 rows 33-34, anchor row 35, ext UP); f tip carries 888 T-head cols 30-32 rows 30-47.
- green2 shares green button; will stall when f rises into ( body (press 2+).
- Purple walls: cols 15-17 rows 9-17 & 21-26; block cols 36-38 rows 36-38. Hollow diamond: (22,37).
- Boxes rows 55-59: f L(6,57)/R(12,57); orange L(21,57)/R(27,57); green L(36,57)/R(42,57); ( L(51,57)/R(57,57).
- Call 28 (13): orange-ext x9 (27,57) [green1 band -> rows 36-38, dot (10,37); orange2 stalls at 7]; green-ext x4 (42,57) [dot -> (22,37); green2 stalls at 2+] -> LEVEL CLEAR expected.

## L5 UPDATE (call 29, actions 227-239)
- Orange-ext x7 committed: green1 band rows 30-32, dot (10,31); orange2 body rows 7-29 (tip 27-29).
- Press 8 (a234) REVERTED AT SETTLE: frame showed both oranges move, orange2 tip entered f body (42-44,30-32) -> FULL revert. NEW RULE: same-color press with any member collision = whole press animates then auto-reverts at settle (no pending-illegal). At-limit members skip (L4), colliding members veto.
- Green presses (a236-239) reverted: f rising to rows 27-29 hits orange2 tip (42-44,27-29). Mutual deadlock.
- PROOF of deadlock: f T-head (888, cols tip-3..tip-1, rows band..band+17, rigid) cannot pass purple 3x3 (36-38,36-38) if static -> f tip <=36 -> f body always covers cols 42-44 -> orange k=9 impossible -> level unsolvable. HENCE hypothesis: purple 3x3 is PUSHABLE by T-head.
- Call 29 batch (11): f-ret x5 (6,57) [tip 33->48, T-head ->45-47, purple pushed ->48-50]; orange-ext x2 (27,57) [band ->36-38, dot (10,37)]; green-ext x4 (42,57) [dot ->(22,37)] -> CLEAR expected. Worst case (purple=wall): only f-ret1 commits, rest revert harmlessly.
- green2 is cols 54-56 (not 55-57). f: band 30-32, tip 33, body to col 55, anchor col 56. Budget 58/64, ~0.46/action.

## L5 call 30 (after actions 240-250)
- a240 f-ret1 committed (tip 36, T-head cols 33-35 rows 30-47). a241-250 ALL reverted: purple 3x3 (36-38,36-38) is STATIC WALL, not pushable.
- NEW HYPOTHESIS: static-scenery collision -> that member stalls independently (L4 button-box precedent); link-vs-link collision -> whole press reverts (a234 proof).
- MASTER PLAN (27 actions): A: orange-ret x5 (21,57) [k 7->2, green1 band ->15-17, orange2 tip 12-14]. B: (-ret x2 (51,57) [tip 38->32, dot off diamond - MUST restore at end]. C: green-ext x4 (42,57) [press1: green1 tip 11->14 legal; presses 2-4: green1 STALLS on wall cols 15-17, f rises alone 30-32 -> 18-20]. D: f-ret x4 (6,57) [tip 36->48, T-head rows 18-35 passes OVER purple 3x3, body -> cols 48-55]. E: orange-ext x7 (27,57) [k->9, green1 band 36-38, dot (13,37); orange2 tip 33-35 clear]. F: green-ext x3 [tip 14->23, dot -> (22,37)]. G: (-ext x2 (57,57) [dot back to (37,25)] -> CLEAR.
- THIS CALL: batch 20 = A5,B2,C4,D4,E5 (k->7). Next call: E2 (27,57), F3 (42,57), G2 (57,57).
- FALLBACK if stall-hypothesis wrong: C2-4, D, E(k=7) revert; state = k=6 band 27-29, green1 tip 14, f 27-29, ( retracted. Then: green-ext x3 commits (band 27-29 legal, f ->18-20, tip 23), then next call f-ret x4, orange-ext x3, (-ext x2 -> clear.
- Budget after a250: check row63. ~52/64 expected.

## L5 call 31 (after actions 251-270)
- RULE CORRECTION: static collisions ALSO fully revert the press (a259-261: green1 tip 14->17 vs wall vetoed everything). L4 "independent stall" must have been at-limit skip, NOT static stall. ALL collisions veto; only at-limit members are skipped.
- State after a270: orange k=6 (green1 band 27-29, tip 14, dot (13,28); orange2 tip 24-26); f band 27-29, tip 36, T-head cols 33-35 rows 27-44; ( tip 32, dot (31,25), diamond (37,25) hollow; green2 tip cols 54-56 rows 30-32.
- WINNING ROUTE (26): S1 orange-ret x3 (21,57) [k->3, band 18-20, green1 tip 14 crosses wall rows fine unextended-ish]; S2 green-ext x3 (42,57) [tip->23 via gap rows 18-20; f rises ->18-20]; S3 f-ret x4 (6,57) [tip->48, T-head rows 18-35 passes ABOVE purple 3x3 and orange2 (rows<=17); body->cols 48-55]; S4 green-RET x4 (36,57) [tip->11, f back down ->30-32, harmless at cols 48-55]; S5 orange-ext x6 (27,57) [k->9, green1 unextended crosses wall, orange2 passes cols 42-44 freely, band->36-38, dot (10,37)]; S6 green-ext x4 [tip->23, dot->(22,37)]; S7 (-ext x2 (57,57) [dot->(37,25) refill] -> SCORE 5.
- THIS CALL: S1-S5 = 20 actions. NEXT CALL: S6 x4 (42,57) + S7 x2 (57,57) = 6 actions -> CLEAR.

## L5 call 32 (after actions 271-290): S1-S5 ALL COMMITTED
- State: green1 band 36-38, tip 11, dot (10,37); orange k=9 (orange2 tip 33-35); f band 30-32 body cols 48-55, T-head cols 45-47 rows 30-47; ( tip 32 dot (31,25); diamond (37,25) hollow; (22,37) hollow.
- THIS CALL: S6 green-ext x4 (42,57) [dot (10,37)->(22,37)] + S7 (-ext x2 (57,57) [dot ->(37,25)] -> SCORE 5 / LEVEL 5 CLEAR expected on final press.
- Next call: expect Level 6 board rendered; analyze fresh.

## LEVEL 6 (Score 5, action 296+). Fresh budget 64.
- Chain: GREEN vertical cols 39-41 (anchor row 17, body rows 12-16, k=1, ext UP) carries YELLOW anchor (col 39 rows 9-11); YELLOW horizontal (body cols 40-47 rows 9-11, k=2, ext RIGHT) carries BLUE anchor (cols 48-50 row 9); BLUE ext DOWN (body rows 10-11, k=0), tip = 3x3 head rows 12-14 cols 48-50 with DOT at (49,13).
- Walls (purple): rows 27-29 cols 3-8 & 18-59 (GAPS: cols 0-2, 9-17, 60-63); left col 3-5 rows 27-41; right cols 57-59 rows 30-41; bottom rows 39-41 cols 45-59.
- Hollow diamond (52,34) inside chamber (rows 30-38, cols 18-56; open from below at cols 6-44 and via left gap).
- PROBLEM: blue head at (52,34) would need blue body crossing wall rows 27-29 at cols 51-53 -> impossible. Yellow min reach col 43, gap is cols 9-17 -> unreachable. Standard moves CANNOT solve -> the 3 icon boxes must matter.
- NEW UI: 3 icon boxes rows 45-51 with filled plus icons: f-box center (12,48), G-box (31,48), I-box (50,48). Unknown mechanic - probing f-box click.
- Button boxes rows 54-60 (new 13-wide layout): f-L(9,57) f-R(15,57); G-L(28,57) G-R(34,57); I-L(47,57) I-R(53,57). L/R semantics presumed retract/extend (unverified this level).
- Call 33: probe ACTION6(12,48).

## L6 call 34 (after action 297)
- ICON BOX = ROTATE LINK 90 deg, pivot at anchor, k preserved. Blue went DOWN->RIGHT on center click (12,48). Blue now: anchor col 48 rows 9-11 (vertical strip), body cols 49-53 rows 9-11, dot (52,10). CCW cycle candidate: down->right->up->left. OR clicking a specific ARM of the plus icon sets absolute direction (untested).
- WINNING GEOMETRY: green LEFT (kG up to tip cols 10-12 rows 15-17), yellow DOWN through gap cols 9-17 (tip to rows 33-35), blue RIGHT along rows 33-35 (kB=12, head cols 51-53, dot (52,34)) -> then rotate/extend etc. All paths verified open: rows 15-17 cols 10-38; gap cols 9-17 rows 27-29; rows 33-35 cols 13-56.
- Call 34 probe: (12,49) f-box BOTTOM arm: if blue -> DOWN = directional-arm model; if blue -> UP = center-cycle CCW model. Then (28,57) x2 = yellow-ret x2 (kY 2->0, tests new button layout; blue slides left with anchor, safe in all rotation outcomes).
- Buttons L6: f-L(9,57) f-R(15,57); G-L(28,57) G-R(34,57); I-L(47,57) I-R(53,57). Icon boxes: f(12,48) G(31,48) I(50,48); arms at center +/-1.

## L6 FULL CHOREOGRAPHY (designed action ~300, budget 62)
Rotation cycle per icon-box click: CCW, ↓→→→↑→←→↓. Riders transported to new tip.
State before batch: green ↑ k=1 (anchor cols 39-41 row 17? tip row ~11), yellow → k=0 (anchor col 39 rows 9-11), blue ↑ k=0 (dot (43,7)).
Batch 1 (15 actions, written):
 a) (31,48) yellow → ↑
 b) (50,48) green ↑→← : assembly transports to green tip cols 36-38
 c) (31,48) yellow ↑→←
 d) (12,48) blue → ←
 e) (31,48) yellow ←→↓
 f) (12,48) blue ←→↓
 g) (12,48) blue ↓→→
 h) (53,57) x8 green-ext: tip cols 36-38 → wait, green now ← so ext moves tip LEFT 3/press; 8 presses = -24 cols, tip 36-38→12-14; assembly slides to cols ~9-14.
Expected after batch: yellow ↓ anchor cols 9-11 rows ~15-17; blue → anchor col 9 rows 18-20, head cols 12-14, dot ~(13,19).
Batch 2 (next call, VERIFY GEOMETRY FIRST):
 - (34,57) yellow-ext x5: blue descends through wall gap (cols 9-17, wall band rows 27-29) to rows 33-35, dot (13,34)
 - (15,57) blue-ext x13: dot walks right +39 cols → (52,34) = diamond center → SCORE 6
Adjust green-ext count ±1 if riding offsets differ.

## ROTATION MECHANIC — CORRECTED (verified actions 301-307)
- Click on icon box rotates the WHOLE SUBTREE (link + all riders) 90° CCW; if blocked, tries 180°, then 270°. Result = first free orientation.
- Each link occupies a 3x3 "mount footprint" adjacent to carrier tip in carrier's direction; footprint is invariant under the link's own rotation. Anchor strip = trailing edge of footprint; body fills rest; head 3x3 beyond (blue only).
- Riders rotate rigidly with the parent and relocate to the new tip's mount region.

## L6 STATE after action 315 (all 15 committed, budget 56)
- green ← k=9: anchor col41 rows15-17, body cols12-40, tip cols12-14
- yellow ↑ k=0: footprint cols9-11 rows15-17 (anchor row17)
- blue ← k=0: footprint cols6-11 rows12-14, head cols6-8, dot (7,13)

## L6 ENDGAME (written action ~316, 20 actions)
1-2. (31,48) x2: yellow ↑→←→↓; blue rides ←→↓→→. Result: yellow ↓ (cols9-11 rows15-17), blue → rows18-20 anchor col9, head cols12-14, dot (13,19)
3-7. (34,57) x5 yellow-ext ↓: blue descends cols9-14 through wall gap (cols9-17, band rows27-29) to rows33-35, dot (13,34)
8-20. (15,57) x13 blue-ext →: dot walks +39 cols to (52,34) = diamond center → SCORE 6
Corridor rows33-35 cols6-53 verified clear (only diamond outline cells at 51-53/33-35, non-blocking per L5).
Risk: yellow max ext <5 or blue max ext <13 unknown; if a press reverts, later presses land short — diagnose next call.

## LEVEL 6 CLEARED (Score 6 at action 335, 20/20 plan steps worked)

## LEVEL 7 (starts action 336, fresh budget 64)
Goals: diamond (25,16) empty; diamond (22,7) ALREADY holds dot (light blue head on it — DO NOT touch light blue).
Left region: red ↓ k=4 rotate-only (icon (61,58)), anchor cols12-14 row6, body rows7-20 — blocks rows15-17; one click → red ← (CCW → blocked by lightblue, 180 ↑ OOB, 270 ← free, body cols0-13 rows6-8).
Right chain (base fixed): yellow ↑ k=0 fp cols48-50 rows12-14 → green → k=1 (anchor col48 rows9-11, body cols49-53) → blue ↓ k=1 (anchor row9 cols54-56, body rows10-14) → orange ← k=0 (fp cols54-56 rows15-17, DOT at (55,16) = center of leading 3x3).
Invariant: orange dir ≡ blue dir − 90°CCW (no orange icon). Dot rides center of orange's leading 3x3.
Walls: vertical cols40-42 rows0-29; band rows27-29 purple cols0-5,9-29,33-41 (gaps 6-8 and 30-32); strip cols15-17 rows27-38 & 42-47 (gap rows39-41); full bands rows45-47.
Buttons (L=retract,R=extend): yellow L(4,51) R(10,51) icon(17,51); blue L(26,51) R(32,51) icon(39,51); lightblue L(54,51) R(60,51); green L(4,58) R(10,58) icon(17,58); orange L(26,58) R(32,58); red icon(61,58).

## L7 ROUTE (39 actions, verified cell-by-cell)
Batch1 (written, 20): red-icon; green-ret x1 (k=0); yellow-icon x2 (↑→←→↓, needs green k=0 else blue fp hits wall); yellow-ext x8 (green mount rows15-17→39-41, cluster descends cols45-50); blue-icon x1 (↑→←, orange→↑, all fit in band rows39-41 for transit); green-ext x7 (partial of 13; cluster slides left, crosses cols15-17 via rows39-41 gap).
Batch2 (19): green-ext x6 (blue fp → cols6-8); blue-icon x1 (←: CCW ↓ blocked by band45-47, 180 → blocked orange hits strip42-44, 270 ↑ FREE → blue ↑ orange →); blue-ext x6 (orange fp rises through gap cols6-8 to rows15-17, dot (7,16)); orange-ext x6 (dot +3/press → (25,16)) → SCORE 7.
Risks: max-ext unknowns (yellow≥8, green≥13, blue≥7, orange≥6); fallback assumptions; dot-riding assumption.

## L7 BATCH1 RESULT (actions 336-355, budget 58)
- Action 336 red icon (61,58): 0 CHANGE — red rotation REFUSED. Theories: (a) fallback chain stops after 180 (never tries 270); (b) chain aborts at OOB orientation; (c) corner 'q' cells of icon box = CW rotation (untested). Full-chain-90/180/270 theory DISPROVED (red ← at cols0-13 rows6-8 is free but wasn't taken).
- All other 19 steps committed exactly as planned. State: green ← k=7 (band rows39-41), blue ← k=1 (fp cols24-26, anchor col26, body cols21-25), orange ↑ k=0 (fp cols18-20, dot (19,40)). Transit pose ✓.

## L7 BATCH2 (written, 20 actions)
1. (60,57) red-box CORNER probe — test CW rotation hypothesis (CW ↓→← = body cols0-13 rows6-8, free, clears rows15-17)
2-7. (10,58) x6 green ext → k=13, blue fp cols6-8
8. (39,51) blue click: 90 ↓ blocked (orange fp would hit band rows45-47) → 180: blue → (body cols7-11), orange ↓ (fp cols12-14 rows39-41, dot (13,40))
9. (39,51) blue click: 90 ↑ free: blue ↑, orange → (fp cols6-8 rows33-35, dot (7,34))
10-15. (32,51) x6 blue ext k=1→7: orange fp rises cols6-8 to rows15-17, dot (7,16)
16-20. (32,58) x5 orange ext: if red moved: dot →(22,16), need 1 more press next call for (25,16). If red still ↓: press1 ok (dot (10,16)), presses 2-5 revert harmlessly (leading 3x3 hits red cols12-14).
FALLBACK if red probe fails: lightblue-ret x3 (dot off goal (22,7) temporarily), red click → red → (90 free), red click → red ← (180; RISK: if OOB-abort theory, this aborts and red stuck at → = LEVEL DEAD, lightblue can't re-deliver → RESET). Try other box cells first ((61,57),(62,58) etc).

## ROTATION RULE — FINAL (proven by actions 336,356,363,364)
Click tries 90 CCW, then 180. NEVER 270. If both blocked -> no-op (retryable).
Corollary: child link can never point back toward its carrier (body overlap) UNLESS child k=0 (body stays inside own 3x3 fp).
Corner cells of icon box do nothing special (356 disproved CW hypothesis).
Link bodies are 3 CELLS WIDE, length 2+3k beyond... (fp = 3x3: 1-wide anchor edge + 2 body rows/cols at k=0).

## L7 BATCH3 (written, 20 actions) — state before: green ← k13 band r39-41, blue ← k1 fp c6-8, orange ↑ k3 fp c0-2 dot(1,31), red ↓, lightblue k3 delivered
1-3 orange-ret x3 (k=0); 4 blue-ret x1 (k=0, orange fp -> c3-5)
5 blue-icon: 90 works now (blue k=0): blue ↓ (body r40-41 c6-8), orange ← (fp c6-8 r42-44)
6 blue-icon: 90 → blocked (orange anchor would hit green c9-11), 180: blue ↑ (body r39-40), orange → (fp c6-8 r36-38)
7-13 blue-ext x7 (k=7): orange fp rises c6-8 through gap r27-29 to r15-17, dot (7,16)
14-15 lightblue-ret x2 (head c21-23 -> 27-29) — PROBE: does goal (22,7) outline+dot stay (locked goal) or move with head (carried)?
16 red-icon: 90 → now free (lightblue moved): red → (body c13-26 r6-8) — clears rows 15-17!
17 red-icon: 90 ↑ OOB, 180 ← -> red ← (cols 0-13 r6-8) IF OOB doesn't abort chain; else no-op (red stays →, still fine for orange delivery)
18-19 lightblue-ext x2: restores head c21-23 if red ←; harmlessly reverts if red stuck →
20 orange-ext x1: dot (10,16)
NEXT CALL: orange-ext x5 -> dot (25,16) -> SCORE 7 (path r15-17 c9-26 clear either way; strip c15-17 starts at r27, not in the way)
Residual risk: if red stuck → AND goal (22,7) requires lightblue presence -> may need RESET.

## L7 BATCH3 RESULT (376-395): ALL 20 STEPS WORKED
- Goal (22,7): outline is STATIC, dot is CARRIED by lightblue (moved with head during ret, restored by ext). Goal satisfied again ✓.
- RED: click2 from → rotated 90 CCW to ↑ WITH CLIPPING: body truncated at board edge (rows 0-7)! RULE UPDATE: OOB does NOT block rotation — body CLIPS at edges. Red now ↑ cols 12-14 rows 0-8, rows 15-17 clear.
- State: orange → k=1 rows 15-17, dot (10,16); blue ↑ k=7 cols 6-8; chain stable; lightblue delivered.
## L7 FINAL (written): orange-ext x5 -> dot (25,16) -> SCORE 7. Exactly 5 actions to avoid stray clicks on L8.

## LEVEL 8 (Score 7, actions from 401)
Hub yellow 3x3 @ cols49-51 rows32-34 in purple box (top rows23-25, sides cols40-42/57-59, bottom rows41-43 GAP at cols49-51). Arms k=0: red UP(29-31), green LEFT(46-48), blue RIGHT(52-54), orange DOWN(35-37).
Top-left green holder cols18-20 rows3-5 dir DOWN, DOT at (19,4). GOAL center (19,43).
lm link rows15-17 anchor col29, dir LEFT k=6 (body 9-28). lb link rows36-38 anchor col9, dir RIGHT k=6 (body 10-29), on red lift cols9-11 rows39-41 dir UP k=0.
Walls: 888 cols6-8 rows15-26, 888 cols30-32 rows36-50, purple block cols12-14 rows21-23.
Buttons: blue L(39,4) R(45,4); orange L(54,4) R(60,4); red L(39,11) R(45,11); green L(54,11) R(60,11); lb L(8,56) R(14,56); lm L(22,56) R(28,56); yellow ROT icon (49,18).
PLAN: dot needs green k=13 (dot row 4+3k -> 43). Clear path: lm retract x4 (k=2, body 21-28), lb retract x4 (k=2, body 10-17). Green ext: press1 both greens legal (hub k=1 cols43-47); press2 hub green JAMS (purple cols40-42) -> SEMANTICS TEST: per-link revert (top continues, dot (19,10)) vs whole-press revert (no change).
If per-link: green ext x11 more -> dot (19,43) -> score 8.
If whole-press: rotate hub (green DOWN thru gap, max k=8) still short of 13 -> rethink.

## L8 findings (actions 401-410)
- WHOLE-PRESS REVERT: shared-color press no-ops entirely if ANY instance jams (a410).
- '8' plates attach to lm/lb tips, slide with retract/extend. lm plate 12 tall (rows15-26@B0), lb plate 15 tall (rows36-50@R0).
- Hidden: purple blockB cols24-26 rows42-44 (blocked lb retract#2). Blue lift cols27-29 rows18-20 UP carries lm mount. Red lift carries lb.
- State now: TG/hubgreen k=1 (dot 19,7; hub green LEFT cols43-47). lm m=5 (body 12-28, plate 9-11). lb n=5 (body 10-26, plate 27-29).
- Geometry: lm center (28-3m, 16-3B); plate cols (24-3m..26-3m). lb center (10+3n, 37-3R); plate cols (12+3n..14+3n). Hub dir budgets from k0: UP 1, LEFT 1, RIGHT 0, DOWN 8 (thru gap, floor row62).
- TG max k=8 shared => dot max row 28 => RELAY REQUIRED. Perfect alignment: TG k=3 dot (19,13); lm at m=3,B=0 center (19,16). Testing handoff on green retract.
- Rotations with all arms k=0 always legal. CCW map: UP->LEFT->DOWN->RIGHT->UP.
## L8 batch (411-426): greenret, rotx3 (blue DOWN), blue x2 (lm up 2), lmret x2 (m=3, plate passes purpleA at rows9-20), blueret x2 (lm to rows15-17 center 19,16, plate cols15-17), rot x2 (green DOWN), green x3 (dot 19,13), greenret x1 = HANDOFF TEST (dot stays (19,13)/jumps lm/rides up (19,10)?)

## L8 batch 411-426 results: ALL EXECUTED. NO HANDOFF (dot rode back up on green retract). Dots glued to carrier, period.
- Hub arm bodies are at cols 48-50 (gap rows 41-43 = cols 48-50 too, blue body passed at a416).
- Current (a426): dirs red LEFT, green DOWN k=2 (TG dot 19,10), blue UP k=0, orange RIGHT k=0. lm m=3 body 18-28 r15-17, plate 15-17 r15-26. lb n=5 body 10-26 r36-38, plate 27-29 r36-50.
- NEW HYPOTHESIS: extension CLIPS at board edge (like rotation) => hub green DOWN absorbs presses past k=8 => TG k=13 possible => dot (19,43).
- Master plan A (this batch, 20): lmret x2 (m=1, body 24-28, plate 21-23), greenret x2 (k=0), rot x1 (red DOWN, green RIGHT), red x3 (R=3, lb r27-29, plate r27-41 clears purpleB), lbret x4 (n=1, body 10-14, plate 15-17), redret x3 (R=0, lb r36-38, col 18-20 clear below), rot x3 (green DOWN), green x2.
- Batch B next: green x11 (to k=8 real, then presses 9-13 = CLIP TEST; no-ops harmless if clip fails, dot parks (19,28)).

## L8 batch 427-446: 20/20 EXECUTED. Corridor col 18-20 CLEAR rows 12-62.
State: TG k=2 dot (19,10). Hub: red LEFT, green DOWN k=2, blue UP, orange RIGHT (all k=0 but green).
lm m=1 (body 24-28 r15-17, plate 21-23 r15-26). lb n=1 (body 10-14 r36-38, plate 15-17 r36-50). R=0.
Batch (447-457): green ext x11. 1-6 real (k=8, dot 19,28). 7-11 = EXT-CLIP TEST (k=13 dot 19,43 SCORE 8 if ext clips at edge; else no-ops).
