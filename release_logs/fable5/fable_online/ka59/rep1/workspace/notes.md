# Game notes

## Level 1 initial layout (64x64)
- Border '#' everywhere; bottom row 63 all 'q'.
- Left panel: '8' region cols 9-23 rows 21-46, extended to cols 24-32 on rows 30-32.
- Purple '"' band cols 33-38 rows 21-46 separates panels.
- Right panel: '8' region cols 39-53 rows 21-46.
- Left: hollow q-square outline cols 11-15, rows 32-36 (interior '8').
- Right: hollow q-square outline cols 44-48, rows 26-30 (interior '8') — same shape, centered in panel.
- Two green-framed 3x3 buttons in left extension:
  - White '$' center at (19,31), frame I at rows 30-32 cols 18-20.
  - Black 'O' center at (28,31), frame I at rows 30-32 cols 27-29.

## Hypothesis
Comparison/choice puzzle: pick a button (white vs black). Maybe "do shapes match?" or "what fill color?".
Test 1: click white button (19,31).

## Action 1 result (click white button 19,31)
- No panel change. Only row 63 last cell q->$ — likely step counter (budget ~64?).
- Buttons may be decorative/legend, not clickable answers.
## New hypothesis
Arrows move the left q-square. Goal: match right panel layout (square centered at rel offset 7,7 → abs center (16,28)). Left square center (13,34). Need Right x3, Up x6.
Test: ACTION1 (Up) once.

## Action 2 result (Up)
- White $ token (3x3 green frame) is the PLAYER. Moved up 3 rows: now rows 27-29, cols 18-20, center (19,28).
- Black O token static at center (28,31). Left q-square (13,34) unchanged.
- Row-63 counter did NOT increment on arrow move (still 1 '$'). Maybe counts only no-op/click/wasted actions.
## Hypothesis v3
Right panel = map of target position. Right square center rel (7,7) → left panel abs (16,28). Player at (19,28): one LEFT away.
Test: ACTION3.

## Action 3 result (Left)
- Player moved to cols 15-17, rows 27-29, center (16,28). Score still 0 — hypothesis v3 wrong.
- Counter incremented (63,62 q->$, now 2). Counter pattern: click no-op +1, Up +0, Left +1.
## Hypothesis v4
Counter penalizes moves away from goal. Up (toward row 28) free; Left (away from col 46) penalized. Goal = right square interior (45-47, rows 27-29), center (46,28) — on movement grid, same row as player.
Question: can player cross '#' cols 24-32 at rows 27-29 and purple band? Test Right x3 to reach cols 21-23 then probe blocking.

## Actions 4-6 (Right x3)
- R1 → center (19,28), R2 → (22,28), R3 BLOCKED by '#' cols 24-26 at rows 27-29.
- Counter = round(2n/3): values 1,1,2,3,3,4 for n=1..6. Just a step budget (~96 actions). NOT directional feedback — v4 wrong.
## Facts
- Player center positions: cols ≡ 1 mod 3 (10,13,16,19,22...), rows ≡ 1 mod 3 (22,25,28,31,...43).
- Corridor rows 30-32 spans cols 9-32; black token at cols 27-29 with one free cell (30-32) behind it before purple band.
- '#' blocks movement.
## Hypothesis v5
Sokoban-style pushing. Test: Down (22,31), Right (25,31), Right → should push black to cols 30-32 if pushable.

## Actions 7-9 (Down, Right, Right-push)
- Player (22,31)→(25,31). Push: black SLID from center (28,31) to (43,31) — ice physics, slides until hitting obstacle.
- Black crossed purple band (cols 33-38) — passable to blocks. Stopped against right square bottom wall (row 30); overlaps corner cell (30,44) in rendering.
- Player does NOT advance when pushing. Player still center (25,31). Score 0.
## Open questions
- Can PLAYER cross purple band via corridor rows 30-32?
- Was wall cell (30,44) destroyed by block? (check if black moves away)
- Goal guess A (mirror): black → center (43,34) [mirror of left square interior]; player → (16,28) [mirror of right square interior]. Overshoot problem: down-push from (43,28) would slide black to bottom (43,45).
## Test
Right x4: expect (28,31),(31,31), then purple test → (34,31),(37,31) if passable.

## Actions 10-13 (Right x4)
- Player (25,31)→(28,31)→(31,31). Purple band BLOCKS player (2 no-ops). Player stuck at (31,31).
- Black unreachable now. Counter 8/64 cells (n=13, budget ~96 actions).
## Test
Click distant cell: ACTION6(46,28) right-square interior. Checking teleport/command mechanics before RESET.

## Action 14 (click 46,28)
- Pure no-op, only counter. Clicks appear useless. Counter fills row 63 right-to-left (9 cells, n=14).
## Analysis
- Black's push right was FORCED (only legal push) → likely intended. Black rests touching right square's bottom-left corner, overlapping corner cell (30,44).
- Goal guess: replicate arrangement with PLAYER touching LEFT square's corner. Candidates: (16,31) top-right corner overlap (32,15); or (10,37) bottom-left corner overlap (36,11).
- Wall-overlap rule unknown: black's rest position overlaps 1 corner cell. Test if player can enter 1-corner-overlap cells.
## Test
Left x5: (28,31),(25,31),(22,31),(19,31), then (16,31) = corner-overlap test + goal candidate.

## Actions 15-19 (Left x5)
- Player walked to (16,31) including 1-corner-overlap cell (32,15) — overlap positions ARE walkable. Score still 0 at (16,31) [confirm next call].
- Counter ~floor(2n/3): 12 at n=19.
## Next
Exact analog of black-square arrangement: player SW of left square, center (10,37) (overlaps corner (36,11)).
Route from (16,31): R(19,31), D(19,34), D(19,37), D(19,40), L(16,40), L(13,40), L(10,40), U(10,37). All cells verified free; final has 1-corner overlap (allowed).

## Actions 20-27 (route to SW corner)
- Route executed perfectly; player at (10,37), overlapping left square corner (36,11), mirroring black's arrangement at right square.
- Score unknown yet (headers lag). Probe with blocked Up (safe no-op if level 1 continues).
- If no score at (10,37): plan RESET and try pushing black LEFT first (stops at (16,31) NE corner) or explore other mechanics (e.g., player+black both at corners simultaneously — already true now!).

## Action 28 (Up from 10,37)
- NOT blocked! Player → (10,34), overlapping 3 q-cells (33-35,11); q restored behind at (36,11).
- REVISED RULE: q outlines do NOT block the player — only '#' and purple '"' do. q likely only stops sliding blocks.
- (10,37) did not score. Earlier "blocked" moves were all '#', never q. Left square interior reachable!
## Test
Right → (13,34): player exactly inside left square interior (rows 33-35, cols 12-14).

## Action 29 (Right)
- Player inside left square interior, center (13,34). Score unknown (header lag). Probing with click(0,0) no-op.
- Deduction: only PLAYER can ever be inside a q-square (q transparent to player, stops blocks). Block stop rule: slides until next position would overlap ≥3 q cells (1-cell corner overlap tolerated).
- If no score: consider RESET; alt line = push black LEFT (stops at (16,31)), then vertical pushes possible: up→(16,22), down→(16,45).

## Action 30 (click 0,0)
- Zero diffs. Player-in-square (13,34) did NOT score.
## Key deduction
- Player can NEVER get east of black's start (rows 27-29 cols 24-26 = '#'; corridor blocked by black itself) → right-push was the ONLY possible push. Black's full reachable set = {(43,31)}. No RESET needed.
- Win must be player position alone (given black at 43,31). Untried candidates:
  1. (13,31): left-panel position corresponding to black's right-panel rel position (col 4, row 10) — player sits on square top edge. STRONG (mirror-panels hypothesis).
  2. (10,31) NW corner overlap, (16,37) SE corner overlap.
## Test
Up from (13,34) → (13,31).

## Action 31 (Up)
- Player at (13,31), on square's top edge (3-cell q overlap fine). Result pending.
## Sweep plan
Position-based win assumed. Untried cells: (10,31),(10,28),(10,25),(10,22),(13,22),(13,25),(13,28),(16,22),(16,25),(19,22),(19,25),(22,22),(22,25),(22,28),(16,34),(13,37),(16,37),(10,43),(13,43),(16,43),(19,43),(22,34),(22,37),(22,40),(22,43).
Batch 1 (10 moves) from (13,31): L(10,31) U(10,28) U(10,25) U(10,22) R(13,22) D(13,25) D(13,28) R(16,28)pass U(16,25) U(16,22).
Batch 2 next: (19,22),(22,22),(19,25),(22,25),(22,28), then south cells.

## Actions 32-41 (sweep batch 1)
- Visited (10,31),(10,28),(10,25),(10,22),(13,22),(13,25),(13,28),(16,28)v,(16,25),(16,22). No score through action 41. Counter 26/64, n=41.
## Batch 2 (20 moves, exhaustive) from (16,22)
R(19,22) R(22,22) D(22,25) L(19,25) D(19,28)v R(22,28) D(22,31)v D(22,34) D(22,37) D(22,40) D(22,43) L(19,43) L(16,43) L(13,43) L(10,43) U(10,40)v R(13,40)v U(13,37) R(16,37) U(16,34).
After this, ALL reachable cells visited. If no score → position-only hypothesis dead; rethink (RESET/mechanics).

## Actions 42-61 (batch 2)
- CORRECTION: panels span rows 21-41 only (row 42+ is '#'). Row-43 cells don't exist; Down at (22,40) was blocked by panel edge.
- Visited everything except (16,37) (SE corner overlap = horizontal mirror of black's SW arrangement). Player now at (16,31). Counter 39/64.
## Test
D,D → (16,34), (16,37). Last untried position.

## Actions 62-63 (D,D)
- Player at (16,37) — SE corner, LAST unvisited cell. Result pending. Counter 40/64 (~33 actions left).
- Full-board diff vs post-push state: zero non-player changes. No hidden progress indicators.
## Next: object-click tests
Click black (43,31), purple (35,31), left square wall (32,13), overlap corner (30,44). All other mechanics exhausted.

## Actions 64-67 (object clicks) — BREAKTHROUGH
- Click on token center (43,31): CONTROL SWAP! Black center O→$ (active), player center $→q (inactive block). Clicks on purple/walls: no-ops.
- Mechanic: click token center = activate it (arrows move active token; active walks through q; inactive = slidable block).
- Win hypothesis: BOTH tokens inside their squares: right token → (46,28), left token → (13,34).
## Plan
U (43,28), R (46,28) [right token in square]; ACTION6(16,37) activate left; L (13,37), U (13,34) [left token in square].

## LEVEL 1 CLEARED (action 72, Score 0->1)
Win = every token inside its matching q-outline interior. Click token center to activate; active moves 3/press, passes q, blocked by '#'/purple; inactive tokens ice-slide when pushed and CAN cross purple.

## Level 2 layout (verified programmatically)
- Regions: left-top cols 0-20 rows 0-23; left-bottom cols 0-20 rows 30-62; right cols 30-62 rows 30-62.
- Walls: '#' cols 21-23 rows 0-23; '#' rows 27-29 (cols 30-63); purple vert cols 21-29 rows 30-62; purple horiz rows 24-29 cols 0-29.
- Goals (interiors): LT 3wx6t rows 9-14 cols 9-11 (for B); LB 6x6 rows 42-47 cols 6-11 (for C); R 6wx3t rows 39-41 cols 54-59 (for A); R 3x3 rows 51-53 cols 51-53 (for P).
- Tokens: A 6x3 rows 33-35 cols 39-44; B 3x6 rows 42-47 cols 33-35; C 6x6 rows 45-50 cols 42-47; P 3x3 active center (37,55).

## Level 2 plan (8 phases, ~64 actions)
P1(4): L,U,U -> P(34,49); U-push B -> rows 30-35 cols 33-35.
P2(8): R, Ux6 -> P(37,31); L-push B -> cols 0-2 rows 30-35 (crosses purple). RISK: partial-height push (P 3 tall vs B 6 tall) untested.
P3(15): Rx4 ->(49,31); Dx8 ->(49,55); L(46,55); U(46,52); U-push C -> rows 36-41 cols 42-47.
P4(6): R(49,52); Ux4 ->(49,40); L-push C -> cols 12-17 rows 36-41.
P5(10): click(14,38) activate C; Lx4 -> C cols 0-5; U-push B -> rows 0-5 cols 0-2 (LT region); Rx2,Dx2 -> C in GOAL cols 6-11 rows 42-47.
P6(7): click(1,2) activate B; Dx3,Rx3 -> B in GOAL rows 9-14 cols 9-11.
P7(8): click(41,34) activate A; Rx5,Dx2 -> A in GOAL rows 39-41 cols 54-59.
P8(6): click(49,40) activate P; R,Dx4 -> P in GOAL rows 51-53 cols 51-53. WIN.

## This call: Phases 1-2 (12 actions)
Verify after: B at cols 0-2 rows 30-35; P at (37,31). Watch partial-push behavior.

## Actions 73-84 (L2 Phases 1-2)
- P at (37,31) as planned. Partial-height push WORKS (3-tall P pushed 6-tall B).
- B slid left but stopped at cols 18-20 rows 30-35 (LB region) — cols 15-17 are free '8'!
- NEW RULE: slides capped at 5 steps (15 cells). Level 1 slide was also exactly 15 cells. Obstacles stop earlier.
## Revised plan (B at 18-20 is fine; C needs 2 pushes)
P3(10): D x7 ->(37,52); R x2 ->(43,52); U-push C -> rows 36-41 (stops below A, 3 steps).
P4(7): R x2 ->(49,52); U x4 ->(49,40); L-push C -> cols 27-32 (5-step cap, rests straddling purple - VERIFY).
P4b(6): L x5 ->(34,40); L-push C -> cols 12-17 rows 36-41.
P5(8): click(14,38) activate C; R (cols 15-20); U-push B -> rows 15-20 cols 18-20 (5 steps thru purple - VERIFY); L x3, D x2 -> C GOAL rows 42-47 cols 6-11.
P6(6): click(19,17) activate B; U x2, L x3 -> B GOAL rows 9-14 cols 9-11.
P7(8): click(41,34) activate A; R x5, D x2 -> A GOAL rows 39-41 cols 54-59.
P8(11): click(34,40)... P at (34,40) after P4b; activate P via click(34,40); R x6, D x4 -> P GOAL (52,52). WIN.
## This call: P3+P4 (17 actions). Verify C rests at cols 27-32 on purple.

## Actions 85-101 (P3+P4) — plan deviation
- NEW RULE: sliding blocks CHAIN-PUSH blocks they hit. C's U-slide hit A: A pushed to rows 30-32 (vs '#' wall), C settled rows 33-38 cols 42-47.
- Final L was a free move (C not beside P): P now (46,40) rows 39-41 cols 45-47. Rendering quirk: P top row shows '$$$' when adjacent below C frame — cosmetic.
- A at rows 30-32 still fine: goal rows 39-41 cols 54-59 = D x3, R x5 (lattice OK).
- Counter: 15 cells at n=29 → rate ~n/2, budget likely ~128. Ample.
## Re-revised plan (avoid C-hits-B on left push: use rows 48-53 band)
PA(6): R,U,U,U,L -> P(46,31); D-push C -> rows 48-53 cols 42-47.
PB1(8): R, D x6 -> (49,49); L-push -> C cols 27-32 rows 48-53 (rests straddling purple — VERIFY).
PB2(6): L x5 -> (34,49); L-push -> C cols 12-17 rows 48-53 (1-cell q overlap (48,12) OK).
PC(12): click(14,50) activate C; U x4 (rows 36-41), R (cols 15-20); U-push B -> rows 15-20 cols 18-20 (thru purple into LT); L x3, D x2 -> C GOAL rows 42-47 cols 6-11.
PD(6): click(19,17) activate B; U x2, L x3 -> B GOAL rows 9-14 cols 9-11.
PE(9): click(41,31) activate A; D x3, R x5 -> A GOAL rows 39-41 cols 54-59. (P inactive parked at (34,49) — paths clear.)
PF(8): click(34,49) activate P; R x6, D -> P GOAL (52,52). WIN.
## This call: PA + PB1 (14 actions). Verify C rests on purple at cols 27-32.

## Actions 102-115 (PA+PB1)
- C slid PAST purple to cols 15-20 rows 48-53 (9 steps). PB2 unnecessary.
- FINAL SLIDE RULE (fits all 6 slides incl. L1): slide 5 lattice steps max; if 5-step endpoint overlaps purple, continue until first fully-purple-free position, then stop. Obstacles/chains stop earlier. (L1 purple band was 9 wide, cols 33-41 — my old note said 33-38, wrong.)
- State: P active (49,49); C rows 48-53 cols 15-20; B rows 30-35 cols 18-20; A rows 30-32 cols 39-44.
## Endgame (29 actions)
PC(11): click(17,50) activate C; U x4 -> rows 36-41; U-push B -> rows 15-20 cols 18-20 (5 steps, clears purple rows 24-29); L x3, D x2 -> C GOAL rows 42-47 cols 6-11.
PD(6): click(19,17) activate B; U x2, L x3 -> B GOAL rows 9-14 cols 9-11.
PE(9): click(41,31) activate A; D x3, R x5 -> A GOAL rows 39-41 cols 54-59.
PF(3): click(49,49) activate P; R, D -> P GOAL rows 51-53 cols 51-53. WIN.
## This call: PC+PD (17 actions).

## Actions 116-132 (PC+PD) — perfect
- C in GOAL rows 42-47 cols 6-11 (center O no longer rendered — likely satisfied-state). B in GOAL rows 9-14 cols 9-11 (active).
- A rows 30-32 cols 39-44; P inactive (49,49). Counter 30/64, n=60 this level (budget ~128).
## This call: PE+PF (12 actions) -> expected WIN
click(41,31); D x3; R x5 [A -> rows 39-41 cols 54-59]; click(49,49); R; D [P -> (52,52)].

## LEVEL 2 CLEARED (action 144, Score 1->2). 72 actions used.

## Level 3 layout
- Room '8' rows 5-58 cols 5-58, '#' border. P 3x3 active center (46,15).
- Yellow plus 1: rows 20-28 cols 50-58 (center 54,24). Yellow plus 2: rows 35-43 cols 20-28 (center 24,39). 9x9 plus shapes (five 3x3 cells).
- Plus outline A: interior rows 20-28 cols 20-28 (center 24,24). Plus outline B: interior rows 35-43 cols 35-43 (center 39,39). 3x3 outline: interior rows 29-31 cols 35-37 (center 36,30) = P goal.
- Targets: yellow2 -> A (U-push 15, cols already match), yellow1 -> B (D-push 15 then L-push 15), P -> (36,30).
- LATTICE PROBLEM: P center ≡ (col 1, row 0) mod 3; all L/R push spots and P goal need col ≡ 0 mod 3.
- HYPOTHESIS: pressing into a wall moves P partially (0-2 cells) -> lattice shift. East wall: P (55,r) + R -> (57,r). Never tested (all prior blocked moves were +1-blocked).
- Assume q transparent to slides (design requires plus to slide INTO outline interiors).
## Full plan (~39 actions)
S1(5): R x3, D -> (55,18); D-push -> yellow1 rows 35-43 cols 50-58.
S2(1): R -> partial shift, P (57,18) [VERIFY].
S3(7): D x6 -> (57,36); L-push -> yellow1 cols 35-43 = IN B.
S4(17): D x3 -> (57,45); L x12 -> (21,45); U -> (21,42); U-push -> yellow2 rows 20-28 = IN A.
S5(9): U x4 -> (21,30); R x5 -> (36,30) = P GOAL. WIN.
Routes verified vs all obstacles; avoid (36,42)->U (would push yellow1 out of goal).
## This call: S1+S2 (6 actions). Verify yellow1 slide and wall-shift.

## Actions 145-150 (S1+S2) — both hypotheses CONFIRMED
- Yellow1 at rows 35-43 cols 50-58 ✓. P at (57,18): WALL PARTIAL-MOVE WORKS (lattice now col ≡ 0 mod 3).
## This call (20): S3 + most of S4
D x6 -> (57,36); L-push -> yellow1 cols 35-43 (IN B, verify); D x3 -> (57,45); L x10 -> (27,45).
## Next call (13): L x2 -> (21,45); U -> (21,42); U-push yellow2 -> IN A; U x4 -> (21,30); R x5 -> (36,30) P GOAL. WIN.

## Actions 151-170 (S3+S4a) — on plan
- Yellow1 IN outline B (rows 35-43 cols 35-43). P at (27,45).
## This call (13): finish L3
L x2 -> (21,45); U -> (21,42); U-push yellow2 -> rows 20-28 IN A; U x4 -> (21,30); R x5 -> (36,30) P GOAL. Expect Score 3.

## LEVEL 3 CLEARED (action 183, Score 2->3). 39 actions.

## Level 4 layout (programmatic)
- Rooms: top-right rows 6-19 cols 33-58; middle rows 20-37 cols 5-58; bottom rows 44-58 cols 5-43. Purple rows 38-43 cols 5-43 (middle<->bottom, blocks only).
- P active (21,30); O token (30,33); yellow plus rows 50-58 cols 20-28 center (24,54).
- Goals: plus outline interior rows 8-16 cols 35-43 center (39,12) [yellow]; middle 3x3 interior rows 29-31 cols 50-52 center (51,30) [P]; bottom 3x3 interior rows 53-55 cols 38-40 center (39,54) [O].
- All on (col%3=0,row%3=0) lattice. No wall-shift needed.
## Plan (52 actions)
S1(4): P R x3 ->(30,30); D-push O -> (30,48) bottom room.
S2(1): click(30,48) activate O.
S3(9): O L x4 ->(18,48); D x3 ->(18,57); R ->(21,57); U-push yellow -> rows 29-37 center (24,33) (5 steps + purple ext).
S4(7): O R x6 ->(39,57); U ->(39,54) O IN GOAL.
S5(1): click(30,30) activate P.
S6a(10): P U, L x4 ->(18,27); D x3 ->(18,36); R ->(21,36); U-push -> yellow rows 20-28 (24,24) (wall-stopped).
S6b(6): L, U x4 ->(18,24); R-push -> yellow cols 35-43 (39,24).
S6c(10): D x2, R x7 ->(39,30); U-push -> yellow rows 8-16 (39,12) IN OUTLINE.
S6d(4): R x4 ->(51,30) P IN GOAL. WIN.
## This call (20): S1+S2+S3+S4(R x6). Next: U, S5, S6.

## Actions 184-203 — on plan
- Yellow in middle room rows 29-37 (24,33) ✓. O active at (39,57), one U from goal. P inactive at (30,30) (q center).
## This call (20): U [O goal]; click(30,30); S6a(10); S6b(6); D x2 [start S6c]. P ends (18,30).
## Next call (12): R x7 ->(39,30); U-push [yellow -> (39,12) outline]; R x4 -> (51,30). WIN.

## Actions 204-223 — on plan
- Yellow rows 20-28 cols 35-43 (39,24) ✓. P active (18,30). O satisfied in goal (hidden rendering).
## This call (12): R x7 ->(39,30); U-push -> yellow (39,12) IN OUTLINE; R x4 ->(51,30) P GOAL. Expect Score 4.

## LEVEL 4 CLEARED (action 235, Score 3->4). 52 actions.

## Level 5 layout
- Open field cols 0-62 rows 0-62 ('#' col 63 only). New: '>' maroon, '-' orange blocks (no outlines for them).
- Purple rect rows 9-20 cols 18-35. Well: purple walls cols 21-23 & 30-32 rows 27-56, floor rows 54-56 cols 21-32; interior cols 24-29 rows 27-53.
- In well: orange 6x2 rows 30-31 cols 24-29 atop maroon 6x4 rows 32-35 cols 24-29 (plug). P active (28,49) below.
- Goal outline rows 26-30 cols 48-52, interior rows 27-29 cols 49-51, center (50,28). Its east wall replaced by maroon 1-wide col 52 rows 27-29 + orange 2x3 cols 53-54 rows 27-29 (door).
- Lattice: P ≡ (col 1, row 1) mod 3; goal col 50 ≡ 2 → reach via partial move against 1-wide maroon door (stop flush at center 50).
## Plan (18 actions)
U x4 -> (28,37); U-push -> plug slides up, extended through purple rect: maroon lands rows 5-8, orange rows 3-4 (chain).
U x4 -> (28,25) out of well; R x7 -> (49,25); D -> (49,28); R -> partial +1 -> (50,28) GOAL CENTER. WIN if engine does move-or-push (partial advance, push only when flush). If final R instead pushes door away or no-ops, adapt next call.

## Actions 236-253 (L5 attempt 1) — plug launched, P STUCK
- PARSING FIX NEEDED: many boards are [frame] animation frames; only use boards after [settled]/[POST-ACTION]/[INITIAL] markers. My L5 'layout' was read from a FRAME: door/goal actually at outline cols 46-51?? -> committed boards show q west wall col 47, interior cols 48-50 center (49,28) — ON P's lattice (49%3=1, 28%3=1). No partial-move trick needed.
- Plug (maroon 6x4 + orange 6x2) launched fine: parked orange rows 3-4? actually '-' rows 3-4 + '>' rows 5-8 cols 24-29, ABOVE purple rect. Plug/door textures CYCLE (animated) — cosmetic.
- P pushed plug from (28,37), then ONE U worked (-> (28,34)), then U x3 all NO-OP despite rows 30-32 cols 24-29 being free '8' in settled boards. R x7 no-op (wall, expected). D worked. INVISIBLE BLOCKER at rows 30-32?
## This call: probe (6 actions): L, U, U, U, R, U
Tests left shaft (cols 24-26): if U works there, blocker is local to cols 27-29; expected path (25,34)->(25,31)->(25,28)->(25,25)->(28,25)->(28,22).

## Actions 254-259 (probe) — P FREE
- All 6 moves worked: left shaft clear; P now (28,25), OUT of well. (Right-shaft U-block at (28,34) remains unexplained — possibly transient object; avoid that cell pattern in future.)
- Goal confirmed in committed board: outline rows 26-30 cols 47-51, interior center (49,28); maroon door col 51 rows 27-29 (cosmetic-cycling), orange 52-53.
## This call (8): R x7 -> (49,25); D -> (49,28) = GOAL. Expect Score 5.

## LEVEL 5 CLEARED (action 267, Score 4->5). 32 actions. (Door trick unnecessary; goal was on-lattice at (49,28).)

## Level 6 layout (committed board)
- Top-left room rows 1-29 cols 1-29: plus outline interior center (7,7); yellow plus center (10,19); pocket maroon1 6x6 rows 15-20 cols 24-29 ('#'-sealed except bottom).
- Top-right room rows 1-29 cols 33-62: 3x3 outline interior rows 21-23 cols 48-50 center (49,22); pocket maroon2 rows 15-20 cols 33-38.
- Purple band rows 30-35 (split by '#' cols 30-32 rows 0-35).
- Middle strip rows 36-50: P (53,49); maroon3 6x6 rows 45-50 cols 42-47 AGAINST wall rows 51-53 ('#' cols 3-59, passages cols 0-2/60-62 to bottom field rows 54-62). '#' pockets rows 45-47 cols 3-5 & 58-60.
- BFS: P confined to middle+bottom; goal (49,22) UNREACHABLE by walking. Maroon3 cannot be pushed up (wall below). Top objects have no visible pusher. UNKNOWN MECHANIC required.
- P lattice (col%3,row%3)=(2,1); '#' pockets + maroon3 give partial-move lattice shifts if needed.
## This call: probes (8): L,L (flush at (49,49)); clicks: maroon3(44,47), pocket1(26,17), pocket2(35,17), yellow(10,19), outlineTR(49,22), outlineTL(7,7).

## Actions 268-275 (L6 probes)
- All 6 clicks: ZERO diffs (clicks on blocks/outlines do nothing; don't advance timers).
- ENGINE FIX: gap-1 press = partial advance THEN push in same press (P closed gap and maroon3 slid L 15: cols 42-47 -> 27-32). P now (49,49).
- FUSE MECHANIC: each P MOVE converts one row of every maroon 6x6 to orange: pockets convert TOP-DOWN (rows 15,16 done), maroon3 BOTTOM-UP (rows 50,49 done). 6 rows total. Unknown event at full conversion.
- Rendering quirk: P edge column shows '$$$' when flush against a block (seen L2, L5, here).
## This call: burn fuse with 6 harmless moves L,R,L,R,L,R (P (49,49)<->(46,49)); observe full-conversion event.

## L6 PISTON DISCOVERY (after actions 276-281)
- Maroon/orange conversion = mod-6 MOVE CLOCK. At wrap (phase 6): all 3 maroons extend 9-row ORANGE PISTONS during frames, then retract; board resets to all-maroon (phase 0).
- Piston zones: left pocket cols24-29 rows21-29 DOWN; right pocket cols33-38 rows21-29 DOWN; maroon3 (cols27-32) rows36-44 UP. All stop flush at purple band edges.
- HYPOTHESIS: piston pushes P through purple (slide-extension until purple-free) = room transport. maroon3 up=entry (left room at cols27-29, right room if maroon3 moved to cols42-47); pockets down=exit from rooms.
- Phase after action 281 = 2 (pockets rows15-16 orange, maroon3 rows50-49 orange).
- P at (49,49). Board otherwise: yellow plus center (10,19) rows15-23 cols6-14 (3-wide arms, 9x9); plus outline interior center (7,7); 3x3 outline center (49,22); divider '#' cols30-32 rows0-35.
- Yellow plus needs: up 12, left 3 (center (10,19)->(7,7)).
## This call: U,U,L*7 to (28,43) flush atop maroon3 (phase 11), then D (no-op probe: does it tick clock? if yes wrap fires, P launched to ~(28,28) left room), then U (backup trigger at phase 12 from (28,40), still in piston zone).

## PISTON LAUNCH CONFIRMED (actions 282-292)
- P launched from (28,43) atop maroon3 -> (28,28) left room. Wrap = every 6th MOVE; NO-OP/blocked moves DO count (blocked D triggered wrap). Clicks don't.
- Piston push = shove + purple-free extension. Landing rows: 3-tall P -> rows 27-29 (center 28); predicted 9-tall plus -> rows 21-29 (center 25); 6-tall block -> rows 24-29.
- P now (28,25), phase 1 after action 292.
- KEY constraints derived: P cannot up-push any block resting at center row 25 (P would need to stand in purple). Divider cols 30-32 rows 0-35 splits rooms; plus crosses only via strip. Pocket maroons (1: cols 24-29, 2: cols 33-38, rows 15-20) are immovable fixtures (sealed; only their down-pistons matter: zones cols 24-29 & 33-38, rows 21-29).
- maroon3 parkable col-ranges: {6-11,12-17,27-32(now),42-47,52-57}; its up-piston zone = its cols, rows 36-44.
- Slide-cap-15 analysis says plus col 7 unreachable (mod-15 families) -> SUSPECT cap may differ for 9x9 plus. TESTING NOW: up-push from (10,19): wall-stop (10,5) if cap>=14; else (10,19-cap). Cap 12 would give (10,7) directly.
## This call: L*6 (P to (10,25); wrap fires harmlessly at move 5, P at (13,25)), then U = up-push plus. Phase after: 2.

## OUTLINE-CATCH DISCOVERY (actions 293-299)
- Up-push slid plus 12 cells: (10,19)->(10,7), stopping EXACTLY row-aligned with outline interior (rows 3-11), passing through q. NOT wall-stop (14) nor cap-15. => matching outline CATCHES its block when aligned mid-slide (snap-stop).
- Plus now (10,7); need left 3. Left-push should catch at (7,7)=GOAL. (If instead pure cap-12: would overshoot to (5,7) - recovery unclear, but catch is strongly supported.)
- Phase after 299 = 2. Wrap at 297 was harmless (P (13,25), nothing in zones).
## This call: R,R then U*6: P (10,25)->(16,7) right of plus (wrap at move 4 harmless, P (16,22) clear). Then L = left-push -> expect plus (7,7) DONE.
## Remaining after: P exit via left-pocket piston (stand (25,28) or (28,28), wrap) -> strip; gap-1 push maroon3 right (P (24,46)) -> cols 42-47; P to (43,43) pad; wrap (pad D no-ops) -> right room (43,28); walk R,R,U,U -> (49,22) WIN.

## PLUS DONE (actions 300-308)
- Left-push: plus slid only 3 cells, caught at (7,7) = outline interior. CATCH MECHANIC CONFIRMED (no fixed cap involved; outline snags matching block mid-slide).
- P (16,7), phase 5 after 308.
## This call (13 actions): D*7 (col 16 down to row 28; wrap harmless at move1 P(16,10) and move7 P(16,28)), R*3 -> (25,28) in left-pocket zone, D*3 no-ops (bottom flush purple) -> wrap fires exactly on move 13 -> P launched down to strip (25,37), phase 0.
## Next call: D*3 -> (25,46) flush left of maroon3; R push -> maroon3 cols 42-47; route P to pad (43,43) (U, R*6-ish; mid wraps harmless); D no-ops until wrap -> launch -> right room (43,28); R,R,U,U -> (49,22) WIN L6.

## POCKET EXIT DONE (actions 309-321)
- All 13 as planned; wrap on move 13 launched P down: (25,28)->(25,37). Phase 0 after 321.
## This call (7 actions): D*3 -> (25,46) flush left of maroon3; R = push (maroon3 27-32 -> 42-47 expected); U; R,R (partial progress toward pad). Observe P's post-push advance (0/1/3 cells unknown) to set exact counts next call.
- Wrap at m6: P around (28-32,43), new maroon3 zone cols 42-47: P clear -> harmless. Phase after batch = 1.
## Next call: finish exact route to pad (43,43) (col must be ~43, ⊆42-47 on rows 42-44), D no-ops to wrap -> launch -> (43,28) right room; R,R,U,U -> (49,22) WIN.
- CAUTION: never press R while flush against maroon3 at rows 45-50 (would re-push it; from 42-47 it would slide to 52-57).

## PUSH DONE (actions 322-328)
- maroon3 -> cols 42-47 rows 45-50 (pad set). P did NOT advance after flush push (stayed (25,46)). P now (31,43), phase 1.
## This call (9 actions, WIN expected): R*4 -> pad (43,43) (phases 2-5); D no-op = phase 6 -> WRAP -> up-piston launch -> (43,28) right room; R,R,U,U -> (49,22) = 3x3 outline center. Plus already at (7,7). Level 6 complete -> score 6.

## LEVEL 6 CLEARED (action 337, score 6). Total L6 = 73 actions (265-337).

## LEVEL 7 (board at log 39508)
- P = 3x6 tall token, cols 54-56 rows 42-47 (two $ at (55,44),(55,45)). Goal outline interior cols 27-29 rows 45-50 (center ~(28,47.5)).
- O = 6x3 token, cols 33-38 rows 51-53 (OO at (35,52),(36,52)). Goal outline interior cols 24-29 rows 24-26.
- Yellow plus 9x9 center (13,13) top-left. Goal outline center (13,40) in LEFT-MIDDLE.
- maroon-a cols 46-51 rows 6-11 (top-right); maroon-b cols 42-47 rows 48-53.
- Purple: vertical cols 21-23 & 40-42 rows 6-17; horizontal rows 18-20 cols 0-18; rows 36-38 cols 22-47.
- Key walls: rows 3-5 cols 21-62; corridor rows 0-2 full width (enters only from top-left cols 0-20); rows 18-20: '#' cols 19-32 & 36-50, GAP cols 33-35 (3 wide: P fits, O 6-wide does NOT); '#' cols 19-21 rows 21-29 & 33-45 with left-middle entry rows 30-32; '#' cols 48-50 rows 21-26/30-38/48-53; rows 46-48 cols 0-21; rows 54-56 cols 43-51; '#' rows 36-38 cols 48-62.
- Regions: top-left (plus, unreachable by walking); top-middle cols 24-39; top-right cols 43-62; middle rows 21-35; left-middle rows 21-45 cols 0-18 (O enters via rows 30-32; P 6-tall CANNOT); lower rows 39-47; bottom rows 49-62. P currently confined BELOW rows 36-38 band (its outline is down here too). O can reach: bottom, lower, (via piston-b launch) middle, right strip, top-right.
- DRAFT plan pieces: O pushes maroon-a left (cols 46-51 -> 31-36); plus needs down-pushes reaching (13,28/31/...) then catch at (13,40); O parked rows 21-23 cols 10-15 as landing-blocker makes piston shove land plus at (13,28); but delivering maroon-a to TOP-LEFT (A2) has no available pusher (P would strand itself above; O can't pass 3-wide gap). UNRESOLVED - need piston empirics.
- P 3-wide fits vertical piston zones (e.g. cols 43-45 rows 6-11 of maroon-a original); O 3-tall fits horizontal corridors.
## This call: probe wrap pistons: 6 moves L,R,L,R,L,R (P oscillates cols 51-53<->54-56 rows 42-47, safe). Wrap at move 6: read frames for piston directions/lengths of both maroons. Phase assumed 0 at level start.

## L7 PISTON PROBE RESULTS (actions 338-343, wrap at 343)
- maroon-a cols 45-50 rows 6-11: fires DOWN, piston rows 12-20 (extends over '#' rows 18-20!). Zone = cols 45-50 rows 12-17, shoves through rows 18-20 into rows 21+.
- maroon-b cols 42-47 rows 48-53: fires UP, piston rows 47-39, flush at purple band rows 36-38. Zone = cols 42-47 rows 39-47, shoves up through band, landing rows 33-35 (3-tall) / 30-35 (6-tall P).
- Phase after 343 = 0.
## L7 CORRECTED TOPOLOGY (settled board at log 40221)
- Rows 0-2 open full width; rows 3-5 '#' cols 21-62, OPEN cols 0-20 (top-left connects to corridor; corridor descends ONLY into top-left).
- Purple verticals: cols 21-23 rows 6-17, cols 39-41 rows 6-17. Purple rows 18-20 cols 0-18. Purple rows 36-38 cols 22-47.
- Rows 18-20: '#' 19-32 & 36-50; OPEN gaps cols 33-35 and cols 51-62 (walkable!).
- '#' cols 19-21 rows 21-29 & 33-45; passage rows 30-32 cols 19-21 open (3 tall).
- '#' cols 48-50 rows 21-26, 30-38(48-62 rows 36-38), 48-53; corridor rows 27-29 cols 48-62 OPEN (3 tall).
- Rows 46-48 '#' cols 0-21(25?); row 48 '#' 0-25ish. Rows 54-56 '#' cols 43-51.
- Plus center (13,13); outline center (13,40). O rows 51-53 cols 33-38; outline rows 24-26 cols 24-29 (middle). P rows 42-47 cols 54-56; outline rows 45-50 cols 27-29 (BELOW band).
## L7 DEADLOCK ANALYSIS
- P's outline is below rows-36-38 band; P is 6 tall: cannot use rows 27-29 corridor / rows 30-32 passage; once launched up (zone-b), P can NEVER return down (no down-piston can exist above the band: maroon-a can't leave rows 6-11 - 6 wide vs 3-wide gap).
- Plus exit needs a top-left presence; only route in = piston shove left through cols 21-23 (no left-firing maroon) or maroon-a parked at cols 15-20 rows 6-11 (needs O push leg1 45-50->30-35 cap15, then P push leg2 from top-middle 30-35->15-20, stopping flush on plus arm) - but leg2 strands P above the band. CONTRADICTION -> untested mechanic must exist.
- Working sub-plan (if maroon-a reaches 15-20): its down-zone cols 15-20 rows 12-17 covers plus arm (15-17,12-14); wrap shoves plus through rows 18-20; O parked rows 21-23 cols 9-14 as landing-blocker -> plus lands (13,28) right below O; O pushes Down -> catch (13,40). O route to left-middle: rows 30-32 passage. O to top-right for leg1: middle->corridor 27-29->strip 51-62->rows 18-20 gap->top-right.
- O launch recipe: click O, U,U (rows 51-53->45-47), R,R,R (cols 42-47; careful maroon-b at rows 48-53), 1 filler tick, wrap -> O lands rows 33-35 cols 42-47.
- P outline walk (no piston): high road 10 presses crosses zone-b cols 42-47 (phase care) or low road ~17 presses under row 57.
## This call: CLICK PROBE (4 actions, 2 ticks -> phase 2): ACTION6(13,13) [plus center], ACTION3; ACTION6(47,8) [maroon-a], ACTION3. Decode by which object moves: plus moves left = plus activatable (game-changer: maybe walk plus to (13,40) if it keeps block purple-crossing); maroon moves = maroons activatable; P moves left = clicks were no-ops (P drifts toward outline, zero waste). Next fallbacks: token-pushes-token test; piston adaptivity via leg1.

## CLICK PROBE RESULT (344-347): clicks on plus (13,13) and maroon-a (47,8) = NO-OPS. Not activatable. P walked left twice: now cols 48-50 rows 42-47. Phase 2.
## FULL SOLUTION SKELETON (hinges on tokens-push-tokens):
1. TEST+SETUP (this batch): O pushes P right (P at 48-50 rows 42-47, O approaches from west at rows 45-47). If P slides (block rules, 15-cap/wall-stop -> cols 60-62): MECHANIC CONFIRMED. O ends cols 42-47 rows 45-47 = in zone-b.
2. O launch (next batch m1 = wrap w/ O in zone): O -> rows 33-35 cols 42-47. O east: rows 30-32? no - up to rows 27-29, east corridor cols 48-62, north strip cols 51-56 through rows 18-20 gap, into top-right rows 6-11 cols 51-56 flush E of maroon-a. Push LEFT: maroon-a 45-50 -> 30-35 (leg1).
3. O return: south strip, west corridor, middle, rows 30-32 passage west into left-middle, up W lane, park rows 21-23 cols 9-14 (BLOCKER, must be set before leg2's next wrap).
4. P: click P, walk into zone (cols 45-47 rows 42-47), wrap -> launched -> rows 30-35 cols 45-47. West to cols 33-35, up gap (rows 12-17), east 1 (36-38), up 2 (rows 6-11), push LEFT: maroon-a 30-35 -> 15-20 flush on plus arm (leg2). Return: down 2, west 1, down gap to rows 30-35, west to cols 27-29 rows 30-35 PARK flush above band. AVOID cols 33-35 rows 12-17 (maroon-a zone after leg1) at wraps.
5. Wrap after leg2: maroon-a (15-20) down-piston shoves plus through rows 18-20; O blocker at rows 21-23 cols 9-14 -> plus lands (13,28) flush below O. O press DOWN -> plus slides, CATCH at outline (13,40). PLUS DONE.
6. O: down to rows 30-32, east passage, to rows 27-29 cols 24-29 (above P). Press DOWN -> pushes P through band -> slide 15 = rows 45-50 cols 27-29 = P OUTLINE (cap AND catch agree). P DONE.
7. O press UP -> rows 24-26 cols 24-29 = O outline. WIN.
## This batch (phase 2 start): click O + R(36-41),Rnoop(push immobile b),Rnoop,Rnoop(WRAP m4 - O clear of zone),U(48-50),U(45-47),R(39-44),R(42-47 flush),R-PUSH-P. Phase after = 5. P expected cols 60-62 rows 42-47 (slide, wall-capped) or 51-53 (3-walk token rules = finale DEAD, rethink) or no move (can't push inactive = DEAD).

## TOKENS-PUSH-TOKENS CONFIRMED (action 357): O pushed P; P slid 12 cells, wall-capped at cols 60-62 rows 42-47. Block rules apply (cap 15, wall stop). FINALE VALID.
- Inactive token center renders 'q'; active renders '$'. Clicks free. Phase after 357 = 5.
## Batch 358-377 (20 moves, O active): m1 U (O 45-47->42-44 in zone, WRAP -> launch -> rows 33-35 cols 42-47), U,U (rows 27-29), R,R,R (cols 51-56), U x7 (m7 wrap @ rows 24-26 clear; m13 wrap @ rows 6-8 clear) -> rows 6-8, m14 L PUSH: maroon-a 45-50 -> 30-35 rows 6-11 (leg1 DONE), m15-m20 D x6 -> rows 24-26 cols 51-56 (m19 wrap @ 21-23 clear). Phase after = 1.
## Next: O continues D to 27-29, west corridor L x3-4 to cols 42-47, D to 30-32, L x7 through passage into left-middle, up W lane to rows 21-23 cols 9-14 (blocker). Then P: click, walk from 60-62 into zone (L x5 to 45-47), wrap launch, gap route, leg2 push, park cols 27-29 rows 30-35. Then wrap shoves plus -> O pushes D (catch 13,40) -> O exits -> pushes P down (outline catch rows 45-50) -> O steps U into own outline. WIN.

## LEG 1 DONE (actions 358-377): maroon-a at cols 30-35 rows 6-11. O at cols 51-56 rows 24-26. P at 60-62 rows 42-47 (inactive). Phase 1.
## Batch 378-397 (19 O-moves + click): D (rows 27-29), L x10 along corridor (m5 wrap @ cols 39-44 clear; m11 wrap @ cols 22-27 partial-walk clear), D (rows 30-32), L x4 through passage (-> cols 10-15), U x3 (m17 wrap @ rows 27-29 clear) -> BLOCKER POST cols 10-15 rows 21-23 (covers plus arm cols 12-14; landing scan blocks c=25-27 -> plus will land c=28 flush below O). Entry 20: ACTION6(61,44) activates P. Phase after = 2.
## Next batch: P L x5 (m4 wrap @ cols 48-50 clear) -> cols 45-47 rows 42-47 (zone), D-fillers x5 pushing immobile maroon-b (wrap m10) -> P launched -> rows 30-35 cols 45-47. Then: W to cols 33-35 (L x4), up gap U x6 -> rows 12-17, R (36-38), U x2 (rows 6-11), L PUSH (leg2: maroon-a 30-35 -> 15-20). Watch maroon-a zone cols 30-35 rows 12-17 at wraps during gap transit AND after leg2 the plus-shove wrap must find O at blocker (it will be - O parked). Then P: D x2, L 33-35, D x5-6 to rows 30-35, L x2 -> park cols 27-29 rows 30-35.

## BLOCKER SET (378-397): O parked cols 12-17 rows 21-23 (valid: covers plus arm cols 12-14). P active at 60-62 rows 42-47. Phase 2.
## NEW RULE: outline ring CORNER q cells block walking (O's 10th L refused entry to cols 22-27 rows 27-29 due to corner (23,27)); ring EDGE q cells walkable (O occupied (24-29,27)). Finale approach must use cols 24-29 exactly when at rows 27-29.
## FINALE ORDER FIX (P parks LAST to avoid blocking O's transit at rows 30-32):
1. Batch A (now): P L x5 (m4 wrap @48-50 clear) -> zone 45-47; D x5 no-op vs maroon-b (m10 wrap LAUNCH) -> rows 30-35 cols 45-47; L x4 -> 33-35; U x6 (m16 wrap @ rows 24-29 clear) -> rows 12-17 cols 33-35 (ph4; INSIDE maroon-a zone - must exit within 2 moves).
2. Batch B: R (36-38, ph5), U (9-14, ph6 wrap clear), U (6-11), L-PUSH leg2 (maroon-a -> 15-20, ph2). Return: D,D (12-17), L (33-35)... wait P at 36-38: D->9-14? recompute in batch B. W1 wrap 4 moves after leg2 fires plus shove -> lands (13,28) below O. P descends gap to rows 30-35, stop at cols 30-32.
3. Click O: D-push plus (catch 13,40). O: D x3 (rows 30-32), R x4 (cols 24-29 flush left of nothing; P at 30-32 clear), U (rows 27-29, cols 24-29 - no corner).
4. Click P: L -> park 27-29 rows 30-35 under O.
5. Click O: D-PUSH P (slides 15, catch -> rows 45-50 outline), U (interior 24-26). WIN.

## BATCH A DONE (398-417): P launched (407 wrap), at cols 33-35 rows 12-17. O blocker intact. Phase 4.
## BATCH B (418-437, 19 moves + 1 click): P: R(36-38,ph5), U(9-14,WRAP clear), U(6-11), L-PUSH LEG2 (maroon-a 30-35 -> 15-20, flush plus arm). P return: D,D(12-17), L(33-35), D(15-20, ph6 W1 WRAP: PLUS SHOVED -> lands (13,28) below O), D x5 -> rows 30-35, L -> cols 30-32 (wrap m14 clear) STOP. Click O (14,22). O: D-PUSH plus -> CATCH (13,40) PLUS DONE. D x3 -> rows 30-32. R -> cols 15-20 (ph5).
## BATCH C (finale, 9 entries): R(18-23, wrap clear), R(21-26), R(24-29), U(rows 27-29 - edge q ok, no corner), click P(31,32), P: L -> park 27-29 rows 30-35, click O(26,28), O: D-PUSH P -> slides 15/catch -> rows 45-50 cols 27-29 = P OUTLINE, O: U -> rows 24-26 interior = WIN score 7.
## RISK: W1 partial-zone shove of plus (only 9 arm cells in zone) - verify at next call before batch C; if plus still in top-left, batch B's O moves became walks (O drifts down cols 12-17) - recover/reset.

## W1 SURPRISE (action 425): transport landed plus at (13,25) = first band-free spot, CHAIN-PUSHING O from blocker 21-23 to 30-32 (flush below). Movable blockers get chained, NOT landed-behind. Deeper landing requires IMMOVABLE obstruction (none exists in left-middle). Click at (14,22) hit plus cell = no-op, O never activated; entries 16-19 were P no-ops (P flush above band), entry 20 moved P to 33-35 rows 30-35.
## STATE after 437: plus (13,25) rows 21-29; O cols 12-17 rows 30-32; P cols 33-35 rows 30-35 (active); maroon-a 15-20 rows 6-11 (frozen forever: P can never touch it again - purple cols 21-23 blocks all pushers). Phase 0.
## ANALYSIS: plus appears LOOP-LOCKED: O up-push returns it to (13,13)/(13,10) (in zone), wrap re-shoves to 25. No token can ever stand above plus in left-middle (band rows 18-20 purple, cols 0-18 fully). No immovable blocker possible. Even a RESET cannot help under current model -> a mechanic must be missing. Flush-piston-push disproven (wrap 431 left plus untouched).
## Batch 438-449 (12 entries): m1 O U-PUSH plus (PROBE: flush-stop (13,13) vs chain-slide (13,10)+maroon->rows 0-5). m2-5 R x4 -> O cols 24-29 rows 30-32. m6 U -> rows 27-29 (ph6 WRAP: plus in zone re-shoved -> (13,25) clean, O/P clear). m7 click P (34,32). m8-9 P L,L -> cols 27-29 rows 30-35. m10 click O (26,28). m11 O D-PUSH -> P slides through band, CATCH rows 45-50 = P OUTLINE. m12 O U -> rows 24-26 = O OUTLINE. 2/3 placed, phase 4. O can exit outline west anytime for plus work.

## Turn @438: batch written (13 entries, click prepended since P was active)
["ACTION6(14,31)","ACTION1","ACTION4"x4,"ACTION1","ACTION6(34,32)","ACTION3","ACTION3","ACTION6(26,28)","ACTION2","ACTION1"]
Ticks: U,RRRR,U(=WRAP m6, plus re-shoved to (13,25)),LL,D,U -> phase 4 at end.
CHECK NEXT TURN: (a) m2 probe result — plus flush-stop vs chain vs maroon-a moved; (b) O stayed rows 30-32 after push (flush push = pusher adv 0); (c) P caught at rows 45-50 cols 27-29 = P OUTLINE; (d) O final rows — if 27-29 (push advanced O down at m12's D), need 1 more U to reach interior rows 24-26.
Then: attack plus loop-lock with probe data.

## BREAKTHROUGH @451 (after batch 438-450 all worked: P seated 45-50/27-29, O seated 24-26/24-29 active)
- 439 probe: plus slid up flush-stop (13,13); wrap fired AT 439 (phase was 5 not 0 — maroon bodies ARE the phase clock: orange rows accumulate 1/move from far end; 5 orange = next move fires). Fire knocked plus back to (13,25) and RECOILED maroon-a body UP 3 (now rows 3-8, cols 15-20). Landing rule re-confirmed band-relative.
- LOOP-LOCK WAS FALSE: west lane cols 0-8 of left region is WALKABLE to rows 21-23 (plus only occupies cols 9-17; top arm only cols 12-14). O at cols 6-11 rows 21-23 has wide-arm contact (cols 9-11, row 24) -> D-push sends plus from (13,25) down: cap-15 AND outline-catch both = (13,40). EXACT.
- Partial-contact push advance=0 re-verified (439: O stayed rows 30-32).
## Batch 451-470 (20 moves, O active, phase 3; wraps m3/m9/m15/m21/m27 all harmless):
D,D (rows 30-32), L x8 (cols 0-5), U x3 (rows 21-23), R,R (cols 6-11 — NEVER a 3rd R: would side-push plus via top arm col 12), D = PUSH -> PLUS SEATED (13,40), D x3 (rows 30-32), R (cols 9-14).
## Next batch (7): R x5 (cols 24-29), U,U -> interior rows 24-26 = ALL 3 SEATED = SCORE 7. Verify plus caught at (13,40) before committing.

## PLUS SEATED (451-470): caught at (13,40) exactly. O at cols 9-14 rows 30-32, active. Score still 6 (needs all 3 seated).
## Batch 471-477 (7): R x5 -> cols 24-29 rows 30-32 (passage m4-5, wraps harmless), U -> rows 27-29 (ring edge ok), U -> interior rows 24-26 = ALL 3 SEATED -> expect SCORE 7 / Level 8.
