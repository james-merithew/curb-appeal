# The guided walkthrough — build brief

The owner, in his own words, across six clarifications:

> "it must be merged within the duplicate app, not just be a set of cards"
> "i want it to essentially have animated things that pop up and point to things and explain
>  and i basically can keep clicking on what it wants me to do"
> "maybe after i click thing 1, thing 2 begins to blink or do something. then i click 2 and
>  something happens on the app, then thing 3 starts blinking"
> "no. the script is separate"
> "POLISHED IS IMPORTANT"
> "it basically should walk through most things and be stunning. intuitive for me and
>  everyone, has additional things to explain"
> "Keep it around 1-2 minutes. should incorporate user flows and ui/ux, and other details."

He will be live, screen-sharing his phone, reading the spoken script aloud while his peers
watch. He taps what blinks. That is the whole interaction.

---

## The two deliverables

**`design/demo-app.html`** — a WORKING duplicate of `design/phone-app-prototype.html` with a
walkthrough layer added. Every screen, every flow, every gesture still works. It is the app,
not a slideshow of the app.

**`design/demo-script.md`** — the spoken narration, one block per step, timed. Not on screen.

---

## The budget: 1 to 2 minutes

**Twelve steps. Six to nine seconds each.** That is the constraint that decides everything
else. On-screen text is a *label*, not a paragraph — a title of two or three words and one
line of at most ~90 characters. The sentence he SAYS is longer; it lives in the script.

If a step needs more than one line on screen, it is two steps or it is script-only.

---

## The route — twelve steps, covering the flows and the interface decisions

Each row: where it starts, what blinks, and the point it must make. The on-screen line is the
implementer's to write inside the character budget.

| # | Screen | Target (real selector) | On-screen point |
|---|---|---|---|
| 1 | `ob-welcome` | the continue control | The promise: access is knowable before you arrive |
| 2 | `ob-needs` | a need chip, then `#btn-needs-apply` | It filters by **your** need, not one wheelchair icon |
| 3 | `screen-map` | `#legend` | Three tiers. Shape and fill carry the tier — colour is never alone |
| 4 | `screen-map` | a pin (`.pinbtn`) | Tap a door. The card rises to the thumb, not the top of the screen |
| 5 | `#sheet-card` | the "how we know" / receipt control | Evidence, date, confidence — never a rating |
| 6 | `#sheet-receipt` | the tier line | The ladder stops at Owner-confirmed. There is no rung above it |
| 7 | `screen-map` | `#fab-filters` or `#fab-needs` | Non-matching places recede. Nothing is ever marked as failing |
| 8 | `screen-map` | `#nav-scan` | The scan: the same control, continuing |
| 9 | `scan-capture` | `#btn-shutter` | The guide is the doorway. Put the doorway inside it |
| 10 | `scan-processing` | the processing beat | ~7 seconds. The hard part is knowing when NOT to read it |
| 11 | `scan-review` | `#btn-publish` | Four criteria. "Not visible" is an answer, not a failure |
| 12 | `scan-done` / map | the new pin | Two public states: scanned on-site, or not yet checked |

**Verify every selector against the file before you use it.** The table above was read out of
the build, but a selector that has moved is a step that silently does nothing. If a target
does not exist, say so in your report and pick the nearest real one — do not invent markup in
the app half to make the walkthrough work.

Steps 2 and 4 involve a choice (which chip, which pin). Pick one deterministically and blink
exactly that one, so the route is identical every time he runs it.

---

## The mechanism

**A layer, not a fork.** Add exactly three things before `</body>`: a `<style id="wt-css">`,
a `<div id="wt">`, and a `<script id="wt-js">`. The app's own 8,900 lines are not edited.
The layer finds the active screen by observing `.screen.active`, and finds its target with
`document.querySelector`. It listens in the **capture** phase so it sees a tap before the app
handles it, and it never calls `preventDefault` — the app's own handler does the navigation.

**Advance rule.** A step ends when its target is tapped, OR when the screen changes to the
next step's screen (so an off-script route that lands in the right place still resyncs).
After advancing, wait for the next screen to settle (`requestAnimationFrame` twice, or the
existing transition duration) before drawing the next ring — a ring on a moving element is
the single thing that will make this look unfinished.

**It never fights the user.** The scrim panels and the callout are `pointer-events:none`.
Every tap in the app still works, on-script or not. If he wanders, the layer waits on the
current step and re-anchors when the target reappears.

**Recovery.** A discreet step counter ("4 / 12") with a back chevron and a skip, in the top
corner, out of the way of everything. If a target vanishes for more than ~2s the callout says
so quietly rather than pointing at nothing.

---

## What "stunning" means here, concretely

**The ring.** A double keyline around the target's real bounding box, inset to hug it —
`--violet600` inner, white outer halo, so it reads on both the dark map chrome and the light
sheets. It pulses on a 1200ms ease, scale and opacity only. This is chrome, not a map mark:
say so in a comment, because violet is Owner-confirmed on the map and a reader will ask.

**The callout.** Small card, `--lavender100` surface, `--indigo900` ink, one hairline of
`--lavender200`, a real arrow pointing at the target. It flips above/below by measured room,
never overlaps the target, and never covers `#navbar` or the shutter. Enters at
`--dur-base` on `--ease-enter`, leaves on `--ease-exit`.

**Progress.** A 2px violet rule across the very top, filling 1/12 per step. Nothing else.

**Reduced motion.** No pulse — a solid ring. No callout transition — it appears. The route
still works identically.

**Contrast.** Measure it. Callout ink on its surface, ring against the dark map ground AND
against a light sheet, progress rule against the header. 7:1 for text, 3:1 for the ring, both
contrast modes. Print the numbers in your report.

**Text size.** The callout must survive 200% text on a 320x568 frame without clipping and
without covering its own target. This is the thing Round 12 got wrong by measuring an
element against its own box instead of its parent's — measure the parent.

---

## The script, `design/demo-script.md`

Twelve blocks matching the twelve steps. Each block:

- **the step number and what he taps** — so he never has to look for it
- **what he says** — 15 to 25 words, written to be spoken, timed at ~150wpm
- **a beat of silence** where the app is doing something (processing, a sheet rising)

Then a header with the total runtime, and a short "if it goes wrong" section: what to say if
a tap misses, and the one-line answer to "so is this ADA-compliant?".

**Claims discipline is absolute.** From `docs/pitch.md`, and these are the ways this pitch
stops surviving its first sceptical question:

- Never an accuracy number. What exists is an *agreement* figure against a reference another
  model produced from the same photographs. "About seven seconds" is safe — it is latency.
- Never "compliant", "ADA-compliant", or "meets code".
- Never that a place IS accessible, and never that one is INACCESSIBLE. Two public states:
  scanned on-site, or not yet checked. Both say how we know, not what we concluded.
- Never that step-free entry is one of the things it checks. The interface names it; the
  engine does not assess it yet. Four criteria: ramp or bevel, handrails, accessible door
  hardware, accessibility signage.
- Do not quote a map size from a document. Read the count off the map on the day.

---

## Done when

- [ ] Twelve steps run end to end, each advancing on its own target's tap.
- [ ] Walked at 150wpm the script lands between 60 and 120 seconds. State the measured number.
- [ ] Every app flow still works with the layer present — including the ones off the route.
- [ ] The ring never lags a screen transition; the callout never covers its own target.
- [ ] Reduced motion, 200% text at 320x568, and both contrast modes all measured, numbers printed.
- [ ] No claim on screen or in the script violates the list above. Quote each line you wrote
      that touches a claim, next to the rule that permits it.
- [ ] `design/demo-app.html` differs from `design/phone-app-prototype.html` ONLY by the three
      added blocks. Prove it with a diff summary.

## Not in this ticket

Changing the app. Narration on screen beyond the one-line label. Audio. Video capture.

## Note for whoever syncs this later

`demo-app.html` was copied from `phone-app-prototype.html` at commit 632455c. Round 14 is
editing the prototype concurrently. Re-copy and re-apply the three blocks when Round 14 lands;
that is why the layer is three appended blocks and not edits threaded through the file.

---

## Addendum: five rules from the canon that this layer will trip over

Added after the brief was written, from a full read of the token library and the rubric.

**1. Zero non-ASCII bytes.** Rubric 5.6 is measured, not aspirational: the file carries no
non-ASCII byte outside base64 payloads. Your callout copy, the step counter and the back
chevron must all be ASCII or drawn as SVG. No em dashes, no arrows, no typographic quotes.
The app already replaced fourteen dingbats with drawings for exactly this reason.

**2. "Verified" is a banned word.** So are "compliant", "absent", and any verdict language
about a place. Where the app says a thing did not appear, the sanctioned phrasings are
"not spotted in this scan", "couldn't confirm yet", and "Not yet seen -- be the first to
scan." Wording is about time and evidence, never about the place.

**3. There is no red in this product, at all.** If you reach for an alert colour, stop. The
walkthrough has no error state that needs one.

**4. The ring's colour needs a decision, not a default.** `--violet600` is Owner-confirmed on
the map AND the partial-match halo; `--marigold400` is the scan action. The existing selection
idiom is `--ring-select: inset 0 0 0 2px var(--purple)` plus a white keyline and an indigo
outer line. Reuse that idiom rather than inventing a colour, and write the one-line reason in
a comment. Whichever you choose, it must clear 3:1 against the dark map ground and against a
light sheet, in both contrast modes.

**5. Motion tokens, current values.** `--dur-base:220ms`, `--dur-screen:260ms`,
`--dur-sheet:320ms`, `--ease-enter:cubic-bezier(.2,.7,.2,1)`,
`--ease-exit:cubic-bezier(.4,0,1,1)`. Sheets take 320ms to snap and 260ms for a screen
transition -- that is what "wait for it to settle" means in real numbers. `linear` is
permitted on progress and nothing else, so the progress rule may use it and the ring may not.
Rubric 4.5 asks that reduced motion REPLACE animation rather than shorten it: the ring
appears in its final state, it does not pulse quickly.

Note also: `design-systems-spec.md` carries pre-Round-4 weights (600/800/900) and em-based
sizes. The current values are the prototype's own anchored `calc()` steps off `--root-fs:15px`
and weights 500/650/800. Take tokens from the build, not from that spec.
