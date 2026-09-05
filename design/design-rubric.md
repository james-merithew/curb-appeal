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
| 3.4 | Contrast passes on every text and non-text indicator, including in high contrast mode. | 3 | Broadly verified; awaiting the audit. |
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
| 5.6 | Nothing is ASCII-fragile: no raw glyph that breaks without the right charset. | 1 | Raw arrows and chevrons appear as literals. |

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

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 7.1 | Text contrast passes everywhere, in both normal and high contrast. | 4 | Swept all 26 screens: every failure is a decorative glyph, not content. Hero 6.74:1, amber 6.91:1. |
| 7.2 | Non-text indicators pass 3:1: toggle tracks, form borders, pins against the map, focus rings. | 1 | Toggle track 1.43:1, form borders 1.27:1, scanned pin 1.79:1. Focus ring 2.80:1, and high contrast makes it 1.23:1 because the override assumes a light background. |
| 7.3 | Every screen announces what it is when it becomes active. | 1 | 12 of 26 screens have no label; six scan-flow transitions announce nothing. |
| 7.4 | Focus moves sensibly on every screen and sheet change, and returns on close. | 0 | Focus lands on the document body after every transition. Sheets never receive focus, never trap it, never return it. |
| 7.5 | Blocked actions and errors are announced, not only shown. | 0 | Two publish gates fail silently: no announcement, no invalid state, no focus move. A working live region exists and is never called. |
| 7.6 | What is announced matches what is shown, at every moment. | 0 | The processing checklist announces all three checks complete before any has run. |
| 7.7 | Every state a sighted user gets from the map is available as text. | 2 | The list view is a complete equivalent, but match state never reaches the pin itself. |
| 7.8 | Keyboard alone completes every flow; Escape closes what it opens; nothing behind a scrim is reachable. | 1 | Escape is inert on all 8 sheets; 76 focusables stay reachable behind the scrim; 64 pins precede search in tab order. |
| 7.9 | Roles are correct and never destroy a native one. | 1 | `role="listitem"` on buttons in three screens destroys the button role. The list view does it correctly. |
| 7.10 | Reduced motion removes animation without removing feedback. | 4 | Every transition drops to near zero; the ring is replaced by a determinate bar, not frozen. |
| 7.11 | Text scaling to the largest setting clips nothing. | 4 | Verified across all 26 screens at both settings. |
| 7.12 | Touch targets meet 44x44 including expanded hit areas. | 3 | Near universal, two real failures. |


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
