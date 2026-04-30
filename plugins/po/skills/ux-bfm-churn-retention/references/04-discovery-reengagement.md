# Discovery & Re-engagement

## Core Principle
A returning user who opens the app and finds it unchanged from their last visit has no reason to stay. Static home feeds are invisible churn engines — they train users to expect nothing new, so they stop checking. The re-engagement moment (a notification, an email, a return visit) is only effective if the app delivers something worth discovering. Personalised, dynamic, interest-matched content is the difference between a returning user who converts and one who closes after 3 seconds.

## Diagnostic Questions
- Does the home feed change meaningfully between sessions, or is it identical a week later?
- Are personalisation signals (listening history, past purchases, browsing patterns) actively used to surface new content?
- When a user reaches the end of a content row, what happens? Dead end or continuation?
- Does your analytics track "non-productive refreshes" — sessions where users open, scroll, and close without taking action?

## Design Checklist
- Rotate the order and composition of personalised content rows between sessions
- Surface content the user hasn't seen yet — not just the same "top picks" every visit
- Personalisation signals (e.g., "because you listened to X") should generate dynamic, scrollable feeds — not static 20-item lists with dead ends
- Track non-productive refresh rate as a leading churn indicator (user bored → user churns)
- When a full-page refresh occurs without action, interpret it as a "nothing here for me" signal and adjust the feed

## Anti-Pattern
**What goes wrong:** Personalisation is implemented as static carousels — "Because you liked X" shows 20 items on day 1 and the same 20 items on day 30. The relationship between the user and the product is used as a hook label, but the actual content doesn't change.
**Why it happens:** Personalisation is treated as a one-time matching exercise (user profile → content type) rather than a continuous discovery system. Teams ship the carousel as a feature without building the refresh/continuation logic.
**BFM Example (Audible):** "Because you listened to Never Enough" is not clickable, shows a fixed list, and ends with no option to continue. The row title implies a personalised relationship, but the behaviour is identical to a generic "popular" list. The personalisation is surface-level.

## BFM Evidence

### Audible — static feed is invisible churn
> "The order doesn't change between sessions. (i.e., you can literally use the app a week later and it's identical)."

> "Each row only shows 20 items... and then ends. There's no additional step for discovery."

The dead-end row is the core problem. A user who has already seen all 20 items from "Because you listened to X" finds nothing new — so they close.

### Audible — personalisation signals wasted
> "These are more like a curated display of related items... with a clear relationship to something you've previously spent 8 hours listening to."

> "This isn't clickable."

The setup is correct (8 hours listening = strong signal) but the execution is broken. The personalised header creates an expectation of relevance, then delivers a static, non-extensible list.

### Audible — BFM recommendations for fixing the loop
> "1. Occasionally change the order of the components."
> "2. Surface new items from inside this filter. What hasn't the user seen yet?"
> "3. At the end of these rows, refresh and fetch more. The user is browsing with intent."
> "And this is a cue that they want more of a specific thing."

### Audible — non-productive refresh as diagnostic signal
> "Tracking the frequency of non-productive refreshes can reveal moments where the user feels bored or uninspired."

> "On the other hand, a whole page refresh might indicate that the user found nothing that interests them. i.e., no relationship or filter that shows results they care about."

The prescription: a home screen refresh is not just a UX event — it's data. A user who refreshes and finds the same content is about to churn. A system that detects this and responds with fresh content can interrupt that decision.

### Audible — the opportunity vs. what happens
> "And yet, Audible waste this key opportunity."

BFM's framing: the home feed, and specifically the personalised sections, are high-intent surfaces. Users who come back to a book app are already motivated — the product just needs to not get in the way.

## What Good Looks Like
A returning user opens the app and sees content they haven't seen before, surfaced from signals they've generated (listening history, saves, browsing behaviour). The "Because you listened to X" row contains new titles on each visit. When they reach the end of a row, more loads. A non-productive refresh triggers a subtle reshuffling. The app feels alive.

## Red Flags
- [ ] Home feed is identical on consecutive visits
- [ ] Personalised rows end with no continuation option
- [ ] "Because you liked X" uses the same 20 items for all users who liked X
- [ ] Non-productive refresh rate not tracked in analytics
- [ ] Returning user email/push points to the same home feed, not to new/unseen content
