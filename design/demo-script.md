# The demo script -- one route, seven chapters

For `design/demo-app.html`. Open it, let the opening screen resolve, and read the
**Say** lines. Tap whatever the ring is around. The route moves on by itself.

**There are no branches any more.** There used to be a 24-step core and three optional
branches, and they overlapped: the Community branch opened by tapping a pin and dragging
the card up, which the core had already spent five steps on, and the Business and
Accessibility branches both opened on the Profile screen with nearly the same line. All
of that material is now folded into one continuous run at the point where the app is
already in the right place. Nothing is shown twice.

**Nothing in this script goes on screen.** The screen carries a two-or-three word title
and one short line. This is what you say over it.

---

## What the pill at the top left does

    <     Chapter name  n/m     >     >>

* `<` and `>` walk the route back and forward.
* The middle says which chapter you are in and where you are inside it.
* `>>` **skips to the start of the next chapter.** It is always there, on every step, on
  every screen, whatever is open. Press it inside a sheet and the ring moves to that
  sheet's close button, then to whatever else it takes to get where the next chapter
  starts -- one tap at a time, with no card and no number, because you are travelling
  rather than presenting. Measured cold from step 1: every one of the six later chapters
  is reachable this way, in three to six taps.

The callout **folds itself** into a small chip in the bottom-left corner a few seconds
after each spoken stop begins -- long enough to read the line once. Hover it, or press and
hold it on a phone, to bring the whole thing back; let go and it folds again. A plain tap
toggles it. The chip always says the step's title.

## Spoken stops and silent transitions

A step that only moves you to the next screen is not a step. Those are **silent**: the
ring is on what to tap, there is no card, no chip, and the number in the pill does not
move. They are marked below. Fifteen of the route's forty steps are silent, and every one
of the twenty-five that is not carries one thing a viewer could not get by looking at the
screen.

**Nothing is rung twice.** Four controls are touched twice over the whole run -- the Key
pill, the card handle, the profile button and *Map* in the nav bar -- and in every one of
those four pairs exactly one of the two is a silent transition. No control and no screen
is spoken over more than once. Measured on the running route, not asserted.

| chapter | spoken stops | silent transitions | measured |
|---|---|---|---|
| 1 Getting in | 2 | 2 | 14.3 s |
| 2 The map | 5 | 3 | 33.6 s |
| 3 One place | 3 | 2 | 20.7 s |
| 4 Corrections | 2 | 3 | 20.6 s |
| 5 The owner | 4 | 2 | 37.6 s |
| 6 Adding a door | 5 | 1 | 42.0 s |
| 7 On itself | 4 | 2 | 34.5 s |
| **whole route** | **25** | **15** | **205.8 s -- 3 min 26 s** |

Measured on the build at 390x844, not estimated; three runs of the finished route measured
203.2, 205.8 and 209.2 seconds, and the per-chapter column is the middle one. The old 24-step core alone
re-measured at 161.5 s on the same harness, and the previous script's figure for the core
plus all three branches was 289.6 s (that total is quoted from the previous round, not
re-measured here). Either way this route is shorter than the old one with its branches
run, and it shows all of the same material without repeating any of it. Under Reduce Motion the same route
measures 202.5 s: the reading allowance is a timer, not a transition, and the
accessibility setting does not shorten it. At the 200% text step, run end to end, it
measures 268.3 s and still finishes. At 320x568 it measures 260.4 s -- see the last note
in "If it goes wrong".

**Do not turn the processing beat into a claim about the product.** The walkthrough's
processing screen runs about 7.9 seconds because it is an animation. A live scan against
production, measured at the size the app actually uploads, takes about **19 seconds** from
shutter to verdict -- the model call is around 8 and the rest is upload, face blur, decode
and the store, on a desk connection rather than a venue's. Say "under half a minute" if
you say anything, and let the screen do the rest.

---

# Chapter 1 -- Getting in

## 1/2 Before you arrive

**Tap:** *Continue as guest*.

**On screen:** "Nothing after this asks you to sign in."

**Say:** "Every place here is a door somebody has to get through, and this tells you what
is at it before you go. Nothing in the next three minutes asks anybody to make an
account."

**Silent:** *Allow location*. Just tap it.

## 2/2 Your needs

**Tap:** the *Wheelchair* card.

**On screen:** "No fit? It dims. It is never hidden."

**Say:** "You say what matters to you, and that changes what we tell you about each place,
not which places you get. A place that does not match your needs recedes in opacity. It is
still on the map, still tappable, still says how we know."

**Silent:** *Continue*.

---

# Chapter 2 -- The map

## 1/5 Every mark named

**Tap:** the *Key* pill.

**On screen:** "Tier is shape and fill, never colour alone."

**Say:** "Every mark the map uses is named in one place, and it stays shut until you ask.
Each tier is a different shape and a different fill, so the map survives greyscale, and
nothing here relies on colour."

**Silent:** *How trust grows* at the bottom of the key.

## 2/5 How trust grows

**Tap:** the **x** on the panel.

**On screen:** "Pins only move up. Nothing is demoted."

**Say:** "Each rung says how we know, not how good the place is. A pin can only ever move
up the ladder. There is no mechanism in the product for taking a place back down."

**Silent:** the *Key* pill again, to shut it. It stays open otherwise, and open it covers
the biggest cluster on the frame.

## 3/5 You are here

**Tap:** the crosshair button on the right.

**On screen:** "Same drawing as the button, so both agree."

**Say:** "That mark is you. It is drawn by the same function that draws the button, so the
two cannot disagree about what the symbol means."

## 4/5 Grouped places

**Press and hold:** any numbered disc. On a laptop, hover it.

**On screen:** "The number counts places, not quality."

**Say:** "A number is places too close to draw apart. Hold it and it says how many and
what mix. The number is a count, never a score -- nothing on this map aggregates into
one."

**Beat:** the preview appears under your finger. Let go when you have said it.

**Silent:** *Filters*.

## 5/5 Never failing

**Tap:** the button at the bottom of the sheet.

**Read off the screen:** the button says how many places are on the map right now. Say
that number rather than one you remember.

**On screen:** "Two public states, and neither is failing."

**Say:** "Filters change which places you see. And there are exactly two public states a
place can be in: scanned on-site, or not yet checked. There is no third state that means
failed, and there is no way to author one."

---

# Chapter 3 -- One place

## 1/3 Tap a door

**Tap:** the pin the ring is around.

**On screen:** "Every hit area is 48px, and none overlap."

**Say:** "The card comes to your thumb, not the top of the screen. And every tap target in
this product is 48 pixels with no two hit circles overlapping at all -- which is stricter
than the guideline asks for, and is the reason close places become a number instead of
crowding."

**Silent:** the handle at the top of the card, to open it up.

## 2/3 The whole card

**Tap:** the handle again.

**On screen:** "Confidence is agreement, not accuracy."

**Say:** "Freshness and confidence, both of them dated. Confidence here is agreement --
how often an independent model reading the same photographs reaches the same answer. It is
not an accuracy figure and we do not publish one, because we have nothing to check it
against."

**Silent:** *See the evidence receipt*.

## 3/3 How we know

**Tap:** the **x** on the receipt.

**On screen:** "Dated sources. Never a rating, never a score."

**Say:** "Dated sources, one after another, and you can always ask a line where it came
from. It is not a rating and it never becomes one."

---

# Chapter 4 -- Corrections

The card is still open at full. Nothing is re-opened.

## 1/2 Something changed

**Scroll the card first.** *Suggest a correction* sits 84 pixels below the bottom of a
390x844 frame -- measured -- so the chip will say **"Further down"** until you scroll. The
step's own line comes back the moment the control is in frame.

**Tap:** *Suggest a correction*.

**On screen:** "A correction can never lower a tier."

**Say:** "Anyone can say something changed. It does not take an account and it does not
take an argument. And whatever the note says, it cannot move this place down the ladder.
There is no path in the product from a report to a demotion."

**Silent:** the note field. Type a sentence -- "the side door has a bell now" is fine. Send
refuses an empty note, so the route waits for you rather than ringing a button that will
bounce.

## 2/2 It reaches a person

**Tap:** *Send suggestion*.

**On screen:** "It marks the place for another look."

**Say:** "That reaches a person. What it does is mark the place as worth another look --
and your note becomes another dated source on the receipt, next to everything that was
already there. Nothing is erased, including by us."

**Beat:** the next screen says the rest in its own words, at length. Let them read it.

**Silent:** *Back to entrance*, then the **x** on the card.

---

# Chapter 5 -- The owner

## 1/4 The top rung

**Tap:** the profile button, top right of the map.

**On screen:** "One rung a photograph can never produce."

**Say:** "Everything you have seen so far came out of a photograph. There is one rung above
it that a machine cannot produce at all, and this is the way in to it."

**Silent:** *My Business*. Scroll to the bottom of Profile; the chip will say **"Further
down"** while you do.

## 2/4 Owner-confirmed

**Tap:** the *Updated today* row.

**On screen:** "The rung above this would be a legal claim."

**Say:** "Owner-confirmed. Attested at the door by a person standing at it, and dated. It
is the top of the ladder and it stops there on purpose -- the next rung up would be a
compliance claim, and you cannot make one of those from a photograph."

## 3/4 What only they know

**Tap:** *Edit entrance*. Scroll down for it -- the three owner actions start 63 pixels
below the fold on a fresh screen.

**On screen:** "Door weight, a buzzer, a side entrance."

**Say:** "This is the part a camera cannot get. How heavy the door actually is. That there
is a buzzer. Which side entrance actually opens. An owner standing at their own door knows
things no photograph contains."

**Silent:** *Review changes*.

## 4/4 Nobody overwrites

**Tap:** *Map* in the bar at the bottom.

**On screen:** "An owner cannot delete a neighbor's scan."

**Say:** "Their change goes out as another dated source, not as an override. The owner
cannot delete a neighbor's scan or a state record -- their update joins the stack. Nobody
gets to erase the record, including the person who owns the building."

---

# Chapter 6 -- Adding a door

**Silent:** *Scan* in the bar at the bottom.

## 1/5 Privacy first

**Tap:** *Allow camera*.

**On screen:** "It runs before the model, and fails closed."

**Say:** "Faces are blurred and location data is stripped, and the screen says so. What it
does not say is where in the pipeline that happens: before anything reads the photograph,
not after. And that path fails closed -- if the blur does not run, nothing goes on."

## 2/5 Frame the door

**Tap:** the shutter.

**On screen:** "One photograph. No form and no checklist."

**Say:** "The shape on screen is a doorway. Put the doorway inside it and take one
photograph. That is the entire instruction -- there is no form and no checklist, because
anything we ask for is something somebody will not do."

## 3/5 It reads the photo

**Tap:** nothing. This one moves on by itself, and there is no ring -- the app's own
progress ring has the screen to itself.

**On screen:** "It reads four things and abstains on the rest."

**Say:** "It is reading the photograph now. It assesses four things: a ramp or bevel,
handrails, door hardware, and accessibility signage. Everything else it declines to
answer. The hard part was never the reading -- it was teaching it to stop."

## 4/5 Before it publishes

**Tap:** *Publish scan*.

**On screen:** "Not visible is an answer we had to teach it."

**Say:** "You see what the photograph supports before anybody else does. 'Not visible' is
a real answer here, and it is the one we spent the most time on."

## 5/5 Published

**Tap:** *Back to the map*.

**On screen:** "Coverage comes from whoever is at the door."

**Say:** "There it is on the map. Anybody at a door can add it, and that is the only place
coverage comes from -- there is no survey team and there is no dataset to buy."

---

# Chapter 7 -- On itself

**Silent:** the profile button. It is rung silently here on purpose: chapter 5 already
spoke over that button, and the two chapters opening on the same screen with nearly the
same line is precisely what was wrong with the old branches.

## 1/4 Its own settings

**Tap:** *Accessibility*, in the Display & access group.

**On screen:** "All three of these change the running app."

**Say:** "An accessibility product that is itself inaccessible is a joke with the audience
as the punchline. There are three settings behind this row and all three of them change the
app you are looking at, live. Nothing here is a preference we store and ignore."

## 2/4 Text size

**Tap:** the **fifth** *A* -- the largest one. Its own label says "Double text size, 200
percent".

**On screen:** "Two hundred percent of default."

**Say:** nothing. Stop talking and let the room watch the interface reflow.

## 3/4 Nothing was cut

**Tap:** the first *A*.

**On screen:** "No clipping, and nothing scrolled sideways."

**Say:** "Nothing was cut off, nothing scrolled sideways, and the walkthrough you are
looking at came with it."

## 4/4 High contrast

**Tap:** the *High contrast* switch.

**On screen:** "It redraws the map, not only the text."

**Say:** "Borders instead of shading, everywhere at once -- and it goes further than the
type. The map ground itself is redrawn: the blocks lose their fills and their footprints
and become outlines, and only the road hierarchy survives, because road widths are
structure rather than decoration."

**Silent:** *Map* in the bar at the bottom. High contrast stays on until you tap it again;
the walkthrough is drawn for it.

**Then:** the walkthrough offers to close itself. The app underneath is untouched.

---

# If it goes wrong

**A tap misses.** Nothing breaks. The layer is drawn over the app, not in front of it, and
every tap you make goes through to the app whether it is on the route or not. The ring
waits where it is. Tap it again.

**The callout is in the way.** It folds itself after a few seconds, and it folds
immediately on the steps where staying open would cover the thing the step is about. If
you want it gone sooner, tap it. If you want it back, tap it again, or hold it.

**You have wandered off.** The chevrons in the pill move the route back and forward. The
ring re-appears the moment its control is back on screen.

**You are short of time.** Press `>>`. It goes to the start of the next chapter from
wherever you are, closing what is open on the way. The chapters worth cutting first are 4
(Corrections) and 7 (On itself); the ones the room usually asks about are 5 (The owner)
and 6 (Adding a door).

**The chip says "Further down".** The control is below the visible screen. Scroll, and the
step's own line comes back as soon as the control is in frame. Three stops need this on a
390x844 frame: *Suggest a correction*, *My Business*, and *Edit entrance*.

**The chip says "Out of view".** That control does not fit on this phone at this text size.
Use the right chevron and carry on.

**The chip says "Just a moment".** The screen it wants has not settled, or the control it
wants is covered -- the app's own toast does this over *Edit entrance* for a couple of
seconds. Wait a beat; use the right chevron if it does not clear.

**Do not run this on a 320x568 frame.** It completes -- measured, 260 s, no stalls -- but
one stop is degraded and it is the app's fault rather than the walkthrough's: on
scan-done, *Back to the map* is drawn at y=511 to 559 and the nav bar occupies y=482 to
568, so the button is entirely underneath it and all five hit samples land on nav bar
buttons instead. The walkthrough correctly refuses to ring a control a thumb cannot
reach and says "Just a moment", so the "coverage comes from whoever is at the door" line
never appears. Say it anyway. At 360x800 and above the button is clear.

**The pin in chapter 3 is not the one you rehearsed.** It picks a well-evidenced pin that
is actually reachable by a thumb on the frame you are running, so it can differ between
phones. Nothing you say in chapters 3 or 4 depends on which place it is.

**The numbered disc does not answer.** Press and hold for about half a second, without
sliding -- a hold that travels is read as the start of a pan. On a laptop, hover it
instead.

**You came back to the tab and it is on the map.** The walkthrough starts on the first step
whose own screen is the one that is up, not at step 1. Verified: with the layer's start
gate held closed while the app was driven to the map, it opened on chapter 2, step 1,
ringing the Key pill.

**Somebody asks "so is this ADA-compliant?"**

> "No, and it never says it is. This says what was visible at a door, when it was seen, and
> who saw it. Compliance is a legal judgement about a building, and you cannot make one from
> a photograph. What we can do is stop people arriving to find out."

**Somebody asks how accurate it is.**

> "We do not publish an accuracy figure, because we have nothing to check it against. What we
> have is agreement -- how often an independent model reading the same photographs reaches the
> same answer -- and every place on the map shows its sources and its dates so you can judge
> the evidence yourself."

**Somebody asks whether it checks for a step at the door.**

> "The interface names step-free entry because that is what people ask us first. The engine
> assesses four things from a photograph today: a ramp or bevel, handrails, door hardware,
> and accessibility signage. Step-free is not one of them yet."

**Do not add "anything else on a card came from a person."** It was in this script and it
was not true. The pilot data seeds eight features per door and the four the engine does not
assess render exactly like the four it does, confidence dots and all -- so a card can show
"Step-free entry" with a confidence beside it and nothing on screen says where it came
from. That is being fixed. Until you have seen it fixed on the build you are holding,
answer with the four and stop there, and if somebody points at a step-free chip on a card,
the honest answer is that it is demo data and it should not be rendering like a finding.

**You want the walkthrough out of the way.** Tap the right chevron until you reach the end,
then the **x**. The app underneath is untouched and stays exactly where you left it.
