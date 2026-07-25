## L7 ENDGAME SUBMITTED (after a524)
a507-524 executed exactly. blk (20,49), t=22, pat R0 red, ring2 (22,31) used.
MOVER PHASE PROVEN H1: n_ticks = 23 + s (s = moves since a506); blocked no-ops a482-483 did NOT tick. Sightings: s11 ctr32, s17 ctr12, s18 ctr17 all match.
SUBMITTED a525-544 (20 acts): R(20,54)=TOUCH1 cw [mover tile20], D(25,54)=TOUCH2 cw2 -> pat 101/110/011 RED = TARGET, L(25,49) exit, D,D,D,D,D=(50,49), R(50,54)=SE RING(t6->42), L,U,U,U=(35,49), L,L=(35,39), U(30,39)=F2 RIDE->(30,29), D,D,D,D=(50,29) COVER => expect SCORE 7 / level clear.
If touch fails (pattern wrong after s20): abort chain mentally, re-derive mover phase from boards; rings left (7,11),(7,41),(7,51).

## L7 EAST TRIP SUBMITTED (after a506)
a493-506 all executed: pattern = R0 (110/011/101) RED. Chamber ring used (a498). blk (40,9), t=26.
Remaining: cw x2 (east mover) + cover (50,29). Target cw2(R0)=101/110/011 red.
TILE MAP (rows 5-50 x cols 9-54, W=wall): saved l7tiles.pkl
  5 .....W.W..
 10 ...W...W..
 15 ...WW.WW..
 20 .WWW...W..
 25 .......W..
 30 .WWW...W..
 35 ...W.W....
 40 ...W.W....
 45 W.WW.WWW.W
 50 WWWW.WW...
East corridor cols 49/54 ONLY reachable via F1 ride (20,39)->(40,39). Return west ONLY via F2 ride (30,39)->(30,29). Cover (50,29) only via (45,29) from (40,29). (45,54)=W: SE ring (50,54) via (45,49),(50,49).
SUBMITTED a507-524 (18 acts) from (40,9) t26: U,U,U,R,R,R,R,U=(20,29)RING2(t42),D,R,R,U=(20,39)F1 RIDE->(40,39),R,U=(35,44),R=(35,49),U,U,U=(20,49). End t~22.
MOVER PHASE: n_ticks=23+s (H1, no-ops did not tick) or 25+s (H2). cycle tiles [10,15,20,25,30,25,20,15,10,5], idx=n%10. At end (s=18): H1 tile15 down, H2 tile25 down. OBSERVE mover in s15-18 boards to pin phase.
NEXT CALL touch plan (from (20,49), t~22):
 H1: R(20,54)=TOUCH1(mover tile20), D(25,54)=TOUCH2(tile25), L(25,49) exit. Then D,D,D,D=(45,49),D(50,49),R(50,54)=SE RING(t42),L,U,U,U=(35,49),L(35,44),L(35,39),U(30,39)=F2 RIDE->(30,29),D,D,D,D=(50,29) COVER = WIN.
 H2: R(20,54) miss(tile30), D(25,54)=TOUCH1(tile25 up), U(20,54)=TOUCH2(tile20), L(20,49) exit (NOT U: tile15 would touch3), then D x7 col49 to (50,49), R ring, then same return.
Rings left after this: (7,11),(7,41),(7,51) + SE (50,54) planned.

## L7 POCKET OPS PROVEN (after a492)
a489-492 executed: blk (30,9)->(35,9)->(40,9)->(40,14)->(40,19), t=20.
- WHEEL COVER (40,9) = COLOR CYCLE: orange - -> blue f (a490). Cycle I->n->- ->f->I. Need n(red): 2 more covers (f->I->n).
- BLOB TOUCH (40,19) = g: S0 -> U0 (a492). Need g5 total: 4 more touches -> R0=110/011/101.
- Target final: cw2(R0)=101/110/011 RED at cover (50,29). cw x2 via east mover.
SUBMITTED a493-506 (14 acts) from (40,19) t20:
L,R(touch2),L,R(touch3),L,D(45,14)=CHAMBER RING t->42,U,R(touch4),L,R(touch5=R0),L,L(40,9)=cover2 f->I,U(35,9),D(40,9)=cover3 I->n RED.
Expect end: blk (40,9), pat R0 red, t~26-28, chamber ring used.
NEXT: verify, then east trip: exit U,U to (30,9), route east to mover col 56 for cw x2 (VERIFY every tile: r10c24=W! use rows 5-9 or southern shelf), rings (22,31),(7,41),(7,51),(52,56),(7,11) still available. Then cover (50,29).

## RESUBMIT NOTE (call after a488, 2nd)
Runner called again WITHOUT executing prior batch (log still ends a488, blk (30,9), t=28, S0 orange). actions.json still held old batch. Rewrote identical batch: D(35,9), D(40,9)=WHEEL COVER#1, R(40,14), R(40,19)=BLOB TOUCH#1. Expect end t=20. Next call: read pattern after wheel cover (color op?) and blob touch (shape op, hope g).

# ===== L7 UPDATE (after a488) — POCKET OPEN! ENTRANCE = WEST COLUMN (COL 9-13) =====
# a484-488 exact incl. (30,9) TEST = STANDABLE. Rows 30-34 cols 9-13 full floor (border reading
#   was wrong; west wall is vertical q at cols 4-8). POCKET ROUTE: (25,9)->(30,9)->(35,9)->pocket.
# COLOR WHEEL (full): rows 41-43 cols 10-12, center (42,11)=$ white. Clockwise from N:
#   I,I,n,n,-,-,f,f (green green red red orange orange blue blue). Cover via tile (40,9).
# TILE MAP ADDITIONS: (30,9) F, (35,9) F, (40,9) F(wheel), (40,14) F, (40,19) F($ blob),
#   (35,14) F, (35,19) F, (45,14) F(chamber ring (47,16)).
# STATE: blk (30,9) t28, pattern S0 ORANGE, attempt 2, all rings live.
# SUBMITTED a489-492: D(35,9), D(40,9)=WHEEL COVER #1 (observe color change), R(40,14),
#   R(40,19)=$ BLOB TOUCH #1 (observe shape op). Ends t=20 at (40,19).
# NEXT CALL: deduce wheel mechanism (need orange->red; L6 cycle would be -»f»I»n = 3 covers) and
#   blob op (need g; if g: 5 total). Then: chamber ring (47,16) via L(40,14),D(45,14) when timer
#   low; east trip for cw x2 (mover col 56; phase re-derive: init 12 dn at attempt start, no-op
#   ticking unknown); finally cover (50,29) with cw2(g5(S0)) RED = 101/110/011.
# ===== L7 UPDATE (after a483) — TIMER DEATH & RESET (MY BLUNDER), ATTEMPT 2 BEGINS =====
# a471-483: F3 ride OK ((30,34)->(10,34)) BUT route L x5 hit WALL tile (10,24) (was in my own
#   tile map!) -> 4 blocked no-ops -> t hit 0 at a480 -> LEVEL RESET at a481. a482-483 blocked D
#   no-ops (-4t). NOW: blk (15,19)=start, t=38, score 6 intact, pattern S0 ORANGE, ALL RINGS
#   RESTORED ((7,11),(7,41),(7,51),(22,31),(47,16)). LESSON: simulate EVERY tile vs tile map
#   before submitting; west crossing rows must use row 5-9 (r10 c24 = W!).
# EAST MOVER INIT STATE (derived): center 12 dir DOWN at level start; no-ops freeze it (verify).
# STILL NEEDED: pocket entrance (unknown!), $ blob op test, color wheel test, then:
#   net cw2 (east mover 2 touches), g x5 ($ blob?), color orange->red, cover (50,29).
# SUBMITTED a484-488: L(15,14) L(15,9) D(20,9) D(25,9)=SW VANTAGE, D=(30,9) ENTRY TEST
#   (tile (30,9) has 3 suspected border cells - if floor, opens NW pocket route via (35,9)?).
#   Ends t>=28; ring (7,11) 4-5 mv away - safe margin.
# NEXT CALL: read SW reveal (rows 30-44 cols 4-13), determine pocket entrance, then full
#   route plan: pocket ops -> east mover cw x2 -> color red -> panel (50,29).
# ===== L7 UPDATE (after a470) — COLOR WHEEL SIGHTED; TIMER ESCAPE VIA F3 RIDE =====
# a470: blk (40,29) t20. Color structure = likely 3x3 COLOR TILE/wheel rows 41-43 cols 10-12,
#   center (42,11)='$' white (L6-style tile center!), around it: (41,11)I,(41,12)I,(42,12)n,
#   (43,12)n,(43,11)'-'; cols 10 cells fogged. Cover to cycle color? (L6: I->n->'-'->f).
# $ blob (41,20),(42,21),(42,22),(43,21) confirmed full shape (4 cells, diagonal): op unknown.
# POCKET ENTRANCE still not found: channel cols 9-13 narrows 5->4->3 wide rows 30-34 (border
#   diagonal kills (33,9),(34,10)); pocket may extend west cols<=10 rows 35-44 under fog.
# TIMER CRUNCH SOLVED: direct walk to NW ring = 11 mv > 10 available. Instead:
# SUBMITTED a471-483 (13 mv): U(35,29) U(30,29) R(30,34)=F3 TRIGGER ride UP -> lands (10,34),
#   then L x5 -> (10,9), U(5,9)=NW RING (7,11) t=2->42, then D x4 -> (25,9) t=34.
#   (25,9) vantage: reveals rows 35-44 cols 4-13 SW fog = hunt pocket entrance.
# NEXT CALL: verify ride landing + ring; study SW reveal; plan pocket entry ($ blob touch via
#   (40,19), color wheel cover via (40,9)?, chamber ring (47,16)); then panel (50,29).
# ===== L7 UPDATE (after a469) — WEST POCKET SEEN: STATIC $ BLOB, COLOR CELLS, 5TH RING =====
# a460-469 exact (F2 ride a468 (30,39)->(30,29) worked). Blk (35,29) t22. Pattern cw2(S0) orange.
# WEST POCKET (rows 35-44, cols 11-23 floor; may extend west into fog):
#   - $ blob cells (41,20),(42,21),(42,22),(43,21) - STATIC across a468-469 (and matches a444
#     snapshot). NOT a patroller. Touch via tile (40,19) (covers all cells) if reachable.
#   - COLOR cells col 12: (41,12)=I green, (42,12)=n red, (43,12)=n red; cols 11,13 fogged.
#     Possibly 3x3 color tile rows 41-43 cols 11-13, or color-picker strip.
#   - RING #5 at (47,16), chamber rows 45-49 cols 14-18 (tile (45,14)), connects up to pocket
#     col-14 corridor: tiles (35,14),(40,14),(45,14).
#   - POCKET ACCESS UNKNOWN: north wall rows 30-34 cols 14-28; cols 12-13 channel only 2 wide;
#     east wall cols 24-28 rows 35-56; border cuts tile (30,9) ((33,9),(34,9),(34,10) likely q).
#     Likely entrance from SW fog (rows 45-59 cols 4-20 unexplored; rows 35-44 cols<=10 fog).
# RINGS: (7,11) NW, (52,56) SE, (47,16) pocket-chamber. Needs: g x5 + orange->red + cover (50,29).
# SUBMITTED a470: D -> (40,29) t20. Window center (41.5,30.5) reveals: color structure fully
#   ((42,11) d2=380.5<400), ring chamber, SW fog rows 45-55 cols 9-20.
# NEXT CALL: find pocket entrance in reveal; identify color mechanism; plan g-touches ($ blob op
#   unknown - test by covering (40,19) once inside). Panel cover = D,D from (40,29)->(50,29) when
#   pattern ready.
# ===== L7 UPDATE (after a459) — CW2 DONE, RING 2 USED, HEADING WEST =====
# a455-459 exact: TOUCH2 (pattern -> cw2(S0) = 111/010/010 ORANGE ✓), ring (7,51) consumed
#   a459 t=42. Blk (5,49). East mover: center 12 dir down at a459 (patrol 7..32 period 10).
# EAST ROOM EXITS: cols 44-48 rows 5-29 = WALL; only exit south via rows 35-39 (cols 44-48 floor
#   rows 35-44). F2 trigger (30,39) rides west -> (30,29).
# REMAINING NEEDS: 5x g + color orange->red, then cover (50,29). Rings left: (7,11) NW, (52,56) SE.
# SUBMITTED a460-469 (10 mv): D x6 -> (35,49), L (35,44), L (35,39), U (30,39)=F2 ride -> (30,29),
#   D (35,29). Ends t=22 at (35,29) - recon spot: window covers west mover corridor (rows 35-44
#   cols 21-23), pocket (35,13-23), panel, rows 45-48 west of panel.
# NEXT CALL: observe west mover shape/patrol; find color tile; plan g x5 + color + cover D,D,D
#   (40,29),(45,29),(50,29)=COVER. Timer: t22 after; if ops need more, nearest ring (52,56) ~9mv.
# ===== L7 UPDATE (after a454) — EAST MOVER OP = CW ROTATION (PROVEN) =====
# a454: D->(25,54) TOUCH #1 worked. Pattern S0 010/010/111 -> 100/111/100 = cw(S0), still ORANGE.
# EAST MOVER = CW SOURCE. Touch = co-locate block tile with mover tile (landing as it arrives OK).
# Mover pinned at center 27 under block (25,54), releases UP. t18.
# ALGEBRA: target cw2(R0) = cw2(g5(S0)). Have cw1. Need net: +1 cw (a=2 mod 4), 5x g, color
#   orange->red. g source unproven -> likely WEST MOVER (~(42,21), corridor cols 21-23 rows 35-44).
#   Color source unknown (roaming tile in unexplored SW pockets? rows 35-48 west).
# SUBMITTED a455-459: U(20,54)=TOUCH2 (mover 27->22 same tile; pattern -> cw2(S0)=001/111/100?
#   [cw2(S0)=rot180(S0)=111/010/010]), L(20,49) break lockstep, U(15,49), U(10,49),
#   U(5,49)=RING(7,51) t42. Mover phases: 22(pin),17,12,7,12 - no accidental collisions checked.
# NEXT CALL: verify pattern=cw2(S0)=111/010/010 orange, t42. Then route west to probe west mover:
#   from (5,49): D,D,D->(20,49)? then west via rows 25-29 (all floor cols 9-43): e.g. D(25,49),
#   L,L,L... toward (25,19)/(30,19) then down to west corridor rows 35-44 cols ~19-23.
#   Watch new window reveals for color tile. Rings left: (7,11),(52,56).
# ===== L7 UPDATE (after a453) — TRUE MOVER MODEL: FIXED PATROL 7..32 PERIOD 10 =====
# a453: D->(20,54) t20. Mover seen at 32. RETRACT fog-freeze/fog-bounce theories.
# *** PROVEN MODEL (fits every sighting+non-sighting a435-453): mover patrols col 56, center row
#   7<->32, 5/eff-move, period 10, bounces at 7 and 32, ALWAYS ticks on effective moves (fan ride
#   = exactly 1 tick). Fog does NOT affect it. ***
# *** VISIBILITY (display only): cell visible iff dist((r,c),(br+1.5,bc+1.5)) < 20 (circle r2<400).
# Phase (d = eff moves after a453; mover 32, dir up): center = [32,27,22,17,12,7,12,17,22,27][d mod 10]
#   tile = (center-2, 54).
# SUBMITTED a454: D -> block (25,54) lands as mover arrives tile (25,54) (center 27) = TOUCH #1.
# IF touch works + op useful: LOCKSTEP CHAIN available: U,U,U,U from (25,54) co-locates every step
#   (mover up 5/tick): touches at 22,17,12,7 -> 5 total ops in 5 moves; then L->(5,49)=ring (7,51)
#   t42. [If op=g: 5xg = S0->R0; still need cw2 + orange->red. cw/color source unknown - west mover
#   at ~(42,21) corridor cols 21-23 rows 35-44? probe later.]
# NEXT CALL: read pattern display (S0 010/010/111 orange now). Deduce op from change.
# ===== L7 UPDATE (after a452) — VISIBILITY-GATED TICKS DISCOVERED; TOUCH RETRY (1 MOVE) =====
# a450-452 executed; intercept MISSED (mover was at 27 not 17). Pattern still S0 orange. Blk
#   (15,54) t22. Mover center 27 (tile (25,54)), next dir UP.
# *** NEW CORE RULE (perfect fit a436-452): mover bounce range rows 7<->27, PERIOD 8, ticks
#   5/eff-move ONLY when its pre-move cells are at least partly inside the visibility window
#   (block-centered +/-20); otherwise FROZEN (no tick). Fan ride = 1 tick. ***
#   Verified chain: a441:22dn, a442 frozen(unseen), a443:27, a444:22(ride), a445 frozen(22),
#   a446:17, a447:12, a448:7, a449:12(seen), a450:17, a451:22, a452:27.
# SUBMITTED a453: D -> block (20,54) lands exactly as mover bounces 27->22 = tile (20,54) = TOUCH.
# NEXT CALL: read pattern display (was 010/010/111 ORANGE). If op=g: S0->U0 (101/101/111).
#   Then: target = cw2(R0) = 101/110/011 RED at cover (50,29). Need net 5xg + cw2 + color->red.
#   Look for cw-op/color sources: west mover (~(42,21), corridor cols 21-23 rows 35-44), rings?
#   Pinned mover releases preserving direction (UP) when block leaves.
#   Timer t20 after touch; ring (7,51) tile (5,49) = L,U,U from (15,54)-ish; rings (7,11),(52,56).
# ===== L7 UPDATE (after a449) — MOVER CYCLE CRACKED (PERIOD 6), TOUCH PROBE SUBMITTED =====
# a445-449 exact. Blk (25,49) t28. Mover center (12,56) at a449, moving DOWN.
# MOVER CYCLE: bounces rows 7<->22 (NOT 27), period 6. Backfit a437-449 all consistent; a444 fan
#   ride ticked it exactly 1. Phase (d'=eff moves after a449): center = [12,7,12,17,22,17][d' mod 6],
#   dir: d'1=7(bounce) d'2=12 d'3=17 d'4=22(bounce) d'5=17. Mover tile = (center-2, 54).
# SUBMITTED a450-452: U(20,49) U(15,49) R(15,54) -> at d'3 block lands tile (15,54) = mover tile
#   (center 17) = TOUCH/PIN. Avoids ring (7,51) tile (5,49). t=22 after.
# NEXT CALL: check pattern display (was S0 010/010/111 ORANGE) -> deduce op. If op=g: need 5 g
#   total + cw2 + color->red for target cw2(R0)=101/110/011 RED at cover (50,29).
#   Consider lockstep touches (L6 style: walk in sync with released mover to chain ops).
#   Release preserves direction (L6 rule): mover under block released, resumes.
#   Timer plan: rings left (7,11),(7,51),(52,56). t22 = 11 moves; ring (7,51) is 2-3 moves from
#   (15,54) region: U(10,54) L?(no) -> (10,49)? ring tile (5,49): from (15,54): L(15,49) U(10,49)
#   U(5,49)=ring t42.
# ===== L7 UPDATE (after a444) — PANEL FOUND (RED 101/110/011), FAN RIDE PERFECT =====
# a442-444 exact: ring(22,31) t42, F1 ride (20,39)->(40,39) [17 frames]. t38 now, blk (40,39).
# PANEL at rows 48-56 cols 27-35: h-ring border, O interior cols 28-34 rows 49-55. TARGET cells
#   (51,30),(51,32),(52,30),(52,31),(53,31),(53,32) = 101/110/011 RED = cw2(R0).
#   COVER POSITION = block (50,29) [rows 50-54 cols 29-33, grid-aligned!].
# COVER ROUTE (from east corridor): U(35,39) U(30,39)=F2 trigger -> west ride -> lands (30,29)
#   [obstruction wall (30,24)+; F3 trigger (30,34) ignored mid-ride], then D(35,29) D(40,29)
#   D(45,29) D(50,29)=COVER. 6 moves. ONLY do when pattern = red 101/110/011.
# SHAPE ALGEBRA: S0 --5xg--> R0, +cw2. Need ops: east mover touch =? (probe!), color orange->red
#   (L6 tile cycle -: ->f->I->n = 3 touches if same cycle; color mechanism unknown on L7).
# WEST MOVER? white $ at (42,21),(42,22),(43,21) partial in fog, west corridor cols 21-23
#   rows 35-44. Different shape than east mover? Investigate later if needed.
# SE ROOM rows 50-54 cols 44-59: floor + RING center ~(52,56). Access via (40,44)->(40,49)->
#   (45,49)->(50,49)->(50,54). Rings left: (7,11),(7,51),(52,56).
# EAST MOVER phase (d eff-moves after a441, period 8 IF ride ticked once): [22,27,22,17,12,7,12,17]
#   center row at d mod 8; tile = (center-2, 54). d=3 now -> center 17. VERIFY on approach (ride
#   may have ticked mover 1x or more - frames!).
# SUBMITTED a445-449: R(40,44) R(40,49) U(35,49) U(30,49) U(25,49). Ends (25,49) t28, d=8.
#   Window reveals east room + mover position -> pin down phase & touch semantics.
# NEXT CALL: verify mover phase; intercept (block tile = mover tile, col 54); observe op on
#   pattern display; then plan full op sequence + color + cover route. Timer: rings nearby.
# ===== L7 UPDATE (after a441) — SE/SOUTH MAPPED, EAST MOVER FOUND, FAN PROBE SUBMITTED =====
# a434-441 exact per plan. Block (20,34) t34. Ring (7,41) consumed a437 (t->42).
# EAST ROOM (rows 5-29, cols 50-59, border q at 60-61): ring (7,51) confirmed. MOVER: plus-shape
#   center $ with (r-1,c)=$ (r,c+1)=$ (r,c-1)=8 (r+1,c)=8; bounces vertically col 56, 5/eff-move.
#   Observed centers: a437 (12,56) a438 (7,56)[bounce top] a439 12 a440 17 a441 22 (going down).
#   Likely range rows 7-27, period 8. Phase from a441: d0=22 down, d1=27(bounce), d2=22, d3=17,
#   d4=12, d5=7(bounce), d6=12, d7=17. Probably this level's pattern-op sprite (like L6 g).
# FANS (all mounted on wall-tile edge, blow away, trigger=adjacent strip tile, mid-strip free,
#   rides ignore other fans):
#   F1 (19,39-43) bottom of wall (15,39), blows DOWN col-strip 39-43. Trigger (20,39).
#   F2 col 44 rows 30-34, left edge of wall (30,44), blows WEST row-strip 30-34. Trigger (30,39).
#   F3 row 35 cols 34-38, top of wall (35,34), blows UP col-strip 34-38. Trigger (30,34) - CAREFUL:
#     landing (30,34) blows block up to (10,34) (wall (5,34) stops).
# SOUTH: west corridor tiles (35,29),(40,29 partial); east corridor (35,39),(40,39)+fog below;
#   SE open area rows 35-39 cols 39-50, tiles (30,49),(35,44),(35,49). Fog: below row 41, and
#   rows 30+ east of col 51. NO PANEL FOUND YET -> must be deep south or SE fog.
# SUBMITTED a442-444: L(20,29)=RING(22,31) t42, R(20,34), R(20,39)=F1 TRIGGER -> ride down
#   col 39-43 to southernmost obstruction (past (25,39),(30,39)F2-trigger-ignored,(35,39),(40,39),
#   into fog). Lands deep south, window reveals bottom tip. Rings left: (7,11),(7,51).
# NEXT CALL: parse landing + reveal; find panel; plan pattern ops (mover touch semantics unknown;
#   current pattern S0 010/010/111 ORANGE). Return north options: F3 up-ride from (30,34).
# ===== L7 UPDATE (after a433) — FOG OF WAR CONFIRMED, WORLD MAP STARTED =====
# a430-433 executed exactly: block (15,19)->U(10,19)->U(5,19)->R(5,24)->R(5,29). t 42->34: TIMER
#   DRAIN = 2/ACTION on L7 (21 moves per full timer; ring refill 42 = 21 moves).
# FOG OF WAR: visible window ~ block center +/-20 rows, -20..+19 cols (clamped); 'O' = fog.
#   World coords ABSOLUTE (landmarks fixed). Composite world saved in l7world.pkl (merge non-O).
# TILE GRID: 5x5 tiles at rows 5+5k, cols 9+5k. 'h'=floor tile, 'q'=wall tile. Map is a DIAMOND
#   (borders cut tiles diagonally at edges; top border rows 0-4, left cols 4-8).
# TILE MAP (F=floor W=wall ?=fog), rows 5-35, cols 9-49:
#   r5 : F(ring@7,11) F F F F[blk now 5,29] W F(ring@7,41) W F(ring@7,51 partial)
#   r10: F F F W F F F W F?
#   r15: F F F W W F W(fan@19,39-43 bottom row) W ?
#   r20: F W W W F(ring@22,31) F F W? ?
#   r25: F F F F F F ? ? ?
#   r30: F(cut) W W W F(cut) ? ...
#   r35: F F(narrows row36 c17-23) W ...  south of row36 = unexplored
# ITEMS: rings (7,11),(7,41),(7,51),(22,31) [single-use refill t=42]. FAN at (19,39-43): mounted
#   under wall tile (15,39) facing DOWN -> trigger tile (20,39), ride down col 39-43 strip into
#   UNEXPLORED south (mid-strip tiles (5,39),(10,39) are free, no ride).
# NO movers seen (diffs a430-433 = fog edges only). Pattern S0 010/010/111 ORANGE. NO panel yet.
# UNEXPLORED: east of col ~50 (rows 5-30), south of row 36. Panel must be there.
# SUBMITTED a434-441: D(10,29) R(10,34) R(10,39) U(5,39)=RING t42, D(10,39) L(10,34) D(15,34)
#   D(20,34). Ends (20,34) t~34; window reveals rows<=41, cols 16-55 (southeast quadrant).
# NEXT CALL: parse reveal; if panel seen, plan route+pattern ops; consider fan ride R(20,39) to
#   probe south. Watch for surprise: if (10,39) triggered up-ride at a436, U at a437 was no-op
#   (still fine: ring covered on landing, t refilled, -2 for no-op).
# ============ LEVEL 7 (score 6, started a429; L6 won a429, L6 took a324-429) ============
# Block (15,19) t42. Pattern display bottom-left: S0=010/010/111 ORANGE.
# MAP (diamond, walkable rows 5-36 cols 9-40): row5-9: cols 9-33; rows10-14: 9-23 + 29-39/40;
#   rows15-19: 9-18 [blk at 19-23] + 34-38 + (19,39-40)='88'; rows20-24: 9-13 + 29-40;
#   rows25-29: 9-38; rows30-34: 9-13 + 29-35 narrowing; rows35-36: funnel 13-24 dead-ends row36.
# ITEMS: ring TL rows6-8 cols10-12 (cover (5,9)); ring2 rows21-23 cols30-32 (cover (20,29));
#   '88' 2-cell feature (19,39),(19,40) next to 2-wide chute rows9-14 cols39-40 (block can't fit
#   — NEW MECHANIC? maybe fan for a non-block entity).
# NO TARGET PANEL VISIBLE (right side all 'O'). Win condition unknown — maybe revealed later,
#   maybe display bottom-left is target here, maybe funnel/chute does something.
# NO other movers visible on first board. Block moves from (15,19): U ok, L ok, D wall, R wall.
# SUBMITTED a430-433: U(10,19) U(5,19) R(5,24) R(5,29). Recon: timer rate, hidden movers (diffs),
#   head toward right region. Route right: (5,29)->? (10,29)D? then (10,34) D (15,34) D (20,34)...
# L6 MECHANICS PLAYBOOK (likely reusable): movers move 5/eff-move ONLY on effective block moves
#   (no-ops freeze world but drain timer); pin under block preserves direction; lockstep chains;
#   sprite-op g 6-cycle P0->Q0->R0->S0->U0->V0 (cw-equivariant); patrol=cw rotation on cover;
#   tile roams + cycles color I->n->'-'->f on cover; rings single-use refill t42; fans strip-
#   trigger rides; panels consumed on covering with matching pattern (shape+color); score +1 only
#   when ALL panels done; win at t>=0 valid.
# ===== L6 UPDATE (after a420) — B2 PERFECT, B3 (WIN) SUBMITTED =====
# ROT1-3 a411-413 exact. Pattern = fOf/OOf/fff = 101/001/111 BLUE = TARGET2. Block (15,44) t13 d87.
# SUBMITTED a421-429 = B3 (d88-96): R(15,49) U(10,49) U(5,49)->down-fan ride->(25,49) R(25,54)
#   D(30,54) D(35,54) D(40,54) D(45,54) D(50,54) = COVER PANEL2 = WIN, t4, score -> 6.
# NEXT CALL: if score 6 -> L7 fresh parse (block, timer rate, panels/targets, movers: sprites may
#   patrol 5/eff-move with pin+direction-preserved release, tile may roam, rings single-use,
#   fans strip-trigger, no-ops freeze everything). L6 took a324-a429 ~106 actions.
# ===== L6 UPDATE (after a400) — B1 PERFECT, B2 SUBMITTED =====
# B1 all exact: g x4 (a386-389 -> cw2(Q0) red), TL ring a391 t42, TILE1 a399 red->orange,
#   TILE2 a400 orange->BLUE. Pattern fOf/fOO/fff (101/100/111 blue). Block (20,19) t33 = d67.
#   Tile pinned at p3=(22,21) under block; releases to p4=(22,26) at d68 (loop continues).
# SUBMITTED a401-420 = B2 (d68-87): D(25,19) L(25,14) L(25,9) D(30,9) D(35,9) D(40,9) D(45,9)
#   R(45,14) R(45,19) R(45,24) U(40,24)@d78 ROT1(26) R(40,29) ROT2(31) R(40,34) ROT3(36 bounce)
#   R(40,39)[release west 31 safe] U(35,39) U(30,39) U(25,39) U(20,39) U(15,39) R(15,44).
#   Expect: block (15,44) t13, pattern fOf/OOf/fff = 101/001/111 BLUE = TARGET2 shape+color.
# NEXT CALL: verify, then B3 (9 acts) d88-96: R(15,49) U(10,49)[s1 21 safe] U(5,49)->ride->(25,49)
#   R(25,54) D(30,54) D(35,54) D(40,54) D(45,54) D(50,54) = WIN2, t4. Score should hit 6.
# ===== L6 UPDATE (after a385) — ENDGAME LOCKED =====
# a379-385 perfect. g-touch#1 at a385: T -> 111/010/010 = cw2(S0). L6 op == L5 g EXACTLY.
# TARGET2 CORRECTED (was off-by-one): rows51-53 cols55-57 = 101/001/111 BLUE = cw(Q0). IN CLOSURE!
# Solution: from cw2(S0): g^4 -> cw2(Q0); cw^3 -> cw(Q0); tile x2 (red->orange->blue); cover (50,54).
# PIN RELEASE = DIRECTION PRESERVED (proven: patrol formula continuity across a342 pin d9-d10).
#   At bounce ends release direction forced. All locksteps deterministic.
# KEY GEOMETRY: block enters panel walls (panel1 precedent). Col 54 walkable rows 30-49 now.
#   Panel2 cover = (50,54) ⊇ pattern rows51-53 cols55-57. Approach: (25,54) D x5.
#   Only route to col 54: (15,39) R R (15,49) U (10,49) U (5,49) -> down-fan ride -> (25,49) -> R.
#   Row 40 crossings at cols 9,39 ALWAYS patrol-safe (patrol cells span cols 15-37).
# FULL PLAN d53-d96 (d=eff moves after a333; a385=d52; t26 now; TL ring d58 -> 42; win t=4):
#  B1 (SUBMITTED a386-400, 15 acts) d53-67: L(10,29)g2 L(10,24)g3 L(10,19)g4 L(10,14)g5
#    [sprite1 pinned@36 releases west, lockstep] L(10,9)[s1 releases east 21 safe] U(5,9)=TL RING t42
#    D(10,9) D(15,9) D(20,9) D(25,9) R(25,14) L(25,9) R(25,14) [+2 phase detour] R(25,19)@d66≡2
#    =TILE1(p2=(27,21)⊂blk; red->orange) U(20,19)@d67≡3 =TILE2(p3=(22,21)⊂blk; orange->BLUE).
#    Expect after B1: pattern fOf/fOO/fff (101/100/111 BLUE), block (20,19), t33.
#  B2 (NEXT CALL, 20 acts) d68-87: D(25,19)[p4 safe] L(25,14) L(25,9) D(30,9) D(35,9) D(40,9)
#    D(45,9) R(45,14) R(45,19) R(45,24) U(40,24)@d78≡6 ROT1(patrol 26 east) R(40,29)@79 ROT2(31)
#    R(40,34)@80 ROT3(36 bounce) R(40,39)@81[release west 31, SAFE] U(35,39) U(30,39) U(25,39)
#    U(20,39) U(15,39) R(15,44). Expect: pattern fOf/OOf/fff (101/001/111 BLUE = TARGET2), t13.
#  B3 (8 acts) d88-96: R(15,49) U(10,49)[s1@d89≡1=21 safe] U(5,49)->ride->(25,49) R(25,54)
#    D(30,54) D(35,54) D(40,54) D(45,54)[enters panel2 top wall] D(50,54) = WIN2 t4.
#    (B3 is 9 moves d88-d96: R,U,U,R,D,D,D,D,D.)
#  All tile/sprite1/patrol positions verified safe at every step (formulas in a333 section).
# NEXT CALL: verify B1 (pattern fOf/fOO/fff, block (20,19), t33). If tile touches misfired:
#   diagnose phase, redo pair; ~9 spare moves before margin gone. Then submit B2.
# ===== L6 UPDATE (after a378) — PANEL1 CONSUMED, PANEL2 REMAINS =====
# d27-d45 ALL PERFECT: tile touch a363 (pattern red T), TR ring a369 (t42), left... down-fan ride
#   a374->375 landed (25,49) as predicted, covered panel1 at (35,54) a378.
# PANEL1 CONSUMED on covering: whole structure rows34-41 cols53-59 -> walkable 'h'. Score STAYS 5
#   until ALL panels done (level clear = score+1). Panel1 area now open floor (new paths!).
# PANEL2 (rows49-55 cols53-59): target cells rows51-53 cols55-57 = 101/010/111 BLUE ('f').
#   Entry: (45,54)->D(50,54) covers rows50-54... wait pattern cells rows51-53 ⊂ block rows50-54 ✓.
#   NOT in L5-g closure => L6 sprite op g' LIKELY DIFFERENT — must probe.
#   Also color: red->blue = 2 tile touches (n->'-'->f).
# STATE a378=d45: block (35,54) t33 pattern nOn/nnO/Onn (red T). Phases (d after a333):
#   patrol [36,31,26,21,16,21,26,31][d%8]; sprite1 [16,21,26,31,36,31,26,21][d%8];
#   tile ctr [(32,26),(32,21),(27,21),(22,21),(22,26),(22,31),(27,31),(32,31)][d%8].
# SPRITE1 TOUCH pairs row10: (10,14)@s16 d≡0; (10,19)@s21 d≡1,7; (10,24)@s26 d≡2,6; (10,29)@s31
#   d≡3,5; (10,34)@s36 d≡4. TOUCH AT BOUNCE (d≡4, s36) => release dir known (west).
#   LOCKSTEP CHAIN: from (10,34)@d≡4, moving L each step touches AGAIN: (10,29)/31, (10,24)/26,
#   (10,19)/21, (10,14)/16 — up to 5 touches in a row!
# TILE touch pairs: (30,24)@ph0 (30,19)@ph1 (25,19)@ph2 (20,19)@ph3 (20,24)@ph4 (20,29)@ph5
#   (25,29)@ph6 (30,29)@ph7. RINGS: TL (5,9) UNUSED; BL+TR used this attempt.
# SUBMITTED a379-385 = d46-d52: U(30,54) U(25,54) L(25,49) U(20,49)->LEFT-FAN ride->(20,39)
#   U(15,39) U(10,39) L(10,34) = SPRITE1 TOUCH #1 (probe g'). t=26 after.
# NEXT CALL: pattern' = g'(red T)? Deduce op (compare vs L5 g: g(T)=cw2(S0)=111/010/010).
#   Then plan: find t,k with target2 reachable; maybe chain lockstep touches; +2 tile touches for
#   blue; then cover panel2 via (45,54) D(50,54). Timer: TL ring if needed.
# ===== L6 UPDATE (after a359) — ROAMER == TILE! =====
# d10-d26 perfect: block (25,39) t20 a359=d26. Pattern T but STILL GREEN — a355 tile touch MISSED:
#   the 'roamer' single white cell IS the tile's center pixel. The whole 3x3 TILE roams the
#   rectangle loop p(d) (centers): [(32,26),(32,21),(27,21),(22,21),(22,26),(22,31),(27,31),(32,31)][d%8].
#   Tile cells = rows r-1..r+1, cols c-1..c+1 around center. Original 'tile at 31-33' was phase-0 snapshot.
# TOUCH positions (block fully contains tile): (30,24)@ph0, (30,19)@ph1, (25,19)@ph2, (20,19)@ph3,
#   (20,24)@ph4, (20,29)@ph5, (25,29)@ph6, (30,29)@ph7.
# SUBMITTED a360-378 = d27-d45 (19 acts):
#   d27 U(20,39) d28 D(25,39) d29 L(25,34) d30 L(25,29) = TILE TOUCH ph6 (green->red)
#   d31 R(25,34) d32 R(25,39) d33 U(20,39) d34 U(15,39) d35 U(10,39) d36 U(5,39)=TR RING t->42
#   d37 D(10,39) d38 D(15,39) d39 R(15,44) d40 R(15,49) d41 U(10,49) d42 U(5,49)->down-fan
#   ride->(25,49) d43 R(25,54) d44 D(30,54) d45 D(35,54) = WIN1. t~33 at win.
#   All mover overlaps checked d27-d41; post-ride positions (col 54) safe vs ALL movers at ANY phase.
# NEXT CALL: score 6? If pattern didn't turn red at d30 (touch semantics wrong), t~33 remains:
#   redo touch via phase table above, then re-cover (35,54). If ride failed: block near (5,49)/(10,54);
#   replan walk. If score 6: L6 may continue (panel2 blue 101/010/111 not in closure) or new level.
# ===== L6 UPDATE (after a342) — ROT#2 DONE, pattern = T =====
# Batch1 perfect: ring a337 (t->42), ROT#2 at a342 (block (40,29) pinned patrol at 31).
#   Pattern = IOI/IIO/OII = T shape, green. Timer 37. All movers matched phase model exactly.
#   d-count: a342 = d9. Phase formulas unchanged (d = effective moves after a333).
# SUBMITTED a343-359 = d10-d26: D(45,29) L(45,24) R(45,29) R(45,34) R(45,39) U(40,39) U(35,39)
#   U(30,39) U(25,39) L(25,34) L(25,29) L(25,24) D(30,24)=TILE(green->red => target1 complete
#   pattern) U(25,24) R(25,29) R(25,34) R(25,39). Expect t=20, block (25,39), pattern IOI/IIO/OII red (n).
# NEXT CALL: verify pattern red T, no accidental rotations (patrol release branch W or E both
#   checked safe). Then FINAL batch d27-d35 (9): U(20,39) U(15,39) R(15,44) R(15,49) U(10,49)
#   U(5,49)->down-fan ride->(25,49) R(25,54) D(30,54) D(35,54) = WIN1. Sprite1 check at d31 (10,49):
#   sprite1 idx7=21 safe. If ride lands elsewhere: replan from actual, t~14 margin.
# AFTER WIN1: investigate — score 6? new level? or L6 continues needing panel2 (101/010/111 BLUE,
#   NOT in 24-state closure -> tile may have more colors or win1 changes pattern).
# ===== L6 UPDATE (after a333) — FULL ROUTE LOCKED =====
# a330-333 = L,U,U,U perfect: block (25,9) t32. NO rot#2: patrol resumed EASTBOUND from 16
#   (16 = natural west bounce). PATROL range 16<->36 period 8. SPRITE1 range 16<->36 period 8
#   (bounced at 36, back to 16 at a333). ROAMER = fixed CW rectangle period 8.
# PHASE MODEL (d = effective moves after a333; NO-OPS DON'T COUNT):
#   patrol col(d)=[36,31,26,21,16,21,26,31][d%8]  (cells rows41-43, cols c-1..c+1)
#   sprite1 col(d)=[16,21,26,31,36,31,26,21][d%8] (rows 11-13)
#   roamer p(d)=[(32,26),(32,21),(27,21),(22,21),(22,26),(22,31),(27,31),(32,31)][d%8]
# SAFE CROSSINGS: block (40,9) & (40,39) NEVER overlap patrol (cells span 15-37 only).
#   Sprite1 only threatens block at row 10 (covers rows10-14). Roamer rows 22-32 cols 21-31.
# ROT#2 INTERCEPT: land (40,29) at d=9 when patrol=31 (cells 30-32 in block cols 29-33).
#   Robust: after pin, whether sprite releases W or E, only later row-40 landing is (40,39)=always safe.
# FULL 35-MOVE ROUTE (verified vs all 3 movers, both release branches):
#   d1-d4: D(30,9) D(35,9) D(40,9) D(45,9)=BL RING t->42
#   d5-d8: R(45,14) R(45,19) R(45,24) R(45,29)
#   d9: U(40,29) = ROT#2 -> pattern T (101/110/011) still green   <== BATCH 1 ENDS (submitted a334-342)
#   d10-d14: D(45,29) L(45,24) R(45,29) R(45,34) R(45,39)   [L/R shuffle = +2 phase to dodge roamer]
#   d15-d18: U(40,39)[safe] U(35,39) U(30,39) U(25,39)
#   d19-d21: L(25,34) L(25,29) L(25,24)
#   d22: D(30,24) = TILE green->red
#   d23-d26: U(25,24) R(25,29) R(25,34) R(25,39)
#   d27-d28: U(20,39) U(15,39)
#   d29-d32: R(15,44) R(15,49) U(10,49) U(5,49) -> top-fan DOWN ride -> lands (25,49) [strip=rows5-9
#     cols49-53 verified grid-aligned; obstruction rows30+ cols49-53]
#   d33-d35: R(25,54) D(30,54) D(35,54) = WIN1 (covers pattern rows36-38 cols55-57)
#   Timer: refill 42 at d4, win at d35 with 11 left.
# SUBMITTED a334-342 = batch1 (d1-d9): D D D D R R R R U.
# NEXT CALL: verify pattern==T (IOI/IIO/OII), timer==37, block (40,29), patrol hidden(pinned 31).
#   If good: submit d10-d26 (17 actions), then final batch d27-d35 (9). If rot missed: recompute
#   patrol phase from diffs, re-intercept via row-45 approach (U into (40,c) when patrol c under block).
# ===== L6 UPDATE (after a329) =====
# a328-329 blocked-U no-ops: timer drained (38->36) but ALL SPRITES FROZE. => SPRITES MOVE ONLY ON
#   EFFECTIVE BLOCK MOVES. Waiting is useless; every sprite step costs us an effective move.
# SPRITE1 (skew rows 11-13) ALSO PATROLS: center 16(a323)->21->26->31->36(a327) eastbound 5/act.
#   Corridor rows 10-14 cols 9-43 -> range likely 11<->41. Touch positions now MOVING targets.
# PATROL corridor rows 41-43 walkable cols 9-43 -> centers 11..41. Sprite pinned under block at
#   c16, was westbound. Cover pairs row40: (40,c-2)<->center c.
# THIRD MOVER: single white cell (32,26)a323->(32,21)->(27,21)->(22,21)->(22,26)a327, 5 cells/act,
#   turns unpredictably. Frozen at (22,26). Role unknown — WATCH each call, avoid co-location.
# Pattern still cw(R0)=101/011/110 green. Need: rot#2 (->T) + 1 tile touch (green->red).
# SUBMITTED a330-333: L(40,9) U(35,9) U(30,9) U(25,9).
#   a330: if patrol resumes WESTBOUND -> c11 under block(40,9) -> ROT#2 -> pattern T (check!).
#     If EASTBOUND/bounce16 -> c21 visible, no rot; track phase (5/eff-move) for later intercept.
#   a331+: block leaves patrol rows; sprite free-runs 1 step per our move. Sprite1 & roamer also step.
# NEXT CALL: read pattern + all three movers' positions. If T: continue R(25,14) R(25,19) R(25,24)
#   D(30,24)=TILE(green->red), then win1 route U(25,24) R x3 to (25,39) U(20,39) U(15,39) R(15,44)
#   R(15,49) U(10,49) U(5,49)->top-fan down ride->(25,49)? [offset unverified] R(25,54) D(30,54)
#   D(35,54)=WIN1. ~14 moves after tile; timer fits (36-4-4-14=14). If no rot#2: compute patrol
#   phase, plan return through row 40: co-locate block landing with sprite center (block c = center-2).
# ===== L6 UPDATE (after a327, prior call) =====
# a324-327 executed perfectly: block (50,24)->L(50,19)->L(50,14)->U(45,14)->U(40,14). Timer 42->38
#   => RATE = 1/action (cheaper than L5's 2!). 42 budget = 42 actions per attempt.
# PATROL walk observed: col 36(a323)->31->26->21->16(a327). 5 cols per action, WESTBOUND.
# ACCIDENTAL CW#1 at a327: block landed (40,14) same action sprite reached c16 (cover pair
#   (40,14)<->c16 here, row 40 not 35!). Pattern now 101/011/110 = cw(R0) = ccw(T). GOOD: need
#   exactly 1 more cw + 1 tile touch (green->red) for target1. Cover pairs row40:
#   (40,14)<->c16, (40,19)<->c21, (40,24)<->c26, (40,29)<->c31, (40,34)<->c36, (40,39)<->c41.
# WEST BOUNCE UNKNOWN (11 or 16). SUBMITTED a328-329: U,U = blocked no-ops at (40,14) (rows 35-39
#   cols 14-18 are walls 'q') — safe waits, sprite hidden under block now.
#   Scenario A (bounce 11): a328 c11, a329 c16 = OVERLAP = CW#2 -> pattern T! Then sprite departs
#     east; a330 exit L(40,9) safe, run tile+win1.
#   Scenario B (bounce 16): a328 c21, a329 c26 eastbound, no rotation. Then intercept returning
#     westbound: need block at (40,19) when sprite hits c21 or (40,24) at c26 — but east bounce
#     unknown too (36 or 41). Plan B: read positions a329, compute phase, time one R-step intercept.
# NEXT CALL DECISION: pattern==T after a329? -> Scenario A confirmed: L(40,9) U(35,9) U(30,9)
#   U(25,9) R(25,14) R(25,19) R(25,24) D(30,24)=TILE(->red) U(25,24) R(25,29) R(25,34) R(25,39)
#   U(20,39) U(15,39) R(15,44) R(15,49) U(10,49) U(5,49) -> top-fan DOWN ride -> (25,49)?
#   [fan cols 50-54 vs block 49-53 offset UNVERIFIED] R(25,54) D(30,54) D(35,54)=WIN1.
#   Timer check: a330 t36 -> ~22 moves -> t~14 at win. OK. Else Scenario B: phase-timed intercept.
# ============ LEVEL 6 (score 5, started a323; L5 won a323 total 117 actions on L5) ============
# Block start (50,24). Timer 42 rate UNKNOWN (measure a324-325). Pattern start: 110/011/101 GREEN = R0!
# TWO TARGET PANELS:
#   panel1 rows 34-41 cols 52-60, pattern rows 36-38 cols 55-57 = 101/110/011 RED (=T=cw^2(R0), same as L5!)
#     win1 entry: (30,54) then D -> (35,54) covers pattern.
#   panel2 rows 48-56 cols 52-60, pattern rows 51-53 cols 55-57 = 101/010/111 BLUE
#     win2 entry: (45,54) then D -> (50,54). NOTE: 101/010/111 NOT in {cw^k(g^t)} closure of R0's
#     6-cycle (checked all 24) -> mystery; maybe win1 changes pattern, or L6 g differs, or only 1 needed.
# ITEMS: sprite1 skew (11,15),(12,16),(12,17),(13,16) cover (10,14) [same shape as L5 -> op g].
#   PATROL sprite rows 41-43, white (41,37),(42,36),(42,37)+8(42,35),(43,36) center col36 @a323;
#     patrol path/range UNKNOWN — L5 was 16<->26 period4; here maybe 31<->41. OBSERVE before
#     crossing rows 40-44 near cols 28-44! Covers: (40,29)|c31, (40,34)|c36, (40,39)|c41.
#   TILE fII/f\$n/--n rows 31-33 cols 26-28, cover (30,24). green->red = 1 touch (I->n).
#   RINGS: TL cover (5,9), TR cover (5,39), BL cover (45,9).
#   FANS: (4,50-54) DOWN over right region rows 5-14 cols 49-58; (20-24,55) LEFT rows 20-24
#     cols 39-53, strip (20,49) -> rides to (20,39).
# WALK BANDS (block r: cols c on c=4mod5): r5,r10: 9-39 + 49,54; r15: 9 + 39,44,49; r20: 9 + 19,24,29
#   + 39,44,49[strip]; r25: 9-39 + 49,54; r30: 9,19,24,29,39 + 54; r35: 9,39; r40: 9-39 (patrol rows!)
#   + 54(rows42-46? col54-58 h rows 42-47); r45: 9-39 + 54(->rows45-49 incl panel2 border risk);
#   r50: 14,19,24,29,34.
# PLAN-1 (target1): tile route (50,24): U45,24 U40,24?? NO - use left: L,L to (50,14), U(45,14),
#   U(40,14) [safe if patrol >= col30], L(40,9) U(35,9) U(30,9) U(25,9) R(25,14) R(25,19) R(25,24)
#   D(30,24)=TILE red. Then cw^2 via patrol (phase!), then (25,x)->(25,54) D(30,54) D(35,54)=WIN1.
# SUBMITTED a324-327: L(50,19) L(50,14) U(45,14) U(40,14). Measure timer rate + 4 patrol samples.
# a300-319: ALL PERFECT. Pattern = TARGET 101/110/011 RED since a310 (double patrol-intercept
#   worked exactly as phased). At (50,39) t30. SUBMITTED a320-323: R(50,44) R(50,49)
#   R(50,54)->up-fan ride col 54 -> should rest (5,54) covering pattern rows6-8 cols55-57 = WIN
#   (score 4->5). Spare U if block rests below panel. If score=5 next call: parse NEW LEVEL 6 fresh
#   (find block, timer rate, panel, target, sprites/tiles/rings/fans; remember: sprites may PATROL,
#   ops may be nonlinear cycles, strip-trigger fans, rings single-use, timer-0 win valid).
# ===== SOLUTION LOCKED (a299) =====
# g = 6-CYCLE: P0=010/110/011 -> Q0=111/001/101 -> R0=110/011/101 -> S0=010/010/111 ->
#   U0=101/101/111 -> V0=011/101/010 -> P0. T=cw^2(R0). Reachable w/ 1 cw = cycle+cw(cycle): NO T.
# SPRITE2 = PATROLLING + REUSABLE (never was single-use!): white cells oscillate col 16->21->26->21,
#   period 4, anchor RESET: col(a)=[16,21,26,21][(a-265)%4] (attempt1 anchor: (a-206)%4).
#   Rotation cw applied when settled block covers sprite (a238 proof). Cover positions:
#   (35,14)<->col16, (35,19)<->col21, (35,24)<->col26. No partial overlaps at grid positions.
# PLAN (a300-a319 submitted, pattern P0 now, at ringB t42):
#   a300 R(10,14) a301 R(10,19)=g1->Q0 a302 L a303 R=g2->R0; a304-305 D,D col19; a306 D(25,19)
#   ->leftfan ride (25,9) [UNVERIFIED ride; if fails: wander harmless rows25, replan]; a307 D(30,9)
#   a308 D(35,9); a309 R(35,14): sprite col16 -> CW#1; a310 R(35,19): sprite col21 -> CW#2 = TARGET
#   101/110/011 RED; a311 D(40,19) a312 L(40,14) a313 D(45,14)=RINGC t14->42; a314 R(45,19)
#   a315 D(50,19) a316-319 R to (50,39) t28.
# NEXT CALL: verify pattern==T; then R(50,44) R(50,49) R(50,54)->UP-ride col54 -> rests (5,54)
#   covering pattern rows 6-8 cols 55-57 = WIN (U spare if rests lower). If ride failed at a306:
#   replan from actual pos; ringC still unspent in that case.
# a294-295: touch5: U0 -> V0=011/101/010 (5 ones). Chain: P0,Q0,R0,S0,U0,V0 (no cycle, no hit).
# SUBMITTED (a296-299): L,R (touch6 = g(V0)) then L,L -> ringB (10,9) arrive t2 -> refill 42.
#   Safe regardless of touch6 result (walk to ringB touches nothing). Next call: eval touch6;
#   if T: win route from ringB 18mv=36 (end 6). If ccw(T): sprite2 leg 10mv, ringC refill, win 10mv.
#   Else: R,R from ringB = touch7 (lands on sprite1), continue off/on probes with 42 budget.
# CHAIN UPDATE (a290-293): EQUIVARIANCE CONFIRMED (touch3 gave predicted S0=010/010/111).
#   touch4: S0 -> U0=101/101/111 (7 ones). Canonical chain: P0(5)->Q0(6)->R0(6)->S0(5)->U0(7)->?
#   MODEL SEARCHES ALL FAIL on 4 canonical pairs: rotation-commuting affine (inconsistent),
#   cellwise h(P,cwP,cw2P,cw3P), isotropic CA (torus+bounded), binary & ternary boolean combos of
#   8 syms + invariant masks. g = nonlinear, no compact form found. PROBE EMPIRICALLY.
#   Win condition: g^t(R0) hits T=101/110/011 (no sprite2) or ccw(T)=101/011/110 (+sprite2 cw, any order).
#   t=1: S0 no, t=2: U0 no.
# SUBMITTED (a294-295): L,R = touch5 -> g(U0). Timer 14->10 on sprite1. STOP-AND-LOOK each touch
#   (overshoot would ruin a hit). Budgets from sprite1 t10: if HIT T: ringB(2mv->6->42) then win
#   route from ringB 18mv=36 -> end 6 OK. If ccw(T): ringB->42, sprite2 leg 10mv->22, ringC->42,
#   win 10mv->22 OK. If neither: touch6 (->6), ringB (->2->42), continue touches via R,R from ringB
#   (=touch, 4 timer) + off/on 4 each -> ~9 more touches max, then NO refills left (ringC on sprite2 leg).
# SPRITE1 BREAKTHROUGH (a287-289): NOT a cycler. g = deterministic op, SAME as L4 sprite
#   (L4: 010/110/011 -> 111/001/101 == sample D). g COMMUTES WITH cw (verified 2 pairs:
#   g(cwP0)=cw(g(P0)), g(cwQ0)=cw(g(Q0))). Canonical chain: P0=010/110/011 -> Q0=111/001/101
#   -> R0=110/011/101 -> S0=010/010/111 (S0 predicted by equivariance, unverified) -> ???
#   Current (a289, t22, on sprite1 (10,19)): pattern R0 = 180(T)! T=101/110/011, ccw(T)=101/011/110.
#   WIN CONDITION: find t with g^t(R0) == T (no sprite2) or == ccw(T) (sprite2 cw anytime,
#   order flexible by equivariance). g^1=S0 no; g^2+ unknown. No cellwise h(P,cwP,cw2P,cw3P)
#   rule fits chain — probe empirically.
#   Ones-count chain: 5,6,6,5(S0),... note P0 5-cell, others 6/5 — g not injective-friendly; watch cycle.
# BATCH C' SUBMITTED (a290-293): L R (touch3, predict S0=010/010/111 = equivariance TEST), L R
#   (touch4 = g(S0) NEW). End t14 on sprite1. Budget then: 2 more touches (->6) + ringB (10,9) 2mv
#   (->2->42) possible. RingB/ringC UNUSED. From ringB: win route 18mv=36 (end 6); sprite2 leg 12mv
#   -> ringC 42 -> win 10mv (end 22). From ringB DO NOT walk R,R (re-touch sprite1) unless intended;
#   detour = R(10,14) D(15,14) R(15,19) D(20,19)...
# BATCH A RESULT (a265-284): PERFECT. RED confirmed a276, ringA a279, end (15,29) t32.
# BATCH B SUBMITTED (a285-289): L(15,24) L(15,19) U(10,19)=s1 t1 [expect 101/001/111] L(10,14)
#   R(10,19)=t2 [expect 101/011/110]. End t22 on sprite1. Then BATCH C (verify S2): sprite2 leg.
# L5 ATTEMPT 2 (RESET at a265). SOLUTION FOUND: touch#3 (a264) gave 100/111/100 != target, BUT
#   cw(S2=101/011/110) = 101/110/011 = TARGET EXACTLY. Intended solve: sprite1 x2 -> S2, THEN
#   sprite2 (single-use rot90cw). Last attempt wasted sprite2 first. Sprite1 seq observed:
#   [any]-> 101/001/111 -> 101/011/110 -> 100/111/100 (cycler model: state-independent presets).
# BATCH A (a265-284, 20): RESET; R(40,54) U(35,54) U(30,54>ride>30,44) U(25,44) L(25,39>up>5,39)
#   L(5,34>chute>25,34) L(25,29)=TILE1 blue; R L=TILE2 green; R L=TILE3 RED; R(25,34)
#   R(25,39>up>5,39) R(5,44)=RINGA arrive t14 refill 42; L(5,39) D(10,39) D(15,39) L(15,34)
#   L(15,29). End (15,29) timer 32, pattern RED 010/110/011. All cells traversed last attempt.
# BATCH B (next call, verify red first): L(15,24) L(15,19) U(10,19)=s1 touch1 [expect 101/001/111;
#   if NOT, cycler wrong -> STOP, s1 is state-fn, replan with new data] then L(10,14) R(10,19)=touch2
#   [expect 101/011/110]. 5 moves -> timer 22.
# BATCH C (verify S2 first!): D(15,19) D(20,19) D(25,19>leftfan>25,9) D(30,9) D(35,9) D(40,9)
#   R(40,14) U(35,14)=SPRITE2 rot -> TARGET. 8 moves -> t6. D(40,14) D(45,14)=RINGC t2->42.
#   RISK: (25,19) ride unverified; if no trigger, settles (25,19), rest no-op safely, replan.
# BATCH D (win, 10 moves, t42->22): R(45,19) D(50,19) R(50,24) R(50,29) R(50,34) R(50,39)
#   R(50,44) R(50,49) R(50,54)=UPRIDE to panel, U=WIN (rest row 11 vs 12 TBD).
# L5 SPRITE1 = SHAPE CYCLER (a262 probe): 2nd touch gave 101/011/110, NOT the XOR-undo.
#   Full seq: 010/110/011 -(sprite2 rot)-> 010/111/100 -(s1#1)-> 101/001/111 -(s1#2)-> 101/011/110.
#   No single rot/mirror/XOR op fits both s1 transitions => preset cycle (also explains L4
#   one-touch-to-target). Current = target with rows1,2 swapped => S3 likely = target 101/110/011.
#   Timer 38 @ (10,19). Budget: retouch (L,R)=4 -> 34; win route from (10,19) = 16 moves = 32 ->
#   finish at 2. ONLY ONE touch chance left; if S3 != target -> RESET (redo color 3 touches etc).
#   Route from (10,19): D(15,19) R(15,24) R(15,29) R(15,34) R(15,39) R(15,44) D(20,44) D(25,44)
#   D(30,44) D(35,44) R(35,49) D(40,49) R(40,54) D(45,54) D(50,54)=up-ride, then U = cover panel.
#   Submitted probe3: ACTION3, ACTION4.
# L5 SPRITE1 MYSTERY (after a260, at ringB (10,9), timer 42, pattern 101/001/111 #.#/..#/### red):
#   Target 101/110/011 (#.#/##./.## red). Sprite1 touch flipped mask 111/110/011 on the pattern
#   (post-rot k=1 state). Rotating-frame XOR model: fixed logical mask M=101/111/110 (== L4's
#   observed flip), effective mask cw^k(M). Reproduces BOTH L4 and L5 observations.
#   BUT: BFS closure with ops {rot90cw (sprite2), XOR cw^k(M)} = only 8 states; target NOT in
#   closure (middle row 110 never occurs). Fixed-mask variant: closure 64, target also absent.
#   => XOR models PROVABLY cannot reach target; sprite1 op must be something else.
#   SPRITE2 = SINGLE-USE this attempt (did not respawn after step-off). Sprite1 DID respawn.
#   Rings A,B,C all consumed. RESET restores sprites/rings/timer, pattern -> orange 010/110/011.
#   PROBE (submitted): R,R from ringB -> (10,14) -> (10,19)=2nd sprite1 touch. XOR predicts exact
#   undo to .#./###/#.. (010/111/100). Any other result reveals true rule (e.g. per-respawn mask
#   cycling, set-to-fixed-shape, etc). Timer after probe: 38.
# L5 BATCH3 (a234-240): SPRITE2 = ROT90CW confirmed (.#./##./.## -> .#./###/#..), walkable
#   despite 8-cells. At ringC (45,14) timer 42. Pattern red, 1 rot applied.
# BATCH4 (a241-260, 20): to SPRITE1 + ringB: R(45,19) R(45,24) U(40,24) R(40,29) R(40,34)
#   U(35,34) R(35,39) R(35,44) U(30,44) U(25,44) U(20,44) U(15,44) L(15,39) L(15,34) L(15,29)
#   L(15,24) L(15,19) U(10,19)=SPRITE1 [expect 'set-to-target' like L4] then L(10,14) L(10,9)=ringB
#   refill arrive timer 2. AVOIDED (35,14) re-rot.
# NEXT (from ringB 42): verify pattern == target 101/110/011 (#.#/##./.## RED). If yes, 18-move win:
#   R(10,14) D(15,14) R(15,19) R(15,24) R(15,29) R(15,34) R(15,39) R(15,44) D(20,44) D(25,44)
#   D(30,44) D(35,44) R(35,49) D(40,49) R(40,54) D(45,54) D(50,54)->UP-ride to panel, then U=WIN
#   (assumes ride rests block top at row 11; if rests row 12, U gives rows 7-11 missing pattern
#   row 6 -> misalignment problem, rethink). DO NOT re-enter (10,19) from (10,14) (re-touch).
#   If sprite1 is XOR/other: recompute needed op sequence (sprite2 rot available, 2-move cycles).

# L5 BATCH2 (a214-233): PERFECT. Color = RED done (cycle f->I->n confirmed). At (40,34) timer 16.
#   KEY: (15,39) side-entry settled FREE (a217) => L5 = strip-trigger model; row-15 westbound
#   crossing (15,34)->(15,29)->(15,24)->(15,19) should be safe => sprite1 reachable.
# BATCH3 (a234-240, 7): LLLL (40,14) U(35,14)=SPRITE2 test [if unwalkable: no-op, still fine]
#   D(40,14) D(45,14)=ringC arrive timer 2 -> refill 42.
# NEXT (from ringC, 42): watch sprite2 transform on pattern. Route to sprite1 (18 moves, timer 6
#   on arrival; then L(10,14) L(10,9)=ringB refill 42): R(45,19) U(40,19)... NO wait actual:
#   (45,14) R(45,19) R(45,24) U(40,24) R(40,29) R(40,34) U(35,34) R(35,39) R(35,44) U(30,44)
#   U(25,44) U(20,44) U(15,44) L(15,39) L(15,34) L(15,29) L(15,24) L(15,19) U(10,19)=sprite1 —
#   that's 19: RECOUNT when planning; ringB (10,9) 2 moves from sprite1 stepping off WEST (no re-touch).
#   AVOID re-crossing (35,14) after sprite2 collected (respawn on step-off => re-touch reapplies!).
# THEN: win route to (50,54) + UP-ride + U. From ringB area: row 15 east crossing back, D-chain
#   (20,44)...(35,44), (35,49)?? grid (35,49) X, D (40,49) D? (45,49) '.'... route to (50,54):
#   via (40,54) D (45,54) D (50,54)-> UP ride. Verify (45,54),(50,54) walkable: grid X at both. YES.
# Shape needed: .#./##./.## -> #.#/##./.## (flip (0,0),(0,1),(0,2)).

# L5 BATCH1 RESULTS (a207-213): TIMER RATE = 2/action! Timer 28 @a213 on tile (25,29).
# CORRECTION: fan (30,39-43) blows UP — chute cols 39-43 rows 5-29, strip (25,39)->(5,39)!
#   (a211 surprise ride). Top chute strip (5,34) -> lands (25,34) (a212, as L4-style).
# Tile touch1: orange -> BLUE. Full cycle now certain: I->n->-->f->I (green,red,orange,blue).
#   Need 2 more touches: f->I(green)->n(RED).
# BATCH2 (a214-233, 20): [ringA] R(25,34) U(F2 ride 20,44) U(15,44) L(15,39; if up-chute
#   whole-corridor -> lands (5,39), later Us no-op, SAME result) U U R(5,44)=RINGA refill.
#   [recolor] L(5,39) L(5,34 -> top chute ride (25,34)) L(touch2 green) R L(touch3 RED).
#   [toward sprite2] R U(F2 ride 20,44) D(25,44) D(30,44) D(35,44) L(35,39 safe below fan)
#   L(35,34) D(40,34). End (40,34), timer ~16.
# NEXT: L L L L (40,14) U(35,14)=sprite2 test [two-tone plus; walkability unknown — if blocked,
#   no-op], then D D = ringC (45,14) refill 42. Observe transform; then sprite1 (10,19) may need
#   (15,34) side-entry test (row 15 is ONLY westbound crossing of chute cols 34-38).
#   WIN once shape+color right: reach (50,54): from (45/50 area) ... (50,54) strip -> UP ride to
#   panel, then U = cover pattern (5,54). Verify ride rest position when we get there.

# LEVEL 5 (score 4! started a207; L4 won ON final action at timer 0 — timer-0 win VALID)
- Block start (40,49); grid r=0 mod 5, c=4 mod 5. Timer 42, rate UNKNOWN (measure batch 1).
- Current: orange .#./##./.## (5 cells). Target: RED #.#/##./.## (6 cells) rows 6-8 cols 55-57,
  panel rows 3-11 cols 52-60. WIN pos (5,54).
- Sprite1 cover (10,19): cells (11,20),(12,21),(12,22),(13,21) = S/Z skew, all white. Transform ?
- Sprite2 cover (35,14): cells (36,16),(37,16),(37,17) white + (37,15),(38,16) OFF-WHITE(8) —
  two-tone plus; cover cells include 8s -> walkability uncertain. Transform ?
- Tile cover (25,29) (cells rows 26-28 cols 30-32). Color cycle known: I->n->-->f; from orange:
  -->f(blue)->?->n(red)... likely 3 touches orange->blue->green->red IF cycle is f->I->n. VERIFY.
- Rings: A (5,44), B (10,9), C (45,14).
- Fans: top (4,34-38) DOWN chute cols 34-38 rows 5-29 (strip (5,34); chute-end (25,34) safe no-op);
  (20-24,33) RIGHT strip (20,34)->(20,44); (25-29,24) LEFT strip (25,19)->(25,9);
  (29,49-53) DOWN strip rows 30-34 cols 49-53; (30-34,59) LEFT strip (30,54)->(30,44);
  (40-44,43) RIGHT strip (40,44)->(40,54); (55,54-58) UP strip (50,54)-> rides col 54-58 to panel
  (expected stop just below/at panel, then U = cover pattern = WIN; exact rest position TBD).
- Right corridor col 54-58 rows 5-29 UNREACHABLE by walking ((30,54) blows left; no side entries);
  the bottom UP-fan ride is the only win approach. (25,54),(20,54),(15,54),(10,54) X but isolated.
- Walk grid (X): r5: 14,19,24,34,39,44,54; r10: 9,14,19,24,34,39,54; r15: 14,19,24,29,34,39,44,54;
  r20: 19,34,39,44,54; r25: 9,14,19,29,34,39,44,54; r30: 9,44,49,54; r35: 9,19,24,34,39,44,49,54;
  r40: 9,14,19,24,29,34,44,49,54; r45: 14,19,24,54; r50: 19,24,29,34,39,44,49,54.
- BATCH (a207-213, 7): R(40,54 safe) U(35,54) U(30,54->blown LEFT->(30,44)) U(25,44) L(25,39)
  L(25,34 chute-end safe) L(25,29)=TILE touch1. Learn: timer rate, color cycle from orange.
- NEXT: cycle color (off/on via R/L at (25,34), 2 moves each) to RED; then sprites for shape;
  then bottom fan ride (50,54) up + U for win. Sprite1 route needs left-top region via (15,34)/(15,29)
  [chute cells — test wind model when entering from side at non-end rows].

# L4 COLOR CYCLE CONFIRMED green(I)->red(n)->orange(-) [a190,192]; with L3's -(orange)->f(blue):
#   full cycle likely I->n->-->f(->I?). Timer 14 on tile (30,34), shape correct.
# BATCH (a193-206, 14 = ALL-IN, timer hits 0 on win move): U,D (3rd touch -> BLUE), then finish:
#   U(25,34) R->F4 ride->(5,39) D(10,39) D(15,39) L(15,34) L(15,29) L(15,24) U(10,24) U(5,24)
#   L(5,19) L(5,14) L(5,9)=WIN covering pattern rows 6-8 cols 10-12.
# If fails (timer-0 loss or wrong color): auto/manual RESET redo ~61 actions:
#   16 to sprite (ring1 en route), +6 to ring2 (D,Lride,RRR,D), +22 to tile, +4 cycles, +12 finish.

# L4 TILE = COLOR CYCLER (a188-190): 1st touch green(I)->RED(n), NOT blue. Timer 16 on tile (30,34).
#   Known transitions: L3 orange(-)->blue(f); L4 green(I)->red(n). Cycle order unknown.
# BATCH (a191-192): U(25,34), D(30,34) = 2nd touch. If red->blue: finish 12 moves, timer 2 left = WIN.
#   If red->orange: 3rd touch would leave timer 12 vs 12-move finish = exact 0 gamble;
#   consider RESET (restores rings+timer, pattern back to green .#./##./.##, 5 cells, sprite needed again).
#   Redo-from-reset cost ~48 actions: start->sprite 16 (ring1 en route), sprite->tile 20, cycles+finish 12-16.

# L4 (a169-187): trek PERFECT. At (30,49) timer 19. F2 ride (15,34)->D->(20,54) worked;
#   (35,14)/(30,44)-class far-corridor cells confirmed free. Strip model solid.
# BATCH (a188-190, 3): L(30,44) U->F3 ride->(25,34) D(30,34)=TILE. Expect green->blue. Timer 16 after.
# NEXT CALL: if pattern BLUE fff/..f/f.f: finish 12 moves timer->4: U(25,34) R->F4 ride->(5,39)
#   D(10,39) D(15,39) L(15,34) L(15,29) L(15,24) U(10,24) U(5,24) L(5,19) L(5,14) L(5,9)=WIN.
#   If color wrong: step off+on tile to cycle (U,D = 2 moves, budget allows ONE extra cycle: 14+12... 
#   actually 2+12=14 <= 16 OK), else RESET.

# L4 WIND MODEL CONFIRMED (a159-168): STRIP-TRIGGER, not whole-corridor!
#   (40,34) & (40,39) entered freely (far cells of F8 corridor, no push); (40,44) [strip adjacent
#   to F8] triggered 10-col slide back to (40,34). Trigger = 5-wide strip adjacent to fan;
#   once triggered slide continues to obstruction. L3 fan differed (long trigger) — level-specific.
# a159-168 recap: D(35,24) L->F5 ride (45,19) RRR (45,34) D ring2 REFILL 42, UU(40,34) R(40,39)
#   R probe -> bounced (40,34). Timer 38 @ a168. Ring1+Ring2 both SPENT. No refills left!
# BATCH (a169-187, 19): D LLLL (45,14) UUUUU (20,14) R (20,19) U (15,19) RRR (15,34)
#   D -> F2 strip ride -> (20,54), D(25,54) D(30,54) D? no: D,D then L(30,49) L... 
#   exact: moves 16-19 = D(F2 ride to 20,54), D(25,54), D(30,54), L(30,49). Ends (30,49) timer 19.
#   (If F2 fails to trigger: same string lands ON TILE (30,34) — also fine.)
# NEXT CALL (14 moves, timer 19 -> 4 margin): L(30,44) U->F3 ride->(25,34) D(30,34)=TILE color->blue,
#   then U(25,34) R->F4 ride->(5,39) D(10,39) D(15,39) L L L (15,24) U(10,24) U(5,24) L L L (5,9)=WIN.
# TIGHT: zero wasted moves allowed. If anything misfires, likely RESET + redo with known 40-move route.

# L4 UPDATE (a143-158): TIMER RATE = 1/action! Ring1 refilled at a151 (42). Timer 35 @ a158.
# SPRITE (30,24): ONE touch changed .#./##./.## -> ###/..#/#.# = EXACT TARGET SHAPE (5->6 cells,
#   NOT a rotation — new transform, maybe 'set to target shape'). DO NOT touch sprite again!
# Only COLOR left: green->blue via tile (30,34) (fII/f$n/--n at rows 31-33 cols 35-37).
# WIND MODEL (from L3+L4 evidence): entering a fan's corridor FROM OUTSIDE triggers blow;
#   moves WITHIN corridor are free; slides ignore other fans mid-flight; nearest fan wins overlaps.
# Fan corridors: F1 DOWN chute cols 44-48 rows 20-49 (lands (45,44)); F2 RIGHT rows 20-24 cols 34-58
#   (lands (20,54); (20,54) enterable from below = terminal, no-op); F3 LEFT rows 25-29 cols 34-48
#   (lands (25,34); (25,34) enterable from above = terminal); F4 UP chute cols 39-43 rows 5-29
#   (lands (5,39); can climb DOWN within it after landing); F5 DOWN cols 19-23 rows 35-49 -> (45,19);
#   F6 RIGHT rows 35-39 cols 9-28 -> (35,24) ((35,24) = terminal, safe); F7 LEFT rows 40-44 cols 9-28
#   -> (40,9); F8 LEFT rows 40-44 cols 34-48 -> (40,34) ((40,34) = terminal).
# TRAPS: (20,44) blown down BOTH models; (20,34) entered from above -> blown right; upper-left
#   region rows 5-29 cols 9-28 unreachable from below EXCEPT via F4 chute ride to (5,39) + climb down.
# BATCH (a159-168, 10): D(35,24) L(F5 ride 45,19) RRR(45,34) D(50,34 RING2 refill 42)
#   UU(40,34) R(40,39) R(40,44)=PROBE: expect (45,44) [F1] or bounce (40,34) [F8 strip].
# NEXT: if (45,44): R(45,49) R(45,54) U(40,54) U(35,54) U(30,54) L(30,49) L(30,44)[F1 risk!]
#   U(25,44)->F3->(25,34) D(30,34)=TILE. If bounced: try (20,54)-route or F3 via right col 54.
# FINISH (from tile, ~12): U(25,34 safe terminal) R(25,39)->F4 UP->(5,39) D(10,39) D(15,39)
#   L(15,34) L(15,29) L(15,24) U(10,24) U(5,24) L(5,19) L(5,14) L(5,9)=WIN covers pattern rows 6-8 cols 10-12.
# Ring2 will be USED; no refills left after — budget carefully or RESET-restart if stuck.

# LEVEL 4 (score 3, block start (5,54), timer 42, rate UNKNOWN — measure on batch A)
- Current pattern GREEN .#./##./.## (5 cells). Target BLUE fff/..f/f.f (6 cells!) —
  rotations can't match: sprite this level must ADD/change cells. OBSERVE transform.
- Panel rows 3-11 cols 7-15; pattern rows 6-8 cols 10-12; WIN pos (5,9), approach L along row 5.
- Key covers: sprite (30,24) [ONLY reachable via F6 ride to (35,24) then U];
  tile (30,34) [via F3 ride: (30,44) U->(25,44) blown to (25,34), then D];
  ring1 (15,19); ring2 (50,34).
- FANS: F1 (19,44-48) DOWN; F2 (20-24,33) RIGHT [zone (20,34-38)->blown (20,54)];
  F3 (25-29,49) LEFT [zone cols 44-48 -> (25,34)]; F4 (30,39-43) UP [zone (25-29,39-43)->(5,39)];
  F5 (34,19-23) DOWN [zone (35-39,19-23)->(45,19)]; F6 (35-39,8) RIGHT [(35,9-13)->(35,24)];
  F7 (40-44,29) LEFT; F8 (40-44,49) LEFT.
- AVOID: (20,34) F2 trap-right; (25,39) F4; (35,19) F5.
- Walkable bands (row:cols): 5-9:(7-28),(39-58); 10-14:(7-15 panel),(24-28),(34-43);
  15-19:(19-43),(49-58),row19(19-58); 20-24:(14-28),(33-58); 25-29:(9-18),(34-49),(54-58);
  30-34:(9-18),(24-28),(34-38/58); 35-39:(8-28),(44-58); 40-44:(9-29),(34-49),(54-58);
  45-49:(14-38),(44-58); 50-54:(24-38),(49-58).
- BATCH A (16 moves, submitted): LLL(->5,39) DD(->15,39) LLLL(->15,19 ring1 refill)
  D L D D L(->30,9... route: (20,19),(20,14),(25,14),(30,14),(30,9)) D(->35,9 F6 ride ->35,24)
  U(->30,24 SPRITE cover). Next call: measure timer rate, diff pattern (transform!), plan tile+finish.
- Finish sketch: sprite -> D(35,24) ... route to tile (30,34) via F3, then to (5,9).
  From tile (30,34): D(35,34)?? band 35-39 cols 44-58 only — check; likely U to (25,34), route west.

# Game mechanics (learned in Level 1, score 1/)
- Player = orange/blue 5x5 block (orange top 2 rows, blue bottom 3). Moves 5 cells per action.
- Blocked moves = safe no-ops; timer ticks regardless.
- Timer: yellow G bar rows 61-62, cols 13-55 (43 columns) = action budget per level; resets each level.
- White plus-sprites: collecting one FLIPS specific cells in bottom-left "current" pattern panel.
- Bottom-left panel (rows ~53-62, cols 1-10, 2x scale) = current pattern (persists across levels).
- In-maze panel (h border, O interior, blue f pattern) = TARGET pattern.
- WIN: make current pattern match target, then drive block INTO the target panel (cover the pattern) => score +1.
- Level 1 solved in 21 actions (lots of probing).

# Level 2 state (as of action 20)
- Target (rows 41-43, cols 15-17): fff / f.. / f.f ; panel at rows 38-46, cols 12-20,
  entered from corridor cols 14-18 going down (final move D from (35,14) -> (40,14)).
- Current: fff / ..f / f.f — middle row differs; L1 sprite swapped middle-row cells, so
  this sprite presumably flips middle "..f" -> "f.." = match.
- Block start: (40,29) [top-left of 5x5]. Sprite: rows 46-48, cols 50-52.
- NEW: yellow 3x3 rings at (16-18, 15-17) and (51-53, 41-43) — function unknown; embedded in walkways.
- Actions 21-37 (submitted): R,U,U,U,U,U,U,R,R,R,D,D,D,D,D,D,D -> (45,49) covers sprite.

# L3 UPDATE (a106-119): TILE = COLOR CHANGER (orange->blue confirmed), shape unchanged.
# RINGS ARE SINGLE-USE PER ATTEMPT (ringA 2nd touch: NO refill). RingB fresh.
# NEW FINISH IDEA: fan#2 (row 4, cols 55-59) should blow block DOWN col 54-58 corridor
# from (5,54) all the way into panel interior (rows 49-55) -> rests covering pattern = WIN.
# Right corridor is cols 54-58 (all rows 10-47), NOT 55-59.
# BATCH (a120-139, 20 moves): DDDLLL (->ringB(30,19), arrive timer 2, refill 42),
#   URRRRRRRUUUL (->sprite (10,49) rot1), R,L (rot2). End timer 14, pattern should = f.f/f../fff.
# NEXT CALL: verify pattern==target, then U (5,49), R (5,54) -> fan ride down into panel WIN.
# Fallback: walk D's down col 54 corridor (~5 moves, timer 10 suffices barely w/ care).

# L3 PROGRESS (a102-105): ESCAPED TRAP — wind is ENTRY-TRIGGERED only (L from (5,34)
# settled at (5,29), no re-blow). Now on ringA (15,34), timer refilled 42.
# ITINERARY: [A: a106-119] ringA->tile (DDDLDDD) observe color effect, tile->ringA (UUUUUUR) refill.
# [B] ringA->sprite DDRRRRUUUL (rot1), sprite->ringA RDDDLLLLUU (arrive timer 2, refill).
# [C] ringA->sprite (rot2), sprite->panel DRDDDDDDD (arrive timer 4) WIN if pattern+color match.
# WATCH: fan#2 row4 cols 55-59 may blow DOWN in top-right region (rows 5-19, cols 44-58) —
# batches B/C pass (10,54)/(10,49); if pushed down unexpectedly, adapt.

# LEVEL 3 CRITICAL: WIND/FAN TILES ('8' off-white)
- Fan at col 8 rows 5-9 blows RIGHT along top-left corridor (rows 5-9, cols 9-38):
  entering it (e.g. U to (5,9) or (5,29)) triggers 16-frame slide to (5,34) = DEAD END TRAP
  (rows 10-14 only walkable at cols 9-13, 29-33, 44-58; (10,34) is q).
- Second fan: row 4, cols 55-59 — likely blows DOWN right corridor (cols 54-58). Untested.
- Timer rate L3 = 2 cols/action confirmed. Blocked moves still cost.
- Action 94 was the trap entry; actions 95-101 all blocked (stuck at (5,34)).
- Escape test (a102-105): L,D,D,R -> if wind is entry-triggered only, L settles (5,29),
  D escapes to (10,29), D (15,29), R (15,34)=ringA refill. If wind re-blows, stuck; RESET next call.
- LESSON: BFS must model wind zones; avoid rows 5-9 cols 9-43 entirely in future routing.
- Corridor col map: rows 10-14: 9-13/29-33/44-58; rows 15-19: 9-13/19-38/44-58;
  rows 20-24: 9-13/19-38/54-58; rows 25-34: 9-13/19-58; rows 35-39: 9-13/29-33/54-58;
  rows 40-44: 9-18/24-38/54-58; rows 45-49: 14-18(+start 9-13)/25-39/53-61(panel);
  rows 50-54: 24-38/panel.

# LEVEL 3 (score 2, started action 87)
- Block start (45,9). Current pattern fff/..f/f.f ORANGE (rows 55-60 cols 3-8 panel).
- Target f.f/f../fff BLUE (panel rows 48-56 cols 53-61; pattern rows 51-53 cols 55-57; entry (50,54) from above).
- Shape: rot180 = 2 sprite touches. Color: orange->blue via NEW 3x3 multicolor tile at (46-48,30-32)
  (fII/f$n/--n colors) — HYPOTHESIS, unverified. Cover at (45,29).
- Sprite (plus) at (11-13,50-52), cover (10,49) — corner w/ 3 neighbors; off/on = R,L.
- Rings: A cover (15,34), B cover (30,19). Pattern did NOT persist from L2 (level-defined start).
- '8' cells at row4 cols 55-59 + col 8 rows 5-9 — unknown, avoid/ignore.
- Pairwise moves: start-ringA 15, ringA-tile 7, tile-ringA 7, tile-ringB 5, ringB-sprite 12,
  ringA-sprite 10, sprite-ringA 10, sprite-panel 9 (DRDDDDDDD), ringA-panel 11, ringB-panel 11.
- SAFE PLAN (if rate=2/action, cap 42): [1] start->ringA 15; [2] ringA->tile->ringA: DDDLDDD + UUUURUU?
  (tile->ringA = UUUUUUR 7); [3] ringA->sprite 10 (rot1), sprite->ringA 10 (arrive 2 left, refill);
  [4] ringA->sprite 10 (rot2), sprite->panel 9 (arrive 4 left) = WIN. Total ~68.
- MUST VERIFY on batch1: timer rate (L1=1, L2=2, L3=?), then tile effect, sprite transform.
- Batch1 (a88-102): UUUUUUUU RRRR DD R -> ringA.

# CONFIRMED MECHANICS (action 41-42)
- RESET: block->start, sprite respawns, ring restored, timer 42, PATTERN RESETS to level start. No life lost visible.
- SPRITE RESPAWNS when block steps OFF its tile (board 43 vs 44)! Multi-collect in one attempt.
- Rings reusable (ringB restored after block left; also refills mid-attempt).

# LEVEL 2 SOLUTION (attempt 2, started action 42)
Pattern needs 3 cw rotations. Sequence (45 moves total):
  [call 1, 20 moves] R,U6,R3,D7 (rot1 at 45,49; timer 8) + D,L,L (ringB refill 42; at 50,39)
  [call 2 DONE submitting a63-81] R,R,U(rot2),D,U(rot3),U7,L7 -> (10,14), timer 4 on arrival.
  [call 3] verify pattern == fff/f../f.f, then D (15,14)=ringA refill, D5 -> (40,14) panel = WIN
CALL-1 RESULT: plan adhered exactly; after rot1 pattern f.f/..f/fff confirms cw model so far.
DISAMBIGUATION at call 2: after rot2 expect f.f/f../fff if sprite=rot90cw;
  if instead fff/..f/f.f then sprite=mirror (vflip) -> rethink (cw model wrong).
Panel entry: (40,14) covers target pattern rows 41-43 cols 15-17.
RingA = (16-18,15-17), block (15,14). RingB = (51-53,40-42), block (50,39).

# KEY MODEL (revised after action 40)
- SPRITE = ROT90 CLOCKWISE of current pattern (consistent with BOTH L1 and L2 observations;
  earlier "mirror" reads were ambiguous aliases).
- RING = TIMER REFILL to 42 (bottom ring at rows 51-53, cols 40-42; block (50,39) covers it).
  Pattern unchanged by ring. Ring persistence/reusability TBD (hidden under block now).
- Current pattern f.f/..f/fff = start + 1 cw. Target fff/f../f.f = start + 3 cw. Need 2 more sprite grabs.
- Sprite is consumed => hypothesis: RESET respawns sprite; pattern may PERSIST across resets
  (it persisted across L1->L2). Action 41 = RESET to test.
- If persists: cycle = RESET, 17-move sprite route, ring refill as needed, repeat; final cycle
  ends with panel run U7,L7,D6 from (45,49) with ring detour first.
- State at action 40: block (50,39) on ring, timer 42, lives 6 n-cells (3 pairs), score 1.

# Level 2 findings (after actions 21-37)
- SPRITES APPLY TRANSFORMS, not fixed flips: L1 sprite = horizontal mirror; L2 sprite = VERTICAL mirror.
  Current went fff/..f/f.f -> f.f/..f/fff (row order reversed).
- Current needs rot180 to reach target fff/f../f.f. (vflip+rot180 = hflip from L2 start pattern.)
- TIMER: Level 2 drains 2 cols/action (L1 was 1/action). 42 start -> ~21 action budget!
  After action 37: 8 cols = 4 actions left this attempt.
- My 17-move sprite route + return is way over budget. Need to learn rings.
- Recon (actions 38-40): D,L,L from (45,49) -> (50,39) covers bottom ring (51-53,41-43).
  Distinguish: result f.f/f../fff => ring is rot90cw-or-hflip; result fff/..f/f.f => rot90ccw-or-vflip;
  other => teleport/timer/other.
- If ring turns out to be hflip: NEXT ATTEMPT solution skipping sprite entirely (17 moves, fits budget):
  from start (40,29): R,U,U,U,U,U,U,L,L,L,L,D(ringA at 15,14),D,D,D,D,D(panel 40,14).
- Timer will expire right after recon -> expect auto-reset (watch red nn 'lives' pairs rows 61-62 cols 56-63).
