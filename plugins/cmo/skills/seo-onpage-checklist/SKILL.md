---
name: seo-onpage-checklist
description: Audit a URL or HTML file against the on-page SEO checklist from Google's Digital Marketing certificate. Checks title tag, meta description, H1/heading hierarchy, image alt+filenames, JSON-LD structured data, canonical, viewport, internal linking, and returns a scored PASS/FAIL report with specific fix suggestions. Use this skill whenever the user asks to audit SEO, check SEO, review SEO of a page, improve SEO, do an SEO review, "is my SEO good", check meta tags, validate schema markup, or pastes a URL and asks what to fix — even if they don't use the word "audit".
---

# SEO On-page Checklist Auditor

A pragmatic on-page SEO audit tool based on Google's Digital Marketing & E-commerce certificate (Course 2, "Attract and Engage Customers"). This skill runs 10 technical checks against a URL or local HTML file and returns a scored report.

## When this skill triggers

The user has pasted a URL (or a local HTML file path) and wants to know what's wrong with its SEO, or wants a structured checklist review. They may phrase it as: "audit SEO of X", "check SEO", "review this page", "what's wrong with my meta tags", "why isn't my page ranking", or simply paste a URL asking "what should I fix".

The skill is **not** the right tool for keyword research (different skill), link-building strategy, content quality grading, or Core Web Vitals performance. Focus is strictly on-page technical SEO as taught in the certificate.

## Workflow

1. **Get the target** — ask the user for a URL or HTML file path if not provided. Accept both.
2. **Run the audit** — execute `scripts/seo_audit.py <target>` which fetches (if URL) or reads (if file) the HTML and prints a markdown report to stdout. Save the report if the user wants to keep it.
3. **Present the report** — show results grouped by category (Title + meta, Headings, Images, Structured data, Technical). For each FAIL, highlight the fix suggestion.
4. **Offer to deep-dive** — for any failure the user cares about, offer to explain the underlying SEO reasoning (why Google cares about this) and give a code/content fix. Pull from `references/checklist.md` for exhaustive detail.

## Running the audit script

```bash
python3 scripts/seo_audit.py https://example.com
python3 scripts/seo_audit.py /path/to/local/page.html
```

The script is standalone — requires `requests` and `beautifulsoup4`. If either isn't installed, the script prints an install hint. On systems where `python3` points to a version with broken native deps (e.g., Python 3.14 pyexpat issue on some macOS installs), try `python3.13` as a fallback.

## Why this matters

On-page SEO isn't just a checklist — each item maps to how Google's crawler + ranking algorithm interprets the page (covered in Course 2 Module 2 lectures m2_02 "How Google works" and m2_03 "How Google ranks"). A failing title tag means Google writes the SERP title itself, often poorly. Missing alt text breaks image search + accessibility. Missing JSON-LD means you lose rich results eligibility entirely. The point of this audit is not to blindly pass checks but to understand what's blocking visibility and fix the specific gaps.

When presenting results, lead with the 2-3 most impactful FAILs — don't bury the signal in a wall of PASS rows. If everything passes, still flag any `WARN` items (e.g., title is valid but generic, meta is present but under-optimized).

## Reference

- `references/checklist.md` — full list of every check, what it tests, why Google cares, and canonical fix examples
- `references/schema-templates.md` — JSON-LD copy-paste examples for Product, Article, FAQ, Recipe, Organization

Read `checklist.md` if the user asks "why does this fail" or wants deeper reasoning than the terse fix suggestion in the report.
