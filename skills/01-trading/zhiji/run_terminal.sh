#!/bin/bash
# 知几-E 交易终端启动脚本
# 用法：./run_terminal.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$HOME/.openclaw/workspace/logs/zhiji"
mkdir -p "$LOG_DIR"

echo "============================================================"
echo "  知几-E 量化交易终端 v2.1"
echo "  策略：气象套利 + 鲸鱼跟随"
echo "============================================================"
echo ""
echo "📂 工作目录：$SCRIPT_DIR"
echo "📝 日志目录：$LOG_DIR"
echo ""

# 检查配置
if [ ! -f "$SCRIPT_DIR/config.example.json" ]; then
    echo "⚠️  配置文件不存在，使用默认配置..."
fi

# 检查凭证
if [ -z "$POLYMARKET_API_KEY" ]; then
    echo "⚠️  未设置 POLYMARKET_API_KEY 环境变量"
    echo "   请在 ~/.taiyi/zhiji/config.json 中配置"
fi

echo ""
echo "🚀 启动策略引擎..."
echo ""

# 运行策略
cd "$SCRIPT_DIR"
python3 strategy_v21.py 2>&1 | tee "$LOG_DIR/terminal-$(date +%Y%m%d).log"

echo ""
echo "============================================================"
echo "  策略执行完成"

# 发送通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "任务完成" "任务已执行" &
echo "============================================================"
