#!/bin/bash
# 电视控制 - 停止脚本

echo "⏹️  停止太一电视控制..."
echo ""

# 停止进程
if pgrep -f "tv-control.*main.py" > /dev/null; then
    pkill -f "tv-control.*main.py"
    echo "✅ 服务已停止"
else
    echo "⚠️  没有找到运行中的进程"
fi

echo ""
echo "启动服务：bash start.sh"
