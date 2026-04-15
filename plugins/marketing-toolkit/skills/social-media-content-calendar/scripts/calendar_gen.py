#!/usr/bin/env python3
"""
Generate a 30-day social media content calendar scaffold.

This script produces the SKELETON — dates, platforms, buckets, counts.
The LLM fills in actual copy per slot using the generated CSV as structure.

Usage:
    python3 calendar_gen.py --config config.json
    python3 calendar_gen.py --brand "PlantCo" --platforms "instagram:30,twitter:60,linkedin:12" --days 30

Config JSON:
    {
      "brand_name": "PlantCo",
      "voice": ["friendly", "educational"],
      "audience": "home gardeners",
      "platforms": {"instagram": 30, "twitter": 60, "linkedin": 12},
      "start_date": "2026-05-01",
      "days": 30,
      "mix": {"educational": 0.30, "entertaining": 0.25, "inspirational": 0.20, "conversational": 0.15, "promotional": 0.10}
    }

    platform values = posts per 30 days (e.g., 30 = 1/day, 60 = 2/day)
"""
import sys
import csv
import json
import datetime
import argparse
import random
import math


DEFAULT_MIX = {
    "educational": 0.30,
    "entertaining": 0.25,
    "inspirational": 0.20,
    "conversational": 0.15,
    "promotional": 0.10,
}


# Posts per 30 days defaults if not specified
DEFAULT_FREQS = {
    "twitter": 90,  # 3/day
    "instagram": 30,  # 1/day
    "facebook": 30,
    "linkedin": 12,  # ~3/week
    "tiktok": 30,
    "youtube": 4,  # 1/week
}


# Best posting hours per platform (local time, 24h)
POST_HOURS = {
    "twitter": [8, 12, 17, 20],
    "instagram": [11, 14, 19],
    "facebook": [9, 13, 15],
    "linkedin": [7, 11, 17],
    "tiktok": [9, 19, 22],
    "youtube": [14],
}


def pick_bucket(mix, rng):
    """Weighted random choice from mix."""
    buckets = list(mix.keys())
    weights = list(mix.values())
    return rng.choices(buckets, weights=weights, k=1)[0]


def generate_calendar(config):
    brand = config.get("brand_name", "Brand")
    voice = config.get("voice", ["friendly", "professional"])
    audience = config.get("audience", "general audience")
    platforms = config.get("platforms", {"instagram": 30})
    start_date_str = config.get("start_date") or datetime.date.today().isoformat()
    start_date = datetime.date.fromisoformat(start_date_str)
    days = config.get("days", 30)
    mix = {**DEFAULT_MIX, **config.get("mix", {})}
    seed = config.get("seed", 42)
    rng = random.Random(seed)

    rows = []
    # For each platform, distribute its N posts across the N days
    for platform, total_posts in platforms.items():
        hours = POST_HOURS.get(platform, [10])
        posts_per_day = total_posts / days
        # Distribute via cumulative rounding to avoid drift
        accum = 0.0
        for day_idx in range(days):
            date = start_date + datetime.timedelta(days=day_idx)
            accum += posts_per_day
            n_today = int(accum)
            accum -= n_today
            for slot in range(n_today):
                hour = hours[slot % len(hours)]
                bucket = pick_bucket(mix, rng)
                rows.append({
                    "date": date.isoformat(),
                    "time": f"{hour:02d}:00",
                    "platform": platform,
                    "bucket": bucket,
                    "copy": f"[{bucket.upper()}] — write {platform} post about {audience} interests in {brand} voice ({'/'.join(voice)})",
                    "hashtags": suggest_hashtags(platform, bucket, brand),
                    "media_brief": media_brief(platform, bucket),
                    "is_derivative": False,
                    "derivative_of": "",
                })

    # Sort by date/time/platform
    rows.sort(key=lambda r: (r["date"], r["time"], r["platform"]))
    return rows, mix


def suggest_hashtags(platform, bucket, brand):
    brand_tag = f"#{brand.replace(' ', '').lower()}"
    bucket_tags = {
        "educational": "#tips #learn",
        "entertaining": "#BTS #fun",
        "inspirational": "#motivation #story",
        "conversational": "#community #question",
        "promotional": "#new #offer",
    }
    counts = {"twitter": 2, "instagram": 5, "facebook": 2, "linkedin": 3, "tiktok": 4, "youtube": 3}
    n = counts.get(platform, 3)
    # Simple heuristic; LLM can replace with brand-specific
    tags = [brand_tag] + bucket_tags.get(bucket, "").split()
    return " ".join(tags[:n])


def media_brief(platform, bucket):
    briefs = {
        "instagram": {
            "educational": "Carousel: 5 slides, bold headline each, minimal text",
            "entertaining": "Single image or reel; candid/BTS vibe; 15-30s if reel",
            "inspirational": "Customer photo or quote card on branded background",
            "conversational": "Bold text on solid color; question in big type",
            "promotional": "Product hero shot, clean background, CTA sticker",
        },
        "twitter": {
            "educational": "Short thread (3-5 tweets) or single tweet with image",
            "entertaining": "Text-only or with gif/meme",
            "inspirational": "Quote with simple image",
            "conversational": "Text-only, end with question mark",
            "promotional": "Image with CTA link in reply",
        },
        "linkedin": {
            "educational": "1200+ char post, optionally with PDF carousel",
            "entertaining": "Rare — use team milestone or behind-scenes reflection",
            "inspirational": "Customer success story, 800-1500 chars",
            "conversational": "Ask a poll (native LinkedIn poll)",
            "promotional": "Announcement post with branded image",
        },
        "tiktok": {
            "educational": "15-30s vertical video, hook in first 3s, text overlay",
            "entertaining": "15-60s, trending audio, quick cuts",
            "inspirational": "30-60s, mix of footage + text overlay + emotional audio",
            "conversational": "Green-screen video or duet invitation",
            "promotional": "30-60s product demo, clear CTA in caption",
        },
    }
    return briefs.get(platform, {}).get(bucket, f"{platform} {bucket} post media")


def mark_derivatives(rows):
    """Heuristic: for every 'educational' core piece on a long-form platform (LinkedIn, YouTube, IG carousel),
    mark 2-3 subsequent posts in next 3 days as derivatives.
    Simplified: just flag 30% of non-long-form educational as derivative."""
    long_platforms = {"linkedin", "youtube"}
    cores = [r for r in rows if r["platform"] in long_platforms and r["bucket"] == "educational"]
    for i, core in enumerate(cores):
        # Flag next 3 posts on any platform as derivatives
        core_idx = rows.index(core)
        derived = 0
        for r in rows[core_idx + 1:]:
            if derived >= 3: break
            if r["platform"] != core["platform"]:
                r["is_derivative"] = True
                r["derivative_of"] = f"{core['date']} {core['platform']} (educational)"
                derived += 1
    return rows


def write_csv(rows, path):
    if not rows: return
    keys = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def summary(rows, mix):
    from collections import Counter
    n = len(rows)
    platform_counts = Counter(r["platform"] for r in rows)
    bucket_counts = Counter(r["bucket"] for r in rows)
    derivative_n = sum(1 for r in rows if r["is_derivative"])
    out = []
    out.append(f"# Content Calendar Summary — {n} posts\n")
    out.append("## Platform distribution")
    for p, c in platform_counts.most_common():
        out.append(f"- {p}: {c} posts")
    out.append("\n## Bucket mix (actual vs target)")
    for b, target in mix.items():
        actual = bucket_counts.get(b, 0) / n if n else 0
        out.append(f"- {b}: {actual*100:.0f}% actual / {target*100:.0f}% target")
    out.append(f"\n## Repurposing")
    out.append(f"- Core pieces: {n - derivative_n}")
    out.append(f"- Derivatives: {derivative_n} ({derivative_n/n*100:.0f}%)")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", help="JSON config file")
    p.add_argument("--out", default="-", help="Output CSV path (default stdout)")
    p.add_argument("--summary", help="Optional summary markdown path")
    args = p.parse_args()

    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        config = {}

    rows, mix = generate_calendar(config)
    rows = mark_derivatives(rows)

    if args.out == "-":
        import io
        sio = io.StringIO()
        w = csv.DictWriter(sio, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
        print(sio.getvalue())
    else:
        write_csv(rows, args.out)
        print(f"Wrote {len(rows)} rows to {args.out}")

    if args.summary:
        with open(args.summary, "w") as f:
            f.write(summary(rows, mix))
        print(f"Wrote summary to {args.summary}")
    else:
        print("\n---SUMMARY---\n" + summary(rows, mix))


if __name__ == "__main__":
    main()
