#!/bin/bash
# 能力涌现智能监控脚本
# 每小时检查一次触发条件

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/emergence-monitor.log"

echo "[$(date)] 检查能力涌现触发条件..." >> $LOG_FILE

cd "$WORKSPACE/skills/taiyi"

# 运行状态检查
python3 emergence-trigger-v2.py status >> $LOG_FILE 2>&1

# 检查是否有触发
result=$(python3 emergence-trigger-v2.py test 2>&1)

if echo "$result" | grep -q "触发能力涌现"; then
    echo "[$(date)] 🦞 检测到能力涌现触发！" >> $LOG_FILE
    echo "$result" >> $LOG_FILE
fi

echo "[$(date)] 检查完成" >> $LOG_FILE
