#!/bin/bash
# Gateway 快速重启脚本 v2.0
# 目标：30 秒内完成重启
# 用法：./gateway-quick-restart.sh

LOG_FILE="/home/nicola/.openclaw/logs/gateway-restart.log"
START_TIME=$(date +%s)

log() {
  local elapsed=$(($(date +%s) - START_TIME))
  echo "[${elapsed}s] $1" | tee -a "$LOG_FILE"
}

log "========== Gateway 快速重启开始 =========="

# 1. 快速停止 (直接 kill + systemctl 并行)
log "停止 Gateway..."
pkill -9 -f "openclaw-gateway" 2>/dev/null || true
systemctl --user stop openclaw-gateway.service --no-block 2>/dev/null || true
sleep 2

# 2. 确认停止
if pgrep -f "openclaw-gateway" > /dev/null; then
  log "⚠️ 仍有残留进程，强制清理..."
  pkill -9 -f "openclaw.*gateway" 2>/dev/null || true
  sleep 1
fi

# 3. 快速启动
log "启动 Gateway..."
systemctl --user start openclaw-gateway.service

# 4. 轮询检查 (最多 15 秒)
log "等待启动完成..."
for i in {1..15}; do
  if curl -s -o /dev/null -w "" http://127.0.0.1:18789/ 2>/dev/null; then
    PID=$(pgrep -f "openclaw-gateway" | head -1)
    elapsed=$(($(date +%s) - START_TIME))
    log "✅ Gateway 启动成功 (PID: $PID, 总耗时：${elapsed}s)"
    log "========== Gateway 快速重启完成 =========="
    exit 0
  fi
  sleep 1
done

# 5. 最终状态检查
PID=$(pgrep -f "openclaw-gateway" | head -1 || echo "")
elapsed=$(($(date +%s) - START_TIME))

if [ -n "$PID" ]; then
  log "✅ Gateway 进程运行中 (PID: $PID, 总耗时：${elapsed}s)"
  log "⚠️  WebSocket 端口待确认"
  log "========== Gateway 快速重启完成 =========="
  exit 0
else
  log "🔴 Gateway 启动失败 (总耗时：${elapsed}s)"
  log "请检查日志：journalctl --user -u openclaw-gateway.service -n 20"
  log "========== Gateway 快速重启失败 =========="
  exit 1
fi
