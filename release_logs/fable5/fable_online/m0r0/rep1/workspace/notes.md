# Game notes

## LEVEL 3 CLEARED at action 155 (Score 3). Used 114 actions on L3 (41->155) due to mechanic discovery.

## Level 4 (from action 155 board)
- Left bg yellow G, right bg purple ". 5x5 players: LEFT (rows34-38,cols14-18), RIGHT (rows24-28,cols45-49). NOT height-symmetric (left 10px lower).
- Two rooms: left cols9-23 rows14-48; right cols40-54 rows14-48 (mirror). Center corridor rows29-33 cols24-39 connects. Blue 'f' 3x3 at rows30-32 cols31-33 (dead center).
- CHECKER red bands (semantics unknown): rows9-13 and rows49-53 in both rooms (cols9-24/39-53); rows24-28 and rows34-38 at cols24-39 (flanking corridor).
- LATTICE MISMATCH: left cols ≡4 mod5, right cols ≡0 mod5 -> exact overlap IMPOSSIBLE. Win likely = both players covering center blue simultaneously (left at cols29-33 + right at cols30-34, rows29-33).
- Rows lattice shared (≡4 mod5). Need +10px relative vertical shift; only possible blocker = checker (or top wall through checker if checker passable).
- PLAN: U,U,U probe. U3 discriminates: (a) checker=safe wall: right blocked at rows14-18; (b) checker=safe floor: right enters rows9-13; (c) deadly: reset. Then:
  (a) U once more (both rows14-18), D,D,D (both rows29-33), R,R,R -> cover blue. 
  (b) U,U more (right blocked by top wall at 9), then D x4, R x3.
- Actions 156-158: sent UUU.

## LEVEL 1 CLEARED at Action 18 (Score 0->1). Goal = merge the two mirrored players. 18 actions used.

## Level 2 (from Action 18 board)
- Left bg magenta C, right bg purple ". Black=corridor. Players '(' 4x4: left rows10-13 cols22-25, right rows10-13 cols38-41.
- NEW: red 'n' checkered tiles = hazards (semantics unknown; avoided entirely).
- Tile grid: origin (6,6), size 4, 13x13. Map ('.'=open,'#'=wall,'n'=hazard,P=player start):
```
 0 ......#......
 1 ....P.#.P....
 2 ......#......
 3 ..#########..
 4 ..#.#######..
 5 .....n#......
 6 .....n#......
 7 .....n#......
 8 nnn.nn#.nnnnn
 9 ......#......
10 .............
11 .............
12 nnnnnnnnnnnnn
```
- Players start tiles: L(1,4), R(1,8). Center divider j=6 open only at rows i=10,11 (and i=12 hazard).
- SAFE merge path (never attempts hazard entry): DLLLDDDRRURRDDDDDDRRRUL (23 moves), merge at (10,5).
- Risky path (leans on hazards as walls) was 20 moves - skipped.
- Actions 19-25: sent prefix DLLLDDD. Predicted after: L(5,1), R(5,11).
- Actions 19-25 verified: players at L(5,1), R(5,11) exactly as predicted. Model solid.
- Actions 26-41: sent RRURRDDDDDDRRRUL (16 moves) -> merge at (10,5). Expect Score 2 at action 41.

## Level 1 layout (Action 0)
- 64x64, 5x5 tiles. Left half yellow (G) bg, right half orange (-) bg. Black (O) blobs = likely corridors/maze.
- Two 5x5 light-blue '(' blocks: LEFT rows 49-53 cols 19-23; RIGHT rows 49-53 cols 39-43. Hypothesis: two players.
- Halves are near mirror images (mirror c -> 63-c) but differ in 13 regions (shapes offset ~1 tile).
- Hypothesis: dual-maze, one input moves both players (right maybe mirrored horizontally).

## LEVEL 2 CLEARED at Action 41 (Score 1->2). Total 41 actions.

## Level 3 (from Action 41 board)
- Left bg purple '"', right bg SOLID red 'n' (solid red = wall, distinct from level-2 checkered hazard).
- Tile grid: origin (10,2), size 4, 11 rows x 15 cols. Players L(9,5) R(9,9). Blue 'F' 2x2 markers at (2,2) left, (5,9) right, (1,7) center crossing.
- Map:
```
 0 ###.####.....##
 1 ##...#.F.###.##
 2 ##F#.#.###.#.##
 3 ##.#.#.#.....##
 4 ##.#...#.######
 5 ##.#####.F...##
 6 #......####..##
 7 ######.#..#.###
 8 ###....#.....##
 9 ###..P.#.P...##
10 ###....#.....##
```
- IMPORTANT DISCOVERY (actions 42-61 replay): blue 'F' tiles are SOLID WALLS, not passable. Every move matched sim once F=wall. Blues unchanged after bumps (bumping does nothing).
- Only crossing between halves is (1,7) = blue-blocked => blues must be removable. ACTION5 never tested.
- After action 61: L(3,2) [directly below left blue (2,2)], R(5,12). Blues at (1,7),(2,2),(5,9).
- Blue adjacency: left blue (2,2) reachable from (1,2) above / (3,2) below only. Right blue (5,9) from (5,8) left / (5,10) right only. Center (1,7) from (1,6)/(1,8).
- Action 62: ACTION5 adjacent-below left blue -> ZERO board change. Interact alone does nothing (or wrong condition).
- Bumping blues also does nothing (actions 60-61 no change).
- Actions 63-65: MY ERROR - sent L,L,A5 but ACTION3(L) moves right player +1 col (mirror!). Both players blocked; zero change. 3 actions wasted.
- REMEMBER: ACTION4(R): left +1 col, right -1 col. ACTION3(L): left -1 col, right +1 col.
- Actions 66-68: sent R,R,A5. After RR: left pinned (3,2) ((3,3)=#), right (5,12)->(5,11)->(5,10) adjacent right blue. Watch for auto-trigger after 2nd R or A5 effect.
- Actions 66-68: RR worked (right now (5,10), both players adjacent to their blues) but NO auto-trigger, A5 still nothing.
- Ruled out: bump removal, A5 interact (alone/adjacent/both-adjacent), simultaneous adjacency.
- Note: both players have each bumped their blue at least once historically - no cumulative effect either.
- Action 69: sent ACTION6(39,31) = click on right blue 2x2 (pixels cols39-40 rows31-32), player adjacent. Watch for removal/teleport/other.
- Blue pixel locations: left blue rows19-20 cols11-12; right blue rows31-32 cols39-40; center blue rows15-16 cols31-32.
- Action 69 RESULT: click on right blue changed BOTH players '(' -> '8' (off-white). Positions unchanged, blues unchanged. Some mode toggle!
- CORRECTION: action 69 click REMOVED right blue (5,9) AND turned players '8' (36 diff = 32 player + 4 blue cells).
- Action 70: ACTION4 in '8' state -> diff 0. Movement FROZEN in '8' state (right should have moved into now-open (5,9)).
- Current: players '8' at (3,2),(5,10); blues left: (1,7),(2,2).
- Action 71 RESULT: clicking left blue -> left blue f->G (YELLOW=activated), right blue G->f (deactivated!). Only ONE blue active at a time. Plus NEW white '$' pixels on border: (row0,col51) and (row63,col12). Players still '8'.
- REINTERPRET action 69: click turned right blue YELLOW (not removed) + players '('->'8'.
- REINTERPRET action 70 (R, diff 0): left blocked by #, right blocked by yellow-blue (if yellow still solid) -> maybe NOT frozen!
- Action 72: ACTION2 diff 0 despite open tile below left player => TRULY FROZEN in '8' state.
- White border pixels are mirror twins: (0,51),(63,12), 51=63-12. Appeared when left blue activated. Col 12 ~ left blue cols 11-12. Exit markers?
- Action 73: A5 in '8' state -> 2 new whites (0,50),(63,13). Whites now: top cols 50-51 (growing left), bottom cols 12-13 (growing right). Mirror pairs (50=63-13). Converging toward center cols 31-32? Counter/progress/timer - unknown.
- Timeline: a69 click right blue: players 8+right yellow, NO whites. a71 click left blue: left yellow, right reverts, whites pair1. a73 A5: whites pair2.
- Action 74: center blue -> YELLOW, left blue reverts to 'f'. NO new whites. Players still '8' frozen at (3,2),(5,10).
- Whites state: top (0,50),(0,51); bottom (63,12),(63,13).
- Action 75: A5 -> whites +1 pair: top 49-51, bottom 12-14. A5 grows lines regardless of which switch active. Lines converge at cols 31/32 (center) in ~17 more A5.
- Tick log: a71 click-left(+1 init at col12/51), a73 A5(+1), a74 click-center(0), a75 A5(+1).
- Theory: line = signal from left blue toward center; when meets, unlock? OR fuse. Arrows tick nothing.
- Action 76: re-click active center blue -> diff 0. No deactivation.
- Action 77 RESULT: click on player -> players '8'->'(' UNFROZEN + active switch deactivated. Whites persist.
- MODEL: click blue = enter switch mode (frozen, switch yellow). A5 (only in mode) grows white border lines +1px pair. Click player = exit mode. Lines persist across mode exit.
- Lines: top cols 49-51 growing left, bottom 12-14 growing right; predict meet/complete when bottom=31, top=32 => 17 more A5.
- Actions 78-95: A5 pump did NOTHING. White lines = LEVEL TIMER, ticking every ~2-3 actions since action 41 (start bot col0/top col63, +1 inward per tick). A5 theory was coincidence. Timer converges at cols 31/32 (center): bottom at 22 now, ~9 ticks (~21 actions) left. Timeout likely = reset.
- Timer ticks so far every 2-2-3 pattern of actions (~2.4 avg). ALL actions tick it (or wall clock).
- NEW HYPOTHESIS: in switch mode, ARROWS MOVE THE ACTIVE BLUE. Earlier tests coincidentally blocked: a70 R moved right-blue into player; a72 D moved left-blue into player. 
- Geometry: center blue at (1,7) pushable L->(1,6) or R->(1,8), then U from (1,8)->(0,8), then along row0 (0,9)-(0,12).
- WARNING: every center-blue parking spot reachable from (1,7) blocks either left route ((1,6)) or right route ((1,8),(0,8)-(0,12),(1,12),(2,12),(3,12)). Right upper region entries: (5,8) [behind right blue!] and col12 row0-3.
- Right blue (5,9) also blocks right player's access to upper region: push right into (5,10)-(5,12) area (player must dodge) to clear (5,8), but parking may block col12 route. NEEDS FULL PLANNER with blue positions in state.
- Likely: after mechanic test, RESET to restart timer, then execute planned full solution.
- Action 96-97: CONFIRMED blues movable! click center + R -> center (1,7)->(1,8). Mapping R=+1col (same as left player, not mirrored) for center blue at least.
- KEY INSIGHT: left blue (2,2) traps LEFT player in lower-left (blocks only route up). All 3 blues must be parked in dead-end nooks: bL->(0,3), bC->(2,10), bR->(10,11).
- FULL PLAN (58 actions): RESET; click bL(11,19), U,R,U; click bC(31,15), R,U,R,R,R,R,D,D,D,L,L,U; click bR(39,31), R,R,D,D,D,D,D; click player(23,47); then phase B 31 moves ULLUUURRRUULLLLUUUUURRRRDRRDDDR (merge at (4,5), right player crosses door).
- Phase B computed with parked blues; path identical to original naive path (blues vacate exactly the needed tiles).
- RISK: right-blue horizontal mapping unknown (assumed uniform R=+1col). Batch 1 ends after first bR push R: expect bR (5,10); if (5,8) it's mirrored -> replan (push L,L to (5,10)... actually then L=+1col).
- Actions 98-117 (batch 1/3): RESET + bL park + bC park + click bR + R.
- Actions 98-117 (batch 1) PERFECT: bL(0,3) f, bC(2,10) f, bR ACTIVE G at (5,10) => UNIFORM mapping for right blue confirmed. Players '8' at (9,5),(9,9). Timer bot 0-7 (8/31 used, plenty).
- Actions 118-137 (batch 2 sent): R,D,D,D,D,D (bR->(10,11)), click player (23,47), then phase B 1-13: ULLUUURRRUULL. Expected after: bR parked (10,11), players '(' at positions from partial path.
- Actions 118-137 (batch 2) PERFECT: blues parked/inactive, players '(' at (6,4),(3,10) exactly as sim.
- Actions 138-155 (batch 3 sent): LLUUUUURRRRDRRDDDR -> merge at (4,5). Expect Score 3 at action 155.
- After reset players: L(9,5) rows46-49 cols22-25, R(9,9) cols38-41. Timer fresh (expect ~32 ticks x2.4 ~ 76 actions).

## Level 1 tile map (rows start 4, step 5; cols step 5), '.'=bg '#'=black:
```
 r0  LEFT     RIGHT(mirrored)
  4  ......   ......
  9  ....##   ...###
 14  ...###   ..####
 19  ..###.   ..###.
 24  ..##..   ..##..
 29  ...#..   ..#...
 34  ...#..   ..#...
 39  ..###.   ..##..
 44  ..####   ..####
 49  ..##(#   ..##(#
 54  ..####   ...###
 59  ......   ......
```

## Tests
- Action 1: ACTION1 (Up) -> BOTH '(' blocks moved up exactly 1 tile (5px). Players confirmed, vertical = same direction, 1 tile per press.

## Tile model (verified)
- tile(i,j) = board rows 4+5i..8+5i, cols 4+5j..8+5j, i,j in 0..11. Corridor = O or '('. bg G/- = wall.
- Maze (after Up move, players at (8,3) and (8,7)):
```
0 ............
1 ...######...
2 ..###.####..
3 .###...###..
4 .##.....##..
5 ..#......#..
6 ..#......#..
7 .###....##..
8 .##(#.#(##..
9 .####.####..
10 .####.###...
11 ............
```
- Hypothesis: goal = merge both players (dual-maze puzzle). Joint BFS (blocked=stay, same-direction moves) from ((8,3),(8,7)): path URULURUUUURULULLLLL (19 moves) merging at tile (1,3).
- CONFIRMED (Action 3): horizontal is MIRRORED. ACTION4(R): left player +1 col, right player -1 col. ACTION3(L): opposite. Vertical same for both. Blocked player stays, other still moves.
- Dynamics validated on blocked cases: left blocked on R at (7,3); right blocked on U at (8,7).
- After Action 3: players (7,3) and (8,6).
- Action 4-18: committed 15-move merge path LULULUUUUURRRUR (merge predicted at tile (1,5), the top bar). L=A3,U=A1,R=A4,D=A2. Goal hypothesis: merging clears level.

## LEVEL 4 (in progress, attempt 2 after checker-death reset at action 158)
Tile lattice: 5px, origin (4,4): tile (r,c) = pixels rows 5r+4..5r+8, cols 5c+4..5c+8.
Tile map (X=deadly checker, .=open, B=blue, P=players):
```
r0  ############
r1  #XXX###XXX##
r2  #...###...##
r3  #...###...##
r4  #...XXX.P.##   R player (4,8)
r5  #....B....##   corridor r5 c1-c9, blue (5,5)
r6  #.P.XXX...##   L player (6,2)
r7  #...###...##
r8  #...###...##
r9  #XXX###XXX##
```
CONFIRMED: X checker = DEATH + level reset (probe UUU killed R at r1). Earlier "45-49" col reading was WRONG; both attempts start R at cols 44-48. Lattices ALIGN (both cols ==4 mod 5). Exact-overlap merge possible.
Death reset gives fresh timer (start positions restored).
No safe vertical wall in rooms (r1/r9 deadly) -> must use blue as vertical blocker.

PLAN (15 actions from reset state):
1. ACTION6(31,31) click blue (pixels 30-32,30-32)
2. A3 x4: blue (5,5)->(5,1); A2 x2: ->(7,1); A4: ->(7,2)  [route avoids L player at (6,2)]
3. ACTION6(16,36) click left player sprite (rows 34-38, cols 14-18) to exit mode
4. A2,A2: L blocked by blue at (7,2), R descends (4,8)->(6,8)
5. A1: both to r5: L(5,2), R(5,8)
6. A4 x3: L 2->3->4->5, R 8->7->6->5, merge at (5,5)
Batch 1 (159-166) SUCCESS: blue parked at (7,2), active/yellow, players frozen. Batch 2 sent (167-173): ACTION6(16,36) unfreeze, D,D (L blocked by blue, R r4->r6), U (both r5), A4 x3 merge at (5,5).
Blue mapping assumed uniform (as L3 center blue): A3=-1col, A4=+1col, A2=+1row.


## LEVEL 4 CLEARED at action 173 (score 4). Total plan: 15 actions post-reset, executed flawlessly (blue blocker at (7,2), merge at (5,5)).

## LEVEL 5 (started action 173)
Tile lattice: 4px, origin rows 6 cols 2: tile (r,c) = pixel rows 6+4r, cols 2+4c. 13 rows x 15 cols. c7 = center wall column, open only at r0-r3 (shared top zone).
Map (P=player, "I- = colored tiles):
```
r0  ..."...........
r1  ...............
r2  ...............
r3  ...............
r4  ###III####"""##
r5  .......#I.....-
r6  .......##.....#
r7  .......#.......
r8  ##---#####"""##
r9  .......#.......
r10 ...#...#.......
r11 .P."...#.....P.
r12 .......#.......
```
L player (11,1), R (11,13). Left maze walls magenta C, right light-magenta z. No deadly checker seen.
Colored geometry: bars (doors?): I r4 c3-5 (left), - r8 c2-4 (left), " r4 c10-12 & r8 c10-12 (right).
Single tiles (buttons?): " (0,3) top zone, " (11,3) left-bottom, I (5,8) right-middle, - (5,14) right-middle.
HYPOTHESIS: button of color X opens/toggles doors of color X. Chain: L->"(11,3) opens purple r8; R crosses down..wait R crosses r8 upward INTO middle (R starts bottom r11; purple bars at r4 AND r8 both right side). R bottom region rows r9-r12 -> cross r8 " -> middle r5-r7 -> stand -(5,14) opens orange r8 left -> L crosses to left-middle r5-r7 -> R stands I(5,8) opens green r4 left -> L to top zone -> L stands "(0,3) opens purple r4 right -> R to top -> merge at c7 rows r0-r3.
PROBE sent (2 actions): A4,A4 -> L to (11,3) purple tile, R to (11,11). Watch: mirror mapping still holds? purple tile walkable/deadly? doors change?
Timer fresh at 173.

L5 UPDATE (action 175): MIRROR FLIPPED vs L3/L4! ACTION4: L -1 col, R +1 col (outward). ACTION3: L +1, R -1 (inward). Probe A4,A4 pushed both to outer walls: L(11,0), R(11,14). U/D mapping still untested.
Sent A3 x3 (176-178): L c0->c3 (onto purple tile if walkable), R c14->c11. Watch purple doors r4/r8 c10-12.

L5 action 178: L on purple plate (11,3) -> BOTH purple bars r4/r8 c10-12 VANISHED. Buttons confirmed. R at (11,11).
Unknown: plate (open only while occupied) vs toggle (permanent). Purple has 2 plates: (11,3) bottom-left, (0,3) top zone -> suggests plate semantics.
Sent (179-183): A1 x4 (L blocked by wall (10,3), R climbs (11,11)->(7,11) through r8 door), then A4 x1 (L off plate ->(11,2), R ->(7,12)). Diff purple bars after: reappear=plate, stay open=toggle.
NOTE vertical mapping unverified; if A1=down, recoverable (~4 wasted).
Mapping L5: A3: L+1col R-1col; A4: L-1col R+1col.
Plate-semantics deadlock risk: L rightward approach (A3) pulls R left off plates; solution = pre-stage L below door columns, have R approach plates with A1/A4 only while L blocked. Full joint BFS planned once semantics known.

L5 action 183: PLATE semantics confirmed (purple bars reappeared when L left plate). A1=up both (normal). State: L(11,2), R(7,12).
planner5.py joint BFS (state (pL,pR), doors open iff matching plate occupied; forbid ending on door tile without plate held pre&post) found 40-move solution from ((11,2),(7,12)):
A3 A3 A1 A4 A4 A1 A4 A4 A1 A1 A3 A2 A4 A4 A4 A1 A1 A3 A3 A3 | A3 A1 A1 A1 A1 A1 A3 A4 A4 A4 A1 A1 A1 A1 A1 A3 A3 A3 A3 (39? no: 40 total, split 20+20)
Full: ['A3','A3','A1','A4','A4','A1','A4','A4','A1','A1','A3','A2','A4','A4','A4','A1','A1','A3','A3','A3','A3','A1','A1','A1','A1','A1','A3','A4','A4','A4','A1','A1','A1','A1','A1','A3','A3','A3','A3'] -- CAUTION count: 40 items, first20 sent as actions 184-203, expected state after: L(5,3), R(5,10).
Remaining 20: ['A3','A3','A1','A1','A1','A1','A1','A3','A4','A4','A4','A1','A1','A1','A1','A1','A3','A3','A3','A3'] wait -- re-derive from planner output next turn to avoid transcription error. Key waypoints: R orange plate (5,14) steps 6-10; L through orange door to (7,2); L to (5,5) as R lands green plate (5,8) step 22; L up through green door to top; L to purple plate (0,3); R up through purple r4 door to (0,11); converge merge at (0,7).
Merge = both arrive (0,7) simultaneously. Timer: 51 total actions used by end, budget ~76. Rerun planner5.py to regenerate exact tail.

L5 action 203: batch 1 perfect, state ((5,3),(5,10)) as simulated. Batch 2 sent (204-223): A3 A3 A1 A1 A1 A1 A1 A3 A4 A4 A4 A1 A1 A1 A1 A1 A3 A3 A3 A3 -> merge at (0,7). Expect score 5 at action 223.

## LEVEL 5 CLEARED at action 223 (score 5). 40-move BFS plan flawless; merge at (0,7).

## LEVEL 6 (started action 223)
Arena rows 6-57, cols 6-57 inside C/z borders. 1px n/O checkerboard forms walls (presumed deadly like L4): outer band rows 6-9 & 54-57; vertical walls cols 6-8, 30-32, 54-56; horizontal door band rows 30-33.
Cells: upper-left (rows 10-29, cols 9-29), upper-right (rows 10-29, cols 33-53), lower-left, lower-right (rows 34-53). Center wall cols 30-32 ABSENT at rows 42-45 = center passage; blue 2x2 block at rows 43-44 cols 31-32 mid-passage.
Objects (4x4): L player (22-25,18-21), R player (22-25,42-45) mirrored. Orange block (14-17,18-21) above L; green block (14-17,42-45) above R; green block (42-45,18-21) lower-left. Door bars rows 30-33: green cols 14-25 (left), orange cols 42-53 (right).
Hypothesis: L5-style plates (stand on color -> matching door opens) OR sokoban pushable blocks. Plate-relay has hold problem (no wall to pin holder). Probe sent (224-225): A1 x2 -> both should reach overhead buttons if 4px steps. Watch: step size, door bars rows 30-33, block pushing.
Timer: L5 used 50 actions (173-223). L6 timer fresh at 223.

L6 action 225: plates confirmed (L on orange (14,18), R on green (14,42), 4px steps, A1=up both). Both door bars open while stood on.
planner6.py: joint BFS (pL,pR,blue,mode; death-safe = never press into checker-overlap) -> 43-action solutions for BOTH signs, both semantics. Plans differ only in the 6 mid-plan horizontal presses (A3x6 vs A4x6).
Door bands rows 30-33: green cols 14-25 (left), orange cols 38-49 (right). Plates: orange (14,18) UL, green (14,42) UR, green (42,18) LL. Blue 2x2 (43,31) center passage rows 42-45. Closed doors BLOCK safely (L5 evidence).
Probe sent (226-228): A3 (player sign: L->14 or 22), ACTION6(31,43) click blue, A3 (blue mapping: ->(43,27) or (43,35)).
Next turn: re-run planner6 BFS from actual post-probe state with observed mappings (relabel A3/A4 accordingly), execute in <=20 batches. Budget: used 5 of ~76 after probe.
CAUTION: planner6 DIRS uses A3=+4col internally; relabel to observed convention when emitting actions.

L6 probes 226-228: ACTION3 = L left / R right (L3 convention, sign=-1); blue ACTION3 = left (uniform). Blue mechanic identical to L3/L4 (freeze+yellow).
Full 44-action verified plan in plan6.json (path + real actions). State after probe: L(14,14) R(14,46) B(43,27) mode=B.
Key structure: blue up to (19,19) pins L on orange plate; R descends orange door to (42,42); blue to (27,23) pins L horizontally at (26,18); R crosses passage to lower-left green plate (42,18); blue to (47,19) pins R below; L descends green band to (34,18); A3 splits, A1 x2 (L grinds closed green door), final ACTION4 merges both at (34,18).
Batch 1 sent (229-248) = plan actions 1-20, ends blue at (27,23) mode B. Batch 2 = actions 21-40, batch 3 = 41-44.
Expected end state batch 2: L(34,18)? no: after action 40 = CLICK_P? recount: action 38 CLICK_P... batch2 = indices 20-39: ends L(34,18) R(42,18) B(47,19) mode n after A2 x2? index39 = A2 #2 -> L(34,18). Then batch 3: ACTION3, ACTION1, ACTION1, ACTION4 -> merge.
