#!/bin/bash
# Polymarket 热度前 5 名天气预测数据采集
# 更新频率：每 30 分钟

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/polymarket-hot-weather-$(date +%Y%m%d).log"

echo "========================================" >> $LOG_FILE
echo "[$(date)] Start Polymarket Hot Weather Data Collection..." >> $LOG_FILE

cd "$WORKSPACE/skills/zhiji"
python3 polymarket-hot-weather.py >> $LOG_FILE 2>&1

echo "[$(date)] ✓ Polymarket hot weather data collection completed" >> $LOG_FILE
