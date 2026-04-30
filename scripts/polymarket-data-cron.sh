#!/bin/bash
# Polymarket 数据采集 Cron - 每 30 分钟执行
# 功能：热门市场数据采集 + 入库

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="/home/nicola/.openclaw/logs/polymarket-weather.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "========== Polymarket 数据采集 =========="

# 执行数据采集脚本
if [ -f "$WORKSPACE/scripts/polymarket-hot-weather-cron.sh" ]; then
    log "📊 执行数据采集..."
    bash "$WORKSPACE/scripts/polymarket-hot-weather-cron.sh" >> "$LOG_FILE" 2>&1
    log "✅ 数据采集完成"
else
    log "⚠️ 数据采集脚本不存在"
fi

log "========== Polymarket 数据采集完成 =========="
log ""
