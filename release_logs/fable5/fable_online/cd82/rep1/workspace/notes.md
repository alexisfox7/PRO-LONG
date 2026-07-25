# Game notes

## Level 1 (initial)
- Target card top-left (black frame, x3-12): white 10x5 (y3-7) OVER purple 10x5 (y8-12). Goal = 10x10 block, top half white, bottom half purple.
- Header palette (gray area): white 3x3 swatch @ x36-38,y3-5; purple 3x3 swatch @ x42-44,y3-5; white underline bar @ x41-45,y7 (under purple swatch — selection indicator?).
- Dispenser: '#' frame x25-38, y24-32, open bottom; interior purple 12x7 (x26-37,y25-31).
- White 10x10 block x27-36, y34-43, below dispenser opening.

## Hypotheses
- Dispenser stamps/pours its color onto block below. Select color via palette click.
- Test 1: ACTION5 (interact) alone — observe effect.

## After Action 1 (ACTION5)
- Mechanic: block rises through dispenser's open bottom, dips into paint, returns. Top 5 rows painted dispenser color.
- Block now: purple y34-38, white y39-43. Target: white top, purple bottom => need 180 flip.
- Dispenser paint not consumed. Underline stays under purple swatch.
- Row 63 = step counter: 1 'O' per action used, 64 budget?
- Next test: ACTION1 (up) — does it flip/rotate block?

## After Action 2 (ACTION1)
- ACTION1 (up): total no-op, board identical, step counter still 1 (no-ops may not count).
- Next: ACTION3 (left) — test rotation. Then ACTION2/ACTION4/clicks if needed.

## After Action 3 (ACTION3)
- ACTION3 tilts DISPENSER 45deg left (diamond, opening lower-left). Paint stays inside, settles with gravity. Block untouched. Counter now 2.
- ACTION4 presumably tilts right (undo). Warning: more tilt might spill paint.
- New hypothesis: dip depth may vary/progress; or palette click (white swatch @ ~37,4) switches paint color. Route to win: get all-purple block, then white dip on top 5.
- Test: ACTION4 (untilt) + ACTION5 (2nd dip) — check depth of 2nd dip.

## After Actions 4-5 (ACTION4, ACTION5)
- ACTION4 untilted dispenser (back upright). ACTION5 2nd dip: depth still 5 rows, no color change. Dip depth FIXED at 5.
- Counter: only state-changing actions count (a5 no-change dip didn't increment). Now 3/64.
- Note: POST-ACTION board in log is pre-animation transient; [settled] board is committed state.
- Remaining ideas to flip block: ACTION2, ACTION6 click on block (32,39), pour via 90deg tilt.
- Test: ACTION2 then ACTION6(32,39).

## After Actions 6-7 (ACTION2, ACTION6(32,39))
- ACTION2: counter incremented (4/64) but NO visible board change => hidden state change? (maybe affects next dip)
- Click on block: totally ignored (no counter, no change).
- Test: ACTION5 dip to see if ACTION2 changed dip behavior.
- Untested: clicks on palette swatches (37,4)/(43,4), click dispenser, 90deg pour.

## After Action 8 (ACTION5 dip post-ACTION2)
- Dip identical/no-op: ACTION2 hidden state did NOT alter dip. Dips idempotent, always top-5, current color.
- Next: ACTION6(37,4) click white palette swatch — expect paint color switch (underline moves, dispenser interior turns white?).
- If color switching works, still need mechanism for purple-on-bottom. Ideas: tilted dip = diagonal paint line; card click; ACTION2 semantics unknown.

## After Action 9 (click white swatch 37,4)
- COLOR SWITCH CONFIRMED: underline now under white swatch; dispenser paint all white ($). Counter ~6.
- Frames re-analysis (action 1): DISPENSER descends 7 rows onto static block (opening down), paints intersection = block top 5 rows. Stroke fixed.
- Reachable states via dips alone: top-k recolor only => need flip/other mechanic for purple bottom.
- Current block: purple top5/white bottom5. Dispenser: white paint. DO NOT dip now (would erase purple).
- Probes: click card (7,7), dispenser (31,28), block bottom (32,41).

## After Actions 10-12 (clicks: card, dispenser, block-bottom)
- Card (7,7): ignored. Dispenser (31,28): counter tick, no visible change. Block bottom (32,41): counter tick, no visible change.
- Theory: clicks SELECT objects invisibly; arrows then act on selected object. Block possibly selected now (last click).
- Counter ~8/64 used. Test: ACTION3 — if block rotates/tilts instead of dispenser, selection confirmed.

## After Action 13 (ACTION3)
- Selection theory DEAD: ACTION3 tilted dispenser again (45deg left, white paint inside). No counter tick this time (counter semantics unclear — maybe timer).
- Ops so far: upright dip => top5:=color. Tilt L/R. Color switch via swatch.
- Test: ACTION5 while tilted 45 — expect diagonal paint region? White-over-purple diff will reveal geometry. Recoverable: purple upright dip restores top5 purple.

## After Action 14 (tilted white dip)
- Tilted dip painted diagonal region: white covered all except right triangle {x+y>70} rows35-38 + wall-excluded (27,43). Paint = RIGID body rotating with container; dip stroke always 7 rows; painted = paint body ∩ block at deepest.
- Reachability analysis: bottom-middle block cells (e.g. 31,43) unreachable by any dip at 0/45/90 tilt => card's purple bottom5 impossible via dips alone => hidden mechanic must exist.
- Counter: ~1 tick per effective action, 9/64 used. Not decoded fully, not bottleneck.
- Current: dispenser tilted 45CCW, white paint; block mostly white + purple triangle right rows35-38.
- TEST flood-fill theory: click purple swatch(43,4), click block(32,41) => if block fills purple, then ACTION4 upright, white swatch(37,4), ACTION5 dip => rows34-38 white, 39-43 purple = WIN.
- If fill fails: sequence still leaves block all-white clean slate, dispenser upright white.

## After Actions 15-19 (fill test + clean slate)
- a15 purple swatch: color switch OK. a16 click block with purple selected: NOTHING => flood-fill theory DEAD.
- a17 untilt OK, a18 white swatch OK, a19 white dip erased purple triangle.
- STATE NOW: block ALL WHITE (x27-36,y34-43), dispenser upright white paint, underline under white. Score 0. Counter ~11/64.
- Unexplored: tilt beyond 45 (90+ pour?), ACTION2 mystery, click block top, click below block, RESET.
- Test: ACTION3 x2 => 90deg CCW. Watch for pour animation / new dip geometry.

## After Actions 20-21 (ACTION3 x2)
- TILT SATURATES at 45deg: second ACTION3 no-op. No 90deg, no pour. Mechanic space: tilt in {-45,0,45}, dip, color swatch.
- ACTION2 transient also empty: truly invisible.
- Reachability (model): union of purple dips at all 3 tilts misses bottom-middle wedge (row40:x31-32, row41:x30-33, row42:x29-34, row43:x28-35) => if model right, target unreachable => interpretation wrong.
- DECISIVE TEST (7 actions): purple swatch(43,4); dip upright; ACTION3; dip 45L; ACTION4,ACTION4; dip 45R. Block currently all white.
  - If block ends ALL purple => model wrong, then white swatch + upright dip = WIN.
  - If wedge stays white => painting interpretation dead; rethink (mirror-match? submit action? recipe?). Then likely RESET.

## After Actions 22-28 (triple purple dips)
- Union of purple dips at 3 tilts = block purple EXCEPT white wedge bottom-middle (row40:x31-32, 41:x30-33, 42:x29-34, 43:x28-35). Model CONFIRMED empirically.
- Wedge cells can NEVER be painted by anything => block-matches-card is IMPOSSIBLE => wrong win-condition interpretation. Card unchanged all game.
- Dispenser now 45CW, purple. Counter ~15/64.
- New interpretation: card = desired SCENE (white=dispenser paint above, purple=block below). Test: click white swatch only -> dispenser white + block mostly purple; check score.

## After Action 29 (white swatch)
- Scene interpretation (white dispenser + purple block): NO score. Dead (or needs fully-purple block, impossible).
- Realization: actions 22-28 never included an upright dip (started tilted); union L+R covered rows34-39 anyway.
- CLOSEST-STATE TEST: ACTION3 (untilt from 45R), ACTION5 (upright white dip) => block = white top5 / purple bottom5 EXCEPT white wedge. If checker samples sparse cells... test cheap.
- If no score: RESET, examine pristine board minutely, rethink from zero.

## After Actions 30-31 (untilt + upright white dip)
- Block: white top5 / purple bottom5 + white wedge. Header a31 shows Score 0 (may lag one action; verify next call).
- Mid-dip-scene theory also poisoned by wedge. Wedge unfixable => any exact-match interpretation dead.
- UNTESTED COMBO: ACTION2 while TILTED (pour gesture). Current: upright, white paint. Test: ACTION3 (45L), ACTION2 (pour?).
- If nothing: RESET next, attempt 2, fresh observation.

## After Actions 32-33 (tilt L, then ACTION2) — BREAKTHROUGH
- ACTION2 while tilted 45L => dispenser rotates to FULL 90L and GROUNDS: frame cols17-25, rows32-45; LEFT wall col17, opening faces RIGHT (col25 open); paint 7x12 (cols18-24, rows33-44) = spans FULL block height.
- Explains ACTION2 upright no-op (no tilt to extend). ACTION1 likely the reverse (lift/rotate back) — was no-op when already upright.
- Block cols27-36 rows34-43, to the right, 2-col gap.
- WIN PATH: purple swatch; sideways dip (paint left 5 cols 27-31 full height); return upright; rotate to 90R; sideways dip (right 5 cols 32-36); return upright; white swatch; top dip => white top5/purple bottom5 = CARD.
- Test now: ACTION6(43,4) purple; ACTION5 sideways dip. Verify band = cols27-31 full height (incl. wedge cols in those columns).

## After Actions 34-35 (purple swatch + sideways dip)
- SIDEWAYS DIP CONFIRMED: painted block cols27-31 FULL HEIGHT purple (stroke 7 right, paint spans rows33-44 > block).
- Block now: cols27-31 all purple; cols32-36: rows34-38 white, row39 purple, wedge-right remains white (row40:32, 41:32-33, 42:32-34, 43:32-35).
- REMAINING WIN PATH: return upright (ACTION1?), go 45R (ACTION4 x?), ACTION2 => 90R grounded right of block, purple sideways dip => cols32-36 full purple => block ALL purple; then upright, white swatch, top dip => CARD MATCH.
- Test: ACTION1 (return rotation?).

## After Action 36 (ACTION1)
- ACTION1 = lift grounded container back to 45 tilt. FULL STATE MACHINE:
  A3/A4: rotate CCW/CW between -45/0/+45; A2 at +-45: ground to 90 (same side, opening faces block); A1: grounded -> 45; A5: dip (stroke 7 toward opening).
- WIN SEQUENCE QUEUED: A4,A4 (to 45R), A2 (ground right), A5 (purple side dip cols32-36), A1, A3 (upright), white swatch, A5 (top dip white rows34-38).
- Expected final block: white rows34-38, purple rows39-43 = CARD. Expect score 1.

## LEVEL 1 SOLVED (Action 44, Score: 1)
- Win sequence executed exactly as planned. Total 44 actions for level 1.

## Level 2 (initial, after action 44)
- Same geometry: dispenser x25-38 y24-32 (purple paint 12x7), block ALL WHITE x27-36 y34-43. Counter reset (row63 all q).
- Palette 3 swatches: white click (34,4), purple (40,4), ORANGE (46,4). Underline under purple.
- CARD target (block coords): purple = rows34-38 ∩ {x+y<=69}; white = rows39-43 ∩ {x+y<=69}; orange = {x+y>=70} (anti-diagonal split).
- EMPIRICAL MASKS (from L1 diffs a23/a28): U=rows34-38 all cols; L(45L dip)={x+y<=70} full 55 cells incl (27,43); R(45R dip)={y-x<=7} incl (36,43); GL=cols27-31; GR=cols32-36. No corner exclusions (a14 note was wrong — cell was already white).
- IMPOSSIBILITY PROOF with these 5 ops: bottom diag70 cells (27,43),(28,42),(29,41),(30,40),(31,39) need orange; only L and GL cover them; both also cover ALL of white target region (rows39-43,{x+y<=69} ⊂ cols27-30); orange must be LAST there, but then nothing can (re)paint white region (R and U don't reach it). Block starts white but GL/L-orange would erase. => NEW MECHANIC required.
- Probe queued: A3 (45L), A2 (ground left), A3 (rotate while grounded??), A5 (dip → reveals mask). If A3-grounded no-op, dip = purple GL cols27-31 (recoverable).
- Other untested: A2 while grounded, A1 at 45 (lift higher?), A4 while grounded-left, clicks on card/new elements.

## After Actions 45-48 (ground left, A3 probe, dip)
- a47 A3-while-grounded: NO-OP (counter tick only). But container frame is at cols17-25, nearly at left play edge => A3 may be a BLOCKED SLIDE, not absent mechanic.
- a48 GL dip confirmed: cols27-31 purple. Block now: cols27-31 purple, cols32-36 white. Dispenser grounded-left, purple. Counter 3.
- NEW HYPOTHESIS: grounded container SLIDES with A3/A4; sliding right (closer to block) deepens dip (paint 7 wide, currently reaches cols25-31 => 5 cols overlap; adjacent would reach 7 cols).
- NOTE: even slides don't obviously solve target (orange bottom-diag still conflicts with white region — any grounded-left orange dip spans full height). May need vertical offset or tilted-grounded dip. Keep probing.
- Queued: A4 (slide right?), A5 (reveal mask change).

## After Actions 49-50 (A4 grounded, dip)
- A4-grounded: TOTAL no-op (no counter). Dip no-change (counter tick only). NO SLIDE MECHANIC.
- Board diff L1-init vs L2-init: ONLY card + palette changed. No new elements.
- Untested remaining: A2 while grounded (rotation continues past 90 => POUR? top candidate), A1 at 45, orange-over-purple color behavior.
- Queued: single A2 (grounded-left, purple paint) — watch for pour/tip animation.

## After Action 51 (A2 grounded-left) — NEW MECHANIC FOUND
- A2 at grounded rotates FURTHER: container now 135deg DIAMOND resting BELOW-LEFT of block (frame diagonals rows40-56, cols~14-30), opening faces UP-RIGHT toward block corner (27,43). Paint held in lower V. Stable.
- Predicted masks: BL-diamond dip = {y-x>=cBL} (lower-left corner triangle, main-diagonal boundary); BR-diamond dip (symmetric, via grounded-right+A2) = {x+y>=cBR} (lower-right triangle, anti-diagonal boundary).
- IF cBR=70: LEVEL 2 SOLUTION = purple upright dip (rows34-38) THEN orange BR dip ({x+y>=70}) on initially-white block. 2 paints!
- Block damage always recoverable: white GL+GR dips repaint everything (incl wedge).
- Current block: cols27-31 purple, cols32-36 white. Counter ~5/64.
- Queued nav to BR (no dips): A1 (BL->GL expected), A1 (GL->45L), A4 (->0), A4 (->45R), A2 (->GR), A2 (->BR). Each step logged; diffs will reveal true transition table even if guesses wrong.
- Next call: verify BR position, then orange swatch (46,4) + A5 to measure cBR.

## After Actions 52-57 (nav BL -> BR) — TRANSITION TABLE CONFIRMED
- All guesses right: A1: BL->GL, GL->45L; A4: 45L->0, 0->45R; A2: 45R->GR, GR->BR.
- Full rotation ladder: BL <-> GL <-> 45L <-> 0 <-> 45R <-> GR <-> BR. A3/A4 rotate only between -45..+45; A2 = down-ladder (45->G->B), A1 = up-ladder (B->G->45).
- BR diamond: frame rows40-56 cols33-49, opening up-left toward block corner (36,43), purple paint inside, stable.
- Queued: orange swatch (46,4) + A5 => measures BR dip mask {x+y>=cBR} on mixed block (visible on both purple and white cols).
- IF cBR=70, WIN SEQUENCE (17 actions from BR): A1, white(34,4), A5 [GR white]; A1, A3, A3, A2, A5 [GL white]; A1, A4, purple(40,4), A5 [upright purple top5]; A4, A2, A2, orange(46,4), A5 [BR orange] => TARGET.

## After Actions 58-59 (orange BR dip) — MASK CONFIRMED
- BR dip = {x+y>=70} EXACT (55 cells). BL by symmetry = {y-x>=7}.
- Block now: orange {x+y>=70}; purple cols27-31 rest; white cols32-36 rest.
- WIN SEQ (18 actions, queued): nav BR->BL (A1,A1,A3,A3,A2,A2), white(34,4), A5 [BL white {y-x>=7} covers whole white-target region];
  A1,A1,A4 (BL->0), purple(40,4), A5 [upright purple rows34-38];
  A4,A2,A2 (0->BR), orange(46,4), A5 [BR orange last].
- Proof: white target ⊂ {y-x>=7} (max needed y-x=9... all cells have y-x>=9? (30,39)=9 ✓ included since >=7); BL-whitened rows34-38 cells repainted purple by upright; all disturbed orange restored by final BR dip; no residual mismatches (checked region algebra).
- Expect Score 2. Counter ~14+18=32/64.

## LEVEL 2 SOLVED (Action 77, Score: 2). Total 77 actions.

## Level 3 (initial, after action 77)
- Same dispenser (purple, x25-38 y24-32) + white block (x27-36 y34-43). Counter reset.
- NEW: HOPPER above dispenser: frame rows18-22 cols29-34, open bottom; contents: WHITE 2 cells (31-32,row19) over PURPLE 4x3 (cols30-33 rows20-22).
- Palette 7 swatches, click coords: white(23,4) purple(29,4) orange(35,4) yellow(41,4) green(47,4) red(53,4) blue(59,4). Underline under purple.
- CARD (block coords): orange RECT cols30-33 rows34-36; green {x+y>=71 AND x>=32}; red {x+y>=71 AND x<=31}; purple = rest (incl diag x+y=70).
- Orange 4x3 rect not composable from L1/L2 masks => new mechanic (hopper => variable paint quantity => smaller strokes?).
- Probe queued: click orange(35,4), then A5. Watch hopper/dispenser/underline changes per action.

## After Actions 78-79 (orange swatch, dip)
- Swatch click recolors dispenser paint AND hopper lower layer (both orange now). Hopper's 2 white neck cells (31-32,row19) UNCHANGED — maybe air/empty or separate.
- A5 dip: standard top-5 (rows34-38 orange). Hopper not consumed/changed by dip.
- KEY: hopper paint body = 4x3 at cols30-33 == card's orange rect (block cols30-33, rows34-36) EXACTLY. Hopper = second smaller stamp?
- Block now: orange rows34-38, white rows39-43.
- Probe queued: click hopper (31,20) then A5 — does click select/activate hopper as the dipping tool?
- Other ideas if no-op: A1 upright (dispenser dips UP into hopper? load/transfer), click hopper frame, arrows after hopper click.

## After Actions 80-81 (click hopper, dip)
- Click hopper (31,20): counter tick, NO effect. Dip after: unchanged (idempotent). Hopper not click-activated.
- Queued: A1 (upright — dispenser rises into hopper above?), then A5 to reveal any behavior change.
- If dead: try clicks on hopper frame/neck (31,18)/(31,19), or A2-from-BL (rotation past BL?), or yellow/green/red swatch behavior on hopper.

## After Actions 82-83 (A1 upright, dip)
- A1 upright: TOTAL no-op (0 diff). Dip: no change. Dispenser does not rise into hopper.
- NEW THEORY: hopper opening faces DOWN toward BLOCK (cols30-33 aligned with orange rect cols30-33!). Dispenser is IN THE WAY at rows24-32. Click-hopper (a80) ticked counter but no effect = drop blocked?
- TEST QUEUED: green swatch (47,4) [visible vs orange block top], A3+A2 (move dispenser to grounded-left, clearing the path), click hopper (31,20). Expect hopper contents to drop onto block cols30-33 top rows.

## After Actions 84-87 (green swatch, tilt, ground, click hopper)
- a84 green swatch: dispenser AND hopper body content -> green. Neck 2 cells stay white.
- a85/a86: HOPPER MOVES WITH DISPENSER (attached assembly!). 229-cell diffs. Now grounded-left: hopper at far left cols~13-15 rows36-41, green inside, no spill.
- a87 click (31,20) = empty space now: 0 diff. Earlier "counter tick" at a80 probably also meaningless.
- Hopper = capped BOTTLE on dispenser top: body 4x3, narrow neck 2-wide (white cells = neck interior?), '####' row18 = CAP. Pour requires opening cap and/or tipping past some angle?
- Block still: orange rows34-38, white rows39-43 (wait a79 dip made orange top5; a85-86 no dips). Actually block top-5 orange, bottom white; plus nothing green yet.
- Queued: A1,A4 (back to upright), click cap (31,18), click neck (31,19). If cap opens (visible diff), then tilt/rotate to pour.
- Fallback probes: A2 to BL saturation (pour at 135?), A5-dip pour interactions, RESET if paint lost.

## After Actions 88-91 — HOPPER STAMP FOUND
- a90 click CAP (31,18) with assembly upright => hopper stamps its 4x3 body onto block cols30-33 rows34-36 (current color). Not consumed. Neck click (31,19) = nothing.
- OP SET now: U rows34-38; L {x+y<=70}; R {y-x<=7}; GL cols27-31; GR cols32-36; BL {y-x>=7}; BR {x+y>=70}; H rect(30-33,34-36). 7 colors.
- L3 WIN (simulated, 0 mismatches; card cross-checked): green BR dip -> red GL dip -> purple 45L dip -> orange H stamp.
- QUEUED (17): A4,A2,A2,A5 [green BR]; A1,A1,A3,A3,A2, red(53,4), A5 [red GL]; A1, purple(29,4), A5 [purple 45L]; A4, orange(35,4), A6(31,18) [orange stamp]. Expect Score 3.

## LEVEL 3 SOLVED (Action 108, Score: 3). Counter reset for L4.

## Level 4 (initial, after a108) + plan
- Same assembly. CARD: blue cols27-31 minus yellow rect(cols27-29,rows37-40); orange {x>=32,x+y<=69}; purple {x>=32,x+y>=70}.
- Yellow rect = hopper footprint when GROUNDED-LEFT (interior cols13-15 rows37-40 -> stamps right onto block cols27-29 rows37-40). Cap grounded-left = col11 rows37-40, click (11,38). (Upright cap click was (31,18).)
- Sim 0 mismatches: orange GR dip -> purple BR dip -> blue GL dip -> yellow grounded-left stamp.
- QUEUED (16): orange(35,4),A4,A2,A5; A2,purple(29,4),A5; A1,A1,A3,A3,A2,blue(59,4),A5; yellow(41,4),A6(11,38). Expect Score 4.
- RISK: grounded cap-click stamp untested; if inert, block = target minus yellow rect; probe then.

## Level 5 (after a124, Score 4) — plan
Card decode (4 layers, sim verified 0 mismatches):
1. blue base everywhere (blue GR dip + blue GL dip)
2. green BL dip {y-x>=7}
3. orange BR dip {x+y>=70}
4. red upright cap stamp (cols30-33, rows34-36)
Blue leftover = card's 8 blue cells: (28,34),(29,34),(29,35),(34,34),(35,34),(34,35),(31,37),(32,37).
Ordering: blue before green (GL/GR overwrite BL cells); green before orange (BR covers BL spill); red stamp last, disjoint.

Batch 1 (20 actions, written a125): blue(59,4), A4, A2, A5 [GR]; A1, A3, A3, A2, A5 [GL]; A2, green(47,4), A5 [BL]; A1, A1, A4, A4, A2, A2, orange(35,4), A5 [BR].
Batch 2 (5 actions, NEXT CALL): A1, A1, A3 [BR->upright], red(53,4), A6(31,18) [stamp]. Expect Score 5.

## LEVEL 5 SOLVED (Action 149, Score: 5)
Batch 2 tail worked exactly as planned. Total 25 actions for L5.

## Level 6 (after a149, Score 5) — plan
Block starts all white; assembly upright, purple. Card decode (sim 0 mismatches), uses white base:
1. green GR dip {x>=32}
2. red L dip {x+y<=70} (overwrites green on diagonal)
3. purple upright cap stamp (cols30-33 rows34-36)
4. yellow grounded-left cap stamp (cols27-29 rows37-40)
White leftover = {u+v>=10, u<=4} triangle — never painted.
16-action queue (a150): green(47,4), A4, A2, A5 [GR]; A1, A3, A3, red(53,4), A5 [L]; A4, purple(29,4), A6(31,18) [stamp]; A3, A2, yellow(41,4), A6(11,38) [GL stamp]. Expect Score 6.
