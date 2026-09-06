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

Gallery 1's mark A (`design/estimated-mark-gallery.html`) is **not** the default: the owner asked
for something other than a teardrop-with-glyph (D39). Gallery 2
(`design/estimated-mark-gallery-2.html`) holds the candidates; take the one the owner names, or
its recommendation if no name is given, and record which.

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

_(qa and a11y appended when they land)_

From `design/interaction-audit-r7.md` (verified independently at the three call sites named). The
audit closed 29 of 39 previous items; these are what Round 8 owns. **Everything else on its punch
list is deferred to Round 9** so this round stays the size of its brief.

**5. Draw the dotted unknown halo on the map (N1, violation).** `renderPins` computes
`const match = m && m.state!=='unknown' ? m.state : null`, so the unknown state is deliberately
dropped and `match-unknown` renders zero times on the map, while `matchHalo('unknown')` already
draws the library's dotted sky700 ring correctly and the list view keeps a dotted carrier for the
same state. What stands in for it today is `.pinbtn.recede{opacity:.8}` — a 20% dim. Pass the
state through, and correct the legend line that currently *documents* the omission ("not yet seen
— no halo"). Reconsider whether `recede` should still dim once a positive mark exists.

**6. Give reduced motion a CSS floor (N2, structural).** There is no
`@media (prefers-reduced-motion: reduce)` rule in the file at all: the only media query is
`(max-width:767px)`, and the whole reduced-motion contract hangs on a `.phone.rm` class written by
`applyPrefs()`. Measured: first paint at 296ms, class applied at 388ms warm and **804ms cold** — a
92 to 500ms window in which an OS-reduce user gets the full motion system, with nothing underneath
if `applyPrefs()` ever throws. Either mirror the `.phone.rm` essentials in a real media query, or
set the class from an inline head script before first paint.

**7. Stop reduced motion deleting the scan's pacing (N3, structural).** `defer()` and `after()`
return 0 under reduce, so the scan runs **420ms instead of 7,439ms**, all three checks land at
once, and the `PROC_CHIPS+600` hold — whose own comment says it exists "so 'Checks complete' is
spoken before the screen changes" — is skipped. Reduced motion should drop the sweep, the scale
and the rotation, and keep the cadence and the announce-then-hold. As written, the clause that
protects screen-reader users is the one the setting turns off.

**8. Test clusters against pins in the collision pass (N4, violation).** Pin-to-pin overlap
respects the build's 10% rule (worst 0.100), but cluster-to-pin is untested: **43.3%** of one pin
is covered by a 48px cluster at overview, 21.0% of another at street. The mark that exists to
resolve density is creating it.

**Note for whoever measures Round 8:** this audit describes the Estimated mark and the confidence
dots as they were. Both change in this round, so re-measure the tier rows rather than carrying
these figures forward.

