# Worked Examples

Three fully-worked stories covering the most common request shapes. Use these
as pattern-match references when you're unsure how to phrase AC, what counts
as "specific enough", or how to split a vague request into concrete scope.

---

## Example 1: Typical feature request (clear domain, moderate clarification needed)

### Original user request
> "Add a way for customers to save their cart so they can come back later."

### Clarification rounds

**Round 1 (PO asks 3 questions):**
- Who: registered users only, or also guests?
- Persistence window: 24h, 7 days, forever?
- Success metric: recovered cart rate (%) or revenue from saved carts?

**User replies:** "Registered only. 30 days. Track recovered cart rate — if it
beats 5% we keep the feature."

**Round 2 (PO covers edge cases):**
- What happens if a product in the saved cart is out of stock when user returns?
- What happens if price changed?
- Should saved cart sync across devices?

**User replies:** "Show out-of-stock items greyed out with a 'notify me' link.
Show old vs new price with a prompt to confirm. Yes, sync across devices for
the same account."

**PO echoes understanding, user confirms.**

### Final story

```
---
story_id: save-cart-for-later
epic: cart-recovery
priority: P1
estimate_hint: M
---

## User Story

**As a** registered shopper browsing on any device
**I want** my cart contents to persist for 30 days and sync across devices
**So that** I can resume checkout later without re-selecting items (target:
5%+ recovered cart rate = ~$40k/month incremental revenue per our baseline
abandonment data)

## Context

Current abandonment rate is 68% (industry avg 70%). ~15% of abandoners cite
"not ready to buy now" in exit surveys. This story targets that segment.
Related epic: cart-recovery. Depends on existing auth + cart services.

## Acceptance Criteria (Gherkin)

**Scenario 1: Registered user adds items and returns next day**
- Given I am signed in on device A
- And I have 3 items in my cart
- When I close the tab without checking out
- And I sign in on device B 24 hours later
- Then my cart shows the same 3 items in the same order

**Scenario 2: Saved item is out of stock when user returns**
- Given I have a saved cart containing product X
- And product X is out of stock when I return
- When I view my saved cart
- Then product X is shown greyed out with a "Notify me when back in stock"
  link and is excluded from the cart subtotal

**Scenario 3: Price has changed since item was saved**
- Given I saved product Y at $29.99 five days ago
- And product Y is now $34.99
- When I view my saved cart
- Then product Y shows "Was $29.99, now $34.99" with a "Use new price" /
  "Remove from cart" prompt before I can check out

## Out of scope
- Guest-cart persistence (separate story — needs cookie/device-fingerprint decision)
- Email reminders to return to saved cart (next sprint)
- Cart sharing between accounts (not in roadmap)

## Open questions for TL
- Current cart service stores in Redis with 24h TTL — does extending to 30d
  require a DB migration, or a new persistence tier?
- Cross-device sync: event-driven via existing user-events bus, or polling?

## INVEST self-check
- [x] Independent — depends only on existing services
- [x] Negotiable — TL may propose different persistence approach
- [x] Valuable — 5% recovered cart target ties directly to revenue
- [x] Estimable — domain is well-understood
- [x] Small — fits in one sprint (M = 2-3 days)
- [x] Testable — every AC has observable outcome
```

---

## Example 2: Very vague performance request (heavy escalation to hypotheses)

### Original user request
> "The app is slow. Make it faster."

### Clarification rounds

**Round 1 (PO probes):**
- Which part of the app feels slow — specific screen or overall?
- On what devices / network conditions — 5G, WiFi, 3G?
- Compared to what — a competitor, or what it used to be?

**User replies:** "Just... everything feels sluggish."

**Round 2 — user is vague on same dimension → escalate to hypotheses:**

> "Let me propose three concrete 'slow's. Pick the one that matches your pain
> (or tell me if I'm missing it):
>
> **(A) Cold start** — time from tap-app-icon to first interactive screen.
> Current ~4.5s on mid-tier Android. Target <2s.
>
> **(B) Screen transitions** — lag when navigating between tabs. Currently
> noticeable jank (below 60fps). Target: consistent 60fps on iPhone 12+.
>
> **(C) Search results** — typing in search bar feels laggy and results take
> >3s to appear. Target: results in <500ms p95.
>
> Which matches what you mean?"

**User replies:** "Option C — search is the worst. I can literally type faster
than results show up."

**Round 3 (PO narrows):**
- Should results update on every keystroke (debounced) or only on submit?
- What's the acceptable time-to-first-result on 4G?
- What should happen when there are zero results?

**User replies:** "Debounced on keystroke, 300ms debounce sounds right. <500ms
on 4G. Zero results → show 'Did you mean...' suggestions + top 3 trending
searches."

**PO echoes, user confirms.**

### Final story

```
---
story_id: search-results-p95-under-500ms
epic: search-performance
priority: P0
estimate_hint: L
---

## User Story

**As a** user searching within the app on 4G or better
**I want** search results to appear within 500ms (p95) after a 300ms debounce
**So that** I don't abandon the search mid-query (current abandonment at
search = 42%, target reduction to <25%)

## Context

Survey + analytics show search is the most common entry point to product
discovery but has a 42% abandonment rate. Current p95 time-to-first-result is
~3.1s on 4G. This story is the first of three in the search-performance epic.

## Acceptance Criteria (Gherkin)

**Scenario 1: User types a query on a 4G connection**
- Given I am on the search screen with 4G connection simulated (1.5Mbps down, 100ms RTT)
- When I type "red sneakers" and pause for 300ms
- Then search results appear within 500ms of the pause
- And the result list shows at least the top 10 matches

**Scenario 2: User types a query that returns zero results**
- Given I am on the search screen
- When I type "asdfqwerty" and pause for 300ms
- Then a "Did you mean..." block appears within 500ms with up to 3
  suggestions based on fuzzy match
- And below it, a "Trending searches" block shows the top 3 platform-wide
  searches of the last 24h

**Scenario 3: User types quickly and keeps typing**
- Given I am typing a query
- When I type additional characters within 300ms of the last keystroke
- Then no search request is issued until I pause for 300ms
- And only the latest query (not intermediate ones) is issued

## Out of scope
- Voice search (separate story)
- Autocomplete suggestions as I type (before 300ms) — separate story
- Search relevance improvements (follow-up epic)

## Open questions for TL
- Current search backend is ElasticSearch behind an API gateway — is the p95
  bottleneck in ES query time or in the gateway/network?
- Client-side: can we cache the last 5 queries locally to avoid re-fetching
  when the user backtracks?

## INVEST self-check
- [x] Independent — can ship without waiting on other search work
- [x] Negotiable — TL may propose server-side debouncing or edge caching
- [x] Valuable — 42% abandonment tied to revenue
- [x] Estimable — perf work is well-understood; TL will size after profiling
- [x] Small — target L (3-5 days); if profiling reveals architecture changes,
  split before starting
- [x] Testable — every AC has measurable latency number
```

---

## Example 3: Clear request with hidden edge cases (auth/permissions domain)

### Original user request
> "Add an 'Invite teammate' button to the workspace settings. They get an
> email, click it, join the workspace."

Seems clear at first glance. But auth/permissions always has landmines.

### Clarification rounds

**Round 1 (PO pushes on edge cases immediately since domain has known traps):**
- Who can invite — workspace owner only, or any member?
- What role does the invitee get by default?
- Does the invite link expire? After how long?

**User replies:** "Owner + admin can invite. Default role = member (read/write
on docs, no admin). Links expire after 7 days."

**Round 2 (PO keeps pressing edge cases):**
- Can the same email be invited twice (e.g. invite expires, re-invite)?
- What if the invitee already has a MoMo account?
- What if the invitee's email domain is on a block-list (competitor / banned)?
- What if a member is invited to a workspace they're already in?

**User replies:** "Re-invite OK — new link invalidates old one. If they have
an account, clicking link should auto-join workspace (no signup). Block-list
not in MVP. If already a member, show 'already a member' toast and no-op."

**Round 3 (PO checks revocation and auditing):**
- Can inviter revoke a pending invite?
- Should there be an audit log entry when someone joins via invite?

**User replies:** "Yes, cancelable before it's used. Audit log: yes, include
inviter + invitee + timestamp + workspace."

**PO echoes. User confirms.**

### Final story

```
---
story_id: workspace-invite-teammate
epic: team-collaboration
priority: P1
estimate_hint: L
---

## User Story

**As a** workspace owner or admin
**I want** to invite a teammate to the workspace by email
**So that** I can grow my team without routing through support (currently
~40 support tickets/week for manual invites, target: <5/week)

## Context

Workspaces today are single-user only. Team use case is the #1 feature
request in customer feedback (172 mentions in last 90 days). This story
delivers the invite flow; follow-ups handle role management and team
billing.

## Acceptance Criteria (Gherkin)

**Scenario 1: Owner invites a new user who doesn't have an account**
- Given I am the owner of workspace W
- When I open workspace settings, enter email "new@example.com", and click "Send invite"
- Then an invite email is sent to new@example.com within 60 seconds
- And the invite is valid for 7 days from send time
- And a pending invite entry for new@example.com is shown in settings
- When the invitee clicks the invite link within 7 days
- Then they are routed to sign-up, and after completing sign-up, they are
  automatically joined to workspace W with role=member

**Scenario 2: Invitee already has a MoMo account**
- Given an active invite exists for email E
- And a user with email E already has a MoMo account
- When that user clicks the invite link
- Then they are signed in (or prompted to sign in if session expired)
- And joined to the workspace with role=member without going through signup
- And a toast says "You've joined workspace W"

**Scenario 3: Re-invite replaces the old invite**
- Given an active invite for email E exists (link L1, 3 days remaining)
- When the owner clicks "Send invite" again for the same email E
- Then L1 is invalidated (clicking it shows "this invite is no longer valid")
- And a new invite with a new link L2 is sent
- And L2 is valid for 7 days from re-send time

**Scenario 4: Invite expires before use**
- Given an invite for email E was sent 8 days ago
- When the invitee clicks the link
- Then they see "This invite has expired. Ask <inviter> to send a new one."
- And they are NOT joined to the workspace

**Scenario 5: User already in workspace clicks an invite link**
- Given user U is already a member of workspace W
- When U clicks an invite link for workspace W
- Then they see "You're already a member of this workspace" and a link to open it
- And no duplicate membership is created

**Scenario 6: Owner cancels a pending invite**
- Given a pending invite for email E exists
- When the owner clicks "Cancel invite" on that row in settings
- Then the invite is invalidated immediately
- And an audit log entry is created (action=invite_cancelled)

## Out of scope
- Role management UI (can only assign "member" in this story; owner/admin promotion is a follow-up)
- Email domain block-list
- Bulk invite (CSV / multi-email paste) — separate story
- Team billing changes — separate epic

## Open questions for TL
- Existing email service — does it support invite-link tokens with
  server-side revocation, or do we need a new table?
- Audit log: write synchronously on each invite event, or async via
  existing event bus?
- Rate limit on invite sends to prevent abuse (e.g. owner invites
  100 fake emails)?

## INVEST self-check
- [x] Independent — depends only on existing auth + email services
- [x] Negotiable — TL may propose JWT vs server-side token store
- [x] Valuable — directly reduces support load + unblocks team feature
- [x] Estimable — scope is bounded with clear AC
- [x] Small — L (3-5 days); if TL surfaces schema migration needs, split
- [x] Testable — 6 scenarios all have observable outcomes
```

---

## Pattern summary

| Request type | Clarification rounds | Key move |
|---|---|---|
| Typical (Example 1) | 2 rounds, ~6 questions | Cover who/persistence/metric then edge cases |
| Very vague (Example 2) | Escalate to hypotheses after round 2 | Offer 3 concrete "slow"s, user picks |
| Permissions-heavy (Example 3) | 3 rounds, ~10 questions | Push hard on who-can-invite, re-invite, already-member, revocation |

When unsure: **always ask one more edge case**. The cost is 30 seconds; the cost of missing it is a bug in production.
