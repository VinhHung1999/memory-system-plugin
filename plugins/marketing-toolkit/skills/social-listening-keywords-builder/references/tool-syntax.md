# Listening Tool Query Syntax

## Hootsuite Streams

**Simple**: One keyword per stream. No boolean — each stream filters by single keyword or hashtag.

Example streams for "PlantCo":
- Stream 1: `PlantCo`
- Stream 2: `#plantco`
- Stream 3: `plantco.com`
- Stream 4: `"Plant Co"`
- Stream 5 (misspelling): `Plantoc OR Plnatco OR Plantco` (free text)

**Pros:** simple, fast setup
**Cons:** can't exclude noise, no boolean precision

## Sprout Social

Supports keyword rules with include/exclude filters.

**Example:**
```
Listening topic: PlantCo
Include any of:
  - PlantCo
  - Plant Co
  - #plantco
  - @plantco
Exclude any of:
  - "test"
  - "spam"
Language: English, Vietnamese
```

**Pros:** good exclusions, topic-based organization
**Cons:** limited to list-of-keywords, no proximity operators

## Brandwatch (most powerful)

Full boolean with AND / OR / NOT, proximity operators, regex.

**Example:**
```
((PlantCo OR "Plant Co" OR plantco.com)
 OR ("Plant Co" NEAR/5 (shop OR store OR reviews)))
AND NOT ("Plant Co Ltd" OR "test")
AND language:en
```

**Operators:**
- `AND`, `OR`, `NOT` (all caps)
- `"exact phrase"` (double quotes)
- `()` grouping
- `NEAR/N` — within N words
- `*` wildcard
- `language:`, `country:`, `site:` field restrictions

**Pros:** most expressive, catches indirect mentions
**Cons:** expensive, learning curve

## Mention

Simpler boolean with AND / OR.

**Example:**
```
PlantCo OR "Plant Co" OR plantco.com
AND NOT spam
Languages: English
```

**Pros:** email alerts, good for small teams
**Cons:** less powerful than Brandwatch

## Brand24

Similar to Mention. Boolean with required + excluded keywords.

**Example:**
```
Required: PlantCo
Optional: "Plant Co", plantco.com, @plantco
Excluded: "test", "Plant Co Ltd"
```

## Twitter/X advanced search (free option)

Search query syntax:
```
(PlantCo OR "Plant Co") -filter:retweets since:2026-04-01
```
- `-` excludes
- `filter:retweets` / `-filter:retweets`
- `since:YYYY-MM-DD`, `until:YYYY-MM-DD`
- `from:@user`, `to:@user`
- `min_replies:N`, `min_retweets:N`, `min_faves:N`

**Pros:** free, real-time
**Cons:** Twitter-only, no persistent alerts

## Reddit search

```
site:reddit.com PlantCo
```
Via Google. Or use Reddit's native search + subscribe to subreddits.

Reddit also has **Reddit Keyword Monitor Pro** and similar free tools.

## Google Alerts (free basic option)

```
"PlantCo" OR "Plant Co" -site:plantco.com
```
- Free
- Email-delivered
- Limited to Google's crawl (slow for social)
- Better for news/blogs than Twitter/Reddit

## Recommended tool tiers

| Budget | Tool | Use case |
|---|---|---|
| $0 | Google Alerts + Twitter advanced search + Reddit | Solo founder, small brand |
| $20-100/mo | Mention, Brand24 | Small team, basic monitoring |
| $200-500/mo | Sprout Social, Hootsuite Insights | Mid-size team, multi-channel |
| $500+/mo | Brandwatch, Talkwalker, Meltwater | Enterprise, crisis monitoring, deep analytics |

## Output in each format

When generating the skill's output, provide ALL 4 common formats:
1. CSV (universal — paste anywhere)
2. Hootsuite streams (list of individual streams)
3. Brandwatch boolean (single powerful query)
4. Sprout rule (include/exclude lists)

User picks their tool and copies the matching block.
