#!/bin/bash
# 太一任务监控脚本
# 功能：检查任务进度 + 逾期告警
# 执行：每小时自动运行

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="/home/nicola/.openclaw/logs"
TASK_FILE="$WORKSPACE/constitution/tasks/TASK-ROADMAP-2026Q2.md"
TODAY=$(date +%Y-%m-%d)

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_DIR/task-monitor.log"
}

log "═══════════════════════════════════════"
log "【任务监控】启动检查"
log "═══════════════════════════════════════"

# 检查任务文件
if [ ! -f "$TASK_FILE" ]; then
    log "❌ 任务文件不存在：$TASK_FILE"
    exit 1
fi

log "✅ 任务文件存在：TASK-ROADMAP-2026Q2.md"

# 检查当日截止任务
log "检查当日截止任务..."
if grep -q "$TODAY" "$TASK_FILE"; then
    log "🔴 发现当日截止任务！"
    grep -n "$TODAY" "$TASK_FILE" | while read line; do
        log "   $line"
    done
else
    log "✅ 无当日截止任务"
fi

# 检查逾期任务
log "检查逾期任务..."
for date in $(seq 1 7); do
    CHECK_DATE=$(date -d "$date days ago" +%Y-%m-%d)
    if [ "$CHECK_DATE" != "$TODAY" ]; then
        if grep -q "$CHECK_DATE" "$TASK_FILE"; then
            if ! grep -B5 "$CHECK_DATE" "$TASK_FILE" | grep -q "✅"; then
                log "🔴 发现逾期任务：$CHECK_DATE"
            fi
        fi
    fi
done

# 检查即将到来的截止
log "检查即将到来的截止..."
for date in $(seq 1 5); do
    CHECK_DATE=$(date -d "$date days" +%Y-%m-%d)
    if grep -q "$CHECK_DATE" "$TASK_FILE"; then
        log "🟡 $date 天后截止：$CHECK_DATE"
    fi
done

log "═══════════════════════════════════════"
log "【任务监控】检查完成"
log "═══════════════════════════════════════"

exit 0
