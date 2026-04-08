#!/bin/bash
# 天气预测 Cron - 每小时执行
# 功能：天气预报数据采集 + 入库

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="/home/nicola/.openclaw/logs/weather-forecast.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "========== 天气预测 =========="

# 执行天气预报脚本
if [ -f "$WORKSPACE/skills/suwen/weather-forecast.sh" ]; then
    log "🌤️ 执行天气预报..."
    bash "$WORKSPACE/skills/suwen/weather-forecast.sh" >> "$LOG_FILE" 2>&1
    log "✅ 天气预报完成"
else
    log "⚠️ 天气预报脚本不存在"
fi

log "========== 天气预测完成 =========="
log ""
