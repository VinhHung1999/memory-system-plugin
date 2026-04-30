# A/B Testing Pitfalls

## 1. Peeking (early stopping)

**What it is:** Checking results daily and stopping when p < 0.05 the first time it crosses.

**Why it breaks:** With daily checks, false-positive rate inflates from 5% to ~25%+. "Significant wins" are often noise.

**Fix:**
- Decide duration upfront based on sample size calc.
- Only check at pre-planned interim points (midpoint + end), not daily.
- Or use sequential tests (rarely needed for marketing A/Bs).

## 2. Novelty effect

**What it is:** New variant wins in week 1, then performance decays as users get used to it.

**Why it breaks:** You ship the variant thinking it's permanent win, then see regression to mean in week 3.

**Fix:**
- Run tests 2-4 weeks minimum (catches novelty decay).
- Don't test tiny cosmetic changes that could have novelty but no durable effect.
- Re-test winners after 30 days in production.

## 3. Simpson's paradox

**What it is:** Variant B beats A in aggregate, but loses in every single segment.

**Example:**
- Desktop users: A converts 3%, B converts 2.5% → A wins
- Mobile users: A converts 1%, B converts 0.8% → A wins
- Aggregate: B converts 1.8%, A converts 1.5% → B wins!

This happens because more mobile users saw B (B had 80% mobile), and mobile converts lower overall.

**Fix:**
- Always segment results by top dimensions: device, traffic source, new vs returning.
- If segments disagree, investigate — often a technical or allocation issue.
- Report both aggregate AND segment-level results.

## 4. Sample Ratio Mismatch (SRM)

**What it is:** Traffic split drifts from intended 50/50 to e.g., 52/48 or worse.

**Why it breaks:** Usually a technical issue — tracking script broken on one variant, or routing uneven. Invalidates the comparison.

**Fix:**
- Compute expected vs observed split with a chi-squared test.
- If p < 0.01 for SRM: DO NOT trust the test. Investigate infrastructure.
- Common culprits: caching, bot traffic to one variant, redirect loop.

## 5. Confounds

**What it is:** Variant B appears to win, but something else changed at the same time.

**Examples:**
- Test started Monday; previous campaign ended Sunday.
- Variant B launched on Black Friday week.
- Another team changed sitewide copy during test.

**Fix:**
- Launch control + test simultaneously (never sequentially).
- Document all sitewide changes during test period.
- Exclude "external event" days if possible.

## 6. Low-power tests

**What it is:** Declaring "no difference" from an underpowered sample.

**Example:** 200 visitors each, 10 conversions vs 12. p = 0.66, "no difference". Actually you have no ability to detect anything smaller than a 40% lift with 200 visitors.

**Fix:**
- ALWAYS run sample size calc first.
- If you can't hit min sample, accept you can only detect BIG effects, not subtle ones.
- Don't conclude "no difference" — conclude "inconclusive, need more data".

## 7. Testing the wrong metric

**What it is:** Testing for CTR win when the real goal is revenue.

**Example:** Variant B increases CTR by 30% but clicks are all low-intent traffic → revenue flat or down. You shipped a CTR win that hurt business.

**Fix:**
- Test the metric closest to business goal. For ads: conversion rate > CTR. For e-commerce: revenue per visitor > conversion rate.
- CTR-only wins must be validated on conversion/revenue before shipping permanently.

## 8. Multiple comparisons

**What it is:** Running 10 tests simultaneously, some "win" by chance.

**Why it breaks:** 1/20 tests "wins" at p<0.05 purely by random chance. If you run 10 tests, expect 0.5 fake winners.

**Fix:**
- Use Bonferroni correction: α / n_tests. 10 tests → require p < 0.005 for significance.
- Or run tests sequentially so each has α=0.05.
- Be suspicious of surprising wins — try to replicate.

## 9. Ignoring effect size

**What it is:** Focusing on p-value alone when effect size is tiny.

**Example:** 0.1% lift is statistically significant with massive sample but clinically meaningless.

**Fix:**
- Report effect size + confidence interval alongside p-value.
- Ask "is this lift worth the implementation cost?" before shipping.

## 10. Not ramping winners

**What it is:** Ship-winner-at-100% immediately, then something breaks and all traffic is affected.

**Fix:**
- Ship winner to 50% for 1 week, monitor for regression.
- Then ramp to 100%.
- Especially important for changes with side effects (e.g., checkout flow changes that could break for some user segments).
