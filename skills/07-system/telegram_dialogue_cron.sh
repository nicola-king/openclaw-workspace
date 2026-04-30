#!/bin/bash
# Telegram 群聊对话定时任务

LOG_FILE="/home/nicola/.openclaw/workspace/logs/telegram_dialogue.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "💬 开始 Telegram 群聊对话"

cd /home/nicola/.openclaw/workspace
python3 skills/07-system/telegram_group_dialogue.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ Telegram 群聊对话完成"
else
    log "❌ Telegram 群聊对话失败"
fi

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
