# Level 1 notes

Board rows 0-63 = file lines 5-68 of each state block.

- Player: blue 5x5 ring (24 cells, hole center) rows 8-12, cols 14-18.
- Goal: blue box rows 49-55 cols 43-49 with lone blue dot at (52,46) — likely target.
- Red hazard: ONE connected component (82 cells): 3x3 "head" rows 9-11 cols 39-41,
  trail down col 40 to row 40, along row 40 left to blob rows 38-42 cols 14-18
  (blocks left corridor below player).
- Corridors (black O = floor): top corridor rows 7-13 cols 13-44; left vertical
  corridor cols 13-19 down to row ~56; mid corridor cols 25-31 rows 14-19;
  room rows 19-25 cols 13-32; bottom corridor rows 48-56 cols 13-50 to goal.
- UI: blue "0" rows 1-3 cols 1-3 (score/level?), off-white 3x3 cols 5-7,
  blue 3-bar row 5, full-width blue row 63 (timer bar?).

## Confirmed mechanics
- Each press moves player exactly 6 cells (5x5 sprite + 1 gap). Positions grid-aligned.
- Red static (82 cells, no change across all frames/actions).
- Timer: row-63 blue bar 64px, lost 1px after action 2 (~1px per 2 actions → ~128 budget).
- Player center path grid: start (10,16); after 2 downs at (22,16).
- BFS (step 6, 5x5 must fit on 'O'): NO path to goal dot (52,46) avoiding red.
  Only path: straight down col 16 through red blob at (40,16), then right along row 52.
  Full path centers: (22,16)→(28,16)→(34,16)→(40,16)→(46,16)→(52,16)→right x5→(52,46).
- Red blob at (40,16) is exactly player-sized/aligned. Red trail runs in 1-wide pipes
  (col 40 rows 12-40, row 40 cols 19-38). Red 3x3 head at (10,40) in top corridor —
  possible button: player at (10,40) would cover it. Reach: from (10,16) 4 rights.

Action 3-5: Down x3 — RESULT: red blob is SOLID (action 5 blocked, no frames logged
for blocked moves). Player at (34,16), directly above red blob at (40,16).
Not pushable downward (space behind was free but move blocked) — 82-cell red is rigid.

Action 6: ACTION5 = LAUNCH: player slid UP from (34,16) to (10,16) over 20 frames
(until wall). Red unaffected. Unclear if always-up or context/facing dependent.
Action 7: Down → player at (16,16).

Action 8-14 results:
- Player CAN step onto red head slot (10,40): red retracts 82→66 cells,
  tail blob at (40,16) fully cleared (red then spans rows 13-42, cols 20-40).
- Action 13 Right from (10,40) blocked (wall).
- ACTION5 = RETURN TO SPAWN (10,16): player retraces back, red restored to 82.
  (Action 6's "launch up" was also just return-to-spawn.)
- Score still 0, Attempt 1. ~14 actions used; timer bar row 63 shrinking slowly.

Action 15-19 results: retraction is SPRING-LOADED — reverts the moment player steps
off inlet (10,40). Details of retracted state (while standing on inlet):
- Blob moves one 6-step back along pipe: (40,16)→(40,22).
- WALLS MORPH: blob carries a 7x7 pocket; rows 37-43 cols 13-25 become floor;
  left corridor rows 38-42 cols 14-18 fully clear.
- On step-off, blob + walls revert instantly (settled). No ratchet on repeat.
- Player slots in maze (6-grid): corridor col 16 rows 10..52, top corridor row 10
  cols 16..40, connector (16,28), room slots (22,22),(22,28), bottom row 52
  cols 16..46(goal).
- Middle room (rows 19-25, cols 13-32) has no obvious purpose → suspect hidden
  pressure plate there.

Action 20-23: room slots have NO plate. Red static everywhere except inlet.

## DECODED: ACTION5 = time-clone toggle
- State A (UI bar under slot1, slot2='8' solid): normal, moves are RECORDED.
- ACTION5 in state A: player rewinds to spawn (10,16); GRAY GHOST spawns at spawn
  and replays the recorded moves (moves since last ACTION5, state-A moves only),
  one move per subsequent player action; after replay exhausts, ghost IDLES in place.
  UI flips (bar under slot2, slot1 gray).
- ACTION5 in state B: ghost dismissed, player rewinds to spawn, state A resumes,
  recording restarts. State-B moves are NOT recorded.
- Evidence: A6 ghost replayed A1-5's D,D,D,D and idled at (34,16) through A13.
  A14 dismissed it. No ghost in A15+ (state A).

## SOLUTION PLAN (executing)
Recording since A14: [R,R,R,R,L,L,D,D,L] (9 moves, at (22,22)).
A24-28: R,U,U,R,R → recording = 14 moves ending ON PLATE (10,40).
A29: ACTION5 → rewind to spawn, ghost replays 14 moves (t1..t14), ends holding
  plate at t14 forever → worm retracted, corridor clear from t14 on.
Ghost path stays in top corridor/room, never in col-16 corridor below row 10.
My moves: t1-t4: D,D,D,D → (34,16). t5-t14: bounce U,D x5 (28,16)<->(34,16).
t15-t17: D,D,D → (40,16),(46,16),(52,16). t18-22: R x5 → GOAL (52,46).
This call sent: R,U,U,R,R,ACTION5,D,D,D,D. Next call: U,D,U,D,U,D,U,D,U,D,
then D,D,D,R,R,R,R,R (18 actions).
Watch: worm should retract transiently at t4 (ghost's first plate touch), 
re-extend t5, retract permanently at t14.

A24-33: plan worked. A51: SCORE 1 — LEVEL 1 CLEARED (51 actions).

# LEVEL 2 (from A52; board at log line 33583)
- Slot grid: rows/cols ≡ 4 mod 6. Spawn/player: (28,52). Goal dot: (22,28),
  box open-left, enter via (22,22).
- Worm A (46 cells): blob (22,16) [blocks (22,10)<->(22,22) goal corridor],
  pipe down col 16, PLATE (40,16) in row-40 corridor.
- Worm B (52 cells): PLATE (28,40) at bottom of col-40 corridor (reachable),
  pipe down col 40, blob (52,40) [blocks bottom corridor (52,34)<->(52,46)].
- Region X (bottom-left: row-40 corridor (40,10),(40,22),(40,28), col-28
  (46,28), bottom row 52 left slots) reachable ONLY via (52,40) = needs B held.
- UI now 3 slots (ring + 8 + 8) → assume 2 ghosts. Model: ACTION5 = spawn ghost
  replaying moves since last ACTION5 (recording runs always); when slots full,
  press clears all (matches L1's dismissal).
- Timer reset to 64.

## L2 PLAN
P1 (9 act): U,U,U,L,L,D,D,D [spawn→(10,52)→(10,40)→B plate (28,40)] + ACTION5.
P2 (17 act): D,D,D,D,L [→(52,46) t5], bounce R,L,R,L (t6-9), L t10 crosses
 (52,40) after ghost1 holds B at t8, L,L (52,28) t12, U,U (40,28) t14,
 L,L → A plate (40,16) t16 + ACTION5#2.
P3 (19 act): U,U,U [→(10,52)], L x7 [→(10,10)], D,D [→(22,10)], bounce U,D,U,D
 (t13-16; ghost2 holds A at t16), R t17 (22,16), R,R → GOAL (22,28) t19.
No path collisions verified between me/ghost1/ghost2 in all phases.

A52-65: P1 done ✓, ACTION5#1 at A60 ✓ ghost1 replaying exactly (t5=(10,40)).
Worm B retract confirmed at A59 (98→82).
A66-76 sent: R,L,R,L bounce (t6-9), L t10 (52,40), L,L (52,28) t12, U,U (40,28)
t14, L,L → A plate (40,16) t16. STOPPED before ACTION5#2 to verify:
ghost1 idle on B plate (28,40) since t8, red should be 82 while I traverse,
66 when I stand on A plate (both worms retracted).
A66-76 ✓ exactly on plan: ghost1 seated on B plate t8 (A68), I crossed (52,40)
A70, standing on A plate A76 (red 66, both worms retracted).
A77-96 sent (20 actions): ACTION5#2 then P3:
U,U,U, L x7 → (10,10), D,D → (22,10), bounce U,D,U,D (ghost2 seats A plate t16),
R,R,R → GOAL (22,28) at t19. Expect score 2.
Ghost2 replay = A61-76 moves: D,D,D,D,L,R,L,R,L,L,L,L,U,U,L,L (16 moves).
Risk: if ACTION5#2 cleared ghosts instead of spawning ghost2, fallback replan.

# LEVEL 3 (score 2 reached at A96; board fresh, timer reset to 64)
- Spawn (22,10). Goal dot (22,22) in box open at BOTTOM: enter (28,22)->(22,22).
- Slot grid rows/cols ≡ 4 mod 6.
- Yellow worm: plate Y=(22,34) [mid col-34 corridor], pipe row 22, blob BY=(22,52)
  blocking right corridor (16,52)<->(28,52).
- Red2: plate P2=(34,40) [dead-end east of (34,34)], pipe col 40, blob B2=(52,40)
  blocking bottom corridor (52,34)<->(52,46).
- Red1: plate P1=(52,22) [mid bottom corridor - SPLITS R1], pipe col 22, blob
  B1=(34,22) blocking (34,16)<->(28,22) [goal approach].
- Regions: R0=spawn+top+col34upper+{(16,52)}; R2=right-lower {(28..52,52),(52,46)};
  R1a={(34,10),(34,16),(40,10),(46,10),(52,10),(52,16)}; R1b={(52,28),(52,34)};
  R3={(28,34),(34,34)}+P2. Left corridor GAP rows 26-30 (no (28,10)).
- Only routes: R0->R2 via BY; R2->R1b via B2; R1b->R1a via P1 slot (walk over);
  R1a->(34,22)=B1->(28,22)->goal, needs P1 held at that time.
- Key trick discovered L1: recorded BLOCKED moves replay as no-op waits →
  ghosts can be choreographed to hold plates at scheduled times.
- No-op moves: at Y: L or R blocked; at P2: R or D blocked; at spawn: L; at
  (34,16): U; on BY slot: L (into pocket wall? verify); at (52,22): D? (pipe below→blocked).
- OPEN QUESTIONS: (1) crush semantics (re-extension onto occupied slot);
  (2) 3rd ACTION5 with 2 ghosts parked (clear-all vs recycle-oldest);
  (3) do ghosts advance replay on ACTION5 turns; (4) walk-through plates OK.
- Draft plan sketch (optimistic, ~123 actions — tight vs 128 timer!) in analysis;
  need experiments before committing.
A97-107 probe sent: U,U,R,R,R,R,D,D(->Y),D(->28,34 walk-through),D(34,34),R(->P2).
Watch: yellow retract on Y; re-extension after leaving Y; red2 retract on P2.

A97-107 probe ✓ all 11 moves: walk-through plate OK.
## L3 KEY: retraction is PERMANENT (ratchet), NOT spring! Yellow: G48->32 on Y,
step-off -> 42 (plate redrawn), blob STAYS at (22,46); old spot (22,52) now floor,
right corridor (16,52)<->(28,52) CLEAR. Red2 retracted on P2: n92->76, blob
(52,40)->(46,40), bottom crossing (52,40) clear (pending step-off ratchet check).
Red1 unchanged: blob (34,22) rows32-36, pipe col22, plate (52,22).
=> NO GHOSTS NEEDED. Route from P2 (34,40), 29 moves:
L; U x4 (->10,34, re-press Y en route, harmless); R x3 (->10,52); D x7 (->52,52);
L x5 (->P1 52,22, red1 retracts (34,22)->(40,22)); L x2 (->52,10); U x3 (->34,10);
R x2 (->34,22); U x2 -> GOAL (22,22).
A108-127 sent: first 20 (L,U4,R3,D7,L5) ending ON P1. Next call: verify red2
ratchet (n stays 76 after A108; if sprung, L at (52,46)->(52,40) blocks - replan
with ghosts), then send final 9: L,L,U,U,U,R,R,U,U.

## L3 MODEL CORRECTED (A104-127 analysis)
- YELLOW worm = LATCH TOGGLE: each plate ENTRY toggles retract<->extend (A104 retract,
  held through step-off A105-109; A110 re-entry re-EXTENDED it while standing; blocked
  my col-52 descent at A117; A118-127 all blocked, player stuck at (16,52)).
- RED worms = SPRING (hold-while-pressed): red2 retracted on P2 (A107), re-extended
  fully the action I stepped off (A108). Same as L1/L2. Ghost holds required.
- "Ratchet" note above is WRONG.

## L3 FINAL PLAN (77 actions from RESET at ~a128)
RESET; P1(11): U,U,R,R,R,R,D,D(Y tog->retract),D,D,R(on P2); ACTION5#1;
P2(29): L,L,L,L(waits recorded),U,U,R,R,R,R,D,D(Y: ghost1 extends at my a8, I
 re-retract a12),U,U,R,R,R,D,D(22,52 a19),D,D,D,D,D(52,52 a24),L,L,L,L,L(P1 a29);
 ghost1 parks P2 at my a11 (red2 held forever). ACTION5#2;
P3(34): same 25-move route ghost2 replays 4 behind me: U,U,R,R,R,R,D,D(Y t8 extend),
 U,U,R,R,R,D,D(22,52 t15; ghost2 re-retracts Y at t12),D x5(52,52 t20),L x5(P1 t25),
 L,L(52,10 t27),U,U,U(34,10 t30),R(34,16 t31),R(34,22 t32; ghost2 parked P1 since
 t29 holding red1),U(28,22 t33),U GOAL(22,22) t34.
Checkpoints: after batch1 verify RESET cleared recording (ghost1 must be at (16,34)
 t7, G=42); if junk ghost -> RESET and redo (ACTION5 restarts recording).
Batch1 sent: RESET,U,U,R,R,R,R,D,D,D,D,R,ACTION5,L,L,L,L,U,U,R (ends phase2 a7,
 me (10,16), ghost1 (16,34)).
Batch2: R,R,R,D,D,U,U,R,R,R,D,D,D,D,D,D,D,L,L,L (ends (52,34) a27).
Batch3: L,L,ACTION5,U,U,R,R,R,R,D,D,U,U,R,R,R,D,D,D,D (ends p3 t17 (34,52)).
Batch4: D,D,D,L,L,L,L,L,L,L,U,U,U,R,R,U,U -> GOAL.

## A128-147 RESULTS + TRUE ACTION5 MODEL (decoded from L2 re-analysis)
- RESET (A128): worked (spawn, worms fresh, TIMER REFRESHED to 64; depletion 1px/2
  actions => 128/attempt). BUT RESET also cleared the recording.
- A140 ACTION5: NO ghost (empty recording) — burned slot1. Frames show REVERSE
  REPLAY: player retraces recorded moves backward; WORLD REWINDS to level start
  (worms re-extend, yellow latch undone).
- TRUE MODEL: press k = world rewind to LEVEL START + player to spawn; ALL prior
  recordings replay CONCURRENTLY from spawn (recording i = moves between press i-1
  and i), one move/action, idle forever at end. Recording always on between presses.
- GHOSTS ARE PASS-THROUGH vs player (L2 A78-82: ghost1 invisible because coincident
  with me; separated at A83, both ghosts visible A83-95, both parked plates ✓).
- L2 ghost1 was never 'dismissed' — it replayed from scratch after press2.
- Slots UI: 'fff'=active slot, presses gray them L->R. 3 slots = 2 ghost recordings.
  Press when all gray = CLEAR-ALL (L1 A14 precedent: dismiss + recording restart,
  fresh slots; L1 A29 press after clear worked fine).
- Yellow latch toggles on EVERY entry by anyone; world rewind resets it extended.

## L3 PLAN v3 (66 actions from A148)
A148: press#2 -> junk ghost2 (7 junk moves: 4 no-op L + U,U,R -> idles (10,16),
  harmless, pass-through). Slots full $###$###$fff.
A149: press#3 -> CLEAR-ALL expected: fresh $fff$888$888, empty recording, spawn.
Then: R1(11): U,U,R,R,R,R,D,D(Y toggle retract t8),D,D,R -> P2 t11. press.
R2(21): U,U,R x7 (10,52 t9), D,D (22,52 t11; Y retracted by ghost1 t8), D x5
  (52,52 t16), L x5 -> P1 t21 (cross (52,40) t18, red2 held by ghost1 since t11). press.
F(30): U,U,R x7,D,D,D x5 (52,52 t16),L x5 (P1 t21, ghost2 arrives same time,
  pass-through OK, ghost2 parks holding red1), L,L (52,10 t23), U,U,U (34,10 t26),
  R,R (34,22 t28; blob retracted to (40,22) held), U,U -> GOAL (22,22) t30.
Verify after A148-149: UI fresh, no ghosts, me at spawn, worms extended.
Risk: press#3 = clear+burn-slot1-empty-ghost loop -> would show $###$fff$888; replan.

## A148-149 RESULTS
- A148 press#2: rewind (16 frames), UI -> $###$###$fff, me spawn. Ghost2(junk 7mv)
  presumed spawned but invisible (t0, coincident at spawn).
- A149 press#3 (slots all gray): ZERO visible effect. 1 board, UI unchanged, no
  rewind anim. Either pure no-op OR silent clear&restart (world/me already at
  start state, empty+junk-at-spawn ghosts -> dismissal invisible; only UI
  contradicts, may lag).
- Full slot map (fresh board) computed: bottom-left pocket has doors (34,22)
  [red1 blob] and P1 slot (52,22) [walkable plate]. (28,10) gap confirmed.
  Solo+latch reach: everything except: south-of-(22,52) needs Y latch toggle (OK
  solo); (52,40) crossing needs P2 held-by-other; (34,22) crossing needs P1
  held-by-other. PROVEN: need TWO simultaneous-replay functional ghosts
  (ghost_A parks P2, ghost_B parks P1, me walks through; pass-through allows
  crossing parked ghost on P1 slot).
- L1 precedent: press-at-full = dismiss-all & restart (A14), enabling A29 press.
  L3 A149 may be same (UI lag?) or no-op.
## TEST SENT (A150-152): L,L,L (no-op at spawn, I stay put).
- If '#' ghost walks (16,10)->(10,10): junk ghost2 alive, A149 was no-op ->
  only 1 functional ghost per reset cycle -> MAJOR replan needed.
- If no ghost + UI fresh ($fff$888$888): A149 = clear&restart -> recording live
  since A149 (these 3 L's recorded, harmless no-ops) -> run plan v3 core:
  R1(11) U,U,R,R,R,R,D,D,D,D,R; press; R2(21) U,U,Rx7,D,D,Dx5,Lx5 end P1; press;
  F(30) U,U,Rx7,D,D,Dx5,Lx5(P1 t21),L,L,U,U,U,R,R,U,U goal. Timer 54px=~108 OK.
- If no ghost + UI gray: recording unknown; try RESET cycle.

## A150-152: no ghost sprite, UI still gray. NEW HYPOTHESIS: ghosts INVISIBLE in L3
but functional. All data consistent: ghost1=[A129-139]=exactly R1 (U,U,R,R,R,R,
D,D,D,D,R -> P2), restarted replay at A148 press (t1=A149). Its t8 (Y toggle,
G 48->32) lands A156; t11 (P2 press, n 92->76 permanent) lands A159.
A153-159 sent: 7x L no-op at spawn. WATCH G at A156, n at A159.
- If drops occur: invisible ghosts confirmed; ghost2=junk; no presses left; P1
  unholdable -> plan: timer-death (bar ~50px = ~100 acts) to force Attempt 2
  hard reinit, then clean run: R1,press,R2,press,F (64 acts, fits fresh 128).
  (NEVER use manual RESET again: soft, kills recording, doesn't ++attempt.)
- If no drops: ghosts dead/dismissed; next test RESET-revival: RESET,U,U,R,
  ACTION5,L,L watching for ghost effects/UI.

## A153-159: NO G/n drops. Invisible-ghost hypothesis DEAD. No ghosts exist.
## A160-177 RESET-REVIVAL TEST sent:
RESET; U,U,R,R,R,R,D,D (8 moves ending ON Y plate, G 48->32 at record; my later
rewind restores 48); ACTION5; L x8 (waits at spawn).
Watch next call:
1. UI after RESET (A160): fresh $fff$888$888 => RESET restores slots; gray => slots
   dead until attempt reset (timer-death).
2. A169 press block: big reverse-replay anim => recording alive post-RESET.
3. G drop 48->32 at A177 (press+8): ghost functional (visible or not).
If ALL pass: next call RESET (refresh timer+slots), then R1(11),press,R2(21),
press,F(30) = 65 acts. If fail: timer-death grind (~128 no-ops after last RESET,
sadly refreshed) to force Attempt 2, then clean 64-act run.

## A160-177 RESULTS
- RESET restores slots ($fff$888$888) + timer (64) ✓. Recording ALIVE post-RESET
  (A169 press = 36-frame reverse-walk of the 8 recorded moves).
- REWIND = literal BACKWARDS WALK with live physics, NOT state restore:
  stepping-off-backwards re-fires springs; reverse-ENTERING a plate re-toggles
  latch (explains A140's apparent 'world restore'). A169: Y latch stayed
  retracted (G=42) because reverse path exited Y northward w/o re-entry.
- A170-177 (8 blocked L's): NO ghost effects. But all were no-ops!
## NEW HYPOTHESIS: ghosts advance ONLY on my SUCCESSFUL moves; ghost currently
  invisible because coincident with me at spawn (t0). Implication if true: no-op
  waits DON'T advance ghosts; choreography waits must be real bounce moves.
## TEST A178-186 sent: U,U,R x7 (I diverge from recorded path at move 7).
  Ghost replay [U,U,R,R,R,R,D,D] would separate at t7 (16,34) and enter Y at t8:
  G 42 -> 48ish (extend toggle) = OBSERVABLE even if ghost invisible.
  If G changes: ghosts functional w/ move-only advance -> replan choreography
  (bounce moves as waits). If not: no ghosts in L3 -> timer-death grind
  (bar 56 -> ~112 no-ops) for Attempt-2 hard reinit.

## A178-186: GHOST MECHANIC CONFIRMED + FINAL MODEL
- Ghosts advance ONLY on my successful moves (blocked no-ops freeze them). Pass-through; invisible when coincident with player.
- A184-186: ghost separated at (16,34), entered Y plate, toggled latch (G 42->38), parked. Model fully verified.
- Press rewind = literal reverse-walk with LIVE physics (re-fires plates). RESET = fresh slots+timer+worms, kills ghosts, recording restarts.

## PLAN v4 (65 actions, verified lockstep) — CURRENT
Needs ghost_A parked on P2 (34,40) and ghost_B parked on P1 (52,22).
- RESET
- R_A (11): U,U,R,R,R,R,D,D,D,D,R -> end on P2. (Y toggled at move8 entry, re-toggled by rewind reverse-entry.)
- ACTION5 press#1 (rewind to spawn, ghost_A stored)
- R_B (21): U,U,R×7 (k9=(10,52)), D,D (k11=(22,52); Y retracted by ghost_A's k8 entry), D×5 (k16=(52,52)), L×5 (k18 crosses (52,40) held: ghost_A parked P2 since its k11; k21=P1)
- ACTION5 press#2 (ghost_B stored)
- F (30): U,U,R×7,D,D,D×5,L×7 (k21 over P1 w/ ghost_B parking same tick; k23=(52,10)), U,U,U (k26=(34,10)), R,R (k28=(34,22); red1 held by ghost_B), U,U -> GOAL (22,22) k30.

### Batch splits
1. [SENT ~A187] RESET + R_A + ACTION5 + R_B k1-k7 (U,U,R,R,R,R,R)
2. R_B k8-k21: R,R,D,D,D,D,D,D,D,L,L,L,L,L + ACTION5 + F k1-k5: U,U,R,R,R  (20)
3. F k6-k25: R,R,R,R,D,D,D,D,D,D,D,L,L,L,L,L,L,L,U,U  (20)
4. F k26-k30: U,R,R,U,U  (5) -> score 3

### Verify after batch1 (next call)
- Me at (10,40); ghost_A visible at (16,34) [its k7]; G=48 (its Y entry k8 pending); UI $###$fff$888; timer fresh-ish.

## A187-206 (batch 1) VERIFIED
Player (10,40), ghost_A (16,34)=its k7, G=48, UI $###$fff$888, timer 55px. All moves succeeded (466/856/3586-line blocks as expected). Batch 2 sent at ~A207: R,R,D×7,L×5,ACTION5,U,U,R,R,R.
Expected after batch 2: press#2 done (UI $###$###$fff... wait slot3 was 888 -> check), ghost_B stored, both ghosts replaying; me at (10,28) (F k5). Verify ghost_A parked P2, ghost_B en route, Y retracted (G=42ish), (52,40) open.

## A207-226 (batch 2) VERIFIED
All 20 succeeded. Ghost_A pressed Y (A207) + P2 (A210); I landed P1 (A220); press#2 rewind A221 (6186 lines — ghosts ALSO reverse-walk with live physics: Y re-extended, confirmed blob back at (22,52) at A226). Me (10,28)=F k5; both ghosts coincident/invisible (same route prefix). UI $###$###$fff. Timer 45px.
Batch 3 sent (~A227): R×4,D×7,L×7,U×2 = F k6-k25. Expect: ghost_A Y-retract at my move 3, parks P2 at my move 11; I cross (52,40) at move 13, end at (40,10) after U,U... wait k24-25 = (52,10)->(46,10)->(40,10). Batch 4: U,R,R,U,U -> GOAL.

## A227-246 (batch 3) VERIFIED
All 20 ok. Ghost_A: Y press A229, parked P2 A232 (it was at k5, so k11 = my move 6 — arithmetic note). Ghost_B parked P1 A242; replay frames ceased after (recordings done). Me (40,10); red1 retracted, (34,22) free; timer 35px.
Batch 4 sent (~A247): U,R,R,U,U -> goal (22,22). Expect score 3 / Level 4.

## LEVEL 3 SOLVED at A251 (score 3). Total plan v4 = 65 actions (A187-251), zero blocked moves.

## LEVEL 4 (loaded A251, fresh slots $fff$888$888, timer 64px)
Elements (settled A251):
- Spawn (10,28) in top-left room rows 7-13 cols 7-31.
- Red worm: plate (28,34) in dead-end stub (cols 31-37, rows 26-31, below wide room); pipe row 28; blob (28,10) blocks col-10 shaft (rows 14-43, cols 7-13).
- Purple: pad 3x3 (28,52) at bottom of col-53 shaft (via right room rows 7-13 cols 38-56); pipe down col 53 + rows 40,52 west to two sealed 7x7 boxes: box1 interior (40,29), box2 interior (52,29). Boxes currently sealed (empty 5x5 interiors).
- Goal chamber C-shape rows 49-55 cols 7-13, interior (52,10), open east; approach corridor rows 49-55 cols 14-25 → box2.
- Wide room rows 19-25 cols 26-44 links: col-28 shaft (spawn), col-41(?) shaft to right room, red plate stub.
- Rows 37-43 room cols 7-25ish links col-10 shaft to box1 west side.
Hypothesis: ghost parks red plate → col 10 opens; purple pad opens/toggles purple boxes (doors on goal path). Unknown purple semantics (spring/latch/other).
Probe sent (~A252, 8 actions): D,D,R,D(plate),U,R,U,U — watch blob retract/re-extend, grid alignment east of wide room.

## A252-259 probe results (L4)
- All 8 succeeded. Red plate (28,34) = SPRING (blob (28,10)->(28,16) while standing at A255, back at A256).
- Grid uniform 6-step both axes: centers 10,16,22,28,34,40,46,52. Right room reached at (10,40).
- Box interiors likely (40,28),(52,28) grid-aligned (recheck outline cols 25-31).
- Probe 2 sent (~A260): R,R,D,D,D(pad 28,52),U — watch purple boxes on pad press/release.

## A260-265: purple pad decoded (partially)
Pad (28,52) entry = ONE-SHOT PULSE: signal runs wire, boxes pulse (box1 bottom row44 + box2 top row48 grow transient purple dots cols 27,29 during frames 12-25), then ALL reverts. No settled-state change whatsoever (spring-hold shows nothing either — settled-on-pad identical). Hypothesis: pulse transfers/swaps box interior contents (box1<->box2); both empty so no-op. Goal corridor rows 49-55 cols 14-24 + chamber sealed EXCEPT via box2 interior (52,28). Box1 interior (40,28) west-adjacent to (40,22).
Plan: ghost_A = D,D,R,D parks red plate (k4). ghost_B = 11-move pad route D,D,R,R,U,U,R,R,D,D,D + U,D,U,D... re-entries (pulse at k11,k13,k15).
Batch sent (~A266): RESET, D,D,R,D, A5#1, D,D,R,R,U,U,R,R,D,D,D(pad), U,D,U (20). Next batch: D, A5#2, final walk L,L,L,D,D,D,D,D,R,R to (40,22), filler L + R-entry attempts around pulses.
CAUTION: blocked player moves freeze ghosts — sequence L/R filler so pulses fire before entry attempts.

## A266-285 (rig batch A) OK
RESET A266; ghost_A(D,D,R,D) press#1 A271; ghost_A parked red plate A275 (my post-press move 4). Pad reached A282 (pulse), re-entries A284 (pulse). Recording since press#1 (14 moves): D,D,R,R,U,U,R,R,D,D,D,U,D,U.
Batch B sent (~A286, 18): D(15th rec move, pulse), A5#2, then post-press: L,L,L,D,D,D,D,D,R,R (to (40,22) by move 10; ghost_A re-parks plate at my move 4), L(11=ghost_B pad pulse1), R(12), R(13=box1 entry attempt; if succeeds pulse2 fires same tick with me inside), L(14), R(15=pulse3 if 13 blocked...), R(16 entry attempt).
Watch: box walls during pulses; whether entry ever succeeds; teleport evidence.

## A286-303: TELEPORT DECODED (L4)
- A300: R into box1 on pulse tick = enter + teleport to BOX2 (52,28) same tick. A301: exit west to GOAL CORRIDOR (52,22). A302: R into box2 on pulse tick = teleport UP to box1 (swap/cycle). A303: R blocked inside box1.
- Box west walls enterable (at least on pulse ticks; exit always). Pulse teleports box occupant to the other box.
- State A303: me in box1 (40,28); ghost_A parked red plate; ghost_B parked pad (done, no more pulses); UI $###$###$fff (badge3 ACTIVE!); timer 46px.
- GAMBLE sent (~A304, 17 actions): ACTION5 press#3 + route: L,L,L,D,D,D,D,D,R,R,L(pulse1),R,R(enter box1+pulse2->box2),L,L(pulse3 midcorridor),L -> GOAL (52,10) at k16.
- If press#3 = no-op: moves execute from box1 (harmless junk), fallback = RESET + full redo (~37 actions).

## A304-320: PRESS#3 = CLEAR-AND-RESTORE
ACTION5 with badge3 active: rewinds player to spawn, KILLS all ghosts, restores ALL 3 badges fresh ($fff$888$888). No ghost replays after. (L3 all-gray no-op was post-clear state.) Slot model: press1/press2 = store ghosts; press3 = wipe & refresh.
A310-320 blocked at (22,10) (blob extended, no ghost). Timer 37px at A320.
REDO sent (~A321, 20): RESET, D,D,R,D, A5#1, D,D,R,R,U,U,R,R,D,D,D, U,D,U — identical to proven rig.
Next batch (18): D, A5#2, L,L,L,D,D,D,D,D,R,R,L,R,R,L,L,L -> GOAL (52,10) at k16. Expect score 4.

## LEVEL 4 SOLVED at A358 (score 4).

## LEVEL 5 map (fresh at A358: slots fff/888/888, timer 64px)
Spawn (16,4). Goal (46,10), chamber rows 43-49 cols 7-13, entered from BELOW via (58,10)->(52,10)->(46,10).
- Yellow1: plate (10,4) [spawn shaft top], pipe row 10, blob (10,22) blocks top-corridor/mid-shaft junction. Retracted blob -> (10,16) (harmless for our routes).
- Yellow2: plate (28,22) [in col-22 shaft], pipe row 28, blob (28,40) blocks descent (28,40)->(40,40). Retracted -> (28,34) cosmetic.
- Red: plate (40,22) [bottom of col-22 shaft], pipe col 22, blob (58,22) blocks bottom corridor. Retracted -> (52,22) cosmetic.
- Purple: pad (28,58) [bottom of right shaft cols 56-62], boxes: box1 int (40,46), box2 int (52,46). box1 west approach (40,40); box2 exits west (52,40) -> D (58,40) -> bottom corridor.
Topology: spawn shaft (col 4, rows 7-37) + wide room rows 19-25 cols 1-25 + col-22 shaft rows 26-43 (plate2, red plate dead-end) + top corridor rows 7-13 cols 19-62 (blob1 at junction) + right shaft cols 56-62 rows 14-31 (pad at bottom) + band rows 26-31 cols 44-62 -> (28,40) -> shaft rows 32-36 cols 38-44 -> box1 west room rows 37-43 cols 38-43. Box2 west room rows 49-55 cols 38-43 -> corridor rows 55-61 cols 7-44.
PLAN (60 actions, 3 phases):
- P0 ghost_A (7): D,R,R,R,D(plate2 toggle),D,D(red plate). A5#1.
- P1 me->pad (21): U(plate1 toggle: blob1 retract),D,D,R,R,R,U,U,R,R,R,R,R,R,D,D,D(pad),U,D,U,D. A5#2. [ghost_A replay: k5 yellow2 retract, k7 red park. Rewind#2 re-extends yellow1+yellow2 via reverse crossings.]
- P2 final (30): D,R,R,R,U,U(10,22),R,R,R,R,R,R(10,58),D,D,D(pad,mine-pulse),L,L(pulse k17),L(28,40),D(pulse k19),D(40,40),R(ENTER box1 + pulse k21 -> TELEPORT box2),L(52,40),D(58,40),L,L,L(58,22 red held by ghost_A since my move 7),L,L(58,10),U,U -> GOAL (46,10).
State timeline verified: yellow1 retract by ghost_B k1 (my move 1); yellow2 retract by ghost_A k5 (my move 5); red held from my move 7.
Batches: B1 (sent ~A359, 20) = P0 + A5 + P1 moves 1-12. B2 (20) = P1 13-21 + A5 + P2 1-10: [R,R,D,D,D,U,D,U,D, A5, D,R,R,R,U,U,R,R,R,R]. B3 (20) = P2 11-30: [R,R,D,D,D,L,L,L,D,D,R,L,D,L,L,L,L,L,U,U].

## LEVEL 5 SOLVED at A418 (score 5). Rig: 60 actions A359-418, zero blocked.

## LEVEL 6 map (fresh at A418)
- Player (34,58) in right shaft rows 31-55 (cols 55-61). GREEN ring (22,58) in separate shaft segment rows 14-25 (connects UP to top corridor rows 7-13; walled below rows 26-30).
- Goal chamber rows 49-55 cols 43-49, marker (52,46), opens WEST (enter (52,40)->R).
- Y1 plate (10,4) / blob (28,4); Y2 plate (10,22) / blob (28,22) — blobs in left band rows 25-31.
- Y3 plate (52,16) / pipe row 52 / blob (52,34) — BLOCKS goal approach corridor rows 49-55.
- R1 blob (10,34) / plate (28,34); R2 blob (10,46) / plate (28,46) — blobs block TOP corridor; plates in stub shafts rows 25-30 cols 31-37 / 43-49, reachable from row-31 band.
- Green hypothesis: second avatar mirroring inputs. Probe sent (~A419): single D.

## A419: GREEN = VERTICAL-MIRROR AVATAR
My D -> green moved UP (22,58)->(16,58) while I went (34,58)->(40,58). Green mirrors vertical axis.
Probe 2 sent (~A420): [D, L]. After D: me (46,58), green (10,58) top corridor. Then L: my L is BLOCKED (shaft walls); green L open to (10,52), green R blocked (edge).
Outcomes: green at (10,52) => horizontal same-direction + green moves even when I'm blocked. Green stays at (10,58) => horizontal mirrored OR green frozen on my blocked move (disambiguate next).

## A420-421 + L6 topology analysis
- A420 D: me (46,58), green (10,58) — corridor. A421 L: I'm blocked -> NOTHING moves (green frozen despite open L, or green H is mirrored and its R was edge-blocked). Ambiguous.
- Green is vertically PINNED in top corridor zone (rows 7-25, col 58 only); pipe channels 3-wide unwalkable.
- Pairing: green row + my row = 56 (or 62 with pinned offset); green at row 10 only when I'm at rows 46+ — where I have NO horizontal moves. => My live H-moves can NEVER walk green along the corridor. Circular deps: Y1/Y2 plates (10,4)/(10,22) need green; left/bottom-left regions need Y1/Y2; Y3 plate needs bottom-left; goal approach needs Y3.
- HYPOTHESIS: ghost replay moves ALSO drive green (mirrored). Would unlock everything: ghost with H-rich route drives green while I position elsewhere.
- Probe sent (~A422): [A5(press#1, recording=[D,D,Lblocked]), D, D, U, U]. Watch: (a) does green rewind on press? (b) double green-steps when ghost k1/k2=D replay concurrent with my D (ghost D + my D both mirror U)? (c) recorded blocked move behavior at k3.
- State pre-probe: me (46,58), green (10,58), slots fresh, timer ~59px.

## A422-426 findings (L6 green driver)
Probe executed: [ACTION5, D, D, U, U]. A422 press#1: rewound me to (34,58), stored ghost_A (recording [D,D,L] from prior turn... actually recording = my moves since last press), green rewound to (22,58)... 
Observed green moves (frame-synced to MY move animations, one step per my successful move):
- A423 (my D): green U (22,58)->(16,58)
- A424 (my D): green U (16,58)->(10,58)
- A425 (my U): green WEST (10,58)->(10,52)  <-- kills simple mirror model (open mirror-D ignored)
- A426 (my U): green EAST (10,52)->(10,58)  <-- reversal
Ghost_A idle at (46,58) throughout A425/426 (its recording ended).

**BOOMERANG-REPLAY HYPOTHESIS (leading):** green replays the press recording MIRRORED (D->U, L->L? no—observed L stayed L... recording had [D,D,L]; green did U,U,L = vertical mirror only) forward to the end, then reverses (retraces backward: L->R), ping-pong looping. Advances one step per my successful move, independent of my direction.
Prediction next: green D to (16,58), then D to (22,58), then forward again U,U,L...
Distinguishing probe: my two D's (safe). Boomerang => green D,D. Input-mirror => green U (blocked at wall row 7).

**Implication if confirmed:** I control green's path by crafting the recording before a press: recording R = green replays vmirror(R) forward/backward repeatedly. To park green on a plate: make plate the recording END (green idles? no—it boomerangs) — need green to be ON plate at the right tick, or recording that ends exactly at plate with odd handling. Yellow plates latch on ENTRY, so each pass over Y-plate toggles! Must count passes carefully (odd number of entries = retracted).

## A427-428: BOOMERANG CONFIRMED
My D,D → green D,D back to (22,58). Green replays vmirror(archived recording) forward then backward (retrace), 1 step per my successful move, direction-independent. Blocked inputs ARE recorded and replay as inputs (the L in [D,D,L] was blocked for me, executed by green).
Unknown: loop vs one-shot after full period; do blobs block green; does green toggle plates.

## L6 map corrections (passability on 6-centers, A428 board)
Row 10 corridor cols 4-58 (green only; my shaft col 58 stops at (28,58) wall).
Green zone: (10..22,58) shaft + row-10 corridor. Green D blocked everywhere in corridor except col 58; U blocked at row 10.
My graph: spawn (34,58); shaft (34..52,58); band (34,46)-(34,58); stubs (28,46),(28,40),(28,34) [R plates]; middle room row 40 cols 16-46; (34,22); mid shaft (46,34); Y3 pocket (52,34)[blob]; goal (52,40)->(52,46).
Left: tower col 4 rows 34-58; bottom corridor (58,4)-(58,16); Y3 plate (52,16) only from (58,16).
Left band row 28 cols 4-22: enter ONLY via (28,4)[Y1 blob] or (28,22)[Y2 blob]. (34,22)<->(28,22) blocked by Y2 blob; (34,4)<->(28,4) blocked by Y1 blob.
Route once Y1,Y2,Y3 retracted: spawn,L,L,D,L,L(40,34)... to Y3 via left: (34,22) needs Y2 open... full: (34,22)->(28,22)->(28,16)->(28,10)->(28,4)->(34,4)->(40,4)->(46,4)->(52,4)->(58,4)->(58,10)->(58,16)->(52,16)[Y3 toggle]->back->(40,22)->(40,28)->(40,34)->(46,34)->(52,34)->(52,40)->(52,46) GOAL.
Row-sum invariant pre-press: my_row+green_row=56 while green unblocked vertically.

## Triple-test probe (this turn)
At (46,58) L is blocked: write 6 blocked L's into buffer, then press#2. Buffer=[D,D,U,U,D,D,L*6] -> green fwd: U,U,D,D,U,U,L(52),L(46=R2 blob!),L(40),L(34=R1 blob!),L(28),L(22=Y2 plate!) endpoint t12.
Next turn: clock 12 moves, read green pos + Y2 blob state:
- green stuck (10,52) => blobs block green
- green (10,22) + Y2 blob retracted to (22,22) => pass-through + toggles => WINNING TOOL
- clock beyond t24 later to test loop vs one-shot.
Press#2 rewinds me to spawn via shaft dance (safe). Ghost_B parks (46,58) harmless.

## A436-447: GREEN BINDS AT PRESS#1 ONLY + LOOPS FOREVER
Green ignored recording#2, kept ping-ponging vmirror(recording#1)=[U,U,L]+[R,D,D], two full periods observed. LOOP confirmed (never idles). => Green's program = recording archived at the FIRST press after level start/RESET. Later presses rewind green but don't rebind.

## L6 FULL SOLUTION DESIGN (the "one-recording" plan)
Program (recording#1 after RESET) = [D,D, L*9, pads*14] (pads=U,D alternating; my writes: D,D real to (46,58), L*9 blocked there, pads oscillate (40/46,58)). N=25, period 50.
Green fwd: U,U -> (10,58); L*9 -> (10,4) [crosses (10,46) t4, (10,34) t6, Y2 (10,22) toggle t8, Y1 (10,4) toggle t11]; pads t12-25 noop. Bwd: noop t26-39, R*9 t40-48 [Y2 re-toggle t42], D,D t49-50.
Windows: Y2 open ticks [8,42), Y1 open [11,61).
My clock path (post-press, ticks=my successful moves), includes red-plate insurance (stand on R2 at settle t3 for green's t4 crossing; R1 at settle t5 for t6) in case red blobs block green:
t1-13: L,L,U(R2 plate),L(28,40),L(R1 plate),R,R(28,46),D(34,46),D(40,46),L,L,L,L(40,22)
t14-33: U(34,22),U(28,22),L,L,L(28,4),D,D,D,D,D(58,4),R,R(58,16),U(52,16 Y3!),D,L,L(58,4),U,U,U,U(34,4)
t34-45: U(28,4),R,R,R(28,22),D,D(40,22),R,R(40,34),D(46,34),D(52,34),R,R(52,46) GOAL
Risks: (a) RESET might not unbind green - detect: green won't live-mirror/rebind; (b) pipe cells in stub pockets might block my plate entries t3/t5 - then clock count shifts, re-plan; (c) race semantics if blobs block green: assumes plate state at settle T-1 governs green move T.
Batches: A: RESET,D,D,L*9,padU/D*8. B: pad*6, ACTION5, t1-13. C: t14-33. D: t34-45.

## A478 CATASTROPHE: GREEN EATEN BY RED BLOB
Green entered (10,46) at t4 as I stepped off R2 plate: blob re-extension during the same tick CONSUMED green (sprite shrank 24->0). Lessons: (1) red blobs DO block/kill green; (2) personally holding a plate fails - state during tick T is after my step-off; (3) blob extension into an occupied cell KILLS the occupant. Green gone for rest of life -> RESET required.

## REVISED MASTER PLAN v2 (ghost-held plates)
Key: parked ghost (recording ended) idles FOREVER and holds plate. Ghost on R1 (28,34) is blocked for U,D,L (only R moves it) -> recording#1 can continue with D,D,L*9,U*10 after reaching R1 without moving ghost_A.
Writes (pre-press#1): real walk L,L,U,L,L (spawn->R1 seat), then blocked D,D + L*9 + U*10 while seated. Recording#1=[L,L,U,L,L,D,D,L*9,U*10], N=26.
Green program vmirror: t1-5 noop, t6-7 U,U, t8-16 L*9 (Y2 t13, Y1 t16), t17-26 noop; bwd: t27-36 noop, t37-45 R*9 (Y2 retoggle t39), t46-47 D,D, t48-52 noop. Y2 open [13,39), Y1 open [16,68).
press#1 -> ghost_A (parks R1 at clock t5). Walk L,L,U (to R2), press#2 -> ghost_B=[L,L,U] parks R2 at t3. Green restarts; crossings t9 (R2, held since t3) and t11 (R1, held since t5) SAFE.
Traversal clocks: t1 L,t2 L,t3 D(40,46),t4-7 L*4(40,22),t8-14 osc U,D,U,D,U,D,U(34,22),t15 U(28,22),t16-18 L*3(28,4),t19-23 D*5(58,4),t24-25 R,R,t26 U(52,16 Y3),t27 D,t28-29 L,L(58,4),t30-33 U*4(34,4),t34 U(28,4),t35-37 R*3(28,22),t38-39 D,D(40,22),t40-41 R,R(40,34),t42-43 D,D(52,34),t44-45 R,R(52,46) GOAL.
Batches: (1) RESET,L,L,U,L,L,D,D,L*9,U*3. (2) U*7,A5,L,L,U,A5,t1-7. (3) t8-27. (4) t28-45.

## LIFE 3 FAILURE: RESET DOES NOT UNBIND GREEN
Green replayed life-2's program ([D,D,L*9,(U,D)*7], bound at A474) after RESET. My walk L,L,U(R2!),L killed it again: green's t4 L into (10,46) coincided with my t4 step-off re-extension. Rule: green keeps last-bound program across RESET; rebind happens ONLY at first press of each life. Extended blob statically BLOCKS green (safe); extension INTO green kills.

## PLAN v3 (life 4)
Walk to R1 seat rerouted so green (replaying old program) is blocked safely: L,L,D(40,46),L,R,L,R,L,R,L,R(40,46),U,U(28,46 during green noop phase),L,L(28,34 seat). Green under old program: U,U,(L to 10,52),then all L's blocked (blob never touched during its L phase t4-11), noops after.
Writes at seat: D,D,L*9,U*10 (all blocked). Buffer#1 = [L,L,D,L,R,L,R,L,R,L,R,U,U,L,L,D,D,L*9,U*10] N=36.
Green NEW program vmirror fwd: mostly noops; t3 U(16,58) [from my D], t12 D(22,58) [my U], t16,17 U,U (10,58), t18-26 L*9: (10,46) t19, (10,34) t21, Y2 toggle t23, Y1 toggle t26, t27-36 noops. Bwd: t49 Y2-retoggle, crossings t51,t53 (ghost-held ok). Y2 open [23,49), Y1 open [26,98).
press#1 (REBIND, ghost_A parks R1 at replay t15), walk L,L,U, press#2 (ghost_B=[L,L,U] parks R2 at t3).
Traversal 55 clocks: t1 L,t2 L,t3 D,t4-7 L*4(40,22), t8-22 osc U/(D,U)*7 end (34,22), t23 D, t24 U, t25 U(28,22), t26-28 L*3(28,4), t29-33 D*5(58,4), t34-35 R,R, t36 U(52,16 Y3), t37 D, t38-39 L,L, t40-43 U*4, t44 U(28,4), t45-47 R*3(28,22), t48-49 D,D(40,22), t50-51 R,R(40,34), t52-53 D,D(52,34), t54-55 R,R GOAL.
Batches: (1) RESET+walk15+D,D,L,L. (2) L*7,U*10,A5,L,L. (3) U,A5,t1-18. (4) t19-38. (5) t39-55.

## PRESS PARITY DISCOVERY (A545-547)
Press A545 (global press #4) did NOT rebind green (post-press clocks L,L -> green U,U = still life-2 program).
Rebind history: press1 A422 REBIND, press2 A435 no, press3 A474 REBIND, press4 A545 no.
=> Green rebinds only at ODD global presses (alternating A/B recorder slots). RESET does not affect parity. Next press = #5 = REBIND.
(Alternative "2-full-loops" theory also fits data but would make level unsolvable given timer - discarded on design grounds.)

## PLAN v4 = v3 redone one cycle later so the R1-seat press is press#5
RESET (life 5; green keeps life-2 program, tick reset). Same proven-safe walk + writes as A508-544:
walk [L,L,D,L,R,L,R,L,R,L,R,U,U,L,L] then blocked writes D,D,L*9,U*10 at R1 seat.
press#5 (badge1): REBINDS green to [L,L,D,...,U*10]-mirror; ghost_A replays and parks R1 at t15.
walk L,L,U (green noops t1-3... t3=U(16,58) fine), press#6 (badge2): ghost_B=[L,L,U] parks R2 at t3; green rewinds+restarts.
Green run: crossings t19 (R2, held from t3), t21 (R1, held from t15), Y2 toggle t23, Y1 toggle t26. Y2 open [23,49), Y1 open [26,98).
Traversal 55 clocks (as v3): t1 L,t2 L,t3 D,t4-7 L*4,t8-22 osc(U then (D,U)*7),t23 D,t24 U,t25 U(28,22),t26-28 L*3(28,4),t29-33 D*5,t34-35 R,R,t36 U(Y3),t37 D,t38-39 L,L,t40-43 U*4,t44 U(28,4),t45-47 R*3(28,22),t48-49 D,D,t50-51 R,R,t52-53 D,D(52,34),t54-55 R,R GOAL.
Verification signature post-press#5: my clocks L,L -> green STAYS at (22,58) (new program t1,t2 = L blk) = rebind OK; green does U,U = rebind failed.

## A585: PRESS#5 NO REBIND - PARITY THEORY DEAD
Rebind rule (fits all 5 presses): green rebinds at a press ONLY IF it completed >1 full loop of its current program since its last rewind (press/RESET). A422 unbound->bind; A435 exactly 1.0 loop->no; A474 16 ticks/period6=2.67->yes; A545/A585 15 ticks/period50=0.3->no.
Period-50 program makes rebind cost 50+ poisoned buffer ticks -> infeasible. BUT NO REBIND NEEDED:

## PLAN v6 - USE THE EXISTING BOUND PROGRAM (it's the v2 corridor run!)
Green's bound program (from A474) mirror: U,U,L*9,(D,U)*7 noops; period 50. Crossings at t4 (10,46) and t6 (10,34); Y2 toggle t8, Y1 toggle t11; bwd Y2-retoggle t42, Y1-retoggle t61 (loop2). Y2 open [8,42), Y1 open [11,61).
RESET (fresh badges; green keeps program). Walk L,L,U (on R2), PRESS#1 (3 ticks, no rebind; ghost_A=[L,L,U] parks R2 at t3). Walk L,L,U,L,L (to R1 seat; green t4 crossing held by parked ghost_A even as I step off - ghost stays!), PRESS#2 (5 ticks, no rebind; ghost_B parks R1 at t5). Green rewind at press#2 passes (10,46) backwards - assumed safe via faithful time-reversal (ghost_A was on plate at those ticks). VERIFY green alive after.
Traversal 39 ticks: t1 L,t2 L,t3 D(40,46),t4-7 L*4(40,22),t8 U(34,22)[Y2 toggles],t9 U(28,22),t10-12 L*3(28,4)[Y1 t11],t13-17 D*5(58,4),t18-19 R,R,t20 U(52,16 Y3),t21 D,t22-23 L,L,t24-28 U*5(28,4),t29-31 R*3(28,22)[<t42 ok],t32-33 D,D,t34-35 R,R(40,34),t36-37 D,D(52,34),t38-39 R,R(52,46) GOAL.
Total 50 actions. Batches: (1) RESET,L,L,U,A5,L,L,U,L,L,A5,t1-9. (2) t10-29. (3) t30-39.
Failure detectors: green missing after press#2 = rewind crush; my t9 blocked = Y2 didn't toggle.

## A588-607: PLAN v6 BATCH 1 — FULL SUCCESS
- Ghost_A parked (28,46) R2, ghost_B parked (28,34) R1. Green SURVIVED press#2 rewind (time-reversal safe).
- t9 U into (28,22) SUCCEEDED => green toggles Y latches CONFIRMED (Y2 opened at green t8).
- State A607: me (28,22), green (10,16) alive, timer 55, slots badge3 only left.
- Submitted batch 2 (t10-29): L*3 -> (28,4) [Y1 opens t11, arrive t12], D*5 -> (58,4), R,R -> (58,16), U press Y3 (52,16), D, L,L -> (58,4), U*5 -> (28,4), R -> (28,10).
- Next: batch 3 (t30-39): R,R (28,22 at t31 < Y2 close t42), D,D (40,22), R,R (40,34), D,D (52,34), R,R -> GOAL (52,46). Score -> 6.

## A608-627: BATCH 2 SUCCESS + MODEL FIX
- Y3 pressed t20 (A618, latch persists). Me (28,10) at t29. Timer 45.
- CORRECTION: blocked program inputs are SKIPPED (no tick), not noops. Green loop period=22:
  fwd U,U,L*9 (t1-11), bwd undo (t12-22 back to spawn). Y2 toggles at 8,14,30,36,... Y1 at 11,33.
- Y2 re-closed at t14; blob confirmed extended at (28,22) on A627 board.
- Batch 3 (t30-39): R(28,16) [green reopens Y2 same tick], R(28,22), D,D(40,22), R,R(40,34), D,D(52,34 via Y3-opened pocket), R,R -> GOAL (52,46). Expect score 6.

## A628-637: LEVEL 6 SOLVED (score 6 at A637). Winning life = 50 actions total.

## LEVEL 7 INITIAL (board at A637)
- Me (28,28). Green (58,22): confined to bottom row-58 corridor (cols 4-22) + col-4 tower up to purple plate A (28,4), gated by YELLOW blob (40,4).
- Goal: blue box rows 48-55 cols 31-39, marker (52,34), entry from east (52,40) moving L.
- RED worm (spring): plate (4,16), pipe row 4, blob (4,34). Blob blocks (10,34)<->(4,40) top corridor to purple plate B (4,52).
- YELLOW worm (latch): plate (40,22) [I can reach via (40,28)], pipe row 40, blob (40,4) blocks green's tower.
- PURPLE (new): pad A (28,4) pipes to box1 (16,16) + box2 (28,16); pad B (4,52) pipes to box3 (40,52) + box4 (52,52). Boxes = 7x7 outlines, sealed 5x5 interiors at grid centers.
- Red plate area {(4,16),(10,16),box1(16,16)} isolated — only via box1. Goal approach (52,40) only via box4/(52,46)/(52,52); col-52 shaft passes THROUGH box3 (40,52).
- Grid passability map (centers 4..58, # blocked):
  r4: 16=Rplate 34=Rblob 40. 46. 52=padB | r10: 16. 34. | r16: 16=box1 28. 34. 40. 46. 52. | r22: 40. 52. | r28: 4=padA 16=box2 22. 28=me 40. 52. | r34: 4. 28. 40. 52. | r40: 4=Yblob 22=Yplate 28. 34. 40. 52=box3 | r46: 4. 22. | r52: 4. 40. 46. 52=box4 34=goal | r58: 4. 10. 16. 22=green
- Hypotheses: purple pads teleport to piped chamber, OR open chamber doors. Yellow toggle frees green's tower. Green program likely unbound (fresh level).
- PROBE (A638-639): L,L — test entering box2 from (28,22) through outline.

## A638-639 PROBE RESULTS
- Chamber outlines DO NOT block me: I entered box2 (28,16). No teleport/diff on entry.
- GREEN LIVE-MIRRORS my moves when unbound (fresh level): my L->green L. Green now (58,10).
- BFS proven: live-mirror cannot achieve {me in box2 + green on padA} — my U drags green down tower.
- L7 topology: padA green-only; red plate cul-de-sac {(4,16),(10,16),box1} box1-only; goal region {(52,40),(52,46),box4} box4-only; box3 dead-ends col-52 shaft. Teleports REQUIRED.
- EXPERIMENT (26 moves, 2 batches): choreography -> green parked padA (28,4), me (40,28), yellow toggled once (blob retracted, green tower crossed safely).
  Batch1 (A640-659): R,R,D,D,L[Ytoggle],R,R,R,U,U,U,U,R,R,L,L,L,U,D,R -> me (16,40), green (52,4).
  Batch2: D,D,D,D,L,L -> me (40,28), green (28,4) PAD A at tick 24. Watch board diffs at pad arrival!
- Post-arrival: green stays on pad iff I avoid U (my U->green D only dislodger).

## A640-659: GREEN IS PRE-BOUND, PAD = TELEPORT TUBE
- Green does NOT mirror me. It came pre-bound with program [L,L,L,U,U,U,U,U] from spawn (58,22),
  ping-pong loop, one tick per my successful move, blocked inputs skipped. Reaches pad A (28,4)
  at forward-pass end; period 16 when tower open (yellow retracted — done, parity 1, persists).
  Pad touches at ticks t16 (observed, A655), t32, t48... (t counted from A640; t20=A659).
- A655 (green lands pad A): 26-frame animation — transient purple TUBE grows between box1 and box2
  (rows 20-24, walls cols 15&17, floor col 16), then dissolves within same tick. Settled = no change.
  Interpretation: pad activation = teleport conduit between its two boxes; fired empty (box2 empty).
- My positions: t20 me (16,40), green (52,4) descending. Yellow blob retracted (latch, parity 1).
- TEST (A660-671, t21-32): D,D,D,D,L,L,U,U,L,L (to box2 t30), R (t31), L (t32 = re-enter box2 exactly
  as green lands pad A). Expect: teleport me box2->box1 (16,16). If not, bounce R,L keeps me
  in-box2-on-even-ticks for t48 touch; and rethink (maybe need to be inside before activation).
- If teleported: walk U,U -> red plate (4,16). Then red retraction, pad B (4,52), box3/box4 for goal.

## A660-671: TELEPORT CONFIRMED
- Entered box2 exactly on green's pad-A touch (t32) -> teleported to box1 (16,16). Sync mechanic proven.
- Green pad-touch schedule: every 16 ticks once tower open (touches at t8+16k if yellow toggled by t5).

## MASTER PLAN v1 (3 stages, post-RESET; each press <=16 green-ticks to avoid rebind):
- S1 (10 ticks): D,D,L(Ytoggle t3),R,U,U,L,L(box2 t8=green pad t8, teleport box1),U,U(red plate t10). PRESS#1.
  Ghost1 replays identically (re-toggles yellow t3, teleports t8), parks RED PLATE t10 forever.
- S2 (14 ticks): direct D,D,R,R,U,U,U,U,L,U,U(4,34 at t11; red open from ghost1 t10),R,R,R(pad B t14). PRESS#2.
  Ghost2 parks PAD B at its t14.
- S3 (17 ticks, no press): D,D,R,R,U,U,U,U,R,R,D,D,D,D = box3 (40,52) at t14 EXACTLY when ghost2 lands
  pad B -> tube box3<->box4 -> teleport to box4 (52,52). Then L,L,L -> GOAL (52,34).
- OPEN RISKS: (a) ghost/player same-cell collision (S2 overlaps ghost1 at t1,t2; S3 overlaps both);
  (b) RESET must restore green's default program after rebind.
## LAB (this sacrificial life, green already >1 loop => press WILL rebind):
- A672-678: U,U (red plate t33-34: confirm spring retract), PRESS (rebind + ghost spawns replaying my
  36-input life), then L,L,R,R deliberately overlapping ghost path (ghost t1 (28,22), t2 (28,16)).
- Next call: check overlap outcome, rebind evidence, then RESET and verify green program restored.

## A672-678 LAB RESULTS (all green-lights)
- Red spring CONFIRMED (blob retracts while plate held: comp 46->30 at A673).
- Press A674: ghost replays stacked under me — NO collision, overlap fine (596 block signature).
- NO REBIND: green kept default [L,L,L,U,U,U,U,U] after press despite many loops. Designed programs
  seem rebind-immune in L7. Stage-length constraint VOID.
- Badges restore on RESET (A672 slots full before this press).
## EXECUTING MASTER PLAN v2 (44 actions total):
- Batch1 (A679-698): RESET, S1=[D,D,L,R,U,U,L,L,U,U] (box2@t8 sync, box1, red plate@t10), PRESS#1,
  then S2 t1-8: D,D,R,R,U,U,U,U (-> (16,40)).
- Batch2 (20): S2 t9-14: L,U,U(4,34 t11; red open ghost1-park t10),R,R,R(pad B t14), PRESS#2,
  then S3 t1-13: D,D,R,R,U,U,U,U,R,R,D,D,D.
- Batch3 (4): D (box3 t14 = ghost2 pad-B landing -> teleport box4), L,L,L -> GOAL (52,34). Score 7.
- Verify after batch1: ghost1 parked (4,16), red retracted, me (16,40), green (16,40-tick=t8... green pos (10,58)-ish path), slots badge1 used.

## A679-698: MASTER PLAN BATCH 1 PERFECT
- S1 executed, press#1 done, ghost1 replay verified (teleported into box1 at its t8, A698 blk 1895).
- Me (16,40) at S2-t8; green (28,4) pad touch t8; red will open at ghost1-park t10.
- Batch2 (A699-718): L,U,U(4,34@t11),R,R,R(padB@t14),PRESS#2,then S3 t1-13 D,D,R,R,U,U,U,U,R,R,D,D,D.
- Batch3: D (box3@t14 = ghost2 padB landing -> teleport box4), L,L,L GOAL.
