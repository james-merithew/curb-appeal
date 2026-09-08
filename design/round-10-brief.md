# Round 10 brief: close what design can close, and name what it cannot

The owner: *"can we keep editing the live app to have everything done please?"*

So this round is a closing pass. The rubric sits at **3.8333 over 72 criteria**. The bar is nothing
below 3 and an average of 3.5 or better, and the average clears it — one criterion sits at 2 and
ten sit at 3. This round takes the ten that design can move, states plainly what the eleventh
needs, and stops guessing at the rest.

**Dispatch after the scan-overlay work (frontdoor #436) lands.** One writer holds this file.

---

## The items, each with what a 4 actually requires

### 1. Every mark is taught where it is seen (5.7, currently 3)

Round 9 added the cluster row and the confidence text. Two marks are still keyed nowhere:

- **the selection keyline** — the double ring that appears around a chosen pin
- **the lavender match disc** — the pale disc behind a pin that has a needs match

Both are drawn on the map and neither appears in the trust legend. Add them, or decide one of them
is decoration and record that decision rather than leaving it unexplained. The legend must still
fit one screen at the largest text size; if it does not, the confidence row is the one that yields,
because the card already explains confidence.

### 2. Pin tap targets are too close together (a11y, not yet on the rubric)

Measured at street zoom: **minimum centre-to-centre 28.9px, and 8 pairs under 44px**. At overview:
**22.7px, 19 pairs**. Each pin's own hit area is 48px, so the targets overlap, and a tap between two
pins is a coin toss. WCAG 2.5.8 asks for 24px minimum spacing; the build's own clustering rule was
supposed to prevent this and is measured on head overlap rather than tap-target distance.

Extend the collision pass to test **tap-target centres**, not just drawn heads. Round 9 fixed the
cluster-versus-pin case the same way, so the shape of the fix already exists in the file.

Add a criterion for it. A defect nothing scores is a defect that comes back.

### 3. The filter change is the last unimplemented feedback clause (9.9, currently 3)

The specification asks that affected pins crossfade over 180ms and newly relevant pins rise 4px
while their halos draw. The build re-renders the pin layer instead. It is one clause and it is the
only thing holding 9.9 at 3.

### 4. Text size reaches +26%, not 200% (a11y N14)

Three steps: 15 / 16.2 / 18.9px. WCAG 1.4.4 expects text to reach 200% without loss of content or
function. Round 9 proved the layout survives its own top step cleanly and that nothing clips at any
size, so the headroom exists. Add steps and re-measure the sweep that found zero clipped nodes.

If 200% genuinely breaks a screen, that is a finding worth recording with the screen named — but
find out rather than assuming.

### 5. The splash auto-advances with no control (a11y N18)

~1.2s, no pause, no way to extend, and reduced motion does not lengthen it. It carries no
information the user must read, so the harm is low, but it is timed content with no mechanism and
that is a WCAG 2.2.1 gap. Either give it a control, or make it advance on interaction with a
generous fallback.

### 6. The location pill clips at a 320px frame

Down from 38–63px to 1–15px after Round 9, and still clipped at the narrowest supported width. The
`aria-label` carries the full text so only sighted users at that width are affected. Finish it: let
the header wrap, or shorten the pill's own content at that breakpoint.

### 7. One shipped state is unreachable from the seeded data (9.11, currently 3)

`evidence-recheck` exists in full — "Could you take another look?", "Re-check entrance", "Maybe
later" — and **no seeded place in the prototype is old enough to reach it**. Note that the *served*
app does reach it (50 of 51 places are past the threshold), so this is a prototype-data gap, not a
product gap. Age one seeded place past the threshold so the state is walkable here too, and say in
the evidence that the two builds differed and why.

### 8. Line length: fix the criterion or fix the copy (1.3, currently 3)

The main reading column measures 52–68 characters, which is right. The median across all
paragraphs is **35**, because most paragraphs in this product are one or two lines by design — a
row label, a caption, a state sentence. A median over paragraphs that are shorter than one line
does not measure line length.

**This is probably a measurement that needs re-scoping rather than copy that needs rewriting.**
Decide, state the reasoning, and rescore honestly either way. Do not raise the score without
changing something.

### 9. Load animation (4.6, currently 3)

Held at 3 and defended: the map body and the splash body are both excluded by rule. Re-measure
against Round 9's new scan beats and the reduced-motion floor, and if nothing animates on load that
the user did not ask for, say so and score it 4. If the shutter wash or the processing sweep
introduced one, that is the finding.

### 10. The scan is a walkable sequence (8.1, currently 3)

Six beats exist and connect. Round 9 left two things named in the evidence as missing: the
**ring countdown** during processing, and the **published-screen mini map**. Build both or record
why not.

---

## What this round must NOT do

- **6.6** ("nothing is 100% verified") sits at **2** and no design round can move it. It needs an
  owner-confirmed entrance to exist in the data — a real business owner claiming a real door. Do
  not score it up, do not soften it, do not invent a rung. Leave it as the escalation it is.
- **6.7** (step-free) is engine work held on measurement, not design work.
- **6.8** (two surfaces) and **8.3** (home screen icon) are recorded and blocked on other people's
  tickets. Re-cite them if the evidence has moved; do not re-solve them here.
- Do not touch the honesty rules. No public negative verdict, `not_visible` is never `absent`, no
  trust pin recoloured for selection, match, freshness or provenance, and a dashed stroke on the
  map means partial match and nothing else.

## How to work

Measure, do not assert. Print the numbers for everything you change: contrast, spacing, durations,
counts of call sites. Re-measure the pin spacing after the collision change rather than assuming
the fix worked. Say explicitly what you did not do, and if a number comes out different from what
this brief predicts, print the real one — the brief has been wrong before and the implementer
catching it is the point.

Rescore every criterion you touch, in place, with evidence. Add the criterion for pin tap-target
spacing. Append a Round 10 entry to the log.
