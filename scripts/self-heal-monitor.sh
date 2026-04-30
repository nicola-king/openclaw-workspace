#!/bin/bash
# 自检 + 自愈 监控守护进程
# 每 5 分钟检查一次，异常时触发自愈

LOG_FILE="/home/nicola/.openclaw/logs/self-heal-monitor.log"
INTERVAL=300  # 5 分钟

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_and_heal() {
  # 检查 Gateway 健康
  if ! curl -s -o /dev/null -w "" http://127.0.0.1:18789/ 2>/dev/null; then
    log "🔴 Gateway 异常，触发自愈..."
    /home/nicola/.openclaw/workspace/scripts/gateway-self-heal.sh
    return $?
  fi
  
  # 检查 Cron 服务 (仅当存在时)
  if systemctl --user list-unit-files | grep -q cron; then
    if ! systemctl --user is-active cron > /dev/null 2>&1; then
      log "🔴 Cron 服务异常，尝试重启..."
      systemctl --user restart cron
    fi
  fi
  
  # 检查磁盘空间
  DISK=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
  if [ -n "$DISK" ] && [ "$DISK" -gt 90 ] 2>/dev/null; then
    log "🔴 磁盘空间告警 (${DISK}%)，清理临时文件..."
    rm -rf /tmp/openclaw-* 2>/dev/null || true
    rm -rf ~/.cache/openclaw/* 2>/dev/null || true
  fi
  
  # 检查内存
  MEM=$(free | grep Mem | awk '{printf("%.0f"), $3/$2 * 100.0}')
  if [ -n "$MEM" ] && [ "$MEM" -gt 85 ] 2>/dev/null; then
    log "🟡 内存使用率高 (${MEM}%)，建议清理"
  fi
  
  log "✅ 系统检查完成"
  return 0
}

# 主循环
log "========== 自检自愈监控启动 =========="

while true; do
  check_and_heal
  sleep $INTERVAL
done
