# Game notes
- 64x64 board, maze of 3x3 tiles. Nodes at rows/cols 15+6k (15..45), corridors '#' between.
- Player: blue 'f' 3x3 (with q center) start node (15,15). Goal: green 'I' at (45,45). Border magenta 'C' row 63 = maybe timer bar.
- solve.py: parses last board, BFS start->goal. Full 18-move path:
  R D D R U R D D L L D R R D R U R D
  (ACTION4,2,2,4,1,4,2,2,3,3,2,4,4,2,4,1,4,2)
- Turn 1: sent first 2 moves (R, D) to verify 1-action = 1-node-step hypothesis.
- Turn 2: confirmed 1 action = 1 node step (6 px). Player at node (21,21) after R,D. Magenta row 63 is step budget: 64->63->61 (ticks down ~per action). Sent remaining 16 moves to goal (45,45).
- Turn 3: Level 1 cleared at action 18 (score 1). Level 2: smaller maze, nodes rows 21/27/33, cols 12..48 step 6. Player (33,12) marker 'q' top-middle; goal (21,48); RED block 'n' with purple '"' marker at (27,36) blocks the ONLY path (all routes east pass through it). Hypotheses: enemy that moves per action, or pushable block. Markers (q/") may indicate facing. Sent single ACTION1 (up, forced move) to observe red behavior.
- solve.py now auto-detects lattice from player pos; treats only $/f/I as walkable — red 'n' excluded (caused NO PATH).
- Turn 4: ACTION1 done, player (27,12). Red still (27,36), '"' marker middle-left (facing left/toward player). Confirmed markers = facing/last-move dir (checked lvl1: q pos matches move dir). Red didn't mimic Up (up from red is wall, so mimic not ruled out!). L2 map: row27 fully connected cols12-48; row33 nodes 12,24,30,36 (corridors 24-30-36 only, 12 isolated except up); verticals row27<->33 at cols 12,24,30,36; goal (21,48) reached only via (27,48) up-corridor col48.
- Mimic contingency plans (if red copies inputs): avoid pushing red to (27,48) then inputting U (red would enter goal). Possible desync: D (red->33,36), L,L (red->33,24 then stuck for L).
- Turn 4 action: single ACTION4 (right). If red moves right -> mimic confirmed. If static -> try push/pass.
- Turn 5: red static after our R (mimic ruled out: (27,42) was open; chase ruled out: LOS along row27, no move). Player (27,18). Sending R,R,R -> (27,30) then push attempt into red at (27,36). Watch: does red shift to (27,42) (push, step), slide to (27,48) (ice-slide), block us (wall), or kill (reset)?
- Concern: if pushes go right, red ends at (27,48) blocking sole goal entry. May need alternate mechanic (push distance, or red vanishes at wall?). Observe first.
- Turn 6: DEATH at action 22. Frames: player moved (27,24)->(27,30) fully, THEN red charged (27,36)->(27,30) one node onto player -> player destroyed, level reset (Attempt 2). Trigger = ending adjacent to red (at least in its facing dir, left). Distance>=2 safe. Actions 23-24 wasted (walled R at respawn (33,12)).
- Must lure red off (27,36): all goal routes pass through it. Charge only onto player node.
- Turn 6 plan: U,R,R,D,R,R -> (33,30) then probe (33,36) below red. Outcomes: death => red guards ALL adjacent (need new idea); survive => facing-only guard; then test if red turns to face player / whether U from below pushes/kills red.
- Turn 7: player safe at (33,36) directly below red; red still faces left, no turn, no charge => guards ONLY its facing-front node (27,30). 
- Turn 7 probe: ACTION1 (up into red from below). Outcomes: blocked (wall-like), push (fails, wall above red), death (reset), or destroys red.
- Turn 8: KEY MECHANIC: moving into red enemy from a non-facing side DESTROYS it (player took its node, red gone). Red only kills via its facing-front node. Lvl2 solution: approach from below via row 33, kill red, then R,R,U to goal.
- Turn 8: sent R,R,U -> (21,48) goal, expect score 2.
- Turn 9: Lvl2 cleared (score 2, action 34). Lvl3: player (42,42), goal (42,24). Reds: R1(24,24) faces R (guards 24,30); R2(24,30) faces D (guards 30,30); R3(36,12) faces R (guards 36,18). Kill rule: move into enemy from non-facing side = kill; entering a guarded node = charge+death; adjacency on non-facing sides safe.
- 19-move plan: U,U,R,U,L,L,U,L,L, D(kill R1 from top), R(kill R2 from left), D,L,L,L, D(kill R3 from top), R,D,R -> goal.
- Turn 10: Lvl3 cleared in 19/19 moves (score 3, total 53 actions). Lvl4: player (40,21) facing R; goal (22,21); RED1 (16,27) faces D (guards 22,27); ORANGE (22,39) faces D, sits on sole chokepoint route (both paths converge at (28,39)->(22,39)). If orange = red-like guard, unsolvable => orange differs. Hypothesis: orange MIMICS player inputs (marker style like player's).
- Map L4: row40: 21-27-33-39-45; col39: 40-34-28-22-16; col45: 40-34-28; row28: 39-45; row22: goal21-27-33-39; col27: 22-16(RED1); col33: 22-16; row16: 27-33-39.
- Turn 10 probe: ACTION3 (L). We are wall-blocked (no node left of (40,21)). If orange mimics, it moves L to (22,33). Zero risk.
- Turn 11: mimic ruled out for orange (no move on our L input; nothing moved). Orange static, faces down col 39. New hypothesis: LOS-triggered (charges/steps when player anywhere in its facing column). Probe: R,R,R -> (40,39), bottom of col 39, distance 3. Watch: orange steps 1 (pursuer, can bait it off chokepoint), charges full column (death, reset - acceptable cost), or static (then inch up: (34,39) next, then test front-kill at (28,39)).
- Turn 12: ORANGE MECHANIC: moves 1 node in its patrol direction per SUCCESSFUL player move (blocked inputs freeze it). Death run: o went 22->28->34->40 and landed on us at (40,39) t3 => collision kill, level reset (attempt 2, we back at (40,21), o back at (22,39) facing down).
- Unknown: patrol top bounce - range 22..40 (period 6) or 16..40 (period 8). Bottom bounce at 40 assumed (unobserved too!). 
- Turn 12: 7 shuffle moves R,L,R,L,R,L,R (we oscillate 21<->27, never near col 39). Expected o: 28,34,40,?,?,?,? -> move 4 reveals bottom bounce (34 = bounce; else?), move 7 reveals top (16 vs 28).
- Draft 17-move solution (if range 16..40): RLRL shuffle x4 then R,R,R,R,U,U,L,U,L,U,L(kill RED1 from its right),D,R... see turn 12 analysis. Recompute once cycle known. Kill RED1 (16,27) from (16,33); goal entry (22,27)->(22,21).
- Turn 13: cycle confirmed: orange range 16..40 col39, period 8. o_t (t=moves from now, o now at 16): t%8: 1:22,2:28,3:34,4:40,5:34,6:28,7:22,0:16. Direct col-39 climb provably impossible (all phases excluded); col-45 route needs (28,39)-entry at t=12 (even parity, t%8=4). 
- 18-move solution from (40,27): RL x3 shuffle (t1-6), R,R,R (t7-9: 33,39,45; t8 at (40,39) with o=16 safe), U,U (34,45),(28,45), L (28,39) t12 o=40, U (22,39) t13 o=34, L (22,33), U (16,33), L kill RED1 t16, D (22,27), L GOAL t18.
- Turn 14: CRITICAL: magenta bar = 20-move budget per attempt (64px, ~3.2px/move). Auto-RESET when 0. Blocked inputs consume budget but do NOT advance orange. My 7+18=25-move plan hit cap at move 20 (action 78) -> auto reset; steps 14-18 wasted as blocked inputs (budget now 48).
- Fix: from fresh reset (o at 22 down, o_t: 28,34,40,34,28,22,16 then period 8; o=16 at t=7,15), k=4 shuffles works: RESET + R,L,R,L + R,R,R,R + U,U + L(28,39 t11, o=40),U(22,39 t12, o=34) + L,U + L(kill RED1 t15) + D,L(goal t17). 17 moves <= 20 budget. Total 18 entries.
- LESSON: always count budget: max 20 moves/attempt. Plan level solutions <= 20 moves including shuffles.
- Turn 15: Lvl4 cleared t17 exactly (score 4, action 102). Lvl5: lattice rows 14,20,26,32,38,44; cols 9,15,21,27,33,39,45,51. Player (14,51), goal (32,27).
  Edges: row14 full 9..51; col9 14-32; col27 14-20-26-32-38-44 (goal at 32); col21 26-32-38; col15 32-38-44; col33 32-38-44; col51 32-38-44; row32 full 9..51; row44 15-21-27-33.
  Enemies (orange patrollers, 1 step per player move): O1 (26,27) facing D; O2 (32,9) facing R; O3 (32,21) facing D (range col21 26-38, period 4); O4 (38,27) facing U. O1/O4 share col 27 (will collide t1 at (32,27)=goal?); O2 crosses O3's node.
  Shortest route: L,L,L,L,D,D,D = 7 moves via col 27 - but that's O1/O4's turf. Budget 20 moves.
- Turn 15: probe L,L -> (14,39). Watch 2 ticks: enemy-enemy collision rules, bounce ranges, whether enemies traverse the goal node.
- Turn 16: Lvl5 budget = 40 moves (drain 1.6px/move, unlike lvl4's 3.2). Enemy sim verified vs log: A/B col27 bouncing walkers (period 10), O2 row32 (period 14), O3 col21 (period 4). Cross-axis enemies overlap freely; same-axis meet/pass with identical position sets.
- Parity analysis: col-27 descent & westward row-32 entry provably impossible (checkerboard parity lock with walkers). Only route: south loop via col9 -> (32,15) -> col15 down -> row44 east -> col33 up -> goal from east. BFS on time-expanded graph (strict: pre-free, post-free, no-swap) = 27 moves, verified.
- Turn 16: sent moves 1-20 of 27. NEXT TURN: send remaining 7: ACTION2,ACTION4,ACTION4,ACTION4,ACTION1,ACTION1,ACTION3. After the 20th move player should be at (44,15) [check log], t=22. solve5.py has sim.
- Turn 17: moves 1-20 executed exactly; player (38,15), enemy sim matches log at t=22 (A=38, B=26, O2=45, O3=32 in their corridors). Sent final 7: D,R,R,R,U,U,L -> goal (32,27) at t=29. Expect score 5.
- Turn 18: Lvl5 cleared t29 (score 5, action 131). Lvl6: player (18,48), goal (18,12). Lattice rows/cols 12..48 step 6.
  Map: row18 full 12..48; col30 top: (12,30)-(18,30)-(24,30)=O1 patrol (period 4, (18,30) at odd t); col18: 18-24-30-36; col36: 18-24-30(+42-48 NO: only via row42); col42: 30-36-42; col24: 30-36? NO: col24 links 30x?? verticals: r21-23: 18,30,36; r27-29: 18,36; r33-35: 18,24,36,42; r39-41: 24,42; r45-47: 24,30,36. row30: 24-30-36-42; row36: 18-24-30-36-42; row42 full 12-48; row48: 24-30-36.
  Reds: R1(30,24)vD, R2(30,42)vD, R3(42,24)^U, R4(42,30)<L, R5(48,24)^U, R6(48,30)^U. Guard web: (36,24):R1+R3; (36,42):R2; (42,24):R4+R5; (42,30):R6.
  O2(42,48) facing L patrols row42. If O2 bounces off reds level is unsolvable => assume pass-through (period 12: t%12: 1:42,2:36,3:30,4:24,5:18,6:12,7:18,8:24,9:30,10:36,11:42,0:48).
  30-move plan (t1..t30): L,L,D,D,L,Lkill R1,R,R,Rkill R2, D,U,D,U(shuffles),D,D(42,42 t15),L,D(48,36),Lkill R6,Lkill R5,R,L,R(waits),Ukill R4 t23,Lkill R3 t24,U,L,U,U,U,L GOAL t30.
- Turn 18: sent t1-t9 (through R2 kill). VERIFY: budget drain rate (need <=2.1px/move for 30 moves), O2 pass-through vs bounce at reds (watch it cross (42,30)/(42,24) at t3/t4), O1 period.
- Turn 19: t1-9 perfect: R1,R2 dead, player (30,42) t9. Budget drain ~1.1/move => ~60 budget ✓. O2 PASS-THROUGH confirmed (seen overlapping R4/R3 nodes at t3/t9, full sweep period 12 matches model).
- Sent t10-t29 (20 moves): D,U,D,U shuffles, D,D to (42,42) t15 (O2 at 30), L,D to (48,36), kill R6 t18, R5 t19, waits R,L,R t20-22, U kill R4 t23 (O2 at 42), L kill R3 t24 (O2 at 48), U (36,24) t25, L,U,U,U -> (18,18) t29. NEXT TURN: single ACTION3 -> goal (18,12).
- Turn 20: Lvl6 cleared t30 (score 6, action 161, attempt 1, zero deaths!). Lvl7: player (30,12), goal (30,48). NEW: MAROON '>' (18,24) facing D, atop col24 (18-24-30). RED (24,42) facing L (guards (24,36)).
  Map edges: row30: 12-18-24-30; col30: 30-36-42; row42: 30-36; col36: 42-36-30-24-18; row24: 36-42; col42: 18-24-30-36; row18: 36-42-48; col48: 18-24-30(goal); col12/18: 30-36; row36: 12-18, 36-42.
  Draft 14-move: R,R,R,D,D,R,U,R,U,U(kill RED from below),U,R,D,D -> goal. Risk: maroon may patrol col24 hitting (30,24)=route t2.
- Turn 20: probe single R -> (30,18). Measure maroon speed (1x/2x?) and direction.
- Turn 21: maroon static after our first move (marker unchanged (20,25)). Hypotheses: (a) red-like front-guard (guards (24,24) only - route safe), (b) LOS-charger down col24 (deadly at (30,24)), (c) LOS-stepper (1/tick, escapable).
- Turn 21 probe: R -> (30,24), the crossing node in maroon's facing line. Outcomes: nothing (a ✓ proceed), maroon steps (c: flee east next), death (b: reset, need lure trick).

## Turn 22 (post-compaction, after Action 162)
- L7 attempt 1, player (30,18). Maroon (18,24) facing DOWN, static through 1 move. Red (24,42) facing LEFT.
- Probe upgraded: R,R -> pass (30,24) [maroon's facing line, 2 nodes below] to (30,30).
- Outcomes: survive+maroon static = front-guard-like, proceed with draft route remainder:
  D,D,R,U,R,U,U(kill red from below),U,R,D,D -> goal (30,48). 10 moves left after this probe.
- If maroon steps/chases (stepper): it trails 1 behind while I keep moving; route may still work, verify each turn.
- If death on move 1: LOS-charger; respawn (30,12), need lure trick.

## Turn 23 (after Action 164)
- MAROON MECHANIC: static until player enters facing line; sees player (no move that turn), then begins stepping 1 node/turn (moved (18,24)->(24,24) on action 164). Chaser or last-seen-walker, speed 1, currently 2 behind.
- Player (30,30). Budget 58px, ~2px/move, ample.
- Committed 11 moves: D,D,R,U,R,U,U(kill red (24,42) from below),U,R,D,D -> (30,48) GOAL.
- Nodes: (36,30),(42,30),(42,36),(36,36),(36,42),(30,42),(24,42)kill,(18,42),(18,48),(24,48),(30,48).
- Risk: maroon behavior beyond 1-step-chase unknown; if death, check frames for its move pattern.

## Turn 24: LEVEL 7 CLEARED (score 7, actions 162-175, 14 moves, 0 deaths)
- Maroon chased 2-behind the whole route; never caught up. Trail-follow ascent is safe at gap 2.

## LEVEL 8 (starts action 176)
Nodes: goal(14,26); (14,32),(14,38); col38: 14-20-26-32; maroon(20,38) faces DOWN; row32: 20-26-32-38-44; red(32,20) faces DOWN (guards (38,20)); col20: 32-38-44; col26: 32-38-44; row44: 14-20-26; player start (44,14).
Cycle for pursuit-shaking: (32,20)-(32,26)-(38,26)-(44,26)-(44,20)-(38,20), len 6.
Goal ONLY reachable via col 38 ascent (14,38)->(14,32)->(14,26). Maroon LOS = {(26,38),(32,38)}.
Budget: 64px fresh, 2px/move = 32 moves.
Maroon models: (a) persistent chaser (b) walk-to-last-seen-then-stop (c) rook charge to corridor end. L7 consistent with all.
Turn 24 plan (10 moves): R,R,U,U,L(kill red from east),R,R,R(activate at (32,38)),L,L -> end (32,26).
Expected after: maroon at (32,38) [models b/c stop there; model a = following me].
Next-turn branches:
- maroon stopped at (32,38): attack from west (R) to test maroon killability (marker should show facing down -> west=side attack). If killable: then ascent R,R,U,U,U... wait from (32,38): U,U,U? col38 up: (26,38),(20,38),(14,38) then L,L to goal = kill+5... total.
- maroon chasing (at (32,32)): lure around cycle D,D,L,U,U,R then R,R,U,U,U,L,L ascent with it 2 behind.
- maroon adjacent-facing charge-kill: NEVER stand at (26,38) while it's at (20,38) facing down.

## Turn 25 (after Action 185)
- Actions 176-185 per plan: red KILLED (180, east attack). Maroon activated (183), stepped (26,38)->(32,38). Me (32,26), it (32,38), gap 2. Marker gone since activation (no facing shown).
- Budget: 20px used, 44 left (~22 moves).
- DANGER: if chaser, moving R to (32,32) = it steps onto me = death. First move must keep gap>=2.
- Sent discriminator: D -> (38,26).
- Branch STOPPED (it stays (32,38)): kill test: U,R,R(attack from west),U,U,U,L,L (8 moves -> goal if maroon killable). If unkillable -> death/reset, attempt 2 with chaser knowledge.
- Branch CHASER (it steps to (32,32)): lure around cycle from (38,26): D(44,26),L(44,20)... CAUTION tie-break ambiguity when it's at (32,26) and I'm at (44,20): its shortest path tie (32,20)|(38,26) - if (32,20) branch, my U to (38,20) = collision death. Must simulate adversarially before committing; may need to re-derive safe cycle timing.

## Turn 26 (after Action 186)
- CHASER CONFIRMED: maroon (32,38)->(32,32) as I moved to (38,26). Persistent, 1 step/move, all steps so far forced-unique (no tie data).
- Maroon UNKILLABLE while chasing: approaching to adjacency lets it step onto my node (death) before I can attack.
- Adversarial pursuit search: UNWINNABLE at any depth. Deterministic tie-break sims: 6/24 direction-priority orders winnable (those preferring D/L/R over U at key ties), 18/24 unwinnable even with full knowledge.
- Winning routes all start (38,26)->D(44,26)->L(44,20). Tie occurs on maroon's response to my L: from (32,26), candidates {(32,20) [L], (38,26) [D]} equidistant-2 to me at (44,20).
  - If maroon->(38,26): trail-follow/D-priority -> continue cycle U(38,20),U(32,20),R,R,R(32,38),U,U,U,L,L (win, ~12 total).
  - If maroon->(32,20): L-priority chaser -> go back R(44,26),U(38,26),U(32,26),R(32,32),R(32,38),U,U,U,L,L per LDUR sim (verify each step vs sim).
- Also testing trail-follower (breadcrumb) model: it would retrace my path exactly; consistent with all data so far.
- Budget: 11 moves used on L8 (42px left = 21 moves). Winning route needs ~12 more. Tight but OK.
- Sent: D,L probe (= winning-route prefix, zero waste).
- IF maroon shows U-priority later (unwinnable class): look for new mechanic (blocked-input freeze? maroon deactivation at distance? RESET and try different activation geometry).

## Turn 27 (after Action 188)
- Probe result: me (44,20), maroon took D branch (32,26)->(38,26). Eliminated: LDUR,LDRU,ULDR,RULD (L-preferring). Alive: trail-follower, DLUR,DLRU,DRLU,RDLU (winnable), UDLR,UDRL,URDL (UNWINNABLE class).
- Next tie is immediate: on my U to (38,20), maroon from (38,26) ties {(32,26)[U], (44,26)[D]}.
  - ->(44,26): D-priority/trail (winnable). Commit remaining 9: U(32,20),R(32,26),R(32,32),R(32,38),U(26,38),U(20,38),U(14,38),L(14,32),L(14,26). Verified safe vs DLUR/DLRU/DRLU + trail models (all subsequent its-steps forced or U-last ties, min gap 2, no lands-on-me).
  - ->(32,26): U-priority. DO NOT continue U (next U to (32,20) = it steps onto me). Safe at dist 2; re-plan (movement-only unwinnable per sim -> seek new mechanic or RESET).
- Sent single probe: U -> (38,20). Budget: 13 used, ~19 moves left; winning line needs 10.

## Turn 28 (after Action 189)
- Tie 2 result: maroon (38,26)->(44,26) = D/trail branch. U-priority ELIMINATED. Alive: trail-follower, DLUR, DLRU, DRLU, RDLU - all winnable, all verified safe for the endgame.
- Committed 9 moves from (38,20): U(32,20),R(32,26),R(32,32),R(32,38),U(26,38),U(20,38),U(14,38),L(14,32),L(14,26)=GOAL. Min gap 2 throughout, no maroon step lands on me under any alive model.
- L8 total if clean: 23 moves, 0 deaths.
- MAROON MECHANIC SUMMARY (for future levels): LOS-activated persistent chaser, 1 step per player move, steps along shortest path to player's current node, tie-break prefers D over U and over L (trail-consistent). Unkillable while chasing. Beat it with cycle dodge + trail-behind ascent; keep gap>=2; never move adjacent-toward it.

## LEVEL 8 CLEARED (score 8, actions 176-198, 23 moves, 0 deaths)

## LEVEL 9 (starts action 199). Player (34,33), Goal (40,33). Budget 64px = 32 moves.
Enemies: O1 orange (16,27) faces L, patrols row16 corridor 9-15-21-27-33, period 8: at 27 when k mod 8 in {6,0}, so (16,27) arrival k must be mod 8 in {2,3,4,5}.
O2 orange (16,45) faces L, row corridor 39-45-51, period 4: k mod 4: 1->39,2->45,3->51,0->45.
O3 orange (22,45) faces D, col45 corridor 16-22-28-34, period 6 from k=1: [28,34,28,22,16,22] for k mod 6 = 1,2,3,4,5,0.
MAROON (22,27) faces D, LOS={(28,27),(34,27)}. First move (34,33)->(34,27) is FORCED and activates it.
R1 red (40,27) faces R = guards GOAL (40,33). R2 red (46,27) faces U = guards (40,27).
Kill order: (46,33)->L kill R2 (east side), (46,27)->U kill R1 (south side), (40,27)->R goal.
Graph edges saved in turn-29 analysis; key: only W-N crossing = col27 through (22,27); only N-E crossing = row10 (10,33)-(10,39); only E-S crossing = (34,39)-(40,39); (16,51) & (16,33) & (10,51) dead ends... (10,51): edge (10,45)-(10,51) only = dead end. (16,33)-(16,27) dead end.
West 6-cycle for maroon dodge: (34,27),(34,21),(28,21),(22,21),(22,27),(28,27).
ROUTE SKELETON: cycle-swap past maroon, N up col27 timed for O1, row10 east, (10,45)->(16,45) [O2/O3 timing!], descend to (34,45) via col45 or (22,39) detour, (34,39),(40,39),(46,39),(46,33),(46,27)K,(40,27)K,(40,33) GOAL.
MODEL AMBIGUITY (maroon): trail-follower vs DLUR vs DLRU/DRLU/RDLU — diverge during cycle dodge. Double-CCW-loop safe for trail-follower & DLUR-ish, FATAL for others at (28,27); ping-pong retime safe for DLRU/DRLU/RDLU, FATAL for trail-follower. -> MUST probe in small batches and branch on observations. Keep gap>=2 always.
Turn 29: sent m1-m2: L,L -> (34,27) [sight turn, maroon frozen], (34,21) [maroon steps: (22,21)|(28,27)|other - observe]. Safe under all models.
O-phase after k=2: O1 (16,15), O2 (16,45), O3 (34,45).

## Turn 30 (after Action 200, k=2)
- k2 tie: maroon (22,27)->(28,27) = D. Trail-follower ELIMINATED. Alive: DLUR/DLRU/DRLU/RDLU (aka "prefer D" data so far; all 3 observed ties chose D when available).
- Budget drain L9 = 1.5px/move -> ~42 moves total. Currently k=2, 61px left (~40 more).
- CRITICAL FINDINGS (searches in turn-30 analysis):
  1. Straight-run schedule W->N->NE->S->goal = 37 moves, needs a=(16,27) arrival ≡ 20 (CRT of O1 mod8 {2,4}, shape mod6, parity).
  2. NE east-detour (22,45)->(22,51)->(28,51)->(28,45) is FORCED by O3 timing, but trailing maroon at gap 2-3 creates DEATH TRAP at (28,51) (its D-tie step (22,45)->(28,45) lands on me; gap>=4 impossible to build - west 6-cycle caps at 3).
  3. Knowledge-set adaptive search over all 4 maroon models: UNSOLVABLE from k2 state AND from fresh start, even with goal-trump + lenient-pre relaxations, MAXK=42. => MY MODEL IS WRONG SOMEWHERE.
- Suspects: O3 bounce range (16,45)-bounce vs continue to (10,45) [period 6 vs 8 - changes ALL NE windows]; O2 east bounce; maroon rule variant.
- Observations pending: O3 at k5=(16,45) both ways; k6: (22,45)=bounce6 vs (10,45)=range8. O2 k3=(16,51) confirms period 4.
- Sent k3,k4,k5 = U,U,R -> me (28,21),(22,21),(22,27). Safe all models. k5 response discriminates: maroon->(28,21)=DLUR (case A osc = (22,27)<->(28,27) at odd/even) vs ->(34,27)=DLRU/DRLU/RDLU (case B osc = (22,27)odd<->(22,21)even).
- NEXT TURN: read maroon case + O3 k5 pos; send 1 oscillation move (case-appropriate); read O3 k6 bounce; re-run searches with corrected schedule + pinned models. Oscillation is sustainable indefinitely (~20 spare moves), so info-gathering is cheap.

## Turn 31 (after k5, Action 203)
- State k5: me (22,27), maroon (28,21) [DLUR pin held: k5 step was U per {U,R} tie → U], O1 (16,21), O2 (16,39), O3 (16,45).
- Maroon blob shows a yellow 'G' pixel (facing indicator?); player 'q' pixel marks last move dir.
- Full DLUR-pinned search: UNSOLVABLE under all combos (O3 per6/per8 × sidekill on/off × goal-trump on/off × adjacency-front rules). Some model assumption is wrong.
- Gap-3 NE entry route (37 moves, kills O2/R2/R1, goal @37) survives IF gap 3 achievable — it isn't under current model (west oscillation locks gap 2).
- (28,51) pocket = death trap at gap 2 (both exits are maroon steps onto me).
- Candidates for wrong assumption: O3 range/period (k6 distinguishes: (22,45)=per6 vs (10,45)=per8), lenient pre-occupancy (enter node enemy vacates), maroon-arrival≠death, blocked-input effects.
- SENT k6 = ACTION2: me →(28,27); maroon (28,21) tie {U,D}→D=(34,21) safe; O1→(16,27); O2→(16,45). Observe O3 k6 position next turn.
- Oscillation sustainable: k7 ACTION1 returns me (22,27), maroon →(28,21) (tie {U,R}→U). ~36 moves budget left at k6.
- NEXT TURN: read O3 k6 pos → fix schedule; re-run search with corrected O3 + lenient pre-occupancy relaxation; if solvable plan found consider RESET for fresh budget (knowledge carries over).

## Turn 32 (after k6, Action 204) — MODEL BREAKTHROUGH
- O3 CONFIRMED period 8: at (10,45) @k6. Schedule O3_8 correct.
- MAROON = LAG-2 PATH REPLAYER: M_k = P_{k-2} exactly (all 6 L9 datapoints). NOT a BFS chaser; L8 "tie" observations were coincidental trail-steps. G pixel = facing indicator.
- Death constraints: P_k != P_{k-2} (maroon steps onto me) and P_k != P_{k-3} (I step onto maroon). No 2-step backtracking, ever; cycles >=4 fine; (28,51) pocket NOT a trap.
- k7 was forced to (34,27): returning to (22,27)=P_5 would be death (my old "safe oscillation" was lethal!).
- (34,33) is a dead-end pocket = suicide under lag-2 rule (only exit is P_{k-2}). Never enter with maroon trailing.
- (16,45) is O2-impassable without killing it (O2 returns every 2 moves); col-45 passage mandatory for goal region (only entrance (34,45)->(34,39)->(40,39)).
- ROUTE (goal @k29): P7..P29 = (34,27),(34,21),(28,21),(22,21),(22,27),(16,27),(10,27),(10,33),(10,39),(10,45),(16,45)[KILL O2 from north, side-kill test],(22,45),(22,51),(28,51),(28,45),(34,45),(34,39),(40,39),(46,39),(46,33),(46,27)[kill R2 from east; faces N],(40,27)[kill R1 from south; faces E],(40,33)=GOAL. Verified vs O1/O2/O3 schedules + maroon constraints programmatically.
- SENT k7-k17 (11 moves) ending at O2 kill test. If survived: next send k18-k29 = A2,A2? no: (22,45)D? wait: k18 (22,45)=A2? from (16,45) down=A2; k19 (22,51)=A4; k20 (28,51)=A2; k21 (28,45)=A3; k22 (34,45)=A2; k23 (34,39)=A3; k24 (40,39)=A2; k25 (46,39)=A2; k26 (46,33)=A3; k27 (46,27)=A3; k28 (40,27)=A1; k29 (40,33)=A4.
- If O2 kill fails (death/reset): side-kill false -> level needs different O2 mechanic; replan attempt 2 (budget refreshes, maroon deactivates, knowledge carries).

## Turn 33 (after k17, Action 215)
- O2 SIDE-KILL CONFIRMED: landed on O2 at (16,45) from north -> O2 dead. Orange kill rule proven: land from non-facing side.
- All models held perfectly: maroon (10,39)=P_15 (lag-2), O3 (28,45)=k17%8=1, O1 (16,21).
- Magenta 42 @k17 (~1.29px/move). Sent k18-k29 endgame: pocket descent, kill R2 (east), kill R1 (south), GOAL (40,33) @k29.
