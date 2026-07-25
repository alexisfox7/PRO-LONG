# Level 1 analysis (Action 0)

Board 64x64. Background 'f' (blue). Col 63 = full yellow column (UI/timer?). Row 63 = full black row (UI?).
Vertical light-blue stripe '(' at cols 30-32 — likely a MIRROR line.

Shapes (unit cells are 3x3 pixel blocks):
- BLACK piece (O) with white $ dots (one per unit cell): bar rows15-17 cols18-26 (3 cells),
  leg rows18-23 cols24-26 (2 cells, right-aligned). L-pentomino, leg on RIGHT under bar.
  Dots at (19,16),(22,16),(25,16),(25,19),(25,22).
- q (off-black) shape rows15-23 cols36-44: EXACT mirror of black piece across stripe (center col 31).
  Leg on LEFT. Likely reflection/shadow display.
- YELLOW target shape rows45-53 cols51-59: bar on top, leg on LEFT — same orientation as the q
  reflection, i.e. horizontal flip of the black piece.

Hypothesis: transform (flip/rotate) black piece so it matches yellow target orientation.
Currently mirror-reflection already matches target; maybe submit works, or maybe the piece
itself must match.

Probe 1: ACTION5 (interact/submit?), ACTION4 (move/rotate?). Watch per-action diffs.

## After Action 2
- Col 63 = step budget: 1 yellow cell turns black per action (top-down). 2 used of 64.
- ACTION5: no effect otherwise.
- ACTION4: piece moved right 3px (1 unit). q = live mirror reflection across col 31 (refl col = 62-c).
- GOAL hypothesis: put piece so reflection covers yellow target (bar rows45-47 cols51-59, leg left cols51-53 rows48-53).
- Piece bar now rows15-17 cols21-29. Need piece bar at rows45-47 cols3-11 => down 10 units, left 6 units = 16 moves.

## Level 1 SOLVED (Action 18, Score 1). 18 actions used.
Confirmed: goal = piece's mirror reflection covers yellow target. Dots are holes in piece.

## Level 2 initial
- Mirror stripe cols 36-38 (center 37), now with $ dots every unit row (permeable?).
- Budget col 63 reset to full.
- Piece (right side): top bar r18-20 c45-53; leg r21-26 c51-53; bottom bar r27-29 c51-59 (Z going down-right).
- Reflection q (left): top bar r18-20 c21-29; leg c21-23; bottom r27-29 c15-23.
- Yellow target (LEFT side): top bar r42-44 c9-17; leg r45-50 c9-11; bottom r51-53 c3-11.
- Reflection-covers-target impossible (piece would need cols>63). Hypothesis: piece must CROSS the dotted mirror (flips/teleports). Probe: 4x ACTION3 (left).

## Level 2 probes (Actions 19-22, 4x LEFT)
- Piece O did NOT move. The MIRROR STRIPE moved left 3px/action (dots mark the movable object!).
- Mirror center: 37 -> 25. refl(c)=2*mc-c. Reflection clips at board edge.
- Col alignment for target needs mc=31 (2 rights from 25). ROWS mismatch: piece r18-29, target r42-53 (offset +24).
- Vertical mirror can't change reflection rows. Need unknown vertical mechanic. Probe: ACTION2, ACTION5.
- NOTE: stripe dots period=3, so a 3px vertical stripe shift may be visually undetectable except at edges.

## Level 2 probes (Actions 23-24)
- ACTION2 while controlling mirror: total no-op, did NOT consume budget (mirror can't move vertically).
- ACTION5 = TOGGLE CONTROL between mirror and piece ($ dots mark controlled object). Costs 1 step.
- Now controlling PIECE. Solution: piece down 8 units (rows 18-29 -> 42-53), switch, mirror right 2 (mc 25->31).
  Then refl: top 9-17, leg 9-11, bottom 3-11 = target. 11 actions total.

## Level 2 SOLVED (Action 35, Score 2). Total 35 actions.

## Level 3 initial (fresh budget 64)
- Mirror HORIZONTAL rows 48-50 (center 49), $ dots => mirror currently controlled. Interrupted visually by yellow at cols 33-35 (objects render over stripe => overlap allowed).
- Piece A (7 cells, L): leg r21-29 c12-14 (top), bar r30-32 c12-23 (bottom, extends right).
- Piece B (6 cells): bar r27-29 c45-56 (top, 4u), 2u r30-32 c48-53 (centered below).
- Targets (yellow):
  - top-left r9-14: 2u c12-17 over 4u bar c9-20 = piece B flipped vertically
  - top-center r3-14: bar c33-44 r3-5, leg c33-35 r6-14 = piece A flipped vertically
  - bottom-left r42-47: bar c9-20 r42-44, 2u c12-17 r45-47 = piece B as-is
  - bottom-center r42-53: leg c33-35 r42-50, bar c33-44 r51-53 = piece A as-is
- cols 33-35 free in rows 15-41 (passage exists).
- SOLUTION: piece A -> right 7, down 7 (to c33-44, r42-53). Piece B -> left 12, down 5 (to c9-20, r42-47).
  Mirror up 7 units to center row 28. Then reflections cover top targets, pieces sit on bottom targets.
  Order: A first, then B (B passes through A's start cols), mirror last. ~40 actions incl toggles.
- Unknown: ACTION5 cycle order (mirror->A? mirror->B?). Probe: ACTION5 then ACTION2 (down is needed by both pieces; if mirror keeps control, down 1 folds into plan as up 8).

## Level 3 probe result (Actions 36-37)
- ACTION5: control mirror -> piece A. ACTION2: A down 1 unit (A now leg r24-32, bar r33-35).
- A remaining: right 7, down 6. Then ACTION5 (next: B or mirror?), probe ACTION2.
- Watch: A's descent crosses mirror rows 48-50; expect render-behind/no block (yellow overlapped stripe initially).

## Level 3 status after Action 52
- Piece A ON bottom-center target (leg r42-50 c33-35, bar r51-53 c33-44). Mirror crossing OK.
- Cycle confirmed: mirror -> A -> B. B controlled, moved down 1 (bar r30-32 c45-56, 2u r33-35 c48-53).
- Budget col reset to 0 used (mechanism unclear — maybe replenishes).
- B needs: left 12, down 4. Then ACTION5 -> mirror, 7 ups (center 49->28).
- This call: 12L + 4D + A5 + 3U (20). Next call: 4 more ACTION1.

## Level 3 SOLVED (Action 76, Score 3). Total 76 actions.

## Level 4 analysis
- Mirror rows 9-11 (center 10), $ dots = controlled. Visual gap at cols 39-41 (strip renders over; not a real hole).
- P1 (7 cells): stubs up r18-20 at c12-14 & c24-26; bar r21-23 c12-26.
- P2: vertical 6-unit line c18-20, r30-47.
- Yellow: strip c39-41 r9-26 & r30-47 (gap rows 27-29 = future mirror slot); cross1 bar r21-23 c33-47 + stubs; cross2 = flipped, bar r33-35.
- Decomposition: cross1 = P1@(c33-47) + strip; cross2 = P1 reflection; strip lower = P2@(c39-41, rows already correct); strip upper = P2 reflection. Mirror center must be row 28.
- SOLUTION: mirror down 6; P1 right 7; P2 right 7 (rows all already correct). Both pieces need identical move, so toggle order irrelevant. 22 actions: 20 now + 2 next call.

## Level 4 SOLVED (Action 98, Score 4). Total 98 actions.

## Level 5 initial
- VERTICAL mirror cols 9-11, holes 'f' at col 10 (NOT dotted). HORIZONTAL mirror rows 15-17, $ dots = controlled. Gaps in horiz mirror at c12-23, c36-38 (yellow T renders there).
- Piece O (11 units, staircase) units (col/3,row/3): r12 c14-17; r13 c17; r14 c17-18; r15 c18; r16 c16-18.
- T (yellow, unit): r5 c4-7+c12; r6 c7; r7 c7-8; r8 c8; r9 c6-10; r10 c8; r11 c8-9; r12 c9; r13 c4+c9-12. 23 cells, 180-symmetric about (8,9).
- Decomposition: P@(4,5) + P180@(8,9) covers all but (12,5),(4,13); implies vert mirror unit c8 (cols 24-26), horiz unit r9 (rows 27-29). But full 4-image model creates many extras -> model wrong OR piece is multiple pieces OR partial reflections.
- (12,5)=Ph image of base(4,5) only; (4,13)=Pv image of base(4,5) only. Curious: only the CORNER cell's single reflections appear.
- Probe: 3x ACTION5 to enumerate control cycle.
- CANDIDATE SOLUTION (unique by decomposition): piece to unit (4,5) i.e. left 10, up 7 from (14,12);
  vert mirror c3->c8 (right 5); horiz mirror r5->r9 (down 4). Covers T fully + 10 extra refl cells.
  Hypothesis: extras allowed (win = all yellow covered). If fail, need stricter model.

## Level 5 cycle (Actions 99-101): hmirror -> vmirror -> piece -> hmirror. Now: hmirror.
Plan: 4x down (hmirror r5->r9), A5, 5x right (vmirror c3->c8), A5, piece 10 left + 7 up.
This call: 4D,A5,5R,A5,9L (20). Next call: 1L + 7U.

## Level 5 SOLVED (Action 129, Score 5). Extras ALLOWED (win = all yellow covered).
Budget col stopped incrementing after action ~36 — NO budget pressure anymore.

## Level 6 analysis
- hmirror rows 0-2 ($ dots, controlled). vmirror cols 21-23 (renders behind yellow).
- 5 pieces (13 cells, units): bar3 {(15,3),(16,3),(17,3)}; vert3 {(14,4),(14,5),(14,6)};
  s1 {(18,4)}; s2 {(15,7)}; L5 {bar (17,9)-(20,9), stub (18,8) above cell2}.
- T: 52 cells, 4-fold symmetric about axes u6 (cols 18-20) and r11 (rows 33-35). Pieces tile one quadrant.
- FINAL CONFIG: vmirror left 1 (u6); hmirror down 11 (r11).
  vert3 -> (7,4..6): 7L. bar3 -> (8..10,7): 7L 4D. s1 (18,4)->(8,3): 10L 1U. s2 (15,7)->(11,6): 4L 1U.
  L5 -> bar (2..5,13), stub (3,12): 15L 4D (only 180-quadrant works; orientation matches natural).
- Total ~53 piece moves + 12 mirror + ~7 toggles. Cycle order unknown; all pieces need >=4L so lefts safe.
- Call 1: 11xD (hmirror), A5, 1L (vmirror?), A5, 4L (some piece). Then observe dots each call.

## Level 6 progress after Action 147
- Mirrors DONE: hmirror r33-35, vmirror c18-20. Cycle: hmirror -> vmirror -> L5 (-> ? -> ...).
- L5 controlled: 4L done, remaining 11L + 4D.
- Unmoved pieces (units): bar3 r3 c15-17 (needs 7L 4D); vert3 c14 r4-6 (7L); s1 (18,4) (10L 1U); s2 (15,7) (4L 1U).
- This call: 11L+4D (L5 done), A5, 4L (safe for any next piece). Track dots next call.

## Level 6 after Action 167 — KEY DISCOVERY
- The four "small pieces" (bar3, vert3, s1, s2) are ONE diagonally-connected 8-cell piece!
  All dotted, all moved 4L together. Objects = diagonal connected components.
- L5 placed correctly: bar (2-5,13), stub (3,12).
- 8-piece now: (10,4),(10,5),(10,6),(11,3),(12,3),(13,3),(11,7),(14,4).
- Solver (extras allowed, mirrors u6/r11 fixed): UNIQUE translation dx=-3, dy=+12.
- This call (168-182): 3L + 12D = 15 actions. Should clear Level 6 (score 6).

## Level 6 SOLVED (Action 182, Score 6). Total 182 actions.

## Level 7 analysis
- hmirror urow 5 ($ = controlled), vmirror ucol 3.
- Piece A (14u): rows16-19 cols5-9 blob (5x2 core r17-18 c5-9, bumps up/down at c6,c8).
- Piece B (9u, staircase): c17 r17-19; c18 r15-17; c19 r13-15.
- Target 42u, 180-symmetric about (12,7). Optimal (searched all mirror configs, no cheaper):
  mirrors -> u12 (9R), r7 (2D); A +3R 6U -> cols8-12 rows10-13; B 2L 12U -> c15 r5-7, c16 r3-5, c17 r1-3.
  Cost 34 moves + toggles. Extras (single-mirror images) allowed.
- Call (183-201): 2D, A5, 9R, A5, 6U (both pieces need >=6U so safe blind).
- Remaining after: if A controlled: 3R done? no — A needs 3R+0 more U; if B: 6 more U + 2L. Check dots.

## Level 7 status after Action 201
- Mirrors DONE (vm u12, hm r7). Cycle: hmirror -> vmirror -> B (staircase). B got the 6U (now c17 r11-13 etc).
- This call (202-219): B 6U+2L (done at c15 r5-7, c16 r3-5, c17 r1-3), A5 -> expect A, 3R+6U (A to cols8-12 r10-13).
- If toggle went to hmirror instead: 3R = no-ops, 6U moved hmirror up 6 (fix: 6D + re-toggle).
- Expect score 7 at action 219.

## Level 7 SOLVED (Action 219, Score 7). Total 219 actions.

## Level 8 analysis
- hmirror urow5 (controlled), vmirror ucol3. Target 60u, 4-fold symmetric about (12,11).
- P1 (7u): bar (7-9,7) + vert (9,8-11) below RIGHT end. P2 (8u): (13,13),(14,13),(13,14),(13-17,15).
- OPTIMAL (searched, unique 44): mirrors u12 (9R), r11 (6D);
  P1 +9R 4U -> bar (16-18,3), vert (18,4-7) [top-right quadrant remainder];
  P2 -9L 7U -> (4,6),(5,6),(4,7),(4,8)-(8,8) [top-left quadrant remainder].
- Call (220-239): 6D, A5, 9R, A5, 3U (safe: P1 needs 4U, P2 needs 7U).
- Next: identify piece by dots; finish (P1: 1U+9R; P2: 4U+9L), toggle, do other piece.

## Level 8 status after Action 239
- Mirrors DONE (u12, r11). Cycle: hm -> vm -> P2. P2 got 3U (now r10-12).
- This call (240-259): P2 4U+9L (done), A5, 6R (P1 needs 9R+4U; if toggle hit hmirror, rights = free no-ops).
- Next call: P1 remaining 3R+4U (or 9R+4U if toggle went to hmirror + extra A5). Expect score 8.

## Level 8 after Action 259
- P2 placed ✓. P1 controlled, 6R done (bar 13-15,7). This call (260-266): 3R+4U -> clears level. Expect score 8 at action 266.
