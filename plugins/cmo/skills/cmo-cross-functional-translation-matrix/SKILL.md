---
name: cmo-cross-functional-translation-matrix
description: |
  Translate a marketing insight, campaign result, or strategic recommendation into the
  language each non-marketing function actually cares about (Finance, Product,
  Operations, HR, Sales, Legal, IT, Customer Success). Generates a structured
  per-function reframing table with that function's KPIs, evidence type, and
  next-step ask. Use when CMO needs to present marketing intelligence to other
  executives, prepare cross-functional meetings, write QBRs, defend budget,
  build cross-functional alignment, or shape the enterprise growth agenda. Auto-trigger
  on phrases like "present to CFO", "translate for Product", "explain to Operations",
  "cross-functional alignment", "executive translation", "enterprise alignment".
---

# CMO Cross-Functional Translation Matrix

## What this does

Converts ONE marketing insight into N tailored versions — one per target function — each speaking that function's KPIs, with the right evidence type and a function-specific ask.

**The core problem this solves:** A CMO presents the same NPS finding to CFO, Head of Product, and COO. CFO yawns. Product nods politely. COO ignores. Same data, wrong framing.

**The fix:** Translate insight → function-specific KPI hook → function-specific evidence → function-specific ask.

## When to invoke this skill

Invoke when the user is:

- Preparing for a cross-functional meeting or QBR
- Drafting a CFO budget defense / business case
- Writing a board update or executive summary
- Sharing customer/market research with non-marketing leaders
- Building a cross-functional alignment plan
- Pitching a marketing program that needs Product/Ops/HR support
- Asked "how should I present this to [function]?"
- Translating campaign results across departments

**Skip when:** The audience is marketing-only, or the insight is a tactical execution detail (e.g., ad copy choice).

## When NOT to use

- Audience is purely marketing team (no translation needed)
- The insight is already framed for the right audience
- Question is about marketing-internal optimization (use other CMO skills)
- For positioning vs competitors → use positioning frameworks instead

## Workflow

1. **Capture the raw insight** — get a 1-3 sentence marketing finding with the underlying data.
2. **Identify target functions** — user specifies (e.g., "CFO + Product"), or default to the canonical 4: Finance, Product, Operations, HR. Add Sales/Legal/IT/CS only if user requests.
3. **Run the translation script** — `scripts/translate_insight.py` produces the structured matrix.
4. **Augment with deck template** if needed — `templates/cross-functional-deck.md` for 1-slide-per-function output.
5. **Apply the credibility check** — read `references/function-language-map.md` to verify each function's KPI choice matches what they actually report.

## Running the script

```bash
python3 /Users/phuhung/coursera/.claude/skills/cmo-cross-functional-translation-matrix/scripts/translate_insight.py \
  --insight "Mobile-first cohort has 18-pt higher NPS and 2x retention vs web at 90 days" \
  --functions "finance,product,operations,hr"
```

Output: structured table per function with reframed message + KPI hook + evidence type + ask.

If `python3` crashes with pyexpat error on macOS, fall back to `python3.13`.

## Output philosophy

Each function row must answer 4 questions:
1. **What does this mean to YOU?** (reframed in their KPI vocabulary)
2. **What evidence should I bring?** (cohort data, attribution, benchmark)
3. **What's the specific ask?** (a budget shift, a roadmap slot, a hiring focus, etc.)
4. **Why should you say yes now?** (link to their current pressure / quarter goals)

DO NOT produce generic "Finance cares about ROI" platitudes. The script + reference combine to produce specific, evidence-backed translations.

## References (load on demand)

- `references/function-language-map.md` — full per-function mapping: KPIs they report, language they use, evidence types they trust, common asks
- `templates/cross-functional-deck.md` — 1-slide-per-function template structure for follow-up deck

## Sources

Built from CMO Excellence (Coursera, Hurix Digital, Dec 2025):
- Module 2 Video: "Building Influence Across Functions"
- Module 2 Reading: "Enterprise Alignment and Cross-Functional Collaboration"
- Module 3 Reading: "Scaling Customer-Centric Growth at the Enterprise Level"

Augmented with: McKinsey research on CMO-CEO-CFO alignment patterns.
