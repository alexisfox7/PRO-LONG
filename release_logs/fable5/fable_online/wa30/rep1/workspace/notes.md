# Game notes

## Level 1 initial layout (64x64)
- Player: 4x4 sprite, white top row `$` + green `I` body, at rows 48-51, cols 32-35. White cap may indicate facing direction.
- Blue boxes (q border, f fill, 4x4):
  - A: rows 24-27, cols 44-47
  - B: rows 28-31, cols 16-19
  - C: rows 36-39, cols 32-35 (directly above player, same cols)
- Container: blue frame rows 28-31, cols 28-39; gray `#` interior rows 29-30, cols 29-38 (10x2). Likely goal for boxes.
- Row 63: full-width light-magenta `z` bar — suspected timer/step budget.

## Confirmed mechanics (after actions 1-2)
- Each move = 4 rows/cols (one 4px cell). Player moved 48->44->40.
- When player becomes adjacent to a box, box border turns gray `h` (contact/grab highlight).
- Bottom z bar = budget: 64 cells; 1 cell consumed (col 63 -> q) after 2 actions (~0.5/action? watch).

## Hypotheses
- Sokoban-like: push boxes into container (interior rows 29-30 cols 29-38).
- Box C at rows 36-39 cols 32-35; pushing up 2 more should put it at rows 28-31, overlapping container rows exactly.
- Test 2 (actions 3-4): FAILED — box does NOT push; player blocked at rows 40-43, box stayed 36-39. No budget consumed by blocked moves (z still 63).
- Test 3 (actions 5-6): SUCCESS — ACTION5 grabs adjacent highlighted box; box border turns white `$` and box rides on top of player (player shrinks to $cap row + 3 I rows, box stacked above). Moves with player.
- Carry state after action 6: box rows 32-35, player rows 36-39, cols 32-35. Container rows 28-31 directly above.
- Test 4 (actions 7-8): SUCCESS — carried box moved INTO container rows 28-31 (frame permeable to carried box), ACTION5 released it there (border -> h). Score still 0: need all 3 boxes. Container = 3 slots: cols 28-31, 32-35 (filled by C), 36-39.
- ACTION5 toggles grab/release; released box stays in place (no gravity).
- Budget: z=61 after 8 actions (blocked moves may not consume).
- Actions 9-17 plan: player (32-35,32-35) -> R,R,R (cols 44-47), Up (rows 28-31, below box A), grab, Down, L,L (box at rows 28-31 slides to cols 36-39 right slot), release. If sideways slide into container blocked, box drops at cols 40-43 — recover by vertical entry route.
- Box A deposited in right slot cols 36-39 via sideways slide (action 17). Sideways container entry CONFIRMED. Settled boxes revert to q border; adjacent ones show h. z=59 after 17 actions.
- Actions 18-27 FAILED to grab B: white cap = FACING direction (moves change facing). ACTION5 grabs only in facing direction. I faced left; box was above. Player ended rows 32-35 cols 24-27 facing right. Box B untouched at rows 28-31 cols 16-19. z=55.
- Release (ACTION5 while carrying) appears NON-directional (box A released while facing left, worked).
- Actions 28-32: POSITION MIS-TRACK — player had ended action 27 at cols 28-31 (not 24-27). L,L put it at 20-23 (right of B with gap... no, adjacent? B at 16-19, so 20-23 IS adjacent), Up moved freely to rows 28-31 (facing up), grab hit empty air above, R -> now rows 28-31 cols 24-27 facing right. Blocked-move facing test NOT performed. z=54.
- LESSON: always verify player position from last board before planning; don't assume.
- Actions 33-44: Down, L x4 (rows 32-35 to cols 8-11), Up (rows 28-31), R (cols 12-15, facing right, adjacent to B's left), grab, R x3 (push B 16-19 -> 28-31 into left slot, player ends 24-27), release. Expect level clear.
- Note: dragging B from its right side fails: player would need to stand in middle slot (box C) to bring B to left slot.
- Old plan for box B: box B at rows 28-31 cols 16-19 -> left slot cols 28-31. Note B is at same rows as container — grab from below (player rows 32-35 cols 16-19), carry: box on head... B grabbed from below puts box above? No—grab attaches box in place. Player below B: box at 28-31, player 32-35. Then move right: box slides at rows 28-31 straight into left slot cols 28-31. Then release. Route: from (32-35,36-39) after A: L,L,L,L,L (cols 16-19), grab, R,R,R (cols 28-31), release = 10 actions.

## Parser: /workspace/parse.py (boards() returns list of (header, 64-line grid))

## LEVEL 2 (started action 45, z bar reset to 64)
- Level 1 cleared at action 44 (score 1): all 3 boxes in container slots.
- Player start: rows 8-11 cols 12-15, facing up.
- Container: rows 28-39, cols 12-19 = 6 slots (2 cols x 3 rows): L-col cols 12-15, R-col 16-19; rows 28-31/32-35/36-39.
- Boxes (5): B1(20-23,40-43) B2(24-27,48-51) B3(28-31,36-39) B4(32-35,48-51) B5(40-43,44-47).
- Orange solid 4x4 at (36-39,24-27): unknown, treat as wall.
- 5 boxes / 6 slots: maybe only 5 required. Leave middle-left slot (32-35,12-15) empty (only reachable from left).
- Slot entry: top slots from above/side, middle-right from right (player 20-23), bottom from below. Box attaches at grab offset and keeps it; grab is directional (facing).
- Actions 46-65: R x8, D x5, L (at 28-31,40-43 facing left), grab B3, L x5 (box -> top-right slot 16-19). NEXT CALL: ACTION5 to release.
- Slot assignments (tentative): B3->top-right(28-31,16-19); B1->middle-right(32-35,16-19)? B1 at (20-23,40-43): route around; B4(32-35,48-51)->middle-right via push left (rows 32-35: path clear? orange at 36-39 no, container... push left from 48: box passes 44-47,40-43,...20-23 -> 16-19; player ends 20-23 rows 32-35. GOOD, B4 is natural middle-right.
- Then B1 -> top-left(28-31,12-15) from above: box below player at rows 28-31? grab B1 facing down (player above it at 16-19? B1 at (20-23,40-43): player at (16-19,40-43) facing down, grab, then carry: box offset below; move left cols 40->12 (8 moves... but box below at rows 24-27... wait need box at rows 28-31 finally with player at 24-27. Player path rows 16-19 then down 2. Box at player+4rows. Route: grab, D (player 20-23, box 24-27), L x7 (cols 40->12: player (20-23,12-15), box (24-27,12-15)), D (player 24-27, box 28-31 = top-left slot), release. Check: box passing rows 24-27 cols 36..12: B2 at (24-27,48-51) no; clear. Player rows 20-23 clear.
- B2(24-27,48-51) and B5(40-43,44-47) -> bottom-right(36-39,16-19) from below? and bottom-left(36-39,12-15) from below: player at rows 40-43, box above. Orange block at (36-39,24-27) is at bottom-row height — careful pathing rows 36-43.
- MAJOR: orange 4x4 = autonomous collector robot, moves 1 cell/action. It grabbed B3 (box border turns BLACK 'O' when robot-carried), carried it along rows 32-35, entered container (robot CAN stand in slots), deposited B3 into top-right slot (28-31,16-19), then grabbed B4 at (32,48), now dragging it left (box attached on robot's right).
- My action-60 grab hit EMPTY AIR (robot had taken B3). I am NOT carrying. h border = box player faces/adjacent (highlight only).
- NEVER blind-ACTION5: would grab slotted box back out. Verify carry state each call.
- Actions 66-85: U x4, R x5, D (at 16-19,40-43 facing down), grab B1 below, D (box 24-27), L x7 (cols 40->12), D (box -> top-left slot 28-31,12-15, player 24-27). NEXT CALL: verify carrying B1, then ACTION5 release.
- Watch: robot may deposit B4 into middle-right; may steal B1 before my grab (recoverable). Avoid rows 32-35 corridor (robot path).
- Board 85: player (20-23,16-19) carrying B1 below at (24-27,16-19), facing down. Robot deposited B4 -> middle-right slot; robot at (28-31,48-51) below B2. Slots filled: TR(B3), MR(B4). z=27 (~0.9/action burn in level 2; level 1 was ~0.25 — maybe robot presence raises tick rate).
- Actions 86-105: L, D (B1 -> top-left slot 28-31,12-15), release, then L, D x6 (col 8-11 to rows 48-51), R x9 (rows 48-51 to cols 44-47), U (44-47,44-47 facing up, below B5).
- NEXT CALL: verify B5 still at (40-43,44-47) and I'm at (44-47,44-47) facing up NOT carrying; then: grab, U (box 36-39), L x7 (box -> bottom-right slot 36-39,16-19), release = 10 actions. If robot took B5 or filled bottom-right with B2, redirect to bottom-left (L x8, box cols 12-15).
- Budget risk: ~30 actions needed vs ~27 z. Blocked moves don't burn z (level 1 evidence).
- Board 105: I misread cols initially — player IS at planned (44-47,44-47) facing up; B5 free at (40-43,44-47) with h; robot at (40-43,40-43) about to grab B5. Slots: TL,TR,MR,BR filled. Open: BL(36-39,12-15), ML(32-35,12-15). z=9!
- Robot deposited B2->BR at board 97-98. Robot route for B5->BL ~11 ticks; my steal route also ~11; z only covers ~9-10. GAMBLE (actions 106-115): D x10 — drop to bottom edge, then blocked-D spam = hopefully free ticks (level-1 evidence: blocked moves don't burn z) while robot carries B5 to BL.
- If z hits 0 -> level resets; redo knowing: let robot work, I do far boxes first. If robot frozen during blocked spam -> blocked moves are full no-ops; plan exact real-move counts.
- z burn NOT strictly 1/action (board 97->98 burned 0). Avg ~0.9 in level 2.

## LEVEL 3 (started action 115/board 116, z=64, score 2 after level 2 clear at action 114 — robot delivered B5; blocked-move idle gamble WORKED, z never hit 0)
- Dashed wall cols 32-35 full height; gaps at rows 12-15 (plugged by box W1) and rows 32-35 (plugged by W2).
- Player start (36-39,16-19) facing up, LEFT side. Robot (12-15,48-51) RIGHT side.
- Container rows 24-39, cols 52-59 = 8 slots (cols 52-55/56-59 x rows 24-27/28-31/32-35/36-39).
- Left boxes: L1(16-19,8-11), L2(20-23,20-23), L3(44-47,12-15). Wall boxes: W1(12-15,32-35), W2(32-35,32-35).
- Boxes must be pushed through gaps IN FRONT of player (grabbed facing right); side-carry through gap impossible (player would hit wall).
- Actions 115-134: U,R,R,R, grab W2, R x5 (W2 -> slot 32-35,52-55), release, L x5 (back through gap to 32-35,28-31), U x4 (to 16-19,28-31).
- NEXT: U(12-15,28-31)? then L x2 (12-15,20-23), D (16-19,20-23) facing down, grab L2, D x3 (box to 32-35,20-23... wait recheck), release, reposition left of box, push right through gap, leave at rows 32-35 cols 40+ for robot.
- Robot will likely take W1 (same rows 12-15). Watch its deposits. 5 boxes, 8 slots.
- Boards 117-136 decoded: W1 was IN upper gap; robot PULLED it out rightward (boards 120-128) and slotted it at (24-27,52-55) — wall RESEALED instantly when W1 left the gap (rows 12-15 cols 32-35 now # lattice).
- My 5 R-pushes on grabbed W2 were ALL BLOCKED: cannot PUSH a box out through a gap from my side (or player cannot enter gap cell). Boxes can only be PULLED out by the far side. I released W2 back; it sits in lower gap; robot now adjacent (32-35,36-39), will pull it out and slot it; lower gap will seal -> left/right permanently split.
- $ cap detector caveat: facing right = cap is rightmost column only (bb('$') gives col of cap, not sprite origin). Grabbed boxes have $ border = invisible to q/h/O box scans.
- z burn ~0.5 even on blocked moves in level 3 (boards 121-126: z 61->58). "Blocked free" NOT reliable.
- Theories: (a) level needs only W1+W2 delivered (others decoys); (b) wall vanishes after both gap boxes delivered, then ferry L1-L3.
- Actions 135-149: grab L1, D x5 (box 36-39 rows, me 40-43, cols 8-11), R x9 (stage box toward wall rows 36-39; will block at box cols 28-31 if wall persists; if wall vanishes, box continues toward cols 44-47).
- Player after: ~(40-43,24-27 or 40-43) carrying L1, facing right. NEXT: check score / wall state / robot; release only when box in a slot.
- Boards 137-151: robot pulled W2 out, slotted it at (32-35,52-55); robot IDLE at (32-35,56-59) in container since. Score STILL 2 -> all 5 boxes needed. Wall fully resealed (no gaps, uniform lattice rows 0-62 cols 32-35).
- I still CARRY L1 (box directly above me); blocked at (36-39,28-31)/me (40-43,28-31) facing right — both box and I faced wall rows there (inconclusive re box-permeability).
- Insight: W2-in-gap push was blocked even though box target cell was free and my target cell (gap, open) was free => GAP CELLS FORBID PLAYER. Hypothesis: aperture cells (rows 12-15 & 32-35, cols 32-35) are box-only doors that visually reseal; a SAME-ROW push may insert a box into them (me staying at cols 28-31), robot pulls from far side.
- Actions 152-160: U (box to 32-35,28-31 aperture rows), release, L, L, U, R (me to (32-35,24-27) facing right), grab, R (push box into aperture 32-35,32-35), R (probe: box exits to 36-39? me likely blocked at aperture edge).
- NEXT: if box entered aperture cells, release and let idle robot (same rows!) pull it. If push blocked, aperture is dead -> rethink entirely (z=42).
- CONFIRMED (board 159): same-row push inserts box INTO sealed aperture (32-35,32-35) — wall lattice is box-permeable at former gap cells; player cannot enter (second R blocked). L1 sits grabbed in aperture.
- Actions 161-174: release L1 in aperture (robot at (32-35,56-59) same rows should pull & slot it), U x5 (cols 28-31 to rows 12-15), L x2, D ((16-19,20-23) facing down), grab L2, D x3 (box to (32-35,20-23), me (28-31,20-23)), release.
- NEXT: reposition (L,L,D,R to (32-35,16-19) facing right), grab, R x3 (L2 -> aperture), release — ONLY IF aperture empty (robot must have pulled L1 first!). Then L3 (44-47,12-15): raise to rows 32-35: grab from below? me (48-51,12-15) facing up, grab, U x3 (box 32-35,12-15, me 36-39? box above me: box 40-43->...; me rows 44->36; box at 32-35 when me 36-39), then release+reposition for same-row push: box needs cols 28-31 first: push right along rows 32-35: me (32-35,x) behind box... plan later.
- z=36 at board 160.
- Boards 161-174: L1 pulled by robot & being slotted (28-31,52-55). L2 staged at (32-35,20-23), me (28-31,20-23) facing down. z=27.
- Actions 175-194: L,L,D,R (to (32-35,12-15)->(32-35,16-19) facing right), grab L2, R x3 (L2 -> aperture, me (32-35,28-31)), release, D x5 (to (52-55,28-31)), L x4 (to (52-55,12-15)), U ((48-51,12-15) facing up below L3), grab L3.
- NEXT CALL: verify carrying L3; then U x3 (box to (32-35,12-15), me (36-39,12-15)), release, L,L,U,R (to (32-35,8-11) facing right), grab, R x5 (L3 -> aperture), release. ~15 actions. Then wait for robot to finish -> level clear expected.
- Board 194: carrying L3 (me 48-51,12-15; box above). Robot pulled L2, ferrying to slot. Slotted: W1(24,52), L1(28,52), W2(32,52). z=14.
- Actions 195-214: U x3 (box to 32-35,12-15), release, L, U (32-35,8-11 facing up), R (BLOCKED by box — testing facing-flip trick), A5 (grab if facing right; if trick failed this grabs nothing... actually facing up grabs air), R x5 (push L3 to aperture, me (32-35,28-31)), release, R x6 spam (blocked ticks ~0.5z to advance robot).
- If facing trick failed: A5 grabbed air, R x5 blocked, final A5 may re-grab or nothing; recover next call with L,U,R loop via (32-35,4-7).
- Endgame: robot must pull L3 + slot (~14 ticks) vs z~4-5 + cheap blocked ticks. Borderline; if z=0 -> reset, redo optimally (~50 actions known-route).


## Call 12 (after action 212, board 214)
- Facing-flip trick WORKED: L3 pushed into aperture (32-35,32-35), released. 4 boxes slotted (rows 24,28,32,36 @ col52). Robot at (36-39,36-39) adjacent to L3.
- z=1. Dispatched ACTION4 x6 (blocked, ~0.5 z each) to TEST z=0 behavior + tick robot.
- NEXT CALL branches:
  a) z=0 no-reset, robot ferrying L3 -> keep blocked-spam ACTION4 x20 until score 3.
  b) Level reset (fresh board, z=64): redo L3 optimally. Stray rights post-reset may have moved player; re-verify position first.
  c) Score 3: map Level 4.
- Optimal L3 redo (~50 acts): W1/W2 leave to robot. L-boxes: grab from side allowing direct staging at rows 32-35 col 28-31, same-row push R into aperture, release, robot pulls. Apertures rows 12-15 & 32-35, cols 32-35. Player NEVER enters aperture cells. Blocked move flips facing (proven, action ~200).


## Call 13 (after action 219, Attempt 2)
- CONFIRMED: z=0 resets level (Attempt 2 started action 215, z back to 64).
- Fresh layout (same as Att.1): aperture boxes (12-15,32-35) & (32-35,32-35) [robot's]; my 3 left boxes: B_a(20-23,20-23), B_b(16-19,8-11), B_c(44-47,12-15). Robot grabbed upper aperture box at tick 219.
- Player after stray Rights: (36-39,28-31) facing right. z=61.
- Dispatched 20: L x4, U x4, R (grab spot 20-23,16-19 facing right), A5 grab B_a, D x3 (me rows 32-35 cols 16-19, box at cols 20-23), R x3 (box into aperture when free; blocked-wait if occupied), R x4 spare blocked-waits.
- NEXT CALL: verify box in aperture (32-35,32-35) and I'm at (32-35,28-31) STILL CARRYING. If so: A5 release, then fetch B_b(16,8): route L x5? (cols 28->8? no: grab from (16-19,4-7) facing right) -- compute exact from actual position. If push still blocked-waiting: more Rights.
- z rate: real ~0.9, blocked ~0.5. Budget: ~45 left after batch; need ~35 more real. Tight -- minimize detours.


## Call 14 (after action 239, Attempt 2, z=49)
- B_a carried into aperture (32-35,32-35), me (32-35,28-31). Upper box slotted (24,52). Robot ferrying lower-orig box (O at 32,44).
- Dispatched 20: A5 (release B_a), L x6 (to 32-35,4-7), U x4 (to 16-19,4-7), R (blocked into B_b -> facing flip right), A5 (grab B_b), D x4 (me 32-35,4-7; box 32-35,8-11), R x3 (partial: me toward cols 16-19).
- NEXT CALL: continue R x3 (box into aperture -- blocked-wait if robot hasn't pulled B_a yet; add spare Rights), then A5 release, then fetch B_c (44-47,12-15): route from (32-35,28-31): D x3? me rows 32->44 at cols 28-31? Plan: go to (44-47,8-11), blocked-flip R into B_c, grab, carry U x3 (box rows 44->32), R x5 (box into aperture). Verify positions first!
- Robot should pull B_a from aperture ~tick 250-ish. Watch for steal conflicts.


## Call 15 (after action 259, Attempt 2, z=36)
- Slotted: (24,52),(28,52),(32,52). Carrying B_b at (32-35,20-23), me (32-35,16-19). B_c last at (44-47,12-15).
- Dispatched 20: R x3 (B_b into aperture), A5 release, D x3 (rows 32->44 cols 28-31), L x3 (cols 28->16, stop right of B_c), U1, L x2 (over B_c via rows 40-43 to cols 8-11), D1 (to 44-47,8-11), R (blocked-flip into B_c), A5 grab, U x3 (me rows 44->32 cols 8-11, box 32-35,12-15), R x1 (of 5).
- NEXT CALL: verify carrying B_c; then R x4 (box into aperture, blocked-wait spares), A5 release -> robot slots -> SCORE 3. Then map Level 4.


## Call 16 (after action 279, Attempt 2, z=23)
- B_b slotted (36,52). 4/5 done. Carrying B_c at (32-35,16-19), me (32-35,12-15).
- Dispatched: R x4 (B_c into aperture), A5 release, R x15 blocked-wait (robot pulls B_c, slots at ~(40,52) -> SCORE 3).
- NEXT CALL: expect score 3 + Level 4 fresh board. Map it: components, player, robot(s), boxes, container, z. If somehow not cleared (z died ~12 margin, should be fine), assess.


# LEVEL 4 (score 3 at action 302; Attempt 1, z=64)
Layout (initial board, action 302 settled):
- Lattice diamond enclosure rows 20-47 cols 20-43 (level-3-style # lattice; player-impassable, box-permeable? TESTING).
- Player starts (32-35,28-31) inside. 6 boxes inside: (24,24),(24,32),(24,36),(36,32),(40,24),(40,36). 7th box outside top-left at (4-7,24-27) next to O wall (cols 28-31 rows 0-19).
- Containers: 2-slot vert (24-31,4-7) left; single (36-39,8-11) left-mid; single (28-31,52-55) right-mid; single (20-23,56-59) right-top; 2-slot horiz (56-59,36-43) bottom. 7 slots = 7 boxes.
- 3 robots: (4-7,56-59), (12-15,8-11), (56-59,24-27).
- O funnel walls bottom corners; z=64 fresh.

## Call 17 (action 302)
- Dispatched 12: R,U,A5(grab box 24,32),U(push into top lattice tile 20-23,32-35),A5 rel, D,L,L,U(blocked-flip at 28-31,24-27),A5(grab box 24,24),U(push into tile 20-23,24-27),A5 rel.
- Tests: lattice permeability (2 tiles), robot pull response.
- NEXT CALL: check whether boxes entered tiles rows 20-23, whether robots pulled them, z burn. If impermeable: try pushing via side edges (cols 20-23 / 40-43) or look for specific aperture tiles.


## Call 18 (after action 314, L4 Att.1, z=56)
- CONFIRMED: lattice tiles box-permeable from inside. Boxes now in top tiles (20,32),(20,24). Robot1 ferrying outside box (O at 4,4 heading to left 2-slot container). Player (24-27,24-27) facing up.
- Dispatched 20: D,R x3,U(flip),A5,U(push box 24,36 -> tile 20,36),A5 | D,L,D(face down at 32-35,32-35),A5,D,D(push box 36,32 -> bottom tile 44,32),A5 | U,L,L,D(flip at 36-39,24-27),A5 [grab box 40,24].
- NEXT CALL: finish: D(push -> tile 44,24),A5, then box (40,36): U,R,R,R,D(flip),A5,D,A5. Verify robot pulls from tiles; watch z.


## Call 19 (after action 334, L4 Att.1, z=44)
- Slotted: (24,4) left-top slot, (20,56) right-top single. In transit: O(20,8) toward left-mid/left-bottom, O(24,52) toward right-mid. Tiles: (44,32) idle. Carrying box at (40-43,24-27), me above facing down.
- Dispatched 20: D(push -> tile 44,24),A5, U,R x3,D(flip at 36-39,36-39),A5,D(push box 40,36 -> tile 44,36),A5, D x10 blocked-wait.
- NEXT CALL: all 6 inside boxes ejected. Robots deliver: remaining slots left-bottom(28,4), left-mid(36,8), right-mid(28,52), bottom 2-slot(56,36/40). If not done, more blocked-wait (D at 40-43,36-39 is safe-blocked). z should hold (~31 after batch).


## Call 20 (after action 374, L4 Att.1, z=18)
- 6/7 slotted. LESSON: robots have SIDE ASSIGNMENTS -- left robot serves left containers and only pulls from left/top-left tiles; bottom robot ignored box in bottom tile (44,36) even while adjacent, because its containers (56,36/40) are full. Last slot: left container bottom (28-31,4-7).
- Fix dispatched (20): A5 re-grab box from tile, U (pull out), L x2 (box below me, to 40-43,28-31), A5 rel, R, D (to 40-43,32-35), L (blocked-flip left), A5 grab, L x2 (push box into LEFT tile 40-43,20-23), A5 rel, L x8 blocked-wait (left robot at (32,8) pulls + ferries to (28,4) ~12 ticks).
- z ~18 -> ~13 needed. If z=0 reset: redo L4 (~30 acts: eject 2 boxes to top-left tiles? NO -- assignments: left container needs 3 boxes via left/top-left, right 2 via top-right, bottom 2 via bottom tiles. Outside box auto-handled by left robot -> left-top slot).


# LEVEL 5 (score 4 at action 398; z=64)
Layout: vertical O wall cols 36-39 full height except channel rows 28-35 (channel bounded by O lips rows 24-27 & 36-39 spanning cols 24-39; channel floor cols 24-43 open, 2 cells high, PLAYER-passable).
- Container 8 slots (24-39,8-15) left. 1 robot (28-31,20-23) at left mouth.
- 6 boxes right side: B1(4,48) B2(8,56) B3(28,44) B4(48,52) B5(52,60) B6(56,44). Player (36-39,44-47).
- KEY TECHNIQUE: grab box facing up (box above me), then drag left along rows 32-35 while box travels rows 28-31 through channel. Works because channel is 2 cells high!
- z budget ~85-90 actions max (0.68/act avg). Full self-delivery ~150 acts = IMPOSSIBLE. Need robot to fetch from right side (test!) or hybrid.

## Call 21 (action 398/403 board, z=64)
- Dispatched 16: U (to 32-35,44-47 under B3), A5 grab (box above), L x5 (drag: box thru channel to (28-31,24-27), me (32-35,24-27)), A5 release next to robot, D x8 blocked-wait (D onto lip rows 36-39 = always blocked).
- WATCH: does robot slot B3? Does it then venture RIGHT through channel to fetch other boxes? If yes: cheap strategy = wait/assist. If no: I haul all; plan B4 via box-above drag (29 acts) etc., z very tight.


## Call 22 (after action 414, L5, z=56)
- B3 SLOTTED at (28,12). Robot came INTO channel and STOLE box from my grip ($->O) -- handoff works, release optional-ish. I ended at (32-35,32-35) facing down. Robot was moving right (24,8)->(24,12) at trace end -- may self-fetch far boxes: OBSERVE its moves during this batch!
- z=56. Full self-haul of 5 boxes ~120 acts ~82 z = TOO MUCH. Must split with robot or economize.
- SIDE-GRAB TECHNIQUE (cheapest): stand LEFT of box facing right (blocked-flip R), grab, drag UP (box rides +4 cols right of me) to rows 28-31, then drag L through channel; box ends (28-31,32-35), release, D to exit.
- Dispatched 20 (B4 haul, 22-act plan minus last 2): R x4, D x4 (to 48-51,48-51), R(flip), A5, U x5 (me (28-31,48-51), box (28-31,52-55)), L x5 (me (28-31,28-31), box (28-31,32-35)).
- NEXT CALL: A5 release, D exit; then check robot behavior: if robot self-fetched a far box (B1/B2/B5) during batch -> I only haul B6 next (22 acts) and let robot do rest; else I haul B6, B1, B2, B5 -- z will be very tight, prioritize and consider reset-with-better-plan if hopeless.
- Costs from center: B4 22, B6 22, B1 23, B2 25, B5 28.


## Call 23 (after action 434, L5, z=46)
- ROBOT SELF-FETCHES far boxes! It crossed channel, grabbed B1 (4,48) [O border]. Robot ranges whole map. Division of labor: robot does B1 then hopefully B2; I haul B4 (in grip at channel, releasing now), B6, B5.
- Dispatched 20: A5 (release B4 at 28-31,32-35), D (exit to 32-35,28-31), R x3, D x6 (to 56-59,40-43), R(flip into B6), A5, U x7 (me to (28-31,40-43), box (28-31,44-47)).
- NEXT CALL: verify positions (robot crossing rows 28-31 cols 44-47 could transiently block my U-run -> misalignment!). Then L x3 (box to 28-31,32-35), A5, D exit; then B5: R x7, D x5, R(flip), A5, U x6, L x7, A5, D (28 acts). Then blocked-wait (D on lip) while robot finishes.


## Call 24 (after action 454, L5, z=35)
- WARNING: robot FROZEN at (8-11,48-51) holding B1 (O at 4,48) for ~20 ticks, since the moment it grabbed. Theory: robot won't move while player also carries (dual-carry freeze)? Or pathing wait. B4 released at (28,32) untouched.
- Me: carrying B6 at (28-31,44-47), at (28-31,40-43) -- B6 haul on plan.
- Dispatched 9: L x3 (box to (28-31,32-35)... wait B4 at (28,32) OCCUPIES that spot! L drags will BLOCK when box hits B4: box can reach (28-31,36-39) only (1 L), then L blocked x2), A5 release at (28,36), D exit (32-35,32-35)? then D x4 blocked-wait on lip.
- CAUTION next call: box B6 likely released at (28,36) NOT (28,32). Verify. Watch robot: if unfroze after my A5 -> one-carrier rule confirmed; plan hauls with release-before-robot-grabs discipline. If still frozen -> investigate (print board area around robot).
- z=35. Remaining: B5 (52,60), B2 (8,56) + robot has B1. If robot dead, level infeasible this attempt -> consider RESET with optimized plan.


## Call 25 (after action 463, L5, z=31)
- Robot STILL frozen holding B1 even after I released B6 and left. Dual-carry theory DEAD.
- REVISED FACTS: robot NEVER collected idle released boxes B4(28,32)/B6(28,40) in channel (~40 ticks). It only (a) stole B3 from my GRIP in channel, (b) self-fetched B1 then froze. Full self-haul ~82z > budget => robot cooperation is by design; handoff = GRIP-STEAL not release. Possible role: robot fetches remote box then WAITS FOR PLAYER TO TAKE IT (test now).
- Dispatched 14: R x2, U x7 (to 4-7,44-47 via cols 44-47), R(flip toward B1), A5 (STEAL attempt from robot), R x3 (blocked, observe robot reaction).
- NEXT CALL: if steal worked (box $ border, mine): drag B1 down cols 48-51 (D x6, box rides right of me... box at cols 48-51 me cols 44-47) to rows 28-31, hold in channel for robot re-steal. Watch if robot unfreezes/resumes (fetch B2? take channel boxes?).
- z will be ~20: likely insufficient to finish attempt 1. PLAN: extract mechanics knowledge now; RESET when clarified; attempt 2 with correct pipeline. Known real costs: hauls B3 8, B4 22, B6 22, B1 23, B2 25, B5 28.


## Call 26 (after action 477, L5, z=24) -- RESET DECISION
- STEAL WORKED: A5 took B1 from robot's grip; robot INSTANTLY unfroze and fetched B2 (hauling fine).
- FREEZE ROOT CAUSE: robots PULL-ONLY. Robot grabbed B1 (pinned top edge) from below -> pull direction blocked -> permanent deadlock. AVOID letting robot target edge-pinned boxes from bad side.
- My R x3 'observation' moves actually PUSHED B1 to top-right (4,60). Lesson: after steal I was facing right holding box -> R pushes it.
- Released boxes in channel (B4,B6 att.1) were never collected -- but that was during robot freeze; unknown if free robot collects idle channel boxes. Grip-steal handoff IS proven (B3).
- ATTEMPT 2 PLAN (z=64, dispatched RESET+19):
  1. RESET; B3 handoff: U, A5, L x5 (box to (28,24) next to robot at (28,20) -> steal), A5.
  2. Sprint to B1 before robot targets it (~act 21 vs robot ~25): R x5, U x6 (this batch), then U, R(flip), A5 grab.
  3. Then: drag B1 down right side to channel (D x6, box cols 48-51), drag L to me (28,16-19)/box (28,20-23); self-slot via: push L (box 28,16), push U from below (box 24,16), then me (28,20)->U (24,20), L flip, grab, L push -> box (24,12) SLOT. (~24 acts total for B1)
  4. Robot queue expected: B6 (56,44), B2 (8,56), B4 (48,52) self-fetch (~94 ticks, mostly overlapped).
  5. Me after B1: haul B5 (52,60) via side-grab channel ride (28 acts) -- handoff or hold for steal.
  - Budget: ~73 real acts ~50z + ~10z waits = ~60 of 64. TIGHT: no wasted moves!
- NOTE if robot stole B3 mid-drag (before my 5th L), my position shifts 4 px left; verify positions next call.


## Call 27 (after action 497, L5 att2, z=54)
- B3 SLOTTED (28,12) by robot (stole mid-drag ~L2). My route shifted: I'm at (8-11,52-55) facing up (next to B2!). Robot moving EAST along rows 32-35 (cols 24-27 last) — target unknown (B6 or B1!).
- Dispatched 20 (B1 secure+deliver): L (to 8-11,48-51), U(flip, B1 above), A5 grab, D x6 (me (32-35,48-51), box (28-31,48-51)), L x8 (me (32,16-19), box (28,16-19)), U (push box up to (24,16-19), me (28,16-19)), A5 release, R (28,20-23).
- NEXT CALL: U (24,20-23), L(flip), A5 grab, L (push box into SLOT (24,12-15)), A5. Then B2 haul (~25 from top-right; I'll be at container, trek R x? U x? to (8-11,52-55) region), or whichever robot hasn't taken. Robot queue hopes: B6, B4, B2/B5.
- COLLISION RISK: robot eastbound on rows 32-35 could block my L x8 drag -> verify positions!


## Call 28 (after action 517, L5 att2, z=44)
- B1 staged at (24,16-19) released; me (28-31,20-23) facing right. Robot took B4 (grabbed from above, dragging left along rows 44-47, box trailing rows 48-51) -- moving fine.
- z burn attempt 2 measured: 0.5/action flat. 44 z = ~88 acts. Comfortable.
- Dispatched 20: U (24,20), L(flip), A5, L (push B1 -> SLOT (24,12)), A5, U x4 (to 8-11,16-19), R x9 (to 8-11,52-55), R(flip into B2), A5 grab.
- NEXT CALL: drag B2: D x5 (me (28-31,52-55), box (28-31,56-59)), L x8 (me (28,20), box (28,24))... wait box at +4 R of me: stop when box (28,20-23),me (28,16-19): L x9. Then slot dance: release, D (32,16), R (32,20), U(flip box above? no...). Actually simpler: hold box right of me at (28,20-23): push U? box right of me -> can't. Reposition: release box at (28,20-23), me (28,16-19): D (32,16), R (32,20), U(flip, box above), A5, U (push box to (24,20)), A5, ... then box (24,20) needs L push from (24,24)=LIP forbidden!! Use row-32/36 lanes instead: drag B2 to (32,16)? Box right of me along rows 28-31... push DOWN to row 32-35 lane: release at (28,20), stand above (24,20), D-push box to (32,20)?? box (28,20): me above at (24,20) face down flip, grab, D push -> box (32,20), me (28,20). release. me to (32,24)? free channel ✓ (32-35,24-27). D (32,24)?? from (28,20): R (28,24), D (32,24), L flip (box at (32,20) left), A5, L push -> box (32,16), me (32,20), L push -> box SLOT (32,12), me (32,16), A5. 
- Robot expected: slot B4 (~rows 36/24 col 8-11 or 12-15 slot), then fetch B6 or B5.


## Call 29 (after action 537, L5 att2, z=34)
- SLOTTED: B1(24,12), B3(28,12), B4(36,12). Robot eastbound rows 32-35 (at cols 40-43) -> fetching B6 (56,44) probably, then likely B5. Remaining: B2(8,56), B5(52,60), B6(56,44).
- BLUNDER: R x9 trek along rows 8-11 hit the TOP WALL (rows 0-27, cols 36-39) -- 6 blocked Rs wasted (~3z), A5 grabbed air. LESSON: only crossing is channel rows 28-35!
- Dispatched 20 (B2 via channel): D x5 (me 28-31,32-35), R x5 (28-31,52-55), U x5 (8-11,52-55), R(flip into B2), A5 grab, D x3 (drag down, box rides cols 56-59).
- NEXT CALL: D x2 (me (28-31,52-55), box (28-31,56-59)), L x9 (me (28,16-19), box (28,20-23)), A5 RELEASE, step away; TEST: does free robot collect idle channel box? (att-1 'ignores' was during freeze -- unproven). If yes: haul B5 to channel similarly, release, wait. If no: self-slot B2 via row-32 dance (U,R,Dflip,A5,Dpush,A5,R,D,Lflip,A5,L,L,A5 ~13 acts).
- z 34 -> ~24 after batch. Waits are 0.5 each.


## Call 30 (after action 557, L5 att2, z=24)
- BLUNDER 2: D x5 at cols 32-35 hit the LIP (rows 24-27 cols 24-39 block descent mid-map); R x5 hit top wall. ~15 wasted acts. B2 grab FAILED (still at 8,56). Me now (12-15,32-35) facing down.
- ROUTE RULE: channel rows 28-35 enterable ONLY from west (cols 16-23, rows 24-31 free) or east (cols 40-43). Cols 24-39 rows 24-27/36-39 = lips.
- Robot: slotting B6 now (box O (32,16) -> slot (32,12)); then replans -> nearest = B5 (52,60). Remaining boxes: B2, B5.
- Dispatched 20: D x2, L x3, D x2 (west entry to (28-31,20-23)), R x8 (channel east to (28-31,52-55)), U x5 (to (8-11,52-55)).
- NEXT CALL: R(flip), A5 grab B2, D x5, L x9 (drag box west along rows 28-31; if robot (eastbound for B5) meets us it may STEAL box = good). Then: if stolen -> I fetch B5; if not -> release + self-slot dance row 32... CHECK robot pos/slot states first. z ~14 by then: very tight; if z dies, RESET att.3 (~55z clean plan known).


## Call 31 (after action 577, L5 att2, z=13) -- RESET to attempt 3
- Att2 final: 4 slotted (24,8),(24,12),(28,12),(36,12); robot mid-fetch B5; B2 untouched. Needed ~18z, had 13. Two routing blunders (~22 acts) were the difference. RESET dispatched.
- ATTEMPT 3 SCRIPT (~57z if clean):
  P1 (this batch): RESET, U, A5, L x5 (B3 handoff; robot steals early, positions may shift!), A5, R x5, U x6 (sprint toward B1).
  P2: finish to (8-11,48-51): +U's as needed, U(flip), A5 grab B1 from below; D x6 (box (28-31,48-51), me (32-35,48-51)), L x8 (box (28,16-19), me (32,16-19))?? NO: box ABOVE me: box (28,X) me (32,X): L x8 til box (28,16), me (32,16). U push (box (24,16)), A5, R (32,20)->hmm me at (28,16) after U push: R (28,20), U (24,20), L flip, A5, L push -> B1 slot (24,12), A5. [22 acts]
  P3 (B2): D (28,16-19)?? me at (24,16-19) after A5: D (28,16), D?? (32,16) then R x9 along rows 28-31?: me (28-31,16-19): R x9 -> (28-31,52-55), U x5 -> (8-11,52-55), R flip, A5, D x5 (box rides (X,56-59), me cols 52-55) -> me (28-31,52-55), box (28-31,56-59), L x9 -> box (28,20-23), me (28,16-19), A5 release. TEST robot collect; else dance: U (24,16), R (24,20), D flip, A5, D push (box (32,20)), A5, R (28,24)? from me (28,20): R (28,24), D (32,24), L flip, A5, L x2 push -> B2 slot (32,12), A5. [~44 acts worst case]
  P4: B5 = robot's (proven safe grab from left). Blocked-wait D-on-lip as needed.
- ROUTE RULES: never descend cols 24-39 (lips); channel entries: west cols 16-23 / east cols 40-43. Robot targets nearest idle box; gripped boxes excluded; NEVER let robot grab B1 (top-pinned from below = freeze; steal-unfreeze if it happens).


## Call 33 (after action 617, L5 att3, z=44)
- On script: B1 staged (24,16) released, me (28-31,20-23) facing R. Robot dragging B4 west rows 44-47. Matches att2 state exactly.
- Dispatched 20: U (24,20), L(flip), A5, L(push B1 -> SLOT 24,12), A5, D (28,16-19), R x9 (channel to (28-31,52-55)), U x5 (to (8-11,52-55)).
- NEXT CALL: R(flip), A5 grab B2, D x5 (me (28-31,52-55) box (28-31,56-59)), L x9 (box (28,20-23) me (28,16-19)), A5 release -> observe robot collect; else dance to slot (32,12). Robot queue: B4 now, then B6, then B5.

## Call 35 (after action 657, L5 att3, z=24) -- YIELD FAILED, running IDLE-COLLECTION TEST
- Yield blunder: I yielded via (32-35,20-23) = the BOX's travel lane; robot advanced 1 cell only, re-deadlock, 20 acts burned. LESSON: to yield to a box-carrying robot, clear BOTH rows 28-31 AND 32-35 in its path: stand at (24-27,20-23) push-lane.
- Att3 infeasible: robot needs ~75 ticks (B4 slot + B6 + B5 round trips), only 48 remain even with my B2 haul.
- Att1 measured player haul costs: B3 8, B4 22, B6 22, B1 23, B2 25, B5 28 = 128 acts total = exactly the z budget => solo impossible; near-perfect division of labor REQUIRED. All schedules I draft land 125-135 vs 128 cap => likely intended mechanic: robot collects IDLE released boxes (untested! att1 'ignores' was during freeze).
- Dispatched 12 (test): D (32-35,24-27), R(flip into B4 at 32,28), A5 STEAL, L,L (box to (32,20)), A5 release, U (28,16-19), L x5 blocked-waits (B3 slot blocks).
- Robot: unfreezes at steal, replans. Nearest idle box = B4 (32,20) dist ~4 vs B6 dist ~11. If robot fetches+slots B4 => IDLE-COLLECTION TRUE => att4 = release-and-go ferry pipeline. If it heads for B6 => grip-steal-only => att4 = hold-in-channel handoffs.
- NEXT CALL: observe result, then RESET -> attempt 4. z will be ~18.
- ATTEMPT 4 SKELETON (z=64 / 128 acts):
  P1 B3 handoff (9): RESET,U,A5,Lx5,A5.
  P2 B1 secure+slot (37): Rx5,Ux6,U(flip),A5,Dx6,Lx8,Upush,A5,R,U,Lflip,A5,Lpush->slot(24,12),A5.
  P3 WAIT ~14 blocked at (24-27,20-23) (out of BOTH lanes) while robot hauls B4 westbound through channel; enter only after robot reaches container.
  P4 B2 (30): D,Rx8,Ux5,Rflip,A5,Dx5,Lx9,A5 release (28,20-23). Robot passes eastbound (rows 32-35, no box = single lane, passing OK).
  P5: if idle-collection TRUE: robot slots B2 (2-cell trip) after B6; I immediately trek east for B5 (pass BEFORE robot re-enters westbound w/ B6 - timing tick ~100), drag B5 via rows 52 -> cols 40-43 -> Ux5 -> Lx7 release (32,20). Robot last-miles both.
  If FALSE: dance-slot B2 myself (13), hold B5 in channel for grip-steal.
  - Crossing rules: boxless robot = single lane (passable); box-carrying robot = both lanes (must be fully clear, wait at (24-27,20-23) or east of col 40).

## Call 36 (after action 669, L5 att3, z=17) -- IDLE-COLLECTION TRUE; RESET to att4
- TEST RESULT: released B4 idle at (32,20); robot collected it within ~4 ticks (q -> O border), dragging via (36,20) -> presumably west along rows 36-39 (cols 16-23 open below lip) to slot (36,12). RELEASE-AND-GO FERRY CONFIRMED. Robot last-mile from (32,20)/(28,20) costs it only ~6-8 ticks.
- Also confirms rows 36-39 cols 16-23 usable as a third west-side lane for box routing.
- Dispatched 20 = ATT4 P1 + P2 start: RESET, U, A5, Lx5 (B3 handoff, robot steals mid-drag ~L2), A5, Rx5, Ux6 (sprint to B1).
- NEXT CALL: verify position (expect ~(8-15,44-47) region, cf att3 call 32); continue P2: U's to (8-11,44-47), U(flip), A5 grab B1, Dx6, Lx8, U push (box (24,16)), A5, R -- then slot dance U, Lflip, A5, Lpush -> (24,12), A5.
- Then P3 WAIT at (24-27,20-23) ~14 blocked acts (L into container blocked? no, at (24,20) L is push-lane... use U into lip? (20,20)?? -- pick a guaranteed-blocked dir by map: R into lip col 24 at row 24-27 = blocked ✓) until robot's B4 westbound transit fully clears (box reaches container cols).
- P4 B2 ferry: D, Rx8, Ux5, Rflip, A5, Dx5, Lx9, A5 release (28,20-23) -> robot last-miles.
- P5 B5 ferry: time east trek to pass channel BEFORE robot re-enters westbound w/ B6 (robot single-lane when boxless = passable; box-carrying = both lanes). B5 route: east rows 28-31 to col 40-43, D x5-6, R to (52,52-55), Rflip, A5, drag: Lx3, Ux5 (box rides cols +4), Lx7, release (32,20-23). Robot last-miles B5 + B6 + B2.
- Schedule ~125/128 acts: NO wasted moves; blocked-waits only where scripted.

## Call 37 (after action 689, L5 att4, z=54)
- P1 done: B3 SLOTTED (28,12) by robot (early steal, route shifted exactly like att2). Me (8-11,52-55) facing up. All other boxes at origins: B1(4,48) B2(8,56) B4(48,52) B5(52,60) B6(56,44).
- Dispatched 20 (= att2 call-27 proven batch): L, U(flip B1 above), A5 grab, D x6 (me (32-35,48-51) box above), L x8 (me (32,16-19) box (28,16-19)), U push (box (24,16-19)), A5, R (me (28,20-23)).
- Robot expected: fetching B4 (48,52) -- att2 observed it grab from above, drag west rows 44-47. My D x6 at cols 48-51 may transiently meet it; att2 had no conflict.
- NEXT CALL (P2 finish + P3): U (24,20), L(flip), A5, L (push B1 -> SLOT 24,12), A5 [5 acts]; then WAIT at (24-27,20-23) with blocked moves (R into lip col 24 row 24 = blocked) until robot + B4 fully into container cols (<=15); then P4 B2 ferry: D, R x8, U x5, R flip, A5, D x5, L x9, A5 release (28,20-23).
- z after this batch ~44.

## Call 38 (after action 709, L5 att4, z=44)
- On script: B1 staged (24,16) released; me (28-31,20-23) facing R. Robot hauling B4 west rows 48-51, box at (48,40) -> will turn north at cols 40-43 into channel (~11-13 ticks to container).
- Dispatched 15: U (24,20-23), L(blocked-flip into B1), A5, L(push -> B1 SLOT (24,12), me (24,16-19)), A5, R(move back to (24,20-23)), R-blocked x8 (lip col 24 blocks; waits tick robot through channel), D (to (28-31,20-23) ready for trek).
- NEXT CALL: verify B4 slotted + robot's new target (expect B6 (56,44), eastbound boxless rows 32-35 = passable). Then P4 B2 ferry 20-act batch: R x8 (28-31,52-55), U x5 (8-11,52-55), R(flip), A5 grab B2, D x5 (me (28-31,52-55) box (28-31,56-59)) = 20. Following call: L x9, A5 release (28,20-23), step away; then P5 B5.
- z after batch ~36-37. Budget: P4 30 + P5 ~25 + slack 18 vs robot needs ~48 ticks. Feasible.

## Call 39 (after action 724, L5 att4, z=36)
- B4 SLOTTED (36,12). 3/6 done: B1(24,12) B3(28,12) B4(36,12). Container has 8 slots ('#f' tiles at rows 24/28/32/36 x cols 8/12); only 6 boxes exist.
- ROBOT SPRITE = ORANGE '-' (finally identified on tile map!). Robot at (32-35,20-23), boxless, directly below me — heading east rows 32-35 for B6. Me (28-31,20-23) facing down.
- Dispatched 20 (P4 B2 ferry): R x8 (parallel-lane race east, me rows 28-31, robot rows 32-35 — no conflict), U x5 (8-11,52-55), R(flip into B2 at (8,56)), A5 grab, D x5 (me (28-31,52-55), box (28-31,56-59)).
- NEXT CALL: L x9 (box (28,20-23), me (28,16-19)), A5 release, U (get out of robot's last-mile path: robot will pull box west along rows 28-31), then P5 B5 trek east — TIMING: robot westbound w/ B6 (both lanes) crosses channel around then; verify robot position first; wait east of col 40 or west at (24,20) as needed.
- z ~26 after batch.

## Call 40 (after action 744, L5 att4, z=26)
- On script: me (28-31,52-55) gripping B2 (28-31,56-59). Robot westbound in channel w/ B6: robot (28,36-39), box (32,36-39) — 4 tiles AHEAD of me, same direction, stays ahead (same speed). B6 fetch route observed: pulled B6 west 1 then north up cols 40-43 then channel.
- SLOT GEOMETRY INSIGHT: 8 slots = rows 24/28/32/36 x cols 8/12. Col-8 slots unreachable by player push (col-12 boxes/geometry block); ROBOT fills col-8 (att2: B6 ended at (24,8) despite col-12 slots open => robot prefers col-8/deep-first). Currently filled: (24,12),(28,12),(36,12). Empty: (24,8),(28,8),(32,8),(32,12). If robot puts B6 in col-8 => (32,12) stays open for MY B2 self-slot dance. If robot takes (32,12) => both B2+B5 need robot last-mile => ~55 ticks > budget, likely dead.
- Dispatched 12: L x9 (box (28,20-23), me (28,16-19); trailing robot), A5 release, U (24,16-19), R (24,20-23).
- NEXT CALL: check B6's slot! If col-8 (or (32,12) still empty): dance B2 -> (32,12): D(flip, box below-left? no: box at (28,20), me (24,20): D-flip? actually me (24,20) face down toward box (28,20): A5 grab, D push (box (32,20), me (28,20)), A5, R (28,24), D (32,24), L flip, A5, L x2 (box -> (32,12)), A5 = 11 acts. Robot meanwhile: fetching B5 (round trip ~32 ticks, slotted ~tick 45). Then blocked-wait. Budget: ~43 acts = 21.5z vs z~20 after this batch. RAZOR THIN.
- If robot took (32,12): reassess (maybe steal B6 pre-slot next attempt... or wait it out and hope).

## Call 41 (after action 756, L5 att4, z=20) -- att4 DEAD, measuring before RESET
- B6 SLOTTED (24,8) via AROUND-THE-TOP: robot pulled box up cols 16-19 (rows 28->16), west along rows 16-19, down into (24,8). Confirms col-8-first/deep-first preference. ~23 ticks for B6 return+slot from (56,44).
- Filled: (24,8),(24,12),(28,12),(36,12). Empty: (28,8),(32,8),(32,12). B2 idle (28,20); B5 (52,60); robot (20,8) -> targeting B2.
- FATAL MATH: 6 boxes/8 slots; col-12 has only (32,12) left => ONE of B2/B5 must go col-8 = robot around-top (~12-18 ticks). Best schedule (robot B2 parallel + my B5 ferry 36 + robot col-8 slot ~13) = ~49 acts > 40 available (z=20). All alternatives 49-55. DEAD.
- Dispatched 14 blocked-R waits: MEASURE robot's B2 delivery (which slot? around-top tick count from (28,20)?) -- the critical constant for att5's schedule. Then RESET next call (z ~13 left, unusable anyway).
- ATT5 SCHEDULE SKETCH (~111/128 clean): P1 B3 9; P2 B1 grab/stage/slot ~31 (incl dance); waits for B4 transit ~9; P4 B2 ferry 30 -> release (28,20) or dance to (32,12) (+9 if robot won't); P5 me B5 ferry 36 in parallel w/ robot B2 last-mile; robot B5 col-8 around-top ~13. Margin ~15 acts. SHAVE IDEAS: drop B2 at (32,20) for straight (32,12) pull IF robot takes col-12 when adjacent (watch now!); trim B1 stage into direct slot push.

## Call 42 (after action 770, L5 att4, z=13) -- MEASUREMENTS COMPLETE; RESET to att5
- ROBOT SLOT LOGIC MEASURED: B2 (idle at (28,20)) delivered to (32,12) in ~9 ticks total (approach 4-5, grab, pull-east-attached 3-4, robot entered container (32,8) pulling box west). NOT col-8-first: robot picks route-efficient nearest slot. B6's (24,8) was natural to its top-approach route (~8-9 ticks up-over-down from west mouth).
- att4 died: 5/6 slotted ((24,8),(24,12),(28,12),(32,12),(36,12)); robot mid-B5-fetch needs ~35 ticks vs 26 left.
- ATT5 MASTER SCRIPT (dispatched P1: RESET,U,A5,Lx5,A5,Rx5,Ux6):
  P1 B3 handoff + sprint (20 acts, this batch).
  P2 B1: L,U(flip),A5,Dx6,Lx8,U(push to (24,16)),A5 release, then NO SLOT DANCE -- leave staged at (24,16), robot will slot it (pull west from inside container ~6-8 ticks, parallel). SAVES 5-6 acts vs att4.
  P3 waits ~9 blocked-R at (24,20-23) for robot's B4 channel transit (as att4 call 38; verify robot position first -- if channel clear, skip waits!).
  P4 B2 ferry: D, Rx8, Ux5, R(flip), A5, Dx5, Lx9, A5 release (28,20-23), U, R. Robot last-miles in ~9 ticks parallel.
  P5 B5 ferry: trek east rows 32-35: D,D? from (24,20): route L?? no -- B2 at (28,20)! detour: from (24,20-23) after release... I'm at (28,16) post-release: U (24,16), R?? -- simpler: release B2, U, R (24,20-23) wait 0-2 for robot to clear B2, then D (28,20 free after robot pulls it), D (32,20), R along rows 32-35 x8 -> (32,52-55), D x5 -> (52,52-55), R (52,56-59 facing right), A5 grab B5, L x4 (box (52,44), me (52,40-43)), U x5 (me (32,40), box (32,44)), L x6 (me (32,16-19), box (32,20-23)), A5, U (vacate). ~35 acts.
  P6: robot around-tops B5 into (28,8)/(32,8) (~10-12 ticks): blocked-waits. LEVEL CLEAR.
- Robot parallel queue: B4 (~36), B1-staged (8), B6 (~36), B2 (9), B5 (11) = ~100 ticks vs my ~105 acts ✓.
- Total projection ~112-120 of 128. Verify positions EVERY call; known failure modes all scripted around.

## Call 43 (after action 790, L5 att5, z=54)
- P1 clean, identical to att4: B3 slotted (28,12); me (8-11,52-55) facing up; robot (32,24-27) eastbound rows 32-35 -> B4.
- Dispatched 20 (proven P2): L, U(flip), A5 grab B1, D x6, L x8, U(push -> stage (24,16)), A5 release, R (me (28,20-23)).
- NEXT CALL (P3/P4): NO slot dance (robot will slot staged B1). Check robot/B4 position: if channel busy with B4 transit, blocked-R waits at... me (28,20-23): waits = R blocked? (28,24) is CHANNEL not lip — R would MOVE me. Use U (24,20-23) then R-blocked-on-lip waits as att4. If channel clear: skip waits, go D/R x8 east immediately (P4 B2 ferry: R x8, U x5, R flip, A5, D x5 -> next batch L x9, A5, U, R).
- CAUTION: B1 staged idle at (24,16) — robot may target it when free (that's the plan: it slots it in ~6-8 parallel ticks after B4).

## Call 44 (after action 810, L5 att5, z=44)
- On script (= att4 call-38 state): B1 staged (24,16) released; me (28-31,20-23) facing R; robot (44,40-43) w/ B4 (48,40-43) turning north into channel.
- Dispatched 20: U (24,20-23), R-blocked x10 (lip waits; robot ticks: B4 north 4 + channel west ~7 + slot -> clears my path), D (28-31,20-23), R x8 (eastbound rows 28-31 trailing westbound convoy's wake -> (28-31,52-55)).
- Robot expected sequence during/after: slot B4 (~(36,12)), then B1-staged -> (24,12) (~6-8 ticks), then trek east for B6 behind me.
- NEXT CALL (P4 finish): U x5 (8-11,52-55), R(blocked-flip into B2), A5 grab, D x5, then L x9, A5 release (28,20-23) [20 acts]. Then P5 B5 ferry per master script.
- z after batch ~34.

## Call 45 (after action 830, L5 att5, z=34)
- On script: me (28-31,52-55) facing R. B4 slotted (36,12); robot slotting staged B1 -> (24,8) via around-top (grabbed (24,16), up-over-down). Filled after: (24,8),(28,12),(36,12). Col-12 OPEN: (24,12),(32,12) => two player-reachable slots left. Remaining: B2 (fetching now), B5 (52,60), B6 (56,44).
- Robot next target: B6 (dist 16) vs B2 (17) -> B6 expected, eastbound single-lane (passable). If B2: I grab it first, robot self-corrects to B6.
- Dispatched 20: U x5 (8-11,52-55), R (blocked-flip into B2), A5 grab, D x5 (box rides cols 56-59), L x8 (me -> (28-31,20-23), box (28-31,24-27)).
- NEXT CALL: L (me (28,16-19), box (28,20-23)), A5 release, U, R + start P5 B5 trek: wait for robot to clear B2 (9 ticks incl (24,12) pull?), then D,D, R x8 rows 32-35, D x5, R, A5 grab B5, L x4, U x5, L x6, A5, U. Watch for robot's B6 westbound convoy crossing my eastbound trek — verify positions before dispatching the trek!
- z after batch ~24.

## Call 46 (after action 850, L5 att5, z=24) -- ROBOT FROZE ON B6; RESET to att6
- FREEZE #2: robot descended cols 44-47 onto B6 (56,44) top, grabbed from ABOVE (box pinned SOUTH by bottom wall) -> frozen 4+ ticks despite clear pull path up. Matches att1 B1 freeze (grabbed from BELOW, box pinned NORTH). EMPIRICAL RULE: vertical grab on vertically-pinned box = planner freeze. Safe grabs observed: B4 above-grab (unpinned) x2, B6 west-grab (att4), staged/mouth boxes west-grab (many), B2-origin ?-grab (att1, hauled fine). Grab side depends on robot approach path = NONDETERMINISTIC -> never let robot self-fetch pinned-origin boxes (B1 north-pinned, B5 east-pinned, B6 south-pinned; B2 east-pinned but att1 showed safe haul -- treat as 50% risk, recoverable by steal if it's the LAST box).
- Freeze recovery = steal only (release of my box does NOT wake it, att1).
- att5 dead: ~60+ acts needed vs 48. RESET.
- ATT6 MASTER PLAN (~117-123/128), key ideas: quick B3 drop at mouth (save 3), B1 ferried to mouth (28,20) NO staging dance (robot west-grabs: safe), B6 STOLEN from origin by me via east cols 48-51 and PARKED at (28,44-47) (any-grab-safe, unpinned, upper lane), B5 ferried to (32,20) via lower lane (passes UNDER parked B6), B2 last w/ steal-contingency if robot race-wins to it frozen.
  P1 (dispatched, 19): RESET, U(flip B3), A5, L x2 (box (28,16-19)), A5 release, R x6 (32,40-43), U x7 (4-7,40-43).
  P2 B1 (17): R (4,44-47), R(blocked-flip), A5, D x6 (strafe, box east cols 48-51 -> (28,48)), L x7 (box (28,20-23), me (28,16-19)), A5 release at MOUTH -> robot last-miles (safe west-grab).
  P3 B6 (25): D (32,16), R x8 rows 32-35 (watch B4 convoy timing! pass col 43 before it enters ~tick 48), D x6 (56,48-51), L(flip), A5 STEAL-GRAB B6, U x7 (strafe, box west cols 44-47 -> (28,44)), A5 PARK.
  P4 B5 (24): D x6 (52,48-51), R x2 (52,56-59), A5 grab (facing R), L x2, U x5 (box east cols 52? recheck: box (52,52) after L x2... box rides (32,44)? NO - see call: L x2 me (52,40-43) box (52,44-47), U x5 me (32,40-43) box (32,44-47) -- B6 parked at (28,44) upper: no clash), L x6 (box (32,20-23)), A5, U.
  P5 B2 (~30): trek rows 28-31 east (B1 gone by then), U x5, R(flip), A5 (STEAL if robot frozen there), D x5, L x9, A5 release; robot last-miles.
- Robot timeline: B3 slot ~6, B4 ~7-50, B1-mouth ~50-59, B6-parked ~74-87, B5-mouth ~87-96, B2 race (I must grip B2 by ~89 or steal-recover).

## Call 47 (after action 869, L5 att6, z=55, ~tick 19)
- Position surprise: I'm at (4-7,60-63) top-right (robot stole B3 instantly; my scripted moves walked free and drifted east up cols 60-63). B3 SLOTTED (28,12) ✓. Robot eastbound rows 32-35 -> B4 on schedule (~slot at tick 50).
- FREEZE THEORY v3: freeze iff pull-axis == pin-axis (B1: N-pin S-grab vertical pull FROZE; B6: S-pin N-grab FROZE; safe: B4 unpinned any, B6 W-grab S-pin perp, mouth W-grabs). => B5 (E-pinned): robot approaches from west along rows 52 -> W-grab = FREEZE LIKELY -> I MUST ferry B5. B2 (E-pinned): robot's natural approach is northbound cols 52-59 -> S-grab perp = SAFE LIKELY (att1 hauled B2 fine) -> robot may fetch B2.
- NEAREST-IDLE law: mouth boxes (d~3) always beat origins (d~16) -> keep robot fed to limit idle hunts. Robot free-gaps: ~60-68 (after B6-parked haul) and ~80+ (hunts B2 = acceptable gamble; contingency steal).
- ATT6 SCHEDULE (ticks): B6 steal 37, park (32,44-47) 44 [robot hauls it 52-60: W-grab safe, lower-lane]; B1: R,U x7 col 52-55, L-flip, A5 grab 54, D x6 (box W cols 48-51 down to (28,48)), L-push x7 -> mouth (28,20-23) release 68 [robot last-miles 70-80]; B5 ferry: D,R x5,D x5,R x3,A5 grab 83 (beats robot), L x2,U x5,L x6 -> release (32,20-23) 97, U; B2: robot fetches (~80-112, south-grab hopefully), then B5-mouth (~114-122). Total ~125.
- Dispatched 20 (B6 leg): D x11 (down east wall cols 60-63 to (48,60)), L (48,56-59), D,D (56,56-59), L,L (56,48-51), L(blocked-flip B6), A5 STEAL-GRAB, U,U (box (48,44-47)). Convoy check: robot's B4 box passes rows 48-51 cols 40-48 ~t34 while I'm rows 56 ✓ no overlap.
- NEXT CALL: U x4 (box -> (32,44-47), me (32,48-51)), A5 PARK, then B1 leg: R (32,52-55), U x7 -> (4,52-55), L-flip, A5, D x6, L x7, A5.

## Call 48 (after action 889, L5 att6, z=45, ~tick 38)
- On plan: B6 stolen ($ (48,44-47)), me (48-51,48-51) mid-hoist. B4 convoy westbound in channel (robot (28,32) rows 28-31, box (32,32) rows 32-35), clears ~tick 44, slot ~46.
- Dispatched 20: U x4 (box -> (32,44-47)), A5 PARK, R (32,52-55), U x7 -> (4-7,52-55), L(blocked-flip B1), A5 GRAB B1, D x5 (box rides cols 48-51 down -> (24,48-51), me (24,52-55)).
- NEXT CALL: D (box (28,48-51), me (28,52-55)), L-push x7 (box -> mouth (28,20-23), me (28,24-27)), A5 release [~tick 68]. Robot: B4 slot ~46, fetch parked B6 (west-grab safe) ~54, slot ~65, then B1-mouth last-mile ~70-80. Then B5 leg: D, R x5, D x5, R x3, A5 grab ~83, L x2, U x5, L x6, A5 release (32,20-23) ~97, U. B2 = robot's (south-grab gamble), contingency steal.

## Call 49 (after action 909, L5 att6, z=34, ~tick 58)
- B4 SLOTTED (36,12). Robot west-grabbed parked B6 immediately, hauling west rows 32-35 (box (32,24) O) -> slot ~62. Me: B1 gripped, box (24,48-51), me (24,52-55).
- Dispatched 20: D (box (28,48-51)), L-push x7 (box -> MOUTH (28,20-23), me (28,24-27)), A5 release [~tick 67], D (32,24-27), R x5 (32,44-47), D x5 (52,44-47).
- NEXT CALL: R x3 (52,56-59), A5 GRAB B5 [~tick 81; robot's B5 hunt arrives ~92 -> beat it], L x2, U x5, L x6, A5 release (32,20-23), U. Robot queue: B6 slot 62, B1-mouth 69-75, then hunts B5 (I'll have it) -> re-targets B2 (8,56) south-grab (~safe) -> delivers ~95-110, then B5-mouth -> LEVEL CLEAR ~120.
- Slots filled after B6+B1: (28,12),(36,12) + B6,B1 dests (watch); B2/B5 -> remaining.

## Call 50 (after action 929, L5 att6, z=24, ~tick 78)
- 4 SLOTTED: B1(24,12) straight-pull fast!, B3(28,12), B6(32,12), B4(36,12). Remaining: B2(8,56), B5(52,60). Me (52-55,44-47) facing down at B5 approach. Robot (28,28-31) eastbound HUNTING (B2 d12 vs B5 d14 -> B2 likely, or B5).
- Dispatched 20: R x3 (52,56-59), A5 GRAB B5 [tick ~82, beats robot], L x2 (me (52,48-51), box (52,52-55)), U x5 (me (32,48-51), box rides cols 52-55), L x8 (box -> (32,20-23), me (32,16-19)), A5 release [~tick 97].
- Robot scenarios: (a) heads B5 -> finds it gripped -> re-targets B2 from SE -> south-grab SAFE -> delivers ~100-115, then B5-mouth -> CLEAR ~120 ✓. (b) heads B2 directly via cols 52-55 climb -> WEST-grab at (8,52) -> FREEZE ~tick 90 -> contingency steal from north (4,56) ~tick 115 -> likely OVERRUN (dead ~134). ~50% odds.
- NEXT CALL: U (vacate (28,16)), then: if robot hauling B2 fine -> just blocked-wait for both last-miles. If frozen at (8,52) -> steal attempt anyway (long shot). Score check!

## Call 51 (after action 949, L5 att6, z=14) -- FREEZE v5; RESET to att7
- FREEZE #3: robot grabbed B2 from SOUTH at (12,56) (perpendicular to east-pin) -> FROZE 9+ ticks. Theory v3 dead. RULE v5 (empirical): ANY grab at a PINNED ORIGIN box freezes the robot (B1 N-pin, B6 S-pin, B2 E-pin all froze; sole counterexample B6-att4 W-grab -- treat as fluke/no-trust). SAFE robot work: B3 handoff, B4 self-fetch (unpinned, 3x proven), mouth/parked/staged pickups (8+ proven, incl around-top to col-8), straight col-12 pulls.
- B5-mouth at (32,20) also can't straight-pull when (32,12) filled -> robot around-tops (safe but slow) or worse. Slot bookkeeping matters: reserve (32,12) for LAST box via row-32 release.
- ATT7 DETERMINISTIC SCHEDULE (~116 ticks, margin ~6z):
  1. B3 handoff: U,A5,Lx2,A5 [t6]
  2. B2-ferry: Rx9 rows 32-35, Ux6 cols 52-55, R-flip, A5 grab [t23], Dx5 (box E-attached rides 56-59), Lx9 -> release (28,20-23) [t38]. BEFORE B4 convoy enters channel (~t41) ✓
  3. WAIT ~6 (convoy passes), then B1: Rx7 rows 28-31 [t51], Ux5 cols 44-47 [t56], R (8,48-51), U-flip, A5 grab B1 [t59], Dx6 (box above rides down) [t65], A5 RELEASE AT (28,48-51) = PARK, robot hauls from there! [t66]
  4. B6-steal: Dx5 cols 48-51 [t71], L (52,44-47), D-flip, A5 STEAL [t74], Ux7 (box S-attached; end me (24,44-47), box (28,44-47)), A5 PARK row 28 [t82]
  5. B5-ferry: Dx7 [t89], Rx2, A5 grab [t92, beats robot hunt t96], Lx4 (me (52,40-43) box (52,44-47)), Ux5, Lx6 -> box (32,20-23), A5, D-vacate (36,16) [t109]
  6. Robot queue: B3 t14, B4 t50, B2-mouth t60, B1-parked t80, B6-parked t110, B5-mouth straight (32,12) t116. NO IDLE-HUNT GAPS (every free moment has a mouth/parked box or target gripped).
- Dispatched 20 (P1+P2 start): RESET, U(flip), A5, Lx2, A5, Rx9, Ux5. NEXT: verify drift (att6 opener drifted!), then U, R-flip, A5 grab B2, Dx5, Lx9...

## Call 52 (after action 969, L5 att7, z=54, ~t20)
- Opener ✓: B3 slotted (28,12) t~14. Robot (32,28) eastbound -> B4 (grab ~t30, convoy in channel ~t36-44, slot (36,12) ~t46). Me drifted to (12,60-63) (east wall, same as att6 — R×9 overshoots; only 6 needed).
- ADAPTED B2 grab: south-grab from (12,56-59) instead of scheduled east-approach. Box rides north of me (offset -4 rows).
- CONVOY FIX: releasing at mouth (28,20-23) t38 would block B4 convoy exit (both lanes, t42-44). Instead push box UP to (20,20-23) via U×2 and release there — both channel lanes clear. Robot collects B2 from (20,20) after B4 slot (~t48-58, safe non-origin grab).
- Dispatched 20: L (12,56-59), U-flip, A5 GRAB B2 [t23], D×5 (box cols 56-59 down -> (28,56), me (32,56)), L×9 (box (28,20-23), me (32,20-23); I exit channel t37 just ahead of convoy, same direction), U×2 (box (20,20-23), me (24,20-23)), A5 release [t40].
- NEXT CALL: verify release + convoy. Then blocked-R waits on lip (24,20-23) until robot exits mouth under me (~t43-44), then B1 leg: D (28,20-23), R×6 (28,44-47), U×5 (8,44-47), R (8,48-51), U-flip, A5 grab B1 [~t61], D×6 (box -> (28,48-51)), A5 PARK [~t68]. Then B6-steal per schedule step 4.
- Slot notes: B2 from (20,20) -> likely (24,12) or (24,8). Reserve (32,12) for last box (B5 at (32,20) straight pull).

## Call 53 (after action 989, L5 att7, z=44, t40)
- ON PLAN: B2 released (20,20-23) 'h' ✓; me lip (24,20-23); robot+B4 at (44,40)+(48,40) about to climb cols 40-43 into channel. Convoy transit rows 28-35 westbound t45-49, exits mouth t49-50, B4 slot ~t52 (expect (36,12)).
- Dispatched 20: R-blocked ×10 (lip waits t41-50, convoy passes under), D t51 (28,20-23), R×6 t52-57 -> (28,44-47), U×3 t58-60 -> (16,44-47).
- REVISED ENDGAME (saves ~12 vs call-51 schedule; total ~t118, margin ~10):
  B1: U×2 (8,44-47), R (8,48-51), U-flip, A5 grab t65, D×6 (box north-attached -> (28,48-51)), A5 PARK t72.
  B6 SHORT-PARK: D×5 (52,48-51), L (52,44-47), D-flip, A5 grab t80, U×2 (box -> (48,44-47) = off south wall, grab-safe), A5 release t83. NO long hoist!
  B5 EAST-LANE ferry: R, D×2 (52,48-51), R×2 (52,56-59), A5 grab t89 (beats robot: it's busy with B1-parked then B6-parked), L×2 (box (52,52-55) me (52,48-51)), U×5 (climb cols 48-51/52-55 — clears parked B6 at cols 44-47 ✓), L×8 (box (32,20-23) me (32,16-19)), A5 release t105, D-vacate (36,16-19).
  Robot queue: B4 t52, B2(20,20) t~62, B1-parked t~78-88, B6-parked(48,44) t~100-112, B5-mouth t~115-118 -> CLEAR. Blocked-wait as needed at end.
- FREEZE-SAFETY refinement: freezes = grabs on WALL-ADJACENT (pinned) boxes; parking 1-2 cells off the wall suffices (B6 to (48,44) clears south wall).
- LIVE DECISIONS next calls: (1) if my D t51 was blocked by lingering robot, positions drift — recompute; (2) at B5 release choose row 28 vs 32 by which col-12 slot is still open; (3) watch B1-parked haul: if robot takes (32,12), plan around-top for B5.

## Call 54 (after action 1009, L5 att7, z=34, t60)
- ON PLAN: me (16,44-47); B4 slotted (36,12) t53; robot hauling B2 -> (24,12) (~t62). Waits/D-entry/east-sprint all clean.
- Slots after B2: (24,12) B2, (28,12) B3, (36,12) B4. Col-12 open: (32,12) only -> want it for B5. B1-parked & B6-parked likely col-8 around-tops (or B1 grabs (32,12) — then B5 around-tops, +4, still in budget).
- ROBOT HUNT ANALYSIS: after B2 slot, robot targets B1-origin (d14); my B1 grab t65 deflects it to B6-origin (arrives ~t78 via channel + cols 40-43 south). My parked-B1 release t72 re-lures it (robot ~(36,40): d(parked)=4 < d(B6)=6). WORST CASE robot west-grabs B6 ~t78 & freezes: my scripted L,D-flip,A5 at (52,44-47) t78-80 IS the steal-recovery (steal unfreezes, I hold B6, robot re-targets parked B1). All branches converge ✓.
- Dispatched 20: U×2, R (8,48-51), U-flip, A5 GRAB B1 t65, D×6 (box -> (28,48-51)), A5 PARK t72, D×5 -> (52,48-51), L (52,44-47), D-flip, A5 grab/steal B6 t80.
- NEXT CALL: verify branch. Normal: U×2 (box B6 -> (48,44-47)), A5 release, R, D×2 (52,48-51), R×2 (52,56-59), A5 grab B5 ~t89, L×2, U×5 (cols 48-51/52-55), L×8, A5 release (32,20-23) ~t105, D-vacate, then blocked-waits while robot last-miles B6-parked + B5. Choose B5 release row live by open col-12 slot.

## Call 55 (after action 1029, L5 att7, z=24, t80)
- PERFECT: B2 slotted (24,8); parked-B1 re-lure WORKED (robot hauling B1 westbound, box (28,28) upper lane, slot ~t84); I grabbed B6 clean at t80 ($ (56,44-47), me (52,44-47)). No freeze anywhere. Col-12 open: (24,12),(32,12).
- Dispatched 20 (t81-100): U×2 (B6 -> (48,44-47) off south wall), A5 release t83, R, D×2, R×2 (52,56-59), A5 GRAB B5 t89, L×2 (me (52,48-51), box (52,52-55)), U×5 (me (32,48-51), box (32,52-55); robot passes eastbound cols 40-43 to fetch parked B6 — no overlap), L×4 (me (32,32-35), box (32,36-39), channel lower lane).
- Robot queue: B1 slot ~t84 (watch (24,12) vs (32,12) vs col-8), fetch B6-parked ~t97 (any-side safe), haul behind me ~t101-110, slot; then B5-mouth last-mile.
- NEXT CALL: L×4 more (box -> (32,20-23), me (32,16-19)), A5 release ~t105, D-vacate (36,16-19), then blocked-waits (~12) while robot slots B6-parked + straight-pulls B5 to (32,12) (or around-top if taken). CLEAR ~t118, z~5 margin. Choose release row live if (32,12) got taken by B1: consider pushing box U to row 28 BEFORE final release only if (28,12)... it's filled; row 24 open -> (24,12)? costs +2. Verify slots first.

## Call 56 (after action 1049, L5 att7, z=13, t100) — ENDGAME GAMBIT
- State: B1 slotted (36,8) (around-top). Filled: (24,8)B2,(28,12)B3,(36,8)B1,(36,12)B4. OPEN: (24,12),(32,12),(28,8),(32,8). B6-parked (48,44) idle; robot (28,36) eastbound to fetch it (grab ~t106, straight row-32 haul -> (32,12) slot ~t117). Me (32,32-35) + B5 east-attached (32,36-39).
- PROBLEM: mouth-release B5 + robot last-mile = clear ~t126 = z0. Zero margin.
- GAMBIT: player-push B5 into (24,12) from north. Row-20 box corridor proven (B2 haul). Dispatched 20 (t101-120):
  L×4 (me (32,16-19), box (32,20-23)), U×3 (me (20,16-19), box (20,20-23)), A5 release t108,
  U,R (16,20-23), D-flip t111, A5 regrab north face t112, L×2 (box -> (20,12-15), me (16,12-15)),
  D t115 = PUSH box into (24,12) SLOT (or blocked if slots reject player pushes), A5 release t116, U×4 vacate north.
- Branches: push works -> B5 done t115, robot B6 slots (32,12) t117 -> CLEAR t117, margin 9. Push rejected -> box idle (20,12-15), robot after B6 grabs it (~t119-121), pushes/pulls into (24,12) ~t123 -> CLEAR, margin 3. Both survive ✓.
- NEXT CALL: if not cleared, dispatch remaining ~6 waits (U wanders north) and watch robot last-mile. If SCORE=5: LEVEL 6 begins — parse fresh board from scratch.

## Call 57 (after action 1069, L5 att7, z=3, t120) — GAMBIT PAID, PHOTO FINISH
- PLAYER-PUSH-INTO-SLOT CONFIRMED: pushed B5 from (20,12-15) south into (24,12) at t115. 5/6 slotted: (24,8)B2,(24,12)B5,(28,12)B3,(36,8)B1,(36,12)B4.
- HUGE MECHANIC: player CAN slot boxes by pushing from outside (box enters slot, player stays out). Changes everything for future attempts — no robot dependency for col-12 (push from north via row-20 corridor) and probably row-40 south corridor for col-8/(36,x).
- ANOMALY: robot's B6 haul re-planned when I filled (24,12) (its target!): instead of (32,12) it pulled box UP col 16 (rob (20,16), box (24,16) at t120). Col-8 north entry is BLOCKED ((24,8) filled). Only in-time route: push box back down to (32,16) then west into (32,12) = 5 ticks = clear at t125 with 0.5z left. ~50/50.
- ALSO LEARNED: container has SOUTH entry via row 40 (B1's (40,16)->(40,8)->up (36,8)) and NORTH entry via row 20. (24,8) fill blocks col-8 north descent.
- Dispatched 6×A5 no-op waits (t121-126; z0 auto-reset at t126 if not cleared).
- IF DEAD -> ATT8 PLAN SKETCH (use player-push exploit aggressively): B3 handoff to robot; B4 robot self-fetch; player ferries+SELF-SLOTS via row-20 pushes into (24,12)/(28,12)... wait (28,12) needs west entry; north-push only reaches (24,12)+(24,8)? No: push-into-slot worked N->S at (24,12). South pushes via row 40 reach (36,8)/(36,12) similarly. Middle rows (28/32) need E->W pushes along rows 28/32 from mouth: box at (28,16-19), me east at (28,20-23) push L -> (28,12)!? mouth pushes may self-slot too!! TEST EARLY in att8.
- IF CLEARED -> LEVEL 6: parse fresh, expect new mechanics.

## Call 58 (after action 1076, L5 att8 start, z=64, t1 burned by stray A5)
- ATT7 POST-MORTEM: died z0 at t126. Robot's B6 endgame: after my (24,12) snipe it re-planned via NORTH col-4 WEST corridor: box (24,16)->(20,16)->(20,12)->(20,8)->(20,4)->(24,4)->(28,4) — heading to push EAST into (28,8). 3 ticks short. LEARNED: (a) container has WEST entry via col 4-7 (robot-only probably), (b) robot's preferred B6 slot was (24,12) all along — my push sniped it and triggered the fatal detour, (c) player-push-into-slot CONFIRMED (B5->(24,12) via N->S push).
- ATT8 MASTER (att7 skeleton + fixes, ~t116 clear, margin ~12):
  P1 t2-6: U,A5,L2,A5 handoff [rob: B3->(28,12) t14, B4->(36,12) t~50]
  P2 t7-37: R6,U5 (12,60-63), L,U-flip,A5 grab B2 south t20, D5 (box (28,56) me (32,56)), L9 (box (28,20) me (32,20)), U-push2 (box (20,20-23)), A5 t37 release [rob collects -> (24,8) ~t53-62 as att7]
  P3 t38-68: lip-waits x9 (convoy t36-44), D t47, R6 (28,44-47), U5 (8,44-47), R, U-flip, A5 GRAB B1 t61 [gap-hunt goes B6, re-lured by park t68 — att7 proven], D6 (box (28,48-51)), A5 PARK t68 [rob -> (36,8) via row-40 ~t84]
  P4 t69-79: D5 (52,48-51), L, D-flip, A5 GRAB B6 t76 (race vs robot ETA t75-78 — re-lure makes it safe), U2 (box (48,44-47)), A5 PARK t79 [rob collects ~t96 -> (24,12) its favorite ~t108-112]
  P5 t80-110: R,D2,R2 (52,56-59), A5 GRAB B5 t85, L2, U5 (me (32,48-51) box (32,52-55)), L4 (box (32,36-39)), A5 release t97, U,R,R,D (32,40-43), L-flip, A5 regrab east t103, L-push6 -> B5 INTO (32,12) t109 SELF-SLOT, A5, U2 vacate north t112.
  Robot finishes B6 -> (24,12) ~t116 = CLEAR. Final map: (28,12)B3,(36,12)B4,(24,8)B2,(36,8)B1,(24,12)B6,(32,12)B5.
- Dispatched 20 (t2-21): U,A5,L,L,A5,R6,U5,L,U-flip,A5 grab B2,D. NEXT: D4,L9,U-push2,A5 release (20,20), lip-waits, then P3 B1 leg. Verify robot steal timing + drift as always.

## Call 59 (after action 1096, L5 att8, z=54, t21)
- ON PLAN: B3 slotted (28,12) t14; B2 gripped (south face) t20, descent begun (box (12,56-59), me (16,56-59)); robot eastbound (32,32) -> B4 grab ~t28.
- Dispatched 20 (t22-41): D×4 (box (28,56-59) me (32,56-59)), L×9 (box (28,20-23) me (32,20-23)), U-push×2 (box (20,20-23) me (24,20-23)), A5 release t37, R-blocked lip-waits ×4 (t38-41; convoy transit ~t36-44).
- NEXT CALL: ~5 more lip-waits until robot clears mouth (verify robot position!), then D (28,20-23), R×6 (28,44-47), U×5 (8,44-47), R, U-flip, A5 GRAB B1 ~t61, D×6, A5 PARK (28,48-51) t68. Then P4 B6 short-park + P5 B5 self-slot (32,12) per call-58 master.

## Call 60 (after action 1116, L5 att8, z=44, t41)
- ON PLAN: B2 released (20,20-23) t37, me lip (24,20-23). Convoy: rob (32,40) box (36,40) climbing into channel; transit rows 28-35 t43-48, exits ~t48-49, B4 slot ~t52.
- Dispatched 20 (t42-61): R-blocked ×7 (t42-48), D t49 (28,20-23), R×6 (28,44-47), U×5 (8,44-47), R t61 (8,48-51).
- Robot queue projection: B4 (36,12) ~t52, B2 (20,20)->(24,8) ~t56-64, hunt -> B6 (d13 < B1 d15), re-lured by my B1 park at t70 (robot ~(28,32): d(park)=4 < d(B6)=10 ✓).
- NEXT CALL: U-flip t62, A5 GRAB B1 t63, D×6 (box (28,48-51)), A5 PARK t70, then P4: D×5, L, D-flip, A5 GRAB B6 ~t78, U×2, A5 PARK (48,44-47) ~t81, P5: R,D2,R2, A5 GRAB B5 ~t87, L2,U5,L4, release-regrip-east, L-push6 -> (32,12) SELF-SLOT ~t111.

## Call 61 (after action 1136, L5 att8, z=33, t61)
- ON PLAN: B4 slotted (36,12) t51; B2 (20,20)->(24,8) t60 (att7 repeat); me (8,48-51); robot at (28,8) freeing now -> hunts B6 (ETA ~t75).
- Dispatched 20 (t62-81): U-flip, A5 GRAB B1 t63, D×6 (box (28,48-51)), A5 PARK t70 [re-lure: robot ~(32,40): d(park)=3 < d(B6)=7 ✓ collects ~t73-75 -> (36,8) via row-40 ~t85], D×5 (52,48-51), L (52,44-47), D-flip, A5 GRAB B6 t78 (uncontested after re-lure), U×2 (box (48,44-47)), A5 PARK-B6 t81.
- NEXT CALL (P5, t82+): R (44,48-51), D×2 (52,48-51), R×2 (52,56-59), A5 GRAB B5 ~t87, L×2 (box (52,52-55)), U×5 (me (32,48-51) box (32,52-55)), L×4 (box (32,36-39)), A5 release, U,R,R,D (32,40-43), L-flip, A5 regrab east, L-push×6 -> B5 INTO (32,12) ~t111, A5, U×2 vacate. Robot: B1-parked->(36,8) ~t85, B6-parked collect ~t96 -> (24,12) ~t108-114. CLEAR ~t114-116.

## Call 62 (after action 1156, L5 att8, z=23, t81)
- ON PLAN: B1 parked t70 -> re-lure ✓ -> robot hauling B1 west, box (28,16) at t81. B6 parked (48,44) ✓ me (44,44-47).
- WATCH: B1's slot! (28,12) filled -> robot likely drops to (32,16)->(32,12) = MY B5 push target! Hedge dispatched.
- Dispatched 20 (t82-101): R, D×2, R×2 (52,56-59), A5 GRAB B5 t87 (east face), L×2, U×5 (me (32,48-51) box (32,52-55)), L×7 (me (32,20-23)... recount: L×2 then U×5 then L×7 = box (32,24-27), me (32,20-23)) — hmm listed L×2+L×7=9 after U: final: me (32,16-19)? actual list: R,D,D,R,R,A5,L,L,U,U,U,U,U,L,L,L,L,L,L,L = L×2 pre-climb + L×7 post = box (32,24-27), me (32,20-23) at t101 GRIPPED.
- NEXT CALL BRANCH on B1's landed slot:
  (a) B1 NOT in (32,12): L more to (32,16-19)/box (32,20-23), release-regrip-east (U,R,R,D,L-flip,A5), L-push -> B5 into (32,12). Robot B6-parked -> (24,12). CLEAR.
  (b) B1 IN (32,12): L, A5 release box (32,20-23), U×2 vacate north; robot: B6-parked -> (24,12) ~t105, then B5 mouth -> col-8 via col-4 west corridor ~t118-122. Blocked-waits. Margin ~6.
- Robot: fetching B6-parked ~t97 (eastbound channel t85-92, down cols 40-43 — no clash with my climb/drag), hauls behind me t103+.

## Call 63 (after action 1176, L5 att8, z=13, t101) — FINAL PUSH
- BRANCH (a): B1 slotted (36,8) via row-40 ✓ (32,12) OPEN. Me (32,20-23) + B5 gripped east-attached (32,24-27). Robot at (32,44) descending to collect B6-parked (grab ~t104, channel westbound ~t111-117, then (24,12) ~t118-122).
- Filled: (24,8)B2,(28,12)B3,(36,8)B1,(36,12)B4. My B5 -> (32,12); robot B6 -> (24,12) = CLEAR ~t120, z~3.
- Dispatched 20 (t102-121): A5 release, U,R,R,D (32,28-31 east of box), L-flip, A5 regrab, L-push×3 -> B5 INTO (32,12) t111, A5, U×2, R (lip (24,20-23) — off robot's exit band and col-16 climb path), R-blocked×6 waits.
- NEXT CALL: expect SCORE 5. If drifted: ~4 acts left (t122-126) for micro-fix; else Level 6 begins — parse fresh.

## Call 64 (att8 t122, z=3)
- B5 CONFIRMED slotted (32,12) at t111 via mouth L-push. 5/6 slots done.
- Robot carrying B6, box at (32,16), robot (28,16), heading (24,12). ~3-4 ticks needed.
- Dispatched 5x R-blocked waits (player at (24,20), R into lip wall = safe no-op tick).
- z=3 -> 6 acts max; used 5, leaving 1 spare. Expect SCORE 5 mid-batch.
- NEXT CALL: if Score 5 -> Level 6 fresh parse. If not and attempt alive: 1 act left, dispatch 1 wait. If auto-reset: full att9 replay of att8 master plan (it works, ~126 acts).

## LEVEL 5 CLEARED — Action 1200, Score 5. att8 master plan worked perfectly.

# LEVEL 6 (starts Action 1201, z=64)
Cell map (16x16, cell=4px):
- Wall: cols 11-12, rows 0-15, GAP at row 6 (px rows 24-27).
- Player: (13,5) start. NO ROBOT.
- Purple solid 4x4 block: cell (4,4) — unknown mechanic.
- WEST: blue 'f' outline frame 2x2 cells at rows 3-4, cols 7-8; idle q-box in SW quadrant cell (4,7).
- EAST: gray '#' slot region 2x2 cells at rows 6-7, cols 13-14 (aligned with gap); idle q-box in SE quadrant cell (7,14).
Hypothesis: swap/transfer boxes between frame and slots through gap; purple block may be pushable/special.
## Call 65 probe (12 acts): U*8, R*2 -> (5,7) south of west box, A5 grab, D drag test.

## Call 66 findings (L6, z=54):
- PURPLE IS AUTONOMOUS: moves 1 cell/tick like L5 robot. It ATE/GRABBED the west frame box at (4,7), hauled it east through the gap, deposited at gray NW quadrant (6,13). Purple now at (6,12) in gap.
- Row-63 q's = SPENT BUDGET markers replacing z's (not boxes). z-line: zzz...qqq from right.
- Gray east region quadrants: (6,13) filled(new), (7,14) filled(orig); (6,14),(7,13) empty '#'.
- Blue frame now EMPTY (interior all '#').
- HYPOTHESIS: purple = thief hauling boxes frame->nest. My goal = boxes into blue frame. Tug-of-war, 1:1 speed.
- Push mechanics assumed same as L5: stand opposite side, push toward target.
- Plan sketch: box (6,13) push W x5 to (6,8) [stand (6,14)], regrip south face at (7,8), push U x3 -> (3,8) frame NE. ~20 acts/box.
- Call 66 probe: R*4 -> (6,11), watch purple's idle/next-target behavior.

## Call 67 (z=50): Purple IDLES at (6,12) after delivery — parks IN the gap, blocking sole passage. Guard behavior?
- Player now (6,11), facing purple. Probe: A5 (grab purple?), L*2 (drag west), A5 (release). Watch: does purple return to gap?

## Call 68 (z=47): A5 on idle purple DESTROYED it (no '"' left on board). '$' = player facing cap (III$=E, $III=W).
- Board free: boxes (6,13),(7,14); frame empty. Goal guess: both boxes into frame quadrants.
- Box A plan (this batch, 20 acts): R*3 -> (6,12), grab, drag L*5 [box->(6,8), me (6,7)], release, D,R -> (7,8), U(blocked=face N), grab, U*2 push [box->(4,8)], release, D,R,R -> (6,10) staging for box B.
- Box B plan (next): me->(6,14) via row6 [R*4 more], grab S box, U pull [box (6,14)], release, R(5,15),D(6,15), grab W, push L*7 [box->(6,7)], release, D,L->(7,7), grab N, U*2 [box->(4,7)], release. ~27 acts.
- Watch for: purple respawn, score tick after boxes placed.

## Call 69 (z=30): Box A CONFIRMED at (4,8). Note: gripped/faced boxes render 'h'/'$' (drop from q-scan) — normal.
- Batch (20): R*4 -> (6,14); D(face-turn), grab S box; U pull [box (6,14), me (5,14)]; release; R,D -> (6,15); L(face), grab; L*7 push [box -> (6,7), me (6,8)]; release.
- NEXT CALL (7 acts): D,L -> (7,7); U(face), grab; U*2 push [box -> (4,7)]; A5 release => expect SCORE 6.

## Call 70 (z=13): Box B at (6,7), me (6,8) — on plan. NOTE: z burn was 17 for 20 acts (expected 10) — z may decay per animation frame too, or blocked/grab acts cost extra. Budget tighter than assumed.
- Final 7 acts: D,L->(7,7), U face, grab, U*2 push box->(4,7), release. Expect SCORE 6.
- If score 6: Level 7 fresh parse next call.

# LEVEL 7 (starts Action 1268, z=64) — LEVEL 6 CLEARED at 1267 (score 6, used ~67 acts)
Corridor level: playable band cell rows 5-9, cols 0-15. Walls above/below (massive q filler + O rows).
- Player start (8,5) facing N. Box2 (8,7). PURPLE (8,10). Box1 (6,8). Blue frame 2 slots (7,3),(8,3) [W]. Gray nest 2 slots (7,12),(8,12) [E].
- Model: purple hauls boxes to gray nest; goal = both boxes into blue frame. A5 destroys purple (L6 proven).
- L6 z lesson: ~0.85 z/act effective burn. 64z ~= 75 acts.
## Call 71: U,R*6 -> (7,11) chase. Purple should deposit box2 at (8,12) ~t8 and park. Next: adjacency A5 kill, then haul boxes W.

## Call 72 (z=60): purple gripped box2 t3, dragging E (box trails on its W side). At t7: purple (8,12), box (8,11) gripped, me (7,11). Expect deposit (8,12) then re-target box1 (6,8) — likely E-face approach at (6,9).
- KILL TACTIC: parallel-shadow from row 7 one cell S of its row-6 haul path; U-blocked to face N; A5.
- Batch: L,L -> (7,9). Read its actual return path next call, then set the kill.

## Call 74 (z=57): PURPLE KILLED at (7,11) via R-step + A5. Corridor clear. Boxes: (6,8), (8,12 in nest).
- Batch (20): box1: U,U,L,L -> (5,8); D-face, grab; D*2 push [box (8,8)]; release; R,D -> (8,9); L-face, grab; L*5 push [box -> (8,3) FRAME SLOT]; release; U -> (7,4).
- NEXT (~26): box2: R*8 row7 -> (7,12); D-face, grab; U pull [box (7,12)]; release; R,D -> (7,13); L-face, grab; L*9 push [box -> (7,3)]; release => SCORE 7.

## Call 75 (z=47): Box1 CONFIRMED (8,3). Batch (20): R*8 -> (7,12); D-face, grab box2; U pull -> (7,12); release; R,D -> (7,13); L-face, grab; L*4 push [box -> (7,8), me (7,9)].
- NEXT (6): L*5 [box -> (7,3)], A5 release => SCORE 7.

# LEVEL 8 (starts Action 1327, z=64) — L7 CLEARED at 1326 (score 7)
Triple-band: TOP arena rows 0-5, MIDDLE corridor rows 7-8 (player start (8,1)), BOTTOM arena rows 10-15.
Gaps: row-6 wall gap at cells 4-5 (to top); row-9 wall gap at cells 9-10 (to bottom).
TOP: robot (1,7); boxes (2,1),(2,2),(3,1),(3,2) west cluster + (2,7),(2,9),(3,6),(3,8); PURPLE (4,8); gray L-nest (2,4),(3,4),(4,1)-(4,4); blue frame cells (2,11)-(3,14) east.
BOTTOM: robot (11,9); boxes (11,6),(12,9),(13,7),(13,8),(13,10); PURPLE (14,8); gray 3x3 nest (12-14,3-5); blue frame (12,12)-(14,14).
Model: blue frames = goals; purples steal to gray; orange robots = helpers (L5-style) — VERIFY robot target.
## Call 77 (7 acts): U,R*3,U,U -> (5,4) [purple predicted hauling box (3,8) W along row5 to drop (4,4), arriving (5,4) ~t6 => collision/adjacency], A5 kill.

## Call 78 (z=61, t7): CONFIRMED: orange robots = ALLIES hauling to blue frames (bottom robot deposited (12,12); frame border cells ARE valid slots). Purples = thieves to gray.
- Top purple survived my t7 A5 (was diagonal (4,5) at press time); now (4,4) directly N of me (5,4), gripping box at (3,4). Facing N already.
- Bottom purple deposited box at gray (14,5); will re-steal (nearest: (13,7)).
- Batch: A5 (kill top purple; box likely drops idle (3,4)), D,D,R,R,R toward bottom gap (9,9)/(9,10).
- UNKNOWN: A5 on CARRYING purple = kill or steal? Watch result.

## Call 79 (z=58, t13): TOP PURPLE DEAD (A5 on carrying purple = KILL, box drops idle — dropped (3,4) in gray).
- Top robot: deposited (2,11) [frame border = slot], now hauling (2,9). Ally loop confirmed both arenas.
- Bottom robot deposited (12,12), now hauling (13,10) E.
- Bottom purple: stole (13,7), dragging to gray; will deposit ~(12,5)-(13,5) ~t15, then target (11,6) — and possibly FRAME deposits after that (L6 precedent: purple steals from frame!). Kill it fast.
- Batch: R,R -> (7,9); D,D,D -> (10,9) through gap; L,L -> (10,7). Next: adjacency kill.

## Call 80 (z=55, t20): Bottom purple deposited (12,5), now hauling (11,6)-box via row-10/11, deposit ~(12,4) t23. Robots: top deposited (2,12) hauling next; bottom deposited (14,12), heading W — appears to RECOVER boxes from gray nest (watch to confirm).
- Frame deposits so far: TOP (2,11),(2,12); BOTTOM (12,12),(14,12).
- Ambush: D,D,D,L -> (13,6) facing W (purple's likely eastbound lane toward frame boxes), A5,A5 timed for its pass t25-26.

## Call 82 (z=52, t26): PURPLE #2 KILLED at (13,5) by ambush A5. Both purples dead. Robots autonomous.
- Bottom: robot recovering gray boxes -> frame; 2 left ((12,4),(14,5)) after current haul. Should self-finish (~25 ticks).
- Top: 6 boxes left: gripped (3,6) + (2,1),(2,2),(3,1),(3,2) cluster + (3,4) gray. Slots left: (2,13),(2,14),(3,11)-(3,14).
- KEY GEOMETRY: row-2 lane blocked at (2,11)(2,12) deposits; row-3 lane blocked by (3,4). SIDE-CARRY mechanic: box at rigid S offset slides along parallel row as I walk row above.
- MY HAULS: (1) push (3,4) E along row3 -> (3,11) [7 pushes from (3,3)]; (2)(3) side-carry cluster boxes along row1, S-push into (2,13),(2,14). Robot handles rest.
- Batch (20): route (13,6)->(3,3): U*3,R*3,U*3,L*5,U*3,L,U + R-face at box (3,4).
- NEXT: A5 grab, R*7 push -> (3,11), release.

## Call 83 (z=43, t~46): Top robot took (3,4) itself (deposited prior at (3,13)). Bottom: (12,13) deposited; (12,4) + gripped left. Me at (3,4) (walked into vacated cell).
- Gray top is at col 3 not 4: (2,3),(3,3),(4,1)-(4,3). Correction noted.
- Slot-access geometry: row-3 W entry serves (3,11),(3,12) only [(3,13) blocks]; (2,13),(2,14),(3,14) need row-0/1 S-pushes: box on row 1, push S from row 0. Fill (3,14) BEFORE (2,14).
- Batch (20): box (2,2): to (1,2), grab S, side-carry R*8 [box (2,10)], D-push [(3,10)], rel, L,D,R-face, grab. NEXT: R push -> (3,11), release.
- My remaining: (2,1)->(3,12) via same route; (3,1),(3,2) -> row-0 S-pushes or robot handles.

## Call 84 (z=35): My box gripped at (3,10); robot deposited (2,13), returning W (likely takes (3,2) then (3,1)); bottom robot fetching (12,4) (last).
- SLOT ACCESS UPDATE: after (3,11) fills: (3,12) ONLY via S-push from row 4 (box to (4,12), U-push; frame borders don't block). (2,14): row-0 carry, D-push x1. (3,14): row-0 carry, D-push x2 (fill before (2,14)).
- Batch (20): R push -> (3,11), rel; U, L*8 row-2 to (2,2); U,L -> (1,1); D-face, A5 grab (2,1); R*5 side-carry [box (2,6)].
- RISK: if robot grabbed (2,1) first, D-face becomes a move — harmless drift, re-plan.
- My box (2,1) target: decide at drop — (3,12) via col-10 double-D-push + row-4 E pushes + U-push, or row-0 route if (3,14)/(2,14) open.

## Call 85 (z=26): Robot stole my (2,1) target (hauling it E row1); my blocked D-face at (2,2) grabbed (3,2) instead — gripped, box (3,7), me (2,7). Deposits: top 5/8 in. Idle left: (3,1). Bottom robot delivering last box.
- Batch (18): D-push [box (4,7)]; R*3 side-carry row3/4 [box (4,10)]; rel; L,D,R-face -> (4,9); grab; R*2 push [box (4,12)]; rel; D,R -> (5,12); U-face, grab, U-push [box (3,12)]; rel.
- After: remaining top: (3,1) + slots (2,14)/(3,14) (robot will take some). Score = all boxes in frames (bottom frame won't fill all 9 slots — only 5 boxes).

## Call 86 (z=18): (3,12) placed by me; (2,14) by robot; bottom DONE (5/5, incl (14,14)); bottom robot crossed to top arena via gaps (!). Last box (3,1) -> last slot (3,14); ONLY access = box to (4,14), U-push from (5,14).
- Two robots converging on (3,1). I park at (5,15) (neutral, near S-entry) + 5 A5 ticks.
- z=18 = 36 acts. Robot trip est ~25-30 ticks. If robot misroutes next call: intervene — steal box, finish S-entry push locally.
- Odd blip: (3,11) vanished 2 ticks then returned — robot walked over/briefly grabbed deposited box; deposited boxes MAY still register as targets. Watch for churn.

# LEVEL 9 (starts Action 1457, z=64) — L8 CLEARED at 1456 (score 8; robot self-delivered last box (3,14) via S-entry)
Cell map: central wall col 9 rows 0-8; row 9 open (W-E link). WEST: boxes (3,2),(5,1),(5,3),(7,1),(7,2),(8,1); gray (8,2); 3x3 blue frame cells (3,5)-(5,7); robot (7,4). EAST: robot (1,11); 1x2 frames (2,13)-(2,14) & (6,13)-(6,14); boxes (5,11),(7,12),(8,14); dithered #/8 texture row 3 cols 10-15 (unknown terrain).
BOTTOM MAZE rows 10-15: pillar grid; entrances from row 9 at cols 0-1 and 3; PURPLE deep at (14,15).
Plan: camp chokepoint (9,3) area; robots haul; kill purple on emergence; then assist hauls.
## Call 89 (8 acts): D, L*5 -> (9,3), A5 x2 ticks.

## Call 90 (z=57): W robot deposited (7,2)-box -> frame (5,5) in 8 ticks — fast cycle. E robot IDLE 8+ ticks (anomaly, watch).
- Maze walls corrected: row11 walls at cells 2,4,8,12; row12 walls 2,4,6,8,10,12,14. Purple at (11,13) OPEN cell (no tunneling), paused 3 ticks.
- Camp continues (9,3): covers exit (10,3). Purple must emerge cols 0-1/3.
- Batch: A5 x6 ticks.

## Call 91 (z=51): PURPLE DORMANT 9+ ticks at (11,13); E robot dormant too. W robot cycling well (took (5,3)).
- Switch to hauling east boxes myself. Assignments: (7,12)->(6,13); (8,14)->(6,14) [U-push x2 from (9,14)]; (5,11)->(2,13) [E-push x2 then U-push x3; CHECK dithered row-3 terrain passability].
- Batch (20): R*8 row9 -> (9,11); U,U -> (7,11); R-face, grab, R push [box (7,13)]; rel; D,R -> (8,13); U-face, grab, U-push [box (6,13) SLOT]; rel.
- If purple wakes: abort hauls, intercept & A5.

## Call 92 (z=33): (6,13) DEPOSITED (haul 1 east). W robot: (3,5),(4,5),(5,5) done, hauling (5,1). W idle left: (7,1),(8,1).
- PURPLE AWAKE: weaving maze W: (13,7) now; predicted route via (15,3)/col-3 to exit (10,3), ~12-15 ticks. Target likely W boxes/(8,2) gray.
- (5,13)-entry to top frame BLOCKED analysis: (6,13),(6,14) filled → (5,11) must go N-col-11 route: U-push x3 -> (2,11), then E-push x2 -> (2,13).
- Batch (20): haul (8,14): D,D,R -> (9,14), U-face, grab, U*2 [box (6,14) SLOT], rel; then L,L,U,L -> (6,11), U-face, grab, U*3 [box (2,11), me (3,11)], rel, L,U.
- NEXT (~8): R-face at (2,10), grab, R*2 [box (2,13)], rel. Then kill purple.

## Call 94 (z=5, attempt 1 DEAD): 7/9 in ((2,13) by E robot!, west 4, east 2). (8,1) undeliverable in ~6 acts. Purple NEVER stole (hovered (7,5)-(8,6)). Burn confirmed ~0.9/act in L9 => z63 ~ 70 acts.
- ATTEMPT 2 MASTER PLAN (waste in att1 was ~26 camp/chase ticks; robot pace ~12-14 ticks/box, 6 west boxes ~ 72 ticks alone => I MUST take 1-2 west boxes after east work):
- Batch1 (20, DISPATCHED): RESET; R*3 ->(9,11); U*2 ->(7,11); Rface,A5,Rpush[(7,12)->(7,13)],rel; D,R ->(8,13); Uface,A5,Upush[->(6,13) SLOT],rel; D,D,R ->(9,14); Uface.
- Batch2 (~20): A5 grab (8,14); U*2 [->(6,14) SLOT]; rel; L,L,U,L ->(6,11); Uface,A5,U*3 [(5,11)->(2,11)]; rel; L?,U ->(2,10); Rface,A5,R*2 [->(2,13) SLOT]; rel. (E robot may wake & steal at (2,11)/(3,11) — LET IT, saves ~5 acts.)
- Batch3: descend col 12 to row 9, W to west arena; take (8,1) (or (7,1) if robot slower); watch slot availability for entry route; purple emerges (10,3) ~t55-60 => kill on adjacency while there.

## Call 95 (z=47): RESET WORKED but true start = (8,8) NOT (9,8) (att-1 'initial' board was post-action). Whole batch whiffed 1 row off — 16 acts wasted, 0 boxes moved. Header still 'Attempt 1'; z fresh 64.
- PURPLE AWAKE FROM T0 this time: (14,15)->(13,9) westbound maze; exit (10,3) ETA ~t26-30. Att-1 evidence: it may hover w/o stealing. Monitor; divert only if it grabs a box.
- W robot FAST: (5,5),(4,5) deposited by t20, fetching (3,2). ~9t/box => west done ~t60 incl (8,1)?
- Me (6,15). Batch (20, DISPATCHED): haulA (8,14)->(6,14): D*3 ->(9,15), L ->(9,14), Uface,A5,U*2,rel [me (7,14)]; haulB (7,12)->(6,13): L ->(7,13), Lface,A5, R-drag [box (7,13), me (7,14)], rel, D ->(8,14), L ->(8,13), Uface,A5,Upush [box (6,13) SLOT],rel [me (7,13)].
- NEXT batch (16): haulC: L,L ->(7,11), U ->(6,11), Uface,A5, U*3 [box (5,11)->(2,11), me (3,11)], rel, L ->(3,10), U ->(2,10), Rface,A5, R*2 [box ->(2,13) SLOT], rel. Then west help ((8,1)) w/ ~z16.

## Call 96 (z=28): haulA+B DONE ((6,14),(6,13) slots filled). Me (7,13). W robot: (3,5),(4,5),(5,5) in; hauling (5,1)-box via row 1 (at (1,4)). Idle left: (7,1),(8,1) west + (5,11) mine. PURPLE exiting maze at (11,3)->(10,3), entering west arena — near (7,1)/(8,1)/gray(8,2). Theft to (8,2) is low-cost (adjacent to sources); real risk = frame stealing churn.
- Batch (12, DISPATCHED): haulC part 1: L,L ->(7,11), U ->(6,11), Uface, A5, U*3 [box (5,11)->(2,11), me (3,11)], rel, L ->(3,10), U ->(2,10), Rface.
- NEXT: if E robot took box -> skip; else A5, R*2 [box ->(2,13) SLOT], rel (4 acts). Then west: descend col ~10/12 to row 9, kill purple if churning, help (7,1)/(8,1). Budget after batch ~z18 (~21 acts).

## Call 97 (z=17): PURPLE STOLE FRAME DEPOSIT (5,5) -> hauling to gray (8,2). CHURN CONFIRMED in L9 (unlike att1 hover). E robot BLOCKED my 3rd U-push by stepping (1,11)->(2,11) when box hit (3,11), then took box (delivering (2,13)). Att2 dead: ~18 acts left vs ~30 ticks robot work + active thief. RESET dispatched.
- E ROBOT WAKE RULE: wakes when col-11 box reaches (3,11). => only push x2, release, let it fetch.
- PURPLE TIMELINE (both attempts): awake t0, arrives west exit (10,3) ~t44-46, first steal ~t45-50 (frame deposits, hauls to gray (8,2)).
- ATTEMPT 3 SCRIPT (from spawn (8,8), z=64):
  B1 (20, DISPATCHED): RESET; R*3 ->(8,11); U*2 ->(6,11); Uface,A5, U*2 [box (5,11)->(3,11)], rel; D*3 ->(7,11); Rface,A5, Rpush [box (7,12)->(7,13)], rel; D ->(8,12); R ->(8,13).
  B2 (~14): Uface,A5,Upush [box ->(6,13) SLOT],rel; D,D ->(9,13)? wait D->(8,13 occupied?) route: after rel me (7,13): D,D ->(9,13), R ->(9,14), Uface,A5, U*2 [(8,14)->(6,14) SLOT], rel.
  B3: D,D ->(9,14), L*10 ->(9,4) arrive ~t44; A5 kill purple on adjacency (it comes (10,3)->(9,3/4)->NE to frame); then haul (8,1): L*3 ->(9,1), Uface,grab, U-push*3 [box (5,1)], then row-6 reroute E to (6,6), U-push into (5,6) [(5,5) likely filled by robot]. Robot handles (7,1) + any purple-dropped box.

## Call 98 (z=47, t20): B1 PERFECT. (3,11) box -> E robot -> (2,13) DONE. (7,13) staged. Me (8,13). W robot: (5,5),(4,5) in, fetching (3,2). Purple (13,9) — IDENTICAL sched to att2.
- TIMELINE CORRECTION: purple steal is ~t50 (att2: z21), NOT t64. Purple: (11,3) t42, (10,3) t43, (9,3) t44, then (9,4),(9,5),(8,5),(7,5),(6,5) climb, grabs (5,5) ~t49, drags W row 6 -> (7,2)->(8,2) gray deposit ~t55.
- B2 (20, DISPATCHED, t21-40): Uface,A5,Upush [(7,13)->(6,13) SLOT],rel; D,D ->(9,13), R ->(9,14), Uface,A5,U*2 [(8,14)->(6,14) SLOT],rel; D,D ->(9,14); L*6 ->(9,8). Ends t40 facing W.
- B3 sketch (t41+): L*4 ->(9,4) arriving t44 EXACTLY as purple hits (9,3) W-adjacent, facing W already => A5 t45 KILL. If it detours (8,3)/(8,4): chase/ambush its return drag route row6: (6,4),(6,3),(6,2),(7,2). After kill: haul (8,1) east-ring route: me ->(8,2) grab W, drag R*6 [box (8,7)], rel, D,L,(9,7) Uface, grab, U*3 [box ->(5,7) SLOT]. Robot handles (3,2),(5,1),(7,1). Est finish ~t66-70 ~ z within budget IF kill clean.

## Call 99 (z=28, t40): B2 PERFECT — east 100% done ((2,13),(6,13),(6,14)+robot). 6/9 in. Me (9,8) facing W. W robot hauling (5,1)-box (at (1,4)); then (7,1) left for it. Purple (11,3) on att2 schedule: (9,3) t42, (9,4) t43, (9,5) t44.
- B3 (10, DISPATCHED): L*3 ->(9,5) t43 [I OCCUPY its climb waypoint; purple (9,4) adjacent W]; A5 t44 (kill if it stays/moves-first), A5 t45; L,L ->(9,3) t47 [free either way]; U ->(8,3) t48; L ->(8,2) t49 (gray, its deposit cell — I block it); L t50 = face W at box (8,1).
- BRANCHES next call: purple dead => grab (8,1), drag R*6 [box (8,7)], rel, D,L,Uface,grab,U*3 -> (5,7) SLOT (~16 acts). Purple alive w/ stolen (5,5)-box => it returns (6,2)->(7,2) ~t51-53, hovers N-adjacent to me: Uface(blocked)+A5 kill, then recover both boxes. Budget z28 ~ 33 acts; haul ~16 + kill margin OK.

## Call 100 (z=19, t50): PURPLE DEAD t44 (waypoint-block at (9,5) worked: it stepped (9,4) adj-W, A5 killed). 7/9 in ((3,6) robot dep). Robot descending col1 for (7,1) (ETA grab ~t54, dep ~t62-66, likely slot (3,7) from its N lane). Me (8,2) facing box (8,1).
- B4 (16, DISPATCHED, t51-66): A5 grab; drag R*6 [me (8,8), box (8,7)]; rel; D ->(9,8), L ->(9,7), Uface, A5 grab, U*3 [box (8,7)->(5,7) SLOT], rel. If robot stole (5,7) first -> box stalls (6,7), reroute needs ~10 acts but z only ~5 spare — pray N-slot preference holds.
- If both land: 9/9 => SCORE 9, Level 10 next. On L10 start: FIRST verify spawn position before scripting (L9 lesson: spawn was (8,8) not (9,8)).
