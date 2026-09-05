# EntryMap demo-map kit

This folder contains eight reusable 1170×800 map compositions as editable SVG and PNG preview files. They reproduce the approved visual language without embedding a proprietary map or claiming geographic accuracy.

## Variants

- `base-map`: land, blocks, roads, labels, and place accents only.
- `before-profile`: the fixed trust ladder without needs-match halos.
- `after-profile`: the same entrances with solid, dashed, and dotted match halos.
- `selected-business`: a selected Scanned on-site entrance without recoloring its trust pin.
- `empty-area`: invitation-led state with no negative grade.
- `mixed-cluster`: count marker with sky, marigold, and violet composition arcs.
- `pin-placement`: entrance anchors, tier size, and halo placement guidance.
- `safe-areas`: visible map area beneath app chrome and bottom sheets.

## Stable SVG groups

`land`, `blocks`, `roads`, `labels`, `places`, `halos`, `pins`, `selection`, and `annotations` are addressable layers. Production code may toggle or replace them independently.

## Important boundary

These are demo and prototype visuals, not geographic truth, navigation data, routing geometry, or a substitute for Mapbox, MapLibre, Google Maps, Apple Maps, OpenStreetMap, or another provider. In production, translate the layer colors, label hierarchy, and visibility rules into the selected provider’s style system and render EntryMap pins/halos as application overlays.

The map SVGs reference the canonical assets in `asset-library/svg/pins` and `asset-library/svg/halos`; do not trace or redraw those symbols.
