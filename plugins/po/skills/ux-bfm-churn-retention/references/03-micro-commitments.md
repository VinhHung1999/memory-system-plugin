# Micro-Commitments & Loyalty

## Core Principle
Users who invest effort — time, attention, data, or money — into a product feel psychological ownership over the relationship. This invested effort creates a "switching cost" that is not financial but emotional: leaving means losing what you put in. The key design goal is to create genuine micro-commitments (price tracking, saved preferences, partial progress, small deposits) that make the user's goal feel partially achieved within your product, reducing the incentive to search elsewhere.

This is distinct from dark patterns. The commitment must move the user toward their actual goal — not trap them through friction.

## Diagnostic Questions
- At what point in the journey has the user invested enough effort that switching feels costly?
- Do users who take one small action (save, track, bookmark) return at significantly higher rates than those who don't?
- Is there a "commitment moment" you can create earlier in the journey — before the user is ready to convert?
- Are your loyalty hooks genuinely moving users toward their goal, or are they side quests?

## Design Checklist
- Create a meaningful micro-commitment as early as possible in the journey (track, save, set a goal)
- The commitment must feel like progress toward the user's real goal, not a detour
- Require minimum friction to create the commitment — social login, one tap, no mandatory account creation upfront
- Close the reward loop: when the commitment pays off ("your tracked price dropped"), surface the result prominently and re-engage with the next commitment
- Don't require account creation before showing the value of the commitment

## Anti-Pattern
**What goes wrong:** Product adds a "save" or "wishlist" feature, but the friction to create an account upfront makes users abandon. The micro-commitment mechanic exists but is gatekept behind a signup wall — which inverts the relationship. The user must trust you before seeing any value.
**Why it happens:** Teams optimise for data capture (email acquisition) over retention mechanics. They want the account before giving the benefit.
**BFM Example (Expedia):** To track prices, Expedia requires full account creation first. The user must give email, create a password, and trust that the result will be worthwhile — before experiencing any of the value. Skyscanner asks for even more. Both lose to Hopper's "price freeze" mechanic, which creates an irreversible financial micro-commitment that immediately reduces the incentive to shop elsewhere.

## BFM Evidence

### Flights Ch.2 — the Invested Effort model
> "So by letting Expedia track the prices for you, they can maintain a relationship between you and the purchase. This reduces the incentive to look elsewhere."

The mechanism: INVESTED EFFORT (time, data shared, action taken) → YOUR REWARD (price alert, notification, confirmed saving). The user has skin in the game.

### Flights Ch.2 — gating the commitment breaks the loop
> "Well, this has been flipped upside down. Now you need to create an account, give up your data, and open a channel of communication. While trusting that the end result will actually be worthwhile."

The contrast: without account creation, the user can just check prices again in a few days at zero cost. The "check again" option requires no trust — so it wins.

> "Where no trust is required, and you know exactly how much effort it will take."

### Flights Ch.2 — Hopper's price freeze as the gold standard
> "To freeze your fare price... this represents a smaller commitment, and will drastically reduce the chances they someone looks elsewhere."

> "With some thoughtful UX, you can nudge them to make a small commitment. Something that at least feels like it's moving them towards their true goal."

Hopper's £19 price freeze is a financial micro-commitment attached to a specific flight. It's a real commitment (money spent) that creates real switching cost (sunk cost + goal alignment). It beats "save to watchlist" precisely because it involves loss aversion.

### Flights Ch.2 — commitments must not be side quests
> "In other words, the user wants to book a holiday. This is an optional step, that might not help them."

The warning: price tracking only retains if the user believes it moves them toward booking. A "Save" button that lives in a hidden tab feels like a side quest — it doesn't connect to the main goal.

## What Good Looks Like
A user who has tracked a flight, set a goal, or frozen a price has made a tangible commitment to your product. When the reward arrives ("your flight dropped £30"), the notification re-engages them with proof that the commitment paid off. They are now primed for the next commitment. Each cycle deepens the loyalty relationship.

## Red Flags
- [ ] Micro-commitment (save, track, wishlist) requires account creation before showing value
- [ ] No visible feedback loop when the commitment pays off
- [ ] The commitment feels like a detour from the user's main goal
- [ ] Users who save/track do not return at a meaningfully higher rate (commitment is hollow)
- [ ] Price freeze / deposit option not offered — only free watchlist (no switching cost)
