# Level 6 (score 5, started action 262)
- Blue plus ctr (15,48) arm 12 (touch reach 13). Yellow SQUARE outline 19x19 (Chebyshev r9) ctr (48,15) = $ start. Off-white 8x8 ring rows 28-35 cols 28-35 (no center cell) — role UNKNOWN. No palettes.
- Boxes: blue (6,12),(9,9),(9,30),(27,12); yellow (30,45),(30,54),(57,45),(57,54).
- Brute force (mod-3, touch): plus max 2/4 blue, square max 2/4 yellow. UNSOLVABLE with known mechanics -> ring must matter (duplicate? resize? morph?).
- If ring DUPLICATES: blue pair-covers exist: plus (9,18) or (9,21) covers (9,9)+(9,30); plus (15,12)/(18,12) covers (6,12)+(27,12). Yellow: square cr=39 or 21, cc 44-55 (mod3: 45,48,51,54) covers row-30 pair via edge; (48,cc same) covers row-57 pair via bottom edge.
- Probe 263-265: cycle is 2-cycle square<->plus ONLY. Ring NOT a shape -> passive station/object. $ now on PLUS (15,48).
- Probe 266-271: RING = SOLID WALL + SHEAR MECHANIC. On Left at (30,48): H-bar blocked (tip col 36, ring (30,35)), V-bar moved to col 45 alone, $ stayed with H at (30,48). SHAPES ARE INDEPENDENT BARS: each bar moves 3/action unless its path hits ring cells (clips, stops before contact). Bars do NOT block on boxes or (assumed, strong evidence) other shapes.
- Ring cells: rows 28&35 full cols 28-35; r29/34: 28,29,30,33,34,35; r30/33: 28,29,34,35; r31/32: 28,35. Interior empty.
- FULL SOLUTION (sim-verified, all blocks k=0 immediate): state H(30,48) V(30,45) [plus active].
  Plus (23): L,U,L,D,D,D (shears: L blocks H -> V col42; D×3 blocks H at row27 via ring row28 -> V drops to (36,39)), then U×7 (H->(6,45),V->(15,39)), L×9 (V crosses ABOVE ring rows, H->(6,18),V->(15,12)), D×1 -> H(9,18) covers (9,9),(9,30); V(18,12) covers (6,12),(27,12).
  A5 (1) -> square. Square bars T(39,15) B(57,15) Lv(48,6) Rv(48,24), 19-long.
  Square (18): U×4 (T->27,B->45), R×2 (ec->21; Rv shears, blocked at col 27), D×3 (T blocked by ring row28 at cols 28-30; B->54), R×8 (T row27 slides free; ec->45; Lv/Rv rows 36-54 cross under ring), D×1 -> T(30,45) covers both row-30 yellows, B(57,45) covers row-57 yellows. CLEAR.
- Batch1 done (272-291): exact plan adherence. H(6,24), V(15,18). $ = virtual intersection (V.row, H.col) — confirmed both here and at first shear.
- Batch2 done (292-311): plus H(9,18) V(18,12) FINAL (all 4 blue covered). SQUARE MODEL WAS WRONG:
- SQUARE = RUBBER RECTANGLE, h+w conserved (=38 cells). When leading edge blocked, trailing edge keeps moving (shrink) and perpendicular dimension EXTENDS 3, alternating which side extends (observed T,B,T,B,T on horiz squeezes). 3 R-presses (309-311) stalled entirely at w=4 (min width? or extension side blocked: B ext would hit purple row 63, R at 27 vs ring col 28). Purple row 63 and board edges assumed solid.
- Shapes confirmed NON-BLOCKING vs each other (square T-edge passed through plus V-bar cells rows 28-30 col 12).
- Rect now rows 27-60 cols 24-27 ($ = rect center). TARGET: T30 B57 L45 R54 (28x10, h+w=38 ✓) — corners land exactly on the 4 yellow box centers. Crossing ring cols must happen at rows 0-27 (h=28 exactly fits above ring rows).
- Batch3 (312-331) FAILED to squeeze: BOARD EDGES CLIP, DON'T BLOCK (top edge slid off-board, h+w unchanged). Only the RING blocks/reshapes. Rect now T=-6(hidden) B=27 L=45 R=48. Off-board cells persist (L5 clipped arms precedent).
- Also: 309-311 stall likely = min dimension 4 (w could not shrink below 4).
- Batch4 sent (332-351): L×4 (cols 33-36, B edge over ring cols), D×2 (B pinned by ring row 28 -> h 34->28, w->10; extension guess L-then-R -> cols 30-39, T back to 0), R×5 (cols 45-54, crossing above ring rows), D×9. Then 1 more D -> rows 30-57 = corners on all 4 yellow centers. If extension alternation guessed wrong, cols off by ±3: recover with 1 L/R press (+1 D) at the bottom — paths verified free either way.

# Game mechanics (confirmed L1)
- Arrows move active shape 3 cells/action. ACTION5 (space) switches active shape ($ marks center).
- Goal: place each shape so its coverage lines pass through all same-colored box centers. Level clears automatically.
- Shape types: plus (covers row+col), X (covers diagonals), diamond (outline, radius 9 = cells at Manhattan dist 9? vertices on axes).
- Level 1 cleared in 20 actions (score 1).

# Level 5 (score 4, started action 185)
- Shapes: yellow X ctr (42,24) arm 11 ($ active); green diamond ctr (18,30) r9; orange plus ctr (33,55) arm 14 (right arm clipped).
- Boxes: blue (6,21),(6,39),(45,33),(51,24),(51,45),(60,33); red (27,51),(36,42); UNKNOWN-color (42,55),(33,58) centers hidden under orange plus arms.
- Palettes: yellow(3-8,3-8), lightblue(3-8,55-60), green(27-32,3-8), blue(52-57,3-8), red(52-57,55-60). NO ORANGE palette.
- Brute force over positions (mod-3), colors, hidden-color hypotheses: NO SOLUTION. An assumption is wrong (quantum? coverage semantics? maybe touching any box cell counts, not center).
- Probes: quantum 3 all shapes. Cycle X->DIA->PLUS. Plus is SYMMETRIC plus pivot now (30,54) arm 14 (I misread cols again).
- Boxes finalized: blue x6 (6,21),(6,39),(45,33),(51,24),(51,45),(60,33); red x3 (27,51),(36,42),(33,58). Q-BLOCK 3x3 at (41-43,53-55) ctr (42,54) = wall or hidden box.
- COVERAGE SEMANTICS: center-only unsolvable; assume TOUCH (shape cell in 3x3 box region counts). Solution (72 acts):
  1. PLUS(active): 10L (30,54->30,24), 8D (->54,24), 1L (54,21) horiz arm touches BLUE palette -> blue, 1U 4R -> (51,33). Covers blues C,D,E,F via row51/col33.
  2. A5, X: 3D (->48,24), 4L (->48,12) SW arm touches BLUE -> blue, 6R (->48,30), 11U -> (15,30). Covers A,B diagonally (d9).
  3. A5, DIA: 7R (15,30->15,51), 11D (->48,51) outline touches RED palette -> red, 4U -> (36,51). Covers (27,51) d9, (36,42) d9, (33,58) via TOUCH (33,57), q-block via (43,53).
- Batch1 done (191-210): plus BLUE at (51,21) ✓. (42,54) revealed = 4th RED box; diamond (36,51) covers its center (d9) ✓.
- Batch2 sent (211-230): 4R (plus->51,33), A5, X: 3D 4L (blue repaint at 48,12) 6R 2U.
- Batch3: 9×A1 (X->15,30), A5, DIA: 7×A4 3×A2. Batch4: 8×A2 (dia->48,51 red) 4×A1 (->36,51). Expect clear.
- Palette-touch hazards checked: plus stops lefts at c=24 (c=21 at row30 would touch GREEN); X descends col 24 then lefts at row 48 (col12 ok, NW arm clears green rows).

# Level 4 CORRECTION (action 119)
- I misread start pos: plus started (36,54) not (36,55). QUANTUM = 3 for ALL shapes, all levels. No per-shape speed.
- Palettes likely just a color legend (magenta shape <-> orange boxes etc), not stations.
- Solution valid: plus (15,36) -> (30,15) [5D,7L] all orange; X (24,24) -> (30,39) [2D,5R] all green.
- Action 139: plus at (30,15), X at (30,39) — boxes geometrically covered but NO CLEAR. Color match required.
- Sent 140-153: ACTION5 (to plus) + 8U + 5R -> plus center (6,30) in orange palette fill. Watch for repaint to orange.
- Action 153: REPAINT CONFIRMED — plus center entered orange fill, shape now orange. Palettes repaint on center-entry.
- KEY MECHANIC: repaint triggers when ANY cell of shape (arms included) overlaps a palette block (border # included). Last palette touched wins. X got repainted MAGENTA at (48,39) via down-left diagonal arm touching magenta fill (55,32)..(58,29).
- Plus is orange at (30,15) covering orange boxes, arms clear of palettes. ✓
- Sent 174-185: X (48,39) -> 3R (arm touches green fill at (48,45)/(48,48)) -> 6U -> 3L -> (30,39) green. Expect clear.
- Path verified palette-free on return. Watch for accidental repaints ALWAYS (check all 4 diagonal arms x10 + plus arms 13).
- LESSON: always parse $ position programmatically, never visually.

# Level 4 (score 3, started action 103)
- Magenta plus: center (36,55)=$, arm 13 (right arm clipped at edge). Light-blue X: center (21,24), arm 10.
- Boxes: orange (18,15),(30,27),(43,15) -> plus-cover ONLY at (30,15). Green (21,48),(24,33),(39,30) -> X-cover ONLY at (30,39).
- Palette squares (6x6, # border): top row light-blue(4-9,c4-9), orange(c28-33), maroon(c52-57); bottom row(54-59) yellow, magenta, green. Vertical pairs: (->G, -->C, >->I. Maybe color legend or repaint stations.
- Plus->(30,15) delta (-6,-40) NOT div by 3; X->(30,39) delta (+9,+15) IS. Sent probe ACTION3 to check movement quantum.
- Action 104 probe: plus moved 4 cells left (55->51). QUANTUM=4 for plus. Targets unreachable mod 4 for both plus (30,15) and X (30,39, needs 3s).
- Action 106: X quantum = 3 (moved 24->24... (21,24)->(24,24)). Per-shape: plus 4, X 3.
- Exhaustive search: NO joint plus+X cover of all 6 boxes under parity constraints. Palettes must matter.
- X target for greens: (30,39) reachable (2D+5R from (24,24)) IF color doesn't matter.
- Plus needs (30,15): row 30 ≡ 2 mod 4, unreachable (rows ≡ 0). Palette = repaint/teleport/speed-change theory.
- Sent 107-119: ACTION5 (switch to plus) + 7U + 5L -> plus center (8,31) inside ORANGE palette fill. Observe effect.
- Palette fills (rows 5-8 / 55-58): lightblue c5-8, orange c29-32, maroon c53-56 / yellow c5-8, magenta c29-32, green c53-56. Repaint-station theory still open.

# Level 3 (score 2, started action 56)
- All shapes RED, 8 red boxes. Shapes: H-line arm21 ctr (45,30)=player; X arm11 ctr (48,18); diamond r12 ctr (48,45).
- Solution: line->(6,27) [13U,1L] covers (6,6),(6,45); X->(24,42) [8U,8R] covers (15,51),(30,48),(33,33); diamond->(30,18) [6U,9L] covers (21,21),(27,9),(39,21). Total 45 moves+2 spaces.
- Action 71: line placed (6,27) OK. Cycle: line -> X. $ at (48,18).
- Action 88: X placed (24,42) OK. $ on diamond (48,45).
- Sent 89-103: diamond 6U+9L -> (30,18). Expect Level 3 clear (score 3) at action 103.

# Level 2 (score 1)
- Orange X: center (18,27) player, arm 11. Boxes (39,9),(42,24),(57,9) -> target (48,18) = 10 down + 3 left.
- Maroon diamond: center (30,39), radius 9. Boxes (3,21),(9,27),(12,12) -> target (12,21) = 6 up + 6 left.
- Blue plus: center (42,48), arm 13. Boxes (36,27),(48,15),(48,33),(60,27) -> target (48,27) = 2 down + 7 left.
- Action 34: orange placed (48,18) OK. Space cycle: orange -> maroon. $ now (30,39).
- Action 47: maroon placed (12,21) OK. Cycle order: orange -> maroon -> blue.
- Sent (48-56): blue 2D+7L -> (48,27). Expect Level 2 clear (score 2) at action 56.
- Row 63 bar: off-white 13 -> 9 during level 2. Possibly per-level step budget. Keep totals lean.
