#!/bin/bash
# 知几-E 定时任务脚本

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/reports/zhiji-$(date +%Y%m%d).log"

echo "[$(date)] 开始知几-E 数据采集..." >> $LOG_FILE

# 07:00 - WMO 气象数据采集
cd $WORKSPACE/polymarket-data/weather-models
python3 wmo_collector.py >> $LOG_FILE 2>&1

# 07:05 - 策略分析
cd $WORKSPACE/skills/zhiji
python3 strategy_v21.py >> $LOG_FILE 2>&1

echo "[$(date)] 知几-E 任务完成" >> $LOG_FILE
