---
name: ab-test-designer
description: Design and interpret A/B tests for Google Ads + landing pages + email. Walks from hypothesis → variant spec → sample-size calc → significance test. Computes statistical significance (chi-squared for proportions, t-test for continuous metrics), flags underpowered tests, and gives concrete verdict (significant win / significant loss / inconclusive — run longer). Use this skill whenever the user wants to A/B test ads or landing pages, set up a Google Ads Experiment, calculate if an existing test is significant, decide when to stop a test, interpret test results, or asks "is variant B actually better?" — even if they don't use the phrase "A/B test".
---

# A/B Test Designer

Build rigorous A/B tests from hypothesis to verdict. Based on Google's Digital Marketing certificate Course 5 Module 3 — A/B fundamentals + Google Ads Experiments setup + results interpretation.

## When this triggers

User is running or planning an A/B test. Phrasings: "A/B test headline", "split test my ads", "is this test significant", "how long do I run the test", "which variant won", "set up Google Ads experiment", "test landing page variants".

**NOT** the right tool for: full experimental design for non-marketing (scientific trials, medical), multi-armed bandits, MVT (multivariate) — this skill focuses on 2-variant A/B for ad/landing/email contexts.

## Workflow

### Pre-test: Design

1. **Hypothesis** — user states belief + reasoning
   Template: *"I believe [change] will cause [metric] to [improve/decrease] by [X%] because [user-centric reason]."*
   Example: "I believe shorter headlines will increase CTR by 20% because mobile users scan quickly."

2. **Variant spec** — generate A (control) vs B (test) differing in ONE element only
   - Headline / body copy / image / CTA text / CTA color / landing page hero / offer
   - NEVER change multiple elements at once (can't attribute result)

3. **Sample size calc** — run `scripts/sample_size.py` with:
   - Baseline conversion rate (e.g., CTR = 2%)
   - Minimum detectable lift (MDE, e.g., 10% relative)
   - Statistical power (default 80%)
   - Significance level (default 5%)
   - Output: minimum impressions/clicks per variant

4. **Google Ads Experiment setup** (if applicable) — from `references/google-ads-experiments.md`:
   - Campaigns → All campaigns → Experiments → "+"
   - Choose scope (all campaigns / select)
   - Pick edit type (Headlines, URL, CTA)
   - 50/50 split (default)
   - Start date, end date (based on sample size calc)

### During test: Monitor

- Don't peek early. Decide duration upfront based on sample size calc.
- Watch for technical breakage (tracking broken = invalidates test)
- Don't pause based on early results — confidence interval is wide until sample is large

### Post-test: Interpret

5. **Compute significance** — run `scripts/ab_significance.py` with counts per variant
   - Discrete metrics (CTR, conv rate): chi-squared or z-test for proportions
   - Continuous metrics (revenue, time): t-test
   - Default α = 0.05 (p < 0.05 = significant)

6. **Verdict** — 3 outcomes:
   - **Significant win**: B > A, p < 0.05, AND sample per variant ≥ minimum → ship B
   - **Significant loss**: B < A, p < 0.05, sample adequate → keep A, log learning
   - **Inconclusive**: |B − A| not significant OR sample insufficient → run longer OR accept no difference

7. **Common pitfalls** (always call out) — from `references/common-pitfalls.md`:
   - **Peeking** (early looks inflate false-positive rate)
   - **Simpson's paradox** (aggregate vs segment results differ)
   - **Novelty effect** (new variant wins briefly then decays)
   - **Sample ratio mismatch** (traffic split drifts from 50/50 → technical issue)

## Running the scripts

```bash
# Pre-test: how many visits per variant?
python3 scripts/sample_size.py --baseline-rate 0.02 --mde 0.10 --power 0.8 --alpha 0.05
# → "Need ~17,000 impressions per variant"

# Post-test: is the test significant?
python3 scripts/ab_significance.py --a-total 10000 --a-converted 200 --b-total 10000 --b-converted 240
# → "B converted at 2.4% vs A's 2.0%. p-value = 0.031. B is significantly better (p<0.05)."
```

Scripts require `scipy` (`pip install scipy`). Both are standalone — no API calls.

## Why this matters

Most A/B tests fail not because the math is wrong but because the **design** is sloppy:
1. Tested 5 things at once → can't attribute the win
2. Stopped at day 2 because "variant B looks better" → peeked into noise
3. No sample size calc → declared "winner" on 200 clicks (not significant, just random)
4. Compared Friday (A) vs Monday (B) → day-of-week confound

This skill enforces the discipline: hypothesis first, one variable, pre-calculated sample size, post-test significance check.

## Statistical significance primer

**p-value** = probability of seeing the observed difference (or larger) assuming no real difference exists.
- p < 0.05 → only 5% chance the "win" is random → confident B is different
- p = 0.2 → 20% chance it's random → NOT significant, inconclusive

**Power** = probability of detecting a real effect if one exists.
- 80% power is standard — means if B is truly better by MDE, 80% of the time your test will catch it.

**MDE (minimum detectable effect)** = smallest lift you care to detect.
- Smaller MDE = much bigger sample needed.
- Don't try to detect 1% lift with 1000 visitors — mathematically impossible.

## References

- `references/google-ads-experiments.md` — step-by-step Google Ads Experiments walkthrough with screenshots descriptions
- `references/common-pitfalls.md` — peeking, novelty, Simpson's paradox, SRM with examples
- `references/hypothesis-templates.md` — 15 hypothesis patterns by metric (CTR, conv rate, revenue)

## Output philosophy

Every analysis should end with:
1. **Verdict** — 1 sentence (win / loss / inconclusive)
2. **Confidence** — p-value + sample adequacy
3. **Next action** — "ship B" / "keep A" / "run N more days" / "test different hypothesis"

Never say "probably better" or "trend toward". Either it's significant (evidence supports shipping) or it's not (need more data or accept no difference).
