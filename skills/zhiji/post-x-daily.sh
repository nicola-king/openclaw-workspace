#!/bin/bash
# 知几-X 自动发布（每日 10:00）
LOG_FILE="$HOME/.openclaw/workspace/logs/cron-zhiji-x.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "=== X 自动发布开始 ==="

# 执行 Python 脚本（自动发布模式）
cd "$HOME/.openclaw/workspace/skills/zhiji"
python3 x-auto-poster.py --type morning --auto >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "✅ X 发布完成"
    # 发送通知
    "$HOME/.openclaw/workspace/scripts/send-cron-notification.sh" "知几 X 发布" "✅ 内容已发布到 X" &
else
    log "❌ X 发布失败"
fi

log "=== X 自动发布结束 ==="
