# The map's ground: blue trees, and an overview that clumps

The owner, on the live build:

> "why aren't the trees on the map? coloring seems better but its missing the trees.
> wh is congress have a blue wavy lines around it?"
> "actually a few streets have blue wavy lines around them"
> "and zooming out view looks weird like a bunch of bento boxes with random cloud photos"

Three observations, two causes, both found in the source and both verifiable before you
change anything. Verify them rather than trusting this brief.

---

## 1. The trees are there. They are blue, so they do not read as trees.

`groundSVG()` emits the canopy as circles filled with `gc('place')`, which resolves to
`--g-place` -> `--sky400` `#76BCFD`, at `G_A.place = .34`. Parks get an 8px grid of `r=5.6`
discs; treed streets get a band down each side, `r=4.6` every 7.5px, keyed off `TREED_V`
and its horizontal twin.

So along Congress and the other treed streets the canopy is a row of overlapping pale blue
discs, which at that size reads as **a wavy blue line**, not as trees. The owner asked
both "why are the trees missing" and "why does Congress have blue wavy lines" about the
same marks.

**Where the colour came from.** Round 7 adopted the handoff map-kit literally -- the kit's
places layer is `#76BCFD` at `.34` and the token's own comment in this file reads
`-> the tree canopy`. The same round removed green outright: *"there is no yellow and no
green anywhere in the kit or on the board."* The canopy kept its geometry and lost the one
cue that made it legible as vegetation.

### The rule this breaks, which nobody has scored

`--sky400` is the **Estimated tier's** colour. `visual-language.md` section 11 sets the
ground rule as *saturation, not hue*, and states that no ground element uses a semantic hue
at full strength, carries a marker's shape, or sits inside a marker's halo. The canopy is
ground furniture painted in a tier colour, in a marker-like shape.

The build already works around the consequence and the workaround is the tell: a canopy
lobe landing within **26px** of a full pin is dropped before it is emitted, so trees never
sit inside a marker's halo. That rule exists because the canopy and the pins are competing,
and they are competing because they are the same hue.

### The decision is made. The owner chose it; do not re-open it.

I put two options to him -- the canopy as lavender texture, or a muted green as a **ground
token** -- and he answered: *"gound token i think."*

**So a green enters the palette as a GROUND token and nothing else.** It is not a semantic
colour, it never means a state, it never appears on a pin, a chip, a sheet or any UI
surface, and it takes a `--g-` name like every other ground value. This reverses Round 7's
"no green anywhere", so say so plainly in the source with the owner's decision cited --
a later reader will find that Round 7 line and needs to know it was overruled on purpose.

Green as ground is defensible on the canon's own terms: section 11 sets the ground rule as
saturation, not hue, no ground tone exceeds chroma 43, and the least saturated marker is
95. Pick a green that sits inside that envelope. A green that competes with a marker is
the wrong green, and the way you will know is the measurement below, not taste.

Whichever you choose: **measure the canopy against all three pin tiers, the cluster disc
and the match halos**, and report whether the 26px drop rule can become unnecessary rather
than load-bearing. A ground that no longer competes should not need to be cut away from
the markers.

---

## 2. The canopy does not scale with zoom. That is the "cloud photos".

Roads scale: `widths[st.cls]*wk`, where `wk` comes from `streetsFor(box)`. The canopy does
not -- **`wk` appears zero times in the canopy layer.** The radii are literals, `5.6` and
`4.6`, and the grid steps are literals, `8` and `7.5`.

So zooming out shrinks the streets, the blocks and the spacing between them while every
tree stays exactly the same number of pixels across. At the overview stop the discs are
proportionally enormous relative to everything else, they overrun the blocks they belong
to, and adjacent discs merge into blobs. That is the "random cloud photos", and the flat
lavender blocks left underneath them are the "bento boxes".

The fix is not only multiplying the radius. At a wide enough view, individual street trees
are not a thing a map should draw at all -- real maps drop them and keep park fill. Decide
what the canopy becomes at each scale, state the thresholds, and say what you drop and
when. **Density is handled by dropping detail, never by drawing the same detail smaller
until it turns to noise.**

Check the same question for everything else the ground emits: the land dot pattern
(`--g-paper` at `.045` on an 18px grid), the building outlines, the block edges. Anything
with a literal size instead of one derived from `wk` has this bug and has it silently.
Print a table of every ground element, its size expression, and whether it scales.

---

## 3. What "bento boxes" is asking for

At the overview stop the ground is flat lavender rectangles with 1px edges and nothing
else once the canopy is fixed. The kit is silent on zoom -- it ships one artboard -- so
this is genuinely unspecified and the file is allowed to decide, as long as it decides
deliberately and records it.

The useful question is what a person is looking for at that scale. It is not individual
buildings; it is *where the doors are and how they cluster*. So the ground at overview
should recede and let the marks carry the frame. If the blocks are the loudest thing on
screen at that stop, the ground is winning an argument it should not be in.

---

## Constraints

- The map layout at both named stops (k = 1.0 and 2.2) is currently **byte-equal to Round
  14**, ground SVG included, and Round 15 verified that. If you change the ground you break
  that equality deliberately -- re-measure and re-record it rather than letting it lapse.
- Pin contrast against whatever ground you choose stays at **3:1 or better**, re-measured
  rather than assumed, in both contrast modes. Round 8's Estimated mark floors at 3.08:1
  against the current ground and that is the number to beat.
- High contrast **simplifies** the ground rather than enriching it; `--g-place` is already
  `#FFFFFF` there and the canopy is skipped entirely (`if(!hc)`).
- `GROUND_CACHE` keys on `[W,H,pad,box,hc]`. If scale becomes an input to the drawing, it
  must be part of that key or the first view drawn wins for every other view.
- Zero non-ASCII bytes. Do not touch the honesty rules, the trust ladder, tier encoding,
  6.6, or Round 14's zoom, shutter and touch-action work.

## How to work

Measure, do not assert. Print the numbers for everything you change, screenshot the
overview stop before and after, and re-measure rather than assuming the fix worked. Rescore
any criterion you touch, in place, with evidence, and append a round entry to the log. Say
plainly what you did not do.
