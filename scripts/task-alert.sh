#!/bin/bash
# 定时任务告警脚本
# 用途：发送任务故障告警通知

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$SCRIPT_DIR/.."
LOG_FILE="$WORKSPACE/logs/task-alert-$(date +%Y%m%d).log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

send_alert() {
    local level=$1
    local title=$2
    local message=$3
    
    # 写入待发送队列，由 auto-exec-report.sh 统一处理
    cat >> /tmp/task-alerts-pending.jsonl << EOF
{"level": "$level", "title": "$title", "message": "$message", "time": "$(date -Iseconds)"}
EOF
    
    log "[ALERT $level] $title - $message"
}

# 检查是否有待发送的告警
check_pending_alerts() {
    if [ -f /tmp/task-alerts-pending.jsonl ]; then
        local count=$(wc -l < /tmp/task-alerts-pending.jsonl)
        if [ $count -gt 0 ]; then
            log "发现 $count 条待发送告警"
            return 0
        fi
    fi
    return 1
}

# 主执行流程
main() {
    log "=========================================="
    log "定时任务告警检查"
    log "=========================================="
    
    if check_pending_alerts; then
        log "告警将通过 auto-exec-report.sh 统一发送"
    else
        log "✅ 无待发送告警"
    fi
    
    log "=========================================="
}

main "$@"
