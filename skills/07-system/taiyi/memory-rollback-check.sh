#!/bin/bash
# 太一-记忆回滚检查
LOG_FILE="$HOME/.openclaw/workspace/logs/cron-memory-rollback.log"
MEMORY_DIR="$HOME/.openclaw/workspace/memory"
MEMORY_MAIN="$HOME/.openclaw/workspace/MEMORY.md"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

log "=== 开始记忆回滚检查 ==="

# 检查今日记忆文件
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$MEMORY_DIR/$TODAY.md"

if [ -f "$TODAY_FILE" ]; then
    LINES=$(wc -l < "$TODAY_FILE")
    log "✅ 今日记忆文件存在：$TODAY_FILE ($LINES 行)"
else
    log "⚠️ 今日记忆文件不存在，创建中..."
    echo "# $TODAY 记忆" > "$TODAY_FILE"
    log "✅ 已创建：$TODAY_FILE"
fi

# 检查 MEMORY.md 是否更新
if [ -f "$MEMORY_MAIN" ]; then
    MAIN_LINES=$(wc -l < "$MEMORY_MAIN")
    log "✅ MEMORY.md: $MAIN_LINES 行"
else
    log "❌ MEMORY.md 不存在"
fi

# 检查昨日记忆是否归档
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
YESTERDAY_FILE="$MEMORY_DIR/$YESTERDAY.md"
if [ -f "$YESTERDAY_FILE" ]; then
    log "✅ 昨日记忆：$YESTERDAY_FILE"
else
    log "🟡 昨日记忆文件不存在（可能刚创建）"
fi

log "=== 记忆回滚检查完成 ==="

# 发送通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "记忆回滚检查" "✅ 记忆文件检查完成" &
