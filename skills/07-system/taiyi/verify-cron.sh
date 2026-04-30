#!/bin/bash
echo "=== 定时任务验证 ==="
echo "Cron 任务数：$(crontab -l 2>/dev/null | grep -v '^#' | wc -l)"
echo "下次执行：23:00 太一心里感悟"
