# Game notes

## Board layout (Level 1)
- 64x64, light-blue background, black-bordered L-shaped panel.
- L-shaped grid of 4x4 cells ('8'=empty, 'I'=green), separated by '$'.
- Cell top-left coords: x = 11+6*col, y = 12+6*row. Cell centers ≈ (x+1..2, y+1..2).
- Top section: rows 0-2 (y=12,18,24), cols 0-6 (x=11..47).
- Bottom section: rows 3-6 (y=30,36,42,48), cols 4-6 only (x=35,41,47).
- Shape = L (7 wide top-3-rows, 3 wide right-4-rows).

## Green cells initially (row,col):
(1,1) (1,2) (1,4) (2,5) (4,5)

## Hypotheses to test
- Arrows slide/move greens (2048/Sokoban style)?
- Clicks toggle cells?
- Turn 1 probe: ACTION4 (Right), then ACTION2 (Down); diff boards.

## Turn 2 findings
- ACTION4/ACTION2 (arrows): NO grid change. Only top row pixel (0,0),(0,1) changed '$'->'8' = step/action counter.
- Step budget likely ~64 (top row width). Avoid wasting actions.
- Next: test clicks. Cell (row r, col c) center: ACTION6(x=12+6c, y=13+6r).
- Probe: click empty cell (0,0) -> ACTION6(12,13); click green cell (1,1) -> ACTION6(18,19).

## Turn 3 findings — PEG SOLITAIRE
- Click green peg => gray 'h' ring highlight around it + light-gray '#' diamond marks legal jump destination.
- Pegs: (1,1),(1,2),(1,4),(2,5),(4,5). Selected (1,1); dest (1,3) highlighted (jump over (1,2)).
- Click empty cell (Action 3) = 15-frame flash, no effect (wasted step).
- Cell centers: ACTION6(12+6c, 13+6r).
- SOLUTION (4 jumps): (1,1)>(1,2)>(1,3); (1,3)>(1,4)>(1,5); (1,5)>(2,5)>(3,5); (3,5)>(4,5)>(5,5).
- Clicks: dest(30,19); sel(30,19); dest(42,19); sel(42,19); dest(42,31); sel(42,31); dest(42,43).
- Turn 3 probe: dest click (30,19) to complete jump 1, then re-click (30,19) to test if landed peg re-selects.

## Turn 4 findings
- Jump confirmed: dest click executes jump, jumped peg removed, selection clears.
- Re-click landed peg re-selects. Mechanic fully verified.
- (1,3) currently selected with dest (1,5) highlighted.
- Sending: dest(42,19), sel(42,19), dest(42,31), sel(42,31), dest(42,43) -> should clear Level 1.

## LEVEL 2 (cleared L1 at Action 11, score 1; step counter reset)
- Main panel (top-left): 7x3 grid, cell x=7+6c, y=9+6r (centers 8+6c,10+6r... use (8+6c,10+6r)+1 -> clicks at (8+6c? no: centers (8..9+6c,10..11+6r)); using (14,16) style = (8+6c,10+6r) with c>=1.
- Pegs main: (1,1),(1,2),(1,4),(1,6) [row y=15].
- Orange/yellow box center board: rows 32-37 cols 30-35, orange 4x4 at (33,31). Click (32,34). Likely special cell/target node.
- Bottom-right panel: 2x2 grid, cell x=43+6c, y=45+6r. Peg at (1,0) [click (44,52)]. 
- Black wires link: main row1 right edge -> orange box right; orange box left -> bottom panel row1 left.
- Topology hypothesis: linear chain main(1,0..6)=pos0-6, orange=pos7, bottom(1,0)=pos8, bottom(1,1)=pos9. Pegs at 1,2,4,6,8.
- Solution if chain works: 1>2->3; 3>4->5; 5>6->7(orange); 8>7->6. One peg left.
- Turn 5: execute jumps 1-2, then select (38,16) to see if orange highlighted as dest.

## Turn 6 findings
- After jumps: main pegs (1,5),(1,6); bottom peg (1,0). Select (1,5) REFUSED (flash) => (1,5) has no legal jump; 5>6->orange NOT legal.
- Selection refused = flash animation, no ring. Refused selects still cost a step.
- Hypothesis update needed: orange may be a peg itself (chain 6-orange-8 all occupied => no jumps), or wire topology differs.
- Turn 6 probe: select (1,6) [44,16]; click orange [32,34]; select bottom(1,0) [44,52]. Observe highlights in each post-action board.
- Current state likely dead (may need RESET after info gathering).

## Turn 7 findings
- A17: select M(1,6) OK, only dest M(1,4). A18: click orange while selected = deselect. A19: select B(1,0) refused.
- Brute force: orange = MOVABLE PEG model explains all refusals (O node occupied). 
- Path from CURRENT state (no reset): O > B(1,0) -> B(1,1) [removes bottom green]; then M(1,5) > M(1,6) -> O-node. 1 green left.
- Clicks: sel orange (32,34); dest B(1,1) (50,52); sel M(1,5) (38,16); dest O (32,34).
- If goal requires removing orange too, this fails -> then RESET and rethink.

## Turn 8 findings
- A20-23 all no-ops: orange NOT selectable (even with nothing selected). M(1,5) still refused. Orange is static.
- Never actually tested jumping OVER orange (both far ends 6,8 were always occupied).
- Model "orange = static obstacle, goal = jump/capture it": solvable. From CURRENT state: 6>5->4; then B(1,0) over O -> M(1,6).
- Clicks: sel(44,16), dest(32,16), sel(44,52), dest(44,16).
- Watch: does B(1,0) select show dest at M(1,6)? Does jump remove orange? Score?
- If B(1,0) select refused again => wire jumps don't exist; RESET + rethink (orange might be goal-pattern display).

## Turn 9 findings
- A25 (6>5->4) worked: main now 1 gray peg at (1,4); bottom 1 gray peg B(1,0).
- Animation: after jump, ALL pegs turn gray '#' (frame 16), then purple box grows bottom-left (rows 51-59, cols 2-12; white 2x2 core rows 55-56, cols 6-7).
- Gray pegs + purple box = terminal-state UI (no legal moves anywhere). Score still 1 -> not a win... OR purple is a confirm button.
- A26/A27 clicks refused during this state; wire-jump disproof not fully conclusive but likely (terminal state implies game sees no legal moves incl. wire).
- Turn 9: click purple button ACTION6(6,55). If restart -> fresh board; if win -> score.

## Turn 9 findings
- A25 (6>5->4) worked: main now 1 gray peg at (1,4); bottom 1 gray peg B(1,0).
- Animation: after jump, ALL pegs turn gray '#' (frame 16), then purple box grows bottom-left (rows 51-59, cols 2-12; white 2x2 core at rows 55-56, cols 6-7).
- Gray pegs + purple box = terminal state UI (no legal moves anywhere). Score still 1 -> not a win... OR purple is a confirm button.
- A26/A27 clicks refused during this state.
- NOTE: wire jump B(1,0) over O -> M(1,6) refusal at A26 may be due to terminal state, still not conclusively disproven... but terminal state itself implies game sees no legal moves incl. wire jump => wire jumps for greens likely don't exist.
- Turn 9: click purple button ACTION6(6,55). If restart -> observe fresh board; if win -> score.

## Turn 10 findings
- Purple button = RESTART level (pegs back to start, greens restored). Step counter NOT reset (17 used of 64).
- Wire jumps for greens conclusively absent (game declared {M(1,4),B(1,0)} terminal).
- Panel-jumps alone: reachable states all dead-end at 2 pegs => hidden mechanic required.
- Untested: arrows on level 2; arrows WITH a peg selected; Undo (ACTION7).
- Turn 10 probe: ACTION4, ACTION1 (watch orange/wires), then select M(1,1) (14,16), ACTION4 (does arrow move/jump selected peg?).

## Turn 11 — CART DISCOVERED
- ACTION4 moves orange cart RIGHT 6px along horizontal wire (rows 31-38 box). ACTION1 refused mid-track. A32 Right also moved cart (peg got deselected first, harmless).
- Cart interior center now (x=44.5, y=34.5). Track: horiz rows 34-35 cols 14-57; vert right cols 56-57 rows 16-35 (to main row1 socket); vert left cols 14-15 rows 34-53; bottom horiz rows 52-53 cols 14-42 (to bottom panel row1 socket).
- MODEL: cart = mobile empty cell. Dock at main socket -> 5>6->cart legal; carry peg to bottom socket -> cartpeg over B(1,0) -> B(1,1). 1 peg left = win.
- Route: 2xRight (center->56.5), 3xUp (->16.5) = docked M(1,7).
- Then jumps: sel(14,16) dest(26,16); sel(26,16) dest(38,16); sel(38,16) [observe cart '#'].
- Budget: 21/64 used before this batch. Success path total ~52. NO room for restart - be careful.
- Next turn: dest cart click; 3xDown, 7xLeft, 3xDown, 4xRight; sel cartpeg, dest B(1,1) (50,52).

## Turn 12 findings
- Cart docked at main socket via 2R+3U: interior rows 15-18, cols 55-58 = virtual (1,8). Jumps 1,2 done: main pegs (1,5),(1,6); bottom B(1,0).
- A42 select (1,5) STILL refused: cart is 1 wire-cell short of adjacency (gap at (1,7), wire stub rows 16-17 cols 48-55).
- Fix hypothesis: ACTION3 slides cart Left along stub -> interior cols 49-52 = (1,7) adjacent. Then 5>6->cart legal.
- Turn 12 (3 actions): ACTION3; sel(38,16); dest cart (50,16).
- If works, next turn EXACTLY 20: R,3xD,7xL,3xD,4xR (18 moves) + sel cart (38,52) + dest B(1,1) (50,52). Budget: 34 used after this turn; 54 total. OK.
- If refused again: 30 actions left, rethink (cart-as-peg bridge model etc).

## Turn 13 — PEG LOADED
- ACTION3 slid cart flush to main panel (interior cols 49-52). 5>6->cart jump EXECUTED: green peg now inside cart, main panel empty, bottom B(1,0) remains.
- Cart center (50.5,16.5). Route to bottom dock: 1R, 3D, 7L, 3D, 4R -> center (38.5,52.5), adjacent-left of B(1,0).
- Final: sel cart (38,52), dest B(1,1) (50,52) -> jump over B(1,0), 1 peg left -> expect WIN.
- Budget: 34 used + 20 = 54/64.

## LEVEL 3 (score 2 at Action 65; counter reset; L2 took 54 actions)
- Panel A rows 4-29: cells x=6+6i, y=6+6j; shape j0:{0,1,3,4} j1:{0,1,3,4} j2:{0,1,2,3} j3:{0,1,2,3} (gap at i=2 for j0,j1).
  Pegs A: (1,1),(4,1),(1,2),(3,2),(2,3). Click cell = (x0+1,y0+1).
- Panel B: 1x1 at x=60-63,y=12-15 (right edge, maybe extends off-screen). 1 peg. No visible lines -> frozen?
- Panel C rows 46-59: j0 y=48: i=0..3 (x=6..24), pegs (1,0),(3,0); j1 y=54: i=0,1,2. No adjacent peg pairs -> frozen?
- Cart1: box rows 10-17 cols 40-47 on wire rows 13-14 (A2 edge col35 <-> B edge col58). Docks: A(5,1) flush / B-left flush.
- Cart2: box rows 46-53 cols 34-41 on wire rows 49-50: C edge col29 <-> up col43-44, bridge rows 37-38, down col55-56, right branch rows 49-50 cols 55-63 DEAD END at board edge.
- Open questions: do arrows move BOTH carts? Hidden win condition (C seems frozen at 2 pegs => win may not be 1 total). Maybe B panel has hidden cell off-screen (L2-style ending).
- Turn 14 probe: ACTION3 (watch both carts); select A(1,1) (13,13) [expect dest (1,3)]; select A(4,1) (31,13) [expect refusal]; select C(1,0) (13,49) [expect refusal].

## Turn 14 findings (L3, A66-69, 4/64 used)
- ACTION3 moved BOTH carts (one arrow = both carts). Cart1 now flush-docked at A right = virtual A(5,1) (interior x36-39,y12-15, click (37,13)). Cart2 flush at C right = virtual C(4,0) (interior x30-33,y48-51).
- Select A(1,1) OK, single dest (1,3). Select A(4,1) refused. Select C(1,0) refused. C panel provably frozen (2 pegs, no triples, cart2 can't be loaded).
- DFS on A + cart(5,1): UNIQUE solution to 1 peg, final peg lands IN CART:
  (1,1)>(1,2)->(1,3); (1,3)>(2,3)->(3,3); (3,3)>(3,2)->(3,1); (3,1)>(4,1)->(5,1)
- Clicks (cell (i,j) -> (7+6i,7+6j)): sel(13,13) dest(13,25); sel(13,25) dest(25,25); sel(25,25) dest(25,13); sel(25,13) dest cart(37,13).
- Plan: 8 jump clicks + 3x ACTION4 (ferry toward B, interior 36->54). Next turn: flush-slide if needed (L2-style), then sel cart, dest over B peg into suspected off-screen cell right of B (x=60-63,y=12-15 at board edge).
- Win condition hypothesis: per-system 1 peg (C frozen at 2 is by design). Total after finish = 3 pegs (1 off-screen + 2 in C).

## Turn 15 findings (A70-80, 15/64 used) — WORLD IS WIDER THAN VIEWPORT
- Jumps 1-4 executed perfectly; peg LOADED in cart1. 3x Right: carts move 6px, CAMERA SCROLLS 8px/press. Camera offset now +24 (world x = screen x + 24). Step counter row 0 is screen-fixed (15 used).
- Cart1 (loaded) interior world x54-57,y12-15 = FLUSH-DOCKED adjacent-left of B peg (world 60-63). Jump dest cell world 66-69 exists (empty). B panel = rows y6 (x66,72) + y12 (x60=Bpeg,66,72), walls world 59-77, vert wire world col 78 rows 5-15 on its right.
- BIG PANEL right: left wall world col 65, sections stacked (horiz walls screen rows 16,23,28,35,40,47,59). Pegs visible (screen): (18-21,48-51),(18-21,54-57),(30-33,48-51),(30-33,54-57),(42-45,42-45),(48-51,48-51). Extends off-screen right.
- Cart2 empty, interior world 42-45,y48-51, AT BRIDGE JUNCTION (moved only 12px/3 presses, 3rd refused: bottom wire has GAP; must go UP over bridge world cols 43-44 up, bridge rows 37-38, down cols 55-56, then right wire world 55-64 docks at big panel row48 section left socket).
- Cart2 ferry idea: bring a big-panel peg back to C dock (4,0) -> unfreezes C: (4,0)>(3,0)->(2,0); (1,0)>(2,0)->(3,0) => C down to 1 peg (0 impossible without 2nd delivery; last C jump into cart possible: pegs (2,0)+(3,0)+empty cart => (2,0)>(3,0)->cart).
- Turn 15 probe: ACTION4 (does camera scroll when both carts refuse? cart1 docked, cart2 gapped) => cheap map reveal right. Then 2x ACTION1 (cart2 climbs bridge; does camera scroll vertically?).

## Turn 16 findings (A81-83, 18/64 used)
- A81 Right with both carts blocked = TOTAL no-op (no camera scroll). Camera only moves when a cart moves. 1 step wasted.
- A82/83 Ups: cart2 climbed to bridge level, interior rows 36-39 cols 18-21 (world 42-45). No vertical camera scroll (world is 64 tall).
- Cart2 route remaining: 2x Right (bridge rows 37-38 to right vertical cols 31-32 screen / 55-56 world), 2x Down (to bottom wire rows 49-50), then Rights+flush to dock at big panel row48 socket (wall world col 65).
- B-jump is FORCED (only cart1-peg can ever remove B peg; landing cell world (66-69,12-15) fixed). Executing now: sel cart1 (31,13), dest (43,13).
- Then 2x Right: cart2 crosses bridge, camera should scroll +8 each -> reveals world right edge.

## Turn 17 — FULL WORLD MAP + SOLUTION (A84-87 done, 22/64 used)
- B-jump executed: peg now at (10,1). Cart1 empty, docked at (8,1). Camera FIXED at +24 (only scrolls when LOADED cart moves; empty cart moves don't scroll — A86/87 proof).
- World grid: cell (i,j) = world x0=6+6i, y0=6+6j. Click screen = (6i-17, 6j+7) at camera 24.
- RIGHT PANEL cells: j0:{10,11} j1:{9,10,11}+cart1(8,1) j2:{10,11,12,13} j3:{10,11} j4:{10,11,12,13} j5:{10,11} j6:{10,11,12} j7:{10,11}+cart2dock(9,7) j8:{10,11}. Pegs: (10,1),(11,2),(12,2),(11,4),(12,4),(10,6),(11,7).
- C panel: j7:{0,1,2,3}+cart2dock(4,7); j8:{0,1,2} (j8 unreachable, no vertical triples). Pegs (1,7),(3,7). Needs ONE delivery; then min 1 peg.
- WIN LINE (assume win=1 peg total):
  R-panel: (12,2)>(11,2)->(10,2); (12,4)>(11,4)->(10,4); (10,1)>(10,2)->(10,3); (10,3)>(10,4)->(10,5); (10,5)>(10,6)->(10,7); (11,7)>(10,7)->cart2(9,7).
  Ferry cart2 loaded to C dock: 1L,2U,2L,2D,2L (9 moves; WATCH: loaded cart may scroll camera LEFT 8/press -> recompute click coords next turn!).
  C: (4,7)>(3,7)->(2,7); (1,7)>(2,7)->(3,7). Final peg (3,7).
- This turn (15 acts): 2xDown,1xRight (dock cart2 at (9,7)); then 12 clicks:
  sel(55,19) dest(43,19); sel(55,31) dest(43,31); sel(43,13) dest(43,25); sel(43,25) dest(43,37); sel(43,37) dest(43,49); sel(49,49) dest(37,49).
- Next turn: 9 ferry moves + 4 C clicks (world coords: sel(31,49) dest(19,49); sel(13,49) dest(25,49); screen = world - camera).

## Turn 18 (A88-102 done, 37/64 used)
- Full 6-jump right-panel solution EXECUTED. Right panel empty; cart2 LOADED at dock (9,7). Only pegs left: C (1,7),(3,7) + cart2 peg.
- Ferry: L,U,U,L,L,D,D,L,L -> dock C (4,7) (interior world 30-33). Camera should scroll 24->16->8->0 on the loaded Lefts (clamp 0).
- C finish (screen=world if camera 0): sel cart (31,49), dest (19,49) [(4,7)>(3,7)->(2,7)]; sel (13,49), dest (25,49) [(1,7)>(2,7)->(3,7)]. Final: 1 peg at (3,7) => expect score 3.
- Failure mode if camera model wrong: 4 flash clicks, no damage; recompute next turn. Budget after batch: 50/64.

## LEVEL 4 (score 3 at Action 115; L3 took 50 actions; counter reset)
- Main panel rows 16-35 cols 4-49: cells x0=6+6i (i=0..6), y0=18/24/30 (j=0,1,2). Pegs at (1,j1),(6,j1). PURPLE cells '"' w/ 'z' blob at (2,j1),(4,j1), black 'OOOO' under them (row 27) = NEW MECHANIC (blocker? pit? goal?).
- Cart (empty) box rows 23-28 cols 53-58 on horiz wire rows 25-26: left to main panel right socket (virtual (7,j1)?), right off-screen (cols 59-63+).
- Bottom panel rows 58-63+ (extends off-screen BOTTOM): cells x0=30,36,42 y0=60; peg at x36. Vert wire cols 55-56 rows 49-63 + horiz wire rows 49-50 cols 55-63 off-screen right.
- World extends right AND down. Camera position unknown (probably top-left clamp).
- Probe: sel peg (13,25) -> purple jumpable? sel peg (43,25); ACTION4 (cart right, camera?); ACTION2 (cart down-refuse test).

## Turn 20 findings (A116-119, 4/64 used)
- Purple cell IS jump-over-able: sel peg (1,j1) showed dest (3,j1) (over purple (2,j1)). Unknown if purple is removed by the jump.
- Clicking another peg while selected = DESELECT only (not switch). A117 wasted as info.
- A118 Right: cart +6px, now box cols 59-63+ half off-screen; NO camera scroll (empty cart). A119 Down: refused (pure no-op).
- Probe: execute jump 1 over purple [sel(13,25), dest(25,25)] -> does purple vanish? Then 2x Right (cart explores off-screen wire; track by move count).

## Turn 21 findings (A120-123, 8/64 used)
- PURPLE = permanent springboard: jump over it works (45-diff jump, vs 57 normal) but purple NOT removed. Pegs: (3,j1),(6,j1) + bottom-panel peg.
- Cart wire right ends just off-screen: cart interior world 66-69 (3 Rights from start), 4th Right refused. Probably hidden dock/junction there - explore later with loaded cart (camera follows loaded carts only).
- Win hypothesis: only GREEN pegs count; purples are terrain.
- Line: (3)>(4p)->(5); then (5)>(6)->cart(7,j1) loads cart (removes (6)); ferry loaded cart off right (camera reveals hidden wire), find route to bottom panel; deliver & finish -> 1 green peg.
- This turn: sel(25,25) dest(37,25); 3x Left (cart back to interior 54-57); ACTION3 again (flush-slide test); sel(37,25) -> does dest show cart cell (7,j1)?

## Turn 22 findings (A124-130, 15/64 used)
- Jump (3)>(4p)->(5) done. Cart1 flush-docked at main socket (interior cols 48-51 = virtual (7,j1)); sel (5,j1) shows '#' DEST INSIDE CART. Load = dest click (49,25), removes (6,j1).
- SECOND CART exists! Was off-screen right on rows 49-50 wire; Lefts pulled it to the junction at cols 53-58 rows 47-52 (interior 54-57/48-51). Junction: horiz rows 49-50 (left: DEAD short stub?; right: off-screen) x vert cols 55-56 going DOWN off-screen (to hidden bottom-panel socket, y>63).
- A126 Left refused for cart1 (at wire end) but A127-129 worked - wire-end may have latch/8px offset; unexplained, low priority.
- Bottom panel UNchanged (cols 28-49; peg at x36-39,y60). World unknown: x>=64 and y>=64.
- Greens after load: cart1 peg + bottom peg = 2. Endgame guess: get cart1 peg into bottom system, capture bottom peg -> 1 green.
- This turn: load cart1 (49,25); 4x Right (loaded cart1 -> camera follows right, reveals east; cart2 returns toward its right wire-end harmlessly).

## Turn 23 — EAST PANEL MAPPED (A131-135, 20/64 used; camera x=54)
- A131 load click caused CAMERA SCROLL (peg entering cart makes it camera target). Cart1 (loaded) drove 4 Rights, now FLUSH-DOCKED at east panel left socket = virtual (11,3), interior world 72-75 screen 18-21.
- EAST PANEL: cells i12-17 x j3-7 (world x0=78+6k, y0=24+6m), except (12,7)=cart2 dock notch. PEGS (12,3),(16,3). PURPLE springboards (13,4),(16,4),(13,6),(16,6),(15,7).
- Cart2 empty, docked at virtual (12,7) (interior world 78-81). Its wire: rows 49-50 world x55-77 + vertical world cols 55-56 going down (below y63) toward hidden bottom-panel socket.
- Bottom panel (off-screen): x28-49,y58+, peg at (x36,y60). Greens total: cart1peg,(12,3),(16,3),bottom = 4.
- FULL EAST LINE (camera 54; click screen=(6i-47, 6j+7)):
  1 (11,3)>(12,3)->(13,3): sel(19,25) dest(31,25)
  2 (13,3)>(13,4p)->(13,5): sel(31,25) dest(31,37)
  3 (16,3)>(16,4p)->(16,5): sel(49,25) dest(49,37)
  4 (13,5)>(13,6p)->(13,7): sel(31,37) dest(31,49)
  5 (16,5)>(16,6p)->(16,7): sel(49,37) dest(49,49)
  6 (16,7)>(15,7p)->(14,7): sel(49,49) dest(37,49)
  7 (14,7)>(13,7)->cart2(12,7): sel(37,49) dest(25,49)  [loads cart2, captures (13,7)]
  Then: 4x Left (cart2 to junction world 54-57), Downs (hidden), deliver over bottom peg -> 1 green WIN.
- RISK: unload (jump 1) might scroll camera (like load did). Sending jumps 1-3 only; verify camera stable, then batch rest.

## Turn 24 (A136-141 done, 26/64): jumps 1-3 OK, camera stable at 54. Unload does NOT scroll camera.
- Now: jumps 4-7 [sel(31,37) dest(31,49); sel(49,37) dest(49,49); sel(49,49) dest(37,49); sel(37,49) dest(25,49) loads cart2] + 4x Left (junction) + 2x Down (probe descent; camera follows loaded cart2).
- After batch: 40/64. Next: finish descent + delivery jump over bottom peg.

## Turn 25 — SOUTH COMPLEX MAPPED (A142-155 done, 40/64; camera ~(15,42))
- East line + load cart2 + 4L,2D ferry all executed. Cart2 LOADED, docked at top of south complex = virtual (c5,r0), screen interior (40-43,18-21).
- Screen grid: x0=9+6c (c0..c7), y0=18+6r (r0..r4). World = screen + (15,42).
- r0 bottom1 panel: c1 E, c2 PEG, c3 E. r4 bottom2 panel: c1 E, c2 PEG, c3 E.
- r1: c0 E, c1 P, [c2 wirebox], c3 P, c4 E, c5 P, c6 E, c7 E. r3: c0 E, c1 P, [c2 box], c3 P, c4 E, c5 E, c6 E, c7 E.
- r2: c0 E, c7 E; horizontal wire tunnel through c1..c6 carrying CART3 (empty, parked at c2 slot, interior screen 21-24/30-33).
- WIN LINE (21 acts -> 61/64), split into 5 safe batches (loads scroll camera; end each batch on the load):
  A: 3xRight (cart3 c2->c5) + sel cart2 (41,19) + dest cart3 (41,31)  [peg down over purple into cart3]
  B: 4xLeft (loaded cart3 c5->c1; camera may scroll left - no clicks)
  C: sel cart3, dest (c1,r0) [up over purple]; sel (c1,r0), dest (c3,r0) [CAPTURE bottom1 peg]
  D: 2xRight (cart3 c1->c3); sel (c3,r0), dest cart3 (c3,r2) [down over purple into cart3]
  E: sel cart3, dest (c3,r4) [down over purple]; sel (c3,r4), dest (c1,r4) [CAPTURE bottom2 peg] -> 1 green, WIN
- Alignment worry: cart2 interior x40-43 vs c5 column x39-42 (1px off). If A's dest not offered, rethink (maybe flush-slide needed).

## Turn 26 (A156-160 done, 45/64)
- Cart3 parked c5 (3R: interior 21->39), cart2 unloaded THROUGH purple (c5,r1) into cart3. Cart-to-cart drop caused NO camera scroll. Cart3 loaded at (c5,r2) interior screen 39-42/30-33.
- Batch B now: 4x Left (cart3 c5->c1). Watch scroll. Then C: sel cart3, dest up (c1,r0); capture bottom1.

## Turn 27 (A161-164 done, 49/64)
- Cart3 (loaded) shuttled c5->c1, interior screen 15-18/30-33. NO camera scroll on loaded cart3 moves (rules fuzzy; irrelevant).
- Batch C: sel cart3 (17,31), dest (17,19) [up over purple to (c1,r0)]; sel (17,19), dest (29,19) [capture bottom1 peg -> (c3,r0)]. After: 53/64, 2 greens left.

## Turn 28 (after A165-168, counter 53/64)
Batch C SUCCESS: peg up over purple to (c1,r0), then captured bottom1 -> peg now at (c3,r0) [screen x27,y18].
Bottom1 panel empty. Cart3 EMPTY at c1 (interior 15-18, rows 30-33). Remaining greens: (c3,r0), (c2,r4). 11 steps left.
Batch D (written): 2x ACTION4 (cart3 c1->c3, empty so no scroll), sel (29,19), dest (29,31) [down over purple (c3,r1) into cart3]. Load-click last per policy. After: 57/64.
Batch E next: sel cart3 (29,31), dest (29,43) [down over purple (c3,r3) to (c3,r4)]; sel (29,43), dest (17,43) [CAPTURE bottom2 peg -> (c1,r4)] -> 1 green, WIN at 61/64.

## Turn 29 (after A169-172, counter 57/64)
Batch D SUCCESS: cart3 empty c1->c3 (2 Rights, no scroll), peg (c3,r0) jumped down over purple (c3,r1) into cart3. Cart3 LOADED at c3 (interior 27-30, rows 30-33). Greens: 1 in cart3, 1 at (c2,r4). 7 steps left.
Batch E (written, FINAL): sel cart3 (29,31), dest (29,43) [down over purple (c3,r3) to (c3,r4)]; sel (29,43), dest (17,43) [CAPTURE bottom2 peg, land (c1,r4)] -> 1 green = expect Level 4 CLEAR at 61/64, score 4.

## Turn 30 — LEVEL 4 CLEARED (Score 4, Action 176, 61/64). LEVEL 5 begins.
L5 board (settled after A176), counter fresh 0/64:
- Top wire rows 7-8, cols 11-53. CART1 empty orange, cols 16-23. CART2 cols 40-47 CARRIES A PURPLE SPRINGBOARD (new mechanic!).
- Main panel cols 10-29 rows 16-35: 3x3 cells, x0={12,18,24}, y0={18,24,30}. Contents: r1c0 PEG (12,24); r1c1 PURPLE (18,24); rest empty. No visible wall gaps/sockets.
- East panel cols 34-47 rows 22-29: 1x2 cells y0=24, x0={36,42}: c0 empty, c1 PEG.
- Vertical wire cols 31-32 (rows 9-44) hugging main panel right side; vertical wire cols 49-50 (rows 21-44) at east panel right side; bottom wire rows 43-44 cols 19-51; branch wire cols 19-20 descends rows 45-58+ OFF-SCREEN (more world below).
- 2 pegs visible total. Probe: select main peg at (13,25) to see dest diamonds.

## Turn 31 (after A177, 1/64)
Main peg selected: h-ring at r1c0, single '#' dest at r1c2 (24-27 rows 24-27) = jump right over purple. Peg still selected.
Panels have NO visible wall gaps — exit mechanism unknown; hypothesis: purple-cart docks flush on vertical wire and enables jumps through/over wall.
Probe written: ACTION3 x2 (cart1 blocked at wire-left per L4 partial-move rule; cart2 40-47 -> 28-35, centering interior on vertical wire junction cols 31-32), then ACTION2 (test descent of purple-cart down wire cols 31-32 along main panel right side).

## Turn 32 (after A178-180, 4/64)
- Arrows DESELECT pegs. Left#1 moved BOTH carts (cart1 16-23 -> 10-17 now wall-blocked; cart2 40-47 -> 34-41). Left#2 cart2 -> 28-35. Down: cart2 turned onto vertical wire cols 31-32, now vertical cart rows 10-17 (purple interior rows 11-14, cols 31-34).
- Lattice: cells x0 = 12,18,24,[30=inter-panel virtual],36,42,[48=east dock virtual]. Cart-purple at x0~30,y0~24 lets peg jump r1c2 (24) -> east c0 (36) THROUGH walls (hypothesis).
- WIN PLAN: (1) cart2 down 2 -> dock (30,24). (2) main peg: r1c0 ->(over panel purple) r1c2 ->(over cart purple) east c0. (3) cart2 out of way: down to bottom wire, 2 Lefts, 3 Downs onto south branch (cols 19-20). (4) cart1: 3 Rights (top wire), ~6 Downs (main vertical), 3 Rights (bottom), ~3 Ups (east wire cols 49-50) -> dock (48,24). (5) east c0 peg jumps over east c1 peg -> CAPTURE, lands in cart1 -> 1 peg = WIN. Est total ~36/64.
- Camera may scroll during phase 3/4 (cart2 loaded with purple moves off-screen south) — recompute click coords for final capture.
- Batch written: 2 Downs, then jump main peg to r1c2, re-select to verify '#' dest at east c0 (37,25).

## Turn 33 (after A181-185, 9/64)
Cart2 docked flush inter-panel (rows 22-29, purple interior ~cols 30-33, rows 24-27 aligned with row B). Peg jumped r1c0->r1c2 (springboard, no capture). Re-selected: dests '#' at r1c0 AND east c0 (36,24) — THROUGH-WALL cart-purple jump CONFIRMED.
Batch written: ACTION6(37,25) jump peg -> east c0; then 2 Downs (cart2 leaves dock toward bottom junction rows ~36-43). Next: 2 Lefts + 3 Downs (cart2 parks down south branch cols 19-20), then cart1 ferry (3R, ~6D, 3R, ~3U) to east dock (48,24), final capture c0-over-c1 lands in cart1 = WIN.

## Turn 34 (after A186-188, 12/64)
Jump SUCCESS: peg at east c0; east panel now c0 PEG + c1 PEG. Cart2 descended to rows 34-41 (interior 35-38, cols 30-33), one press above bottom junction (wire rows 43-44).
Batch: ACTION2 (cart2 onto junction, interior ~41-44), ACTION3 x2 (slide to south junction, interior cols ~18-21). Next: 3 Downs (park cart2 down south branch), then cart1 ferry 3R/~5D/3R/~3U to east dock (48,24), capture click pair.
Cart1 at cols 10-17 top wire: blocked for Left/Down ✓ (won't move during these).

## Turn 35 (after A189-191, 15/64)
Cart2: turned onto bottom wire, slid left, now vertical over south junction (cols 16-23, interior 18-21, rows 40-47).
PLAN SIMPLIFIED: no east-dock ferry. Cart1 -> inter-panel dock (30,24): 3 Rights (cart1 10-17 -> 28-35; cart2 drifts right along bottom wire 16-23 -> 34-41, interior 36-39 = mid-wire, then Down-blocked, harmless), 3 Downs (cart1 rows 4-11 -> 22-29 dock; cart2 immobile, no camera scroll). Then sel east c1 (43,25), click (31,25): c1 jumps LEFT over c0 = CAPTURE, lands in cart1 -> 1 peg = WIN at ~23/64.

## Turn 36 (after A192-199, 23/64) — capture worked, NO CLEAR
East c1 captured c0, landed in cart1 at inter-panel dock (rows 23-28). 1 peg visible (in cart1) but Score still 4 => MORE PEGS OFF-SCREEN (south branch cols 19-20 and/or east wire rows 19-20). Win counts whole world.
Cart2 now mid-bottom-wire cols 34-41 (interior 36-39). Cart1 LOADED at dock cols 29-35ish rows 23-28.
Batch: 1 Right (cart2 -> 40-47, clears cart1's landing zone), 3 Downs (cart1 dock -> bottom junction rows 40-47; loaded => camera may scroll), 2 Lefts (cart1 -> south junction cols 16-23; cart2 trails to 28-35, then Down-blocked there since main wire ends at bottom), 2 Downs (cart1 descends south branch, reveals south world).

## Turn 37 (after A200-207, 31/64)
- Camera shifted dx=-12 during the 2 Lefts: horizontal loaded-cart moves scroll camera 6px/press; vertical moves do NOT scroll. Screen = world + 12 now (main panel at cols 22-41).
- SOUTH BRANCH DEAD-ENDS at world rows ~52-59 (no wire below cart1, no panel). It is a parking spur only. No pegs south.
- Cart1 (PEG) at branch end, world rows 52-59, cols 16-23. Cart2 (purple) at bottom wire, world cols 28-35, interior on main junction (can move UP the main wire).
- Remaining pegs must be EAST via rows 19-20 wire (connects to east vertical wire top, world cols 49-50).
- Route written (11): 2 Ups (cart1 -> south junction; cart2 rises main wire to 28-35), 5 Rights (cart1 bottom wire -> east junction 46-53; cart2 on vertical wire immobile), 4 Ups (cart1 -> rows 19-20 junction, interior rows 18-21; cart2 tops out at top wire rows 4-11).
- Next: Rights to drive cart1 east along rows 19-20 wire, camera follows revealing east world. NOTE: Rights will also slide cart2 east along the TOP wire (both horizontal) — watch for it.

## Turn 38 (after A208-218, 42/64)
Camera: screen = world - 18. Cart1 (peg) at east-wire top junction, interior screen cols 30-33, rows 18-21. Cart2 parked top wire (world 28-35).
EAST WORLD REVEALED: rows 19-20 wire continues east (screen cols 36-50), ends at vertical junction screen cols 48-49 descending to a dock at rows 22-29, flush LEFT of a NEW PEG cell (screen 54-57, rows 24-27, lattice x0=54). Beyond: empty cell x0=60 (row B) and a TALL 3x3 panel (wall col 58) continuing off-screen east with cells rows 18-21/24-27/30-33.
PLAN: 3 Rights (cart1 interior -> cols 48-51 junction; camera scrolls ~18px east; cart2 slides to top-wire end world 46-53), 1 Down (cart1 -> dock rows 22-29). Then capture: sel cart peg, jump right over new peg landing x0=60 cell (2->1 pegs; if no more pegs east, WIN).
Predicted post-scroll screens: cart1 interior ~cols 30-33, new peg ~36-39, landing ~42-45 (verify fresh).

## Turn 39 (after A219-222, 46/64)
Camera scrolled 18 more east (screen = world - 36). Cart1 DOCKED rows 22-29, interior cols 30-33 (peg), flush left of new peg cell (36,24). Landing cell (42,24) EMPTY in a 1-wide 3-tall mid panel (x0=42, rows y0=18/24/30).
FAR-EAST panel (cols 52+): cells x0=54 (3 rows, all empty) and x0=60: PURPLE at row B (rows 23-26), empty cells rows 18-21/30-33. Vertical wire cols 49-50; horizontal wire row 14 heading east off-screen. World may continue east.
Batch: sel cart peg (31,25), click (43,25) = capture new peg, land (42,24). 2->1 visible pegs. If score bumps, L5 done; else continue east.

## Turn 40 (after A223-224, 48/64) — capture OK but EAST REGION revealed; current attempt likely DOOMED
Capture: cart-peg jumped P3, landed world (78,24) [strip col cells (78,18/24/30)]. Camera jumped: screen = world - 69, dy 0.
EAST REGION (world coords = screen+69, rows same):
- Top 1x6 panel rows 4-11: cells x0=90,96,102(PURPLE),108,114,120(PEG B world (120,6)).
- Center 3x3 panel: x0=90,96,102, y0=18,24,30; PURPLES at (96,24) and (102,30); all cells empty.
- Right 3x2 panel: x0=114,120, y0=18,24,30; PEG C at (114,30).
- Bottom 1x3 panel rows 52-59: x0=90,96,102, y0=54; PEG D at (102,54). Connector col above: cell (96,42), PURPLE (96,48).
- CART3 (purple) docked on vertical wire world 126-127, rows 16-23 (virtual cell (126,18)?).
- Wires: horiz rows 13-14 world 85-128; vertical 85-86 rows 15-22 (docks virtual (84,18) right of strip top cell (78,18)); vertical 109-110; vertical 126-127; horiz rows 37-38 world 85-128; bottom connector wires.
- WEST & EAST wire systems are DISCONNECTED (rows19-20 wire ends ~world 68; east starts 85). Pegs cross only via the strip jumps.
- Peg A (ours, world (78,24)) is STUCK: only escape = another peg arrives at (78,18) [via (90,18) jumping west over cart3-purple docked at (84,18)] then captures A downward.
- 6 pegs at fresh start: P1 main, P2 east-c1, P3 strip (72,24), B, C, D.
- DECISION: current attempt unwinnable in 16 steps. SCOUT east region with remaining steps (selects reveal dest diamonds; knowledge survives reset), then RESET and replay optimized (~38-step west prefix known).
Probes written: sel/desel C (46,31), B (52,7), D (34,55).

## Turn 41 (after A225-230, 54/64)
All 3 east pegs REFUSED selection (zero diffs) => B, C, D currently have no legal moves (need cart3-purple docks / incoming pegs).
Key lattice insight: rows 13-14 wire => y0=12 virtual dock row (between top y0=6 and center y0=18): cart3 at (120,12) enables B down to (120,18). Bottom wire rows 37-38 => y0=36 dock row: (96,36) enables chain (96,30)->(96,42)->over(96,48)purple->(96,54)->D captures->(90,54).
UNSOLVED: B & C interaction — my current map says impossible (B oscillates (120,6)<->(120,18), C fully stuck). MISSING STRUCTURE likely (wire 126-127 extent? world beyond 128? (108,y) docks via wire 109-110?). SCOUT: D (test cart3 descent), U, U (to rows13-14 junction), R, R (slide east, camera follows loaded cart3, reveal far east).
Then RESET (counter back to 0; keep knowledge). West replay prefix (~38 steps) in Turn 40 notes.

## Turn 42 (after A231-235, 59/64)
- Cart3 wire: vertical world 127-128 rows 15-29+ (Down worked); junction with rows13-14 wire at top; NO wire east of junction (Rights = 0 diff). Cart3 now at junction = virtual (126,12).
- Camera follows only the PEG-carrying cart (cart3 purple moves never scrolled; earlier scrolls all involved cart1 with peg or capture events).
- Cart1 rose to rows 16-23 during Up probes (harmless, resetting anyway).
- UNTESTED KEY: cart3 sliding WEST along rows13-14 wire (y=12 dock row under top panel). Batch: ACTION3 (cart3 -> (120,12)), ACTION6(52,7) (select B, expect '#' dest at (120,18) i.e. screen rows 18-21 x 51-54), then RESET (counter -> 0, fresh attempt with full map).
REPLAY PREFIX (post-reset, from Turn 40/32 notes, ~38 steps): L,L,D,D,D; sel P1+jump x2 (4 clicks); D,D,D,L,L; R,R,R,D,D,D; capture east c1 over c0 (2 clicks); D,D,D,R,R,R,U,U,U,U,R,R,R,D; capture P3 (2 clicks) -> peg A at (78,24).
EAST ENDGAME (draft, verify B dest first): B down->(120,18) via (120,12)... then chain TBD — C still unsolved; D chain via (96,36) dock + (96,48) purple; A capture via visitor from (90,18) over (84,18) dock; final survivor allowed at (78,30) or (90,54).

## Turn 43 (after A236-238: cart3 Left OK, B select REFUSED, RESET done -> Attempt 2, 0/64)
- Cart3 slid west on rows13-14 wire ✓ (y=12 dock row mobile). B refused selection with cart3 at (120,12) => (120,18) cell DOES NOT EXIST. Right panel cells: (114,18) only in row A; (114,24),(120,24); (114,30 C),(120,30).
- East entry graph (current best): strip (78,18) <-over (84,18) dock-> (90,18); verticals x=90,96 top<->center via y=12 docks; (108,y) docks for row-hops center<->right; (96,36) dock -> connector -> (96,48) purple -> (96,54) -> D. C unstick: needs peg at (114,24) [from (102,24) <- (90,24) hop over (96,24) purple <- ??? entry gap]. FIRST-MOVER PROBLEM UNRESOLVED: no east peg can move first; traveler arrives stuck at (78,24). MISSING LINK suspected — parse wire graph programmatically from logged boards (esp. wire 85-86 extent below row 22; (84,24) dock?).
- ATTEMPT 2 west replay phase 1 written (9): L,L,D,D,D; sel P1 (13,25); jump (25,25); re-sel (25,25); jump (37,25) -> P1 at east c0.

## Turn 44 (after A239-247, 9/64) — EAST SOLVED ON PAPER
Phase 1 replay ✓ (P1 at east c0, P2 at c1, cart2 docked (30,24)).
BREAKTHROUGH: wire 85-86 (screen 16-17 in -69 view) spans rows 15-38 FULL HEIGHT (strip east side), joining rows13-14 and rows37-38 wires. Docks (84,18),(84,24),(84,30) all exist. Same for wires 110-111 and 127-128 (full height).
EAST SOLUTION (56 steps: 32 cart3 arrows + 24 clicks):
cart3 (126,18) -1U 7L 2D-> (84,24); A: (78,24)>E>(90,24); (90,24)>E over(96,24)purple>(102,24);
cart3 -2U 4R 2D-> (108,24); A: (102,24)>E>(114,24); C: (114,30)>N over A CAPTURE>(114,18);
cart3 -2U 1R-> (114,12); C: >N>(114,6); B: (120,6)>W over C CAPTURE>(108,6); B: >W over(102,6)purple>(96,6);
cart3 -3L-> (96,12); B: >S>(96,18); B: >S over(96,24)purple>(96,30);
cart3 -2L 4D 2R-> (96,36); B: >S>(96,42); B: >S over(96,48)purple>(96,54); D: (102,54)>W over B CAPTURE>(90,54) = 1 PEG WIN.
TOTAL PLAN ~94 steps > 64 counter. Lower-bound analysis: perfect solve ~94 => the 64-px counter CANNOT be a hard reset for L5 (else unsolvable). Proceeding; watch behavior when counter hits 64 (~mid west ferry).
Batch (13): D,D,D (cart2 exit), L,L (park south junction), R,R,R,D,D,D (cart1 to dock (30,24)), sel (43,25), dest (31,25) (capture c1-over-c0 into cart1).

## Turn 45 (Attempt 2, counter 22/64)
Phase 2 verified: peg captured into cart1 at screen (30,24). Diffs 28+56 = select+capture. 1 peg on-screen.
Sent ferry: D3 R3 U4 R3 D1 (14 arrows) -> counter 36/64. Cart1 should dock east side; camera scrolls with loaded cart horizontal moves.
Next: recompute P3 capture clicks from fresh board (Attempt1: sel ACTION6(31,25)? was screen=world-36 -> clicks (31,25),(43,25) pattern), then east sequence from Turn 44.

## Turn 46 (Attempt 2 DEAD, counter 36/64)
Ferry trace (6px cart boxes, cells=interior): C1 dock(30,24) D3->(30,42); R,R pushed C2 (36,42)->(48,42) bottom junction; R3 diff 0 (C2 blocked at junction, C1 flush behind); U4: C2 rose vertical x0=48 to (48,18) top junction (C1 mid-wire U-blocked); R: C1->(48,42) junction +scroll, C2->(54,18) bridge; R,R: C1 junction R-blocked, C2->(66,18); D: C2 -> DOCK (66,24). Camera now screen=world-18.
FATAL: subtree {vertical x0=48 y18-42, bridge y0=18 x48-66, dock(66,24)} is a TREE off the bottom junction. C2(purple) at dock leaf, C1 at root: carts cannot reorder on a tree => C1 can NEVER reach dock. P3 (72,24) then uncapturable (jump W over purple-cart lands in purple cart = illegal; no cell (60,24); no mid at (78,24)). Attempt 2 unwinnable => RESET.
ROOT CAUSE: pre-ferry C2 parking at (36,42) EAST of C1 descent col x0=30 on bottom wire. Attempt-2 prefix bug: the 3 Rs (C1 top-wire leg) dragged C2 from south junction (18,42) to (36,42).
FIX (Attempt 3 west, 40 steps): 
 1-5: L,L,D,D,D (C2 -> dock (30,24));
 6-9: sel(13,25),(25,25),sel(25,25),(37,25) (P1 -> east c0 (36,24));
 10-16: D,D,D,L,L,D,D (C2 exit -> (30,42) -> (18,42) -> SPUR (18,54); spur = R-blocked, D-blocked parking);
 17-22: R,R,R,D,D,D (C1 -> dock (30,24); C2 spur-safe);
 23-24: sel(43,25),(31,25) (c1 captures c0 into C1);
 25-38: ferry D3,R3,U4,R3,D1 -> C1 leads (C2 trails harmlessly up main wire during U4) -> C1 DOCKS (66,24);
 39-40: 6 scrolls during ferry => screen=world-36 (=attempt-1 Turn 39 frame): sel (31,25), click (43,25) -> capture P3, peg A lands (78,24).
Then east 56 (Turn 44). Total ~96. Counter-soft bet unchanged.
ACTION7 undo test queued this batch (2 presses pre-RESET, zero risk).

## Turn 47 (Attempt 3, counter 9/64)
ACTION7 UNDO CONFIRMED: reverses 1 move per press, COSTS +1 counter (36->37->38 during test). Net 2 steps per undone move.
RESET + phase 1 replay clean: P1 (36,24), P2 (42,24), C2 docked (30,24), C1 top wire (12,6). Counter 9.
Sent phase 2 (15): D3 (C2 exit), L2, D2 (C2 -> SPUR (18,54) fix), R3 D3 (C1 -> dock (30,24)), sel(43,25) jump(31,25) (capture into C1). Expect counter 24.
Next: ferry D3,R3,U4,R3,D1 (14) -> C1 docks (66,24), 6 scrolls -> screen=world-36; then sel(31,25) click(43,25) captures P3 -> peg A (78,24). Then east 56 (Turn 44).

## Turn 48 (Attempt 3, counter 24/64)
Phase 2 clean: C1 LOADED at dock (30,24), C2 spur (18,54). Capture diffs 28+56.
Sent (16): ferry D3,R3,U4,R3,D1 (C1 leads this time; C2 spur R/D-blocked, Us pull it up main wire harmlessly) -> C1 docks (66,24), 6 loaded-R scrolls -> screen=world-36; then sel(31,25) click(43,25) -> cart peg jumps P3, lands (78,24) = PEG A. Expect counter 40, camera jumps to screen=world-69 after capture (attempt-1 precedent).
Next: verify offset, then east endgame 56 steps (Turn 44 solution): cart3 1U 7L 2D -> (84,24), A east twice, etc. NOTE east arrows also move C1/C2 (harmless, disconnected systems).

## Turn 49 (Attempt 3, counter 40/64) — WEST COMPLETE, EAST BEGINS
Ferry + P3 capture ✓ (capture diff 2174 incl camera jump). Camera: screen = world-69, y unshifted. Board matches Turn-44 map: A(78,24) [screen x 9-12], B(120,6) [51-54], C(114,30) [45-48], D(102,54) [33-36]; purples (102,6),(96,24),(102,30),(96,48); cart3+purple docked (126,18) [G 56-61]; C1 empty at (66,24) west edge.
Sent batch A (14): cart3 U,7L,2D -> dock (84,24); sel A (10,25), dest (22,25) [A->(90,24) over cart3-purple]; sel (22,25), dest (34,25) [A->(102,24) over (96,24) purple]. Counter -> 54.
Remaining east script (screen=world-69 clicks, RE-VERIFY offset after any capture):
 B4: cart3 2U,4R,2D -> (108,24) [8]; sel(34,25) dest(46,25) [A->(114,24)]; sel C (46,31) dest (46,19) [C jumps N over A CAPTURE -> (114,18)]. counter -> 66 (crosses 64!).
 B5: cart3 2U,1R -> (114,12) [3]; sel(46,19) dest(46,7) [C->(114,6)]; sel B (52,7) dest (40,7) [B W over C CAPTURE -> (108,6)]; sel(40,7) dest(28,7) [B over (102,6) purple -> (96,6)].
 B6: cart3 3L -> (96,12); sel(28,7) dest(28,19) [B->(96,18)]; sel(28,19) dest(28,31) [B over (96,24) -> (96,30)].
 B7: cart3 2L,4D,2R -> (96,36) [8]; sel(28,31) dest(28,43) [B->(96,42)]; sel(28,43) dest(28,55) [B over (96,48) -> (96,54)]; sel D (34,55) dest (22,55) [D W over B CAPTURE -> (90,54) = 1 PEG, WIN].

## Turn 50 (Attempt 3, counter 54/64)
Batch A ✓: cart3 dock (84,24) [screen G 14-19], A -> (102,24) [screen 33-36 r24-27]. Jump diffs 44/52, no scrolls, camera still world-69.
Sent B4 (12): cart3 2U,4R,2D -> (108,24); sel A (34,25) dest (46,25) [A -> (114,24) over cart3]; sel C (46,31) dest (46,19) [C jumps N over A CAPTURE -> (114,18)]. Counter crosses 64 at the click phase -> 66. WATCH: hard-reset vs soft. If soft: verify offset post-capture, continue B5-B7 from Turn 49 script.

## Turn 51 (Attempt 3) — COUNTER IS SOFT, COUNTS DOWN PAST 64
B4 ✓: A -> (114,24), C captured A -> (114,18). NO RESET at 64: counter hit 64 then DECREMENTS per action (64->63->62); row0 now shows ## + 62x 8 (weird render, no $). Level alive, Score 4, 3 pegs: B(120,6), C(114,18), D(102,54). Cart3 docked (108,24). East captures do NOT scroll camera (C-over-A kept world-69).
Sent B5+B6 (16): cart3 2U,1R -> (114,12); C (46,19)->(46,7) [-> (114,6)]; B (52,7)->(40,7) [W over C CAPTURE -> (108,6)]; B (40,7)->(28,7) [over (102,6) purple -> (96,6)]; cart3 3L -> (96,12); B (28,7)->(28,19) [-> (96,18)]; B (28,19)->(28,31) [over (96,24) purple -> (96,30)].
Next (B7, 14): cart3 2L,4D,2R -> (96,36); B (28,31)->(28,43) [-> (96,42)]; B (28,43)->(28,55) [over (96,48) -> (96,54)]; D (34,55)->(22,55) [W over B CAPTURE -> (90,54)] = 1 PEG WIN.

## Turn 52 (Attempt 3) — FINAL BATCH SENT
B5+B6 ✓ flawless: C->(114,6), B captured C ->(108,6), B over purple ->(96,6), cart3 ->(96,12), B ->(96,18)->(96,30). 2 pegs: B(96,30), D(102,54). Cart3 (96,12).
Sent B7 (14): cart3 2L,4D,2R -> (96,36) [via wire 85-86 full-height + rows37-38 wire]; B (28,31)->(28,43) [->(96,42)]; B (28,43)->(28,55) [over (96,48) purple ->(96,54)]; D (34,55)->(22,55) [W over B CAPTURE ->(90,54)] = 1 PEG => expect Score 5, LEVEL 5 CLEAR (~Action 373).
If score bumps: L6 starts — parse fresh board, small probe batches.

# LEVEL 6 (started Action 374, Score 5)
Initial board (screen=world assumed, counter 64 fresh):
- Panel: rows 10-53 walls col 10 / col 35 (upper) & col 47 (lower, widens at row 34). Upper cells x0=12,18,24,30 x y0=12,18,24,30; lower cells x0=12..42 x y0=36,42,48; pocket cell (24,54) rows 53-59.
- PEGS: P1 (18,24), P2 (12,48), P3 (24,54). RED 'n' block at (18,18) — NEW ELEMENT, unknown semantics.
- Carts: TWO empty (orange interior) side-by-side on east wire, boxes cols 47-52 & 53-58 rows 41-46; cart A interior = virtual cell (48,42) docked flush east of (42,42). Wire rows 43-44 continues EAST off-screen (world extends east).
- Only candidate first move: P1 N over red -> (18,12) IF red is jumpable.
Turn 53 probe (2): click red (19,19) — selectable?; click P1 (19,25) — dest diamonds reveal red mechanics.

## Turn 54 (L6, 2/64 used)
RED MECHANICS probe: red (18,18) IS selectable, shows jump dest (18,30) S over P1 = red can JUMP over pegs. P1 select shows dest (18,12) N over red = pegs can jump over red. Both mobile.
Sent (1): ACTION6(19,13) — P1 (currently selected) jumps N over red -> (18,12). KEY QUESTION: does red get captured (removed) like a peg, or persist like purple?

## Turn 55 (L6, 3/64)
P1 jumped over red -> (18,12), diff 44 NO CAPTURE: red persists = mobile springboard. Red itself jumps over PEGS (capture? testing now).
Capture geometry findings: P2 (12,48) UNCAPTURABLE in place (no landing cells beyond); P3 (24,54) pocket likewise. Both must be EXTRACTED via red trampoline: red at (12,42)/(18,48) frees P2; red at (24,48) frees P3 (hops N to (24,42)).
Sent (4): P1 back S over red -> (18,24) [sel (19,13), dest (19,25)]; then RED S over P1 -> (18,30) [sel (19,19), dest (19,31)]. WATCH: does P1 survive red hop? (critical for all routing).

## Turn 56 (L6, 7/64) — FULL SOLUTION SENT
Red hop over peg: NO capture (P1 survived). Capture rule: only peg-over-peg.
State: P1 (18,24), red (18,30), P2 (12,48), P3 (24,54).
Solution (10 clicks): P1 S over red ->(18,36); red S over P1 ->(18,42); P1 S over red ->(18,48); P2 E over P1 CAPTURE ->(24,48); P3 N over P2 CAPTURE ->(24,42). Leaves P3 alone at (24,42) + red (18,42). Expect Score 6 at ~17/64 IF no pegs exist east (wire off-screen — L5 lesson). If no score bump: explore east via carts.

## Turn 57 (L6, 17/64) — NO CLEAR at 1 visible peg; EAST WORLD EXISTS
Solution executed ✓ (both captures) but Score still 5 => pegs off-screen east. State: P3 (24,42), red (18,42), carts A (48,42 dock) + B east of it, wire rows 43-44 heads east.
Sent (14): leapfrog east on row y0=42 — red E over P3 ->(30,42); P3 E ->(36,42); red E ->(42,42); P3 E ->(48,42) INTO CART A; then 6x Right (cart A ferries peg east, camera scrolls 6/press -> screen=world-36; cart B pushed ahead). Next: parse east world, locate remaining pegs.

## Turn 58 (L6, 31/64) — EAST REGION MAPPED
Leapfrog + cart entry ✓ (entry diff 1868 = camera jump 20px on peg entering cart; then 6R scrolls). Camera offset ~56 (screen+56=world approx; work in screen).
EAST (screen): panel rows 10-29, wall col 32; cells x0=34,40,46,52 at y0=12,18(,24 partial); PEG P4 (40,18); PURPLES (34,24),(52,24) with walls below; y0=18 band EXTENDS EAST off-screen (row 17-22 open to col 63). Garage box below (cols 26-40, rows 40-47) holds cart A (peg, slot 27-32) + cart B (33-38, junction slot). LEFT vertical wire (cols 35-36) garage->panel bottom = dock (34,30) under purple (34,24). East wire rows 43-44 -> RIGHT vertical (cols 53-54) -> dock (52,30) under purple (52,24).
Sent (8): R (cart B out east, cart A -> junction slot), U,U,U (cart A -> top dock (34,30)); sel cart peg (35,31), dest (35,19) [N over purple -> (34,18)]; sel (35,19), dest (47,19) [E over P4 CAPTURE -> (46,18)].
Next: check further-east pegs via band y0=18; right vertical dock (52,30) route available.

## Turn 59 (L6, 39/64)
Cart ride ✓ but camera scrolled +6 during the R (peg-cart horizontal) => my 4 clicks all REFUSED (0 diff, wrong coords — LESSON: recompute clicks after ANY peg-cart horizontal move). 
Now (screen, offset +6 vs turn 58): cart A docked (28,30) interior rows 30-33; purple above (28,24); P4 (34,18); purple2 (46,24); right vertical wire cols 48-49 -> dock (46,30); cart B on east wire (34-39, rows 41-46); FAR-EAST structure at screen 62-63 rows 41-46 ('O$' = wall+cells, panel at wire level).
Sent (4): sel (29,31), dest (29,19) [peg N over purple -> (28,18)]; sel (29,19), dest (41,19) [E over P4 CAPTURE -> (40,18)]. If score->6 WIN; else scout east (peg must re-enter a cart for camera-follow).

## Turn 60 (L6, 43/64) — FINAL-PEG MERGE MECHANIC + GOAL PAD
The (28,18)-over-P4 jump: BOTH pegs vanished, GRAY peg-shaped piece ('#' 12px) formed at landing (40,18), AND a goal pad appeared at screen cols 2-12 rows 51-63 (concentric purple rings, white 2x2 center ~cell (6,54)), far southwest below the wire. Score still 5.
HYPOTHESIS: last capture (2 pegs -> 1) turns survivor GRAY; win = deliver gray to goal pad.
PROBLEM: gray at (40,18) has NO adjacent mids (P4 gone, purples at (28,24)/(46,24) not adjacent) — if gray moves by jumping, it is STUCK => would need RESET+replay arranging final merge at (28,18) (which can hop S over purple into cart A dock (28,30) and ride).
RED is now permanently immobile (no pegs to hop) at west (18,42) — irrelevant?
Sent probe (1): select gray (41,19) — does it show dests (walk? jump?) or refuse?

## Turn 61 (L6, 44/64) — RESET + REPLAY v2
Gray select REFUSED (0 diff) = no legal moves (stuck at (40,18), no adjacent mids). Attempt 1 dead.
REPLAY v2 (merge staged next to RED, then red-gray leapfrog into cart):
 After RESET (clicks at fresh camera screen=world):
 a. red S over P1 -> (18,30); b. P1 S over red -> (18,36); c. red S -> (18,42); d. P1 S -> (18,48);
 e. P2 E over P1 CAPTURE -> (24,48) [3->2 pegs, normal]; f. P3 N over P2 MERGE -> GRAY at (24,42).
 Then: red (18,42) E over gray -> (30,42); gray E over red -> (36,42); red E over gray -> (42,42); gray E over red -> (48,42) = INTO CART A [8 clicks, UNTESTED: red-over-gray & gray-over-red].
 Then: cart B out of the way, drive cart A (gray) east/park above GOAL PAD (world x ~50-74, south of main wire, ring purple y0=48, center y0=54); gray jumps S over ring -> CENTER = expected WIN.
 Camera: gray-cart horizontal moves will scroll (recompute clicks fresh).
Sent (14): ACTION2 (arrow-vs-gray probe), RESET, clicks a-f. Expect gray at (24,42), 12/64 used.

## Turn 62 (L6 attempt 2, 12/64) — CORRECTED UNDERSTANDING + GRAND PLAN
f was NORMAL capture (world pegs were 4: P1,P2,P3,P4east; f made 3->2). MERGE fires only on 2->1. Current: S GREEN (24,42), red (18,42), carts A(48,42) B(54,42), P4 east at E2. 12/64.
Goal pad world x0~66 (screen 2-12 at offset +62 in attempt 1), south of main wire between west garage (world 47-59) and east region (world 88+). Ring purple y0~48, center y0~54, 2px-wide render (mini-scale; delivery mechanism TBD on arrival).
GRAND PLAN:
 P1 leapfrog: red->(30,42), S->(36,42), red->(42,42), S->(48,42) INTO CART A [8 clicks, THIS BATCH]; camera may jump +20 on entry.
 P2: red E over loaded cart A -> INTO CART B (54,42) [2 clicks, UNTESTED mechanic].
 P3: R x7 (B leads east; 6R->A slot1+B junction; 7th->B out, A junction) then U x2-3 (A -> left dock Ld under Lp) then R x2, U x3 (B -> right dock Rd under Rp (46,24)e).
 P4: red: Rd hop N over Rp -> E4 (46,18). S: Ld hop N over Lp -> E1 (28,18).
 P5: S E over P4(E2) -> MERGE gray at E3 (40,18) + pad reveal; red E4 W over gray -> E2; gray E3 W over red -> E1; gray S over Lp -> CART A at Ld.
 P6: D x2, L x4+ — drive gray west to world x0=66 above pad (scrolls -6 each L; recompute), deliver (S-jump over ring or D-spur; observe).
Cart-entry camera jumps + capture reveals => verify screen coords EVERY turn before clicks.

## Turn 63 (L6a2, 20/64)
Leapfrog + S into cart A ✓ (camera +20, screen=world-20). Red at screen (22,42)=world (42,42). Carts: A(S) world (48,42), B world (54,42).
Sent (9): sel red (23,43), dest (35,43) [red E over loaded A -> INTO CART B, world (54,42)]; then R x7 (drive both east: 6R -> A slot1/B junction of east garage, 7th -> B out east, A junction slot). Camera follows A (S) — scrolls with each R.
Next: U x2-3 (A -> Ld), R x2 U x3 (B -> Rd), then panel entries.

## Turn 64 (L6a2, 29/64) — BIG CHOREOGRAPHY BATCH
Red in cart B ✓; 7R done: A(S) garage slot1 (screen 27-32) under LEFT vertical (cols 29-30 rise from slot1!), B(red) slot2 (33-38). Right vertical cols 48-49. Camera screen offsets stable now (no horizontal peg-cart moves until delivery drive).
Sent (19): U,U [A -> Ld dock (28,30)s]; R,R [B -> under right vertical (45-50)]; U,U,U [B -> Rd (46,30)s];
 sel (29,31) dest (29,19) [S: Ld hop N over Lp -> E1 (28,18)s];
 sel (47,31) dest (47,19) [red: Rd hop N over Rp -> E4 (46,18)s];
 sel (29,19) dest (41,19) [S E over P4 -> MERGE GRAY at E3 (40,18)s + pad reveal];
 sel (47,19) dest (35,19) [red W over gray -> E2];
 sel (41,19) dest (29,19) [gray W over red -> E1];
 sel (29,19) dest (29,31) [gray S over Lp -> INTO CART A at Ld].
Counter -> 48. Next: D x2 (A down to garage), L x4-5 (drive west, scrolls -6 each), deliver gray into goal pad (world x0~66, center y0~54) — observe pad structure fresh before final clicks.

## Turn 65 (after A467, 48/64 used, L6 attempt 2)
- 19-action choreography fully executed. Final state: survivor S is GREEN (not gray) inside cart A at Ld dock (screen 28,30 area, rows 30-33 GIIIIG). Red 'n' parked at E2 (34,18). P4 captured. Score still 5.
- CRITICAL: NO goal pad anywhere (rows 51-63 empty). Attempt-1's gray figure + purple-ring pad did NOT reproduce despite identical final capture. Revised theory: gray = stuck-piece rendering (attempt-1 S had zero legal moves at E3); pad reveal trigger unknown, possibly tied to stuck state or position.
- Win condition still unknown at 1 peg. Camera offset +62.
- Next batch queued: D,D (cart A Ld->garage slot1), L,L,L,L (west along main wire). Expect 4 camera scrolls of -6 each -> offset ~+38. Target: cart interior world x0~66, above attempt-1 pad location (world x 64-74, rows 51-63). RECOMPUTE all screen coords after scrolls before any click.
- Fallback if nothing at x~66: far-east 'O' structure (world ~124+, rows 41-59, seen at screen 62-63 when offset +62).

## Turn 66 (after A473, 54/64 used, L6 attempt 2)
MAJOR MECHANICS DISCOVERY (from L2 history, boards 24-28):
- GRAY pegs = pieces with no legal moves (stuck). When ALL pieces stuck, every peg renders gray '#' and the purple FLOWER spawns at screen x2-11 rows 51-63 (world fixed? appeared same screen spot in L2 and L6-attempt1).
- The flower is a SOFT-RESET BUTTON: in L2, clicking its white center (6,55) respawned all pegs (diff 182, pegs 0->5). It is NOT a goal.
- L6 attempt1 vs attempt2 final capture: identical jump E1-over-E2->E3. Attempt1: red was isolated -> everything stuck -> gray + flower. Attempt2: red at E4 adjacent -> red had a move -> no flower, S green.
- L6 initial state (board 374, offset 0): 3 green pegs + 1 red, west panel 4 cols, diamond seen = dest marker of selected red (not a goal marker). Dest diamonds appear at ALL legal landings of selection incl. carts; they clear after the move.
- CONCLUSION: reducing to 1 green does NOT clear L6. Likely more pegs/goal in FAR-EAST structure (world 124+, rows 40-59, white panel behind O wall) never yet seen inside.
- East corridor: narrow band rows 16-23 (cells rows 18-21) extends east of east-panel wall (world 113): cells E5 (114-117), E6 (120-123), continues past world 125. Second corridor wall row 23. Corridor may lead over/into far-east structure.
- Click limit: dest clicks need screen<=63 = world<=offset+63. At offset +62 max reach: S to E5, red to E6, then stuck. Need offset>+62 => peg-cart must drive east past Ld junction.
- Current: A(with S) x0~66 world on wire (screen 28-33 rows 41-46, offset +38), B empty at ~83 (17px ahead east), red at E2, counter 54/64 (soft).
- Cart alignment facts: R*4 from current = both carts under their dock verticals (reverse of D,D,L*4); U,U redocks A at Ld, B at Rd. A stays on wire & reversible for extra R presses (L*k undoes). B behavior past its junction unknown (may turn up right vertical or stop at wire end ~110).
- SENT: R*6. Expect offset ~ +74 (if A unblocked to x0 102), revealing far-east structure interior (world up to ~137). Watch B's stop position. Recovery to dock: L*2, U, U.

## Turn 67 (after A479, 60/64 used, L6 attempt 2)
R*6 executed: offset now +74 (east panel west wall at screen 14). REVEALS:
- 2nd GREEN PEG in far-east structure: world (126-129, rows 48-51), in a 1-wide vertical column: empty cell (126-129,42-45) above, peg (48-51), empty cell (54-57) below. Pegs now 2 total (S + far peg). This is why 1-green didn't clear!
- Far-east complex: west wall world 124; wide band rows 41-46 with cells (126-129,42-45),(132-135,42-45), white surface continues east past 137; connector column at world 136+ rows 29-39 (only 1px visible); corridor rows 17-22 cells: E5(114-117),E6(120-123),E7(126-129),E8(132-135), continues east.
- Carts: A(with S) at world 102-107 + B at 108-113, ADJACENT, enclosed in east garage (world 101-114, walls rows 40/47, east wall 114). B stopped exactly under right vertical (110-111) = still dock-aligned. A is NOT aligned (left vert 91-92).
- Desync trick: U presses move B up the right vertical while A no-ops. Then R moves A to 108 (wire end) -> camera offset +80 (screen 63 = world 143).
- Restore path for A: L*3 (108->90) then U,U docks A at Ld. B stays parked right side (off wire) - actually GOOD (frees the wire).
- Capture plan for far peg: jumper must reach cell (126-129,42-45) and jump down over peg -> lands (54-57). Reaching that cell likely requires: corridor east to E9(138-141?), descend connector (hopefully purple springboards), enter band, west-leapfrog with red. Corner turns need static mids - check for purples in reveal.
- CLICK LIMIT crunch: S walking in panel caps at world<=offset+63; offset drops to +62 when S redocks/exits at Ld. May need to test whether walking pegs near screen edge auto-scrolls camera (never tested).
- SENT: U,U,R (B climbs to Rd, A to wire end, offset +80). Pure reveal probe, reversible.

## Turn 68 (after A482, 63/64 used, L6 attempt 2, offset +80)
Desync WORKED: B docked at Rd (108-113, rows 29-34), A with S at wire-end (108-113, rows 42-45), offset +80 (max possible; screen63=world143).
- PEG3 revealed at (138-141, rows 36-39): 3 greens total (S, peg2@126 rows48-51, peg3@138 rows36-39). L6 = capture both far pegs.
- Band rows 42-45 cells: c1(126-129), c2(132-135), c3(138-141). Peg3 column: empty cell (138,30-33) above peg3, peg3 (36-39), c3 below. Peg2 column: c1 above, peg2 (48-51), cell (54-57) below.
- Connector at world 143+: corridor bottom wall opens at 143 (rows 24-27 white at 143, wall at 142). Structures at 144+ INVISIBLE & UNCLICKABLE at offset +80 (cart-camera max). Likely cells/purples or even a second dock+cart there.
- Captures needed: X at (138,30-33) jumps down over peg3 -> c3. Y at c1 jumps down over peg2 -> (54-57). Entry to those cells unresolved (depends on 143+ structure).
- ONLY viable path: test AUTO-SCROLL on walking pegs near screen edge.
- Piece-stuck note: S in cart + red isolated did NOT trigger gray/flower -> cart-riding pegs count as mobile.
- SENT (13): L*3 (A to Ld-align x0=90, camera back to +62; B stays at Rd), U*2 (A docks Ld), then clicks: (30,31)->(29,19) S exits cart over Lp to E1; (29,19)->(41,19) S over red to E3; (35,19)->(47,19) red over S to E4; (41,19)->(53,19) S over red to E5. All coords proven at +62 except (53,19). STOPPED before red->E6 in case auto-scroll shifts coords mid-batch.
- Next: check if camera followed S/red eastward. If yes: continue leapfrog to E9+ and investigate 143+. If no: consider undo/RESET or other camera tricks.

## Turn 69 (after A495, L6 attempt 2) - FULL SOLUTION DERIVED
Camera AUTO-JUMPED to offset +105 when S landed E5 (diff 1625). Everything east now visible AND clickable.
EAST MAP (world x of 4px block, row bands; offset +105: screen = world-105):
- Corridor rows 18-21: red@107(E4), S@113(E5), empty E6@119,E7@125,E8@131,E9@137,E10@143,E11@149, CART C (empty, docked in corridor slot)@154-159 interior 155-158, E12@161.
- Rows 24-27: Rp@~108, PURPLE2@143-146 (under E10), PEG4@161 (under E12).
- Rows 30-33: cells @137, @149, @161. Vertical wire V1@145-146 (rows ~30-43), V2@156-157 (rows 24-43, cart C's dock wire).
- Rows 36-39: PEG3@137. Rows 42-45: band c1@125,c2@131,c3@137; east wire rows 43-44 world 145-158 connecting V1/V2.
- Rows 48-51: PEG2@125. Rows 54-57: pocket@125.
- 4 greens: S + peg2 + peg3 + peg4. Win = capture all 3 far pegs (reduce to 1).
KEY MECHANICS: red jumps over greens WITHOUT capturing; loaded carts = valid mids; pegs exit carts by jumping over adjacent pieces; carts stopped mid-vertical act as cells at that height; camera auto-scrolls on peg moves near screen edge (1625 diff).
SOLUTION SEQUENCE:
1. Leapfrog: red->E6, S->E7, red->E8, S->E9, red->E10, S->E11, red->CART C (lands in cart, corridor slot). [SENT THIS TURN: 14 clicks (3,19)(15,19)(9,19)(21,19)(15,19)(27,19)(21,19)(33,19)(27,19)(39,19)(33,19)(45,19)(39,19)(51,19)]
2. S@E11 over loaded cart -> E12: (45,19),(57,19). S@E12 down over peg4 -> (161,30): (57,19),(57,31). CAPTURE PEG4.
3. Arrows D,D: cart C (red) -> (155,30). S (161,30) W over cart -> (149,30): (57,31),(45,31).
4. Arrows D,D,L,L,U,U: cart C -> V1 top (143,30). S W over cart -> (137,30): (45,31),(33,31).
5. S down over peg3 -> c3: (33,31),(33,43). CAPTURE PEG3.
6. Arrows D,D: cart C -> V1 bottom (143,42-45), adjacent east of S@c3.
7. Red exits cart W over S -> c2: sel cart (39,43)?? verify, dest (27,43).
8. S@c3 over red -> c1: (33,43),(21,43).
9. S@c1 down over peg2 -> pocket: (21,43),(21,55). CAPTURE PEG2 -> 1 green -> WIN.
CAUTIONS: verify camera offset EVERY turn before clicks (auto-scroll may shift +/-); red-boarding-cart may trigger camera jump (batch stopped before step 2); arrows also move west carts A/B - harmless (disconnected); counter soft.

## Turn 70 (after A509, L6)
Phase 1 leapfrog COMPLETE: S@E11(149), red inside cart C (corridor slot), camera stable +105. All 14 clicks landed (28/44,36/52 pairs).
SENT (8): (45,19)(57,19) S over loaded cart -> E12; (57,19)(57,31) S down over PEG4 -> (161,30) CAPTURE; D,D cart C w/ red -> (155,~30); (57,31)(45,31) S west over loaded cart -> (149,30).
Risks: E12 landing near right edge could auto-scroll (level likely ends ~world 168, so probably not); cart height after D,D may be off (jump refused = harmless, adjust).
Remaining: D,D,L,L,U,U -> cart to V1 top (143,30); S->(137,30): (45,31)(33,31); S down over peg3 -> c3: (33,31)(33,43); D,D cart -> V1 bottom; red exits W over S -> c2: sel cart (39,43) dest (27,43); S over red -> c1: (33,43)(21,43); S down over peg2 -> pocket: (21,43)(21,55). WIN expected.

## Turn 71 (after A517, L6)
Phase 2+3 PERFECT: peg4 captured (S went E12 -> down over peg4 -> (161,30)); cart C w/red descended to (155,30); S shuttled west to (149,30). Pegs=3 (S, peg2, peg3). Camera stable +105.
SENT (18) - full finish: D,D (cart to east wire), L,L (west to V1), U,U (up to V1 top 143,30); (45,31)(33,31) S west over cart -> (137,30); (33,31)(33,43) S down over PEG3 -> c3 CAPTURE; D,D (cart to V1 bottom 143,42-45); (39,43)(27,43) red exits cart west over S -> c2; (33,43)(21,43) S over red -> c1; (21,43)(21,55) S down over PEG2 -> pocket CAPTURE -> 1 green -> expect Score 6 / L7.
If cart misaligned after L,L the U's no-op and later clicks fizzle - diagnose from diffs next turn.

## Turn 72 - LEVEL 6 CLEARED (Score 6, Action 535, diff 2094)
Full 18-action finisher executed perfectly: cart shuttle -> S(137,30) -> peg3 capture c3 -> cart V1 bottom -> red exit c2 -> S c1 -> peg2 capture pocket. The derived loaded-cart-as-moving-mid solution worked exactly as planned.

## LEVEL 7 initial (board 535, counter 0, offset unknown/fresh):
- Top-left box (screens 4-12, rows 10-23): GREEN peg (12-15) above purple (17-20), passage below to dock on wire rows 25-26 (dock posts 'OO' screens 7-8 row 24).
- Top-right box (screens 40-48): RED above purple, same dock structure (posts screens 42-43).
- Top wire rows 25-26 (screens 7-45). Vertical screens 25-26 (rows 27-36) down to mid wire rows 37-38 (screens 13-44). CART (empty) at screens 35-42 rows 34-41 (body 36-41) on mid wire.
- More verticals: screens 13-14 (rows 39-46), 42-43 (rows 39-45), 56-57 (rows 37-49), 60-61 right edge (rows 25-49?), wires rows 49-50 right.
- Bottom-left purple boxes rows 46-51 (screens 10-18, 40-48) above openings into bottom PANEL rows 52-59: band cells rows 54-57 with EMBEDDED purples: cells at screens 12-15, P@18-21, cell 24-27, P@30-33, cells 36-39,42-45,48-51,54-57,60-63... extends EAST off-screen.
- 1 green + 1 red visible; more content likely east (like L6).
SENT: sel green (8,13), sel red (44,13) - read dest diamonds for both to map legal moves.

## Turn 73 (L7, counter 2)
Both sel probes REFUSED (diff 0): green and red have NO moves until a cart docks under their purple. Confirms L7 opening = cart logistics first.
Cart body at x0=36 (screens 36-41, rows 35-40) on mid wire rows 37-38 (spans 13-44). Vertical to top wire at screens 25-26 (alignment x0=23 or 24; only 24 reachable: 36-6k). Top wire rows 25-26 spans 7-45; left dock under green box at x0~5-6; right dock under red box at x0~41-42.
SENT (9): L,L (x0 36->24), U,U (climb to top wire, body rows 23-28), L,L,L (west to x0=6, left dock), then sel green (8,13) + dest cart (8,26) = green hops purple into cart.
If U misaligned (x0 24 vs 23): U no-ops, L*3 slides west on mid wire, clicks fizzle - recover next turn.

## Turn 74 (L7, counter 11)
Green boarded cart at left dock (cart rows 23-28, screens 5-10, on top wire west end). Camera offset 0 (clamped, cart x0<28). Sel probes earlier confirmed: purple hops need docked cart below.
Hypothesis: bottom-left purple mini-boxes (screens 10-18 & 40-48, rows 46-51) are hop-DOWN portals into the bottom band (cells rows 54-57). Wire vertical at screens 13-14 (rows 39-46) leads to a dock at the left mini-box.
SENT (11): R*3 (x0 5->23, align vertical 25-26), D,D (to mid wire), L*2 (x0 23->11, align vertical 13-14), D,D (down to mini-box dock ~rows 43-48), sel peg in cart (14,45), dest band cell (13,55) = green hops down into bottom band.
No camera movement expected (x0 always <=28 => offset clamped 0). If dock height off, clicks fizzle - adjust next turn.

## Turn 75 (L7, counter 22)
Green dropped into bottom band cell (screens 12-15, rows 54-57). Cart empty at left mini-box dock (x0=11, rows 40-46). One D was refused (dock reached at 1 D) - dock heights: mini-box dock rows 40-46.
Band layout rows 54-57: green@12-15, P@18-21, cell@24-27, P@30-33, cells@36-39,42-45,48-51,54-57,60-63+ (east off-screen).
Green solo reach: over P -> 24-27, over P -> 36-39, then STUCK (plain cells). Need red in band as leapfrog partner (like L6 corridor).
SENT (11): U,U (cart up to mid wire), R,R (x0 11->23, vertical 25-26), U,U (top wire), R,R,R (x0 23->41, right dock under red box), sel red (44,13), dest cart (44,26). Red boards.
Next: ferry red down: L*3, D,D, R*3 (x0 23->41, vertical 42-43), D (right mini-box dock), sel red (44,43)?, dest band (43,55). Then leapfrog east.

## Turn 76 (Action ~569)
- Batch verified: 9 arrows (2nd U refused, diff 0, harmless), red boarded cart at mid-wire east dock via (44,13)+(44,26). Cart+red at x41-46 rows 23-28. Camera offset 0. Green in band cell x12-15 rows 54-57.
- Map re-confirmed: mid wire rows 25-26 (x7-41); vertical x25-26 rows 27-36 to lower wire rows 37-38 (x13-45); verticals x13-14 & x43-44 down to mini-box docks (row 46); mini-box purples rows 47-50; band rows 53-58 with cells: green@12-15, P@18-21, 24-27, P@30-33, 36-39, 42-45, 48-51, 54-57, 60-63+. East verticals x56-57 & x62-63 lead to off-screen content.
- Queued: L,L,L (x0 41->23), D,D (to lower wire), R,R,R (x0 23->41), D (right mini-box dock rows 41-46), sel red (44,43), dest band (43,55). Red drops into band cell 42-45.
- Next: leapfrog green+red east. Green solo path: hop over P@18-21 -> 24-27, over P@30-33 -> 36-39. Then red@42-45 is mid: green 36-39 over red -> 48-51? No: jump lands 2 cells away; green@36-39 jumps over red@42-45 -> lands 48-51. Then red over green -> 54-57, etc. Watch camera auto-jump near east edge (walking pegs near screen edge trigger it, diff ~1625) — stop batch before green/red reach screen x>55.

## Turn 77 (Action ~580)
- Ferry complete: red in band cell x42-45 rows 54-57 (diffs 28+44 on drop). Cart empty at right mini-box dock x41-46 rows 41-46. Green still x12-15. Camera offset 0.
- Queued 8 clicks (4 jumps): green 13,55->25,55 (over P@18-21); ->37,55 (over P@30-33); green over red ->49,55; red over green 43,55->55,55. Stopped there: red landing x54-57 near screen edge, camera auto-jump possible (L6 diff 1625). Verify camera before next jumps.
- Continuation if camera holds: green@48-51 over red@54-57 -> 60-63 (sel 49,55 dest 61,55), then red over green eastward off current screen — camera must jump by then. Recompute coords from new offset each time.

## Turn 78 (Action ~588) — CAMERA JUMPED, offset now 44
- Leapfrog batch worked (diffs 36/52 x3), then red's jump to world 54-57 triggered camera auto-jump (diff 1766). Offset = 44 (green world 48-51 @ screen 4-7; red world 54-57 @ screen 10-13).
- EAST MAP (world coords, offset 44): band ends with cell 60-63 (rows 54-57), wall at 64-65. Cart dock at world 65-68 rows 55-56 (vertical 67-68 rows 49-54 from wire 49-50). East mini-box world 71-78: dock row 46, purple 72-75 rows 47-50, band cell 72-75 rows 54-57. Upper strip rows 22-28: wire row 22 world 76-95, cart E (empty) at world 77-82 rows 23-28, purple 84-87 rows 24-27, cell 90-93 rows 24-27. East grid: column cells world 90-93 at rows 24-27/30-33/36-39/42-45; rows 36-39 & 42-45 rows have cells 90-93, purple 96-99, cell 102-105 continuing east off-screen. Top frame world 73-92 rows 14-21 (verticals 73-74, 91-92 rows 15-21). More wires off east (rows 19-20 world 103-107, row 34 world 95-107).
- EAST CART NETWORK (separate from west network — wire 37-38 east segment is world 55-74, gap from west's 13-45): wire 25-26 (61-76), wire 22 (76-95), wire 37-38 (55-74), wire 49-50 (55-68), wire 14 (73-92); verticals: 61-62 (rows 27-36), 55-56 (rows 39-50), 67-68 (rows 49-55, dock at bottom), 73-74 down (rows 39-45 to mini-box dock), 73-74 up (rows 15-21), 91-92 (rows 15-21). Cart x0 = vertical_x0 - 2. West cart W is STUCK on west network (fine, empty, parked).
- PLAN: 1) green over red -> 60-63; 2) red over green -> INTO empty cart E parked at 65-70 (interior 66-69, needs rows 54-57 alignment — VERIFY cart rest rows first); 3) green over red-loaded cart -> east band cell 72-75; 4) green up over mini-box purple into cart at east dock; 5) ferry both pegs to upper strip (dock x0=77), jump east over purple 84-87 into grid 90-93; 6) leapfrog east grid.
- Queued: cart E route L3(77->59),D2(->wire37),L(->53),D2(->wire49),R2(->65),D2(->dock 65-70); then green jump sel(5,55) dest(17,55) -> world 60-63. Cart W refused all (no U in batch). Verify cart E rest rows before red's boarding jump.

## Turn 79 (Action ~602)
- Cart E rest position CONFIRMED: world 65-70, rows 53-58, interior 54-57 = band-aligned. Green jumped to 60-63 (screen 16-19). Red at 54-57 (screen 10-13). Camera offset still 44.
- Queued: red over green into cart — sel (11,55), dest (23,55). Stopped there: peg-boarding may snap camera (L6 precedent), which would invalidate green's follow-up click coords.
- Next: green over red-loaded cart -> east band cell 72-75 (at offset 44: sel (17,55), dest (29,55) — recompute if camera moved). Then cart E must LEAVE dock (red inside... wait red must exit first? No: green passes OVER the loaded cart; then red-loaded cart drives to east strip via U,R? routes; green climbs mini-box via cart... REVISIT: after green at 72-75, cart E (red aboard) drives U,L,L,U,U,R,U,U,R,R,R to strip dock x0=77 rows 23-28; red jumps east over purple 84-87 -> grid cell 90-93 rows 24-27; cart E returns empty to east mini-box dock (world 71-76 rows 41-46); green jumps up over purple 72-75 -> cart; ferry green to strip; green jumps over purple into grid... but needs mid — red should wait at 90-93? green in cart at dock 77-82, purple 84-87 occupied? purple IS the mid (box purples work as mids). Both pegs land in grid column 90-93 sequentially: red exits to 90-93 rows 24-27, then must vacate for green: red needs a mid to move down the column — green arrives at 90-93 only after red moves. Column cells: 24-27/30-33/36-39/42-45. Red at 24-27 can't move alone. PROBLEM: order matters — think next turn.

## Turn 80 (Action ~604)
- Red boarded cart E (diffs 28+44): red now cart interior world 66-69 rows 54-57. NO camera snap (offset 44 held). Green at 60-63.
- Queued 15: green vault sel(17,55) dest(29,55) -> 72-75; red-cart route U,L,L,U,U,R,U,U,R,R,R (65->77 strip dock, rows 23-28); red exit sel(35,25) dest(47,25) over purple 84-87 -> grid cell 90-93 rows 24-27.
- Cart W side effect: U pulls it to west wire 37-38, L,L to x0=29, ends rows 35-40 x0=35..41ish — harmless, west done.
- Next: cart E (empty) returns: L,L,L (77->59), D,D (wire 37-38), R,R (59->71), D,D (vertical 73-74 -> mini-box dock rows 41-46); green@72-75 jumps UP over purple into cart (sel ~(29,55) dest ~(29,43)); then green-cart (camera follows green carts? watch) to top frame: U at x0=71? vertical 73-74 rows 15-21 — test U from wire 25-26 at x0=71; if connected: U,U to wire 14, R,R,R (71->89), D,D (vertical 91-92, park interior rows ~18-21 above red@90-93); green jumps down over red -> cell 30-33; red down over green -> 36-39; green down over red? (30-33 over 36-39 -> 42-45); then leapfrog EAST: red 36-39 over purple 96-99 -> 102-105; green 42-45 over purple -> 102-105(row42); continue east off-screen.

## Turn 81 (Action ~619)
- Full 15-batch success: green@72-75 (band cell, screen 28-31 r54-57), red@grid cell 90-93 r24-27 (screen 46-49), cart E empty at strip dock 77-82 r23-28, cart W harmlessly at west x0=41 r35-40. Offset 44.
- Vertical 73-74 spans rows 15-26 (connects wire 13-14 world 73-92 to wire 25-26). Vertical 91-92 rows 15-21 connects wire 13-14 to wire 22. Strip purple box HANGS from wire 22 at 83-88 (cart can't slide past; top-frame detour required).
- Queued 11: cart L3 (77->59), D2 (wire 37-38), R2 (59->71), D2 (vertical 73-74 rows 39-45 -> mini-box dock 71-76 r41-46), green board: sel(29,55) dest(29,43).
- Next: green-cart drive U,U (wire 37-38), L,L (71->59), U,U (wire 25-26), R,R (59->71)? NO WAIT: vertical 73-74 lower segment is rows 39-45 (dock branch); upper segment rows 15-26 from wire 25-26. From dock: U,U to wire 37-38, L,L to 59, U,U to wire 25-26, R,R to 71, U,U to wire 13-14, R,R,R to 89, D,D down vertical 91-92 -> park rows ~17-22 above red. GREEN-cart: camera follows (offset = x0-28, ends ~61). Then green jumps down over red -> 30-33; red down over green -> 36-39; green down over red -> 42-45? (wait: green@30-33 over red@36-39 -> 42-45 yes); then east leapfrog over purples 96-99 both rows -> 102-105; continue east (expect camera reveals).

## Turn 82 (Action ~630)
- Green boarded cart E at mini-box dock (sel/dest 28+44). Cart E at 71-76 r41-46, green interior 72-75 r42-45. Offset still 44 (no snap on boarding). Cart W drifted to west x0=41 r35-40.
- Queued 14 arrows: U (wire 37-38), L,L (71->59), U,U (vert 61-62 -> wire 25-26), R,R (59->71), U,U (vert 73-74 -> wire 13-14 r11-16), R,R,R (71->89), D,D (vert 91-92, expect park r17-22, interior 18-21, above red@90-93 r24-27; 2nd D refused if so).
- Green-cart drive scrolls camera (expect offset ~61 = x0 89 - 28). VERIFY offset+park rows next turn before clicks.
- Then: green down-jump over red -> cell 30-33 (world 90-93). Then red@24-27 down over green -> 36-39; green down over red -> 42-45; then east over purples 96-99: red (r36-39) -> 102-105, green (r42-45) -> 102-105. Continue east, camera reveals.

## Turn 83 (Action ~644)
- Cart drive complete: parked at 89-94 r17-22, green interior 90-93 r18-21 directly above red@90-93 r24-27. Camera did NOT scroll (offset 44) — green-cart scroll rule apparently not universal (maybe only when cart would leave view).
- Queued 8 clicks (offset 44): green down (47,19)->(47,31) [->30-33]; red down (47,25)->(47,37) [->36-39]; green down (47,31)->(47,43) [->42-45]; red east (47,37)->(59,37) [->102-105 r36-39, expect camera auto-jump on this landing, screen 58-61].
- Next: recompute offset; green east over purple (r42-45) -> 102-105; continue twin-corridor leapfrog east; empty cart at 89-94 r17-22 may need repositioning later.
- Camera-follow rule refined: walking-peg landing at screen x>=~54 triggers scroll (both colors). Cart moves: no scroll observed this level.

## Turn 84 (Action ~652) — CAMERA at offset 84; ENDGAME MAPPED
- Column descent + red east all worked. Red@102-105 r36-39 (screen 18-21), green#1@90-93 r42-45 (screen 6-9). Cart E empty parked 89-94 r17-22.
- REVEALED (world): TWIN CONTAINERS (goal pockets, G-border purple boxes like start boxes) at 119-125 & 125-131, seats ~120-123 & 126-129 r6-9, hanging under wire row 5-10 gap; west approach wire 7-8 (109-118, cart x0=113 = adjacent-west), east stub 132-135 r7-8 (vertical 134-135 r9-15 to cart#3 home dock frame r16 world 131-138). GREEN#2 in box at 138-141 r42-45 (cells r36-39 empty, purple spring seat r30-33, dock above r23-28 via vertical 139-140 r21-27). CART#3 at 131-136 r17-22 on wire 19-20 (world 103-131). Verticals off wire 19-20: 103-104 (r21-33, cart x0=101, park interior 102-105 r30-33 above corridor), 109-110 (r9-27, connects wire 7-8), 115-116 (r21-33, x0=113 park above 114-117), 127-128 (r21-27 dangling x0=125). Corridors: top r36-39, bottom r42-45; cells at 90-93, 102-105, 114-117; purples 96-99, 108-111. Column at 90-93: cells r24-27/30-33/36-39/42-45. Cart E network (wire 13-14 world 73-92) is ISOLATED from container network.
- KEY MECHANICS ASSUMED: purple seats are occupiable; peg on/below seat springs over it to adjacent/2-away cart; occupied seat = valid mid.
- SOLUTION: (1) park cart#3 at x0=101 (interior 102-105 r30-33); green#1 east over purple ->102-105(42), up over red -> cart. (2) cart#3 U, R(->107), U,U (vert 109-110 -> wire 7-8), R(->113)... NO WAIT green#1 must go to green#2's box FIRST as mid: cart#3 route to box dock x0=137 (via home dock, R past 131, D — EMPIRICAL). green#1 springs down -> box 36-39. (3) green#2 up over green#1 -> seat 30-33, spring -> cart. (4) deliver green#2 via WEST approach (x0=113): over container#1 purple -> container#2 seat. (5) cart back to box dock; green#1 springs up over purple -> cart. (6) deliver green#1 via EAST stub: over container#2 (occupied=valid mid) -> container#1 seat. (7) red stays corridor-stuck — acceptable.
- Queued 11: L*5 (cart#3 131->101; carts E/W refused), D,D (park r29-34, interior 30-33), green east sel(7,43) dest(19,43), green up-over-red sel(19,43) dest(19,31).

## Turn 85 (Action ~663) — CONTAINERS ARE MOBILE CARTS
- Trace of 652-658: the twin G-bordered containers MOVED with arrows! L presses slid them west along their top rail (until wire ends); D presses sent container#1 DOWN vertical 109-110: now at world 107-112 r17-22 (seat 108-111 r18-21, z rows 18-19). Container#2 still at 113-118 r4-10. Cart#3 parked vertical 103-104 BOTTOM = rows 23-28 (interior 102-105 r24-27) — CANNOT go lower (wall row 34); my r30-33 park idea was wrong, so corridor up-jump landing is void. Green#1 still 102-105(r42), red 102-105(r36).
- G-border = mobile box; $-border = static. Static: west start boxes, mini-boxes, corridor purples, strip purple, green#2 box purple. Mobile: 2 containers only.
- L6 goal recall: capture to 1 green = WIN. L7 likely same → must capture green#2 (or green#1) — but ENTRY PROBLEM: peg zone (corridors, column 90-93, cart E net, west) vs wire-19-20 zone (cart#3, containers, green#2 box dock) have NO peg crossing found: all r24-27 park slots east of column top (90-93) have void at 96-99 (no vertical/wire); wire 13-14 (73-92) isolated from everything east; containers can't reach peg zone.
- Unknown mechanics to probe: (a) can pegs land ON purple seats/springboards (adjacent entry)? (b) weird vertical void-skip?
- Queued 5: D (container#1 -> vertical 109-110 bottom r23-28, seat 108-111 r24-27, adjacent-east of cart#3 interior; all other carts refuse D), probe A: green sel(19,43) dest(13,43) adjacent-onto-purple, probe C: red sel(19,37) dest(19,25) void-skip into cart#3.
- If both fail: consider that goal may not need green#2; maybe seat green#1 in container via unknown route; or capture green#1 BY green#2?? (green#2 immobile); or L7 goal is different (deliver red home?). Also possible: I mis-ID'd cart#3's bottom stop — recheck after D.

## Turn 86 (~A668)
Probes all failed: container#1 D refused (diff 0, vertical 109-110 only spans r9-21); adjacent-onto-purple & void-skip clicks diff 36 (sel change only). No exotic mechanics.
NEW: vertical 127-128 spans r14-27. Green#2's box spring is G-BORDERED (mobile class) at world 137-142 r29-34, directly under vertical 139-140 (r21-27)+dock frame r28. U never pressed at offset 84.
ORACLE recalled from L7 start: sel click on immobile peg = diff 0; movable peg = diff 28. Clicking green#2 directly answers "does it have any legal move?"
Plan: ACTION1 (test spring-box lift on vertical 139-140 + watch all containers/carts), ACTION6(55,43) oracle-sel green#2, ACTION6(60,60) deselect on void.
Next turn: parse U diff via G""""G / G----G traces; if box lifted, remap green#2 column. If sel diff 28, enumerate green#2's legal destinations — likely the intended extraction mechanic.

## Turn 87 (~A671) — MASTER PLAN FOUND
U press (A668) lifted whole fleet 6px: box 29-34→dock 23-28 (climbed vertical 139-140!), cart#3→17-22 (wire), cart E→11-16, cont#1→10-16. Green#2 sel = diff 0 (still immobile).
KEY DISCOVERIES (board 670):
- Main grid (world 88-120, bands 36-39 & 42-45): columns = empty(90-93) | PURPLE(96-99) | pegs(102-105) | PURPLE(108-111) | empty(114-117). Purples = grid springs, bidirectional (red sprang 90→102 before).
- 90-93 column = LADDER: cells at 24-27, 30-33, 36-39, 42-45. Top cell 24-27 sits under wire slot 89-94 (cart E's vertical 92-93). Purple at 84-87 r23-26 springs west into corridor (unused).
- Green#2 column (world 136-144): dock 22-29 (box now there), vertical 139-140 r21-27, EMPTY cell int 36-39, green#2 int 42-45. Void below.
- L7-start seat exit was actually SPRING over purple into vessel (diff 44, green cell 12-15 → cart 23-26). Purple seats = mobile springboards, not landable probably.
- Top wire rows 7-8 (world ~109-134); verticals: 92-93(r9-21), 103-104(r21-28), 109-110(r9-21), 115-116(r21-33!into grid), 127-128(r14-27), 133-134(r9-18), 139-140(r21-27). Mid wire 19-20 → world ~147.
- Only WIRE-LEVEL (r17-22) vessels slide on L/R; top-wire vessels slide too (straddle 7-8); others static.
MASTER PLAN: (1) green#1 springs W→90-93 42-45; red springs W→36-39; G over R→30-33; R over G→24-27; L,L (cart#3 101-106→89-94 wire level); G over R→lands IN cart#3 int 18-21 (gamble: landable at non-dock wire slot). (2) R×8 cart#3→137-142; D (cascade: box dock→bottom 29-34, cart#3→dock 23-28; cont#1 drops to wire — inert). (3) click green#1 (24-27) spring over box purple 30-33 → cell 36-39. (4) shuffle: U (cart#3→wire, box→dock), L×3 (cart#3→119-124 safe from verticals), U (box→wire 17-22), R (box 143-148 east of vert; conts slide top wire), R,R (cart#3→137-142), D,D (cart#3→bottom 29-34 int 30-33). (5) click green#2 (55,43)→(55,31): jumps over green#1, CAPTURES → lands in cart → WIN.
Sent this turn: ladder part (steps 1): 12 actions ending with boarding hop. If boarding fails (diff 36), reversible: R over G→36-39, G over R→42-45, spring back E.

## Turn 88 (~A683)
Ladder OK: green#1@90-93 r30-33, red@90-93 r24-27. BUT L,L failed for cart#3: wire 19-20 only spans world ~100-147 (nothing west of 100 at that height). Cart E instead slid WEST on hidden wire 13-14 (world <=92, west only) — now off-screen west. Cart E's 89-94 slot = bottom stop of vertical 92-93, NO east wire → dead end as ferry. Boarding hop clicks fizzled (diff 0).
Lateral rule refined: vessel slides on L/R iff straddling a horizontal wire at its height (wires: 7-8 top ~107-134, 13-14 west <=92, 19-20 mid 100-147).
NEW BOARDING STATION: vertical 115-116 (r21-33) from wire 19-20 down to grid frame 34 at world 114-117. Cart#3 docks at frame 29-34, interior 30-33 = directly above grid cell 114-117 36-39. Pegs reach 114-117 via grid purples (108-111 springs).
Sent (18): R,R (cart#3 101->113, also container#2 slides east top wire, cart E slides back east toward home), D,D (box dock->BOTTOM 29-34 ready for spring; cart#3 -> 23-28 -> 29-34 int 30-33; container#1 -> wire level 16-21 CAUTION slides on future R; cart E descends home), then clicks: reverse-ladder (red down 24->36 over green, green down 30->42 over red), springs east x2 each (90->102->114 both bands), then green#1 UP over red into cart#3 interior (31,31).
Target state: green#1 IN cart#3 @114-117 r30-33; red parked @114-117 r36-39 (job done).
NEXT TURN: U,U (cart#3+green -> wire 17-22), R x4 (113->137-142 straddle vert 139-140; container#1 may slide too — monitor), D (cart#3 -> dock 23-28 above box), click green#1 (54,25)->(55,37)?? = spring over box purple into cell 138-141 r36-39. Then shuffle: U, L,L,L (cart#3 to 119-124 safe), U (box->wire), R,R,R (box->143-148 refused at wire end; cart#3 ->137-142), D,D (cart#3 -> bottom int 30-33). FINAL: green#2 (55,43)->(55,31) jump over green#1 CAPTURE land in cart = WIN L7.

## Turn 89 (~A701)
ALL 18 OK: green#1 IN cart#3 (interior 30-33 @114-117, bottom of vert 115-116); red parked @114-117 r36-39; box @bottom 29-34 (137-142); cart E home @89-94 wire-level (inert — no lateral wire there); cont#1 @wire 16-22 (107-112); cont#2 @top wire 119-124.
KEY: wire 19-20 ends at world ~140 (row 19 cols 57-63 empty) → box at 137-142 REFUSES east slides. Box is eastmost vessel at east end.
Sent (10): U,U (cart#3->wire; box->dock->wire; cont#1->top), R,R,R (cart#3 113->131-136; box refused at 137-142), D (box wire->dock; cart#3 no vert at 131-136 stays), R (cart#3->137-142 over box's dock), D (STACKED: box dock->bottom 29-34; cart#3 wire->dock 23-28), click (55,25)->(55,37): green#1 springs from cart over box purple int 30-33 into CELL 138-141 r36-39. DELIVERED (if stacked descent works).
NEXT TURN (the swap — box must vacate column; cart#3 to bottom int 30-33):
Box is eastmost & east-end → cannot park east. Escape: hoist box up vertical 133-134 (rows 9-18, upward from wire at 131-136) OR sink it down vert 127-128 (bottom stop 23-28 @125-130). Watch cont#2 position (may occupy 133-134 slot). Sketch: U (cart#3 dock->wire@137; box bottom->dock), L (cart#3->131), U (box->wire; cart#3 rises 133-134 to 11-16), L (box->131 under cart#3), L (box->125), D (cart#3 11-16 -> wire@131; box 125-130 descends vert 127-128 -> 23-28 PARKED AWAY), R (cart#3->137), D,D (cart#3 dock->bottom int 30-33). FINAL: green#2 (55,43)->(55,31) jump over green#1, CAPTURE, land in cart = WIN L7 (score 7).
If click this turn fizzled (stacked descent refused), fix with extra D + clicks first.

## Turn 90 (~A711)
DELIVERY COMPLETE: green#1 @138-141 r36-39 (sprang from cart#3-in-dock over box purple). Cart#3 empty in dock 23-28; box at bottom 29-34; red spent @114-117 r36-39; green#2 @138-141 r42-45.
Containers migrated east: cont#2 @131-136 r11-16 (parked on vert 133-134), cont#1 @131-136 r17-22 WIRE LEVEL (slides on L/R!).
SWAP PROBLEM: box is eastmost on wire & wire ends 140; sinking box via vert 127-128 (bottom 23-28 @125-130) requires box WEST of cart#3 — impossible (can't reorder on wire). Also cont#2 threatens to drop to wire and plug the east-end slot (D when 131-136 wire empty), which would let it sink into the dock = catastrophic block.
INSIGHT: test whether green#2's capture jump landing on the EMPTY BOX SEAT (purple, 30-33) is legal — never tested jump-LANDING on seat (only 1-cell adjacent move failed). Green#2 has exactly one candidate move → sel oracle unambiguous: diff 28 = legal (then click executes capture = WIN), diff 0 = must engineer swap.
Sent (2): ACTION6(55,43) sel green#2, ACTION6(55,31) capture jump over green#1 into seat.
If diff 0: swap choreography still unsolved — ideas: use U-refusal tricks (cont#2 plugs 133-134 hoist), or sink cart#3 at 125-130 temporarily and hoist box... revisit with fresh board.

## Turn 91 (~A713)
Oracle result: diff 0,0 — green#2 has NO legal move with box seat at 30-33. Purple seats NOT jump-landable. Swap mandatory.
SWAP CHOREOGRAPHY v2 (17 actions sent):
A1 L: cont#1 wire131->125. A2 D: cont#2 drops 11-16->wire@131; cont#1 sinks 127-128 vert ->23-28@125. A3,A4 L,L: cont#2 ->119. A5 U: cart#3 dock->wire@137; box bottom->dock; cont#1 pops up ->wire@125; cartE rises ->11-16. A6,A7 L,L: cart#3 ->125; cont#1 ->113; cont#2 ->107; (cartE drifts west on wire 13-14). A8 U: box dock->wire@137; cont#2 rises 109-110 ->11-16@107; cart#3@125 refused (127-128 down-only). A9 L: box ->131; cart#3 ->119; cont#1 ->107. A10 U: BOX rises 133-134 -> 11-16@131 PARKED OFF-WIRE; cont#1 refused (cont#2 above). A11-A13 R,R,R: cart#3 ->125->131(under parked box)->137 over vert 139-140; cont#1 ->125. A14 D: cart#3 ->dock 23-28; cont#1 sinks @125; box drops back to wire@131 (harmless); cont#2 drops wire@107; cartE home. A15 D: cart#3 ->BOTTOM 29-34 int 30-33 EMPTY; box refused (no down-vert @131) STAYS OUT.
A16/A17: green#2 (55,43)->(55,31): jump over green#1(36-39), GREEN-OVER-GREEN CAPTURE, land in empty docked cart#3 -> 1 green left -> WIN L7 (expect Score 7).
If desync: later arrows refuse benignly, clicks fizzle; re-derive from fresh board.

## Turn 92 (~A730) — LEVEL 7 CLEARED, Score 7 at action 729!
Swap choreography v2 executed perfectly; green#2 jumped over green#1 into empty docked cart#3 = capture = win. Total L7 cost ~194 actions.
LEVEL 8 initial (board 729): 8x6 cell grid, screen cols 11-59 rows 16-53. Cell cols C1..C8 at x=12,18,24,30,36,42,48,54 (+0-3); bands B1..B6 at y=18,24,30,36,42,48.
Pieces: green#1 (C1,B2); green#2 (C8,B6) cornered. Purples: (C2,B2),(C6,B2),(C7,B3),(C2,B4),(C6,B4). Holes 'f': (C4,B5),(C4,B6). Notch/dock replacing (C1,B4): wire stub rows 37-38 from vertical 7-8 (rows 37-63) into grid west edge.
Wires: bottom-left wire rows 61-62 cols ~7-26 with CART (frame 17-22ish rows 58-63); vertical 26-27 rows 61-63 (goes off-screen below); bottom-right wire rows 61-62 cols 50-57; vertical 50-51 off-screen below; vertical 55-56 rows 54-63 touching grid bottom frame UNDER green#2 col C8. Underworld likely below row 63 connecting left/right networks.
WIN PATH: only 2 pegs, no red. Deliver green#1 to (C8,B5) or (C7,B6); green#2 jumps over it (lands (C8,B4)/(C6,B6) in-grid empty) = capture = 1 green = WIN.
Green#1 mobility: spring E over (C2,B2) -> (C3,B2) and back only. Boarding cart unresolved: notch cart at (C1,B4) enterable only from (C3,B4) spring W over (C2,B4) — (C3,B4) unreachable by pegs alone. May need vessel at other dock or unknown structures below.
Sent probes (5): sel green#1 (13,25) oracle; (25,25) spring E; R (cart slide test/alignment with vert 26-27); D,D (descend + camera pan reveal underworld).

## Turn 93 (~A735)
Probes: green#1 sprang E to (C3,B2) ok (28/44). R slid cart 17-22 -> 23-28 (dock structure at cols 22-29 rows 58-63 appeared in frame). D: cart descended vertical (cols 25-26!) fully BELOW screen row 63 — underworld exists, camera does not pan. Second D refused (diff 0) = at below-screen bottom stop (or no visible change).
Vertical positions corrected: left below-wire vertical at cols 25-26; right verticals: 50-51 (rows 61-63+, off-screen below), 55-56 (rows 54-63, touches grid bottom frame under C8/green#2).
KEY GEOMETRY: cart docked at top of vertical 55-56 = frame 53-58, interior cols 54-57 rows 54-57 = virtual cell (C8,B7) DIRECTLY below green#2.
WIN IDEAS: (a) container (mobile purple) docked at (C8,B7) + cart below it on wire = green#2 springs down over seat into cart -> green#2 mobile, ride to notch (C1,B4), spring E over (C2,B4) to (C3,B4)... then green#1 (C3,B2) and green#2 (C3,B4) separated by empty (C3,B3) — STILL unsolved final. (b) unknown underworld content may hold second vessel/container. Need exploration.
Boarding problem: green#1 confined to {(C1,B2),(C3,B2)}; notch cart at (C1,B4) enterable only from (C3,B4).
Sent (6): R,R,R,R (test hidden bottom wire eastward), U,U (re-emerge: right side cols 48-53 if connected, else back at left 23-28).

## Turn 94 (~A745, Level 8)
- Probe results: R×4 with carts below screen → all diff 0 (refused or invisible). U#1 (board 739, diff 100): TWO carts appeared on bottom wire 61-62 — left frame cols 23-28, right frame cols 47-52, both rows 59-64. U#2 refused (diff 0).
- Row-63 scan board 733: shaft 'O' cols [25,26] and [49,50] → shafts exactly 24px (4 steps) apart, ALIGNED with 6px lattice. Earlier "misaligned 50-51" reading was wrong.
- Board 740 row 63 cols [22,29,46,53] = two cart frame borders; row 55 [7,8,55,56] = verticals 7-8 (notch dock) and 55-56 (under C8).
- Ambiguity: did our cart slide underworld to right shaft while a 2nd rose at left, or was a 2nd cart always in right shaft? Both now at wire level.
- Probe batch written: ACTION6(55,49) oracle green#2 (diff 28 = has unknown legal move; 0 = frozen), ACTION6(2,10) deselect, then D, L×4, U — drop carts into shafts, slide west underworld, rise: where they pop reveals underworld connectivity.

## Turn 95 (~A749-752, Level 8)
- Turn-94 probe results: green#2 oracle (no cart below) = diff 0, FROZEN. D dropped both carts into shafts (diff 100). L×4 underworld = all diff 0 (no hidden horizontal connection between shafts). U restored carts to same spots. Conclusion: shafts 25-26/49-50 are dead-end vertical stubs; bottom wire 61-62 is TWO segments (left cols 7-22+cart, right cart+53-56).
- Carts have ORANGE fill ('-', rows 60-63 / frame rows 2-5) = possibly LOADED. Cart geometry: 8 wide (O border) x 6 tall, interior 4px aligned to lattice. Left cart interior x=24 (C3 col), right x=48 (C7 col).
- KEY TOPOLOGY: wire 53-54 spans cols 10-59 = full-width underworld highway directly under grid = virtual band B7 (interior y=54). Vertical 55-56 rows 53-62 connects right bottom wire to it (under C8). Vertical 7-8 rows 37-62 connects left bottom wire to notch stub 37-38 → dock at (C1,B4).
- Win concept: get a green into a cart at (C8,B7), jump up over green#2 (C8,B6) → land (C8,B5) = capture. OR green#2 drops into cart at (C8,B7), ferry west on wire 53-54... exits unclear (no occupied B6 mids elsewhere).
- This turn's probe: ACTION4 (right cart east onto vertical 55-56), ACTION1 (up to (C8,B7)), ACTION6(55,49) re-oracle green#2 (diff 28 = drop-into-vessel move exists!), ACTION6(55,55) attempt drop destination.

## Turn 96 (~A753-755, Level 8)
- Turn-95 results: A4 slid right box east to interior 54-57 ✓; A1 docked it at (C8,B7) frame rows 53-58, interior 54-57×54-57 — PERFECTLY under green#2. But oracle green#2 = diff 0 (STILL frozen) and click cart interior = diff 0. No drop mechanic; loaded vessel below doesn't grant moves.
- VESSEL SPRITE ID (from L7 board 728): solid orange 'G----G' fill = BOX (jump mid, NOT landable). L7's landable cart = pinwheel 'G-##-G'/'G#--#G' (orange+gray). Purple-seat vessels = '"$z"/"zz"'. BOTH L8 vessels are BOXES. No landable cart seen yet in L8.
- Deduction: green#1 pocket {(C1,B2),(C3,B2)} can never gain a new mid (boxes only reach B7/notch B4, not adjacent to B2). So solution must free green#2: box mid at (C8,B7) ✓ exists, but landing (C8,B8) needs an EMPTY CART. Right box was originally HIDDEN in right shaft below screen → shafts can hold vessels → maybe empty carts hide deeper in shafts.
- Bottom-wire straddle: interior rows 60-63 = B8. Wire 53-54 straddle: interior rows 54-57 = B7. Lattice consistent.
- This turn: ACTION3 (left box off left shaft 25-26 → interior 18-21; right box slides west too → interior 48-51), then ACTION1 ×2 — if hidden carts exist in shafts they rise to bottom wire. Watch rows 58-63 cols 22-29/46-53.

## Turn 97 (~A756-760, Level 8)
- Turn-96 results: A3 moved ONLY left box (back to its L8-start spot, interior 18-21); right box at (C8,B7) top-of-vertical dock did NOT slide (pinned/not straddling). U,U = diff 0: SHAFTS ARE EMPTY dead-ends, no hidden carts.
- L8 initial state recheck (board 730): left box started at interior 18-21 on left bottom wire; right box started hidden in right shaft below screen.
- Vessel sprite = 8 wide x 8 tall (O,G,4x orange,G,O), interior 4x4. Bottom-wire straddle interior=B8 (rows 60-63); vertical-top dock at 55-56 gives interior B7 (54-57).
- Vertical 7-8 (cols 7-8, rows 37-62) gives left box access to column C0 (x=6) bands B4..B8; crosses wire 53-54 at rows 53-54. Stub wire 37-38 → notch dock (C1,B4).
- Open question: is landing-on-box actually illegal? Never explicitly tested in L7 (only used box as mid). If legal, green#2 jump down over (C8,B7) box onto (C8,B8) box could work — but left box can't reach right bottom segment except via wire 53-54 highway.
- This turn: left box west x2 (interior 6-9, onto vertical 7-8), U (to (C0,B7) frame 52-59, wire 53-54 at frame rows 1-2 — same geometry as right box's dock), then E,E — TEST whether wire 53-54 supports horizontal sliding. If yes: highway open, ferry left box east to (C8,B8) later. If no: next turn continue U to notch level.

## Turn 98 (~A761-765, Level 8)
- Turn-97 results: left box slid W x2 (interior 6-9) and rose to (C0,B7) frame 52-59 ✓, but R,R = diff 0: PINNED. Wire "53-54" is NOT a wire — it is the grid's bottom O-border (matches top border row 16). NO under-grid highway. Left box currently at (C0,B7) on vertical 7-8; right box at (C8,B7) top of vertical 55-56.
- Vessel topology final: left bottom segment (interiors x=6/12/18/24) + vertical 7-8 (C0 col, stops B7..B4/stub) + stub 37-38 → notch (C1,B4). Right segment: (C7,B8) over empty shaft, (C8,B8) east end, (C8,B7) vertical top. Segments DISCONNECTED. Landing-on-box untestable (no config places a box 2 from a green over an occupied mid).
- Grid seats sprite = L7 container seat ('"""" / "$z" / "zz" / """" / OOOO'), rendered 1 row above cell interior. Five static seats.
- Only remaining outs: (a) seats clickable/movable; (b) holes interactive; (c) some unknown mechanic. If a seat could occupy (C4,B2) or (C3,B3), green#1 gains full-grid mobility via seat chain: (C5,B2)-over(C6,B2)->(C7,B2)-over(C7,B3)->(C7,B4)-over(C6,B4)->(C5,B4) etc.
- This turn probes: click seat (C6,B2)@(43,25); then empty cell (C4,B2)@(31,25) (dest if seat selected); deselect; click hole (C4,B5)@(31,43); deselect.

## Turn 99 (~A766-771, Level 8)
- Turn-98 results: ALL probe clicks diff 0 — seats NOT clickable, holes NOT clickable, empty cells inert. L8 interactive surface so far: green#1 shuttle + box shuffling only.
- Untested mechanic: ARROWS WITH A PEG SELECTED (all prior arrow presses had nothing selected). If selected pegs are arrow-movable, entire level opens up.
- This turn: sel green#1 (25,25) [expect 28], ACTION4 (does green#1 step/jump east? boxes are pinned L/R so any grid-region diff = peg moved), deselect, sel green#2 (55,49) [expect 0 but may silently select], ACTION1 (up; note left box will rise (C0,B7)->(C0,B6), right box U-pinned — so a diff at cols 54-57 rows 42-51 = green#2 moved), deselect.
- Box state entering turn: left at (C0,B7) vertical 7-8; right at (C8,B7) vertical 55-56 top.

## Turn 100 (~A772-776, Level 8)
- Turn-99 results: sel green#1 diff 28 = ring 'h' around (C3,B2) + '#' DESTINATION MARKER diamond at (C1,B2) interior — SELECTION SHOWS ALL LEGAL DESTS as '#'. Green#1 has exactly 1. Arrow with peg selected = plain deselect (no peg motion). Green#2 sel = diff 0 even with box mid at (C8,B7) → (C8,B8) not landable / box-top-dock not a mid.
- Row 0 = action counter, 64 per lap, WRAPS with new chars ('8'→'#'→'h'→'q'), L7 used 3 laps, NO reset at lap end. No time pressure.
- Deduction chain: green#2 permanently frozen; capture must be green#1 jumping over green#2 FROM a vessel at (C8,B7) landing (C8,B5) — the exact L7 win pattern. Needs a BOARDABLE vessel (cart), but both vessels are sealed boxes. Hypothesis: NOTCH (C1,B4) is an unloading dock — docking a box there converts/unloads it (why else does the notch exist?).
- Box state: left at (C0,B6) after turn-99 stray U; right at (C8,B7).
- This turn: U,U (left box → stub level B4), R (dock at notch (C1,B4)), sel green#1 (watch for NEW '#' dests), deselect. Watch box sprite for interior change (orange → pinwheel '-##-' = cart!).

## Turn 101 (~A777-781, Level 8)
- Turn-100 results: left box docked INTO notch (C1,B4) ✓ (interior cols 12-15 rows 36-39, beside seat (C2,B4)). NO unload/conversion — still solid orange. Green#1 sel: still only dest (C1,B2). Notch is not (visibly) an unloader.
- This turn: click docked box interior (13,37) — if diff 28, boxes in grid cells are selectable/movable like pegs (dests as '#'). Deselect. ACTION4 push test (does box push into grid / shove seat?). Re-click box. Deselect.

## Turn 102 (~A782-787, Level 8)
- Turn-101 results: all diff 0 — docked box not clickable, not pushable east. Box pinned at notch (C1,B4).
- CORRECTION: both C4 holes are FULL diamonds '8ff8/ffff/ffff/8ff8' (B5 rows 42-45, B6 rows 48-51) — peg-shaped shadow sockets = likely GOAL cells for the two greens (delivery win, like L7 goal pockets).
- L8 transition frames (after A729) = L7 win animation only (green riding cart up), no L8 hints. Pristine board 729 matches model exactly.
- Known-mechanics state space provably sterile → hidden mechanic must exist. Untested: selected-peg + Down while vessel docked directly below (L7 seat-exit input pattern).
- This turn: sel green#2 (55,49), ACTION2 (drop test; right box may ride down to (C8,B8) — noise), deselect, ACTION1 (restore box), click box top seam (56,54), deselect.

## Turn 103 (~action 795) — SHAFT DEPTH PROBE (underworld theory revival)
Decisive re-read of L5/L6 notes: **camera follows ONLY peg-carrying carts; empty-cart moves NEVER scroll the camera and show diff 0 when off-screen.** This invalidates my turn-96 "shafts are dead ends" proof — that test used a SINGLE Down before the lateral probes. If shafts are ≥2 deep, the cart sat mid-tube (walls block L/R) and every observation is consistent with a hidden underworld below row 63.

Also corrected this session (from L2/L3/L5 notes): orange 4x4 interior = EMPTY LANDABLE CART (not sealed box); purple-loaded cart = mobile mid enabling through-wall jumps.

**Probe in flight**: D (right cart (C8,B7)→(C8,B8)), L (→(C7,B8) over right shaft; left cart unpins notch→(C0,B4)), D,D,D descend shaft, U,U,U return.
**Read-out next turn**: which U press re-shows the right cart at (C7,B8) (diffs cols 46-60, rows 58-63)?
- Re-emerge on U#1 → depth-1 dead end, underworld theory dies.
- Re-emerge on U#2 or U#3 → depth ≥2 → hidden region below row 63 likely.
Left-cart noise separable: its diffs live at cols 4-11 (C0 vertical, stops B4-B8).
**If depth ≥2 next turn**: probe lateral at depth (D×depth, L×4, U×depth), watch for re-emergence at LEFT shaft (cols 22-29) to map underworld connectivity.

## Turn 104 (~action 803) — SHAFT VERDICT + EAST WIRE DISCOVERY
**Probe result**: right cart vanished on D#1 into right shaft, D#2/D#3 refused, re-emerged on U#1. Shaft depth = exactly 1 (dead-end pocket). Combined with turn-96 lateral test (L refused at depth), UNDERWORLD THEORY IS DEAD.

**Map corrections from fresh full-board scan** (old compressed map was wrong):
- Row 54 = blue 'f' FULL-WIDTH HIGHWAY, cols 11-54, directly under grid bottom border (row 53). This IS the B7 highway (turn-97 "disproof" was about the wrong element — 'OO' runs are separate).
- Col 61 = blue 'f' VERTICAL WIRE running the ENTIRE east side, rows 17-53, joining highway at SE corner (row 54 cols 57-60 'ffff'). Stops presumably at C9,B1..B6. **(C9,B6) is directly EAST of green#2 (C8,B6)!**
- LEFT system (isolated from right): notch (C1,B4) ↔ stub ↔ OO vertical cols 7-8 (rows 42-63) ↔ OO run rows 61-62 cols 7-27 ↔ left shaft cols 25-26 (depth ~1). C0 vertical does NOT touch highway (gap cols 9-10).
- RIGHT system: right shaft pocket (cols 49-50, depth 1) ↔ OO run rows 61-62 cols 49-56 ↔ OO vertical cols 55-56 ↔ top dock (C8,B7) straddling highway ↔ highway ↔ SE corner ↔ east wire.
- Left cart now at (C0,B4); right cart on OO run over right shaft (cols 46-53, rows 58-65).

**Open question**: turn-97 R,R refusal at top dock — was it the L6 "pinned at vertical-top dock" rule? If pinned, SE corner unreachable from top dock and east wire needs another approach. Testing now.

**In flight (5 actions)**: R (cart→junction; left cart→notch), U (→top dock), R (→SE corner — PIN TEST), U (→up east wire, hopefully (C9,B6)), CLICK green#2 at (55,49).
**Read-out**: if click yields selection ring + any '#' dest markers → NEW MECHANIC (empty cart adjacency?) → jackpot. If R at top dock refused → pin rule confirmed, rethink east-wire access.
**Speculative parking lot**: holes (C4,B5)/(C4,B6) stacked directly above highway stop (C4,B7) — peg-falls-through-holes-into-cart theory. Also: peg-loaded cart into left shaft would scroll camera (camera follows pegs).

## Turn 105 (~action 806) — GRAND REFRAME: SEATS ARE MOBILE PIECES, f-LINES ARE SHADOWS
Dead theories (verified vs L2 board 30):
- f-lines (row 54 under grid, col 61 east side, notch 'fffff', dock 'f' bits) = DROP SHADOWS (same south+east trim exists on every L2 panel; never functional). Highway/east-wire theories DEAD. "Pin" = simply no rails there; OO black = the only cart rails.
- L2's landable cart interior = SOLID ORANGE 'G----G' — SAME sprite as L8's two vessels → L8 vessels ARE landable carts (L7 "box" was a purple-loaded cart).
- "Holes" at (C4,B5),(C4,B6) = peg-shaped BLUE PEGS ('8ff8/ffff' diamond = same shape as green '8II8/IIII'). New piece type, clicked once (31,43) diff 0 — but they had no adjacent pieces, so no legal moves → false negative.
- CLICK AUDIT: all L8 clicks = (13,25),(25,25),(55,49),(2,10),(43,25),(31,25),(31,43),(13,37),(56,54). Seat (C2,B2) at (19,25) NEVER CLICKED. It is the ONLY purple ever adjacent to a piece (green#1). "Seats immobile" was NEVER TESTED. L6/L7 notes: purples jump like pegs ("P1 S over red", "P2 E over P1 CAPTURE").
- L8 attempt 1 still intact; green#1 at (C3,B2) since board 741. Right cart at top dock (C8,B7), left cart in notch (C1,B4).

THEORY OF THE LEVEL: purple (C2,B2) springs E over green#1 → (C4,B2), opening chain: green#1 over it → (C5,B2), over seat (C6,B2) → (C7,B2), over seat (C7,B3) → (C7,B4), etc. Reposition purples as portable mids to reach (C8,B5); then green#1 jumps S over green#2 → capture/merge, landing IN topdock cart (C8,B7); then deliver survivor (gray?) by cart. Blues at C4 may need capturing too, or are goal-related.

**In flight (3 clicks)**: (19,25) select purple [expect diff 28, marker at (31,25)]; (31,25) execute spring to (C4,B2); (25,25) select green#1 [final board should show '#' markers at (C1,B2) AND (C5,B2)].
**Risk noted**: purple-over-green capture would lose green#1 — judged unlikely (cross-color jumps never captured in L5-L7).
**If purple select fails**: clicks 2-3 harmless. Next fallback: RESET and study intro frames.

## Turn 106 (~action 809) — SEATS IMMOBILE; BLUE LADDER THEORY
- Purple (C2,B2) click with green#1 adjacent: diff 0. SEATS ARE FIXTURES, definitively.
- Green#1 selected (diff 28): still exactly one dest (C1,B2). Currently selected.
- BLUE LADDER: bottom blue (C4,B6) at click (31,49) NEVER TESTED; its jump N over blue (C4,B5) → (C4,B4) is the only untested legal-looking move in the level.
- PARITY LAW (jumps move ±2, parity per axis is invariant): green#1 forever (odd col, even row) — can NEVER reach (C8,B5); so the capture must be green#1 jumping FROM the topdock cart N over green#2 → (C8,B5). Cart rides break parity. Boarding: green#1 must reach (C3,B4) then W over seat (C2,B4) into notch cart (C1,B4).
- FULL CANDIDATE SOLUTION:
  1. blue#2 (C4,B6) N over blue#1 → (C4,B4)   [THIS TURN]
  2. blue#1 (C4,B5) N over blue#2 → (C4,B3)
  3. blue#2 (C4,B4) N over blue#1 → (C4,B2)
  4. green#1 (C3,B2) E over blue#2 → (C5,B2); E over seat (C6,B2) → (C7,B2); S over seat (C7,B3) → (C7,B4)
  5. blue#2 (C4,B2) S over blue#1 (C4,B3) → (C4,B4)
  6. green#1 W over seat (C6,B4) → (C5,B4); W over blue#2 (C4,B4) → (C3,B4); W over seat (C2,B4) → INTO NOTCH CART (C1,B4)
  7. Drive loaded cart: L (unpin notch → (C0,B4)), D,D,D (→ (C0,B7)... note: left cart system only reaches C0 column + bottom run — WAIT: loaded cart must reach RIGHT system topdock (C8,B7) — SYSTEMS ARE DISCONNECTED! PROBLEM! Re-examine after ladder works: maybe loaded green jumps OUT mid-route over... revisit. Camera will follow loaded cart (may reveal connections).
- Click map: blue#2=(31,49), blue#1=(31,43), dests: (C4,B4)=(31,37), (C4,B3)=(31,31), (C4,B2)=(31,25); green dests: (C5,B2)=(37,25), (C7,B2)=(49,25), (C7,B4)=(49,37), (C5,B4)=(37,37), (C3,B4)=(25,37), notch=(13,37).
- RISK: blue-over-blue may CAPTURE (purple-over-purple did in L6). If blue#1 vanishes this turn → try ACTION7 undo next turn; if undo fails → RESET replay (nothing else lost).
**In flight (3)**: (2,10) deselect green#1; (31,49) select blue#2 [expect diff 28, marker at (C4,B4)]; (31,37) execute N jump.

## Turn 107 (~action 812) — BLUE LADDER WORKS, NO CAPTURE. FULL PRISON BREAK SENT
- (31,49) selected blue#2 (diff 28, marker at (C4,B4)); (31,37) EXECUTED (diff 44). Blues now (C4,B4)+(C4,B5), (C4,B6) empty. Blue-over-blue does NOT capture.
- SENT 18 clicks (9 jumps, sel+dest pairs):
  1. blue#1 (C4,B5)→N over (C4,B4)→(C4,B3): (31,43),(31,31)
  2. blue#2 (C4,B4)→N→(C4,B2): (31,37),(31,25)
  3. green#1 (C3,B2)→E over blue (C4,B2)→(C5,B2): (25,25),(37,25)
  4. green#1 →E over seat (C6,B2)→(C7,B2): (37,25),(49,25)
  5. green#1 →S over seat (C7,B3)→(C7,B4): (49,25),(49,37)
  6. blue#2 (C4,B2)→S over (C4,B3)→(C4,B4): (31,25),(31,37)
  7. green#1 →W over seat (C6,B4)→(C5,B4): (49,37),(37,37)
  8. green#1 →W over blue#2 (C4,B4)→(C3,B4): (37,37),(25,37)
  9. green#1 →W over seat (C2,B4)→INTO NOTCH CART (C1,B4): (25,37),(13,37)
- Expected end state: green#1 IN left cart at notch; blues at (C4,B3),(C4,B4); green#2 unchanged.
- NEXT TURN: drive loaded cart (camera follows loaded carts): L → (C0,B4), then D,D,D,D toward bottom run → toward LEFT SHAFT; descend with peg → camera should scroll/reveal off-screen content and (hopefully) the connection toward green#2 / right system. Endgame: green#1 must jump over green#2 (capture) from adjacent cell — likely from a cart position adjacent to (C8,B6).
- Unproven steps to watch: green-over-blue (step 3) and boarding (step 9).

## Turn 108 (~action 830) — GREEN#1 BOARDED. DRIVING TO LEFT SHAFT
- All 18 clicks executed (alternating 28/36 selects + 44/52 jumps). Green#1 IN notch cart at (C1,B4) ('GIIIIG' interior). Blues rest at (C4,B3),(C4,B4). Green#2 untouched.
- SENT (9 arrows): L (notch→(C0,B4)), D×4 (vertical stops B5,B6,B7,B8), R×3 (bottom run: interiors 12-15, 18-21, 24-27 = over left shaft), D (descend shaft WITH PEG — camera follows loaded carts → expect scroll/reveal of below-screen world).
- Right cart side effects: D#1 topdock→(C8,B8) junction; other arrows refused. Fine — clears topdock.
- If shaft is still a depth-1 pocket even when loaded and no reveal: U back out, rethink (maybe target is elsewhere; green#1-in-cart at (C0,B6) is adjacent-W of (C1,B6) through wall — through-wall exit jumps possible per L5 if mid exists).
- Endgame still needed: green#1 must capture green#2 (jump over it). Watch for new geometry.

## Turn 109 (~action 839) — UNDERWORLD REVEALED. FULL SOLUTION DERIVED
Camera scrolled +30 rows following loaded cart. Current view (camera offset +30 vs original):
- Upper grid now rows -14..23 (green#2 at rows 18-21 cols 54-57 = (C8,B6), click (55,19)); upper highway shadow row 24; right cart at old-(C8,B8) junction rows 28-35 cols 52-59.
- LOWER GRID (1 band, LB1): border row 40 top/47 bottom, cols 10-60; cells C1-C8 interiors rows 42-45, x-interiors same as upper (C1=12..15 ... C8=54..57). TWO NEW BLUES at (C7,LB1),(C8,LB1).
- Left shaft (cols 25-26) bottom = notch dock (C3,LB0) rows 34-40 — loaded cart (green#1) parked there, above (C3,LB1).
- Right shaft (cols 49-51) bottom = notch dock (C7,LB0) — the old "depth-1 pocket". Its D-refusal = blue at (C7,LB1) blocking.
- RAIL rows 49-50, cols 13-41, below lower grid; BIG VESSEL (3-slot, 19 wide, rows 47-52, cols 41-59): [purple seat | EMPTY slot | purple seat], middle slot interior cols 49-52 ≈ under C7. Vessel at rail EAST END (can only slide W).
SOLUTION:
A. Blues ladder west to (C3),(C4): (C8)W→C6, (C7)W→C5, (C6)W→C4, (C5)W→C3. [8 clicks: sel/dest (55,43)(43,43); (49,43)(37,43); (43,43)(31,43); (37,43)(25,43)]
B. L×4: vessel slides west 4 stops → middle slot under C3. (Left cart L refused; right cart L→over-shaft then refused.)
C. Green#1 jumps from left cart (C3,LB0) S over blue (C3,LB1) → INTO vessel middle slot (C3,LB2). [sel (25,37), dest (26,49)]
D. R×4 (vessel home; right cart→junction), L,L (right cart→over-shaft; vessel west 2), D (right cart→pocket (C7,LB0); left cart→(C3,LB1) harmless), R,R (vessel home; green under C7).
E. Blues ladder back east to (C6),(C7): (C3)E→C5, (C4)E→C6, (C5)E→C7. [6 clicks]
F. Green#1 (C7,LB2) jumps N over blue (C7,LB1) → INTO right cart at pocket (C7,LB0). [2 clicks]
G. U (cart+green rise), R (→junction), U (→topdock (C8,B7)). Camera follows.
H. Green#1 jumps N over green#2 → (C8,B5): CAPTURE → expect WIN/merge.
**In flight (14)**: phases A+B+C. Watch: vessel slide mechanics (untested), double-through-border entry jump (precedent: L7 topdock exit jumps). If camera scrolls mid-batch, last 2 clicks may misfire — verify green#1 position next turn before continuing.

## Turn 110 (after A~854, board 848)
Turn-109 batch SUCCEEDED in full: blue ladder west ((C8),(C7)->(C3),(C4) at LB1), vessel slid west-4 (cols 17-35), green#1 jumped cart->over blue->INTO vessel middle slot (C3,LB2). Verified board 848 rows 47-52: vessel shows -II-/IIII/IIII/-II- => green inside. Left cart EMPTY at notch (rows 35-39). Right cart over right shaft (rows 28-35, cols 46-53).
PHASE D issued (arrows only, 9): R,R,R,R (vessel->home, green under C7; right cart->junction then refused), L,L (right cart->over-shaft; vessel west-2), D (right cart->pocket (C7,LB0); left cart D refused: blue at (C3,LB1); vessel D refused), R,R (vessel->home, green->(C7,LB2)).
Expected end state: green#1 at (C7,LB2) in home vessel; right cart docked pocket (C7,LB0); blues (C3,LB1),(C4,LB1).
NEXT (re-derive coords from fresh board — loaded vessel slides scroll camera):
E. 6 clicks: blues ladder east (C3)->(C5), (C4)->(C6), (C5)->(C7).
F. 2 clicks: green#1 N-jump over blue (C7,LB1) INTO right cart (C7,LB0).
G. arrows U,R,U: cart+green rise -> junction -> topdock (C8,B7).
H. 2 clicks: green#1 N over green#2 -> (C8,B5) CAPTURE => expect WIN (watch for L6-style merge/goal-pad epilogue).

## Turn 111 (after A856, board 856)
Phase D SUCCEEDED: R#1 moved vessel+right cart (diff 266, cart->junction), R#2-4 vessel only; L#1 cart back over-shaft + vessel (270), L#2 vessel only; D cart DESCENDED into pocket (diff 103 rows 28-40); R,R vessel home. Board 856: vessel home cols 41-59, green#1 in middle slot under C7 (rows 48-51 cols 48-51); right cart EMPTY docked pocket rows 34-40 interior cols 48-51 (C7,LB0); blues (C3,LB1),(C4,LB1); left cart empty at notch (C3,LB0). Camera did NOT scroll during loaded-vessel slides (stayed on screen).
PHASES E+F+G issued (11 actions):
E clicks y=43: (25->37) blue C3->C5 over C4; (31->43) blue C4->C6 over C5; (37->49) blue C5->C7 over C6.
F: (49,49) select green in vessel; (49,37) jump N over blue (C7,LB1) INTO right cart pocket.
G: U (loaded cart rises), R (->junction), U (->topdock (C8,B7)). Camera will scroll +~30 following loaded cart.
NEXT TURN (H): re-derive coords from fresh board; green#1 at topdock jumps S?N? — green#2 at (C8,B6), topdock is (C8,B7) above it... jump N? No: topdock B7 is BELOW-screen? Upper grid rows: B7 bottom. Green jumps from cart over green#2 -> (C8,B5): CAPTURE => WIN expected. Watch for L6-style merge/goal-pad epilogue; score should hit 8.

## Turn 112 (after A867, board 867)
E+F+G ALL SUCCEEDED: blue ladder east (diffs 28/44 x3, blues now C5? no wait — final blues at (C4,LB1),(C6? ) irrelevant now), green#1 jumped vessel->cart (863/864 rows 36-52 col 47-52), cart rode U (1656 scroll), R (121), U (1709 scroll) to TOPDOCK.
Board 867 (camera on upper grid): loaded cart 'G-II-G/GIIIIG' rows 35-41 cols 53-58 at topdock below C8; green#2 at C8 bottom cell rows 30-33 cols 54-57; landing cell rows 24-27 C8 EMPTY. Purple seats at (C2,r5-8),(C6,r5-8),(C7,r11-15),(C2,r17-21),(C6,r17-21); blue pegs upper grid at (C4,r12-15),(C4,r18-21).
PHASE H issued: ACTION6(55,37) select green#1 in cart; ACTION6(55,25) jump N over green#2 -> capture. EXPECT SCORE 8 / possibly L6-style merge->gray + goal-pad epilogue. If score stays 7 and a gray peg appears, look for a goal pad to deliver it to.

## Turn 113 — LEVEL 8 CLEARED (A869, score 7->8)
Phase H worked exactly: select (55,37), jump (55,25) over green#2 = capture => immediate win. No merge epilogue. L8 total understanding validated: parity law, cart rides, vessel ferry, blue ladders.

## LEVEL 9 initial board (board 869)
5x6 grid panel cols 17-47 rows 16-53. Cell cols C1..C5 interiors x: 19-22,25-28,31-34,37-40,43-46 (click x=20,26,32,38,44). Cell rows R1..R6 interiors y: 18-21,24-27,30-33,36-39,42-45,48-51 (click y=19,25,31,37,43,49).
Pieces: GREEN A (C1,R5), GREEN B (C5,R6); blues (C3,R1),(C4,R2),(C2,R5),(C2,R6). EMPTY CART docked at (C5,R4), rail heads EAST off-screen at rows 37-38 (world continues right).
Parity: A (odd,odd), B (odd,even) => only B-over-A capture possible (vertical, odd col). Target: A to (C5,R5), B jumps N over A into cart = capture => expect win (or gray merge + eastward delivery).
SOLUTION (4 jumps, 8 clicks): 1) A E over blue(C2,R5)->(C3,R5); 2) blue(C2,R5) E over A->(C4,R5) [only blue with right parity for (C4,R5)]; 3) A E over blue->(C5,R5); 4) B N over A->cart (C5,R4) CAPTURE.
Clicks: (20,43)->(32,43); (26,43)->(38,43); (32,43)->(44,43); (44,49)->(44,37).
If no win: gray peg in cart -> ride east with ACTION4, camera follows.

## Turn 114 (after A877, board 877)
CORRECTION: L9 grid is IRREGULAR — (C5,R5) DOES NOT EXIST (R5 east wall at col 42; R5 spans C1-C4 only; R6 spans C1-C5). Jump 3+4 refused (diff 0): A had no legal moves at (C3,R5), B none at (C5,R6). Selection refusal = piece has zero legal moves (confirmed again).
Wrote BFS solver (state=(A,B,blues), jump rules, capture=win). From CURRENT state (A(3,5), B(5,6), blues (3,1),(4,2),(4,5),(2,6)) → 12-jump WIN:
1 bl(4,5)->(2,5); 2 bl(2,6)->(2,4); 3 bl(2,5)->(2,3); 4 bl(2,4)->(2,2); 5 bl(2,3)->(2,1); 6 bl(2,1)->(4,1) over (3,1); 7 bl(4,1)->(4,3) over (4,2); 8 bl(4,2)->(4,4); 9 bl(4,3)->(4,5); 10 bl(4,4)->(4,6); 11 B(5,6)->(3,6) over bl(4,6); 12 B(3,6)->(3,4) over A CAPTURE => WIN.
Issued jumps 1-10 (20 clicks). NEXT TURN: jumps 11-12: (44,49)->(32,49); (32,49)->(32,37). Click map: x=20,26,32,38,44 for C1-5; y=19,25,31,37,43,49 for R1-6.

## Turn 115 (after A897, board 897)
Jumps 1-10 ALL executed (diffs 28/44 and 36/52 variants; 36/52 = select overlapped with adjacent-piece rings, jump still fine). Board 897 cell map confirms BFS state: blues (3,1),(2,2),(4,5),(4,6); A(3,5); B(5,6); cart empty (5,4).
Issued jumps 11-12: (44,49)->(32,49) B over bl(4,6); (32,49)->(32,37) B over A = CAPTURE => expect score 9.
Cell-map one-liner used (handy): sample b[y][x] at cell centers x=20,26,32,38,44 / y=19,25,31,37,43,49.

## Turn 116 (after A901, board 901)
CAPTURE happened (diff 64 = jump + A removed; jumper B now sole green at (3,4); A gone) but SCORE STILL 8. L9 win != one green — DELIVERY REQUIRED via cart (5,4) + east rail (rows 37-38). NEW RULE LEARNED: capture alone doesn't clear; sole green must be delivered somewhere east.
Blues now: (3,1),(2,2),(4,5),(4,6).
Issued: bl(4,6)->(4,4) over bl(4,5) [clicks (38,49),(38,37)]; G(3,4)->cart(5,4) over bl(4,4) [clicks (32,37),(44,37)]; then ACTION4 x4 to ride east (camera follows loaded cart; watch for destination/goal pad).

## Turn 117 (after A909, board 909)
Green boarded cart (905 = jump + camera scroll), rode east 4 (906-909). Board 909: loaded cart at cols 20-27 rows 35-41 on rail rows 37-38, mid-transit. NEW EAST PANEL revealed: walls rows 10 & 29, west wall col 26, extends east off-screen. Cells rows 12-15/18-21/24-27; cell cols start x=28 (+6 each). Contains: GREEN peg at top-left cell (rows 12-15, cols 28-31); purple seats at (rows 11-15 cols 46-49),(rows 11-15 cols 58-61),(rows 23-27 cols 34-37). L9 has MORE greens — not done. Rail continues east under panel; no dock visible yet.
Issued ACTION4 x6 to keep riding east; look for vertical rail/notch up into the new panel.

## Turn 118 (after A915, board 915)
Rode east 6 more. Board 915 (camera scrolled): mega-panel's EAST wall now visible at col 63. Panel is L-shaped: main body rows 10-29 (3 cell rows: y-bands 12-15,18-21,24-27), plus SE annex cols ~50-63 rows 29-41 (2 more cell bands 30-33, 36-39) — east two cell-columns (x 52-55, 58-61) form a 5-row grid. RAIL rows 37-38 ends at col 50 with opening into annex bottom band (rows 36-39) — cart will enter annex cells.
Pieces on screen: blues at (rows 18-21, cols 46-49) and (rows 18-21, cols 52-55); purple seats rows 11-15 (cols 10-13, 22-25), rows 23-27 (cols 34-37, 46-49, 0-1 partial). Green #next off-screen WEST (was top-left of panel). Cart+green still on rail at screen cols 21-26.
Issued ACTION4 x4: expect cart to enter annex bottom-left cell then maybe next cell east; then green disembarks north via jumps.

## Turn 119 (after A919, board 919) — L9 FULL SOLUTION
Mosaic stitched (boards 909-919, +6/board): mega-panel = cells c1-12 x r1-3 (rows y 12-15,18-21,24-27) + annex c11-12 x r4-5 (rows 30-33,36-39). West wall world x=26, cell c_k interior x=28+6(k-1). Seats (mids, immobile): (4,1),(6,1),(2,3),(8,3),(10,3). Blues (10,2),(11,2). GREEN#2 (1,1) cornered (uncapturable there; no moves). Cart+GREEN#1 docked at (10,5) outside annex west wall, jump-adjacent to (11,5).
BFS 29-jump WIN: [1-9] blue pair leapfrog west r2 ->(1,2),(2,2); [10] G2 S->(1,3); [11] G2 E over seat->(3,3); [12] bl(1,2)->(3,2); [13] G2 N->(3,1); [14,15] G2 E over seats->(5,1)->(7,1); [16-19] blue pair east ->(6,2),(7,2); [20] G2 S->(7,3); [21,22] G2 E over seats->(9,3)->(11,3); [23-26] blue pair east ->(10,2),(11,2); [27] bl(11,2) S over G2 ->(11,4); [28] G2 S over bl ->(11,5); [29] G1 cart E over G2 ->(12,5) CAPTURE.
CAMERA: current offset 60 (screen=world-60). Clicks screen-only => shuttle cart west 5 (ACTION3 x5, offset 30). Then click x for c_k = 6k-6 (c1 use x=1); y: r1=13,r2=19,r3=25,r4=31,r5=37. After jump 28: ACTION4 x5 (offset back 60), cart re-docks (10,5); jump 29 clicks (23,37)->(35,37).
SCHEDULE: T119: A3 x5 + jumps 1-7 (19 acts). T120: jumps 8-17 (20). T121: jumps 18-27 (20). T122: jump 28 + A4 x5 + jump 29 (9). Click list per jump in solver output above.

## Turn 120 (after A938, board 938)
T119 batch perfect: 5x ACTION3 (camera offset now 30), blue jumps 1-7 done — pair at (3,2),(4,2). Cell sample confirms solver state. Cart+G1 mid-rail at screen x21-26 (world 51-56).
Issued jumps 8-17 (20 clicks): 8 (4,2)->(2,2); 9 (3,2)->(1,2); 10 G2 (1,1)->(1,3); 11 G2 ->(3,3); 12 bl(1,2)->(3,2); 13 G2 ->(3,1); 14 G2 ->(5,1); 15 G2 ->(7,1); 16 bl(2,2)->(4,2); 17 bl(3,2)->(5,2). c1 clicks use x=1.
NEXT: T121 jumps 18-27: (18,19)(30,19); (24,19)(36,19); (36,13)(36,25); (36,25)(48,25); (48,25)(60,25); (30,19)(42,19); (36,19)(48,19); (42,19)(54,19); (48,19)(60,19); (60,19)(60,31). T122: (60,25)(60,37); A4 x5; (23,37)(35,37).

## Turn 121 (after A958, board 958)
Jumps 8-17 all executed. Sample: G2 (7,1); blues (4,2),(5,2); seats intact — exact solver state.
Issued jumps 18-27 (20 clicks): blues ->(6,2),(7,2); G2 S->(7,3), E->(9,3), E->(11,3); blues east ->(10,2),(11,2); bl(11,2) S over G2 ->(11,4).
NEXT T122 (final): jump 28 G2 (11,3)->(11,5): (60,25)(60,37); ACTION4 x5 (cart re-docks (10,5), camera offset back 60); jump 29 G1 cart->over G2->(12,5) CAPTURE: clicks (23,37)(35,37). Expect score 9 (or further delivery — check).

## Turn 122 (after A978, board 978)
Jumps 18-27 all executed. State: G2 (11,3); blues (10,2),(11,4); cart+G1 still west mid-rail.
Issued finale: jump 28 G2 (11,3)->(11,5) [(60,25)(60,37)]; ACTION4 x5 cart re-docks (10,5) camera offset 60; jump 29 G1 over G2 ->(12,5) CAPTURE [(23,37)(35,37)]. Expect score 9. If not: check board for delivery requirement (seats? another green? cart destination).

## Turn 123 — LEVEL 9 CLEARED (A987, score 8->9). L10 initial board 987.
L9 confirmed win rule: level clears when a green captures the LAST other green (exactly one green left).
L10 LAYOUT: TOP PANEL rows 2-9 cols 22-43: cells T1(24-27),T2(30-33 GREEN#1),T3(36-39). TOP RAIL rows 11-12 cols 7-57; left vertical cols 7-8 rows 13-40 -> horizontal rail rows 41-42 cols 7-22 entering BIG PANEL band r2; right vertical cols 55-56 rows 13-56 -> blue-loaded cart docked rows 56-63 (cart with BLUE peg inside!). Three EMPTY carts in notches under top rail: cart1 interior cols 18-21, cart2 interior 30-33 (ALIGNED UNDER T2), cart3 interior 42-45; frames rows 14-21.
BIG PANEL rows 32-63 cols 16-49: 5x5 cells c1..c5 x=18,24,30,36,42(+3 interior), r1..r5 y-bands 34-37,40-43,46-49,52-55,58-61. MISSING cell (c1,r2) = rail entry/cart dock. Pieces: blues (c4,r1),(c5,r1),(c2,r2),(c3,r3),(c1,r4); GREEN#2 (c5,r5).
KEY MECHANIC HYPOTHESIS: cart ON top rail has interior rows 10-13 = mid-band between T2 (rows 4-7) and cart2 notch interior (16-19). So blue cart parked under T2 = occupied mid; G#1 jumps S over it INTO cart2.
MASTER PLAN: (1) blue cart U up right rail to top rail, L to interior cols 30-33; (2) G#1 S into cart2; (3) cart2 U onto rail, L, D left vertical, R to dock at (c1,r2); (4) G#1 E over blue(c2,r2) -> (c3,r2); (5) in-panel jumps to put G#1 at (c5,r4); (6) G#2 jumps N over G#1 -> (c5,r3) CAPTURE = WIN. BFS phase 5 when there.
UNKNOWN: do empty notch carts respond to arrows (L8 left cart didn't move on U — reason unclear). TESTING: U x6, watch all 4 carts.

## Turn 124 (after A993, board 993)
U x6 results: press 1 lifted ALL THREE empty carts from notch band (16-19) to TOP-RAIL band (10-13, frames 9-14ish) — now flush under top panel wall; presses 2-6 only moved blue carts. TWO blue-loaded carts exist (second was off-screen south): blueA interior rows 22-25, blueB rows 28-31, both on right vertical cols 55-58, stacked.
RAIL NETWORK CORRECTED: three vertical stubs (cols 18-19,30-31,42-43) connect top rail (rows 11-12) to a MID RAIL rows 23-24 (cols 19-45, isolated from right vertical). Cart parking bands per stub: 10-13 (on-rail), 16-19 (notch/mid-stub = original), 22-25 (mid rail).
REVISED ESCAPE: need blueA interior at cols 30-33 band 10-13 (mid for jump) AND E2 empty at band 16-19 cols 30-33 (landing). Then G#1: T2 (rows 4-7) -S-> cart E2 (16-19). Then clear blueA aside, E2+green U to top rail, L to left corner, D left vertical (cols 7-8) to rows 41-42 rail, R dock at big panel (c1,r2) missing cell; disembark E over blue (c2,r2) -> (c3,r2); BFS in-panel; G#2 captures G#1 at (c5,r4) from (c5,r5) -> lands (c5,r3) = WIN.
TESTING NOW: U,U (blueA to top rail band 10-13, blueB trails at 16-19 on vertical), then L,L,L — observe whether L slides all on-rail carts, whether they stack/block, quantization of positions.

## Turn 125 (after A998, board 998)
U,U,L,L,L results: blueA turned right-corner onto TOP RAIL, now int cols 36-39 band 10-13. Empties compressed west: E1 int 6-9 (AT left corner), E2 12-15, E3 24-27. THREE blue carts on right vertical (supply column keeps feeding from below): B(16-19),C(22-25),D(28-31) bands.
MECHANICS LEARNED: carts block each other (stacking, no passing); L/R cascade all top-rail carts by 6px where free; U lifts ALL stub/mid carts to top rail (global poison after stub-parking); D drops stub-aligned top-rail carts one band (stubs at int cols 18-21,30-33,42-45; three bands 10-13/16-19/22-25); corner cart (6-9) descends left vertical on D.
ESCAPE GEOMETRY (v4): pre-click config: blueA at (30-33,10-13) + empty cart at (30-33,16-19); click G1 T2 (31,5) -> (31,17). Then R (blueA aside), U (GC to top rail), L xk (GC to corner 6-9; trailing carts scatter into stubs during descent — harmless), D x5 (left vertical bands to bottom rail 40-43), R x2 (dock at (c1,r2) int cols 18-21), disembark click E over blue (c2,r2) -> (c3,r2). CRITICAL: no cart may ever sit at corner 6-9 during a D before GC's descent; keep extra empties EAST of col 30 or in stubs.
IN-PANEL endgame after: BFS with G1 (c3,r2), G2 (c5,r5), blues (c4,r1),(c5,r1),(c2,r2),(c3,r3),(c1,r4); G2 captures G1 -> WIN. ALSO possible: stub capture (G2-cart jumps over G1-cart into empty cart, all stacked on one stub).
TESTING: R x4 to observe cascade + right-end behavior. Then design exact D.

## Turn 125 addendum — L10 MASTER SEQUENCE (worked out fully)
Position classes: stubs 18/30/42 & corner 6 all ≡6 mod 12; 6-spaced trains alternate classes; JAM at right end (54) then reverse-L retunes spacing/classes. bA@54 during D = drop-to-right-vert RISK (avoid). Corner 6-9 during D = left-vertical descent (avoid until GC's own descent).
SAFE PARKING: (42,b2/b3) east stubs; (30,b3) SHIELD (makes landing@(30,b2) D-immune; shield U-rises only if b2 free). Stub18 parking = cursed (U-lifts to west top rail). 3rd empty just needs to be EAST of 33 on top rail at escape time (trails harmlessly; sinks into stub18/42 during descent D's — harmless since no U afterward).
SEQUENCE from state [E1 6, E2 12, E3 24, bA 36] (= after this turn's R x4 it will be [30,36,48,54], i.e., mid-sequence):
R x5 total: [36,42,48,54]; L: [30,36,42,48]; D: E1->(30,b2), E3->(42,b2), E2@36+bA@48 safe; D: E1->(30,b3)=SHIELD, E3->(42,b3); R,R: [E2 42->48?? actual: [36,48]->[42,54]->[48,54]]; L,L,L: [42,48]->[36,42]->[30,36]; D: E2->(30,b2)=LANDING, bA@36 safe; L: bA->(30,b1)=MID. CLICK (31,5)->(31,17): G1 escapes T2 -> landing cart.
POST: R (bA->36), U (GC->(30,b1); shield rises to b2 — harmless), L x4 (GC->corner 6-9; trail bA->12 safe class), D x5 (GC down left vertical to bottom rail band 40-43; shield re-sinks; trail carts sink into stubs — all harmless), R x2 (GC 6->12->18 = DOCK (c1,r2)), CLICK (19,41)->(31,41)?? disembark: G1 jumps E over blue(c2,r2)@int cols 24-27 band rows 40-43 -> (c3,r2): select G1-in-cart (19-ish,41) dest (31,41). VERIFY coords at the time.
THEN in-panel BFS: G1(c3,r2) G2(c5,r5) blues (c4,r1),(c5,r1),(c2,r2),(c3,r3),(c1,r4); target G2-over-G1 capture => WIN.
THIS TURN already committed R x4 (safe, on-path). NEXT TURN: R,L,D,D,R,R,L,L,L,D,L + 2 escape clicks (13 actions), verifying board between.
