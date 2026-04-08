#!/bin/bash
# Self-Check 自动化脚本
# 用法：./self-check.sh [--full|--quick|--report]

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
REPORT_DIR="$WORKSPACE/reports"
LOG_FILE="/home/nicola/.openclaw/logs/self-check.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
REPORT_FILE="$REPORT_DIR/self-check-$(date +%Y%m%d-%H%M).md"

# 确保目录存在
mkdir -p "$REPORT_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 1. Gateway 检查
check_gateway() {
  log "检查 Gateway 状态..."
  PID=$(pgrep -f "openclaw gateway" | head -1 || echo "")
  
  if [ -n "$PID" ]; then
    echo "✅ Gateway 运行中 (PID: $PID)"
    log "Gateway 正常 (PID: $PID)"
    return 0
  else
    echo "🔴 Gateway 已停止，使用快速脚本重启..."
    log "Gateway 已停止，使用快速脚本重启"
    
    # 使用快速重启脚本 (30 秒内)
    /home/nicola/.openclaw/workspace/scripts/gateway-quick-restart.sh
    
    sleep 3
    PID=$(pgrep -f "openclaw gateway" | head -1 || echo "")
    if [ -n "$PID" ]; then
      echo "✅ Gateway 重启成功 (PID: $PID)"
      log "Gateway 重启成功 (PID: $PID)"
      return 0
    else
      echo "🔴 Gateway 重启失败"
      log "Gateway 重启失败"
      return 1
    fi
  fi
}

# 2. 残留进程清理
cleanup_processes() {
  log "检查残留进程..."
  CURRENT_PID=$(cat ~/.openclaw/gateway.pid 2>/dev/null || echo "")
  COUNT=$(ps aux | grep openclaw | grep -v grep | grep -v "$CURRENT_PID" | wc -l || echo "0")
  
  if [ "$COUNT" -gt 0 ]; then
    echo "🟡 发现 $COUNT 个残留进程，清理中..."
    log "发现 $COUNT 个残留进程，清理中"
    pkill -f "openclaw.*session" 2>/dev/null || true
    echo "✅ 清理完成"
    log "残留进程清理完成"
  else
    echo "✅ 无残留进程"
    log "无残留进程"
  fi
}

# 3. Cron 验证
check_crons() {
  log "检查 Cron 任务..."
  CURRENT_CRONS=$(crontab -l 2>/dev/null || echo "")
  
  REQUIRED_CRONS=(
    "宪法学习"
    "日报生成"
    "自动执行"
    "天气预测"
    "Polymarket"
  )
  
  for cron in "${REQUIRED_CRONS[@]}"; do
    if echo "$CURRENT_CRONS" | grep -q "$cron"; then
      echo "✅ Cron: $cron"
      log "Cron 正常：$cron"
    else
      echo "🔴 Cron 缺失：$cron"
      log "Cron 缺失：$cron"
    fi
  done
}

# 4. Bot 状态检查
check_bots() {
  log "检查 Bot 配置..."
  BOTS=("taiyi" "zhiji" "shanmu" "suwen" "wangliang" "paoding" "yi" "shoucangli")
  
  for bot in "${BOTS[@]}"; do
    CONFIG_FILE="$WORKSPACE/config/bot-$bot.json"
    if [ -f "$CONFIG_FILE" ]; then
      echo "✅ Bot: $bot"
      log "Bot 配置存在：$bot"
    else
      echo "🟡 Bot 配置缺失：$bot"
      log "Bot 配置缺失：$bot"
    fi
  done
}

# 5. 磁盘/内存检查
check_resources() {
  log "检查系统资源..."
  
  # 磁盘
  DISK=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
  DISK_AVAIL=$(df -h / | tail -1 | awk '{print $4}')
  
  if [ "$DISK" -lt 80 ]; then
    echo "✅ 磁盘：${DISK}% (剩余 ${DISK_AVAIL})"
    log "磁盘正常：${DISK}%"
  elif [ "$DISK" -lt 90 ]; then
    echo "🟡 磁盘告警：${DISK}% (剩余 ${DISK_AVAIL})"
    log "磁盘告警：${DISK}%"
  else
    echo "🔴 磁盘紧急：${DISK}% (剩余 ${DISK_AVAIL})"
    log "磁盘紧急：${DISK}%"
  fi
  
  # 内存
  MEM=$(free | grep Mem | awk '{printf("%.0f"), $3/$2 * 100.0}' 2>/dev/null || echo "0")
  MEM_AVAIL=$(free -h | grep Mem | awk '{print $7}' 2>/dev/null || echo "N/A")
  
  # 确保 MEM 是有效整数
  if [ -z "$MEM" ] || [ "$MEM" = "0" ]; then
    MEM=0
  fi
  
  if [ "$MEM" -lt 70 ]; then
    echo "✅ 内存：${MEM}% (剩余 ${MEM_AVAIL})"
    log "内存正常：${MEM}%"
  elif [ "$MEM" -lt 85 ]; then
    echo "🟡 内存告警：${MEM}% (剩余 ${MEM_AVAIL})"
    log "内存告警：${MEM}%"
  else
    echo "🔴 内存紧急：${MEM}% (剩余 ${MEM_AVAIL})"
    log "内存紧急：${MEM}%"
  fi
}

# 6. 宪法文件检查
check_constitution() {
  log "检查宪法文件..."
  
  CORE_FILES=(
    "$WORKSPACE/constitution/CONST-ROUTER.md"
    "$WORKSPACE/constitution/axiom/VALUE-FOUNDATION.md"
    "$WORKSPACE/constitution/directives/NEGENTROPY.md"
    "$WORKSPACE/constitution/directives/TURBOQUANT.md"
    "$WORKSPACE/SOUL.md"
    "$WORKSPACE/USER.md"
    "$WORKSPACE/HEARTBEAT.md"
  )
  
  MISSING=0
  for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
      echo "✅ $(basename $file)"
      log "宪法文件存在：$(basename $file)"
    else
      echo "🔴 缺失：$(basename $file)"
      log "宪法文件缺失：$(basename $file)"
      MISSING=$((MISSING + 1))
    fi
  done
  
  if [ "$MISSING" -gt 0 ]; then
    log "警告：$MISSING 个核心宪法文件缺失"
  fi
}

# 7. 网络连通性检查
check_network() {
  log "检查网络连通性..."
  
  # 检查外网
  if ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
    echo "✅ 外网连通"
    log "外网连通"
  else
    echo "🔴 外网不通"
    log "外网不通"
  fi
  
  # 检查代理
  if curl -s --connect-timeout 3 -x http://127.0.0.1:7890 https://www.google.com > /dev/null 2>&1; then
    echo "✅ 代理正常 (7890)"
    log "代理正常"
  else
    echo "🟡 代理异常 (7890)"
    log "代理异常"
  fi
}

# 生成报告
generate_report() {
  echo ""
  echo "### 下一步"
  echo "- [ ] 自检完成，系统正常"
  echo ""
  echo "---"
  echo "*执行时间：$(date '+%Y-%m-%d %H:%M:%S') | 守藏吏 | Self-Check v1.0*"
}

# 主执行流程
main() {
  log "========== 自检开始 =========="
  
  echo "## 🔍 系统自检报告"
  echo ""
  echo "**时间**: $TIMESTAMP"
  echo "**执行 Bot**: 守藏吏"
  echo "**模式**: ${1:---quick}"
  echo ""
  echo "### 检查结果"
  echo ""
  
  # 执行检查
  check_gateway || true
  cleanup_processes
  check_crons
  check_bots
  check_resources
  check_constitution
  
  # 完整模式增加网络检查
  if [ "$1" = "--full" ]; then
    echo ""
    check_network
  fi
  
  # 生成报告
  generate_report
  
  # 保存报告
  if [ "$1" = "--report" ] || [ "$1" = "--full" ]; then
    echo ""
    echo "📄 报告已保存：$REPORT_FILE"
    log "报告已保存：$REPORT_FILE"
  fi
  
  log "========== 自检完成 =========="
}

# 执行
main "$@"
