# Can other models make the screening more accurate?

Four candidates were run against the same 52 held-out entrances the vision model was
validated on, using the same photographs. Each was scored the same way: correct verdicts
over committed verdicts, with the tuning half kept separate from the held-out half so a
gain has to survive data the idea was not built on.

Only one of the four looked like it had earned a place, and the confirmation run
took it back. Nothing ships.

## The table

| Enhancement | What it adds | Tuning half | Held-out half | Cost | Verdict |
|---|---|---|---|---|---|
| **Monocular depth** (Depth Anything V2 small) | Reads the ground plane to catch steps the camera flattens | 84.6% → 100% | 88.5% → 96.2% | ~10 s/door, CPU, no API | **Drop** — did not survive the confirmation run |
| **Grounded crops** (OWL-ViT boxes) | Crops to the door and handle, then re-asks | 82.7% → 92.3% | 94.2% → **86.5%** | $0.0075 + ~60 s/door | **Drop** |
| **Text recognition** (RapidOCR) | Reads storefront signs to name the business | — | 66.7% precision, 34.6% recall | ~1 s/photo, no API | **Not on its own** |
| **Agreement gating** (two passes of the same model) | Commits only where two independent passes agree | — | 98.6% at 79.6% coverage | 2× the API cost | **Available as a dial** |

## Depth: the one that looked like it worked

Step-free entry was the weakest criterion, and it fails in a specific way. A platform poured
in the same concrete tone as the sidewalk looks flat head-on, especially when the photograph
is taken while standing on it. Colour and texture cannot separate those; geometry can.

A small depth model reads the ground plane and looks for an interior plateau, a riser face,
below the door. On the photographs it was measured with, it caught **all seven** of the vision
model's known step misses, and a control ruled out confidence arithmetic: flipping the vision
model's low-confidence verdicts with no depth involved gives exactly the baseline.

That result did not survive the confirmation run the recommendation itself asked for.

### The confirmation run

`eval/depth_steps_confirm.py`, results in `eval/out/experiment_depth_steps_confirm.json`.
Every number below uses the frozen parameters — aggregation, threshold, uncertain band and
the confidence gate — exactly as the earlier pass left them. Nothing was retuned.

| Slice | What is new about it | Vision alone | Gated fusion |
|---|---|---|---|
| Control: the original doors, the original two views | nothing — reproduction check | 89.5% (34/38) | **97.4% (37/38)** |
| The same doors, photographs the pass never read | new pixels, same entrances | 90.0% (18/20) | **80.0% (16/20)** |
| Doors the depth pipeline had never seen | new entrances | 85.7% (6/7) | **75.0% (6/8)** |

The control matters most. Re-running the frozen gate on its own cached inputs reproduces the
earlier run verdict for verdict, with zero mismatches, so the collapse in the other two rows
is not a reimplementation artefact. It is the finding.

**The 96.2% was a property of two photographs, not of the entrances.** Handed different views
of the *same* doors, the same gate lands ten points below the vision model it was meant to
improve. Six overrides fired: two fixes, four breaks.

**No parameter setting rescues it.** Sweeping the confidence gate from 65 to 90, with and
without the handrail veto, the best available fusion on the largest slice is 90.0% — reached
at the setting where no override fires at all. Every setting that lets depth act is worse
than leaving it out.

### Every new error, and which mode it belongs to

Two families, and neither is the pair the earlier write-up warned about.

**Depth misses real steps as soon as the camera stands back** — door-08, door-20, door-37,
door-56, door-58, all stepped, all scoring 0.000 on *every* wider view. At the two nearest
frames the riser spans enough rows to register; a metre further back it does not, and the
score falls to zero rather than degrading. Because the gate treats a committed "no step" as
grounds to override, this turns a correct vision verdict into a false step-free claim, which
is the worst error the product can make. door-08 and door-56 were broken exactly this way.

**One cluttered view poisons the door** — door-09, door-31, door-42, door-51, door-54, all
step-free, each with exactly one view scoring 0.26 to 1.00 and all its siblings at 0.000. The
culprits are a guard rail with parked cars behind it, an A-frame sandwich board, a raised
planter, and a paving seam running across the ground band. Aggregation is `max`, so a single
bad frame decides the entrance, and the false-positive rate therefore *rises* with the number
of photographs a user takes.

door-09 is the instructive one: the vision model calls a phantom riser there too, for an
unrelated reason. The two signals are not independent, so the gate does not catch it — it
corroborates it, and the entrance ends up wrong with two sources agreeing.

**The handrail veto was never real.** The gate as written above included "no handrails already
visible". That clause existed only in prose; it was not in the analysis code and had never
been measured. Implemented and measured here, it changes exactly one verdict on the unseen
doors. n=1 cannot carry it.

### What could not be tested, and why that is the whole story

The recommendation was to confirm on roughly twenty more entrances. There are not twenty.

All 64 entrances carry ground truth. Doors 13-64 were the two halves and are used up. Eighteen
are sealed. That leaves the twelve pilot entrances, four of which are sealed, so **eight**
genuinely unseen doors exist — and across all 64 entrances only thirteen have a step at all,
of which exactly **one** is both unseen and unsealed. The 2026-09-04 captures are all already
scored; there is no unscored capture anywhere in the set. No amount of care makes eight doors
and one step into a confirmation.

So the strongest honest evidence is the middle row of the table: the frozen gate, on new
photographs of already-held-out entrances. That is a fair test of the thing that actually
breaks — capture variation — and the gate fails it. A stronger verdict would need roughly
forty new entrances with a realistic share of steps, captured by someone other than the
person who shot the tuning set.

**Verdict: drop.** Not "needs more data" — more data is needed to *rehabilitate* it, but the
evidence in hand is not neutral. On the largest honest slice the gate is a ten-point
regression whose optimum parameter setting is "off", and its dominant failure is the one that
matters most. The finding is worth keeping: the ground-plane profile is real geometry and
works at close range on level ground. What does not work is letting it overrule a vision model.

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

Nothing ships into the engine. Two enhancements are dropped with evidence, one is repositioned
into the interface rather than the engine, and one becomes a product dial. Step-free entry stays
on the vision model alone, and the honest fix for it is more labelled stepped entrances, not a
second model overruling the first.

The broader lesson repeats what prompt tuning already showed, one level deeper. Prompt tuning
taught that gains measured on the half that shaped the idea did not survive the half that did
not. Depth passed that test and still failed, because a held-out *door* is not a held-out
*photograph*: the depth rule was validated on two frames per entrance, and it was those two
frames, not the entrances, that carried the result. Any future candidate that reads geometry
out of a photograph gets tested on views nobody chose for it before it is believed.
