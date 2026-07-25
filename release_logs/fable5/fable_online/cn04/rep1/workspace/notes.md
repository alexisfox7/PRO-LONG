# Game notes

## SOLVED MECHANIC
- Dock puzzle: player white piece has red feet; move/rotate (ACTION5=90° CW) so ALL feet overlap matching red sockets on a target structure. Overlap = level clear.
- Move = 3px/action. Timer bar row 0 resets each level (32px); rotations cost 1px, moves mostly free. Not binding so far.
- Level 1 solved in 14 actions (could be ~8 optimal).

## Level 2 (Action 14+, orange bg)
- Player L-shape rows 11-28 cols 11-19; foot A DOWN at (17-19,20-22), foot B RIGHT at (14-16,26-28). Feet Δ = (-3,+6).
- Targets: green (sockets (45,15),(51,21),(51,27),(39,30)), yellow (sockets (18,39),(33,39),(15,45),(27,54)), blue ((51,51),(57,51)).
- Match: yellow pair (18,39)up & (15,45)left. 6 downs docked: feet+sockets MERGED to gray 'h'. Score unchanged — level continues.
- CHAIN MECHANIC: merged white+yellow assembly now has yellow's 2 remaining red protrusions as new "feet": right-facing (32-34,38-40), down-facing (26-28,53-55). Δ(-6,+15).
- Green pair matches: west-facing (44-46,14-16) & north-facing (38-40,29-31), Δ(-6,15). Translation +12x,-24y = 8 ups + 4 rights (ups first; path checked clear).
- After green dock, green's remaining sockets (51,21)e,(51,27)e likely must chain to blue ((51,51),(57,51) up-facing, Δ(6,0))... green leftover Δ(0,6) vertical vs blue (6,0) horizontal → will need rotation? Check later whether assembly can rotate (ACTION5).
- Turn 5 probe RESULT: assembly hypothesis WRONG. White piece detached alone; feet AND yellow sockets reverted red. Docking is reversible, no fusion.
- Enumerated all tab pairs x4 rotations: Y1&Y3 is the ONLY match for player feet, but docking there doesn't clear. => something else must move.
- Tab inventory (center,facing): Green G1(45,15,W) G2(51,21,E) G3(51,27,E) G4(39,30,N); Yellow Y1(18,39,N) Y2(33,39,E) Y3(15,45,W) Y4(27,54,S); Blue B1(51,51,N) B2(57,51,N); Player A(S) B(E), Δ B-A=(-3,6).
- Tab facings imbalanced (4E/2W, 4N/2S) => structures likely need rotation too; all tabs merge pairwise = clear?
- White piece now at: body rows 23-40 cols 11-19, foot A (17-19,32-34) S-facing, foot B (14-16,38-40) E-facing.
- Turn 6 RESULT: ACTION6 click SELECTS a piece (selected piece renders WHITE; deselected reverts to own color — original "white" piece is actually PURPLE '"'). Arrows move selected piece. Yellow moved up 3.
- FULL SOLUTION (tab pairing forced by facing balance; B must rotate 90 CCW = 3x ACTION5):
  P tabs A(18,33,S),B(15,39,E); Y tabs Y1(18,36,N),Y2(33,36,E),Y3(15,42,W),Y4(27,51,S); G static tabs G1(45,15,W),G2(51,21,E),G3(51,27,E),G4(39,30,N); Blue B1(51,51,N),B2(57,51,N).
  Pairs: A-Y1, B-Y3 (P onto Y), Y2-G1, Y4-G4 (Y onto G), Bblue rotated CCW -> tabs W-facing Δ(0,6) onto G2,G3.
  Targets: P shift (+12,-18) from turn-7 position; Y shift (+12,-21); Blue rotate 3xCW then translate (measure after rotation).
  Final assembly verified: overlaps only at tab pairs (18 cells each).
- Y has NO overlap-free path (BFS): assuming transit overlap is allowed (undock slide-through observed). P path IS clear: ups then rights.
- Turn 7 DONE: P at final (body rows 5-22 cols 23-31; tabs (30,15)S,(27,21)E still red awaiting Y).
- Turn 8 sent: ACTION6(24,33) select Y, ACTION1 x7, ACTION4 x4 (dock Y onto P+G; transit overlap assumed OK), then ACTION6(52,57) select blue, ACTION5 x3 (rotate 270 CW = CCW 90; tabs should face W, Δ(0,±6)).
- Turn 8 DONE: Y docked (all 4 tabs gray) — transit overlap IS allowed, pieces never block. Blue rotated: tabs W-facing at (51,51),(51,57).
- Rotation pivot note: blue tabs stayed at same left position after 3xCW — rotation keeps bbox roughly in place.
- Turn 9 sent: ACTION1 x10 (blue already selected) -> tabs onto G2(51,21),G3(51,27). Expect score 2 + Level 3.
- LESSON for future levels: pieces overlap freely in transit; only final tab-on-tab (opposite facings) matters; assembly = all tabs paired -> clear.

# Level 3 (Action 62+, score 2, orange bg, timer full 32)
- Green piece left (rows 14-34, cols 8-22): S/C shape, 2 E-facing tabs at (21,15) and (21,33), Δ(0,18).
- Off-black 'q' L-piece top-right (rows 11-16, cols 32-49); 'q' maze piece center (rows 29-49, cols 29-49). NO red tabs on q pieces!
- Open Q: are q pieces movable? do they hide sockets? Maybe green must physically slot into maze.
- Turn 10 RESULT: L3 renders SELECTED piece green + red tabs visible; UNSELECTED pieces off-black, tabs hidden. All 3 shapes are movable pieces.
- Piece S (initially selected, now dark at orig position): 2 E tabs at (21,15),(21,33), Δ(0,18).
- Piece L (now selected, moved up 3; body row 11-13 col 47-49 block + rows 11-13? actually bar rows 11-13 cols 35-49 + ...): tabs W(33,12), N(48,9). Original position tabs: W(33,15), N(48,12).
- Piece M (maze, rows 29-49 cols 29-49): tabs unknown.
- Timer consumed 1px on L's move (moves DO cost sometimes; ~7px used in 63 actions, fine).
- Balance guess: M has 1 W + 1 S tab (to pair S's 2E... no: E2/W1 -> M needs 1W; N1 -> M needs 1S) unless rotations.
- Turn 11 RESULT: M (maze) tabs: N(33,30), E(48,45). Pieces show TRUE color when selected (S=green, L=yellow, M=purple).
- SOLUTION SEARCH (verified, unique minimal): rotations S:0, L:0, M:180 (2x ACTION5). Pairs: S.E(21,15)-M.W'; S.E(21,33)-L.W; L.N(48,9 cur)-M.S'.
- Relative offsets (M-rotated frame anchor): S at (-69,-60), L at (-81,-39). Assembly fits board (w<=63,h<=62). No body overlaps.
- Piece bodies: S=117 cells, L=45 (bar 15x3), M=180.
- Turn 12 DONE: M rotated 180 in place. New tabs: W(30,33), S(45,48).
- Turn 13 sent (20 actions): click S(15,15), R x3, D x6 [S done: tabs at (30,33)✓,(30,51)]; click L(40,12), L x1, D x8 [L partial: needs 5 more downs].
- Turn 14: ACTION2 x5 to finish L -> L.W at (30,51), L.N at (45,48) -> level clear expected (score 3).

# Level 4 (Action 92+, score 3, blue 'f' bg, timer full)
- Piece A (light-blue '(', selected initially): rows 11-31 cols 8-25 complex shape; 2 S-facing tabs: (24,27), (9,33). Δ(15,-6).
- Piece U (dark): rows 20-31 cols 35-49, upward-open U. Piece R (dark): rows 41-58 cols 44-58 ring w/ channel. Piece B (dark): bar 9x3 rows 47-49 cols 17-25.
- Turn 15 reveals: A(lt-blue): S(24,27),S(9,33). U(green, rows20-31 cols35-49): W(36,21),E(48,21). R(orange ring rows41-58): W(45,42),W(45,57). B(yellow 3x3 at (21,48)): W(18,48),E(24,48).
- SOLUTION: rots A0,U1,R1,B1 (1 CW each for U,R,B; A never moves).
  Final targets: U body (14-25,29-37), tabs N(24,27),S(24,39); R body (8-25,41-49), tabs N(24,39),N(9,39); B body (8-10,35-37), tabs N(9,33),S(9,39).
  Pairs: A.S(24,27)-U.N; U.S(24,39)-R.N; A.S(9,33)-B.N; B.S(9,39)-R.N.
- Turn 16 sent: click+rotate U, R, B (6 actions). B ends selected.
- Turn 17 measured post-rot: U tabs N(45,21),S(45,33); R tabs N(45,42),N(60,42); B tabs N(18,48),S(18,54).
- Deltas: B(-9,-15)=3L+5U; U(-21,+6)=7L+2D; R(-36,-3)=12L+1U.
- Turn 17 sent (20): B full move (8), click U(45,27)+7L+2D (10), click R(50,45)+1L (2).
- Turn 18 FIX: click (45,27) MISSED U body (hole in rotated C-shape) -> B stayed selected, drifted to left edge (clamped at x=2; board edge blocks moves) then 2 downs. LESSON: always click a verified body cell!
- Board edges DO block movement (B clamped at col 2).
- Turn 18 sent (20): R 11L+1U (docks R), click B(3,42)+2R+2U (docks B), click U(36,24)+2L.
- Turn 19: U needs 5 more lefts + 2 downs -> completes level (score 4).

# Level 5 (Action 148+, score 4, purple bg, timer full)
- P1 (selected, yellow): body rows 14-22 cols 26-31 (S-ish), 3 tabs: E(30,15), W(24,18), E(34,21). WHITE $ 3x3 at (26-28,23-25) attached below leg — unknown meaning (core? anchor?).
- P2 dark top-right rows 5-19 cols 47-55 (n/H shape). P3 dark left rows 38-52 cols 5-13 (E shape). P4 dark bottom-right rows 47-55 cols 47-55 (U/J shape).
- Turn 20 reveals (CORRECTED after parse bugs — always derive tabs programmatically!):
  P1: E(30,15), W(24,18), E(33,21) + white $ block (26-28,23-25) part of body.
  P2: N(54,6), N(48,9) [staggered Δ(-6,3)]. P3: E(12,39),E(12,45),E(12,51). P4: N(48,48), N(54,51) [staggered Δ(6,3)].
- NO perfect matching exists (10 tabs). MAX = 4 pairs w/ 2 dangling: rots P1:1cw, P3:1cw, P2&P4 none.
  Pairs: P1.S x2 <-> P2.N x2 (stagger matches!); P1.N <-> one P3.S; P4.N (one) <-> another P3.S.
  Hypothesis: 4-pair connected assembly may clear; else white block may accept a dangling tab.
- Turn 21 sent: click P1(27,15)+ACTION5, click P3(6,39)+ACTION5. Next: measure, choose variant minimizing moves, translate all.

# Level 1 details (historical)

## Initial board (Action 0)
- 64x64, bg '(' light blue. Shapes drawn with 3px-thick strokes → logical cell = 3x3 px.
- Timer bar: row 0, cols 16-47 ('q' off-black), 32px wide. Hypothesis: shrinks per action.
- Player: white '$' shape rows 11-25 cols 11-25, with red 'n' feet rows 26-28 at cols 14-16 & 20-22 (feet centers 6px apart, horizontal).
- Target: green 'I' ring cols 41-49 rows 29-49 (9 wide, 21 tall), red 'n' sockets on LEFT exterior cols 38-40 at rows 35-37 & 41-43 (6px apart, vertical).
- Hypothesis: rotate player 90° (feet pointing right?) and move so red feet align with green red sockets. ACTION5 may rotate.

## Confirmed mechanics
- Movement = 3px per action (one cell). ACTION4 moved shape x+3; timer unchanged.
- ACTION5 = rotate 90° CW (feet down -> left). Timer lost 1px (32->31, consumed pixel turns '$').
- Timer possibly only depletes on rotation, or every 2 actions. 31px left — not binding yet.

## State after Action 2
- Player bbox x14-31, y11-25; feet point LEFT at cols 14-16, rows 14-16 & 20-22.
- Target: feet pointing RIGHT at cols 38-40, rows 35-37 & 41-43 (green ring left sockets).

## Turn 2 result (Action 10)
- Rotations worked: feet point RIGHT at cols 29-31, rows 32-34 & 38-40.
- Timer 28px after 10 actions (rotations cost 1 each; some other cost too).

## Turn 3 plan
- Feet need +3px down, +9px right to hit sockets (cols 38-40, rows 35-37 & 41-43).
- Sent: ACTION2, ACTION4 x3. Expect dock -> score. If blocked at green wall, re-evaluate (maybe feet must PLUG INTO ring interior instead).

## L5 growth log (P1 extensible, fixed rotation r0 — ACTION5 grows, never rotates)
- Press 1 (a152): +spine seg (27,24) with W tab (24,24); tip -> (27,27)... wait tip->(26-28,26-28)
- Press 2 (a156): +arm east rows 26-28: body (27,27)?? actually arm cells (30,27),(33,27),(36,27) + converted tip cell (27,27); E tab (39,27); tip -> (27,30)
- After press 2: P1 tabs E(30,15), E(33,21), E(39,27); W(24,18), W(24,24). 12 tabs total on board.
- PROVED: no perfect matching at 12 tabs (facings forced P3=E/P2=W/P4=W; P2 dΔ(3,6) fits e1,e2; P4 Δ(3,-6) cannot cover e3 + P3 3rd slot). Growth must continue.
- P2 r3 W-tab rel Δ(3,6) == P1 e1->e2 Δ. P4 r3 W-tab rel Δ(3,-6).
- P3 currently r1 (S tabs (6,45),(12,45),(18,45)); r0 = E tabs colinear Δ(0,6); need 3 CW presses to return.
- Hypothesis: press 3 adds W(24,30) completing W column colinear Δ(0,6) x3 for P3 dock; expect ~14 tabs final (P1 E4 W3? balance E7W7 with P3=E,P2=W,P4=W).
- Sent a157-158: ACTION5 x2 (P1 still selected). Timer at a156: 2px used, 30 left.

## L5 SOLUTION (verified perfect matching, 7 pairs, P1 anchored)
P1 final tabs: E(30,15),(33,21),(39,27),(36,33); W(24,18),(24,24),(24,30). Growth done (tip gone after 4 presses).
Targets (tab-cell coincidence):
- P3 r0: E-tabs -> (24,18),(24,24),(24,30). Final body: bar (18,18..30 step3), legs (21,18),(21,24),(21,30).
- P2 r3: W-tabs -> (30,15),(33,21). Final body: (33,15),(36,15),(39,15),(42,15),(36,21),(39,21),(42,21),(42,18).
- P4 r3: W-tabs -> (36,33),(39,27). Final body: (39,33),(42,33),(42,30),(42,27).
Sent a159-170: rotate P3 x3 (click 12,39), P2 x3 (click 51,18), P4 x3 (click 51,54).
Next: measure post-rotation positions, translate each piece (click + moves) onto targets.

## L5 translations (measured after rotations, a170)
- P3 r0 at tabs (12,39),(12,45),(12,51); body bar x=6 y39-51, legs x=9. Move: 4R,7U. Click (6,45).
- P2 r3 at tabs (48,6),(51,12); body (51,6),(54,6),(57,6),(60,6),(60,9),(60,12),(54,12),(57,12). Move: 6L,3D. Click (57,6).
- P4 r3 at tabs (48,54),(51,48); selected already. Move: 4L,7U.
Sent a171-190: P4 4L+7U; click P2 (57,6); 6L; 2D. REMAINING next turn: 1x ACTION2 (P2 last down), then click P3 (6,45), 4x ACTION4, 7x ACTION1.

## LEVEL 5 CLEARED at a203 (score 5). Total plan worked exactly: grow P1 x4, rotate P3->r0/P2->r3/P4->r3, translate all onto P1 anchor.

## LEVEL 6 (a204+, blue 'f' bg, timer fresh 32px)
5 pieces:
- G green (selected at start): bar y=6 x6-18; col x=6 y9-18; (18,9); (9,18). Tabs S(18,12), E(12,18), S(6,21).
- Q2 top-right: (48,6),(51,6),(54,6),(57,6),(48,9),(48,12),(57,9),(57,12),(54,15),(57,15). Tabs hidden.
- Q3 zigzag mid-left: (27,21),(24,24),(27,24),(21,27),(24,27),(24,30),(24,33). Tabs hidden.
- Q4 left tall-L: (6,39),(6,42),(6,45),(6,48),(6,51),(6,54),(9,54). Tabs hidden.
- Q5 bottom-center: ~(36,45),(42,45),(36,48),(42,48),(33,51),(36,51),(42,51),(45,51),(30,54),(33,54),(44?,54),(33-45,57). NEEDS precise re-parse.
Sent a204-207: reveal clicks (51,6),(24,27),(6,45),(36,51).

## L6 revealed inventory (a207)
- G green rotatable: body (6,6),(9,6),(12,6),(15,6),(18,6),(6,9),(6,12),(6,15),(6,18),(9,18),(18,9); tabs S(18,12), E(12,18), S(6,21)
- Q2 orange rotatable: body (48,6),(51,6),(54,6),(57,6),(48,9),(57,9),(57,12),(57,15); tabs S(48,12), W(54,15)
- Q3 yellow EXTENSIBLE (fixed rot): body (24,24),(27,24),(24,27),(24,30); tip (24,33); tabs N(27,21), W(21,27)
- Q4 lt-blue rotatable: body (6,42),(6,45),(6,48),(6,51),(6,54); tabs N(6,39), E(9,54)
- Q5 purple EXTENSIBLE: body (36,48),(42,48),(33,51),(36,51),(42,51),(45,51),(33,54),(45,54),(33,57),(36,57),(42,57),(45,57); tip (39,57); tabs W(30,54), N(36,45), N(42,45)
- Parity: no perfect matching at 12 tabs for any G/Q2/Q4 rotations (both axes odd-off). Growth mandatory, >=2 tabs.
Sent a208-210: ACTION5 (grow Q5), click Q3 (24,27), ACTION5 (grow Q3).

## L6 growth probes (a208-210)
- Q5 press1: NO tab added; container WIDENED (right wall +3px): tabs now W(30,54), N(36,45), N(45,45) (N spacing 6->9); tip (42,57); body {(33,51),(33,54),(33,57),(36,48),(36,51),(36,57),(39,57),(45,48),(45,51),(45,57),(48,51),(48,54),(48,57)}. Q5 growth TUNES SIZE. Warning: spacing 6 no longer available unless RESET.
- Q3 press1: +body (24,33),(27,33), +S tab (24,36), tip->(30,33). Tabs: N(27,21), W(21,27), S(24,36).
- Balance @13 tabs: no matching. Hypothesis Q3 press2 adds S(30,36) -> 14 tabs; unique facing family: G r3 (E,E,N), and {Q2 r0 + Q4 r1} or {Q2 r3 + Q4 r2}. N4=S4, E3=W3.
Sent a211: ACTION5 (Q3 press 2, Q3 still selected).

## L6 search results (a214, 16 tabs)
- Q3 unfold COMPLETE (tip vanished a214): body {(24,24),(27,24),(24,27),(24,30),(24,33),(27,33),(30,33),(33,33),(36,33),(39,33),(39,30),(39,27),(39,24),(39,21)}; tabs N(27,21), W(21,27), W(36,21), S(24,36), S(39,36), E(42,24).
- Exhaustive search (all G/Q2/Q4 rots x Q5 stages 0-4 simulated):
  - Perfect matching (8 pairs): impossible.
  - 7 pairs + all-5-connected: all offset-inconsistent except 4 configs spanning >57 cells (too big). Zero valid.
- Conclusion: Q5 must grow more; stage>=2 geometry unknown (simulation assumed straight widening — tip may turn corners like L5 unfold).
- Q5 growth semi-irreversible; but proven necessary.
Sent a215-216: click Q5 (33,54), ACTION5 -> observe true stage 2.

## L6 deep-search results (a216)
- Q5 stage2 CONFIRMED = simulation (widen: shift x>=tip+3, +1 bottom cell, tip east; N spacing 12).
- Exhaustive searches ALL ZERO: perfect matching (all rots incl Q3 rotatable, Q5 stages 0-5 sim); 7-pair+all-connected (stages 2-5).
- 7-pair graphs have 3 cycles -> offset consistency kills everything; the 4 consistent span >57.
- Conclusion: some model assumption wrong. Most suspect: Q5 stage>=3 sim (tip may turn corner like Q3's unfold did).
- Note: sim stage3 N-spacing = 15 = Q3 S-S spacing (suspicious design match; Q3.S x2 <-> Q5.N x2 works with Q3 at Q5+(12,9), bodies clear).
Sent a217-218: click Q5 (33,54), ACTION5 -> observe true stage3.

## NEW MECHANIC (a217-218): clicking the CURRENTLY SELECTED piece DESELECTS it (toggle). ACTION5 with nothing selected = no-op (0 diff, no timer cost). Q5 still stage 2.
Sent a219-220: click Q5 (33,54) [selects, was deselected], ACTION5 -> true stage3.

## L6 SOLUTION FOUND (turn ~a220)
Perfect opposite-facing matching IMPOSSIBLE (all matchings offset-inconsistent — verified w/ tallies).
Real solution: 7 opposite pairs + 1 PERPENDICULAR pair (Q2.S + Q3.W both at (36,21)).
Lesson: tab docking may accept any-facing coincidence; old dangling-overlap constraints were wrong and hid this.
Zero rotations. Q3 stays. Displacements (px): G +(9,9); Q2 (-12,9); Q4 (9,-9); Q5 (-12,-9).
Pair cells: (27,21)G.S-Q3.N; (21,27)G.E-Q3.W; (15,30)G.S-Q4.N; (36,21)Q2.S-Q3.W(perp);
(42,24)Q2.W-Q3.E; (24,36)Q3.S-Q5.N; (39,36)Q3.S-Q5.N; (18,45)Q4.E-Q5.W.
Execution: Q5(sel) L4 U3; click(6,6) G R3 D3; click(48,6) Q2 L4 D3; click(6,48) Q4 R3 U3. 29 acts.
Sent a221-240: Q5+G full, Q2 click+L4+D1. REMAINING next turn: D2 (Q2), then ACTION6(6,48), R3, U3 (Q4).
Timer counts UP from col16; 3/32 used pre-move.
