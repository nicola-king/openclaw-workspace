#!/bin/bash
# 自动执行保障机制 - 每 5 分钟进度汇报
# 用法：添加到 crontab: */5 * * * * bash /home/nicola/.openclaw/workspace/scripts/auto-exec-cron.sh

WORKSPACE="/home/nicola/.openclaw/workspace"
STATUS_FILE="/tmp/auto-exec-status.json"
LOG_FILE="$WORKSPACE/logs/auto-exec-cron.log"
REPORT_SCRIPT="$WORKSPACE/scripts/auto-exec-report.py"

# 创建日志目录
mkdir -p "$WORKSPACE/logs"

# 记录执行时间
echo "=== Auto-Exec Cron: $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# 检查 Gateway 状态
GATEWAY_PID=$(pgrep -f "openclaw gateway" || echo "")
if [ -z "$GATEWAY_PID" ]; then
    echo "⚠️ Gateway 未运行，尝试重启..." >> "$LOG_FILE"
    cd "$WORKSPACE" && openclaw gateway start >> "$LOG_FILE" 2>&1
else
    echo "✅ Gateway 运行中 (PID: $GATEWAY_PID)" >> "$LOG_FILE"
fi

# 更新状态文件
cat > "$STATUS_FILE" << EOF
{
    "last_check": "$(date +%s)",
    "last_check_time": "$(date '+%Y-%m-%d %H:%M:%S')",
    "gateway_pid": "$GATEWAY_PID",
    "status": "running",
    "auto_exec_activated": true
}
EOF

# 生成并发送进度汇报（如果有任务在执行）
if [ -f "$REPORT_SCRIPT" ]; then
    python3 "$REPORT_SCRIPT" --check-only >> "$LOG_FILE" 2>&1
fi

echo "✅ Auto-Exec Cron 完成" >> "$LOG_FILE"
