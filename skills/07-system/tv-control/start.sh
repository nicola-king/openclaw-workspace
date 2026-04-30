#!/bin/bash
# 电视控制 - 一键启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 启动太一电视控制..."
echo ""

# 检查是否已在运行
if pgrep -f "tv-control.*main.py" > /dev/null; then
    echo "⚠️  服务已在运行"
    ps aux | grep "tv-control.*main.py" | grep -v grep
    echo ""
    echo "停止服务：pkill -f 'tv-control.*main.py'"
    echo "重启服务：bash $SCRIPT_DIR/restart.sh"
    exit 0
fi

# 启动服务
cd "$SCRIPT_DIR"
nohup python3 main.py >> logs/tv-control.log 2>&1 &
PID=$!

sleep 2

# 检查启动状态
if ps -p $PID > /dev/null; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "进程 ID: $PID"
    echo "日志文件：logs/tv-control.log"
    echo ""
    echo "Telegram Bot: @taiyi_bot"
    echo "HTTP API: http://0.0.0.0:5001"
    echo ""
    echo "停止服务：kill $PID"
    echo "查看日志：tail -f logs/tv-control.log"
else
    echo "❌ 服务启动失败"
    echo "查看日志：tail -logs/tv-control.log"
    exit 1
fi
