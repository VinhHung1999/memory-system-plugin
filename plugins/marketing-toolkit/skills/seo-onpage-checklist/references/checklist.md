# Full SEO On-page Checklist Reference

Reference detail for each check the audit script runs. Use when the user asks "why does this matter" or wants a fix beyond what the terse report shows.

## 1. Title tag
**What it checks:** `<title>` exists, 10-60 chars, not a default placeholder.

**Why Google cares:** Title is the strongest on-page ranking signal for the target keyword and the text shown in SERP results. Default titles ("Untitled", "Home") tell Google nothing; missing titles force Google to pick text from body content, often badly.

**Fix:**
- Include the target keyword near the start
- Include the brand name at the end (e.g., "Best Potted Cactus for Home Office — PlantCo")
- Stay under 60 chars to avoid SERP truncation

## 2. Meta description
**What it checks:** `<meta name="description">` present, 50-160 chars.

**Why Google cares:** Not a direct ranking signal since 2009, but strongly affects CTR from SERP. If missing, Google synthesizes one from the page, often awkwardly.

**Fix:**
- 120-160 chars is the sweet spot
- Include primary keyword once (bolded in SERP when it matches query)
- End with a CTA: "Shop now", "Learn more", "Read the guide"

## 3. H1 tag
**What it checks:** Exactly one `<h1>` with non-empty text.

**Why Google cares:** Confirms page topic; reinforces the title keyword.

**Fix:** One H1 per page, containing the target keyword or a close variant. Can differ from title (title optimized for SERP click, H1 for on-page reading).

## 4. Heading hierarchy
**What it checks:** Headings don't skip levels (e.g., H1 → H3 without H2).

**Why Google cares:** Hierarchy maps document structure; screen readers rely on it; topic modeling uses it.

**Fix:** Sequential nesting — H1 for page, H2 for sections, H3 for subsections.

## 5. Images (alt + filenames)
**What it checks:**
- All `<img>` have non-empty `alt` attributes
- Filenames aren't generic (`image1.jpg`, `DSC_0001.png`)

**Why Google cares:**
- Alt text is the only way image-only content is indexed (Google Images traffic)
- Alt is the accessibility fallback for screen readers and broken images
- Descriptive filenames reinforce the keyword signal

**Fix:**
- Alt describes the image content, not the filename ("red terracotta cactus pot on wooden shelf" not "image")
- Rename files before upload: `red-cactus-pot.jpg` not `IMG_1234.jpg`
- Decorative/spacer images: use `alt=""` (empty) to signal screen readers to skip

## 6. Structured data (JSON-LD)
**What it checks:** At least one `<script type="application/ld+json">` block referencing schema.org.

**Why Google cares:** Enables rich results — stars for products, recipes with ingredients, FAQ dropdowns, event date/location. A page without structured data can rank well but still loses real estate to competitors with rich results.

**Fix:** Pick the schema type matching content:
- E-commerce product → `Product` schema
- Blog post → `Article` schema
- Recipe → `Recipe` schema
- FAQ section → `FAQPage` schema
- Company home → `Organization` schema

See `schema-templates.md` for copy-paste JSON-LD examples.

## 7. Canonical tag
**What it checks:** `<link rel="canonical" href="...">` present.

**Why Google cares:** Duplicate URLs (tracking params, session IDs, trailing slashes) cause ranking signals to split across URLs. Canonical tells Google which URL is authoritative.

**Fix:** Always set canonical to the clean, preferred URL. Self-referencing canonicals on single pages are fine and recommended.

## 8. Viewport meta
**What it checks:** `<meta name="viewport" content="width=device-width, initial-scale=1">`.

**Why Google cares:** Google uses mobile-first indexing since 2019. Pages without viewport are treated as non-mobile-responsive and may be penalized in mobile rankings.

**Fix:** Always include the viewport meta in `<head>`.

## 9. Internal links
**What it checks:** At least 3 internal links on the page.

**Why Google cares:** Internal links distribute PageRank, help crawlers discover pages, and signal topical relationships. A page with no internal links may be considered orphaned.

**Fix:** Link to 3-10 related pages with descriptive anchor text (not "click here"). Link to pillar content, related products, or category pages.

## 10. HTML lang attribute
**What it checks:** `<html lang="en">` (or appropriate code) present.

**Why Google cares:** Signals the page's language to search engines and accessibility tools. Important for international SEO and hreflang alternates.

**Fix:** Add `<html lang="en">` (or `vi`, `es`, `fr`, etc.). If the site has multiple languages, each language version needs correct lang + hreflang.

## Scoring philosophy

The 100-point score is a rough signal — not a ranking predictor. A page with everything PASS can still rank poorly if content is thin, irrelevant, or links are spammy. Conversely, a page with 70/100 but strong content and backlinks can rank #1.

Use the score as a "floor check" — the minimum technical hygiene. Then focus on content quality, keyword intent match, and link-building (outside this skill's scope).
