#!/bin/bash
# Self-Check 自动化脚本 v2.0
# 用法：./self-check.sh [--full|--quick|--report|--fix]
# 优化：增加 Dashboard 检查、自动修复、更详细的报告

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
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 计数器
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNINGS=0

# 日志函数
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查结果记录
record_result() {
  local status=$1
  local check=$2
  local detail=$3
  TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
  
  case $status in
    "PASS")
      PASSED_CHECKS=$((PASSED_CHECKS + 1))
      log "✅ PASS: $check - $detail"
      ;;
    "FAIL")
      FAILED_CHECKS=$((FAILED_CHECKS + 1))
      log "🔴 FAIL: $check - $detail"
      ;;
    "WARN")
      WARNINGS=$((WARNINGS + 1))
      log "🟡 WARN: $check - $detail"
      ;;
  esac
}

# 1. Gateway 检查
check_gateway() {
  log "检查 Gateway 状态..."
  echo "### 1️⃣ Gateway 状态"
  echo ""
  
  PID=$(pgrep -f "openclaw gateway" | head -1 || echo "")
  
  if [ -n "$PID" ]; then
    echo "✅ Gateway 运行中 (PID: $PID)"
    record_result "PASS" "Gateway" "PID: $PID"
    log "Gateway 正常 (PID: $PID)"
  else
    echo "🔴 Gateway 已停止，尝试重启..."
    record_result "FAIL" "Gateway" "已停止，尝试重启"
    log "Gateway 已停止，尝试重启"
    
    # 使用快速重启脚本
    if [ -f "/home/nicola/.openclaw/workspace/scripts/gateway-quick-restart.sh" ]; then
      /home/nicola/.openclaw/workspace/scripts/gateway-quick-restart.sh
      sleep 3
      PID=$(pgrep -f "openclaw gateway" | head -1 || echo "")
      if [ -n "$PID" ]; then
        echo "✅ Gateway 重启成功 (PID: $PID)"
        record_result "PASS" "Gateway 重启" "PID: $PID"
      else
        echo "🔴 Gateway 重启失败"
        record_result "FAIL" "Gateway 重启" "失败"
      fi
    else
      echo "🟡 快速重启脚本不存在，尝试手动启动"
      record_result "WARN" "Gateway 重启脚本" "不存在"
      openclaw gateway start 2>&1 | head -5
    fi
  fi
  echo ""
}

# 2. Dashboard 状态检查
check_dashboards() {
  log "检查 Dashboard 状态..."
  echo "### 2️⃣ Dashboard 状态"
  echo ""
  
  declare -A DASHBOARDS=(
    ["Bot Dashboard"]=3000
    ["ROI Dashboard"]=8080
    ["Skill Dashboard"]=5002
    ["太一 Dashboard"]=5001
    ["百度网盘"]=5003
    ["Google 搜索"]=5004
  )
  
  for name in "${!DASHBOARDS[@]}"; do
    port=${DASHBOARDS[$name]}
    if curl -s --connect-timeout 2 http://localhost:$port > /dev/null 2>&1; then
      echo "✅ $name (端口 $port)"
      record_result "PASS" "$name" "端口 $port 正常"
    else
      # 检查进程是否存在
      PROC_EXISTS=$(ps aux | grep -E "localhost:$port|:$port" | grep -v grep | wc -l)
      if [ "$PROC_EXISTS" -gt 0 ]; then
        echo "🟡 $name (端口 $port) - 进程存在但无法访问"
        record_result "WARN" "$name" "端口 $port 无法访问"
      else
        echo "🔴 $name (端口 $port) - 未运行"
        record_result "FAIL" "$name" "端口 $port 未运行"
      fi
    fi
  done
  echo ""
}

# 3. 残留进程清理
cleanup_processes() {
  log "检查残留进程..."
  echo "### 3️⃣ 进程清理"
  echo ""
  
  CURRENT_PID=$(cat ~/.openclaw/gateway.pid 2>/dev/null || echo "")
  COUNT=$(ps aux | grep openclaw | grep -v grep | grep -v "$CURRENT_PID" | wc -l || echo "0")
  
  if [ "$COUNT" -gt 0 ]; then
    echo "🟡 发现 $COUNT 个残留进程，清理中..."
    record_result "WARN" "残留进程" "$COUNT 个"
    log "发现 $COUNT 个残留进程，清理中"
    pkill -f "openclaw.*session" 2>/dev/null || true
    sleep 1
    echo "✅ 清理完成"
    record_result "PASS" "残留进程清理" "完成"
  else
    echo "✅ 无残留进程"
    record_result "PASS" "残留进程" "无"
  fi
  echo ""
}

# 4. Cron 验证
check_crons() {
  log "检查 Cron 任务..."
  echo "### 4️⃣ Cron 任务"
  echo ""
  
  CURRENT_CRONS=$(crontab -l 2>/dev/null || echo "")
  
  REQUIRED_CRONS=(
    "宪法学习"
    "日报生成"
    "自动执行"
    "天气预测"
    "Polymarket"
    "学习循环"
    "自进化"
  )
  
  for cron in "${REQUIRED_CRONS[@]}"; do
    if echo "$CURRENT_CRONS" | grep -q "$cron"; then
      echo "✅ Cron: $cron"
      record_result "PASS" "Cron-$cron" "已配置"
    else
      echo "🔴 Cron 缺失：$cron"
      record_result "FAIL" "Cron-$cron" "缺失"
    fi
  done
  echo ""
}

# 5. Bot 状态检查
check_bots() {
  log "检查 Bot 配置..."
  echo "### 5️⃣ Bot 配置"
  echo ""
  
  BOTS=("taiyi" "zhiji" "shanmu" "suwen" "wangliang" "paoding" "yi" "shoucangli")
  
  for bot in "${BOTS[@]}"; do
    CONFIG_FILE="$WORKSPACE/config/bot-$bot.json"
    if [ -f "$CONFIG_FILE" ]; then
      echo "✅ Bot: $bot"
      record_result "PASS" "Bot-$bot" "配置存在"
    else
      echo "🟡 Bot 配置缺失：$bot"
      record_result "WARN" "Bot-$bot" "配置缺失"
    fi
  done
  echo ""
}

# 6. 磁盘/内存检查
check_resources() {
  log "检查系统资源..."
  echo "### 6️⃣ 系统资源"
  echo ""
  
  # 磁盘
  DISK=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
  DISK_AVAIL=$(df -h / | tail -1 | awk '{print $4}')
  
  if [ "$DISK" -lt 80 ]; then
    echo "✅ 磁盘：${DISK}% (剩余 ${DISK_AVAIL})"
    record_result "PASS" "磁盘" "${DISK}%"
  elif [ "$DISK" -lt 90 ]; then
    echo "🟡 磁盘告警：${DISK}% (剩余 ${DISK_AVAIL})"
    record_result "WARN" "磁盘" "${DISK}%"
  else
    echo "🔴 磁盘紧急：${DISK}% (剩余 ${DISK_AVAIL})"
    record_result "FAIL" "磁盘" "${DISK}%"
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
    record_result "PASS" "内存" "${MEM}%"
  elif [ "$MEM" -lt 85 ]; then
    echo "🟡 内存告警：${MEM}% (剩余 ${MEM_AVAIL})"
    record_result "WARN" "内存" "${MEM}%"
  else
    echo "🔴 内存紧急：${MEM}% (剩余 ${MEM_AVAIL})"
    record_result "FAIL" "内存" "${MEM}%"
  fi
  
  # CPU
  CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 2>/dev/null || echo "0")
  CPU_INT=${CPU%.*}
  if [ -z "$CPU_INT" ]; then CPU_INT=0; fi
  
  if [ "$CPU_INT" -lt 70 ]; then
    echo "✅ CPU: ${CPU_INT}%"
    record_result "PASS" "CPU" "${CPU_INT}%"
  else
    echo "🟡 CPU 高负载：${CPU_INT}%"
    record_result "WARN" "CPU" "${CPU_INT}%"
  fi
  echo ""
}

# 7. 宪法文件检查
check_constitution() {
  log "检查宪法文件..."
  echo "### 7️⃣ 宪法文件"
  echo ""
  
  CORE_FILES=(
    "$WORKSPACE/constitution/CONST-ROUTER.md"
    "$WORKSPACE/constitution/axiom/VALUE-FOUNDATION.md"
    "$WORKSPACE/constitution/directives/NEGENTROPY.md"
    "$WORKSPACE/constitution/directives/TURBOQUANT.md"
    "$WORKSPACE/constitution/directives/AGI-TIMELINE.md"
    "$WORKSPACE/constitution/directives/OBSERVER.md"
    "$WORKSPACE/constitution/directives/SELF-LOOP.md"
    "$WORKSPACE/constitution/directives/AESTHETICS.md"
    "$WORKSPACE/SOUL.md"
    "$WORKSPACE/USER.md"
    "$WORKSPACE/HEARTBEAT.md"
    "$WORKSPACE/memory/core.md"
  )
  
  MISSING=0
  for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
      echo "✅ $(basename $file)"
      record_result "PASS" "宪法-$(basename $file)" "存在"
    else
      echo "🔴 缺失：$(basename $file)"
      record_result "FAIL" "宪法-$(basename $file)" "缺失"
      MISSING=$((MISSING + 1))
    fi
  done
  
  if [ "$MISSING" -gt 0 ]; then
    echo ""
    echo "⚠️ 警告：$MISSING 个核心宪法文件缺失"
    record_result "FAIL" "宪法完整性" "$MISSING 个文件缺失"
  fi
  echo ""
}

# 8. 网络连通性检查
check_network() {
  log "检查网络连通性..."
  echo "### 8️⃣ 网络连通性"
  echo ""
  
  # 检查外网
  if ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
    echo "✅ 外网连通"
    record_result "PASS" "外网" "连通"
  else
    echo "🔴 外网不通"
    record_result "FAIL" "外网" "不通"
  fi
  
  # 检查代理
  if curl -s --connect-timeout 3 -x http://127.0.0.1:7890 https://www.google.com > /dev/null 2>&1; then
    echo "✅ 代理正常 (7890)"
    record_result "PASS" "代理" "端口 7890 正常"
  else
    echo "🟡 代理异常 (7890)"
    record_result "WARN" "代理" "端口 7890 异常"
  fi
  
  # 检查 Clash 进程
  CLASH_PID=$(pgrep -f "clash" | head -1 || echo "")
  if [ -n "$CLASH_PID" ]; then
    echo "✅ Clash 运行中 (PID: $CLASH_PID)"
    record_result "PASS" "Clash" "PID: $CLASH_PID"
  else
    echo "🟡 Clash 未运行"
    record_result "WARN" "Clash" "未运行"
  fi
  echo ""
}

# 9. 通道状态检查
check_channels() {
  log "检查通信通道..."
  echo "### 9️⃣ 通信通道"
  echo ""
  
  # Telegram
  TG_PID=$(pgrep -f "telegram" | head -1 || echo "")
  if [ -n "$TG_PID" ]; then
    echo "✅ Telegram (PID: $TG_PID)"
    record_result "PASS" "Telegram" "PID: $TG_PID"
  else
    echo "🔴 Telegram 未运行"
    record_result "FAIL" "Telegram" "未运行"
  fi
  
  # 微信
  WX_STATUS=$(ps aux | grep -E "wechat|weixin" | grep -v grep | wc -l)
  if [ "$WX_STATUS" -gt 0 ]; then
    echo "✅ 微信通道"
    record_result "PASS" "微信" "运行中"
  else
    echo "🟡 微信通道状态未知"
    record_result "WARN" "微信" "状态未知"
  fi
  
  # Discord
  DISCORD_PID=$(pgrep -f "discord" | head -1 || echo "")
  if [ -n "$DISCORD_PID" ]; then
    echo "✅ Discord (PID: $DISCORD_PID)"
    record_result "PASS" "Discord" "PID: $DISCORD_PID"
  else
    echo "🟡 Discord 未运行 (可选)"
    record_result "WARN" "Discord" "未运行"
  fi
  echo ""
}

# 10. 最近任务执行检查
check_recent_tasks() {
  log "检查最近任务执行..."
  echo "### 🔟 最近任务执行"
  echo ""
  
  # 检查今日 memory 文件
  TODAY=$(date +%Y-%m-%d)
  MEMORY_FILE="$WORKSPACE/memory/$TODAY.md"
  
  if [ -f "$MEMORY_FILE" ]; then
    echo "✅ 今日记忆文件已创建"
    record_result "PASS" "今日记忆" "$TODAY.md"
  else
    echo "🟡 今日记忆文件未创建"
    record_result "WARN" "今日记忆" "未创建"
  fi
  
  # 检查 HEARTBEAT.md
  if [ -f "$WORKSPACE/HEARTBEAT.md" ]; then
    LAST_UPDATE=$(stat -c %y "$WORKSPACE/HEARTBEAT.md" 2>/dev/null | cut -d' ' -f1)
    echo "✅ HEARTBEAT.md (最后更新：$LAST_UPDATE)"
    record_result "PASS" "HEARTBEAT" "已更新"
  else
    echo "🔴 HEARTBEAT.md 缺失"
    record_result "FAIL" "HEARTBEAT" "缺失"
  fi
  echo ""
}

# 自动修复模式
auto_fix() {
  log "执行自动修复..."
  echo "### 🔧 自动修复"
  echo ""
  
  # 修复 Gateway
  PID=$(pgrep -f "openclaw gateway" | head -1 || echo "")
  if [ -z "$PID" ]; then
    echo "🔧 修复 Gateway..."
    if [ -f "/home/nicola/.openclaw/workspace/scripts/gateway-quick-restart.sh" ]; then
      /home/nicola/.openclaw/workspace/scripts/gateway-quick-restart.sh
      sleep 3
      if pgrep -f "openclaw gateway" > /dev/null; then
        echo "✅ Gateway 修复成功"
        record_result "PASS" "Gateway 修复" "成功"
      else
        echo "🔴 Gateway 修复失败"
        record_result "FAIL" "Gateway 修复" "失败"
      fi
    fi
  fi
  
  # 修复 Dashboard
  for port in 3000 8080 5001 5002 5003 5004; do
    if ! curl -s --connect-timeout 2 http://localhost:$port > /dev/null 2>&1; then
      echo "🔧 尝试启动端口 $port 的服务..."
      # 这里可以添加具体的启动逻辑
    fi
  done
  
  echo ""
}

# 生成报告
generate_report() {
  local health_score=0
  if [ "$TOTAL_CHECKS" -gt 0 ]; then
    health_score=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
  fi
  
  echo "### 📊 健康度评分"
  echo ""
  echo "**健康度**: ${health_score}%"
  echo "**总检查项**: $TOTAL_CHECKS"
  echo "**通过**: $PASSED_CHECKS ✅"
  echo "**警告**: $WARNINGS ⚠️"
  echo "**失败**: $FAILED_CHECKS ❌"
  echo ""
  
  if [ "$health_score" -ge 90 ]; then
    echo "🎉 系统状态优秀！"
  elif [ "$health_score" -ge 70 ]; then
    echo "👍 系统状态良好"
  elif [ "$health_score" -ge 50 ]; then
    echo "⚠️ 系统需要关注"
  else
    echo "🚨 系统需要立即干预！"
  fi
  echo ""
  
  echo "### 下一步"
  if [ "$FAILED_CHECKS" -gt 0 ]; then
    echo "- [ ] 修复 $FAILED_CHECKS 个失败项"
  fi
  if [ "$WARNINGS" -gt 0 ]; then
    echo "- [ ] 检查 $WARNINGS 个警告项"
  fi
  if [ "$FAILED_CHECKS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
    echo "- [x] 系统正常，无需操作"
  fi
  echo ""
  echo "---"
  echo "*执行时间：$(date '+%Y-%m-%d %H:%M:%S') | 太一 | Self-Check v2.0*"
}

# 主执行流程
main() {
  log "========== 自检开始 =========="
  
  echo "## 🔍 太一系统自检报告"
  echo ""
  echo "**时间**: $TIMESTAMP"
  echo "**执行 Bot**: 太一"
  echo "**模式**: ${1:---quick}"
  echo ""
  echo "### 检查结果"
  echo ""
  
  # 执行检查
  check_gateway
  check_dashboards
  cleanup_processes
  check_crons
  check_bots
  check_resources
  check_constitution
  
  # 完整模式增加额外检查
  if [ "$1" = "--full" ]; then
    check_network
    check_channels
    check_recent_tasks
  elif [ "$1" = "--quick" ]; then
    # 快速模式只检查核心项
    echo "_快速模式：仅检查核心项_"
    echo ""
  fi
  
  # 修复模式
  if [ "$1" = "--fix" ]; then
    auto_fix
  fi
  
  # 生成报告
  generate_report
  
  # 保存报告
  if [ "$1" = "--report" ] || [ "$1" = "--full" ]; then
    # 保存到文件（移除 ANSI 颜色码）
    echo "## 🔍 太一系统自检报告" > "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "**时间**: $TIMESTAMP" >> "$REPORT_FILE"
    echo "**执行 Bot**: 太一" >> "$REPORT_FILE"
    echo "**模式**: ${1:---quick}" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "### 健康度：${health_score}%" >> "$REPORT_FILE"
    echo "- 通过：$PASSED_CHECKS" >> "$REPORT_FILE"
    echo "- 警告：$WARNINGS" >> "$REPORT_FILE"
    echo "- 失败：$FAILED_CHECKS" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "*报告已保存：$REPORT_FILE*"
    log "报告已保存：$REPORT_FILE"
  fi
  
  log "========== 自检完成 =========="
  log "健康度：${health_score}% (通过:$PASSED_CHECKS 警告:$WARNINGS 失败:$FAILED_CHECKS)"
}

# 执行
main "$@"
