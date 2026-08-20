# Game notes (Level 1)

## Layout (initial state, Action 0)
- Play grid: white border rows 8-42, cols 13-50. Inside: 9 cols x 8 rows of 4x4 cells, checkerboard O/q.
  - Cell (bc,br) top-left = col 14+4*bc, row 9+4*br.
- Yellow BLOCK: rows 13-16, cols 30-33 (grid cell br=1, bc=4). 4x4 solid G with 2-wide notch (qq) at bottom center (row 16, cols 31-32).
- Yellow CUP/socket: rows 33-37, cols 29-34. U-shape, walls at cols 29 & 34, floor row 37, with 2-wide bump (GG) at row 36 cols 31-32 — matches block's notch. Same column center (31.5) as block.
- Bottom panel rows 41-47 (white): 5 glyphs centered at cols 21,26,31,36,41. Colors: O,8,O,8,8 (black, offwhite, black, offwhite, offwhite). Glyph = 3-wide bar (row 42) + 1-wide stem (rows 44-46).
- Blue circle: rows 51-59, cols 32-40, center ~(36,55). Callout line ($): from circle top (36,50) → row 49 spanning cols 36-48 → up at col 48 to row 48 (touching under panel right edge).

## Hypotheses
- Block should fall/drop into cup (notch matches bump; already column-aligned).
- Blue circle may be a button; panel sequence may be a code (binary O/8: 0,1,0,1,1?).

## Probes (Action 1-2)
1. ACTION6(36,55) click blue circle
2. ACTION6(31,14) click yellow block

## Learned (Actions 1-2)
- Row 1 = timer bar: 61 f initially, -1 per action (~60 budget).
- Blue circle (36,55) = PLAY button. Executes 5-slot sequence in panel (slots centered cols 21,26,31,36,41, rows 42-46).
  - O (black) slot = block moves DOWN 1 grid cell on that beat; 8 (off-white) = no-op.
  - After sequence completes without landing in cup, board reverts (demo-like).
- Clicking the block itself does nothing.
- Block start br=1; cup at br=6 (block must rest rows 33-36). Need 5 downs = all 5 slots O.
- Current sequence: O,8,O,8,8. Need to toggle slots 2,4,5 → O by clicking (hypothesis).

## Learned (Actions 3-6)
- Clicking slot stems at (26,44),(36,44),(41,44) does NOTHING (panel unchanged).
- Play (A6) replayed same demo: block down on beats 1,3 (O slots), ends rows 21-24 (br=3, bc=4), reverts.
- New hypotheses: (a) slot clickable area = top bar row 42; (b) cup is movable - place it at block end position (br=3), i.e. cup walls rows 21-24, floor 25.
- A7 probe: click (26,42) [slot2 bar]; A8 probe: click (31,23) [grid cell br=3,bc=4].

## Learned (Actions 7-8)
- CONFIRMED: slot toggle click target = top bar row 42 (e.g. (26,42)). Slot2 bar toggled 8->O. Stem rows 44-46 unchanged (stem color may be cosmetic/other meaning).
- Grid cell clicks do nothing; cup not movable by click.
- Plan: toggle slot4 (36,42), slot5 (41,42) -> all O; press play (36,55) => 5 downs, block lands in cup br=6.

## Level 2 (Score 1, board at log line 2198+)
- Right grid: 7x7 cells, cell (bc,br) = cols 33+4*bc, rows 4+4*br. White border col 32/62, row 3/32.
- Block: bc=3, br=5 (cols 45-48, rows 24-27), notch on TOP. Inverted cup ceiling row 7, seat at br=1 (rows 8-11), same column. Need 4 UP moves.
- Program: 3 rows x 4 slots. Bar rows: A=33, B=39, C=45. Slot centers cols 39,44,49,54. All 8 (no-op) initially.
- Left gray panel = worked example: its program row A = all O(black), B/C = 8; scene shows block fused in left-facing cup (rows 16-19, cols 22-25 abs). Suggests channels/directions per row, mapping unknown.
- Legend boxes bottom-left: blue box (cols 7-15): yellow left + $ dots right; gray box (cols 17-25): yellow top + $ dots below. Meaning TBD.
- Play button center (46,58).
- Timer resets each level (61).
- Probe A12-15: toggle A1(39,33), B2(44,39), C3(49,45), play(46,58) -> frames reveal each row's direction on beats 1,2,3.

## Learned (Actions 12-15, L2 probe)
- Confirmed: program columns = beats (highlight surrounds whole column, rows 32-50). All rows of a column fire on its beat.
- Row A (bar row 33) O = MOVE LEFT 1 cell. Row C (bar row 45) O = ROTATE CCW (notch top->left). Row B (bar row 39) O = NO visible effect (beat 2, block at bc=2 br=5, nothing moved anywhere on board incl. left panel).
- Frames have a global 1-row upward scene shift during playback (rendering artifact) - account for it when diffing.
- Board reverts after play; PROGRAM persists. Current program: A1=O, B2=O, C3=O.
- Open q: does clicking an O slot cycle to a 3rd color (more commands, e.g. UP)? Never re-clicked an O.
- A16-19: click A1(39,33) [O->?], C3(49,45) [O->?], B1(39,39) [8->O], play(46,58). Watch cycle colors + beats: if A1/C3 become new color X, frames show X's effect on beats 1,3; B on beats 1&2 (block under cup at start, bc=3).

## Learned (Actions 16-19, L2 probe 2)
- Clicking O slot toggles back to 8 (only 2 states, no color cycling).
- Program was B1=O,B2=O; play ran beats (column highlights f2-f5) but block NEVER moved, even directly under cup. Row B = inert in current mode.
- Level needs 4 UP moves in 4 columns => some mechanism must yield UP. New hypothesis: legend boxes are MODE selectors:
  - Blue-bordered box (cols 7-15, rows 54-62, center ~(11,58)): yellow at left + dots rightward = horizontal axis.
  - Gray-bordered box (cols 17-25, rows 52-62, center ~(21,57)): yellow at top + dots downward/below = vertical axis.
  - Maybe clicking the gray box switches movement rows to vertical (A=?, B=up/down?).
- A20-21: click gray box (21,57), then play (46,58) with B1,B2 armed. Watch for UI change post-click and block motion in frames.

## Learned (Actions 20-21) - KEY MECHANIC
- The two bottom-left boxes are MODE OPTIONS (selected = blue border). Clicking gray box selected option 2 (vertical).
- Selecting an option plays a DEMO in the left panel: with option 2, demo object rose UP 1 cell/beat while left-panel row A (all O) executed. => Option selection sets row-A direction: opt1=LEFT(horizontal icon), opt2=UP(vertical icon).
- Left panel = demo area for selected option; its row C stems turned O (glyph cosmetic, meaning unclear).
- A21 play failed because program had row B armed (B is not a move in either mode so far).
- Current program: A all 8; B1=O,B2=O; C all 8. Mode: option2 (vertical).
- A22-28: clear B1(39,39),B2(44,39); set A1(39,33),A2(44,33),A3(49,33),A4(54,33); play(46,58). Expect 4 ups -> block seats in ceiling cup -> clear.

## Learned (Actions 22-28) - play FAILED, revised model
- With option2 selected and row A bars all O: block moved LEFT each beat and slid OFF-GRID (vanished at beat 4). Bars are ALWAYS horizontal-left here; option boxes do NOT change bar semantics - they only pick which tutorial demo plays in left panel.
- Demo(opt2) program that moved object UP: row C STEMS dark (bars leftover from opt1 demo did NOT execute... in demo only selected-axis commands run).
- Revised model: each slot glyph = BAR (horizontal cmd) + STEM (vertical cmd), separate sub-slots. L2: bar=left, stem=up (both toward cup: option icons show direction toward yellow cup). L1: bar=down (single-axis level).
- Stems were unclickable in L1, but L2 may differ. Post-A28: program rowA bars all O (need clearing later), stems all 8, mode=opt2, timer 44 left.
- A29-30 probe: click (39,48) [C1 stem], (44,36) [A2 stem] - check toggling.

## Learned (Actions 29-30)
- STEMS clickable in L2! C1 stem (39,48) and A2 stem (44,36) toggled to O (full 3px stem darkens). Stem = vertical command sub-slot.
- Current program: rowA bars A1-A4 = O (left moves, must clear); stems dark: col39 rowC, col44 rowA; else 8.
- A31-37: clear bars (39,33),(44,33),(49,33),(54,33); add stems C3 (49,48), C4 (54,48); play (46,58).
- Expect: beats 1-4 each have one up-stem (rows differ; tests row-independence) -> 4 ups -> block seats in ceiling cup -> level clear.

## Learned (Actions 31-37) - play FAILED, better model
- Pre-play program: bars all 8; stems dark: A2(col44), C1,C3,C4. Result: beat1 C1stem=NOTHING, beat2 A2stem=block moved RIGHT 1 cell, beats 3,4 C stems=nothing. Reverted.
- Command table L2: A.bar=LEFT, A.stem=RIGHT, B.bar=nothing(2 tests), B.stem=UNTESTED, C.bar=rotCCW, C.stem=nothing.
- Model: row A=horizontal pair, row B=vertical pair (bar=down? stem=up?), row C=rotation. Demo's "C stems" display was apparently just conceptual animation, not literal.
- Timer 35 left. A38-39 probe: set B1 stem (39,42), play. If block rises on beat1 => B.stem=UP.
- Current stems dark: A2(44), C1(39), C3(49), C4(54). Bars: none.

## Learned (Actions 38-39)
- B.stem ALONE = inert too (block never moved with B1 stem + C stems armed). All single elements now mapped: A.bar=LEFT, A.stem=RIGHT, C.bar=rotCCW; B.bar, B.stem, C.stem alone = nothing.
- COMBO HYPOTHESIS: opt2 demo program had BOTH A bars and C stems dark in all 4 cols while object rose 1 cell/beat. So {A.bar + C.stem} same column = UP (stem redirects horizontal cmd vertically).
- Post-A39 panel: A bars all 8; stems dark A2(44), B1(39), C1(39), C3(49), C4(54). Timer 33.
- A40-47: set A bars x4 (39,33),(44,33),(49,33),(54,33); clear A2 stem (44,36), B1 stem (39,42); set C2 stem (44,48); play (46,58). All cols = {A.bar+C.stem} => 4 UPs => block seats in ceiling cup => clear.

## LEVEL 2 SOLVED (Action 47, Score 2). COMMAND TABLE CONFIRMED
- A.bar=LEFT; A.stem=RIGHT; A.bar+C.stem=UP; C.bar=rotCCW; B row inert.
- L3 demo (DOWN option selected) shows A.bar+A.stem per column => DOWN. Full table: L=A.bar, R=A.stem, U=A.bar+C.stem, D=A.bar+A.stem.

## Level 3 (Score 2)
- Right grid 7x7: cell (bc,br)=cols 33+4bc, rows 4+4br. Block bc=1,br=4, notch TOP. Inverted cup bc=5, ceiling row 11, seat br=2, bump cols 54-55.
- Magenta wall column bc=3 (cols 45-48) all rows EXCEPT br=3 (gap rows 16-19).
- Program: 3 rows x 6 cols. Bars y=33/39/45 (A/B/C); stems y=35-37/41-43/47-49; col centers x=34,39,44,49,54,59. All empty at start.
- 4 option boxes bottom-left: DOWN(selected, blue, cols1-9), UP(11-19), LEFT(21-29), RIGHT(31-39). Icons: yellow=target side, $ dots=trail.
- Play button = blue circle center (57,58). Timer fresh 61.
- Plan A48-56: path U,R,R,R,R,U through wall gap: col1 UP (34,33)+(34,48); cols2-5 RIGHT stems (39,36),(44,36),(49,36),(54,36); col6 UP (59,33)+(59,48); play (57,58). (1,4)->(1,3)->(2,3)->(3,3 gap)->(4,3)->(5,3)->(5,2) seat.

## LEVEL 3 SOLVED (Action 56, Score 3), 9 actions, first try.

## Level 4 (Score 3)
- Grid 7x7 same coords. BIG BLOCK 8x8 (2x2 cells) at bc=3-4, br=1-2 (cols 45-52, rows 8-15), 4-wide x 2-deep notch at BOTTOM center (cols 47-50, rows 14-15).
- Normal cup (opening UP, for 4x4 block w/ bottom notch): bc=2, br=5 (interior cols 41-44 rows 24-27), bump cols 42-43 row 27, floor row 28.
- Magenta wall: whole row br=4 (rows 20-23) EXCEPT gap at bc=2 (cols 41-44) — directly above cup.
- Program: 3 rows x 6 cols, right panel. Bars y=33/39/45; stems y=35-37/41-43/47-49; cols x=34,39,44,49,54,59. All empty. Play button (57,58). Timer 61.
- Option boxes: box1 (5,58) LEFT icon, SELECTED; box2 (15,58) BIG yellow square (grow?); box3 (25,58) DOWN icon; box4 (35,58) tiny square (shrink?).
- IMPORTANT: L4 demo panel (3 cols) for LEFT shows {A.stem + C.stem} dark — CONTRADICTS L2/L3 table (A.bar=LEFT). Hypothesis: glyph->command mapping is PER-LEVEL, taught by demos. Must watch demos.
- Likely solution shape: SHRINK big block to 4x4, then move to cup via gap: e.g. (3,2)-shrunk -> L,D,D,D into (2,5). Need mappings for LEFT/DOWN/SHRINK.
- A57-59: click box2 (15,58), box3 (25,58), box4 (35,58); watch demo frames + demo program panels to learn each command encoding.

## Learned (Actions 57-59) - L4 command table from demos
- Demos confirmed per-level glyph mapping. L4 table (from demo settled program panels, canonical rows):
  - GROW = {B.stem} (obj grew 4->8->12->16 px, top-left anchored)
  - DOWN = {A.bar + A.stem}
  - SHRINK = {A.bar + B.stem} (16->12->8->4, top-left anchored)
  - LEFT = {A.stem + C.stem} (box1 program at level load)
- NOTE: settled boards after demos can show global 1-row UP shift (artifact). Use canonical coords: bars y=33/39/45, stems mid y=36/42/48, cols x=34,39,44,49,54,59, play (57,58).
- Plan A60-72 (13 actions): col1 SHRINK (34,33)+(34,42); col2 LEFT (39,36)+(39,48); cols3-6 DOWN (44/49/54/59: bar 33 + stem 36); play (57,58).
- Path: big block top-left cell (3,1); shrink->4x4 at (3,1); L->(2,1); D x4 ->(2,5) through gap (2,4); seats in cup (bump 42-43 row 27 matches bottom notch).

## LEVEL 4 SOLVED (Action 72, Score 4). 16 actions total. Command table verified in play: SHRINK {Ab+Bs}, LEFT {As+Cs}, DOWN {Ab+As} x4.

## Level 5 (Score 4)
- Block: 4x4 at bc=4,br=1 (cols 49-52, rows 8-11), notch on RIGHT edge (col 52, rows 9-10, 1w x 2t).
- Magenta wall row br=3 (rows 16-19), gap at bc=4 (cols 49-52) directly below block.
- PURPLE cup: walls cols 47-48 & 57-58 (rows 20-29), floor rows 28-29, interior cols 49-56 x rows 20-27 (8x8 = cells bc4-5, br4-5), bump 4w x 2t at cols 51-54 rows 26-27. Fits an 8x8 block w/ 4x2 BOTTOM notch.
- Solution shape: ROTATE CW (notch right->bottom), DOWN x3 (br1->4 through gap), GROW (top-left anchored: 4x4 at (4,4) -> 8x8 cols 49-56 rows 20-27 = exact cup fit). 5 commands, 6 columns.
- 5 option boxes: box1 (5,58) tiny square=SHRINK, SELECTED, program {Ab+Bs} = SAME as L4 shrink (encodings may be stable after all; L2 A.bar=LEFT still unexplained). box2 (15,58) big square=GROW. box3 (25,58) DOWN icon. box4 (35,58) DIAMOND = rotation? box5 (45,58) 3x3 PURPLE square = unknown.
- Demo scene: 16x16 block (4x scale) w/ 8x4 bottom notch — demos act on it.
- Known encodings (L4-proven): DOWN={Ab+As}, GROW={Bs}, SHRINK={Ab+Bs}. Need: rotation CW encoding, purple meaning.
- A73-74: click box4 (35,58), box5 (45,58); read demo frames + settled programs.

## Learned (Actions 73-74)
- Box4 demo: notch cycled bottom->left->top->right = ROTATE CW. Encoding {A.bar + B.bar}.
- Box5 demo: big block turned PURPLE (no motion). Encoding = ALL SIX elements dark in one column {Ab,As,Bb,Bs,Cb,Cs}. Purple cup presumably requires purple block.
- Cumulative encoding table (stable across L4/L5): DOWN={Ab+As}, LEFT={As+Cs}, GROW={Bs}, SHRINK={Ab+Bs}, ROT-CW={Ab+Bb}, PAINT-PURPLE={all 6}. (L2 anomaly: bare Ab=LEFT there; L2/L3 also had UP={Ab+Cs}, RIGHT={As}.)
- A75-90 (16 actions): col1 ROT-CW (34,33)+(34,39); col2-4 DOWN (39/44/49: 33+36); col5 GROW (54,42); col6 PAINT (59,33/36/39/42/45/48); play (57,58).
- Expected: notch right->bottom, drop through gap to (4,4), grow to fill cup interior (cols 49-56 rows 20-27), paint purple, clear.

## LEVEL 5 SOLVED (Action 90, Score 5). 18 actions. ROT-CW, DOWN x3, GROW, PAINT all worked as decoded.

## Level 6 (Score 5)
- Maze level. Block: 4x4 at (0,6) (cols 33-36 rows 28-31), notch LEFT. Cup: opening RIGHT, interior cell (1,1) (cols 37-40 rows 8-11), bump col 37 rows 9-10 on back wall.
- Magenta wall cells (bc,br): (1,0),(3,1),(5,1),(1,2),(3,2),(5,2),(1,3),(3,3),(5,3),(1,4),(5,4),(0,5),(1,5),(2,5),(3,5),(5,5).
- YELLOW-DOTTED phantom cells (checkered G on bg): (5,0),(4,4),(5,6). Hypothesis: CHECKPOINTS (reaching one saves position across runs) — BFS min path start->cup = 12 moves > 6 columns, so multi-run mechanic needed. Checkpoint route: run1 start->(4,4): R,R,R,R,U,U (6); run2 (4,4)->(5,0): U,U,U,U,R (5); run3 (5,0)->cup: L,L,L,D,L (5).
- Option boxes: box1 DOWN (selected; demo prog {Ab+As} matches known), box2 (15,58) UP, box3 (25,58) RIGHT, box4 (35,58) LEFT. Directions only.
- Assumed encodings: R={As}, U={Ab+Cs}, L={As+Cs}?? (L2 said Ab=LEFT — anomaly; box4 demo can confirm before run3), D={Ab+As}.
- A91-101 (11): box2+box3 demos (confirm U/R encodings post-hoc), program R,R,R,R,U,U (cols1-4 As at (34/39/44/49,36); cols5-6 Ab+Cs at (54/59,33)+(54/59,48)), play (57,58).
- Watch: does block stop/save at (4,4)? Does board revert? Are moves 1-cell or slides?

## Learned (Actions 91-101) - CHECKPOINT CONFIRMED
- Run R,R,R,R,U,U executed perfectly (1-cell moves, encodings R={As}, U={Ab+Cs} valid). Block ENDED ON PAD (4,4) and board did NOT revert — block persists there. Checkpoint mechanic real.
- Settled board showed 1-row-up shift artifact (timer appears on row 0: ~57 blue left; possibly timer partially reset at checkpoint).
- Program persists: cols1-4={As}, cols5-6={Ab,Cs}.
- A102-119 (18): retarget program to U,U,U,U,R,-: cols1-4 toggle As off + Ab,Cs on; col5 -> {As}; col6 -> empty; play (57,58). Route (4,4)->U x4->(4,0)->R->(5,0) pad.
- Then run3: (5,0) -> L,L,L,D,L -> cup (1,1). L={As+Cs} (L4-proven; L2 anomaly ignored).

## Learned (Actions 102-119)
- Leg 2 success: block (4,4)->U x4->(4,0)->R->(5,0), persists on pad. Timer 47 left. Pads remain visible after visit.
- Program now: cols1-4={Ab,Cs}, col5={As}, col6 empty.
- A120-129 (10): retarget to L,L,L,D,L,-: col1-3 Ab off+As on (34/39/44: 33,36); col4 Cs off (49,48)+As on (49,36); col5 Cs on (54,48); play (57,58). Expect (5,0)->(2,0)->D(2,1)->L(1,1) seat in right-facing cup => clear.

## LEVEL 6 SOLVED (Action 129, Score 6). 39 actions (3 checkpoint runs).

## Level 7 (Score 6)
- Block (2,6) cols 41-44 rows 28-31, notch TOP. Inverted cup embedded in magenta block (cells bc1-3 x br0-1): interior (2,1) cols 41-44 rows 8-11, bump 42-43 row 8, ceiling row 7.
- Column bc=2 fully free between: straight path U x5 (br6->1).
- Decoys/unused: pads (5,1),(0,2),(5,5); magenta (0,3),(4,5),(4,6); GREEN portal walls col 37 & col 60 rows 16-19 with orange/maroon arrows (wrap tunnel at br=3?) — not needed if straight path works.
- A130-140 (11): cols1-5 = UP {Ab+Cs} (34/39/44/49/54 at y33+y48), col6 empty, play (57,58).

## Learned (Actions 130-140) - BEAM HAZARD
- Straight U x5 FAILED: block rose (2,6)->(2,5)->(2,4), then entering (2,3) triggered the green emitters (col 37 & 60, rows 16-19): full row filled with arrows and block was DESTROYED; board reverted. Row br=3 is a kill-beam spanning bc1-6; (0,3) is magenta => entire br=3 impassable by movement.
- Only 4 direction options this level => pads must bridge the beam. Pads: (5,5) below beam; (5,1),(0,2) above. Hypothesis: stepping onto a pad TELEPORTS to another pad (L6 never tested mid-run/exact-landing semantics beyond persistence).
- Program after fail: cols1-5 U, col6 empty. Timer ~50.
- A141-152 (12): retarget to R,U,U,R,R,D: col1 U->R (34: 33,48 off; 36 on); cols2-3 stay U; col4 U->R (49); col5 U->R (54); col6 D (59,33)+(59,36); play. Route (2,6)->(3,6)->(3,5)->(3,4)->(4,4)->(5,4)->(5,5) pad. If teleport: expect block at (5,1) or (0,2) after; else checkpoint at (5,5).
- Next-leg plans: from (0,2): R,R,U -> cup (3 moves). From (5,1): D,L,L,L,U (5 moves; (3,1) is magenta, go via br=2).

## Learned (Actions 141-152)
- Run R,U,U,R,R,D succeeded: block now persists ON pad (5,5). NO teleport on landing (arrived at final beat 6). Beam/board unchanged. Timer refilled to 50 (checkpoint refreshes timer).
- Hypothesis refinement: teleport may need pad ENTRY with beats REMAINING (L6+L7 landings were always final-beat or run-end). Test: program U,D,----: block (5,5)->U(5,4)->D re-enter pad at beat2 w/ 4 beats left.
- Program before this: col1 R, col2 U, col3 U, col4 R, col5 R, col6 D.
- A153-164 (12): col1->U (36 off... precisely: (34,36)off As,(34,33)Ab,(34,48)Cs), col2->D ((39,48)off,(39,36)As), col3->empty ((44,33),(44,48)), col4 (49,36)off, col5 (54,36)off, col6 ((59,33),(59,36))off; play.
- Outcomes: (a) block ends at (5,1) => teleport confirmed, then D,L,L,L,U to cup. (b) block back at (5,5) => no teleport, rethink (maybe grid clicks, or beam timing).

## Learned (Actions 153-164) - BEAM IS TIMED, NOT TRIGGERED
- U,D test: no teleport; block re-checkpointed (5,5). Timer 44. Start cell (2,6) shows residual pad marker.
- KEY: frames show beam OFF beats 1-2, ON beats 3-6 (fired in empty-column beats with no block near!). Run1 death at beat 3 = block walked into scheduled activation.
- Order within a beat = MOVE then FIRE (run1 died same beat it entered; fire-then-move would have delayed death to beat 4).
- Crossing window: be in br=3 only during beat 2, exit on beat 3 move (before fire).
- A165-171 (7): program U,U,U,U from (5,5): beat1 (5,4), beat2 (5,3) beam row (off), beat3 exit to (5,2) before fire, beat4 land pad (5,1) checkpoint. col1 already U; col2 D->U (39,36 off, 39,48 on); col3,col4 U (44/49 at 33+48); play.
- Then final leg: (5,1): D,L,L,L,U -> cup (2,1) (never touches br=3).

## Learned (Actions 165-171) - BEAM CROSSED
- U,U,U,U worked exactly as modeled: (5,5)->(5,4)->(5,3) [beat2, beam off]->(5,2) [beat3 move-before-fire]->(5,1) pad. Checkpoint held. Timer 40.
- Beat-scheduled hazards confirmed: beam off beats 1-2, on 3-6; move resolves before fire.
- A172-182 (11): retarget cols to D,L,L,L,U,-: col1 (34,48)off+(34,36)on; col2-4 (39/44/49: 33 off, 36 on); col5 U (54,33)+(54,48); play. Route (5,1)->(5,2)->(4,2)->(3,2)->(2,2)->(2,1) cup => clear.
