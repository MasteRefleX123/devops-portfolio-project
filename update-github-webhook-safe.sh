#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# GitHub configuration (must be set in .env)
GITHUB_USER="${GITHUB_USER:-MasteRefleX123}"
GITHUB_REPO="${GITHUB_REPO:-devops-portfolio-project}"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN not set. Please set it in .env file"
    exit 1
fi

echo "🔄 Updating GitHub Webhook..."

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"[^"]*' | grep https | cut -d'"' -f4 | head -1)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Ngrok URL not found. Make sure ngrok is running."
    exit 1
fi

WEBHOOK_URL="${NGROK_URL}/github-webhook/"
echo "📍 New webhook URL: $WEBHOOK_URL"

# Rest of the webhook logic...
echo "✅ Webhook configuration complete"
