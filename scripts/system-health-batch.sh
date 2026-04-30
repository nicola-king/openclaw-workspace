#!/bin/bash
# 太一系统健康批量任务 - 合并系统级监控
# 替代: cron-diagnose + system-selfcheck + protect-crontab + gateway-guard
# 执行频率: 每 2 小时

cd /home/nicola/.openclaw/workspace

LOG_FILE="logs/system-health-batch.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] === 系统健康批量任务启动 ===" >> "$LOG_FILE"

# 1. Gateway 守护
if ! pgrep -f openclaw-gateway > /dev/null 2>&1; then
    echo "[$TIMESTAMP] ⚠️ Gateway 未运行，尝试启动..." >> "$LOG_FILE"
    sudo systemctl start openclaw-gateway.service 2>&1 >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] ✓ Gateway 运行正常" >> "$LOG_FILE"
fi

# 2. Cron 诊断修复
if [ -f "scripts/cron-diagnose-fix.py" ]; then
    /usr/bin/python3 scripts/cron-diagnose-fix.py >> logs/cron-diagnose.log 2>&1
    echo "[$TIMESTAMP] ✓ Cron 诊断完成" >> "$LOG_FILE"
fi

# 3. 系统自检
if [ -f "scripts/system-cron-selfcheck.py" ]; then
    /usr/bin/python3 scripts/system-cron-selfcheck.py >> logs/system-selfcheck.log 2>&1
    echo "[$TIMESTAMP] ✓ 系统自检完成" >> "$LOG_FILE"
fi

# 4. Crontab 保护
if [ -f "scripts/protect-crontab.sh" ]; then
    bash scripts/protect-crontab.sh >> logs/crontab-protection.log 2>&1
    echo "[$TIMESTAMP] ✓ Crontab 保护完成" >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] === 系统健康批量任务结束 ===" >> "$LOG_FILE"
