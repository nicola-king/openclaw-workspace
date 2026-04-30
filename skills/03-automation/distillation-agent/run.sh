#!/bin/bash
# 太一蒸馏提炼 Agent 运行脚本
# 每周一中午 12:00 执行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/distillation-agent.log"

echo "🧬 太一蒸馏提炼 Agent 启动..."
echo "时间：$(date)"
echo "日志：$LOG_FILE"
echo ""

# 确保日志目录存在
mkdir -p "$WORKSPACE/logs"

# 执行蒸馏 Agent
python3 "$SCRIPT_DIR/distillation_agent.py" 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "✅ 蒸馏提炼完成！"
echo "时间：$(date)"
