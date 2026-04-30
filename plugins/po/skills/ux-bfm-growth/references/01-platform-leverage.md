# Platform & Network Leverage

## Core Principle
The fastest way to grow is not to start from zero. Every product that has an existing user base, data relationship, or partner network is sitting on a growth asset that most teams ignore. Platform leverage means deliberately designing the new product so that existing users are automatically better served — and in being better served, they pull the new product into their social graph. This is structural growth: the product's architecture is the distribution strategy.

## Diagnostic Questions
- Does your product have access to existing user relationships, social graphs, or behavioural data that could personalise the new experience from day one?
- Is account creation with an existing platform faster AND better for the user — not just faster?
- Do users who sign up via platform integration automatically generate a growth event (bringing followers, connecting friends, seeding content)?
- Would a standalone signup (email/password) produce a meaningfully worse experience?

## Design Checklist
- Make platform login the obvious default — not just because it's easier, but because it produces a demonstrably better product experience
- The integration must feed into a growth loop: each platform-connected user should automatically create pull for other users
- Don't offer email/password as an equal-weight alternative if it produces a worse product experience — you are not obligated to degrade the product to appear neutral
- Leverage existing social graph to seed content, connections, and recommendations from day one — not after the user has "built up" their account

## Anti-Pattern
**What goes wrong:** Platform login is added as a convenience feature (one-tap signup) without connecting it to a growth loop. Users sign up faster but the new product is otherwise identical to a standalone experience. The network asset is not activated.
**Why it happens:** Platform integration is owned by the auth team. Growth is owned by a different team. Nobody connects the two.
**BFM Example (Threads vs. standalone):** Threads mandated Instagram login — widely criticised as a limitation. BFM's analysis shows it was a deliberate growth architecture: Instagram-connected accounts enter a viral growth engine (followers, pending follows, imported profile), while email-only accounts would produce worse individual experiences AND contribute nothing to the growth loop.

## BFM Evidence

### Threads — Instagram login as growth architecture, not convenience
> "It's been widely criticised that you need an Instagram account to use Threads. But rather than being a shortcut to releasing the app sooner, I think it's been a fantastic growth strategy."

> "A recent study by oAuth found that 62% of users still prefer to use a username and password when given the choice."

The insight: if Threads had offered email signup, 62% of users would have chosen it — and those users would both have a worse experience AND contribute nothing to the viral growth engine.

> "While Instagram-connected accounts are pushed into their growth engine... these 'email and password' users would both have a worse individual experience, and contribute less to Threads' viral growth."

### Threads — profile import as the growth accelerator
> "Sure, connecting via Instagram makes it easier to technically have an account. (i.e., fewer actions). But more importantly, in a single click... [users import their profile, bio, followers]."

The imported profile is not just a convenience — it's a pre-built identity that makes the user's first post visible to followers who are already primed to engage.

### Threads — pending follows as a growth engine
Threads allows users to follow celebrities who are not yet on Threads. When those celebrities eventually join, all pending followers are notified — creating a re-engagement moment and a distribution event simultaneously. The growth loop operates even before the followed user is active.

### Threads — 3 technical steps to content
> "Sign-up journey: 3 technical steps → Account active → Content serving."

The personalization (which posts to show) is seeded from Instagram data immediately. A new user sees relevant content from minute one — not the empty-state "follow some accounts to get started" experience that kills standalone social apps.

## What Good Looks Like
A new product where the platform-integrated signup produces a measurably better Day 1 experience: pre-filled profile, pre-seeded social graph, pre-personalised content feed. The user who signs up via Instagram sees content and connections from minute one. The hypothetical user who signed up with email would have to spend 30 minutes to reach the same state. Platform login is not just faster — it is better.

## Red Flags
- [ ] Platform login is offered as a convenience feature with no downstream product benefit beyond faster signup
- [ ] Email/password produces an identical product experience to platform login
- [ ] No growth loop is activated by the platform connection (no follower notification, no social graph seeding)
- [ ] Platform data (existing social graph, behaviour) is not used to personalise the Day 1 experience
