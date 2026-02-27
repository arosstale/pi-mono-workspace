#!/bin/bash
# artale-agents/launch.sh
# One-command launch after tokens are configured

set -e

echo "🚀 Artale 3-Agent Lead System"
echo "=============================="

# Check for .env
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Copy .env.example to .env and fill in your tokens"
    exit 1
fi

# Load environment
source .env

echo ""
echo "✅ Environment loaded"

# Check critical tokens
if [ -z "$DISCORD_TOKEN" ]; then
    echo "❌ DISCORD_TOKEN missing"
    echo "Get it from: https://discord.com/developers/applications"
    exit 1
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️ TELEGRAM_BOT_TOKEN missing (optional but recommended)"
fi

echo ""
echo "📁 Checking Knowledge Base..."

# Check KB files
KB_COUNT=$(find kb/ -type f \( -name "*.md" -o -name "*.pdf" \) 2>/dev/null | wc -l)
if [ "$KB_COUNT" -eq 0 ]; then
    echo "⚠️ No KB files found. Strategist will use generic templates."
    echo "Upload files to kb/ for better results."
else
    echo "✅ Found $KB_COUNT KB files"
fi

echo ""
echo "🔧 Starting Agents..."

# Start Prospector (Discord/LinkedIn scanning)
echo "  → Prospector Agent starting..."
node agents/prospector/index.js &
PROSPECTOR_PID=$!
echo "    PID: $PROSPECTOR_PID"

# Start Strategist (RAG-powered offers)
echo "  → Strategist Agent starting..."
node agents/strategist/index.js &
STRATEGIST_PID=$!
echo "    PID: $STRATEGIST_PID"

# Start Outreach (Multi-channel messaging)
echo "  → Outreach Agent starting..."
node agents/outreach/index.js &
OUTREACH_PID=$!
echo "    PID: $OUTREACH_PID"

echo ""
echo "✅ All agents running!"
echo ""
echo "📊 Monitoring:"
echo "  - Prospector scans every 30 minutes"
echo "  - Strategist processes qualified leads"
echo "  - Outreach sends messages and tracks replies"
echo ""
echo "🔔 Notifications:"
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "  - Telegram alerts: ACTIVE"
else
    echo "  - Telegram alerts: DISABLED (set TELEGRAM_BOT_TOKEN)"
fi
echo ""
echo "📈 View dashboard:"
echo "  http://localhost:3000/dashboard"
echo ""
echo "🛑 To stop: kill $PROSPECTOR_PID $STRATEGIST_PID $OUTREACH_PID"
echo ""
echo "Platform Engineer Kelsey Hightowel"
echo "System live."