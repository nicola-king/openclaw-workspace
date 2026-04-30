#!/bin/bash
# IP 监控自进化智能体 - 定时任务脚本

LOG_FILE="/home/nicola/.openclaw/workspace/logs/ip_self_evolving_cron.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "🌐 开始 IP 自进化监控"

cd /home/nicola/.openclaw/workspace
python3 skills/01-trading/zhiji/ip_self_evolving_monitor.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ IP 自进化监控完成"
else
    log "❌ IP 自进化监控失败"
fi

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
