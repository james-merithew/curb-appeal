# Can other models make the screening more accurate?

Four candidates were run against the same 52 held-out entrances the vision model was
validated on, using the same photographs. Each was scored the same way: correct verdicts
over committed verdicts, with the tuning half kept separate from the held-out half so a
gain has to survive data the idea was not built on.

Only one of the four earned a place.

## The table

| Enhancement | What it adds | Tuning half | Held-out half | Cost | Verdict |
|---|---|---|---|---|---|
| **Monocular depth** (Depth Anything V2 small) | Reads the ground plane to catch steps the camera flattens | 84.6% → **100%** | 88.5% → **96.2%** | ~10 s/door, CPU, no API | **Ship, gated** |
| **Grounded crops** (OWL-ViT boxes) | Crops to the door and handle, then re-asks | 82.7% → 92.3% | 94.2% → **86.5%** | $0.0075 + ~60 s/door | **Drop** |
| **Text recognition** (RapidOCR) | Reads storefront signs to name the business | — | 66.7% precision, 34.6% recall | ~1 s/photo, no API | **Not on its own** |
| **Agreement gating** (two passes of the same model) | Commits only where two independent passes agree | — | 98.6% at 79.6% coverage | 2× the API cost | **Available as a dial** |

## Depth: the one that works

Step-free entry was the weakest criterion, and it fails in a specific way. A platform poured
in the same concrete tone as the sidewalk looks flat head-on, especially when the photograph
is taken while standing on it. Colour and texture cannot separate those; geometry can.

A small depth model reads the ground plane and looks for an interior plateau, a riser face,
below the door. It caught **all seven** of the vision model's known step misses.

The control matters more than the headline. Simply flipping the vision model's low-confidence
verdicts, with no depth involved, gives 88.5% on the held-out half, exactly the baseline. The
gain is geometry, not confidence arithmetic.

**Why it must stay gated.** A full flight of stairs renders as a smooth ramp in monocular depth,
scoring zero, which is the worst possible error for a step detector. Glass doors turn street
reflections into phantom ground. So depth may override only when it commits, the vision model's
confidence is below about 85, and no handrails are already visible. It runs in parallel with the
vision call, so the 15-second budget is untouched.

**Before it ships:** confirm on roughly 20 more entrances. Eleven stepped doors across both
halves is a thin base for a rule this consequential.

## Grounded crops: why it looked good and was not

Cropping to the door and handle before re-asking is an appealing idea, and on the tuning half
it delivered: 82.7% to 92.3%.

On held-out data it went backwards. Zero fixes, four new errors, all of them a true handle
being called absent. **Three of the four had no handle box at all**, so the model saw a
whole-door crop and committed to "absent" instead of abstaining. A narrower view produced a
more confident wrong answer.

A coverage gate, overriding only when a handle box actually exists, cuts the damage from four
errors to one, but the held-out half still lands at 92.3% against a 94.2% baseline. A gate that
only reduces harm without ever showing benefit is not a shipping case.

The tuning-half gains are suspect on their own terms: that run's target list was drawn from the
tuning half's own misses, so it was aimed at the answers. The box images are worth keeping as a
debugging aid, not as a scoring path.

## Text recognition: right idea, wrong job

Reading the sign to name the business is genuinely useful, but two thirds precision and one
third recall is not something to run unattended. Awnings, reflections and partial words defeat it.

It belongs inside the confirm step, not instead of it: the phone's location proposes nearby
businesses, text recognition helps rank them, and the person taps the right one. The real fix
for naming is location-constrained place lookup, which is what the app's scan flow now does.

## Agreement gating: a dial, not an improvement

Running the same model twice and committing only where both passes agree gives 98.6% accuracy,
but answers only 79.6% of the time. It does not make the model better; it trades coverage for
confidence at double the cost.

That is worth having as a product control rather than an engine default. It is the honest
mechanism behind a verified tier: the entrances that clear it are the ones two independent
readings agreed on, and the rest stay unclaimed rather than wrong.

Measured on the four criteria the study labels, independent passes disagree on **17.8%** of
cells, which is what the 79.6% coverage figure costs.

## What this changes

One enhancement ships, gated, on one criterion. One is dropped with evidence. One is repositioned
into the interface rather than the engine. One becomes a product dial.

The broader lesson repeats what prompt tuning already showed: gains measured on the half that
shaped the idea did not survive the half that did not. Every number above is reported on both.
