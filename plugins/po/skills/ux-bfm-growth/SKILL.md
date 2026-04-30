---
name: ux-bfm-growth
description: "Apply the Built For Mars (BFM) growth framework — based on 8 real UX case studies (Costa, Lovable, Monzo Perks, Monzo Savings Challenge, Reddit, Robinhood, Substack, Threads). Use this skill when asked about: user acquisition, viral loops, referral programs, platform leverage, app install strategy, gamification for growth, creator flywheels, channel strategy. Trigger on phrases like 'how to grow', 'acquisition', 'viral', 'referral', 'app installs', 'user growth', 'network effects', 'gamification', 'creator strategy', 'word of mouth'."
---

# BFM Growth Framework

8 BFM case studies reveal how products grow — and where growth strategies backfire. This skill encodes those mechanisms.

## How to Use

Identify which growth category applies, load the relevant reference file, and apply the framework.

**Output format:**
```
## Growth Analysis: [Topic]

### Growth mechanism at play
[Which growth pattern applies and why]

### BFM Evidence
[Verbatim quotes from case studies]

### Recommendation
[Concrete, actionable change]

### Watch out for
[Where this strategy becomes a dark pattern or backfires]
```

---

## 5 Growth Categories

| # | Category | Key Question | Reference |
|---|----------|-------------|-----------|
| 1 | **Platform & Network Leverage** | Are you using existing networks to bootstrap growth instead of starting from zero? | `references/01-platform-leverage.md` |
| 2 | **Channel Strategy: Coercion vs. Alignment** | Are you forcing users to your preferred channel, or making it the obvious best choice? | `references/02-channel-strategy.md` |
| 3 | **Gamification & Habit Loops** | Does your product create behaviour loops that sustain engagement AND generate word-of-mouth? | `references/03-gamification-habits.md` |
| 4 | **Creator & Community Flywheel** | Are your power users growing the product for you? | `references/04-creator-flywheel.md` |
| 5 | **Referral & Viral Mechanics** | Is sharing built into the product experience, or bolted on as a separate programme? | `references/05-referral-viral.md` |

---

## Quick Diagnostic Checklist

- [ ] Growth strategy starts from zero users rather than leveraging an existing platform/network
- [ ] App install prompts appear on every web page visit, even for users who just want to browse
- [ ] Referral reward is a fixed round number applied automatically — no surprise element
- [ ] Gamification streak/challenge ends without a meaningful reward or social moment
- [ ] Creator tools require creators to leave your platform to share or build their audience
- [ ] Growth relies on blocking competitor experiences (third-party API shutdown, web degradation)
- [ ] Signup flow obscures pricing until user has invested effort — then reveals paywall
- [ ] Network effect is not designed in — users don't automatically bring other users

---

## When to Load Reference Files

**Load `01-platform-leverage.md`** when the product has access to an existing user base, data set, or partner network that could bootstrap growth.

**Load `02-channel-strategy.md`** when deciding between web vs. app, aggressive install prompts, or how to migrate users between surfaces.

**Load `03-gamification-habits.md`** when designing streaks, challenges, milestones, or any loop designed to sustain long-term engagement.

**Load `04-creator-flywheel.md`** when building for a platform where creators or power users generate content that attracts other users.

**Load `05-referral-viral.md`** when designing referral programmes, sharing mechanics, or any feature where one user bringing another is the growth model.
