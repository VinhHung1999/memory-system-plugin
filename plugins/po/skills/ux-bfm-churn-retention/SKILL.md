---
name: ux-bfm-churn-retention
description: "Apply the Built For Mars (BFM) churn & retention framework — based on 5 real UX case studies (Audible, Flights Ch.2, LinkedIn, Strava, Trello). Use this skill when asked about: why users leave, how to prevent cancellation, re-engagement flows, subscription retention, notification fatigue, habit loops, or any question about keeping users active. Trigger on phrases like 'users are leaving', 'high churn', 'cancellation rate', 'win-back', 'how to retain', 'reduce churn', 'inactive users'."
---

# BFM Churn & Retention Framework

5 BFM case studies reveal why users leave and what actually keeps them. This skill encodes those mechanisms.

## How to Use

Identify which retention failure category applies, load the relevant reference file, and apply the framework.

**Output format:**
```
## Churn Analysis: [Topic]

### Why users are leaving
[Which retention failure mechanism applies and why]

### BFM Evidence
[Verbatim quotes from case studies]

### Recommendation
[Concrete, actionable change]

### Watch out for
[Common mistake — the dark-pattern version of this fix]
```

---

## 5 Retention Failure Categories

| # | Category | Key Question | Reference |
|---|----------|-------------|-----------|
| 1 | **Cancellation Timing** | Are you trying to save users after they've already decided to leave? | `references/01-cancellation-timing.md` |
| 2 | **Notification Fatigue** | Is noise from your app causing accidental churn? | `references/02-notification-fatigue.md` |
| 3 | **Micro-Commitments & Loyalty** | Have users invested enough to feel locked in (positively)? | `references/03-micro-commitments.md` |
| 4 | **Discovery & Re-engagement** | Is stale content killing return visits? | `references/04-discovery-reengagement.md` |
| 5 | **Core Value Focus** | Are you adding complexity instead of deepening the one thing that retains? | `references/05-core-value-focus.md` |

---

## Quick Diagnostic Checklist

- [ ] Cancellation screen is the first place users are shown value they'd lose — too late
- [ ] Push notifications fire for non-urgent events, training users to ignore all alerts
- [ ] User can start over from zero after taking a break — no invested effort preserved
- [ ] Home feed/content doesn't change between sessions — stale experience
- [ ] Adding new features to solve churn instead of deepening the core use case
- [ ] Price tracking / watchlist requires account creation before showing value
- [ ] Cancellation copy lists features, not personal user data ("you ran 47 km this month")
- [ ] Re-engagement email arrives weeks after lapse with no acknowledgment of the gap

---

## When to Load Reference Files

**Load `01-cancellation-timing.md`** when designing cancel flows, "save the cancel" screens, or pause/downgrade options.

**Load `02-notification-fatigue.md`** when notification open rates are dropping, users are muting the app, or churn correlates with notification volume.

**Load `03-micro-commitments.md`** when users are comparison-shopping, not returning after first session, or abandoning mid-funnel.

**Load `04-discovery-reengagement.md`** when DAU/WAU ratio is dropping, users open the app and immediately close it, or content engagement is low despite good library.

**Load `05-core-value-focus.md`** when product roadmap debates centre on adding features to combat churn instead of improving the core loop.
