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
| 1.1 | A real type scale, not ad-hoc sizes. Every size on screen traces to a defined step. | 4 | Round 2: 177 selectors mapped onto the spec's 8 steps. **0** literal `font-size` values in `em` remain anywhere in the file (was 29 distinct values). The 8 remaining `px` sizes are exactly the spec's legitimate set: the 15px root and its two `[data-textsize]` overrides (16.2 / 18.9), the text-size picker's own 14/17/20 preview (it must not scale with the setting it controls), the 13px desktop stage caption outside the phone, and `.street-label` at 10.5px, the one deliberate non-scaling piece of content type because the map geometry is computed in px. The eight steps are also authored once as `.t-display` &hellip; `.t-micro`. **Round 4 (asset library):** the scale survives the face change unaltered &mdash; the eight steps are `em`-relative, so moving from Nunito to Atkinson Hyperlegible Next changed no size. Re-measured over all 26 screens at both text-size settings: **0** clipped text nodes, **0** horizontal overflow. |
| 1.2 | Weight carries hierarchy. No more than three weights doing real work; 900 is not the default. | 4 | **Round 4 re-pitched the ladder onto the new face and re-measured it.** Atkinson Hyperlegible Next's variable axis runs 200-800, so 600/800/900 becomes **500 / 650 / 800** &mdash; still exactly three weights, and the top one is still a reserved resource. 650 and 800 are not arbitrary: the library's own assets set badge labels at 650 and state headings at 750, so the two upper steps are the weights the approved boards are drawn in. Measured in the browser over all 26 screens on every text-bearing leaf element inside the phone: **500 on 125, 650 on 211, 800 on 61**, and weight 700 on 4 &mdash; those 4 are the UA bolding `<b>`, not a rule, the same 4 Round 2 measured. CSS still contains **0** literal `font-weight` values. *Superseded Round 2 evidence:* 900 on 21 declarations, 800 on 112, 600 on 71; measured 900 went 234 of 506 (46%) to 95 of 565 (17%). |
| 1.3 | Line length stays readable, roughly 45-75 characters for body copy. | 3 | Held at 3 on a Round 3 measurement rather than left "unchanged". The main reading column is right: `--fs-body` 14.3px / `--lh-body` 1.5 in a 358px column gives 52-68 characters. But sampling every multi-line paragraph across all 26 screens gives a median of **35 characters per line**, because most supporting copy sits in a narrower sub-column beside a 36px icon box and a chevron. That is under the band, and the spacing pass widened it only slightly. Fixing it is a layout decision about whether row sub-copy may use the full width, not a token change. Recorded rather than rounded up. |
| 1.4 | Line height rises for body copy and tightens for display sizes. | 4 | Round 2: leading is named at every step and applied with the size, never left to inherit `normal`. Display 1.0, h1 1.1, h2 1.15, h3 1.22, body 1.5, sub 1.45, meta 1.35, micro 1.25, plus `--lh-row` 1.3 for one-line row labels that may wrap to two. |
| 1.5 | Numerals align in tabular contexts (freshness, counts, distances). | 4 | **Round 4 caught a live regression here and fixed it.** Round 2's 4 rested on a measurement of the FACE: Nunito's default figures are tabular, so no `font-variant-numeric` was needed and the proposed `.tnum` class would have been a no-op at all 27 sites. Atkinson Hyperlegible Next's figures are **proportional**: measured in the browser at 40px/650, ten `1`s render 174.00px and ten `0`s render 263.21px &mdash; an **89.21px spread** that would have silently pulled every freshness, count and distance column out of line. The face supports `tnum`; `font-variant-numeric:tabular-nums` is now set once on `body`, and the same measurement is **0.00px** across all three weights. Set at the root rather than at 27 sites because root is exactly the scope the old face gave for free. |
| 1.6 | Letter-spacing tightens on display sizes and opens on small caps labels. | 4 | Round 2: 10 ad-hoc values collapse to 5 tokens &mdash; four negative display values (-0.025 / -0.02 / -0.015 / -0.01em), `--ls-caps` 0.08em on every uppercase micro label (replacing .05, .06 and .08em across 9 sites), `--ls-caps-wide` 0.14em on the two deliberately wide-tracked marks (welcome tagline, map street labels), and `--ls-flat` 0 elsewhere. The one negative value at 0.7em, which was invisible and harmful, is gone. **Round 4 (asset library):** unchanged; the five tracking tokens are face-independent and re-measured clean. |
## 2. Hierarchy and layout

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 2.1 | One clear primary action per screen; secondary actions visibly subordinate. | 4 | Round 2, board section 4. Three button ranks now differ in kind, not only in tint: primary is the only filled control (solid purple, or marigold on the camera ask &mdash; the one moment the product asks rather than offers), secondary is white with a 2px purple border and never a grey fill, tertiary is plain purple text. The grey-lavender `.btn.ghost` fill and the grey `.btn.quiet` fill are both gone. `--fw-display` is reserved for the primary label, so the rank is carried by weight as well as by fill. |
| 2.2 | Spacing follows one scale; no arbitrary gaps. | 4 | Round 3. Forty distinct values, 37% of them off-grid, become a **10-step scale** (0&middot;2&middot;4&middot;6&middot;8&middot;12&middot;16&middot;24&middot;32&middot;48) plus **7 layout constants** for the fixed chrome. Nearest step, ties round up, applied mechanically to CSS and to every inline style. Measured on the committed file: **611** numeric values across `padding` / `margin` / `gap`, of which **574 resolve to a token** and **12 raw `px` remain** &mdash; and all twelve are the documented geometry sites (the scan button&rsquo;s -26px rise above the bar, the 40px and 52px clearances for the card close button and the map-control stack, the two 60px list-header margins, the 44px back-button balance, two optical nudges at -3px and -2px, and `.ow-stackrow.new` whose -14px bleed must equal its 14px padding). Each is commented with what it is anchored to, so a later pass does not "fix" it. The four bottom paddings that all meant "clear the nav bar" (96 / 100 / 104 / 110) collapse to `--pad-bottom` 104, which also closes a real defect: `.screen-body` was padding 96px against an 86px nav. |
| 2.3 | Related things are grouped by proximity before they are grouped by a box. | 4 | Round 3, on the stated rule: *a box earns its keep only when it changes surface, carries a state, or holds a scroll boundary; grouping alone is proximity's job.* **Nine boxes removed or merged, four kept with the reason written into the file.** The three &ldquo;How trust grows&rdquo; rungs are now three rows on the sheet's own white separated by `--sp-7` (three boxes inside one white sheet is a box inside a box); `.need-breakdown` indents under the chip it breaks down; `.receipt-note` became the sub-line of the `.prov-row` it had been detaching from; `.whatsnext` lost the border that only repeated its heading; `.policy-line` stopped being a shadowed white card holding one line of copy. **Six treatments of &ldquo;a quiet supporting note&rdquo;** &mdash; `.tax-box`, `.state-card .sc-note`, `.ow-flagnote`, `.priv-line`, `.guardrail`, `.a11y-note`, three of them filled and rounded at three different paddings and three borderless &mdash; are now **one** component; the purple ones keep their purple ink and lose only the fill. The four owner cards dropped their inner row hairlines, because card + divider + row rhythm is three signals for one grouping. Kept, each with its reason: `.tile` (the fill carries freshness ageing, so the box *is* the state), `.preview` (it is a preview *of a card*, so the box is the subject), and `.evidence` / `.ow-note-card` (the 3px left rule reads as a quotation; only the doubled fill went). |
| 2.4 | The eye reaches the most important thing first on every screen. | 4 | Round 2. The map had no reading order at all: 64 identical pins. It now has four levels that encode evidence strength and nothing else &mdash; 1 owner pin at 40px, 9-11 scanned at 30px, the rest as 14px dashed rings, and numbered discs for density. Counted at default zoom: 1 level-1, 9 level-2, 48 level-3 rings, 1 disc holding 6. The few purple marks read first, the marigold next, the rings as ground texture. |
| 2.5 | Density suits the job: the map is calm, the card is informative, settings are scannable. | 4 | Round 2, measured the same way before and after (sum of each mark's rendered geometry bounding box, over the 390x844 map viewport): **34,321px&sup2;, 11.3% of the map &rarr; 14,905px&sup2;, 4.9%** &mdash; a 57% reduction in drawn mark area with **every one of the 64 places still on screen** (58 marks + 1 disc of 6). Zoomed out, estimated collapses entirely: 8 full pins + 14 discs holding 56 = 64, so the wide view answers "where has anyone actually been" instead of "where are there doors". Ceiling of 12 full pins at phone width is respected (10 drawn). |
| 2.6 | Optical alignment where geometric alignment looks wrong (icons in rows, pin tips). | 4 | Round 2, both halves fixed and measured. **Pin tips:** the button is now a zero-size anchor on the projected coordinate and the art hangs from it by the tip; across all 58 pins the drawn tip's offset from the coordinate is max &#124;dx&#124; = 0.00px, max &#124;dy&#124; = 0.00px (previously the pin was placed by its box origin with no compensating transform, so it pointed roughly a storefront's width away from what it marked). Level-3 rings, which have no tip, are centred instead. **Row icons:** seven different leading-icon boxes (26/30/32/34/34/38/38px, two different radii, two different fills) collapse to one 36px box at radius 11 on `--icon-box`, so labels align down every column. **Round 3 closed the third rule in design-systems-spec 2.7:** the six circular glyph containers that hold a tick or a numeral (`.tl-dot`, `.ow-tick`, `.ci-dot`, `.nl-dot`, `.p-ring`, `.cr-mark`) now carry `padding-bottom:1px` on their flex centring, because a checkmark is optically low and geometric centring makes it sit high in its circle. Three privacy rungs that were carrying an inline 34px / radius-10 / `#fff` icon box now use the one `--icon-box`, so that column aligns with every other. |

## 3. Colour and depth

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 3.1 | The palette carries meaning, and meaning only. Blue estimated, marigold scanned, purple owner, green match, amber ageing, no red. | 4 | Held through the new map ground, which is the hardest test it has faced. The ground echoes the whole palette on **saturation, not hue**: no ground tone exceeds chroma 43 while the least saturated marker colour is chroma 95, so a marker is always the most saturated thing within its own radius; no ground element is ever a lone disc or a teardrop (canopy is only ever four or more overlapping lobes, a kerbside band, or a filled grove); and any lobe whose centre lands within 26px of a full pin is dropped before it is emitted, so nothing decorative can sit inside a marker halo. No red anywhere. Round 3 also **settled the estimated blue**, which two committed files disagreed about: `design/pins-and-icons.html` specified #2C63C9, `design/map-hierarchy.html` used #3F79DC, and the shipped teardrop's token read #3F79DC while its own inline fallback read #2C63C9. One token now &mdash; `--blue-edge:#2C63C9`, the gallery's value, the one the level-3 ring already shipped as, and the one that drops the ground's luminance floor from 0.691 to 0.510 and so makes this ground possible at 3:1. `--blue-pin` is gone. Round 2's halo judgement (green, not the gallery's purple) stands unchanged. **Round 4 (asset library):** **the palette is now the approved one, not an approximation of it.** Eleven values from `asset-library/tokens/variables.css` are the only authored colours in the file; every other colour is one of them or a documented two-step mix of two of them. The five the owner flagged all moved: ink #241F3A &rarr; indigo900 #17103D, purple #7053C5 &rarr; violet600 #5B35F5, sky #7CC4FA &rarr; sky400 #69B7FF / sky700 #1266A6, marigold #F0A32F &rarr; marigold400 #FFBF24, lavender #EDEBFA &rarr; lavender100 #F2EEFF. Meaning is unchanged and the tiers are unchanged. The one retirement is the match halo: Round 2 chose green because purple already meant owner-confirmed, and the library supersedes that with three approved halos that carry the state in LINE STYLE first &mdash; solid indigo900 good, dashed violet600 partial, dotted sky700 unknown. `--match-green` is gone. Live hex literals in the file: **81**, every one traceable to the official palette; the four legacy values that still appear (#BF0A30, #002868, #5A4BE0, #C4D0F6) appear only inside comments recording what was removed. |
| 3.2 | No screen is monotone; each has a considered accent relationship. | 4 | Round 2's seven illustrations are unchanged and re-verified; Round 3 answered the one surface they could not reach. The map was a flat lavender canvas &mdash; one block tone, one street width, no implied light, trees as scattered dots &mdash; and it is now **Terrain's colour on Relief's light**: warm sand ground, sage canopy, marigold plazas, and cool lavender towers standing among warm putty low-rise, so a block reads as buildings of different eras rather than one slab. Depth comes from the four things the canon asks for and not from a drop shadow: a real road hierarchy (16 / 11 / 8 / 4.5px), footprints in five tones **ramped by mass** so the variation reads as building size rather than noise, one light direction applied to every footprint as a two-step cast shadow plus a lit top-and-left edge, and landcover as areas. Measured on the drawn SVG at 390x844: **1,711 shapes from 15 ground tones**, where the old ground drew 128 from 4. |
| 3.3 | Elevation is consistent: the same surface level always reads the same. | 4 | Round 3. **24 distinct shadows become 4 levels** carried by 6 tokens, plus 5 named rings that were never elevation in the first place. Each level is two shadows &mdash; a tight contact shadow that anchors the object and a wide ambient one that gives it distance &mdash; which is exactly what makes one level read the same on a white sheet and on the map ground; opacity rises .07 &rarr; .14 &rarr; .20/.24 so the ordering is legible. Measured in the browser over every element inside the phone, **11 distinct `box-shadow` values are painted**, and they are: `--elev-1` (14 cards resting on the lavender ground), `--elev-2` (18 things that float over the map), `--elev-3-dock` (`.sheet`, `#sheet-card`, `.ow-sheet` &mdash; one docked sheet drawn three different ways), `--elev-3-dark` (`.wl-card` on the aubergine hero), `--elev-3-free` (the trust popup and the toast, which had **no shadow at all**), `--ring-action` (two marigold glows for one action), `--ring-select`, `--ring-quiet`, `--knob` (two knob shadows for one knob), and the two progress rims the accessibility round owns and this round did not touch. Across **60 `box-shadow` declarations** there is no hand-written elevation value anywhere inside the phone. High contrast now **redefines the level tokens centrally**, so a surface is outlined because of the level it is at; previously two rules hand-picked 11 components and every other elevated surface was missed. `.search-bar .searchfield` left level 2 &mdash; it is a form control, not a floating object. |
| 3.4 | Contrast passes on every text and non-text indicator, including in high contrast mode. | 4 | **Re-measured from scratch in Round 4, because a palette swap is exactly how measured contrast gets silently undone.** The tone under every marker is hit-tested against the ground SVG's own paint list. Normal contrast, for estimated dashed outline &middot; scanned body rim &middot; owner body fill &mdash; **modal ground tone 4.55 / 13.42 / 4.83**, **worst tone anywhere 4.45 / 13.13 / 4.73**, and **receded to 80%** by a selection or a needs profile, **3.27 / 8.03 / 3.63** modal and **3.23 / 7.93 / 3.57** worst. High contrast: **11.70 / 17.83 / 6.42** modal, **9.20 / 14.02 / 5.05** worst, **6.47 / 9.68 / 4.41** and **5.51 / 8.23 / 3.70** receded. The two match halos measure with the marks they share a colour with (good = indigo900, partial = violet600). All 24 figures clear 3:1, and **22 of the 24 are better than the Round 3 figure they replace** &mdash; Round 3's worst tone was 4.14 / 4.37 / 4.15 and receded 3.08 / 3.13 / 3.02, so every worst-case and every receded figure improved, in both contrast modes. The two that did NOT improve are the estimated outline and the owner fill on the MODAL tone in normal contrast: 4.55 against Round 3's 4.74, and 4.83 against 5.35. Both are the cost of taking the library's colours (sky700 is slightly lighter than the retired #2C63C9, violet600 slightly lighter than #7053C5); both remain over 3:1 by a wide margin, and both buy a better floor where it actually binds, which is the worst tone and the receded state. Text: measured over all 26 screens in four modes &mdash; normal, high contrast, and each at the largest text setting &mdash; **0 failures in all four**, minimum non-large ratio **6.42:1**, which is white on logo violet, the exact pairing and the exact ratio the library's own report signs off for bold control labels. The only value the round had to raise was the marigold button label: at #5F371B it measured 6.21:1 on marigold400, and it is now #533021 at 7.02:1. Focus rings, read from the CSSOM because `:focus-visible` cannot be forced from script: violet600 on its white halo 6.42:1, lavender100 on its indigo900 halo 15.66:1, sky400 on indigo900 in the new dark chrome 8.33:1, and in high contrast #0E0A25 on white 19.29:1 and white on #0E0A25 19.29:1. |
| 3.5 | Colour is never the only carrier of state. | 4 | Tiers carry shape, match carries text. |
| 3.6 | The wordmark is always two-tone and matches the approved logo &mdash; "entrymap in the top right is not the correct with the light blue and white" &mdash; and the bottom bar carries the logo's palette, "dark blue and light blue and yellow", not purple on purple. | 4 | **Closed in Round 4, and the reason it could not close before is now clear.** Rounds 1-3 rendered the wordmark as two coloured `<span>`s and had to invent an on-light pairing, because on a WHITE pill the logo's light blue is unavailable at any legible ratio. Board 02 shows why that was the wrong problem: the map header on the approved boards is not a white pill, it is a solid indigo900 bar, and the wordmark on it is the on-dark variant &mdash; light blue "entry", white "map". Round 4 ships the board. **The wordmark is the library asset** (`asset-library/svg/brand/wordmark-on-dark.svg`, path and text data verbatim, background rect dropped because here the real surface is behind it, `textLength` added so the lockup cannot overflow if Nunito Sans has not loaded) at all three sites the owner named: splash, welcome and the map header. **The chrome is the board's**: `.apphead` is a full-width indigo900 bar and `.navbar` is the same indigo900. **The bottom bar is now literally "dark blue and light blue and yellow"** &mdash; indigo900 ground, sky400 on the active Map tab (8.33:1, the pairing the library's report approves), marigold400 on the Scan ring, lavender200 on the inactive labels (13.33:1), and active state still carried by the rule above the tab and by the weight, so the 1.05:1 hue-only problem does not return. The light blue also reaches LIGHT chrome, where before Round 4 there was no correct answer and now there is one: sky700 #1266A6, the library's own on-light sky, on the Estimated tier throughout and on every informational cue. Two side effects worth naming: the status bar now follows the chrome (`data-chrome`), which incidentally fixed a live defect &mdash; on the welcome and capture screens it was painting `--ink` on a dark ground; and the pushed-screen title rows (`.flowhead`) are deliberately NOT converted, because they sit inside the scrolling body and making them a fixed dark bar is layout surgery this round did not need. That is the one remaining gap between the build and the boards, and it is named rather than hidden. |
| 3.7 | The map ground has depth and uses more of the icon colours: "use more of the icon colors within the map and the map is so flat." Saturation, not hue &mdash; a marker is always the most saturated thing in its own radius. | 4 | Round 3 built it, as the recommended combination: **Terrain's colour on Relief's light**. All four sources of depth are in the app, not just the rule. **Road hierarchy:** Congress, Guadalupe, Lavaca and Cesar Chavez primary at 16px, the numbered cross streets secondary at 11px, Colorado minor at 8px, four service alleys at 4.5px, each street casinged so it reads as a channel carved into the block rather than a white stripe laid over it; the three unlabelled arterials got their labels. **Block variety:** footprints split from the block, gapped by a 1.1px party wall, in five tones. **Implied light:** one direction for the whole map, as Relief's two-step cast shadow plus a lit top-and-left edge on every footprint, with the tonal ramp keyed to footprint **mass** so the variation reads as buildings of different sizes rather than as noise. **Landcover:** a grove, kerbside tree bands, courtyard clumps and marigold plazas as real areas. The colour answer is Terrain's: warm sand ground, sage canopy, marigold plazas, cool lavender towers standing among warm putty low-rise. Measured: **1,711 shapes from 15 ground tones** where the old ground drew 128 from 4. The saturation rule is enforced rather than described &mdash; no ground tone exceeds chroma 43 against the least saturated marker's 95, no ground element is ever a lone disc, and any canopy lobe within 26px of a full pin is dropped before it is emitted. Contrast re-measured against every tone a marker can land on: see 3.4. **Round 4 (asset library):** the ground survived the palette swap and is now **derived from the official palette rather than sitting beside it**. The library ships no map-ground tokens, so each of the 17 tones is re-solved as a two-step mix &mdash; an official base carried toward white (which sets chroma) then toward indigo900 (which sets lightness) &mdash; targeting the Round 3 tone's exact CIE lightness and chroma. Bases: marigold400 for the sand, putty and plaza family; lavender200 for the cool towers; and, for the canopy, a 50/50 marigold400 + sky400 mix, because the approved palette contains no green and those are the only two official hues that make one. The honest finding is that Round 3's warm family was ALREADY on the marigold hue line at very low chroma, so eight of the seventeen tones came back byte-identical and the rest moved by one or two steps of 255. The saturation rule is restated against the new markers: the loudest ground tone is the plaza at CIE chroma 16.3 while the least saturated marker colour is now sky700 at 40.9, a ratio of 0.40 against Round 3's 0.45. The luminance floor moved in our favour: sky700 needs 0.4715 where #2C63C9 needed 0.4789, and the darkest tone drawn anywhere is 0.7235. |
| 3.8 | "Make sure the palettes and styles match throughout." One palette and one set of component styles on every screen, not a per-screen dialect. | 4 | Round 3. The four systems this line was waiting on all landed &mdash; spacing (2.2, now 4), grouping (2.3, now 4), elevation (3.3, now 4) and radius (23 distinct values to one five-step ladder) &mdash; and the score is the floor of what it audits, so it moves with them. Beyond those, a deliberate sweep of all 26 screens, done by inventorying every declaration in the stylesheet by property and by selector rather than by looking at screens, found and fixed **twenty distinct classes of "the same thing drawn two ways"**: 24 shadows, 23 radii, 6 border widths for one control edge, 3 hairline colours plus a fourth undeclared grey `#D8CCF3`, 4 alphas of translucent white across 12 floating surfaces, 6 row heights, an undeclared quiet fill `#F8F7FD` at 5 sites, a fourth ink `#6C6486` on the chevrons, a literal `#4A4463` on the diff arrow, a literal `#2A1A5E` progress rim, 6 treatments of a quiet note, 3 treatments of a quoted note, 5 press scales and 2 ad-hoc press washes, two docked-sheet top radii, two legends at two radii, two pills written as pixel radii, three privacy rungs carrying an inline icon box instead of `--icon-box`, a form control wearing the floating map shadow, 40 spacing values, and 19 durations with 7 easings. The estimated-tier blue was the sharpest find: two committed files specified different hexes and the shipped teardrop's token disagreed with its own inline fallback (3.1). **Round 4 (asset library):** this is the line the round was called for, and it is the strongest evidence it has had. The build's palette was an approximation of the logo assembled by hand; it is now the approved library, with **eleven authored colours** and everything else derived from them by a stated rule. What moved: 100 source lines of legacy hex swept onto the official palette; `--teal-ink`, `--match-green`, `--match-ink`, `--match-wash`, `--brand-amber`, `--street`, `--block` and `--tree` retired; `--amber-ink` and `--marigold-ink` collapsed into one colour (they were #6B4F00 and #6E4A00 &mdash; two names for one hue); every shadow `rgba` re-based from the retired #241F3A onto indigo900; the desktop stage behind the phone, which was three greys, re-derived onto lavender. **Thirty icon names are now the library's own drawings** and the twenty-seven that stay are the ones it has no equivalent for, re-expressed on the library's 32 grid so both families paint at the same 2.3 stroke (5.4). The three pins, the three match halos, the tier badges, the confidence dots, the freshness pill, the five provenance marks, the Texas record and the brand marks are the library's assets. The two remaining deviations from the boards are named, not hidden: the pushed-screen title rows are still light (3.6), and the six state illustrations stay ours (5.1, 5.2). |
## 4. Motion

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 4.1 | Motion explains a relationship: where a thing came from, where it went. | 4 | Round 3. Fifteen of the 26 screens cut outright and the other eleven fade-rose 8px with no direction. Screens now **push and pop by direction** &mdash; `screen-fwd` +12px, `screen-back` -12px, `screen-lat` a plain fade, 12px being the smallest travel at which direction is legible &mdash; and the direction is written by the three navigation functions that already knew it. Verified: `data-dir` reads `fwd` after `goScreen`, `back` after `goBack`, `lat` after a bottom-nav tab. The trust popup **grows from the control that opened it** instead of scaling from the screen centre, which said nothing: with the legend focused, `--pop-x` / `--pop-y` measure **20.2% / -61.7%**, which is the legend's centre expressed in the popup's own coordinate space (read from `offsetLeft`/`offsetTop`, because `transform-origin` percentages are against the untransformed box). The list **rises 8px and settles**, because it is the map's content re-presented rather than a different place, and it still leaves the accessibility tree when closed. An active-filter chip **arrives** with `chipIn` on first appearance (measured: class `achip arriving`, animation `chipIn`, 220ms) and does not re-animate on later re-renders; on removal it runs the reverse before the DOM removal. The map pan now travels on the sheet's own clock, so the selected pin visibly steps aside for the card instead of teleporting. |
| 4.2 | Durations are consistent and short: roughly 150-250ms for UI, longer only for narrative beats. | 4 | Round 3. **Nineteen distinct durations become two**: `--dur-fast` 160ms for feedback and in-place state change, `--dur-base` 220ms for anything that travels. Both sit inside the criterion's band. Four narrative constants are named and scoped to the scan sequence, which criterion 4.4 already scores 4 and this round did not re-time (`--dur-settle` 900, `--dur-check` 1500, `--dur-drop` 700, `--dur-ripple` 1000). Counted in the committed CSS, the only time values that remain are those six, `0s` &times;6 (the sheets' visibility guards), `.01ms` &times;4 (the two reduced-motion kill-switches) and three progress durations the criterion exempts. Sheets are **220ms in and 160ms out** &mdash; a sheet leaves faster than it arrives, which is what makes a dismissal feel obedient rather than sluggish, and the visibility guard's delay tracks the duration it is paired with. |
| 4.3 | Easing is consistent and physical; nothing linear except progress. | 4 | Round 3. Seven easings &mdash; two general-purpose curves doing the same job, two near-identical overshoots at 1.2 and 1.15, plus `ease-out`, `ease-in` and `linear` &mdash; become **two curves plus one scoped spring**: `--ease-enter` for arriving and settling, `--ease-exit` for leaving, and `--ease-spring` on `dropIn` and `pinTap` only, which is where the canon asks for overshoot. Counted in the committed CSS: exactly **three** `cubic-bezier` values, **zero** `ease-out`, **zero** `ease-in`, and **four** `linear` &mdash; the two progress arcs' `stroke-dashoffset` and the two progress bars' `width`, which is the criterion's own exemption. |
| 4.4 | The processing sequence is the one deliberate narrative moment and it earns its length. | 4 | The self-drawing ring with named checks. |
| 4.5 | Reduced motion removes animation without removing meaning or feedback. | 4 | Re-verified in Round 3 after the motion system landed, and the rule that protects it is now structural rather than a habit: **no deferred step anywhere uses `transitionend` or `animationend`**, because at the 0.01ms duration the kill-switch imposes those events can fire before a listener attaches and leave an element stuck. A `defer(ms, fn)` helper collapses the wait to 0 under reduced motion and is deliberately *not* the existing `after()`, whose timers live on `scanTimers` and would be cancelled by a nav action &mdash; which would have left the list view hidden-but-focusable. With Reduce motion on: sheet and chip transition durations read `1e-05s`, `#ringwrap` is `display:none`, the determinate bar is visible at 100%, all three checks land, the checklist text agrees, and the flow completes to Review. Every `:active` press survives, because a `transition:none` press has no duration to zero. *Round 2 evidence:* re-verified in Round 2 after the pin animations were rewritten for the new anchor: with Reduce motion on, `#ringwrap` is `display:none`, checkitem transition is 1e-05s, the determinate bar reads 100%, all three checks land, the live region still says "Checks complete. 3 features identified.", and the checklist text agrees ("Doorway framed &mdash; done"). The flow completes to Review. **Round 4 (asset library):** re-verified: the in-app Reduce motion toggle still puts `.rm` on the phone and the screen-change animation computes to `none`; no animation was added this round. |
| 4.6 | Nothing animates on load that the user did not ask for. | 3 | Held at 3, and defended rather than left alone. The screen-push animation added this round could easily have become a second load animation, so the map body and the splash body are both excluded by rule (`#screen-map .screen-body, #ob-splash .ob-body{animation:none}`) and the splash keeps its own `splashIn` / `splashOut` pair. Measured on a cold load: **zero** elements inside the active screen have a running animation once the splash has left. It stays a 3 because the splash still animates on load without being asked, which is the criterion as written. |

## 5. Craft details

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 5.1 | Empty states say what to do, not that something is empty. | 4 | Round 2. The copy was already right; the drawing was missing. The saved-list empty state now opens on the "empty shelf" illustration above "No saved entrances yet &mdash; save an entrance from its card and we'll tell you when its information changes", and the map-empty invite opens on the street scene above "No entrances mapped here yet / Be the first to help neighbors plan ahead", with a marigold **Scan an entrance** beside an outlined **Try another area**. Neither says a place or a person failed. **Round 4 (asset library):** the library's six state assets were read and deliberately **not** adopted, and the reason is a measurement rather than a preference: each bakes its headline at 17px and its sub-copy at 12px into the SVG, which cannot move with the text-size setting and would fail 7.11, cannot be announced, and would duplicate the HTML copy the screens already carry; each also draws its own card frame, doubling the card the screen already draws. Their artwork content is a lavender disc with one small glyph, which is a simpler thing than the seven drawings this line scores. What the library DID change here is the palette they are drawn in &mdash; every colour in all seven is now an official token &mdash; and the pins that appear inside them, which are the library's. |
| 5.2 | Loading, offline and permission-denied states are designed, not default. | 4 | Round 2. All three states screen cards carry their own finished drawing at one size (offline storefront with a cloud, camera, map), replacing three 52px glyph discs; the scan primer opens on the storefront doorway; the correction-submitted screen opens on the note-and-tick drawing. Every one is drawn from tokens, so it re-tints itself in high contrast rather than being redrawn. **Round 4 (asset library):** same call as 5.1 for the permission, processing, offline and published states: the artwork stays ours because the library's bakes 12px copy into the SVG; the palette is now official. |
| 5.3 | Touch feedback on every interactive element. | 4 | Round 3. **Two treatments, chosen by shape rather than by importance.** Compact controls (buttons, chips, pills, circular controls) scale to `.97`; full-width rows take a wash, because scaling a row that spans the screen looks like a rendering fault, and rows sitting on the lavender ground use a darker wash so the press is visible from a non-white start. Press-down is instantaneous and the release eases out &mdash; feedback that fades *in* is not feedback. Counted in the committed CSS: **47 components carry `cursor:pointer` or `cursor:grab`, and 44 have an `:active` treatment.** The three that do not are named exceptions: `.pinbtn`, which has `pinTap` &mdash; the canon's squash-and-rise, better feedback than either treatment &mdash; and the two native inputs on the claim screen, which sit inside `.authz` / `.verify-opt` rows that press around them. The eight presses that already existed used five different scale values (.93 / .95 / .97 / .98) and two ad-hoc wash colours; all are normalised, with the 76px shutter (.93) and the 72px scan ring (.95) kept deeper because they are physically larger. |
| 5.4 | Icons share one grid, weight and terminal style. | 4 | **Round 4 moved the grid to the library's.** Thirty names are now the library's own path data verbatim &mdash; 20 UI icons, 8 feature icons, the community provenance mark and the Texas record &mdash; on its 32 grid. The 27 that stay are the ones the library ships no equivalent for and they are named in the source: the map's own controls (list, zoom-in, zoom-out, locate, back), the bare tick that sits inside a filled selection disc (the library has only the OUTLINED check, which is the owner badge and means something else), bookmark, share, upload, external, phone, directions, plus, minus, text-size, the five persona glyphs, the three settings glyphs, lock, bell, sparkle, warning, and handrails. Those 27 are re-expressed on the 32 grid by scaling the 24-grid path 4/3 with `stroke-width:1.725`, which paints at exactly **2.3** &mdash; the library's own UI-icon weight &mdash; so a legacy icon and a library icon are indistinguishable in weight. The library's feature icons ship at 2.2 and are levelled up to 2.3, because this line asks for one weight. Round 4 also found that the library dedupes what we drew twice: `provenance/owner-source` IS `ui-icons/storefront`, `photo-source` IS `photo`, and `public-record` IS `receipt`. |
| 5.5 | Copy is plain, specific and human; no jargon, no cheerfulness the moment does not earn. | 4 | Consistently strong. Unchanged. |
| 5.6 | Nothing is ASCII-fragile: no raw glyph that breaks without the right charset. | 4 | Still **0** non-ASCII bytes outside the base64 payloads, verified by scanning the file with the payloads stripped. Round 4 went further, because the font swap exposed a second failure mode the charset rule does not catch: a glyph that is safely escaped can still have no glyph in the UI face. Measured over all 26 screens, **19 of 402 text nodes fell out of Atkinson Hyperlegible Next into Arial** &mdash; every back button (U+2039), every close button (U+2715), every row chevron (U+203A), the location pill's triangle (U+25BE), the "My needs" heart (U+2665), the processing and timeline ticks (U+2713), and the eight decorative dingbats in `FEATS` (U+2913, U+27CB, U+2562, U+25C9, U+2310, U+21E2, U+267F, U+21D4). All of them are drawings now, from the library where it ships one. Re-measured: **402 of 402 text nodes render in the UI face; 0 fall back.** |

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
| 7.1 | Text contrast passes everywhere, in both normal and high contrast. | 4 | Unchanged and not regressed. The decorative glyphs that were the only failures (`>`, `->`, the transparent tick) are now `aria-hidden`, and the two that stay visible were raised from 2.62:1 to 4.6:1. Checklist pending text went 2.47:1 -> 6.34:1 (`--faint` on the ground). **Round 4 (asset library):** re-measured after the palette swap, over all 26 screens in four modes (normal, high contrast, and each at the largest text setting): **0 failures in every mode**. Minimum non-large ratio **6.42:1** in all four, which is white on logo violet &mdash; the library's own approved pairing for bold control labels, at the library's own ratio. Only two pairings in the whole build sit under the library's 7:1 body-text bar and both are control labels rather than body copy; every text ink the build uses for reading (`--ink`, `--sub`, `--faint`, `--blue-ink`, `--marigold-ink`, `--purple-ink`) was derived against a 7:1 target on lavender100 and measures 8.00 / 8.00 / 7.05 / 7.03 / 7.01 / 8.82. |
| 7.2 | Non-text indicators pass 3:1: toggle tracks, form borders, pins against the map, focus rings. | 4 | Every indicator the audit measured now passes in **both** modes. Normal / high contrast: toggle track 3.37 / 6.66, form and chip borders 3.37 / 6.66, dot outlines 3.37 / 6.66, scanned-pin rim 5.04 / 8.04, estimated-pin stroke 3.59 / 8.09, progress track vs ground 3.29 / 3.02, progress-arc rim vs track 3.39 / 3.39, nav current-tab bar 9.62 / 13.25. Four tokens (`--edge`, `--track`, `--marigold-edge`, `--ring-rim`) carry all of it. **Round 4 (asset library):** re-measured. The tokens that carry 1.4.11 were all re-derived from the official palette against their stated targets and all pass: `--edge` #8C889F 3.42:1 on white and 3.01:1 on lavender100, `--edge-strong` #77728D 4.51:1 on the brightest street, `--track` #86839A 3.01:1 on the ground, `--blue-edge` sky700 4.45:1 on the worst ground tone, `--marigold-edge` indigo900 13.13:1, `--ring-rim` indigo900 4.86:1 on the track and 10.81:1 on marigold400. The new dark chrome adds two: the location pill and the round buttons on the indigo900 bar carry a #78748E hairline at **3.98:1** against the bar, with white content on a #373158 fill at 12.05:1. The tier-tinted hairlines on badges and chips (sky400 on white 2.14:1, marigold400 fills) are **the library's own badge idiom** &mdash; its Estimated badge is literally a #69B7FF hairline on white &mdash; and each of those components carries a text label and a glyph, so neither the control nor its state is identified by that hairline; they were at the same ratios before this round. |
| 7.3 | Every screen announces what it is when it becomes active. | 4 | All 26 screens now carry an `aria-label` (12 had none) and `tabindex="-1"`; `showScreen()` moves focus onto the screen, which is a labelled region, so the name is announced by the focus move. Walked all 26: `focusIsScreen: true` on every one. |
| 7.4 | Focus moves sensibly on every screen and sheet change, and returns on close. | 4 | Screen change: `document.activeElement` is the new screen on all 26 (was `BODY`). Sheet open: focus lands on the sheet heading (`H3.sheet-h`; the card sheet lands on `H2.card-name`). Sheet close: focus returns to the opener - Filters FAB after Escape, and the originating **pin** after the card closes, re-found by id across the re-render. `closeSearch()` returns focus to `#search-btn`. A nav token abandons the restore if the app navigated instead. |
| 7.5 | Blocked actions and errors are announced, not only shown. | 4 | `toast()` now routes through `announceUI()` - every toast reaches `#sr-announce` (verified: region text matches toast text). Submit claim unchecked: screen holds, `aria-invalid="true"`, `aria-describedby="claim-authz-err"`, inline error shown, focus on `#claim-authz`, announced "Claim not submitted...". Publish with the face-flagged photo (from both `ow-photos` and `ow-review`): inline error naming photo 3, `aria-invalid` on the publish button **and** on the Crop control, focus on Crop, announced. Checking the box / cropping clears all of it. |
| 7.6 | What is announced matches what is shown, at every moment. | 4 | The transparent tick is `aria-hidden` in all three places (`.ci-dot`, `.p-ring`, `.tl-dot`). The checklist is a real list whose per-item state text is written by `setCheckState()` at the moment the class lands. At t=0: "Doorway framed - not checked yet ..." (was "tick Doorway framed tick Entry path visible tick Photo quality checked"). Sampled through a full run: **zero** frames where announced-done != visual-done. |
| 7.7 | Every state a sighted user gets from the map is available as text. | 4 | One `placeSentence()` now feeds both the list row and the pin. 64/64 pins name their match state: "Royal Blue Grocery. 241 W 3rd St. Scanned on-site. Good match, 3 of 3 needs. Seen 2 days ago. 300 ft. Seen: Step-free entry, Wide door, Easy-grip handle, Clear approach." Was "Royal Blue Grocery - Scanned on-site". |
| 7.8 | Keyboard alone completes every flow; Escape closes what it opens; nothing behind a scrim is reachable. | 4 | Escape closes the search overlay and all 8 sheets. With a modal sheet open: `aria-modal="true"`, background `inert` (live regions exempted), **0** focusables reachable outside the sheet (was 76), Tab trapped. Tab order on the map: search, list toggle, zoom, locate and both FABs at indexes 1-9, then a "Skip the 64 map pins" control, then the pins (first pin at index 10; was index 0 with 64 pins ahead of search). Scan flow walked with real Tab presses: primer -> Close scan -> Allow camera -> capture -> Cancel scan -> Capture photo. No element anywhere in the app has a click handler without a native control under it (swept: 0 non-native clickables), so Enter/Space activation is the UA's. |
| 7.9 | Roles are correct and never destroy a native one. | 4 | 0 `button[role="listitem"]` in the document. Saved, My scans and My corrections are `UL role="list"` > `LI` > `BUTTON`, matching the list view. Seven labelled `<div>`s got a real role; 0 remain. The non-modal card sheet is `role="region"`, not `dialog`. Freshness is a labelled group with `aria-pressed`; the claim result is a `radiogroup` of `radio`s with a roving tabindex, arrow keys and a visible tick. |
| 7.10 | Reduced motion removes animation without removing feedback. | 4 | Re-verified after the changes: sheet, checkitem and ring transitions all 1e-05s, `#ringwrap` `display:none`, the determinate bar at 100%, all three checks landed, "Checks complete. 3 features identified." still announced, checklist text agrees. **Round 4 (asset library):** re-verified alongside 4.5. |
| 7.11 | Text scaling to the largest setting clips nothing. | 4 | Top step raised from 17.4px (+16%) to 18.9px (+26%). Swept all 26 screens at Default, Larger, and Larger + high contrast: the set of overflow findings is **identical** across all three and every entry is a `.sr-only` element or clipped map geometry - no visible text clips. The toast, the one failure in Round 0, now wraps: 358px wide, 3 lines, `scrollWidth == clientWidth`. **Round 4 (asset library):** re-measured at the largest setting in both contrast modes after the face change: **0** clipped text nodes and **0** horizontal overflow across all 26 screens. |
| 7.12 | Touch targets meet 44x44 including expanded hit areas. | 4 | The two failures are fixed. `#card-grip` 390x44 (padding grew, the 5px grip bar did not). `#search-clear` keeps its 34px disc with a `::before{inset:-5px}` hit area: all four `elementFromPoint` probes at +/-21px hit the button. **Round 4 (asset library):** re-measured across all 26 screens in all four modes: **0** targets under 44x44, counting a wrapping `<label>` as the target for the native radio and checkbox controls it wraps. |
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

---

**Round 3 (2026-09-05).** The map ground, and the three systems Round 2 deferred:
elevation, spacing, motion. Plus touch feedback and a palette-and-style consistency sweep
the product owner asked for by name. Everything below was driven in a browser at 390x844
over `python -m http.server`, walking all 26 screens.

**The sheet grew while this round was in flight.** Commit 2073c88 turned nine owner
directives into scored criteria, so the file is now **54 criteria, not 45**. Three of the
nine are Round 3's work and are rescored here (3.7 the map ground, 3.8 the palette-and-style
sweep, 3.6 re-verified); the other six are product and coverage work this round did not own
and did not touch. Restated on the 54-criterion sheet, Round 2's file scores **3.54** with
**8** criteria below 3.

**3.54 -> 3.83.** Criteria below 3 go **8 -> 1**.

**Is the bar met? Not quite, and it is worth being exact about why.** The average clears 3.5
comfortably. Every criterion this round owned is now at 3 or above, and every one of the
seven it was told to close is at 4. **One criterion remains at 2: 6.6**, the owner's "nothing
is 100% verified, which to me looks bad." That is not a systems defect and no amount of
elevation, spacing or motion moves it. The directive ledger already records why it is hard --
a rung above Owner-confirmed would be a compliance claim from photographs, which 6.4 forbids
and which is the whole honesty position -- and names the two answers that are real: publish
the 52 on-site scans the operator already took, and let confidence do the work the tier
cannot. Both are engine and data work, neither is scheduled, and neither belonged in a round
scoped to elevation, spacing and motion. **So: the average bar is met and the floor bar is
not, by exactly one criterion, and that criterion needs a product decision rather than a
design pass.**

Six other criteria stand at 3 rather than 4, each held there on a measurement rather than a
shrug: line length (1.3), the light blue still missing from light chrome (3.6), the splash
still animating on load (4.6), step-free coverage (6.7), and the three from the ledger that
need engine or manifest work (8.1, 8.2, 8.3).

*The map ground, and the regression it caught.* The brief called this the round's real work
and it was, but not for the reason it looked like. `design/map-ground.html` measured the
**shipped** ground breaking the contrast fix Round 1 landed: the tree dots were `#AFC2F2`
and `#C4D0F6`, scattered at random across exactly the blocks the estimated rings sit in, and
a ring landing on one measured **2.37:1** against a 3:1 floor. Decoration had quietly undone
an accessibility fix, and nobody would have seen it, because it only happens where a dot and
a ring collide. The rebuilt ground is **Terrain's colour on Relief's light** as recommended
-- warm sand ground, sage canopy, marigold plazas, cool lavender towers among warm putty
low-rise, with a two-step cast shadow and a lit top-and-left edge on every footprint and a
tonal ramp keyed to footprint mass -- on the derived road hierarchy (Congress, Guadalupe,
Lavaca and Cesar Chavez primary at 16px, the numbered cross streets secondary at 11px,
Colorado minor at 8px, four service alleys at 4.5px, with the three missing labels added).
The contrast is now hit-tested against the drawn SVG's own paint list rather than assumed,
and re-measured after every subsequent change in the round; the table is in 3.4. High
contrast **simplifies**: 1,711 shapes become 61, with zero circles and zero paths -- one
block tone, hard outlines, no shadow, no canopy, no plaza, and only the road hierarchy
surviving, because widths are structure and everything else was enrichment.

*The estimated blue, settled.* `pins-and-icons.html` said `#2C63C9` and `map-hierarchy.html`
said `#3F79DC`; worse, the shipped teardrop's token read `#3F79DC` while its own inline
fallback read `#2C63C9`, so the file disagreed with itself. Settled on **`#2C63C9`**: it is
the pin gallery's canonical value, it is what the level-3 ring -- the only marker that
touches raw ground with no white lift halo -- already shipped as, and it drops the ground's
luminance floor from 0.691 to 0.510, which roughly doubles the tonal range the ground may
use and is what makes this ground possible at 3:1 at all. `--blue-pin` is gone; one name.

*The three systems.*

- **Elevation (3.3, 3 -> 4).** 24 distinct shadows to 4 levels in 6 tokens, plus 5 named
  rings that were never elevation. 11 distinct values are painted across the whole app and
  every one is a token. High contrast redefines the level tokens centrally instead of
  hand-picking 11 components in two rules and missing everything else.
- **Spacing (2.2 and 2.3, 2 -> 4).** 40 values to a 10-step scale plus 7 layout constants;
  574 of 611 values resolve to a token and the 12 raw `px` that remain are the documented
  geometry sites, each commented with what it is anchored to. Nine boxes gave way to
  proximity, six treatments of "a quiet supporting note" became one, and three treatments of
  "a quoted note" became one.
- **Motion (4.1 and 4.2, 2 -> 4; 4.3, 3 -> 4).** 19 durations to 2 plus 4 named narrative
  constants; 7 easings to 2 curves plus 1 scoped spring. Screens push and pop by direction,
  the popup grows from its opener, sheets are 220 in and 160 out, the list rises and settles,
  chips arrive and leave.

*Touch feedback (5.3, 2 -> 4).* 44 of 47 interactive components now press, in two treatments
chosen by shape. The three that do not are named: the pin, which has something better, and
the two native inputs inside rows that press around them.

*The consistency sweep, which is the part with the interesting number.* Twenty distinct
classes of "the same thing looks different", found by inventorying every declaration in the
stylesheet by property and by selector rather than by looking at screens. Beyond the systems
above: **23 border-radius values** to five steps plus a pill, a circle and five named
geometries (69 declarations rewritten); **six border widths** for one control edge to one;
**three hairline colours** plus a fourth undeclared grey (`#D8CCF3`) to one token, with high
contrast darkening it centrally instead of patching `.prof-row` alone and leaving six other
row types light; **four alphas of translucent white** across twelve floating surfaces to
`--float-white`; **six row heights** (48/50/52/56/60/64) to three; an undeclared quiet fill
`#F8F7FD` at five sites to `--wash-quiet`; a fourth ink `#6C6486` on the chevrons and a
literal `#4A4463` on the diff arrow to `--sub`; a literal `#2A1A5E` progress rim to a token;
two docked-sheet top radii to one; two legends at two radii to one; the fabs' 26px and the
grip's 3px, which were pills written as numbers, to `999px`; the search field, which was
wearing the floating map shadow though it is a form control; and three privacy rungs carrying
an inline icon box instead of the one `--icon-box`.

*Deliberately not done.* The card sheet's three positions still change height without
animating. The `0fr -> 1fr` grid-row technique keeps collapsed content in the accessibility
tree, which would contradict the round that closed the screen-reader defects; decision 3 in
design-systems-spec defers it and this round honoured that. Every other motion item was
independent of it. `revealSelected()` is still called twice around the position change -- once
immediately so the pan starts with the sheet, once after it settles -- and the second call is
on a timer, never `transitionend`.

*Round 1 and Round 2 re-verified, nothing regressed.* All 26 screens take focus on change
(**26/26**); **0** duplicate ids; **0** `button[role="listitem"]`; **64/64** pin accessible
names still carry match state, freshness and distance; pin tips still land on their coordinate
at max |dx| = |dy| = **0.00px**; `toast()` still reaches the live region; all **7** sheets
close on Escape, the Filters sheet lands focus on its heading (`H3.sheet-h`), traps it (**0**
focusables reachable behind the scrim), is `aria-modal`, and returns focus to its opener;
`closeSearch()` still returns focus to `#search-btn`. Reduced motion re-verified through a
full scan run. Text scaling swept at Default / Larger / Larger+high-contrast: **81 overflow
findings at every setting, identical to the pre-round file at every setting**. The two-tone
wordmark still renders in two inks (`#1D5FA8` and `#4B2E9E`) and the bottom bar still carries
three different tab colours (`#1D5FA8` map, `#6E4A00` scan, `#4A4463` profile). Touch targets:
the only sub-44px controls are the two 20x20 claim inputs inside 44px+ labels, as since Round
1. **No horizontal scroll on any of the 26 screens** once the push animation settles -- the
2-4px seen mid-flight is the 12px travel itself, clipped by the phone's `overflow:hidden`.
File is **0 non-ASCII bytes**, one inline script, no external scripts, single self-contained
HTML. **Console is silent** across a full walk of all 26 screens plus high contrast, zoomed
out, the card at all three positions and the list toggle.

*Two places I went off-spec, recorded rather than quietly taken.*

1. **The hairline stays `#DCD6F2`, not the spec's `#EDEAF7`.** design-systems-spec 3.2 was
   written before Round 2 chose `#DCD6F2` for the card boundary. Adopting the lighter value
   would have visibly undone Round 2's card treatment, so the consolidation used Round 2's
   measured value for all nine sites instead. One token either way; the spec's intent is met
   and the newer decision wins.
2. **The merged note is `--fs-sub`, not the spec's `--fs-meta`.** Two of the six notes live on
   the accessibility settings screen, and shrinking supporting copy there is the wrong
   direction. Six treatments still became one, which is what the criterion measures.

*Known and unchanged.* The seven pins whose 44x44 centre is covered by floating map chrome
are pre-existing overlay behaviour with the list view as the canon-mandated equivalent path.
Line length in row sub-copy (1.3) is a layout question, not a token question, and is the one
criterion in the file where the measurement got worse-looking because it finally got taken
properly.
**Round 4 (2026-09-05) -- the approved asset library.** The product owner supplied
`design/board-refs/mockups-final/`: 63 editable SVG masters, PNG exports, official
design tokens, a contrast report, and six final boards. It supersedes the palette and
the marks the build had grown by hand. This round makes the build match the assets
instead of approximating them.

*What was adopted.* Eleven official colours are now the only authored colours in the
file; every other colour is one of them or a stated two-step mix of two of them. The
three tier pins, the three match halos, the tier badges, the confidence dots, the
freshness pill, the five provenance marks, the Texas record, thirty icons and the
brand mark and wordmark are the library's own path data. The map header and the bottom
nav are the boards' indigo900 chrome, which is what finally closed 3.6.

*What had to be derived, and why.* The library ships no token for a second or third
ink, for a tier ink that clears its own 7:1 body-text rule, for a washed tint, for a
non-text boundary, for a progress track, for press feedback, for the phone shell, or
for any of the seventeen map-ground tones. Each of those is now solved numerically as
a mix of two official colours against a stated contrast target, and the mix is written
into the source beside the value. Nothing kept its old hue.

*Two adaptations of library assets, both stated in the source.* The Estimated pin's
dashed outline is drawn in sky700 rather than sky400, because the library's own report
lists sky400 as the ON-DARK sky and it measures 1.63:1 on this map's ground &mdash; sky700
is the on-light sky the very same asset already uses for its italic i. The Scanned
pin's body rim is indigo900 rather than white, because marigold400 is 1.22:1 on the
worst ground tone and a white rim would leave the mark with no boundary; indigo900 on
marigold400 is what the library's own Scanned badge strokes that fill with.

*What the palette swap nearly broke, and what caught it.* Two regressions were found by
measurement and neither was visible: Atkinson Hyperlegible Next's figures are
proportional where Nunito's were tabular, which would have pulled every numeric column
out of line (89.21px over ten digits); and 19 of 402 text nodes fell silently out of
the UI face because it carries no glyph for the arrows, ticks and dingbats the chrome
was drawing with. Both are fixed. This is the risk the round was warned about and it
was real.

*The font.* Atkinson Hyperlegible is designed for low vision and is the better face for
this product on the merits. The original family ships only 400 and 700, which cannot
carry a three-weight ladder, so the variable "Next" cut (200-800) is used and the
ladder is re-pitched to 500 / 650 / 800 &mdash; the weights the library's own assets are
drawn in. Both it and Nunito Sans (which the official wordmark SVGs name) load from
Google Fonts alongside the existing arrangement; the file is still one self-contained
document with no local assets.

*Verified by measurement*, served over http at 390x844, across all 26 screens, in four
modes (normal, high contrast, and each at the largest text setting): 0 text-contrast
failures, minimum non-large ratio 6.42:1; 0 targets under 44x44; 0 horizontal overflow;
0 clipped text; 0 duplicate ids; 0 console errors on a cold load and after a full sweep
of every screen in both contrast modes; 402 of 402 text nodes in the UI face; digit
spread 0.00px. Pins against the drawn ground, normal and high contrast, modal and worst
tone and receded to 80%: 24 figures, all over 3:1, 22 of them better than the Round 3
figure they replace (the two that are not are the estimated and owner marks on the modal
tone in normal contrast, 4.55 and 4.83 against 4.74 and 5.35 -- every worst-case and every
receded figure improved).

**Average across all 54 criteria: 3.85** (3.8519, was 3.8333). 3.6 moved 3 to 4. Nothing else
moved, and nothing regressed.

*Is the bar met?* The bar is "nothing below 3 and the average 3.5 or better". The
average clears it comfortably and did before this round. **The bar is not met**, and
Round 4 did not aim to meet it: 6.6 still sits at **2** &mdash; there is no path in the
product by which a place reaches full confidence, which is a product decision the owner
has to make, not something a systems round can invent. Six more sit at 3 (1.3 line
length, 4.6 load animation, 6.7 step-free answered at the door, 8.1 scan sequence, 8.2
photo storage, 8.3 home-screen icon). Those seven are the whole remaining list, and none
of them is a palette or an asset problem.
