---
name: email-campaign-builder
description: Build a complete email marketing campaign brief from a goal + funnel stage + persona. Picks the right email type (acquisition, welcome, newsletter, promotional, retention), drafts subject line variants (3 for A/B), writes HTML + plain-text body using type-specific templates, defines segmentation rules, and sets KPI targets with industry benchmarks (open 20-25%, CTR 2-5%, conv 1-5%, ROI 42:1). Use this skill whenever the user wants to draft/plan/launch an email campaign, write a welcome email, build a newsletter, send a promotional blast, set up a retention email, or asks for "an email for X" — even if they don't use the word "campaign".
---

# Email Campaign Builder

Produces a complete, launch-ready email campaign brief grounded in Google's Digital Marketing certificate (Course 4 "Think Outside the Inbox"). Built around the email-type ↔ funnel-stage matrix so the right kind of email goes to the right audience.

## When this triggers

User asks to write, plan, or launch an email — anywhere from vague ("write me an email for new subscribers") to specific ("draft a promotional email for 30% off winter sale, targeting lapsed customers"). Also triggers on "newsletter ideas", "welcome flow", "win-back campaign", "retention email", "cart abandonment email" (which is a type of retention/promotional).

**NOT** the right tool for: transactional emails (password reset, order confirmation — those are product notifications, not marketing), bulk cold outreach/spam, or email deliverability troubleshooting.

## Workflow

1. **Collect inputs** — if the user didn't provide them, ask concisely for:
   - Campaign goal (e.g., "get new signups to try the product", "reactivate customers who haven't bought in 90 days")
   - Funnel stage (awareness / consideration / conversion / loyalty) — infer from goal if possible
   - Target persona (demographics + goal + barrier) — can be a 2-3 sentence sketch
   - Brand voice — 2-3 adjectives ("playful and confident" / "formal and data-driven")
   - Key offer or message (what's the hook?)

2. **Pick the email type** — use the matrix in `references/type-funnel-matrix.md`:

   | Funnel stage | Email type |
   |---|---|
   | Awareness | Acquisition |
   | Consideration | Welcome |
   | Consideration/Conversion/Loyalty | Newsletter |
   | Consideration/Loyalty | Promotional |
   | Loyalty | Retention |

3. **Generate subject line variants** — 3 options optimized for A/B testing, following rules in `references/subject-line-formulas.md`:
   - Clarity beats catchiness — answer "what are you offering?"
   - 30-60 chars (mobile preview cuts ~50)
   - Include personalization token if relevant
   - 1 emoji max, brand-fit only

4. **Draft body** — load the matching template from `templates/<type>.html` (and plain-text fallback from `templates/<type>.txt`). Apply brand voice to copy. Fill in offer, CTA, social proof slots.

5. **Define segmentation** — default 3-4 segments from `references/segmentation-defaults.md`:
   - High-engagement (opened in last 30d)
   - Net-new (signed up last 7d)
   - Lapsed (no engagement 60+ days)
   - VIP (top 10% spend)

   User may override. Output segmentation as JSON or Mailchimp tag syntax.

6. **Set KPI targets** — pull from `references/benchmarks.md`. Always include:
   - Open rate target (benchmark 20-25%)
   - CTR target (2-5%)
   - Conversion rate target (1-5%)
   - Unsubscribe ceiling (<0.5%)
   - ROI expectation (42:1 industry avg, adjust for vertical)

7. **Assemble the brief** — output a single markdown document with:
   - Summary (goal, type, target segment)
   - 3 subject line variants (A/B/C) with rationale
   - HTML body (inline-styled, mobile-first)
   - Plain-text body (accessibility + spam-filter fallback)
   - Segmentation rules (SQL-style OR Mailchimp tag filters)
   - KPI targets + benchmarks
   - Compliance footnote (CAN-SPAM / GDPR basics)

## Why this approach

Email marketing has the highest ROI of any channel (42:1 avg) but most drafts fail because they pick the wrong type for the stage — e.g., sending a newsletter to cold leads (they haven't opted in to regular contact yet) or a promotional blast to new subscribers who haven't built trust. The matrix + template pattern prevents that mismatch.

Subject line clarity matters more than cleverness: Course 4 research shows "What are you offering?" test is the single strongest predictor of open rate. The 3-variant A/B output gives the user direct A/B test setup.

HTML + plain-text dual output isn't optional: plain-text is both an accessibility win AND a spam-filter signal (emails without it are more likely to be flagged).

## References

- `references/type-funnel-matrix.md` — full type ↔ stage decision guide with examples
- `references/subject-line-formulas.md` — 20 proven subject line patterns by goal
- `references/segmentation-defaults.md` — 4 default segments + custom segment builder
- `references/benchmarks.md` — KPI benchmarks per vertical (e-comm, SaaS, nonprofit)
- `references/compliance.md` — CAN-SPAM, GDPR, CASL one-pager

## Templates

- `templates/acquisition.html` + `.txt`
- `templates/welcome.html` + `.txt`
- `templates/newsletter.html` + `.txt`
- `templates/promotional.html` + `.txt`
- `templates/retention.html` + `.txt`

Each template is a Jinja-style fill-in structure with slots for `{{subject}}`, `{{greeting}}`, `{{offer}}`, `{{cta_text}}`, `{{cta_url}}`, `{{social_proof}}`, `{{footer}}`.

## Optional script

`scripts/build_brief.py` — if the user provides a JSON config, generates the full brief non-interactively. Useful for pipelines. Usage:
```bash
python3 scripts/build_brief.py config.json > campaign-brief.md
```
