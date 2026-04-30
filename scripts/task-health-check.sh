#!/bin/bash
# 定时任务健康检查脚本
# 用途：每小时检查所有定时任务状态，发现异常立即告警

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$SCRIPT_DIR/.."
LOG_FILE="$WORKSPACE/logs/task-health-$(date +%Y%m%d).log"
STATUS_FILE="/tmp/task-health-status.json"
ALERT_FILE="/tmp/task-health-alert.json"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

alert() {
    local level=$1
    local message=$2
    echo "{\"level\": \"$level\", \"message\": \"$message\", \"time\": \"$(date -Iseconds)\"}" > "$ALERT_FILE"
    log "${RED}[ALERT $level]${NC} $message"
}

check_task_health() {
    log "开始检查定时任务健康状态..."
    
    local total_tasks=0
    local healthy_tasks=0
    local warning_tasks=0
    local error_tasks=0
    
    # 读取任务配置
    if [ ! -f ~/.openclaw/cron/jobs.json ]; then
        alert "P0" "任务配置文件不存在"
        return 1
    fi
    
    # 解析任务状态
    python3 << 'EOF'
import json
import sys
from datetime import datetime, timedelta

now = datetime.now()
now_ms = now.timestamp() * 1000

with open('/home/nicola/.openclaw/cron/jobs.json', 'r') as f:
    data = json.load(f)

jobs = data.get('jobs', [])
total = len(jobs)
healthy = 0
warning = 0
error = 0

issues = []

for job in jobs:
    name = job.get('name', 'unknown')
    enabled = job.get('enabled', False)
    state = job.get('state', {})
    errors = state.get('consecutiveErrors', 0)
    last_run_ms = state.get('lastRunAtMs', 0)
    next_run_ms = state.get('nextRunAtMs', 0)
    last_status = state.get('lastStatus', 'unknown')
    
    # 检查是否启用
    if not enabled:
        issues.append(f"{name}: 未启用")
        error += 1
        continue
    
    # 检查错误计数
    if errors >= 3:
        issues.append(f"{name}: 连续错误{errors}次")
        error += 1
        continue
    
    # 检查是否超时未执行
    if last_run_ms > 0:
        last_run = datetime.fromtimestamp(last_run_ms / 1000)
        age = now - last_run
        
        # 根据任务频率判断是否超时
        schedule = job.get('schedule', {}).get('expr', '')
        if schedule.startswith('*/5'):  # 每 5 分钟
            if age > timedelta(minutes=15):
                issues.append(f"{name}: 超时未执行 ({age})")
                warning += 1
                continue
        elif schedule.startswith('*/10'):  # 每 10 分钟
            if age > timedelta(minutes=30):
                issues.append(f"{name}: 超时未执行 ({age})")
                warning += 1
                continue
        elif schedule.startswith('0 '):  # 每日任务
            if age > timedelta(hours=26):
                issues.append(f"{name}: 超时未执行 ({age})")
                warning += 1
                continue
    
    healthy += 1

# 输出结果
result = {
    "total": total,
    "healthy": healthy,
    "warning": warning,
    "error": error,
    "issues": issues,
    "timestamp": now.isoformat()
}

print(json.dumps(result, indent=2))

# 判断健康度
if error > 0:
    sys.exit(2)  # 严重
elif warning > 0:
    sys.exit(1)  # 警告
else:
    sys.exit(0)  # 健康
EOF
    
    return $?
}

send_notification() {
    local level=$1
    local message=$2
    
    # 写入告警文件，由 auto-exec-report.sh 统一发送
    cat >> /tmp/task-alerts-pending.jsonl << ALERT
{"level": "$level", "message": "$message", "time": "$(date -Iseconds)"}
ALERT
    
    log "告警已记录：$level - $message"
}

generate_report() {
    local health_data=$1
    
    # 生成健康报告
    python3 << EOF
import json
from datetime import datetime

health = json.loads('$health_data')

report = f"""
# 定时任务健康检查报告

> 检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 健康状态

| 指标 | 数值 |
|------|------|
| 总任务数 | {health['total']} |
| 健康任务 | {health['healthy']} |
| 警告任务 | {health['warning']} |
| 故障任务 | {health['error']} |
| 健康率 | {health['healthy']/health['total']*100:.1f}% |

## ⚠️ 问题列表

"""

if health['issues']:
    for issue in health['issues']:
        report += f"- {issue}\n"
else:
    report += "✅ 所有任务正常\n"

report += f"\n---\n*报告生成：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

with open('/tmp/task-health-report.md', 'w') as f:
    f.write(report)

print("报告已生成：/tmp/task-health-report.md")
EOF
}

# 主执行流程
main() {
    log "=========================================="
    log "定时任务健康检查开始"
    log "=========================================="
    
    # 执行健康检查
    health_data=$(check_task_health)
    check_result=$?
    
    # 生成报告
    generate_report "$health_data"
    
    # 根据结果处理
    case $check_result in
        0)
            log "${GREEN}✅ 所有任务健康${NC}"
            echo '{"status": "healthy", "time": "'$(date -Iseconds)'"}' > "$STATUS_FILE"
            ;;
        1)
            log "${YELLOW}⚠️  存在警告任务${NC}"
            echo '{"status": "warning", "time": "'$(date -Iseconds)'"}' > "$STATUS_FILE"
            send_notification "P2" "定时任务存在警告，请查看报告"
            ;;
        2)
            log "${RED}❌ 存在故障任务${NC}"
            echo '{"status": "error", "time": "'$(date -Iseconds)'"}' > "$STATUS_FILE"
            send_notification "P1" "定时任务存在故障，需要立即处理"
            ;;
        *)
            log "${RED}❌ 检查失败${NC}"
            echo '{"status": "unknown", "time": "'$(date -Iseconds)'"}' > "$STATUS_FILE"
            send_notification "P0" "定时任务健康检查失败"
            ;;
    esac
    
    log "=========================================="
    log "健康检查完成"
    log "=========================================="
}

# 执行
main "$@"
