# EntryMap production asset library

This package contains 107 editable SVG masters plus mobile-ready PNG exports. The mockup boards remain at the ZIP root.

## Brand system

- Deep indigo #17103D: app chrome, high-contrast text, dark surfaces.
- Logo violet #5B35F5: core brand mark, primary icons, Owner-confirmed pins.
- Sky blue #69B7FF: Estimated pins and informational cues.
- Marigold #FFBF24: Scanned on-site pins and the Scan action.
- Pale lavender #F2EEFF: canvas and quiet supporting surfaces.
- White #FFFFFF: sheets, cards, and dark-surface type.

Body copy uses deep indigo on white or pale lavender. Accent colors are not used for small body text.

## Fixed trust ladder

1. **Estimated**: hollow white pin, dashed sky-blue outline, italic i, 0-of-3 ring.
2. **Scanned on-site**: solid marigold pin, person icon, 2-of-3 ring.
3. **Owner-confirmed**: solid violet pin, storefront icon, 3-of-3 ring, separate outlined check.

Do not use shields, the word “verified” for owners, a fourth tier, red, gray, or negative grades. Texas state records are provenance only.

## Folders

- svg/brand: logo, wordmark, app icon, favicon, monochrome variants.
- svg/pins: the three fixed trust tiers.
- svg/halos: solid/dashed/dotted needs-match states.
- svg/ui-icons: navigation, actions, trust, and receipt controls.
- svg/feature-icons: the seven allowed visually confirmed entrance features plus unknown.
- svg/provenance: photo, community, owner, public record, and Texas marks.
- svg/badges: trust, freshness, and confidence components.
- svg/states: reusable empty, permission, processing, success, offline, and re-check illustrations.
- svg/motion: pin-drop reference frames.
- png: raster exports organized by category and size.
- tokens: JSON and CSS design tokens, including reduced-motion behavior.

## Interaction notes

Pins upgrade only. Tapping any claim opens a receipt with source photo, date, method, stacked provenance, freshness, confidence, and “Suggest a correction.” Match halos communicate good/partial/unknown through line style as well as color. The live scan lasts about seven seconds; the pin drop takes 620 ms and collapses to the end state when reduced motion is enabled.

## Type

Use Atkinson Hyperlegible for UI where available, with Aptos/Arial fallbacks. Use Nunito Sans for the joined lowercase EntryMap wordmark when reconstructing it in code; production interfaces should use the supplied SVG wordmarks.

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
