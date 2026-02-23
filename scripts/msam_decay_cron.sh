#!/bin/bash
# MSAM decay cycle cron script
# Run this hourly to maintain memory health

# Path to MSAM
MSAM_PATH="/home/majinbu/msam"

# Run decay cycle
cd "$MSAM_PATH"
python -m msam.remember decay >> /var/log/msam-decay.log 2>&1

# Run consolidation daily at 3 AM
HOUR=$(date +%H)
if [ "$HOUR" -eq 3 ]; then
    python -m msam.remember consolidate >> /var/log/msam-consolidate.log 2>&1
fi
