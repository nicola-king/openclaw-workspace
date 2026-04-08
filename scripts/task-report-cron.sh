#!/bin/bash
# 定时任务结果汇报 Cron 脚本
# 频率：每日 07:00（凌晨任务完成后）、23:00（日报生成后）

cd /home/nicola/.openclaw/workspace

# 发送汇报
python3 scripts/task-result-reporter.py >> logs/task-report.log 2>&1
