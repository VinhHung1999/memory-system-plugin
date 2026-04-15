# 📣 Marketing Toolkit — Claude Code Plugin

8 production-ready marketing skills distilled from Google's **Digital Marketing & E-commerce Professional Certificate** (7 courses, 267 video lectures).

Every skill is self-contained:
- `SKILL.md` — trigger rules + workflow
- `scripts/` — deterministic Python scripts (no LLM creativity needed for the math)
- `references/` — benchmarks, playbooks, templates loaded when needed
- `templates/` — ready-to-paste HTML/CSV/MD files

---

## The 8 skills

| Skill | Trigger when user says... | Output |
|---|---|---|
| **`seo-onpage-checklist`** | "audit SEO of X", "improve SEO", "check meta tags" | Scored 0-100 report with top fixes per page |
| **`email-campaign-builder`** | "write welcome email", "promotional email", "newsletter draft" | Full brief: 3 subject A/B + HTML body + plain text + segmentation + KPIs |
| **`email-metrics-analyzer`** | "analyze email CSV", "is my open rate good" | 4-pillar report with 🟢🟡🔴 per metric + 3 next experiments |
| **`social-media-content-calendar`** | "plan 30 days social", "content calendar for X" | CSV 100-266 rows with real copy, platform-specific + voice-consistent |
| **`ab-test-designer`** | "A/B test headline", "is my test significant", "should I stop" | Sample-size calc + p-value verdict (win / loss / inconclusive) |
| **`ai-marketing-prompts`** | "write a prompt for", "my AI output is generic" | T-C-R-E-I prompt, ready to paste into ChatGPT/Claude/Gemini |
| **`social-listening-keywords-builder`** | "track brand mentions", "set up Hootsuite", "monitor competitors" | CSV + boolean queries for Hootsuite, Brandwatch, Sprout, Mention |
| **`marketing-performance-dashboard`** | "weekly marketing report", "how are my ads doing" | Unified dashboard pulling GA4 + Google Ads (or from CSV / pasted numbers) |

---

## Benchmark results

All skills evaluated against baseline (no skill, general knowledge only):

| Skill | Pass rate (with) | Pass rate (without) | Delta |
|---|---|---|---|
| seo-onpage-checklist | 92% | 58% | +34% |
| email-campaign-builder | 94% | 39% | **+55%** |
| email-metrics-analyzer | 94% | 56% | +38% |
| social-media-content-calendar | 90% | 50% | +40% |
| ab-test-designer | 100% | 88% | +12% |
| ai-marketing-prompts | 94% | 44% | **+50%** |
| social-listening-keywords-builder | 94% | 56% | +38% |
| marketing-performance-dashboard | 88% | 29% | **+59%** |
| **Average** | **93%** | **48%** | **+45%** |

---

## Synergy — use as a pipeline

```
1. ai-marketing-prompts           → research audience + brand voice (T-C-R-E-I)
2. seo-onpage-checklist           → audit site technical SEO
3. social-media-content-calendar  → 30-day organic social plan
4. social-listening-keywords-builder → monitor brand mentions
5. email-campaign-builder         → draft email campaigns
6. email-metrics-analyzer         → measure email performance
7. ab-test-designer               → optimize winning variants
8. marketing-performance-dashboard → weekly unified report
```

---

## Installation

### Via plugin marketplace (if registered)
```
/plugin install marketing-toolkit
```

### Manual
```bash
git clone https://github.com/VinhHung1999/memory-system-plugin
# In Claude Code:
/plugin install ./memory-system-plugin/plugins/marketing-toolkit
```

### Python dependencies

Some skills require Python packages:
- `seo-onpage-checklist` → `requests`, `beautifulsoup4`
- `email-metrics-analyzer` → `pandas`
- `marketing-performance-dashboard` → `google-analytics-data`, `google-ads`, `google-auth-oauthlib`, `jinja2` (optional: `matplotlib`)

Install all at once:
```bash
pip install --user requests beautifulsoup4 pandas google-analytics-data google-ads google-auth-oauthlib jinja2 matplotlib
```

On systems where `python3` has broken native modules (e.g. Python 3.14 pyexpat bug on some macOS setups), the skills automatically fall back to `python3.13`.

---

## Design philosophy

### Why deterministic scripts + reference docs (not pure LLM)

LLMs are creative but inconsistent. Marketing metrics need to be:
- **Reproducible** — same numbers every run
- **Auditable** — show your math
- **Fast** — 30 seconds, not 3 minutes of token generation

Scripts handle the deterministic parts (computing ROI, generating misspellings, parsing HTML, rendering reports). The LLM handles the creative/interpretive parts (writing actual copy, interpreting context, tailoring recommendations).

### Why reference docs instead of bigger SKILL.md

Claude's context window is finite. The `references/` pattern means:
- Core workflow always loaded (~500 lines)
- Deep-dive docs loaded on-demand when user asks "why"
- Net result: faster reads, more detail available when needed

### Why traffic lights 🟢🟡🔴

Stakeholders don't read tables. They scan. A 3-color signal is the fastest way to answer "is this good?"

---

## Source

Built by learning all 7 courses of Google's Digital Marketing & E-commerce certificate:
1. Foundations of Digital Marketing and E-commerce
2. Attract and Engage Customers with Digital Marketing
3. From Likes to Leads: Interact with Customers Online
4. Think Outside the Inbox: Email Marketing
5. Assess for Success: Marketing Analytics and Measurement
6. Make the Sale: Build, Launch, and Manage E-commerce Stores
7. Satisfaction Guaranteed: Develop Customer Loyalty Online

Transcripts + enriched notes live at `~/coursera/google-digital-marketing-ecommerce/`.

---

## License

MIT — use freely, modify, redistribute.
