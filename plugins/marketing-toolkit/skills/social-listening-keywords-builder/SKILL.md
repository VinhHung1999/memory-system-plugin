---
name: social-listening-keywords-builder
description: Build a comprehensive social listening keyword list for a brand across 6 categories (brand names + misspellings, product names, slogans, key people, industry buzzwords, hashtags). Auto-generates common misspellings/typos, suggests industry terms, and outputs CSV + ready-to-paste boolean queries for Hootsuite, Sprout Social, Brandwatch, and Mention. Use this skill whenever the user wants to set up social listening, monitor brand mentions, track competitors on social, audit what's being said about their company, configure a listening dashboard, or asks "what keywords should I track" — even if they don't mention "listening".
---

# Social Listening Keywords Builder

Builds a complete keyword list for monitoring what's being said about your brand (and competitors) across social platforms. Based on Google's Digital Marketing certificate Course 3 Module 3 — the 6-category listening framework.

## When this triggers

User is setting up social listening and wants to know what keywords/queries to track. Phrasings: "set up social listening", "track brand mentions", "monitor competitors on social", "what keywords should I watch", "Hootsuite setup", "configure Brandwatch streams", "what should I track on Twitter/Reddit/etc."

**NOT** the right tool for: scraping actual mention data (use Hootsuite/Brandwatch directly), sentiment scoring (different skill), or content calendar planning (use `social-media-content-calendar`).

## The 6 categories (from m3_03 "Social listening strategies")

Every complete keyword list covers these 6 buckets:

1. **Brand & product names** — exact + variations + common misspellings
2. **Slogans & taglines** — current + retired (people still quote old ones)
3. **Key people** — founder, CEO, public-facing employees (they get @mentioned)
4. **Industry buzzwords & topics** — terms prospects use when searching
5. **Hashtags** — branded (#YourBrand) + community + trending-in-industry
6. **Competitors** — their names + misspellings (to catch head-to-head discussions)

Plus 3 extensions:
- **Negative-context modifiers** — "complaint", "problem", "vs", "alternative to" — catches dissatisfied mentions even when brand name isn't tagged
- **Multi-language variants** — if brand operates internationally
- **Product category terms** — generic terms your product solves for ("project management" for Asana)

## Workflow

1. **Collect inputs** concisely:
   - Brand name + 3-5 main products
   - Founder/CEO name + 1-3 public-facing employees
   - Current slogan(s) + any retired ones you remember
   - 3-5 direct competitors
   - Industry (for buzzword generation)
   - Languages to monitor (default: user's primary language + English)

2. **Generate misspellings** — run `scripts/misspell.py brand_name` OR apply patterns from `references/misspelling-patterns.md`:
   - Keyboard-adjacent swaps (e.g., "Asana" → "Aasana", "Asna", "Sana")
   - Doubled/dropped letters
   - Phonetic variants
   - Common abbreviations

3. **Build category lists** — fill all 6 categories using `templates/keyword-brainstorm.md` mental checklist

4. **Generate tool-specific queries** — output as:
   - CSV (one keyword per row, with category column)
   - Hootsuite stream queries (boolean syntax)
   - Brandwatch query (nested boolean with AND/OR/NOT)
   - Sprout Social rule sets
   - Mention alert queries

5. **Output** — single markdown response with:
   - Full CSV block (copy-paste into spreadsheet)
   - Tool-specific query blocks (paste into each listening tool)
   - Recommended review cadence (daily scan for 10 min, weekly deep-dive)

## Running the script

```bash
python3 scripts/misspell.py "Brand Name"
# → prints common misspellings based on keyboard adjacency + phonetic rules
```

Standalone — no dependencies.

## Tool syntax differences (why we need different outputs)

- **Hootsuite streams**: simple keyword-match, 1 keyword per stream, no boolean
- **Brandwatch**: full boolean (AND/OR/NOT, proximity operators)
- **Sprout Social**: rules + exact-match phrases, separate negative/positive filters
- **Mention**: keyword + optional AND/OR + language filter
- **Brand24**: keyword + context filters

One keyword list, 4-5 different query formats. Skill generates them all.

## Output structure

```markdown
# Social Listening Keyword List — {Brand}

## Summary
- Total keywords: N
- Categories covered: 6
- Recommended daily scan time: 10-15 min

## Full keyword list (CSV)
```csv
category,keyword,notes
brand,BrandName,exact name
brand,Brand Name,spaced variant
brand,brandname.com,domain mention
misspelling,Barnd Name,transposition
...
```

## Hootsuite stream queries
...

## Brandwatch query (copy-paste)
```
((BrandName OR "Brand Name" OR brandname.com)
 OR (Barnd* OR Brnad* OR "Brand Nmae"))
AND NOT ("spam" OR "test")
```

## Sprout Social setup
...

## Review cadence
- **Daily (10 min):** scan overnight mentions, respond to negative sentiment within 4h
- **Weekly (45 min):** deep-dive by category, sentiment breakdown, competitive landscape
- **Monthly (90 min):** refine keyword list, remove noise, add trending terms
```

## References

- `references/misspelling-patterns.md` — keyboard adjacency rules + phonetic substitutions for Latin, Cyrillic, Vietnamese
- `references/tool-syntax.md` — boolean query syntax per listening tool
- `references/category-examples.md` — real-world examples per category (what good looks like)

## Why comprehensive coverage matters

The biggest listening failure mode: **missing mentions because the keyword wasn't in the list**. Users call your brand "ur brand" on Reddit, misspell it on Twitter, quote old slogans — if you only track the exact brand name, you miss 30-50% of actual mentions.

The 6-category + misspellings approach is more setup work upfront (30 min vs 5 min) but catches an order of magnitude more relevant mentions.

## Common pitfalls

- **Missing the industry buzzwords** — you want to be in conversations where people discuss the problem you solve, even before mentioning a brand
- **Over-listing competitors** — 15 competitors = noise. Pick 3-5 direct rivals.
- **Never updating** — quarterly keyword review is mandatory. Trends shift.
- **Tracking without acting** — listening without response triage = wasted effort. Pair with response SLAs (reply to negative sentiment within 4 hours).
