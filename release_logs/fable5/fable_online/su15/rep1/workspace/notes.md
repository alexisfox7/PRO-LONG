# Game notes

## Level 1 initial state
- Top strip rows 0-9 background 'q' (UI?): purple 3x3 at (30-32,4-6) = target color indicator?
- Blue creature 'f' blob rows 11-19 cols 44-53, gray 'h' eyes at (47-49,14-16), mouth detail (46,17)
- Gray 'h' dotted trajectory: (44,19),(42,21)...(12,51),(8,55),(6,57) — step (-2,+2), i.e. direction (-1,+1)
- White '$' plus centered (10,53) sits on trajectory (fills the (10,53) dot slot)
- Purple 3x3 target at (3-5,58-60); trajectory extrapolates to center (4,59)
- White floor row 63

## Hypotheses
- H1: click landing cell / target to fire or score. Test: ACTION6(4,59)
- H2 (if H1 fails): click creature to fire; or click sets aim direction

## Findings
- Clicking empty/target cell (4,59): only a contracting white ring animation (click feedback), no game effect.
- Row 63 white bar = step budget: 64 cells, -2 per action => ~32 action budget. Don't waste clicks.

## Action log
- Turn 1: ACTION6(4,59) — no effect, budget -2
- Turn 2: ACTION6(48,15) — no effect (ring feedback only), budget -2. Creature click is no-op.
- Turn 3 results:
  - Click white plus (10,53): purple 3x3 MOVED from (3-5,58-60) to (9-11,52-54) (plus slot). Plus = "move here" marker. Budget -2.
  - Click UI purple (31,5): ZERO diff, no budget cost. Top strip clicks are free no-ops.
  - Click dot (32,31): no effect, budget -2.
- Theory: goal = move purple block along dotted path UP to blue creature (feed it). Path dots spaced 2, direction (+1,-1) toward creature at (44,19)->mouth.
- Turn 4 results:
  - Click purple block itself: no-op, budget -2.
  - Click adjacent dot (12,51): block hopped there, left 'h' dot at old center (10,53). WORKS.
- Mechanic: click trail dot to move block there. Far dot (32,31) failed earlier — range limited? Plus-marker jump was 3 dots.
- Trail dots up from (12,51): (14,49),(16,47),(18,45),(20,43),(22,41),(24,39),(26,37),(28,35),(30,33),(32,31),(34,29),(36,27),(38,25),(40,23),(42,21),(44,19), then creature mouth.
- Budget: 52 cells = 26 actions left after turn 4.
- Turn 5 results: 2-dot hop (12,51)->(16,47) WORKED; then ->(18,45). Range >=2. Old center leaves 'h' dot.
- Block now at (18,45). Remaining dots: (20,43),(22,41),(24,39),(26,37),(28,35),(30,33),(32,31),(34,29),(36,27),(38,25),(40,23),(42,21),(44,19) then mouth.
- Budget: 48 cells = 24 actions.
- Turn 6 results: 3-dot hops WORK. Block at (30,33). Hop range >=3 (11 fails). Budget 44 cells = 22 actions.
- Turn 7 results: hops to (36,27),(42,21) then (44,19) -> SCORE 1, LEVEL 1 CLEARED. Delivering colored block along trail to creature = win.

## Level 2 (fresh budget 64)
- Palette UI top-left rows 1-2: lightblue swatch cols 1-2, magenta 5-6, purple 9-10, yellow 13-14.
- Target indicator in q-strip: YELLOW 4x4 at (30-33,3-6).
- Big eyeless blue creature rows 23-31 cols 29-38.
- Scattered '(' lightblue dots: (18,37),(42,37),(37,40),(16,41),(50,54),(14,55),(48,56),(16,57).
- Turn 8 results: palette yellow click = FREE NO-OP (legend only). Creature click = no-op, -2. Budget 62 cells.
- Turn 9 results:
  - Click near dot at (41,37): merged with NEAREST dot (37,40) -> 2x2 MAGENTA block at (41-42,36-37). Growth: lightblue 1x1 -> magenta 2x2 -> purple 3x3 -> yellow 4x4 (palette = size legend; indicator = goal 4x4 yellow).
  - Click on the block itself: no-op, -2.
- Remaining dots: (18,37),(16,41),(50,54),(14,55),(48,56),(16,57). Block at (41-42,36-37). Budget 56.
- Turn 10 result: click dot (18,37) made a SECOND 2x2 magenta at (17-18,36-37) absorbing ITS nearest dot (16,41). Blocks don't grow by dot clicks; equal sizes must merge pairwise: 1+1->2x2 magenta, presumably 2+2->3x3 purple, 3+3->4x4 yellow.
- State: magenta A (41-42,36-37), magenta B (17-18,36-37); dots left: (50,54),(14,55),(48,56),(16,57). Budget 54.
- Earlier solo-block click no-op likely because no merge partner existed.
- Turn 11 results:
  - Click (41,36) top-left cell of A: A moved up-left 1 so clicked cell became its bottom-right corner. (Explains a18 no-op: clicked cell WAS already bottom-right.) Movement = block relocates anchored to click?
  - Dot merges OK: C at (49-50,53-54) [absorbed (47,56)], D at (13-14,54-55) [absorbed (16,57)].
- State: magentas A(40-41,35-36), B(17-18,36-37), C(49-50,53-54), D(13-14,54-55). No dots left. Budget 50=25 actions.
- Level 1 movement range was >=6 cells (3 dots), 22 cells failed.
- Turn 12 results: free movement CONFIRMED. Click cell -> block moves so clicked cell = bottom-right corner (2x2). Jumps of 5-6 cells fine. A now (29-30,35-36). Budget 46=23 actions.
- Turn 13 results:
  - Click (24,36): A AND B both jumped to click and MERGED -> purple 3x3 at (23-25,35-37) centered on click. Click attracts all equal blocks within range (~6-7).
  - Click (18,37): purple re-centered there (17-19,36-38). 3x3 centers on click.
- State: purple P1 center (18,37); magentas C(49-50,53-54), D(13-14,54-55). Budget 42=21 actions.
- Turn 14: all 9 actions worked. YELLOW 4x4 at (16-19,38-41); click cell anchors at (x-2..x+1,y-2..y+1). Budget 24=12 actions.
- Turn 15 results: yellow at (28-31,30-33), overlaps creature edge cells — NO score yet. Edge contact insufficient.
- Turn 16 result: yellow fully inside creature -> SCORE 2, LEVEL 2 CLEARED. Delivery = block fully inside creature (edge overlap not enough).

## Level 5 (fresh budget 64)
- SCORE 4: L4 cleared at Action 114 via bait->merge->2 hops->deliver (3-6,54-57). Win registers on placement click.
- L5: indicator YELLOW 4x4 only. Creature at TOP: rows 11-19, cols 28-36 (row11:30-34, row12:29-35, row13:28-36, rows13-17 full 28-36, row18:29-35, row19:30-34).
- Pieces: 4 magentas: M-A(6-7,25-26), M-B(42-43,26-27), M-C(53-54,26-27), M-D(14-15,28-29). 4 dots: (44,53),(14,54),(58,59),(3,60). Units 12, need 8 -> dots are SACRIFICIAL decoys (rings can eat all 4).
- TWO rings: R1 c(6,38.5), R2 c(48,38.5). Each chases ITS nearest piece. 2-ACTION FUSE: each ring eats nearest magenta (d~12.4) on its 2nd drift. Both sides must be defused in acts 1-2.
- Turn 29 (4 acts): bait R1 (3,44) [lunges to ~(0,50), then chases/eats bottom-left dots = busy ~5 acts]; bait R2 (47,40) [R2 at drift1 (50.3,33.3), lunges to ~(44.8,44.5), eats bottom-right dots]; left merge (11,23)->P-left(10-12,22-24); right merge (48,26)->P-right(47-49,25-27).
- Master plan (13 acts total): walks P-left (16,20),(21,18),(26,17); P-right (43,23),(39,21),(35,20); MERGE (30,18)->YELLOW(28-31,16-19); bait R1 (17,25) [R1 will be ~6 away pre-delivery]; deliver (31,15)->(29-32,13-16) fully inside = WIN.
- Drop branches: act1 drop -> R1 closes on P-left by act4, RESCUE next turn with flee click >=12 from R1 (e.g.(14,17)); act2 drop -> R2 eats M-C at act3 (-1 unit, still 11>=8, replan right side with M-B+dots).

- Turn 29 results: ALL 4 OK. R1 lunged->(2,50.5), ate dot(3,60) act117, now (7,54.5) chasing dot(14,54) d7. R2 (initially targeted M-B side, tie-break) lunged->(52,46.5), ATE dot(44,53) act118 (drift STOPS ON prey when eating), now (46,52.5) chasing dot(58,59) d13.6. P-left(10-12,22-24), P-right(47-49,25-27) formed. Dots left: (14,54),(58,59). Budget 56.
- Ring timeline: R1 eats (14,54) ~act+1, then chases P-left from d~30 (arrives ~act+7). R2 eats (58,59) ~act+3, then P-right from d~25+.
- Turn 30 (6 acts): P-left (16,20)->(15-17,19-21); P-right (43,23)->(42-44,22-24); P-left (21,18)->(20-22,17-19); P-right (39,21)->(38-40,20-22); P-right (35,20)->(34-36,19-21); P-left (26,17)->(25-27,16-18) [may pull P-right d8.25 -> early merge yellow (24-27,15-18) = fine, deliver via (30,16)].
- Turn 31 endgame: bait R1 (~(20.6,26.7) projected; click (14,31)); merge (30,18)->YELLOW(28-31,16-19); deliver (31,15)->(29-32,13-16) inside creature = WIN. If early-merged: deliver (30,16)->(28-31,14-17) inside = WIN.

- Turn 30 results: all 6 walks OK. P-left(25-27,16-18), P-right(34-36,19-21). Rings ate all 4 decoy dots; units exactly 8. R1 (25,37.5) inbound, R2 (44,46.5). Budget 44. Pull-range refined: 7.6 pulls, 8.25 does NOT.
- L4 frame check: ring speed vs existing 4x4 yellow = 5.66 (no speedup; the 12.5 moves are click-triggered lunges only).
- Turn 31: SINGLE action (31,15): pulls P-left (d4.1) + P-right (d5.0) -> merge YELLOW anchored (29-32,13-16) = fully inside creature -> expected instant WIN (merge+delivery in one click). Rings 23+/33+ away, safe. If merge-formation doesn't trigger win check: yellow sits inside; next turn nudge (31,14) re-anchors (29-32,12-15) also inside.

## Level 6 (fresh budget 64)
- SCORE 5: L5 cleared in 15 actions via one-click merge+delivery at (31,15).
- L6: indicator YELLOW 4x4. Palette now 6 tiers: (1x1, C2x2, "3x3, G4x4, -orange(5?), n red(6/7?). UI also shows a z-ring icon at (36-40,3-6) next to indicator.
- Board: RED 7x7 block (33-39,32-38) c(36,35) — ONLY piece. Ring c(18,35.5) d~15 (3 drifts to eat). TWO creatures: top-left (2-10,12-20), bottom-right (52-60,53-61).
- Hypothesis: ring-eat degrades piece one tier (L4 evidence) -> feed red to ring 2-3x until yellow 4x4 emerges, then deliver. Which creature accepts = unknown (wrong = harmless no-op).
- Turn 32 recon (3 acts): (40,40) test red movability [if moves: centers (37-43,37-43)]; (46,45) continue toward bottom-right creature or safe no-op; (52,49) ditto. Ring drifts toward red meanwhile; watch for first EAT (displacement + resulting size!).

- Turn 32 results: RED IS MOVABLE, 7x7 centers on click. Red walked to (49-55,46-52) beside bottom-right creature. Ring chasing: (30,47.5), d19 to red. Budget 58.
- Bottom-right creature exact shape: row53:54-58, row54:53-59, rows55-59:52-60, row60:53-59, row61:54-58. Fully-inside 4x4 delivery: anchor click (55,57)->(53-56,55-58).
- Feed plan: let ring eat red repeatedly (degrade one tier + displace each eat). AFTER YELLOW APPEARS: ring is adjacent and will re-eat within ~1-2 actions -> deliver IMMEDIATELY (one click to (55,57) if in range) or bait ring away first.
- Turn 33 (3 acts): no-op clicks (10,40),(10,42),(10,44) far from everything; ring closes 19->13.3->7.7->~2: first EAT expected on act 3. Observe displacement + resulting tier/size.

- Turn 34 results (acts 129-133): ring crept to (46,48.5) then ATE red at act 133. EAT MECHANIC: red 7x7 -> ORANGE 5x5, EXPELLED directly AWAY from ring (slid east to wall, settled (59-63,46-50)). Palette-tier degrade: red->orange->yellow(next!). Ring settled (45-49,47-50) c(47,48.5). Budget 48.
- Turn 35 (5 acts): (60,54) orange->(58-62,52-56); BAIT (46,45) ring->( ~42.7,42.3); (56,57) orange->(54-58,55-59) inside creature footprint; no-ops (10,50),(10,52) -> ring returns and EATS orange ~act5, YELLOW expelled SE toward corner (~(60-63,57-60)).
- Turn 35 results (acts 134-138): all 5 OK but eat NOT yet triggered. Orange parked (54-58,55-59) inside creature footprint. Bait (46,45) lunged ring from d9.0 (lunge trigger extends to >=9.0) to (43,40.5); ring drifted back SE via (47,44.5),(51,48.5) to c(55,52.5), now d2.5 from orange. Budget 38.
- Turn 36 (1 act): time-advance click (10,54) far from everything -> ring lands on orange, EATS: orange->YELLOW 4x4 expelled SOUTH (ring approaches from north). Stop to observe landing (expected ~(54-58,59-62), maybe wall-clipped). Then bait+rescue per plan below.
- Turn 36+ plan: BAIT ring away NW first (it sits on eat spot adjacent to yellow — rescue click order-of-ops risk), then move yellow to full-inside anchor: click (58,59)->(56-59,57-60) or (59,57)->(57-60,55-58) depending on landing. WIN.

## Level 3 (fresh budget 64=32 actions)
- Indicators: YELLOW 4x4 (30-33,3-6) AND PURPLE 3x3 (36-38,4-6). Two targets!
- Creatures: left blob (5-13,46-54) center ~(9,50); right blob (19-27,46-54) center ~(23,50).
- Dots 1x1: D1(31,15),D2(31,22),D3(12,23),D4(55,23),D5(61,23),D6(8,28). Magentas 2x2: M1(18-19,16-17),M2(46-47,22-23),M3(30-31,32-33).
- Unit math: 6*1+3*2=12 = yellow(8)+purple(4). Exact.
- Merge rule: click attracts equal pieces within ~6 (nearest-cell distance); merged piece centers/anchors at click. 2x2 anchor: click=bottom-right. 3x3: click=center. 4x4: click=(x-2..x+1,y-2..y+1).
- Turn 17 plan: merges: (31,19) D1+D2->M4; (58,23) D4+D5->M5; (10,25) D3+D6->M6; (24,18) M1+M4->P1; (52,23) M2+M5->P2.
- Turn 17 results: all 5 merges OK. P1(23-25,17-19), P2(51-53,22-24), M6(9-10,24-25), M3(30-31,32-33). Budget 58 (only -6 for 5 actions? merge clicks may be free-ish).
- Turn 18 (9 actions): M6 walk (15,28),(20,31); merge M3+M6 at (25,32)->P3; P1 walk (24,24); merge P1+P3 at (24,28)->YELLOW(22-25,26-29); yellow hops (24,35),(24,41),(24,47),(23,50)=fully inside RIGHT creature. Creature-color assignment UNTESTED — if not eaten, move yellow out to left creature (9,50).
- Turn 18 results: chain worked; yellow (21-24,48-51) fully inside RIGHT creature but NOT eaten, score 2. Wrong creature or needs both delivered. Budget 46=23 actions.
- Turn 19 results: SCORE 3, LEVEL 3 CLEARED. Yellow->left creature + purple->right creature. (Wrong-creature delivery = harmless no-op, recoverable.)

## Level 4 (fresh budget 64=32 actions)
- Indicator: YELLOW 4x4 only. One creature rows 53-61 cols 1-9 (9-wide rows 55-59).
- 8 dots: (5,26),(11,26),(31,27),(36,29),(8,41),(12,47),(33,47),(30,51). No magentas.
- NEW object: lightmagenta 'z' ring at (52-56,19-22) — unknown, avoiding it (far from all activity).
- Turn 20 FAILED: the 'z' RING IS AN ENEMY. Phase-1 behavior: moves 4 Chebyshev/action toward NEAREST piece; on contact EATS piece (M2 2x2 -> degraded to displaced 1x1 dot), creature+indicator turn gray '#' = level unwinnable (units exact). After fail-state, ring speeds to ~12/action erratic.
- Ring contact radius ~3 from center (hollow circle 5x4).
- RULES: never leave the ring's nearest-piece target stationary when ring within ~7; kite with 6-hops (gain ~2/action); merge only when ring >=10 from participants; avoid corners (bottom-left death trap).
- Turn 21: RESET; then (34,28) C+D->M2; kite M2 down-left (33,34),(32,40),(26,43); merge G+H at (31,49)->M4.
- Projected end state: ring ~(34,36) chasing M2 (25-26,42-43) Cheb ~8.5; M4 (30-31,48-49) Cheb ~12.
- Turn 21 results: reset OK; merge C+D->M2 OK; hop (33,34) OK; **click (32,40) SILENTLY DROPPED** (zero diff, no budget, no ring move — same as act73 anomaly; ~10% click drop rate?). (26,43) was then out of range (harmless). G+H->M4 OK.
- State: M2 (32-33,33-34) DANGER ring c(38,33.5) Cheb 5.5; M4 (30-31,48-49); dots A(5,26),B(11,26),E(8,41),F(12,47). Budget 56=28.
- Turn 22 (4 acts): kite M2 (28,37),(23,41); merge M2+M4 at (27,45)->P2; P2 flee (21,48). Drop-cascade risks accepted; if a1 drops M2 likely eaten -> reset.
- Turn 22 results: all 4 clicks OK. P2 (20-22,47-49). RING MODEL REVISED:
  - Speed scales with largest piece: ~4/action when <=2x2, ~12.5/action once a 3x3 exists. OVERSHOOTS: moves fixed ~12.5 euclid toward nearest piece, passes THROUGH harmlessly; eats ONLY if final landing center within ~3 of piece (attempt1 kill: landed d2.5; survived d3.35+).
  - Ring now OSCILLATES stably around stationary P2: endpoints ~(18,40.5) and ~(22.6,52). Landing distances to P2 ~4.9/8 = stable trap. Keep P2 STATIONARY as bait anchor!
- Turn 23 (5 acts, all far from ring, keep >P2-distance to avoid retarget): (9,46) E+F->M3(8-9,45-46); (8,26) A+B->M1; M1 walk (8,32),(8,38); merge M1+M3 at (8,42)->P1(7-9,41-43).
- Then: P1 hop (15,46)-ish, merge P1+P2 at (18,47)->YELLOW(16-19,45-48); deliver 3 hops to creature (5,57). Watch: yellow may raise ring speed further (24?).
- Turn 23/attempt-2 FAILED at Action 92: "stable oscillation" was WRONG — ring CREPT ~5.66/action onto stationary P2 and ate it. NEVER park a piece as bait.
- FINAL RING MODEL: drift ~4-5.66/action toward nearest piece. If click lands within ~10 of ring center -> LUNGE 12.5±1.5 toward/past click. Eats only if final landing center within ~3-3.3 of a piece (piece degrades one tier + expelled; level grays = dead).
- SAFETY RULES: (a) no clicks with d(ring,click) in [8.6,11.9] death band; (b) clicks <=8.5 OK only if worst-case landings (11.5-14.5 along ring->click dir) >=4.5 from every piece; (c) clicks >=12 -> plain drift; (d) no piece may end an action within ~9 of ring unless it moves next; (e) bait click = no-op click <=8.5 from ring into empty space, throws ring ~12.5 away, buys 2-3 actions.
- Turn 24 (attempt 3 opening, 5 acts): RESET; (34,28) C+D->M2(33-34,27-28); (31,49) G+H->M4(30-31,48-49) while ring far; kite M2 via (33,33) and (32,39).
- Turn 24 results: all 5 OK. M2(31-32,38-39), M4(30-31,48-49), dots A(5,26),B(11,26),E(8,41),F(12,47). Ring drifted (54,20.5)->(38,35.5) at ~5.5/act toward M2 (d 6.9!). Budget 59 cells (odd decrements: merges ~-1, hops -2?).
- KEY INSIGHT: flee hops gain only ~0.5-1.5/action vs ring drift 5.66 — BAITS (lunge throws ring ~12.5) are the only way to gain distance. Drift CAN eat (attempt-2 P2).
- Turn 25 (4 acts): bait (43,31) [ring lunges to ~(47.5,27.5)]; merge M2+M4 at (29,44)->P2(28-30,43-45); P2 flee (24,49)->(23-25,48-50); flee (19,52)->(18-20,51-53). Projected ring end ~(34.6,39.2), d to P2 ~19. If bait DROPPED: ring ends ~(25.4,46.9), d P2 6.8 -> turn 26 must open with bait/flee.
- Endgame route (P2 already en route): P1 build left (M1 at (8,26), walks (8,32),(8,38); M3 at (10,44); P1 merge (8,41)->(7-9,40-42)); P1 hop (11,46)->(10-12,45-47); P2 hop (14,50)->(13-15,49-51); YELLOW merge click (12,48)->(10-13,46-49); deliver (7,53)->(5-8,51-54); (5,57)->(3-6,55-58) INSIDE creature = WIN.
- Turn 25 results: ALL 4 OK, model confirmed: bait lunged ring (38,35.5)->(46,27.5); drift exactly 5.66/act toward nearest piece. P2(18-20,51-53), ring (34,39.5) d18. Budget 54.
- Turn 26 (5 acts): E+F->M3 at (10,44)->(9-10,43-44); A+B->M1 at (8,26)->(7-8,25-26); BAIT (31,41) [ring ~(25.2,46.7)->lunge to ~(34.1,37.9)]; P2 flee (13,51)->(12-14,50-52); P2 flee (9,55)->(8-10,54-56) staged at creature edge.
- Projected main-branch end: ring ~(24.9,45); nearest piece becomes M3 (d~15) — ring will chase M3 next turn!
- Turn 27 sketch: M1 walk (8,32); merge M1+M3 at (8,38) [both in range: 6.0 & 5.1] -> P1(7-9,37-39) — relieves M3 before ring arrives; P1 hops (11,44)->(10-12,43-45), (10,50)->(9-11,49-51); YELLOW merge (9,52)->(7-10,50-53); deliver (6,56)->(4-7,54-57) INSIDE = WIN. Insert baits per actual ring pos; yellow may change ring speed — keep ring >=16 at merge time.
- If bait (act3) DROPPED: ring ends ~(15,51.5) d5.6 behind P2 — turn 27 must open bait (e.g. (21,47)) before anything else.
- Turn 26 results: acts 102-104 OK (M3(9-10,43-44), M1(7-8,25-26), bait lunged ring to (34,35.5)). Act 105 (13,51) FAILED-REVERTED: click attracted BOTH P2 (d5.0) AND M3 (d7.6, 2x2) -> mixed sizes converged, blinked, REVERTED; cost -3 budget. Act 106 (9,55) no-op (P2 d9.8 out of range).
- NEW MECHANIC: attraction radius ~8-9.7 nearest-cell (M3 pulled at 7.6; nothing pulled at 9.8). If mixed-size pieces both in click range -> move INVALID, everything reverts (-3). Equal sizes in range -> merge at click. Keep clicks >=10 from any piece you don't want involved; <=6 for intended movers.
- Consequence: P2 cannot stage near M3. Order: absorb M3 into P1 FIRST, then P2 approach (purple+purple in range = merge, which is fine/good).
- State after 106: P2(18-20,51-53), M3(9-10,43-44), M1(7-8,25-26), ring c(30,39.5) chasing P2 d15.2. Budget 46.
- Turn 27 (4 acts): bait (35,34) [ring->(38.4,30.2)]; M1 walk (8,32) [M3 at d11.05 safely out of pull range]; P1 merge (8,38) [pulls M1 d6 + M3 d5.1] ->P1(7-9,37-39); P2 hop (14,47) [P1 at d9.4 may also pull -> merge = yellow (12-15,45-48), fine] ->P2(13-15,46-48) or yellow.
- Turn 28 sketch (from actual state): bait if needed; yellow merge ~(15,48) with ring >=17 (4x4 may drift 12.5!); bait; hop (10,53); deliver (6,56)->(4-7,54-57) INSIDE=WIN. Win-check-vs-ring-move order unknown — keep ring >=17 from yellow at all times.
- Turn 27 results: all 4 OK. Ring lunged to (38,27.5) then drifted; P1(7-9,37-39) formed; P2 hopped to (13-15,46-48) WITHOUT pulling P1 (d9.4 no pull; pull range is 7.6-9.4). Ring c(26,39.5), budget 40.
- Turn 28 (win attempt, 4 acts): BAIT (31,34) [ring->( ~34.5,30)]; click (7,44) [pulls P1 d5 AND likely P2 d6.3 -> YELLOW (5-8,42-45); if P2 unpulled just P1 moves]; click (6,50) [yellow->(4-7,48-51), or P1/merge]; click (5,57)... (5,56) [yellow->(3-6,54-57) FULLY INSIDE creature = WIN].
- Batch ENDS at potential win click — never let leftover actions fire blind on a fresh level.
- Residual risks: bait-drop + 4x4-drift-12.5 branch ~2.5% eat; win-check-vs-ring-order gamble only in worst branch. If win: level 5 next, fresh recon.
- Attempt-3 master plan (adapt to real ring pos each turn): merge M2+M4 at ~(31,43)->P2; flee P2 left/down (27,48),(21,50)-style; A+B->M1 at (8,26); E+F->M3 at (9,46); M1 walk (8,32),(8,38); M1+M3->P1 at (8,42); P1+P2->YELLOW at ~(9,46) [occupies (7-10,44-47)]; deliver (7,53) then (5,57) -> (3-6,55-58) fully inside creature. Insert baits whenever ring closes within ~9 or a needed click falls in death band.

## Level 7 (fresh budget 64, score 6 after act 139)
- L6 WON at act 139: single time-advance click -> ring ate orange inside creature, yellow expelled south pinned by wall INSIDE creature = instant win. Eat-inside-creature trick works when a wall backs the expulsion.
- Indicators: TWO yellow 4x4 (30-33,3-6)+(36-39,3-6). Rows 1-2 tier-icon legend (1x1..7x7 palette) = UI only.
- Creatures: LEFT (19-27,13-21) 9x9, RIGHT (40-48,18-26) 9x9. Yellow fully-inside anchor clicks: LEFT x21-26,y15-20; RIGHT x42-47,y20-25.
- Pieces: magentas M1(6-7,35-36) M2(20-21,35-36) M3(30-31,37-38) M4(9-10,25-26); RED 7x7 (51-57,46-52) c(54,49).
- Rings: ZL c(14,52.5) chasing M2; ZR c(54,57.5) d8.5 from red -> will eat red automatically ~act 1-2, orange expelled NORTH (ring approaches from S), slides to UI wall -> (52-56,10-14) c(54,12).
- Master plan: four magentas -> yellow -> deliver LEFT creature. Red->orange->yellow via ZR eats -> deliver RIGHT. After left delivery (if absorbed), rings converge on parked orange; eat pins yellow at UI wall (expelled N, no displacement); then bait + 2 hops + anchor click (45,21)->(43-46,19-22) = WIN.
- Turn 37 (3 acts): (8,31) M4+M1->P1(7-9,30-32); (25,36) M2+M3->P2(24-26,35-37); BAIT (20,50) for ZL (est ZL2 ~(18-20.5,42-44.5), click d<=8.3, lunge S landing ~(19-21,55-58), buys ~3 acts).
- Turn 38 sketch: verify rings; P1 walk (13,33)->(12-14,32-34); merge (18,34) pulls P1 d4 + P2 d6.1 -> YELLOW (16-19,32-35); deliver hops (17,28),(19,22), anchor (23,18)->(21-24,16-19) inside LEFT; interleave baits vs ZL/ZR as needed. Watch whether delivered yellow is ABSORBED (unknown!).
- Turn 37 results (acts 140-142): ALL 3 OK (act142 bait did NOT drop — ZL lunged (22,44.9)->(18,56.9), exactly per model). P1(7-9,30-32), P2(24-26,35-37) formed. ZR ate red DURING act140 (eat radius ~<=3 to nearest CELL); EXPULSION DISTANCE ~11 cells (red c(54,49)->orange c(53,38), L6 consistent). Orange (51-55,36-40). ZR c(53,45.9) d~6 from orange -> eats it act143, yellow-R expelled NORTH to ~(51-54,25-28). ZL c(18,56.9) chasing P2 d22. Budget 58.
- Turn 38 (3 acts): (13,33) P1 walk ->(12-14,32-34) [ZR eats orange same act]; BAIT ZR (58,45) [lunge SE to wall ~(61,49)]; BAIT ZL (17,51) [est ZL ~(21.6,46.1)-(25,48.9), click d 6.7-8.3, lunge SW landing ~(12-13,52-56)]. End batch to verify yellow-R landing.
- Turn 39 sketch: merge (18,34) pulls P1 d4+P2 d6.1 -> YELLOW-L(16-19,32-35); right anchor (46,24) pulls yellow-R d~5.1 -> (44-47,22-25) FULLY INSIDE right creature (observe absorption!); then YELLOW-L hops (17,28),(19,22), anchor (23,18)->(21-24,16-19) inside LEFT = WIN. Interleave baits; final click must survive ring phase (win check is AFTER ring moves — L6 act139 order).
- Drop branches T38: act1 drop -> orange survives, act2 pulls orange to (56-60,43-47) + ZR lunges adjacent -> eat next act, yellow-R pinned E wall (recoverable, longer route). act3 drop -> ZL closes on P2, next-turn open with ZL bait (~(27,45)) before merge.
- Turn 38 results (acts 143-145): ALL OK. YELLOW-R (51-54,26-29) c(52.5,27.5) (expelled ~10.5 N). P1(12-14,32-34), P2(24-26,35-37). ZL c(13,52.9) (lunge landed per model), ZR c(57,45.9) heading back to Y-R d19. Budget 52.
- DRIFT MODEL CONFIRMED = CHEBYSHEV-4: each axis moves up to 4 toward target per action (diag=5.66 euclid). Lunge 12.6 verified again.
- Turn 39 (2 acts, end early to observe absorption): (18,34) merge P1 d4 + P2 d6.1 -> YELLOW-L (16-19,32-35); (46,24) pulls Y-R d5.4 -> (44-47,22-25) FULLY INSIDE right creature. Projected end: ZL (17.5,44.9) d11 from YELLOW-L; ZR (49,37.9) d14 from delivered Y-R. KEY OBSERVATION: is delivered Y-R absorbed/locked or still eatable?
- Turn 40 sketch (if Y-R persists): hops (17,28),(19,22); bait ZR when it nears Y-R (e.g. ZR ~(45.5,29.9) -> bait (45,36), lunge S landing ~(44.5,42)); win anchor (23,18) -> (21-24,16-19) inside LEFT = WIN (win check is AFTER ring phase — ensure no ring lands within ~3.3 of either yellow on final action). If Y-R absorbed: rings both chase YELLOW-L; bait ZL as needed, same delivery hops.
- Drop branches T39: act1 drop -> act2 independent, redo merge next turn. act2 drop -> ZR at (52.5,37.9) d9 from Y-R; next turn REDO anchor immediately (click d15.3 from ZR, safe) or bait first.
- Turn 39 results (acts 146-147): BOTH OK. YELLOW-L (16-19,32-35); YELLOW-R DELIVERED (44-47,22-25) fully inside right creature but NOT ABSORBED (still eatable, creature shows 53 cells). No score yet (need both, like L3). ZL c(18,44.5) d11 from Y-L (eats on 3rd move); ZR c(49,37.5) d12.7 from Y-R (eats on 3rd move). Budget 48.
- KEY: dropped click = NO ring movement either -> a dropped bait is never itself fatal; danger only when a drop makes a LATER action's ring phase land on prey. Rule: end batch right after critical baits, verify, then continue.
- Turn 40 (3 acts, drop-robust in all single-drop branches): BAIT ZL (14,50) [d6.8, lunge SW landing ~(10.6,54.7)]; hop Y-L (17,28)->(15-18,26-29); BAIT ZR (45,36) [ZR ~(45.5,29.5) d6.5, lunge S landing ~(44.5,42.1); still lunges (d2.55) in act1/act2-drop branches]. End batch, verify.
- Turn 41 sketch: hop Y-L (19,22)->(17-20,20-23); WIN anchor (23,18)->(21-24,16-19) fully inside LEFT creature; win check after ring phase — verify no ring within reach of either yellow on that action.
- Turn 40 results (acts 148-150): ALL OK. ZL baited to (10,56.5), now back at c(17,48.5) d21 from Y-L. Y-L hopped (15-18,26-29). ZR baited to c(42,41.5) d18 from Y-R. Budget 42.
- Turn 41 (2 acts, WIN attempt): hop Y-L (19,22)->(17-20,20-23); anchor (23,18)->(21-24,16-19) FULLY INSIDE left creature -> both yellows delivered = WIN. Ring phases safe (ZL lands ~(22.5,40.5), ZR ~(45.5,33.5), both >8 from prey). Drop branches: act1 drop -> act2 no-op (d9.4 no pull), redo; act2 drop -> redo; both safe.

## Level 8 (fresh budget 64, score 7 after act 152)
- L7 CLEARED act 152 (13 actions): win registered on final anchor click with both yellows fully inside their creatures. Delivered pieces persist (NOT absorbed) until all indicators satisfied — must guard them from rings.
- Indicators: TWO ORANGE 5x5 (30-34,2-6)+(37-41,2-6). Green 'I' 8-cell glyph at (44-48,3-6) + new legend icons row 6-7 (z ring, I green, > maroon) — unexplained, watch.
- Creatures 9x9 at four corners: TL(3-11,15-23), TR(52-60,15-23), BL(3-11,51-59), BR(52-60,51-59). Orange fully-inside center-clicks: TL x5-9,y17-21; BL x5-9,y53-57; etc.
- Pieces: Y1(3-6,40-43), Y2(13-16,42-45), RED(20-26,24-30) c(23,27). Rings: A c(45,32.5) chasing red (eats it ~act4-5, expelled WEST to ~(10-14,25-29)); B c(49,49.5) chasing red; C c(31,54.5) chasing Y2/orange-1.
- Plan: Y1+Y2 merge = orange-1; red eat = orange-2 (near TL creature). Deliver BL + TL.
- Turn 42 (5 acts): merge (10,43)->ORANGE-1(8-12,41-45); hop (9,49)->(7-11,47-51); deliver (7,55)->(5-9,53-57) INSIDE BL; BAIT C (25,57) [C ~(19,53), d7.2, lunge ESE landing ~(29.5,60)]; click (8,21) -> if red eaten act4 (ring A lands d3.0 borderline), pulls orange-2 (all landing variants d3.2-5.7) to (6-10,19-23) INSIDE TL = WIN. If eat happens act5 instead, click is harmless no-op -> next turn: bait A if needed, redo (8,21) = win.
- Drop notes: act1 drop self-heals (act2 pulls BOTH yellows d6.7/5.7 -> merge at (9,49) anyway). act4 drop -> next turn MUST open with C bait (C ~(15,55) d6 from orange-1). act5 drop -> redo next turn safely.
- Turn 42 results (acts 153-157): all 5 executed. Orange-1 DELIVERED (5-9,53-57) in BL. Bait C worked. Red eaten at act157 RING PHASE (after my click) -> orange-2 (10-14,24-28) undelivered. EAT THRESHOLD REFINED: landing d3.0 to nearest cell did NOT eat (act156); eat at <3. Rings: A c(28,26.5) chasing o2 (4 moves), B c(29,35.5) chasing o2, C c(27,56.5) chasing delivered o1 (~4-5 moves). Budget 58.
- Turn 43 (1 act): click (8,21) pulls o2 d3.6 -> (6-10,19-23) fully inside TL creature = WIN. All rings >=20 from click; ring phase harmless.
- Turn 43 result (act 158): click pulled o2 to (6-10,19-23) but cell (10,23) sticks OUT of creature's rounded corner (9x9 blob shape rows: 5,7,9,9,9,9,9,7,5 wide) -> 24/25 inside, NO WIN. Creature full-width rows only: TL rows 17-21 cols 3-11. Rings: A c(24,22.5) chasing o2 (3 moves out!), B c(25,31.5), C c(23,54.5) chasing o1 (3 moves out). Budget 56.
- LESSON: 5x5 delivery into 69-cell blob MUST center on the blob center row/col band (click within x5-9,y17-21 for TL means center rows — corners are rounded!). Center-click (7,19) is the true safe anchor; edges of the 5x5 anchor range fail.
- Turn 44 (1 act): click (8,19) re-centers o2 -> (6-10,17-21) fully inside TL = WIN. Rings 12-16+ away, ring phase harmless (A lands d~10.6 from o2, C d~10 from o1).
- Turn 44 result (act 159): o2 re-centered (6-10,17-21) FULLY INSIDE TL, o1 fully inside BL — NO WIN, score still 7! Both oranges inside creatures insufficient.
- UI decode attempt: indicators read [orange][orange][8-cell GREEN STAR glyph at (44-48,3-6)]. New legend row 6-7: z(ring), I(green), >(maroon) icons. THEORY: merge orange+orange -> GREEN 6x6 'star' piece, deliver THAT (formula UI: - + - = I). Legend row6-7 = catalog of special entities. Alt theories: specific-creature pairing (expensive to test, 8+ hops/orange); green=6x6 tier missing from rows1-2 ladder.
- Plan: walk o1 north from BL (hops (7,49),(7,43),(7,37),(7,31),(7,25)) to stage (5-9,23-27) below TL, then merge-click (7,19) pulls o1 d4 + o2 d0 -> GREEN (4-9,16-21) fully inside TL = WIN (if theory right; if it makes red 7x7 instead -> cannot fit any blob -> RESET). If green forms but no win, walk green to other creatures (recoverable).
- Rings now: a c(20,18.5) chasing o2 d~10 (2-3 moves!), b c(21,27.5) same, c c(19,54.5) chasing o1 d~10. DELIVERED PIECES ARE EATABLE — keep cycling baits every ~3 acts.
- DOUBLE-BAIT trick: one click within 8.5 of TWO rings lunges BOTH (a+b are ~9 apart, midpoint clicks reach both).
- Turn 45 (2 acts, drop-safe): (26,23) double-bait a (d7.5) + b (d6.7) -> both lunge E to ~(30,26)/(30,19); (21,57) bait c (post-drift ~(15,55), d6.3) -> lunge E to ~(27,59). End batch (any drop leaves eats >=2 moves away; re-bait next turn).

## Turn 46 (after acts 160-161) — MAJOR: RINGS MERGE INTO GREEN STAR
- Act 160 double-bait (26,23): BOTH rings a+b lunged to coincident landing -> MERGED into GREEN STAR `I`, 8 cells, X-star shape, bbox 5x4, appeared (23-27,21-24).
- Confirms legend ladder: z+z -> I (ring+ring = green star). Same merge rule as pieces: equal entities coincident -> next tier.
- Act 161 bait ring c to (21,57): c lunged to (25-29,57-60) c(27,58.5), d~18 from o1.
- Star drifted (-4,-4) to (19-23,17-20) c(21,18.5) during act 161 ring phase — Chebyshev-4 toward o2 (nearest piece), d~11 from o2 nearest cell. Contact in ~3 moves.
- State: o1 delivered BL (5-9,53-57), o2 delivered TL (6-10,17-21), both creatures show deliveries, NO WIN yet. Indicator: [orange][orange][green star glyph].
- THEORY: star must reach/enter a creature or touch o2 to complete formula. RISK: star may EAT o2 (degrade to yellow, expel) like rings do.
- Turn 46 plan: single far no-op click (45,40) to advance time 1 step, observe star behavior at d~7 before contact move. Preserves options.

## Turn 47 (after act 162)
- Act 162 no-op (45,40): star drifted -4x to (15-19,17-20) c(17,18.5) — d=5 from o2 nearest cell (x=10). NEXT drift lands d=1 -> eat risk on o2 (if star eats like rings). Ring c drifted -4x to (21-25,53-56) c(23,54.5), d=12 from o1 — 2 safe phases, EAT lands on 3rd phase.
- Budget char is '$' in row 63 (51 left), not apostrophe. Fix parser.
- FUSE ANALYSIS: star 1-phase fuse to o2; ring c 3-phase fuse to o1. Every click advances both. First click MUST bait star.
- WIN THEORY: 3rd indicator = deliver the STAR to a free creature (TR x52-60,y15-23 or BR). Star only drifts toward pieces (all west), so must be moved by lunges. Pure-east lunges from c17: 29.6, 42.2, 54.8 — 3rd landing bbox (53-57,17-20) FULLY inside TR. But ring c eats o1 on that same 3rd phase — order unknown, must delay c with a bait mid-sequence (costs star a -4 backdrift; then geometry needs 4 lunges, sum 43 > 3x12.6 — needs angled lunges or wall clip, neither clean).
- Turn 47: TEST star bait response. Click (24,18): d=7.0 from star. Outcomes: (a) lunges east ~12.6 -> ring-like, proceed with delivery plan; (b) pulled to click like a piece -> piece-like, new options (could pull star into creature directly with clicks!); (c) ignores & drifts -4 -> d=1 from o2 -> learn if it eats; if o2 dies, RESET and rebuild (we know how to recreate star via double-bait).
- If (b) pull-like: HUGE — a click inside TR creature pulls star in if within 7.6. Delivery becomes trivial 2-3 clicks.

## Turn 48 (after act 163) — STAR IS PULL-ABLE (piece-like!)
- Act 163 click (24,18) d=7.0: star PULLED to click (c 17->24, landed AT click, not lunge). Star = piece-like for pulls, but drifts Chebyshev-4 toward nearest piece when un-pulled. Does NOT get eaten/merge with rings apparently.
- Ring c drifted to bbox x17-21 c(19,54.5): d=8 from o1 -> 2 phases to eat (eat lands phase 2).
- PLAN: deliver star to TR creature (x52-60,y15-23) via pull chain. Turn 48 batch (2 clicks, drop-safe ordering):
  1. (31,18) pull star east (nearest-cell d=5). Ring c drifts to x13-17 (safe, d=4 landing).
  2. (23,55) bait ring c east: d=8.0 lunge -> c ~(27.6,54.5), resets fuse to ~4-5 phases. Star backdrifts -4 this phase -> c~(27,18.5). END BATCH (bait last = drop-safe).
- Turn 49: pull chain (39/47/55-ish, hops <=+9, nearest-cell d<=7) -> final star c~(55-56,18) bbox x53-57 fully inside TR -> win check. Ring c timeline safe for 3+ phases after bait.
- Drop analysis: click1 drop -> click2 bait still valid (d=4 from unmoved c, still lunges). click2 drop -> re-bait next turn (c at 1 safe phase). Never put actions after an unverified bait.

## Turn 49 (after acts 164-165)
- Both clicks worked: star pulled to c(31), then bait lunged ring c east to bbox x25-29 (d=16 from o1, 4 safe phases: 12/8/4/0-eat). Star backdrifted to bbox x25-29,y17-20 c(27,18.5). Budget 47.
- Star exact shape (5x4 X): rel cells (2,0),(1,1),(3,1),(0,2),(2,2),(4,2),(1,3),(3,3). Pull anchor: click (x,18) -> bbox (x-2..x+2, 16..19).
- TR creature rows: y15:54-58, y16:53-59, y17-21:52-60, y22:53-59, y23:54-58.
- Turn 49 batch: 3 pulls (36,18),(45,18),(54,18) — hop nearest-cell d=7.07/7.0/7.0 (<7.6 ✓). Final bbox x52-56,y16-19: all 8 cells verified inside TR. Ring c lands d=4 on pull3 phase (no eat, safe). WIN CHECK on pull3.
- If drop mid-chain: star backdrifts -4 (safe, o2 eat needs 2+ un-pulled phases), c advances less. Recover next turn.
- If NO WIN after full delivery: re-theorize (star->specific creature? star+orange overlap?). Ring c at d=4 -> bait FIRST next turn: c bbox x13-17 c(15,54.5), bait (23,55).

## LEVEL 8 CLEARED — act 168, Score 8. Star delivered to TR creature via 3-pull chain. Win = all 3 indicators simultaneously: orange-in-creature x2 + star-in-creature. L8 total: 17 actions.

## LEVEL 9 (act 168+, budget 64, all $ row 63)
- Indicators: [orange 5x5 (30-34,2-6)] [purple 3x3 (37-39,4-6)] [maroon glyph (42-47,3-6)]
- Rings (8-cell diamond, bbox 5x4): r1 c(16,13.5), r2 c(54,14.5), r3 c(17,23.5), r4 c(56,34.5)
- Pieces: C1 magenta 2x2 (18-19,46-47), C2 magenta 2x2 (23-24,52-53), red 7x7 (35-41,48-54)
- Creatures 9x9 rounded (rows 5,7,9,9,9,9,9,7,5): TL (7-15,37-45), BL (7-15,51-59), BR (50-58,51-59)
- STRATEGY: purple = C1+C2 merge, deliver (BL nearest). orange = ring eats red once (degrade n->-), deliver. maroon = merge r1+r3 -> S1, merge r2+r4 -> S2, merge S1+S2 -> maroon, deliver. Manage: rings must NOT eat magentas/purple; only ONE eat on red.
- Ring drift targets: r1,r3 -> C1 (r3 d~21, ~5 phases). r2,r4 -> red (r4 d~17.7 ~3-4 phases, r2 d~34).
- L8 ring-merge mechanic recap: one click within lunge range (<=~8.5) of both rings -> both lunge, merge AT click.
- Turn 50 batch: (16,18) merge r1+r3 -> S1 at click (d 4.5/5.6). (21,50) merge C1+C2 -> purple 3x3 at click (d 3.6/2.8; red d 14.1 no pull -> no mixed-size invalidation). Phases advance r2/r4 toward red by 8 total — fine, first red eat is desired (makes orange).
- NEXT: pull purple into BL (via ~(14,53) then (11,55)); watch S1 (drifts toward nearest piece), r2/r4 approach red; after red eaten once -> bait rings off orange, merge r2+r4, then S1+S2.

## Turn 51 (after acts 169-170)
- Act 169 (16,18): r1+r3 MERGED -> star S1 bbox (13-17,17-20). r2 drifted to c(49,18.5), r4 to c(52,38.5) (both -4,+4 toward red).
- Act 170 (21,50): magentas MERGED -> purple 3x3 (20-22,49-51) at click. S1 drifted +4+4 to (17-21,21-24) c(19,22.5) (targets purple, d~25). r2 c(45,22.5), r4 c(48,42.5).
- r4 fuse: next phase drifts (-4,+4) -> lands d=1 from red -> EATS red -> ORANGE 5x5 spawns, expelled away from ring: predicted orange center ~(29.6,57.3), bbox ~(27-32,55-60). r4 rests c(44,46.5), then hunts orange: phase2 d~6.7, phase3 EAT ORANGE -> must bait r4 on click3.
- Turn 51 batch: (14,53) pull purple (d=6.3) -> bbox (13-15,52-54) [same phase: r4 eats red]. (11,55) pull purple (d=2.2) -> bbox (10-12,54-56) FULLY inside BL creature = DELIVERY 1. (40,43) bait r4 north (d~7.5 from predicted c(40,50.5)) -> lunge to ~(40,37.9), toward r2 for future S2 merge. Bait LAST = drop-safe.
- Next: merge r2+r4 -> S2 (click within 8.5 of both), then S1+S2 -> maroon, deliver maroon (TL or BR), pull orange into remaining creature. Watch S1 (hunts purple, ~7 phases); delivered pieces stay eatable.

## Turn 52 (after acts 171-173)
- Act 171: purple pulled to (13-15,52-54). r4 landed d=1 by red (eat delayed one phase, same as L8 timing).
- Act 172: purple -> (10-12,54-56) DELIVERED (BL). r4 ATE red -> ORANGE 5x5 expelled to (26-30,53-57). 
- Act 173 bait (40,43): r4 lunged NW and COLLIDED with r2 -> MERGED into star S2 (32-36,33-36)! Rings all gone. S1 at (9-13,33-36) (hunting delivered purple, ~5 phases).
- Lesson: ring lunge landing on/near another ring = merge (contact merge), even when 2nd ring wasn't baited.
- State: S1 c(11,34.5), S2 c(34,34.5), orange (26-30,53-57), purple delivered (10-12,54-56). Budget 58.
- Turn 52 batch: (26,34) pull S2 west (d=6.08) -> c(26,34) bbox (24-28,32-35); S1 drifts to (9-13,37-40). Then (18,36) MERGE CLICK: both stars' nearest cells within 7.6 (5.83/6.32) -> expect MAROON at click (star+star pull-merge, untested but piece-like). END batch to observe.
- Then: 3 pulls orange east -> (52,55) bbox (50-54,53-57) fully in BR. Then pull maroon (~(18,36)) NW into TL creature LAST -> win check fires while all 3 delivered (maroon drifts, so it must be delivered on final action).
- Drop-safety: click1 drop -> click2 only pulls S1 east (harmless). click2 drop -> re-merge next turn.

## Turn 53 (after acts 174-175) — MAROON EXISTS
- Act 174: S2 pulled to (24-28,32-35) ✓; S1 drifted to (9-13,37-40) ✓.
- Act 175 (18,36): STARS PULL-MERGED -> MAROON '>' 13 cells bbox (16-20,34-37) at click. Star+star merge via double-pull confirmed. Full ladder: z+z->I, I+I->>.
- Maroon shape rel: (0,0),(2,0),(4,0),(1,1),(3,1),(0,2),(1,2),(2,2),(3,2),(4,2),(1,3),(2,3),(3,3). Anchor: click -> bbox (x-2..x+2,y-2..y+1).
- Maroon drift forecast (targets purple): c(18,35.5)->(14,39.5)->(11,43.5)->(11,47.5) after 3 phases; lands d=5 from purple (safe; eat needs <3 + 1-phase delay).
- Turn 53 batch (4 clicks, endgame): orange pulls (36,55),(44,55),(52,55) [hops d=6] -> bbox (50-54,53-57) fully in BR (rows 53-57 span 50-58). Then (11,41) pulls maroon (nearest cell (11,46), d=5) -> bbox (9-13,39-42) fully in TL -> ALL THREE DELIVERED -> WIN CHECK.
- Drop risks: any orange-pull drop -> later pulls miss (14+ away), orange stalls, maroon still pulled at click4 (d ok from earlier positions) -> delivered but no win, maroon drifts out next phase -> redo. Click4 drop -> maroon 2 phases from eating purple -> pull it FIRST next turn.
