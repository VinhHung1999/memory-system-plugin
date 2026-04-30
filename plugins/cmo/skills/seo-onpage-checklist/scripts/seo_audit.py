#!/usr/bin/env python3
"""
SEO on-page audit tool.
Usage:
    python3 seo_audit.py https://example.com
    python3 seo_audit.py /path/to/page.html

Runs 10 on-page SEO checks and prints a scored markdown report.
Based on Google's Digital Marketing certificate (Course 2).
"""
import sys
import os
import re
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: missing dependencies. Install with:")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)


DEFAULT_TITLES = {"untitled", "new page 1", "home", "home page", "document", ""}
UA = "Mozilla/5.0 (compatible; SEOAuditor/1.0; +https://example.com/bot)"


def load_html(target):
    """Return (html_text, base_url_or_None)."""
    if target.startswith(("http://", "https://")):
        r = requests.get(target, headers={"User-Agent": UA}, timeout=15)
        r.raise_for_status()
        return r.text, target
    if not os.path.exists(target):
        raise FileNotFoundError(f"File not found: {target}")
    with open(target, "r", encoding="utf-8", errors="ignore") as f:
        return f.read(), None


def check_title(soup):
    t = soup.find("title")
    if not t or not t.text.strip():
        return "FAIL", "No <title> tag. Add a descriptive 30-60 char title including target keyword."
    text = t.text.strip()
    if text.lower() in DEFAULT_TITLES:
        return "FAIL", f'Title is a default placeholder ("{text}"). Rewrite with real page content + keyword.'
    if len(text) < 10:
        return "FAIL", f"Title too short ({len(text)} chars). Aim 30-60 chars."
    if len(text) > 60:
        return "WARN", f"Title {len(text)} chars — may truncate in SERP. Shorten to ≤60."
    return "PASS", f"Title: '{text}' ({len(text)} chars)"


def check_meta_description(soup):
    m = soup.find("meta", attrs={"name": "description"})
    if not m or not m.get("content", "").strip():
        return "FAIL", "No meta description. Add 120-160 char summary with CTA language + keyword."
    content = m["content"].strip()
    n = len(content)
    if n < 50:
        return "FAIL", f"Meta description too short ({n} chars). Target 120-160."
    if n > 160:
        return "WARN", f"Meta description {n} chars — may truncate in SERP. Trim to ≤160."
    return "PASS", f"Meta description: {n} chars"


def check_h1(soup):
    h1s = soup.find_all("h1")
    if not h1s:
        return "FAIL", "No <h1> tag. Add one descriptive H1 that summarizes page topic."
    if len(h1s) > 1:
        return "WARN", f"Found {len(h1s)} <h1> tags. Use exactly one H1 per page."
    text = h1s[0].get_text(strip=True)
    if not text:
        return "FAIL", "Empty <h1>. Add descriptive text."
    return "PASS", f'H1: "{text[:80]}"'


def check_heading_hierarchy(soup):
    headings = []
    for level in range(1, 7):
        for h in soup.find_all(f"h{level}"):
            headings.append(level)
    if not headings:
        return "FAIL", "No headings at all. Structure content with H1/H2/H3."
    # Check no level is skipped going down
    issues = []
    prev = headings[0]
    for level in headings[1:]:
        if level > prev + 1:
            issues.append(f"jumped H{prev}→H{level}")
        prev = level
    if issues:
        return "WARN", f"Heading level skips detected ({', '.join(issues[:3])}). Use sequential H1→H2→H3."
    return "PASS", f"{len(headings)} headings in sequential hierarchy"


def check_images(soup):
    imgs = soup.find_all("img")
    if not imgs:
        return "PASS", "No images on page (nothing to audit)."
    missing_alt = [i for i in imgs if not i.get("alt", "").strip()]
    generic_filenames = []
    for i in imgs:
        src = i.get("src", "")
        name = os.path.basename(urlparse(src).path)
        if re.match(r"^(img|image|dsc|photo|pic)[-_]?\d*\.(jpe?g|png|gif|webp)$", name, re.I):
            generic_filenames.append(name)
    issues = []
    if missing_alt:
        issues.append(f"{len(missing_alt)}/{len(imgs)} missing alt text")
    if generic_filenames:
        issues.append(f"{len(generic_filenames)} generic filenames (e.g., {generic_filenames[0]})")
    if issues:
        return "FAIL", "; ".join(issues) + ". Add descriptive alt + rename files (e.g., red-cactus-pot.jpg)."
    return "PASS", f"All {len(imgs)} images have alt text + descriptive filenames"


def check_structured_data(soup):
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    if not scripts:
        return "FAIL", "No JSON-LD structured data. Add Schema.org markup (Product, Article, FAQ, etc.) to qualify for rich results."
    # Basic sanity: must contain @context with schema.org
    valid_count = 0
    for s in scripts:
        txt = s.string or ""
        if "schema.org" in txt.lower():
            valid_count += 1
    if valid_count == 0:
        return "WARN", f"Found {len(scripts)} JSON-LD block(s) but none reference schema.org."
    return "PASS", f"{valid_count} Schema.org JSON-LD block(s) present"


def check_canonical(soup):
    c = soup.find("link", rel="canonical")
    if not c or not c.get("href"):
        return "WARN", "No canonical <link>. Add rel='canonical' to prevent duplicate-content issues."
    return "PASS", f"Canonical: {c['href']}"


def check_viewport(soup):
    v = soup.find("meta", attrs={"name": "viewport"})
    if not v or "width=device-width" not in (v.get("content", "") or ""):
        return "FAIL", "Missing/invalid viewport meta. Add <meta name='viewport' content='width=device-width, initial-scale=1'>."
    return "PASS", "Viewport meta set for mobile"


def check_internal_links(soup, base_url):
    links = soup.find_all("a", href=True)
    if not links:
        return "WARN", "No <a href> links at all. Add internal links to help crawlers discover related pages."
    if base_url:
        host = urlparse(base_url).netloc
        internal = [a for a in links if urlparse(urljoin(base_url, a["href"])).netloc in ("", host)]
    else:
        # Heuristic: relative links count as internal
        internal = [a for a in links if not a["href"].startswith(("http://", "https://"))]
    if len(internal) < 3:
        return "WARN", f"Only {len(internal)} internal links. Add 3-10 contextual internal links for discoverability."
    return "PASS", f"{len(internal)} internal links"


def check_lang(soup):
    html = soup.find("html")
    if not html or not html.get("lang"):
        return "WARN", "Missing <html lang='...'>. Set page language (e.g., 'en', 'vi') for accessibility + international SEO."
    return "PASS", f"Language: {html.get('lang')}"


CHECKS = [
    ("Title tag", check_title),
    ("Meta description", check_meta_description),
    ("H1 tag", check_h1),
    ("Heading hierarchy", check_heading_hierarchy),
    ("Images (alt + filenames)", check_images),
    ("Structured data (JSON-LD)", check_structured_data),
    ("Canonical tag", check_canonical),
    ("Viewport meta", check_viewport),
    ("Internal links", check_internal_links),
    ("HTML lang attribute", check_lang),
]

STATUS_ICON = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}


def audit(target):
    html, base = load_html(target)
    soup = BeautifulSoup(html, "html.parser")

    results = []
    for name, fn in CHECKS:
        try:
            if fn is check_internal_links:
                status, detail = fn(soup, base)
            else:
                status, detail = fn(soup)
        except Exception as e:
            status, detail = "FAIL", f"Check raised: {e}"
        results.append((name, status, detail))

    passes = sum(1 for _, s, _ in results if s == "PASS")
    warns = sum(1 for _, s, _ in results if s == "WARN")
    fails = sum(1 for _, s, _ in results if s == "FAIL")
    total = len(results)
    score = round(passes / total * 100)

    out = []
    out.append(f"# SEO On-page Audit: {target}\n")
    out.append(f"**Score: {score}/100** — {passes} PASS, {warns} WARN, {fails} FAIL\n")
    out.append("## Results\n")
    out.append("| Check | Status | Detail |")
    out.append("|---|---|---|")
    for name, status, detail in results:
        icon = STATUS_ICON[status]
        out.append(f"| {name} | {icon} {status} | {detail} |")
    out.append("")

    critical = [r for r in results if r[1] == "FAIL"]
    if critical:
        out.append("## Top fixes (in priority order)\n")
        for i, (name, _, detail) in enumerate(critical, 1):
            out.append(f"{i}. **{name}** — {detail}")
        out.append("")

    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 seo_audit.py <url-or-file>")
        sys.exit(1)
    target = sys.argv[1]
    try:
        print(audit(target))
    except requests.RequestException as e:
        print(f"ERROR fetching URL: {e}")
        sys.exit(2)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
