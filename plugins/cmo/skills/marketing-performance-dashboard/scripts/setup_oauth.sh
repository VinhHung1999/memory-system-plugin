#!/bin/bash
# One-time OAuth setup for Google Analytics Data API + Google Ads API.
#
# Prerequisites:
# 1. Go to https://console.cloud.google.com/
# 2. Create or pick a project
# 3. APIs & Services → Enable APIs → enable:
#    - Google Analytics Data API
#    - Google Ads API
# 4. Credentials → Create Credentials → OAuth client ID
#    Application type: Desktop app
# 5. Download the JSON file (usually named client_secret_*.json)
# 6. Place it at ~/.config/marketing-dashboard/credentials.json

set -e

CONFIG_DIR="$HOME/.config/marketing-dashboard"
CRED_FILE="$CONFIG_DIR/credentials.json"
TOKEN_FILE="$CONFIG_DIR/token.json"
CONFIG_FILE="$CONFIG_DIR/config.json"

mkdir -p "$CONFIG_DIR"

if [ ! -f "$CRED_FILE" ]; then
    echo "ERROR: credentials.json not found at $CRED_FILE"
    echo ""
    echo "Setup steps:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Create or select a project"
    echo "3. APIs & Services -> Enable APIs -> Enable:"
    echo "   - Google Analytics Data API"
    echo "   - Google Ads API"
    echo "4. APIs & Services -> OAuth consent screen -> configure (External, add your email as test user)"
    echo "5. APIs & Services -> Credentials -> Create Credentials -> OAuth client ID"
    echo "   Application type: Desktop app"
    echo "   Name: marketing-dashboard"
    echo "6. Download JSON, save as $CRED_FILE"
    echo ""
    echo "Re-run this script when done."
    exit 1
fi

# Ensure Python deps
echo "Checking Python dependencies..."
python3 -c "import google.auth, google.oauth2.credentials, google_auth_oauthlib.flow, google.analytics.data_v1beta, google.ads.googleads.client" 2>/dev/null || {
    echo "Installing required Python packages..."
    pip install --user google-analytics-data google-ads google-auth-oauthlib
}

# OAuth flow
python3 << 'PYEOF'
import os, json
from google_auth_oauthlib.flow import InstalledAppFlow

CRED = os.path.expanduser("~/.config/marketing-dashboard/credentials.json")
TOKEN = os.path.expanduser("~/.config/marketing-dashboard/token.json")

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/adwords",
]

flow = InstalledAppFlow.from_client_secrets_file(CRED, SCOPES)
creds = flow.run_local_server(port=0)
with open(TOKEN, "w") as f:
    f.write(creds.to_json())
print(f"OAuth token saved to {TOKEN}")
PYEOF

# Config (user fills IDs)
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" <<EOF
{
  "ga4_property_id": "PASTE_GA4_PROPERTY_ID_HERE",
  "google_ads_customer_id": "PASTE_ADS_CUSTOMER_ID_HERE_no_dashes",
  "google_ads_developer_token": "PASTE_DEVELOPER_TOKEN_HERE",
  "google_ads_login_customer_id": "PASTE_MANAGER_ACCOUNT_ID_IF_MCC"
}
EOF
    echo ""
    echo "Config scaffold written to $CONFIG_FILE"
    echo "Edit this file and paste your real IDs before running dashboard."
    echo ""
    echo "How to find each:"
    echo "  ga4_property_id: GA4 admin -> Property settings -> Property ID (9 digits)"
    echo "  google_ads_customer_id: Google Ads top-right (format: 123-456-7890; strip dashes)"
    echo "  google_ads_developer_token: Tools & Settings -> API Center -> Developer Token"
    echo "  google_ads_login_customer_id: only if using a Manager Account (MCC)"
fi

echo ""
echo "OAuth setup complete!"
echo "Next: run 'python3 scripts/dashboard.py --days 30 --out dashboard.md'"
