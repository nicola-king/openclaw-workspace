#!/bin/bash
# 自进化蒸馏提炼 Agent v2.0 运行脚本
# 每周日 12:00 执行 (额外自进化蒸馏)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/self-evolving-distillation.log"

echo "🧬 自进化蒸馏提炼 Agent v2.0 启动..."
echo "时间：$(date)"
echo "日志：$LOG_FILE"
echo ""

# 确保日志目录存在
mkdir -p "$WORKSPACE/logs"

# 执行自进化蒸馏 Agent
python3 "$SCRIPT_DIR/self_evolution_distillation_agent.py" 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "✅ 自进化蒸馏提炼完成！"
echo "时间：$(date)"
