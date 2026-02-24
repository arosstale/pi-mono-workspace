#!/bin/bash
# restart_daemon.sh - Restart the research daemon
# Part of Research Engine

RESEARCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAEMON_SCRIPT="$RESEARCH_DIR/research_daemon.py"
PID_FILE="$RESEARCH_DIR/research_daemon.pid"
LOG_FILE="$RESEARCH_DIR/research.log"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Research Engine Daemon Restart ===${NC}"
echo ""

# Kill existing process if running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Killing existing daemon (PID: $OLD_PID)${NC}"
        kill $OLD_PID
        sleep 1
    fi
    rm -f "$PID_FILE"
fi

# Start new daemon
echo -e "${BLUE}Starting daemon...${NC}"
nohup python3 "$DAEMON_SCRIPT" >> "$LOG_FILE" 2>&1 &
NEW_PID=$!

echo $NEW_PID > "$PID_FILE"

sleep 2

# Check if it's running
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Daemon started successfully (PID: $NEW_PID)${NC}"
    echo ""
    echo -e "${BLUE}Recent logs:${NC}"
    tail -5 "$LOG_FILE"
else
    echo -e "${RED}✗ Daemon failed to start${NC}"
    echo ""
    echo -e "${BLUE}Check logs: $LOG_FILE${NC}"
    cat "$LOG_FILE" | tail -20
    exit 1
fi

echo ""
echo -e "${GREEN}=== Daemon Restart Complete ===${NC}"
