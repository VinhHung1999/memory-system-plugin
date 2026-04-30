---
name: ux-bfm-benchmarking
description: "Apply the Built For Mars (BFM) benchmarking framework — based on 11 cross-product UX comparisons (banking UX chapters 7-9, video call showdown, supermarkets, parcel delivery, overdraft application, maps, bank account opening, PS5 vs Xbox). Use this skill when comparing products across the same category, running competitive UX audits, or applying the BFM task-based benchmarking methodology. Trigger on: 'compare X vs Y', 'benchmark', 'competitive UX', 'how does X compare to', 'best in class for', 'which app does X better', 'industry standard for', 'UX audit against competitors'."
---

# BFM Benchmarking Framework

BFM's benchmarking studies compare products in the same category doing the same tasks — revealing where industry norms are set and where the gap between best and worst is largest.

## How to Use

Apply the BFM benchmarking methodology: define the task set, identify the competitors, run the same tasks across all, and score on specific criteria.

**Output format:**
```
## Benchmark: [Product Category] — [Specific Task]

### Category baseline
[What the industry standard looks like for this task]

### Best-in-class
[Which product does this best, and what specifically makes it better]

### Worst-in-class
[Which product does this worst, and what specifically fails]

### BFM Evidence
[Verbatim observations from benchmarking studies]

### Recommendation
[Specific, actionable change to reach best-in-class]
```

---

## BFM Benchmarking Methodology

BFM benchmarks by running identical tasks across competing products and scoring specific UX moments. Key principles:

1. **Same task, same starting state** — all products tested on the same scenario (e.g., "send £100 to an overseas account")
2. **Score specific moments** — not overall impressions, but specific interaction points (notification format, form field count, error recovery)
3. **Find the outlier** — one product always does something meaningfully better or worse; that's the insight
4. **Industry norm vs. industry best** — distinguish between "everyone does this" and "this is the right way"

---

## 5 Benchmarking Domains

| # | Domain | Coverage | Reference |
|---|--------|----------|-----------|
| 1 | **Banking UX** | Sending money, notifications, balance display, overdraft flow | `references/01-banking-ux.md` |
| 2 | **Video Calls** | Zoom, Teams, Meet, FaceTime — core call UX patterns | `references/02-video-calls.md` |
| 3 | **Retail & Supermarkets** | Grocery ordering, checkout, delivery tracking | `references/03-retail-supermarkets.md` |
| 4 | **Delivery & Logistics** | Parcel tracking, delivery notification, carrier comparison | `references/04-delivery-logistics.md` |
| 5 | **Cross-category methodology** | How to run a BFM-style benchmark on any product category | `references/05-benchmark-methodology.md` |

---

## Quick Diagnostic Questions (for any benchmark)

- What is the specific task — not "make a payment" but "send £100 to an overseas payee for the first time"?
- What does the best product do at each decision point?
- Where does the worst product add a step, a click, or ambiguity that the best product eliminates?
- Is the gap between best and worst caused by a design decision, or a policy/technical constraint?
- What would it take for the worst product to match the best — one change, or a system redesign?
