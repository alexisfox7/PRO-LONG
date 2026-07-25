# Game notes

## Level 1 mechanics hypothesis (Action 0)
- Board has 4 sub-boards, each a 3x3 grid of 6x6 tiles (blue f / red n) with a center "signature" tile.
- Signature is 3x3 of 2x2 cells: '$'(white)=red tile, '#'(gray)=blue tile, center 'n'.
- TL/TR/BL boards: signature matches their own tile layout (worked examples).
- BR board (framed with q border, rows 32-63, cols 32-61) is the puzzle: all tiles blue, signature says target = [n,f,f],[n,·,n],[n,f,f].
- BR tile centers: rows 36-41/44-49/52-57, cols 36-41/44-49/52-57. Click centers ~(38|46|54, 38|46|54).
- Action 1-4: clicked (38,38),(38,46),(54,46),(38,54) → SOLVED, Score 1. Click toggles tile to signature color. No examples needed.

## Level 2 (after Action 4)
- Background q. Palette top-right: blue rows0-3, orange rows4-7 (cols 60-63) = the two tile colors.
- Two 3x3 grids sharing middle tile row: tile rows 14,22,30 (grid A) and 30,38,46 (grid B); tile cols 20,28,36. Sigs at (22,28) and (38,28), center '-' orange → $=orange, #=blue.
- SigA: $##/$-$/$#$ ; SigB: $#$/#-#/$$# ; shared row consistent ($,#,$).
- Actions 5-11: clicked 7 $ tiles: (22,16),(22,24),(38,24),(22,32),(38,32),(22,48),(30,48). Expect score 2.
- Tile centers: x=22/30/38 for cols 20/28/36; y=16/24/32/40/48 for rows 14/22/30/38/46.
- Actions 5-11 → SOLVED, Score 2.

## Level 3 (after Action 11)
- Diamond of 4 overlapping 3x3 grids on q bg; base tiles red n; palette red/orange top-right.
- KEY RULE REFINED: in a signature, '$' cells = the sig's CENTER-PIXEL color, '#' cells = the other palette color. (Level 3 sigs had centers 'n' or '-'; "always click $" gave overlap conflicts; center-color rule fully consistent.)
- Sig tiles: S1(12,28) cen '-', S2(28,20) cen 'n', S3(28,36) cen 'n', S4(44,28) cen '-'.
- Actions 12-25: 14 clicks toggling red→orange → SOLVED, Score 3.

## Level 4 (after Action 25)
- Palette (cols 60-63): f rows0-3, n rows4-7, '-' rows8-11 → 3 colors, likely click cycle order f→n→-.
- 3 grids: GA cen sig(22,20) center '-', rows y16/24/32 × x14/22/30; GB sig(22,36) center 'f', same rows × x30/38/46; GC sig(38,28) center '-', rows y32/40/48 × x22/30/38.
- Sigs: A=#$#/#-#/#$#, B=#$#/#f#/##$, C=$##/#-#/$$$.
- Rule with 3 colors: $=center color; # forced to RED by overlap consistency (GA# ∈{f,n}, GB# ∈{n,-} → n).
- TARGET (non-blue cells): red(n): (14,16),(30,16),(46,16),(14,24),(30,24),(46,24),(14,32),(30,32),(38,32),(22,40),(38,40); orange(-): (22,16),(22,32),(22,48),(30,48),(38,48). Blue stays: (38,16),(46,32).
- Action 26: probe click (14,16) → turned n. CONFIRMED cycle f→n→'-' (palette top-to-bottom order).
- NOTE: [settled] markers only appear on level transitions; normal post-action boards follow [POST-ACTION BOARD STATE] directly. Parse the LAST post-action block, not last [settled].
- Actions 27-46: 10 red singles + 5 orange doubles = 20 clicks → SOLVED, Score 4.

## Level 5 (after Action 46)
- 7x7 tile grid (tile (r,c): y=4+8r..9+8r, x=6+8c; centers y=6+8r, x=8+8c). Base green I; palette green/purple at cols 54-55 rows 0-7 (NOT a sig — exclude).
- NEW: sigs describe their own 3x3 NEIGHBORHOOD (sig at grid pos = map center). 'h'=non-paintable (absent or sig tile). $=center-pixel color, #=other. Fully consistent, zero conflicts.
- 3 magenta-checker (C/I) tiles = unset tiles; all constrained purple. Click behavior on them unknown.
- Actions 47-58: 12 clicks done. Score still 4 — CHK MECHANIC DISCOVERED:
- **CHK (checker) tiles are Lights-Out buttons**: clicking toggles the CHK's own color (green-checker ↔ purple-checker) AND all 4 orthogonal paintable neighbors. Plain tiles toggle only themselves (verified via per-action diffs).
- After actions 47-58: all 12 target-purple tiles correct (CHKs now purple-checker ✓), but CHK clicks flipped 9 neighbors to purple erroneously.
- Actions 59-67: revert (0,2),(1,1),(1,3),(3,1),(3,3),(4,4),(5,3),(5,5),(6,4) to green. Expect score 5.
- FUTURE: when CHK tiles present, plan click parity jointly (CHK click = vector toggling itself+neighbors).
- Actions 59-67 → SOLVED, Score 5. (Purple-checker counts as purple for win check.)

## Level 6 (after Action 67)
- 6x7 tile grid; tile (r,c): rows ys=[6,14,22,30,38,46][r], cols xs=[4,12,20,28,36,44,52][c]; click center = (xs[c]+3, ys[r]+3). Palette yellow G / green I.
- All plain tiles yellow with magenta dot at TOP-middle (uniform). Hypotheses: (A) all tiles toggle self+4 ortho neighbors; (B) dot=UP arrow: toggles self+tile above; (C) self only.
- Sigs: S(0,1) hhh/#Ih/$$#, S(2,4) #$#/$I$/$$#, S(3,2) #$$/$I$/#$#, S(5,5) #$$/hI#/hhh. Center I → $=green, #=yellow.
- TARGET green cells: (1,0),(1,1),(1,4),(2,2),(2,3),(2,5),(3,1),(3,3),(3,4),(4,2),(4,5),(4,6); rest yellow. All consistent.
- Paintable: (0,0),(1,0..5),(2,1;2;3;5),(3,1;3;4;5),(4,1..6),(5,6).
- Action 68: probe → toggled (4,3)+(3,3): CONFIRMED dot = UP arrow; click toggles self + immediate tile above (sigs/absent unaffected, no skipping assumed).
- Actions 69-82: chain-solved 14 clicks (simulated, matches target): (0,0),(1,0),(2,1),(3,1),(1,2),(2,2),(4,2),(3,3),(4,3),(1,4),(3,4),(3,5),(4,5),(4,6). Expect score 6.
- MECHANIC LIBRARY so far: plain tile=self toggle; full checkerboard C tile=self+4 ortho; top-dot tile=self+above. Marks on tiles encode toggle footprint.
