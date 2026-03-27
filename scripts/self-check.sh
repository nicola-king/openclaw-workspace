#!/bin/bash
# OpenClaw 系统自检脚本
set -e
LOG_FILE="$HOME/.openclaw/workspace/logs/self-check.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }
check_pass() { log "✅ $1"; }
check_warn() { log "⚠️  $1"; }
check_fail() { log "❌ $1"; }

echo "======================================" | tee "$LOG_FILE"
echo "  OpenClaw 系统自检" | tee -a "$LOG_FILE"
echo "  $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "======================================" | tee -a "$LOG_FILE"

# 1. Gateway
log "【1/6】Gateway 状态..."
if openclaw gateway status 2>&1 | grep -q "running"; then
    check_pass "Gateway 运行正常"
else
    check_fail "Gateway 未运行"
fi

# 2. Cron
log "【2/6】Cron 任务..."
CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "openclaw" || echo "0")
if [ "$CRON_COUNT" -gt 0 ]; then
    check_pass "Cron 任务：$CRON_COUNT 个"
else
    check_warn "无 Cron 任务"
fi

# 3. 技能
log "【3/6】技能文件..."
SKILL_COUNT=$(find "$HOME/.openclaw/workspace/skills" -name "SKILL.md" 2>/dev/null | wc -l)
check_pass "技能文件：$SKILL_COUNT 个"

# 4. 宪法
log "【4/6】宪法文件..."
CONST_COUNT=$(find "$HOME/.openclaw/workspace/constitution" -name "*.md" 2>/dev/null | wc -l)
check_pass "宪法文件：$CONST_COUNT 个"

# 5. 磁盘
log "【5/6】磁盘空间..."
DISK=$(df -h "$HOME" | awk 'NR==2 {print $5}')
check_pass "磁盘使用：$DISK"

# 6. Git
log "【6/6】Git 状态..."
cd "$HOME/.openclaw/workspace"
if git status --porcelain 2>&1 | grep -q "nothing to commit"; then
    check_pass "Git 工作区干净"
else
    UNCOMMITTED=$(git status --porcelain | wc -l)
    check_warn "有 $UNCOMMITTED 个未提交文件"
fi

echo "======================================" | tee -a "$LOG_FILE"
echo "  自检完成" | tee -a "$LOG_FILE"
echo "======================================" | tee -a "$LOG_FILE"
