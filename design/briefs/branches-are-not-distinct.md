# The branches, and the control that appears and disappears

The owner, running the published build:

> "i see you also have separate walkthroughs for the different flows, but they dont
> seem that much different and the drop down to switch to another user flow only pops
> up at a certain page number, which is weird."

Both are correct. The second one is my error and I will name it as such.

---

## 1. The branch control appears and disappears, and that is my instruction

The previous brief said, in my words: *"Entry is only from the map with nothing open...
because a branch entered from inside a sheet has nowhere clean to return to."*

The implementer did exactly that: `#wt-more` is hidden unless the current step is on the
map with nothing open. So the control materialises at some step numbers and vanishes at
others, for a reason that lives entirely inside the layer's own bookkeeping.

**That is a technical constraint leaking into the interface.** The return problem is real
-- a branch entered from inside a sheet has to put him back somewhere -- but the fix
belongs in the layer, not in the user's field of view. The layer already remembers the
step it was on and returns to it; it simply needs to also close what is open and get to
the map before it starts the branch, and reverse that on the way back.

**Build it so the control is always there.** Present on every step of the core route, in
one place, in one state. Tapping it from inside a sheet closes the sheet and goes to the
map itself, because that is what the layer would have made him do by hand. If some entry
genuinely cannot be made to work, the control stays visible and says why when pressed --
a control that is present and explains itself beats a control that disappears.

It still must never be the blinking target, and no step in any route may point at it.

---

## 2. The branches are not different enough, and here is why

Read together, the three read as one thing because of how they open and what they spend
their steps on.

**Two of the three open on the same screen with nearly the same line.** Branch A begins
`Your account / Settings, contributions and business.` and Branch C begins
`Your account / The app's own settings live here.` A viewer who has seen one has, as far
as the opening frame goes, seen the other.

**Branch B spends its first three steps on navigation and says nothing.**
`Tap a door / Any place on the map.` then `Open it up / More of the card.` then
`All of it / Everything this card has.` Three steps and three lines before the branch
reaches its own subject.

**Every branch ends on a step called `Back to the map`.** Three endings, one shape.

So roughly half of the branch material is the presenter navigating, narrated. The parts
that are actually distinct are buried in the middle.

### What each branch is actually about

Each one has a thesis it is not currently stating. Open on it, do not build up to it.

**Business.** *This is the one rung a machine cannot produce.* Everything else on this
map came from a photograph. Owner-confirmed came from a person standing at their own
door, and it is the top of the ladder because the next rung would be a compliance claim a
photograph cannot support. What an owner knows that a camera cannot see -- the door's
weight, a buzzer, a side entrance -- is the point of the whole flow.

**Community.** *A correction can never change a verdict.* It marks a place as needing
another look, and it reaches a person rather than a form. Nothing is ever erased; earlier
evidence stays on the receipt. That is the answer to "what if you are wrong about
someone's business", and right now the demo asserts it in the script without ever showing
it.

**Accessibility.** *The product turns its own settings on itself, live.* An accessibility
product that is itself inaccessible is a joke with the audience as the punchline. Turn
text to 200% on screen and let the interface reflow while they watch. Do not narrate it.

### The rule for this pass

**A step that only moves the presenter to the next screen is not a step.** Make it a
silent transition: no callout, no counter increment, the ring on what to tap and nothing
else -- or fold it into the step that follows. Judge each branch by how many of its steps
carry a fact, and say the ratio in your report.

Three distinct openings, three distinct endings. If two branches want the same closing
line, one of them has the wrong closing line.

---

## What does not change

The core route is the spine and the branches stay optional. Runtimes stay in the region
they are now -- roughly 30 to 50 seconds each -- and if cutting the navigation steps makes
a branch shorter, that is a better branch, not a gap to fill.

Claims discipline is absolute and unchanged: no accuracy figure, never "compliant" or
"verified", never that a place is accessible or inaccessible, never that step-free entry
is assessed. The engine reads four criteria.
