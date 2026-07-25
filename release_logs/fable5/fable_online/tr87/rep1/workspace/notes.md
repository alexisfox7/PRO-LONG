# Game notes (Level 1)

## Layout (64x64)
- Top: legend of 6 pairs, blue '(' tile <-> magenta 'z' tile joined by 'hhh'.
  Tile origins (r0,c0) of 7x7 tiles; 5x5 glyph at (r0+1,c0+1):
  rows r0 in (4,13,22); blue cols 12 & 35, magenta cols 22 & 45.
  Pair order: (5,13)-(5,23)=pair0, (5,36)-(5,46)=pair1, (14,..)=pair2,3, (23,..)=pair4,5.
- Blue banner: glyph rows 41-45, glyph col starts 15,22,29,36,43 (5x5 each).
- Magenta banner: glyph rows 52-56, same col starts.
- $ cursor: open box at cols 15-19, rows 48-49 (top) + 59-60 (bottom), bracketing magenta slot 0.

## Decoded (initial state)
- Blue banner = legend blue glyphs of pairs [3,4,0,1,2] (each rendered rotated, mostly r1=90°).
- Magenta banner = legend magenta glyphs of pairs [2,5,4,?,0] (rotated variants; slot3 matched nothing).
- Hypothesis: goal = set magenta seq to [3,4,0,1,2] (pair-translation of blue).
- Hypothesis: Left/Right move cursor, Up/Down cycle symbol in cursor slot.

## Parsing helper
Use python: tile(r,c) 5x5 'O'/'.' extraction; dihedral variants matching against legend.

## Probe sent (Action 1-2): ACTION1 (Up), ACTION4 (Right) — observe what changes.

## Confirmed mechanics (after Action 2)
- ACTION1 (Up): cycles glyph in cursor slot. Slot0: M2(rotated) -> M5 (exact orientation).
- ACTION4 (Right): moves cursor right one slot (cols 15->22).
- Row 63 = step budget bar: one '8'->'q' consumed (rightmost col63) after 2 actions. Watch it.
- Targets: magenta slots must become pairs [3,4,0,1,2] (= blue banner translation).
- Current mag: [M5, M5(rot), M4(rot), ?, M0(rot)]; cursor at slot 1.
- Cycle order unknown: M2->M5 via Up. Probing Action 3-5: Up,Up,Down on slot1.

## After Action 5
- Up/Down cycle symbol identity (orientation shown varies, likely cosmetic).
- Observed symbol cycle: 2->5 (Up), 5->0 (Up), 0->1 (Up), 1->0 (Down). Global order: ...2,5,0,1,... with {3,4,'?'} unplaced.
- Slot3 has unknown 7th glyph '?': OOOOO/O...O/OOOOO/.O.O./.OOO. — maybe part of cycle.
- State after A5: mag=[M5,M0,M4,?,M0], cursor slot1, budget bar 62/64 (1 cell ~ 2-3 actions).
- Targets: [M3,M4,M0,M1,M2].
- Actions 6-8: Up (slot1 M0->M1, done), Right (to slot2), Up (learn successor of M4).

## After Action 8
- M4 --Up--> M2. Cycle (Up dir): 4,2,5,0,1,[3,U in some order],back to 4. len 6 or 7.
- State A8: mag=[M5,M1,M2,U,M0], cursor slot2, budget 60.
- Slot1 DONE (M1). Targets remaining: slot0 M5->M3, slot2 M2->M0 (2 ups), slot3 U->M1, slot4 M0->M2 (2 downs).
- Actions 9-12: Up,Up (slot2 done), Right, Down (slot3 probe: if M1 done; if M3 then one more Down needed; resolves cycle fully).
- Unknown: whether cursor wraps right from slot4 to slot0.

## After Action 12
- Down on slot3: U -> M1. Slot3 DONE. Full up-cycle: 0->1->U->3->4->2->5->0 (7 states incl U).
- State A12: mag=[M5,M1,M0,M1,M0], cursor slot3, budget 58. Slots 1,2,3 done.
- Actions 13-22 (finisher): Right, Down, Down (slot4: 0->5->2 done), Left x4 (to slot0), Down x3 (5->2->4->3 done).
- If board matches [M3,M4wait...] — targets [3,4,0,1,2]; after this: [M3,M1?...] no: [3,1,0,1,2]? NO — slot1 target is M4?? Recheck: targets [M3,M4,M0,M1,M2]; slot1 currently M1 but target M4!!

## CORRECTION (before Action 13)
- Slot1 target is M4 (not M1). Current [M5,M1,M0,M1,M0] vs targets [M3,M4,M0,M1,M2]: slots 2,3 done; slot0 needs 3 downs (5->2->4->3), slot1 needs 3 ups (1->U->3->4), slot4 needs 2 downs (0->5->2).
- Route from cursor slot3 (13 actions): R, D,D (slot4), L,L,L (slot1), U,U,U, L (slot0), D,D,D. Sent as Actions 13-25.
- Expect level clear after this; if not, orientation may matter — reassess.

## LEVEL 2 (Action 25 cleared L1; score 1; budget reset 64)
- Settled board at log lines 4220+. New structure: legend = magenta Z symbol -> STRING of yellow glyphs.
  Z tiles at (5,6),(5,29),(14,6),(14,36),(23,6),(23,43); yellow glyph cells listed in code.
- Legend: Z0->[Y0]; Z1->[Y1,Y2,Y3]; Z2->[Y4,Y5]; Z3->[Y6,Y6]; Z4->[Y7,Y8,Y9]; Z5->[Y10].
- Magenta banner rows41-45, glyph cols 19,26,33,40 = [Z0,Z4,Z3,Z5].
- TARGET yellow banner (7 slots, rows 52-56, col starts 8,15,22,29,36,43,50): [Y0,Y7,Y8,Y9,Y6,Y6,Y10].
- Current slots: [Y10~,Y3~,Y7~,Y2,Y8,Y8~,Y1] (~=rotated, cosmetic). Cursor slot0.
- Mechanics assumed same: Up/Down cycle glyph, L/R move cursor, orientation cosmetic.
- Actions 26-38: 13x Up on slot0 to map the glyph cycle (watch for wraparound).

## After Action 38 (L2 spin complete)
- Wheel (same for all slots, 7 states, Up order): idx0=Y10, 1=Y3, 2=Y8, 3={Y1,Y4}, 4={Y0,Y2}, 5={Y5,Y6}, 6={Y7,Y9}.
  Rotation classes: Y0~Y2, Y1~Y4, Y5~Y6~Y6b, Y7~Y9; singles Y3,Y8,Y10. Win = class match (rotation-invariant).
- Current idx: [6,1,6,4,2,2,3]; target idx: [4,6,2,6,5,5,0].
- Full solution 24 actions: DD R DD R UUU R UU R UUU R UUU R DDD. Sent first 20 (through slot5); remainder next call: R,D,D,D.
- Budget 58 cells; fine.

## After Action 58
- Slots 0-5 correct: [Y0/2, Y7/9, Y8, Y7/9, Y5/6, Y5/6, Y1/4]; cursor slot5; budget 48.
- Actions 59-62: R, D,D,D (slot6 idx3->0 = Y10). Expect Level 2 clear (score 2).

## LEVEL 3 (Action 62 cleared L2; score 2; budget reset 64)
- Settled board at log line 8881. Direction reversed: yellow banner (rows 41-45, 8 glyphs, col starts 5,12,...,54) is GIVEN; blue banner (rows 52-56, 7 slots, col starts 8,15,22,29,36,43,50) is EDITABLE (cursor slot0).
- Legend (class ids, rotation-invariant): p0:[0]->[7]; p1:[1,1]->[8,9]; p2:[2]->[10,10]; p3:[3,3]->[11]; p4:[4,5,4]->[8]; p5:[6]->[12].
- Yellow banner classes [0,4,5,4,2,6,1,1]; unique segmentation p0,p4,p2,p5,p1.
- TARGET blue classes: [7,8,10,10,12,8,9]. Current blue: [11,7,7,12,9,7,8].
- Wheel order unknown (6 blue classes + decoys?). Actions 63-70: 8x Up on slot0 to map wheel.
- Class reps stored implicitly; re-derive via cid() ordering: legend glyph scan order Y-then-B per pair as in code.

## After Action 70 (L3 spin complete)
- Wheel Up-order: [11,13,9,10,8,12,7] (13=decoy). Budget 60.
- Current [13,7,7,12,9,7,8] idx[1,6,6,5,2,6,4]; target [7,8,10,10,12,8,9] idx[6,4,3,3,5,4,2].
- Solution 22 actions: DD R DD R DDD R DD R UUU R DD R DD. Sent first 20; remainder next call: D,D on slot6.

## After Action 90
- Slots [7,8,10,10,12,8,8]; cursor slot6; budget 50. Actions 91-92: D,D (8->12? no: idx4->2 = 8->10->9... wheel [11,13,9,10,8,12,7]: down from 8(idx4) -> 10(idx3) -> 9(idx2)). Expect L3 clear (score 3).

## LEVEL 4 (Action 92 cleared L3; score 3; budget 64)
- Board at log line 13472. TWO-STEP legend chains: 4 pairs blue->magenta (B2Z: 2:3,4:5,9:6,10:0) and 4 pairs magenta->yellow (Z2G: 0:1,6:7,3:8,5:11). Class ids per cid() scan order of legend tiles (bands r0=3,11,19,27; tile cols 12,22,35,45).
- Blue banner (given, rows 41-45, cols 8..50): [2,4,10,9,4,2,10] -> compose -> YELLOW TARGET [8,11,1,7,11,8,1].
- Yellow banner (editable, rows 52-56): current [12,13,8,7,1,12,12]; decoy classes 12,13. Cursor slot0.
- Actions 93-100: 8x Up on slot0 to map wheel.

## After Action 100 (L4 spin complete)
- Wheel Up-order: [12,13,14,8,11,7,1] (decoys 12,13,14). Budget 60.
- Current [13,13,8,7,1,12,12] idx[1,1,3,5,6,0,0]; target [8,11,1,7,11,8,1] idx[3,4,6,5,4,3,6].
- Solution exactly 20 actions: UU R UUU R UUU R R DD R UUU R D. Sent as Actions 101-120. Expect L4 clear (score 4).

## LEVEL 5 (Action 120 cleared L4; score 4; budget 64)
- Board at log line 18823. NEW MECHANIC: banners are GIVEN (blue rows 44-48 cols 15..43: [5,7,8,8,0]; magenta rows 53-57: [4,9,9,1,6]); cursor brackets LEGEND pair0 blue tile (rows 7-19, cols 9-13). We edit the LEGEND.
- Legend pairs (structure fixed): p0 (10,8)L1->(10,18)R1: [0]->[1]; p1 (10,31)L1->(10,41)R2: [0]->[2,2]; p2 (22,8)L2->(22,25)R1: [3,3]->[4]; p3 (22,38)L1->(22,48)R1: [5]->[6].
- Goal: edit legend cells so blue banner translates to magenta banner. Token length constraint: #p1=#p2, order perm of 4 pairs.
- Best candidates: (p2,p1,p0,p3): p2[5,7]->[4], p1[8]->[9,9], p0[8]->[1], p3[0]->[6] (7 edits, but p0L=p1L=[8] ambiguous lefts); injective-left options cost 8 edits, e.g. (p3,p2,p0,p1): p3[5]->[4], p2[7,8]->[9], p0[8]->[9], p1[0]->[1,6].
- Class ids from cid() scan: legend cells then banners (blue 5,7,8 & mag 9 are non-legend classes).
- Actions 121-124: R,R,R,R to map cursor path over legend cells.

## After Action 124
- Cursor visits TILES in order: p0L, p0R, p1L, p1R(whole 2-glyph), p2L(whole 2-glyph), ... presumably p2R, p3L, p3R. Cursor now at p2L [3,3]. Budget 62.
- Actions 125-132: 8x Up on p2L to learn multi-glyph tile cycling (single wheel? combo wheel?).

## After Action 132 (p2L spin)
- Double tiles cycle both glyphs together: only [x,x] states. Blue L-tile wheel Up-order: [3,0,7,10,11,5,8] (pos 3:0,0:1,7:2,10:3,11:4,5:5,8:6). Decoys 10,11.
- Doubles constraint kills [5,7] solutions. Chosen solution (p3,p1,p2,p0): p3:[5]->[4], p1:[7]->[9,9], p2:[8,8]->[1], p0:[0]->[6].
  L edits: p1L 0->7 (1 up), p2L [0,0]->[8,8] (2 downs; currently [0,0] after spin). p0L/p3L unchanged.
  R edits: p0R 1->6, p1R [2,2]->[9,9], p2R 4->1, p3R 6->4. Magenta wheel unknown.
- Cursor at p2L; tile order p0L,p0R,p1L,p1R,p2L,p2R,p3L,p3R. Budget 58.
- Actions 133-140: R (to p2R), 7x Up (map magenta wheel).

## After Action 140 (magenta wheel mapped)
- Magenta R-tile wheel Up-order: [4,6,1,10,2,9,11]. Blue L-tile wheel: [3,0,7,10,11,5,8]. Budget 54.
- Final legend target: p0 [0]->[6], p1 [7]->[9,9], p2 [8,8]->[1], p3 [5]->[4]; verifies blue[5,7,8,8,0] -> mag[4,9,9,1,6].
- Route from p2R (17 actions, sent 141-157): UU(p2R->1) RR D(p3R->4) LLL DD(p2L->[8,8]) L U(p1R->[9,9]) L U(p1L->7) LL D(p0R->6). Expect L5 clear (score 5).

## After Action 157 (L5 not yet cleared — off-by-one)
- 17-action finisher had cursor error: from p1L, LL went to p0L (only 1 L needed for p0R).
- Final D edited p0L: old-0 -> old-3 (blue wheel down). p0R still old-1 (unedited).
- All other tiles correct: p3=[5]->[4], p1=[7]->[9,9], p2=[8,8]->[1] verified in final board.
- Cursor now on p0L. Fix sent (158-160): U (p0L 3->0), R (to p0R), D (p0R 1->6). Expect score 5.

## Level 6 (started Action 161; L5 cleared at Action 160, score 5)
Board at log line 23708. Layout:
- Legend 3 rows (r5,r17,r29): blue tile (r,9,1 glyph at r+1,10); mag double (r,19; glyphs r+1,20 and r+1,27); mag single (r,38; glyph r+1,39); yellow (r,48; glyph r+1,49). hhh connectors blue->magdouble and magsingle->yellow.
- A-pairs (blue->2mag): 0->[1,2]; 5->[6,7]; 9->[7,7]
- B-pairs (mag->yel): 3->4; 6->8; 10->11
- Blue banner FIXED rows44-50, glyphs (45,22),(45,29),(45,36): [5,12,13]
- Yellow banner rows53-59, glyphs (54,12+7k) k=0..5: [14,15,8,8,15,14]
- Cursor starts on R1 blue tile (box rows2-14, cols10-14).
Mechanic hypothesis: edit legend so composition maps blue banner -> yellow banner:
  5->[14,15], 12->[8,8], 13->[15,14] (via B on each magenta).
Note R2 double [6,7] unequal => no lockstep here (unlike L5), or doubles fixed.
Candidate solution (9 edits): R2: blue keep 5, double->[6,10]; R1: blue->13, double->[10,6]; R3: blue->12, keep [7,7]; B: (6->8)=>(6->14), (3->4)=>(7->8), (10->11)=>(10->15).
Class ids (this scan): legend order rows then blue banner then yellow banner; 16 classes.
Sent 161-170: 7xUp (spin blue R1, map wheel, return to start) + 3xRight (learn cursor path).

## After Action 170 (L6 probes)
- Blue wheel Up-order: [0,16,13,5,12,9,17] (7 states; contains 5,12,13; decoys 16,17). Spin returned to 0.
- Cursor traversal (Rights): blue tile -> mag DOUBLE as whole unit (box cols 20-31) -> mag single (39-43) -> yellow (49-53). Now on R1 yellow.
- Doubles selected whole => likely lockstep advance preserving offset on magenta wheel. R3 [7,7] offset 0 handles 12->[mz,mz]. R1/R2 offsets must accommodate [mx,my] and [my,mx] (need gap g and -g).
- Sent 171-186: 7xUp (yellow R1 wheel, return), LL, 7xUp (mag double R1 wheel + lockstep check, return).

## After Action 186 (L6 wheels mapped, solution computed)
- Yellow wheel Up: [4,15,16,11,8,17,14]. Magenta wheel Up: [1,6,3,7,18,2,10].
- Doubles: lockstep on magenta wheel, offset preserved. Offsets: R1=5, R2=2, R3=0.
- SOLUTION: A: R1 13->[7,6], R2 5->[6,7] (unchanged), R3 12->[10,10]; B: R1 7->15, R2 6->14, R3 10->8.
  Composition check: 5->[6,7]->[14,15]; 12->[10,10]->[8,8]; 13->[7,6]->[15,14] = yellow banner OK.
- Edits (tile idx 0..11 linear, cursor at t1=R1dbl): t0 blue 0->13 2U; t1 dbl 3U; t2 magS 3->7 1U; t3 yel 4->15 1U; t7 yel 8->14 2U; t8 blue 9->12 1D; t9 dbl [7,7]->[10,10] 3U; t11 yel 11->8 1U.
- Route (26 total): L 2U R 3U R 1U R 1U RRRR 2U R 1D R 3U RR 1U.
- Sent 187-206 (batch 1 of 20): L UU R UUU R U R U RRRR UU R D R U... ends with R onto t9 (no Ups there yet).
- REMAINING batch 2 (6): UUU (t9 dbl [7,7]->[10,10]) RR (to t11) U (11->8). Expect L6 clear.
- RISK: assumed Right wraps from R1yel(t3) to R2blue(t4); verify at steps 12-15.

## After Action 206 (batch 1 verified)
- All batch-1 edits correct: R1 [13,[7,6],7,15]; R2 [5,[6,7],6,14]; R3 [12,[7,7],10,11]. Cursor on R3 dbl. Row-wrap R confirmed.
- Sent 207-212 (batch 2): UUU ([7,7]->[10,10]) RR U (yel 11->8). Expect L6 clear (score 6).
