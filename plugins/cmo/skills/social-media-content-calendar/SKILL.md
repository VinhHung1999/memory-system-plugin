---
name: social-media-content-calendar
description: Generate a 30-day social media content calendar tailored to brand voice + audience + platforms. Allocates posts across 5 content buckets (entertaining, educational, inspirational, conversational, promotional), applies platform-specific frequency + format rules (Twitter/X, Instagram, Facebook, LinkedIn, TikTok, YouTube), drafts per-platform copy with brand voice, and maps core pieces to repurposed derivatives. Output is a CSV calendar + summary markdown ready to schedule in Buffer/Hootsuite/Later. Use this skill whenever the user wants to plan social media posts, build a content calendar, schedule content for a month, or needs a posting plan for a campaign — even if they don't use the word "calendar".
---

# Social Media Content Calendar Generator

Takes inputs about the brand and produces a 30-day multi-platform posting plan. Built on Google's Digital Marketing certificate Course 3 "From Likes to Leads" — the 5 pillars framework + 5 content buckets + platform rules.

## When this triggers

User wants to plan social media posts ahead of time. Phrasings: "make content calendar", "plan next month's social", "Instagram schedule", "content plan for product launch", "what should I post", "need 30 days of content".

**NOT** the right tool for: one-off single post drafts (just write directly), paid social ad campaigns (different skill), influencer partnerships, analytics/reporting (use `email-metrics-analyzer` analog for social when built).

## Workflow

1. **Collect inputs** — ask concisely for whatever's missing:
   - **Brand name + voice** (3-5 adjectives: "playful, confident, data-driven")
   - **Target audience** (1-2 sentences: who they are, what they care about)
   - **Platforms** (pick from: Twitter/X, Instagram, Facebook, LinkedIn, TikTok, YouTube)
   - **Posting frequency per platform** (e.g., IG 1x/day, Twitter 3x/day, LinkedIn 3x/week)
   - **Campaign theme** (optional: launch, holiday, seasonal)
   - **Start date** (default: today)

2. **Set content mix** — default 5-bucket allocation (user can override):
   - 30% Educational (tips, how-to, insights)
   - 25% Entertaining (memes, BTS, humor)
   - 20% Inspirational (quotes, customer stories, mission)
   - 15% Conversational (questions, polls, AMA prompts)
   - 10% Promotional (product features, offers, CTAs)

3. **Apply platform rules** — from `references/platform-rules.md`:
   - Twitter: 3-10 posts/day, chronological, 280 chars, hashtag light (1-2)
   - Instagram: 1-2 posts/day, visual-first, captions 150+ chars, 3-5 hashtags
   - Facebook: 1x/day, longer captions OK, link previews
   - LinkedIn: 3-5/week, weekday mornings, professional voice, 1200+ chars
   - TikTok: 1-3/day, trending audio, vertical video
   - YouTube: 1/week long-form or 1/day Shorts

4. **Generate calendar** — run `scripts/calendar_gen.py` or compose inline. For each slot:
   - Pick content bucket per mix %
   - Match topic to brand/audience
   - Draft copy matching brand voice + platform format
   - Suggest hashtags (per platform rules)
   - Suggest image/video brief
   - Mark core-vs-derivative (repurposed pieces linked)

5. **Output**:
   - `calendar.csv` (date, platform, bucket, draft_copy, hashtags, media_brief, is_derivative)
   - `summary.md` (overview: mix breakdown, core pieces + derivatives, week-by-week)

## Why this approach

Most content calendars fail because they're "topic lists" not "posting plans" — miss voice consistency, platform specifics, and repurposing. The 5-bucket mix prevents the all-promotional trap (which kills engagement and invites unfollows). Platform rules prevent wasted effort (long LinkedIn copy on Twitter = ignored).

Repurposing is the productivity lever — every core piece (blog, video, major announcement) should spawn 3-5 platform-native derivatives. The calendar marks which is which so you batch-produce core content and efficiently derive the rest.

## Content bucket definitions (from m2_05)

| Bucket | Purpose | Examples |
|---|---|---|
| **Educational** | Teach audience something useful | "3 tips for X", tutorial, data insight |
| **Entertaining** | Humor, personality, community | Meme, BTS photo, team joke, TGIF |
| **Inspirational** | Aspiration, mission, social proof | Customer success, quote, milestone |
| **Conversational** | Two-way, driver of comments | Question, poll, "this or that", AMA |
| **Promotional** | Product/offer/CTA | Launch, sale, feature highlight |

The default mix errors toward engagement (85% non-promo). For e-commerce with frequent sales, user may want 20%+ promotional — that's fine, but warn about unfollow risk if >30%.

## Repurposing logic

Core → derivatives:
- **Blog post** → Twitter thread (5 tweets) + IG carousel (5 slides) + LinkedIn native article + IG reel (15s highlight) + email newsletter link
- **Long YouTube video** → 3 Shorts + IG carousel + Twitter thread + LinkedIn post
- **Customer case study** → IG reel + LinkedIn post + Twitter quote card + newsletter feature

Mark derivatives in calendar so user batches core content production.

## Running the script

```bash
python3 scripts/calendar_gen.py --config /path/to/config.json > calendar.csv
```

Config JSON structure:
```json
{
  "brand_name": "PlantCo",
  "voice": ["friendly", "educational", "earnest"],
  "audience": "home gardeners 25-45",
  "platforms": {
    "instagram": 30,
    "twitter": 60,
    "linkedin": 12
  },
  "start_date": "2026-05-01",
  "days": 30,
  "mix": {"educational": 0.35, "entertaining": 0.25, "inspirational": 0.15, "conversational": 0.15, "promotional": 0.10}
}
```

Script outputs a CSV. Skill then drafts copy for each row inline (LLM generation — script provides scaffolding, LLM does creative fill).

## References

- `references/platform-rules.md` — frequency, format, tone, hashtag rules per platform
- `references/bucket-playbook.md` — 20 prompt patterns per bucket (educational ideas, conversational starters, etc.)
- `references/repurposing-tree.md` — core-to-derivative mapping with examples

## Output philosophy

The calendar should be immediately usable — paste into Buffer/Hootsuite/Later and schedule. That means:
- Real copy (not placeholders)
- Realistic post counts (respect platform frequencies)
- Repurposing marked so user knows production workload (3 core + 15 derivatives < 18 originals)
- Voice consistency across platforms but format/length platform-appropriate

Don't output a "content strategy document" — that's for Course 3's strategy-planning skill (if built). This skill's job is the concrete 30-day plan.
