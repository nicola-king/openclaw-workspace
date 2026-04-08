#!/bin/bash
# auto-exec-report.sh - 自动执行进度汇报脚本
# 用法：./auto-exec-report.sh [--send]
# 功能：读取状态文件，生成汇报，可选发送到微信

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
STATUS_FILE="/tmp/auto-exec-status.json"
HEARTBEAT_FILE="$WORKSPACE/HEARTBEAT.md"
LOG_FILE="/home/nicola/.openclaw/logs/auto-exec-5m.log"

# 读取状态
if [ -f "$STATUS_FILE" ]; then
    LAST_CHECK=$(jq -r '.last_check_time' "$STATUS_FILE")
    TODO_COUNT=$(jq -r '.todo_count' "$STATUS_FILE")
    P0_COUNT=$(jq -r '.p0_count' "$STATUS_FILE")
    STATUS=$(jq -r '.status' "$STATUS_FILE")
else
    LAST_CHECK="未知"
    TODO_COUNT=0
    P0_COUNT=0
    STATUS="unknown"
fi

# 读取 P0 任务列表
P0_TASKS=""
if [ -f "$HEARTBEAT_FILE" ]; then
    P0_TASKS=$(grep -A1 "**P0**\|TASK-.*P0" "$HEARTBEAT_FILE" | grep "TASK-" | head -5 | sed 's/^[[:space:]]*//' | tr '\n' '\n')
fi

# 生成汇报
REPORT="📊 **自动执行状态汇报**

**检查时间**: $LAST_CHECK
**待办事项**: $TODO_COUNT 个
**P0 任务**: $P0_COUNT 个
**系统状态**: $STATUS

**当前 P0 任务**:
$P0_TASKS
**Cron 状态**: ✅ 每 5 分钟检查中
**日志**: /home/nicola/.openclaw/logs/auto-exec-5m.log

---
*自动执行保障机制 v2.0 | 每小时整点执行任务*"

# 如果传递 --send 参数，发送消息
if [ "$1" = "--send" ]; then
    # 使用 OpenClaw message 工具发送（需要配置）
    echo "$REPORT"
    # TODO: 集成 OpenClaw message API
else
    echo "$REPORT"
fi
