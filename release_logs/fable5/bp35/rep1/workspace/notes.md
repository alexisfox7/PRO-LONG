# Game notes

## Level 1 initial analysis (Action 0)
- 64x64. Background: black 'O' with gray 'h' stars. Row 63: white '$' bar.
- Water regions (light blue '('):
  - A: rows 0-11, cols 31-53 (top right)
  - B: rows 19-29, cols 13-53
  - C: rows 37-62, cols 13-53
  - Vertical channel rows 30-36, cols 43-47 connects B <-> C
- Ship: 5x5 bounding box at cols 19-23, rows 37-41, at TOP of region C (buoyant?).
  Blue 'f' diamond + yellow 'G' at right edge (cols 22, rows 38-39) — faces right.
- Green 5x5 blocks ('I' with 'h' corners):
  - 3 blocks rows 1-5 at cols 13-17, 19-23, 25-29 (left of region A)
  - 4 blocks rows 13-17 at cols 31-35, 37-41, 43-47, 49-53 (above region B)
  - Purpose unknown: goals? move counter?
- Channel width 5 = ship width 5. Exact fit.

## Hypothesis
Ship floats to ceiling of water region. Move right to align with channel
(cols 43-47), rise into B, then find route to A. Testing ACTION4 x2 to
measure step size.

## Confirmed mechanics (after Actions 1-2)
- ACTION4 moves ship RIGHT by exactly 6 columns (colored bbox 20-22 -> 26-28 -> 32-34).
- Ship stays at ceiling of region C (buoyant, y bbox 37-40 unchanged).
- Bottom row 63 is a STEP BUDGET bar: white '$' cells turn purple '"' left-to-right,
  1 per action. 64 cells total => likely 64-action budget per level.
- Channel at cols 43-47; ship colored bbox must be 44-46 (gap 43-47) to align.
- Ship x-positions reachable from start (step 6): 20,26,32,38,44,50 -> 44 aligns!

## Confirmed (after Actions 3-4)
- Aligning ship under open channel triggers AUTO-RISE (24-frame animation).
- Camera follows ship: world scrolled down 18 rows; ship always drawn at rows 37-40.
- Current screen layout (after rise into region B):
  - rows 0-5: top water region (cols 13-53, full width)
  - rows 7-11, 13-17, 19-23: green blocks cols 13-29 (3 per row-band, left side)
  - rows 13-29: region A water (cols 31-53)
  - rows 31-35: 4 green blocks (cols 31-35,37-41,43-47,49-53) = PLUGS between B and A
  - rows 37-47: region B (ship at top, cols 44-46)
  - rows 48-54: channel we rose through (cols 43-47)
  - rows 55-62: region C below
- Green 5x5 blocks are channel-width -> hypothesis: they plug channels; maybe click removes them.
- Ship x bbox currently 44-46, directly under green block at cols 43-47. No auto-rise (blocked).
- Budget bar: 4 purple after 4 actions.

## Confirmed (after Action 5)
- CLICK on green block DISSOLVES it (shrink animation) and opens full channel
  including 1-px boundary rows. Ship auto-rises if channel is above it.
- Ship rose into region A. Camera keeps ship at screen rows 37-40; world scrolls.
- Clicks use SCREEN coords -> never plan clicks after an expected scroll (rise).
- Left/Right moves are 6 cols per press, scroll-independent.
- Board after Action 5 (screen coords):
  - rows 1-29 cols 13-53: huge top water region, with black island rows 12-18
    cols 24-42 containing 3 green blocks (rows 13-17, cols 25-29/31-35/37-41)
  - cols 13-29, rows 31-47: 3x3 grid of 9 green blocks (bands 31-35,37-41,43-47)
  - ship region A: water cols 31-53 rows 37-53, ship bbox 44-46
  - below: old plugs rows 55-59 (43-47 removed), region B water rows 61+
- Budget: 5/64 used.

## Actions sent
- Turn 1: ACTION4 x2 (probe) -> ship 32-34
- Turn 2: ACTION4 x2 -> ship 44-46, auto-rose into region B
- Turn 3: ACTION6(45,33) -> plug dissolved, rose into region A
- Turn 4: click(27,39) open pocket W of A; L x3 into pocket (bbox 26-28);
  click(27,33) open upward channel -> rise to under island; L x1 (bbox 20-22)
  -> clear island west edge, auto-rise to surface. ALL WORKED. Total scroll +36.

## After Action 11 (11/64 budget)
- Ship faces movement direction (yellow G tip flips to leading side).
- Ship at ceiling of top region, gap cols 19-23, screen rows 37-41.
- NEW: magenta 'z' diamond (3x3 + tips) at rows 19-21, cols 20-22 — floats at
  ceiling of the NEXT region up (rows 19-29). Probably the GOAL (dock/rescue?).
- 3 plugs between ship region and magenta region: rows 31-35, cols 31-35/37-41/43-47.
- No plug/channel at ship's current column (19-23).

## Actions sent Turn 5
- R x2, click(33,33), L x2 -> reached magenta -> LEVEL 1 CLEARED (Score 1
  at Action 16, 16 actions total). Goal = dock ship with magenta creature.

## LEVEL 2 (starts Action 16 state, budget reset to 0/64)
- Ship gap cols 19-23 rows 37-41, top of big water region (rows 37-62, cols 13-53).
- Rows 31-35: full row of 7 plugs (cols 13-17..49-53, step 6).
- Rows 25-29: second full row of 7 plugs.
- Rows 13-23: left chamber water (cols 13-29); black cols 30-36; right water
  column cols 37-53 spans rows 0-23 -> continues off-screen above.
- Rows 7-12: three purple towers (cols 14-16, 20-22, 26-28, rows 7-11) with
  'G$G' bases at row 11, thin 1-wide water channels at cols 18, 24 (rows 7-12).
  Towers sit above left chamber. Purpose unknown (goal? city?). No magenta visible.

## Turn 6 result: FAILURE - LEVEL RESET (Attempt 2)
- Action 17 click(21,33): worked, ship rose +6 into vacated plug slot.
- Action 18 click(21,33): ship rose +18 into left chamber, reached ceiling
  directly under MIDDLE TOWER (cols 20-22) -> ship DISSOLVED (death anim)
  -> auto reset as "Action 19 / Attempt 2" (3 actions burned total).
- LESSON: rising into a slot under a purple tower KILLS the ship (or towers
  are delivery points that reject an empty ship). AVOID tower columns.
- Revealed territory above (from A18 boards, original-level coords):
  - rows -17..-13: plugs at cols 13-17, 43-47, 49-53
  - rows -11..-7 and -5..-1: plug bands at cols 13-35 (4 wide)
  - cols 37-41 clear above right column at least to row -18.
- Magenta likely somewhere up the right column / above area.

## Turn 7 result: SUCCESS - ship rode right column up (+48 scroll, A20-24, 5 plugs used... 10/64 budget)
## Board after A24 (screen coords):
- Ship slot cols 37-41, gap rows 37-41, top of right column (cols 37-53).
- Rows 31-35: plugs at 13-17, 37-41, 43-47, 49-53.
- Rows 13-18: SECOND TOWER SET at cols 38-40, 44-46, 50-52 (G$G row 17),
  thin channels cols 42, 48. Towers cap ALL right-side slots -> death traps.
- Upper region: rows 19-29 full width 13-53; LEFT PART (cols 13-36) extends
  up to rows 13-18 too -> ceiling row 12, NO towers above (black rows 1-11
  except plug pair at cols 31-35, rows 7-11 and 1-5) -> safe rise at 13-17.
- 4x2 plug grid rows 37-47, cols 13-35 (embedded in black, carveable).
- First tower set now at rows 55-59; left chamber rows 61+.
- World map so far is one tall vertical shaft system; more unknown above row 0.

## Turn 8 result: SUCCESS (A25-37, 18/64 budget). Ship between plug pair at cols 31-35.
## Board after A37:
- Plug above ship: rows 31-35, cols 31-35 (upper of pair). Safe above (black at 13-17 over col 31-35).
- Region rows 19-29 (cols 13-53) with a tower embedded at right (cols 50-52, rows 19-23).
- Plug row rows 13-17: cols 13-17, 19-23, 25-29.
- Water band rows 7-11 full width.
- Rows 1-5: SIX towers (14-16,26-28,32-34,38-40,44-46,50-52) + 7-WIDE WATER
  CHANNEL at cols 18-24 = the ship-sized door upward. Thin channels 30,36,42,48.
- First/second tower sets far below now.

## Turn 9 result: SUCCESS (A38-41, 22/64 budget). Ship rose through wide channel,
now INSIDE six-tower row at slot cols 18-24 (gap 19-23), rows 37-42 screen.
Horizontal movement blocked by towers.
## Board after A41 (screen coords):
- Plug stack col 19-23: rows 31-35, 25-29(part of full row), 19-23, 13-17
  -> leads to water band rows 7-11, but tower 20-22 (rows 1-5) above = DEATH.
- Full plug row rows 25-29: cols 19-53 (6 plugs) = horizontal corridor.
- Plug stack col 49-53: rows 25-29, 19-23, 13-17 -> water band 7-11 -> ceiling
  row 6 at cols 31-53 is WATER (top-right region rows 0-6, cols 31-53) = SAFE.
- Third tower set rows 1-5 at cols 14-16, 20-22, 26-28 (left only).
- Budget 22/64.

## Turn 10 result: SUCCESS (A42-54, 35/64 budget!). Ship in right stack gap 49-53,
one plug above (rows 31-35). Corridor row fully dissolved (now water, rows 43-47).
## Board after A54:
- Above plug: full-width water band rows 25-29; right region rows 13-24 (cols 31-53);
  ceiling row 12 has opening at cols 31-41 into higher band rows 7-11 (cols 13-41);
  plugs at 43-47 & 49-53 (rows 7-11); FULL 7-plug row at rows 1-5; unknown above.
- Third tower set at rows 19-23 (cols 14-28, left side of right region).
- BUDGET WATCH: 35 used, 29 left. Be efficient.

## Old actions Turn 10 (13 actions)
- click(21,33) x2 (rise 2 plugs into corridor row, scroll +12 total)
- then corridor eastward: [click(27,39),R] x5 slots (25-29,31-35,37-41,43-47,49-53)
  using coords (27,39),(33,39),(39,39),(45,39),(51,39) with R after each
- click(51,33): dissolve first stack plug above (rise +6)
- STOP: verify no tower above col 49-53 before final rise (12 rows revealed).

## Turn 11 result: SUCCESS (A55-57, 38/64). Ship at gap 37-41 under full 7-plug row.
## MAGENTA SPOTTED: rows 19-21, cols 32-34 (slot 31-35), ceiling of region
rows 19-29. No tower above slot 31-35 (4th tower set at cols 38-52). 
## Actions sent Turn 12 (2 actions): L (gap 31-35), click(33,33) -> rise into
magenta from below -> expect LEVEL 2 CLEAR (Score 2).

## Old actions Turn 11 (3 actions)
- click(51,33): dissolve last right-stack plug -> rise +24 (top row 37->13), scroll +24.
- L x2: gap 49-53 -> 43-47 -> 37-41; at 37-41 ship fits row-12 opening (31-41)
  -> auto-rise +6 into band rows 7-11. Total scroll +30.
- Next turn: full plug row will be at screen rows 31-35; unknown territory
  revealed above. Choose safe column, click (x,33) to rise.

## LEVEL 2 CLEARED at Action 59 (Score 2). Docking from below worked.

## LEVEL 3 initial (budget 0/64)
- Ship gap 19-23, rows 37-41, lower region (rows 37-62, cols 13-53).
- ORANGE blocks (new!): two 5x5 at cols 31-35, rows 37-41 & 43-47, floating
  at lower-region ceiling. They BLOCK the top lane at cols 31-35.
- Green plugs: band rows 31-35, cols 37-41/43-47/49-53 (right side only);
  cols 13-36 of that band is solid black.
- Upper region rows 0-29: X-marks (orange dots, 3x3 checker) at rows 8-10,
  centers x=21,27,33 (slots 19-23/25-29/31-35). Theory A: targets where
  orange blocks rest (block at ceiling row 6 spans rows 7-11 only if ceiling
  black there — but row 6 is water at 13-36, black 37-53...). Theory B: mines.
- Top edge: teeth at cols 19-41 row 0; open exits above at cols 13-18, 42-53.
- Upper-right ceiling row 6 (cols 37-53); left part open to row 0.
- No magenta visible; must be off-screen (above?).

## Turn 13 probe: R, R -> stand adjacent (25-29) then try PUSH orange block.
Outcomes: push -> block to 37-41; blocked -> ship stays; then reassess.
ACTION7 = Undo (never tested) available as safety.

## Turn 13 result (A60-61, 2/64): push FAILED. Ship stopped adjacent (gap 25-29).
Orange blocks NOT pushable by movement.
## Turn 14 probe: click(33,39) x2 on orange stack top. Theories: dissolve
(like green) or buoyancy-toggle (sink). Either way lane 37-41 clears; second
click handles lower block after it floats up. Watch animation to distinguish.

## Turn 15 (after A62-63, budget 4/64): KEY MECHANIC FOUND
- Orange blocks are CLICK-TOGGLES: click dissolves full block -> 5-cell X-mark residue (checkerboard, rows 38-40 cols 32-34); click again REGROWS to full. My 2-click probe undid itself (A62 opened, A63 closed).
- X-marks at rows 8-10 (centers x=21,27,33) = orange blocks in dissolved state; presumably passable, clickable to grow.
- No spontaneous regrowth between actions (stable toggle).
- L3 topology: ship slots 13-17..49-53. Left column (13-24) dead end (no channels above). Right column (37-53) has 3 green plugs (cols 37-41,43-47,49-53, rows 31-35) up to big upper region rows 13-29 (cols 13-53). Above that, only cols 13-35 continue up (rows 6-12, contains X-marks) to rows 1-5 (cols 13-53), then row-0 exits: cols 13-18 (slot 13-17) and 42-53 (slots 43-47,49-53). Magenta off-screen above.
- Turn 15 plan: click(33,39) toggle block OFF, ACTION4 into slot 31-35 (tests X-residue passability - RISK: unknown if entering X toggles growth/kill), ACTION4 to slot 37-41, click(39,33) open first plug -> rise to upper region + scroll.
- If reset happens mid-list: leftover actions are benign (ACTION4s + plug click from start slot 19-23 are safe/no-ops).

## Turn 16 (after A64-67, budget 8/64): plan WORKED - X-residue is PASSABLE, ship rose thru plug channel, scroll +24
- Ship now slot 37-41 (screen rows 37-41), region rows 37-53 (cols 13-53). Shaft cols 13-35 (rows 30-36, X-marks rows 32-34 centers x=21/27/33) leads to region rows 25-29.
- DANGER: 4 purple towers rows 19-23 at cols 20-22/26-28/32-34/38-40 sit on teeth row 24 -> slots 19-23/25-29/31-35/37-41 at rows 25-29 are DEATH (settle under tower). Slot 13-17 rises safely thru teeth opening 13-18, up narrow shaft rows 13-23, to region rows 7-11 (ceiling row 6 black at cols 13-18).
- Region rows 1-5: pocket cols 19-29 (capped row 0), orange blocks FULL at 31-35 & 37-41 rows 1-5, then cols 43-53 open with row-0 EXIT cols 43-53.
- STRATEGY: toggle 3 shaft X-marks ON (blocks at 19-23/25-29/31-35 rows 31-35) = ceilings so ship can traverse rows 37-41 leftward w/o auto-rise into tower deaths. Toggle both rows-1-5 orange blocks OFF now (clicks (33,3),(39,3)) while screen coords valid. Then ACTION3 x4 -> slot 13-17 -> big auto-rise to rows 7-11 + scroll ~30.
- NEXT TURN: ship at slot 13-17 rows 7-11 (screen 37-41). Plan: ACTION4 (19-23, rises to pocket rows 1-5, +6), then ACTION4 x4 across rows 1-5 (25-29, 31-35 X, 37-41 X, 43-47) -> rise thru row-0 exit off-screen. Verify no towers above exit after scroll before final rise!

## Turn 17 (after A68-76, budget 17/64): all 9 executed, ship rose left shaft, scroll +30. Ship slot 13-17 rows 37-40 (alcove, ceiling row36 black cols13-18), facing LEFT.
- WORLD MAP (current screen): R5 body rows 30-41 cols 19-53 water (+alcove 13-17 rows 37-41). Pocket cols 19-30 capped row 29 (black). Cols 31-41 water up to teeth row 24 (openings 1px at 24/30/36; teeth blocks 19-23/25-29/31-35/37-41). Upper tower pair rows 19-23 at cols 32-34, 38-40 (DEATH under slots 31-35/37-41). Right side cols 42/43-53 water continuous rows 13-41 -> top region R6 rows 1-11 (cols 13-53). Row-0 EXIT cols 25-41. Below: shaft cols 13-17 rows 42-54 down to R3 (rows 55-59), teeth row 54, tower chamber rows 49-53 (4 towers), right shaft cols 42-53 rows 42-54 connects R3 to R5 body. R2 X-shaft blocks (3, toggled ON by us) visible rows 61-62 cols 19-35.
- X pairs on this screen: centers (33,27),(39,27) [grown = blocks rows 25-29] and (33,33),(39,33) [grown = blocks rows 31-35].
- STUCK ANALYSIS: from alcove, ACTION4 -> slot 19-23 auto-rise to pocket rows 30-34 (TRAP: exit right at 31-35 = tower death if X OFF, move-blocked if X ON b/c outline row30 vs ship top row30). Crossing at rows 37-41 impossible (no ceiling toggles exist over cols 19-30). Right shaft slots 43-47/49-53 would rise clean to R6 rows 1-5, then left 1 slot -> row-0 exit. ALL routes need crossing cols 19-42 at rows 37-41. Level needs unknown mechanic.
- Turn 17 probes: ACTION6(33,21) click upper-left tower (removable?); ACTION6(15,38) click ship (buoyancy toggle/sink?). If ship sinks: route = sink down left shaft to R2 floor, cross floor east (37-41 channel open - falls to R1!), or other sink-based routing. If towers removable: pocket->31-35 rise becomes safe -> rows 25-29 -> 37-41 (remove 2nd tower) -> 43-47 rise to R6.

## Turn 18 (after A77-78, budget 19/64): probes NO-OP (towers and ship NOT clickable, only budget bar changed).
- L2 death recheck: ship died separated from tower by 1px floor -> teeth+tower slots definitely fatal.
- GEOMETRY CORRECTION (programmatic water runs, cols 13-53):
  rows 19-24: water only col 36 + cols 42-53. rows 25-30: water cols 31-53. rows 31-36: water cols 19-53. rows 37-41: cols 18-53 + alcove.
  => Traversal band after rise at 19-23 = rows 31-35 (ceiling row 30 slab covers cols 19-30, safe no towers).
  => Slots 31-35/37-41 rise through rows 25-30 to rows 25-29 = tower DEATH unless capped.
  => UPPER X pair (33,27),(39,27) grown = blocks rows 25-29 cols 31-35/37-41, outline rows 24-30: caps those slots, outline row 30 does NOT collide with ship top row 31. LOWER X pair (33,33),(39,33) must stay OFF (remnants passable, proven).
  => Slot 43-47: water cols 42/43-53 continuous rows 13-36 -> clean rise to R6 rows 1-5.
- ROUTE: click (33,27),(39,27) [grow upper pair], then ACTION4 x5: 19-23 (rise to rows 31-35, +6 scroll), 25-29, 31-35 (capped), 37-41 (capped), 43-47 -> BIG RISE to R6 rows 1-5 + scroll ~30.
- NEXT TURN: ship should be R6 slot 43-47 rows 1-5 (screen rows 37-41). Inspect revealed region above old row 0 (goal/magenta expected, exit opening cols 25-41). Then ACTION3 -> slot 37-41 -> rise through exit -> dock magenta. Watch for towers above exit before committing.
- Settling under grown orange blocks is SAFE (proven A73-75, 3 settles under X-shaft blocks).

## Turn 19 (after A79-85, budget 26/64): crossing WORKED, big rise at 43-47 to top region. Ship slot 43-47 rows 37-41.
- MAGENTA FOUND: rows 1-3 cols 44-46 (ring 43-47), i.e. slot 43-47 at top ceiling - directly above ship but ceiling row 36 black at cols 42+.
- Current screen: throat rows 30-36 cols 25-41 w/ X remnants centers (27,33),(33,33),(39,33). Teeth row 24: open cols 13-24, blocks 25-29/31-35/37-41 + towers (26-28/32-34/38-40 rows 19-23) = all 3 throat slots FATAL rises. FULL orange blocks (togglable) at cols 13-17 & 19-23 rows 31-35 embedded in left slab = openable risers! Left path up: rows 25-29 water 13-41, row 24 open 13-24, rows 19-24 water 13-24, rows 12-18 water 13-23, top region rows 1-11 (water 13-29, block 31-35 rows 1-5 FULL + block 31-35 rows 7-11 FULL, water 37-42, magenta 43-47, water 48-53).
- PLAN: grow 3 throat caps ((27,33),(33,33),(39,33)); toggle OFF riser block (21,33) and top block (33,3); ACTION3 x4 (crossing capped slots 37-41/31-35/25-29, then rise at 19-23 to rows 1-5, scroll +36); ACTION4 x4 (25-29, 31-35 remnant, 37-41, 43-47 = LATERAL DOCK with magenta).
- RISK: lateral docking unproven (L1/L2 docked by rising from below). If blocked, ship rests at 37-41 rows 1-5; rethink next turn.

## Turn 20: LEVEL 3 SOLVED (A98, score 2->3, lateral docking WORKS, budget hit exactly 64). Total 98 actions, 3 levels.
## LEVEL 4 initial (budget 0/64): ship slot 25-29 rows 37-41 facing right.
- Layout: main region rows 37-53 (water cols ~24-53 upper part, 13-53 lower); TWO FLOOR TOWERS rows 37-41 at cols 14-16, 20-22 (bases row 41, standing on floor row 42) LEFT of ship; 1px water cols 18, 24 beside them.
- Right stair: rows 31-36 water cols 38-54; rows 25-30 water cols 44-54; channel rows 18-24 cols 50-54 (OFF-GRID vs ship slots 13/19/25/31/37/43/49 - col 49 black!); top region rows 7-17 water cols 13-53 (empty, ceiling row 6).
- FLOOR PLUGS (new!): green plugs BELOW floor row 54 at cols 14-18 and 20-24 (rows 55-59); bottom water region rows 61-62 (continues off-screen below?).
- No magenta visible. Hypothesis: dissolve floor plug -> water DRAINS -> ship descends with water level (new mechanic). Channel 50-54 off-grid supports non-ship purpose (water/flow?).
- Turn 20 probe: ACTION6(16,57) click floor plug 1, watch animation for drain/level change.

## Turn 21 (after A99, budget 1/64): plug 1 dissolved -> channel cols 13-17 rows 54-60 open (plug was 13-17 on-grid, plug 2 = 19-23). NO water drain, nothing floated up, ship unmoved. Water is static decoration.
- KEY observations: towers (14-16, 20-22 rows 37-41 on shelf row 42) stand directly ABOVE the two plug channels. Shelf row 42 has 1px holes at cols 18, 24. Anything rising a plug channel settles rows 43-47 under shelf = directly under a tower (possible trap for magenta?).
- Magenta NOT visible; likely in bottom region off-screen below (rows 61+). Top region rows 7-17 (cols 13-53) seems empty/decoy; reached only via off-grid channel 50-54 (rows 18-24).
- OPEN QUESTIONS: (1) partial moves (slide-until-blocked would re-align grid, enabling channel 50-54); (2) ACTION7 undo semantics.
- Turn 21 probe: ACTION3 (into 1px gap col 24: partial move would put ship at 24-28; full block = stay 25-29) then ACTION7 (if undo: restores 25-29). Fully safe/reversible; no rises possible at 24-28/25-29 (ceiling black).
- DO NOT commit ship upward (right stair) until goal location understood - ascent is irreversible!

## Turn 22 (after A100-101, budget 3/64, L4 Attempt 1)
- A100 (ACTION3 into 1px gap): ship did NOT move, only TURNED to face left. Conclusion: NO partial moves — 6 or nothing. Blocked moves still turn the ship.
- A101 (ACTION7): undid the turn (ship faces right again). ACTION7 = undo confirmed; depth beyond 1 step untested.
- Char census: no '-' (orange toggles), no 'z' (magenta) anywhere on L4 screen. Only O,h,(,",f,G,$,I.
- Water runs: rows 37-41 [(18,18),(24,24),(30,53)]; row 42 [(18,18),(24,53)]; rows 43-53 [(13,53)]; rows 54-60 [(13,17)] (plug-1 channel open); rows 61-62 [(13,53)].
- Both plug channels capped above by tower shelf row 42 (1px holes at cols 18,24 only). Goal presumably off-screen below.
- Turn 22 probe: click plug 2 center (21,57) — verified b[57][21]=='I'. Watch frames for anything rising from bottom region. Still honoring: do NOT commit right-stair ascent until goal understood.

## Turn 23 (after A102, budget 4/64, L4 Attempt 1)
- A102 opened plug 2: channel cols 18-23 rows 54-60 now water; merged with plug 1 => rows 54-60 run (13,23). NOTHING rose from bottom region (frames clean). No magenta on screen.
- CORRECTED full water map (scan): rows 7-17 (13,53) FULL WIDTH; rows 18-24 (49,53) <- NOT 50-54, aligns with slot 49!; rows 25-30 (43,53); rows 31-36 (37,53); rows 37-41 (30,53)+1px holes 18,24; rows 43-53 (13,53); rows 54-60 (13,23); rows 61-62 (13,53).
- RIGHT STAIR IS VIABLE: 25->31->37(rise to band 31-36)->43(rise to 25-30)->49(rise thru 18-24 to top region 7-17). Top region full width; goal likely off-screen above (camera scrolls on rise).
- Turn 23 plan: ACTION4, ACTION4 (reach slot 37-41, auto-rise ~6 rows), then ACTION7 to TEST whether undo can reverse a move+rise. If yes: ascents become reversible = huge safety tool. If no-op: ship stays risen, no harm.

## Turn 24 (after A103-105, budget 7/64, L4 Attempt 1)
- A103: moved to slot 31-35. A104: moved to slot 37-41 + AUTO-ROSE 6 rows to band 31-36 (camera scrolled 6). A105: ACTION7 UNDID THE MOVE+RISE ENTIRELY (board identical to A103). 
- KEY MECHANIC: ACTION7 reverses a full move+rise as one unit. Ascents are REVERSIBLE via single undo. De-risks exploration.
- Ship now: slot 31-35, band rows 37-41 (world), facing right.
- Turn 24 plan: climb the stair: ACTION4 (slot 37-41, rise to band 31-36), ACTION4 (slot 43-47, rise to 25-30), ACTION4 (slot 49-53, rise thru 18-24 channel to top region rows 7-17, settles rows 7-11). Camera scrolls ~30 rows total; observe what's revealed above. If bad, one ACTION7 undoes the last rise.

## Turn 25 (after A106-108, budget 10/64, L4 Attempt 1)
- Stair climbed as planned. Ship at slot 49-53, top region (screen rows 37-47 = full width 13-53). Camera scrolled 30 rows.
- NEW: RED diamond 'n' (21 cells, same diamond shape as L3 magenta) sealed in 5x5 pocket, screen cols 31-35 rows 25-29. Pocket exactly filled by red. 7 rows solid rock (screen 30-36) between pocket and top region.
- Screen census now: only O,(,h,n,f,G — NO plugs, toggles, towers on screen. Towers/plugs now off-screen below.
- Red = likely the L4 goal (color variant of magenta?) or hazard. Pocket cols 31-35 align with ship slot 31.
- Turn 25 probe: click red center ACTION6(33,27) from safe distance (clicks are position-independent; worst case no-op).

## Turn 26 (after A109, budget 11/64, L4 Attempt 1)
- A109 click on red diamond: RED = GRAVITY-FLIP ORB. Red consumed (gone), ship SANK from top region down (at cols 49-53, right of towers, safe) to floor of wide region world 43-53. Ship now screen rows ~27-31, cols 49-53. 43 frames, 1803 diffs, camera re-anchored (screen = world - 22 approx; anchor via tower shelf: towers at screen rows 15-18).
- Ship now SINKS to floors (buoyancy inverted). ACTION7 right now could undo the flip; moving on commits.
- New world below revealed: world 61-65 full width; 66-72 water cols 13-29 with FOUR GREEN PLUGS in rock at cols 31-35,37-41,43-47,49-53 (screen rows 45-49); 73-77 full width; 78-83 split (13-35)+(43-53); more off-screen below.
- Both old plug channels (cols 13-23, world 54-60) = the descent route from region 43-53. That is why plugs existed!
- Tower risk: descent at slots 13/19 transits far beneath towers (fatal case was SETTLING with 1px gap; transit assumed safe - unproven).
- Turn 26 plan: 5x ACTION3 (49->43->37->31->25->19); at slot 19-23 ship falls through channel 18-23, sinks deep (61-65 -> 66-72 via cols 13-29 -> 73-77 -> 78-83 -> ?). Camera will scroll down; observe.

## Turn 27 (after A110-114, budget 16/64, L4 Attempt 1)
- Descent survived (transit under towers is SAFE). Ship in LEFT pocket region world 78-83 (cols 13-35), slot 19-23, floor screen row 31. Camera: world = screen + 52.
- Screen map: rows 0-1 world 52-53; 2-8 plug channels (13-23); 9-13 world 61-65 full width; 14-20 world 66-72 (13-29) + 4-plug band-1 at cols 31-35/37-41/43-47/49-53 rows 15-19; 21-25 world 73-77 full width; 26-31 world 78-83 split (13-35)+(43-53); right region continues rows 26-37 (43,53); rock rows 38-50 contains 2 RED ORBS (19-23 & 31-35, rows 39-43) + STACKED plugs (43-47 & 49-53, rows 39-43 and 45-49); 4 TOWERS rows 51-54 (cols 14-16,20-22,32-34,38-40) in water band rows 51-56 runs (18,18),(24,30),(36,36),(42,53); rows 57-62 full width; row 62 floor open (13,25),(29,53) -> deeper off-screen.
- RED ORB ECONOMY: 2 left; need 1 UP-flip (reposition) + 1 DOWN-flip (descend right shaft) = exact.
- DANGER: rising at slot 19-23 or 13-17 = settle 1px under tower = DEATH. Safe rise col: 25-29 (caps at world 60 rock, settles 61-65).
- Turn 27 plan: open 3 plugs on col 49-53 shaft [(51,17) band-1, (51,41),(51,47) stacked], ACTION4 (19->25), click red (21,41) -> gravity UP, ship rises to world 61-65 ceiling at cols 25-29. Next turn: traverse right to slot 49, then click last red (31-35, recompute coords after scroll) -> sink full shaft: 66-72 channel, 73-77, 78-89, stacked channels, tower band (42-53 safe), 57-62, floor gap (29,53) -> deeper.

## Turn 28 (after A115-119, budget 21/64, L4 Attempt 1)
- A115-117 opened col 49-53 shaft plugs (band-1 + both stacked). A118 moved 19->25. A119 red orb A -> gravity UP, ship rose to world 61-65 slot 25-29. Camera C=24 (world=screen+C, C=shipTopWorldRow-37).
- TRAP DISCOVERED: last orb B (world 91-95, cols 31-35) is OFF-SCREEN with C=24, and gravity-up can never descend. Off-screen = unclickable. Chicken-and-egg.
- FIX: capped-rise trick. Undo A119 (ACTION7 restores gravity down + orb A + left pocket position 25-29). Then move to slot 31-35, flip up: rise CAPPED at world 73-77 by CLOSED band-1 plug 31-35 -> C=36 -> orb B visible at screen (33,55-59). Traverse right to 43-47 (ceiling = closed band-1 plug 43-47, settles 73-77). Click orb B (33,57) -> gravity DOWN -> fall into right region 78-89, rest on CLOSED stacked plugs 43-47 (world ~89) -> C~52, stacked plugs on screen -> next turn click both -> fall past tower band (water 42-53, no tower at 43-53) into world 109-114; floor opens (29,53) -> deeper.
- Click robustness: orb A (21,41) valid at C=52; orb B col 33 spans world rows 91-95 so (33,57) tolerates camera +/-2.
- If ACTION7 fails on clicks (untested): all subsequent actions are harmless no-ops/safe moves in gravity-up state.
- Turn 28 list: ACTION7, ACTION4, ACTION6(21,41), ACTION4, ACTION4, ACTION6(33,57)

## Turn 29 (after A120-125, budget 27/64, L4 Attempt 1)
- Capped-rise plan executed perfectly: undo restored orb A; rise at 31-35 capped at 73-77; traversed to 43-47; orb B click -> gravity DOWN; ship fell onto closed stacked plug 43-47, resting world 85-89 (screen rows 26-31). Both orbs consumed - gravity DOWN permanent. Camera C=58.
- MAGENTA FOUND: 5-cell diamond at world cols 26-28 rows 115-117 (screen (27,57-59)), SEALED in rock cavity below tower band (cap world 114, floor 118, sides 25/29). No physical approach possible.
- Ship shape correction: hull is 6 rows: top+bottom rows are 3-wide (center cols), middle 4 rows 5-wide. Keel = 3 center cols.
- World 114 floor: open 13-25 and 29-53 (ship falls through at most slots); only 26-28 (magenta cap) blocked. Below: 115-117 open (13,24)+(30,53), 118 open except 26-28, 119-120 full width, more off-screen below.
- Tower-settle danger zones at region 109-114: slots 31-35, 37-41 (and 13-17,19-23) directly beneath towers - do not SETTLE there. Safe: 25-29 (water gap 24-30 in band), 43-53.
- Turn 29 probe: click magenta (27,58) - sealed like red orbs were, likely click-activated = possible win.

## Turn 30 (after A126, budget 28/64, L4 Attempt 1)
- A126: magenta click = NO-OP. Goal needs physical mechanism.
- Analysis: ship keel (3-wide, center cols) landing at slot 25-29 would rest exactly ON magenta cap (world 114 cols 26-28). But cols 25-29 sealed from above (rock world 96-102 open only 49-53; tower-band gap 24-30 unreachable from above). No route to land on cap.
- All fall routes pass through open floor 114 into unknown depths below world 120. No orbs left. Must explore depths: maybe another orb or riser there.
- Turn 30: incremental — click upper stacked plug (45,35) only; ship drops ~6 onto lower plug, camera reveals ~6 more rows (world ~121-126). ACTION7 still usable to revert. Next: recompute lower plug coords (expect ~(45,45)) and continue.

## Turn 31 (after A127, budget 29/64, L4 Attempt 1)
- A127 opened upper stacked plug; ship dropped 6 onto lower plug (screen 26-31, cols 43-47). Camera C=64 (magenta now screen (27,51-53)). Below-tower water world 109-126+ full width, floor below screen.
- REALIZATION: col-49 shaft already fully open — ACTION4 slides ship right off the plug into free fall down 49-53: world 90-102, tower band (42-53 safe), depths. Zero clicks, keeps lower plug as platform, ACTION7-undoable.
- Turn 31: ACTION4. Observe deep-world reveal (looking for floor, orbs, risers, or path to magenta cap slot 25-29 / underside).

## Turn 32 (after A128, budget 30/64, L4 Attempt 1)
- A128: ship free-fell col-49 shaft into deep basin (world 109-131 full width, floor world 132). Ship slot 49-53, world 126-131 (screen 26-31). C=100.
- THIRD RED ORB in sealed pocket world 139-143, cols 25-29 (screen rows 39-43, center (27,41)) — below basin floor, click-activated like the others.
- Endgame geometry: click orb at slot 25-29 -> gravity UP -> ship rises col 25-29; mast (3-wide, cols 26-28) stops 1px below magenta pocket floor (world 118). Bet: dock works through 1px (symmetric to tower kill through 1px). If not: ACTION7 undo and rethink.
- Settling far below towers proven safe (A110-114) — basin traversal at slots 43/37/31 fine.
- Turn 32: ACTION3 x4 (49->25), ACTION6(27,41).

## Turn 33 — LEVEL 4 SOLVED at A133 (Score 4, 133 total actions). 1PX DOCK CONFIRMED: mast 1px under z through rock = dock. Budget reset.

## LEVEL 5 initial map (screen, gravity UP, ship slot 19-23 rows 37-41):
- z: sealed cavity rows 7-9 cols 32-34 (top center). Dock plan: mast at row 11 via slot 31-35 rise in TALL REGION (rows 12-23, cols 25-41; floor row 24 SOLID — enter only from top with gravity down).
- Top pockets rows 7-11: (25,30)+(36,42), row 11 spans (25,42). 1px cols 48,54 rows 7-11 between 3 NORMAL towers (rows 7-10, cols 44-46,50-52,56-58, bases row 11).
- RED ORB: pocket cols 49-53 rows 37-41 (center (51,39)) right of ship band.
- Ship band rows 37-47 (13,47); below rows 48-53 water (36,47)+1px 18,24,30; 4 HANGING towers rows 50-53 cols 14-16,20-22,26-28,32-34 (bases row 49 on TOP) — presumed kill if ship settles ABOVE them (mirror rule). Fatal landing slots with gravity down: 13-35. Safe fall slots: 37-41, 43-47 -> region rows 54-59 (37,47) -> 2 bottom plugs rows 61-65 (cols 37-41,43-47) -> off-screen below.
- Upper-right 3x2 plug grid rows 13-17 & 19-23, cols 43-47,49-53,55-59. Opening connects chamber rows 12-24 to tall region (via col 42) and to right shaft (55-59, rows 25-41, sealed below on screen).
- Turn 33 plan: 3x ACTION4 (19->37), click orb (51,39) -> gravity DOWN, fall at slot 37-41 to bottom plugs. Then explore below.

## Turn 34 (after A134-137, budget 4/64, L5 Attempt 1)
- Descent as planned: orb 1 consumed (gravity DOWN), ship fell slot 37-41 onto plug pair 1 (rows 33-37 screen, cols 37-41 & 43-47). Camera scrolled 28 (screen = old - 28).
- Note: old ship band (now rows 9-13) reads (13,59) full width — orb pocket + col48/54 walls may have opened; verify if needed for return trip.
- New below: band rows 39-43 (13,47); rows 44-50: left col (13,17) + right (37,48) with 2 STANDING towers rows 45-48 cols 50-52,56-58 (bases row 49 below them); rows 51-55 (13,17)+(37,59); rows 56-61: (13,18)+(24,24 1px)+(49,59) + 2 standing towers rows 57-60 cols 20-22,26-28 (bases row 61) + PLUG PAIR 2 rows 57-61 cols 37-41,43-47; row 62 (13,18),(24,24) continues off-screen.
- No orb on screen — must be deeper. Fall path at slot 37-41 clear of all towers.
- Turn 34: click plug under ship (39,35) -> fall to plug pair 2 (rest ~rows 51-56). Camera scrolls ~24.

## Turn 35 (after A138, budget 5/64, L5 Attempt 1) — WORLD MAP STITCHED (W = orig screen coords)
- W7-9 z cavity (32-34); pockets W7-11 (25,30)+(36,42); tall region W12-23 (25,41) floor W24; upper 3x2 plug grid W13-17/W19-23 cols 43-47,49-53,55-59; shaft W25-41 (55,59); home band W37-47 — W37-41 now (13,59): ORB POCKET WALLS DISSOLVED on consumption (band<->shaft connected!).
- W42-47 shelf (13,47) over hanging towers W50-53 (bases W49) = mirror-kill risk + dead end. Chute (37,41) W60-66 (1a open); band2 W67-71 (13,47) floor W72 solid 18-36 only; left column (13,17) W72-90 -> (13,29) W91-96 (X-toggles W92-94 at 19-23,25-29) -> BASIN W97-107 (13,59) -> W108-113 (19,47) -> W114 (19,29) -> unseen below.
- DEAD ENDS: plug2 channels (floor W91 solid at 37-47); right chamber W84-89 (49,59) floor W90; shelf. Basin first-entry: impossible from above except band2 slot 13-17 (unreachable) => deep orbs must be revealed by camera and clicked remotely.
- RETURN PATH VERIFIED (for future flip-UP): from plug2 area at slot 37-41 rise: pocket->W72-77->band2->chute->home band W37-41 settle. Then slide right to shaft 55-59, rise to W25-29 (chamber plugs clickable from that camera, screen=world+12).
- DOCK LINE (needs ~3 more flips): shaft->chamber(open plugs)->tall region->rise pocket(36,42)@37-41->FLIP DOWN->tall floor W18-23->slide 31-35->FLIP UP->mast W11 dock.
- Turn 35: click plug 2a (39,35): ship drops into channel (hull W85-90, rests floor W91), camera +7 => reveals W115-121. Hunt for deep orbs. Outline W84 dissolves so later rise-out is clear.

## Turn 36 (after A139)
- A139 opened plug 2a; ship now STUCK in 2a cavity (37-41, W84-89), gravity DOWN. Reveal to W120: pit (19-29, W114-119), floor W120, NO ORBS anywhere. Deep-orb hypothesis refuted.
- SHIP SPRITE corrected: 5 wide x 6 tall rounded shell (casing 'O' ring, corners open); body f/f/G inside. Start "notch walls" were the ship's own casing.
- PLUG DISSOLUTION MECHANIC NAILED (diff 1a vs 2a): removes 5x5 plug + any adjacent 1px rock wall that has WATER on the far side. Corners of the ring never dissolve. 1a opened top+bottom (chute above, band2 below); 2a opened only top (floor thick = trap).
- Upper plug grid analysis: dissolving all 6 would connect shaft->corridor->tall region BUT 1px corner nubs at (42,18),(48,18),(54,18) survive, and ship (6 tall) cannot pass 5-tall gaps. Top dock complex entry still UNSOLVED. Top z dock config verified: rise at cols 31-35 -> mast casing W11, 1px rock W10, z W9 = dock... if ever inside.
- INTENDED DESCENT: right chamber -> deep plug grid (49-53 & 55-59, W91-95) under the deep towers; both its top (W90) and bottom (W96) walls dissolve into water -> basin. Pre-dissolve the plug BEFORE entering col 49-53 so ship free-falls past towers (no settle near kill zone), lands basin W102-107.
- Turn 36 plan: ACTION7 (escape 2a trap, restore A138 state C=52), ACTION4 (->43-47), ACTION6(51,41) (=world (51,93) deep plug), ACTION4 (fall to basin 102-107), ACTION3 x4 (-> pit 19-29, settle W114-119). Camera then shows ~W88-151: hunt below W120.
- If ACTION7 no-ops: every subsequent action is harmless (blocked moves / water clicks). Reassess.

## Turn 37 (after A140-147, budget 14/64, L5 Attempt 1) — BREAKTHROUGH: lateral dock solves endgame
- A140-147 all executed: undo out of 2a trap, right, deep-plug pre-dissolve, free-fall descent, 4x left -> ship in PIT, slot 25-29, world rows 114-119, gravity DOWN, facing left, C=88.
- DEEP ORB confirmed (49-53, W139-143), clickable screen (51,53). Toggles X-state at (20-22)/(26-28, W92-94), centers screen (21,5)/(27,5); grown = 5x5 blocks (19-23)/(25-29, W91-95) capping the deep-left-tower kill rises.
- ENDGAME RESOLVED via L3 precedent (Turn 19-20 notes): LATERAL DOCK WORKS — ship moved sideways INTO ringed magenta slot, dock overrides ring/goal collision. L5 z is at (32-34, W7-9) in slot 31-35, flanked by water pockets 25-30 and 36-42 (rows 7-11, chamber 25-41 rows 11-23 below). Route: gravity UP, enter chamber via P4 (col 42 wall rows 19-23 dissolves, water far side), slot 37-41 auto-rise to f-nose 7 (rows 7-11), then ACTION3 -> slot 31-35 = DOCK. Tower 1 (44-46, W7-11, base G$G row 11) is lateral only — no vertical 1px config, safe.
- THIS TURN (12 actions): toggle both caps ON (27,5),(21,5); click orb (51,53) -> gravity UP, rise capped f-nose ~96 under block; ACTION3 x2 (19-23 capped, 13-17 big rise to band2 f-nose 67); ACTION4 x4 (19,25,31, 37-41 big rise thru 1a+chute to home band f-nose 37); ACTION4 x3 (43,49, 55-59 shaft rise f-nose 25). All moves camera-independent.
- NEXT TURN: ship at 55-59 f-nose W25 under rock 24 (P6 floor). Camera should anchor nose screen 37 (gravity UP) -> C = 25-37 = -12. Click P6 center world (57,21) -> ship auto-rises into cavity 19-23 (safe: rock18+plug P3+rock12 above, not 1px). Then P5 (51,21), ACTION3, P4 (45,21), ACTION3, ACTION3 (chamber, big rise to 7-11), ACTION3 = DOCK. Do clicks one-or-two per turn if camera uncertain; rises re-anchor camera predictably (+6 per small rise).
- Budget after this turn: 26/64. Remaining need: ~7 actions -> ~33/64. Comfortable.

## Turn 38 (after A148-159, budget 26/64, L5 Attempt 1) — ascent complete, executing dock endgame
- All 12 executed perfectly: caps toggled, orb flipped gravity UP, capped rises, band2 traverse, big rises at 37-41 (chute) and 55-59 (shaft). Ship slot 55-59, f-nose W25 = screen 37 (C=-12, screen=world+12). No deaths, still Attempt 1.
- Screen-verified: z (33,19-21) ctr (33,20)=W(33,8); towers (44-46/50-52/56-58, scr 19-23, G$G base scr 23=W11); P1-P3 scr rows 25-29 (W13-17); P4-P6 scr rows 31-35 (W19-23) at cols 43-47/49-53/55-59.
- THIS TURN (7): click P6 (57,33) -> floor row W24 dissolves (water below), ship rises 6 to cavity f-nose W19, camera scrolls +6 (nose anchor 37 -> screen=world+18); click P5 (51,39), P4 (45,39) [if scroll assumption wrong, clicks hit rock = no-op, moves get blocked, ship safe — retry next turn]; ACTION3 x2 (49-53, 43-47 through dissolved side walls); ACTION3 (37-41: enters chamber via opened col-42, BIG RISE to f-nose W7, rows 7-11); ACTION3 (31-35 = LATERAL DOCK with z, L3 precedent).
- Tower 1 (44-46, W7-11) is 2+ cells lateral from ship at 37-41 — kill rule is vertical 1px nose/keel config only. Safe.
- Expect score 4->5, Level 6 load. Budget after: 33/64.

## Turn 39: LEVEL 5 SOLVED (A166, score 4->5, lateral dock into z slot 31-35 worked). Total 166 actions, 5 levels, L5 took 64 actions on Attempt 1.
## LEVEL 6 initial (budget 0/64, screen=world, gravity carried over = UP): ship slot 19-23, f-nose 37 (rows 36-41), facing right, under rock band 30-36.
- RED ORB: (37-41, 31-35) ctr (39,33), embedded in band 30-36 ring 36-42; water above (band 25-29 full-width 13-53) AND below (middle region) -> consumption opens vertical channel 37-41 through band.
- MIDDLE REGION rows 37-53 cols 13-53 (ship here). Floor row 54: 1px gaps 18/24/30/36/42 + WIDE opening 48-53. BOTTOM CHAMBER rows 55-59: 6 towers G$G base row 55 (top) at 14-16/20-22/26-28/32-34/38-40/44-46 -> gravity-DOWN sink at slots 13-47 = DEATH (1px rock 54) EXCEPT 49-53 (open shaft, water rows 55-62, continues off-screen below).
- BOTTOM TOGGLES (X): ctrs (39,51),(45,51) -> grown 5x5 floors at 37-41/43-47 rows 49-53 = the only safe DOWN-parking in middle region.
- TOP: 3 towers rows 7-11 base G$G row 11 at 14-16/20-22/26-28 above rock 12 (1px gaps 18,24) -> upper-left chamber (13-29, rows 13-29) rises ALL FATAL (toggles ctrs (15,21),(21,21),(27,21) are DECOYS - grown blocks at rows 19-23 would trap under, not protect a crossing; chamber has no onward exit anyway).
- UPPER ROUTE (gravity UP): band 25-29 (13-53) -> slot 49-53 rises up RIGHT SHAFT (49-53, rows 7-29) to rows 7-11; region rows 7-11 cols 31-53 + rows 7-12 cols 30-41; TOP CHANNEL (37-41, rows 0-6) off-screen above (z suspected there). Right shaft dead-ends at band 30-36 (no middle connection).
- FULL L6 ROUTE: [P1 now] grow both floor toggles, 3x ACTION4 to 37-41, click orb -> flip DOWN, sink onto block rows 43-48, channel opens. [P2] right to 43-47 (block), 49-53 -> sink thru shaft off-screen below; explore, find orb #2. [P3] click orb #2 -> UP; rise back thru 49-53 into middle (f-nose 37); lefts to 37-41 -> rise thru orb channel to band 25-29 (f-nose 25, rock 24 caps at cols 30-48); rights to 49-53 -> big rise up right shaft (f-nose 7); ACTION3 x2 -> 37-41 -> BIG RISE thru top channel to off-screen top.
- Turn 39 actions (6): ACTION6(39,51), ACTION6(45,51), ACTION4 x3, ACTION6(39,33). Expect: gravity DOWN, ship on block 37-41 rows 43-48, camera may scroll (DOWN anchor nose~26). Budget 6/64.

## Turn 40 (after A167-172, budget 6/64, L6 Attempt 1): Phase 1 perfect.
- Both floor blocks grown (37-41/43-47, W49-53). Orb consumed -> gravity DOWN, ship sank onto left block: slot 37-41, world rows ~42-47, screen 26-31 (C=16, world=screen+16). Orb channel through band 30-36 open (verify later on return).
- Shaft 49-53 visible as water world 60-78, continues off-screen below.
- Turn 40 (2): ACTION4 (43-47, settle on right block), ACTION4 (49-53, sink thru row-54 opening, chamber, deep shaft, off-screen). Expect big camera scroll down; then map new region, find orb #2 (needed for UP re-flip) and possibly z. Budget after: 8/64.
- REMINDER Phase 3 (after orb #2 UP-flip): rise shaft 49-53 into middle region f-nose 37; ACTION3 x2 to 37-41; rise thru orb channel to band 25-29; ACTION4 x2 to 49-53; big rise right shaft to rows 7-11; ACTION3 x2 to 37-41; big rise top channel (W0-6) off-screen above.

## Turn 41 (after A173-174, budget 8/64, L6 Attempt 1): bottom region mapped — z FOUND, sequencing puzzle solved.
- Ship sank shaft to bottom floor: slot 49-53, world rows 84-89, floor 90 (C=58 on l6c board).
- BOTTOM REGION (world rows 79-89, WIDER than upper world — extends left to col 7): upper band rows 79-83 water cols 7-23 & 31-53 (rock pillar 24-30), ceiling 78 rock everywhere except 49-53 (shaft). Bottom corridor rows 84-89: z POCKET slot 13-17 (z 3x3 diamond at (14-16, 85-87), ring cols 13/17 rows 85-87 + 3-wide caps (14-16) rows 84/88... verify), ORB #2 pocket (25-29, 85-89) ring cols 24/30 + top 84 (pillar above -> top ring will NOT dissolve; sides WILL - water both sides), water elsewhere. Floor 90 solid.
- KEY DEDUCTION: z dock needs lateral entry at rows 84-89 (overlap z 85-87) under gravity DOWN; orb #2 blocks slot 25-29; consuming it flips UP and auto-lifts ship out of corridor (all right-side slots rise to 79-84 band or higher; pillar blocks left passage at band height) => must consume orb #2, ascend to unexplored TOP (via orb-1 channel + right shaft + top channel 37-41 world rows 0-6), find a DOWN-flip (orb #3 expected), fall back to bottom at 49-53, then walk floor LEFT through the now-permanently-open pocket to dock z at 13-17.
- PROVEN by log diff (A138 vs A140 identical): ACTION7 undo restores EVERYTHING incl. dissolved terrain — no undo tricks possible.
- SOFT-TOP MODEL: top casing is the soft/overlap part (all UP settles overlap ceiling rock with top casing); bottom casing hard (rests on floors, L5 pit rows 114-119 on floor 120). => gravity-DOWN slide through 5-tall corridor under orb-pocket top-ring (84) should PASS (hard span 85-89, soft top overlaps 84). To be tested at endgame.
- Turn 41 (5): ACTION6(27,29) orb #2 -> flip UP, pocket sides dissolve, ship rises shaft to middle region (49-53, f-nose 37, C->0); ACTION3 x2 (43-47; 37-41 rise thru orb-1 channel to band 25-29 f-nose 25); ACTION4 x2 (43-47 capped; 49-53 BIG RISE right shaft f-nose 7, C->-30). Camera then reveals top region (world rows -30..6). Budget after: 13/64.
- NEXT: inspect top region; enter top channel (ACTION3 x2 to 37-41 -> big rise) only after checking for tower kill-configs above.

## Turn 42 (after A175-179, budget 13/64, L6 Attempt 1): ascent perfect, top region partially revealed.
- Ship slot 49-53, f-nose W7 (C=-30, world=screen-30). Orb #2 consumed (bottom corridor now open for endgame).
- TOP REGION (world rows -30..6 visible, room continues OFF-SCREEN above): BIG ROOM cols 13-53, water from -30 (and above) down to floor -12. Floor -12: rock 13-35 with 1px gaps 18/24/30, WATER 36-53 -> lower extension (36-53, rows -12..-7), floor -6 except channel 37-41 (rows -6..6) down to middle region.
- 4 HANGING TOWERS (base G$G at top, W-11; body -10..-7) at 14-16/20-22/26-28/32-34 under floor -12 -> gravity-DOWN landing on floor -12 at slots 13-17/19-23/25-29/31-35 = 1px KILL. 
- TOGGLES at W-23..-19: X remnants ctrs (15,-21),(21,-21),(27,-21),(33,-21),(45,-21),(51,-21); GROWN 5x5 BLOCK at 37-41 (-23..-19) directly above channel column = DOOR under which ship will settle (f-nose -18).
- No orb, no z visible yet (n=0). Expect DOWN-flip mechanism above screen top.
- Turn 42 (2): ACTION3 x2 -> 43-47 (f-nose 7), 37-41 -> BIG RISE up channel thru lower extension + room to f-nose -18 under grown block. Camera re-anchors C=-55, revealing world -55..-31 (room top).
- NEXT: inspect room top; likely click grown block OFF (ctr screen (39,34) if C=-55) -> rise to room ceiling; CHECK FOR TOWERS first. Endgame after DOWN-flip: fall to bottom via channel+shaft (49-53) to floor 90, ACTION3 x3 thru open pocket (soft-top model: hard span 85-89 passes under pocket top-ring 84), dock z at 13-17.

## Turn 43 (after A180-181, budget 15/64, L6 Attempt 1): in big room under door block. C=-54 (world=screen-54, dy=24 vs l6d by cross-corr).
- Ship slot 37-41, f-nose W-17 (hard -17..-13), under grown door block (37-41, -23..-19; outline rows -24/-18 soft).
- UPPER GAUNTLET MAP: room water 13-53 rows -35..-13. STANDING TOWERS bodies -41..-38, G$G base W-37 at cols 32-34/38-40/44-46/50-52, in pockets above rock shelf -36 (1px gaps at 36/42/48) => gravity-UP rise at slots 31-35/37-41/43-47/49-53 from room = nose -35 under 1px shelf = KILL. Slots 13-17/19-23 capped safe (thick rock). Slot 25-29 = LEFT CHANNEL water rows -48..-36 (wall col 31... col 30 water to -36) -> UPPER BAND rows -53..-49 (cols 25-53), ceiling -54 rock at 25-42, OPENING at 43-53 row -54 leading further up OFF-SCREEN.
- X toggles at W-21 centers: (15,-21),(21,-21),(27,-21),(33,-21),(45,-21),(51,-21) + grown door 37-41. Grown = platforms -23..-19 (safe landings for later DOWN phase over the hanging-tower kill floor -12).
- Turn 43 (3): ACTION6(33,33) grow cap 31-35; ACTION3 (31-35 capped, nose -17); ACTION3 (25-29, BIG RISE up left channel to nose -53). Camera re-anchor C~-90 reveals world above -54. Budget after: 18/64.
- NEXT: rights along upper band (31-35, 37-41 capped by ceiling -54), then 43-47/49-53 rise thru -54 opening into next region — CHECK REVEAL FIRST for shelf/tower kill patterns. Still hunting the DOWN-flip orb. Endgame reminder: fall route back = channel 37-41 -> middle -> shaft 49-53 -> bottom floor 90 -> 3 lefts thru open pocket -> dock z 13-17.

## Turn 44 (after A182-184, budget 18/64, L6 Attempt 1): TOP IS A DEAD END — PARITY LOCK DIAGNOSED. RESETTING.
- Ship reached upper band 25-29 (nose W-53, C=-90). Reveal: above ceiling -54, ONLY a pocket (43-53, W-59..-54), pure water, sealed above (-60 solid). NO ORB. Rest of upper world all rock. WORLD NOW FULLY MAPPED (rows -60..90, cols 7-53): exactly TWO orbs existed (orb1 mid, orb2 bottom), both consumed.
- BUOYANCY MODEL (reframed): default state = BUOYANT (rise); each orb click toggles rise/sink globally + consumes orb. L1-L3 shipped buoyant, no orbs. L6 start buoyant -> orb1 sink -> orb2 buoyant. PARITY LOCKED BUOYANT with z requiring SINK-mode lateral entry at rows 84-89 (85-89 hard-cell overlap with z 85-87). Corridor-left (19-23, 13-17 floor positions) and pocket interior are sink-only; left band (79-84) unreachable buoyant (pillar 24-30 W79-83 blocks 25-29 at band height; z top-cap at 84 blocks 13-17 entry). Ship at top cannot descend at all => ATTEMPT LOST.
- Orb2 CANNOT be clicked before orb1 (off-screen until camera follows ship to bottom; descent requires sink; first reachable orb = orb1). Parity unavoidable under known mechanics => MISSING MECHANIC. Only untested candidate: CLICKING THE Z GOAL (never tried in any level). Possible effects: no-op / ring dissolution / remote dock.
- TRAPS catalogued: top pocket (enter => stuck forever buoyant, exit move blocked by rock -59..-55 at 37-41); extension right (36-53,-12..-7) sink-stuck except 37-41; left band buoyant = stuck; upper-left chamber = kill.
- Turn 44 (10): RESET; redo proven descent: ACTION6(39,51),(45,51) grow floors; ACTION4 x3 (->37-41); ACTION6(39,33) orb1 -> sink onto block; ACTION4 x2 (43-47, 49-53 -> bottom floor 90, rows 84-89, C=58); ACTION6(15,28) CLICK Z TEST (z world (15,86)).
- NEXT TURN: inspect z-click result (diff board). If ring dissolved or dock triggered -> proceed accordingly. If no-op -> ship parked safe at bottom 49-53 sink-mode, orb2 intact; remaining ideas: empirically test pillar-block assumptions, examine frames of orb2 click for overlooked propagation, consider budget-reset exploit.

## Turn 45 (after A194)
- A185-194 redo perfect: ship sink-mode at slot 49-53 (world rows 84-89), C=58, budget 9/64, orb2 intact.
- z-click (15,28) A194 = 0-diff NO-OP confirmed.
- L2 win re-parsed: A59 was ACTION6 plug click -> ship ROSE into magenta = RISE-DOCK exists (vertical overlap docks too).
- Left corridor ceiling = row 78 solid across cols 5-48; only shaft = cols 49-53. Buoyant press in corridor -> hard span 79-83, NO z overlap (z 85-87). Sink entry still required.
- NEW HYPOTHESIS (this turn's test): buoyancy mode may survive ACTION7 (mode is not board state; 0-diff undo proof only covered terrain).
  Sequence: 3 lefts to 31-35 (solid ceiling above), click orb2 (27,29), UNDO, click orb2 again, 3 lefts.
  - If mode survives undo: 2nd click flips buoyant->SINK, orb consumed, rings 24/30 dissolve, ship stays floored -> lefts 31->25->19->13 dock z (lateral override). WIN.
  - If mode restored: 2nd click = rise to 79-83, pillar 24-30@79-83 blocks lefts (harmless), RESET next turn (budget restarts).
- Orb2 screen coords (27,29) valid: C unchanged by lateral moves, dx=0.

## Turn 46 (after A203)
- PARITY TEST FAILED: undo DOES restore buoyancy mode (A200 board identical to A198 — ship rose both clicks). Orb2 consumed, rings 24/30 dissolved, ship buoyant pressed at 31-35 rows 79-83 (C=42), lefts A201-203 pillar-blocked (0 movement).
- LEVEL FULLY DECODED from initial board (C=0) + A198 view (C=42):
  * Ship starts slot 19-23 rows 37-41, pressed under rock band 30-36. Orb1 = plug IN the band at 37-41x31-35.
  * Middle region rows 37-53 water (cols 13-53); floor 54 has 6 kill-tower boxes (G$G caps row 55, purple bodies 56-59) under EVERY slot except shaft 49-53. 1-wide slits at 18/24/30/36/42.
  * X-remnants (orange X shapes) at centers (39,51),(45,51) initially; clicks grew 5x5 blocks 37-41/43-47 x 49-53 + 1px outlines = safe sink landings over towers. NO remnants anywhere in bottom region (verified).
  * Descent: grow both blocks, 3R (pressed under band), click orb1 -> sink onto block, R (block2), R (shaft 49-53) -> bottom floor.
  * Bottom: ceiling 78 uniform cols 7-48 (only shaft hole 49-53). Corridor 7-23 rows 79-89. Buoyant press = f rows 79-82 (too high for z 85-87). Sink floor profile f 85-88 = exact z overlap. Pillar 24-30x79-83+cap 84 has EXACT grown-block anatomy (core 25-29x79-83, outline 24-30x78-84) — may be toggleable!
- Fundamental geometry: buoyant ship can NEVER be at rows 85-89 in corridor (no low ceilings except ring caps). Dock requires sink at corridor floor; sink lost on orb2. Need new mechanic.
- THIS TURN probes (attempt is dead, all free info, ends RESET): ship-click (33,38) [mode toggle? -> would sink + 3 lefts through OPEN pocket = WIN this attempt], pillar-click (27,39) [toggle off? -> 3 lefts test slot-entry dock at height 79-83], z-cap click (15,42) [casing dissolve?], RESET last (safe in all branches incl. accidental L7 spillover).
- Next turn if all no-op: RESET already done; descent redo = 8 actions: (39,51),(45,51),R,R,R,(39,33),R,R.

## Turn 47 (after A213)
- ALL probes 0-diff NO-OPS: ship-click, pillar-click (pillar = plain rock, not toggle), z-cap click. RESET done at A213 -> fresh attempt, ship at start 19-23.
- Upper region scanned (l6b/d/e/f): X-remnants at row 21 (centers 15,21,27) and row -21 (centers 15,21,27,33,45,51 + grown block 37-41x-23..-19); INVERTED kill towers (caps at bottom, r11 & r-11 clusters) kill RISING ships; small 1x2 G markers at (40,44-45),(52,8-9),(38,-16..-15),(26,-52..-51). NO third orb, NO second z anywhere. Upper region = decoy/punishment space.
- Grown block geometry: 5x5 centered on X center (X(39,51) -> block 37-41x49-53).
- ONLY untested L6 interaction: sink-mode lateral move INTO intact orb2 ring (col 30) at floor level. Outcomes: (a) blocked-turn no-op; (b) contact-consume without flip -> sink retained -> lefts dock z = WIN; (c) consume+flip with ship in pocket 25-29 -> pressed under cap 84 (nose 84, f 85-88) -> subsequent lefts test 19-23-rise + slot-entry-dock-at-79-83; (d) death -> info.
- THIS TURN (14): proven descent [grow(39,51),grow(45,51),R,R,R,orb1(39,33),R,R] + 3 lefts to 31-35 + LEFT-INTO-RING + 2 more lefts (win in (b), tests in (c), harmless in (a)).
- If (a) next turn: ship 31-35 sink, orb2 intact, ~50 budget. Ideas left: click orb2 from 49-53 (rise up shaft) then buoyant upper-region toggle experiments (row-21 blocks); budget-overflow reset asymmetry test; death-reset asymmetry (needs sink to die - only pre-orb2).

## Turn 48 (after A227)
- Contact-consume FALSIFIED: A225-227 lefts into intact ring = 0-diff blocked. Ship SINK at 31-35 floor (f 85-88 world), orb2 intact, 14/64 used.
- COMPOSITE WORLD MAP BUILT: /workspace/l6_world.pkl + l6_map_left.txt + l6_map_right.txt (world rows -90..120).
- Attempt-1 trajectory decoded (camera-calibrated): A175 orb2 click at 49-53 -> rose 48 rows up shaft (persistent buoyant CONFIRMED). A177 rose through orb1-hole. A182 grew (33,-21) block as tower protection. A184 ended top region 25-29x-54..-49. Full spine: start(37-53) -> band 30-36 (orb1 at 37-41) -> upper corridor 13-29 (slab 18-24 at 31-48; inverted towers caps@11 over slots 13-29; X row 21 protects) -> shafts 49-53@18-24, 37-41@-6..6 -> chamber -35..-13 (floor -12 towers under 13-35, X row -21, inverted towers caps@-37 over 31-53) -> shaft 25-29@-48..-36 -> top region -59..-49 (EMPTY). Post-orb2 buoyant space fully enumerated: NOTHING interactive. Decoy.
- L2 death forensics: A18 second click on (21,33) = DEATH -> board becomes green-block fill, ship removed, budget row CONTINUES (death does not restart budget), attempt counter++ (deaths only; voluntary RESETs don't increment). RESET restores fully. Death preserves NOTHING exploitable.
- L2 win pattern: repeated grow-clicks before moves (protection blocks), TRIPLE-click (21,33) A41-43 suggests re-togglable X blocks; final win = dissolve plug BELOW z + rise-dock. L2 z-box bottom was effectively a PLUG.
- L6 grown blocks render ORANGE; pillar renders BLACK = real rock (not a block). Confirmed.
- FASTER DESCENT DISCOVERED (untested): 5 rights pressed under band to 49-53 (over shaft), click orb1 -> falls straight to bottom = 6 actions, no platform grows needed (blocks only needed if stopping at 37-47).
- THIS TURN probes (ship parked): z-box bottom cap (15,88)=scr(15,30), right wall (17,86)=scr(17,28), left wall (13,86)=scr(13,28), pocket top-ring (27,84)=scr(27,26), pocket right ring (30,86)=scr(30,28), pocket left ring (24,86)=scr(24,28). If any dissolves -> L2-style plug-wall mechanic in play.

## Turn 49 (A228-233 results, wrote probes for A234-235)
- Probe results: z-box walls (15,88),(17,86),(13,86) + pocket sides (30,86),(24,86) = ALL NO-OPS (1-diff budget tick only).
- A231 click screen(27,26)@C=58 = world (27,84) pocket TOP RING → CONSUMED ORB2! Whole ring+orb 24-30x85-89 dissolved to water; ship rose to buoyant 31-35x79-83 (pressed under ceiling 78); camera now C=42. Frames: dissolve → rise → scroll. So ring-top cell was part of the orb assembly (remote-clickable).
- STATE NOW: both orbs consumed, BUOYANT, ship 31-35x79-83, C=42, 20/64 budget, attempt 1. This equals attempt-1 dead-end state.
- NEW DISCOVERY (world map audit for interactive colors): TWO BOXED ORANGE PLUGS in start region: 5x5 orange at 37-41x49-53 and 43-47x49-53, black casing (rows 48/54, cols 36/42/48), sitting on start floor 54. NEVER CLICKED. Kill towers sealed below floor 54 under all slots 13-47 (caps G row 55, bodies 56-59); floor 54 holes: x18,24,30 (1-wide slits, unusable) + shaft 49-53.
- Orb1 hole confirmed: band 30-36 has water gap at 37-41 (orb1 assembly sealed it before consumption).
- Start cavern = x13-53, rows 37-53, ceiling band 36, floor 54.
- THIS TURN: click plug centers remotely: world (39,51)=scr(39,9), world (45,51)=scr(45,9) at C=42. Hypothesis: toggleable X-grown blocks hiding a 3rd orb (parity-lock breaker: consume orb2 for pocket-open, then hidden orb → sink → walk pocket → corridor → dock z at 13-17).
- If plugs no-op: try multi-undo depth (3x ACTION7 to unwind to sink state), then reconsider.

## Turn 50 (A234-235 results; MAJOR breakthrough in level understanding; wrote A236-245)
- A234/235: plug clicks DISSOLVED both plug boxes ENTIRELY (orange + casings -> water), leaving X remnants at (39,51),(45,51). No hidden orb. Confirms boxed oranges are toggleable and casings dissolve with them.
- PRECISE GEOMETRY (programmatic openranges, corrects earlier misreads):
  band hole x37-41 rows 30-36 (orb1 was there); slab x30-48 rows 18-24; left pocket x13-29 rows 13-24 (kill ceilings row 12 w/ inverted towers 7-11 at slots 13-17,19-23,25-29); riser x30-41 rows 7-13; mid shaft x37-41 rows -6..6; upper floor -12 (open x36-53); chamber A x13-53 rows -35..-13 w/ X row -21 (15,21,27,33,45,51) and PRIZE BOX (casing 36-42 x -24..-18, orange 5x5 37-41 x -23..-19, X center (39,-21)); ceiling -36 w/ inverted towers at 31-35,37-41,43-47,49-53 (caps -37!); shaft 25-29 -48..-36; chamber B 19-47 x -53..-49; top pocket 37-47 x -59..-54 (EMPTY).
- Ship positions from checkpoints: A166 start under band slot 19-23 (f 37-40); A172 ON plug1 (f 43-46) -> plugs are SINK LANDING PADS; A174 bottom 49-53; A179 upper-shaft top 49-53 (f 7-10, C=-30); A181 UNDER PRIZE BOX (f -17..-14, C=-54); A184 chamber B under -54 (f -53..-50, C=-90). A186-194 = RESETs.
- SOFT-CELL RULE: ship soft casing (nose/keel-side O cells) CAN overlap solid (proven: nose overlaps ceiling row). Only hard f/G/keel collide.
- PRIZE BOX = the only unopened container = the lock-breaker candidate. Hypotheses: contains ORB3 (-> flip sink) or a Z (-> L2-style rise-dock) or empty (-> rising under it = DEATH via ceiling -36 tower at 37-41).
- MASTER PLAN (this turn = A236-245): regrow plug1+plug2 (clicks (39,9),(45,9) at C=42) as future landing pads; then buoyant rise route: R,R,R (31-35 -> 49-53, auto-rise long shaft -> under band 36), L,L (-> 37-41, rise through band hole -> under slab, nose 24 f 25-28 keel 29), R,R (-> 49-53, rise -> under 6, f 7-10), L (park 43-47 rows 6-11, C≈-30, NOT under box).
- NEXT TURN: verify C (expect ≈-30), click prize box X at world (39,-21) = screen (39, -21-C) REMOTELY. Then:
  - If ORB revealed (caged ring): move L,L (43->37-41, rise to under-ring), click orb -> SINK -> falls to slab top 18 (keel 17, C=-12). Then R? no: L?? from slab top 37-41: ... descent: slab-top -> L/R moves at rows 12-17; to descend: R,R -> 49-53 falls to band top (24-29); L (nose-soft over slab edge) 43-47 on band; L 37-41 -> falls through band hole -> lands PLUG1 (keel 48); R -> plug2; R -> 49-53 falls long shaft -> bottom floor; L x4 -> 43,37,31,25-29 (pocket OPEN this attempt, nose-soft passes under pillar row 84); L -> 19-23; L -> 13-17 = z overlap DOCK (risk: low-f (15,88) vs casing bottom cap (14-16,88) might block; L3/L5 lateral docks suggest dock check wins).
  - If Z revealed: move L,L -> rise into z cells -> dock (L2 pattern).
  - If EMPTY: do NOT go to 37-41; click (39,-21) again to regrow as protection ceiling; rethink.
- Budget after this turn: 32/64.

## Turn 51 (A236-245 executed perfectly; wrote A246)
- A236/237: plugs REGROWN (casing+orange restored, 40+33 cells) — landing pads ready.
- A238-245: rise route executed exactly as planned. A245: ship at slot 43-47, f world 7-10 (pressed under 6), C=-30, score-match 0.998.
- Prize box confirmed intact on screen: casing scr rows 6-12 cols 36-42, X/orange center world (39,-21) = scr (39,9). Ship NOT under box.
- THIS TURN (A246): single click ACTION6(39,9) = open prize box remotely. Next turn: read contents:
  - ORB/ring revealed -> L,L (to 37-41, rise under ring), click orb -> SINK -> falls to slab top -> descent: R,R (falls 49-53 to band top), L,L (to 37-41, falls through band hole onto plug1), R (plug2), R (falls long shaft to bottom), L,L,L (to 31-35), L (25-29 through open pocket), L (19-23), L (13-17 dock z).
  - Z revealed -> L,L -> rise into z = dock.
  - EMPTY -> do NOT move left; regrow box (click again) and rethink.
- Budget: 33/64 after A246.

## Turn 52 (A246 result: PRIZE BOX EMPTY; z-shell + buoyant-z discoveries; wrote A247-250 edge-pan probes)
- A246: box + casing fully dissolved (45 cells) -> water; X remnant remains at (39,-21). NO orb, NO z. All L6 containers now opened: everything empty. => No third mode flip exists as an object.
- CROSS-LEVEL FORENSICS (z positions over time):
  - Z's MOVE with buoyancy mode: L1 z sank in steps to floor; L4 z ROSE; L5 z sank to ship level right before dock. Z = buoyant creature like ship.
  - L5 A165->166 DOCK PROOF: ship f-cell landed on z-shell bottom-cap cell (33,40) and G overlapped z -> dock fired. => Z-SHELLS (the O plating around z, same construction as ship soft casing) DO NOT BLOCK HARD CELLS. Dock = hard f/G cells reach z cells, shell irrelevant.
  - L6 z at world 15,85-87 (plus-shape), shell caps 84/88, sides 13/17. Sink-mode ship entering slot 13-17 at floor (f 85-88) WILL DOCK. Z pinned by shell (cannot rise/sink itself).
- => WIN CONDITION FINAL: sink mode + open pocket + walk to 13-17. LOCK: orb order forced (orb1 first) makes final mode buoyant.
- LOCK-BREAK HYPOTHESIS: consume ORB2 FIRST (if orbs are toggles, one flip = SINK + pocket open; orb1 never needed!). Requires camera showing rows 84-89 while ship still up top. Camera has always tracked ship... TESTING EDGE-CLICK PANNING NOW: A247-250 = clicks (32,62),(32,63) bottom edge, (63,30) right edge, (0,30) left edge from state C=-30. If any click shifts C (big board diff) -> panning exists -> RESET, move ship over plug1 (3 rights), pan camera down, click orb2, sink-land plug1, R,R to shaft -> bottom, 4 lefts through open pocket -> 13-17 DOCK.
- If no panning: remaining ideas: orb model might be fixed-setter (orb2=buoyant-setter -> unsolvable that way); deep-undo semantics; blocked-move dock attempt (need sink at 19-23 — impossible); re-examine A175/A231 frames for transient pocket-open-while-sink windows.
- Current: ship 43-47 under ceiling 6 (f 7-10), C=-30, buoyant, budget 33/64 (37 after probes). Attempt otherwise dead (no sink available) -> RESET planned after diagnosis.

## Turn 53 (after A247-250)
- Edge-click camera panning: DEAD. All 4 clicks (32,62),(32,63),(63,30),(0,30) were no-ops (ndiff=1, budget tick only). Camera is strictly ship-tied.
- Undo atomicity RE-VERIFIED rigorously: diff(197,199)=2, diff(198,200)=2 (both diffs = budget-row ticks). A199 undo = 1 frame instant, fully restores orb2+pocket+mode+ship. Click-undo parity exploit definitively dead.
- Current state: buoyant ship parked 43-47 w7-10 under ceiling 6, C=-30, budget 37/64, both orbs consumed, pocket open, prize box dissolved (A246), plugs regrown. Attempt deadlocked barring unknown mechanic.
- NEXT DIAGNOSTIC (this turn): ACTION7 x3 — tests (a) does undo skip the 4 no-op edge clicks A247-250? (b) does undo#1 restore prize box (undoing A246)? (c) do further undos rewind ship moves A245/A244? Characterizes undo stack depth. If undo is deep + skips no-ops, could potentially rewind all the way to pre-orb2 state... but undo restores EVERYTHING so rewinding doesn't create new states, only old ones. Real value: if undo can rewind MANY actions cheaply, then after RESET we can use undo as cheap route rollback. Also: if undo #1 is a no-op itself (stack empty / no-ops not skipped), that tells us undo only reverses the immediately-preceding action.
- After this: RESET and rethink with orb model as fixed-setter test (click orb1 seat area again? seats empty though). Honest assessment: may need to reset and re-dock attempt with different order of exploration.

## Turn 54 (after A251-253) — MAJOR REFRAME
- A251-253 (3x ACTION7): all no-ops. Undo depth = exactly 1 and does NOT skip no-ops (A251 did not restore prize box dissolved at A246). Undo mechanic fully dead.
- RESET re-seals pocket: A175 opened pocket, A185 RESET, A198 re-click had dissolve frames => reset restores terrain. Pocket-persistence idea dead.
- z is STATIC in world during orb2 frames (A175 43-frame analysis: screen drift = camera scroll). L6 z is fully caged, never moves.
- n-census across ALL boards (166-253): exactly 2 red blocks ever (orb1 at band hole, orb2 at bottom tunnel). No third flip exists. Final gravity ALWAYS UP. => bottom z dock IMPOSSIBLE. It is a decoy/unreachable.
- z-census: only the one z. Purple '"' + yellow G cells = kill tower bodies/cap flanks (already modeled).
- **TOP POCKET x44-54, rows -59..-54 (6 tall = exact ship height, 2 slots wide: 43-47 & 49-53) NEVER ENTERED in any run.** Run 1 abandoned at chamber B top (A184) right below it. Best win-condition candidate.
- Run 3 decode: A234-237 clicked world (39,51)/(45,51) = PLUGS (C=42 bottom camera), not chamber remnants. A246 clicked world (39,-21) = dissolved pre-grown prize box (C=-30). Ship NEVER rose into chamber A in any run.
- **ROUTE TO POCKET from current park (43-47, f 7-10, C=-30, budget 40/64):**
  1. ACTION6(39,9) = regrow prize box at (37-41)x(-23..-19) [remnant confirmed present on A253 board]
  2. ACTION3 → 37-41, rise mid shaft x37-41 (-6..6), through floor -12 hole (open x36-53), caught under box: nose -19, f -18..-15 (box catch = same physics as plug catch)
  3. [next turn: recalibrate C ≈ -45] click remnant (33,-21) → grow platform for slot 31-35
  4. ACTION3 → 31-35 caught at f -18..-15; ACTION3 → 25-29: no ceiling tower there (verified towers only at slots 31-53), rises up shaft x25-29 (-48..-36) to chamber B, pressed under -54 (nose -53, f -52..-49)
  5. ACTION4 x3: 31-35, 37-41 (stay pressed under -54, keel soft-overlaps floor -48 during shift = OK), 43-47 → rises INTO TOP POCKET (hard trio 44-46 fits open x44-54; soft col 43 overlaps = OK). If not win, ACTION4 → 49-53 fully inside pocket.
  - WARNING: pocket entry is irreversible (buoyant, L exit blocked at height). Attempt is dead anyway if this fails → then RESET.
- Kill-safety verified: no purple towers at x25-29 ceiling -36; floor -12 under-towers at slots 13-35 hang at rows -11..-7 x14-34, rising col x37-41 clear.

## Turn 55 (after A254-255)
- A254 regrow box OK (5 frames). A255 L: ship rose mid shaft (30 frames), caught under box at slot 37-41, f world -17..-14 (casing bottom -18 is the catch, my -19 estimate was off by one). C=-54 (tower caps at screen 17/43 confirm).
- Executing pocket run: ACTION6(33,33)=grow platform (33,-21) [casing x30-36 rows -24..-18, clear of ship], L->31-35 (f stays -17..-14 under casing row -18), L->25-29 rise shaft x25-29 to chamber B (nose -54 overlap, f -53..-50, keel -49), then R,R,R -> 31-35,37-41,43-47 (keel -48/-49 soft overlaps fine) with 43-47 rising into TOP POCKET (f -59..-56, nose -60 overlap, keel -55), plus final R -> 49-53 deeper in pocket.
- Budget: 42/64 used before this batch; 7 actions -> 49/64. If pocket is not the win: attempt dead, RESET next turn and rethink with remaining knowledge.

## Turn 56 (after A256-262) — pocket NOT the goal; corrected world map
- Pocket run executed flawlessly (A258 42-frame rise to chamber B, A261 12-frame rise into pocket, A262 R to 49-53). Score still 5. TOP POCKET IS NOT THE WIN. Ship stuck in pocket (L exit blocked, buoyant). Attempt dead, 49/64 budget.
- REBUILT world composite programmatically: /workspace/l6_world2.pkl = (comp dict (r,x)->char, assigned dict action->camera C). /workspace/l6_map.txt = full render rows -96..121. All 97 boards calibrated; cameras {-96,-90,-54,-30,-12,0,16,42,58}. l6d was C=-30 NOT -12 (old notes' left-pocket/slab geometry was wrong).
- CORRECTED GEOMETRY (key): under-slab corridor rows 25-29 spans x13-53 (floor=band top 30, safe, no towers). Left pocket x13-29 rows 13-24 opens DOWNWARD into that corridor; remnants (15,21),(21,21),(27,21) grow ceiling blocks rows 19-23 protecting from inverted towers (bodies 7-10, caps G$G at 11, rock row 12). Start cavern open x13-36 to floor 54 (towers below, caps 55, G$G); shelf at x37-49 row 48 = plug casing tops (plugs are cased boxes rows 49-53 sitting on floor 54; dissolving them removes the landing shelf). 1-wide slits x18,24(,30) pierce floors 54, -12, 12 but all dead-end in tower strips — purpose unknown, likely decor. Tower caps are G$G (yellow-white-yellow); '?' in composite = my f/G filter.
- Row 63 = step budget bar (1 purple per action, resets on RESET). NOT a resource meter (earlier 'meter' reading was a camera-alignment artifact comparing screen-fixed UI across different cameras).
- World-aligned orb diffs: orb clicks change ONLY their own block+casing cells (plus budget bar). No remote side effects. Lock fully confirmed: 2 flips, final=UP, z needs DOWN. 
- UNTESTED MECHANIC: budget exhaustion (bar full at 64). Never observed. Hypothesis worth testing: auto-reset on budget-exhaust may differ from manual RESET (preserve terrain? restore orbs but keep tunnel open? increment attempt?). If it restores orbs but preserves open tunnel => WIN LINE: orb1, descend, walk left through open tunnel, dock.
- THIS TURN: burning exactly 15 blocked right-moves (ship at 49-53 in pocket, right wall x55 solid, blocked move = turn only, safe) to reach 64/64 and observe.
- If auto-reset = same as RESET: next plan = fresh attempt; remaining untried interactions: left-pocket remnants (15,21),(21,21),(27,21); chamber-A remnants (15,-21),(21,-21),(27,-21),(45,-21),(51,-21); deliberate death semantics (dissolve plug under parked ship); clicking orb1 site remnantless water; proximity clicks near z with sink ship at 19-23?? (unreachable).

## Turn 57 (after A263-278; DEATH SEMANTICS REFRAME; wrote A279-281)
- A263-277: 15 blocked rights filled bar to 64. A278 AUTO-RESET: board byte-identical to pristine A166 (diff=0), attempt 1->2, budget 0. Budget exhaustion = full restore + attempt++.
- L2 DEATH FORENSICS (corrects Turn 48 "nothing exploitable" claim):
  * A18 frames: ship rises 16 frames, DISSOLVES at frame 16-17, frames 17-27 = NO SHIP anywhere. No auto-respawn.
  * A19 header already "Attempt 2" -> death itself incremented attempt.
  * Aligned diff A18-settled vs A19-post-RESET (shift -24, 0.95 corr): the two dissolved green blocks REMAINED DISSOLVED post-death; RESET restored them. DEATH PRESERVES DISSOLVED TERRAIN; RESET RESTORES IT.
  * Budget row continues through death (Turn 48 obs). Death = ship removal + attempt++ ONLY. Post-death playability NEVER tested (L2 went straight to RESET).
- LOCK RELEVANCE: win needs DOWN gravity + open tunnel simultaneously; orb2 opens tunnel but flips UP. If death preserves orb-dissolved state AND gravity mode, or if post-death respawn has exploitable state, lock may break. Orbs-restored-but-tunnel-open is IMPOSSIBLE (orb2 assembly IS the tunnel fill).
- THIS TURN TEST (A279-281): ACTION6(39,33) click orb1 from pristine start (C=0) -> DOWN -> ship falls slot 19-23 onto floor 54, kill tower cap 55 below (1px rule) -> expected DEATH (1 action!). Then ACTION4 x2 = post-death probes WITHOUT reset: does ship respawn? does anything respond? is orb1 hole still open?
- Key observables next turn: (a) did fall actually kill (validates downward 1px rule); (b) post-death board: orb1 restored or still dissolved; (c) ACTION4 behavior: no-op / respawn / auto-reset; (d) if respawn: position + gravity mode.
- Branches: if post-death actions are pure no-ops -> death useless, lock stands, only untried: left-pocket remnants (15,21),(21,21),(27,21) + chamber-A remnants. If respawn with terrain preserved -> map full death-exploit line.

## Turn 58 (after A279-282; death mechanic CLOSED; wrote A283-286)
- A279: orb1 click -> ship fell slot 19-23, DIED on floor 54 (frame 15 dissolve). Downward 1px kill rule validated.
- A280: game FORCE-INJECTED RESET (attempt 2->3, repeats plan-step label; same as L2 A19). DEATH ALWAYS AUTO-RESETS NEXT ACTION -> preserved-terrain state is never playable. Death exploit DEAD. All reset paths (manual, budget, death) = full restore.
- A281-282: two rights, ship now slot 31-35 pressed under band (f 37-40, C=0), budget 2/64, attempt 3, orbs intact (RESET restored).
- Map audit: x31-35 rows 79-83 'block with plus hole' in composite = ARTIFACT (parked ship soft O shell not filtered in voting). Bottom corridor truly sealed; tunnel is sole entry, sink-only (nose 84 soft overlaps pillar cap, hard 85-88 fits tunnel).
- LAST UNTRIED LOCK-BREAK: orb-site regrow. Plugs regrow on remnant re-click; orb sites dissolve to bare water (no remnant) but re-click NEVER TESTED. If orb1 regrows -> win line: orb1 down, fall shaft (49-53), orb2 (tunnel open, rise to under-band), click (39,33) regrow, click again -> DOWN, fall to bottom, 6 lefts through tunnel -> dock z 13-17.
- THIS TURN (A283-286): R,R,R (31-35 -> 49-53 over shaft), ACTION6(39,33) consume orb1 -> ship falls straight to bottom floor at 49-53 sink mode (proven path A174). Budget 6/64.
- NEXT TURN: calibrate C (expect 42 or 58); probe z-body click (15,86 world) [never clicked z cells themselves, only shell/walls]; click orb2 ring (27,84 world); after rise to under-band: test orb1-site regrow click (39,33). If regrow works -> full win line. If all fail -> RESET; remaining: left-pocket remnants (15,21),(21,21),(27,21), chamber-A remnants row -21.

## Turn 59 (after A283-286; wrote A287-290)
- A283-285 rights OK; A286 orb1 click -> 44-frame fall, ship at bottom slot 49-53 SINK (f world 85-88, keel 89), C=58, budget 6/64, attempt 3. Orb2 intact on screen (n at x25-29 scr rows 27-29).
- THIS BATCH (C=58 now; C=0 expected after rise, per assigned[175]=0):
  A287 ACTION6(15,28) = z-BODY click probe, world (15,86) — z cells themselves never clicked before.
  A288 ACTION6(27,28) = consume orb2 (red body, world (27,86)) -> tunnel opens, flip UP, ship rises shaft to under-band 49-53, camera -> C=0.
  A289 ACTION6(39,33) = ORB1-SITE REGROW TEST (band hole, world (39,33)).
  A290 ACTION6(39,33) = if regrown: consume -> DOWN -> ship falls shaft to bottom (proven safe). If regrow flips gravity by itself, A290 hits floor rock = no-op (still fine: bottom+DOWN+tunnel open+orb1 present).
- SUCCESS next turn: ship bottom SINK + tunnel open -> 6 lefts (49->43->37->31->25[tunnel, nose 84 soft overlaps pillar cap]->19->13) = DOCK z. 
- FAILURE (regrow no-op): ship buoyant under band 49-53, attempt dead -> RESET; remaining untried: left-pocket remnants (15,21),(21,21),(27,21), chamber-A remnants row -21, z-probe results.

## Turn 60 (after A287-290; regrow DEAD, markers debunked; wrote A291-297)
- A287 z-body click (15,86): no-op (2 frames). A288 orb2 consume OK -> ship rose shaft, settled buoyant under band 49-53, C=0. A289/A290 orb1-site clicks: PURE NO-OPS (1-diff budget ticks). ORB REGROW DOES NOT EXIST. Orb sites = dead water.
- 1x2 'G markers' DEBUNKED: (40,44-45)=GG only in A172/A191/A219 (all C=16 ship-on-plug1 boards) = ship's own G sprite cells (facing indicator column). Same for (52,8-9)@A179, (38,-16..-15)@A181, (26,-52..-51)@A184. Not terrain, not collectibles.
- Lock re-derived airtight: corridor sealed except tunnel (rows 60-77 solid, slits sealed at 60, left wall x0-6, floor 90); tunnel sink-only; buoyant ship can NEVER overlap z (intermediate slot 19-23 has no low ceiling; rises to 79-82, z at 85-87). Sink after tunnel-open impossible (orb order forced, no regrow, undo atomic, death force-resets).
- LAST LEVERS: 8 never-clicked X remnants — pocket (15,21),(21,21),(27,21); chamber-A (15,-21),(21,-21),(27,-21),(45,-21),(51,-21). Could be non-block surprises (3rd orb? cage release?). Symmetry says 5x5 growers, but untested.
- THIS TURN (attempt 3 dead, orbs spent, ship 49-53 under band C=0, bar 10/64): click 3 pocket remnants at screen (15,21),(21,21),(27,21); then L,L (43-47, then 37-41 rise through open band hole to corridor f 25-28, C->-12), R,R (43-47, 49-53 rise to upper shaft top f 7-10, C->-30) — positions camera for chamber-A remnant clicks next turn at screen (15,9),(21,9),(27,9),(45,9),(51,9).
- If all 8 remnants = plain blocks: level model complete and lock unbroken -> deep rethink (question dock-overlap assumption? question orb toggle semantics? try dying while DOWN with ACTION7-after-forced-reset probe?).

## Turn 61 (after A291-297; wrote A298-307)
- A291-293: pocket remnants (15,21),(21,21),(27,21) = PLAIN 5x5 orange growers (casing 18/24, body 19-23). No surprises. 3 of 8 unknowns resolved.
- A294-297: route exact: ship now upper-shaft top 49-53 (world f 7-10), C=-30, bar 17/64. Chamber-A remnants on screen at row 9 (world -21): x15,21,27,45,51. Prize box intact (pristine restore).
- THIS BATCH (10 queued; runner will INSERT forced RESET after death, as at A280):
  1-5: click (15,9),(21,9),(27,9),(45,9),(51,9) = last 5 unclicked remnants.
  6: L -> 43-47, caught under newly-grown (45,-21) block (f -17..-14 ish).
  7: L -> 37-41, caught under prize box (f -17..-14, A181/A255 replay).
  8: L -> 31-35, UNPROTECTED ((33,-21) remnant not grown this attempt) -> rises to ceiling -36, cap -37 over 31-35 -> DEATH.
  [forced RESET injected -> attempt 4]
  9: ACTION7 = UNDO-THE-FORCED-RESET probe (never tested; undo depth 1 restores previous board — does that include reset boards? If yes -> shipless post-death terrain-preserved state!).
  10: ACTION3 = probe action in whatever state results (shipless: spawn? no-op? | pristine: harmless L to 13-17 under band).
- Key reads next turn: remnant click diffs (plain blocks?), death frames, A7-after-reset diff, final probe behavior.
- If all plain + undo-of-reset fails: L6 object/mechanic model COMPLETE and lock unbroken. Then deep rethink: dock-adjacency assumptions, orb toggle semantics (only ever clicked from one mode each), sink-death + undo probes, or accept-and-scan for overlooked cells programmatically (full-map interactable census).

## Turn 62 (after A298-308; object model COMPLETE, lock unbroken; wrote A309-314)
- A298-302: ALL 5 chamber-A remnants = plain 5x5 growers. All 10 L6 toggles are plain blocks. Census done.
- A303-305: L,L,L route as planned; A305 death at 31-35 ceiling tower (38 frames). A306 forced RESET (attempt 4).
- A307 ACTION7 after forced reset: NO-OP (1-diff). RESETS CANNOT BE UNDONE. Exotic undo probe dead.
- A308: ship moved L to slot 13-17, pressed under band (f 37-40), C=0, bar 2/64, attempt 4, all pristine.
- MODEL NOW FORMALLY COMPLETE AND LEVEL UNSOLVABLE WITHIN IT => model has a hole. Untested interaction class: clicks on STRUCTURAL cells (towers, band, slab, floors). Precedent for cell-specific click behavior: orb2 assembly (sides no-op, top-center consumed).
- THIS BATCH (all remote, C=0, ship stays 13-17): (15,55) floor54-tower cap $ center; (15,57) tower body; (15,11) inverted pocket-tower cap; (39,21) slab interior; (25,33) band interior; (45,33) band-right interior. Risky clicks LAST: if band dissolves, ship rises into pocket slot 13-17 -> cap 11 death -> forced reset (acceptable; coords stay valid post-reset at C=0).
- If all no-op: next census wave: floor 54 cells, rock cells, z-shell corner cells (need bottom camera), pillar row 84 cells, box wall cells (O casings of towers, e.g. (13,55)/(17,55)).

## Turn 63 (after A309-314; L4/L5 forensics; wrote A315-324)
- A309-314: ALL structural clicks no-op (tower cap $, tower body, inverted cap, slab, band x2). Structure inert.
- L5 A138/A139 decoded: staged descent through dissolvable GREEN platform blocks (camera fell 24 then 6). Greens = L2-style platforms; L6 has ZERO green cells.
- L4 decoded (camera chain): multiple red orbs, alternating UP/DOWN flips down a deep world (win at world row ~187). KEY PATTERN: A119 orb click -> bad rise -> A120 UNDO (restores orb + mode + position) -> A121 reposition -> A122 re-click same orb from better spot. Undo-retry of orb clicks confirmed as intended mechanic (works in L6 too, but repositioning doesn't beat the pillar).
- Plug-dissolve audit: casing removal exposes hidden 1-wide floor-54 slits at x36/x42 (like x18/24/30). Cosmetic.
- A204 audit: ship WAS clicked dead-center while buoyant = genuine no-op. Sink-ship-click still untested (do NOT test pre-orb2 — if it toggles mode we lose sink).
- LAST QUIRK CANDIDATES: orb2 assembly cells never clicked: bottom row (24-30,89), corners (24/30,84),(24/30,85). Cell-specific precedent: top-center (27,84) CONSUMED+flip; mid-sides (24,86),(30,86) NO-OP. If some cell dissolves WITHOUT flip -> sink+open tunnel -> dock = WIN.
- THIS BATCH (attempt 4, ship 13-17 under band, bar 8/64): 6 rights -> 49-53, orb1 (39,33) -> fall to bottom C=58 sink; then probe assembly bottom cells at screen (27,31),(24,31),(30,31) = world (27,89),(24,89),(30,89).
  Outcomes: dissolve-no-flip = JACKPOT (next turn 6 lefts dock); consume+flip = ship rises under band (then next turn test SINK... no, test ship-click-while-buoyant? already no-op; instead RESET); no-op = more probes next turn: (24,26),(30,26)=world row 84 corners, (24,27),(30,27)=row 85 corners, then core consume + park for any remaining ideas.

== TURN 64 (after A315-324) ==
- A321 orb1 consumed (fall 44fr), A322 click world (27,89) = assembly BOTTOM-CENTER -> CONSUMED orb2 + flip UP (44fr). So consuming cells = core, top-center (27,84), bottom-center (27,89). Mid-sides (24,86),(30,86) no-op. A323/324 wasted (camera moved to C=0, clicks hit water). LESSON: never queue clicks after a potential flip in same batch.
- Upper-map anomaly sweep: nothing new; matches established model (all decoys).
- L1 WIN FORENSICS (decisive): L1 ship = 4x3 diamond core + O soft shell ring (z = identical parked ghost-ship). A16 Left slid ship core THROUGH z shell ring (ring vanished frame 2) into EXACT core overlap (top-aligned) -> score++. So z shell/caps/ring are NON-BLOCKING soft cells; dock = core-on-core overlap. L6 dock therefore = sink ship slot 13-17, core rows 85-88 over z rows 85-87. Confirms lock: sink-mode corridor entry still required.
- THIS TURN (attempt 5): RESET, 6 rights -> 49-53, orb1 (39,33) -> fall C=58, probe 6 assembly corners: screen (24,27),(30,27),(24,31),(30,31),(24,26),(30,26) [= world rows 85,89,84 at x24/30], then 6 lefts.
  * If any corner dissolves tunnel WITHOUT flip: lefts transit tunnel -> corridor -> slot 13-17 = DOCK/WIN.
  * If a corner consumes+flips: camera moves, later clicks/water no-ops, lefts pillar-blocked (harmless).
  * If all no-op: lefts park ship sink at 31-35, orb2 intact — ideal staging for next-turn core-click/undo experiments.

== TURN 65 — FULL SOLUTION DECODED ==
- A333: assembly corner (24,85) = 4th consuming cell (flip UP). A340: buoyant ship ROSE THROUGH BAND HOLE (orb1 gone) into upper world. A342 death at pocket 25-29.
- ORB3 EXISTS: red orb embedded in rock, world rows -95..-91, x49-53. Clickable only from top pocket (C=-96), screen (51,3).
- DEATH RULE (final): pressing/landing against 1-THICK barrier with $-cap tower behind = death (A279 sink-landing floor54/caps55; A342 buoyant-press row12/caps11). MINES ARE HARMLESS pass-throughs (A184,A258 rose through live mine 27). Toggle: mine X <-> 7x7 block (box = entombed mine 39; dissolve re-exposes mine, A246/254).
- PROVEN ASCENT (attempt 1): 49-53 orb1 click -> bottom; orb2 (27,29)@C58 -> top; L,L (rise band hole, C-12); R,R (right column, C-30); L,L (main shaft to under-box, C-54); grow blocks; L past blocks; rise 25-29 -> chamber B (C-90); R,R,R -> top pocket (C-96).
- THIS TURN (20 actions, from 13-17 under band): 6R -> 49-53; orb1 (39,33); orb2 (27,29); L,L; R,R; L,L [under box, C=-54]; GROW block27 (27,33) + block33 (33,33); L->31-35 (under blk33), L->25-29 (under blk27), L->19-23 (RISE to -35..-32, thick rock, mine21 pass harmless); R->25-29 (rise shaft -> CHAMBER B core -52..-49).
- NEXT TURN (expect chamber B, C=-90): R->31-35, R->37-41, R->43-47 (rise TOP POCKET, C=-96); click ORB3 screen (51,3) -> flip DOWN, fall chamber B floor 43-47 core -53..-50; L->37-41, L->31-35, L->25-29 (fall shaft, LAND ON BLOCK27 core -29..-26 SAFE); R->31-35 (block33 top), R->37-41 (box top), R->43-47 (fall to core -11..-8 on row -6); L->37-41 (fall main shaft to shelf18, core 13-16); L->31-35; L->25-29 (fall pocket, mine pass, land band-top core 25-28); then R->31-35, R->37-41 (fall band hole to plug1 top 43-46), R->43-47, R->49-53 (fall long shaft to bottom 85-88); L x6 (43,37,31,25=TUNNEL OPEN,19,13=Z OVERLAP = WIN).
- NO RESETS from here on: tunnel (orb2) stays consumed/open. Budget: 23/64 after this batch.
- Facing/turns: NO turn cost; blocked move = 3fr bump no-op. Move=5fr, fall/rise animations larger.

== TURN 66 (after A346-365) ==
- ASCENT PERFECT: A346-365 exactly as planned. Blocks grown at chamber mines 27/33 (A360/361), under-block sidle L,L,L to 19-23 rise (core -35..-32, C=-72), R into shaft -> CHAMBER B core -53..-50 slot 25-29, C=-90. Attempt 5, bar 23/64, tunnel OPEN (orb2 consumed A353, no resets since).
- THIS BATCH (20): R,R,R (31,37,43 -> rise TOP POCKET C=-96); ORB3 click screen (51,3) [world (51,-93)] -> flip DOWN, fall to chamber B floor 43-47; L,L,L (37,31,25 -> fall shaft, LAND ON BLOCK27 core -29..-26); R,R,R (block33 top, box top, 43-47 -> fall to core -11..-8); L,L,L (37 -> fall main shaft to shelf18 core 13-16; 31; 25 -> fall pocket THROUGH LIVE MINE (27,21) [assumed harmless falling] -> band top core 25-28); R,R,R,R (31; 37 -> fall band hole to plug1 top; 43 plug2 top; 49 -> fall long shaft to BOTTOM core 85-88); L,L,L (43,37,31).
- NEXT TURN: L (25-29 TUNNEL), L (19-23), L (13-17 = Z CORE OVERLAP = WIN +score). Then Level 7 begins.
- Risk: orb3 flip direction assumed DOWN (L4 alternation); pocket-mine falling pass assumed harmless (rising pass proven x2). If death: forced reset attempt 6, redo whole route (~30 actions).

== TURN 67 (after A366-386) ==
- Descent perfect through step 14 INCLUDING live-mine falling pass (A378 safe). A380 DEATH: fell through band hole at 37-41 — "plugs" DO NOT EXIST initially! They are X mines at (39,51),(45,51) that attempt 1 GREW into 7x7 blocks (A167/168) = landing pads covering spike floor 54 (caps row 55). Without pads: ship falls to keel 53 = 1-thick floor over caps = spike death. RULE CONFIRMED again.
- Attempt 6 fresh (all restored: orbs 1-3, tunnel closed, blocks gone). Ship at 13-17 under band (leftover queue moves), C=0, bar 6/64.
- REDO with fix. Batch 1 (this turn, 20): GROW PADS (39,51),(45,51); R x6 -> 49-53; orb1 (39,33) -> bottom; orb2 (27,29) -> tunnel open, rise top; L,L (band hole rise C-12); R,R (right column C-30); L,L (under box C-54); grow block27 (27,33), block33 (33,33); L (under blk33), L (under blk27).
- Batch 2 (next, 20): L (19-23 rise -35..-32); R (shaft -> chamber B); R,R,R (top pocket C-96); ORB3 (51,3); L,L,L (fall shaft -> block27 pad); R,R,R (blk33, box, 43-47 fall -11..-8); L (fall main shaft shelf18); L,L (31; 25 fall pocket -> band top); R,R (31; 37 fall band hole -> PAD1 keel 47 SAFE); R (pad2); R (49-53 fall long shaft -> bottom 85-88); L (43-47).
- Batch 3 (final, 4): L,L (37,31), L (25 TUNNEL), L (19), L (13 = Z WIN) — 5 actions. Budget total ~51/64 OK. NO RESETS.

## Turn 68 (after A406, attempt 6)
Batch 1 executed 20/20 PERFECTLY. Verified: pads grown (A387/388), orb1 (A395, ->bottom C=58), orb2 (A396, tunnel open, rise C=0), band-hole rise (A397-398), right column (A399-400), under prize box (A401-402), block27+block33 grown (A403/404), parked slot 25-29 under block27, core -17..-14, C=-54.
Batch 2 written (20): L (rise 19-23 to -35..-32); R,R,R,R (shaft -> chamber B -> top pocket C=-96); ORB3 click (51,3) = DOWN flip; L,L,L (fall to block27 pad); R,R,R (via blk33/box, 43-47 fall -11..-8); L (main shaft -> shelf18); L,L (25 fall pocket -> band top); R,R (37 fall band hole -> PAD1 keel 47 SAFE); R (pad2); R (49-53 long shaft -> bottom 85-88); L (43-47).
Expected end: ship at slot 43-47 on bottom floor, C=58ish. Batch 3 (final, 5): L,L,L,L,L -> 37,31,25(tunnel),19,13 = Z WIN at ~A431 (~51/64 budget).
ORB3 click coords (51,3) computed at C=-96 top pocket — position deterministic, click is only click in batch, safe per A323 rule since all pre-click moves have known settles.

## Turn 69 (after A426, attempt 6)
Batch 2 executed 20/20 PERFECTLY, no deaths. A412 orb3 click at C=-80 pre-settle (flip DOWN), descent chain all landings safe. A425: ship bottom floor world 85-88 slot 49-53 (C=58). A426: L -> slot 43-47. Budget 46/64.
Batch 3 written (5): L,L,L,L,L -> slots 37,31,25(through open tunnel),19,13 = core overlap with z at slot 13-17 = LEVEL 6 WIN expected at ~A431, 51/64 budget. Kept list at exactly 5 so nothing spills into unknown Level 7.

## Turn 70 — LEVEL 6 CLEARED at A431 (score 6). Level 7 begins.
L7 initial board (post-A431), screen==world? camera horizontal appears FIXED (ship at col 21, not centered); vertical likely ship-tied. Row 63 bar: ALL $ (full!) — maybe bar counts DOWN this level, or resets on level start. Monitor.
Layout (screen rows):
- Background open space = '(' light blue (water?). Walls = black O with red-brick (n 5x5) and h texture.
- Ship: core rows 37-40, cols 20-22 (f/G), BUOYANT, pressed under shelf rows 30-36 (solid cols 0-48).
- Under-shelf pocket corridor rows 37-42, cols 13-41. Mine (3x3 orange X) at (39,39). Wall cols 42-48 rows 37-53.
- Left channel cols 13-17: open rows 0-29 → buoyant ship moving left to slot 13-17 will RISE to top (row ~1) and reveal upper world.
- Wide band rows 13-23 cols 13-59 open. Rows 24-29: open except spike towers.
- SPIKE TOWERS point UP this level: purple cols 20-22 rows 26-29 + G$G cap at row 25; same at cols 44-46. Standing on shelf top (row 30). Danger to SINKING ships landing on caps.
- Mine grid (3x3 X, orange): centers (27,3),(33,3),(39,3),(27,9)... cols 27/33/39 × rows 3,9,15,21,27; also (39,39),(39,51).
- Top-right region cols 25-47 rows 1-12 (mine field), sep from left channel by wall 18-24.
- Right channel cols 49-59: open rows 0-62 full height.
- Bands rows 43-47 (cols 13-59) and 60-62 (cols 13-59); floor row 54 solid cols 0-48 (no caps seen → safe); rows 48-53 open cols 13-41.
- NO z visible on screen — target off-camera (probably above or below).
Plan: probe with single ACTION3 → ship rises left channel to top, camera scrolls up, reveals upper world.

## Turn 71 (after A432)
A432 L: ship slid to cols 14-16, rows 37-40 — did NOT rise. Shelf rows 30-36 spans cols 0-48, seals pocket above; left channel 13-17 only exists rows 0-29 (above shelf). Camera FIXED so far (board unchanged except ship+bar). Ship sprite mirrors to face movement direction (G=tail? now col 14).
Bar row 63 DEPLETES: 'z' marks fill from left per action. 1 used, 63 left.
Pocket 13-41 rows 37-42 sealed for buoyant ship (walls 0-12, 42-48, shelf above). Only object: mine (39,39). No z target visible; no orbs visible. Hypothesis: mines here may behave differently (block-grow like L6? detonate? polarity toggle?).
Test: ACTION6(39,39) click pocket mine.

## Turn 72 (after A433)
A433 click mine (39,39): grew 5x5 ORANGE brick, cols 37-41 rows 37-41, + O outline col36/row42. Same visual grammar as wall bricks (red n 5x5 @ left edge col1-5; black O 5x5 w/ h corners in shelf/walls). Mine->brick toggle confirmed for L7 (5x5 this time, brick aligned to 6-grid slot 37-41).
Hypothesis: ALL bricks clickable/toggleable -> "digging" level. Ship escapes sealed pocket by dissolving shelf brick above, then rises left channel (13-17) to top.
Test: ACTION6(15,33) — click shelf above ship (ship cols 14-16, rows 37-40).
Bar: 2 used.

## Turn 73 (after A434)
A434 click shelf brick (15,33): NO-OP (only bar mark). Black bricks INERT — digging hypothesis dead. Clicks likely only work on mines/grown bricks (like L6) + maybe ship/red bricks.
Pocket escape requires polarity flip (sink) -> fall to 43-47 band -> right to channel 49-59 (full height, rows 0-62) -> explore.
Test queue: (1) click ship (15,38) [polarity toggle?]; (2) click orange brick (39,39) [dissolve toggle]; (3) click red brick (3,39).
Bar: 3 used.

## Turn 74 (after A435)
A435 click ship (15,38): NO-OP. Ship not clickable.
Correction to layout: band rows 43-47 is FULLY open cols 13-59 (wall 42-48 exists only rows 37-42 and 48-53) -> band connects directly to right channel.
Buoyant ship physics: lateral + rise only; ceiling-stepping downward impossible (lateral move = shift 6 then settle; can't slide under a lower ceiling that overlaps current rows). So escape needs either a polarity flip mechanism or opening the shelf.
Test now: water-slot click (27,39) — does clicking empty water grow a brick (grow-anywhere hypothesis)?
Remaining candidates after: red brick (3,39); spike cap $ (21,25); orange brick dissolve (39,39); mine (39,51).
Bar: 4 used.

## Turn 75 (after A436)
A436 water click (27,39): NO-OP. Clicks do NOT grow bricks in empty water. Confirmed inert so far: black bricks, ship, water. Only mines interactive (grow 5x5 orange brick).
Batch probe (3): red brick (3,39); spike cap $ (21,25); purple tower (21,27). All remote from ship; if surprise flip occurs mid-batch, later clicks land on inert shelf regions (safe).
If all no-op: interactive surface = 17 mines only -> solution must be built entirely from mine-brick engineering; will then think hard about what pattern of grown bricks changes physics for the ship (water displacement? sealed air chambers?).
Bar: 5 used.

## Turn 76 (after A439) — BREAKTHROUGH
A437 click RED BRICK (3,39): brick CONSUMED (col 1-5 world 37-41 now water) + POLARITY FLIP -> ship sank from pocket to world 49-52 cols 14-16 (on bottom shelf top, keel 53, floor 54). Camera C=22. A438 cap click, A439 tower click: NO-OPs.
RED BRICKS = one-shot polarity flips, clickable REMOTELY. ~10 remain on left border col 1-5, world rows 3,9,15,21,27,33,[39 used],45,51,57,63,69,75,81.
Z TARGET VISIBLE: caged (thin O shell) at world rows 72-76 cols 19-23, bottom-left region.
World map additions (world rows):
- wall cols 42-48: worlds 37-42 AND 48-53 (gap at 43-47 band). Orange brick (grown) worlds 37-41 cols 37-41 + outline 36/42.
- bottom shelf 54-60 cols 0-48. Band 61-65 open 13-59. World 66: wall 49-53, open 13-48 + 54-59.
- SPIKE TOWER #3 (up-cap): cap world 67 cols 50-52, tower 68-71 — DEATH TRAP under channel slot 49-53 (thin wall 66 above it -> landing = thin-barrier death rule).
- z cage worlds 72-76 cols 19-23; solid block cols 30-42 worlds 72-84; open cols 13-29 worlds 61-84 (except cage); open 43-59 worlds 79-84; chute 55-59 clear worlds ~0-83, floor 84 (safe, no caps).
PLAN (17 actions total, 4 turns):
A: R,R,R,R (slots->37-41 on shelf, mine harmless), FLIP click (3,29) [world (3,51) brick] -> rise under orange brick 43-46; R (under wall bottom 42), R (rise channel 49-53 -> press under wall 48-54 at 13-16), R (rise 55-59 chute to top ~world 0-4). [THIS TURN]
B: FLIP DOWN (new click coords) -> fall 55-59 to 80-83 floor 84; L (49-53), L (43-47).
C: FLIP UP -> rise 43-47 to under bottom shelf 61-64; L,L,L (37-41,31-35,25-29); L (19-23).
D: FLIP DOWN -> fall onto z cage (world 72) -> core overlap -> WIN.
Note: if flip is not a toggle (sets DOWN only), batch A's last 3 rights bump harmlessly at wall 42-48 — safe failure mode.
Bar: 8 used.

## Turn 77 (after A448) — attempt 1 died, full analysis
A447 DEATH: rising 55-59 chute hit DOWN-CAP at ~world -49 (tower 56-58 hangs from slab -54, cap at bottom). A448 forced RESET -> attempt 2, ship back in pocket 19-23, ALL state restored (mine 39,39 back, red bricks back), BAR RESET TO 0 (deaths clear budget).
Recon from death-pan (frames static C=-24 reliable for world -24..39; pan rows -84..-25 UNRELIABLE ±3):
- World -84..-79: open sky. Slab -78..-54 full width. Chute 43-47: worlds -53..-12, mines at (45,-51?),(45,-45?),(45,-39?),(45,-33?),(45,-21 CONFIRMED static). Chute top -53..-50 SAFE press (no caps). Chute FLOOR = slab -12 (43-54, 1-thick, UP-cap tower 44-46 at -11..-7 beneath = LANDING DEATH).
- Zone -41..-31: open 43-59 (SKETCHY: -31 row contradicts -30; needs recon). Block 48-54 @-48..-42 above; pillar 48-54 top ~-30 below.
- Upper-left region: cols 13-29(35), worlds -29..-7. Ceiling -30 (slab 0-42). HANGING towers+DOWN-caps: 26-28 & 38-40 @-29..-26, caps -25 (block slots 25-29,37-41 for buoyant). Pillar towers+UP-caps: 32-34 & 44-46 @-10..-7, caps -11, under 1-gaps (block slot 31-35 for sinking at slab level). Slab -6..0 (18-54). Mines upper-left: (21,-27),(21,-21)?,(27,-21) CONF,(21,-15)?.
- PRE-GROWN dissolvable orange bricks: hole1 = 37-41@-23..-19 (in block 36-42@-24..-18); hole2 = 31-35@-17..-13 (in block 30-36@-18..-12).
- Minefield room: cols 25-47, rows 1-12, sealed except bottom (band 13-23). Mines (27,3),(33,3),(39,3),(27,9),(33,9),(39,9); band mines (27,15),(33,15),(39,15),(27,21),(33,21),(39,21); shelf-top mines (27,27),(33,27),(39,27).
- Mid-shelf-top (keel on 30): slots 25-41 safe; 19-23 & 43-47 = tower boxes (lid 24, cap 25 = landing DEATH).
- 49-53 chute: 13..65 open, wall 66 (1-thick) + cap 67 = landing DEATH. 55-59 chute: -48..83 open, killer cap -49 at top, floor 84 safe.
- z cage 19-23@72-76; bottom cavern 13-48 x 61-71 open; block 30-42@72-84; bottom-left 13-29@77-84 open (below 84 unknown); bottom-right 43-59@79-83, floor 84.
ROUTE TO PERCH (validated on reliable data): grow (39,39)+(27,9) at C=0; flip red (3,39) -> corridor 19-23@49-52 C=22; R,R,R -> 37-41; flip (3,29)[world 3,51] -> press under pocket brick 43-46; R (under wall 43-46); R (rise 49-53 -> 13-16 under wall 48-54) [BATCH 1 = this turn, 9 actions]. Then L,L,L -> minefield 31-35@1-4; flip down -> shelf-top 26-29; L -> 25-29; flip up -> press under brick(27,9) @13-16; L (19-23@13-16); L (13-17 -> RISE channel -> PERCH core -29..-26). RECON from perch (C~-55 shows -55..8) then decide endgame (candidate: hole1 dissolve + chute-brick stops -> 55-59 drop at -32 -> floor 84 -> flip up -> band 61-64 -> L to 19-23 -> flip down onto z cage).
DANGER LIST (never): rise at 55-59 (cap -49); land 49-53 bottom (wall66/cap67); land on tower lids (19-23/43-47 rows 24); fall at 43-47 chute to floor -12; lateral into caps (32-34/44-46 @-11..-7; 26-28/38-40 @-29..-25); fall past 84 at 13-29 (unknown abyss).
Bar: 0 (reset). Batch 1 = 9 actions.

== TURN 78 (after A457) ==
Batch 1 SUCCESS: ship 49-53 @ world 13-16 pressed under wall 48-54. C=-24 at A457.
Recon from this view: chute 43-47 mines confirmed at (45,-21) AND (45,-15) [new]. hole1 orange brick visible world -23..-19 cols 37-41. Red bricks continue every 6 up: -21,-15,-9,-3 all present.
Bar: 9 used.
BATCH 2 (this turn): L,L,L -> ship rises into minefield room, ends 31-35 @ core 1-4 pressed under slab row 0. Vertical move 12 rows -> C uncertain after; flip-down click deferred to batch 3 (measure C first).
Then batch 3: flip↓ (red brick at current C) + L -> shelf-top 25-29 core 26-29. Batch 4: flip↑ + L + L -> rise 13-17 channel to PERCH core -29..-26.

== TURN 79 (after A460) ==
Batch 2 SUCCESS: ship 31-35 @ world core 1-4 under slab. C=-36 (caps at screen 11/25/61 = world -25/-11/25).
BATCH 3 (this turn): ACTION6(3,39) = red brick world (3,3) -> flip DOWN; ship falls to shelf-top core ~26-29 (slot 31-35, mines pass-through); then L -> slot 25-29 on shelf top.
Fall ~25 rows -> C unpredictable after. Batch 4 next turn: measure C, flip UP (red click), press under grown brick 25-29@7-11 core ~13-16; L -> 19-23@13-16; L -> 13-17 channel RISE to PERCH core -29..-26.
Red bricks remaining: world y in {-33..-3 step 6 above, 3,9,15,21,27,33} (39,51 consumed).

== TURN 80 (after A462) ==
Batch 3 SUCCESS: flip↓ + L -> ship slot 25-29 core world 25-28 on shelf-top. C=-2. Bar 14.
Verified: red (3,9) alive at screen (3,11); grown brick 25-29@7-11 with O outline bottom world 12 (matches wall 18-24 bottom) -> press-under core 13-16, seamless L slides.
BATCH 4 (this turn): ACTION6(3,11)=flip UP [consumes red (3,9)] -> press under brick core 13-16; L -> 19-23@13-16 under wall; L -> 13-17 channel, RISE ~42 rows -> PERCH core -29..-26 (ceiling -30).
Next turn: RECON from perch (C should show ~-55..8): verify zone -41..-31 cols 43-59, chute 43-47 mines (-51?,-45?,-39?,-33? + confirmed -21,-15), pillar 48-54 top, block 48-54@-48..-42. Then plan endgame descent.
Red bricks remaining after this: 15,21,27,33 (+ any above -3: -9,-15,-21,-27,-33...).

== TURN 81 (after A465) == PERCH REACHED, FULL RECON DONE, ROUTE SOLVED ==
Ship 13-17 core -29..-26 UP, C=-66, bar 17. Killer cap 55-59 confirmed at -49 (tower 56-58@-53..-50).
MAP CORRECTIONS (l7_world.pkl = stitched authoritative map, world rows -84..84):
- Initial-board camera was C=0 (NOT 22); attempt-1 boards A437-443 C=22, A444-445 C=6, A446 C=-24, A447 death C=-84.
- Right shaft cols 49-59 open rows 24-60 (11 wide); pillar 48-54 = rows -30..12 only; mid shelf 0-48@30-36; wall 42-48@37-53.
- Bottom: rows 61-65 open 13-59; row 66 WALL at 49-53 + UP-cap (50-52,67) + tower 50-52@68-71 [death to land/rise at 49-53 bottom]; rows 66-71 open 13-48 & 54-59; rows 72-78 open 13-19?,24-29,43-47,55-59 (block 30-42, pillar 48-54); rows 79-83 open 13-29,43-59; row 84 SOLID 43-59 (floor), OPEN 13-29 (abyss? never fall there).
- z cage: plates 20-22@72 & 20-22@76, side walls 19,23@73-75, z inside at 20-22@73-75.
- Zone -41..-31: cols 43-59 fully open. Block 48-54@-48..-42. Chute 43-47 mines every 6: -51,-45,-39,-33,-27,-21,-15. Upper mines: col 21 @-21,-15,-9; col 27 @-21. hole1 brick 37-41@-23..-19 in block 36-42@-24..-18 (cap of tower 38-40 sits at -25 on block top -24). hole2 brick 31-35@-17..-13 in block 30-36@-18..-12. Towers 26-28&38-40@-29..-26 caps -25; towers 32-34&44-46@-10..-7 caps -11 on slab 18-54@-6..0.
KEY INSIGHT: transit corridor at core rows -17..-14: press under grown brick(21,-21) outline(-18) at 19-23 -> under grown brick(27,-21) outline(-18) at 25-29 -> through DISSOLVED hole2 cavity at 31-35 -> under block 36-42 bottom(-18) at 37-41 -> chute 43-47 RISE to safe top press core -53..-50. Then grow (45,-33) brick, flip DOWN: land core -40..-37 -> R pillar-top core -35..-32 -> R BIG DROP 55-59 to floor 84 core 79-82 (only safe bottom entry, proven by elimination). Then L,L, flip UP at 43-47 -> press under shelf bottom 60 core 61-64 -> L x4 -> 19-23@61-64 -> flip DOWN -> fall onto z cage (thin shell assumed pass-through) = WIN.
BATCHES: A(this turn,4): grow(27,-21)=scr(27,45); dissolve hole2 (33,-15)=scr(33,51); R->19-23; flipDOWN red(3,-15)=scr(3,51) -> ship falls to slab core -11..-8 (brick 21 NOT grown yet so fall is clear; mines pass). B(6): [measure C] grow(21,-21); flipUP red; R,R,R,R -> chute top -53..-50. C(4): [measure C] grow(45,-33); flipDOWN red; R; R -> core 79-82. D(3): [measure C] L; L; flipUP red -> core 61-64. E(5): [measure C] L,L,L,L; flipDOWN red -> WIN. Total 22 more, ~39 bar.
CHECK batch A result: hole2 dissolve is UNTESTED assumption — verify brick 31-35@-17..-13 gone next turn; if not, replan (ship safe on slab either way).
Reds consumed (attempt2): 39,51,3,9 (+ -15 after batch A).

== TURN 82 (after A469) ==
Batch A SUCCESS: ship slab 19-23 core -11..-8, C=-38, bar 21. Brick (27,-21) GROWN ✓. Hole2 DISSOLVED ✓ — BUT structure surprise: cols 31-35 now open -18..-13 (former block top -18 GONE); only 1-row ledge 31-35@-12 remains (cap -11 beneath at 32-34 = landing DEATH). Dissolve REVEALED MINE (33,-15): mines<->bricks are toggle pairs!
REVISED CROSSING (31-35 shaft has no mid ceiling): enter 31-35 at -17..-14 -> auto-rise to core -29..-26 pressed under -30 BETWEEN towers (safe, verified open; caps at 26-28/38-40 don't touch cols 31-35). Then re-grow brick (33,-15), flipDOWN -> land on its top -17 -> core -22..-19. R -> 37-41 (hole1 dissolved; if bottom outline -18 remains: land core -23..-20; if all gone: fall to slab -6 core -11..-8 SAFE but then R=DEATH at cap (44-46,-11) — MUST CHECK hole1 remnant next turn before the second R). R -> 43-47 land on grown brick (45,-15) top -17 core -22..-19. flipUP -> chute top -53..-50. grow (45,-33), flipDOWN -> core -40..-37, R -> pillar-top -35..-32, R -> BIG DROP 55-59 -> core 79-82. L,L, flipUP -> 43-47 rise -> core 61-64 under shelf. Lx4 -> 19-23@61-64. flipDOWN -> fall onto z cage. WIN.
BATCH B (this turn, 6): grow(21,-21)=scr(21,17); dissolve hole1 (39,-21)=scr(39,17); grow mine(45,-15)=scr(45,23); flipUP red(3,-21)=scr(3,17); R; R -> end: ship 31-35 core -29..-26 between towers.
NEXT (batch C): [measure C] verify hole1 remnant; grow(33,-15); flipDOWN red; R (onto 37-41) — then decide 2nd R based on hole1 obs.
Reds consumed: 39,51,3,9,-15,(-21 after this batch).

== TURN 83 (after A475) ==
Batch B SUCCESS: bricks (21,-21),(27,-21) grown (outline tops -24 solid, bottoms -18); hole1 FULLY dissolved (revealed mine (39,-21); cols 37-41 open -23..-7 EXCEPT solid row -24 remains = ceiling!); brick (45,-15) grown (outline box: top -18 cols 42-48, body -17..-13, bottom merges floor -12). Ship 31-35 core -29..-26 between towers, C=-66, bar 27.
Grown-brick rule refined: outline = full solid box; landing surface = outline TOP (e.g. -18 for (33,-15) brick).
BATCH C (this turn, 3): grow (33,-15)=scr(33,51); flipDOWN red (3,-27)=scr(3,39); R. -> fall onto brick(33) box top -18 core -23..-20; R falls 37-41 to slab core -11..-8 (SAFE: no caps at 37-41; -24 row is only solid above).
BATCH D next: [measure C] flipUP red; R. -> rise 37-41 to ceiling -24 press core -23..-20; R -> 43-47 rises full chute to top press core -53..-50 (chute clear: only mines).
Then E: [measure C] grow(45,-33); flipDOWN red; R; R -> land -40..-37, pillar-top -35..-32, BIG DROP -> 79-82. F: L,L,flipUP -> 61-64. G: Lx4, flipDOWN -> z WIN.
DANGER reminders: never R from slab 37-41 (cap 44-46@-11); never fall at 31-35 without brick (ledge -12+cap).
Reds consumed: 39,51,3,9,-15,-21,(-27 after this).

== TURN 84 (after A478) ==
Batch C SUCCESS: ship slab 37-41 core -11..-8, C=-38, bar 30. Brick (33,-15) grown.
BATCH D (this turn, 2): flipUP red (3,-9)=scr(3,29); R. -> rise to ceiling -24 press core -23..-20; R -> 43-47 RISE full chute -> top press core -53..-50.
BATCH E next: [measure C] grow (45,-33); flipDOWN red; R; R -> brick top (outline -36? NOTE: grown brick (45,-33) outline box top = -36! land core -41..-38, recheck rows); R -> pillar-top; R -> BIG DROP -> 79-82.
  CORRECTION to E plan: brick (45,-33): body -35..-31, outline TOP -36 (cols 42-48) -> landing core -41..-38 (not -40..-37). Then R->49-53: rows -41..-38: zone open -41..-31 OK (row -41 open) -> falls to pillar top -30 -> core -35..-32. R -> 55-59 rows -35..-32 zone open -> BIG DROP to floor 84 core 79-82. Still valid.
F: L,L,flipUP -> 43-47 rise -> core 61-64. G: Lx4, flipDOWN -> z WIN.
Reds consumed: 39,51,3,9,-15,-21,-27,(-9 after this).

== TURN 85 (after A481) == DEATH A479 + RESET -> ATTEMPT 3 ==
DEATH CAUSE: flipUP at slab 37-41 pressed core -23..-20 under 1-THICK row -24 with DOWN-cap at -25 directly behind = thin-barrier+cap death (L6 rule — applies to CEILING presses too, not just floors!). NEVER press under a 1-thick row with a cap behind it.
FIX: after slab drop at 37-41 core -11..-8: RE-GROW hole1 via revealed mine (39,-21) (mine<->brick toggle), then flipUP -> press under hole1 BOX BOTTOM -18 (thick: brick body -23..-19 behind = SAFE) -> core -17..-14 -> R -> chute 43-47 (KEEP CLEAR: never grow (45,-15) this attempt) -> rise to top press core -53..-50 (thick ceiling -54.. SAFE).
ATTEMPT 3 STATE: ship 25-29@37-40 pocket (A481 R executed), C=0, bar 1. All bricks/mines/reds RESET.
FULL ROUTE (validated steps marked ✓):
S1(8,this turn): grow(39,39)scr(39,39)✓; grow(27,9)scr(27,9)✓; flipDOWN red(3,39)scr(3,39)✓ -> fall 25-29@49-52; R; R -> 37-41@49-52✓; flipUP red(3,51)scr(3,29)[C=22 twice-validated]✓ -> press 43-46 under pocket brick; R -> band 43-46✓; R -> 49-53 rise press 13-16✓.
S2(3): L,L,L -> minefield 31-35@1-4 ✓.
S3(2): [C] flipDOWN red; L -> shelf-top 25-29@25-28 ✓.
S4(3): [C] flipUP red -> press 13-16 under brick(27,9); L -> 19-23@13-16; L -> 13-17 RISE to perch -29..-26 ✓.
S5(4): [C] grow(27,-21); dissolve hole2 (33,-15); R -> 19-23@-29..-26; flipDOWN red -> slab 19-23@-11..-8 ✓.
S6(5): [C] grow(21,-21); flipUP red -> press -17..-14; R -> 25-29 press; R -> 31-35 shaft rise -> between towers -29..-26 ✓.
S7(3): [C] grow(33,-15); flipDOWN red -> land box top -18 core -23..-20 ✓; R -> fall thru dissolved hole1 shaft -> slab 37-41@-11..-8 ✓.
S8(3): [C] REGROW hole1 (39,-21); flipUP red -> press -17..-14 under box bottom (SAFE thick); R -> 43-47 RISE to TOP -53..-50. [NEW]
S9(4): [C] grow(45,-33); flipDOWN red -> land box top -36 core -41..-38; R -> fall pillar-top -35..-32; R -> BIG DROP 55-59 -> floor 84 core 79-82.
S10(3): [C] L; L; flipUP red -> 43-47 rise -> press 61-64 under shelf bottom 60 (thick).
S11(5): [C] L,L,L,L -> 19-23@61-64; flipDOWN red -> fall onto z cage (thin shell assumed pass-through; fallback: flipUP recover).
Est total ~44 bar ✓. 11 red flips needed — all reds reset, verify on-screen red before each flip click.

== TURN 86 (after A489) ==
S1 SUCCESS (identical to attempt 2): ship 49-53 @ world 13-16, C=-24, bar 9.
S2 (this turn, 3): L,L,L -> minefield room 31-35 core 1-4 under slab.
Next S3: [measure C] flipDOWN red; L -> shelf-top 25-29@25-28.

== TURN 87 (after A492) ==
S2 SUCCESS: ship 31-35 core 1-4, C=-36 (same as attempt 2), bar 12.
S3 (this turn, 2): flipDOWN red(3,3)=scr(3,39) [validated A461]; L -> shelf-top 25-29 core 25-28.
Next S4: [measure C] flipUP red -> press 13-16 under brick(27,9); L; L -> 13-17 rise to perch -29..-26.

== TURN 88 (after A494) ==
S3 SUCCESS: ship shelf-top 25-29 core 25-28, C=-2 (same as attempt 2), bar 14.
S4 (this turn, 3): flipUP red(3,9)=scr(3,11) [validated A463]; L -> 19-23@13-16; L -> 13-17 channel RISE -> perch core -29..-26.
Next S5: [measure C, expect -66] grow(27,-21); dissolve hole2 (33,-15); R; flipDOWN red -> slab 19-23@-11..-8.

== TURN 89 (after A497) ==
S4 SUCCESS: perch 13-17 core -29..-26, C=-66 (same as attempt 2), bar 17.
S5 (this turn, 4): grow(27,-21)=scr(27,45); dissolve hole2=scr(33,51); R -> 19-23@-29..-26; flipDOWN red(3,-15)=scr(3,51) -> fall to slab 19-23 core -11..-8. [all validated A466-469]
Next S6: [measure C, expect -38] grow(21,-21)=scr(21,17); flipUP red(3,-21)=scr(3,17); R; R -> between towers 31-35@-29..-26.

== TURN 90 (after A501) ==
S5 SUCCESS: slab 19-23 core -11..-8, C=-38 (same as attempt 2), bar 21.
S6 (this turn, 5): grow(21,-21)=scr(21,17); DISSOLVE HOLE1=scr(39,17) [needed for S7 fall-through shaft]; flipUP red(3,-21)=scr(3,17); R -> 25-29 press -17..-14; R -> 31-35 shaft rise -> between towers core -29..-26. [validated A470-475, minus grow(45,-15) which must NOT happen]
Next S7: [measure C, expect -66] grow(33,-15)=scr(33,51); flipDOWN red(3,-27)=scr(3,39); R -> land box top -18 core -23..-20 then fall thru hole1 shaft to slab 37-41 core -11..-8.

== TURN 91 (after A506) ==
S6 SUCCESS: between towers 31-35 core -29..-26, C=-66 (same as attempt 2 A475), bar 26. Bricks (21,-21),(27,-21) grown; hole1 dissolved (mine 39,-21 revealed); chute 43-47 CLEAR.
S7 (this turn, 3): grow(33,-15)=scr(33,51); flipDOWN red(3,-27)=scr(3,39); R -> land brick33 box top -18 core -23..-20, then R falls thru hole1 shaft -> slab 37-41 core -11..-8. [validated A476-478]
Next S8 (NEW, the death-fix): [measure C, expect -38] REGROW hole1 via mine(39,-21)=scr(39,17)@C=-38; flipUP red -> press core -17..-14 under hole1 box bottom -18 (THICK=safe); R -> 43-47 RISE to top press core -53..-50.

== TURN 92 (after A509) ==
S7 SUCCESS: slab 37-41 core -11..-8, C=-38, bar 29. Mine (39,-21) confirmed present.
S8 (this turn, 3) THE FIX: regrow hole1 via mine(39,-21)=scr(39,17); flipUP red(3,-9)=scr(3,29); R -> press core -17..-14 under hole1 box bottom -18 (thick brick body above = SAFE, unlike the -24 cap death); R -> 43-47 chute (clear) RISE ~36 rows to top press core -53..-50.
Reds remaining in view at C=-38: -33(scr5), -9(scr29->consumed now), -3(scr35), 15(scr53), 21(scr59).
Next S9: [measure C, expect ~-77?] grow mine(45,-33); flipDOWN red -> land box top -36 core -41..-38; R -> pillar-top core -35..-32; R -> BIG DROP 55-59 -> floor 84 core 79-82.

== TURN 93 (after A512) ==
S8 SUCCESS — DEATH-FIX VALIDATED: hole1 regrown, thick press at -17..-14 worked, ship rose chute to TOP press 43-47 core -53..-50. C=-90, bar 32.
S9 (this turn, 4): grow mine(45,-33)=scr(45,57) [confirmed on screen]; flipDOWN red(3,-39)=scr(3,51); R; R.
Expected: fall from -50 -> land brick box top -36 -> core -41..-38; R -> 49-53 falls to pillar-top -30 -> core -35..-32; R -> 55-59 BIG DROP (~115 rows) -> floor 84 -> core 79-82.
Next S10: [measure C, expect ~+40s] L; L; flipUP red -> 43-47 rise -> press under shelf bottom 60 -> core 61-64.
Then S11: L,L,L,L; flipDOWN red -> fall onto z cage (pass-through assumed) = WIN.

== TURN 94 (after A516) ==
S9 SUCCESS: big drop survived! Ship 55-59 core 79-82 on floor 84, C=52, bar 36.
S10 (this turn, 3): L -> 49-53@79-82; L -> 43-47@79-82; flipUP red(3,75)=scr(3,23) -> rise 43-47 (72-78,66-71,61-65 all open) -> press under bottom shelf 60 (thick) -> core 61-64.
Next S11: [measure C] L,L,L,L -> 19-23@61-64; flipDOWN red -> fall 65-71 -> z cage plate 20-22@72 (thin-shell pass-through assumed; if ship lands on top core 67-70 instead: flipUP to recover and rethink).

== TURN 95 (after A519) ==
S10 SUCCESS: ship 43-47 core 61-64 pressed under bottom shelf, C=24, bar 39.
S11 (this turn, 5) FINALE: L,L,L,L -> 19-23@61-64 (ceiling 60 continuous, rows 61-65 open); flipDOWN red(3,63)=scr(3,39) -> fall 65-71 -> z cage 19-23@72-76 (z at 20-22@73-75). Expect LEVEL CLEAR (score 7).
Fallback if cage plate blocks (ship lands core 67-70): flipUP recovers to 61-64; then try clicking cage or another approach.

## Turn 96 (A524 done): LEVEL 7 CLEARED, score 7. LEVEL 8 begins.
L8 initial board (screen, C unknown, likely fresh camera):
- Ship slot 19-23, rows 37-40, UP polarity, pressed under shelf (shelf rows 30-36, spans cols 0-30 and 48-63; GAP cols 31-47).
- Seven DOWN-pointing spike towers rows 7-12: purple body rows 7-10, G$G cap row 11, 1-thick O base row 12, at cols 8-10,14-16,...,44-46. 2-wide channels between (12-13,18-19,24-25,30-31,36-37,42-43) — too narrow for ship.
- CRITICAL: gap slots 31-35/37-41/43-47 rising → press under 1-thick row 12 with cap behind = DEATH (A479 rule). Do NOT drift right with UP polarity past col 30.
- Right shaft cols 48-60 open rows 0-12, connects to band rows 13-29 above shelf. World likely extends above row 0.
- Purple 5x5 box `Oh"""hO` at cols 12-18, rows 18-24 — only novel object. NO reds, NO mines, NO z goal visible.
- Bottom floor rows 54-62 solid. Bar 0.
Probe: ACTION6(15,21) click purple box center.

## Turn 97 (A525): L8 box mechanic = SPLIT. Click box -> it dissolves, spawns 4 copies at 6-grid cardinal neighbors.
State: boxes at centers (9,21),(15,15),(15,27),(21,21). Bar 1. Ship unmoved (19-23 rows 37-40, UP under shelf).
ROUTE PLAN: need boxes at (33,21),(39,21),(45,21) as ceilings over shelf gap (bottoms row 24 -> ship pressed rows 25-28),
corridor rows 25-28 cols 31-53 must stay clear => FORBID boxes 33_27,39_27,45_27,51_27,51_21,57_15.
Never CLICK 33_21/39_21/45_21 (click removes). 39_21 must spawn from clicking 39_15; 45_21 from clicking 45_15 (spawns 51_15 shaft-blocker
-> then ship presses under 51_15 at rows 19-22 at slot 49-53, exits right via slot 55-59, free rise).
Exit: gap slot 31-35 rise -> under 33_21 -> right -> 39_21 -> 45_21 -> 49-53 under 51_15 -> 55-59 -> free rise up shaft (world above).
UNKNOWN: box-box collision on spawn (merge vs annihilate); wall-overlap spawn behavior.
This batch: click (21,21) [spawns 15_21,27_21,21_15,21_27], click (27,21) [spawns 21_21,33_21!,27_15,27_27], 
click (27,15) [TEST: spawns 21_15 OCCUPIED + 27_9 tower-overlap + 33_15 + 27_21].
DANGER: do NOT click 33_15 until collision rule known (its spawn hits needed 33_21).

## Turn 98 (A528): collision rules PROVEN: spawn into occupied box = no-op (merge); spawn into wall/tower = no-op. Clicks fully safe.
Boxes: 9_21,15_15,15_21,15_27,21_15,21_21,21_27,27_21,27_27,33_15,33_21. Ship unmoved. Bar 4.
Batch (8): click 33_15 (spawns 39_15... wait no: spawns 27_15,39_15,33_21 noop,33_9 noop), click 39_15 (spawns 33_15,45_15,39_21!,39_9 noop),
click 45_15 (spawns 39_15,51_15,45_21!,45_9 noop), then R,R,R,R,R:
19-23 -> 25-29 (under shelf) -> 31-35 (rise, press under 33_21 bottom row24, ship rows 25-28) -> 37-41 (under 39_21) -> 43-47 (under 45_21) -> 49-53 (rise, press under 51_15 bottom row18, ship rows 19-22).
Next: ACTION4 to 55-59 -> BLIND free rise up shaft (world above row 0 unknown - watch for caps).

## Turn 99 (A536): SHIP HAS NO GRAVITY IN L8. Stayed rows 37-40 across all 5 rights; now slot 49-53 (cols 50-51 core), mid-air. Bar 12.
Boxes/ceilings built as planned (33/39/45_21, 51_15) but unused so far.
Hypothesis: click the ship to toggle polarity (no red bricks in L8). Test: ACTION6(51,38) = ship center.
Safe either way at slot 49-53: UP -> press under 51_15 (rows 19-22); DOWN -> floor 54 (rows 49-52). No caps near.

## Turn 100 (A537): ship-click = NO-OP (1 diff = bar tick). Ship inert at grid cell (51,39), slot 49-53 rows 37-40. Bar 13.
Corrections: slot 49-53 is UNDER right shelf (48-63 rows 30-36), not the shaft. Ship has NO gravity/buoyancy at all in L8.
Grid cells: centers cols 3+6k, rows 3+6k (boxes & ship align to it; ship cell = (51,39)).
Open questions: vertical mechanic? Candidates: click empty cell (place box?), box spawn onto ship cell (push/carry?), ACTION7.
Probe now: ACTION6(51,45) = empty cell directly below ship. If box appears -> click-to-place mechanic.

## Turn 101 (A538): empty-cell click = NO-OP (bar tick only, bar 14). Only box clicks act.
Batch (5): 1) ACTION6(9,9) tower-click probe (win condition / hidden mechanic?).
2-5) chain clicks (45,21),(45,27),(45,33),(45,39): walks a box down col 45; final click spawns into SHIP CELL (51,39)
-> tests push (ship shoved to (57,39)?) vs carry vs crush-death vs no-op. Death acceptable: attempt reset teaches crush rule.
Boxes before batch: 9_21,15_15,15_21,15_27,21_15,21_21,21_27,27_15,27_21,27_27,33_15,33_21,39_15,39_21,45_21,51_15.

## Turn 102 (A543): GRAND REFRAME. Ship IS up-buoyant; camera tracks ship PERFECTLY in L8 (ship always screen rows 37-40).
Scrolls: +12 at A533 (rose under 33_21), +6 at A536 (rose under 51_15-old = box now at screen (51,33)). Total C shift -18.
A539-542 clicks used STALE coords -> hit walls/empty/tower = no-ops. Tower click (45,27) = NO-OP (towers inert).
A543 click (45,39) split box: spawns up(45,33)+down(45,45); left blocked by box(39,39); RIGHT spawn onto SHIP CELL = NO-OP (ship blocks, no crush, no push).
NEW WORLD (screen A538/A543): top solid row 0; open area rows 1-5 cols 7-60; right block rows 6-12 cols 43-63 (thick, safe ceiling);
ORANGE BOX (off-grid!) cols 43-49 rows 13-17, sitting on row-18 band top, between corridor (cols 7-42 rows 13-17) and shaft (cols 50-60 rows 13-24).
Rows 6-12 cols 7-42 OPEN (path from corridor up to top area). Row 30 band opening: cols 55-59 EXACTLY slot 55-59.
Ship: slot 49-53 pressed under box (51,33). Bar 19.
PLAN: ACTION4 -> slot 55-59, rise ~24 world rows, press under right block (rows 13-16). Camera will scroll +24. THEN probe orange box click with fresh coords.
LESSON: ALWAYS recompute coords from the LATEST board; camera moves invisibly (ship pinned at rows 37-40).

## Turn 103 (A544): rise to slot 55-59 OK; camera +24. Ship rows 37-40 (pinned), grid (57,39), pressed under block rows 30-36 (c43-63).
GOAL FOUND: z-diamond center (57,2), rows 1-3 c56-58, thin O shell (L7 pass-through precedent), directly above ship, 36 rows up.
World (screen A544): row 0 solid c42-63 + open c7-17,c25-41 (world continues above!); z chamber rows 1-5 c49-59 SEALED
(left wall c43-48 rows 1-5, below block rows 6-12 c43-63); rows 13-17 open band c7-60; SANDWICH rows 18-24: solid rows 18 & 24 full width,
NINE ORANGE boxes rows 19-23 at every grid col (9..57,21); rows 25-29 open; block rows 30-36 c43-63; ship niche rows 37-41 c50-60
shared with single ORANGE box at grid (45,39); shaft below rows 42-48 c50-60; towers rows 49-53; purples rows 55-62.
Ship's ONLY exit = LEFT along rows 37-40 (right walled, down=buoyant). DO NOT spawn anything at (51,39) or ship is trapped -> RESET.
Orange boxes UNTESTED. Probe: click far one (9,21). Bar 20.

## Turn 104 (A545): ORANGE BOX RULE: click -> dissolves to harmless mine (X, pass-through) AND OPENS the solid rows above+below
its 5-wide footprint (sandwich rows 18 & 24 opened at c7-11). Orange boxes = channel plugs. Toggle-back presumed (L7 analogy).
Batch (8): click (45,39) single orange (clears ship's left exit; opens row36/42 c43-47; mine remains, pass-through),
click (21,21) (opens sandwich channel c19-23), then 6x ACTION3:
55-59 -> 49-53 -> 43-47 (through mine) -> 37-41 (RISE +12, press under row 24, rows 25-28) -> 31-35 -> 25-29 -> 19-23
(RISE +24 through sandwich channel + rows 13-17 + 6-12 + 1-5, press under row 0 c18-24, ship rows 1-4).
Camera will scroll ~36 total; next turn reveals world above row 0. Bar after: 28.
z chamber (c49-59 rows 1-5) sealed from left/below; likely entered from ABOVE row 0 world. Ship pinned screen rows 37-40 ALWAYS.

## Turn 105 (A553): batch executed perfectly. Ship slot 19-23 rows 37-40 pressed under old-row-0 band (screen row 36 c18-24,
also purple box grid (21,33) sits on it). Camera +36. Bar 29.
SCREEN NOW: sky rows 0-29 c7-60 fully open, row 0 OPEN c7-60 (world continues above).
Right block rows 30-42 c42-63 contains ORANGE PLUG grid (51,33) (rows 31-35 c49-53) directly above z-chamber.
Z-cage at c55-59 rows 36-40 (z body 37-39 c56-58); chamber interior rows 37-41 c49-55 + row 41 c49-59; left wall c42-48 rows 31-48.
ENTRY ANALYSIS: chamber unreachable by buoyant ship. WIN ROUTE (hypothesis): explore sky above for DOWN-flip mechanism;
then: click orange (51,33) (opens rows 30&36 c49-53, mine pass-through), position ship sky slot 49-53, flip DOWN,
fall through channel into chamber (land rows ~37-41 on row-42 floor), then ACTION4 into cage (thin shell pass-through) -> z overlap WIN.
Do NOT click (51,33) prematurely? Actually harmless either way; but click coords only when camera known.
Sandwich openings (old rows 18/24) now at rows 54/60 c7-11 & c19-23; mines old row 21 c9/c21.
NOW: ACTION4 -> slot 25-29 -> free rise into UNKNOWN sky above row 0. Watch for caps.

## Turn 106 (A555): ATTEMPT 2 (A554 ACTION4 -> rise at slot 25-29 through sky -> VOID above world -78 = DEATH; level fully reset).
WORLD MAP COMPLETE (world coords = initial screen rows):
void <= -79 | sky -78..-49 open c7-60 | row -48 solid c18-24(sky-box frame)+c42-63 | -47..-43: SKY BOX grid (21,-45) purple,
plug grid (51,-45) orange in block c42-63 | row -42 solid c18-24+c42-63 (openings c7-17,c25-41=DEATH EXITS) |
band -41..-37: open c7-41, wall c42-48, CHAMBER c49-54 + CAGE c55-59 (z at c56-58, world -41..-39) | row -36 solid c43-63 |
-36..-30 block c43-63 | -29..-25 open band | -24 solid full | -23..-19 NINE orange plugs (grid row -21) | -18 solid full |
-17..-13 open | -12..-6 block c43-63 | -5..-1 niche band + plug (45,-3) | 0-6 slab c0-49 + shaft c50-60 | 7-12 towers+caps
+shaft c48-60 | 13-17 open | 18-30 box zone (seed purple (15,21)) | shelf 30-36 c0-30+c48-63 gap c31-47 | 37-53 lower open |
floor 54-62.
ENDGAME THEORY: (1) rebuild gap ceilings [clicks (15,21),(21,21),(27,21),(27,15),(33,15),(39,15),(45,15) then 5R,1R = A536/A544 route];
(2) pop plugs (45,-3),(21,-21) [on-screen when camera right]; 6L to press under -42 at slot 19-23... NO WAIT better: from sandwich
press (under -24, ship top -23, camera [-60,3]): sky box (21,-45) VISIBLE at screen 15 -> relay clicks:
(21,-45),(27,-45),(33,-45),(39,-45),(39,-51),(45,-51) -> box lands (51,-51) above channel; also pop plug (51,-45);
(3) ship to sky press under (51,-51) at slot 49-53 (ship world -47..-44 inside popped plug cell);
(4) DESCENT MECHANISM (UNKNOWN!!) -> fall through -42 opening into chamber, land world -41..-38 on block top -36;
(5) ACTION4 -> cage pass-through -> z overlap -> WIN.
MISSING: down-flip. Tests this turn: cap click ACTION6(9,11); ACTION4+ACTION7 (undo semantics / maybe ACTION7=down?).
NEVER: click (21,-45) while ship pressed under it; never enter sky slots without ceiling (VOID DEATH).
Bar 0 fresh. 64 cap comfortable for full plan (~30 actions).

## Turn 107 (after A558): PROBES: cap click = NO-OP; ACTION7 = UNDO (reverted the ACTION4 move; costs bar, no refund; only returns to visited states -> useless for chamber entry).
GLYPH SEMANTICS CORRECTED (huge): '(' Light Blue = WATER (open, ship buoyant in it); 'O' Black + 'h' speckles = SOLID ROCK (starfield look).
Map verified via z/orange anchors: A553 world=screen-78; A544 world=screen-42. Turn-106 world map CONFIRMED correct.
Z REGION (world): rock c42-48 wall w-41..-37; WATER chamber c49-54 w-41..-37, extends c49-59 at w-37 (and c49-55,c59 at w-38);
z diamond c56-58 w-41..-39 embedded in 'O' cells (thin shell? L7 pass-through precedent). Death screen red block = UI cutscene, NOT a world object. NO red flip-bricks in L8.
WIN PLAN (box relay, ship never descends): park ship at SANDWICH PRESS SPOT = slot 25-29, cell (27,-15), w-17..-14, pressed under FULL-WIDTH solid w-18. Camera there: world=screen-54; whole sky+chamber visible; ship immune to all box dissolutions.
BATCH A (this turn, 20, all proven attempt-1 prefix): 7 build clicks (15,21),(21,21),(27,21),(27,15),(33,15),(39,15),(45,15); 6xR (rises +12,+6,+24; camera end world=screen-42); click (45,39)=plug(45,-3) pop; click (21,21)=plug(21,-21) pop; 5xL -> slot 25-29 sandwich press. Bar after: 23.
BATCH B (next, 8 clicks, camera world=screen-54): (51,9)=pop plug(51,-45) [opens w-48,w-42 at c49-53]; (21,9)=click sky box (21,-45) [spawns (21,-51) up, (21,-39), (15,-45); SAFE: ship not under it]; then row -51 relay: (21,3),(27,3),(33,3),(39,3),(45,3) -> box lands (51,-51); (51,3)=click (51,-51) -> DOWN-SPAWN INTO MINE CELL (51,-45) = CRITICAL TEST (also spawns (57,-51),(51,-57) harmless). Bar 31. OBSERVE.
BATCH C (if spawn-into-mine worked): (51,9)=click box(51,-45) -> spawns (51,-39) into chamber water; (51,15)=click box(51,-39) -> spawns RIGHT (57,-39) onto z = WIN TEST. Bar 33.
FALLBACKS: if mine blocks spawn -> box-win dead, need ship descent (rethink; undo can't help). If z-cell spawn no-ops -> ditto. (45,-51) reclick re-spawns (51,-51) if ship press ceiling needed later. Box (21,-39) will occupy old A553 spot band (fallback degraded, acceptable).
NEVER: click (21,-45) while ship pressed under its frame (ship IS pressed under sky-box frame at A553 spot; that's why relay runs from sandwich press instead).

## Turn 108 (after A578): BATCH A PERFECT. Ship slot 25-29 (cell (27,-15)), w-17..-14, pressed under full-width w-18. Bar 23.
Camera world=screen-54 CONFIRMED (z at screen 13-15 c56-58; plug (51,-45) orange at screen rows 7-11 c49-53; sky box (21,-45) at screen (21,9) body c19-23 rows 7-11).
Popped-plug mine renders as small orange remnant (see (45,-3) at screen rows 50-52).
BATCH B (this turn, 8 clicks, camera static since no ship moves): (51,9) pop plug; (21,9) sky box [spawns (21,-51),(15,-45),(27,-45),(21,-39)];
(21,3),(27,3),(33,3),(39,3),(45,3) row -51 relay -> (51,-51); (51,3) click (51,-51) -> DOWN-SPAWN INTO MINE CELL (51,-45) = CRITICAL TEST.
Expect after: purple 5x5 at screen c49-53 rows 7-11 if test PASSED. Bar 31.
BATCH C next if passed: (51,9) [box(51,-45) -> spawns (51,-39) chamber], (51,15) [box(51,-39) -> spawns (57,-39) onto z] = WIN TEST.

## Turn 109 (after A586): BATCH B done, bar 31. RELAY OK but CRITICAL TEST FAILED: down-spawn (51,-51)->(51,-45) NO-OP.
Reason (geometry): box needs 7x7 frame; channel/chamber only 5-6 wide with rock at frame cols -> NO BOX CAN EVER ENTER channel (51,-45), chamber (51,-39), or z cell (57,-39). BOX-WIN DEAD. Ship (5 wide) must descend channel c49-53 itself.
STATE A586 (camera world=screen-54): row -57 boxes (21..51 grid, frames -60..-54); row -51 boxes (15,21,27,33,39,45,57), (51,-51) EMPTY;
row -45 boxes (15,21,27,33,39); plug(51,-45)=mine, channel w-48/w-42 c49-53 OPEN; band box (21,-39); ship (27,-15) pressed under w-18; chamber empty.
CLICK-RECREATION RULE: clicking box re-spawns into ANY empty cardinal neighbor -> clearing a run needs hole-following (ship occupies cell to suppress left-respawn: spawn-onto-ship = no-op).
HOLE-FOLLOW PATH to hover above channel (all ceilings pre-exist -> ordering-safe):
 1. pop sandwich plug (27,-21) [scr (27,33) at current camera] -> opens w-18/w-24 c25-29 -> ship AUTO-RISES 24 to w-41..-38 under (27,-45) frame; camera +24 (world=screen-78 after).
 2. click (27,-45)=scr(27,33) -> ship rises into cell, under (27,-51) frame, w-47..-44.
 3. click (27,-51)=scr(27,27) -> ship rises, under (27,-57) frame, w-53..-50.
 4. click (33,-51)=scr(33,27) [left-spawn=ship no-op]; ACTION4 -> ship (33,-51).
 5. click (39,-51)=scr(39,27); ACTION4 -> ship (39,-51).
 6. click (45,-51)=scr(45,27) [right-spawn refills (51,-51) - fine]; ACTION4 -> ship (45,-51).
 7. click (51,-51)=scr(51,27) [left=ship no-op, down=mine no-op] -> clean hole; ACTION4 -> ship (51,-51) w-53..-50 under (51,-57), DIRECTLY ABOVE OPEN CHANNEL. Observe settle!
 NEVER click (51,-57) with ship under it (void death) unless (51,-63) pre-spawned.
THIS TURN (3 tests): ACTION6(57,14)=CLICK Z (unknown; maybe win/magnet); ACTION6(51,9)=CLICK MINE (expect re-plug toggle; re-pop later costs 1);
ACTION6(27,33)=step 1 pop+auto-rise test. Bar->34. Next: read results; if no descent mechanic revealed, run steps 2-7 (~9 actions) and observe ship above channel.
PISTON-EJECT (last resort, death-risk): re-plug mine while ship inside plug cell -> eject down? crush? Test only if all else fails.

## Turn 110 (after A589): TESTS: z click = NO-OP (inert). Mine click = RE-PLUG CONFIRMED (plug restored, w-48/w-42 re-sealed; symmetric toggle).
Sandwich pop (27,-21) = ship AUTO-ROSE +24 same-action to (27,-39) w-41..-38 under (27,-45) frame. Camera world=screen-78. Bar 34.
Ship never sinks (water below every press spot, never fell). Channel currently SEALED (plug re-plugged).
THIS TURN (11): hole-follow to hover + decisive pop:
 a1 (27,33)=click(27,-45) -> rise to (27,-45) w-47..-44 [cam ws-84]
 a2 (27,33)=click(27,-51) -> rise to (27,-51) w-53..-50 [cam ws-90]
 a3 (33,39)=click(33,-51) hole; a4 R -> (33,-51)
 a5 (39,39)=click(39,-51) hole; a6 R -> (39,-51)
 a7 (45,39)=click(45,-51) [right-spawn refills (51,-51)]; a8 R -> (45,-51)
 a9 (51,39)=click(51,-51) [down=plug solid no-op, left=ship no-op -> CLEAN hole]; a10 R -> ship (51,-51) w-53..-50 under (51,-57), ABOVE CHANNEL
 a11 (51,45)=POP PLUG (51,-45) -> opens w-48 (right below ship) + w-42. OBSERVE SINK OR NOT. Bar->45.
If ship sinks -> chamber -> next turn ACTION4 = WIN. If not: ship stable & escapable (undo or click (45,-51) box then L).
Remaining ideas if no sink: multi-undo semantics; RESET+rethink. NEVER dissolve (57,-51) or (51,-57) with ship exposed (void).
All safety pre-checks done: every up-path capped by -57 boxes; all spawns no-op or intended.

## Turn 111 (after A600): BREAKTHROUGH - full mechanic decode from L7 A524 win frames.
L7 WIN = ACTION6(3,39) clicked a RED BRICK (n) -> ship SANK 12 rows through TWO 1-thick O layers onto z = GRAVITY FLIP (bounce-up after was win cutscene, not buoyancy).
A554 settled board = TOP OF L8 WORLD, world = A554row - 150. RED BRICK EXISTS at w-143..-139 cols 31-35 (NOT death UI - my "no red bricks" scan conclusion was WRONG).
World top: brick in rock w-150..-120; funnel towers w-119..-115 (c26-28/32-34/38-40, caps DOWN at w-115); w-114 rock line (gaps c30,c37 1-wide);
funnel water w-113..-108 c25-42; towers w-107..-103 (c20-22/44-46); w-102 water c24-42; towers w-101..-97 (c14-16/50-52); w-96 water c18-48;
towers w-95..-91 (c8-10/56-58); w-90 water c12-54; lake w-89..-61 c7-60.
KILL GAUNTLET: EVERY lane's free-rise ceiling = 1-thick rock with G$G cap behind = DEATH (attempt-1 A554 death: lane 25-29 pressed w-114, cap w-115). Box-ladder pressing is the ONLY safe rise.
A600 state: ship (51,-51); (33..51,-51) row boxes CONSUMED by hole-follow (empty); channel OPEN (mine w-46..-44); (39,-45),(33,-57),(39,-57),(45,-57),(51,-57) boxes exist.
PLAN (17, bar 45->62): 1 (51,33) rise into (51,-57) [spawns (51,-63),(57,-57)]; 2 (45,39) dissolve (45,-57) [spawns (45,-63),(45,-51)=support]; 3 L;
4 (39,39) dissolve (39,-57) [spawns (39,-63),(39,-51)=landing]; 5 L; 6-13 (39,33)x8 ladder to (39,-105) — NEVER a 9th rung ((39,-111) click = w-113 press = cap death);
14 (33,3) = RED BRICK (camera ws-144, brick screen rows 1-5) -> flip, ship sinks lane 37-41 to rest on (39,-51) frame ~w-58..-55;
15 R (onto (45,-51) support); 16 R (slot 49-53 = hole -> falls thru channel+mine to chamber floor w-40..-37); 17 R (thru 1-thick cage wall col55 onto z c56-58 w-41..-39) = WIN?
RISKS: flip may be dive-12 (then bounce back safe, RESET next turn); flip may expire on landing (ship re-rises to (39,-111) frame, safe); lateral 1-thick wall pass unproven.

## Turn 112 (after A617): LEVEL 8 SOLVED (score 8) — 17-step flip plan worked EXACTLY. Total confirmed mechanics:
- Red brick click = PERSISTENT gravity flip (lasted A614-A617 across 4 actions).
- Thin 1-thick O walls pass-through LATERALLY too (A617: ship slid through cage wall onto z).
- L9 START (A617 final board, bar 0/64, camera baseline "cam0", world=screen at start):
  Ship rows 37-40 c19-23 alcove (1-thick shelf below at c20-22, r41). Rock band r30-36 with water GAP c31-47.
  Upper water r0-29 c13-60 (continues above screen); box at (39,15) body r13-17 c37-41.
  RED BRICKS c1-5 at r25-29 and r37-41 (left strip c0-5 alternates water pockets r0-23/31-35/43-62 and bricks, sealed by 1-thick rock rows 24/30/36/42).
  Mid water r37-53 c13-60; floor r54 (rock r54-60 c6-63); BOTTOM-LEFT PASSAGE r61-62 c0-23 (leads below?). Right wall c61-63. No z visible — z off-screen (up or down-left).
PLAN turn 112 (3): click (39,15) [spawns (33,15),(45,15),(39,9),(39,21)]; R; R -> ship rises thru gap at slot 31-35, presses SAFELY under (33,15) frame at r19-22. Camera reveals ~18 rows above. Observe.

## Turn 113 (after A620): scout OK. Ship (33,19)cam0 pressed under box (33,15)cam0. Camera world=screen-18 (rel cam0). Bar 3/64.
TOP OF WORLD revealed: w-18 full rock line; GREEN 5x5 BLOCKS (I) at w-17..-13, cols 14-18/20-24/26-30 (NEW MECHANIC, untested);
tower gauntlet w-11..-6 c31-59 (caps DOWN at w-7, 1-wide gaps c36/42/48/54); water pocket w-11..-6 c13-30; upper water w-5..+11 c13-60.
Boxes now: (33,15),(45,15),(39,9),(39,21) cam0. Still no z. Unexplored: bottom-left passage (cam0 r61-62 c0-23), region right of towers, below floor.
Green-click safety check: ship at (33,19) — any gravity direction outcome = safe press (right wall c61-63 plain, left wall c7-12 plain, down w30 rock band, up already pressed). No caps in any line.
PLAN turn 113 (1): ACTION6(22,3) = click middle green block. Observe effect.

## Turn 114 (after A621): GREEN = DESTRUCTIBLE BLOCK. Click -> dissolves to water (no spawn/gravity effect). Middle ceiling block (19-23 x r1-5 screen / w-17..-13) now open pocket.
Green blocks: bodies c14-16/20-22(CLEARED)/26-28, borders 13,17/19,23/25,29. Ceiling row 0 (w-18) intact; row 6 (w-12) 1-thick under greens.
THIN-LAYER RULE (reconciled): moving ship passes 1-thick O only if open space beyond (L7 shelf, L8 cage wall); blocked if solid behind (L8 frame rest, tower kill-press).
DANGER reminder: do NOT click box (33,15) while ship under it — ship would rise into cell (33,15) pressing row 12 (1-thick, G$G cap behind at r11 c32-34) = DEATH.
PLAN turn 114 (1): ACTION3 -> ship slot 25-29 free-rises ~30 to press under row 6 (w-12; green behind, not cap — safe). Camera +30 reveals w-48..-18 above ceiling. Then decide entry via cleared pocket lane 19-23.

## Turn 115 (after A622): CAMERA FIX — nothing drifted; world static. World coords = A617 rows. Ship world -11..-8 lane 25-29, pressed under w-12 thin rock (green 26-28 behind = safe). Camera: screen=world+48. Bar 5.
Turn-114 note errata: greens are at WORLD -17..-13 (not cam0 1-5). Middle green (20-22) cleared at A621; its seals w-18/w-12 at c19-23 OPEN -> full vertical channel c19-23.
UPPER FLOOR (w-48..-19): left water col c13-29 (w-41..-19), band w-24 rock c30-48 (water c13-29!), UP-CAP towers w-23..-19 at c38-40/44-46/50-52/56-58 (kill SINKING ships), w-18 rock line c24-63 (open c19-23). Wide water c13-47 at w-47..-43. Lane c55-59 separate. Above w-48: UNKNOWN. Red bricks (static, upper strip): (3,-45),(3,-21) + originals (3,27),(3,39). z still unseen.
Boxes intact: (33,15),(45,15),(39,9),(39,21).
PLAN turn 115 (13, bar->18): chain box up middle channel then ladder:
 1-7: clicks (33,62),(27,62),(21,62),(21,57),(21,51),(21,45),(21,39) = walk box (33,15)->(27,15)->(21,15)->(21,9)->(21,3)->(21,-3)->(21,-9)->ends box at (21,-15), cell (21,-9) empty.
 8: ACTION3 -> ship into cell (27,-9)->(21,-9) wait: ship slides left into lane 19-23 at w-11..-8 pressed under (21,-15) frame.
 9-13: rides ACTION6(21,33) x5 -> ship (21,-15)->(21,-21)->(21,-27)->(21,-33)->(21,-39) w-41..-38 pressed under (21,-45) frame. STOP (next up-spawn (21,-51) unverified).
 All spawn cells verified water. Side spawns harmless (audited). Camera ends screen=world+78 revealing w-78..-48.

## Turn 116 (after A635, bar 18/64)
- 13-action plan EXECUTED perfectly. Ship at (21,-39) w-41..-38, c20-22, pressed under w-42 line (box (21,-45) behind = safe). Camera screen=world+78.
- BAR DECODED: bar counts UP from 0 at level start (A617=L9 action 1, bar 0). Now 18/64 used, 46 left. L8 took 61.
- z SEARCH: NO z anywhere in w-78..+62 (full world height scanned; A615/616 z was L8's goal). z must be ABOVE w-78 ceiling or BELOW w+62 floor.
- WORLD MAP (w=A617row; screen=world+camera, A635 camera=+78):
  - w-78: full-width solid ceiling (r0 of A635)
  - w-77..-73: top room, water c13-59 (left col c0-5 separate)
  - w-72..-66: structure A: cap towers lanes 15-51 (caps G$G at w-71 UNDER w-72 line, 4-tall purple bodies w-70..-67, solid w-66 below). RIGHT GAP: c54-59 water
  - w-65..-61: solid band c6-54; right col c55-59 water
  - w-60..-54: structure B: purple towers lanes 15-45, caps at w-55 BELOW bodies; w-54 line gaps 1-wide c18,24,30,36,42; right col open
  - POCKET w-53..-49 (c13-47): LETHAL for free-rise (caps at w-55 behind w-54 thin at every lane). Never ride into row -51 cells except... none safe.
  - w-48 line: gaps c13-17, c25-47; w-47..-43 corridor c25-47 water + right col
  - w-42 line c0-36; SHAFT c37-47 water w-42..-25; right col c55-59 w-47..-25
  - w-41..-19: middle lane c19-23 + box stacks lanes 15,27 (cells -39,-33,-27,-21) + rock c30-36; right region c37-59 water w-35..-25
  - w-24 floor: caps BELOW at lanes 39,45,51,57 (c38-40,44-46,50-52,56-58); gaps c19-23,c42,c48,c54. Safe landing cols: c41-43,c47-49,c53-55 (behind=O,(,O)
  - w-18 line (gap c19-23 only); greens (15,-15),(27,-15), lane21 cleared; w54-60 solid floor c6-63; w61-62 pocket c0-23 (sealed, hints world below w63)
  - Left col c0-5 water w-77..w62+, red brick plugs lane 3 at (3,-57),(3,-45),(3,-21),(3,27),(3,39); west wall c6-12 unbroken except w61-62
- RIGHT COLUMN c55-59: clean water w-72..-25, no caps. THE ascent route to top room. Entry only from w-35..-25 region (via shaft descent flipped-gravity, landing risk) — or unneeded if z is below.
- PASS RULE (refined): moving/falling ship passes 1-thick O iff ALL cells beyond are open; presses/stops if occupied behind; dies if cap behind pressed cell.
- THIS TURN: 1 action probe ACTION6(21,33) = ladder ride to (21,-45). Safe (up-spawn (21,-51) water; press under w-48 w/ box frame behind). Camera -> +84, reveals w-84..-79 = BEHIND THE CEILING. Look for caps/water/z above w-78. Also observe whether side spawns (15,-45),(27,-45) occur (informs future chains).
- NEXT: if water/z above ceiling -> plan right-column ascent (shaft descent at safe cols c41-43/47-49/53-55 flipped, walk to c55-59 floor at w-24, re-flip, rise). If solid thick -> consider bottom route (flip, fall middle lane to w30 roof, ... floor w54 dead end though) or rethink.

## Turn 117 (after A636, bar 19/64, camera=+84, ship (21,-45) w-47..-44)
- Probe SUCCESS. Above ceiling w-78: PLUG ROW at w-83..-79, all 8 lanes 15..57 (h---h/----- cells), sandwiched by solid w-84 and w-78. Red brick (3,-81) in left col. Plugs = seal-doors like greens: click opens seal rows above/below footprint.
- Side spawns CONFIRMED: ride spawned (15,-45),(27,-45),(21,-51 pocket canopy).
- Rides PUNCH HOLES in lines crossed: w-42 c19-23 now open. Also: many "lines" = object SHELLS (occupied cells render O border; empty cells render water). Terrain vs shell distinction!
- MASTER ROUTE (est ~25 actions, fits in 64 budget):
  P0 click plug 57 NOW (only visible at high camera) -> converts (57,-81) to spawnable rung slot. Later ladder: ride spawns box INTO cleared plug cell; ship pressed under it = safe; final rides pass ceiling safely w/ canopy always above.
  P1 canopy-walk right at row -45: dissolve (27,-45) [spawns canopy (27,-51)+stopper (33,-45)]; ACTION4 -> ship into (27,-45) pressed under canopy/shell. Repeat: click (33,39),(ACTION4),(39,39),ACTION4 -> ship (39,-45); each dissolve spawns canopy at row -51 + stopper + DOWN rung (39,-39) when dissolving (39,-45).
  P2 flip gravity (brick (3,3) at cam+84) -> ship sinks onto (39,-39) box top.
  P3 ride DOWN: click (39,-39)[(39,45)], click (39,-33)[(39,51)] -> ship rests atop (39,-27) pad at w-33..-30. NEVER ride (39,-27): floor caps at c38-40 = death.
  P4 pad-walk right at w-29 tops: ACTION4 (stop at (45,-33) box); click (45,51) dissolve [spawns pad (45,-27)]; ACTION4; click (51,51) [pad (51,-27)]; ACTION4; click (57,51) [pad (57,-27) + LADDER SEED (57,-39)]; ACTION4 -> ship atop (57,-27), c57ish.
  P5 re-flip (brick (3,-57) on screen ~r13) -> ship rises pressed under (57,-39). Check alignment (body c56-58 vs c57-59; may need nudge).
  P6 ladder UP lane 57: rides at (57,-39),(-45),(-51),(-57),(-63),(-69),(-75) = 7 clicks; screen click row stays 31ish as camera follows (+6/ride). At (57,-75) top room: camera=+114 REVEALS w-114..-51 -> verify whats above w-84 BEFORE final ride into plug cell (57,-81).
- DANGER LIST: never click canopy directly over ship in pocket rows (-51): ride=death via w-54 caps at lanes 15-45. Never ride into row -27 at lanes 39,45,51 (floor caps). Pocket free-rise=death. w-24 floor: caps below at lanes 39,45,51,57.
- THIS TURN: ACTION6(57,3) [plug test], ACTION6(27,39) [dissolve (27,-45)], ACTION4 [hop]. Verify next: plug 57 cleared (seals open c56-58 at w-78/-84?), ship position/press state, spawns (27,-51),(33,-45).

## Turn 118 (after A639, bar 22/64, camera +84)
- A637 plug click WORKED: seals w-84 & w-78 opened FULL 5-wide c55-59. Leftover '-' debris X-pattern in cell (56/58 at w-82,-80; 57 at w-81) — unknown if solid. Re-clicking (57,3) this turn to test. (Recoverable later: at camera +114 plugs visible at screen rows 31-35.)
- A638 dissolve + A639 hop CONFIRMED: ship now (27,-45) body c26-28, pressed under canopy (27,-51). Boxes: (15,-45),(33,-45),(21,-51),(27,-51); stacks intact.
- THIS TURN (7): ACTION6(57,3) debris test; (33,39) dissolve->canopy (33,-51)+spawn (39,-45); ACTION4 hop to (33,-45); (39,39) dissolve->canopy (39,-51)+RUNG (39,-39)+stopper (45,-45); ACTION4 hop to (39,-45); (3,3) FLIP (ship sinks ~2 rows onto rung (39,-39) top; camera may shift to +86); (39,46) first DOWN-RIDE test (click lands on box rows 45-47 either camera). Expect ship into (39,-39), spawns (39,-33) rung below + (45,-39) + (39,-45) refill.
- Next turn: verify flip/sink/down-ride semantics, ship pos; then ride (39,-33), STOP (never ride (39,-27): floor caps). Then pad-walk right per master plan (turn-117 notes).

## Turn 119 (after A646, bar 29/64)
- FLIPPED camera pin = ship screen rows 27-30 (proven L8 A614 + L9 A645). Camera now +74.
- A645 flip WORKED (camera re-pinned +84->+74). A646 (39,46) was a NO-OP water click (computed for stale camera).
- PLUG TOGGLE: A640 re-click of plug 57 RE-SEALED it. Must re-click at ladder top: camera +114 puts plug rows -84..-80 at screen 30-34 -> click (57,32).
- Verified settled A646: ship (39,-45) rows 27-31 c38-41; rung (39,-39) rows 33-37; box (45,-45) present; (39,-33),(45,-39),(39,-27) empty water.
- This turn: ACTION6(39,35) x2 = two down-rides lane 39 (target identical for both under either ride semantics, camera re-pins -6 per ride), then ACTION4 first pad-walk step (blocked safe by (45,-33)/(45,-39) box).
- NEXT: pad-walk right dissolving (45,-33),(51,-33),(57,-33) ~ clicks (45,29),(51,29),(57,29) at camera +62, ACTION4 between; NEVER ride into row -27 (floor caps at lanes 39/45/51/57); land only c41-43/47-49/53-55 on w-24 floor; then re-flip brick (3,-57) and ladder up lane 57.

## Turn 120 (after A649, bar 32/64)
- A647-649 PERFECT: two down-rides (camera 74->68->62), ship at (39,-33) screen rows 27-30 resting on spawned rung (39,-27); ACTION4 blocked by box (45,-33) as planned.
- Flipped gravity = ship SINKS, rests on box below, screen pin rows 27-30 confirmed stable.
- Verified at camera 62: (45,-33) box present rows 27-31 c43-47; (51,-33),(57,-33),(45,-27),(51,-27) all empty water; re-flip brick at screen (1-5,3-7) -> click (3,5).
- This turn: pad-walk steps 1-2: click (45,29) dissolve -> spawns (45,-27) support + (51,-33) stopper; ACTION4 into (45,-33); click (51,29); ACTION4 into (51,-33). Camera should stay 62 (same world row).
- NEXT turn: click (57,29), ACTION4 into (57,-33); click (3,5) re-flip (gravity normal, ship floats up pressed under (57,-39) box); then ladder rides up lane 57: click box above ship each time (~(57,33) style targets, camera re-pins +6/ride). ~8 rides to plug row -84; re-click plug 57 (~(57,32) at camera +114); final ride through plug. Budget ~50/64 total.

## Turn 121 (after A653, bar 36/64)
- A650-653 PERFECT: pad-walk steps 1-2 done. Ship in (51,-33) body c50-52 rows 27-30; supports (45,-27),(51,-27) spawned; stopper (57,-33) present; camera held 62.
- Verified: (57,-39) and (57,-27) empty -> dissolving (57,-33) spawns first ladder rung above AND support below.
- This turn: ACTION6(57,29) dissolve stopper; ACTION4 into (57,-33); ACTION6(3,5) RE-FLIP (gravity normal, ship presses up under rung (57,-39), camera re-pins to 72 = ship top w-35 at screen 37); then 2 ladder rides ACTION6(57,33) x2 (rung interior at screen rows 31-35 each time, camera +6/ride).
- Ladder ride targets stay (57,33) every ride (camera re-pin keeps rung above at rows 31-35).
- NEXT: verify camera 72 assumption; continue rides -51,-57,-63,-69,-75,-81 (lane 57 clean, no caps; pocket caps were lanes 15-45 only). At top (~camera +114) re-click plug 57 ~(57,32/33) to re-open, final ride through plug row -84..-80. Budget ~49/64.

## Turn 122 (after A658, bar 41/64)
- A654-658 PERFECT: pad-walk done, re-flip worked (camera 62->72), 2 ladder rides (camera 78, 84). Ship (57,-45) rows 37-40 body c56-58; rung (57,-51) present rows 31-35; water above to -64.
- Plug geometry confirmed (A639/640 boards): plug cell (57,-81), interior w-83..-79; WATER above at w-84 row 0. A639 showed open-state pattern; A640 re-seal solid.
- This turn: 5 rides ACTION6(57,33) x5 -> ship (57,-75), camera 114 (reveals w-114..-84 region!). Rung chain spawns up each ride; (57,-69) in structure-A right gap, (57,-75) in top room, both open. Riding into (57,-75): up-spawn blocked by sealed plug (fine), ship rests pressed under plug.
- NEXT turn: inspect revealed top region for z/goal; plug at screen rows 31-35 -> click (57,33) toggles OPEN; ship should free-rise through into region above. Bar will be 46/64; ~18 left for finish.

## Turn 123 (after A663, bar 46/64)
- A659-663 PERFECT: 5 rides done, ship (57,-75) pressed under sealed plug 57, camera 114. Side-spawn box at (51,-75).
- TOP REGION REVEALED (w-114..-85): open water c13-59; wall columns c6-12 and c61-63; c0-5 water. ONLY feature: GREEN block at cell (27,-93) (screen rows 19-23, c25-29). NO z visible -> goal above w-114 or behind/via green.
- All 8 plugs sealed at row -81 (screen 31-35), solid O seal rows at screen 30 and 36.
- This turn: single test ACTION6(57,33) -> toggle plug 57 OPEN. Watch: does ship free-rise through? How far? Any caps above -114? Plug open-state passability?
- If ship free-rises: camera reveals higher region; then navigate toward green (27,-93)/goal. Bar 47 after; 17 left. Lean batches from here.

## Turn 124 (after A665 RESET -> ATTEMPT 2, bar 0/64)
- A664 DEATH ANALYSIS: opening plug 57 while pressed directly under it -> ship free-rose through open plug (passable, debris X does NOT block ship), camera did NOT follow, ship died above w-114 (frames 8-18 rise offscreen; 28-47 respawn fall). Runner auto-RESET (A665). NEVER open a plug with ship pressed under it unless a safe stop exists above.
- KEY INSIGHT: GREEN at (27,-93) is SOLID until clicked -> safely catches free-rise in LANE 27. Lane 57 has nothing above -> death.
- ATTEMPT 2 MASTER PLAN (~55 actions):
  P1 (THIS TURN, 19): replay A618-636 verbatim (A617 A4 was no-op; reset board == A617-settled, verified full-board diff empty). -> ship (21,-45), camera +84.
  P2 (6): canopy-walk right NO plug click: (27,39),A4,(33,39),A4,(39,39),A4 -> ship (39,-45).
  P3 (1): flip (3,3) [brick (3,-81) at cam 84].
  P4 (9): (39,35)x2, A4, (45,29), A4, (51,29), A4, (57,29), A4.
  P5 (1): re-flip (3,5) [brick (3,-57) at cam 62].
  P6 (7): (57,33)x7 ladder up -> ship (57,-75) pressed under SEALED plug 57 (safe, proven).
  P7 (10): canopy-walk LEFT under sealed plug row at cam 114: [(51,39),A3],[(45,39),A3],[(39,39),A3],[(33,39),A3],[(27,39),A3] -> ship (27,-75). Box (51,-75) exists from ride-7 side spawn. Pressing under w-78 seal with plug body behind = safe (not G$G).
  P8 (1): click (27,33) = open plug 27 -> ship free-rises through (27,-81),(27,-87), PRESSES UNDER GREEN (27,-93) = safe stop. Camera re-pins 132.
  P9 endgame (~9 spare): observe revealed w-132+ region; click green (toggle) -> expect z inside (rise-dock win) or further route.
- DO NOT click plug 57 at all this attempt. DO NOT re-click plugs (toggle!).

## Turn 125 (after A684, bar 19/64, Attempt 2)
- P1 replay PERFECT: A666-684 reproduced attempt-1 state byte-identically (full diff A636 vs A684 = empty). Ship (21,-45), camera 84.
- This turn: 20-action batch = P2 canopy-right [(27,39),A4,(33,39),A4,(39,39),A4] + P3 flip (3,3) + P4 down/pad [(39,35)x2,A4,(45,29),A4,(51,29),A4,(57,29),A4] + P5 re-flip (3,5) + first 3 rides (57,33)x3. All byte-identical proven coords (A637/A640 removals don't affect these regions; plug 57 sealed both attempts during rides).
- After: bar 39, ship (57,-51), camera 90. NEXT: 4 rides (57,33)x4 -> (57,-75) under sealed plug; then P7 walk-left x5 [(51,39),A3,(45,39),A3,(39,39),A3,(33,39),A3,(27,39),A3]; P8 click (27,33) plug 27 -> free-rise to under GREEN (27,-93). NO plug-57 clicks!

## Turn 126 (after A704, bar 39/64, Attempt 2)
- 20-batch PERFECT: byte-identical to attempt-1 A659. Ship (57,-51), camera 90, 3 rides done.
- ACTION3 semantics VERIFIED (A621->A622): turn+move in ONE action (ship moved 6 cols left and flipped orientation). No turn-only tax.
- This turn 15 actions: rides (57,33)x4 -> (57,-75) under sealed plug (replay A660-663, spawns (51,-75)); walk-left [(51,39),A3]x5 lanes 51,45,39,33,27 at camera 114 (row -75 boxes at screen rows 37-41, stoppers spawn ahead, sealed plugs above = safe ceiling); then (27,33) OPEN PLUG 27 -> ship free-rises (27,-81),(27,-87) -> PRESSES UNDER GREEN (27,-93). Camera re-pins 132.
- Remote plug click harmless even if walk stalls (only free-rises if ship directly under).
- After: bar 54/64, 10 left for endgame. NEXT: observe w-132..-114 reveal + green; click green (27,~37 at cam 132? green cell (27,-93) interior w-95..-91 -> screen 37-41 -> click (27,39)) -> expect z reveal/dock.

## Turn 127 (after A719, bar 54/64, Attempt 2)
- 15-batch PERFECT: rides + walk-left + plug 27 open all worked. Ship free-rose and PRESSED UNDER GREEN (27,-93): ship in (27,-87) rows 37-40 body c26-28 (Gff facing left), camera 126.
- NEW REVEALS (w-126..-88): open water c13-59; BOX at (45,-123) screen rows 1-5 c43-47; GREEN #2 embedded in LEFT WALL c8-12 at w-125..-121 (door to left column c0-5?). NO z yet -> higher still.
- A623-625 were bottom box-ladder clicks (dissolve+spawn up), NOT greens. Green click semantics UNKNOWN.
- This turn (4): canopy chain along row -123 via remote clicks: (45,3) spawns (39,-123)+(51,-123)+(45,-117); (39,3) spawns (33,-123)+refills; (33,3) spawns (27,-123) CANOPY. Then (27,33) click GREEN: if opens -> ship free-rises -93..-117, pressed under canopy (27,-123) SAFE (camera 156, reveals w-156+); if not -> ship stays pressed, no harm.
- After: bar 58/64, 6 left. If z near top: rides. If budget runs out -> attempt 3 replay needs trimming (route is 54 + endgame; consider skipping canopy chain if green learned passable, or shorter canopy row -117).

## Turn 128 (after A723, bar 58/64, Attempt 2)
- CANOPY CATCH WORKED: A720-722 built row -123 canopies; A723 green #1 click opened it (greens = passable when clicked, like plugs); ship free-rose (27,-87)->(27,-117), pressed under canopy box (27,-123). Camera 156.
- TOP OF WORLD REVEALED (w-156..-133): solid mass w-156..-138; hanging cap towers w-137..-134 with G$G caps POINTING DOWN at w-133 at EVERY lane 15..57; 1-thick line w-132 with caps directly behind = KILL CEILING everywhere. 1-wide slots c18,c24,c54 (too narrow for ship). NO z ANYWHERE in w-156..+62!
- Board: canopy row -123: boxes (27),(39),(45),(51); (33,-123) empty. Row -129: boxes (33),(39),(45). Row -117: ship(27) + boxes (33),(39),(45). GREEN #2 door at (9,-123) in left wall c6-12; left col c0-5 water up to w-131, THICK solid cap above (safe press but dead end).
- STUCK ANALYSIS: cannot rise (kill ceiling), cannot dissolve (27,-123) (free-rise death), cannot build canopies left (no clickable neighbor), cannot flip (no brick on screen). Right = dead end. Only lead: GREEN #2 may be a PRIZE container (orb/z, cf L5 prize boxes).
- This turn: 1 action ACTION6(9,33) = open green #2 remotely. Observe contents/door.
- If bar hits 64 -> auto reset attempt 3. Route to current state = 58 actions; MUST TRIM for attempt 3 (ideas: plug 33 instead of 27 saves 2 walk steps; skip A619/A620 if no-ops? verify; canopy chain maybe 2 clicks if green passable known - no, canopy still needed).
- LAST RESORT lead: 'w61-62 pocket c0-23 sealed, hints world below w63' -> goal may be BOTTOM world via left column descent + gravity flips.

## Turn 129 (after A724, bar 59/64) -> RESET to ATTEMPT 3, NEW BOTTOM ROUTE
- A724: green #2 opened wall c6-12 at row -123 fully (empty door, no z). Top world = DEAD END (kill ceiling every lane).
- L8 WIN RECAP: z = 5-cell diamond marker; ship rode/moved INTO z = dock, score +1 (A617 final A4).
- BOTTOM WORLD FOUND (re-read initial board): 'floor w54-60' = ROW OF BOXES cell-row 57 lanes 15-57; second box row w61-65 lanes 27-57; LANES 15/21 OPEN at row 63 = water pocket c13-23 -> bottom world below w63 (never seen). Left col c0-5 water runs all the way down too. z MUST be down there.
- ATTEMPT 3 ROUTE: RESET; click (3,39) FLIP (brick beside ship, rows 37-41); ship sinks (21,39)->(21,45)->(21,51) rests on floor-box (21,57); flipped camera pin ship rows 27-30, box below at rows 33-37 -> down-rides click (21,35) each; ride1 into (21,57) spawns (21,63) into pocket; ride2 into (21,63) spawns (21,69)...; continue until z visible. Preview 5 cells ahead each stop; STOP before any upward G$G caps.
- This turn: RESET + flip + 2 down-rides. After: ship (21,63), camera ~-34, reveals to w~97.

## Turn 130 (after A728, 3rd try, bar 3/64, gravity FLIPPED, ship (21,51), camera -22)
KEY FACTS LOCKED IN:
- Z CONFIRMED at world rows 67-69, cols 14-16 = cell (15,69), in bottom pocket w61-71 c0-23.
- Red brick click => gravity flip AND brick DISSOLVES (A726). (3,39) now gone. Remaining: (3,27),(3,-21),(3,-45),(3,-57),(3,-81).
- Floor w54-60 is TERRAIN tiles (O/h interiors, clicks no-op A727/728), not boxes.

WINNING ROUTE (fully verified against A684 board):
E1 (THIS TURN action 1): click (3,5) = brick (3,27): dissolves + flips to NORMAL; ship rises to (21,39) = attempt-1 start state.
Then verbatim A618-636 replay (19 actions, proven deterministic twice, no clicks touch c0-12):
  (39,15),A4,A4,(22,3),A3,(33,62),(27,62),(21,62),(21,57),(21,51),(21,45),(21,39),A3,(21,33)x6
=> ship (21,-45), camera 84. E1+replay = exactly 20 = this turn's batch.

NEXT TURN ENDGAME (12 actions):
1. ACTION6(15,39)  - dissolve box (15,-45); spawns canopy (15,-51)
2. ACTION3         - ship -> (15,-45), rises through w-48 gap c13-17, pressed under canopy
3. ACTION6(3,3)    - brick (3,-81): dissolve + FLIP; ship falls onto stack top (15,-39)
4-7. ACTION6(15,35) x4 - down-ride stack -39,-33,-27,-21
8. ACTION6(15,35)  - opens green (15,-15) below ship -> falls through open lane 15
                     (w-12 and w24 lines are c0-12 only) -> lands thick band w30 at (15,27)
9. ACTION3 -> (9,27); 10. ACTION3 -> (3,27) no support -> falls: passes 1-thick w30/w36
    lines c0-5, through dissolved (3,39) hole, lands (3,69) on w72 floor
11. ACTION4 -> (9,69); 12. ACTION4 -> (15,69) = Z DOCK, score 8->9.
Total bar ~35/64. Verify next turn: board diff vs A684 should show only lane-3 bricks (3,27),(3,39) missing.

## Turn 131 (after A748, bar 23/64)
Batch executed perfectly: A729 brick(3,27) flip+dissolve, A730-748 replay. Settled A748 board
byte-identical to A684 (lane-3 bricks off-screen at camera 84). Ship (21,-45), camera 84.
Wrote the 12-action endgame (see Turn 130 notes) -> expect Z DOCK, score 8->9, bar ~35.

## Turn 132 (after A749-760, bar 35/64, attempt 3) — PARITY CONTRADICTION + setter test
**Endgame failure autopsy (A749-760)**: 12-action route died on two map errors:
1. w−12 line spans ALL cols except lane-21 gap (not just c0-12) — ship stopped in green cell (15,−15), then side-spawned box (15,−9) trapped it.
2. Wall c6-12 solid w−17..w24 — lane 9 NOT open at w27 (A757/758 ACTION3 blocked).
Ship now: (27,−9) FLIPPED resting on box (27,−3), cam 38. Bricks left: B21, B45, B57.

**THE PARITY CONTRADICTION (toggle model)**: all 6 bricks lie in lane 3 = the ONLY descent path
(column c0-5 → door (9,−123) → pocket → z). Final descent needs FLIPPED (sink) with all 6 gone.
6 toggles from initial NORMAL = NORMAL. Contradiction. Eliminated escapes:
- Undo = FULL state restore (verified 0-diff at A138/140, A197/199, A249/251-253) — no parity break.
- No 7th flip source: exactly 6 'n' objects ever, all lane 3.
- In-column box catcher: catch-22 (pre-built blocks descent; ship-in-column can't reach door area to build).
- Sparing a brick: impossible, all 6 obstruct the path.
- No alternate pocket/column entry (full topology verified from A724/A726/A748/A755 dumps).

**HYPOTHESIS: bricks are gravity SETTERS not togglers.** All 4 observed clicks (B39 N→F, B27 F→N,
B81 N→F, B57 F→N) fit BOTH models. If setter (e.g. odd-world-row bricks set F, others set N — or
per-brick fixed direction), parity dissolves and level is solvable.

**TEST (this turn, 2 actions)**: ACTION6(3,17) = B21 (verified 'nnnnn' at screen rows 15-19 cols 1-5,
w−24 line row 14, w−18 line row 20). Currently FLIPPED.
- Toggle model → NORMAL: ship rises, presses under sealed green (27,−15) [1-thick w−12 + solid green
  behind = safe stop], cam re-pins to ~48, then ACTION6(3,3) hits B45 (screen rows 1-5) → FLIPPED.
- Setter-F model → gravity STAYS FLIPPED, no camera re-pin (distinguishable!), (3,3) = water no-op.
Both outcomes safe; B21/B45 dissolves needed anyway. Attempt 3 is a write-off regardless (B57 needs
high camera, unreachable while FLIPPED down here).

**Next turn**: if setter confirmed → redesign route with flip-free dissolves. If toggle confirmed →
RESET, click (3,39)=B39 → F, sink to (21,51) cam −22, click z at screen (15,46) to probe z mechanic.

## Turn 133 (A761-762 results) — TOGGLE MODEL CONFIRMED
A761 click (3,17)=B21 while F: ship re-pinned top 27→37 = NORMAL. A762 click (3,3)=B45: pin 37→27 = FLIPPED.
Every brick click = dissolve + toggle. Setter hypothesis DEAD. Parity contradiction is real under known mechanics.

Also confirmed from A725/A726: attempt spawn = ship top w37, cam 0, NORMAL; B39 clickable at (3,39) on spawn
board; after B39 click ship sinks to (21,51), cam −22, z visible at screen rows 45-47 (center (15,46)),
B27 at screen rows 3-7.

**This turn (bar was 37, write-off attempt)**: RESET → ACTION6(3,39) → ACTION6(15,46) = click the z goal
itself. Probing for unknown mechanic (teleport? goal activation?). Bar after: 3.

**Remaining exotic hypotheses if z-click is a no-op**:
- Click the ship itself.
- Click yellow G$G caps / kill ceiling.
- Enter column at w−123 while FLIPPED by resting on a box parked at (15,−117), keeping ODD bricks
  (e.g. keep 1, dissolve 5 → F at entry). Problem: ship then lands on kept brick in column; clicking it
  → N → floats to column top → stuck (no flip sources visible at cam 166). Still a contradiction unless
  some new mechanic intervenes.
- Box-walking into the column: clicking a box spawns copies into ALL empty cardinal neighbors; could fill
  column cells. No descent mechanism under N though (up-rides only).

## Turn 134 (A763-765) — z-click is a NO-OP
RESET, B39 click (→F, ship sank to (21,51), cam −22, bar 1), then ACTION6(15,46) on the z:
board diff vs A764 = ONE cell (bar tick). z-click hypothesis DEAD.

Current state: attempt 4(ish), bar 2, FLIPPED, ship (21,51) on pocket ceiling, B39 dissolved,
B21/B27/B45/B57/B81 remain. z at screen (14-16, 45-47). Ship pixels: screen row27 col21 f;
rows28-29 cols20-21 ff col22 G; row30 col21 f.

**This turn**: probe ship self-click: ACTION6(21,28) (blue body), ACTION6(22,28) (yellow tail).
Looking for any 7th-toggle / unknown mechanic. Attempt is throwaway; safe to experiment.

**If no-op, remaining exotic candidates**:
- Click G$G lane caps (visible only at cam ≥ ~24+... caps at w−24 above box lanes; also kill ceiling w−133/−132).
- Click terrain 'h' cells / the O outline ring around ship.
- Re-click a dissolved brick's location (empty water where brick was).
- Click a green while ship passing? (timing unlikely — turn-based)
- Deep re-read of early-level logs for any gravity change NOT caused by a brick click.

## Turn 135 (A766-767) — ship self-click NO-OP; cap-click probe launched
A766 (21,28) blue body, A767 (22,28) yellow tail: both 1-cell diffs (bar ticks only). Ship self-click DEAD.
Log-wide flip audit (all 150 L9 actions): every gravity flip = brick click (or RESET). No hidden toggles ever.
Char inventory across cameras: only O,(,h,n,",f,G,$,-,I,z. Sole never-clicked object: G$G caps.

CAP GEOMETRY DECODED (A620/A622 landmark analysis — brick-pair spacing fixes cameras):
- A620 cam 18 (ship rose to w19 top after 2×ACTION4 from spawn, lane 33); A622 cam 48 (ship w−11, lane 27!).
- Caps at w−7 AND w−23, lanes 33/39/45/51/57 (G$G start cols 32,38,44,50,56).
- Cap cell structure: box-outline cell with '"""' rows and G$G on BOTTOM row (down-pointing kill face).
- Also: spawn ACTION4→lane27, ACTION4→lane33 rises ship to top w19 (cam 18) — cheap high perch!
- A621 (22,3) + A622 ACTION3 put ship at lane 27 w−11 (cam 48) — the box-ladder entry.

**This turn (bar 4→9)**: ACTION6(3,5) B27→N ship rises to spawn perch cam 0; ACTION6(39,15) replay A618
(box dissolve, keeps path byte-identical); ACTION4 ×2 → lane 33 top w19 cam 18; ACTION6(33,11) = CLICK CAP
at (33,−7). Outcomes: flip → 7th-toggle escape EXISTS (level solvable!); dissolve → free-rise opens (marginal);
no-op/death → caps dead, attempt auto-resets (throwaway anyway; B27+B39 already consumed).

## Turn 136 (A768-772) — cap-click NO-OP; undo-of-flip is the new lead
A772 cap click (33,11): 1-cell diff (bar tick). Caps inert. All exotic clicks now dead: z, ship body/tail, cap.
Wall c6-12 scan across cams (full coverage w-156..84, no gaps): open ONLY at door w-125..-121 and pocket w61-71.
A724 re-dump: door band w-125..-121 is open c0-23 (full corridor from column to top-world). Column top cap
w-132 + thick solid above = sealed. 1-wide slots c18/c24 only. Topology 100% closed.
BAR-FULL NEVER OBSERVED (max bar ever = 61, L8 win). "64 = reset" is an assumption. Bar row = 'z'*n + '$'*(64-n).

**KEY REALIZATION**: all prior undo full-restore proofs (A138/140, A197/199, A249/251-253) undid NON-FLIP
actions. Undo of a GRAVITY FLIP is untested. If ACTION7 restores board/ship but NOT gravity direction:
click brick (N->F) + undo (brick back, still F) = free flip source = PARITY ESCAPE.

**This turn (4)**: ACTION6(32,63) bar-row click probe; RESET (fresh: all 6 bricks, ship spawn (21,43) top w37,
cam 0, N); ACTION6(3,39) = B39 -> F, ship sinks to (21,51) cam -22; ACTION7.
READOUT next turn: if post-undo ship at spawn top w37 (pin 37, N) with B39 restored = full undo (no escape).
If ship re-sinks to (21,51) (pin 27) WITH B39 restored = board-only undo = LEVEL SOLVABLE via undo flips.
Route sketch if escape: normal door route but keep parity odd via one brick-click+undo pair at the right moment
(undo restores brick AND keeps F; brick re-dissolvable later... careful: undo also restores ship position —
must click+undo while ship rest position is flip-invariant? NO — undo restores ship to pre-click rest; if
gravity differs, ship immediately re-settles under new gravity. Usable: yes, plan around re-settling.)

## Turn 137 (A773-776) — undo IS full restore (gravity included); bar-overflow test begins
A773 bar-row click (32,63): no-op (verified safe no-op click for any state). A774 RESET; A775 B39 click
(F, ship sank); A776 ACTION7: ship back at SPAWN top w37 pin 37 = NORMAL, B27+B39 both restored.
UNDO RESTORES GRAVITY TOO. Undo escape DEAD.

**ROUTE THEORY PROGRESS (brick-hop descent)**: if ship enters column at (3,-123) F standing on box bridge
(bridge boxes at (15/9/3,-117) buildable via door-cell box walk — door cell empties again after its box is
clicked), then down-rides descend with automatic canopy refill (vacated cell refills each ride — VERIFY in
A647-649 boards). Landing on topmost intact brick, F camera reach = brick cells up to +24 below current
support brick. Brick gaps: -81→-57 (24 ✓), -57→-45 (12 ✓), -45→-21 (24 ✓), -21→+27 (48 ✗ TOO FAR),
+27→+39 (12 ✓). Climb can preserve B81/B57 by using B45 (click (3,39) at cam 84) and B21 ((3,41) at cam 62)
for P3/P5 — zero extra actions. BUT the ENTRY FLIP (N→F at door, cam 162, no bricks visible) remains
unsolved — every route dies there. Also the -21→+27 gap needs a mechanism.

**LAST UNTESTED MECHANIC: bar overflow (max ever seen = 61)**. Possibilities: attempt reset (assumed),
cap-and-continue (= infinite budget!), or something exotic (gravity flip = the escape). Testing via
20× no-op bar clicks per turn from bar 2. This turn → bar 22. Need ~3 more turns to reach 64.

## Turn 138 (A777-796) — bar burn 1/3 done (bar 22); descent search exhausted
20 no-op bar clicks executed cleanly. Two more burn turns to overflow.
OFFLINE ANALYSIS (column descent, all orderings):
- Ride-chain descent with canopy refill works down to B81; B81 click (N) caught by canopy ✓; B57 click (F)
  falls to B45 BUT leaves canopy at -93; any later N-flip free-rises ship back to stale canopy; canopy cannot
  be walked down (out of window). B21 reachable from B45 stand (screen 59). After B21: N-rise to stale canopy;
  B27/B39 never visible from high positions (48-row gap). Descent state machine: all paths strand ship high
  with N gravity and low bricks invisible.
- ENTRY FLIP (door, cam 162): impossible — no brick ever visible; climb REQUIRES N for all post-P5 phases;
  ship at door always N. No F source exists at altitude. This is THE wall.
- BUDGET NOTE: full route (climb 54 + bridge ~8 + descent ~15 ≈ 77) EXCEEDS 64 — if bar-full = reset, level
  needs a sub-64 route even if a flip escape existed. If bar caps-and-continues: budget infinite.
Bar-overflow test outcome space: (a) reset at 64 → need sub-64 route + flip miracle; (b) cap/continue →
budget solved, flip still needed; (c) exotic effect (flip?) → potential total solution.

## Turn 139-140 (A797-836) — burn complete to bar 62
This turn: 4 clicks crossing bar 64. Watch A838/839 boards: reset (spawn state, bar 0)? cap at 64?
gravity change? score change? Read frames carefully including any forced-RESET insertion by runner.

## Turn 141 (A837-840) — BAR IS NOT A BUDGET: triangle wave!
Bar hit 64 (A838): NO reset, board unchanged. A839: 63, A840: 62 — bar now DECREMENTS per action.
=> NO step budget exists. Unlimited actions per attempt. All prior 64-cap route constraints VOID.
(Historical "attempt resets" were all manual RESETs or deaths — never bar-driven. Confirmed by scan.)

IMPOSSIBILITY PROOF (brick-only mechanics): N => ship w monotone non-increasing... precisely: under N ship
never moves down; under F never up. Bricks (only flip sources) clickable only when in window; deepest-window
click position for any brick requires ship top >= -109. Door entry at -123 (above). A FLIPPED ship cannot
rise to the door; a NORMAL ship at the door can never descend or flip (no source visible from <= -117 region).
=> No brick-click sequence solves the level. Solution requires an unknown mechanic.

REMAINING UNKNOWN: bar countdown reaching 0 (event?). Testing: 62 more no-op clicks (~3 turns).
This turn: 20 clicks -> bar 42 (counting down).

## Turn 144 (A901-905) — BAR ZERO = RESET; TRUE BUDGET = 128; sandwich-ride hypothesis
A902 bar hit 0 (countdown); A903 = FORCED RESET (attempt 2->3, repeated step label, full restore, bar 0).
Bar = triangle 0->64->0, attempt resets when returning to 0. TOTAL BUDGET 128 ACTIONS/attempt. Route fits!
Current: fresh attempt 3, bar 2 (A905), spawn state, ALL 6 BRICKS, N.

**HOLE IN IMPOSSIBILITY PROOF**: ride may be CONTACT-based not gravity-based. Never tested: N-gravity ship
pressed under ceiling WITH box directly below (sandwich) — click box below = down-ride?? If yes:
FULL ROUTE EXISTS (sketched): climb via B45/B21 flips (preserve B81,B57) -> door bridge -> seed column
scaffold -> enter (3,-123) sandwiched -> sandwich-rides DOWN (each ride refills above + spawns below,
side boxes at (9,W) each ride) to (3,-87) atop B81 -> click B81 (F, fall to B57) -> click B57 (N, rise to
canopy -93, pressed) -> up-ride once + sandwich-rides down empty column to (3,21) atop B27 -> click B39
remote (F) -> click B27... (parity juggle; end N) -> sandwich-ride to pocket (3,63) -> clear (9,63) box
(click: spawns (9,69) hmm) -> walk (9,63)->(15,63) -> get box into (15,69)=z cell via (9,69) click -> 
sandwich down-ride INTO z = WIN. (Endgame ordering needs care re: side-spawns; refine after test.)

**THIS TURN'S TEST (4)**: A4,A4 (lane-33 perch, ship cell (33,21) pressed under grid box (33,15), cam 18);
ACTION6(33,33) up-ride -> ship (33,15), refill expected at (33,21) = box below = SANDWICH, cam 24;
ACTION6(33,45) click box BELOW ship. READ: ship down into (33,21) = REVOLUTION; ship stays = dead end.

## Turn 145 (A906-910) — DEATH: skipped A618 seed box; retest with it
A907 (2nd ACTION4): ship rose lane 33 shaft into w-7 cap = DEATH (57 frames). A618's (39,15) dissolve is
what seeds box (33,15) (side-spawn) — without it lane 33 is a kill chute. A908 auto-RESET (attempt 4, free).
A909/A910 were water no-ops. Current: attempt 4, bar 2, spawn, all 6 bricks, N.
LESSON: lane-27 rise is safe from spawn; lane-33 needs (33,15) box seeded first.
**Retest (5)**: (39,15) seed, A4, A4 [perch (33,21) under (33,15), cam 18], (33,33) up-ride [-> ship (33,15),
refill (33,21) below, cam 24], (33,45) = SANDWICH DOWN-RIDE TEST on box below.

## Turn 146 (A911-915) — CRITICAL MECHANICS CORRECTION: rides do NOT refill vacated cell
A911-913 clean (seed, perch (33,21) under (33,15), cam 18). A914 up-ride -> ship (33,15), cam 24 ✓,
spawns went to (39,15) refill + (39,21), but (33,21) [ship's vacated cell] = WATER. NO REFILL.
=> ladder climbs never left boxes below; sandwich must be seeded via SIDE boxes.
A915 (33,45) hit water = no-op. Sandwich never formed.
ROUTE IMPACT: scaffold descent plans must seed below-boxes from side-spawned columns (lane 9 companions
exist: each column ride spawns (9,W) side box which can then seed (3,W+6) via click... verify geometry).
Current: cam 24, ship (33,15) pressed under (33,9); boxes (39,15),(39,21); B21 VISIBLE rows 1-5 ✓ (visibility
model confirmed); B27 rows 49-53; B39 partial 61-62.
**This turn (2)**: (39,45) = click box (39,21) -> spawns left (33,21) = box directly below ship = SANDWICH;
then (33,45) = THE TEST: click box below ship under N. Down-ride => level solvable.

## Turn 147 (A916-917) — sandwich down-ride DEAD; CROSS-LEVEL AUDIT => TRIGGER-BRICK HYPOTHESIS
A916 seeded (33,21) below ship OK; A917 clicked it under N: box dissolved (spawns (27,21),(33,27)), SHIP DID NOT MOVE.
Rides strictly require pressed-contact in gravity direction. Impossibility proof premises all verified... under KNOWN mechanics.
Pocket-floor lead re-confirmed dead (turn-130: floor = terrain, A727/728 no-ops).

CROSS-LEVEL LOG AUDIT (zero-action, decisive):
- L7 (A431-523): SAME base game. Flip clicks at various (3,y); pins 38(N)/28(F) for its 2-tall ship. Nothing new.
- L8 (A524-617): board evolves PER TICK (purple rain descending 6 rows/action) — level-specific. Red brick APPEARED
  mid-level (A613) at (33,3); clicking it (A614) = flip (pin 38->28, 43-frame settle), then 2xA4 into z = WIN.
- Purple '"' in L9 = BOX INTERIOR FILL (A617 spawn board: single box (39,15) purple-filled; A618 click = normal
  dissolve+4-way spawn). No purple mystery.
- **L6 (A166-430) KEY FIND**: brick #1 at (37-41,31-35); click = flip + dissolve. Then after flip + 2x ACTION4
  (ship reaching screen col 50), brick #2 APPEARS at (25-29,27-31) — REPRODLUCED deterministically in attempts 1 & 2
  (A172-174 and A191-193). Bricks can be POSITION-TRIGGER SPAWNED when ship reaches a location.
- L9 dissolved bricks verified NOT regenerating over 7+ actions (A726-733 lane-3 scan).

**HYPOTHESIS**: L9's 7th flip source is a trigger-spawned brick in the never-visited door corridor / column top
(c0-23 at w-123). Parity works: entry flip (trigger) + 6 brick toggles = 7 = odd => F at pocket. 

**PLAN (multi-turn, budget 128 OK)**:
T1 (this turn, 20): RESET + P1 replay 19 verbatim -> ship (21,-45) cam 84.
T2 (20): turn-125 batch verbatim: P2 canopy-right 6, P3 flip (3,3), P4 down/pad 9, P5 re-flip (3,5), rides (57,33)x3.
T3 (15): turn-126 batch verbatim: rides (57,33)x4, walk-left [(51,39),A3]x5 lanes 51->27, (27,33) open plug 27
   -> ship pressed under green (27,-93).
T4 (5): turn-127/128 verbatim: (45,3),(39,3),(33,3) canopy chain row -123; (27,33) open green#1 -> free-rise to
   (27,-117) pressed under canopy (27,-123) cam ~156; (9,33) open green#2 door.
T5 (9, NOVEL — watch every frame for 'n' spawns): (27,31) up-ride -> ship (27,-123) cam 162 [ride spawns
   (27,-129) canopy + (21,-123) + (33,-123)]; then [(21,39) dissolve blocker/spawn canopy, A3] x4 pattern:
   (21,39),A3,(15,39),A3,(9,39),A3,(3,39),A3 -> ship (3,-123) IN COLUMN pressed under (3,-129), box below (3,-117).
   Door cell (9,-123) gets box-filled by (15,39) click, then dissolved by (9,39) click (spawns (3,-123) box,
   dissolved in turn by (3,39) click which spawns (3,-129)+(3,-117)).
If trigger brick appears anywhere: click it -> F -> sink onto (3,-117) -> down-rides (3,35)x6 -> B81... plan
descent flips carefully (canopy stack pre-build trick: remote clicks (3,45),(3,51),(3,57),(3,61) from (3,-123)
build boxes -117/-111/-105/-93 with gap -99 — refine when trigger confirmed).
If NO trigger: attempt lost but corridor/column state fully observed; next audit L1-L5 for other spawn conditions.

## Turn 148 (A918-937) — T1 PERFECT
RESET + P1 replay: settled A937 byte-identical to A748 (diff 0). Ship (21,-45), cam 84, bar 19, N.
This turn = T2 (turn-125 batch verbatim, 20): P2 canopy-right, P3 flip (3,3)=B45? [historically (3,3) at cam 84
= B81 per turn-124 P3 label; whichever — proven byte-identical], P4 down+pad-walk, P5 re-flip (3,5), 3 ladder rides.
Expect after: ship (57,-51), cam 90, bar 39. Then T3 (15): rides x4, walk-left x5 pairs, open plug 27.

## Turn 149 (A938-957) — T2 PERFECT
Byte-identical to A659 (diff 0). Ship (57,-51), cam 90, bar 39, N, 3 rides done.
This turn = T3 (turn-126 batch verbatim, 15): rides (57,33)x4 -> (57,-75) under sealed plug 57;
walk-left [(51,39),A3]x5 -> ship (27,-75); (27,33) opens plug 27 -> free-rise to pressed under GREEN (27,-93), cam 126.
Expect bar 54. Then T4 (5): (45,3),(39,3),(33,3) canopy row -123; (27,33)?? NO — green#1 click coords at cam 126: (27,39)?
CHECK turn-127: canopy chain clicks were (45,3),(39,3),(33,3) at cam 126, then GREEN#1 click = (27,33)... verify A723 tool
call exactly next turn. A724 door click was (9,33) at cam 156 (post-rise).

## Turn 150 (A958-972) — T3 PERFECT
Byte-identical to A719 settled (diff 0). Ship pressed under green#1 (27,-93), cam 126, bar 54, N.
This turn = T4 verbatim A720-724 (5): canopy chain row -123 [(45,3),(39,3),(33,3)], (27,33) open green#1
-> free-rise to (27,-117) pressed under canopy (27,-123) cam 156, (9,33) open door green#2.
Next turn T5 NOVEL corridor entry (9): (27,31) up-ride [-> ship (27,-123), cam 162, spawns (27,-129)+(21,-123)+(33,-123)];
then (21,39),A3,(15,39),A3,(9,39),A3,(3,39),A3 -> ship (3,-123) in column pressed under (3,-129).
WATCH EVERY BOARD for 'n' trigger-brick spawns. Verify cam/box layout before T5 (esp. rows -129 boxes at 33,39,45).

## Turn 151 (A973-977) — T4 PERFECT; T5 corridor entry committed
Byte-identical to A724 (diff 0). Ship (27,-117) pressed under canopy (27,-123), cam 156, bar 59, N, door OPEN.
Board verified: corridor row -123 = screen rows 31-35; c0-23 water there; (33,-123) empty; row -129 boxes at 33/39/45
only ((15/21/27,-129) empty); wall c6-12 solid above/below door band; kill line row 24 w-132 with 1px gaps c18/c24.
T5 (9, NOVEL): (27,33) up-ride -> ship (27,-123) cam 162 [spawns (27,-129),(21,-123),(33,-123)];
(21,39) dissolve [spawns (21,-129),(15,-123),(21,-117)]; A3 -> (21,-123);
(15,39) [spawns (15,-129),(9,-123)box-in-door,(15,-117)]; A3 -> (15,-123);
(9,39) [spawns (3,-123) only]; A3 -> (9,-123) under wall;
(3,39) [spawns (3,-129),(3,-117)]; A3 -> ship (3,-123) IN COLUMN pressed under (3,-129), box below (3,-117).
WATCHING every settled/frame board for trigger-spawned 'n' bricks (L6 precedent). If trigger appears: click -> F ->
down-ride chain (3,35)x6 to B81. If nothing: attempt stuck N-in-column; next step = L1-L5 audit for spawn conditions.

## Turn 152 (A978-986) — T5 corridor entry PERFECT; NO trigger brick
Ship walked corridor lanes 27->3 exactly as planned. Now: ship (3,-123) IN COLUMN (first ever), N, pressed under
box (3,-129), box below (3,-117), cam 162, bar ~68 (past peak, counting down, 60 left).
NO 'n' in ANY frame of A978-986. Trigger hypothesis NOT confirmed at corridor. Boxes now: row -123: (39),(45)
remain; row -117: (3),(15),(21),(33),(39),(45) [gap (27) ship-vacated]; canopies (3,-129) + (15/21/27,-129)
spawned during walk. Door cell (9,-123) empty again (its box dissolved to spawn (3,-123)).
Column cap above (3,-129) verified SAFE terrain (no G$G, rows 20-24 solid O).
THIS TURN (1): ACTION6(3,33) = up-ride into (3,-129) -> ship top -131 pressed under cap w-132, cam 168.
REVEALS w-168..-163 (never seen!) + last unvisited cell (trigger chance). No spawns expected ((3,-135) solid,
(9,-129) wall, vacated no-refill).
If nothing: L1-L5 mechanics audit next; attempt still has ~59 actions for further probes.

## Turn 153 (A987) — BREAKTHROUGH: HIDDEN TOP BRICK ROW FOUND
A987 up-ride to cap: ship (3,-129) rows -131..-128, cam 168, pressed under cap w-132 (SAFE).
REVEAL rows 1-5 (w-167..-163): FULL ROW OF RED BRICKS at lanes 9,15,21,27,33,39,45(,51,57?) —
interiors 'nnnnn' cols 7-11,13-17,... Only visible at cam 168 (cap press). Not trigger-spawned: always there,
above the previously-known map edge. = unlimited-ish flip sources at altitude. PARITY SOLVED.
Column scan (all cams): c0-5 between cap and floor w72 = ONLY the 6 bricks (shells 1-thick, vanish on dissolve)
+ current box (3,-117). w-12 line does NOT cross c0-5. Pocket rows 61-71 c0-5 water, floor 72 solid.

WIN ROUTE (20 this turn + 1 next):
(9,3) flip F -> fall rest on box (3,-117) shell; (3,34) ride x6 [-117,-111,-105,-99,-93,-87; spawns below
consumed each time, none left after]; (3,34) = B81 click -> N, rise to cap; then pairs:
(15,3) F fall onto B57, (3,34) -> N rise; (21,3)/(3,34) B45; (27,3)/(3,34) B21; (33,3)/(3,34) B27;
(39,3)/(3,34) B39; (45,3) F -> FULL FALL to pocket floor, ship (3,69) rows 68-71, cam -41; ACTION4 -> (9,69).
NEXT TURN: ACTION4 -> (15,69) = Z DOCK = WIN (score 9).
(3,34) works whether ship rests on shell (interior s 32-36) or interior top (31-35). Bar after batch ~89/128 OK.
No death modes: ship stays c1-5, cap safe, falls land on shells/bricks, pocket walk safe.

## Turn 154 (after A1007) — RIDE-THROUGH MECHANIC + descent state
- REVISED MECHANIC: clicking a brick the ship is PRESSED AGAINST (gravity direction) = RIDE-THROUGH: brick/box dissolves, ship moves into its cell, NO gravity flip. Only REMOTE brick clicks flip gravity. All A989-1005 (3,34) clicks were 12-frame down-rides; each ride spawns box copies into empty cardinal neighbors of dissolved cell EXCEPT ship-occupied & ship-vacated cells → infinite down chain in open water.
- Top-brick clicks (15,3)...(45,3) were 2-frame no-ops (ship never returned to cap). A1004 (39,3)=6 frames, unidentified remote hit, apparently harmless. A1007 ACTION4 blocked by wall (3-frame turn only).
- State at A1007: ship (3,-51) resting on B45, gravity F, cam≈79-80. B81/B57 dissolved via ride-through. B45,B21,B27,B39 remain. Bar ~89/128 used (~39 left).
- WIN CHAIN: 20× ACTION6(3,34) rides: -45(B45),-39,-33,-27,-21(B21),-15,-9,-3,3,9,15,21,27(B27),33,39(B39),45,51,57,63,69 → ship at (3,69) pocket floor, cam≈-41. Side spawns blocked by wall except pocket band: rides into (3,63)/(3,69) spawn blockers (9,63)/(9,69).
- ENDGAME next turn (~4 actions, verify board first): click box (9,69) (est screen (9,28)) → ACTION4 to (9,69) → click (15,69) box (est (15,28)) clears z cell → ACTION4 DOCK into z (15,69) = score 9. Budget 89+20+4=113<128 OK.

## Turn 155 (after A1027) — MECHANIC RESOLVED + 7-action win ladder
- Frame forensics A989-1005: every 12-frame ride consumed a PURPLE BOX below ship (frame0 shows '"' at rows 34-36 dissolving). Bricks were NEVER ridden through. TRUE RULE: click box directly below = ride (dissolve+move+spawn copies); click BRICK anywhere = FLIP GRAVITY + dissolve brick. A1008 clicked B45 (brick below) -> flip N, ship rose 44 frames to cap. B81/B57 never existed in path (dissolved pre-chain / map misattribution).
- A1027 state: ship pressed under cap, N gravity, cam 168, facing RIGHT ('ffG'). Top bricks remain at lanes 15,21,27,33 (screen cols 13-17,19-23,25-29,31-35, rows 1-5). Lane 9 consumed by A988.
- Column audit: B21(3,-21) present (A1008 rows 57-61). B27(3,25-29 world) present at A620(cam18) AND A767(cam-22). B39 GONE at A767 (present at A620) - dissolved mid-attempt. Band w61-71 + floor w72 clear, no leftover boxes (falls/flips spawn nothing).
- Bar: 45 used of 64 down-slope, 19 'z' left.
- WIN LADDER (7 actions, all falls free of box spawns): (15,3) flip F -> fall cap to B21; (3,34) click B21 flip N + dissolve -> rise to cap; (21,3) flip F -> fall to B27 (land cell (3,21)); (3,34) click B27 flip N + dissolve -> rise; (27,3) flip F -> fall ALL the way to pocket floor (3,69); ACTION4 -> (9,69); ACTION4 -> (15,69) = z DOCK = SCORE 9.
- Fallback branches: if B27 already gone, 3rd click's fall lands (3,69) directly; then (3,34)=floor no-op, (27,3) hits unknown at world (27,43) (likely wall no-op, spawns can't reach pocket), ACTION4 x2 still docks. 12 actions spare.

## Turn 156 (after A1034) — B39 exists; 4-action finisher
- Ladder ran perfectly through 5 flips (all 44-frame), but A1032 fall landed on B39 at (3,39) — it EXISTS (Turn-155 "B39 gone at A767" was a misread, probably wrong cam). Settled A1034: cam -4, ship cell (3,33) pressed on B39, F gravity, facing right. A1033/34 blocked by wall c6-12 (band opens only w61+). B21, B27 confirmed dissolved (rises at A1029/1031).
- Column below B39 verified clear w43-66 on current board; floor w72. Bar: 52 used, 12 left.
- FINISHER: (3,34) click B39 = flip N + dissolve -> rise to cap; (33,3) top brick lane 33 = flip F -> fall full column to (3,69); ACTION4 -> (9,69); ACTION4 -> (15,69) z DOCK = score 9.
- Robustness: if yet another brick hides at (3,69), ship lands (3,63) instead; ACTION4 into open band (9,63), auto-sink to (9,69), ACTION4 -> z. Same 4 actions. 8 spare after.
