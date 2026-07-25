# Game notes

## Level 1 initial state (Action 0)
- Row 0: full Green 'I' line (timer bar?)
- 'q' off-black 4x3 @ x36-39,y1-3 above 'C' magenta 4x4 @ x36-39,y4-7 (falling piece?)
- Blue 'f' 20x4 bar @ x12-31, y16-19 (paddle?)
- Yellow 'G' U-shaped cups: x16-27 and x40-51, rows 52-59 (goals?)
- Off-white '8' floor rows 60-63

## Mechanics learned
- ACTION3/4 move blue bar 4 cells per press (bar is 20 wide, rows 16-19).
- ACTION5: magenta beam grows down from emitter (x36-39, fixed) 4 rows/frame to floor y59, cups flash white, bar flashes red, then all reverts = MISS.
- Timer row 0: 2 green cells consumed per action → ~32 action budget.
- Cup holes (interior): cup1 x20-23, cup2 x44-47, rows 52-55.
- NOTE: grep -n is 1-indexed; use marker_line0+1..+65 for boards.

## Beam split mechanic (Turn 3 discovery)
- Beam falls from emitter; when it hits the bar it spreads over bar top (bar width +4 each side) and splits into two 4-wide streams falling at (barLeft-4..barLeft-1) and (barRight+1..barRight+4).
- Streams that hit cup prong tops split again around the prong; cups flashed maroon '>' = fail; floor flashes green.
- Streams entering holes fill them but landing on prongs = miss (everything reverts).
- SOLUTION GEOMETRY: bar at x24-43 → left stream x20-23 = cup1 hole, right stream x44-47 = cup2 hole.

## Level 1 SOLVED (Action 8, score 1): bar x24-43 + ACTION5, both streams into holes.

## Level 2 layout (board at log line 4969, 0-idx)
- 3 inverted cups top: cup1 x12-23 (hole x16-19), cup2 x28-39 (hole x32-35), cup3 x44-55 (hole x48-51); holes open downward, rows 8-11.
- Red blocks: A x8-19 y16-19 (shields hole1), B x28-39 y24-27 (shields hole2).
- Bar x20-39 y36-39; emitter x40-43 fires UP from y56.
- Only hole3 has clear vertical path. Bar x28-47 → right stream x48-51 = hole3.
- Open questions: do holes fill cumulatively across shots? Do ACTION1/2 move bar vertically? Are red blocks destructible/clickable (ACTION6)?

## Flash semantics (confirmed via L1 success + L2 shot)
- Maroon '>' cup = beam filling it (GOOD). White '$' cup = missed this shot (BAD).
- Win condition: ALL cups filled in a SINGLE shot. Board reverts after every shot regardless.
- Streams fire sequentially in animation (right first, then left) but both count.
- L2 shot @bar x28-47: hole3 filled (maroon), cups1-2 white → need 3 simultaneous streams.

## Paddle system (Turn 5 discovery)
- ALL red blocks are paddles. ACTION6 click selects one (turns blue 'f'); previously selected turns red 'n'.
- Arrows move selected paddle 4 cells/press in all 4 directions (ACTION1 up, ACTION2 down).
- Split rule (beam from below): spread on impact side (4 rows below paddle), width = paddle ±4; two 4-wide streams rise alongside at [L-4..L-1] and [R+1..R+4].
- 12-wide paddle at xL..L+11 splits incoming into L-4..L-1 and L+12..L+15.

## L2 solution attempt (turn 6)
- W 20-wide at x28-47 y32-35 (already placed): beam→streams x24-27, x48-51(hole3).
- Move block A (12-wide) from x8-19,y16-19 to x20-31,y12-15: left stream x24-27 splits → x16-19(hole1), x32-35(hole2).
- Actions: click A (12,17), right x3, up x1, fire.

## L2 SOLVED (Action 20, score 2) — cascade split confirmed working.
- IMPORTANT: streams touching cup prongs = fail; must enter holes cleanly.

## L3 layout & plan (turn 7)
- Cups: H1 x8-11, H2 x28-31, H3 x52-55. Emitters: E1 x4-7, E2 x36-39, E3 x56-59 (all fire on ACTION5).
- Paddles: w16 x8-23 y20-23; w20 x40-59 y28-31; w24#1 x8-31 y32-35; w24#2 x36-59 y40-43 (blue).
- Target: A=w16 x12-27 y16-19 (→H1+H2); B=w20 x32-51 y24-27 (E2→H2+H3); C=w24#1 x0-23 y36-39 (E1→feeds A via x24-27); D=w24#2 x40-63 y44-47 (E3→feeds B via x36-39).
- Off-board branches (C left, D right) assumed harmless.
- Sent 14-action sequence ending in ACTION5.

## L3 SOLVED (Action 34, score 3). Off-board branches harmless. Duplicate streams into same hole OK.

## L4 layout & plan (grid unit = 3 now; assume moves are 3/step — VERIFY)
- Beam falls from x23-25 (emitter top). Cups y53-58: holes x11-13(c1), x29-31(c2), x41-43(c3), x53-55(c4).
- Paddles: f15 [17,31] y17-19 (top, catches beam — don't move); n15 [38,52] y17-19; q-paddle 21w [8,28] y29-31 with pass-through center (q) at [17,19]... center = L+9..L+11; 12A [44,55] y32-34; 12B [38,49] y41-43.
- PLAN: n15 → [14,28] y23-25 (click(40,18), down2, left8): splits S1 x14-16 → x11-13(c1)+x29-31(c2).
  q → [32,52] y44-46 (click(10,30), down5, right8): S2 x32-34 → edges x29-31(c2)+x53-55(c4), center pass x41-43(c3). 12A/12B stay (above q, not in fall paths).
- Batch1 (sent, 20 acts): n15 full; q down5 + right3 (at [17,37] y44-46 after). Batch2: right x5, ACTION5.
- q-center pass-through is UNTESTED assumption; verify on fire.

## L4 fire #1 FAILED — new physics rule
- Spread propagates along impact-side rows (3 rows before paddle) and is BLOCKED by objects in those rows: 12B at y41-43 stopped q-paddle (y44-46) spread at x38 → no right-edge stream → cup4 unfilled.
- CONFIRMED: q-center pass-through works (cup3 got stream through the gap). Cups 1,2,3 filled ✓.
- Fix sent: click 12B (40,42), up 1 (→y38-40), re-fire. Keep spread rows of every paddle clear!

## L4 SOLVED (Action 63, score 4).

## L5 layout & plan
- Cups top (holes): c1 x20-22, c2 x38-40, c3 x50-52. Sideways wall cup: recess x8-10 y38-40 (prongs y35-37,y41-43 at x8-10).
- Emitters UP: E1 x20-22, E2 x44-46. Paddles: n9 [20,28]y32-34, 12w [29,40]y20-22, f15 [41,55]y32-34(blue). Purple deflector: bar x32-37 y41-43, foot x35-37 y44-46 (bends rising stream left, exit at bar rows — assumption).
- PLAN: f15→[23,37]y26-28 (up2,left6 — no click, already selected); 12w→[38,49]y47-49 (click(30,21),right3,down9); n9→[17,25] (click(22,33),left1); deflector up1 (click(33,42),ACTION1) → exit y38-40; fire.
- Streams: E1→n9: x14-16 STRAY(ceiling, tolerance test!), x26-28→f15→x20-22(c1)+x38-40(c2). E2→12w→x35-37(deflector→wall cup)+x50-52(c3).
- Batch1 sent (20): f15 done; 12w click+right3+down8 (1 down step remains).
- Batch2: ACTION2, click n9, ACTION3, click deflector, ACTION1, ACTION5.

## L5 fire #1 FAILED — deflector exit rows = FOOT rows (not bar rows)
- Deflector bends rising stream 90° left; exit stream travels at the FOOT's y-rows.
- Exit at y41-43 hit wall-cup lower prong (maroon fail). All 3 top cups DID fill ✓.
- Ceiling stray x14-16 tolerance still unknown (this fail explained by prong hit).
- Horizontal streams hitting vertical obstacles split vertically (recess got partial C + below-stray).
- Fix sent: deflector up 1 more (foot y38-40), re-fire.

## CONFIRMED RULE: any stream hitting floor/ceiling/wall = green flash = FAIL. Zero strays mandatory.
## L5 fire #2: all 4 cups filled cleanly but ceiling stray x14-16 caused fail (ceiling flashed green).

## L5 design v4 (zero strays, sent as 19 actions):
- Deflector foot → x20-22 y38-40 (5 lefts; was selected): E1 beam → deflected left y38-40 → recess x8-10 ✓.
- n9 → [41,49] y32-34 (click(18,33), 8 rights): catches x47-49 → {x38-40 c2, x50-52 c3}.
- 12w → [35,46] y41-43 (click(40,48), 1 left, 2 up): E2 first hit → {x32-34 → f15, x47-49 → n9}.
- f15 stays [23,37] y26-28: catches x32-34 → {x20-22 c1, x38-40 c2 dup}.
- Then ACTION5. All leaves = cups. Timer: 45 cells left, ~13 needed ✓.

## CRITICAL RULE: selection RESETS after ACTION5 (fire). ALWAYS ACTION6-click the paddle before moving it post-fire!
## L5 fire #3 failed because 5 lefts moved the still-selected 12w, not the deflector. State after action 111:
- f15 [23,37] y26-28 ✓correct; n9 [38,46] y26-28; 12w [23,34] y47-49; deflector bar x32-37 y35-37 / foot x35-37 y38-40.
## L5 fix batch (18 acts): click defl(33,36)+5L (foot→x20-22); click n9(42,27)+1R,2D (→[41,49]y32-34); click 12w(25,48)+4R,2U (→[35,46]y41-43); fire. Timer 33 left.
## L5 SOLVED (Action 129, score 5).

## L6 layout (settled board at log line 29578 0-idx; unit=3; walls x0-4/x59-63; timer 64 full)
- Emitter DOWN x29-31 (q y2-4, C y5-7).
- Blue L-paddle (selected): stem x29-31 y17-19 + base x29-34 y20-22 (base extends RIGHT). In beam path!
- Vertical red paddle: x44-46, y14-25 (3w x 12t) — NEW type, untested.
- Left wall cups (open right): recess x8-10 y23-25 (prongs y20-22/y26-28); recess x8-10 y38-40 (prongs y35-37/y41-43).
- Right wall cup (open left): recess x53-55 y32-34 (prongs x53-58 y29-31/y35-37).
- q-center paddle 15w [23,37] y32-34, pass-through center x29-31 (under emitter). Edge streams would be x20-22, x38-40.
- Purple deflector INVERTED vs L5: stem x32-34 y44-46 (top), bar x29-34 y47-49 (below, extends left) — catches falling x32-34?, exit rows unknown.
- Bottom cup opens UP: hole x29-31 y53-55, prongs x26-28/x32-34, base y56-58.
- 4 targets: hole x29-31 (falling), left recesses y23-25 & y38-40 (leftward streams), right recess y32-34 (rightward stream).
- Turn 17 probe: single ACTION5 with initial config to observe L-paddle / downstream behavior.

## L6 probe results (Action 130, frames at 29654+65*(f-1), f=1..30)
- "Blue L-paddle" is a PURPLE DEFLECTOR (U) — was blue because selected. Selected objects render blue!
- CHUTE RULE (both confirmed): falling stream landing on deflector BAR beside the stem flows AWAY from stem, at the 3 rows ABOVE the bar (= stem rows), starting at bar_edge±1. No spread, no strays from landing.
- Stem-tip dead-on hit = messy 3-way (spread ±3 both sides + center re-emerges below q gap). AVOID stem-tip hits.
- Vertical paddle V (3w x 12t): horizontal stream hitting its side → spread along 3 impact-side columns spanning ±3, outputs = 2 horizontal streams SAME direction at rows (top-3..top-1) and (bottom+1..bottom+3). Confirmed rightward; leftward assumed by mirror.
- Off-center hit on q-paddle = plain 2-edge split, NO center pass. Aligned hit = 3-way (L4).
- Timer rate L6 = 1 cell/action (63 left after probe).

## L6 SOLUTION (design A, 40 actions in 2 batches):
Final positions: Q [23,37] y20-22 (gap x29-31); U stem x35-37 y32-34 + bar x35-40 y35-37; D stem x23-25 y32-34 + bar x20-25 y35-37; V x14-16 y26-37.
Routing: beam→Q gap pass→bottom cup T1; left edge x20-22 falls→D bar→left y32-34→V→left y23-25 (T2 recess) + y38-40 (T3 recess); right edge x38-40 falls→U bar→right y32-34→T4 right recess.
Order (transit-collision-free): U 3R; Q 4U; V 4D+10L; D 3L+4U; U 5D+1L; fire.
- B1 (20): 6(30,18),4R x3, 6(24,33),1U x4, 6(45,20),2D x4,3L x6.
- B2 (20): 3L x4, 6(30,48),3L x3,1U x4, 6(39,18),2D x5,3L x1, ACTION5.
Clicks: U orig (30,18); Q (24,33); V (45,20); D (30,48); U-after-3R (39,18).

## Tests
- Turn 1: ACTION3 (bar moved left 4, x12-31→x8-27), ACTION5 (beam miss).
- Turn 2: bar at x8-27. Sent ACTION4 x3 (bar→x20-39, covers beam x36-39) + ACTION5 to test bar-beam interception.
