# EntryMap design rubric

The bar: a product that looks like it was made by people who care, for people who are
usually given software that does not care. Not decorated. Considered.

Scored 0-4 per line. 0 absent, 1 present but wrong, 2 acceptable, 3 good, 4 nothing to add.
A round is finished when nothing sits below 3 and the average is 3.5 or better.
Every score needs a named screen as evidence. "Looks fine" is not a score.

Revision history lives at the bottom. Update the scores in place each round.

---

## 1. Typography

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1.1 | A real type scale, not ad-hoc sizes. Every size on screen traces to a defined step. | 2 | Sizes are largely em-based off one root but several one-off values exist. |
| 1.2 | Weight carries hierarchy. No more than three weights doing real work; 900 is not the default. | 2 | 900 is used very widely, which flattens emphasis. |
| 1.3 | Line length stays readable, roughly 45-75 characters for body copy. | 3 | Card and sheet copy is constrained. |
| 1.4 | Line height rises for body copy and tightens for display sizes. | 2 | Display text uses body leading in places. |
| 1.5 | Numerals align in tabular contexts (freshness, counts, distances). | 1 | No tabular-nums anywhere. |
| 1.6 | Letter-spacing tightens on display sizes and opens on small caps labels. | 3 | Wordmark and kickers do this. |

## 2. Hierarchy and layout

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 2.1 | One clear primary action per screen; secondary actions visibly subordinate. | 3 | Welcome and card follow this. |
| 2.2 | Spacing follows one scale; no arbitrary gaps. | 2 | Mixed values, mostly a 4px grid but with strays. |
| 2.3 | Related things are grouped by proximity before they are grouped by a box. | 2 | Several boxes do work proximity could do. |
| 2.4 | The eye reaches the most important thing first on every screen. | 3 | Card and map are clear; some settings screens are flat lists. |
| 2.5 | Density suits the job: the map is calm, the card is informative, settings are scannable. | 3 | Holds. |
| 2.6 | Optical alignment where geometric alignment looks wrong (icons in rows, pin tips). | 2 | Not deliberately handled. |

## 3. Colour and depth

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 3.1 | The palette carries meaning, and meaning only. Blue estimated, marigold scanned, purple owner, green match, amber ageing, no red. | 4 | Enforced throughout and tested. |
| 3.2 | No screen is monotone; each has a considered accent relationship. | 3 | Welcome fixed; some settings screens are still lavender-on-lavender. |
| 3.3 | Elevation is consistent: the same surface level always reads the same. | 2 | Shadows vary between sheets, cards and pills. |
| 3.4 | Contrast passes on every text and non-text indicator, including in high contrast mode. | 4 | Measured Round 1: text was already clean; every non-text indicator now clears 3:1 in both modes (see 7.2). |
| 3.5 | Colour is never the only carrier of state. | 4 | Tiers carry shape, match carries text. |

## 4. Motion

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 4.1 | Motion explains a relationship: where a thing came from, where it went. | 2 | Sheets and screens mostly cut or fade. |
| 4.2 | Durations are consistent and short: roughly 150-250ms for UI, longer only for narrative beats. | 2 | Values vary widely. |
| 4.3 | Easing is consistent and physical; nothing linear except progress. | 3 | Mostly one curve. |
| 4.4 | The processing sequence is the one deliberate narrative moment and it earns its length. | 4 | The self-drawing ring with named checks. |
| 4.5 | Reduced motion removes animation without removing meaning or feedback. | 4 | Verified: ring becomes a static bar. |
| 4.6 | Nothing animates on load that the user did not ask for. | 3 | Splash only. |

## 5. Craft details

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 5.1 | Empty states say what to do, not that something is empty. | 3 | Saved empty state does this. |
| 5.2 | Loading, offline and permission-denied states are designed, not default. | 3 | The states screen exists. |
| 5.3 | Touch feedback on every interactive element. | 2 | Buttons scale; rows and chips mostly do not. |
| 5.4 | Icons share one grid, weight and terminal style. | 2 | Stroke widths vary between 2.2 and 2.4. |
| 5.5 | Copy is plain, specific and human; no jargon, no cheerfulness the moment does not earn. | 4 | Consistently strong. |
| 5.6 | Nothing is ASCII-fragile: no raw glyph that breaks without the right charset. | 4 | All 405 non-ASCII characters converted: HTML entities in markup, a CSS escape for the one `content:` glyph, `\uXXXX` in JS strings (entities would be double-escaped by `esc()`), plain ASCII in comments. The file is now byte-for-byte ASCII and renders identically. |

## 6. Product truth

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 6.1 | No public negative verdict anywhere, in any state. | 4 | Held through the owner surfaces. |
| 6.2 | Every claim shows its evidence and its date. | 4 | Provenance stack. |
| 6.3 | Trust tier is never a filter, and never granted by a source that did not earn it. | 4 | Enforced. |
| 6.4 | Nothing implies measurement or legal compliance. | 4 | Vocabulary holds. |

## 7. Accessibility behaviour

This product is for disabled people. A defect here is a product defect, not a checklist miss.
Content accessibility and behavioural accessibility are scored separately because this file
is strong at the first and weak at the second.

All Round 1 evidence below was measured in the browser at 390x844, served over
`python -m http.server`, on the working copy as committed.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 7.1 | Text contrast passes everywhere, in both normal and high contrast. | 4 | Unchanged and not regressed. The decorative glyphs that were the only failures (`>`, `->`, the transparent tick) are now `aria-hidden`, and the two that stay visible were raised from 2.62:1 to 4.6:1. Checklist pending text went 2.47:1 -> 6.34:1 (`--faint` on the ground). |
| 7.2 | Non-text indicators pass 3:1: toggle tracks, form borders, pins against the map, focus rings. | 4 | Every indicator the audit measured now passes in **both** modes. Normal / high contrast: toggle track 3.37 / 6.66, form and chip borders 3.37 / 6.66, dot outlines 3.37 / 6.66, scanned-pin rim 5.04 / 8.04, estimated-pin stroke 3.59 / 8.09, progress track vs ground 3.29 / 3.02, progress-arc rim vs track 3.39 / 3.39, nav current-tab bar 9.62 / 13.25. Four tokens (`--edge`, `--track`, `--marigold-edge`, `--ring-rim`) carry all of it. |
| 7.3 | Every screen announces what it is when it becomes active. | 4 | All 26 screens now carry an `aria-label` (12 had none) and `tabindex="-1"`; `showScreen()` moves focus onto the screen, which is a labelled region, so the name is announced by the focus move. Walked all 26: `focusIsScreen: true` on every one. |
| 7.4 | Focus moves sensibly on every screen and sheet change, and returns on close. | 4 | Screen change: `document.activeElement` is the new screen on all 26 (was `BODY`). Sheet open: focus lands on the sheet heading (`H3.sheet-h`; the card sheet lands on `H2.card-name`). Sheet close: focus returns to the opener - Filters FAB after Escape, and the originating **pin** after the card closes, re-found by id across the re-render. `closeSearch()` returns focus to `#search-btn`. A nav token abandons the restore if the app navigated instead. |
| 7.5 | Blocked actions and errors are announced, not only shown. | 4 | `toast()` now routes through `announceUI()` - every toast reaches `#sr-announce` (verified: region text matches toast text). Submit claim unchecked: screen holds, `aria-invalid="true"`, `aria-describedby="claim-authz-err"`, inline error shown, focus on `#claim-authz`, announced "Claim not submitted...". Publish with the face-flagged photo (from both `ow-photos` and `ow-review`): inline error naming photo 3, `aria-invalid` on the publish button **and** on the Crop control, focus on Crop, announced. Checking the box / cropping clears all of it. |
| 7.6 | What is announced matches what is shown, at every moment. | 4 | The transparent tick is `aria-hidden` in all three places (`.ci-dot`, `.p-ring`, `.tl-dot`). The checklist is a real list whose per-item state text is written by `setCheckState()` at the moment the class lands. At t=0: "Doorway framed - not checked yet ..." (was "tick Doorway framed tick Entry path visible tick Photo quality checked"). Sampled through a full run: **zero** frames where announced-done != visual-done. |
| 7.7 | Every state a sighted user gets from the map is available as text. | 4 | One `placeSentence()` now feeds both the list row and the pin. 64/64 pins name their match state: "Royal Blue Grocery. 241 W 3rd St. Scanned on-site. Good match, 3 of 3 needs. Seen 2 days ago. 300 ft. Seen: Step-free entry, Wide door, Easy-grip handle, Clear approach." Was "Royal Blue Grocery - Scanned on-site". |
| 7.8 | Keyboard alone completes every flow; Escape closes what it opens; nothing behind a scrim is reachable. | 4 | Escape closes the search overlay and all 8 sheets. With a modal sheet open: `aria-modal="true"`, background `inert` (live regions exempted), **0** focusables reachable outside the sheet (was 76), Tab trapped. Tab order on the map: search, list toggle, zoom, locate and both FABs at indexes 1-9, then a "Skip the 64 map pins" control, then the pins (first pin at index 10; was index 0 with 64 pins ahead of search). Scan flow walked with real Tab presses: primer -> Close scan -> Allow camera -> capture -> Cancel scan -> Capture photo. No element anywhere in the app has a click handler without a native control under it (swept: 0 non-native clickables), so Enter/Space activation is the UA's. |
| 7.9 | Roles are correct and never destroy a native one. | 4 | 0 `button[role="listitem"]` in the document. Saved, My scans and My corrections are `UL role="list"` > `LI` > `BUTTON`, matching the list view. Seven labelled `<div>`s got a real role; 0 remain. The non-modal card sheet is `role="region"`, not `dialog`. Freshness is a labelled group with `aria-pressed`; the claim result is a `radiogroup` of `radio`s with a roving tabindex, arrow keys and a visible tick. |
| 7.10 | Reduced motion removes animation without removing feedback. | 4 | Re-verified after the changes: sheet, checkitem and ring transitions all 1e-05s, `#ringwrap` `display:none`, the determinate bar at 100%, all three checks landed, "Checks complete. 3 features identified." still announced, checklist text agrees. |
| 7.11 | Text scaling to the largest setting clips nothing. | 4 | Top step raised from 17.4px (+16%) to 18.9px (+26%). Swept all 26 screens at Default, Larger, and Larger + high contrast: the set of overflow findings is **identical** across all three and every entry is a `.sr-only` element or clipped map geometry - no visible text clips. The toast, the one failure in Round 0, now wraps: 358px wide, 3 lines, `scrollWidth == clientWidth`. |
| 7.12 | Touch targets meet 44x44 including expanded hit areas. | 4 | The two failures are fixed. `#card-grip` 390x44 (padding grew, the 5px grip bar did not). `#search-clear` keeps its 34px disc with a `::before{inset:-5px}` hit area: all four `elementFromPoint` probes at +/-21px hit the button. |


---

## Round log

**Round 0 (2026-09-05).** Baseline scored after the screen packs were folded in, the
welcome screen was rebuilt on the logo canvas, and a full screen-reader audit was run
(design/a11y-audit.md: 10 blocking defects, 18 improvements, 11 confirmations).

Average across all 44 criteria: **2.61**. Twenty-two criteria sit below 3.

Two distinct gaps, and they are not the same kind of problem.

*Craft.* Meaning, copy and honesty score 4s: the product's thinking is finished. What is
missing is that four systems exist informally and are applied inconsistently — type scale,
spacing scale, elevation scale and motion scale. That is a tractable, mechanical fix.

*Behaviour.* The accessibility scores split hard: content 4s, behaviour 0s and 1s. Everything
a screen reader is *told* is excellent; everything it should be told *when something happens*
is missing. Screen changes announce nothing, focus is dropped on every transition, two publish
gates fail in total silence, and the processing checklist announces success before any check
has run. On a product for disabled people this outranks every craft item.

Order of work: accessibility behaviour first, then the four design systems, then motion.

---

**Round 1 (2026-09-05).** Accessibility behaviour. All ten blocking defects in
design/a11y-audit.md closed, plus fifteen of the eighteen improvements and the ASCII sweep.

Recounted the sheet while scoring: there are **45** criteria, not 44, so the Round 0
figures restate as 2.53 average with 21 below 3. On that same count, Round 1 is
**2.53 -> 3.22**, and criteria below 3 go **21 -> 12**.

*What moved.* Section 7 went from an average of 1.75 to 4.00 and is the first section
with nothing below 3. The three that mattered most:

- **Silent refusals (7.5, 0 -> 4).** `toast()` now announces through the live region that
  was already there and never called. Both publish gates render an inline error beside the
  control that blocks them, mark it invalid, describe it, move focus onto it, and announce.
  The refusal is now the same event in both channels.
- **Screen changes (7.3/7.4, 1 and 0 -> 4).** Every screen has a name and takes focus. A
  keyboard user no longer restarts at the document top 26 times; a screen-reader user is
  told which screen they landed on.
- **The lying checklist (7.6, 0 -> 4).** The tick is out of the accessibility tree and the
  announced state is written when the check lands. Sampled across a full run there is no
  moment where the two channels disagree.

Also closed: match state, freshness and distance now reach the pin itself (7.7); sheets get
focus in, a trap, Escape and focus return, with nothing reachable behind the scrim (7.8);
the three row lists stopped destroying their buttons' role (7.9); every non-text indicator
clears 3:1 in both modes, including the focus ring on the two dark screens where high
contrast had been making it worse (7.2, 1.23:1 -> 15.76:1); both touch-target failures
(7.12). 5.6 went 1 -> 4 with the ASCII sweep and 3.4 went 3 -> 4 on the measured contrast.

*What did not move.* Nothing in sections 1, 2, 4 or 6 was touched this round, by design —
the type, spacing, elevation and motion scales are still informal, and that is the next
round's work. Fifteen of the eighteen improvements closed outright; three are only partly
closed and are named here rather than claimed:

- **I5 (headings).** Every screen that had none now has an `<h1>` and the section labels are
  real `<h2>`s, but `.chips-title` inside the card and the sheets is still a `<div>`, so
  heading navigation within a card is still shallow.
- **I6 (the capture coach).** It no longer interrupts every 1.7s — `aria-live` is gone and
  it announces once on entry — but the visible chip still rotates, so WCAG 2.2.2's pause
  mechanism for auto-updating content is not there.
- **I15 (200% text).** The app's own top step went +16% -> +26% and clips nothing at any of
  its three settings, but a real 200% root is a layout project, not a token change.

The `[proc]` `console.log` instrumentation stays: it is a development aid, not an error, and
the console is otherwise clean.

*Verification limit worth recording.* The browser pane could not synthesise Enter or Space
key activation, so keyboard *activation* is evidenced structurally — a sweep found zero
elements in the app with a click handler and no native control under them — rather than by
observing a keypress fire a handler. Focus movement, tab order, Escape and the trap were
all driven with real key events.
