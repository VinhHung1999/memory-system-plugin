# Cluster Customer Feedback Prompt Template

From Course 7 M4 m4_01 "Justine: Driving impact with AI in the workplace".

Use when you have 50-500 open-ended customer responses (survey answers, reviews, support tickets) and need to find themes.

## Full T-C-R-E-I prompt

```
**Task (T):** Cluster these {N} customer {responses_or_reviews} into 5-7 themes. Rank themes by frequency, include 2-3 representative verbatim quotes per theme, and note any surprising or counter-intuitive patterns.

**Context (C):**
- Source: {survey / reviews / support_tickets / NPS_comments}
- Collection period: {date_range}
- Audience: {segment — who are these people}
- Business context: {what_product_they_were_commenting_on}
- What we think we'll find (to check against): {your_hypothesis}

**References (R):**
Paste the responses here (anonymized if any PII):

```
{Paste responses here, one per line}
```

**Evaluate (E):**
After clustering:
1. Which 2 themes, if fixed/amplified, would have the biggest business impact?
2. Which 1 theme did I NOT expect to see (surprise finding)?
3. Any signal of customers trying to communicate something they couldn't quite articulate? (read-between-the-lines insight)
4. Which themes are actionable NOW vs require roadmap work?

**Iterate (I):**
After initial clusters:
- "Re-cluster into just 3 actionable themes, cutting the rest"
- "For theme #{N}, suggest 3 specific product changes we should consider"
- "Draft a 1-page stakeholder summary of these findings"
```

## Why this wins over spreadsheet categorization

Manually tagging 200 survey responses = 3-4 hours. AI clustering = 30 seconds + your review. The quality is comparable for themes, and the "surprising finding" step regularly surfaces things humans miss (because humans tag what they expected).

## Privacy guardrails

Before pasting:
- **Remove PII** — names, emails, phone numbers, account IDs
- **Anonymize**: "User #123 said..." instead of "Jane Doe from Acme said..."
- **If highly sensitive** (healthcare, legal, finance): use a local LLM or enterprise tier with data-retention opt-out

See `references/privacy-guardrails.md` for full list.

## Expected output structure

| Rank | Theme | Frequency | Quotes | Action priority |
|---|---|---|---|---|
| 1 | ... | 45/200 | ... | High/Med/Low |

Plus the surprising finding + read-between-the-lines insights.

## Common failure modes

- **Themes too vague** ("Users want better UX") → Ask for specificity: "Each theme must be concrete enough that I could write a 1-page change proposal for it."
- **No surprise finding** → Force it: "Even if nothing stands out, tell me which theme I would probably NOT have predicted."
- **Long quotes** → "Verbatim quotes must be under 20 words each — pick the most-representative snippet."
