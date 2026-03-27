#!/bin/bash
# Zhiji-E Cron Job Script

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/zhiji-$(date +%Y%m%d).log"

echo "[$(date)] Start Zhiji-E data collection..." >> $LOG_FILE

# WMO Weather Data Collection
cd "$WORKSPACE/polymarket-data/weather-models"
python3 wmo_collector.py >> "$LOG_FILE" 2>&1

# Strategy Analysis
cd "$WORKSPACE/skills/zhiji"
python3 strategy_v21.py >> "$LOG_FILE" 2>&1

echo "[$(date)] Zhiji-E task completed" >> $LOG_FILE
