# Game notes

## Level 1 initial board (Action 0)
- 64x64, rendered in 2x2 pixel blocks (effective 32x32).
- Row 0: 'z' light-magenta full-width strip — likely UI/timer.
- Rows 1-27: gray 'h' left half (x0-31), white '$' right half (x32-63).
- Black 'O' band rows 28-31, x20-63; yellow 'G' notch inside at x38-39 (slider on track?).
- Blue 'f' 4x4 blocks at x60-63, y24-27 and y32-35 (flank right end of band) — goals?
- Rows 32-63: gray x0-51, white x52-63.
- Figure at x46-51, y44-49: off-black 'q' left-pointing arrow + yellow 'G' vertical bar ("◄|") — player or button?

## Probes (Action 1-2) — RESULTS
1. ACTION6(48,46) arrow figure — NO effect. Only timer: (63,0) z->q.
2. ACTION6(39,30) yellow notch — NO effect. Only timer: (61,0),(62,0) z->q.
=> Row 0 is a step budget depleting right-to-left (~1-2 px/action, 3 used of 64).
=> Arrow figure & notch are not click-targets (or clicks there are no-ops).

## Probes (Action 3-5) — RESULTS
3. ACTION6(61,26) top blue block: top boundary 32->28 (left 4px), bottom boundary 52->56 (right 4px). Figure moved with bottom boundary (bar always at boundary-2).
4. ACTION6(50,30) black band: no effect.
5. ACTION6(10,10) gray field: no effect.

## MECHANIC (Level 1)
- Blue blocks at x60-63 are buttons: top one (y24-27) shifts top boundary LEFT / bottom boundary RIGHT by 4px. Bottom one (y32-35) presumably the reverse.
- Fixed yellow notch x38-39 on band = target. Goal: align figure's yellow bar (bottom-boundary-2) with notch => bottom boundary at x=40.
- Timer row 0: ~1px/action, 6/64 used after 5 actions.

## Actions 6-9: 4x ACTION6(61,34) — SUCCESS, Level 1 cleared at action 9 (Score 1).

## CONFIRMED MECHANIC
- Sections of white/gray separated by black bands. Blue 4x4 buttons sit adjacent to a band, inside a section's white area: clicking pulls 4px of white across that band into the button's section (paired section loses 4px).
- One section has a figure (arrow + colored bar). Bar occupies the 2 GRAY px adjacent to the white/gray boundary. Goal: align bar with the fixed notch of same color on a band. Timer row 0 resets each level, ~1px/action.
- White width cannot go negative — route white through intermediate sections as needed.

## Level 2 (score 1)
- Bands rows 20-23 & 40-43. Sections: A(1-19) white=52, B(24-39) white=12, C(44-63) white=8 + figure (green bar x8-9, arrow points right).
- Green notch x28-29 on band 2 => need C white=28 (+20).
- Buttons x0-3: B1 y16-19 (A pulls from B), B2 y24-27 (B pulls from A), B3 y36-39 (B pulls from C), B4 y44-47 (C pulls from B).
- Plan: 2x (2,25) [B:12->20], then 5x (2,45) [C:8->28, B:20->0]. SUCCESS — score 2 at action 16.

## Level 3 (score 2) — vertical tubes
- Field x6-57,y1-57 inside q border. 5 tubes of white liquid, walls (O, 2px wide) between: A x14-15(top38), B x26-27(top52), C x36-37(top36), D x48-49(top30).
- Tubes(x-range, surface, height): t1(6-13,54,4) t2(16-25,56,2) t3(28-35,54,4) t4(38-47,52,6) t5(50-57,30,28).
- Figures sit atop liquid, bar at surface-1, arrow up: green in t1(bar y53), purple in t4(bar y51), yellow in t5(bar y29).
- Notches: green wall A y41, purple wall C y39, yellow wall D y47. (1px resolution this level.)
- Targets: t1 surf 42 (+12), t4 surf 40 (+12), t5 surf 48 (-18).
- Buttons f at rows 56-57 flanking each wall: (12,56)=t1 pull from t2 | (16,56)=t2 from t1 | (24,56)=t2 from t3 | (28,56)=t3 from t2 | (34,56)=t3 from t4 | (38,56)=t4 from t3 | (46,56)=t4 from t5 | (50,56)=t5 from t4.
- Action 17 probe result: QUANTUM = 2px/click this level (t4 +2, t5 -2). Timer 63/64 after probe — timer seems per-level generous.
- Full solution: 22 clicks, order "ababacbacbacbadddddddd" then 2 more d.
  a=(12,56) t2->t1 x6, b=(24,56) t3->t2 x5, c=(34,56) t4->t3 x3, d=(46,56) t5->t4 x8 (9 total incl. probe).
  Constraints held in sim: heights >=0, t2 <=6 (wall B top 52), final t1=16/t2=0/t3=0/t4=18/t5=10.
- Actions 18-37: first 20 executed as planned. State: t1 surf42 (green ALIGNED), t4 44, t5 44, t2/t3 empty. Timer 46/64.
- Actions 38-39: final 2x (46,56) — SUCCESS, score 3 at action 39. Level 3 done.

## Level 4 (score 3) — inverted colors, gray bg, white liquid bottom
- Walls 3px wide: W1 x12-14 (top 31, '8' window rows 43-54), W2 x27-29 (top 22, '8' rows 34-45, NO buttons), W3 x42-44 (top 25, YELLOW notch rows 29-30), W4 x55-57 (top 34).
- Tubes: t1 x0-11 surf 49 (fig: yellow bar rows 47-48, arrow up), t2 x15-26 EMPTY, t3 x30-41 surf 55, t4 x45-54 surf 58, t5 x58-63 surf 46.
- Buttons rows 61-63: (9-11)=t1 pull t2 | (15-17)=t2 pull t1 | (39-41)=t3 pull t4 | (45-47)=t4 pull t3 | (51-53)=t4 pull t5 | (58-60)=t5 pull t4. Wall2 has NONE.
- Puzzle: figure in t1, notch on W3 rows 29-30 (t1 surface must reach 31? or figure must travel?). '8' windows likely key to cross wall2.
- Probes 40-41: window click (13,48) NO-OP. Button (16,62): QUANTUM=3 rows/click. t2 was not empty (base liquid rows 61-63 everywhere). Post: t1 surf 52 (fig bar 50-51), t2 surf 58, t3 55, t4 58, t5 46.
- Windows not clickable. Hypothesis: '8' windows auto-conduct liquid when surface reaches their range (W2 rows 34-45) — only way across buttonless W2.
- Actions 42-47 done: t3 surf 43 touching W2 window rows 43-45 — NO auto-flow. t4 FULLY empty (tubes can drain to zero, base rows too). t5 surf 52. t1 surf 52 (bar 50-51), t2 surf 58.
- Insight: alignment is row/coordinate-based (level 1 bar/notch were far apart) => goal: t1 surface = 31 (bar 29-30). t1 needs +21 rows = 7 pulls from t2; t2 must be fed via W2 window (no buttons).
- Actions 48-53: t3 surf 34 fully covering W2 window — STILL no flow. t4 empty, t5 surf 61 (3 rows left). Timer 46.
- Liquid inventory (rows): t1 12, t2 6, t3 30, t4 0, t5 3 = 51. t1 needs 33 rows for surf 31 => must get 21 via t2 => W2 crossing mandatory.
- Actions 54-56: t3 surf 31 (above window top) — no flow; submerged-window click no-op. Windows are NOT passive holes and NOT clickable. t4,t5 EMPTY. Timer 42.
- State: t1 12 rows (surf 52), t2 6 (58), t3 33 (31). No frames ever observed this level.
- Analyzed: {t1,t2}=18 rows isolated unless W2 crossed; t1 needs 33 => crossing mandatory. Off-by-one infeasibilities everywhere for surface-alignment hypotheses.
- NEW HYPOTHESIS: button pulls from adjacent tube; if adjacent EMPTY, reaches through to next tube (explains missing W2 buttons).
- Actions 57-61: 4 drains worked (t1 empty, t2 surf 46 = 18 rows); 5th click NO-OP => reach-through hypothesis DEAD. Pulling from empty tube = wasted action.
- Figure SANK to t1 floor (bar rows 62-63, arrow above). t2 surf 46 faces W1 window rows 43-54 directly — still zero passive flow. Timer 36.
- State: t1 0 + figure, t2 18 (s46), t3 33 (s31), t4 0, t5 0.
- Key rows math: t1 needs 33 rows (s31) OR figure must reach tube adjacent W3 at s31. {t1,t2} stuck at 18 rows w/o W2 crossing.
- Action 62: (46,62) works (t3 s34, t4 s61/6rows) but NO equalization — pool-merge DEAD. Timer 35.
- BREAKTHROUGH HYPOTHESIS: windows are FIGURE passages. Bar rows = s-2,s-1. At s=46 bar 44-45 overlaps BOTH windows — the recurring "off-by-one" was exact design. Liquid NEVER crosses windows; {t1,t2}=18 rows and {t3,t4,t5}=33 rows are separate conserved pools. Final: figure must reach t3 (adjacent W3 notch) at s3=31 (t3=33 rows = its whole pool).
- FULL PLAN from state (t1 0+fig, t2 18 s46, t3 30 s34, t4 6 s61, t5 0):
  1. 3x (10,62): t1/t2 -> 9/9 rows, both s55, bars in W1 window [43-54] -> figure crosses W1 to t2?
  2. 3x (16,62): all 18 back to t2 (s46, fig bar 44-45)
  3. 1x (46,62): t3 30->27 rows (s37, in W2 band [35,46]) -> figure crosses W2 to t3
  4. 2x (40,62): t3 +6 from t4 -> s31. Bar 29-30 = notch. WIN.
- Actions 63-65: t1/t2 both s55, figure refloated in t1 (bar 53-54, inside W1 band) — NO auto-crossing. Timer 31.
- Refined hypothesis: figure rides TRANSFER flow across wall when bar is inside window band during a button transfer.
- Action 66: transfer during band alignment — figure did NOT ride (t1 58, t2 52, fig bar 56-57 in t1). Timer 29.
- Actions 67-69: SOLVED THE MECHANIC. (10,62) realigned 55/55; CLICKING THE WINDOW (13,53) with both surfaces equal & bar in band triggered 42-frame animation — FIGURE CROSSED W1 into t2! Window turned ORANGE after use. Figure click was no-op. Figure arrow now points RIGHT (toward target).
- MECHANIC: equalize both tubes' surfaces within window band (bar rows s-2,s-1 inside window rows), then CLICK the window => figure crosses.
- Actions 70-77: 3x (16,62) consolidate t2 to s46 (18 rows, t1 empty); 4x (46,62) dump t3 to s46 (18 rows, t4 15 rows s49); click W2 window (28,44) => figure into t3.
- Actions 70-77: SUCCESS — figure crossed W2 into t3 (bar 44-45). t2 s46, t3 s46, t4 15 rows (s49). Timer 15 (burn ~1.4/action; window-crossing animations cost extra).
- Actions 78-82: SUCCESS — score 4 at action 82. Level 4 done (73 actions used total for L4... heavy exploration).

## Level 5 (score 4) — horizontal, 4 sections, gray left/white right
- Sections (rows / white-boundary x / white width): A 1-13 b16 w48 | B 17-31 b59 w5 | C 35-48 b47 w17 | D 52-63 b44 w20. Total white 90.
- Bands+windows: band1 rows14-16 window x28-39, YELLOW notch x20-21; band2 rows32-34 window x40-51, no notch; band3 rows49-51 window x25-36, GREEN notch x14-15.
- Figures: GREEN in A (bar x14-15, arrow left), YELLOW in D (bar x42-43, arrow left). Bar = boundary-2..boundary-1.
- Goal: green in C w/ boundary 16 (w48); yellow in B w/ boundary 22 (w42). 48+42=90 exact.
- Crossing ranges (boundary): band1 [30,40], band2 [42,52], band3 [27,37]. Crossing = click window when both adjacent boundaries in range (equality impossible by parity for q>1 → hopefully not required).
- Buttons x61-63 (pull white INTO own section): A rows11-13, B rows17-19 (from A), B rows29-31 (from C), C rows35-37 (from B), C rows46-48 (from D), D rows52-54 (from C).
- Action 83 probe: QUANTUM=3. CORRECTED widths (initial): A48 B6 C18 D21 (total 93). After probe: A45 B9 C18 D21. Boundaries: A19 B55 C46 D43.
- Crossing ranges (width w=64-b): band1 w in [24,34]; band2 w in [12,22]; band3 w in [27,37]. Click window at (bar_x, band_center_row): band1 y15, band2 y33, band3 y50.
- Buttons: ab=(62,12) ba=(62,18) bc=(62,30) cb=(62,36) cd=(62,47) dc=(62,53) (xy pulls INTO x from y).
- MASTER PLAN (avoids co-location; band2 used once as SWAP):
  P1: cb x3, dc x2, ba x2, cb x2 -> A39 B0 C27 D27; click (35,50): yellow D->C.
  P2: bc x3, ba x5 -> A24 B24 C18 D27; click (38,15): green A->B.
  P3: cb x1 -> B21 C21; click (41,33): SWAP green->C, yellow->B (hope both cross).
  P4: cd x9 (C->48 from D), ba x7 (B->42 from A) -> aligned: green bar 14-15, yellow bar 20-21. WIN.
- Actions 84-93: P1 SUCCESS — yellow crossed into C (bar rides C boundary). Band3 window orange (used). State A39 B0 C27 D27. Timer 60. Residual liquid-bridge rows at 47/53 (harmless).
- Actions 94-102: P2 SUCCESS — green in B (bar x38-39). A24 B24 C18 D27. Timer 58.
- Actions 103-104: P3: cb x1 (B21 C21 b43), click (41,33) — FAILED, no frames. Both bars co-located x41-42 (equal boundaries => bars always overlap). Suspect click ambiguity; deadlock analysis => crossing into occupied section MUST be allowed, so failure is selection, not occupancy.
- Action 105-106 TEST: dc (62,53) desyncs C to w18 (yellow bar x44-45, green stays x41-42), then click (44,33) = yellow's unique bar cell. Tests: (a) crossing w/ UNEQUAL boundaries (both in band2 range [12,22]); (b) unique-bar-cell click selects one figure. If no-op: equality may be required => co-location unavoidable => try clicking arrow 'q' cells or figure body to disambiguate.
- Widths differ: t1,t2,t3=12, t4=10, t5=6 — transfers still fixed 3 rows regardless.
- Actions 105-106: dc OK (C18 b46, D30; yellow bar x44-45 unique). Click (44,33) NO-OP => UNEQUAL boundaries block crossing even w/ unambiguous bar. Equality REQUIRED => bars always co-locate for B/C swap.
- All windows back to '8' (orange transient, reusable). Timer 56.
- NEXT HYPOTHESIS (row-select): band rows disambiguate: y32 (B-adjacent) selects B-side figure, y34 (C-adjacent) selects C-side. Test: cd (62,47) -> B21 C21 equal; click (41,34) to cross YELLOW C->B. If no-op, try (41,32) next turn.
- Actions 107-108: cd OK (B21 C21 equal); click (41,34) bottom-row NO-OP. Row-select hypothesis DEAD.
- EDGE HYPOTHESIS (strong): all 4 successful crossings had boundary == window_far_edge+1 (bar = LAST 2 window cells; window fully exposed, surface at its right edge). Failures were mid-window. Band2 window x40-51 => need B=C=w12 (boundary 52, bars x50-51).
- Plan: ab x3 (B21->12, A24->33), dc x3 (C21->12, D27->36), click (50,33). If swap/cross works: cd x12 (C->48, D->0), ba x10 (B->42, A->3) => green bar x14-15 in C, yellow x20-21 in B. WIN. Liquid: 3+42+48+0=93 exact.
- Actions 109-115: EDGE HYPOTHESIS CONFIRMED. B12/C12 (boundary 52, bars x50-51 = window far edge), click (50,33) => 64-frame SWAP: BOTH figures crossed simultaneously (green->C, yellow->B). Co-location never an issue — doorway swaps both.
- MECHANIC FINAL: crossing = both boundaries at window_far_edge+1 (window fully exposed), click window => all doorway figures cross/swap.
- State after 115: A33 B12(yellow) C12(green) D36, timer 53. Finish: cd x12 (C->48), ba x10 (B->42). 22 actions: 20 this call + 2 next.
- Actions 116-135: cd worked to C39 then NO-OP x3 (125-127). ba x8 fine (A9 B36). DISCOVERY: walls have OPEN LEFT ENDS (band1 x16-63, band2 x25-63, band3 x10-63). Section surface cannot rise past its bounding wall's top edge => caps: A boundary>=16 (w<=48), B/C boundary>=25 (w<=39), D boundary>=10 (w<=54).
- => C48/B42 IMPOSSIBLE. True goal: YELLOW in A w42 (bar x20-21), GREEN in D w48 (bar x14-15). Need 2 more crossings.
- REVISED PLAN from A9 B36(yellow b28) C39(green b25) D9, timer 47:
  S1: bc x1 (B39 C36), ab x5 (A24 B24, boundary 40), click (38,15) => yellow B->A.
  S2: interleave cb,dc,cb,dc,cb,dc,dc,dc,dc (C ends 27, D 27, B15; C capped 39 never exceeded), click (35,50) => green C->D.
  S3: bc x1 (B18 C24), ba x6 (A42 B0), dc x7 (C3 D48) => yellow bar x20-21 in A, green bar x14-15 in D. WIN (hope auto; else click notches).
- Dispatching S1+S2 (17 actions), verify, then S3 (14 actions).
- Actions 136-152: S1+S2 PERFECT. Yellow B->A (44f anim), green C->D (43f anim). State A24(yellow) B15 C27(-) D27(green), timer 42.
- S3 dispatched: bc x1, ba x6 (A42, yellow bar x20-21=GG notch), dc x7 (D48, green bar x14-15=II notch). B0 C3. Expect auto-win; else click notches (20,15)/(14,50).
- Actions 153-166: MY ERROR — used ba (62,18) which grows B, needed ab (62,12). Result A6 B36 C3 D48. D/green PERFECT (bar x14-15 on II notch). No auto-win yet (yellow misaligned).
- Fix: ab x12 => A42 B0. Yellow bar x20-21 on GG notch. Timer 37.

## Level 6 (score 5) — gravity LEFT, T-layout
- Sections: TL x0-20 rows1-29 (w3, YELLOW fig bar x3-4); TR x24-63 rows1-29 (w15); BOTTOM rows33-63 (w18). Total 36. Vertical wall x21-23 full height. Band rows30-32 spans x0-53 (open x54-63).
- Windows: W1 x6-17 (TL<->bottom), W2 x30-41 (TR<->bottom). YELLOW notch x48-49 in band.
- Doorway rule (gravity left): boundary == window LEFT edge, window fully in air, both sides equal. W1: both w6. W2: TR w6, bottom w30.
- Win: yellow in TR at w24 (b48, bar x48-49). Bottom would need w48 > total 36 => must be TR.
- Buttons (guess, pull INTO own section): TL-from-bottom (1,28); TR-from-bottom (25,28); bottom-from-TL (1,34); bottom-from-TR (25,34).
- MASTER PLAN (if q=3): (1,28) x1 [TL6], (25,28) x3 [TR24, bottom6], click (6,31) yellow->bottom; (1,34) x2 [TL0 bottom12], (25,34) x6 [TR6 bottom30], click (30,31) yellow->TR; (25,28) x6 [TR24 bottom12]. WIN.
- Probing quantum: (1,28) + (25,28).
- Actions 179-180: quantum=3 ✓, buttons confirmed. State TL6 TR18 bottom12, yellow bar x6-7 (at W1 doorway).
- Dispatching full solve (18): (25,28)x2 [TR24 bot6], click(6,31) [yellow->bottom]; (1,34)x2 [TL0 bot12], (25,34)x6 [TR6 bot30], click(30,31) [yellow->TR]; (25,28)x6 [TR24 bot12] => bar x48-49 = notch. WIN expected.

## Level 7 (score 6) — gravity UP, elevator middle, 3 figures
- Sections (depth rows from row8): TL x8-21 d20; M x24-39 continuous rows8-55 d8; TR x42-55 d6 (PURPLE fig); BL x8-21 rows32+ d8 (YELLOW); BR x42-55 rows32+ d10 (GREEN). Total 52. Timer row0.
- Liquid at TOP (gravity up); surface=bottom of liquid; bar = surface row(s) below; depth+row8-1 = last liquid row.
- Windows: right wall rows16-23 (M<->TR; doorway M=8,TR=8); left wall rows38-45 (BL<->M; BL=6,M=30); right wall rows38-45 (BR<->M; BR=6,M=30). NO window TL top.
- Notches: GREEN row18 left wall (G in M d10); YELLOW row26 right wall (Y in TR d18); PURPLE row50 left wall (P in BL d18).
- Buttons (pull INTO): TL(20,8) M-from-TL(25,8) M-from-TR(38,8) TR(43,8) BL(20,32) M-from-BL(25,32) M-from-BR(38,32) BR(43,32). q=2 expected.
- PLAN v3 (51 actions): a) (25,8),(43,8),click(40,16): P->M. b) (25,32)x1,(38,32)x2,(25,8)x8 [M30 BL6 BR6 TL2], click(22,38): SWAP P->BL, Y->M. c) (20,8)x11 [M8 TL24], click(40,16): Y->TR. d) (25,8)x11 [M30 TL2], click(40,38): G->M. e) (20,32)x6 [BL18], (43,8)x5 [TR18], (25,8)x1 [TL0 M10]. WIN.
- KEY: only ONE figure in M at a time (same-side doorway figures would swap/conflict); P down + Y up share one swap click.
- Dispatching step a (3 actions).
- Actions 199-201: step a SUCCESS (36f anim). q=2 ✓. P in M bar row16. TL18 M8 TR8 BL8 BR10, timer 63.
- Dispatching: step b = (25,32),(38,32)x2,(25,8)x8 [BL6 BR6 TL2 M30], click(22,38) SWAP P->BL Y->M; then (20,8)x8 [start of drain toward M8].
- Next call: (20,8)x3 more [TL24 M8], click(40,16) Y->TR; then step d,e.
- Actions 202-221: step b SWAP SUCCESS (54f): P->BL, Y->M. Drain partial: TL18 M14 TR8 BL6 BR6, timer 57. All on plan.
- Dispatching 20: (20,8)x3 [TL24 M8], click(40,16) Y->TR; (25,8)x11 [TL2 M30], click(40,38) G->M; (20,32)x4 [BL14 M22].
- FINAL call after: (20,32)x2 [BL18 M18], (43,8)x5 [TR18 M8], (25,8)x1 [TL0 M10] => WIN.
- Actions 222-241: FAIL — TL cap = 22 (rows 8-29 = 22 rows)! 3rd (20,8) no-opped => M was 10 not 8 => both clicks no-opped. Section caps: TL/TR 22, BL/BR 24, M 48.
- State: TL0 M24(Y bar32) TR8 BL14(P) BR6(G), timer 50.
- REPLAN: (20,8)x8 [TL16 M8], click(40,16) Y->TR; (25,8)x8 [TL0 M24], (25,32)x3 [BL8 M30] = 20 actions this call.
- NEXT: click(40,38) G->M; (20,32)x5 [BL18 M25->]; wait recompute: after G->M: M30. (20,32)x5: BL18 M20; (43,8)x5: TR18 M10. WIN. 11 actions.
- Actions 242-261: Y->TR SUCCESS (36f). TL0 M30 TR8(Y) BL8(P) BR6(G), timer 44.
- FINAL dispatch: click(40,38) G->M; (20,32)x5 [BL18 M20]; (43,8)x5 [TR18 M10]. Bars: P row50, Y row26, G row18 = all notches. WIN expected.
