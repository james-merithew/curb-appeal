# Responsive specification

## Breakpoints

| Range | Layout behavior |
|---|---|
| 320–374 px compact phone | 16 px page gutters; one-line header location truncates; sheets use 92% full stop for receipts; feature chips stack; 48 px controls remain unchanged. |
| 375–429 px standard phone | 20 px gutters; default mockup composition; sheets use 18%, 54%, and 92% stops; two compact filter chips may share a row. |
| 430–599 px large phone | 24 px gutters; business summary may show freshness and confidence side by side; cap readable content width at 520 px. |
| 600–1023 px tablet | Map remains primary; business details become a 360–440 px side sheet in landscape and a bottom sheet in portrait; bottom navigation may remain centered at max-width 520 px. |
| 1024 px and wider demo/projector | Render a centered phone-safe UI or landscape map with a 420 px detail rail; increase map pin ladder uniformly by up to 1.25×; never reduce contrast or line-style differences. |

## Safe areas and text scaling

- Add device top/bottom safe-area insets outside the minimum control dimensions.
- Keep the selected map pin inside the visible map region as sheets move.
- At 200% text size, allow cards, filter rows, provenance lines, and buttons to grow vertically; do not clip or scale text down.
- Bottom navigation labels remain visible at all supported phone widths.
- On a narrow phone, collapse secondary metadata onto a second line before truncating the business name.
- Source photos use a fixed visual aspect ratio with descriptive alternative text; cropping never hides the entrance threshold.

## Projector mode

- Use deep indigo text on white/lavender or white text on deep indigo.
- Body text targets at least 7:1; line work remains at least 3 px after projection scaling.
- Trust tiers remain shape + icon + color; match remains line style + label/color.
- Suppress dense minor map labels before suppressing evidence labels.
- The scan sequence stays under eight seconds and is the only theatrical animation.
