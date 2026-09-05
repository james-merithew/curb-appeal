# EntryMap production asset library

This package contains 98 editable SVG UI masters, mobile-ready PNG exports, and two byte-locked approved brand PNG sources. The mockup boards remain at the ZIP root.

## Immutable brand source

The logo and wordmark must never be reconstructed, retyped, recolored, traced, or regenerated. Use the approved PNG files in canonical-brand exactly as supplied. Transparent, monochrome, light-background, app-icon, and vector variants are intentionally omitted because no approved source artwork exists for them.

## Canonical sampled palette

- Deep indigo #1E1142: sampled approved background; app chrome and high-contrast text.
- Violet #4F34DB: sampled approved logo field; Owner-confirmed pins and primary icons.
- Sky blue #76BCFD: sampled approved entry wordmark; Estimated pins and information cues.
- Marigold #FDB327: sampled approved logo arc; Scanned on-site pins and Scan action.
- Lavender path #CFBCEE: sampled approved entrance path.
- UI lavender tints #F5F2FC and #E8E1F7: lightened supporting surfaces.
- White #FFFFFF: sheets, cards, and dark-surface type.

Body copy uses deep indigo or dark violet. Accent colors are not used for small body text.

## Fixed trust ladder

1. **Estimated**: hollow white pin, dashed sky-blue outline, italic i, 0-of-3 ring.
2. **Scanned on-site**: solid marigold pin, person icon, 2-of-3 ring.
3. **Owner-confirmed**: solid violet pin, storefront icon, 3-of-3 ring, separate outlined check.

Do not use shields, the word “verified” for owners, a fourth tier, red, gray, or negative grades. Texas state records are provenance only.

## Folders

- canonical-brand: byte-identical approved full logo and app-header lockup.
- svg/pins: the three fixed trust tiers.
- svg/halos: solid/dashed/dotted needs-match states.
- svg/ui-icons: navigation, actions, trust, and receipt controls.
- svg/feature-icons: the seven allowed visually confirmed entrance features plus unknown.
- svg/provenance: photo, community, owner, public record, and Texas marks.
- svg/badges: trust, freshness, and confidence components.
- svg/states: reusable empty, permission, processing, success, offline, and re-check illustrations.
- svg/motion: pin-drop reference frames.
- png: raster exports organized by category and size; no generated logo variants.
- tokens: JSON and CSS design tokens, including reduced-motion behavior.

## Interaction notes

Pins upgrade only. Tapping any claim opens a receipt with source photo, date, method, stacked provenance, freshness, confidence, and “Suggest a correction.” Match halos communicate good/partial/unknown through line style as well as color. The live scan lasts about seven seconds; the pin drop takes 620 ms and collapses to the end state when reduced motion is enabled.

## Type

Use Atkinson Hyperlegible for UI where available, with Aptos/Arial fallbacks. The EntryMap wordmark is approved artwork, not live text; never substitute a font.

## Interaction component library

- controls: primary, scan, secondary, quiet, pressed, focused, and unavailable states.
- navigation-states: active Map, Scan, Profile, and keyboard-focus treatments.
- chip-states: filters plus fresh, aging, and unknown feature claims.
- field-states: empty, focused, filled, and needs-attention without red.
- feedback: saved, published, offline, and camera-permission patterns.
- sheet-states: 18%, 54%, and 92% bottom-sheet stops with a visible drag handle.
- scan-states: four progress checkpoints for the seven-second scan.
- receipt-elements: photo, Texas record, and correction rows.

## Pin hierarchy

Evidence controls the base size: Estimated is smallest, Scanned on-site is four pixels larger, and Owner-confirmed is four pixels larger again. Context then scales the entire ladder: overview 32/36/40 px, street 40/44/48 px, selected 52/56/60 px, and receipts 24/28/32 px. The live scan drop briefly uses 64 px before settling. Mixed clusters use a count plus three composition arcs and never masquerade as a single trust tier. See tokens/pin-hierarchy.json.
