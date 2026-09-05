# EntryMap visual language

Extracted from the six concept boards in `board-refs/entrymap-design-mockups/ui-concept-boards/`,
which are the canonical visual source, read against the current build. The boards predate the
rename, so they show the old wordmark; everything else in them stands.

This document exists because "make it stunning" is not actionable and "match board 03, panel 2"
is. Each section says what the boards do, what the build currently does, and the gap.

The overall character: **light, airy, generous**. Soft illustration, white cards on a pale
lavender ground, one confident purple, marigold reserved for action and the scanned tier.
Nothing is cramped and nothing is decorated. The single exception is the welcome hero, which
is now the logo's own deep aubergine, because the logo is newer canon than the boards and
because an all-lavender opening was the specific thing that read as flat.

---

## 1. Illustration

**Boards.** Soft two-tone line illustrations with real depth: a storefront with columns,
lanterns, potted plants and a yellow door, sitting inside a pale lavender circle. Street scenes
with buildings, trees and a figure. Line weight is light, fills are pale blue and lavender, and
the one saturated element is a marigold door or awning that draws the eye.

**Build.** Flat rectangles with square windows. Correct in structure, absent in charm.

**Gap — the largest single one.** The illustrations are the product's warmth. Every one needs
rebuilding as a real drawing: consistent 2px line weight, two pale fills plus one marigold
accent, sitting in a soft circular or rounded field. This applies to the scan primer, the
location primer, the empty states and the onboarding art.

## 2. Cards and rows

**Boards.** White, radius roughly 16px, a hairline lavender border rather than a heavy shadow,
generous internal padding. A row is: leading line icon in a consistent box, label, trailing
control or chevron, with hairline dividers between rows inside one card.

**Build.** Cards rely on shadow rather than border, padding is tighter, dividers are
inconsistent.

**Gap.** Adopt border-plus-soft-shadow at one elevation level, raise padding, and make every
row use the same leading-icon box so labels align down the column.

## 3. Selection

**Boards.** Unselected is an empty ring on white. Selected is a filled purple disc with a white
tick, **and** the whole row gets a pale purple tint with a purple border. The state is legible
from across the room.

**Build.** Selection is mostly a tint or a border, and the tick treatment varies.

**Gap.** One selection component, used everywhere: needs picker, filters, notification toggles.

## 4. Buttons

**Boards.** Primary is solid purple, full width, radius roughly 12px, generous height.
Secondary is **white with a purple border**, never a grey fill. Tertiary is plain purple text.
The one deliberate exception is the camera permission, where the primary is **marigold**,
because it is the moment the product asks for something rather than offers something.

**Build.** Secondary was a grey-lavender fill; the welcome now uses the outline. The marigold
permission button is not implemented.

**Gap.** Outline secondary everywhere, and marigold for the camera ask specifically.

## 5. Pins

**Boards.** Chunky and confident. A filled teardrop with a white glyph inside: an information
mark for estimated, a person for scanned on-site, a storefront for owner-confirmed, with the
owner pin carrying a separate outlined tick. Each sits on a soft white halo that lifts it off
the map. Estimated is a dashed outline rather than a fill, which reads as provisional at a
glance.

**Build.** Pins are small and thin-stroked, and read as generic markers rather than as three
distinct tiers.

**Gap.** Increase size and weight, put the real glyph inside each, add the halo, keep the
dashed treatment for estimated.

## 6. The map itself

**Boards.** Building footprints in two or three pale tones so blocks have texture, tree
clusters as soft blue rosettes, street names set in small caps along the street, and a visible
distinction between street and block.

**Build.** Flat white blocks, thin lines, sparse trees.

**Gap.** Vary the block fills, thicken the streets slightly, and let the street labels sit
along the roads rather than floating.

## 7. The scan flow

**Boards, panel by panel.**

- **Primer.** Illustration in a lavender circle, a lock icon with "Only the doorway is
  captured", marigold "Allow camera", "Not now" as a text link.
- **Capture.** Real viewfinder with white corner brackets, a dark translucent coaching pill
  centred at the top ("Center the full doorway") and a second at the bottom ("Step back a
  little"), a dashed horizon line with a small centre circle, and a large marigold-ringed
  shutter.
- **Processing.** A large purple progress ring with the countdown inside it, then three named
  check rows, each a card with a circular icon and a progress indicator, then "Usually under 8
  seconds" and an explicit reduced-motion note.
- **Review.** The photograph, "Visually confirmed" with feature chips, then Retake as outline
  and Publish scan as solid purple.
- **Published.** A mini map showing all three tiers with a legend, and the provenance row.

**Build.** The self-drawing ring and named checks are implemented and are the strongest motion
in the product. Missing: the countdown inside the ring, the corner brackets and dual coaching
pills, the marigold shutter ring, and the mini map with legend on the published screen.

## 8. Typography

**Boards.** Two levels do most of the work: a bold two-line headline at roughly 24px with tight
leading, and a lighter grey subtitle at roughly 15px with generous leading. Row labels are
medium weight, not heavy. Weight 900 appears only in the wordmark.

**Build.** Weight 900 is used very widely, which flattens hierarchy, and display text carries
body leading.

**Gap.** Reserve the heaviest weight for the wordmark and headline numbers. Row labels drop to
600 or 700.

## 9. What the boards get right that the build must not lose

- 44px targets and 7:1 text contrast are called out on the boards themselves. They are part of
  the visual language, not a constraint applied afterwards.
- The Texas flag appears only as provenance, never as a badge.
- Pins communicate evidence source and strength, never a rating.
- "Sources, dates, and confidence — not a badge" is printed on board 02. That sentence governs
  every surface.
