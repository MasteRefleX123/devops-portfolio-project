#!/bin/bash

set -euo pipefail

# Load environment variables
if [ -f .env ]; then
    # shellcheck disable=SC2046
    export $(cat .env | grep -v '^#' | xargs)
fi

# GitHub configuration (must be set in .env)
GITHUB_USER="${GITHUB_USER:-MasteRefleX123}"
GITHUB_REPO="${GITHUB_REPO:-devops-portfolio-project}"
API="https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}"

if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "❌ GITHUB_TOKEN not set. Please set it in .env file"
    exit 1
fi

echo "🔄 Updating GitHub Webhook..."

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"[^"]*' | grep https | cut -d'"' -f4 | head -1)

if [ -z "${NGROK_URL}" ]; then
    echo "❌ Ngrok URL not found. Make sure ngrok is running."
    exit 1
fi

WEBHOOK_URL="${NGROK_URL}/github-webhook/"
echo "📍 New webhook URL: ${WEBHOOK_URL}"

AUTH_HEADER="Authorization: token ${GITHUB_TOKEN}"
ACCEPT_HEADER="Accept: application/vnd.github+json"

# Find existing webhook by URL
echo "🔎 Checking existing webhooks..."
HOOKS_JSON=$(curl -s -H "$AUTH_HEADER" -H "$ACCEPT_HEADER" "${API}/hooks")
HOOK_ID=$(echo "$HOOKS_JSON" | grep -n '"id"' | head -1 | sed -E 's/.*: ([0-9]+).*/\1/' || true)
MATCHING_ID=$(echo "$HOOKS_JSON" | grep -B3 -A20 '"url"' | cat >/dev/null; echo "")

# Robust matching by config.url
MATCHING_ID=$(echo "$HOOKS_JSON" | awk -v url="$WEBHOOK_URL" '
  /\{/{inobj=1; buf=""}
  {if(inobj) buf=buf $0 "\n"}
  /\}/{if(inobj){inobj=0; if(buf ~ /"config"/ && buf ~ /"url"/ && buf ~ url){print buf}}}
' | grep '"id"' | head -1 | sed -E 's/.*"id"\s*:\s*([0-9]+).*/\1/' || true)

if [ -n "$MATCHING_ID" ]; then
  echo "♻️  Updating existing webhook ID: $MATCHING_ID"
  curl -s -X PATCH -H "$AUTH_HEADER" -H "$ACCEPT_HEADER" \
    -d "{\n      \"config\": {\n        \"url\": \"${WEBHOOK_URL}\",\n        \"content_type\": \"json\",\n        \"insecure_ssl\": \"0\"\n      },\n      \"events\": [\"push\", \"pull_request\"],\n      \"active\": true\n    }" \
    "${API}/hooks/${MATCHING_ID}" >/dev/null
else
  echo "➕ Creating new webhook"
  curl -s -X POST -H "$AUTH_HEADER" -H "$ACCEPT_HEADER" \
    -d "{\n      \"name\": \"web\",\n      \"config\": {\n        \"url\": \"${WEBHOOK_URL}\",\n        \"content_type\": \"json\",\n        \"insecure_ssl\": \"0\"\n      },\n      \"events\": [\"push\", \"pull_request\"],\n      \"active\": true\n    }" \
    "${API}/hooks" >/dev/null
fi

echo "✅ Webhook configuration complete"
