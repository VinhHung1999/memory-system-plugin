---
name: cmo-ceo-cfo-alignment-audit
description: |
  Diagnose how well a CMO is strategically aligned with their CEO and CFO,
  using McKinsey-derived indicators that distinguish high-performing
  trio relationships from low-trust ones. Walks an interactive 12-15
  question audit, scores each axis (CEO alignment, CFO alignment) with
  traffic-light gaps (red/yellow/green), and produces a remediation
  playbook with prioritized actions, recurring rituals, and quarterly
  re-audit cadence. Use when CMO needs to assess executive relationship
  health, after CMO/CEO/CFO transitions, before budget defense, when
  marketing budget is at risk, when CMO feels underappreciated by exec
  team, or for first-90-days planning. Auto-trigger on phrases like
  "CMO alignment", "exec alignment", "CMO CEO CFO relationship",
  "executive trust audit", "marketing budget at risk", "first 90 days CMO",
  "board prep relationship", "executive influence diagnostic".
---

# CMO ⇄ CEO ⇄ CFO Alignment Audit

## What this does

Diagnostic that scores how strategically aligned a CMO is with their CEO and CFO across 12-15 indicators (drawn from McKinsey research on what high-performing trios look like). Outputs:

1. **Per-axis scores** — CEO alignment (0-15), CFO alignment (0-15), Trio overall (0-30)
2. **Traffic-light gap report** — 🔴 high-risk / 🟡 watch / 🟢 healthy per indicator
3. **Remediation playbook** — prioritized actions per gap (week-1 / 30-day / quarter)
4. **Recurring rituals recommendation** — weekly/monthly/quarterly cadences to install
5. **Re-audit timing** — when to re-run (default: 90 days)

**The core problem this solves:** Most CMOs think they're "fine" with CEO and CFO until budget gets cut, marketing gets blamed for a miss, or a new CEO/CFO arrives. By then it's too late. McKinsey research shows CMOs with formal CEO+CFO alignment drive ~2x stronger revenue outcomes — but most CMOs have no diagnostic to assess where they stand.

## When to invoke this skill

- **First 90 days** — new CMO onboarding, new CEO, or new CFO
- **Quarterly health check** — recurring exec relationship diagnostic
- **Before budget defense** — pre-mortem on which gaps will hurt the ask
- **After a marketing miss** — figure out which alignment gap caused the blame
- **When marketing feels underappreciated** — quantify the trust gap
- **Pre-board-meeting prep** — ensure CMO/CEO/CFO present united narrative
- **After strategic pivot** — verify exec alignment survived the change
- **Asked "how should I work better with my CFO?" / "audit my exec relationships"**

**Skip when:**
- Question is about a specific tactical decision (use other CMO skills)
- Cross-functional audience is broader than CEO+CFO (use cross-functional translation matrix instead)
- Issue is marketing-internal (team alignment, not exec alignment)

## When NOT to use

- Tactical campaign question
- Pure strategic/positioning question (no exec relationship angle)
- Cross-functional alignment with Product/Ops/HR (different skill)
- Personnel issue (HR, not strategic alignment)

## Workflow

1. **Confirm scope** — is the user auditing CEO alignment, CFO alignment, or both? (Default: both.)
2. **Run the interactive audit** — `scripts/audit_alignment.py --interactive` walks through 12-15 questions OR `--csv <file>` for batch input. User answers a-d on each.
3. **Read the indicators reference** — `references/alignment-indicators.md` for what each indicator means + McKinsey source + diagnostic-question rationale.
4. **Generate playbook** — script outputs traffic-light scorecard. LLM expands into prioritized remediation per gap.
5. **Install rituals** — `templates/quarterly-trio-review.md` for the recurring CMO/CEO/CFO sync agenda.
6. **Schedule re-audit** — default 90 days; sooner if any axis scores 🔴.

## Running the script

Interactive mode (typical use):

```bash
python3 /Users/phuhung/coursera/.claude/skills/cmo-ceo-cfo-alignment-audit/scripts/audit_alignment.py --interactive
```

Batch mode (paste answers from a CSV — useful for re-audits):

```bash
python3 /Users/phuhung/coursera/.claude/skills/cmo-ceo-cfo-alignment-audit/scripts/audit_alignment.py --answers answers.csv
```

If `python3` crashes with pyexpat error, fall back to `python3.13`.

## Output philosophy

The audit must answer 4 questions for the CMO:

1. **Where am I right now?** (overall score + per-axis)
2. **Which 3 specific gaps will hurt me first?** (red items prioritized)
3. **What do I do this week vs this quarter?** (timed playbook)
4. **What recurring ritual prevents this from regressing?** (cadence install)

DO NOT produce vague "build trust with your CFO" advice. Every red gap must come with: (a) a specific behavior to change, (b) a ritual to install, (c) a measurable success indicator.

The audit is INTENTIONALLY uncomfortable. CMOs who are actually misaligned often score themselves charitably. The script asks pointed questions (e.g., "Can your CFO articulate marketing's top 3 metrics WITHOUT looking?") that surface the gap they would otherwise rationalize.

## References (load on demand)

- `references/alignment-indicators.md` — full indicator list with McKinsey source, diagnostic question rationale, and what each scoring level means
- `templates/quarterly-trio-review.md` — agenda template for recurring CMO/CEO/CFO sync (the most common ritual that fixes 60%+ of gaps)

## Sources

Built from CMO Excellence (Coursera, Hurix Digital, Dec 2025):
- Module 2 Video: "Shaping the Enterprise Growth Agenda"
- Module 2 Reading: "Enterprise Alignment and Cross-Functional Collaboration"
- Module 3 Reading: "Scaling Customer-Centric Growth at the Enterprise Level"

Augmented with: McKinsey research on CMO-CEO-CFO alignment patterns, HBR research on executive relationship health.
