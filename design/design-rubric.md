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
| 1.1 | A real type scale, not ad-hoc sizes. Every size on screen traces to a defined step. | 4 | Round 2: 177 selectors mapped onto the spec's 8 steps. **0** literal `font-size` values in `em` remain anywhere in the file (was 29 distinct values). The 8 remaining `px` sizes are exactly the spec's legitimate set: the 15px root and its two `[data-textsize]` overrides (16.2 / 18.9), the text-size picker's own 14/17/20 preview (it must not scale with the setting it controls), the 13px desktop stage caption outside the phone, and `.street-label` at 10.5px, the one deliberate non-scaling piece of content type because the map geometry is computed in px. The eight steps are also authored once as `.t-display` &hellip; `.t-micro`. |
| 1.2 | Weight carries hierarchy. No more than three weights doing real work; 900 is not the default. | 4 | Round 2. CSS: **0** literal `font-weight` values remain; three tokens carry everything &mdash; `--fw-display` 900 on **21** component declarations (plus the 8 `.t-*` step classes), `--fw-strong` 800 on 112, `--fw-body` 600 on 71. 700 is gone from the stylesheet. Measured in the browser over all 26 screens on every text-bearing leaf element: weight 900 went **234 of 506 (46%) &rarr; 95 of 565 (17%)**, 800 went 82 &rarr; 281, 700 went 170 &rarr; 4 (and those 4 are the UA bolding `<b>`, not a rule). 900 now appears only on the wordmark, the eight heading steps, the one primary action label per screen, and the three headline numbers (`.counter-line`, `.tile .t-value`, `.ow-tierline`). |
| 1.3 | Line length stays readable, roughly 45-75 characters for body copy. | 3 | Unchanged. Body sits at `--fs-body` 14.3px / `--lh-body` 1.5 in a 358px content column: 52-68 characters. |
| 1.4 | Line height rises for body copy and tightens for display sizes. | 4 | Round 2: leading is named at every step and applied with the size, never left to inherit `normal`. Display 1.0, h1 1.1, h2 1.15, h3 1.22, body 1.5, sub 1.45, meta 1.35, micro 1.25, plus `--lh-row` 1.3 for one-line row labels that may wrap to two. |
| 1.5 | Numerals align in tabular contexts (freshness, counts, distances). | 4 | Settled by measurement, not by code (design-systems-spec, decision 1). Nunito's default figures are already tabular: ten `1`s and ten `8`s render at identical width with no `font-variant-numeric` applied, difference 0.00px at 40px/700. The proposed `.tnum` class would have been a no-op on all 27 sites, so it was not added. The alignment the criterion asks for is already there. |
| 1.6 | Letter-spacing tightens on display sizes and opens on small caps labels. | 4 | Round 2: 10 ad-hoc values collapse to 5 tokens &mdash; four negative display values (-0.025 / -0.02 / -0.015 / -0.01em), `--ls-caps` 0.08em on every uppercase micro label (replacing .05, .06 and .08em across 9 sites), `--ls-caps-wide` 0.14em on the two deliberately wide-tracked marks (welcome tagline, map street labels), and `--ls-flat` 0 elsewhere. The one negative value at 0.7em, which was invisible and harmful, is gone. |

## 2. Hierarchy and layout

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 2.1 | One clear primary action per screen; secondary actions visibly subordinate. | 4 | Round 2, board section 4. Three button ranks now differ in kind, not only in tint: primary is the only filled control (solid purple, or marigold on the camera ask &mdash; the one moment the product asks rather than offers), secondary is white with a 2px purple border and never a grey fill, tertiary is plain purple text. The grey-lavender `.btn.ghost` fill and the grey `.btn.quiet` fill are both gone. `--fw-display` is reserved for the primary label, so the rank is carried by weight as well as by fill. |
| 2.2 | Spacing follows one scale; no arbitrary gaps. | 2 | Unchanged and untouched by design &mdash; the spacing scale is Round 3's work. One token landed as a side effect of the card pass (`--pad-card` 18px), which is not a scale. |
| 2.3 | Related things are grouped by proximity before they are grouped by a box. | 2 | Unchanged. Round 3. |
| 2.4 | The eye reaches the most important thing first on every screen. | 4 | Round 2. The map had no reading order at all: 64 identical pins. It now has four levels that encode evidence strength and nothing else &mdash; 1 owner pin at 40px, 9-11 scanned at 30px, the rest as 14px dashed rings, and numbered discs for density. Counted at default zoom: 1 level-1, 9 level-2, 48 level-3 rings, 1 disc holding 6. The few purple marks read first, the marigold next, the rings as ground texture. |
| 2.5 | Density suits the job: the map is calm, the card is informative, settings are scannable. | 4 | Round 2, measured the same way before and after (sum of each mark's rendered geometry bounding box, over the 390x844 map viewport): **34,321px&sup2;, 11.3% of the map &rarr; 14,905px&sup2;, 4.9%** &mdash; a 57% reduction in drawn mark area with **every one of the 64 places still on screen** (58 marks + 1 disc of 6). Zoomed out, estimated collapses entirely: 8 full pins + 14 discs holding 56 = 64, so the wide view answers "where has anyone actually been" instead of "where are there doors". Ceiling of 12 full pins at phone width is respected (10 drawn). |
| 2.6 | Optical alignment where geometric alignment looks wrong (icons in rows, pin tips). | 4 | Round 2, both halves fixed and measured. **Pin tips:** the button is now a zero-size anchor on the projected coordinate and the art hangs from it by the tip; across all 58 pins the drawn tip's offset from the coordinate is max &#124;dx&#124; = 0.00px, max &#124;dy&#124; = 0.00px (previously the pin was placed by its box origin with no compensating transform, so it pointed roughly a storefront's width away from what it marked). Level-3 rings, which have no tip, are centred instead. **Row icons:** seven different leading-icon boxes (26/30/32/34/34/38/38px, two different radii, two different fills) collapse to one 36px box at radius 11 on `--icon-box`, so labels align down every column. |

## 3. Colour and depth

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 3.1 | The palette carries meaning, and meaning only. Blue estimated, marigold scanned, purple owner, green match, amber ageing, no red. | 4 | Held, and defended once in Round 2: the pin gallery draws the needs-match halo in **purple**, which would have collided with owner-confirmed. The halo's *form* was taken from the gallery verbatim (solid ring on a soft disc for a good match, broken ring for partial, nothing at all for "not yet seen") and only the hue comes from `--match-green`. One new token, `--blue-pin` #2C63C9, is the level-3 ring and stays inside the estimated tier's own blue. |
| 3.2 | No screen is monotone; each has a considered accent relationship. | 4 | Round 2: the seven finished illustrations landed, each with the two pale fills plus one marigold accent that the boards use. Scan primer (storefront doorway), location permission (map primer), empty saved list, offline / camera-off / choose-your-area on the states screen, correction submitted, and the map-empty invite. The lavender-on-lavender screens all now carry a drawing with a marigold element in it. |
| 3.3 | Elevation is consistent: the same surface level always reads the same. | 3 | Round 2, partial and named as such. Every resting card now reads the same &mdash; `.prof-card`, `.srow`, `.lrow` and `.state-card` share one hairline (`--hairline` #DCD6F2) plus one shadow (`0 2px 10px rgba(36,31,58,.07)`), which is the board's "hairline border, not shadow doing the work" rule. Sheets, pills, FABs and the toast still carry four different shadows; the full elevation scale is Round 3's work, so this is a 3, not a 4. |
| 3.4 | Contrast passes on every text and non-text indicator, including in high contrast mode. | 4 | Re-measured in Round 2 against the three map surfaces, because the pins were rebuilt. Normal / high contrast, on the lavender ground: estimated ring 4.78 / 4.39, scanned rim 5.04 / 8.04, owner rim and cluster-disc edge 8.18 / 10.35, match halo 4.58 / 4.21. On the block and street fills every figure is higher (estimated 5.24 and 5.62 normal). The worst case is a mark **receded** to 80% opacity by a selection or a needs profile, composited against the ground: estimated 3.37 / 3.17, scanned 3.48 / 4.94, owner 5.07 / 6.17 &mdash; all still over 3:1, which is why the recession step is 20% and not more. Round 1's text and indicator results are unchanged (see 7.1, 7.2). |
| 3.5 | Colour is never the only carrier of state. | 4 | Tiers carry shape, match carries text. |
| 3.6 | The wordmark is always two-tone and matches the approved logo &mdash; "entrymap in the top right is not the correct with the light blue and white" &mdash; and the bottom bar carries the logo's palette, "dark blue and light blue and yellow", not purple on purple. | 3 | Directive ledger, added 2026-09-05, scored against HEAD 5cbb19f. **Wordmark: done at all three sites.** Splash (`.splash-word`), welcome (`.wl-word`, `entry` #7CC4FA on the aubergine, `map` #fff) and the map header pill (`.wordmark .w-entry` `--brand-blue-ink` #1D5FA8, `.w-map` `--purple-ink`) all render `<span class="w-entry">entry</span><span class="w-map">map</span>`. Light blue and white where the ground is dark, the light-background pairing where it is white; measured entry 6.45:1, map 9.62:1. **Bottom bar: partial.** Three of the logo's four colours reach it &mdash; deep blue on the map tab, marigold on scan, purple on profile, each carried by `currentColor` so the bar and the weight still carry active state and the 1.05:1 hue-only problem does not return. The logo's *light* blue (#7CC4FA) is in no chrome outside the two dark screens, and the owner named it explicitly, so this is a 3 and not a 4. |
| 3.7 | The map ground has depth and uses more of the icon colours: "use more of the icon colors within the map and the map is so flat." Saturation, not hue &mdash; a marker is always the most saturated thing in its own radius. | 2 | Directive ledger, scored against HEAD 55b9684. The rule is written (visual-language section 11: road hierarchy, block variety, implied light, landcover) and four candidate grounds are drawn and measured against the pins in `design/map-ground.html`, but **at HEAD none of it is in the app** &mdash; the prototype's ground is still one block tone, one street width and scattered tree dots. Round 3 owns it and is mid-flight; this line is here so the directive survives whatever that round does with it, not to judge it. |
| 3.8 | "Make sure the palettes and styles match throughout." One palette and one set of component styles on every screen, not a per-screen dialect. | 2 | Directive ledger, scored against HEAD. Four systems now agree across screens: type (1.1, 1.2), icons (5.4), selection and button rank (2.1), and resting-card treatment (3.3). Four do not: spacing (2.2, at 2), grouping (2.3, at 2), elevation above the resting card (3.3, at 3 &mdash; sheets, pills, FABs and the toast still carry four different shadows), and radius (23 distinct values at HEAD). The score is the floor of what it audits, so it stays at 2 until those land. Round 3 owns all four. |

## 4. Motion

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 4.1 | Motion explains a relationship: where a thing came from, where it went. | 2 | Sheets and screens mostly cut or fade. |
| 4.2 | Durations are consistent and short: roughly 150-250ms for UI, longer only for narrative beats. | 2 | Values vary widely. |
| 4.3 | Easing is consistent and physical; nothing linear except progress. | 3 | Mostly one curve. |
| 4.4 | The processing sequence is the one deliberate narrative moment and it earns its length. | 4 | The self-drawing ring with named checks. |
| 4.5 | Reduced motion removes animation without removing meaning or feedback. | 4 | Re-verified in Round 2 after the pin animations were rewritten for the new anchor: with Reduce motion on, `#ringwrap` is `display:none`, checkitem transition is 1e-05s, the determinate bar reads 100%, all three checks land, the live region still says "Checks complete. 3 features identified.", and the checklist text agrees ("Doorway framed &mdash; done"). The flow completes to Review. |
| 4.6 | Nothing animates on load that the user did not ask for. | 3 | Unchanged. Splash only. |

## 5. Craft details

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 5.1 | Empty states say what to do, not that something is empty. | 4 | Round 2. The copy was already right; the drawing was missing. The saved-list empty state now opens on the "empty shelf" illustration above "No saved entrances yet &mdash; save an entrance from its card and we'll tell you when its information changes", and the map-empty invite opens on the street scene above "No entrances mapped here yet / Be the first to help neighbors plan ahead", with a marigold **Scan an entrance** beside an outlined **Try another area**. Neither says a place or a person failed. |
| 5.2 | Loading, offline and permission-denied states are designed, not default. | 4 | Round 2. All three states screen cards carry their own finished drawing at one size (offline storefront with a cloud, camera, map), replacing three 52px glyph discs; the scan primer opens on the storefront doorway; the correction-submitted screen opens on the note-and-tick drawing. Every one is drawn from tokens, so it re-tints itself in high contrast rather than being redrawn. |
| 5.3 | Touch feedback on every interactive element. | 2 | Unchanged and untouched by design &mdash; touch feedback is Round 3's work with the motion scale. |
| 5.4 | Icons share one grid, weight and terminal style. | 4 | Round 2, measured. One 24 grid, one stroke width (2), one terminal style (round cap, round join), rendered by one function. 38 named icons; 56 static chrome glyphs are painted at boot from a `data-icon` attribute and 40 more are `iconSVG()` calls in JS. Hand-written 24-grid `<svg>` blocks went **50 &rarr; 4** and the four that remain are deliberate: two are the match **heart**, which is a mark like the pins and the Texas flag rather than an icon, and two are the `.ie-icon` inline-error glyph, which the accessibility round owns and this round was told not to touch. Stroke widths in the swept set ranged 1.8-2.8 before; there is now exactly one. |
| 5.5 | Copy is plain, specific and human; no jargon, no cheerfulness the moment does not earn. | 4 | Consistently strong. Unchanged. |
| 5.6 | Nothing is ASCII-fragile: no raw glyph that breaks without the right charset. | 4 | Held through Round 2, which added ~17KB of new SVG. Re-measured on the committed file: **0 bytes above 127**. Still one inline `<script>`, no external scripts, single self-contained HTML. |

## 6. Product truth

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 6.1 | No public negative verdict anywhere, in any state. | 4 | Held through the owner surfaces. |
| 6.2 | Every claim shows its evidence and its date. | 4 | Provenance stack. |
| 6.3 | Trust tier is never a filter, and never granted by a source that did not earn it. | 4 | Enforced. |
| 6.4 | Nothing implies measurement or legal compliance. | 4 | Vocabulary holds. |
| 6.5 | The state record is provenance and never a filter: "what about the texas verified? the filter is awkward for that one too." Nobody needs a record; they need a doorway they can use. | 4 | Directive ledger, scored against HEAD. `FILT_FEATS` is exactly `step_free`, `width`, `hardware` &mdash; three needs, no record. The Texas inspection appears in three honest places and nowhere else: a provenance row on the card that opens the receipt, the receipt row that is the one and only site of the flag glyph, and a read-only row on the owner's edit screen ("Owners edit observations, not state records"). It never alters a pin tier and there is no state-records map layer. This satisfies the same rule as 6.3: if a person may not filter to Owner-confirmed, they certainly may not filter to weaker evidence about a different tenant. **The owner asked this at 19:27 on 2026-09-05 and was never told it was already true.** |
| 6.6 | "Nothing is 100% verified, which to me looks bad. How does a person get that?" The map must not read as a product that knows nothing &mdash; without inventing a rung above Owner-confirmed. | 2 | Directive ledger, scored against HEAD. **This directive conflicts with a settled rule and is recorded rather than dropped.** A "100% verified" tier would be a compliance claim from photographs, which 6.4 forbids and which is the whole honesty position; so the literal ask cannot be built. The complaint underneath is fair and has two answers already in hand, neither of which is scheduled in any design round: (1) 11 of 64 places show as Scanned on-site while the operator photographed all 64 &mdash; the map understates itself, and publishing the rest is the owner's own instruction "publish the scan results for all 64 before demo day"; (2) confidence &mdash; agreement between independent sources &mdash; is already on the card as dot-triples and in the overview line "Neighbors and a state record agree", and can say "three sources agree" without a new rung. Score is 2 because the honest ceiling is reachable and not reached. |
| 6.7 | Step-free is answered where it matters, or honestly marked unanswered: "how to fix the step-free problem". It is the criterion people most need and the one street imagery evidences worst. | 3 | Directive ledger, scored against HEAD. The design surface is honest already: a place with no observation reads "Not yet seen &mdash; be the first to scan", a scan that did not see the feature reads "not spotted in this scan", and neither is a negative verdict (6.1). What is missing is coverage, not copy: the two fixes named in visual-language section 13 &mdash; on-site scans, which show the ground plane, and gated monocular depth, which took step-free from 88.5% to 96.2% on held-out entrances &mdash; are engine work with no design round attached. A 4 needs the estimated tier to stop going quiet on the column that matters most. |

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

## 8. Flows the product promises

A screen can score 4 on every line above and still not add up to a thing a person can
use end to end. This section scores the promises the product owner made out loud, so
that a flow he asked for cannot be finished in pieces and never assembled.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 8.1 | The scan is a walkable sequence, not a button: "did you also add a scanning screen walk through? a processing screen for the scans? how long would a live scan take?" | 3 | Directive ledger, scored against HEAD. Six beats exist and connect: primer (storefront illustration, "Only the doorway is captured", marigold **Allow camera**) &rarr; live viewfinder with the coaching chip &rarr; processing &rarr; review &rarr; publish &rarr; published. The processing screen answers "how long" in words, not just in motion: `#proc-caption` reads "Usually under 8 seconds", and "Usually under 15 seconds" when agreement gating adds the fourth check. Three named checks, a self-drawing ring and the feature chips are 4.4's work and hold. Two board beats are still missing and are why this is a 3: the countdown inside the ring, and the mini map with the three-tier legend on the published screen (visual-language section 7). |
| 8.2 | "The photos should also auto store the images." A scan keeps its photos with no save step, the app says so plainly, and the photos are what other people see on the card. | 3 | Directive ledger, scored against HEAD. What is there: the card renders a `.photostrip` of the place's own scan photos with "N of M photos &middot; tap for the receipt", and the receipt renders them full width, so a scanner's photo does reach other people (this closes the earlier "shouldn't the photos they take be on the photo when you click on it"). The offline path is designed &mdash; "Saved for later / Your scan will upload when you're back online". Privacy is stated as automatic: "Faces are auto-blurred and GPS is stripped at upload &mdash; you never have to do a privacy step." What is missing: **no screen on the ordinary online path tells the user the photo was kept, or where to find it again.** Publishing a scan says the scan published, not that the image is stored. A 4 needs one plain line on the published screen and a route back to the user's own photos. The object store behind it (buckets and keys handed over 2026-09-05 19:45) is build work outside this file, and no design round is waiting on it. |
| 8.3 | The app goes on a phone home screen and wears the logo mark there: "the logo should be the app image", "the image is just a door, not what we agreed it to be", "theres not an add to homescreen". | 3 | Directive ledger, scored against HEAD. `<link rel="apple-touch-icon" sizes="180x180">` points at the brand mark (`entrymap-touch-icon.png`), and `apple-mobile-web-app-capable` makes iOS Add to Home Screen give a standalone window, so the door image is gone and the mark is the icon. There is **no web app manifest**, so on Android the install prompt has no name, no icon and no theme colour, and the phone falls back to a screenshot. A 4 is a manifest carrying the same mark, the name EntryMap, the aubergine theme colour, and standalone display. |


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

---

**Round 2 (2026-09-05).** Board fidelity and the type scale. Everything measured below was
driven in a browser at 390x844 over `python -m http.server`, walking all 26 screens.

**2.53 (R0) -> 3.22 (R1) -> 3.69.** Criteria below 3 go **12 -> 5**, and three whole
sections (1, 3, 5) now have nothing below 3.

*What moved.*

- **The map (2.4, 2.5, 2.6: 3/3/2 -> 4/4/4).** This was the round's real work. Sixty-four
  identical pins became a four-level hierarchy that encodes evidence strength and nothing
  else. Owner-confirmed is the largest full pin, scanned on-site is medium, estimated is
  demoted from a full teardrop to a 14px dashed ring with no glyph, and everything that
  yields becomes a numbered disc. Measured: drawn mark area fell from 11.3% of the map
  viewport to 4.9% while all 64 places stayed on screen. Zoomed out, estimated collapses
  entirely (8 pins + 14 discs holding 56). Selection scales the chosen pin up and steps the
  rest back by 20% without hiding anything; a needs profile lets matching places hold full
  opacity and take a match ring while the rest recede; **no mark anywhere says a place
  fails**. The density rules run on the real dataset: weaker levels yield on overlap, the
  ceiling of a dozen full pins holds (10 drawn), the selected place is exempt and always on
  top, and every mark keeps a 44x44 tap target whatever its drawn size.
- **Pin anchoring (part of 2.6).** Pins were placed by their box origin with no compensating
  transform, so they pointed roughly a storefront's width away from what they marked. The
  button is now a zero-size anchor on the projected coordinate; measured across 58 pins, the
  drawn tip lands on the coordinate with max offset 0.00px in both axes. `revealSelected()`
  was updated in the same change, since it reads the same box and that box now means the tip.
- **Type (1.1, 1.2, 1.4, 1.6: 2/2/2/3 -> 4).** 177 selectors onto 8 steps; zero literal
  `font-weight` and zero literal `em` font-sizes left in the file. The weight rule is the
  part that mattered: 900 went from 94 CSS sites to 21, and on screen from 46% of all
  text-bearing elements to 17%. Row labels dropped to 800 and reading copy to 600.
- **Icons (5.4: 2 -> 4).** The gallery's 36-icon set landed and every call site moved onto
  it, plus 12 glyphs that only existed by hand and were added to the same grid. Hand-written
  24-grid SVG blocks: 50 -> 4.
- **Illustrations (3.2, 5.1, 5.2: 3 -> 4).** All seven placed.
- **Components (2.1: 3 -> 4; 3.3: 2 -> 3).** One selection component everywhere &mdash; empty
  ring on white, filled purple disc with a white tick plus a tinted, purple-bordered row when
  selected &mdash; replacing the inverted solid blocks the needs picker and filter chips used.
  Cards took a hairline plus generous padding. Secondary buttons became white with a purple
  border; the camera permission is marigold.

*What did not move, and why.* Sections 4 (motion) and 2.2 / 2.3 / 5.3 are untouched on
purpose: the brief scoped this round to type only, leaving elevation, spacing and motion for
Round 3. 3.3 rose to 3 rather than 4 because resting cards now agree but sheets, pills and
FABs still carry four different shadows. Section 6 is unchanged at 4s. Section 7 was
re-verified, not re-scored.

*Three judgement calls made against the galleries, each recorded rather than quietly taken.*

1. **The match halo is green, not the gallery's purple.** `pins-and-icons.html` draws it in
   purple. In this product purple already means owner-confirmed and green means "matches your
   needs" and nothing else (3.1, settled in Round 0). Colliding those two would have cost more
   than it bought, so the halo's form is the gallery's verbatim and only the hue is ours.
2. **Level 3 is a new tier on `pinSVG`, not a gallery drawing.** The pin gallery has no
   glyph-less ring, because visual-language section 10 asks for one and the gallery predates
   it. Rather than keep two pin modules, `pinSVG('ring', size)` was added alongside the three
   the gallery ships, in the same idiom, on a new `--blue-pin` token chosen so the ring still
   clears 3:1 after the 20% recession a selection applies (3.37:1 measured).
3. **The welcome hero keeps its aubergine, and the street scene went to the map-empty
   state.** The illustration agent rates the street scene the weakest of the seven, and
   visual-language is explicit that the dark hero is newer canon than the boards. Replacing it
   would have contradicted the document this round is meant to follow. The drawing was not
   wasted: "No entrances mapped here yet / be the first" is a street with nothing marked on it,
   which is what that illustration is a picture of.

*Round 1 re-verified, nothing regressed.* All 26 screens still take focus on change
(26/26); 0 duplicate ids; 0 `button[role="listitem"]`; 58/58 pin accessible names still
carry match state, freshness and distance; `toast()` still reaches the live region; the
Filters sheet still lands focus on its heading, traps it (0 focusables reachable behind the
scrim), closes on Escape and returns focus to the FAB; the card sheet still returns focus to
the originating pin, re-found by id across the re-render. Reduced motion re-verified through
a full scan run. Text scaling swept at Default / Larger / Larger+high-contrast: the overflow
finding count is **17 at every setting, identical to the pre-round file at every setting** —
one new 2px flex finding on the location pill appeared and was fixed before commit. Non-text
contrast re-measured for the rebuilt pins (3.4). File is still 0 non-ASCII bytes, one inline
script, no external scripts. Console is clean on load and across the sweep.

*Known and unchanged.* Seven pins on the map have their 44x44 centre covered by floating map
chrome (the legend card, the FABs, the nav bar). That is the pre-existing overlay behaviour,
not a product of the new anchoring, and the list view is the canon-mandated equivalent path.
The two 20x20 inputs on the claim screen remain inside 44px+ labels, as in Round 1.

---

**Directive ledger pass (2026-09-05).** Not a round. No implementation, no rescoring of
any criterion another round owns. This pass reads the product owner's own messages in the
session and asks one question of each: *is this written down anywhere that gets scored?*

Why it exists, in his words: directives should not "get lost, overwritten, or not
completed." It had already happened once — the note about the wordmark colours was written
into visual-language *after* the round that should have implemented it was dispatched, so
that round never saw it and he raised it three times before it moved. Prose in a design
document is not a safeguard. Prose does not get scored, and an unscored intention is
exactly the thing that goes missing.

**Nine criteria added: 3.6, 3.7, 3.8, 6.5, 6.6, 6.7, 8.1, 8.2, 8.3.** The sheet goes from
45 criteria to 54. Every new line is scored against committed HEAD (5cbb19f / 55b9684),
not against the working copy, because Round 3 is editing the prototype as this is written.

*Already represented, and where.* "More hierarchy on the map, the pins are all the same
size, it looks messy" → 2.4 and 2.5, closed in Round 2. "Better design elements,
transitions, typography, hierarchy" → section 1 (type, closed), section 2 (hierarchy and
spacing, 2.2 and 2.3 open), section 4 (motion, open). "Production ready and a stand out
product" → the bar stated at the top of this file, and the finish rule: nothing below 3,
average 3.5 or better. "Make sure the processing visual is stunning yet simplistic" and
"some kind of animation showing its processing" → 4.4. "The extra symbols around the
original symbols is so confusing, it should be in a hierarchy" → 2.4 and visual-language
section 10. "Photos they take should be on the photo when you click on it for others to
see" → now scored inside 8.2, and satisfied.

*Recorded against a settled rule rather than dropped.* 6.6. "Nothing is 100% verified,
which to me looks bad" cannot be answered with a tier above Owner-confirmed, because that
would be a compliance claim from photographs and 6.4 forbids it. The nearest thing that
respects the rule is written into 6.6 and is genuinely available: publish the on-site scans
for all 64 places, and let source agreement carry what the ladder must not.

*What nothing is currently scheduled to deliver.* This list is the point of the pass.

1. **The bottom bar is missing the logo's light blue** (3.6). Deep blue, marigold and
   purple landed; #7CC4FA reaches no chrome outside the two dark screens, and he named it.
2. **Publishing the on-site scans for all 64 places** (6.6). Asked for directly — "publish
   the scan results for all 64 before demo day" — and again as "publish the sealed 18 after
   the freeze too". No design round owns it; it is the single largest reason the map reads
   as knowing less than it does.
3. **Step-free coverage** (6.7). The copy is honest; the evidence is thin. On-site scans
   and gated depth are the two fixes and both sit outside every design round.
4. **The countdown inside the processing ring, and the published screen's mini map with
   legend** (8.1). Named as missing in visual-language section 7 and never scheduled since.
5. **Telling the user their photo was stored** (8.2). "The photos should also auto store
   the images." Storage is being built; nothing on the published screen says so, and there
   is no route back to a scanner's own photos.
6. **A web app manifest** (8.3). Add to Home Screen works on iOS only.
7. **He was never told the Texas filter was already gone** (6.5). The change is real in the
   build and correct; it existed only as prose in visual-language section 13 and was never
   scored, so nothing could report it back to him.

*Outside this file, and flagged so it is not lost with it.* "Why don't you know the
storefront for doors 13 to 64? You are supposed to automatically assign them for the user."
That is the capture-to-place assignment pipeline, not a design surface, and it belongs in
the ticket tracker rather than in a rubric line. It is named here only because this pass is
the last place it could have gone missing.
