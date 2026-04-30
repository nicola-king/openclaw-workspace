#!/bin/bash
LOG_DIR="/home/nicola/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/channel-monitor.log"
}

log "========== 通讯通道检查 =========="

if pgrep -f "[Tt]elegram" > /dev/null || pgrep -f "tsetup" > /dev/null; then
    log "✅ Telegram 运行正常"
else
    log "⚠️ Telegram 未运行，尝试重启..."
    nohup /home/nicola/下载/tsetup.6.7.5/Telegram/Telegram > /tmp/telegram.log 2>&1 &
    sleep 5
    if pgrep -f "[Tt]elegram" > /dev/null || pgrep -f "tsetup" > /dev/null; then
        log "✅ Telegram 重启成功"
    else
        log "❌ Telegram 重启失败"
    fi
fi

if pgrep -f "[Dd]iscord" > /dev/null || pgrep -f "/usr/share/discord" > /dev/null; then
    log "✅ Discord 运行正常"
else
    log "⚠️ Discord 未运行，尝试重启..."
    nohup /usr/bin/discord > /tmp/discord.log 2>&1 &
    sleep 5
    if pgrep -f "[Dd]iscord" > /dev/null || pgrep -f "/usr/share/discord" > /dev/null; then
        log "✅ Discord 重启成功"
    else
        log "❌ Discord 重启失败"
    fi
fi

log "========== 检查完成 =========="
