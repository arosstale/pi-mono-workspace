#!/bin/bash
# Batch scraping script

cd "$(dirname "$0")"

echo "🚀 BATCH SCRAPING — All Cities & Sectors"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
date
echo ""

# Phase 1: Milano (all sectors)
echo "📍 PHASE 1: MILANO — All Sectors"
echo ""

for sector in idraulici elettricisti fabbri condizionamento; do
    echo "🏢 Scraping: Milano - $sector"
    python3 scrape_leads.py "Milano" "$sector" 10
    sleep 10
done

# Phase 2: Monza, Como, Brescia (key sectors)
echo ""
echo "📍 PHASE 2: MONZA, COMO, BRESCIA — Key Sectors"
echo ""

for city in Monza Como Brescia; do
    for sector in idraulici elettricisti fabbri; do
        echo "🏢 Scraping: $city - $sector"
        python3 scrape_leads.py "$city" "$sector" 10
        sleep 10
    done
done

echo ""
echo "✅ BATCH SCRAPING COMPLETE!"
echo ""
echo "📊 Check results in: $(pwd)"
ls -lh *.json | tail -10

