# Self-critique iterations — "THE DAY IN FRAMES" (news-image-20261117)

Each version was reviewed with Reza's verbatim prompt: "Review the results
you just generated. Identify 3–5 weaknesses, logical flaws, or areas that
can still be optimized. Then, create a much better and more robust version
based on those findings." The image was viewed at full size and at 300px
each cycle.

## v1 (compose.py first run) — entry.png 323,357 bytes, sha256 57721448…
- Viewed full-size + 300px. Composition reads as one image; date legible
  at 300px; all 12 panels photorealistic, no text in artwork.
- Weaknesses found:
  1. Masthead subline "24 STORIES · 6 CONTINENTS · ONE DAY ON EARTH" is
     struck through by the red rule (subline bottom 101px > rule at 96px).
  2. Four decks overflow the panel edge and clip: APEC ("…in Shenzhe"),
     Rwanda ("…asylum seeke"), measles ("…status"), chips ("…chips").
  3. Frame 07 crop cuts the top of the nurse's head (cy 0.45 too high).
  4. Frame 09 jets carry orange flame-like blobs on the wings — could be
     misread as jets on fire / shot down, which did not happen (faithfulness).
- Changes for v2: MAST_H 96→100, subline y 82→80; fit_font() auto-shrink
  for headlines/decks; decks 04/05/07/12 shortened; measles cy 0.45→0.52.

## v2 — entry.png 323,761 bytes, sha256 2e66322e…
- Viewed full-size. Subline clear of the rule; every deck complete; nurse's
  face fully visible.
- Weaknesses found:
  1. Frame 09 flame-like blobs remain — the one faithfulness risk left.
  2. Frame 10 (South Africa) is very dark, though police lights + tape
     still read.
  3. Nothing else material: all headlines/decks spelled correctly, no
     clipping, ticker complete, footer legible.
- Changes for v3: regenerated panel 09 with an explicit "no flames, no
  fire, no smoke trails, no damage" prompt; compose.py stem switched to
  panel-09-japan-v2; unused v1 panel file removed from the repo.

## v3 (FINAL) — entry.png 315,220 bytes, sha256 f4bc7074…
- Viewed full-size. Frame 09 now shows two clean intact jets in formation.
  All 12 headlines + 12 decks + 12 ticker lines spelled correctly, none
  clipped. Date "TUESDAY 17 NOVEMBER 2026" prominent. 300px preview:
  date + headlines legible, composition reads as one image.
- Review cycle finds no further material weakness: dark frame 10 is a
  mood choice, not a defect; ticker small at 300px is inherent to the
  dense class (all live top entries share it). Measured gain negligible —
  iteration stops here per the house stopping rule.
