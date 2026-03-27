#!/bin/bash
# 素问-天气预测（每小时）
LOG_FILE="$HOME/.openclaw/workspace/logs/cron-weather.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

log "=== 开始天气预测 ==="

# 获取三亚天气
WEATHER=$(curl -s "wttr.in/Sanya?format=%t+%c+%h+%w" 2>/dev/null || echo "天气数据获取失败")

log "🌤️ 三亚天气：$WEATHER"
log "✅ 天气预测完成"

# 发送通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "天气预测" "🌤️ 三亚天气：$WEATHER" &
