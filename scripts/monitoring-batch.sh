#!/bin/bash
# 太一监控批量任务 - 合并同类项，降低系统负载
# 替代: check-bailian-quota + cron-watchdog + auto-exec-cron + price-alert + polymarket
# 执行频率: 每 30 分钟

cd /home/nicola/.openclaw/workspace

LOG_FILE="logs/monitoring-batch.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] === 监控批量任务启动 ===" >> "$LOG_FILE"

# 1. 百炼配额监控
if [ -f "scripts/check-bailian-quota.py" ]; then
    /usr/bin/python3 scripts/check-bailian-quota.py >> logs/model-router.log 2>&1
    echo "[$TIMESTAMP] ✓ 百炼配额监控完成" >> "$LOG_FILE"
fi

# 2. 自动执行 Cron
if [ -f "scripts/auto-exec-cron.sh" ]; then
    bash scripts/auto-exec-cron.sh >> logs/auto-exec-cron.log 2>&1
    echo "[$TIMESTAMP] ✓ 自动执行 Cron 完成" >> "$LOG_FILE"
fi

# 3. 价格告警
if [ -f "scripts/price-alert-cron.sh" ]; then
    bash scripts/price-alert-cron.sh >> logs/price-alert.log 2>&1
    echo "[$TIMESTAMP] ✓ 价格告警完成" >> "$LOG_FILE"
fi

# 4. Polymarket 数据 + 热度监测
if [ -f "scripts/polymarket-data-cron.sh" ]; then
    bash scripts/polymarket-data-cron.sh >> logs/polymarket-data.log 2>&1
    echo "[$TIMESTAMP] ✓ Polymarket 数据完成" >> "$LOG_FILE"
fi

if [ -f "scripts/polymarket-hot-weather-cron.sh" ]; then
    bash scripts/polymarket-hot-weather-cron.sh >> logs/polymarket-hot-weather.log 2>&1
    echo "[$TIMESTAMP] ✓ Polymarket 热度完成" >> "$LOG_FILE"
fi

# 5. Cron 看门狗
if [ -f "scripts/cron-watchdog.sh" ]; then
    bash scripts/cron-watchdog.sh >> logs/cron-alerts.log 2>&1
    echo "[$TIMESTAMP] ✓ Cron 看门狗完成" >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] === 监控批量任务结束 ===" >> "$LOG_FILE"
