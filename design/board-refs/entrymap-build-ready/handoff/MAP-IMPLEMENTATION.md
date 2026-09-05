# Map implementation

## Rendering stack

1. The selected map provider renders geographic base layers.
2. EntryMap applies provider-style equivalents for land, blocks, roads, labels, parks/water, and building footprints.
3. The application renders trust pins as custom overlays using `asset-library/svg/pins`.
4. Match halos, selection, freshness, and clusters are independent overlay layers.
5. Bottom sheets and nearby-result cards are application UI, not map annotations.

The eight `map-kit` variants demonstrate composition and state; they do not supply navigation data.

## Layer and z-order contract

| Layer | z-index | Rule |
|---|---:|---|
| Provider geography | 0 | Never encodes EntryMap trust. |
| Mixed cluster | 10 | Count plus three composition arcs; never looks like a trust pin. |
| Estimated | 20 | 32/40/52 px by overview/street/selected context. |
| Scanned on-site | 30 | 36/44/56 px by context. |
| Owner-confirmed | 40 | 40/48/60 px by context. |
| Match halo | 50 | Solid/dashed/dotted external outline. |
| Selected | 60 | White keyline, 6 px lift, approximately 12% scale. |
| Live scan | 70 | 64 px during the single drop; settles to street size. |

Receipt pin sizes are 24/28/32 px. Freshness uses a muted-amber clock overlay without recoloring a pin. Texas provenance is omitted from map pins.

## Camera behavior

- Recenter and selected-business camera changes use the 450 ms map timing token.
- Preserve the selected pin’s screen position while a bottom sheet opens.
- Cluster overlapping unselected pins before labels or icons become illegible.
- Recalculate clusters after meaningful zoom completion, not every animation frame.
- Filter changes crossfade affected pins over 180 ms; relevant pins rise 4 px while halos draw.
- In reduced motion, update camera and overlay state immediately while retaining spatial context.

## Provider styling translation

- Land: `#F5F2FC`; secondary blocks/buildings: `#E8E1F7`; entrance-path lines: `#CFBCEE`.
- Roads: white cores with lavender edges; keep important street names deep indigo `#1E1142`.
- Optional water/park accents may use sky `#76BCFD` at reduced opacity, never as trust markers.
- Suppress provider POI icons that compete with EntryMap pins.
- Validate label and road contrast on device and on a grayscale projector.

## Map accessibility

- Mirror visible entrances in a nearby-results list ordered by distance and current filter match.
- A pin’s accessible name is “{business name}, {trust tier}, {match result if profile exists}.”
- Expose zoom, recenter, search area, list view, and selected-business close controls outside gesture-only map interactions.
- Do not announce each cluster recalculation; announce the resulting count only after the map settles.
