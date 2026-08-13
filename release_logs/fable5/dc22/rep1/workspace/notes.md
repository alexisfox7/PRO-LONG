# Game notes

## LEVEL 1 SOLVED (score 1) at action 28 via 20-action escort. Mechanics fully confirmed.

## Level 2 (board shifted down 1 row; reverse trip top box -> bottom box)
- Player (green II) at rows 21-22, cols 24-25 in top box (rows 19-24, cols 22-27).
- Blue A rows 21-24, red A rows 25-30, maroon 31-34 (cols 18-21); gray cols 8-11 rows 31-34; blue B slot/ghost rows 35-38; bottom box rows 39-44 cols 8-13 (target center rows 41-42, cols 10-11).
- Shape click coords still: red (48,19), blue (48,36).
- Committed 19 actions: Lx2, Dx6, redToggle, Lx5, blueToggle, Dx4.
- Note: no step bar visible at level start (row 63 all gray).

## Board layout (Level 1, initial)
- 64x64. Gray 'h' border rows 0-9 and 59-62; white '$' bar row 63.
- Left panel cols 0-31 (bg 'q'), right play area cols 34-63 (bg 'O'), dashed white divider cols 32-33 (2x2 dashes every 4 rows, rows 10-51).
- Right area objects (identical plus/cross shapes, white outline):
  - RED shape: rows 16-22, cols 41-55 (47 red cells)
  - BLUE shape: rows 33-39, cols 41-55 (47 blue cells)
- Left panel icons:
  - rows 18-23 cols 18-27: blue 4x4 block + gray box w/ YELLOW 2x2 center → legend? "select blue"?
  - rows 30-34 cols 8-21: gray(4)/red(6)/maroon(4) horizontal bar → maybe step budget/timer
  - rows 35-36 cols 8-11: scattered blue dots (dashed)
  - rows 37-43 cols 8-13: gray box w/ GREEN 2x2 center → button pressed state?

## Hypotheses
- H1: click object matching color shown in legend (blue). Testing: ACTION6(48,36) click blue center.

## Findings after Action 1 (clicked blue at 48,36 — CORRECT apparently)
- Instruction slot: rows 18-23, blue block cols 18-21 beside yellow-center box. Was SOLID before, became CHECKERED after correct click.
- Done slot: rows 34-37 cols 8-11 above green-center box (rows 38-43). Was checkered, became SOLID blue.
- Both shapes' white outlines disappeared (outline = selectable?).
- Row 63 bottom bar: (63,0) $→h. Step counter, 64 budget.
- Red/maroon bar rows 30-33 cols 8-21 (####nnnnnn>>>>) unchanged — meaning unknown (lives? queue?).
- Score still 0.

## Findings after Action 2 (clicked red at 48,19)
- Red 6x4 block moved from shelf (rows 30-33, cols 12-17) to Stack A (rows 24-29, cols 18-21), vertical now, resting on maroon.
- Area conserved (24 cells). Step bar -1 (63,1 $→h). Score 0.
- Panel model: Stack A cols 18-21 beside YELLOW box (rows 18-23 cols 22-27): blue ghost rows 20-23, red 24-29, maroon 30-33.
  Stack B cols 8-11 on GREEN box (rows 38-43 cols 8-13): blue 34-37, gray 30-33.
  Shelf at rows 30-33 spanned cols 8-21 initially: gray|red|maroon.
- Blue click: blue went from Stack A top slot to Stack B (onto green box, where its checkered ghost was).
- Hypothesis: clicking a shape advances matching color block along route toward green stack. Or toggles between stations.

## Action log
- Turn 1: ACTION6(48,36) click blue — blue delivered to green stack.
- Turn 2: ACTION6(48,19) click red — red moved into yellow-station column.
- Turn 3: ACTION6(48,19) click red again — red toggled BACK to shelf (30-33, cols 12-17). Toggle confirmed.

## Mechanics (confirmed)
- Click shape = toggle its color block between 2 fixed slots:
  - BLUE: slot A-top (rows 20-23, cols 18-21, beside yellow box) <-> slot B (rows 34-37, cols 8-11, on green box). Checkered ghost shows vacated/empty slot.
  - RED: shelf (rows 30-33, cols 12-17) <-> slot A-mid (rows 24-29, cols 18-21).
- Combos tried, no score: (blueA,redShelf) init; (blueB,redA); (blueB,redShelf).
- Turn 4: (blueA, redA) reached — full tower blue/red/maroon in column A. NO SCORE. All 4 toggle combos exhausted.
- Turn 5 probes: green box click = NO-OP. ACTION1 = green 2x2 PLAYER moved up 2 rows (40-41 -> 38-39, cols 10-11)!

## Player/escort model (turn 6)
- Green 2x2 player starts inside green box; arrows move it 2 cells/press.
- Route green->yellow: B column (blue slot rows 34-37, cols 8-11) -> gray 30-33 -> shelf right through red slot (cols 12-17) -> maroon (18-21) -> up red A slot (24-29) -> blue A slot (20-23) -> right into yellow box (GG at cols 24-25, rows 20-21).
- Escort plan (if blocks = corridors): blueB; Up x4; redShelf; Right x5; redA; Up x3; blueA; Up x2; Right x2. ~19 actions.
- TEST turn 6 result: player did NOT move into empty space. BLOCKS = CORRIDORS confirmed.
- Turn 7: full 20-action escort committed:
  blueB, Upx4 (to gray top rows 30-31), redShelf, Rightx5 (to maroon cols 20-21), redA, Upx3 (to red top 24-25), blueA, Upx2 (rows 20-21), Rightx2 (into yellow box GG at cols 24-25).
- If some move gets blocked, player position desyncs from plan — re-derive from board next turn.
- Shape geometry note: both play-area shapes are T/mushroom: 3 rows of 7-wide (top) + 2 rows of 13-wide (bottom). Red at rows 17-21, blue at rows 34-38, cols 42-54.

## LEVEL 2 actual layout (actions 29-47 were ALL no-ops; player never moved, clicks missed)
- Player II rows 30-31 cols 4-5, inside gray 4x4 block cols 4-7 rows 28-31.
- Solid blue 4x4 cols 8-11 rows 28-31 (right of player block).
- Ghost (checkered blue) shaft cols 4-7 rows 32-39 (4x8!) below player block.
- Upper corridor rows 24-27: gray 8-11 | red 12-19 (8w) | maroon 20-23 | red 24-31 (8w) | gray 32-35.
- Yellow GG goal box rows 12-15 cols 20-23 (above maroon segment; gap rows 16-23 = 8-tall shaft needed).
- Lower corridor rows 40-43: gray 4-7 | z 8-15 | C magenta 16-19 | z 20-27.
- Red icon box rows 52-55 cols 16-19 (red cup icon; gap rows 44-51 below magenta segment).
- Play shapes: MAGENTA rows 20-24 (click 52,21), BLUE rows 38-42 (click 52,39). Red NOT clickable this level.
- Step bar row 63: 7 consumed after 19 acts (bar semantics unclear - watch).
- Turn: probing both clicks to learn toggle slots.

## Level 2 toggle semantics (probed, actions 48-49)
- MAGENTA click (52,21): toggles the two z 8x4 arms of lower corridor between HORIZONTAL (cols 8-15 & 20-27, rows 40-43) and VERTICAL shafts at cols 16-19 (up: rows 32-39, down: rows 44-51 reaching red box at 52-55). Hub C (16-19,40-43) fixed. Currently VERTICAL after probe.
- BLUE click (52,39): toggles blue between slot (cols 8-11, rows 28-31, half-checker when empty) and shaft (cols 4-7, rows 32-39). Currently SHAFT (solid) = player can descend.
- Expected: upper corridor red 8x4 arms mirror this around maroon hub (cols 20-23): vertical would give up-shaft rows 16-23 to YELLOW GOAL. Red toggle likely enabled by red pickup in red box.
- Phase A committed (19 acts): D x5 (to rows 40-41), magenta->horizontal, R x6 (to hub 16-17), magenta->vertical, D x6 (to red box rows 52-53).

## Phase A SUCCESS (actions 50-68)
- Player reached red box (rows 52-53, cols 16-17). Red icon consumed -> NEW RED SHAPE in play area rows 29-33 (click 52,30).
- Current: blue = shaft mode (solid cols 4-7 rows 32-39); magenta arms = VERTICAL; step bar 15/64 used.
- Return route (37 acts, split 20+17):
  T1 (committed): Up x6 (to hub 40-41), magenta->horizontal, Left x6 (to gray cols 4-5), Up x6 (climb blue shaft to gray block 28-29), blue->slot.
  T2 (next): Right x2 (into blue slot 8-9), Up x2 (corridor gray 24-25), Right x6 (to maroon hub 20-21), red->vertical (52,30), Up x6 (shaft 16-23 into yellow box rows 12-13).

## Leg 1 done (actions 69-88): player rows 28-29 cols 4-5, blue=slot mode. Bar 22/64.
## Leg 2 committed: Rx2, Ux2, Rx6 (to maroon hub rows 24-25 cols 20-21), red toggle (52,30), Ux6 -> yellow box. Expect score 2.

## Leg 2 (actions 89-105): player at rows 12-13 cols 20-21 INSIDE yellow box, but score still 1 - not on GG marker (cols 22-23). Win requires standing ON the 2x2 goal marker. Committed ACTION4.
## Bar: 28/64 used.

## LEVEL 2 SOLVED (score 2) at action 106. Standing ON the 2x2 goal marker = win, confirmed again.
## Post-win frame shows [frame 1/1]; board after win is NOT the next level layout (learned in L2: never plan from post-win frame).
## Turn: no-op click ACTION6(62,10) to reveal true Level 3 board.

## LEVEL 3 layout (revealed action 107; fresh bar 1/64)
- Player II: cols 30-31, rows 18-19 in box cols 28-31 rows 16-19 (top-right).
- GOAL GG: cols 32-33, rows 38-39 in box cols 30-33 rows 36-39.
- Main corridor rows 24-27: gray 4-7 | BLUE solid 8-11 | red 12-19 | maroon hub 20-23 | red 24-31.
- Blue ghost slots: (cols 24-27, rows 16-19) left of player box; (cols 4-7, rows 20-23) below top-left box; (cols 12-15, rows 40-43) bottom cluster. Blue has 4+ slots -> click may CYCLE.
- Purple ghosts: A vertical cols 16-19 rows 32-39; B horizontal cols 24-33 rows 32-35 (above goal box). Purple pickup icon (solid, 6 cells) in box cols 16-19 rows 40-43.
- Checkered magenta 2x2 pads: box cols 4-7 rows 16-19 (pad at 6-7,16-17); box cols 12-15 rows 44-47 (pad at 12-13,46-47). Hypothesis: teleport pads?
- Red arms 8w around maroon hub: vertical form would be up-shaft cols 20-23 rows 16-23, down-shaft rows 28-35 (mirrors L2).
- Shapes/clicks: red (50,17) rows 16-20; blue (50,26) rows 25-29; magenta (52,35) rows 34-38. No purple shape yet (needs pickup).
- Turn: probe clicks magenta, blue, red (in that order).

## Level 3 probe results (actions 108-110)
- MAGENTA click: swaps checker phase of both 2x2 pads only. Hypothesis: teleport when player ON pad.
- BLUE click: state A (solid corridor slot 8-11 rows 24-27; 3 outer slots ghost) <-> state B (3 outer slots SOLID: (24-27,16-19),(4-7,20-23),(12-15,40-43); corridor ghost). Currently B.
- RED click: horizontal arms (12-19 & 24-31, rows 24-27) <-> vertical shafts cols 20-23 (up 16-23, down 28-35). Currently VERTICAL.
- Master plan: P1 Lx4 Dx3 (via blue 24-27 + up-shaft to hub); P2 red->horiz, blue->A, Lx9 (to gray 4-5); P3 blue->B, Ux4, Rx1 (onto pad1 6-7/16-17), magenta click = teleport test.
- Then: pad2 (12-13,46-47) -> Ux2-3 via blue slot (12-15,40-43) -> Rx2 purple box pickup -> return via teleport -> blue A, Rx7 to hub, red vert, Dx5, purple->B, Rx6, Dx2 onto GG (32-33,38-39).
- Turn committed (20): Lx4, Dx3, redC, blueC, Lx9, blueC, Ux1. Player should end rows 22-23, cols 4-5.

## Leg 1 SUCCESS (actions 111-130): player rows 22-23 cols 4-5, blue=B, red=HORIZONTAL. Bar 10/64.
- Pad1 checker at (rows 16-17, cols 6-7) in gray box 4-7/16-19; pad2 at (rows 46-47, cols 12-13) in gray box 12-15/44-47. Purple icon at rows 42-43, cols 16-19.
## Leg 2 committed (11): Ux3 (into gray box, rows 16-17 cols 4-5), Rx1 onto pad1, magenta(52,35) TELEPORT TEST; then assuming teleport to pad2: Ux3 (via blue slot 12-15/40-43 to rows 40-41), Rx2 (cols 16-17), Dx1 onto purple icon -> pickup, expect purple shape spawn.
- If teleport fails: trailing moves mostly blocked near pad1; re-derive next turn.
- After pickup remaining plan: back to pad2, magenta teleport to pad1, Dx1 Lx1? no — route: pad2->blue slot->? Actually return: from purple box Ux1 Lx2 Dx3 to pad2, magenta click, at pad1: Dx3 (blue slot B), then blue->A? No: need corridor. blue->B keeps slot 4-7/20-23; Dx3 to rows 22-23, then blue->A (corridor 8-11 solid) blocks exit? Corridor route: player in slot 4-7 can go down? slot rows 20-23, gray 4-7 rows 24-27 below. Dx1 to 24-25, blue->A, Rx9 to hub 22-23? red->vert, Dx5 to rows 34-35? purple->B (bridge 24-33/32-35), Rx? Dx? onto GG (32-33,38-39). Refine next turn.

## Leg 2 SUCCESS (actions 131-141): TELEPORT CONFIRMED (magenta click while ON pad warps player between pads).
- Player rows 42-43 cols 16-17; purple icon consumed -> purple shape rows 43-47 cols 45-57, click (51,45). Bar 14/64.
- Both purple slots ghost: A vertical (16-19, 32-39), B horizontal (24-33, 32-35). Red=HORIZONTAL, blue=B.
## Endgame committed (19): purple(51,45)->hope A solid; Ux5 (climb A shaft to rows 32-33); red(50,17)->vertical (down-shaft 20-23/28-35); Rx3 (into red shaft cols 22-23); purple(51,45)->B (bridge 24-33/32-35); Rx5 (to cols 32-33); Dx3 (through goal box onto GG 32-33/38-39). Expect SCORE 3.
- Risk: purple first click might give B not A -> Up blocked at rows 40-41, desync but recoverable (player stuck in box; re-derive).

## Endgame stall (actions 142-160): PURPLE click toggles BOTH slots A+B together solid<->ghost (NOT A<->B). First click solidified both (climb+bridge worked); my 2nd click at step 11 ghosted everything -> Rx5 blocked. Player rows 34-35 cols 22-23 (red shaft bottom), red=VERTICAL. Score 2.
## Fix committed (9): purple(51,45) re-solidify, Rx5 across B bridge (rows 34-35 -> cols 32-33), Dx2 onto GG (32-33,38-39) = expect SCORE 3; then no-op click (62,10) to reveal Level 4 true board.

## LEVEL 3 SOLVED (score 3) at action 168 (final Dx2; trailing reveal click discarded - runner stops list on win).
## KEY LEARNING: post-win [settled] board IS the next level layout (verified L2->L3 identical except bar cell). No reveal click needed. Also: no-op clicks DO consume bar.

## LEVEL 4 layout (from settled board after action 168; bar 0/64)
- Divider now cols 38-39 (white dashes); left puzzle cols 0-37, play area cols 40-63.
- Player II rows 18-19 cols 4-5 in gray box (4-7, 18-21). BLACK 'O' corridor rows 20-21 cols 8-23 (black=passable?) to tall gray column (24-27, 18-29).
- Pad1 Cz (4-5, 24-25) in gray box (4-9, 24-27). Off-white 8 bridge (8-13, 28-29). Gray block (4-9, 30-37). Off-white 8 (4-9, 38-39).
- Pad2 zC (18-19, 32-33) in gray box (16-19, 30-33).
- Orange bar (16-31, 40-41) -> gray box (28-31, 42-45) with GG goal (30-31, 44-45).
- Play shapes: MAGENTA T rows 17-21 cols 46-58 (click 52,19); YELLOW blob n=40 rows 25-31 cols 43-49 (click 46,28); gray 6x6 box (54-59, 26-31) = future shape slot?
- Gaps: player box not connected to pad1 box (rows 22-23 q); gray column bottom (rows 28-29) dead-ends; bottom-left 8 (38-39) doesn't reach orange (starts col 16).
- Probing: yellow click (46,28), then magenta click (52,19).

## L4 probe results (actions 169-170)
- YELLOW click (46,28): BOTH off-white '8' platforms slide RIGHT 2 cols per click. Now: block1 rows 28-29 cols 10-15 (orig 8-13); block2 rows 38-39 cols 6-11 (orig 4-9).
- MAGENTA click (52,19): swaps pad checker phases = teleport pads (pad1 rows 24-25 cols 4-5; pad2 rows 32-33 cols 18-19), as L3.
- The whole-board 14-row shift seen after click 1 was a render/scroll artifact, NOT a mechanic (board2 vs base = only platform+pad diffs).
- Bar 2/64. Black 'O' corridor rows 20-21 cols 8-23 assumed passable (only exit from player box).
- Platform tracks: block1 track rows 28-29, bounded right by column cols 24-27 -> max cols 18-23 (4 more clicks). Block2 track rows 38-39.
- CONFLICT WATCH: block1 orig position was the pad1-box descent link; both platforms move together. May need platforms to bounce/wrap, or ride them (platform carries player?). Test by observing.
- Route plan: column bottom (24-25,28-29) -> L onto block1 bridge (18-23) -> D2 to pad2 -> teleport -> pad1 -> descend left cluster (needs block1 back?? or ride block2 to orange) -> orange bar -> goal box GG (30-31,44-45).
## L4 leg 1 committed (19): D1, Rx10 (black corridor to column cols 24-25), Dx4 (to rows 28-29), yellowx4 (block1 -> cols 18-23 bridge).

## L4 leg 1 result (actions 171-189)
- Player STUCK at rows 20-21 cols 6-7: black 'O' corridor rows 20-21 cols 8-23 NOT passable (9 R's blocked).
- Platforms slid right per yellow click; on 4th click they DOCKED and turned ORANGE, view snapped back to normal (undocked phase renders world shifted up 14 - cosmetic).
- Docked positions: block1 (cols 18-23, rows 28-29) bridges column (24-27) -> pad2 box top (cols 18-19); block2 (cols 14-19, rows 38-39) rests on orange bar left end.
- PROBLEM: even with bridges, pad1 box & pad2 box networks dead-end away from orange bar/goal; and player can't exit start box at all.
- Pads now: pad1 zC/Cz (4-5,24-25), pad2 Cz/zC (18-19,32-33).
- Bar 9/64. Untested: gray 6x6 play-area box (54-59, 26-31) click (56,28).
## Probes committed (3): R (is corridor open now that platforms docked?), click (56,28) gray box, R again.

## L4 probes (actions 190-192)
- R blocked (corridor closed). GRAY BOX click (56,28): spawned off-white 8 2x2 platforms INSIDE black regions: corridor rows 20-21 got 8s at cols 8-9 and 22-23; orange bar rows 40-41 became 8s cols 16-21 & 26-31 with BLACK gap cols 22-25. Then R moved player ONTO corridor platform (rows 20-21, cols 8-9).
- Model: black = void crossed by rideable 8 platforms; docked platforms became static orange track. Gray box = platform spawner/toggler.
- Bar 11/64. Committed: yellow click (does it advance corridor platforms, carrying player?), then R.

## L4 actions 193-194
- YELLOW click while docked = platforms RESET to original spots (off-white). Yellow cycle period 5: P0 orig -> +2 -> +2 -> +2 docked(orange) -> reset. Corridor 8-platforms (rows 20-21) NOT affected by yellow.
- R still blocked (black next to player). Player rows 20-21 cols 8-9 on corridor platform.
- Bar 12/64. Testing: gray box click again (advance corridor platforms? carrying player), then R.

## L4 SEESAW mechanic (actions 195-196)
- GRAY click count g: corridor 8-bridge grows 2 cols per side per click; bar 8s shrink same. g=0 corridor black 8-23/bar full orange 16-31; g=2 now (corridor black 12-19, bar black 20-27). g=4 = corridor fully bridged, bar fully void. Unknown: does g cycle 4->0?
- Player rode R onto new cells: rows 20-21 cols 10-11. Yellow state y=0 (block1 8-13@28-29, block2 4-9@38-39). Bar 13/64.
## Full route plan
A: gray x2 (g=4), Rx7 (cross corridor to column cols 24-25), Dx4 (column bottom 28-29). [this turn, + yellow x5]
B: yellow x5 -> block1 docks 18-23 orange bridge; walk Lx1-3 onto it, Dx2 -> pad2 (18-19,32-33); magenta click -> teleport to pad1 (4-5,24-25).
C: yellow x1 (reset y=0; block1 back to 8-13@28-29 under pad1 box); D,Rx2,D (onto block1), Dx1 (gray block 8-9@30-31), Dx3 (to 36-37), D (onto block2 8-9@38-39).
D: yellow x5 with player ON block2 = RIDE test (platform carries player?) -> docked 14-19, player ~18-19@38-39.
E: gray x1 (hope g cycles ->0, bar full orange); D (onto bar 40-41), Rx6 (to cols 30-31), Dx2 -> GG (30-31,44-45). WIN.
## Committed (18): grayx2, Rx7, Dx4, yellowx5.

## Phase A SUCCESS (actions 197-214): corridor fully orange (static), player column bottom (24-25,28-29), block1 docked 18-23@28-29, block2 docked 14-19@38-39, bar rows 40-41 fully void. Budget 21/64.
## Phase B+C committed (18): Lx3 (onto block1 to cols 18-19), Dx2 (pad2 32-33), magenta(52,19) teleport->pad1 (4-5,24-25); yellow(46,28) reset platforms to P0 off-white (block1 8-13@28-29, block2 4-9@38-39); D, Rx2, Dx6 (descend: pad1 box -> block1 -> gray block -> block2, end rows 38-39 cols 8-9); yellow x2 = RIDE TEST (if platforms carry player, ends cols 12-13; if not, still on block2 at 8-13, ends cols 8-9).
## Remaining: yellow x3 (finish dock 14-19, player ~18-19), gray x1 (hope g cycles 4->0 restoring orange bar), D onto bar, Rx5-6, Dx2 onto GG. WIN expected.

## Phase B+C SUCCESS (actions 215-232): teleport pad2->pad1 worked; descent complete; player rows 38-39 cols 8-9 ON block2 (8-13, y=2). PLATFORMS DO NOT CARRY PLAYER (2 yellow clicks, player cols unchanged) - but player stays on if platform still under him; WALK between clicks instead.
- Bar 28/64. g=4 (bar void), corridor stays orange permanently.
## Endgame committed (18): Rx2 (to 12-13), [yellow, R] x3 (leapfrog: platform +2, walk +2; y=5 dock 14-19, player 18-19), gray(56,28) hoping g cycles 4->0 (bar restored orange), D (onto bar 40-41), Rx6 (to cols 30-31), Dx2 -> GG (30-31,44-45). Expect SCORE 4.
- If gray doesn't cycle: D blocked, player parks at 18-19 on docked block2; re-derive.

## Actions 233-250: leapfrog worked; player rows 38-39 cols 18-19 on docked orange block2 (14-19). Gray click at g=4 DECREMENTS (bounce): bar now g3 state (8s at 16-17 & 30-31). D/Rx6/Dx2 all no-op safely. Bar 36/64.
## Committed (12): gray x3 (g3->g0, bar full orange 16-31), D (onto bar 40-41 @18-19), Rx6 (to 30-31), Dx2 -> GG. Expect SCORE 4.

## LEVEL 4 SOLVED (score 4) at action 262 (~48 effective actions used of 64 budget).
- L4 total mechanics: gray box = seesaw platform bridges (corridor grows / bar shrinks, bounces at extremes); yellow = slide 2 big platforms right 2/click, dock->orange->reset cycle (period ~6); magenta = pad teleport; platforms do NOT carry player - leapfrog (walk to leading edge, click, walk).
## L5: post-win board is a SCROLL TRANSITION composite (h band rows 33-40 splits old L4 top / new L5 bottom). Cannot plan from it. Committed no-op click (62,10) to reveal true L5 board.
- Visible L5 hints (bottom fragment): pad zC/Cz at rows 47-48 cols 22-25ish, gray box below it, orange column rows 51-57 cols 22-25, white $ floor rows 55-57 cols 3-19.

## LEVEL 5 layout (revealed action 263; bar 1/64)
- Player II rows 34-35 cols 30-31 in gray box (30-33, 34-37); blue GHOST shaft checker cols 26-29 rows 34-37 left of player.
- Pad A (24-25, rows 6-7) atop orange column cols 22-25 rows 10-19 (partially checkered rows 14-19). Pad B (10-11, rows 34-35) in box (10-13, 34-37) above solid blue column (10-13, 38-41) + gray box (42-45).
- Purple PICKUP box (10-13, rows 18-21). White $ slab rows 14-17 cols 3-19; white col 3-6 rows 14-25; white rows 26-29 cols 6-18. Red 'n' ring rows 24-31 cols 2-10 (unknown).
- Black corridor rows 44-45 cols 14-29. Purple ghost column cols 26-29 rows 46-53; purple SOLID bridge rows 50-53 cols 14-23. GOAL GG (10-11, rows 50-51) in box (10-13, 50-53). 8-platform (14-19, rows 54-55).
- Right shapes: yellow (47,22); gray 6x6 (56,22); legend row 28-31: ( f ( f quads cols 43-61; red bar (54,35); blue T (53,41); magenta T (52,48).
## Probes committed (5): blueT(53,41), magentaT(52,48), redbar(54,35), yellow(47,22), gray(56,22). Diff each.

## L5 probe results (actions 264-268). NORMALIZED coords (player anchor 30-31/34-35); views scroll +-, always re-anchor on player!
- blueT (53,41): toggles blue block: (24-27,34-37 beside player, now SOLID) <-> (8-11,38-41 below pad B box, now ghost).
- magentaT (52,48): pad phase swap. Pad A (20-21,6-7) box (20-23,6-9); pad B (8-9,34-35) box (8-11,34-37).
- redbar (54,35): ZERO effect - inert (needs red pickup? red 'n' ring icon rows 24-31 cols 0-8 on white floor = probable pickup).
- yellow (47,22): slides 8-platform (rows 54-55) right 2 (now cols 14-19).
- gray (56,22): spawned corridor 8s at ends of black corridor rows 44-45 cols 12-27 (now 8s at 12-13 & 26-27).
- Topology: START cluster {player box (28-31,34-37), blue (24-27,34-37), gray (24-27,30-33)} SEALED - gap rows 24-29 cols 24-27 to upper gray box (24-27,20-23). TOP cluster: pad A box -> orange column (20-23,10-21) -> white slab (rows 14-17) -> purple pickup box (8-11,18-21) + white col -> white floor (26-29) -> red ring. CORRIDOR cluster: pad B box -> blue col (8-11,38-41) -> gray (8-11,42-45) -> corridor (44-45) -> purple ghost col (24-27,46-53) -> purple bridge (12-21,50-53) -> GOAL GG (8-9,50-51).
- UNRESOLVED: how to exit start cluster. Legend quads rows 28-31: '(' cols 43-46, 'f' 48-51, '(' 53-56, 'f' 58-61 - unprobed clickables?
## Committed (7): Lx2 (onto blue), Ux3 (gray box climb, 3rd U expect BLOCKED at rows 28-29), click quad1 (44,29), click quad2 (49,29).

## L5 actions 269-275
- Climb confirmed: player world (30-31, 26-27) in gray box (24-27,30-33); 3rd U BLOCKED. Gap rows 24-29 cols 24-27 confirmed sealed.
- CLICKS ARE WORLD COORDS (engine maps through scroll). Legend buttons world rows 28-31: '(' cols 42-44(no-op), 'f' 46-49, '(' 51-54, 'f' 56-59.
- f-button (48ish,29) click = RED SPRITE moved: from white floor (rows 24-31, cols 0-8 ring shape) UP into white column (rows 22-27, cols 0-7, rotated). Sprite = mobile obstacle/entity on white network (floor rows 26-29 cols 1-16, column cols 1-4 rows 14-29, slab rows 14-17 cols 1-17).
- Hypothesis: f-buttons steer red sprite along white path; sprite may be key/pickup enabling redbar (inert), which may bridge the start gap.
## Committed (3): f2(57,29) x2, f1(48,29) - observe sprite motion per button.

## L5 actions 276-278: f2 (57,29) INERT (x2 no-op). f1 (48,29) advances red sprite UP white column ~4 rows/click (now rows 16-23, cols 0-7). Sprite = path follower on white network.
- Hypothesis: sprite walks floor->column->slab->orange column-> maybe parks in start gap (24-29,24-27) as bridge, or fetches/enables something.
## Committed (5): f1 x5 - advance sprite, map its path.

## L5 actions 279-283: f1 advanced sprite onto slab (rows 13-19 after 1st click); remaining 4 clicks hidden (render cut top rows 4-22, sprite offscreen above row 23). Sprite presumably walking slab rightward toward orange bridge/column.
## Committed (5): f1 x4 (continue path), then U (blocked no-op, hoping render recenters on player to reveal top rows).

## L5 actions 284-288: sprite=RING (donut collar around white path) now parked at slab/column corner (rows 12-19, cols 0-7) - TERMINUS, extra f1 clicks no-op. White floor now clear. Step bar shows only 2 used?! (may count only player moves - budget not a concern).
## NEW HYPOTHESIS: blue block toggle-relocation CARRIES standing player (unlike L4 slides). Test: player D,D from gray box onto blue (34-35, 26-27), click blueT -> blue jumps to (8-11,38-41); if carried, player lands next to pad B cluster; U into pad B box.
## Committed (4): D, D, blueT(53,41), U.

## L5 actions 289-292: CARRY TEST FAILED + new blueT rule
- D,D onto blue slot A (player 34-35,26-27 norm). blueT click WHILE STANDING ON A: full toggle DID happen (A->ghost, B->solid, 14-cell diff). Player NOT carried (stayed put, standing on ghost A).
- Next move (U): toggle REVERTED (A solid, B ghost again) + step bar row63 cols 2-4 $->h. RULE: blueT toggle is unstable/reverts if player occupies the source slot when toggled; to relocate blue permanently, click while player is OFF the blue slots (proven: action-264 toggle B->A persisted 28 actions).
- Current state: blue SOLID at A (34-37,24-27 norm), ghost at B (38-41,8-11). Player in start gray box (32-33,26-27).
- NORMALIZED frame (GG anchor rows 50-51 cols 8-9). Raw last board = norm cols +2, rows +0.
- Route sketch: corridor cluster needs blue at B (padB->slotB->gray->corridor 44-45, bridged by gray-button 8s) then purple column (GHOST - needs purple pickup in TOP cluster) -> bridge -> GG. Start exit STILL unsolved.
- Leads: quad3 '(' (raw cols 53-56 rows 28-31) UNPROBED - may drive ring the reverse direction (slab connects RIGHT to orange column -> down to start gap!). Redbar re-probe now ring is at terminus.
## Committed (3): quad3(55,29) x2, redbar(52,35).

## L5 actions 293-295: QUAD3 = ring REVERSE driver!
- quad3 (55,29) x2: ring moved RIGHT along slab +4 cols/click (now collar rows 13-19, centered cols ~8-15). f1=leftward, quad3=rightward.
- redbar (52,35): STILL inert (0 diffs) even with ring parked/moving.
- Slab (rows 14-17) ends col 17 -> orange bridge (rows 14-17, cols 18-23) -> orange column (cols 20-23, rows 10-21) -> gray (24-27, rows 20-23) -> START GAP (rows 24-29, cols 24-27). If ring rides orange down, it may bridge the gap = start exit!
- Clicks are WORLD coords: buttons stay at world rows 28-31 regardless of render scroll. quad3=(55,29).
## Committed (5): quad3 x5 (drive ring right/down toward orange column and start gap).

## L5 actions 296-300: quad3 x5 -> ring advanced 2 more steps then STOPPED
- Click 1: ring to cols 12-19 (slab). Click 2: moved again (render scrolled, ring now off-screen above world row 23). Clicks 3-5: total no-ops (raw boards identical; click 3 only ticked step bar row 63 by 1).
- Ring parked at slab right end / orange junction (world cols ~16-23, rows 13-19) = quad3 TERMINUS. It does NOT auto-continue onto orange column.
- Start gap (rows 24-29, cols 24-27) still open 'q' - NOT bridged.
- Step bar row 63: 6 'h' consumed of 58; budget fine.
- Camera follows player; world rows <23 cropped in current renders. Blocked move re-renders full world (R is blocked for player at 32-33/26-27).
## Committed (2): R (blocked, reveal render), redbar(52,35) re-probe with ring at right terminus.

## L5 actions 301-302: REDBAR WORKS at junction!
- Blocked R revealed ring collar at slab right end rows 14-19 cols 13-19 (quad3 terminus).
- redbar(52,35) click: ring PIVOTED at slab/orange corner - bottom lobe (rows 18-19) rotated to top (row 13, cols 15-19). Redbar = advance/rotate ring at junction (was inert when ring elsewhere).
- Hypothesis: repeated redbar clicks walk ring onto orange column (cols 20-23) and DOWN toward gray (20-23) and start gap (24-29 cols 24-27).
## Committed (6): redbar x6.

## L5 actions 303-308: redbar x6 ALL NO-OP (only 1 step-bar tick)
- The action-302 pivot was a ONE-TIME step; ring parked rows 13-18 cols 12-19 (pivoted pose at slab/orange junction), redbar inert again.
- THEORY: the 4 legend buttons + redbar are context-sensitive to ring position/network. quad1 '(' and f2 'f' were probed only when ring was elsewhere - maybe they drive ring on ORANGE network, active now.
- Button WORLD coords (fixed): quad1 41-44, f1 46-49, quad3 51-54, f2 56-59 (rows 28-31); redbar rows 34-36 cols ~48-56; blueT rows 39-43; magentaT rows 46-50.
## Committed (3): quad3(53,29), quad1(43,29), f2(58,29) - retry each with ring at junction.

## L5 actions 309-311: quad3/quad1/f2 with ring at junction pose - ALL still no-op.
- Ring is at a hard terminus (slab/orange junction, pivoted pose). No button moves it. Orange column may not be ring-traversable.
- NEXT: play-area direct clicks never tested. Probing: pad B tile (8,34), pad A tile (22,6), ring body (16,15). Hypotheses: pad click = teleport destination select / ring click = grab or activate.
## Committed (3): ACTION6(8,34), ACTION6(22,6), ACTION6(16,15).

## L5 actions 312-314: play-area clicks (padB, padA, ring body) - ALL no-op (ring click only ticked bar).
- Pads and ring are not clickable. Step bar now 7h; bar ticks look sporadic (not per action) - maybe wall-clock. Not a concern yet.
- NEXT LEAD: gray button clicked only ONCE in L5 (spawned 8s at corridor rows 44-45 ends). L4 gray was multi-click seesaw with TWO-SIDED effect. Maybe repeated grays extend corridor 8s inward AND/OR bridge the start gap (rows 24-29 cols 24-27 between gray boxes).
## Committed (4): gray(56,22) x4 - watch corridor 8s AND the start gap each frame.

## L5 actions 315-318: GRAY CYCLE MAPPED (corridor rows 44-45, cols 12-27)
- g1(earlier): 8s at ends 12-13,26-27. g2: +14-15,24-25. g3: +16-17,22-23 (gap 18-21 left). g4: DOCKED - entire 12-27 solid ORANGE bridge. g5: reset to g3 state (8s 12-17,22-27, gap 18-21).
- Current: g3-equivalent state; ONE more gray click re-docks the full orange corridor bridge.
- Corridor route segment solved on demand. Start escape still open.
- Ring at orange junction does not react to gray. Untested combos: yellow multi-click cycle; blueT x2 while standing on ghost slot A (swap-carry hypothesis).
## Committed (4): D, D (onto blue slot A), blueT(53,41) x2 - second click may swap block AND player to slot B.

## L5 actions 319-322: blueT x2 while standing on A
- D,D: player walked to slot A BOTTOM half (36-37, 26-27) - slot A is 4x4 fully walkable.
- blueT click 1: A->ghost (held), B->SOLID. Player stays. blueT click 2: PURE NO-OP (no swap-carry, no revert). Revert only fires on player MOVE.
- Init-vs-now diff: initially BOTH blue slots were checker ghosts; initial player pos was (34-35, 30-31) right gray box; ring has left the white floor (floor now clear/walkable); step bar 11h used.
- Blue conclusions: blueT works remotely (toggle persists if player off-slots). Use later: set B solid before walking pad B -> slot B -> gray -> corridor.
- NEW IDEA: L4's seesaw trigger was a PLAY-AREA gray box click. L5 start gap (24-29, cols 24-27) lies exactly between upper gray box (20-23) and lower gray box (30-33) = potential local seesaw pair. Probing direct clicks: upper box (26,22), lower box (26,31), gap (26,26).
## Committed (3): ACTION6(26,22), ACTION6(26,31), ACTION6(26,26).

## L5 actions 323-325: play-area gray box clicks all no-op (first click only settled blue back to A-solid; ANY non-blueT click settles held toggle).
## Frame analysis findings:
- blueT 14-frame anims = iris-masked toggle animation, no hidden content.
- redbar click ALWAYS attempts a ring pivot: at floor it BOUNCED (frames wiggle, settle back); at slab junction it succeeded once (+1 shift), now blocked again.
- Ring path topology: bottom-left corner (floor rows 26-29 x column cols 1-4) is a JUNCTION. f1 = up/left branch (took ring up column to slab corner, then... quad3 took slab-right). quad3 = right/down branch. From initial position quad3 would have driven ring RIGHT ALONG FLOOR - never tried!
- KEY GEOMETRY: ring collar on floor spans rows 24-31 = exactly start gap (24-29) + lower box top (30-31). Floor rows 26-29 sits directly above lower gray box rows 30-33 (cols 24-27). Escape hypothesis: park ring at floor right end / beyond via redbar pivots -> collar lobes bridge cols 17-27 rows 24-31 -> player walks out (up from box onto floor or along collar lobe).
## Committed (6): f1(48,29) x6 - retrace ring: junction -> slab-left -> corner -> down column toward floor.

## L5 actions 326-331: f1 x6 from junction: click 1 moved ring once (render scrolled), clicks 2-6 NO-OP. Ring stuck somewhere above world row 23 (render cropped).
- f1 may not be a reverse driver; possibly undid the redbar pivot only, or one-way path semantics still unclear.
## Committed (1): D (blocked at rows 38-39 under slot A) to force full re-render and locate ring.

## L5 action 332: RING IS A GRABBER - redbar pivot HOOKED it onto the orange column!
- The single successful f1 click (action 326) dragged ring AND orange column LEFT 4: column now cols 16-19 (was 20-23), ring collar rows 13-18 cols 8-15.
- f1 stalls further left: ring collar would overlap purple pickup box (rows 18-19, cols 8-11) - collision block.
- Column original position: cols 20-23 rows 10-21 (ladder from pad A box down to upper gray box). Column is 4 wide x 12 tall.
- Open Qs: can quad3 drag it right past original spot (cols 24-27 overlaps upper box rows 20-21 - maybe blocked)? Does redbar re-pivot/unhook or move coupling vertically?
## Committed (3): quad3(53,29) [drag right], redbar(52,35) [pivot], quad3(53,29) [drag right again]. Diff each.

## L5 actions 333-335: drag limits mapped
- quad3#1: dragged ring+column RIGHT 4 back to original (column 20-23, collar 12-19). redbar: no-op at this pose. quad3#2: no-op (column at 24-27 would overlap upper gray box rows 20-21 - collision).
- Column shuttle: cols 16-19 <-> 20-23 ONLY. Blockers: purple pickup box (left, collides with collar), upper gray box (right, collides with column).
- Purple system insight: bridge (50-53, 12-21) SOLID vs column (46-53, 24-27) GHOST = anti-phase; purple toggle likely swaps them. Also 2-col gap (22-23) between bridge and column at rows 50-53.
- Only untested mechanism: YELLOW multi-click cycle (platform rows 54-55, at cols 14-19, 6-wide).
## Committed (4): yellow(47,22) x4 - map slide/dock cycle.

## L5 actions 336-339: yellow cycle mapped
- Platform slides right 2/click: 14-19 -> 16-21 -> 18-23 -> 20-25 -> click4 DOCKS ORANGE at cols 22-27 rows 54-55 (below purple column). = endgame ferry/extension piece.
## Hidden-pad-at-start hypothesis DISPROVED (boards 269+: right box is plain gray under player start).
## NEW MASTER HYPOTHESIS - RING COLLAR AS GAP LADDER:
- Collar = 8x8 annulus, 2 thick: lobes top/bottom (2 rows x 8), sides (2 cols x 4 rows).
- On the floor track the collar spans rows 24-31 EXACTLY = start gap rows 24-29 + lower box top 30-31.
- If collar reaches cols 20-27: its RIGHT side (cols 26-27, rows 26-29) fills the start gap at the player's column; player climbs rows 30-31 -> 28-29 -> 26-27 -> 24-25(top lobe) -> 22-23 upper box = ESCAPE.
- Ring track on floor ends ~col 16 (collar cols 9-16 at right terminus) - but redbar PIVOT = roll-around-tip step (bounced at floor-left due to column base; at slab-end it stepped once then blocked by orange column). At floor RIGHT tip all free space - pivots may chain, rolling collar rightward off the tip toward cols 20-27.
- Current ring is hooked to orange column up on slab - RESET restores pristine state (ring at floor-left, blue double-ghost, column 20-23, platform origin, corridor unbuilt).
## Committed (4): RESET, then quad3 x3 (drive ring RIGHT along floor from initial spot). Watch for floor-right terminus, then redbar pivots next.

## L5 actions 340-343: RESET + quad3 x3 - HYPOTHESIS CONFIRMED SO FAR
- RESET restored pristine state. quad3 drives ring RIGHT ALONG FLOOR +4/click: cols 0-7 -> 4-11 -> 8-15 -> 12-19 (rows 24-31, n=30 full collar visible). Collar already overhangs floor tip (floor ends col 16).
- Target: collar at cols 20-27 (right side cols 26-27 fills gap). CONCERN: bottom lobe rows 30-31 would overlap lower box cols 24-27 at that position -> possible collision block at the 16-23 -> 20-27 step.
- Fallback: collar at 16-23 = ladder at cols 22-23 (player: from rows 30-31 cols 24-25, L onto bottom lobe at 22-23, climb U x3 to top lobe rows 24-25) but top exit at cols<=23 doesn't reach upper box (cols 24-27). Then redbar tip-pivots may roll collar further.
- Climb prerequisite when ready: blueT to solidify slot A (double-ghost after reset), or walk gray-only path.
## Committed (4): quad3 x2 (-> 16-23, then attempt 20-27), redbar x2 (tip pivots). Diff each.

## L5 actions 344-347: ring TERMINUS at cols 12-19 (rows 24-31) - quad3 x2, redbar x2 ALL no-op.
- Structural reason: collar must enclose its track; left wall would clip floor tip cells (col 16) if it advanced. Ring can NEVER leave the track. COLLAR-LADDER ESCAPE DEAD.
- Collar reachable extremes on floor: cols 0-7 (start) ... cols 12-19 (right terminus). Right wall cols 18-19 rows 26-29; gap needs cols 24-27. 6 short.
- PRISTINE STATE CORRECTION (census of post-RESET board): blue is SOLID AT B, ghost at A (my 'double-ghost' claim was from post-blueT board). Pad cells: only pad B visible in that render (pad A off-crop).
- Recurring pattern: 2-row q gaps everywhere (collar top lobe->column bottom rows 22-23; collar bottom lobe->pad B box rows 32-33; bridge->column cols 22-23). Suspicious - maybe intentional 'almost' connections.
- UNTESTED FUNDAMENTAL: are checker/ghost cells walkable? Original L,L onto A happened when A was SOLID.
## Committed (4): L, L (onto ghost A right half?), D (ghost A bottom), D (expect blocked at rows 38-39).

## L5 actions 348-351: GHOSTS ARE NOT WALKABLE (fundamental)
- L ok (34-35,c28-29), L onto ghost A BLOCKED, D ok (36-37,c28-29), D blocked (gap rows 38-43). No frames/anims.
- Pristine cluster = right box ONLY (4 positions). Slot A + lower box need blueT remote toggle first.
- Post-RESET state now: ring at floor-right terminus (rows 24-31, cols 12-19), corridor UNBUILT (reset cleared gray progress), 8-platform at origin cols 12-17, blue B solid, column at 20-23. Step bar row63 all $ = fresh budget.
- Vertical stack at cols 24-27: upper box 20-23 / GAP 24-29 / lower box 30-33 / slot A 34-37 / GAP 38-43 / corridor 44-45 / purple ghost col 46-53 / yellow dock 54-55. Both gaps 6-row.
- UNTESTED: hooked-pose LEFT (column at 16-19) probes redbar/quad1/f2. Redbar pivot may walk ring DOWN column (2-row gap collar-top->column-bottom rows 22-23 at cols 16-19 suggests intended coupling).
## Committed (15): f1 x7 (floor-right -> floor-left -> up column -> slab-left terminus; termini absorb overshoot), quad3 x3 (slab -> junction terminus), redbar (one-time pivot/hook), f1 (drag column left to 16-19), then probes: redbar, quad1(43,29), f2(58,29).

## L5 actions 352-366: BUTTON SEMANTICS CRACKED - four directional drivers
- f1 x7 on floor = NO-OP (f1 is NOT a floor driver). quad3/redbar/f1/redbar no-op. f2 no-op on floor.
- quad1 (43,29) MOVED RING LEFT 4 on floor (c12-19 -> c8-15, diff=52). So: quad1=LEFT, quad3=RIGHT, f1=UP, f2=DOWN; all context-sensitive to track geometry. redbar=pivot at corners.
- Earlier 'quad1/f2 inert' results were all at poses where left/down was impossible.
- NEVER TESTED: f2 (down) with ring at slab/orange junction PRE-pivot = descend orange column (cols 20-23, rows 10-21). Collar enclosing column = cols 18-25: right wall cols 24-25 reaches INTO start-gap columns. Column bottom abuts upper gray box - descent may ladder the gap.
- Ring now floor c8-15 rows 24-31. Column at original cols 20-23.
## Committed (12): quad1 x2 (floor-left), f1 x4 (up column, terminus-safe), quad3 x3 (slab right to junction, terminus-safe), f2 x3 (DESCEND TEST).

## L5 actions 367-378: ring path retraced to junction; f2 results HIDDEN
- quad1 x2 -> floor-left c0-7; f1 x3 -> up column (r13-19); f1#4 no-op (or crop); quad3 x3 -> slab to junction c12-19 r13-19.
- f2 x3: renders cropped ring region ('?'), diffs 0/1/0 vs visible area - DESCENT RESULT UNKNOWN.
## Committed (1): D (blocked at rows 38-43) to force full re-render.

## L5 action 379: full render - f2 at junction (pre-pivot) = NO-OP. Ring still r12-19 c12-19, column at 20-23.
- Down-descent onto column requires the redbar HOOK first (post-pivot, f1/quad3 drag ring+column as assembly).
- Left-pose probes (column at 16-19): f2/redbar/quad1 STILL never tested (previous attempt died en route).
## Committed (9): redbar (hook), f1 (drag left, col->16-19), D (blocked, render), f2, f2, D (render), redbar, quad1, D (render).

## L5 actions 380-388: LEFT POSE achieved (via quad1, not f1!)
- rb = pivot ok; f1 post-pivot NO-OP this time; f2 x2 at right pose no-op; quad1 = DRAG LEFT (diff=90): column now c16-19 r10-21, ring c8-15 r13-18, bridge remnant c14-15. Column no longer under pad A box.
- Post-pivot drag driver = quad1 (left) / quad3 (right, presumably). Earlier notes blaming f1 were wrong.
- Ring overlaps purple pickup box corner at c11 r18 (interpenetration allowed).
- Column bottom r20-21 at c16-19 hovers over floor tip (c16, r26); gap r22-25.
- SPECULATIVE CHAIN: rb pivot here -> ring onto column vertical track -> f2 descend to column bottom -> quad3 drag column+low ring back right to c20-23 -> rb pivot at column-bottom/upper-box junction -> ring onto c24-27 start-gap stack.
## Committed (6): rb, D(render), f2, D(render), f2, D(render) - probe pivot+descent at left pose.

## L5 actions 389-394: left pose fully dead - rb no-op, f2 x2 no-op. Ring c8-15 r13-18, column c16-19.
- f2 has NEVER fired anywhere (floor mid, junction pre-pivot, right pose post-pivot, left pose). Ring has never descended.
- Column at c16-19 breaks top-cluster spine (pad A box and upper box disconnected from column).
- LADDER GEOMETRY GOAL: ring at floor terminus (c12-19, r24-31) + column at c16-19 = 2-row gap r22-23 alignment; pivot there might hook ring UP onto column. But hook currently pins ring at slab level - ordering conflict.
- NEXT: quad3 restore to junction, then SECOND rb pivot (may ratchet transfer onto column), then f2 descend attempts.
## Committed (8): quad3, D(render), rb, f2, D(render), f2, rb, D(render).

## L5 actions 395-402: RING SYSTEM FULLY DEAD. quad3 restored (col c20-23, ring junction pose); rb#2, f2 x2, rb#3 all no-op (1 bar tick).
- Ring total reachable set: floor c0-7..c12-19, white column, slab c0-7..c12-19, one junction pivot, hook-drag col c16-19<->c20-23. f2 NEVER fires. Ring cannot approach start gap. Purpose unclear (maybe column repositioning for top-cluster walking later).
- SYNTHESIS: pads link top<->corridor clusters; start cluster needs its own warp. Hidden pad may lie under opaque gray (lower box) or under solid slot A. Ghost-A render shows no C/z, but boxes are opaque.
## Committed (11): blueT remote (A solid), L, L (onto A bottom band r36-37 c24-25), mT, U (A top r34-35), mT, U (lower box r32-33), mT, U (lower box top r30-31), mT, U (blocked render). Each mT = teleport probe per band.

## L5 actions 403-413: magenta band sweep = NO teleports (all 4 bands static). Hidden-pad hypothesis DEAD.
- Player now on lower box top (r30-31, c24-25), slot A SOLID (blue at A, B ghost).
- FULL-HISTORY AUDIT: normalized diffs of every consecutive L5 board pair = ZERO unexplained changes outside known zones. No hidden mechanism has ever fired.
- Untested surface: play-area clicks on never-clicked structures (L4 precedent: seesaw was a play-area click).
## Committed (17): click sweep - player(24,30), right box(30,36), slot A(26,36), lower box(26,32), GG(8,50), purple bridge(16,51), purple ghost col(25,48), corridor(20,44), yellow platform(14,54), blue B ghost(9,39), gray under B(9,43), white slab(8,15), white floor(8,27), orange column(21,14), upper box(25,21), purple pickup(9,19); then U (blocked, render).

## L5 actions 414-430: click sweep ALL INERT (2 bar ticks). Play area has zero click targets. Only 8 UI buttons + moves exist.
- Endgame fully routable once player reaches pad B box: blue->B, corridor docked, purple toggle (needs pickup), platform/dock logistics, bridge -> GG. Missing link remains start->top cluster.
- Gray cycle only ever observed g1-g5 (RESET cleared to g0). Corridor right end c26-27 is directly under the slot-A gap r38-43. Deeper cycle states may build vertically.
## Committed (10): gray(56,22) x10 - map extended cycle, watch corridor AND gap r38-43 c24-27 AND anything else.

## L5 actions 431-440: gray cycle = period-8 seesaw empty<->dock (g8=empty, bounces). Rows 44-45 only. Currently g2-state (8s c12-15,c24-27). Blue confirmed exactly 2 slots (A solid now, B ghost).
- (pose x driver) matrix has untested cells: LEFT POSE {f1, quad1#2}, SLAB-LEFT CORNER {f2, quad1}, COLUMN MID {f2, quads}.
- MASTER SEQUENCE: drag col left, unhook ring leftward (q1 x2), descend white column (f2 x2 - NEVER TESTED THERE), floor drive right to terminus, redbar pivot UP onto col across 2-row gap r22-23 = LADDER.
- Ring state now: hooked, junction pose c12-19 r13-18, col c20-23.
## Committed (9): q1 (drag left), q1 (UNHOOK TEST), U(render), q1 (slab-left), f2 (DESCEND TEST), U(render), f2, f2, U(render).

## L5 actions 441-449: CRANE BREAKTHROUGH
- quad1 does NOT unhook - it CARRIES ring+column left: col c16-19 -> c12-15(org c10-15) -> c8-11 (org c6-11). Column LEFT its channel entirely.
- f2 x3 FIRED at slab-left: assembly descended white column: col rows r14-25 -> r18-29 -> r22-33. COLUMN NOW c8-11 r22-33, standing on pad B box (c8-11 r34-37). Ring r25-30 c0-7 (floor level).
- Col real position = org bbox + 2 (2-col tab on left side).
- ESCAPE GEOMETRY: quad3 x3 -> ring c12-19 (floor terminus), col c20-23 r22-33 = vertical bridge: covers c22-23 rows 22-33; player lower box top (r30-31 c24-25): L onto col, U x4 to col top band r22-23, R onto upper box c24-27 r20-23. ESCAPE!
- LOOMING ISSUES (noted for later): purple pickup sub-cluster (slab/floor/white col) may be player-unreachable (tab q-notches at (14,19),(17,19) block slab<->col at even bands; col at LEFT pose c16-19 r10-21 FILLS the notches - possible pickup route). Pad A needs col RESEATED at c20-23 r10-21 (reverse crane: quad1 x3, f1 x3, quad3 x3). Blue must go to B before corridor descent (remote toggle, player off slots).
## Committed (10): q3 x3 (bridge), L, U, U, U, U, R (escape onto upper box), U (r20-21).

## L5 actions 450-459: START CLUSTER ESCAPED!!!
- quad3 x3 bridged col to c20-23 r22-33; player climbed L,Ux4,R,U -> now UPPER BOX r20-21 c24-25. Start cluster abandoned forever (slot A stays solid, irrelevant).
- NEXT: reverse crane to reseat col c20-23 r10-21 (quad1 x3 -> c8-11 r22-33; f1 x3 -> r10-21; quad3 x3 -> c20-23). Then player climbs col (c22-23 bands r10-21) to pad A box -> pad A tile r6-7 c22-23 -> magentaT teleport -> pad B.
- PICKUP PLAN (pending): reseat, climb to r16-17 c22-23, then CARRY TEST: quad1 with player standing on col (does drag carry player to c18-19?). If carried: col at left pose fills tab notches -> slab -> pickup box (D at c8-9 r16-17->r18-19). If strand/fall: RESET recovery costs ~escape replay (~25 actions).
- blueT NOW (remote, player off slots): blue -> B solid for corridor descent later.
## Committed (13): blueT, q1 x3, f1 x3, q3 x3 (reseat), L (onto col r20-21 c22-23), U, U (climb to r16-17).

## L5 actions 460-472: reseat + climb executed. Col c20-23 r10-21 (original seat), player ON col r16-17 c22-23. Blue toggled to B (solid).
- CARRY TEST NOW: quad1 with player aboard. Case carried: player c18-19, col c16-19 (notches filled) -> L x5 along slab to c8-9 r16-17 -> D onto pickup box. Case no-op: L moves bounce at c18-19 notch. Case strand: all bounce; RESET recovery (~30 actions to replay escape).
## Committed (8): q1 (CARRY TEST), L, L, L, L, L (slab walk), D (pickup box r18-19 c8-9), D (box bottom).

## L5 actions 473-480: CARRY FAILED (player pins col - q1 blocked); L-walks bounced at notch; player descended to col bottom r20-21 c20-21.
- DISCOVERY: hooked junction-pose ring CURRENTLY covers both tab notches: (14,19)=n, (17,19)=n. Band r16-17 c18-19 = {-,-,-,n}; band c16-17 = {\$,\$,n,\$}; c14-15 = all n. If n walkable -> full slab crossing WITHOUT carry.
## Committed (10): U, U (col r16-17 c20-21), L (crossing test c18-19), L, L, L, L, L (to c8-9 via ring/slab), D (pickup box r18-19), D (box bottom). Failure mode: harmless bounces.

## L5 actions 481-490: ring crossing FAILED - all 6 L bounced at c18-19 (n in band). RING UNWALKABLE confirmed.
- REPARSE of 473: q1 carry test actually FIRED (col at c16-19 in board 473, player floating c22-23) then REVERTED on next move = HOLD semantics like blue on-slot. Carry impossible, "pin" mischaracterized.
- NEW ROUTE (no carry needed): column parked at c8-11 r22-33 (escape parking) spans pad-B-box-top(r34) to pickup-box-bottom(r21). Ladder!
- PLAN: climb seated col to pad A tile (c22-23 r6-7) FIRST; then crane q1 x3,f2 x3 (player on static pad A box, no pin); then magentaT -> pad B (c8-9 r34-35); then U x8: col r32-33..r22-23 (6), pickup box bottom r20-21 (1), icon r18-19 (1) = COLLECT.
## Committed (15): U x7 (climb r20->r6, c20-21), R (pad A tile), q1 x3 (43,29), f2 x3 (58,29), magentaT (52,48). Expect: player teleported to pad B c8-9 r34-35, col parked c8-11 r22-33.

## L5 actions 491-505: PLAN PERFECT. Climb to pad A (491-498), q1 x3 (col c8-11, 499-501), f2 x3 (col r22-33, 502-504), magentaT (505) -> PLAYER AT PAD B r34-35 c8-9. Teleport confirmed.
- Column parked c8-11 r22-33 (tab c6-7 r26-29). Ladder: pad B top r34 -> col r32-33..r22-23 -> pickup box bottom r20-21 -> icon r18-19.
## Committed (8): U x8 from pad B: 6 to col top r22-23, 1 to box bottom r20-21, 1 to ICON r18-19 c8-9 = COLLECT. Then inspect world diff (expect purple toggle spawn).

## L5 actions 506-513: U x8 perfect. PICKUP COLLECTED at r18-19 c8-9 (icon vanished, diff44).
- SPAWN: PURPLE TOGGLE BUTTON, UI panel norm r14-16 c44-56, raw click (52,14). Raw=norm+(0,+2) this render.
- State: bridge r50-53 c12-21 SOLID; ghost col c24-27 checkered; corridor g2 (8s c12-15,c24-27, O mid); 8-platform origin c12-17 r54-55; blue B solid; col parked c8-11 r22-33 (ladder stays).
- ENDGAME ROUTE: D x13 (pickup box->col->pad B->pad B box->slot B->gray box bottom r44-45 c8-9); gray(56,22) x2 -> g4 full corridor dock c12-27; yellow(47,22) x4 -> dock c22-27 r54-55; R x9 -> c26-27 r44-45; purple(52,14) -> col solid; D x4 -> col bottom r52-53 c26-27; D -> dock r54-55; L x3 -> c20-21; purple -> bridge solid; U x2 -> bridge r50-51; L x6 -> GG c8-9 r50-51. SCORE 5.
## Committed (20): D x13, gray x2, yellow x4, R (corridor entry c10-11). Next batch: R x8, purple, D x5, L x3 (~17), then purple, U x2, L x6 (~9).

## L5 actions 514-533: ALL ON PLAN. Player r44-45 c10-11; corridor g4 FULL ORANGE c12-27 r44-45; platform slid to c20-25 (4 clicks moved, dock needs 5th from c12-17 origin); pickup ladder intact.
## Committed (14): yellow#5 (dock c22-27?), R x8 (c10-11 -> c26-27 on corridor), purple(52,14) toggle (col solid/bridge ghost), D x4 (descend col c26-27 r46-53). Verify dock+platform state before stepping to r54-55.
- OPEN Q: does dock consume 8-platform? If platform respawns/persists c20-25, span c20-27 connects to bridge via U at c20-21. Else need more yellow cycles.

## L5 actions 534-547: yellow#5 DOCKED orange c22-27 r54-55 (8-platform CONSUMED, c12-21 empty); R x8 -> c26-27 r44-45; purple toggle = col SOLID/bridge GHOST; D x4 -> player r52-53 c26-27 col bottom.
- Remaining gap: r54-55 c18-21 empty; bridge c12-21 r50-53. Need platform respawn cycle to cover c20-21 (or c18-23).
- Dock is safe (col solid = retreat up). Do NOT toggle purple until crossing secured.
## Committed (7): D (dock r54-55 c26-27), yellow x4 (respawn test -> slide toward c18-23), L, L (-> c22-23). Then: L (c20-21 platform), purple (bridge solid), U x2 (bridge r50-51), L x6 -> GG = score 5.

## L5 actions 548-554: YELLOW PIECE = dock itself; player aboard PINS it (click1 held: platform showed origin c12-17 while dock vanished; clicks 2-4 no-op; revert on move). Ferry impossible. Player now r54-55 c22-23 on dock; col solid; bridge ghost.
- FIX: dismount onto solid column (R, U -> r52-53 c24-25), yellow x5 remote (dock->origin->...->c20-25 overlapping col footprint), D onto platform c24-25, L x2 -> c20-21, purple (bridge solid), U x2 -> bridge r50-51, L x6 -> GG.
## Committed (19): R, U, yellow x5, D, L, L, purple(52,14), U, U, L x6. Expect SCORE 5.

## L5 SOLVED at action 573 (score 4->5). Final run 555-573 flawless: dismount col, yellow x5 remote cycle to c20-25, drop, L x2, purple toggle (bridge solid), U x2, L x6 across bridge to GG.
- L5 total: ~310 actions (263-573). Key mechanics recap: crane (quad drags + f-lift with hook), piece-pinning (any ridden piece cannot move; held/revert), pads teleport, seesaw corridor (gray period-8), yellow platform cycle with dock consume/respawn, purple anti-phase toggle (spawned by pickup), ghosts/ring unwalkable, parity even-bands, 2 cells/move.
## LEVEL 6 START. Board 573 shows scrolled L5 win frame + new content bottom-left (gray boxes, G( icon, nn/zz mini icons, white paths c20-23). Committed (1): ACTION1 probe for fresh settled L6 board.

# LEVEL 6 (board 574 = initial, player r50-51 c28-29)
- PLAY AREA: bottom slab r48-53 c18-29 (pad zC c18-19 r48-49, player c28-29 r50-51); right mini-slab r48-53 c32-37 (nn icon r48-49 c34-37, pad Cz c32-33 r52-53); white cross track c20-23 r8-29 + r20-23..r28-29 c20-31; RED RING BOX 8x8 outline r30-37 c22-29 white inside; ORANGE cross c0-19 r30-37 with small ring 4x4 c8-11 r32-35; top-left gray box c4-11 r4-11 with -G/G- checker icon; gray col c6-11 r44-53; 8-stair r54-59 (c6-11,c8-13,c12-17) + orange piece c16-21 r56-57; top-right gray plate c32-39 r4-11.
- UI: yellow btn ~(56,8), magenta btn ~(53,25), GG indicator widget r6-7 c46-47 (UI, not goal?), CROSS LEGEND r31-42 c45-56: holes with glyphs up='"', left='-', right='I', down='(' -- HYPOTHESIS: arrows control different pieces (dir->piece mapping)!
- In-world widget boxes c32-37 r56-61 with glyph rows '8$f(8$'/'$-(f$I' = legends?
## Committed (4): U,D,L,R probe to test arrow->piece mapping and walkability.

## L6 actions 575-578: arrows = normal player moves (U/D/L/R all moved player; slab walkable c18-29 r48-53). Legend widget NOT arrow mapping.
- World graph: bottom slab (player) isolated from white cross track (gap r40-47). Pads zC (c18-19 r48-49, slab left) and Cz (c32-33 r52-53, right mini-slab) = likely teleport pair. Orange cross arm right end c19 r32-35 ADJACENT to white channel c20-21 r30-37 (bypass channels around big ring box c22-29 r30-37).
- Structures recap: white track c20-23 r8-29 + r20-29 c20-31 + r38-39 c20-31; big red ring 8x8 r30-37 c22-29 (outline n, inside white); orange cross c0-19 r30-37 w/ small ring 4x4 c8-11 r32-35; top-left gray box c4-11 r4-11 (-G/G- checker r4-5 c4-5); top plate r4-11 c32-49 with GG r6-7 c46-47 (possible GOAL); gray col c6-11 r44-53; 8-stairs r54-59 down-right; orange piece c16-21 r56-57; mini-slab c32-37 r48-53 (nn icon r48-49 c34-37, Cz pad c32-33 r52-53).
## Committed (8): yellow(56,8) probe, L x5 (c28-29 -> c18-19 r50-51), U (onto zC pad r48-49), magenta(53,25) = teleport test.

## L6 actions 579-586: yellow shifted stairs (r54-59) & consumed orange piece c16-21; L x5+U to zC pad (pad-step flipped -G/G- checker top-left box); magenta = TELEPORT zC->Cz pad, player now r52-53 c32-33 mini-slab.
- WORLD RECONFIG (trigger unclear: yellow or teleport): orange cross now VERTICAL c8-11 r28-43 (stubs c6-7/c12-13 r31-36, small ring c8-11 r32-35) reaching gray col top r44; NEW WHITE r32-35 c14-19 bridges stubs to white channel c20-21. Stairs now r54-55 c8-13, r56-57 c6-15, r58-59 c14-19.
- Potential grand route: gray col c8-11 r44-53 <- orange column -> r32-35 stubs -> white bridge -> white track -> top r8-9. But player still needs entry to gray col/slab cluster.
- Pads: bottom-slab pad c18-19 r48-49 (phase Cz/zC), mini-slab pad c32-33 r52-53 (under player).
## Committed (4): U (off pad), yellow(56,8) #2 diff, U (r48-49 c32-33), click nn-icon (35,48) probe.

## L6 actions 587-590: U,U fine (player r48-49 c32-33); yellow#2 = stair train marches right +2 (stair1 c10-15 r54-55, stair2 c8-17 r56-57, orange piece deposited r58-59 c16-21); nn-icon click (35,48) NO-OP.
- CORRECTION: world reconfig (cross->vertical col c8-11 r24-43, white bridge r32-35 c14-19) happened at act 586 = MAGENTA TELEPORT, not yellow. Orange col spans box2-bottom(r23)..gray-col-top(r44).
- Budget bar r63 ticks on clicks: 2/63 used ('hh'). Not unlimited - avoid wasteful clicks.
- Static gray anchors: gray col c6-11 r44-53; box1 c4-11 r4-11 (G- checker c4-5 r4-5); box2 c4-11 r16-23 (glyphs G( r18, nnzz r19); plate c32-49 r4-11 with GG r6-7 c46-47 = GOAL; mini-slab c32-37 r48-53; widgets c32-37 r56-61.
- D-PAD HYPOTHESIS: panel cross holes clickable: left(46,36) moves '-' orange, top(50,32) moves '"', bottom(50,40) moves '(', right(54,36) moves 'I' player.
## Committed (4): click left-hole, top-hole, bottom-hole, right-hole - diff each.

## L6 actions 591-594: all 4 panel cross-hole clicks NO-OP (no world/panel/budget change). Legend is informational, not clickable.
- PHASE THEORY: magenta teleport (act 586) toggled world phase (cross horizontal->vertical col + white bridge + stair reshuffle). -G/G- checker on box1 = phase indicator (flipped on pad-step 585).
- Current train: stair1 c10-15 r54-55 (ladders from gray col c10-11), stair2 c8-17 r56-57, orange c16-21 r58-59. Gray-col cluster ladders DOWN but not to slab. Missing link: slab <-> gray col cluster.
## Committed (3): D,D (onto mini-slab pad r52-53 c32-33), magenta = teleport back + phase-flip test.

## L6 actions 595-597: D,D + magenta = teleport back (player bottom-slab pad r48-49 c18-19) + PHASE TOGGLE CONFIRMED (beam V->H). Box B mid checker f/( = phase indicator; -G/G- flips on pad-step.
- PHASE PARITY TRAP: player on bottom slab => phase H; on mini-slab => phase V (teleport flips both). Phase-V cluster {white track, bridge, beam, box2, gray col} touches player world ONLY at gray-col/stair1 junction c6-11 r54-55 = stair1 INITIAL slot, already marched away (now c10-15... wait c10-11 still overlaps!).
- TO CHECK: s1 c10-15 still covers c10-11 under gray col! Ladder slab->s1 needs s1 c14-19 (2 clicks) but gray col needs c6-11...c10-11. s1 c10-15: slab D lands? slab bottom c18-29: s1 covers none of it. CONFLICT: single junction, monotone march.
- Testing train wrap/period with yellow x4 (orange piece -> toward widget column c32-37; watch for wrap/reversal/dock).
## Committed (4): yellow x4, player safe on slab pad.

## L6 actions 598-601: CAROUSEL PERIOD 6 CONFIRMED (act 601 = initial config = k0). States k0..k5 recorded:
- k0: r54 c6-11 | r56 c8-13, O c16-21 | r58 c12-17
- k1: r54 c8-13 | r56 c6-15(10w) | r58 c14-19
- k2: r54 c10-15 | r56 c8-17(10w) | r58 O c16-21
- k3: r54 c12-17 | r56 c10-19(10w) | r58 c6-11
- k4: r54 c14-19 | r56 c12-17 + O c18-21 | r58 c8-13
- k5: r54 O c16-21 | r56 c6-11 + c14-19 | r58 c10-15
- ROUTE: k5 ladder slab->train: D r54 c18-19 (O), L c16-17, D r56 (c14-19), L c14-15, D r58 (c10-15), L,L c10-11, U r56 (c6-11 piece). Then yellow ->k0: support swaps to c8-13 piece (or rides), U -> r54 c6-11 piece at c10-11, U -> GRAY COL c6-11 r44-53. Phase parity trap: on slab side phase=H (beam horizontal, gray col top dead-ends r44). NEXT: test REMOTE magenta as phase flipper w/o teleport.
## Committed (19): yellow x5 (k0->k5), D,D,D,L,D,L,D,L,L,U (park r56 c10-11), yellow (k5->k0), U,U,U (toward gray col r50-51).

## Act 620 state (L6)
- 19-act carousel-ladder batch SUCCEEDED exactly as planned. k5->k0 click at act617 moved train (56 diff cells) with player aboard at r56-57 c10-11 — support swap worked, NO pin/revert for carousel (unlike L5 column/dock pieces).
- Player now world r50-51 c10-11, embedded in gray col (c6-11, r44-53). Viewport offset=0 (raw=world) at act620.
- Phase H confirmed: beam horizontal cross r30-37 c0-19, ring nnnn r32-35 c8-11. Box1 indicator r4-5 c4-5 = -G/G-.
- Budget bar (only visible in full renders): act601 h=3, act620 h=4. Slow growth, ~4/64. Not urgent.
- Committed (6): U,U,U (to col top r44-45), ACTION6(53,25) REMOTE magenta phase-flip test (player off-pad), U,U (probe: climb beam if phase flipped to V; harmless bounce if not).
- If flip works: beam vertical c8-11 r24-43 sits directly above gray col top. Climb ~10 U to r24-25, reach box2 (r16-23 c4-11, bottom rows # walkable). Then route toward white track c20-23 / GG plate r4-11 c32-49 (GG r6-7 c46-47).

## Act 626 state (L6) — phase V achieved, ring is the lock
- REMOTE MAGENTA CONFIRMED: ACTION6(53,25) with player off-pad = pure phase toggle (H->V), NO teleport, +1 budget tick. Diff: beam segs r24-29 & r38-43 c8-11 appear, left arm r32-35 c0-5 vanishes, bridge r32-35 c14-19 orange->white, pad checkers + boxB f/( flip.
- Player at r40-41 c10-11 on beam lower seg (phase V). WARNING: this segment VANISHES in phase H (r38-43 void) — do not toggle while standing r38-43 or r24-29.
- TOPOLOGY (BFS 2x2, offset-0 world):
  - Player comp (35 pos): beam lower r36-42 c8-11 + gray col + slab + train k0 + orange piece r56-57 c16-21.
  - White comp (56 pos): strip r32-35 c12-19 (walkable BOTH phases) + big box r28-39 c20-31 perimeter (big ring r30-37 c22-29 sealed, interior 6x6) + right col r24-27 c28-31 + top band r20-23 c20-31 + left col c20-23 r8-23.
  - SEPARATED by single ring cells: white comp reaches (r34-35,c12-13); player comp reaches (r36-37,c10-11); ring c8-11 r32-35 (walls n, interior 2x2 c9-10 r33-34) blocks in BOTH phases.
- UI buttons decoded: yellow btn (56,8)=click on UI GG icon; magenta btn (53,25)=click on UI C icon. Legend cross = action colors: Up='"' purple, Down='(' ltblue, Left='-' orange, Right='I' green.
- Box2 recipe r18-19: ' G( / nnzz ' — hypothesis: red cells become magenta/walkable via G(=yellow-then-Down? or a door mechanism. Red blob r48-49 c34-37 click already proven no-op.
- Plate r4-11 c32-49 w/ GG r6-7 c46-47 overlaps UI border — may be goal or UI decoration. White col top reaches r8-11 c20-23; gap c24-31 r8-19 void.
- Committed (4 test clicks): (11,34) ring wall, (9,33) ring interior, (7,18) box2 glyph, (4,4) box1 checker. Player parked safe on beam (no moves).

## Act 630 state (L6)
- PARSER FIX: get(i) must slice lines[idxs[i]+1 : idxs[i+1]] and take FIRST 64 board lines (old +90/last-64 window bled into next board, produced phantom diffs).
- All 4 test clicks NO-OPS (ring wall (11,34), ring interior (9,33), box2 glyph (7,18), box1 checker (4,4)). Zero board diff, no budget tick. Only UI icon clicks (yellow GG, magenta C) do anything in L6.
- Component census: {player: beam-lower+graycol+train}, {white structure+strip r32-35 c12-19}, {box2+beam-upper (V)}, {box1}, {right platform+pad B (enclosed, 8 pos)}, {plate r4-11 c32-49}. EVERYTHING funnels through the red ring c8-11 r32-35.
- NEW HYPOTHESIS: recipe 'G(' = yellow click WHILE phase V ('('=lt-blue = boxB phase-V indicator glyph) -> 'nnzz' red turns magenta/walkable. All previous yellow clicks were in phase H. Player parked safe r40-41 c10-11 on V-beam.
- Committed (1): ACTION6(56,8) yellow in phase V. Watch red cells (ring r32-35 c8-11, blob r48-49 c34-37) for n->z.

## Act 631 state (L6) — geometry PROVEN sealed under known mechanics
- Yellow-in-phase-V = plain carousel k0->k1. Recipe hypothesis #1 dead.
- Viewport NEVER scrolls in L6 (off=0 all boards; old "scroll" observations = buggy parser artifacts).
- PLAYER START was r50-51 c28-29 on LEFT PLATFORM (under white box). Level starts phase H, k0.
- Ring interior r33-34 = ODD row parity; player always even-pair -> interior PERMANENTLY unreachable. Ring sealed both phases.
- k-state geometries (r54|r56|r58, from boards): k0: c6-11|c8-13 + orange r56 c16-21|c12-17; k1: c8-13|c6-15|c14-19; k2: c10-15|c8-17|orange r58 c16-21; k3: c12-17|c10-19|c6-11; k4: c14-19|c12-17+orange c18-21|c8-13; k5: orange r54 c16-21|c6-11+c14-19|c10-15.
- EXHAUSTIVE product-graph search (pos x phase x k, moves+yellow+magenta/teleport): 671 states, 72 positions, ALL in bottom region (r36-59) + gray col + beam lower. White structure/box2/box1/plate UNREACHABLE. A mechanic is missing.
- Next suspects: (a) legend cross GLYPH cells (arm ends, colored) as remote-control buttons: '"'=(52,34) up, '-'=(48,38) left, 'I'=(56,38) right, '('=(52,42) down — maybe they move a piece/ring (L5-crane-like). Prior no-op tests only hit the q holes. (b) click sequences: yellow then '(' glyph. (c) clicking game objects (pads, plate, GG, train).
- Committed (4): click 4 legend glyph cells. Player parked (40,10) V,k1 — safe across k/phase since beam-lower static vs k.

## Act 635 state (L6)
- Legend glyph-cell clicks (52,34),(48,38),(56,38),(52,42): ALL zero-diff no-ops. Only yellow GG icon + magenta C icon are live controls, confirmed again.
- NEW HYPOTHESIS: pad teleport destination may be PHASE-DEPENDENT (pad checker Cz/zC flips with phase = network indicator). On-pad magenta only ever fired in phase H (act586, A->B). Never tried in phase V.
- Committed (18): D x7 (beam+gray col to r54 slab k1), then R+yellow ratchet x3 (slab slides right under player k1->k4), R, U x3 to pad A (48,18) still phase V, then ACTION6(53,25) on-pad magenta in phase V. Watch teleport destination — if it lands in white box / ring interior / plate, level cracks open.
- If it just goes A->B as in H: remaining ideas: (i) yellow click while ON pad; (ii) examine level-start animation frames for hints; (iii) budget bar semantics; (iv) some rideability nuance of carousel (piece carrying player somewhere un-walkable).

## Act 653 state (L6)
- Phase-V on-pad teleport = same A->B + flip. Teleport is NOT phase-dependent. Player now pad B (52-53,32-33), phase H, k4.
- No animation frames inside L6 (all 308 frame markers are pre-L6).
- Product-graph proof stands: with (arrows, yellow=k+1, magenta=flip+teleport) the level is unsolvable. One of those assumptions must be incomplete.
- Committed (10 click battery on game objects, player parked on pad B): white box (20,38), strip (14,33), gray col (8,50), train piece k4 (16,54), plate (34,6), GG cell (46,6), top band (24,20), left platform (28,48), big-ring interior (25,33), player/pad B itself (32,52). Watch for ANY diff.
- If all no-op: remaining ideas: push mechanics test (walk into piece side), walking on untested chars, double-click patterns, RESET to view intro, click-and-hold semantics N/A.

## Act 663 state (L6)
- 10-click object battery (white box, strip, gray col, train piece, plate, GG cell, top band, platform, big-ring interior, player cell): ALL zero-diff. Game cells 100% inert. Only yellow GG icon + magenta C icon are controls.
- Conclusion: missing mechanic = unobserved effect of known controls in untested player states. Player has NEVER stood on the ORANGE carousel piece (beam-colored!).
- Recipe re-read: box2 columns align G-over-n (c7) and (-over-z (c8): "yellow<->red, blue<->magenta" mappings. Meaning unclear.
- Committed (10): magenta (teleport B->A, phase->V), D x4 (to (56,18) mounting ORANGE piece k4 c18-21), R (->(56,20) still orange), R (void test: vehicle-drive?), U (bounce test), yellow (k4->k5; (56,20) UNSUPPORTED in k5 — deliberately probing unknown unsupported-after-carousel case: fall/stranded/bump = new info; worst case RESET), magenta (flip while on orange).
- Watch: player position each step, esp. after Y (ride vs stay vs fall).

## Act 673 state (L6)
- ORANGE PIECE TESTS: not a vehicle (R/U into void = bounce, diff 0). Aboard-yellow (k4->k5, orange moves away): player FLOATED unsupported at (56,20-21) over void — NO GRAVITY. Then next click (magenta) REVERTED carousel to k4. => L5 pin rule refined: carousel click persists iff player remains supported at same position (act617 supported->persisted; act672 unsupported->held+reverted).
- Product-graph model stands consistent; level still sealed. Missing mechanic hunt continues.
- NEW recipe reading: 'nnzz' = two pad NETWORKS: red pads (nn = the blob r48-49 c34-37) and magenta pads (zz). Column alignment G-over-n, (-over-z: YELLOW button drives red-pad teleport, magenta drives magenta pads. Test: stand adjacent/on red blob, click yellow.
- Player now (56,20-21) embedded in orange k4 c18-21, phase H.
- Committed (14): L,U,U,U,U (to pad A), magenta (teleport->B (52,32), phase V), U,U (to (48,32) left of blob), YELLOW test#1, D,R (to (50,34) below blob), YELLOW test#2, R (to (50,36)), YELLOW test#3. Carousel cycles k4->k5->k0->k1 harmlessly meanwhile; watch for teleports/red-cell changes.

## Act 687 state (L6)
- Yellow beside blob at (48,32),(50,34),(50,36): plain carousel cycles, zero non-train diff. Red-pad-teleport hypothesis DEAD.
- Player parked (50,36-37) right platform, phase V, k1.
- Committed (7 clicks): recipe '(' (8,18), recipe 'z' (8,19), recipe 'n' (6,19), pad A cell (18,48), pad B cell (32,52), widget f/( checker (34,58), big ring wall (24,30).
- If all no-op: RESET to watch L6 intro + rethink from start position (50,28).

## Act 694 state (L6)
- Final click sweep (recipe '('/'z'/'n' glyphs, pad A/B cells, widget checker, big ring wall): ALL no-op. Budget bar = pure action-count TIMER (~1 tick/11 actions, now 11/64 — если fills, likely level reset; ~580 actions margin).
- Every mechanic in interaction space exhausted; sealed-level proof stands.
- Plate insight: UI-side 8x8 box (r4-11 c42-49) with GG at rel (2-3,4-5) = MAP of game-side plate (r4-11 c32-39) -> actual goal cell likely (6-7,36-37).
- Committed: RESET. Goals: (a) watch for intro [frame] animation; (b) attempt 2 fresh state; (c) test exotic combos from start pos (50,28) — arrows-on-pad, etc.

## Act 695 state (L6, post-RESET)
- RESET: spawn actually (52-53,28-29) (act574 board was post-first-move U). Timer bar cleared to 0. No intro frames. World identical.
- Realization: WIDGET r56-61 c32-37 is in GAME AREA (not UI) and mirrors legend cross. Its arm glyphs never clicked: '"'=(35,57) up, '-'=(33,59) left, 'I'=(37,59) right, '('=(35,61) down, plus f-checker cell (35,58). Might be a D-pad controlling another object (beam/ring/white box?).
- Committed (5): click those five widget cells. Player at spawn (52,28), phase H, k0 — safe.

## Act ~700 state (attempt 2, phase H, k0, spawn 52-53/28-29)
- Widget arm/checker clicks (34,58),(35,58),(35,57),(33,59),(37,59),(35,61): ALL zero-diff no-ops.
- Cross-level grep: every level L1-L6 has GG 2x2 goal in-game; L6 goal = (r6-7, c46-47) on plate r4-11 c32-49; right region IS terrain.
- L4/L5 precedent: buttons were SHAPE-INTERIOR clicks (L4 gray box (56,28) seesaw; L5 five shapes).
- Committed 10-click battery on never-tested shape interiors: widget bottom-center (34,59),(35,59); box1 plain interior (6,6),(9,6),(6,9),(9,9); box2 plain (5,17),(10,21); plate centers (36,7),(45,8).
- Next: diff all 10 boards; any responder => characterize mechanic, re-run product-graph. All no-op => systematic grid-scan of click space in batches.

## Act ~710 state
- 10-click battery (widget bottom, box1/box2 interiors, plate centers): ALL zero-diff.
- Conversion scan of whole log: n<->C/z changes ONLY at level transitions + pad checker animations. No red->magenta mechanic ever fired.
- Corrected geometry: big-ring interior r31-36 c23-28 is 6x6, CONTAINS even 2x2 slots (32/34 x 24/26) — valid teleport destination. Small ring interior (33-34,9-10) truly odd-sealed.
- Phase-V bridge r32-35 c14-19 connects strip to white box left edge c20-21; whole white structure walkable IF strip reached; still no plate connection (plate r4-11 c32-49 is an island; white col top r8-11 c20-23 dead-ends, gap c24-31).
- Red 6-cell UP-ARROW glyph at r48-49 c34-37 (not a blob): r48 nn@c35-36, r49 nnnn@c34-37. Marks top-left of right platform. (48,32) standable, symmetric to pad A position on left platform.
- Arrows never move non-player objects (full-log scan). Widget = D-pad legend: '"'purple=Up, '-'orange=Left, 'I'green=Right, '('lightblue=Down; center f/( swaps with phase. UI cross legend r31-42 c45-56 same glyphs, center hole.
- Click audit done (see log): magenta tested only from (44,10),(48,18),(52,32),(56,20). NEVER from (48,32).
- COMMITTED: walk to pad A, teleport to pad B, up x2 to (48,32), magenta click = hidden-pad test beside red arrow, then ACTION1 probe.

## Act ~722 state (player (48,32), phase H, k0)
- Hidden-pad-at-(48,32) DEAD: magenta there = plain phase flip (120-cell standard diff); up-probe blocked by red arrow.
- NEW: box1 G/- checker r4-5 c4-5 swaps on every phase flip (same motif as pad C/z checkers and widget f/( center). All 2x2 checkers are phase-linked.
- COMMITTED 15 clicks: legend glyphs+hole in H (52,34),(48,38),(56,38),(52,42),(52,38); red-arrow cells in H (35,48),(36,49),(34,49); GG (46,6) H; plate (45,8)... then flip V via (53,25); widget glyphs in V (35,57),(33,59),(37,59),(35,61).

## Act ~737 state (player (48,32), phase V->flipping H, k0)
- 15-click complementary-phase battery: ALL no-op.
- BREAKTHROUGH INSIGHT (from L5 analysis): buttons in this game are STATE-DEPENDENT PISTONS — (48,29) in L5 gave diff52 twice then diff0 (object at limit), later diff86 again. Dead-click verdicts from single tests are UNRELIABLE.
- L5 UI had ~8 buttons incl FOUR 4x4 blocks ((((/ffff/((((/ffff at r28-31 = 4 independent buttons. L6's legend cross arms (4x4 q-blocks, r31-42 c45-56, glyphs purple=Up/orange=Left/green=Right/lightblue=Down) are almost certainly 4 buttons.
- Arm clicks so far only in V (dead — maybe object at limit or wrong hitbox cell). COMMITTED: flip to H, click 4 arm centers + 4 inner cells + hole center in H.
- If arms move the PLAYER by 1 cell (parity shift!) -> unlocks ring keyhole (33-34,9-10) odd slot. Watch player pos closely.

## Act ~747 state (player (48,32) H k0)
- Legend arm clicks in H: dead. Structural diff L6 start vs now: ZERO — everything cyclical.
- Consensus terrain built for all 12 (phase,k) combos from all L6 boards: ZERO conflicting cells => world fully determined by (phase,k). Product graph re-run: 676 states, 72 positions, rows 36-58 only. Ring = single lock. Upper beam (V, r24-31) connects to box2 bottom (r22-23 c8-11)! Strip+bridge connect to white structure. But all sealed behind ring.
- On-pad destination clicks: 10 clicks incl GG cell (46,6) happened while standing on pad B — all dead. Hypothesis dead.
- UNTESTED interaction: magenta phase-flip while standing on V-ONLY beam cells (38-42, c8-11) — the phase analog of carousel pin rule. Outcomes: revert / floating / eject. Route needs 26 actions: committed first 20 (ends mid-climb ~(48,10) V k0... exact: after 20 acts player at (44,10)? — verify next turn). Remaining 6: A1 x6? then ACTION6(53,25) TEST + probe.
- Route: 2xA2 -> padB, 5xY (k->5), M (teleport padA + V), 4xA2, 2xA3, A2, 2xA3, A1, Y(k0), 8xA1 to (42,10).

## Act ~777 state (player (42,10) V k0)
- UNSUPPORTED PHASE FLIP TEST: flip at V-only (42,10) HELD (board 774 shows player floating in full H terrain), then REVERTED on next input which applied in V. Phase flips share carousel pin-rule semantics: held visually, revert on input. No float-movement possible.
- No discriminating held-state test exists on beam (H-valid moves from V-only cells are all V-valid too).
- COMMITTED 18-click sweep of never-clicked play-area shapes: white col (21,10), top band (25,21), right col (29,25), white box edges (20,30),(21,33),(25,38),(30,33), big ring wall (25,30), big ring interior (25,33), strip (16,33),(18,34), cross arm (2,33),(5,34), upper beam (9,26),(10,28), gray col top (8,44), orange piece k0 (18,56), plate left (33,10). Context: V, k0, player (42,10).

## Act ~795 state (player (42,10) V k0)
- 18-shape sweep: ALL dead. Play-area clicks conclusively inert in L6.
- L1 DECODED: UI T-icons = COLOR SOLIDITY TOGGLES. L1 red-T click turned red 'n' -> maroon '>' (walkable); blue-T toggled blue. Player walked THROUGH toggled cells. L5 (48,29) also toggled '$'<->'n' (red walls).
- L6 UI inventory: yellow key (carousel), magenta T (phase+pads), q-cross (4 unlit blocks w/ color labels purple/orange/green/lightblue at bottom-right corners), timer, dashed border. NO red toggle button visible. L5's four blocks were LIT ((f(f colored) from level start; L6's are 'q' = inactive.
- Recipe 'nnzz' reread: red-on -> 'z' walkable (L6's maroon-analog is light-magenta!). 'G(' = the trigger. Yellow-in-V alone is dead (20 tests). Now testing 'G(' as SEQUENCE: yellow click THEN '(' cell click (widget center ( cell / legend ( glyph), both phases.
- Yellow NEVER clicked while standing on pad B (only pad A, 9x) — candidate G-pad teleport test for later (box1 G/- checker looks like a yellow-type pad; box1 would be the destination!).
- COMMITTED 16 acts: [Y,(34,58),Y,(35,59),Y,(52,42)] in V; A1 x3 to (36,10); M flip; [Y,(35,58),Y,(34,59),Y,(52,42)] in H. Net k unchanged (6 Y clicks). Watch for n->z anywhere.

## Act ~811 state
- Y->'(' recipe test: ALL DEAD. Every '(' click (widget cells 34/35,58/59 and legend 52,42, both phases) = 0 diffs even right after yellow. 'G(' recipe hypothesis dead.
- Player after batch: (36,10) H k0 (6 yellows = full cycle).
- COMMITTED 20 acts: prefix of 21-act BFS route to pad A: [Y,Y,M@(36,10)->V, A2x9 ->(54,10), A4x2, Y, A4, Y, A4 ->(54,18), A1x2 ->(50,18)]. End state (50,18) V k4.
- NEXT TURN: A1 -> pad A (48,18); YELLOW test on pad A; M flip (teleport pad B, H); YELLOW test on pad B. Watch for teleport to box1 (4,4) G/- checker or any conversion.
- If dead after that: q-cross activation hunt, then batched grid scan of unclicked cells.

## Act ~831 state
- 20-act route prefix executed perfectly; player (50,18) V k4. Score 5.
- COMMITTED 4 acts: A1 -> pad A (48,18); Y on pad A (watch for special); M flip (teleport -> pad B (52,32) H); Y on pad B (watch for special).
- Expected if all normal: end (52,32) H k0. Any deviation = pad-yellow mechanic.

## Act ~835 state — MAJOR remap
- Pad yellow tests dead (plain carousel both pads). Player (52,32) H k0.
- FULL TERRAIN RE-RENDER INSIGHTS:
  * V phase has ORANGE COLUMN c8-11 rows 24-43 running through the small ring UP to box2 gray block (r16-23 c4-11). Box2 recipe row r19 'nnzz': zz c8-9 IS the walkable doorway into box2. nn c6-7 blocks left half.
  * Upper system (strip c0-19 in H, V-bridge c14-19, big-ring frame, white zigzag to r8-11 c20-23) is ONE component, connected to lower zone ONLY through the small ring. Ring = single lock confirmed spatially.
  * Big-ring frame floats (rows 40-47 under it are void in both phases).
  * Legend/widget = color->arrow map: purple=Up, orange=Left, green=Right, lightblue=Down.
  * Carousel = escalator rows 54-59 c6-21; 8-platforms shift with k; ORANGE PIECE 6x2 rides it: V/H k5 r54-55 c16-21, k0 r56-57 c16-21, k2 r58-59 c16-21, k4 r56-57 c18-21 (4w), k1/k3 hidden.
  * Y on varying cells tested often (incl (56,20) on piece) - no carry, no elevator. MAGENTA-ON-PIECE NEVER TESTED (16 magenta clicks audited, none on piece).
- HYPOTHESIS: orange piece = orange teleport pad; magenta while standing on it teleports to an orange destination (ring interior r33-34 c9-10? box1 G/- checker? V stubs?).
- COMMITTED 10: Yx5 (k->5), M@padB (teleport padA, V), A2x3 -> (54,18) on piece (V k5), then M test.
- Timer: row 63 gray h fill c0-11 = 12/64 ticks (~1/11.7 acts). Attempt budget fine.
- If dead: bump-into-ring test (A1 at (36,10)); then reconsider.

## Act ~845 state
- Magenta-on-orange-piece: DEAD (plain phase flip, no teleport). Player (54,18) H k5.
- Audit: Up NEVER pressed at (36,10)/(36,8) in L6 (only L1 board 10). Bump-into-ring untested.
- COMMITTED 20: 19-act route to (36,10) [A2,A3x2,A2,A3x2,A1,Y,A1x6,M,A1x4] ending V k1? (BFS says V k0 after 1 Y from k5) + final A1 = BUMP into ring south wall.
- Next turn: check bump result; if nothing, bump again in H (M then A1), bump red blob on padB platform (A1 at (50,34)/(50,36), A4 at (48,32)); then wider bump sweep of all red faces.

## Act ~865 state — BREAKTHROUGH: RED IS WALKABLE
- Bump test: A1 at (36,10) MOVED PLAYER INTO RING at (34,10), overlapping n cells (n->I). No color changes. Red 'n' walkable all along; WALK set was wrong assumption.
- Re-BFS with n in WALK from (34,10,V,k0): 1910 states, 181 positions, rows 8-58 cols 0-36. Upper system fully open incl white col top (8,20)-(10,22), big ring, box2.
- PLATE STILL UNREACHABLE by transitions (gap c24-31 rows 8-11). Need one more link — candidate: STAND ON box2 recipe plaque 'G(' / 'nnzz' (now walkable), or new-position clicks.
- COMMITTED 11: A1 x7 (34,10)->(20,10), A3 x2 ->(20,6), A1 ->(18,6) ON recipe (covers G at (18,7) + nn), A1 ->(16,6).
- Player before: (34,10) V k0. If (34,10) was held state, first A1 self-corrects.
- '(' walkability unknown (position (18,8) has '(' cell) — avoided.

## Act ~876 state — RECIPE COLLECTED, NEW UI PANEL
- Standing on box2 plaque (18,6) CONSUMED recipe (G( + nnzz -> all #) and SPAWNED 4x4 UI panel rows 46-49 c49-52: quadrants nn/GG/((/zz (red,yellow / lblue,lmagenta).
- Player now (16,6) V k0, box2 interior all gray.
- Panel = likely clickable color-toggle (L1 style) OR conversion map (n->G, (->z).
- COMMITTED 4 clicks: quadrants at (49,46) red, (51,46) yellow, (49,48) lblue, (51,48) lmagenta. Observe each diff.
- Remaining puzzle: plate gap c24-31 rows 8-11. If a toggle makes some color solid/walkable in the gap... note gap is 'q' void though. Maybe toggles affect GG itself or spawn bridge.

## Act ~880 state — PANEL = PAD A COLOR SELECTOR
- Quadrant clicks recolor pad A (48-49,18-19): red(49,46)->'>/n', yellow(51,46)->'-/G', lblue(49,48)->'f/(', lmag(51,48)->'C/z'. Direct selection, works from anywhere.
- HYPOTHESIS: pad color selects teleport partner checker: C/z->pad B; -/G->box1 checker (4,4); f/(->widget center (58,34); >/n->? (unknown red checker).
- GOAL ROUTE: set yellow, stand pad A, magenta -> teleport box1 (4,4) top area.
- COMMITTED 20: click yellow quadrant + route steps 1-19 of 32 toward pad A (descend box2 col, A2 x2,A4? see actions).
- REMAINING ROUTE (next turn, from where batch ends): ['ACTION2','ACTION4','ACTION6(56,8)','ACTION4','ACTION6(56,8)','ACTION4','ACTION6(56,8)','ACTION4','ACTION6(56,8)','ACTION4','ACTION1','ACTION1','ACTION1'] then ACTION6(53,25) = magenta teleport test. (route computed from (16,6,V,k0); batch1 covers first 19 route acts; remaining 13 + M.)
- Timer 16/64 at act ~878.

## Act ~900 state — PANEL IS A CYCLE BUTTON
- Correction: panel quadrants do NOT direct-select. ANY panel click advances pad A color one step in cycle: C/z -> >/n(red) -> -/G(yellow) -> f/((lblue) -> C/z. Click at (51,46) this turn set RED (expected yellow under selector theory -> falsified).
- Player (52,8) V k0 descending fine (route through ring west wall worked, red walkable).
- COMMITTED 15: panel click (->YELLOW pad), A2,A4,Y,A4,Y,A4,Y,A4,Y,A4,A1x3 -> pad A (48,18) V k4, then M = teleport test.
- Yellow partner: box1 '-G' checker (4,4) most likely (pattern match); GG itself possible (color match) = instant win.
- Timer 17/64.

## Act ~915 state — TELEPORTED TO BOX1 (4,4)
- Yellow pad A + magenta = teleport to box1 checker (4,4), phase flipped V->H. Pattern-matched partners CONFIRMED: C/z<->padB, -/G<->box1. f/( -> widget center (58,34) presumed; >/n partner unknown (no '>' checker seen elsewhere).
- Box1 interior all '#' now (checker under player). Plate unchanged, GG at (6-7,46-47).
- Box1 still island (gap c12-19 rows 4-11 to white col; gap c24-31 to plate).
- COMMITTED 15: serpentine sweep of all 16 box1 positions [(4,4)->(4,10), down, (6,10)->(6,4), down, (8,4)->(8,10), down, (10,10)->(10,4)] hunting step-on plaques like box2's.
- State: (4,4) H k4(?). Timer ~17/64.
- If no trigger: next ideas = magenta at (4,4) teleports back to pad A; try lightblue pad -> widget teleport; scan board 899 for '>' checker partner (red).

## Act ~930 state
- Box1 sweep: NO triggers, pure island. Player (10,4) H.
- No '>/n' checker anywhere (board 890 scan) -> red pad color = dead/decoy.
- All checkers: box1 (4,4) '-G', padA (48,18) '-G' (still yellow), padB (52,32) 'Cz', widget (58,34) 'f('.
- COMMITTED 13: A1x3 -> (4,4) box1 checker; M -> teleport padA (V); panel click -> pad lblue 'f('; M -> teleport WIDGET CENTER (58,34) (H); then widget sweep A1,A2,A2,A1,A3,A4,A4 (up arm, center, down arm, center, left arm, center, right arm).
- Widget = last unexplored territory. Watch for step-on triggers on arms/glyph cells.
- If clean: think about dashes c40-41 (plate touches rows 4-9), or arrows-from-widget-center mechanic (widget=D-pad?).

## Act ~943 state — WIDGET = REMOTE CONTROL FOR GIANT LEGEND AVATAR
- M at box1 -> pad A (933). Panel click 934 showed 0 diffs because pad cells were UNDER player — it DID set lightblue. M at 935 -> teleported player to WIDGET CENTER (58,34).
- Arrow presses in widget move player among widget cells AND a GIANT 4x4 avatar mirrors moves in the LEGEND cross (rows 31-42 c45-56): center hole invisible, arms render avatar in arm color: top purple, bottom lightblue, left orange, right GREEN 'I' (current, avatar at 35-38 c53-56; real player widget right arm (58,36), H phase).
- Static green glyphs at (38,56)/(59,37) were avatar/player INSIDE right arms all along — the level START had these parked there!
- Player-detector must filter blobs: real player = 2x2 in play area; avatar = 4x4 in legend.
- Widget corners are '#' walkable?? maybe 9 positions. Legend corners 'O'.
- COMMITTED 5: click lit green arm (54,36); A3 (avatar->center); A1 (avatar->top arm purple); A1 again (test avatar exit upward — jackpot if it moves toward GG!); click lit purple arm (50,32).
- BIG HYPOTHESIS: GG is the goal for the GIANT avatar (4x4 at c45-48 rows 4-7 would cover GG at 6-7,46-47). Find how avatar leaves the cross upward.

## Act ~948 state — RING IS DRIVABLE VIA LIT ARM CLICKS
- Click lit green arm (943): big red ring moved RIGHT 4 (R30C22 -> R30C26... wait actually C22->26). Click lit purple top arm (947): ring UP 4 (R30->R26). Ring = 8x8 red shell floating over static white plaza; only 'n' cells move. Current ring rows 26-33, c26-33.
- Avatar/player mirror in lockstep while player inside widget (arrow presses move both; blocked if avatar blocked).
- White structure static (plaza c20-31 r28-39, zigzag, col c20-23 r8-29) — route to white col top intact without ring.
- CROSSING PLAN: ring to R=6 (interior rows 7-12), C=22: player walks (8,20)->(8,28) through interior; then ring shift right (C=26): (8,28) walkable in both; then (8,30),(8,32),(8,34) -> plate -> GG at (6,46) walk-in.
- OPEN QUESTION: are arm clicks conditional on avatar parked there? Exit-from-widget parks avatar at CENTER (teleport only from center checker) -> final crossing shift needs UNCONDITIONAL clicks.
- COMMITTED 9: [right-arm click TEST (54,36) — if ring moves right => unconditional; top clicks x5 => R=6; A2,A3 avatar->left arm; left click (46,36)].
  - If unconditional: C ends 26, need 1 more left next turn, then exit+route+cross+green-click+walk to GG.
  - If conditional: C ends 22 PERFECT, but final green click needs solution (avatar parked at center problem!) — ideas: test magenta-exit from non-center, corner walks, or re-examine.
- Player: widget left arm after batch. Timer ~19/64.

## Act ~957 state
- Arm clicks CONDITIONAL (948: right-arm click w/ avatar on top = 0 diffs).
- Ring UP blocked at R=18 on C=26 (951-953 zero-diff). Support hypothesis: ring needs overlap with walkable terrain; C=22 has white col c22-23 support up to R=6. Ring NOW rows 18-25, c22-29 (R18,C22). Avatar at left arm, player widget left arm.
- ENDGAME BLOCKER: exit-from-widget parks avatar at center (unlit) -> remote clicks dead. Need exit-from-arm OR desync trick (teleport-in lands player center while avatar stays parked -> enter+immediately-exit preserves parking).
- COMMITTED 4: A4,A4 (player+avatar -> right arm), magenta from ARM (teleport-out test), then (54,36) green click: if teleported => remote-click test (ring right C=26); if not teleported => local click also fires C=26 (recoverable via left click).
- CROSSING GEOMETRY (final): ring (R6,C22): white col -> interior -> (8,28) or top-wall row (6,28). Shift C=26 keeps (8,28)/(6,28) walkable; then (8,30/32/34) -> plate -> GG (6,46). Ring right-shifts at R6 have plate support at C>=26.
- Timer ~19/64. Score 5.

## Act ~961 state (turn end)
- Player: widget right arm (58-59,36-37), phase V, k=4. Ring rows18-25 c26-33.
- Magenta-from-arm = plain flip, NO teleport (dead). Ring = 1-thick 8x8 shell, interior void → BRIDGE PLAN RETRACTED (parity + shell both kill it).
- Dash col c40-41: pattern identical in H and V (verified boards 600-960) → dash-ladder dead.
- NEW PLAN: physical plaque sweep of unvisited upper white system (plaques invisible until stepped on — box2 proved it). Priority: white col top rows 8-14 c20-22 (aligns with plate band).
- BFS (WALK incl 'n') from post-exit (48,18,H,4): 47-step route to (12,22):
  A2x4,A3x3,A2,A3,Y,A1,Y,A1x6,MAG(flip,not-on-pad),A1x6,A4x5,A1x2,A4x4,A1x4,A3x3,A1x4
- COMMITTED (20): [A3 (widget center), MAG (teleport→padA,H)] + route steps 1-18 (ends after A1x6 before the mid-route MAG flip).
- NEXT TURN: verify pos, then MAG flip + remaining 29 steps (A1x6,A4x5,A1x2,A4x4,A1x4,A3x3,A1x4). Watch for ANY diff outside player trail = plaque trigger.
- Pad A still lightblue f/( (panel untouched) — that's why widget-center MAG exits to pad A.

## Act ~981
- Batch executed perfectly: player (44,10), phase H, k=0 — exact BFS prediction. Score still 5.
- Board 980 vs terr(H,0): only mismatches = ring relocation (now rows18-25 c26-33, old spot reverted to '$') + consumed box2 plaque. No plaques triggered yet.
- Ring shell red = walkable, interior = underlying terr → route MORE permissive than model, still valid.
- COMMITTED (20): MAG(flip→V @44,10), A1x6→(32,10), A4x5→(32,20), A1x2→(28,20), A4x4→(28,28), A1x2→(24,28).
- REMAINING next turn (9): A1x2→(20,28), A3x3→(20,22), A1x4→(12,22). Then sweep col top (8,20)-(14,22).
- Watch diffs each turn for plaque triggers along plaza path.

## Act ~1001
- Batch part-failed: MAG flip + A1x6 OK (player (32,10) via V vertical corridor), first A4 → (32,12), then STUCK 12 actions.
- ROOT CAUSE: '$' at rows32-35 c14-19 in phase V is a PIT (unwalkable background), not floor. terr/WALK model wrong there. In phase H the orange arm rows32-35 c0-19 covers it = bridge to plaza. LESSON: white is not uniformly walkable; pit-white exists. Left plus-structure toggles with PHASE (H=horizontal arm c0-19, V=vertical corridor c8-11 rows24-43).
- Discovered 4x4 mini-ring (red shell) at rows32-35 c8-11 (present both phases; player walked its top edge).
- H-phase map: south plaza rows28-39 c20-31; neck c28-31 rows24-27; under-ring strip rows20-23 c20-31 (big ring interior white c27-31); white col c20-23 rows8-23 (contiguous to plaza!).
- COMMITTED (20) from (32,12): MAG(→H), A4x4→(32,20), A1x2→(28,20), A4x4→(28,28), A1x4→(20,28), A3x3→(20,22), A1x2→(16,22).
- NEXT: A1x4→(8,22), sweep col top rows8-14 c20-22 for plaques; then plaza/strip sweep. Timer ~25/64.

## Act ~1021 — MAJOR MODEL REVISION
- Batch: arm walk c12→c18 OK, but (32,18)→(32,20) BLOCKED (plaza '$' 4-support refused). (32,12)→(30,12) SUCCEEDED with only ONE '-' support cell.
- NEW MOVEMENT MODEL: '$' white is (likely) NEVER walkable in L6 — pit/background. Real floor = '#','8','-','n',pads,widget glyphs. Moves OK with >=1 real-floor target cell; 0 real cells = blocked. ALL white-route plans (plaza, col, white col top) were fantasy; player has never stood on '$'.
- Avatar does NOT persist after leaving widget (legend arms unlit, board 1020) → no remote ring driving from outside.
- Ladder c40-41 rungs (rows ≡0-1 mod4, full height) sit on 'O' UI — probably background too; no rung adjacent to real floor.
- Plate rows 4-11 c32-49 ('#' real) is ISOLATED. Access = likely undiscovered plaque/teleport. Red >/n checker partner absent from board (decoy or not-yet-spawned).
- Timer row63: 26/64.
- VISITED-POSITION AUDIT (all L6 boards): box1 16/16 swept. UNSWEPT: box2 8 pos [(16,4),(16,8),(16,10),(18,4),(18,8),(18,10),(20,4),(22,4)]; H-arm west+row34 11 pos; tower col6 5 pos [(44,6)..(52,6)]; padB block 4 pos [(48,34),(48,36),(52,34),(52,36)]; widget corners [(56,32),(56,36),(60,32),(60,36)].
- COMMITTED (17): serpentine H-arm sweep from (30,12): A2, A3x6 → (32,0), A2, A4x9 → (34,18). Phase stays H.
- NEXT: box2 sweep needs phase V corridor (from arm: to (32,8)? climb rows 24-43 c8-11 in V, then box2). Then tower col6, padB block, widget corners.

## Act ~1038
- H-arm sweep complete (17/17 moves exact): NO plaques on arm (only player diffs). Player (34,18), phase H, k=0. Timer ~26/64.
- COMMITTED (20): A3x4 → (34,10); MAG(→V); A1x9 corridor+box2 → (16,10); A3 → (16,8); A2 → (18,8); A3x2 → (18,4); A1 → (16,4); A2 → (18,4). Covers box2 unvisited: (18,10),(16,10),(16,8),(18,8),(18,4),(16,4).
- REMAINING box2: (20,4),(22,4). Then: tower col6 [(44,6),(46,6),(48,6),(50,6),(52,6)], padB block [(48,34),(48,36),(52,34),(52,36)], widget corners [(56,32),(56,36),(60,32),(60,36)].
- Flip safety: only flip while on cells existing in BOTH phases (mini-ring shell / corridor c8-11 rows 32-35).

## Act ~1058
- Box2 sweep batch 20/20 exact. Player (18,4), phase V, k=0. V-vs-V diff = ONLY timer (29/64 now). No plaques on (18,10),(16,10),(16,8),(18,8),(18,4),(16,4).
- COMMITTED (20): A2x2 → (22,4)★ last box2 cells; A4x3 → (22,10); A2x11 corridor down → (44,10); A3x2 → (44,6)★; A2x2 → (48,6)★. Sweeps: (20,4),(22,4),(44,6),(46,6),(48,6).
- REMAINING unswept after this: (50,6),(52,6) tower; padB block [(48,34),(48,36),(52,34),(52,36)]; widget corners [(56,32),(56,36),(60,32),(60,36)].
- If all sweeps dead → rethink: clicks on plate/GG directly, clicks on rungs, legend-center click with avatar at center, ring lower-zone parking.

## Act ~1078
- Tower col6 sweep 20/20: (20,4),(22,4),(44,6),(46,6),(48,6) stepped — NO plaques (timer-only diffs, 30/64). Player (48,6), V, k=0.
- Carousel k-map (terr): k0:(54,c6-11)(56,c8-13)(58,c12-17)+or(56,c16-21); k1:(54,c8-13)(56,c6-15)(58,c14-19); k2:(54,c10-15)(56,c8-17)+or(58,c16-21); k3:(54,c12-17)(56,c10-19)(58,c6-11); k4:(54,c14-19)(56,c12-17)+or(56/57,c18-21)(58,c8-13); k5:or(54,c16-21)(56,c6-11&c14-19)(58,c10-15).
- COMMITTED (20): A2x2 (50,6)★(52,6)★; A2 (54,6); A4x2 (54,10); A2 (56,10); A4 (56,12); A2 (58,12); A4x2 (58,16); Y(k1); Y(k2); A1 (56,16); Y(k3); A4 (56,18); Y(k4); A1 (54,18); A1 (52,18); A1 (50,18); A1 (48,18)=pad A.
- NEXT TURN from pad A (lightblue, k=4): panel click (49-52,46-49 any quadrant) → pad becomes C/z; MAG → teleport pad B (52,32); sweep padB block (48,34),(48,36),(52,34),(52,36); then widget corners via lightblue teleport chain.

## Act ~1098
- Carousel traverse 20/20 flawless. Player pad A (48,18), V, k=4. Tower sweep done, no plaques.
- COMMITTED (20): panel(f/(→C/z); MAG→padB(52,32)[→H]; sweep A4(52,34)★ A4(52,36)★ A1(50,36) A1(48,36)★ A3(48,34)★; return A2(50,34) A2(52,34) A3(52,32); MAG→padA[→V]; panel x3 (C/z→>/n→-/G→f/(); MAG→widget center(58,34)[→H]; A1(56,34); A3(56,32)★; A2(58,32); A2(60,32)★; A4(60,34).
- REMAINING sweeps after: (60,36),(56,36) widget corners — next turn 2 moves (A4,A1).
- IF ALL SWEEPS EMPTY: fallback experiments = direct clicks on plate/GG cells, rung clicks, widget-corner avatar behavior (avatar to legend corners?), legend center-hole click, mini-ring direct clicks/pushes, ring parked positions in pit.

## Act ~1118 — RED BUTTON DISCOVERED
- Teleport chain 20/20. padB sweep TRIGGERED PLAQUE: red cells (48,35)-(49,37) consumed → '#', SPAWNED red UI icon rows 17-19 c47-55 (3rd big button; yellow=k+1 at (56,8), magenta=phase/teleport at (53,25), RED=??? at ~(51,18)).
- Legend: player at widget CORNER → avatar not rendered, no arm lit. Corners (56,32),(60,32) walked; remaining (60,36),(56,36).
- Player now (60,34) S arm, phase H, k=4. Pad A currently lightblue f/(.
- COMMITTED (5): click RED btn ACTION6(51,18); A4 (60,36)★; A1 (58,36); A1 (56,36)★; click RED again. Observe diffs per click.
- Hypothesis: red button relates to ring drive or red pad partner.

## Act ~1123
- Widget corners all swept (no plaques there). RED button clicked from S arm and NE corner: 0 diffs both — CONDITIONAL button.
- Theory: red button pairs with red pad color >/n (the "decoy" color) — its trigger button was locked behind the padB plaque.
- COMMITTED (6): A3 (56,34); A2 (58,34) center; MAG → pad A [→V]; panel x2 (f/( → C/z → >/n RED); click RED (51,18). Observe.
- If nothing: try MAG while pad red; try red-click from OTHER positions (pad B, checkers, widget center); try red-click with avatar on arms.

## Act ~1129
- Player on pad A (48,18), phase V, k=4. Panel clicked x2 (pad presumed >/n RED, hidden under player). RED button click on red pad in V: 0 diffs. 
- Legend arm lights confirmed toggling with player arm position (N arm purple lit when player N arm).
- COMMITTED (2): MAG (red-pad teleport theory / phase→H), RED button again (H + red pad test).
- NEXT IDEAS if dead: RED-click while standing ON mini-ring shell (RED=ring-button theory, mirroring MAG=pad-button); RED-click at box1/box2; RED-click while in widget with avatar on each arm (maybe drives ring remotely now).

## Act ~1131
- MAG on (presumed red) pad A = plain flip (→H). RED button on red pad H: 0 diffs. Red-pad theory dead unless pad color wasn't actually red (unverified — hidden under player!).
- COMMITTED (20) route pad A → mini-ring: A2x3 (54,18)[k4]; A3x2 (54,14); A2 (56,14); A3 (56,12); A2 (58,12); A3 (58,10); Y(k5); A1 (56,10); Y(k0); A1 (54,10); A1x5 tower → (44,10); MAG(→V); A1 (42,10).
- First move steps OFF pad A → next boards reveal actual pad color (verify panel cycle worked!).
- NEXT TURN: A1x4 → (34,10) mini-ring, position (32,10) or (32,8) on shell, click RED (51,18). If dead: RED from widget with avatar on arms; RED clicked on the big ring cells directly (ACTION6 on ring shell).

## Act ~1151
- Pad A CONFIRMED red '>n/n>' after step-off → panel cycle verified; red pad + MAG/RED = truly dead.
- Route 20/20. Player (42,10), V, k=0. Timer ~32/64.
- COMMITTED (10): A1x5 → (32,10) mini-ring top shell; RED; A3 → (32,8) corner; RED; MAG (on-ring flip→H, checks ring-teleport); RED (H+ring).
- IF DEAD: remaining RED-click contexts: in-widget with avatar on each arm (N/W/E/S) — maybe RED+lit-arm = ring drive from anywhere?; click directly ON big-ring cells e.g. ACTION6(28,18); RED while on box1/box2 checkers; RESET-level rethink.

## Act ~1161
- RED button 0-diff in ALL contexts tried: widget S arm(H), NE corner(H), red pad(V+H), mini-ring top(V), corner(V), corner(H). MAG on mini-ring = plain flip (no ring teleport).
- NEW THEORY: red 17-19c47-55 bar = ITEM/INDICATOR not button (uniform 9x3 bar vs shaped yellow/magenta icons). Maybe bridge piece for gap rows8-11 c24-31 (8 wide).
- Player (32,8), phase H, k=0. Timer ~32/64.
- COMMITTED (8 clicks, player stationary): RED(51,18)+GAP(27,9) drag test; RED alt cell (49,17); GAP again; GG(46,6); big-ring shell(28,18); rung(40,20); RED bottom row (51,19).
- IF ALL DEAD: consider in-widget RED with avatar on N/W/E arms (only S tested); clicking pit cells; clicking plate '#'; RESET+fresh-eyes review of early L6 boards for missed mechanics.

## Act ~1169 — RING-TELEPORT THEORY
- Click battery all 0-diff (GG, big ring, rungs, red bar cells, gap). No floor anomalies remain anywhere (scan clean).
- THEORY: red pad partner = BIG RING INTERIOR (teleport into ring). Failed at 1129 because ring interior sat over pit void → unsupported → aborted to plain flip. FIX: drive ring so interior overlaps plate '#' (target R=6..10, C=38: rows6-13 c38-45 over plate rows7-11), then red-pad MAG.
- Red bar might BE the ring-drive unlock (for the R=18 stall / eastward moves).
- Player (32,8) H k=0 → must return to widget via pad A (lightblue) to drive ring: 3x N-clicks (50,32), 3x E-clicks (54,36).
- COMMITTED (20) leg 1: MAG(→V); A2x11 corridor+tower → (52,8)... wait: (34,8)..(44,8) 6 presses, (46,8)..(52,8) 4 presses, (54,8) 1; A4 (54,10); A2 (56,10); A4 (56,12); A2 (58,12); A4x2 (58,16); Y(k1); Y(k2). Ends (58,16) k2.
- NEXT legs: A1 (56,16); Y(k3); A4 (56,18); Y(k4); A1x4 → pad A; panel x2 (red→yellow→lightblue); MAG → widget; then drive batch: A1 N-arm, N-click x3, A2, A4 E-arm, E-click x3, A3 center, panel x2 (→C/z? NO: lightblue→C/z→>/n 2 clicks to RED), MAG → pad A?? recheck: MAG from center needs pad lightblue. Order: panel x2 AFTER exiting. Exit first (MAG center→padA while lightblue), then panel x2 (→red), then MAG → ring-teleport test.

## Act ~1189
- Leg 1 perfect 20/20. Player (58,16), V, k=2. Ring still R=18,C=26.
- COMMITTED (20) leg 2: A1 (56,16); Y(k3); A4 (56,18); Y(k4); A1x4 → pad A (48,18); panel x2 (red→yellow→lightblue); MAG → widget center [→H]; A1 N-arm (56,34); N-click (50,32) x3 [ring R 18→14→10→6 IF unlocked]; A2 center; A4 E-arm (58,36); E-click (54,36) x3 [C 26→30→34→38].
- Watch: N-click diffs reveal if R=18 stall is gone (red bar unlock theory). E-clicks whether ring crosses pit east boundary.
- NEXT: A3 center; MAG (lightblue→padA); panel x2 (→red); MAG on red pad → RING-INTERIOR TELEPORT TEST. If ring at rows6-13 c38-45: interior over plate rows7-11 c39-44 (real '#') → landing supported!

## Act ~1209 — ARENA MODEL (center-in-pit)
- All 6 ring-drive clicks (1201-1208 area) were 0-diff; ring stuck at (18,26).
- Board 942 (successful E-drive) vs 1205: identical phase H, k=4, avatar lit on E arm, same click (54,36) → mechanism fine, blocking is POSITIONAL.
- Model: ring center (rows R+3..R+4, cols C+3..C+4) must lie inside the pit polygon (plaza 28-39/c20-31 + neck 24-27/c28-31 + strip 20-23/c20-31 + white col 8-23/c20-23). Fits all 7 successful + 6 blocked historical moves.
- Predicted legal route: (18,26)→W(18,22)→W(18,18)→N(14,18)→N(10,18)→N(6,18) — ring can climb the col at C=18.
- Committed batch (14): A3,A3 to W arm; W-click ×2; A4,A1 to N arm; N-click ×3; A2 to center; MAG (lightblue teleport→pad A, flips H→V); panel ×2 (→red); MAG = red-teleport test with ring parked at col top.
- Next turn: verify each ring hop; check if final MAG teleported into ring interior or plain-flipped.

## Act ~1224 — MODEL LOCKDOWN + DOCK HYPOTHESIS
Results of last batch: ring route (18,26)→W(18,22)→W(18,18)→N(14,18)→N(10,18)→N(6,18) ALL SUCCEEDED — center-in-pit arena model validated 12/12. Red-pad MAG at (6,18): PLAIN FLIP again.
Definitive findings this turn:
- Panel is a strict 1-step cycle Cz→>n→-G→f(→Cz, quadrant clicked is IRRELEVANT (proven a877-881,a901 with exact board alignment). Pad NOW = >n red.
- '>' maroon has NEVER existed anywhere except pad A (full-history scan) → red teleport partner does not exist yet; may SPAWN on a condition (like red bar spawned from padB red plaque at board 1103, trigger=stepping on it).
- Unlit arm clicks DON'T drive: a591-594/a739-741 clicked W/N/E with legal targets, player outside widget, ring never moved. Only the arm lit by avatar (player at matching widget position) drives. → RIDING THE RING IS IMPOSSIBLE.
- All L1-5 cleared by stepping player onto a 2x2 GG tile. L6 goal = GG (6-7,46-47) on plate rows 4-11 c32-49. Plate crosses UI border at rows 6-7,10-11 (# bridges). Plate unreachable by walking AND by ring (gap rows 6-13 c26-31 all void-q; ring set cannot cross void).
- V-phase pit ⊇ H-phase pit, V adds rows 32-35 c14-19 white (H-arm east segment becomes pit!) → NEW ring position (30,14) legal in V only. V also has real '--' floor at c12-13 rows 32-35 flanking mini-ring.
- DOCK HYPOTHESIS: mini-ring (32-35,c8-11) marks where the big ring must dock. Big ring at (30,6) would center exactly on mini-ring interior. Route: (30,14)[V] then W,W — those W-clicks test whether center-over-real-floor moves are legal.
- Legend arm glyph colors: N='"'purple, W='-'orange, E='I'green, S='('lightblue (static decor at arm bottom-right corners).
Committed batch (20): panel x2 (red→orange→lightblue), MAG (teleport→widget center, flip H→V), A2, S-click(50,42) x3 [S NEVER TESTED — expect (6,18)→(18,18)], A1,A4, E x2 [→(18,26)], A3,A2, S x3 [→(30,26)], A1,A3, W x2 [→(30,18)].
Next turn: if S-clicks worked, one more W→(30,14), then W,W dock test toward (30,6); watch for spawns after each park. Timer 40/64.

## Act ~1244 — S-CLICKS PROVEN, RING AT (30,18), PHASE V
Batch executed perfectly: S-click coords (50,42) WORK (3 S-drives), route (6,18)→(18,18)→E,E→(18,26)→S,S,S→(30,26)→W,W→(30,18). Player at widget-W (58,32), phase V (b[26][9]='-'), pad A lightblue f( (2 panel clicks then teleport). Timer ~41/64.
Committed: W-click x3 → (30,14) [center V-white, should work], then (30,10) [center mixed -/$, tests ≥1-white rule], then (30,6) [center = mini-ring interior '--', DOCK]. Watch for spawns/score.

## Act ~1247 — DOCKED AT (30,6); CENTER RULE = NON-VOID
All 3 W-drives succeeded: (30,18)→(30,14)→(30,10)→(30,6). Big ring now CONCENTRIC around mini-ring. Drive rule finalized: center 2x2 must be NON-VOID (white pit OR real floor both OK; only 'q' blocks). No spawn/score from docking. Timer 42/64. Player at widget-W, phase V.
Bridging analysis (done): plate is center-isolated (void moat ≥2 center-steps) → ring can NEVER reach plate. Static-bridge math: box1(c11)→plate(c32) gap = 10 two-col blocks; big shell (4 blocks) + mini (2 blocks) = 6 → walking bridge IMPOSSIBLE even with perfect stone placement. Leapfrog impossible (driver must be in widget; teleports only from pads). → Solution must be something else.
CARGO HYPOTHESIS: docked big ring may CARRY the mini-ring when driven (mini stays centered) → tests: E-drive and watch mini position.
Committed batch: MAG (flip→H, observe docked pair in H), red-bar click (docked context), A4,A4 (player to widget-E), E-click (assembly drive test → does mini move to rows 32-35 c12-15?). Re-dock if needed = W-click x1 (always legal, center=mini interior).

## Act ~1252 — RED BAR = MERGE BUTTON!! FAT RING EXISTS
- MAG flip→H (board 1246). RED BAR CLICK (1247): rings FUSED into 6x6 2-thick "fat ring" rows 31-36 c7-12, interior 2x2 '--' at (33-34,9-10). Bar persists after use. No other side-effects; no '>' anywhere; pad still f(.
- E-click (1250): fat ring drives as a unit → rows 31-36 c11-16. Player at widget-E.
- Fat ring should be self-supporting (carries its own '--' interior under its center) → FREE ROAM hypothesis: can park ANYWHERE on the 4-grid, including across void.
- RAFT hypothesis: player standing on fat platform pressing into void may slide the platform (vehicle semantics).
Committed batch (20): A3,A1 (widget-N), N-click x6 [(31,11)→(7,11) — crosses void centers at (29-30,13-14) etc → free-roam test; ends overlapping box1 east edge], panel x3 (f(→Cz→>n→-G orange), MAG (teleport→box1 (4,4), flip→V), A2, A4 x7: walk (6,4)→(6,16) boarding fat, last A4 = raft test into void.
Contingencies: free-roam fail → N-clicks 0-diff, player safely walks box1 only. Raft fail → player on fat/box1, exit via box1 anchor MAG. Timer ~42/64.

## Act ~1272 — BATCH WHIFFED; RED-CORE TELEPORT TEST
Last batch failed completely: all 6 N-clicks blocked → FREE-ROAM FALSE (fat ring obeys center-non-void vs UNDERLYING terrain; its own core doesn't count). MAG fired at widget-N (not on anchor) → plain flip (now phase V); pad cycled to -G; A4s blocked at widget-E. 20 actions wasted. Fat still (31,11). Timer ~44/64.
Analysis: fat reachable set (V): (31,7),(31,11)H,(31,15),(31,19),(31,23),(31,27),(27,19..27),(23,27),(19,19..27),(15,19),(11,19),(7,19). Plate-adjacent park (7,31) EXISTS (center on plate floor) but NO ROUTE (moat: centers (9-10,25-26),(29-30) void). Merge/split leapfrog impossible (split puts mini exactly at big center; relative shift = 0). Static bridge math still impossible.
LIVE HYPOTHESES: (1) RED teleport = into ring CORE — core is now REAL floor ('--' at 33-34,13-14) → may finally work. Parity note: core is odd-aligned; landing may misalign player (or snap). (2) RAFT: player aboard + press into void slides platform (untested, needs H/V-arm trek to board).
COMBO ENDGAME if both work: park fat at (7,19) col-top, red-teleport into core, raft east across moat to plate/GG (only if raft ignores center rule... else still stuck).
Committed (6): A3 (widget center anchor), panel (-G→f(), MAG (teleport→padA, flip→H), panel x2 (f(→Cz→>n), MAG (RED-CORE TELEPORT TEST → expect player at (33,13) inside fat).
If fail: player on padA, phase flips →V — convenient for corridor trek to board fat manually and raft-test.

## Act ~1278 — RED CONFIRMED DECOY; PLUS-STRUCTURE FOLLOWS RING; RAFT TREK LEG 1
- Red-core teleport FAILED (1276: red pad + MAG with real-floor fat core = plain flip). Red teleport permanently dead.
- DISCOVERY: the plus/phase structure CENTERS ON THE RING: fat at (31,11) → V corridor now rows 24-43 c12-15 (detached from tower c6-11!). H-arm still c0-19. Phase indicator b[26][9] obsolete; use rows 24-27 c12-15 (or corridor position) instead. Current phase V, timer 45/64, k=4, pad >n red, player pad A.
- Fat at (31,7) re-centers corridor at c8-11 → tower-adjacent again. With fat at (31,7): flanks '-' c6,c13 rows 31-36; whites c4-5,c14-15 rows 32-35.
Committed (20): panel x2 (>n→-G→f(), MAG (→widget, flip→H), A3, W-click (fat→(31,7), center (33-34,9-10) H-arm ✓), A4, MAG (→pad A, flip→V), descent A2x3,A3x2,A2,A3,A2,A3 (→58,10 k4-supported), Y(→k5), A1 (→56,10), Y(→k0), A1 (→54,10 tower bottom).
NEXT TURN: A1 x11 → (32,10) [corridor c8-11, fat cells at rows 32-33], then RAFT TESTS: A3,A3 → (32,6)?? then A3 press into white c4-5 = W-raft-test; and/or A4 side: (32,12) then A4 into white c14-15 = E-raft-test. If fat slides → RAFT MECHANIC EXISTS → replan crossing to plate. If blocked → last resort thinking (maybe RESET or deep re-examination).

## Act ~1298 — TREK LEG 2: CLIMB + RAFT TESTS
Leg 1 perfect: fat (31,7), corridor realigned c8-11, player (54,10), phase V, k=0 (after 2 Y-rides), timer ~46.
Committed (18): A1 x11 [(54,10)→tower→corridor→(32,10) ON fat], A4 [(32,12) fat+flank], A4 [E-RAFT TEST into white c14-15], A3 x5 [walk back west across fat to (32,6)?? then final A3 = W-RAFT TEST into white c4-5].
Outcomes: fat slides → RAFT EXISTS → replan moat crossing. Both blocked → raft dead; consider: any mechanic left? (S-arm in special states, splitting via bar re-click, RESET.)

## Act ~1315 — RAFT DEAD; SOLUTION FOUND: PIPE DRIVE + H-ARM BRIDGE
- Raft disproven both directions (boards 1308-1314 identical, fat never moved). Player-overlap render quirk: fat draws over player.
- FAT CELLS ARE WALKABLE (player at (32,6-7) supported only by fat col 7 over void).
- WHITE PIPE NETWORK (drive terrain, underlying): lake rows 28-39 c20-31 (+arm rows 32-35 c14-19); horiz rows 20-23 c20-31; branch rows 24-27 c28-31 (NOT c20-23!); vertical c20-23 rows 8-23 topping at rows 8-11.
- PLUS-ARM GEOMETRY CONFIRMED (board 1250 + V measurements): arms = center±9 long, center±1 wide. V: c8-11 rows 24-43 at center (33,9). H at fat(31,11): rows 32-35, c4-23 (east end hidden under lake).
- ⇒ SOLUTION: drive fat to pipe-top center (9-10,21-22). In H phase, H-arm = rows 8-11, cols 12-31 — EXACTLY bridges box1(c11)↔plate(c32). Fat body rows 7-12 c19-24 covers the white pipe segment (walkable either way).
- FULL PLAN (~90 acts, timer 48/64 ok):
  1. Trek to pad A (26): A4, A2x10 (corridor→tower (52,8)), A4, A2→(54,10)[k0], A2→(56,10)[k0], A4→(56,12)[persists k0-k4], Yx4→k4, A4→(56,14), A1→(54,14), A4x2→(54,18), A1x3→(48,18).
  2. MAG (pad f() → widget center (58,34), phase V→H.
  3. Drives (player at widget, H phase): E x5 [(33,13)(33,17)(33,21)(33,25)(33,29)], N x3 [(29,29)(25,29)(21,29)], W x2 [(21,25)(21,21)], N x3 [(17,21)(13,21)(9,21)]. Widget moves: A4→Epos; clicks (54,36)x5; A1,A3→Npos; (50,32)x3; A2,A3→Wpos; (46,36)x2; A1,A4→Npos; (50,32)x3. ~21 acts.
  4. MAG widget-center → pad A (H→V). Panel click x3: f(→Cz→>n→-G. MAG on pad A → box1 (4,4), V→H ✓ final phase H.
  5. Walk: A2x2→(8,4), A4 x~21 across H-arm rows 8-9 (through fat cells c19-24) to plate, up-right to GG (6-7,46-47).
- THIS BATCH (20): trek steps 1-20, ends (56,14) k4. NEXT: A1,A4,A4,A1,A1,A1, MAG(53,25), A4, E-click(54,36)x5, A1, A3, N-click(50,32)x3... 
- Watch next turn: player reached (56,14)? k=4 (rows54-55 platform c14-19)? Any Y-press mishap → player may have fallen (check for reset).

## Act ~1335 — TREK LEG 1 PERFECT
- Player (56,14), k=4, timer 50/64, pad A still f(. All 20 acts as planned.
- THIS BATCH (20): A1→(54,14), A4x2→(54,18), A1x3→(48,18)=padA, MAG(53,25)→widget center (58,34) [V→H], A4→Epos(58,36), E-click(54,36)x5 [fat→(33,29)], A3+A1→Npos(56,34) via center, N-click(50,32)x3 [fat→(21,29)], A2+A3→Wpos(58,32).
- Verified: all 13 drive destinations have ALL-4 non-void center cells (H-corridor c0-19 rows 32-35 covers E leg 1-2; lake/pipe covers rest) — rule strictness moot.
- NEXT TURN: W-click(46,36)x2 [fat→(21,21)], A4→center, A1→Npos, N-click(50,32)x3 [fat→(9,21) FINAL], A2→center(58,34), MAG→padA [H→V], panel(51,48)x3 [f(→Cz→>n→-G], MAG→box1(4,4) [V→H], then A2x2→(8,4), A4 walk east. Verify after this batch: fat center at (21-22,29-30)? player at Wpos? phase H (corridor rows 32-35)?

## Act ~1355 — DRIVES 1-8 PERFECT
- Fat at (21,29) rows 19-24 c27-32 ✓. Player Wpos (58,32) ✓. Timer 52/64. H-corridor rows 20-23 c20-39 renders '-' floor OVER white pipe cells (key confirmation for final bridge walk).
- THIS BATCH (20): W-click(46,36)x2 [fat→(21,21)], A4→center, A1→Npos, N-click(50,32)x3 [fat→(9,21) FINAL PARK, body rows 7-12 c19-24], A2→center(58,34), MAG→padA [H→V], panel(50,47)x3 [f(→Cz→>n→-G], MAG on padA→box1(4,4) [V→H, arm rows 8-11 c12-31 = BRIDGE], A2x2→(8,4), A4x5→(8,14).
- NEXT TURN (17): A4 x12 → (8,38), A1 → (6,38), A4 x4 → (6,46) = STEP ON GG. Watch for SCORE 5→6!
- Risks: panel cycle count (f(→Cz→>n→-G = exactly 3 clicks); MAG3 requires standing ON padA (yes, player teleports onto it); phase parity H at end ✓.

## Act ~1375 — BRIDGE COMPLETE, PLAYER ON ARM
- Everything landed: fat parked (9,21) [rows 7-12 c19-24], teleport chain worked (box1 -G checker visible), phase H, arm rows 8-11 c12-31 rendered, player at (8,14). Timer 53/64, score 5.
- THIS BATCH (17): A4x12 → (8,38), A1 → (6,38), A4x4 → (6,46) = GG. EXPECT SCORE 6.
- If L7 starts: parse fresh board from scratch, all L6 mechanics may not apply.
