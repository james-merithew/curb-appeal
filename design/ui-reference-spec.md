# Curb Appeal — UI reference spec (canon as of 2026-09-03)

Derived from James's chosen reference mock (save the image alongside this file).
This supersedes the exploratory pages (`map-ui-directions.html`, `map-ui-hybrids.html`);
those remain as archives.

## Design tokens

- **Ground**: soft lavender/periwinkle map canvas (#EDEBFA-ish), white cards, generous
  radius (~16px), airy spacing. Buildings pale, streets white, trees dotted blue.
- **Accents**: marigold (scan/action + Scanned tier), purple (Owner tier + links/actions),
  soft blue (Estimated tier + feature icons), teal/green reserved — see rules below.
- **Type**: rounded humanist sans throughout (reference uses a single family; the
  editorial-serif option from Field Notes was not carried into the reference).
- **Nav**: bottom bar Map · **Scan** (center: outlined circle with camera glyph, marigold
  ring — the v2 treatment, James's pick 2026-09-03) · Profile.

## Trust tiers (three, fixed wording)

| Tier | Pin | Notes |
|---|---|---|
| Estimated | hollow pin, dashed blue outline, italic ⓘ | never gray, never reads negative |
| Scanned on-site | solid marigold pin, person glyph, segmented ring | the trust workhorse |
| Owner-confirmed | solid purple pin, storefront glyph, OUTLINED check floating beside | no shield, never "verified" |

- Pins only upgrade. No negative state exists anywhere.
- Match halo when a needs profile is set: labeled chip ("Good match") + halo;
  good=solid / partial=dashed / unknown=dotted (line style + color, never color alone).

## External-data accessories

- **TABS/state record**: small Texas tab on the pin shoulder (reference shows the flag;
  at small sizes prefer the lone-star outline — flags turn to noise below ~24px).
  Card row: "Texas accessibility inspection on record · <year>" with chevron to receipt.
- Other sources (OSM etc.): provenance rows on the card only, each with source glyph,
  label, and date. External data never fills ring segments or chips.

## Card anatomy (bottom sheet, top to bottom)

1. Tier avatar + business name + tier chip.
2. Two tiles: **Freshness** ("2 days ago", clock icon — ages to muted amber, worded
   about time) and **Confidence** ("High" + dot-triple).
3. Provenance rows (receipts): camera row "Photographed Tuesday — 4 neighbors, 1 owner",
   then external-source rows. Every row opens its receipt (photo/date/method).
4. Feature chips: icon + feature name + dot-triple confidence (●●○). Named by what was
   seen ("Step-free entry", "Wide door", "Easy-grip handle") — never legal claims.
5. Unknown row: "Not yet seen — be the first to scan." (invitation, not apology).
6. "Suggest a correction" (purple, pencil icon) — on every card.
7. Buttons: **My needs** (heart) · **How trust grows** (the trust-explainer page).

## Color rules (resolved tensions)

- **Green is reserved for match state** ("Good match" chip) and nothing else — confidence
  dots use the tier's own hue or neutral teal, NOT green, so green never leaks toward
  "verified accessible" semantics.
- Amber = freshness aging only. Red does not exist in the product.

## Signature animation (live scan)

Photo in → ~7s processing (progress ring, checklist items ticking in one by one) →
pin drops with bounce + ripple, chips populated, counter ticks. Under 8 seconds;
prefers-reduced-motion collapses to end state.

## Baked-in elements beyond the mock (all previously agreed — required, not optional)

1. **Map layers**: a "State records" toggle lighting every TABS-matched pin at once
   (the demo beat), and the **route layer** — Austin curb-ramp/sidewalk condition as
   corner markers + path shading between user and door ("Curb ramp at corner ·
   condition B · City of Austin").
2. **My-needs picker**: one-time, skippable profile (wheelchair · cane/walker · low
   vision · limited grip · stroller); persona seeds default feature weights from the
   researched persona-feature matrix, individually tunable. Once set, pins show
   good/partial/unknown match halos and cards re-highlight the chips critical to
   THAT persona. Trust tier is never a filter facet.
3. **Estimated-tier CTA**: its provenance line always ends with the replacement
   invitation — "Estimated by AI from street imagery · <date> — been here? Confirm in
   30 seconds." The AI glyph is the sparkle ✦ with a dashed circle. The estimate
   visibly wants to be replaced; that is the growth loop.
4. **Scan accepts whatever the user has**: in-app camera, camera-roll upload, 1 photo
   or 6. One photo yields an honest partial checklist; when coverage is thin the app
   asks "got it — one more photo from further back?" instead of guessing. A disabled
   user who can only upload one photo is a first-class citizen.
5. **Owner funnel**: "Claim your door" banner — get scanned, get seen; missing-feature
   fixes "may qualify for federal tax credits — ask your accountant" (Section 44/190,
   never stated as tax advice). Owner/verified-tier captures are in-app only with
   time+location attestation (anti-staging); camera-roll uploads cannot earn the
   owner tier.

   **Claim flow (canonical, per James 2026-09-03):**
   Public map → "For business owners" → Claim your door → find & select business →
   submit ownership confirmation → pending review → approved → **My business workspace**.
   - Ownership confirmation options (GBP-style): call/text to the number already on
     the public listing, email at the business domain, or an in-store-delivered code
     entered from the workspace. Demo scale: "pending review" = manual approval by us;
     the flow is unchanged when it automates.
   - A claim NEVER changes the public pin by itself — only the workspace's attested
     capture can earn the Owner-confirmed ring.
   - Workspace contents: the pin as customers see it, claim status, the guided
     capture flow, correct/dispute channel, tax-credit explainer.
6. **How trust grows** page: the tier ladder explained with receipts philosophy
   ("every badge opens into its evidence"), method + error-rate disclosure lives here
   once (Zestimate pattern), and the roadmap line: "as licensed accessibility
   specialists join, a fourth ring lights up."
7. **Privacy is invisible but stated**: faces are auto-blurred and GPS is stripped at
   upload; a one-line note in the scan flow says so. Frames where a face survives
   blur are auto-quarantined without costing the door its verdict — the user never
   performs a privacy step.
8. **Freshness guard on identity**: pins resolve to live place_ids; a business Google
   marks closed gets its pin retired from public view (never shown as a negative —
   it simply leaves the map).
9. **Disagreement handling**: when sources conflict (AI vs OSM vs owner), the card
   shows the neutral form only ("owner reports X; a scanner measured Y — help us
   re-check"); disagreements otherwise stay internal as scan priorities.
10. **Language rules everywhere**: features not legal claims; "not visible" never
    rendered as "absent"; wording about time, never about the place; no red, no
    public negative state, anywhere, ever.
