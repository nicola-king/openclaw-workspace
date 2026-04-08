#!/bin/bash
# Gateway 自愈脚本
# 触发条件：Gateway 不可用时自动执行
# 目标：60 秒内自动恢复

LOG_FILE="/home/nicola/.openclaw/logs/gateway-self-heal.log"
START_TIME=$(date +%s)
MAX_RESTART_ATTEMPTS=3

log() {
  local elapsed=$(($(date +%s) - START_TIME))
  echo "[${elapsed}s] $1" | tee -a "$LOG_FILE"
}

# 检查 Gateway 健康度
check_gateway_health() {
  # 1. 检查进程
  if ! pgrep -f "openclaw-gateway" > /dev/null; then
    return 1
  fi
  
  # 2. 检查 HTTP 端口
  if ! curl -s -o /dev/null -w "" http://127.0.0.1:18789/ 2>/dev/null; then
    return 1
  fi
  
  # 3. 检查 WebSocket (可选)
  # if ! curl -s http://127.0.0.1:18789/ | grep -q "OpenClaw"; then
  #   return 1
  # fi
  
  return 0
}

# 自愈流程
self_heal() {
  log "========== Gateway 自愈流程启动 =========="
  log "检测到 Gateway 异常，开始自愈..."
  
  local attempt=1
  while [ $attempt -le $MAX_RESTART_ATTEMPTS ]; do
    log "尝试第 $attempt/$MAX_RESTART_ATTEMPTS 次重启..."
    
    # 1. 快速重启
    /home/nicola/.openclaw/workspace/scripts/gateway-quick-restart.sh >> "$LOG_FILE" 2>&1
    
    # 2. 等待 10 秒
    sleep 10
    
    # 3. 检查是否恢复
    if check_gateway_health; then
      PID=$(pgrep -f "openclaw-gateway" | head -1)
      elapsed=$(($(date +%s) - START_TIME))
      log "✅ 自愈成功 (PID: $PID, 总耗时：${elapsed}s, 尝试次数：$attempt)"
      log "========== Gateway 自愈流程完成 =========="
      
      # 发送通知 (可选)
      # /home/nicola/.openclaw/workspace/scripts/notify.sh "Gateway 自愈成功" "尝试 $attempt 次，耗时 ${elapsed}s"
      
      return 0
    fi
    
    log "⚠️ 第 $attempt 次重启失败，准备下一次尝试..."
    attempt=$((attempt + 1))
    sleep 5
  done
  
  # 所有尝试失败
  elapsed=$(($(date +%s) - START_TIME))
  log "🔴 自愈失败 (总耗时：${elapsed}s, 尝试 $MAX_RESTART_ATTEMPTS 次)"
  log "========== Gateway 自愈流程失败 =========="
  
  # 发送告警
  # /home/nicola/.openclaw/workspace/scripts/notify.sh "Gateway 自愈失败" "需要人工介入"
  
  return 1
}

# 主流程
main() {
  # 检查是否需要自愈
  if check_gateway_health; then
    echo "✅ Gateway 健康，无需自愈"
    exit 0
  fi
  
  # 执行自愈
  self_heal
  exit $?
}

main "$@"
