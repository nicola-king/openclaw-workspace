#!/bin/bash
# 启动 Telegram 实时@监听服务

LOG_FILE="/home/nicola/.openclaw/workspace/logs/telegram_listener_start.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "📡 启动 Telegram 实时@监听服务"

# 检查是否已在运行
if pgrep -f "telegram_realtime_listener.py" > /dev/null; then
    log "⚠️  监听服务已在运行"
    exit 0
fi

# 后台启动
cd /home/nicola/.openclaw/workspace
nohup python3 skills/07-system/telegram_realtime_listener.py >> /home/nicola/.openclaw/workspace/logs/telegram_realtime_listener.log 2>&1 &

PID=$!
log "✅ 监听服务已启动 (PID: $PID)"

# 保存 PID
echo $PID > /tmp/telegram_listener.pid

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
