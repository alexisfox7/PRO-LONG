# Game notes

## LEVEL 1 SOLVED at action 8 (score 0->1). Total 8 actions used.
Solution recipe: rotate ring so single G block reaches bracketed top[0] slot.
Red arrow (4,32)=CCW, green arrow (58,32)=CW. Choose shorter direction.
Cost: 5 timer cells per press, ~12 press budget (col x=0, 64 green cells).
Post-win board still showed solved L1 ring; sent no-op bg click (32,8) to reveal L2.

# LEVEL 6 SOLVED at action 92 (score 5->6). 21 actions for L6 (72-92). Swap model of A6 confirmed.
Sent no-op (32,8) as action 93 to reveal L7.

# Level 6 (from action 72, timer 64)
THREE wheels, each = 3 concentric octagon rings (8 cells: N,NE,E,SE,S,SW,W,NW; 2x2 blocks):
Left wheel center (15,14ctr): r1 N(12,14) NE(12,17) E(15,16) SE(18,17) S(18,14) SW(18,11) W(15,10) NW(12,11)
  r2: N(9,14) NE(9,19) E(15,19) SE(21,19) S(21,14) SW(21,7) W(15,7) NW(9,7)
  r3: N(6,14) NE(6,23) E(15,22) SE(24,23) S(24,14) SW(24,4) W(15,4) NW(6,4)
Right wheel center (15,44): same offsets (x+30).
Bottom wheel center (45,29): r1 N(42,29) NE(42,32) E(45,32) SE(48,32) S(48,29) SW(48,26) W(45,26) NW(42,26)
  r2: N(39,29) NE(39,35) E(45,35) SE(51,35) S(51,29) SW(51,23) W(45,23) NW(39,23)
  r3: N(36,29) NE(36,38) E(45,38) SE(54,38) S(54,29) SW(54,20) W(45,20) NW(36,20)
G blocks: left r1 SW (18,11); right r1 NE (12,47); bottom r1 W (45,26).
Brackets (bracket around cell): (27,26), (27,32), (33,29) — between-wheel cells with blocks # ( ".
7 GREEN arrows (no red): A1(27,15) A2(57,15) A3(15,28) A4(45,28) A5(42,45) A6(53,55) A7(30,58).
Probe results (73-79):
- A1 (27,15) / A2 (57,15) / A5 (42,45): RADIAL hop of left/right/bottom wheel: ring contents
  move r1->r2->r3->r1, angular index preserved.
- A3 (15,28) / A4 (45,28) / A7 (30,58): angular CCW of all 3 rings (block idx i -> i-1;
  idx order [N,NE,E,SE,S,SW,W,NW] = 0..7 clockwise).
- A6 (53,55): swaps bracket cells with adjacent r3 cells: P1<->L3[3](SE), P2<->R3[5](SW), P3<->B3[0](N).
  (Alt hypothesis: 4-cycle L3SE->P1->P2->R3SW + swap P3<->B3N — watch result!)
G after probes: left (r2,idx4), right (r2,idx0), bottom (r2,idx5).
Queued 13 presses (80-92): A1,A3 | A2,A4x3 | A5,A7x5 | A6 -> G's at L3SE,R3SW,B3N then swap into brackets.

# LEVEL 5 SOLVED at action 71 (score 4->5). 11 actions for L5 (61-71).
BFS over op-space worked perfectly; use that approach for any multi-op level.
Sent no-op (32,8) as action 72 to reveal L6.

# Level 5 (from action 61, timer 64)
Top row y6: 5 blocks x17,23,29,35,41 (4x4, step 6) = [(,f,#,",8]; arrows red (10,7) left / green (52,7).
BRACKETS (yellow corners) around top positions 1 (x17) and 5 (x41).
Serpentine 17-cycle S0..S16 (path order, 4x4 blocks):
S0=(6,17) SHARED with top row pos1; S1=(12,17); S2=(18,17)=G1; S3=(18,23); S4=(18,29);
S5=(24,29); S6=(30,29); S7=(30,23); S8=(30,17); S9=(36,17); S10=(42,17); S11=(42,23);
S12=(42,29); S13=(48,29); S14=(54,29)=G2; S15=(54,23); S16=(54,17); wraps S16->S0.
Serpentine arrows: red (12,37), green (37,37). Directions UNKNOWN.
Plan (if serpentine backward available cheap): back x2 (G1->S0), top-left x1 (G1->x41 bracket),
 forward x5 (G2->S0 bracket) = 8 presses. If green=forward only variant: forward 3, top-left 1, back 5 = 9.
Probe results (62-63): top row + serpentine = ONE 21-cycle (C0..C20; C0=T4,..,C4=T0=S0, C5=S1..C20=S16).
Serp green (37,37) = all blocks C-1 (BG); serp red (12,37) = C+1 (BR, assumed).
Top red (10,7) = top-row-only: blocks left, T0 wraps to T4 (TR: C0..3 ->+1, C4->0).
Top green (52,7) = TG assumed reverse (C1..4 -> -1, C0->4).
State after 63: G1 at C5 (S1), G2 at C17 (S13). Brackets = T0 (C4) & T4 (C0).
BFS 8-press solution queued (actions 64-71): BG,TG,BR,TR,BR,BR,BR,BR -> G1 C4, G2 C0. WIN expected.

# LEVEL 4 SOLVED at action 60 (score 3->4). 16 actions for L4 (45-60).
Sent no-op (32,8) as action 61 to reveal L5.

# Level 4 (from action 45, timer 64, cost likely 1/press)
Topology: 2 rows x 2 cols, each a 10-cycle crossing at 4 intersections.
Row T y15, Row B y45: cells x=9,12,15,18,21,39,42,45,48,51 (idx 0-9)
Col L x15, Col R x45: cells y=9,12,15,18,21,39,42,45,48,51 (idx 0-9)
Intersections: T2=L2 (15,15); T7=R2 (45,15); B2=L7 (15,45); B7=R7 (45,45)
Values: T=[8,#,8,",(,G,f,8,#,"]  B=[8,f,#,(,8,f,f,",(,8]
        L=[(,f,8,#,",#,",#,-,(]  R=[f,#,8,8,(,",#,",(,#]
G at T5; orange at L8. Targets: yellow bracket=B7 (45,45); orange bracket=B9 (51,45).
Arrows (click coords x,y): Row T: red-left (6,15), green-right (25,15) [dup pair (36,15)red,(55,15)green]
 Row B: red-left (6,45), green-right (25,45) [dups (36,45),(55,45)]
 Col L: green-up (15,6), red-down (15,25) [dups (15,36) green,(15,55) red]
 Col R: green-up (45,6), red-down (45,25) [dups (45,36),(45,55)]
Assumed semantics: green shifts toward arrow direction (up/right), red down/left. UNVERIFIED.
Plan (11 presses): colL up x1 (orange->B2); rowB left x3 (orange->B9 tgt);
 rowT right x2 (G->T7=R2); colR down x5 (G->R7=B7 tgt).
Probe results (46-47): vertical arrow shifts BOTH columns; horizontal shifts BOTH rows!
Green-up (15,6)=cols up; red-left (6,45)=rows left. Presumed: (25,15)=rows right, (15,25)=cols down.
State after 47: G at T4, orange at B1.
Queued 13 presses (simulated OK): rows-right x3 (G->T7), cols-down x1 (park G R3),
rows-right x5 (orange->B9 tgt), cols-down x4 (G->R7=B7 tgt). Win expected ~action 60.

# LEVEL 3 SOLVED at action 44 (score 2->3). 19 actions for L3 (26-44).
16-press plan executed flawlessly. Sent no-op (32,8) as action 45 to reveal L4.

# Level 3 (from action 26): two interlocked 16-cell rings (chain links)
Cell coords (y,x = top-left of 2x2 block):
Left ring CW: L0(19,21) L1(19,24) L2(19,27) L3(22,30)* L4(25,33) L5(28,33) L6(31,33)
  L7(34,30)* L8(37,27) L9(37,24) L10(37,21) L11(34,18) L12(31,15) L13(28,15)=YELLOW TARGET
  L14(25,15) L15(22,18)
Right ring CW: R0(19,33) R1(19,36) R2(19,39) R3(22,42) R4(25,45) R5(28,45)=ORANGE TARGET
  R6(31,45) R7(34,42) R8(37,39) R9(37,36) R10(37,33) R11(34,30)* R12(31,27) R13(28,27)
  R14(25,27) R15(22,30)*
Shared cells: (22,30)=L3=R15 and (34,30)=L7=R11.
Blocks: G(yellow) at R3 (22,42); orange '-' at L11 (34,18).
Brackets: yellow corners around (28,15)=L13; orange corners around (28,45)=R5.
Arrows y40-43: left ring red(22-23,41) green(24-25,41); right ring red(35-36,41) green(37-38,41).

Draft 18-press plan (pending direction/cost probe), plan A:
1. Right +2 toward R5 (G R3->R5)   2. Left CCW x4 (orange L11->L7=R11)
3. Right CCW x6 (orange R11->R5 TARGET; G R5->R15=L3)   4. Left CCW x6 (G L3->L13 TARGET)
CCW = decreasing index. Verify green direction via probe; mirror plan if needed.
Probe results (27-28): topology CONFIRMED. Left green (24,41) = CCW (index-1);
right green (37,41) = CW (index+1); right red (35,41) = CCW. Timer 1/press, 62 left.
After probes: G at R4, orange at L10.
Queued 16-press solution (simulated OK): R-green x1, L-green x3, R-red x6, L-green x6
 -> G to L13 (yellow bracket), orange to R5 (orange bracket). WIN expected at action ~44.

# LEVEL 2 SOLVED at action 25 (score 1->2). 17 actions for L2 (9-25).
Plan executed perfectly; simulation approach works. Post-win board still shows solved L2;
sent no-op click (32,8) as action 26 to reveal L3.
General recipe: probe each arrow once, diff to derive ring topology, then simulate full solution.

# Level 2 CONFIRMED MECHANICS (actions 10-11 probes)
- Row1 green (38,17): rotates OUTER 26-cell ring CW: row1 L->R, x35 strip down
  (incl. row2/row3 x35 cells), row4 R->L, x23 strip up (incl. row3/row2 x23 cells).
- Row2 green (47,26): shifts ONLY row2 right (10-cycle wrap). Red (14,26) presumed left.
- Timer cost: 1 cell/press this level (62 left after action 11).
- State after action 11: G1 at row1 x35 (outer idx4), G2 at row3 x23 (outer idx20).
- Solution queued (actions 12-25, 14 presses, simulated & verified):
  outer CW x3 -> G1 to row2x35, G2 to row2x23
  row2 green x4 -> G2 to row2x35, G1 to row2x17
  outer CW x3 -> G2 to row3x35 (bracket2), G1 untouched
  row2 red x4 -> G1 to row2x35 (bracket1). WIN expected.

# Level 2 notes (started action 9, timer refilled to 64)
Row-1 of 8 progress segments (row y1) turned green after L1 clear.
Layout (block coords = top-left of 2x2, step 3):
- row1 y17: x23..x35 (5 blocks): (, f, ", G, "   arrows: red x20-21, green x38-39 (click y17)
- strip x23 & x35 at y20,y23 (between row1-row2): x23: ",#  x35: f,(
- row2 y26: x17..x44 (10): 8,f,f,8,(,",#,(,#,#   arrows: red x14-15, green x47-48 (click y26)
- strips y29,y32: x23: 8,8  x35: 8,#
- row3 y35: x17..x44 (10): 8,(,f,8,f,(,",f,#,(   arrows red/green same x (click y35)
- strips y38,y41: x23: G,#  x35: 8,f
- row4 y44: x23..x35 (5): (,(,",",#   NO arrows
- Brackets (G corners x34&x37): around x35-36 block of row2 (y25/28) and row3 (y34/37)
- G blocks: row1 x32 AND strip x23 y38
Goal guess: put G blocks into the two brackets (row2 x35, row3 x35).

Probe (actions 10-11): green arrow row1 (38,17), then green arrow row2 (47,26). Diff to learn ring paths.

# Level 1 notes

## Confirmed mechanics (after actions 1-2)
- 20-block ring conveyor: top row 7 blocks (y19-22, x=12..51 step6), right col 3 (x48-51, y25/31/37),
  bottom row 7 (y43-46, reversed), left col 3 (x12-15, y37/31/25).
- GREEN arrow (click 58,32): rotates ring CLOCKWISE by 1 (top row moves right). Verified by full diff.
- Clicking a block (19,20): NO effect, NO timer cost.
- Timer: column x=0 starts all 'I' (64 green cells); each rotation turns 5 cells 'O' from top.
  => budget ~12 rotations total. After 1 press: 59 left (~11 presses).
- Row y1: 8 black OOOO segments — unchanged so far, meaning unknown (maybe level count).
- Ring has exactly ONE yellow (G) block; yellow corner brackets fixed around top[0] cell (x12-15,y19-22).
  Goal hypothesis: rotate ring until G sits in bracketed top[0] slot.

## State after action 2
top: [(, 8, #, (, f, ", G]  bot: [8, f, f, (, ", #, (]  (bot listed left-to-right)
G at top[6]. Need 6 CCW (red) or 14 CW (green).

## Action 3 result
RED arrow (4,32) = CCW rotation confirmed (top row shifts left). Board back to initial config.
G at top[5]. Timer 54/64 (~10 presses left).

## Actions 4-8 (queued)
5x red press -> G should land in bracket at top[0]. Expect score -> 1 / level clear.

## Ring order clockwise from top[0]:
top[0..6], colR y25,y31,y37, bot[6..0], colL y37,y31,y25 (20 cells)

## Level 7 (revealed action 93)
- Top row y23-24, 8 slots x=20,23,26,29,32,35,38,41 (slot 0-7). Yellow bracket at slot 7 (x41-42, corners x40/x43 rows 22/25).
- Column x20-21: cells y23 (SHARED with slot 0), y26 (#), y29 ("). Green up-arrow click (20,20), red down-arrow click (20,33). 3-cycle presumed, unprobed.
- Mini-ring 2x2: cells (35,29) (35,32) (38,29) (38,32) [row,col of top-left]. Yellow bracket at (35,32) (corners rows 34/37, x31/x34).
- Red arrow click (29,42): top row shift LEFT (slot i <- i+1) + mini CCW (BR->TR->TL->BL). Confirmed action 94.
- Green arrow click (33,42): presumed inverse (shift right + mini CW). Probing.
- After action 94: mini G IN bracket (TR); top G at slot 6 (x38).
- Parity: red/green alone unsolvable (need shift ≡7 mod 8 with rotation ≡0 mod 4 → contradiction). Must park G in column.
- Draft solution (if assumptions hold): Gr,Gr (G slot6->0, mini CW2), park via column, R (mini CCW1... net), unpark (column x2), R -> G slot0->7, mini net 0. ~7 presses.
- Action 95 confirmed green (33,42) = shift right + mini CW (TL->TR->BR->BL). Action 96: column up (20,20) swaps/cycles slot0 with y26 (3-cycle vs 2-swap ambiguous; y29 had same value).
- Column press did NOT decrement timer (no timer diff) — column moves may be free.
- Actions 97-100 queued: green,up,red,up. Then finisher: if G at slot0 -> red once; if G at y26 -> up, red. Both end with G slot7 + mini G TR = solved.
- Actions 97-100 executed; column confirmed 3-CYCLE up (y23<-y26<-y29<-y23). G at y26, col=(",G,#), mini G at BR.
- Finisher queued (101-102): up (20,20) -> G slot0; red (29,42) -> G slot7 + mini CCW G->TR. Expect score 7.
- LEVEL 7 SOLVED at action 102 (score 7). Total 9 presses on L7 (94-102). Parking through the x20 column broke the mod-8/mod-4 parity conflict.
- Action 103 queued: no-op (32,8) to reveal Level 8 (final).

## Level 8 (revealed action 103) — FINAL
- 3 G blocks at x18-19: y9, y18, y27. 3 yellow brackets bottom row y51-52 at x24, x30, x36 (corners rows 50/53).
- Lattice: diagonal lanes upper-left (e.g. (12,3)->(15,6)->(18,9)->(21,12)->(24,15)->(27,18) step +3/+3), vertical columns x24/x30/x36/x42 spaced 3 rows down to y51.
- Arrow pairs (red x49-51, green x53-55): A rows 23-26 click (50,24)/(54,24); B rows 28-31 (50,29)/(54,29); C rows 33-36 (50,34)/(54,34). Bottom pair D rows 56-59: red (32,57), green (36,57).
- Probes queued (104-107): green A, green B, green C, green D.
- L8 model: 3 disjoint cycles, each = top diagonal sub-lane + connector diagonal + vertical column + bracket at bottom, wrapping bracket->head.
  C1 (len15, bracket idx14): (9,18),(12,21),(15,24),(18,27),(21,30),(24,33),(27,36),(30,36),(33,36),(36,36),(39,36),(42,36),(45,36),(48,36),(51,36). Sub-lane A = idx0-1.
  C2 (len16): (6,6),(9,9),(12,12),(15,15),(18,18),(21,21),(24,24),(27,27),(30,30),(33,30),(36,30),(39,30),(42,30),(45,30),(48,30),(51,30). Sub B = idx0-5.
  C3 (len14): (12,3),(15,6),(18,9),(21,12),(24,15),(27,18),(30,21),(33,24),(36,24),(39,24),(42,24),(45,24),(48,24),(51,24). Sub C = idx0-6.
  greenD (36,57) advances all cycles +1; sub greens advance +1 within sub region (wrap to idx0). Decoy cells (x42 col, upper x36 col, etc.) never move.
- After probes: Gs at idx (2,6,7); goal (14,15,13). BFS 5-press solution queued (108-112): redD(32,57), gA(54,24), gB(54,29), gC(54,34), redD(32,57). Expect score 8 = GAME COMPLETE.
