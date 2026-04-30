#!/bin/bash
# OpenClaw 系统自检自愈脚本
# 功能：系统健康检查 + 自动修复
# 用法：bash /tmp/openclaw-watchdog.sh [--auto-heal]

set -e

LOG_DIR="/home/nicola/.openclaw/workspace/logs"
LOG_FILE="$LOG_DIR/watchdog-$(date +%Y-%m-%d).log"
STATE_FILE="/tmp/openclaw-watchdog-state.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[$timestamp] $1" | tee -a "$LOG_FILE"
}

check_gateway() {
    log "${BLUE}检查 Gateway 状态...${NC}"
    if curl -s http://127.0.0.1:18789/ > /dev/null 2>&1; then
        log "${GREEN}✅ Gateway 运行正常 (18789)${NC}"
        return 0
    else
        log "${RED}❌ Gateway 未响应${NC}"
        return 1
    fi
}

check_dashboard() {
    log "${BLUE}检查 Dashboard 状态...${NC}"
    if curl -s http://127.0.0.1:5001/ > /dev/null 2>&1; then
        log "${GREEN}✅ 太一 Dashboard 运行正常 (5001)${NC}"
        return 0
    else
        log "${YELLOW}⚠️  太一 Dashboard 未运行${NC}"
        return 1
    fi
}

check_disk() {
    log "${BLUE}检查磁盘空间...${NC}"
    local usage=$(df /home | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$usage" -lt 80 ]; then
        log "${GREEN}✅ 磁盘健康：${usage}%${NC}"
        return 0
    elif [ "$usage" -lt 90 ]; then
        log "${YELLOW}⚠️  磁盘警告：${usage}%${NC}"
        return 1
    else
        log "${RED}❌ 磁盘危急：${usage}%${NC}"
        return 2
    fi
}

check_github_auth() {
    log "${BLUE}检查 GitHub 认证...${NC}"
    if gh auth status > /dev/null 2>&1; then
        log "${GREEN}✅ GitHub 已登录${NC}"
        return 0
    else
        log "${RED}❌ GitHub 未登录${NC}"
        return 1
    fi
}

check_memory_files() {
    log "${BLUE}检查记忆系统...${NC}"
    local required_files=("core.md" "context.md" "evolution.md" "residual.md")
    local missing=0
    for file in "${required_files[@]}"; do
        if [ ! -f "/home/nicola/.openclaw/workspace/memory/$file" ]; then
            log "${YELLOW}⚠️  缺失：memory/$file${NC}"
            missing=$((missing + 1))
        fi
    done
    if [ $missing -eq 0 ]; then
        log "${GREEN}✅ 记忆系统完整${NC}"
        return 0
    else
        log "${YELLOW}⚠️  缺失 $missing 个文件${NC}"
        return 1
    fi
}

check_constitution() {
    log "${BLUE}检查宪法完整性...${NC}"
    if [ -d "/home/nicola/.openclaw/workspace/constitution" ]; then
        local file_count=$(ls /home/nicola/.openclaw/workspace/constitution/*.md 2>/dev/null | wc -l)
        if [ "$file_count" -gt 10 ]; then
            log "${GREEN}✅ 宪法完整：$file_count 个核心文件${NC}"
            return 0
        fi
    fi
    log "${RED}❌ 宪法不完整${NC}"
    return 1
}

check_skills() {
    log "${BLUE}检查技能系统...${NC}"
    local skill_count=$(ls /home/nicola/.openclaw/workspace/skills/ 2>/dev/null | wc -l)
    if [ "$skill_count" -gt 20 ]; then
        log "${GREEN}✅ 技能系统正常：$skill_count 个分类${NC}"
        return 0
    else
        log "${YELLOW}⚠️  技能数量异常：$skill_count${NC}"
        return 1
    fi
}

check_redundant_processes() {
    log "${BLUE}检查冗余进程...${NC}"
    local count=$(ps aux | grep dashboard-auto-manager | grep -v grep | wc -l)
    if [ "$count" -le 2 ]; then
        log "${GREEN}✅ 进程正常：$count 个${NC}"
        return 0
    else
        log "${YELLOW}⚠️  发现冗余进程：$count 个${NC}"
        return 1
    fi
}

heal_gateway() {
    log "${BLUE}🔧 尝试修复 Gateway...${NC}"
    openclaw gateway restart 2>&1 | tee -a "$LOG_FILE"
    sleep 5
    if check_gateway; then
        log "${GREEN}✅ Gateway 修复成功${NC}"
        return 0
    else
        log "${RED}❌ Gateway 修复失败${NC}"
        return 1
    fi
}

heal_dashboard() {
    log "${BLUE}🔧 尝试启动 Dashboard...${NC}"
    bash /home/nicola/.openclaw/workspace/scripts/dashboard-auto-manager.sh open 2>&1 | tee -a "$LOG_FILE"
    sleep 3
    if check_dashboard; then
        log "${GREEN}✅ Dashboard 启动成功${NC}"
        return 0
    else
        log "${RED}❌ Dashboard 启动失败${NC}"
        return 1
    fi
}

heal_redundant_processes() {
    log "${BLUE}🔧 清理冗余进程...${NC}"
    ps aux | grep dashboard-auto-manager | grep -v grep | awk '{print $2}' | tail -n +2 | xargs -I {} kill -9 {} 2>/dev/null || true
    local count=$(ps aux | grep dashboard-auto-manager | grep -v grep | wc -l)
    log "${GREEN}✅ 保留 $count 个进程${NC}"
    return 0
}

run_health_check() {
    local score=0
    local total=8
    check_gateway && score=$((score + 1)) || true
    check_dashboard && score=$((score + 1)) || true
    check_disk && score=$((score + 1)) || true
    check_github_auth && score=$((score + 1)) || true
    check_memory_files && score=$((score + 1)) || true
    check_constitution && score=$((score + 1)) || true
    check_skills && score=$((score + 1)) || true
    check_redundant_processes && score=$((score + 1)) || true
    
    local percentage=$((score * 100 / total))
    echo ""
    log "=========================================="
    if [ $percentage -ge 90 ]; then
        log "${GREEN}🏥 系统健康度：${percentage}%${NC}"
    elif [ $percentage -ge 70 ]; then
        log "${YELLOW}🏥 系统健康度：${percentage}%${NC}"
    else
        log "${RED}🏥 系统健康度：${percentage}%${NC}"
    fi
    log "得分：$score / $total"
    log "=========================================="
    echo "{\"timestamp\":\"$(date -Iseconds)\",\"score\":$score,\"total\":$total,\"percentage\":$percentage}" > "$STATE_FILE"
    return $((total - score))
}

run_auto_heal() {
    log "${BLUE}🔧 开始自动修复...${NC}"
    check_gateway || heal_gateway
    check_dashboard || heal_dashboard
    check_redundant_processes || heal_redundant_processes
    log "${GREEN}✅ 自动修复完成${NC}"
    run_health_check
}

show_status() {
    echo ""
    echo "=========================================="
    echo "       太一系统自检报告"
    echo "=========================================="
    echo ""
    if curl -s http://127.0.0.1:18789/ > /dev/null 2>&1; then
        echo "Gateway:        ✅ 运行中 (18789)"
    else
        echo "Gateway:        ❌ 未运行"
    fi
    if curl -s http://127.0.0.1:5001/ > /dev/null 2>&1; then
        echo "Dashboard:      ✅ 运行中 (5001)"
    else
        echo "Dashboard:      ⚪ 未运行"
    fi
    local disk_usage=$(df /home | tail -1 | awk '{print $5}')
    echo "磁盘空间：      $disk_usage"
    if gh auth status > /dev/null 2>&1; then
        echo "GitHub 认证：   ✅ 已登录"
    else
        echo "GitHub 认证：   ❌ 未登录"
    fi
    local memory_files=$(ls /home/nicola/.openclaw/workspace/memory/*.md 2>/dev/null | wc -l)
    echo "记忆文件：      $memory_files 个"
    local skills=$(ls /home/nicola/.openclaw/workspace/skills/ 2>/dev/null | wc -l)
    echo "技能分类：      $skills 个"
    local constitution=$(ls /home/nicola/.openclaw/workspace/constitution/*.md 2>/dev/null | wc -l)
    echo "宪法文件：      $constitution 个"
    local redundant=$(ps aux | grep dashboard-auto-manager | grep -v grep | wc -l)
    echo "Dashboard 进程： $redundant 个"
    echo ""
    echo "=========================================="
}

case "${1:-check}" in
    check|--check|-c)
        log "🛡️  太一系统自检开始..."
        run_health_check
        ;;
    heal|--heal|-h)
        log "🔧 太一系统自愈开始..."
        run_auto_heal
        ;;
    status|--status|-s)
        show_status
        ;;
    *)
        echo "太一系统自检自愈脚本"
        echo ""
        echo "用法：$0 {check|heal|status}"
        echo ""
        echo "命令说明:"
        echo "  check  - 健康检查 (默认)"
        echo "  heal   - 自动修复 + 健康检查"
        echo "  status - 快速状态查看"
        ;;
esac
