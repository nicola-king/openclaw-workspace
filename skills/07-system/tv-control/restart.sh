#!/bin/bash
# 电视控制 - 重启脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔄 重启太一电视控制..."
echo ""

# 停止旧进程
if pgrep -f "tv-control.*main.py" > /dev/null; then
    echo "⏹️  停止旧进程..."
    pkill -f "tv-control.*main.py"
    sleep 2
    echo "✅ 旧进程已停止"
else
    echo "⚠️  没有找到运行中的进程"
fi

echo ""
echo "🚀 启动新进程..."
bash "$SCRIPT_DIR/start.sh"
