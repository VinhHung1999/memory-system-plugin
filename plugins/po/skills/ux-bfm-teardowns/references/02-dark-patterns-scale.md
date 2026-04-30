# Dark Patterns at Scale

## Core Principle
Dark patterns in small products are a footnote. Dark patterns in products used by hundreds of millions of people are a systemic harm. Scale amplifies the impact of every manipulative design choice — a pattern that causes 5% of users to inadvertently opt into data tracking affects 5 million people when the product has 100 million users. BFM teardowns focus on dark patterns in mainstream, trusted products precisely because the harm is not proportional to user naivety — it is proportional to user count.

## Diagnostic Questions
- Does the design make it difficult or impossible to say "no" to a choice that should be binary?
- Is the default option the one that benefits the company, not the user?
- Are UI elements designed to obscure rather than inform the user's decision?
- Is the user being "walked through" a commitment they may not have intended to make?

## Design Checklist
- Every permission, opt-in, or data collection request must have a clearly visible "no" option with equal visual weight to "yes"
- Defaults must be set to the state that is best for the user — not the company
- Removing navigation options (back buttons, close buttons) is never acceptable at a subscription or data-collection step
- "Continue" should never be the only visible action on a screen that is asking for consent

## Anti-Pattern
**What goes wrong:** A product uses a series of low-friction, seemingly reasonable design choices that cumulatively result in users granting permissions, sharing data, or subscribing to plans they did not clearly intend. Each individual choice seems defensible ("we just want to explain the benefit"); the cumulative effect is manipulation.
**BFM Example (Ticketmaster permission prompt):** The permission request for data tracking shows one button: "Continue." The iOS system dialog then appears with "Ask App Not to Track" as the only alternative. A user who wants to say no must navigate two screens and actively hunt for the declination option — the "yes" is automatic; the "no" requires effort.

## BFM Evidence

### Ticketmaster — no "no" button on data tracking
> "What is notable though, is that there's not a button to say no. You have to click on something that says continue."

> "Help us improve your app experience — Sharing your data allows Ticketmaster to personalize the app for you... [CTA: Continue]"

The design: "Continue" is the only button visible. The only way to decline is to navigate to the iOS system-level permission dialog that appears after tapping "Continue." Most users tap Continue, see the iOS dialog, and tap "Allow" — never realising there was a "no" option available.

### Ticketmaster — foot-in-the-door permission stacking
> "It's not unusual to open an app and immediately be shown a pop-up. Nor is it rare for that pop-up to be asking you to share all of your data."

The foot-in-the-door technique: each small permission granted makes the next permission feel more reasonable. First permission: app tracking. Second: notifications. Third: location. Each builds on the compliance established by the previous.

### Substack — removing navigation to prevent abandonment
> "One reason [the screen is so bare] is that they've removed any link to go backwards."

At the email capture step, Substack removes the back navigation. A user who changed their mind cannot exit the subscription flow without closing the app entirely. The elimination of escape routes is a textbook dark pattern — it manufactures completion by removing choice.

### Substack — vague CTA to obscure commitment
> "You might click to subscribe, and think nothing about the next screen. Other than it's quite vague."

> "Take a moment to think about their conundrum. If they were to even mention prices here, some people wouldn't bother subscribing to the free version."

The design deliberately withholds pricing information at the email-capture step. The user commits to entering the subscription flow before understanding what they are committing to. This is not an oversight — BFM frames it as a deliberate product decision.

### Substack — defaulting to maximum subscription commitment
> "...they'll push you into upgrading."

After the subscriber completes a multi-step flow, the subscription plan selection defaults to the highest-value tier (Annual £155/year), not the free plan. The user must actively downgrade to the free option.

## What Good Looks Like
A permission screen with two clearly visible buttons of equal weight: "Allow" and "No Thanks." A subscription flow that shows pricing before asking for an email. A plan selection page that defaults to the free or lowest-cost option. Navigation that is always available so the user can change their mind at any point.

## Red Flags
- [ ] Permission request has only one visible button ("Continue", "Next", "OK") with no "decline" visible
- [ ] Subscription or payment flow has no back/exit navigation
- [ ] Plan selection defaults to the most expensive option
- [ ] Pricing first appears after the user has already entered their email or agreed to something
