# Emotional Design

## Core Principle
Emotion is the mechanism of memory. Users remember how an experience made them feel, and that feeling drives retention, referral, and return. Emotional design is not decoration — it is the deliberate creation of moments that produce a felt response: anticipation, ownership, delight, calm, or pride. The prerequisite is that the emotion is aligned with what the user is actually trying to do at that moment.

## Diagnostic Questions
- What emotion is the user already experiencing at this point in the flow, and does the design reinforce or contradict it?
- Is the celebratory or emotional moment earned — has something real happened that warrants the feeling?
- Does this moment create a memory that will make the user want to return?

## Design Checklist
- Place emotional peaks at natural completion moments, not at arbitrary checkpoints mid-flow
- Build anticipation before a reveal — the moment of scratching, waiting, choosing — so the emotion has a run-up
- Align the emotion with the user's current goal: a user filling in a bank form is not ready to celebrate; a user who just claimed their first investment is
- Intentionally slow the user down at moments that should feel meaningful (breathing exercise, loading animation, settling shoe)
- Follow a high-emotion moment immediately with a tangible reminder — the certificate, the portfolio view, the receipt — to anchor the feeling to a real outcome
- Test whether the user can answer "what am I celebrating?" if they see confetti or a success animation

## Anti-Pattern
**What goes wrong:** A confetti animation fires when the user completes an onboarding step mid-flow. The user is still in task-completion mode — focused on what comes next — so the confetti reads as noise, not delight. The copy underneath the animation is obscured by the celebration. The user doesn't know what they are supposed to feel proud of.
**Why it happens:** Confetti and celebrations are added to onboarding as a UX best-practice checkbox without auditing whether the emotional moment is earned or whether it is timed to the user's actual mental state.
**BFM Example:** Chase — confetti fires during account setup onboarding, before the user has used the product, received value, or done anything worth celebrating. The study title says it directly: "Why Confetti Celebrations Backfire." The emotion is real, but its deployment is misaligned.

## BFM Evidence
### Headspace — intentionally slowing the user creates investment
> "Do you know what happens when you open the Headspace app for the first time? They encourage you to take a long, deep breath. It's unusual to intentionally slow the user down in this way. But their sign-up flow is a masterclass of psychology and timing."

### Headspace — goals create a measure of success before the experience begins
> "There's a psychological advantage to having a clear goal. It's forced you to actually consider a measure of success. Without this, many people would go into the app, and then have to work out what they're trying to achieve."

### Headspace — the breathing exercise before account creation builds emotional investment
> "Which they'll then immediately attempt to leverage, by asking you to do a short breathing exercise. They're going to try and make you reach your goal before you've even used the app."

### Robinhood — the physical act of claiming builds anticipation
> "The physical act of scratching this box builds suspense. And to be clear, this isn't a dark pattern by default. It depends how it's used. As a rough example, this type of showmanship could help to create the illusion of a very personalised offer."

### Robinhood — the certificate closes the emotional loop
> "After claiming your stock, you're presented with a one-off certificate. And there's quite literally no utility behind it. It's not a proof of ownership. Usually in situations like this, you want to 'tie together' both parts of the experience. i.e., 'remember this free stock you received? And how rewarding it felt to become an investor?'"

### Chase — confetti fires at the wrong moment
> "The confetti moment is introduced [mid-onboarding]. Confetti vs. task completion alignment [is missing]. The user's internal question during confetti: 'What am I celebrating?' Confusion creation through misalignment: Backfire mechanism explained."

## What Good Looks Like
Robinhood's stock claim sequence — the specific non-round dollar amount creates anticipation; the curated choice creates ownership; the congratulations certificate creates a landmark; and the portfolio view that immediately follows closes the loop. Even the waiting animation of the stock sliding into place is a micro-moment of anticipation. Every element serves the emotion, and the emotion serves memory.

## Red Flags
- [ ] Confetti or celebration animation fires before the user has received any real value
- [ ] The text explaining what is being celebrated is obscured by the celebration animation
- [ ] The onboarding does not slow down at any point — every screen pushes the user forward at the same pace
- [ ] There is no physical or visual landmark (certificate, first transaction, card activation) to anchor the emotional moment
- [ ] Celebration moments are placed at form-completion steps rather than at value-delivery steps
