# Game notes

## Level 1 initial state (Action 0)
Coordinates as (x=col, y=row).
- Hollow purple diamond outline, center (39,21), radius 3, corners/edge midpoints missing — suspected goal.
- White diamond (r2) with purple center at (7,36).
- Purple 5x5 blob with magenta 'C' center at (17,47).
- Gray diamond (r2) with purple center at (27,59).
- Off-white '8' dotted diagonal trails: (9,38)->(14,44) links white diamond to purple blob; (19,49)->(25,57) links purple blob to gray diamond. Trails = movement history or chain links?
- Background: black 'O' blob region surrounded by light gray '#'; col 0 all white '$'.

## Confirmed mechanics (after actions 1-2)
- Column 0 = step budget bar: loses one '$' from top per action (rows 0,1 now 'O' after 2 actions). ~64 budget.
- Chain of 3 segments: WHITE diamond = head, PURPLE blob = middle, GRAY diamond = tail, connected by '8' dotted trail.
- Action 1: clicked gray tail (27,59) -> white and gray SWAPPED colors/roles (head<->tail reversal). Nothing moved.
- Action 2: clicked (39,21) (goal outline center) -> chain stretched in straight line from tail: gray tail stayed at (7,36), white head jumped to click point (39,21), purple middle repositioned midway at (23,28), '8' trail along the line. Head landed exactly inside goal outline (purple center matches outline center).
- After action 2: white head+purple center at (39,21) INSIDE goal outline; unknown if level cleared (score still showed 0 in Action 2 header, which is pre-execution).

## More findings
- Action 3: clicked head at its own position (39,21) -> NO-OP (only budget bar decremented). White head inside outline does NOT clear level. Clicking head = no-op (or move-to-same-spot).
- Swap (action 1) only recolors: positions unchanged, head/tail roles trade places.
- Middle always lands at midpoint of tail->head line.

## More findings 2
- Action 4: swap worked (gray in goal, white head at (7,36)) but score still 0. Gray in goal does NOT clear either.
- Current hypothesis: PURPLE blob (middle) must be in goal (purple outline = purple object).

## Batch for actions 5-7 (from state: head white (7,36), tail gray (39,21), middle (23,28)):
1. ACTION6(29,21): head -> (29,21), tail stays in goal, middle -> (34,21)
2. ACTION6(39,21): click tail -> swap roles (head at 39,21, tail at 29,21)
3. ACTION6(49,21): head -> (49,21), middle -> midpoint = (39,21) = GOAL
If score still 0 after: try stacking all segments, or clicking middle blob, or shape-match ideas.

## LEVEL 1 SOLVED (score 1) at action 5
Clear condition (level 1): gray tail sitting in goal outline + chain fully CONTRACTED (head(29,21), blob(34,21), tail(39,21) — centers 5 apart, touching, colinear). Merely having gray (or white) in goal while chain stretched did NOT clear. Goal outline flashed white/purple then level transitioned.
Runner stops remaining plan steps when score changes (steps 2-3 not executed).

## LEVEL 2 layout (settled after action 5, log line ~1943)
- Step budget bar col 0: 5 used.
- ORANGE goal outline r3 centered (40,51).
- Active chain A (ORANGE centers, Y-shape/star, 4 segments):
  - Center: orange 5x5 blob, C center at (24,12)
  - Arm 1: WHITE diamond head at (17,6) (orange center)
  - Arm 2: gray diamond at (49,9) (orange center)
  - Arm 3: gray diamond at (8,21) (orange center)
  - 8-trails: white->blob, blob->(49,9), blob->(8,21)
- Inert chain B (PURPLE): gray diamond (45,35, purple center) - purple blob C (49,41) - gray diamond (54,48, purple center). No white head. Maybe decorative (solved level 1 chain?) or activatable.
- Light blue '(' terrain regions (probably impassable): big lake x~14-38 rows 22-32; left region x1-28 rows 32-54; right x52-63 rows 29-47; small bits. Black 'O' = open.
- Goal area x37-43 rows 48-54 is black/open.

## Level 2 mechanics learned (action 6 probe: click (40,45))
- Head teleports to click point; both grays anchored; BLOB moves to CENTROID of the 3 arm endpoints (exact: ((8+49+40)/3,(21+9+45)/3)=(32.3,25)->(32,25)).
- Move REVERTED on settle: blob landed on blue lake at (32,25). So invalid placement causes full revert (action still consumed). Unknown whether rejection was due to blob-on-blue (likely) or head flight path crossing blue.
- Frames show the attempted state, then settle reverts.

## Level 2 plan sketch
Goal: replicate level-1 clear pattern at orange outline (40,51): a GRAY at (40,51), blob at distance 5, other arms at distance 5 from blob. Candidate final: grayA(40,51), blob(40,46), grayD(36,43), head(44,43) (centroid (40,45.67)->(40,46)?).
To move a gray: click it (role swap, from level 1), then click destination.
Blue map: lake rows 22-32 x~14-38(varies); left-bottom region; right region x52-63 rows 29-47. Verify per-cell from settled board before each click.
- Action 7 probe: ACTION6(43,30): blob centroid -> (33,20) black; head path crosses lake. Tests whether flight path matters.

## Action 7 result: REVERTED again — head flight path (or trails) crossing blue also invalid. Conservative rule: head flight line, blob position, and all blob->arm trail lines must avoid blue/walls/objects.

## Level 2 solution route (validated by simulation, 10 steps):
1. ACTION6(44,20)  move W (17,6)->(44,20)
2. ACTION6(8,21)   swap (head -> piece at (8,21))
3. ACTION6(40,21)  move
4. ACTION6(36,44)  move (arm E2 placed)
5. ACTION6(49,9)   swap
6. ACTION6(40,21)  move
7. ACTION6(40,51)  move (goal piece placed in outline)
8. ACTION6(44,20)  swap
9. ACTION6(41,30)  move (staging)
10. ACTION6(44,44) move -> final: gray(40,51) in goal, blob(40,46), gray(36,44), head(44,44), all touching => expect CLEAR
Chain B gray cells block x43-47 rows 33-37; corridor x40-42 clean. Steps 1-4 submitted as actions 8-11; steps 5-10 next call (verify swap semantics first).

## After actions 8-11: state matches simulation exactly. FLOOR rounding confirmed for blob centroid. Budget bar RESETS per level (reverted actions still consume bar). 
## Actions 12-17 submitted: route steps 5-10 (swap (49,9); (40,21); (40,51); swap (44,20); (41,30); (44,44)) -> expected level 2 clear.

## Actions 12-17: executed perfectly. Final config reached: gray(40,51) in goal, blob(40,46), gray(36,44), head(44,44). Goal outline FLASHING win animation (10 uncovered cells flash, 2 blob-covered cells don't — same as level 1 win). Settled board still level 2; transition presumably on next action. Level 2 effectively SOLVED.
## Win condition (generalized): a GRAY diamond centered in goal outline + all chain segments contracted/touching the blob (links ~5).
## Action 18: harmless wall click (63,0) to advance/reveal level 3.

## Action 18: still Level 2, score 1! Flash persists but NO win. Revised hypothesis: links must be EXACTLY distance 5 (level-1 win had 5,5 exact; current side arms at 4.47). Flash = partial condition met (goal outline occupied correctly).
## Actions 19-22: swap (36,44); move (36,43); swap (44,44); move (45,46). Final: gray(40,51), gray(36,43), head(45,46), blob(40,46) — ALL exact 5.0. Blob stays (40,46) throughout (verified floor centroid).

## Actions 19-22 results: A19 swap ok; A20 click (36,43) NO-OP (within head hitbox); A21 swap ok; A22 click (45,46) NO-OP — head click HITBOX is ~Manhattan radius 3 around center (clicks there = no-op, no move). Must click >=4 away from head center.
## Actions 23-26: swap (36,44); move -> (32,47); swap (44,44); move -> (40,43). Final: gray(40,51), gray(32,47), head(40,43), blob(37,47) — all exactly 5.0 (verified, intermediate blob (38,47) safe).

## Actions 23-26: SUCCESS mechanically — final: head(40,43), gray(32,47), blob(37,47), gray(40,51-goal). ALL links exactly 5.0. STILL NO WIN. Exact-5 alone insufficient.
## New hypothesis: chain B (purple) must also be assembled, and/or the orange chain must contain NO white head (head parked in chain B). Test: click chain B gray (54,48) — if head role transfers cross-chain, orange chain becomes all-gray (might win instantly); then (45,45) contracts chain B vertically: ends (45,35),(45,45), blob (45,40), links 5,5.
## If (54,48) is a no-op: (45,45) will move orange head; blob would go (39,47) overlapping goal diamond -> likely rejected/revert (harmless).

## A27-28: cross-chain head transfer WORKS (clicking any gray moves white role there). Chain B contracted (45,35)-(45,40)-(45,45) links 5,5. Still no win. Chain B now blocks corridor x43-47 rows 33-47.
## Outline GAP theory: outline is r4 diamond ring missing 4 tips; level-1 win chain entered through left tip gap ((35,21)); flash at A17 happened when blob (40,46) sat aligned through TOP gap (40,47). Current blob (37,47) diagonal = no flash/win.
## A29-34 plan: relocate chain B head to (51,43) (blob (48,39), links 5,5, clears corridor); transfer to orange (40,43), move to (44,44) (blob->(38,47)); transfer (32,47), move to (36,44) (blob->(40,46) ALIGNED = A17 flash config); park head at chain B gray (45,35) -> orange chain ALL GRAY + aligned + contracted. Win?
## If still no win: need exact-5 too: arms (36,43)+(45,46) with blob (40,46); (45,46) now unblocked after chain B moved. Approach clicks from >=4 Manhattan away.

## CORRECTION: A34 was NOT a no-op. Board after A34 shows white ring at (45,35) — cross-chain transfer out of flashing anchored chain WORKS. Orange chain now ALL GRAY + anchored/flashing: grays (36,44),(44,44),(40,51-goal), blob (40,46). Head in chain B: white(45,35 purple center), blob(48,39), gray(51,43).
## PURPLE OUTLINE discovered at center (57,18) — same r4 12-cell ring, gaps at tips (57,14),(57,22),(53,18),(61,18). Win hypothesis: BOTH chains anchored at same-colored outlines.
## A35-40 submitted: anchor chain B at (57,18) via left gap:
1. ACTION6(51,43) swap -> head (51,43)
2. ACTION6(51,27) move (vertical, x51 clear of blue x52+; blob->(48,31), no overlaps)
3. ACTION6(47,18) move (blob->(46,26))
4. ACTION6(45,35) swap
5. ACTION6(57,18) move -> ends (47,18),(57,18), blob (52,18) aligned via gap (53,18), links 5,5
6. ACTION6(47,18) swap -> GRAY at (57,18) in goal, head (47,18). Expect WIN.
Note: avoided direct (51,43)->(47,18) flight because it crosses own blob (48,39) — unknown if own-blob overflight is legal.
If no win: orange links are 5,4.47,4.47 — fix orange to exact-5 config: arms (36,43)+(45,46), blob (40,46) (centroid floor checks out: (40+36+45)/3=40, (51+43+46)/3=46). Requires staging hops due to hitbox (clicks <4 Manhattan from head = no-op).

## LEVEL 2 SOLVED (score 2) at action 39 — win triggered when HEAD landed at purple goal center (57,18) with blob (52,18) gap-aligned links 5,5 AND orange chain anchored (5,4.47,4.47). So: win = ALL chains anchored at same-colored outlines; head-in-goal OK; links need NOT all be exactly 5 (goal link 5 through gap + others ~touching suffices). Final swap unneeded.

## LEVEL 3 layout (settled after action 39):
- GREEN chain (4 arms + blob): head WHITE (14,16), grays (34,9),(39,16),(23,21), blob (27,15) — top region.
- PURPLE chain (linear): grays (37,34),(53,40), blob (45,37) — midfield.
- GREEN outline r4 center (55,53), gaps (55,49),(55,57),(51,53),(59,53). PURPLE outline r4 center (34,57), gaps (34,53),(34,61),(30,57),(38,57).
- Terrain: top region rows 1-25; river rows 26-27 blue x>=23 (only west corridor x5-22 passes rows 23-31); mid region rows 32-42 x5-50ish; second river rows 43-46 blue x5-44, ONLY crossing x45-59 (row 43), x49-61 (row 44), x48-63 (rows 45-46); bottom region rows 47-63. Bridge pocket rows 28-31 x26-48 connects mid only.
- /workspace/sim.py: simulator with State/click validation (flight, blob 5x5, trails vs blue '(#$'). Reuse it (reads latest settled board).
- Outline RING cells are passable for flights (level-1/2 evidence); blob/diamond may cover ring cells. Blob-arm dist 4.47 (1-cell overlap) proven legal.

## A40-50 submitted (purple relocation, validated in sim):
(37,34)transfer; (47,43); (61,45); (53,40)swap; (53,49); (44,57); (61,45)swap; (56,62); (34,62); (34,57) -> purple final (34,57),(39,57)blob,(44,57) links 5,5 via right gap = ANCHORED; then (23,21) transfer head to green.
Risk: step2 blob (50,41) sits 3.16 from arm (53,40) (2-3 cell overlap) — if rejected, step 3 (61,45) self-recovers (flight from (37,34) valid, blob (49,39) valid).

## GREEN plan (next turns): final plus-config: goal arm (55,53), blob (50,53) via left gap, arms (50,48),(50,58),(45,53) (centroid floor = (50,53) exact, all links 5).
Phase 1 (head at (23,21)): move arms down west corridor into mid region rows 32-42 (validated candidates: (23,21)->(14,33)ish routes; rows 24-31 tight: row 28 blue x22-30, row 25 blue x26-29, row 26 blue x24+, row 27 blue x23+).
Phase 2: cluster east (x41-50 rows 39-42), cross x49-59 rows 43-47 one arm at a time, keep blob/trails valid (blob center x in [51,59] at row 44-ish crossing).
Phase 3: place plus-config; trails/blob may cover green ring cells. Purple final cells occupy x32-46 rows 55-59 — avoid in green flights along bottom.

## Actions used so far: 51 (after this batch)

## Level 3 GREEN route — VALIDATED ([DATE] turn)
Full 22-click sequence passes sim (all moves OK, worst blob-arm overlap = 1 cell, same as proven 4.47 class):
seq=[(16,33),(39,16),(8,34),(34,9),(12,40),(14,16),(24,41),
     (44,37),(16,33),(44,33),(12,40),(52,36),(8,34),(55,38),
     (52,36),(59,51),(44,33),(55,53),(44,37),(51,45),(55,38),(55,43)]
- Stage A (0-6): arms descend west corridor -> arm3 (16,33), arm2 (8,34), arm1 (12,40), arm0 (24,41). Blob (15,37).
- Stage B (7-13): cluster east -> arm0 (44,37), arm3 (44,33), arm1 (52,36), arm2 (55,38). Blob (48,36).
- Stage D (14-21): far-first descent: arm1->(59,51) [blob (50,39)], arm3->(55,53) [blob (53,44)],
  arm0->(51,45) [blob (55,46)], arm2->(55,43) [blob (55,48) = FINAL, all links 5.0] => WIN expected.
SUBMITTED first 20 clicks this turn (through arm0->(51,45)).
REMAINING NEXT TURN: ACTION6(55,38) [transfer arm2], ACTION6(55,43) [final move -> win].
Key terrain fixes vs old draft: (19,31) first hop invalid (trail hits (22,28) blue); row 34 blocked x53-56
so old cluster spot (56,34) replaced by (55,38); arm0 uses (24,41)/(44,37) to keep blob means clear of arms.
sim.py State() updated: P anchored arms (34,57),(44,57) blob (39,57); head starts G arm3 (23,21).
Actions used before this turn: 50 (11 into level 3). This turn +20 -> 70 total.

## Turn update (actions 51-70 executed)
All 20 green-route clicks executed flawlessly; board matches sim exactly:
arms (55,38),(51,45)[head],(59,51),(55,53), blob (55,46). Purple still anchored (39,57).
THIS TURN submitted final 2 clicks: (55,38) transfer -> (55,43) move => blob (55,48), all links 5.0 => expect score 3 / level 4.
Total actions after this turn: 72.

## LEVEL 4 (started action 73, score 3, budget bar full 64)
Three chains (blob=floor mean of arms CONFIRMED):
- chain1: arms purple-pip (39,6)gray, (23,20)WHITE HEAD; blob (31,13) tri-color (orange NW/green NE/purple bottom)
- chain2: arms green-pip (17,36),(10,47),(27,52); blob (18,45) (green W/yellow E)
- chain3: arms blue-pip (46,36),(46,52); blob (46,44) (blue W/red E)
8 rings (r4): (20,8) ltmag/mag | (50,12) green/yellow = chain2 MATCH | (12,17) orange/ltblue |
 (53,28) maroon | (14,29) blue-top/orange-bottom | (36,49) orange/green/purple = chain1 MATCH |
 (17,54) blue/red = chain3 MATCH | (55,54) green/ltblue. 5 non-matching rings = decoys? unknown.
HYPOTHESIS (testing now): blob must be centered IN its pattern-matched ring (patterns match incl orientation),
arms at dist 5 through gaps. Fallback = L1-3 arm-in-ring (arm center in ring, blob at 5, arms at 5).
Terrain: big lake x~25-47 rows 22-38 (W edge ~x25-28 rows 28-38, E edge x40-43); W corridor x8-24 open rows 22-44;
E corridor x44+ open; walls '#' frame + row 61-63 center x33-49.
THIS TURN (10 clicks): nudge chain2 arm (17,36)->(13,36) (clears W flight lane), then chain1:
head (23,20)->(18,39) W descent [blob(28,22)]; transfer (39,6); ->(52,44) [blob(35,41)]; ->(42,51) [blob(30,45)];
->(36,54) [blob(27,46)]; transfer (18,39); ->(36,44) => blob (36,49) IN RING, links 5/5. WATCH FOR ANCHOR/FLASH.
If no anchor: convert to arm-in-ring with 3 clicks: (36,39) move, T(36,54), (36,49) move -> arms (36,39),(36,49), blob (36,44).
Chain2 final candidates (blob-in-ring (50,12)): arms (46,10),(54,10),(50,16) or (46,14),(54,14),(50,8) (mean exact).
Chain2 route: N via W corridor AFTER chain1 top pieces leave; top crossing to NE.
Chain3 final: arms (12,54),(22,54), blob (17,54) IN ring; route S of chain2 diamond (27,52) once it moves.
Actions before this turn: 72. This turn +10 -> 82.

## Turn update (actions 73-82 executed) — BLOB-IN-RING CONFIRMED
Chain1 anchored: blob (36,49) centered in tri-color ring -> 21-frame flash, RING CELLS TURNED WHITE.
Win rule for L4: each blob centered in its pattern-matched ring; arms attached ~4-5 via floor-mean.
THIS TURN (16 clicks): chain2: T(27,52)->(18,20); T(13,36)->(30,12)->(46,10); T(10,47)->(12,24)->(50,16);
T(18,20)->(54,10) => blob (50,12) IN RING (links 4.47/4.0/4.47 — exact mean forces this; 4.47 proven L2).
chain3: T(46,52)->(40,58); T(46,36)->(17,49); T(40,58)->(17,59) => blob (17,54) IN RING (5.0/5.0). WIN expected.
If no win: check which ring is NOT white -> likely chain2 link lengths; re-rig chain2 arms.
Route lessons: anchored chain1 column x33-39,y42-56 is a wall; S crossings must use y>=57 (x36 crossing at y58 OK);
chain2 blob (16,45) blocked (17,49) until chain2 left; (27,52) diamond blocked SW until moved.
Actions after this turn: 98 (26 into level 4, budget 64).

## Level 5 (started action 99, budget 64)
Board inventory (programmatic detectors):
- RINGS (r4, 12 cells, two half-colors): (48,9) green-W/yellow-E; (15,15) blue-top/orange-bottom; (57,18) ltmag-top/mag-bottom; (13,28) blue-W/red-E; (53,28) all-green.
- PADS (5x5 corner-cut blob shapes, half-colored/half-white): (33,19) white-W/red-E; (14,40) blue-W/white-E; (56,43) white-W/yellow-E; (20,53) green-W/white-E.
- Chain A: arms (25,35)[HEAD], (43,34); blob (34,34) all-white. Chain B: arms (41,47),(34,55),(52,55); blob (42,52) all-white. Floor-mean verified.
- Terrain mostly open; wall wedges top (x23-40 rows 0-8, x56-63, x1-8), '#' x1-3 rows ~33-50, bottom walls rows 62-63 center.

THEORY (paint-and-deliver): blob anchors/visits ring to acquire ring's two half-colors, then delivers each colored half to matching pad (pad shows one half colored = required, white half = wildcard). Pairings: ring (13,28) -> pads (33,19) red-E + (14,40) blue-W; ring (48,9) -> pads (56,43) yellow-E + (20,53) green-W. Rings (15,15),(57,18),(53,28) presumed decoys/alternates.

Probe (actions 99-104, sim-validated zero rejects):
(18,28) move; (43,34) transfer; (8,28) -> blob (13,28) IN RING [observe paint]; (38,21) -> blob (28,24) [tests mobility after ring]; (18,28) transfer; (28,18) -> blob (33,19) ON PAD [observe delivery].
Observables next turn: blob color change after step 3? flash/whitening at pad after step 6? chain locked after ring (steps 4-6 reject)?

### L5 probe results (actions 99-104, all executed, score still 4)
- Ring visit (blob centered (13,28)) did NOT paint blob (still white after leaving) and did NOT flash (2-frame anim only). Ring intact.
- Blob on pad (33,19): displays white-W/RED-E (pad's pattern). => THEORY REVERSED: pads are PAINT SOURCES, rings are GOALS (L4 rule: blob pattern must match ring pattern incl. orientation).
- Pairings: pads (33,19) red-E + (14,40) blue-W -> ring (13,28) blue-W/red-E. Pads (56,43) yellow-E + (20,53) green-W -> ring (48,9) green-W/yellow-E. Rings (15,15),(57,18),(53,28) = decoys (no matching pad colors).
- Trail cells render as blob's color ('8' off-white for white blob), not gray.

### Actions 105-110 plan (sim-validated, zero rejects)
(9,38) move [check: red-E persists off pad?]; (38,21) transfer; (20,42) -> blob (14,40) BLUE PAD; (17,31) move; (9,38) transfer; (9,25) -> blob (13,28) IN RING, arms dist 5.0/5.0 -> expect 22-frame flash/anchor.
Chain B next: pads (56,43),(20,53) then ring (48,9). B arms (41,47),(34,55),(52,55), blob (42,52).

### L5 confirmed mechanics (actions 105-110)
- Paint persists off pad; pads consumed after use. Blob became blue-W/red-E, anchored ring (13,28): 21-frame flash, ring whitened. Score still 4 (need both rings).
- L5 rule = collect pad half-colors to match ring pattern (orientation matters), then blob-in-ring anchor (L4 rule).

### Actions 111-124: chain B (sim zero rejects/warnings)
transfer(41,47); (58,39); transfer(34,55); (59,36)->blob(56,43) YELLOW PAD; (15,50); transfer(58,39); (25,50); transfer(52,55); (21,59)->blob(20,53) GREEN PAD; (48,4); transfer(25,50); (44,12); transfer(15,50); (52,12)->blob(48,9) RING ANCHOR (arms all dist 5.0). Expect flash + score 5.

## Level 5 CLEARED (score 5, action 124, 22-frame flash on ring (48,9) anchor). 26 clicks total, zero rejects.

## Level 6 (starts action 125, budget 64)
- Chains: A arms (11,11)H,(4,19),(22,19) blob (12,16); B arms (50,43),(51,57) blob (50,50).
- Rings (4-quadrant): (51,12) purple-NW/green-NE/blue-S; (29,31) ltmag-top/mag-bottom [DECOY: no ltmag pad]; (11,55) yellow-NW/mag-E/ltblue-SW.
- Pads (quadrant-colored): (39,6) red-NW [decoy], (34,17) green-NE, (56,23) maroon-E [decoy], (45,30) mag-E, (11,33) blue-S, (32,44) yellow-NW, (16,45) purple-NW, (25,55) ltblue-SW, (38,57) orange-NW [decoy].
- NOTE: pad rendering slightly ragged; use component-detector centers, not eyeball.
- Assignment: chain A -> pads (16,45),(11,33),(34,17) -> ring (51,12) [this turn, 14 clicks actions 125-138, arms (47,15),(55,15),(51,7) all dist 5.0; 3-arm all-5.0 works if offset sums give floor mean = center].
- Chain B -> pads (45,30) mag-E, (32,44) yellow-NW, (25,55) ltblue-SW -> ring (11,55), anchor arms (7,52),(15,58) dist 5/5. CAUTION: '(' cells in pad (25,55)/ring (11,55) SW are objects, not lake — must patch sim blocked() before validating chain B (currently blocks '(').
- Chain B draft route (unvalidated): T(50,43),(44,26),T(51,57),(48,35)->mag; (36,48)... wait recompute with center (45,30): needs sums x 90-92,y 60-62. Draft: T(50,43)->(44,26): blob? arms (44,26),(51,57): (47,41); T(51,57)->(47,35): sums (91,61) -> blob (45,30) MAG. Then yellow (32,44): sums 64-66/88-90: (28,40),(37,48)? (65,88)->(32,44) OK. Then ltblue (25,55): sums 50-52/110-112: (21,51),(30,60)? (51,111)->(25,55) OK. Then ring: (7,52),(15,58).

### L6 actions 125-138 result: REJECT at action 131 click(5,6) — NEW RULE: arm's r2 diamond must avoid '#' walls ((5,4)/(4,5) are wall). Sim now checks this.
- Rejects do NOT stop the runner; later clicks executed with shifted state. Blue+green pads missed, anchor failed (2-frame anim only).
- State after 138: A arms (21,41),(47,15),(55,15), blob (41,23) purple-NW painted, head A2. B arms (49,43),(50,57), blob (49,50) [corrected: eyeball was off-by-one; ALWAYS use pip detector].
- Floor-mean rule re-confirmed: (123/3,71/3)->(41,23); B (99/2,100/2)->(49,50).

### Actions 139-149 recovery (sim-validated): (7,29); T(21,41); (17,29); T(47,15); (9,43)->blob(11,33) BLUE; (47,15); T(17,29); (48,8)->blob(34,17) GREEN; (51,7); T(7,29); (55,15)->blob(51,12) ANCHOR d5/d5/d5.
### Chain B next (recompute from corrected arms (49,43),(50,57)): mag-E (45,30), yellow-NW (32,44), ltblue-SW (25,55), ring (11,55) arms (7,52),(15,58). Patch sim '(' handling first (pad/ring '(' cells are objects, not lake; but keep caution on whether game blocks them).

### L6 chain A ANCHORED at ring (51,12), action 149, 21-frame flash. Score still 5 (level needs both rings).
### Actions 150-162: chain B (sim-validated; sim '(' unblocked — no lake this level):
T(49,43); (41,26); T(50,57); (49,35)->blob(45,30) MAG; (36,48); T(41,26); (28,40)->blob(32,44) YELLOW; (21,51); T(36,48); (29,59)->blob(25,55) LTBLUE; (15,58); T(21,51); (7,52)->blob(11,55) RING ANCHOR d5/d5. Expect flash + score 6.
Risk noted: if game treats '(' pad/ring cells as blocking (lake semantics), the (29,59) click or anchor may reject — diagnose via missing frames next turn.
