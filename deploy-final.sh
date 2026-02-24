#!/bin/bash

# Netlify Deploy via Git (Manual Link Method)
echo "🚀 Netlify Deploy via Git Link"
echo ""

TOKEN="nfp_rCyYJ4CycbXAPb1zQzLDT3gnn9zQEiuB6edf"
SITE_ID="1f61c929-1809-4759-9366-32ab3a3f9460"

# Try to link and deploy
echo "📦 Step 1: Attempting link..."
echo "$TOKEN" > ~/.netlifyrc

echo "📦 Step 2: Attempting deploy..."
cd /home/majinbu/pi-mono-workspace/openclaw-wrappers

# Create a fake .netlify/state.json to satisfy CLI
mkdir -p .netlify
echo '{"siteId":"'$SITE_ID'"}' > .netlify/state.json

# Try deploy with direct site ID
netlify deploy --prod --site-id=$SITE_ID --dir=. --message="Deploy" --auth=$TOKEN 2>&1 || echo "Deploy failed (expected on Node v24)"

echo ""
echo "✅ Deploy attempted"
echo ""
echo "🔗 Site URL: https://openclaw-wrappers.netlify.app"
echo ""
echo "📋 If site shows 404, do manual web deploy:"
echo "   https://app.netlify.com"
