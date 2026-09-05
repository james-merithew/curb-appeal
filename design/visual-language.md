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

---

## 10. Map hierarchy and density

The map currently renders every place as the same pin at the same size. With sixty-four of them
in a few blocks the screen reads as noise: no focal point, no reading order, and no way to tell
at a glance which markers are worth attending to. Same-size pins also waste the one thing a map
has that a list does not, which is the ability to say what matters by how it looks.

**The hierarchy encodes evidence strength, and nothing else.** Not accessibility quality, not a
rating, not a recommendation. This is the board's own rule, printed on board 02: pins
communicate evidence source and strength. A bigger pin means we know more about that entrance,
never that the entrance is better. Stated that way the hierarchy is not only defensible, it is
the most honest thing the map can do, because the weakest evidence currently shouts as loudly as
the strongest.

**Four levels.**

| Level | Tier | Treatment | Why |
|---|---|---|---|
| 1 | Owner-confirmed | Full pin, largest, purple, storefront glyph, tick badge, halo | Rarest and strongest evidence: someone at the door attested to it |
| 2 | Scanned on-site | Full pin, medium, marigold, person glyph, halo | Somebody stood there and photographed it |
| 3 | Estimated | A small dashed ring, no glyph, no teardrop | It marks that a door is probably there without borrowing the visual weight of evidence |
| 4 | Cluster | One numbered disc | Density, not a place |

Level 3 is the change that does most of the work. Estimated is both the most numerous tier and
the weakest claim, and drawing it as a full pin is what makes the map look busy and overclaim at
the same time. As a quiet dashed dot it becomes texture: present, countable, tappable, and
clearly provisional.

**State modifiers, applied on top of the level.**

- **Selected** scales up and takes a stronger halo; everything else drops slightly in opacity.
  Nothing is ever hidden.
- **Needs match**, when a needs profile is set: matching places hold full opacity and take the
  match ring; non-matching recede in opacity only. Recession is not a negative verdict, and no
  mark is ever added to say a place fails.
- **Zoom out** collapses estimated entirely into cluster counts, leaving only levels 1 and 2 as
  pins, so the wide view answers "where has anyone actually been" rather than "where are there
  doors".

**Density rules.**

- Where two markers overlap by more than about 40%, the weaker level yields: an estimated ring
  merges into a cluster before a scanned pin does, and a scanned pin yields before an owner pin.
- Around a dozen full pins is the ceiling at phone width. Past that, cluster.
- The selected place is exempt from every rule above: it is always drawn, always on top.

The result is a reading order the eye follows without instruction. The few purple pins first,
the marigold ones next, and the estimated rings registering as ground texture rather than as
sixty-four competing items.

---

## 11. Map ground: depth and colour

Two complaints, and they are separate problems with a shared answer.

**"The map is so flat."** Every block is the same tone, every street the same width, and the
trees are token dots. There is no road hierarchy, no landcover, no implied light, and nothing
sits on top of anything else. A real map reads as a place because it has all four.

**"Use more of the icon colours within the map."** The ground is nearly monochrome while the
palette carries five hues, so the map looks unrelated to the product sitting on top of it.

**The constraint that shapes the answer.** Blue means estimated, marigold means scanned on-site,
purple means owner-confirmed, green means needs-match and amber means ageing evidence. Those
meanings are load-bearing and they live on markers. If the ground starts using the same hues at
the same strength, a green park becomes indistinguishable from a match halo and the palette
stops meaning anything.

So the rule is **saturation, not hue**. The ground may echo the whole palette, but only at a
saturation and value where it reads as terrain and never as state. A marker must always be the
most saturated thing within its own radius. Concretely: ground hues stay well below the
saturation of any semantic colour, and no ground element ever uses a semantic hue at full
strength, ever carries a marker's shape, or ever sits inside a marker's halo.

**Depth comes from four things, none of which is a drop shadow on the map.**

1. **Road hierarchy.** Primary streets wider and brighter than side streets, alleys thinner
   again. Currently every street is one width, which is most of why it reads as a diagram.
2. **Block variety.** Building footprints in several close tones rather than one, so a block
   reads as many buildings instead of one slab.
3. **Implied light.** A consistent soft edge on the same side of every footprint. One direction,
   applied everywhere, is what makes footprints sit on the ground rather than float on it.
4. **Landcover.** Plazas, tree canopy, and water if any is in frame, as real areas rather than
   scattered dots.

**What must survive.** The three pins keep their measured contrast against whatever ground is
chosen, at 3:1 or better; a richer ground is the most likely way to break the fix that just
landed, so it is re-measured, not assumed. High contrast mode still simplifies the ground rather
than enriching it. The ground never competes with the card sheet for attention, and street
labels stay legible at phone size.

---

## 12. The wordmark and the bottom bar

Two specific corrections from the product owner, both about the palette being absent from the
app's own furniture.

**The wordmark in the map header is wrong.** It renders as one flat colour. The logo is
two-tone: *entry* in light blue, *map* in white. The header pill is white, so white-on-white is
not available there and the light-background pairing has to be used instead: *entry* in a blue
dark enough to hold on white, *map* in the dark ink. Both halves must be legible and the
two-tone reading must survive. The onboarding mark already defines this pairing; the header
should use the same one rather than inventing a third.

The rule underneath: the wordmark is always two-tone, and which two tones depends on what it
sits on. On deep aubergine it is light blue and white. On white it is deep blue and dark ink.
It is never one colour.

**The bottom bar is monochrome and should not be.** It is purple on purple. The logo carries
deep blue, light blue, marigold and white, and none of that reaches the one component visible
on nearly every screen. Bring the palette into it.

The constraint is the same one that governs the map ground: on markers those hues carry
meaning, so in the navigation they must read as brand rather than as state. That is achievable
because the bar is persistent chrome and nothing in it represents a place. Keep the active tab
unambiguous, keep every label legible, and do not let the scan button's marigold ring read as
the scanned-on-site tier.
