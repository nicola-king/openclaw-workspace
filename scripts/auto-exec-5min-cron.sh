#!/bin/bash
# 自动执行保障 Cron - 每 5 分钟检查并推进任务
# 功能：任务发现 + 自动执行 + 进度追踪 + 阻塞上报

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/auto-exec-5m.log"
STATUS_FILE="/tmp/auto-exec-status.json"

# 确保日志目录存在
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "========== 自动执行检查 =========="

# 1. 读取 HEARTBEAT 待办
log "📋 读取 HEARTBEAT 待办..."
HEARTBEAT_FILE="$WORKSPACE/HEARTBEAT.md"
if [ -f "$HEARTBEAT_FILE" ]; then
    TODO_COUNT=$(grep -c "^\- \[ \]" "$HEARTBEAT_FILE" 2>/dev/null || echo "0")
    log "✅ 待办事项：$TODO_COUNT 个"
else
    log "⚠️ HEARTBEAT.md 不存在"
    TODO_COUNT=0
fi

# 2. 检查 P0 任务
log "🎯 检查 P0 任务..."
P0_COUNT=$(grep -c "TASK-.*P0\|**P0**" "$HEARTBEAT_FILE" 2>/dev/null || echo "0")
log "✅ P0 任务：$P0_COUNT 个"

# 3. 更新状态文件
log "📊 更新状态..."
cat > "$STATUS_FILE" << EOF
{
    "last_check": "$(date +%s)",
    "last_check_time": "$TIMESTAMP",
    "todo_count": $TODO_COUNT,
    "p0_count": $P0_COUNT,
    "status": "running"
}
EOF
log "✅ 状态已更新"

# 4. 触发任务执行（如果有 P0 任务）- 每小时执行一次避免过度打扰
HOUR=$(date +%H)
MINUTE=$(date +%M)
if [ "$P0_COUNT" -gt 0 ] && [ "$MINUTE" = "00" ]; then
    log "🚀 发现 P0 任务，触发执行..."
    # 读取第一个 P0 任务并执行
    FIRST_TASK=$(grep -A2 "**P0**" "$HEARTBEAT_FILE" | grep "TASK-" | head -1 | awk '{print $2}')
    if [ -n "$FIRST_TASK" ] && [ -f "$WORKSPACE/scripts/auto-exec-task.sh" ]; then
        bash "$WORKSPACE/scripts/auto-exec-task.sh" "$FIRST_TASK" >> "$LOG_FILE" 2>&1 || true
        log "✅ 任务执行完成：$FIRST_TASK"
    else
        log "⚠️ 无法提取任务或脚本不存在"
    fi
else
    log "✅ 持续监控中（下次执行：$((60-MINUTE))分钟后）"
fi

# 5. Git 提交（每 30 分钟）
MINUTE=$(date +%M)
if [ "$MINUTE" = "00" ] || [ "$MINUTE" = "30" ]; then
    log "💾 Git 提交..."
    cd "$WORKSPACE"
    if ! git diff --quiet 2>/dev/null; then
        git add -A
        git commit -m "🤖 自动执行检查 [$(date '+%Y-%m-%d %H:%M')]" >> "$LOG_FILE" 2>&1 || true
        log "✅ Git 提交完成"
    else
        log "✅ 无变更，跳过提交"
    fi
fi

log "========== 自动执行检查完成 =========="
log ""
