# Default Segmentation

From Course 4 Module 3 m3_03 "Segment your mailing list".

## 4 default segments (use unless overridden)

### 1. High-engagement
- Opened an email in last 30 days
- OR clicked a link in last 30 days
- Send: new promos, exclusive previews, ambassadors/VIP invites
- Tag: `engaged-30d`

### 2. Net-new
- Signed up in last 7 days
- Has NOT completed welcome flow
- Send: welcome sequence (3-5 emails over 14 days)
- Tag: `new-7d`

### 3. Lapsed
- No open/click in 60+ days
- Has past purchase OR account
- Send: win-back sequence (2-3 emails with escalating incentive)
- Tag: `lapsed-60d`

### 4. VIP
- Top 10% of list by revenue (e-commerce) OR engagement (content)
- Send: early access, higher-quality offers, direct appreciation
- Tag: `vip`

## Custom segmentation dimensions

Combine as needed:

### Geographic
- Country, region, city, timezone
- Use for: local events, shipping offers, regional promotions, climate-based products ("Winter collection" only to cold climates)

### Demographic
- Age, gender, income bracket, occupation, education
- Use for: product relevance (e.g., wedding dress sale to 25-35 age)
- Source: signup form + enrichment tools (Clearbit, FullContact)

### Behavioral
- Purchase history (last-purchase date, # of purchases, LTV)
- Browse history (categories viewed, products abandoned in cart)
- Email engagement (open rate, click rate, last-open date)
- Most powerful dimension for e-commerce

### Psychographic
- Interests, values, lifestyle
- Source: opt-in preferences, survey responses, behavior inference
- Harder to collect but highest relevance

## Example: e-commerce cactus shop

| Segment | Rule | Email type |
|---|---|---|
| New subscriber | signup <= 7d ago | Welcome sequence |
| Active buyer | last purchase <= 30d | Newsletter + cross-sell |
| Engaged browser | opened >= 3 emails but 0 purchases | Promotional (soft) |
| Cart abandoner | added to cart, didn't purchase, <= 3d | Retention (reminder + small incentive) |
| Lapsed | last purchase 90-180d | Retention (win-back) |
| Dormant | 180+ days no engagement | Sunset flow |

## Output format (for Mailchimp / HubSpot / ActiveCampaign)

**Mailchimp tag syntax**:
```
Tag includes: engaged-30d
AND Date: email_opened is within last 30 days
```

**HubSpot list syntax**:
```
Filter 1: Contact property > Last email open date > is less than 30 days ago
Filter 2 (AND): Contact property > Lifetime email engagement > is more than 5
```

**SQL for self-hosted systems**:
```sql
SELECT * FROM subscribers
WHERE last_open_date >= NOW() - INTERVAL '30 days'
  AND total_revenue > (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY total_revenue) FROM subscribers)
```

## Don't

- **Over-segment** — 10+ tiny segments becomes unmanageable. Start with 3-4, add as data grows
- **Under-segment** — blasting the same message to 100K subscribers wastes ROI
- **Segment without data** — if you don't have purchase history, don't pretend (use engagement as proxy)
- **Static segments only** — always prefer dynamic (recomputed per send) over manually-tagged
