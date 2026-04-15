# OAuth Setup Walkthrough

Step-by-step for Google Cloud Console + OAuth consent + API enablement.

## Total time: 20-40 minutes (first-time)

This is the hardest part of the skill. Don't skip steps.

## Step 1: Google Cloud Project (5 min)

1. Go to **https://console.cloud.google.com/**
2. Top bar → project dropdown → **New Project**
3. Name: `marketing-dashboard` (or whatever)
4. Create → wait ~30s → switch to it

## Step 2: Enable APIs (5 min)

1. Hamburger menu → **APIs & Services** → **Library**
2. Search "Google Analytics Data API" → click → **ENABLE**
3. Back to Library → Search "Google Ads API" → click → **ENABLE**

Wait for each to activate (few seconds).

## Step 3: OAuth Consent Screen (10 min)

1. **APIs & Services** → **OAuth consent screen**
2. User Type:
   - **External** (if personal Google account)
   - Internal (if Google Workspace org account)
3. App name: `marketing-dashboard`
4. User support email: your Gmail
5. Developer contact: your Gmail
6. **SAVE AND CONTINUE**
7. Scopes screen — click **ADD OR REMOVE SCOPES**:
   - Check `analytics.readonly`
   - Check `adwords`
   - UPDATE → SAVE AND CONTINUE
8. Test users screen (ONLY IF External):
   - Click **+ADD USERS**
   - Add your own Gmail (the one you'll grant access from)
   - SAVE AND CONTINUE

## Step 4: OAuth Client ID (5 min)

1. **APIs & Services** → **Credentials**
2. **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `marketing-dashboard`
5. **CREATE**
6. Download JSON (button in the popup or next to the newly-created credential)
7. Rename to `credentials.json` and move to `~/.config/marketing-dashboard/credentials.json`

```bash
mkdir -p ~/.config/marketing-dashboard
mv ~/Downloads/client_secret_*.json ~/.config/marketing-dashboard/credentials.json
```

## Step 5: Google Ads Developer Token (10 min — SKIP if not using Ads)

1. Sign in to Google Ads (ads.google.com) as the account you want to query
2. **Tools & Settings** → **Setup** → **API Center**
3. If first time: accept Terms
4. You'll see a **Developer Token** — usually starts as "Pending" (BASIC access)
5. For BASIC access: you can query your OWN ads accounts only (sufficient for most use cases)
6. For STANDARD access: apply via form (takes 1-3 business days)

BASIC is fine to start. You'll hit rate limits at scale but enough for weekly dashboards.

## Step 6: Find Your IDs

### GA4 Property ID
1. GA4 admin (gear icon) → **Property Settings**
2. Property ID = 9-digit number (e.g., `123456789`)

### Google Ads Customer ID
1. Google Ads top-right — you'll see a 10-digit number formatted `123-456-7890`
2. Strip dashes: `1234567890` → this is your customer_id

### Google Ads Manager (MCC) Customer ID (only if using)
1. If your ads account is under a Manager account, get the MCC's customer ID
2. Most solo/SMB users DON'T have this — leave blank

## Step 7: Run Setup Script

```bash
cd ~/.claude/skills/marketing-performance-dashboard
bash scripts/setup_oauth.sh
```

This:
1. Installs Python deps
2. Opens browser for OAuth consent
3. Saves token to `~/.config/marketing-dashboard/token.json`
4. Creates `~/.config/marketing-dashboard/config.json` scaffold

## Step 8: Fill Config

Edit `~/.config/marketing-dashboard/config.json`:

```json
{
  "ga4_property_id": "123456789",
  "google_ads_customer_id": "1234567890",
  "google_ads_developer_token": "abcXYZ123...",
  "google_ads_login_customer_id": ""
}
```

Use empty string `""` for `login_customer_id` if NOT using Manager Account.

## Step 9: Test

```bash
python3 scripts/dashboard.py --days 7 --out /tmp/test_dashboard.md
cat /tmp/test_dashboard.md
```

If error, check:
- Does credentials.json exist?
- Did OAuth consent actually complete (you clicked "Allow")?
- Are your IDs correct in config.json?
- Is the account that granted OAuth the same account with access to the properties?

## Common errors

### "403 Access Denied" for GA4
- The OAuth account doesn't have access to the GA4 property
- Grant access: GA4 admin → Property Access Management → Add User

### "Developer token required" for Ads
- Fill `google_ads_developer_token` in config.json
- Must be approved (or at least "Pending BASIC")

### "Quota exceeded"
- GA4: 200 requests/hour — wait
- Ads: check developer token status (STANDARD has higher quota than BASIC)

### "Refresh token not found"
- Rerun `scripts/setup_oauth.sh`
- OAuth credentials expire after ~6 months of no use

## Privacy note

Your token is stored at `~/.config/marketing-dashboard/token.json`. It grants read access to your GA + Ads data to LOCAL scripts only. Don't share this file.

If you stop using: revoke via https://myaccount.google.com/permissions
