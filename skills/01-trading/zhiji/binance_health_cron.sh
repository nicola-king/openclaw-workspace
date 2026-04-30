#!/bin/bash
# 币安健康自检定时任务

LOG_FILE="/home/nicola/.openclaw/workspace/logs/binance_health_cron.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "🏥 开始币安健康自检"

cd /home/nicola/.openclaw/workspace
python3 skills/01-trading/zhiji/binance_health_check.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ 健康自检完成"
else
    log "❌ 健康自检失败"
fi

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
