# Round 8 brief: make every mark on the map readable without asking, and remove the ones that are not

Assembled from the directive log's pass 3 (D36, D37, both decided by the owner at 21:40 on
2026-09-05) and from the three Round 7 re-audits, which are appended below as they land. One
implementer, alone, on `design/phone-app-prototype.html`. Do not start while any re-audit is
still measuring the file.

---

## 1. A new Estimated mark, with no dash (D37, option 1)

The library dashes both the Estimated pin outline (`pins/estimated.svg`, `7 6`) and the
partial-match halo (`halos/partial-match.svg`, `15 9`). Two meanings on one line style, shipped
side by side. The owner: "the dashes around the estimates and it also meaning partial is
confusing. maybe estimated needs a new icon?"

Draw a new Estimated mark. Constraints that already stand:

- Tier is carried by **shape and fill**, never by colour alone (3.1, the trust ladder).
- The outline stays sky700 `#1B6599`: the library's sky400 fails 1.16:1 on the block edge and
  2.02:1 on its own white fill (3.9). Re-measure the new mark on every ground tone in both
  contrast modes and print the table.
- The italic "i" glyph is part of the current asset; the confidence dots are removed (see §2).
  Decide about the glyph on evidence, not habit.
- Pin sizes per zoom stay on `pin-hierarchy.json`; a new silhouette must still read at 32px.
- Halos are untouched: solid good, dashed partial, dotted unknown. After this round, a dash on
  the map means partial match and nothing else.
- The legend row for Estimated is redrawn with the mark. Every place the old mark appears
  (legend, onboarding tier tiles, the trust ladder sheet, the card's tier badge, welcome screen
  tiles) changes together, or the ladder stops holding across screens (the critique's credit).

Deliver the mark as a gallery first if more than one candidate is plausible; the owner has asked
to see options before they land.

## 2. Take the confidence dots off the pins; teach the cluster count (D36 + D38)

The owner first chose to keep the dots and add a legend row (D36, option 1), then, looking at
the live map again: "the three circles above each icon is stupid" (D38). D38 wins.

- **Remove the three confidence dots from every pin at every zoom level**, in every tier and
  every state, and from every place the pin artwork is echoed (legend, onboarding tier tiles,
  the trust ladder sheet, the card's tier badge, the welcome tiles). A pin carries tier by
  shape and fill, match by halo line style, and nothing else.
- Confidence stays where it is explained: the card's Confidence tile and the pin's accessible
  name (`placeSentence()`). Nothing about the confidence *data* changes; only the pin stops
  drawing it.
- The `pinDots()` path and the library's dot geometry are removed from the build, not hidden,
  so a later round cannot switch them back on by accident.
- Add the **cluster row** to the trust legend: the numbered disc, "N places here — tap to
  open". The legend must stay one screen at the largest text size.
- Make the cluster disc's accessible name say what the number is, if it does not already.

The gallery's recommended mark A (`design/estimated-mark-gallery.html`) was drawn with hollow
dots because it predates D38; take A without the dots.

## 3. Score the two new criteria

Paste 5.x (every mark is taught where it is seen) and 5.y (one line style, one meaning) from
`design/directive-log.md` pass 3 into the rubric's map section and score them against the
result, with the measurements.

## 4. Do not

- Do not touch the match halos' line styles.
- Do not recolour any trust pin for selection, match, freshness or provenance.
- Do not adopt `estimated.svg` from either package; it is the asset being replaced.
- Do not widen into the re-audit findings below unless they are marked for this round.

---

## Round 7 re-audit findings marked for this round

_(appended when `qa-report-r7.md`, `a11y-audit-r7.md` and `interaction-audit-r7.md` land)_
