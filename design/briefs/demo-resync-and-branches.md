# Re-sync the walkthrough onto Round 14, and add the three branches

Two jobs in one pass, because both touch the same file and the second is pointless
before the first.

---

## Job 1: the re-sync

`design/demo-app.html` was copied from `design/phone-app-prototype.html` at commit
**632455c** (Round 13). The prototype is now at **4c2dcd7** (Round 14). The demo build
therefore has none of Round 14, and Round 14 is precisely the round that fixed the
things the owner complained about from his phone.

**Method:** re-copy the prototype at 4c2dcd7, then re-apply the three walkthrough
blocks. That is the whole reason the layer was built as three appended blocks rather
than edits threaded through the file. Take the blocks from the current `demo-app.html`
so the drag, collapse and content-avoidance work comes with them.

**This is not a straight re-copy, because Round 14 moved things the route points at.**
Re-verify every one of the 22 targets. The ones known to have moved:

- **The nav bar no longer exists on the capture screen.** Round 14 removed it
  (`display:none` plus `inert`) and docked the shutter at the Scan ring's exact pixel
  row -- `--capture-floor:36px`, the ring's centre measured at a constant 74px above
  the frame bottom on all five sizes. Step 9 rings `#btn-shutter`; confirm it still
  resolves and that the ring lands on the docked position, not the old in-flow one.
- **Step 8 goes `#nav-scan` then `#btn-allow-cam`.** `#nav-scan` still exists on the
  map screen. Confirm the hand-off into `scan-primer` still works with the nav bar's
  new conditional display.
- **The map's zoom model changed completely.** `zoomedOut` and `ZOOM_OUT_K` are gone;
  `mapK` is a continuous multiplier clamped 0.40-3.30 with stops at 1.0 and 2.2. Step 4
  rings a specific pin chosen deterministically. Re-derive that choice against the new
  model and confirm the pin is not clustered away at the frames the owner will use.
- **`.vf-media` is new** and now carries the viewfinder's `overflow:hidden`. Any
  placement logic that walked up to `.viewfinder` for a clipping box now has a
  different ancestor. This is the one most likely to break silently.
- **The welcome screen scrolls now**, with docked actions. Step 1 rings `#ob-guest`.
  Round 14 fixed the defect where it was unreachable at 320x568 / 200%. The layer had
  a message for that case; check whether it still needs one.
- **`.review-img` gained a 200px floor** -- it rendered 0px tall at five frame/step
  combinations. Step 11 sits on that screen.

Re-run the whole twelve-step route on the re-synced build before touching Job 2.

---

## Job 2: three optional branches

The owner asked for the walkthrough to cover more: *"the personal aspect, community,
business, setting preferences, the accessibility features"*. He also said *"Keep it
around 1-2 minutes"*. Both hold, so the extra material is **optional branches, not
extra spine.**

The core route stays exactly twelve steps and about 100 seconds. Three branches sit
beside it, each 3-4 steps and 20-30 seconds, each entered on demand and returning to
where it left. He runs the core; if the room asks, or he has time, he branches.

### The entry point

A control on the HUD -- next to the step counter, in the same discreet register -- that
offers the branches available from the current screen. It must not be reachable by
accident mid-run, and it must never be the thing that blinks. The blinking target is
always the core route's next step.

Decide and state whether a branch can be entered from any step or only from the map.
My instinct is only from the map, because that is where all three naturally begin and
because a branch entered from inside a sheet has nowhere clean to return to.

### Branch A -- Business

The owner flow. Claim a door, confirm what is there. Real targets:
`#btn-claim` -> `claim-find` -> `claim-confirm` -> `claim-track`, or the owner screens
`ow-overview` / `ow-edit` / `ow-photos` / `ow-review` / `ow-published`. Pick the
shortest path that shows a business owner asserting something about their own entrance,
because that is the top rung of the ladder and the demo never otherwise shows it.

Worth knowing: `door-11` (Jo's Coffee) is the only Owner-confirmed place in the seeded
data, and it clusters away at mobile frames -- so the core route never shows an
Owner-confirmed receipt. This branch is where that gap gets closed.

### Branch B -- Community

Corrections and contributions. A place card -> `[data-act="correct"]` ->
`#sheet-correct` -> send -> `screen-corr-done`, and `screen-contrib` with its two tabs.
The point this branch must land: **a correction never changes a verdict.** It marks the
place as needing another look and it reaches a person, not a form. That is the answer
to "what if you're wrong about someone's business", and right now the demo asserts it
in the script without ever showing it.

### Branch C -- Accessibility

`screen-a11y`: text size, high contrast, reduce motion. Show the app actually changing.
This is the branch with the most force in the room, because it is an accessibility
product demonstrating that it is itself accessible -- and because the walkthrough layer
survives all three settings, which is worth seeing rather than claiming.

The step that lands it: turn text size up and let the interface reflow on screen. Do not
narrate it. Let them watch it work.

---

## Constraints that carry over unchanged

- **Three appended blocks, nothing else.** The app's own lines stay untouched. Prove it
  with a diff summary against 4c2dcd7.
- **Zero non-ASCII bytes.** Measured, rubric 5.6.
- **Never `preventDefault`.** Capture-phase listening; the app's own handlers navigate.
- **`pointer-events:none`** on everything except the callout itself, which is now
  draggable. An off-script tap must still reach the app.
- **Reduced motion replaces animation, never shortens it.**
- **Claims discipline.** No accuracy number. Never "compliant", "verified", "absent".
  Never that a place is accessible or inaccessible -- two public states, scanned
  on-site or not yet checked. Never that step-free entry is assessed: the engine reads
  four criteria, ramp or bevel, handrails, accessible door hardware, accessibility
  signage.
- **The script.** `design/demo-script.md` gains a block per branch step, in the same
  shape, with each branch's runtime stated separately from the core's. State the core
  total and each branch total, measured at 150 wpm, not estimated.

## Done when

- [ ] The re-synced build carries every Round 14 change, proven by diff against 4c2dcd7.
- [ ] All 22 core targets re-verified against the new build; any that moved are named.
- [ ] The twelve-step core route still runs end to end, still about 100 seconds.
- [ ] Three branches run and return cleanly to where they were entered.
- [ ] Branch entry is discreet, unreachable by accident, and never the blinking target.
- [ ] Drag, collapse and content-avoidance survive the re-sync.
- [ ] Runtimes measured and stated separately: core, and each branch.
- [ ] Anything that could not be re-verified is named rather than assumed.

---

## Job 0, which comes first: what the design critic found

A critic ran the whole route at 390x844 and again at 320x568 / 200%, tapping the real
targets. Its verdict: *"a good prototype with two or three finished parts, not a
finished product"*, and the reason governs this pass:

> Every measurement the brief asked for passes -- the ring lands after the transition,
> the callout never covers its own target, nothing clips at 200%, contrast clears the
> floors. And the run still looks unfinished, because the properties that were measured
> are not the properties that carry the impression. Nobody measured "does the callout
> cover the thing this step is about", and the answer is yes on eight of twelve steps.

**Do not touch these. They are finished and they were hard.** The settle discipline (the
ring goes dark during a transition and returns only after the target's rect has been
identical for three frames -- never once caught painted on a moving element); the
two-part ring that stays legible on five different grounds because one member always
carries; `hitAt()`'s five-point test with strict-centre-to-choose and lenient-to-keep;
and the `SCALES` ladder that makes 200% at 320x568 decent rather than merely unclipped.

### 1. The callout is a caption pretending to be a tooltip. Fix that first.

It measures **366 x 74.5px -- max width, two lines -- on eleven of twelve steps**. It
never shrinks to its content because every line in `STEPS` wraps at max width. A
97%-of-frame opaque strip with a 12px nub, placed 10px from its target, will cover
something almost every time, and `placeCall()` cannot know: its only constraints are
"not the target" and a four-item `KEEPOUT`.

Measured collisions, each landing on the thing its own step is about:

| Step | What it covers |
|---|---|
| 1 | `#ob-signin` entirely -- the opening frame hides the primary CTA |
| 2 | the **Cane or walker** row, while the line reads "Choose what matters" |
| 3 | the **Estimated** row, while paraphrasing its definition (the owner found this one) |
| 4 | the place name's descenders at the peek stop |
| 5, 6 | the photo strip and the top band of both photographs |
| 7 | the **freshness** control entirely, on the filters step |
| 8 | the privacy sentence -- the one sentence that screen exists to say |
| 10 | **"Entry path visible"**, under a line reading "watch what it names" |
| 11 | the **Clear approach** chip and the fourth criterion, on the four-criteria step |
| finish | the `SEEN AT THIS DOOR` chips -- the run ends by covering the product |

**Shorten every line to fit one line.** The original brief capped on-screen text at a
2-3 word title plus one line of ~90 characters and said anything longer belongs in the
script; that cap was not held. Then let the box size to its content, and give
`placeCall()` a real keep-clear region per step rather than a global four-item list.

Also: the callout's default `--ui-lavender-1` surface with a `--ui-lavender-2` hairline
**disappears into the app's own furniture** on every light screen, because the app is
already made of pale rounded cards with hairline borders. The critic noted the
high-contrast variant -- white with a 2px indigo900 border -- is a *better object*. Take
the hint.

### 2. Give the ring one shape.

`radiusOf()` inherits the target's computed radius, so the run contains five ring
shapes: a rounded rect around a row, a rounded rect **around a teardrop pin**, a
full-bleed rect whose verticals are clipped off both screen edges (`#card-grip` measures
390px wide on a 390px frame, so what you see is two horizontal rules reading as a border
on the sheet), a capsule around a text line, and a circle.

Step 4 is the worst and it is the money shot: a squarish violet box around a marigold
teardrop that already carries a dashed circular halo, with the box's bottom rule running
across the pin's tip. `round:true` exists in the step schema and is used only at step 10.
Pins want it -- better, a circle concentric with the pin *head*, ignoring the tip.

### 3. Two colour collisions, neither with the map.

- **Against the app's own secondary button.** The visual language mandates "white with a
  purple border" everywhere. At steps 1 and 5 the ring lands on one, giving **two
  concentric violet rounded rectangles 5px apart** -- a mis-registered border, not a
  highlight.
- **Against marigold.** Steps 8 and 11 draw a violet rect around the circular marigold
  Scan control and the marigold Publish button. Violet-boxing the product's one reserved
  action colour is the loudest wrong note in the run.

Solve both. A ring that adapts -- or an inset treatment on controls that already carry a
keyline -- is likely better than one that always paints outside.

### 4. Step 10 is the weakest moment in the run.

Nothing is tapped for 7.9 seconds. A violet ring pings outward every 1.2s around a
control that cannot be pressed, **on top of the app's own self-drawing progress ring** --
which the visual language calls the strongest motion in the product. Two concentric
rings, one of them insisting. The app's `#ringwrap` also shifts 8px at t~3.2s, so both
twitch once mid-stillness.

Drop the ring at step 10 and let the app's own ring be the star. Move or dock the
callout below the check rows. If a mark is wanted, make it static -- there is nothing to
press.

### 5. The pulse is a metronome, not a breath.

A single outward ping with a 360ms dead hold, ~83 across a 100-second run, never
resting. And it is aspect-distorted: `scale(1.12)` on a 366x48 box grows it 22px
horizontally and 2.9px vertically, so on wide targets the "breath" is a stretch. Slow it,
cut the amplitude, and make it a uniform-radius glow rather than a scaled box.

### 6. Step 6 frames the wrong rung.

The ring lands on `"Austin Transit Partnership - Scanned on-site"` under a caption
reading **"The ladder ends at owner-confirmed."** `pickPin()` prefers `door-11` (Jo's
Coffee, the only Owner-confirmed place) and lands on `door-09` every run at 390x844. The
in-file comment argues the line is about the ladder, not the place; that does not survive
a viewer reading the ringed text. Open an Owner-confirmed card deterministically at step
4, or move the ring off the tier line and change the line to something the artifact
supports.

Related: two of twenty-one taps are theatre. `#rcpt-body p.sheet-p` is body text and
`#mini-map` is `aria-hidden="true"` with no click handler -- the tap does nothing in the
app, and the route advances only because the layer saw the click. Everywhere else a ring
means "press this".

### 7. The smaller ones, all measured

- **The callout never fades between steps.** `retarget()` removes `.on` from the ring but
  never from `#wt-call`, so the enter/exit transitions run once, at step 1. Twelve hard
  cuts of a full-width card teleporting. The `--ease-exit` branch is dead code.
- **A flash at the 10 to 11 boundary:** `scan-review` active with the ring still at step
  10's geometry for one sample, clearing in ~250ms.
- **Ten of twenty-one taps change nothing on screen** except the ring hopping. Step 1
  repeats its line verbatim across a full screen change -- seven seconds of a
  hundred-second run where the layer says nothing new.
- **Fallback copy is tooling voice:** "This step is waiting for its control", "Use the
  chevrons". If one appears on stage the fiction breaks. Product voice, or nothing.
- **Six non-ASCII bytes** at lines 9266, 9270, 9436, 9439, 9541, 9603 -- em dashes, curly
  quotes, and two glyphs. The markup uses the entities correctly and the JS overwrites
  them with raw characters. Rule 1 of the addendum is measured at zero.
- **Step 11 quotes `"Not seen"`**, which is not one of the sanctioned phrasings and not
  what the app says ("Not yet seen from these photos"). Quoting words the product does
  not use, on the step about how the product words things.
- **Steps 2 and 7 will read as a reversal** -- "It changes the match shown, not which
  places appear" against "Filters change what you see". Both true; make the distinction
  legible or drop one.
- **`done: noSheet` is a state, not an event.** Steps 6c and 7b advance the instant no
  sheet is open, guarded only by a 380ms lock, so an off-script route closing both sheets
  can skid forward at ~2.6 steps/second. Require the predicate to have been false at
  least once since `retarget()`.

### The bar for this pass

The critic named three as the difference between a demo his peers watch and one they
read the seams of: **the callout small enough to stop hitting content; one ring shape,
off marigold and off step 10; and step 6 not framing "Scanned on-site" under a caption
about owner-confirmed.** Those three are the pass. The rest is polish and should also
land, but not at their expense.

---

## Two owner directives that override parts of this brief

Both arrived after the brief was written. Where they conflict with anything above, they win.

### 1. "It can be longer too."

The 1-2 minute cap is lifted. The core route may run longer than 100 seconds.

**Read this correctly, because the obvious reading makes the build worse.** It does not
mean more words per callout. The critic's central finding is that the callout is a
366px band covering app content on eight of twelve steps, and it is that size *because
every line wraps to two lines at max width*. Longer runtime spent on longer lines would
make the single worst problem worse.

It means **more steps, each still one short line.** Where a step is currently carrying
two ideas in two wrapped lines, split it into two steps with one line each. Where the
route skipped something because of the budget, put it back. The per-callout cap stays:
a 2-3 word title and one line short enough to render on **one** line at the default text
size on a 390px frame -- measure it, do not estimate it.

A good target is 16-20 core steps at 2 to 2.5 minutes. Do not pad to reach it, and do
not cut a flow to stay under it. State the measured runtime.

### 2. Drag is out. It shrinks, and he brings it back.

The owner, having run the build with the drag in it:

> "the movable pop up explainers are cumbersome to deal with. id rather the shrink and
> i can hover to see it again or something"

**Remove the drag entirely.** A partial drag implementation is in the file now (roughly
333 lines were added on top of the 9,608-line build, carrying `pointerdown` handlers and
a `folded` state). Strip the drag; keep and rebuild the fold as the primary behaviour.

**The behaviour to build instead:**

- The callout appears at full size when a step begins, sized to its content, and is
  readable without any action.
- It **folds on its own** to a compact chip after a short dwell -- long enough to read
  one short line, no longer. Pick the dwell by reading the line aloud at 150 wpm and
  adding a beat, and state the number and the reasoning.
- It also folds **immediately, without waiting**, if at full size it would cover the
  region the step is about. That is the per-step keep-clear region item 1 of Job 0 asks
  for; the fold is what makes it always satisfiable rather than a placement puzzle with
  no solution on a small frame.
- **Hover on a pointer device, press-and-hold on a touch device, re-expands it**, and it
  re-folds on release. A plain tap toggles it open and shut, because press-and-hold is
  not discoverable on its own and he will be on a phone.
- The chip has **one home**, not a floating position. The critic's complaint that the
  callout "never establishes a home, so the eye has to re-find it twelve times" is fixed
  by the fold, not despite it -- give the chip a consistent dock and the eye learns it
  once. Choose the dock so it never collides with `#navbar`, the shutter, or the HUD, and
  say where you put it and why.
- The chip must say enough to be worth glancing at. A bare dot is not it; the step's
  2-3 word title probably is.

**This replaces the tap-to-collapse from the previous brief** -- same idea, but folding is
now the default state rather than an escape hatch, which is the actual change.

Accessibility: folding is a state change, not a transition, under reduced motion. The
chip is a real button with an accessible name, focusable, and Enter/Space expand it. The
full text stays in the DOM for a screen reader whether folded or not -- folding is
visual. Do not put the only copy of anything behind a hover.

---

# RESCORE AND ROUND LOG - re-sync onto Round 15, the fold, and the three branches

Scored against the running build, not against the diff. Every figure below was taken
from `design/demo-app.html` served over http and driven by Playwright
(`design/_wt-drive.py` + `design/_wt-measure.js`, `design/_wt-a11y.py`), at 390x844
unless stated. The Browser pane cannot be used for this: its rAF stops the moment the
pane is not the fronted view, and the layer's whole tracking loop is rAF, so a probe
run there reports a frozen layer as a broken one.

## One correction to the brief, carried out

The brief says re-sync onto `4c2dcd7` (Round 14). Superseded: the re-sync is onto
**`8c8644c` (Round 15)**. Two facts the brief could not have known followed from it:
`#legend` is no longer a control (the tier card became a 179x48 pill, `#key-toggle`,
shut by default), and the demo build in the tree was already on Round 14, not Round 13.

## Done when

- [x] **The re-synced build carries every Round 15 change, proven by diff.**
      `diff 8c8644c:design/phone-app-prototype.html design/demo-app.html` is exactly
      one hunk: `9840a9841,11185`. 1,345 appended lines, nothing above them touched.
      `design/phone-app-prototype.html` in the worktree is byte-identical to `8c8644c`.
- [x] **All core targets re-verified; the ones that moved are named.** See the target
      table in the round report. Two were deleted from the route as theatre
      (`#rcpt-body p.sheet-p`, `#mini-map`), one was replaced (`#legend` ->
      `#key-toggle`), and five are new (`#key-toggle` x2, `#key-cta`, `#locate-btn`,
      a numbered cluster disc).
- [x] **The route runs end to end.** 24 core stops, 0 stuck, 0 page errors, at
      390x844, at 320x568 with 200% text, under Reduce Motion and under High Contrast.
- [x] **Three branches run and return cleanly.** A 6 stops / 49.5 s, B 8 / 49.6 s,
      C 6 / 31.7 s, all 0 stuck, all returning to the core stop they were entered from.
- [x] **Branch entry is discreet, unreachable by accident, never the blinking target.**
      `#wt-more` is hidden except on `screen-map` with no sheet open (measured true on
      the map, false inside a sheet); no step in any route names it.
- [x] **Drag removed; the fold rebuilt as the default state.** No `pointerdown`
      dragging remains. Auto-fold after the dwell, immediate fold when the expanded
      card would cover the step's subject, hover / press-and-hold / tap / Enter / Space
      all measured.
- [x] **Runtimes measured and stated separately.** Core 158.8 s; A 49.5 s; B 49.6 s;
      C 31.7 s; all four 289.6 s.
- [x] **Anything that could not be verified is named rather than assumed.** See "What
      is not done" in the round report.

## Job 0 - the critic's findings

1. **Callout sized to its content, off the subject.** Was 366 x 74.5px on eleven of
   twelve steps and covering the subject on eight of twelve. Now: **0 of 24 stops wrap
   to more than one line** and **0 of 20 stops with a declared subject overlap it at
   all** at 390x844 default text. Expanded it measures 132-295 x 38-56px against the
   old fixed 366 x 74.5; folded it is 80-172 x 37.8px. Surface changed to white with
   a 2px indigo900 keyline (the old high-contrast variant), as the critic suggested.
2. **One ring shape.** Radii across the run: `16px` on 15 stops, `50%` on 7, `999px`
   on 1 (a capsule traced in inset mode). Never inherited except in inset mode, where
   the ring *is* the control's edge. Pins get a circle on the pin head.
3. **Colour collisions.** Marigold targets (`#btn-allow-cam`, `#btn-shutter`,
   `#btn-publish`) draw white-then-indigo900, never violet, and never over the
   marigold: measured `--wt-ink: var(--indigo900)` on all three. Keylined secondary
   buttons draw one 3px violet band *inside* their own edge, so no second rectangle
   appears outside them.
4. **Step 10 is now step 22 and has no ring.** `ring:false`; the callout docks below
   the checklist, clear of `#ringwrap`, `.checklist`, `#proc-chips` and
   `#proc-caption`. The app's progress ring has the screen to itself.
5. **The pulse.** A uniform box-shadow spread, 2600ms with 46% of the cycle at rest,
   replacing `scale(1.12)` at 1200ms. No transform, so no aspect distortion, and no
   second hard rectangle.
6. **Step 6 no longer frames the wrong rung.** The core route makes no owner-confirmed
   claim at all: measured at 390x844 the map draws 10 pins and 8 discs and **zero**
   standalone Owner-confirmed pins, so the claim was unsupportable. Branch A shows the
   owner-confirmed receipt instead. Both theatre taps are gone.
7. **The smaller ones.** Callout fades between steps (`.on` now removed in
   `retarget()`); `done` predicates must read false once before they can fire;
   fallback copy rewritten in product voice ("Further down", "Out of view", "Just a
   moment"); the `"Not seen"` quotation is gone; steps 2 and 7 split into four steps
   that cannot read as a reversal; **zero non-ASCII bytes in the whole file**, measured
   (the previous build had 21 bytes on 6 lines, not 6 bytes).

## The bar

The critic named three as the difference. All three are met and measured: the callout
no longer hits content (0 of 20), the ring has one shape vocabulary and is off marigold
and off the processing step, and nothing in the route frames "Scanned on-site" under a
caption about owner-confirmed.

**Bar met at 390x844 with default text.** It is *not* fully met at 320x568 with 200%
text, and that is stated rather than hidden: 19 of 25 samples wrap to two lines there,
5 of 20 stops overlap their subject (worst 25%), and 7 stops show a scroll or fit hint
instead of their own line. Those are frame-and-text-size facts, not placement bugs -
the type scale ladder and the fold are what keep that frame usable at all - but a
reader running that configuration will see a different quality of run.
