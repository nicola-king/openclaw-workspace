#!/bin/bash
# Taiyi Daily Briefing - 每日 08:00 自动发送
# Created: 2026-03-28 13:30

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/daily-briefing-$(date +%Y%m%d).log"

echo "[$(date)] Start Daily Briefing..." >> $LOG_FILE

cd "$WORKSPACE/skills/taiyi"
python3 daily-briefing.py >> "$LOG_FILE" 2>&1

echo "[$(date)] ✓ Daily Briefing completed" >> $LOG_FILE
