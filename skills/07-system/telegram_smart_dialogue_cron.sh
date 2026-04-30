#!/bin/bash
# Telegram 群聊智能对话定时任务 (每 30 分钟检查一次)

LOG_FILE="/home/nicola/.openclaw/workspace/logs/telegram_smart_dialogue.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "💬 开始 Telegram 智能对话检查"

cd /home/nicola/.openclaw/workspace
python3 skills/07-system/telegram_smart_dialogue.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ Telegram 智能对话检查完成"
else
    log "❌ Telegram 智能对话检查失败"
fi

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
