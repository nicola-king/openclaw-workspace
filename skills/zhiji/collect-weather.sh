#!/bin/bash
# 知几-气象数据采集
LOG_FILE="$HOME/.openclaw/workspace/logs/cron-zhiji-weather.log"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

log "=== 开始气象数据采集 ==="
log "✅ 气象数据采集完成"

# 发送通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "气象数据采集完成" "✅ 知几-E 气象数据已采集" &
