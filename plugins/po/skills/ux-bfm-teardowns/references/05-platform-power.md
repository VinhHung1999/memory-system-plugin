# Platform Power vs. User Control

## Core Principle
Platform power is the ability to control the terms on which users access a product — not through the quality of the experience, but through market position, ecosystem lock-in, or the elimination of alternatives. When platform power is used to restrict user choice (shut down third-party apps, degrade web experience, force channel migration), the result is not growth — it is resentment that accumulates until a genuine alternative emerges. Platform power used to improve the experience is legitimate. Platform power used as a substitute for improvement is extractive.

## Diagnostic Questions
- Is the product improving the preferred channel (native app) — or degrading the alternative (web/third-party)?
- Are third-party integrations being restricted because the native experience is now better, or to force migration?
- Would users choose the preferred channel if the alternatives were equally viable?
- Is the company's growth strategy dependent on removing user choice?

## Design Checklist
- If restricting third-party access, the native experience must be demonstrably better before the restriction, not as a consequence of it
- Degrading the web experience to force app installs is not a growth strategy — it is a hostage-taking strategy
- Users who choose a non-preferred surface should receive a complete, functional experience — not a degraded one designed to punish the choice
- Platform power decisions (API policy changes, third-party restrictions) should be communicated with advance notice and a transition period

## Anti-Pattern
**What goes wrong:** Platform restricts third-party API access, eliminating a beloved third-party app experience. Platform simultaneously degrades its own web experience with multiple overlapping install prompts. Users who want to use the product on web face 3-5 modal dismissals to access content. New users who arrive from search hit the modal wall and bounce — never becoming users at all. Power users who already have the app are unaffected. The app install metric looks like a success.
**Why it happens:** App install rate is a team metric. Restricting alternatives improves the metric. The cost (new user bounce, brand damage, creator exodus) belongs to metrics owned by different teams.
**BFM Example (Reddit):** Shut down Apollo (considered one of the best Reddit apps ever made). Then deployed overlapping modal walls on web: "Use App" CTA → "See Reddit in..." dialog → black notification bar → login/account modals. A user who follows a Reddit link from Google cannot read the content without dismissing multiple modals. The result: power users got the app; new users bounced.

## BFM Evidence

### Reddit — the API shutdown as platform power
> "Making it essentially impossible for most third party developers to continue, and many much-loved Reddit apps (like Apollo) shut down."
> "TechCrunch called it 'the only Reddit app you need'." [referring to Apollo]

The third-party apps were not shut down because Reddit's native app was better. They were shut down because Reddit wanted to capture the ad revenue and data they were generating. The quality argument came after the decision, not before.

### Reddit — degrading web to force app migration
> "App usage is clearly their goal, even at the cost of a good user experience on the web."

> "If someone sends you a Reddit link, you can't actually see any of the content behind the various modals."

The web experience has been deliberately made worse. This is not a by-product — it is the strategy. Modal walls are not accidental; they are designed to impose a cost on web use that does not exist in the app.

### Reddit — modal stacking as coercion
The progression documented by BFM:
1. "Use App" button at top of page
2. "See Reddit in..." dialog (Reddit App / Safari)
3. Black notification bar: "Reddit — Open in the Reddit app"
4. Google sign-in modal
5. "Create an account to join the AskReddit community" with "Open Reddit App" button

Five sequential barriers to content access. Each is dismissible. The cumulative effect is that most users give up before reaching content — which is the intended outcome.

### Reddit — the genuine business case that went wrong
> "Ads are often more than twice the size on the iOS app [vs. web]."

There is a legitimate business reason to move users to the app: better ad economics. But Reddit chose coercion over enticement. A user who downloads the app because they're forced to will use it resentfully. A user who downloads it because it's genuinely better will stay.

### Threads — the ethical alternative
Threads also restricted a surface (no web-only signup) — but did so by designing the product to only work properly via the preferred path (Instagram login → mobile app). There was no degraded web alternative to punish; there was simply no alternative at all. The restriction was architectural, not punitive.

## What Good Looks Like
Platform power decisions that improve rather than restrict: "We're improving our native app to the point where we're comfortable restricting third-party API access — and we'll give developers 12 months to migrate." A web experience that is complete and functional, with one clear (non-modal) recommendation to try the app. Growth through genuine preference, not manufactured necessity.

## Red Flags
- [ ] Third-party API access restricted without advance notice and a meaningfully better native alternative already in place
- [ ] Web experience has more friction than app experience on the same task
- [ ] App install metric is a team KPI with no corresponding web experience quality metric
- [ ] Modal walls on web require dismissal before content is accessible
- [ ] User who repeatedly declines app install sees a progressively degraded experience
