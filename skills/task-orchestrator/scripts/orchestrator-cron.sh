#!/bin/bash
# Task Orchestrator Cron - 每 30 分钟自动检查

WORKSPACE="/home/nicola/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/task-orchestrator"

echo "=== Task Orchestrator 自动检查 ==="
echo "时间：$(date '+%Y-%m-%d %H:%M')"

# 1. 扫描任务
python3 "$SKILL_DIR/task-tracker.py" scan

# 2. 检测异常
python3 "$SKILL_DIR/correction.py" detect

# 3. Cron 保护检查 (🆕)
bash "$WORKSPACE/scripts/protect-crontab.sh"

# 4. Skills 心跳检查 (🆕)
bash "$WORKSPACE/scripts/skill-heartbeat.sh"

# 5. 生成报告
python3 "$SKILL_DIR/task-tracker.py" report
python3 "$SKILL_DIR/orchestrator.py" summary

echo "=== 检查完成 ==="
