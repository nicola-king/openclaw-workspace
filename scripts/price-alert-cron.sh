#!/bin/bash
# Price Alert Monitor - 每 5 分钟检查价格波动
# Created: 2026-03-28 13:30

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/price-alert-$(date +%Y%m%d).log"

echo "[$(date)] Start Price Alert Monitor..." >> $LOG_FILE

cd "$WORKSPACE/skills/zhiji"
python3 price-alert.py >> "$LOG_FILE" 2>&1

echo "[$(date)] ✓ Price Alert Monitor completed" >> $LOG_FILE
