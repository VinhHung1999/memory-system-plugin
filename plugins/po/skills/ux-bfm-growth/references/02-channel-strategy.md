# Channel Strategy: Coercion vs. Alignment

## Core Principle
Every platform eventually wants users on its highest-value surface — usually the native app. The question is how to get them there. Coercion (blocking the web experience, modal-bombing, third-party shutdowns) works in the short term and destroys trust in the long term. Alignment (making the app genuinely better, so users choose it) works in the long term and builds the brand in the short term. The worst outcome is coercion that users notice — they feel manipulated, and the product gets the negative press without the conversion.

## Diagnostic Questions
- Is the app experience meaningfully better than web, or just more aggressively promoted?
- How many times does a first-time web visitor see a prompt to switch to the app before they can access content?
- Are you creating value on web to build intent, or degrading web to force migration?
- What happens to a user who consistently refuses the app prompt — do they get a good experience or a degraded one?

## Design Checklist
- Make the app genuinely superior — larger ads, better personalisation, exclusive features — and communicate that clearly once per session
- Limit app install prompts to one per session maximum; multiple prompts in a single visit signals the web experience is being deliberately degraded
- Never gate content behind a modal that requires login/download to dismiss — this is user-hostile and directly causes bounce
- If third-party app access is being restricted, do it because the native experience is now better — not as the primary strategy for forcing migration

## Anti-Pattern
**What goes wrong:** Web experience is systematically degraded (modals, smaller ads, blocked content) to force users to the app. Users learn to resent the brand. Power users who already had the app are unaffected. New users who came from search or a shared link hit a modal wall and bounce, never becoming users at all. App downloads come from existing users, not new acquisition.
**Why it happens:** App install rate is a team metric. The team can improve their metric by degrading web. The cost (new user bounce rate, brand perception) belongs to a different metric owned by a different team.
**BFM Example (Reddit):** Reddit shut down third-party APIs (killing Apollo, the most-loved Reddit client), then systematically degraded the web experience to force app installs: multiple overlapping modals, "Use App" CTAs on every page load, login walls to see content, and ad units twice the size on app vs. web.

## BFM Evidence

### Reddit — the coercion playbook
> "App usage is clearly their goal, even at the cost of a good user experience on the web."

> "'Oh what? You mean that single CTA? You're overreacting.' Three if you already have the app installed."

The progression: (1) "Use App" button at top of page → (2) "See Reddit in..." dialog with Reddit App / Safari options → (3) black notification bar "Reddit — Open in the Reddit app" → (4) Google sign-in modal → (5) "Create an account to join the AskReddit community." A first-time visitor from Google cannot access content without dismissing 3-5 overlapping modals.

> "In other words, if someone sends you a Reddit link, you can't actually see any of the content behind the various modals."

> "Making it essentially impossible for most third party developers to continue, and many much-loved Reddit apps (like Apollo) shut down."

### Reddit — the genuine advantage: ad unit size
> "Ads are often more than twice the size on the iOS app [vs. web]."

The legitimate business case for moving users to app: app ads are more valuable. This is a real economic difference. But Reddit leads with coercion rather than communicating this value difference. Users who would voluntarily switch for a better experience are instead pushed into switching resentfully.

### Threads — channel alignment, not coercion
Threads' approach: don't offer a degraded alternative. The Instagram-login requirement means every user is automatically on the best path. No web experience is being destroyed; the product simply works on mobile and works better with Instagram. Users who want Threads choose to get it properly.

The contrast with Reddit: Reddit had a beloved web and third-party experience, then deliberately degraded it. Threads never created the alternative to degrade — the native app is the product.

## What Good Looks Like
App install prompts that appear once per session, communicate a genuine benefit ("ads on app are full-screen, web ads are small-banner — your choice"), and accept "no" gracefully. A web user who declines the app prompt repeatedly gets a full web experience — slower, smaller ads, but complete. The app grows through genuine preference, not manufactured necessity.

## Red Flags
- [ ] App install prompt appears more than once per session on web
- [ ] Web users cannot access content without dismissing a modal first
- [ ] Third-party access restricted without a meaningfully better native replacement
- [ ] App download metric is owned by a team with no accountability for web experience quality
- [ ] The only advantage of the app is "you won't see these prompts"
