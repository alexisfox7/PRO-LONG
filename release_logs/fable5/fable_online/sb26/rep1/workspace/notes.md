# Game notes

## CONFIRMED MECHANICS
- Top rows 0-7: target color sequence (ring icons).
- Click palette button (rows 57-60) = select (white border). Click slot = paint with selected color.
- Painting consumes palette color (gray stub remains). Clicking filled slot SWAPS:
  old color returns to palette at the position of the color being placed.
- Slot centers are FIXED: empty 2x2 and filled 4x4 share center. L1/L2 centers: x=22.5,28.5,34.5,40.5.
- Click zones are wide (~6px pitch) - aim at centers.
- Row 53 bar = step budget (64 cells), 1 cell per paint. Resets each level.
- Level clears automatically when all slots match target (score +1). ACTION5 probably not needed.

## Level 1: SOLVED (score 1). Used 14 actions (some wasted on hypothesis tests + misclick at (37,29) which hit slot3 not slot4).

## Level 2: SOLVED (score 2). Depth-first flatten hypothesis CONFIRMED.
No ACTION5 submit needed - clear auto-registers; score/transition appear one action later.

## Level 3: SOLVED (score 3).

## Level 4: SOLVED (score 4). Ring tokens placeable like colors.

## Level 5: SOLVED (score 5). Duplicate rings work: same panel referenced twice.

## Level 6: SOLVED (score 6).

## Level 7: SOLVED (score 7). Recursion is fully recursive (depth 2 worked).

## Level 8 (current, actions 113+)
- Target: TWO rows R,Y,O,B,G,P / R,Y,O,B,G,P = infinite repeat truncated at 2 rows.
- SELF-REFERENCE: redRing in palette; red main panel = [blueRing, G, P, redRing]
  f(red) = f(blue)+G+P+f(red) = RYOB GP RYOB GP... matches display.
- blue = [R,Y,O,B]. All 8 tokens used.
- Red slots row26 x22/28/34/40; blue row40 same x. Palette row58: P6,Y13,O20,R27,B34,G41,nRing48,fRing55
- Sent 16 actions.

## Level 7 (old)
- Target palindrome: R,B,G,Y,G,B,R. Two-level nesting:
  red=[Red,blueRing,Red] slots row16 x25/30/35
  blue=[Blue,greenRing,Blue] slots row29 x25/30/35
  green=[Green,Yellow(pre),Green] empties row42 x25/x37
- Palette row58: R6, B13, R20, G27, B34, G41, Iring48, fring55
- Sent 16 actions.

## Level 6 (old)
- Target: Blue,Yellow,Yellow,Orange,Purple,Purple,Green,Magenta,Magenta
- Main red panel 3 slots (12,18,24 @row22). Sub-panels pre-filled w/ own color in slot1:
  green(44,50@row22 empty), blue(18,24@row36), orange(44,50@row36)
- A=[blueRing,orangeRing,greenRing]; blue+=Y,Y; orange+=P,P; green+=M,M
- Palette row58: Y3, M10, P17, Y24, M31, P38, Iring45, fring52, -ring59
- Sent 18 actions.

## Level 5 (old)
- Target 9 icons: M,G,R,R,G,R,R,Y,P. TWO blue ring tokens = panel B referenced twice;
  B's contents count each time in flatten. A1=M, A2=ring, A3=ring, A4=Y, A5=P, B=(G,R,R).
- A row22 x19,25,31,37,43; B row36 x25,31,37
- Palette row58: P6, M13, R20, R27, Y34, G41, ring48, ring55
- Sent 16 select+paint actions.

## Level 4 (old)
- NEW: palette can contain RING TOKENS (panel references) to be placed by player.
  Solid 4x4 in panel = plain color; ring 4x4 = panel reference.
- Target: Yellow,Red,Green,Blue,Magenta,Orange,Purple
- A slots row22: 19,25,31,37,43. B: B1=solid Green pre-placed, B2(31,36), B3(37,36)
- Mapping: A1=Y, A2=R, A3=greenring, A4=O, A5=P, B2=Blue, B3=Magenta
- Palette: Yellow10, Magenta17, Orange24, Red31, Purple38, Blue45, GreenRing52 (row 58)

## Level 3 (old)
- Target: Red, Green, Purple, Yellow, Magenta, Blue, Orange
- Panel A (red): A1(19,23), A2=greenring, A3(31,23), A4=bluering, A5(43,23)
- Panel B (green): B1(19,35), B2(25,35); Panel C (blue): C1(37,35), C2(43,35)
- Flatten: A1,(B1,B2),A3,(C1,C2),A5
- Palette row58: Orange10, Green17, Purple24, Yellow31, Blue38, Magenta45, Red52
- Sent 14 select+paint actions.

## Level 2 (old)
- Target: Orange, Purple, Red, Blue, Green, Yellow, Magenta (7 colors)
- Panel A (red frame, rows 17-28): slots A1,A2 empty, A3=green ring (pipe down to panel B), A4 empty. Click row 22.
- Panel B (green frame, rows 32-41): 4 empty slots. Click row 36.
- NESTED STRUCTURE: green ring in A3 = reference to green-framed panel B.
  Hypothesis: depth-first flatten A1,A2,(B1,B2,B3,B4),A4 = target sequence.
  => A1=Orange, A2=Purple, A4=Magenta, B1=Red, B2=Blue, B3=Green, B4=Yellow
- Palette clicks: Red(10,58) Purple(17,58) Green(24,58) Orange(31,58) Magenta(38,58) Blue(45,58) Yellow(52,58)
- Sent 14 actions (7 select+paint pairs) at action 15+. All executed correctly (A15-A28).
- Board after A28: A=[Orange,Purple,ring,Magenta], B=[Red,Blue,Green,Yellow]. Palette empty.
- Score lags one header: completion at action N shows score bump at N+1 header, and new
  level board appears with action N+1. Sent ACTION5 probe (as after L1).
- OPEN QUESTION: is ACTION5 the required submit, or does clear auto-trigger?
