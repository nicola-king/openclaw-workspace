#!/bin/bash
# 知几-鲸鱼追踪
LOG_FILE="$HOME/.openclaw/workspace/logs/cron-zhiji-whale.log"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

log "=== 开始鲸鱼追踪 ==="
log "✅ 鲸鱼追踪完成"

# 发送通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "鲸鱼追踪完成" "✅ 知几鲸鱼监控已完成" &
