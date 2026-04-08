#!/bin/bash
# 定时任务每日验证脚本
# 用途：每日检查所有任务执行情况，生成日报

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$SCRIPT_DIR/.."
REPORT_FILE="$WORKSPACE/reports/task-daily-report-$(date +%Y%m%d).md"
LOG_FILE="$WORKSPACE/logs/task-verify-$(date +%Y%m%d).log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

generate_daily_report() {
    python3 << 'EOF'
import json
from datetime import datetime, timedelta

now = datetime.now()
yesterday = now - timedelta(days=1)

# 读取任务配置
with open('/home/nicola/.openclaw/cron/jobs.json', 'r') as f:
    data = json.load(f)

jobs = data.get('jobs', [])

# 统计
total = len(jobs)
enabled = sum(1 for j in jobs if j.get('enabled', False))
has_errors = sum(1 for j in jobs if j['state'].get('consecutiveErrors', 0) > 0)

# 计算健康率
health_rate = (total - has_errors) / total * 100 if total > 0 else 0

# 生成报告
report = f"""# 定时任务每日验证报告

> 日期：{now.strftime('%Y-%m-%d')} | 生成时间：{now.strftime('%H:%M:%S')}

---

## 📊 核心指标

| 指标 | 数值 | 目标 | 状态 |
|------|------|------|------|
| 总任务数 | {total} | - | - |
| 启用任务 | {enabled}/{total} | 100% | {'✅' if enabled == total else '⚠️'} |
| 健康任务 | {total - has_errors}/{total} | ≥95% | {'✅' if health_rate >= 95 else '⚠️'} |
| 健康率 | {health_rate:.1f}% | ≥95% | {'✅' if health_rate >= 95 else '⚠️'} |

---

## 📋 任务执行详情

"""

# 按通道分组
channels = {}
for job in jobs:
    ch = job.get('delivery', {}).get('channel', 'unknown')
    if ch not in channels:
        channels[ch] = []
    channels[ch].append(job)

for ch, ch_jobs in sorted(channels.items()):
    report += f"### {ch} 通道 ({len(ch_jobs)} 个任务)\n\n"
    report += "| 任务 | 状态 | 错误数 | 下次执行 |\n"
    report += "|------|------|--------|----------|\n"
    
    for job in ch_jobs[:10]:  # 最多显示 10 个
        name = job['name']
        status = '✅' if job.get('enabled') else '❌'
        errors = job['state'].get('consecutiveErrors', 0)
        next_run = job['state'].get('nextRunAtMs', 0)
        next_time = datetime.fromtimestamp(next_run/1000).strftime('%m-%d %H:%M') if next_run else 'N/A'
        
        error_mark = f"⚠️{errors}" if errors > 0 else "✅"
        report += f"| {name} | {status} | {error_mark} | {next_time} |\n"
    
    if len(ch_jobs) > 10:
        report += f"\n... 还有 {len(ch_jobs) - 10} 个任务\n"
    
    report += "\n"

# 告警统计
alert_count = 0
alert_file = '/tmp/task-alerts-pending.jsonl'
if os.path.exists(alert_file):
    with open(alert_file, 'r') as f:
        alert_count = sum(1 for _ in f)

report += f"""---

## 🔔 告警统计

| 指标 | 数值 |
|------|------|
| 今日告警 | {alert_count} |
| P0 紧急 | 0 |
| P1 严重 | 0 |
| P2 警告 | {alert_count} |

---

## ✅ 验证结论

"""

if health_rate >= 95 and enabled == total:
    report += "**✅ 所有指标正常，系统健康运行**\n"
elif health_rate >= 80:
    report += "**🟡 部分任务异常，需要关注**\n"
else:
    report += "**❌ 系统健康度低，需要立即处理**\n"

report += f"\n---\n*报告生成：{now.strftime('%Y-%m-%d %H:%M:%S')}*\n"

# 保存报告
with open('/tmp/task-daily-report.md', 'w') as f:
    f.write(report)

print(f"报告已生成：/tmp/task-daily-report.md")
print(f"健康率：{health_rate:.1f}%")
EOF
}

# 主执行流程
main() {
    log "=========================================="
    log "定时任务每日验证开始"
    log "=========================================="
    
    # 生成报告
    generate_daily_report
    
    # 移动报告到正式位置
    if [ -f /tmp/task-daily-report.md ]; then
        mv /tmp/task-daily-report.md "$REPORT_FILE"
        log "报告已保存：$REPORT_FILE"
    fi
    
    log "=========================================="
    log "每日验证完成"
    log "=========================================="
}

main "$@"
