#!/bin/bash
# ============================================
# 脚本名：heartbeat-cli.sh
# 用途：HEARTBEAT 任务 CLI 快捷命令集合
# 作者：太一 AGI
# 版本：v1.0
# 创建时间：2026-04-02 07:05
# ============================================

set -euo pipefail

readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
readonly LOG_FILE="/tmp/heartbeat-cli.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log() {
  echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$LOG_FILE"
}

success() {
  echo -e "${GREEN}✓${NC} $*" | tee -a "$LOG_FILE"
}

warning() {
  echo -e "${YELLOW}⚠${NC} $*" | tee -a "$LOG_FILE"
}

error() {
  echo -e "${RED}✗${NC} $*" | tee -a "$LOG_FILE"
}

# 1. 检查 Gateway 状态
check_gateway() {
  log "检查 Gateway 状态..."
  
  if pgrep -f "openclaw gateway" > /dev/null; then
    success "Gateway 运行中"
    return 0
  else
    error "Gateway 未运行"
    warning "尝试启动 Gateway..."
    openclaw gateway start
    sleep 3
    
    if pgrep -f "openclaw gateway" > /dev/null; then
      success "Gateway 已启动"
      return 0
    else
      error "Gateway 启动失败"
      return 1
    fi
  fi
}

# 2. 检查会话状态
check_sessions() {
  log "检查活跃会话..."
  
  local count
  count=$(openclaw sessions list --limit 10 2>/dev/null | grep -c "active" || echo "0")
  
  if [[ "$count" -gt 0 ]]; then
    success "活跃会话：$count 个"
    openclaw sessions list --limit 5
  else
    warning "无活跃会话"
  fi
}

# 3. 检查待办任务
check_tasks() {
  log "检查待办任务..."
  
  if [[ -f "$SCRIPT_DIR/../HEARTBEAT.md" ]]; then
    local pending
    pending=$(grep -c "^\- \[ \]" "$SCRIPT_DIR/../HEARTBEAT.md" || echo "0")
    success "待办任务：$pending 个"
    
    if [[ "$pending" -gt 0 ]]; then
      echo ""
      echo "待办清单:"
      grep "^\- \[ \]" "$SCRIPT_DIR/../HEARTBEAT.md" | head -5
    fi
  else
    warning "HEARTBEAT.md 未找到"
  fi
}

# 4. 检查通道状态
check_channels() {
  log "检查消息通道..."
  
  # 微信通道
  if [[ -f "$SCRIPT_DIR/../MEMORY.md" ]]; then
    if grep -q "微信.*✅" "$SCRIPT_DIR/../MEMORY.md"; then
      success "微信通道：正常"
    else
      warning "微信通道：状态未知"
    fi
  fi
  
  # Telegram 通道
  if grep -q "Telegram.*✅" "$SCRIPT_DIR/../MEMORY.md" 2>/dev/null; then
    success "Telegram 通道：正常"
  else
    warning "Telegram 通道：状态未知"
  fi
}

# 5. 检查系统资源
check_resources() {
  log "检查系统资源..."
  
  # CPU
  local cpu_usage
  cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 || echo "N/A")
  echo "CPU 使用率：${cpu_usage}%"
  
  # 内存
  local mem_usage
  mem_usage=$(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}' || echo "N/A")
  echo "内存使用率：${mem_usage}"
  
  # 磁盘
  local disk_usage
  disk_usage=$(df -h / | tail -1 | awk '{print $5}' || echo "N/A")
  echo "磁盘使用率：${disk_usage}"
}

# 6. 检查定时任务
check_cron() {
  log "检查定时任务..."
  
  local cron_count
  cron_count=$(crontab -l 2>/dev/null | grep -c "openclaw" || echo "0")
  success "OpenClaw 定时任务：$cron_count 个"
  
  if [[ "$cron_count" -gt 0 ]]; then
    echo ""
    crontab -l 2>/dev/null | grep "openclaw"
  fi
}

# 7. 检查记忆文件
check_memory() {
  log "检查记忆文件..."
  
  local today
  today=$(date +%Y-%m-%d)
  
  if [[ -f "$SCRIPT_DIR/../memory/${today}.md" ]]; then
    local lines
    lines=$(wc -l < "$SCRIPT_DIR/../memory/${today}.md")
    success "今日记忆文件：${today}.md ($lines 行)"
  else
    warning "今日记忆文件未创建：${today}.md"
  fi
  
  if [[ -f "$SCRIPT_DIR/../MEMORY.md" ]]; then
    local size
    size=$(du -h "$SCRIPT_DIR/../MEMORY.md" | cut -f1)
    success "长期记忆：MEMORY.md ($size)"
  fi
}

# 8. 生成心跳报告
generate_report() {
  log "生成心跳报告..."
  
  local report_file="/tmp/heartbeat-report-$(date +%Y%m%d-%H%M%S).md"
  
  cat > "$report_file" << EOF
# 心跳检查报告

**时间**: $(date '+%Y-%m-%d %H:%M:%S')
**主机**: $(hostname)
**操作者**: 太一 AGI

## 检查结果

| 项目 | 状态 |
|------|------|
| Gateway | $(pgrep -f "openclaw gateway" > /dev/null && echo "✅ 运行中" || echo "❌ 未运行") |
| 活跃会话 | $(openclaw sessions list --limit 10 2>/dev/null | grep -c "active" || echo "0") 个 |
| 待办任务 | $(grep -c "^\- \[ \]" "$SCRIPT_DIR/../HEARTBEAT.md" 2>/dev/null || echo "0") 个 |
| 定时任务 | $(crontab -l 2>/dev/null | grep -c "openclaw" || echo "0") 个 |
| 内存文件 | $(ls "$SCRIPT_DIR/../memory/"*.md 2>/dev/null | wc -l) 个 |

## 系统资源

- CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 || echo "N/A")%
- 内存：$(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}' || echo "N/A")
- 磁盘：$(df -h / | tail -1 | awk '{print $5}' || echo "N/A")

## 建议

$(if ! pgrep -f "openclaw gateway" > /dev/null; then echo "- ⚠️ 启动 Gateway"; fi)
$(if [[ $(grep -c "^\- \[ \]" "$SCRIPT_DIR/../HEARTBEAT.md" 2>/dev/null || echo "0") -gt 5 ]]; then echo "- ⚠️ 待办任务较多，建议优先处理 P0 任务"; fi)

---
*报告生成：$report_file*
EOF

  success "报告已生成：$report_file"
  cat "$report_file"
}

# 9. 快速清理
cleanup() {
  log "清理临时文件..."
  
  local count=0
  
  # 清理/tmp 中的日志
  for file in /tmp/heartbeat-*.log /tmp/auto-exec-*.log; do
    if [[ -f "$file" && $(find "$file" -mtime +7) ]]; then
      rm -f "$file"
      ((count++))
    fi
  done
  
  success "清理了 $count 个旧日志文件"
}

# 10. 发送心跳消息
send_heartbeat() {
  log "发送心跳消息..."
  
  local target="${1:-@SAYELF}"
  local message="💓 心跳检查完成
  
- Gateway: $(pgrep -f "openclaw gateway" > /dev/null && echo "✅" || echo "❌")
- 会话：$(openclaw sessions list --limit 10 2>/dev/null | grep -c "active" || echo "0") 个活跃
- 待办：$(grep -c "^\- \[ \]" "$SCRIPT_DIR/../HEARTBEAT.md" 2>/dev/null || echo "0") 个
- 系统：$(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}') 内存

详情：/tmp/heartbeat-report-*.md"

  openclaw message send --target "$target" --message "$message"
  success "心跳消息已发送至 $target"
}

# 主菜单
show_menu() {
  echo ""
  echo "================================"
  echo "  HEARTBEAT CLI 快捷命令"
  echo "================================"
  echo ""
  echo "用法：$SCRIPT_NAME <命令> [参数]"
  echo ""
  echo "可用命令:"
  echo "  gateway      - 检查 Gateway 状态"
  echo "  sessions     - 检查会话状态"
  echo "  tasks        - 检查待办任务"
  echo "  channels     - 检查消息通道"
  echo "  resources    - 检查系统资源"
  echo "  cron         - 检查定时任务"
  echo "  memory       - 检查记忆文件"
  echo "  report       - 生成心跳报告"
  echo "  cleanup      - 清理临时文件"
  echo "  send [目标]  - 发送心跳消息"
  echo ""
  echo "  all          - 执行全部检查"
  echo "  help         - 显示帮助"
  echo ""
}

# 执行全部检查
check_all() {
  log "开始全面心跳检查..."
  echo ""
  
  check_gateway
  echo ""
  
  check_sessions
  echo ""
  
  check_tasks
  echo ""
  
  check_channels
  echo ""
  
  check_resources
  echo ""
  
  check_cron
  echo ""
  
  check_memory
  echo ""
  
  generate_report
  echo ""
  
  success "全面检查完成"
}

# 主逻辑
main() {
  if [[ $# -eq 0 ]]; then
    show_menu
    exit 0
  fi
  
  local command="$1"
  shift
  
  case "$command" in
    gateway)
      check_gateway
      ;;
    sessions)
      check_sessions
      ;;
    tasks)
      check_tasks
      ;;
    channels)
      check_channels
      ;;
    resources)
      check_resources
      ;;
    cron)
      check_cron
      ;;
    memory)
      check_memory
      ;;
    report)
      generate_report
      ;;
    cleanup)
      cleanup
      ;;
    send)
      send_heartbeat "$@"
      ;;
    all)
      check_all
      ;;
    help|--help|-h)
      show_menu
      ;;
    *)
      error "未知命令：$command"
      show_menu
      exit 1
      ;;
  esac
}

main "$@"
