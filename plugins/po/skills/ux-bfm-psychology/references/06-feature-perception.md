# Feature Perception

## Core Principle
Features go unnoticed — and unfelt — when they are presented without a personal value context. A feature list tells users what a product can do; a benefit framed against the user's stated goal tells them what it will do for them specifically. The gap between a feature being available and a feature being perceived as valuable is almost entirely a communication problem.

## Diagnostic Questions
- Is each feature introduced in the context of a problem the user said they have, or as a generic item in a list?
- Can the user calculate their approximate personal ROI from this feature before they decide whether to use it?
- After onboarding, will the user naturally discover this feature in the app — or is it hidden behind a menu they may never open?

## Design Checklist
- Reframe every perk or feature to answer "so what does this mean for someone who said they want X?"
- Introduce features in the order that matches the user's stated priority, not in a fixed sequence
- Provide a concrete value anchor before asking the user to evaluate a perk (e.g., show money saved, not just money-back percentage)
- After onboarding, surface features contextually in the moment they are relevant — not only in a setup wizard
- Avoid bombarding users with multiple "new benefits" screens at once; one benefit experienced > five benefits listed

## Anti-Pattern
**What goes wrong:** A premium subscription onboarding flow presents all unlocked perks immediately after payment as a series of cards. The user taps through without engaging because the perks feel generic, administrative, and disconnected from why they subscribed.
**Why it happens:** Teams build a feature-complete onboarding checklist. Each feature gets a card. The order is determined by engineering priority or alphabetical order, not user goal alignment. No one reframes the copy.
**BFM Example:** Monzo Perks — after subscribing, the onboarding asked users to set up custom spending categories as the very first step. The user had no existing transaction data in view, no context about which categories already existed, and no ability to undo duplicate categories. The first impression of a £7/month subscription was an administrative task they could not complete meaningfully.

## BFM Evidence
### Monzo Perks — a single value anchor drives conversion; a perk bundle does not
> "This creates a clear value proposition. Uber can now use this to frame the cost of their membership. But a lot of subscriptions don't have one single feature to lean into like this. Instead, they're more like bundles of smaller features. They don't all solve a single specific problem, but exist as perks."

### Monzo Perks — the badge: no context, no benefit, no image
> "And immediately telling them about their upgraded badge. There's literally no context, no obvious benefit, and you don't even know what it looks like."

### Monzo Perks — goal collected, not applied
> "So how could they do this better? How can you turn an intention into perceived value. Firstly, the order in which features (or perks) are introduced can be massively influential. Secondly, there's been no effort to reframe these benefits to align with the user's goal."

### Monzo Perks — reframing through the user's lens works
> "So Monzo should be specific, and frame their perks in a way that relates to the user's goal. If the user says that they're interested in spending money abroad... then this perk (or feature) should be reframed through that lens. e.g., 'extra cards can be used abroad to protect you'. Oh, that actually sounds quite useful."

### Monzo Perks — too many screens, too little meaning
> "After almost every click the user is bombarded with a new set of unlocked benefits. Some of which spiral into actual administrative tasks that demand concentration. This bias towards action is intended to get you to try as many of the perks as possible. But it may be having an adverse effect."

### Chatbots — features buried in a labyrinthine flow go undiscovered
> "They don't use chatbots as gatekeepers. Instead, they give you clear context about what is happening."

## What Good Looks Like
Uber One — every touchpoint anchors value to the same number: money saved on delivery fees. Before signup it says "Save £14.67 on this order with Uber One." During the order it says "Saving £14.67 with Uber One and promotions." After signup it shows a running total of money saved. There is no ambiguity about personal ROI.

## Red Flags
- [ ] Features are listed in a fixed order that does not match the user's stated goal priority
- [ ] No concrete monetary or time-saving value is shown alongside the feature description
- [ ] The user is asked to complete an administrative task (configure categories, set up a badge) before they have seen the app's main value
- [ ] Features are only visible in a dedicated "Perks" or "Benefits" section, not surfaced contextually in the product
- [ ] Copy describes what the feature is ("custom categories") rather than what it does for this user ("see exactly where your £5,000 annual shopping bill is going")
