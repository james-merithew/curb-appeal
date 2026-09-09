# The demo script — twenty-four steps, spoken, plus three optional branches

For `design/demo-app.html`. Open it, let the opening screen resolve, and read the
**Say** lines. Tap whatever the violet ring is around. The route moves on by itself.

**Nothing in this script goes on screen.** The screen carries a two-or-three word title
and one short line. This is what you say over it.

The callout **folds itself** into a small chip in the bottom-left corner a few seconds
after each step begins — long enough to read the line once. Hover it, or press and hold
it on a phone, to bring the whole thing back; let go and it folds again. A plain tap
toggles it. The chip always says the step's title, so a glance is enough.

| | steps | spoken words | speech at 150 wpm | measured runtime |
|---|---|---|---|---|
| **Core route** | 24 | 404 | 161.6 s | **158.8 s** |
| **Branch A — Business** | 6 | 96 | 38.4 s | **49.5 s** |
| **Branch B — Community** | 8 | 99 | 39.6 s | **49.6 s** |
| **Branch C — Accessibility** | 6 | 66 | 26.4 s | **31.7 s** |
| **Core plus all three** | 44 | 665 | 266 s | **289.6 s — 4 min 50 s** |

Words counted, not estimated. Runtimes measured on the build at 390x844, not estimated.

The owner lifted the two-minute cap, and the extra time went into **more steps, not
longer lines** — every on-screen line renders on one line at the default text size on a
390px frame, measured on all twenty-four.

The measured runtime is the layer's own pace: each step's reading dwell plus a nine-tenths
of a second beat before the tap, plus the app's own transitions. Your pace will differ.
If a step runs long, stop talking and tap.

**Do not turn the processing beat into a claim about the product.** The walkthrough's
processing screen runs about 7.9 seconds because it is an animation. A live scan against
production, measured at the size the app actually uploads, takes about **19 seconds** from
shutter to verdict — the model call is around 8 and the rest is upload, face blur, decode
and the store, on a desk connection rather than a venue's. If a colleague scans a real
door while you are on stage, they will wait roughly twice as long as the walkthrough does.
Say "under half a minute" if you say anything, and let the screen do the rest.

---

# The core route

## 1 — Before you arrive

**Tap:** *Continue as guest*.

**Say:** "Every place here is a door somebody has to get through. This tells you what is at
it before you go."

---

## 2 — Where you are

**Tap:** *Allow location*.

**Say:** "It centres on where you are, so the first thing you see is the block you are
standing on."

---

## 3 — Your needs

**Tap:** the *Wheelchair* card.

**Say:** "You say what matters to you. One tap, and it is optional."

---

## 4 — Not a filter

**Tap:** *Continue*.

**Say:** "That changes what we tell you about each place, not which places you get. Nothing
disappears because of who you are."

---

## 5 — The map key

**Tap:** the *Key* pill on the map.

**Say:** "Every mark the map uses is named in one place, and it stays shut until you ask."

**Beat:** the key opens in place. Let it land.

---

## 6 — Three tiers

**Tap:** *How trust grows* at the bottom of the key.

**Say:** "Three tiers. Estimated, scanned on-site, owner-confirmed. Each is a different
shape and fill, so colour never carries it alone."

---

## 7 — How trust grows

**Tap:** the **×** on the panel.

**Say:** "Each rung says how we know, not how good the place is. Pins only ever move up."

---

## 8 — Shut it again

**Tap:** the *Key* pill.

**Say:** "And it goes away. It is a control, not furniture."

---

## 9 — You are here

**Tap:** the crosshair button on the right.

**Say:** "That mark is you. Same drawing as the button, so the two cannot disagree."

---

## 10 — Grouped places

**Press and hold:** any numbered disc on the map. On a laptop, hover it.

**Say:** "A number is places too close to draw apart. Hold it and it says how many, and what
mix."

**Beat:** the preview appears under your finger. Let go when you have said it.

---

## 11 — Tap a door

**Tap:** the pin the ring is around.

**Say:** "Tap a door and the card comes to your thumb, not the top of the screen."

---

## 12 — At a glance

**Tap:** the handle at the top of the card.

**Say:** "Name, entrance, tier and match. That is the peek, and for most people it is
enough."

---

## 13 — The whole card

**Tap:** the handle again.

**Say:** "Freshness and confidence, both of them dated. Nothing here is a score."

---

## 14 — How we know

**Tap:** *See the evidence receipt*.

**Say:** "Every line on this card carries where it came from. You can always ask it."

---

## 15 — The receipt

**Tap:** the **×** on the receipt.

**Say:** "Dated sources, one after another. It is not a rating and it never becomes one."

---

## 16 — No account

**Tap:** the **×** on the card.

**Say:** "None of that needed a login. A guest sees the same map a signed-in user does."

---

## 17 — Filters

**Tap:** *Filters*.

**Say:** "Filters change which places you see."

---

## 18 — Never failing

**Tap:** the button at the bottom of the sheet.

**Read off the screen:** the button says how many places are on the map right now. Say
that number rather than one you remember.

**Say:** "Nothing here is ever marked as failing. A place is scanned on-site, or it is not
yet checked."

---

## 19 — Add a door

**Tap:** *Scan* in the bar at the bottom.

**Say:** "Scan is the same product carrying on. Anybody at a door can add it, and that is
where coverage comes from."

---

## 20 — Privacy first

**Tap:** *Allow camera*.

**Say:** "Faces are blurred and location data is stripped on the way up. You never have to
do a privacy step."

---

## 21 — Frame the door

**Tap:** the shutter.

**Say:** "The shape on screen is a doorway. Put the doorway inside it and take one
photograph. That is the whole instruction."

---

## 22 — It reads the photo

**Tap:** nothing. This one moves on by itself.

**Say:** "It is reading the photograph now and naming what it can see. The hard part was
never the reading. It was teaching it when to say nothing."

**Beat:** this is the long one, and there is no ring on it — the app's own progress ring
has the screen to itself. If you land early, say nothing until the review screen appears.

---

## 23 — Before it publishes

**Tap:** *Publish scan*.

**Say:** "You see what the photograph supports before anybody else does."

---

## 24 — Two public states

**Tap:** *Back to the map*.

**Say:** "There it is. Two public states, and only two: scanned on-site, or not yet
checked. Both of them say how we know."

**Beat:** you land back on the map and the walkthrough offers to close itself.

---

# The three branches

They are **optional and they are not the spine.** Run the core; branch if the room asks or
if you have the time.

**How to start one:** on the map, with nothing open, a fourth control appears in the
walkthrough's pill at the top left — a **+** next to the chevrons. Tap it and pick a
branch. It is only there on the map, it is never the thing that blinks, and the route
comes back to exactly the step you left when the branch ends.

Two of the three begin by scrolling to the bottom of the Profile screen. The walkthrough
says **"Further down"** while you do it and puts the step's own line back the moment the
control is on screen. That is expected, not a fault.

---

## Branch A — Business (6 steps, 33 s)

The one place in the demo where an Owner-confirmed entrance exists, because the only
owner-confirmed place in the pilot data groups into a numbered disc at phone sizes and the
core route can never open it.

### A1 — Your account
**Tap:** the profile button, top right of the map.
**Say:** "Everything else lives behind here. Settings, what you have contributed, and your
business if you have one."

### A2 — My business
**Tap:** *My Business* — scroll to the bottom of Profile.
**Say:** "This is the same door from the other side: the owner's side."

### A3 — Owner-confirmed
**Tap:** the *Updated today* row.
**Say:** "Owner-confirmed. Attested at the door and dated, which is the top rung and the
only one a person has to stand somewhere to earn."

### A4 — What only they know
**Tap:** *Edit entrance* — scroll down for it.
**Say:** "An owner knows things a photograph cannot see. Door weight, a buzzer, which side
entrance actually opens."

### A5 — Reviewed as well
**Tap:** *Review changes*.
**Say:** "Their change goes out as another dated source, not as an override. Nobody gets
to erase the record, including them."

### A6 — Back to the map
**Tap:** *Map* in the bar at the bottom.
**Say:** "Same door, both sides of it."

---

## Branch B — Community (8 steps, 42 s)

The answer to "what if you are wrong about someone's business". Until now the demo has
only asserted this. Here it shows it.

### B1 — Tap a door
**Tap:** the pin the ring is around.
**Say:** "Any place on the map."

### B2 — Open it up
**Tap:** the card handle.
**Say:** "More of the card."

### B3 — All of it
**Tap:** the handle again.
**Say:** "And the rest of it, including what to do if it is wrong."

### B4 — Something changed
**Tap:** *Suggest a correction*.
**Say:** "Anyone can say something changed. It does not take an account and it does not
take an argument."

### B5 — In your words
**Type:** a sentence. Anything — "the side door has a bell now" is fine.
**Say:** "In your own words, not a form with a right answer."

### B6 — It reaches a person
**Tap:** *Send suggestion*.
**Say:** "That reaches a person. A correction never changes a verdict on its own — it
marks the place as worth another look."

### B7 — Nothing is erased
**Tap:** *Back to entrance*.
**Say:** "And nothing is erased. Your note becomes another dated source on the receipt,
next to everything that was already there."

### B8 — Back to the map
**Tap:** the **×** on the card.
**Say:** "The card is where you left it."

---

## Branch C — Accessibility (6 steps, 31 s)

An accessibility product demonstrating that it is itself accessible. Do not narrate the
reflow. Let them watch it.

### C1 — Your account
**Tap:** the profile button.
**Say:** "The app's own settings."

### C2 — Accessibility
**Tap:** *Display & accessibility*.
**Say:** "Three settings, and all three of them are live. Nothing here is a preference we
store and ignore."

### C3 — Text size
**Tap:** the third **A**.
**Say:** "Turn it up."

**Beat:** stop talking. Let the room watch the screen reflow.

### C4 — Nothing was cut
**Tap:** the first **A**.
**Say:** "Nothing was cut off, nothing scrolled sideways, and the walkthrough you are
looking at came with it."

### C5 — High contrast
**Tap:** the *High contrast* switch.
**Say:** "Borders instead of shading, everywhere at once."

**Note:** high contrast stays on until you tap it again. If you are going back to the core
route, that is fine — the walkthrough is drawn for it too.

### C6 — Back to the map
**Tap:** *Map* in the bar at the bottom.
**Say:** "Settings stay on this device. Signing in syncs them; not signing in does not
cost you them."

---

# If it goes wrong

**A tap misses.** Nothing breaks. The layer is drawn over the app, not in front of it, and
every tap you make goes through to the app whether it is on the route or not. The ring
waits where it is. Tap it again.

**The callout is in the way.** It folds itself after a few seconds, and it folds
immediately on the steps where staying open would cover the thing the step is about. If
you want it gone sooner, tap it. If you want it back, tap it again, or hold it.

**You have wandered off.** The chevrons in the pill at the top left move the route back and
forward. The ring re-appears the moment its control is back on screen.

**The chip says "Further down".** The control is below the visible screen. Scroll, and the
step's own line comes back as soon as the control is in frame.

**The chip says "Out of view".** That control does not fit on this phone at this text size.
Use the right chevron and carry on.

**The chip says "Just a moment".** The screen it wants has not settled, or the control it
wants is covered. Wait a beat; use the right chevron if it does not clear.

**The pin at step 11 is not the one you rehearsed.** It picks a well-evidenced pin that is
actually reachable by a thumb on the frame you are running, so it can differ between
phones. Nothing you say at steps 11 to 16 depends on which place it is.

**The numbered disc at step 10 does not answer.** Press and hold for about half a second,
without sliding — a hold that travels is read as the start of a pan. On a laptop, hover it
instead.

**Somebody asks "so is this ADA-compliant?"**

> "No, and it never says it is. This says what was visible at a door, when it was seen, and
> who saw it. Compliance is a legal judgement about a building, and you cannot make one from
> a photograph. What we can do is stop people arriving to find out."

**Somebody asks how accurate it is.**

> "We do not publish an accuracy figure, because we have nothing to check it against. What we
> have is agreement — how often an independent model reading the same photographs reaches the
> same answer — and every place on the map shows its sources and its dates so you can judge
> the evidence yourself."

**Somebody asks whether it checks for a step at the door.**

> "The interface names step-free entry because that is what people ask us first. The engine
> assesses four things from a photograph today: a ramp or bevel, handrails, door hardware,
> and accessibility signage. Step-free is not one of them yet."

**Do not add "anything else on a card came from a person."** It was in this script and it
was not true. The pilot data seeds eight features per door and the four the engine does not
assess render exactly like the four it does, confidence dots and all — so a card can show
"Step-free entry" with a confidence beside it and nothing on screen says where it came
from. That is being fixed. Until you have seen it fixed on the build you are holding,
answer with the four and stop there, and if somebody points at a step-free chip on a card,
the honest answer is that it is demo data and it should not be rendering like a finding.

**You want the walkthrough out of the way.** Tap the right chevron until you reach the end,
then the **✕**. The app underneath is untouched and stays exactly where you left it.
