# Round 6 brief: the things a designer would fix before showing anyone

From `design/graphic-critique.md`, plus the QA and change audit when it lands. Written before
dispatch so nothing is lost while Round 5 holds the file.

Round 5 already owns: the brand mark, marigold as the action colour, restoring the Estimated
pin, the card's freshness and confidence tiles, the dark title bars, and the interaction spec's
20 violations. **Do not duplicate those.** Everything below is additional.

---

## Two visible rendering faults

**1. The selected pin paints on top of sheets.** Its lift z-index escapes the map's stacking
context, so a purple pin sits over the correction form's first select and over the empty-state
headline. Reproduces by walking the real flow, not only by jumping to a screen. This is the most
visible defect in the build and it is a stacking-context bug, not a z-index number to raise.

**2. Fifty-two identical estimated rings at default zoom.** Clustering exists and works, and is
only applied at the zoomed-out level. Eleven amber pins collide into a heap, and the legend
teaches a dashed-teardrop mark that appears nowhere on the default map. Round 5 restores the
correct Estimated artwork; this is the separate problem that clustering must also run at default
zoom.

## Demo scaffolding in shipped copy

`(staged for demo)` appears on the card's primary provenance row. `Open My Business (staged)` is
a visible label. This is exactly the class the product owner asked about: things the build should
not include. Remove the words; keep the behaviour honest by other means if a caveat is genuinely
needed.

## Components do not hold their shape across screens

The critique counted: **the tier badge has five treatments, the feature chips three layouts,
headers four patterns.** Round 3's consistency sweep worked property by property, which caught 20
classes of drift but could not see this, because each instance is internally consistent and only
differs from its siblings. This needs a component pass, not a property pass: one tier badge, one
feature chip, one header, used everywhere.

## The type scale is em-relative and compounds

The same body role renders at **14.25, 12.9, 12.667, 12.255, 11.7 and 11.467 pixels** on
different screens, because em steps multiply inside nested containers. Profile alone uses twelve
size and weight pairs. This is the invisible reason the build reads slightly less crisp than the
boards even where the layout is correct. Anchor the scale so a step means one size everywhere.

## The illustrations: four survive, three do not

- **Keep:** the door, saved, thanks and offline drawings.
- **`camera`** is a hubcap, not an aperture: six radii through the centre.
- **`street`** has a one-point-perspective ground under flat-elevation buildings, three pavement
  joints that share no vanishing point, a figure drawn in a different stroke weight, and — in a
  product called EntryMap — **no entrance**, with the marigold spent on an awning.
- **`map`** is off-family and mis-sells the product: it promises a blue rotated map when the app
  delivers a cream orthogonal one.

Also worth knowing: five of the seven are one hand, but three of those five are the same door
with different props, so the set has less range than its count suggests.

## The welcome screen

The aubergine decision is right and the execution does not yet pay for it. The screen earns brand
continuity, a real dark-to-light handoff and a status-bar solution, then spends half its height on
a logo shown for the third time in five seconds and a doorless skyline.

The critique's single suggested fix: re-tint the `street` drawing for the dark ground, run it
full-bleed, and give it one lit yellow doorway. That requires fixing `street` first, which is the
weakest drawing in the build and currently carries the first impression.

## The place card

The photographs win the eye over the verdicts. The Freshness and Confidence pair is coloured
asymmetrically for no reason. The library's feature icons are absent from the one screen most
users actually meet. The bottom slices a sentence.

---

## What the critique credited, and Round 6 must not damage

The trust ladder as a shape-first system that holds across all 26 screens. The My Needs sheet,
which improves on the board by adding a sub-line saying what each choice does. `ow-review`, an
invention with no board panel and the most professionally designed information screen in the
build. The Accessibility screen's self-demonstrating text-size control. And the zoomed-out map
ground, which reads more like Austin than the boards' cooler version.
