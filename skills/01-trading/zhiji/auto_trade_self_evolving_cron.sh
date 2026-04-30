#!/bin/bash
# 自动交易自进化智能体 - 定时任务脚本

LOG_FILE="/home/nicola/.openclaw/workspace/logs/auto_trade_self_evolving_cron.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "💰 开始自动交易自进化检查"

cd /home/nicola/.openclaw/workspace
python3 skills/01-trading/zhiji/auto_trade_self_evolving.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ 自动交易自进化检查完成"
else
    log "❌ 自动交易自进化检查失败"
fi

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
