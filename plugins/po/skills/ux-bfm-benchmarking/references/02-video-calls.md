# Video Call UX Benchmarking

## Core Principle
Video call products (Zoom, Teams, Google Meet, FaceTime, Whereby) converge on the same core tasks — join a call, mute/unmute, share screen, record — but diverge significantly on the micro-interactions that determine whether a meeting runs smoothly or awkwardly. BFM's video call showdown reveals that the products with the best call UX are not necessarily the ones with the most features — they are the ones that handle the highest-frequency, highest-stakes moments (joining, muting, leaving) with the least friction.

## Key Benchmarks

### Joining a Call
The "join" moment is high-stakes: late to a meeting, someone has shared a link, the user is under social pressure to join quickly. The number of steps between link click and "in the call" varies significantly across products.

**BFM observation (The Video Call Showdown):**
Products with the best join experience pre-fill user details (name, camera/mic settings from last session) and surface a single "Join" CTA. Products with the worst join experience require re-authentication, settings configuration, or plugin installation before joining.

**Benchmark standard:** Link → preview screen → join in ≤2 clicks. No plugin installation required for guests.

### Mute/Unmute UX
The mute button is the highest-frequency action in any video call. Its discoverability, reliability, and feedback quality directly affect call quality.

Key failure modes:
- Mute state unclear (user cannot tell at a glance whether they are muted)
- Mute action has a delay (user speaks, then mutes, then realises the last 2 seconds were heard)
- Keyboard shortcut for mute not obvious or inconsistent

**Benchmark standard:** Mute state visible on every screen without moving the mouse. Keyboard shortcut displayed on hover.

### Screen Sharing
Screen sharing is used in most professional calls but the flow to initiate it varies from 1 click to 4 clicks across products.

**Key observation:** Products that require the user to navigate to a menu > select source > confirm > share (4 steps) create awkward pauses in meetings. Products with a persistent "Share" button in the call toolbar (1-2 steps) enable seamless transitions.

### Leaving a Call
The "leave" action is surprisingly variable. Some products offer "Leave" and "End for all" as equally visible options — creating accidental meeting termination. Others require confirmation. The best design: "Leave" is immediately available; "End for all" requires a deliberate secondary action.

## BFM Evidence (The Video Call Showdown)
The showdown compared products across specific task scenarios with identical starting conditions. The output identified clear leaders and laggards for each task type, with particular attention to:

1. **Guest join experience** — how does the product treat someone who receives a link but has no account?
2. **Recovery from technical failure** — what happens when audio drops, camera freezes, or connection is lost?
3. **Meeting management** — muting others, removing participants, waiting room management

The benchmark confirmed that the best-rated products were not necessarily the market leaders — they were the ones that handled failure states gracefully and minimised friction at the highest-frequency actions.

## What Good Looks Like
A video call product where: guests can join in ≤2 clicks without creating an account; mute state is visible at all times without moving the mouse; screen sharing initiates in ≤2 steps from any call screen; and "End for all" requires explicit confirmation rather than being equally accessible to "Leave."

## Red Flags
- [ ] Joining a call as a guest requires plugin installation or account creation
- [ ] Mute state not visible without moving the mouse to the toolbar
- [ ] "End for all" and "Leave" are equally prominent with no confirmation step
- [ ] Screen sharing requires navigation to a menu (vs. persistent toolbar button)
- [ ] No recovery path when audio/video fails mid-call (requires leaving and rejoining)
