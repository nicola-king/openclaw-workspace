#!/bin/bash
# OpenClaw 自检自愈脚本 (v2.0)
# 每 30 分钟自动执行健康检查和自愈

set -e

WORKSPACE=~/.openclaw/workspace
LOG_DIR=$WORKSPACE/logs
MEMORY_DIR=$WORKSPACE/memory
TIMESTAMP=$(date +%Y%m%d_%H%M)
LOG_FILE=$LOG_DIR/self-heal-$(date +%Y%m%d).log
REPORT_FILE=$MEMORY_DIR/self-heal-report.json

# 创建目录
mkdir -p $LOG_DIR $MEMORY_DIR

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

log "========== 自检自愈开始 =========="

# 初始化报告
cat > $REPORT_FILE << EOF
{
  "timestamp": "$(date -Iseconds)",
  "checks": [],
  "issues": [],
  "actions": [],
  "status": "healthy"
}
EOF

# 检查项计数器
CHECKS=0
ISSUES=0
ACTIONS=0

# 1. Gateway 进程检查
log "检查 Gateway 进程..."
CHECKS=$((CHECKS + 1))
if ! pgrep -f "openclaw-gateway" > /dev/null; then
    log "❌ Gateway 未运行，尝试重启..."
    cd $WORKSPACE && openclaw gateway restart
    ACTIONS=$((ACTIONS + 1))
    log "✅ Gateway 已重启"
    
    # 更新报告
    jq --arg ts "$(date -Iseconds)" \
       '.checks += [{"name": "gateway", "status": "restarted", "time": $ts}] |
        .actions += [{"action": "restart_gateway", "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
else
    PID=$(pgrep -f "openclaw-gateway" | head -1)
    log "✅ Gateway 运行中 (PID: $PID)"
    
    jq --arg ts "$(date -Iseconds)" --arg pid "$PID" \
       '.checks += [{"name": "gateway", "status": "running", "pid": $pid, "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
fi

# 2. 残留进程检查
log "检查残留进程..."
CHECKS=$((CHECKS + 1))
STALE=$(ps aux | grep -E 'openclaw|gateway' | grep -v grep | grep -v 'openclaw-gateway' | wc -l)
if [ $STALE -gt 0 ]; then
    log "⚠️ 发现 $STALE 个残留进程"
    ps aux | grep -E 'openclaw|gateway' | grep -v grep | grep -v 'openclaw-gateway' | awk '{print $2}' | xargs kill -9 2>/dev/null || true
    ACTIONS=$((ACTIONS + 1))
    log "✅ 已清理残留进程"
    
    jq --arg ts "$(date -Iseconds)" --argjson stale "$STALE" \
       '.checks += [{"name": "stale_processes", "count": $stale, "time": $ts}] |
        .actions += [{"action": "kill_stale_processes", "count": $stale, "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
else
    log "✅ 无残留进程"
    
    jq --arg ts "$(date -Iseconds)" \
       '.checks += [{"name": "stale_processes", "count": 0, "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
fi

# 3. 磁盘空间检查
log "检查磁盘空间..."
CHECKS=$((CHECKS + 1))
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ $DISK_USAGE -gt 90 ]; then
    log "❌ 磁盘空间不足 (${DISK_USAGE}%)"
    ISSUES=$((ISSUES + 1))
    
    jq --arg ts "$(date -Iseconds)" --arg usage "${DISK_USAGE}%" \
       '.checks += [{"name": "disk_space", "usage": $usage, "time": $ts}] |
        .issues += [{"type": "disk_space", "usage": $usage, "time": $ts}] |
        .status = "warning"' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
else
    log "✅ 磁盘空间正常 (${DISK_USAGE}%)"
    
    jq --arg ts "$(date -Iseconds)" --arg usage "${DISK_USAGE}%" \
       '.checks += [{"name": "disk_space", "usage": $usage, "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
fi

# 4. 宪法文件完整性检查
log "检查宪法文件..."
CHECKS=$((CHECKS + 1))
CONSTITUTION_FILES=(
    "constitution/CONST-ROUTER.md"
    "constitution/axiom/VALUE-FOUNDATION.md"
    "constitution/directives/NEGENTROPY.md"
    "SOUL.md"
)

MISSING=0
for file in "${CONSTITUTION_FILES[@]}"; do
    if [ ! -f "$WORKSPACE/$file" ]; then
        log "❌ 缺失：$file"
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -gt 0 ]; then
    log "❌ 缺失 $MISSING 个宪法文件"
    ISSUES=$((ISSUES + 1))
    
    jq --arg ts "$(date -Iseconds)" --argjson missing "$MISSING" \
       '.checks += [{"name": "constitution", "missing": $missing, "time": $ts}] |
        .issues += [{"type": "constitution_missing", "count": $missing, "time": $ts}] |
        .status = "warning"' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
else
    log "✅ 宪法文件完整"
    
    jq --arg ts "$(date -Iseconds)" \
       '.checks += [{"name": "constitution", "status": "complete", "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
fi

# 5. Git 状态检查
log "检查 Git 状态..."
CHECKS=$((CHECKS + 1))
cd $WORKSPACE
UNCOMMITTED=$(git status --porcelain | wc -l)
if [ $UNCOMMITTED -gt 0 ]; then
    log "⚠️ 有 $UNCOMMITTED 个未提交文件"
    
    jq --arg ts "$(date -Iseconds)" --argjson uncommitted "$UNCOMMITTED" \
       '.checks += [{"name": "git_status", "uncommitted": $uncommitted, "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
else
    log "✅ Git 工作区干净"
    
    jq --arg ts "$(date -Iseconds)" \
       '.checks += [{"name": "git_status", "uncommitted": 0, "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
fi

# 6. 内存使用检查
log "检查内存使用..."
CHECKS=$((CHECKS + 1))
MEM_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')
if [ $MEM_USAGE -gt 90 ]; then
    log "❌ 内存使用过高 (${MEM_USAGE}%)"
    ISSUES=$((ISSUES + 1))
    
    jq --arg ts "$(date -Iseconds)" --arg usage "${MEM_USAGE}%" \
       '.checks += [{"name": "memory", "usage": $usage, "time": $ts}] |
        .issues += [{"type": "memory_high", "usage": $usage, "time": $ts}] |
        .status = "warning"' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
else
    log "✅ 内存使用正常 (${MEM_USAGE}%)"
    
    jq --arg ts "$(date -Iseconds)" --arg usage "${MEM_USAGE}%" \
       '.checks += [{"name": "memory", "usage": $usage, "time": $ts}]' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
fi

# 更新最终状态
if [ $ISSUES -gt 0 ]; then
    jq --argjson issues "$ISSUES" \
       '.status = "warning" | .issues_count = $issues' \
       $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
    log "⚠️ 自检完成：发现 $ISSUES 个问题"
else
    jq '.status = "healthy"' $REPORT_FILE > /tmp/report.json && mv /tmp/report.json $REPORT_FILE
    log "✅ 自检完成：系统健康"
fi

log "检查项：$CHECKS | 问题：$ISSUES | 操作：$ACTIONS"
log "报告：$REPORT_FILE"
log "日志：$LOG_FILE"
log "========== 自检自愈完成 =========="

# 返回状态码
if [ $ISSUES -gt 0 ]; then
    exit 1
else
    exit 0
fi
