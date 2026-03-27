#!/bin/bash
# 定时任务完成通知脚本
# 用法：send-cron-notification.sh "任务名称" "任务内容"

TITLE="$1"
CONTENT="$2"
LOG_FILE="$HOME/.openclaw/workspace/logs/cron-notification.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Telegram 配置（太一 Bot）
TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
CHAT_ID="7073481596"  # SAYELF 的 Telegram ID

MESSAGE="📱 *$TITLE*

$CONTENT

时间：$(date '+%Y-%m-%d %H:%M')"

curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "text=$MESSAGE" \
    -d "parse_mode=Markdown" \
    2>/dev/null

if [ $? -eq 0 ]; then
    log "✅ 通知发送成功：$TITLE"
    echo "✅ 通知已发送到 Telegram"
else
    log "❌ 通知发送失败：$TITLE"
    echo "❌ 通知发送失败"
fi
