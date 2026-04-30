#!/bin/bash
# 知几-实时下注监控
LOG_FILE="$HOME/.openclaw/workspace/logs/cron-zhiji-bet.log"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

log "=== 下注监控 ==="
log "✅ 下注监控完成"

# 发送通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "任务完成" "任务已执行" &
