#!/bin/bash
# TurboQuant 压缩率监控面板 - 快速启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/home/nicola/.openclaw/workspace/logs/dashboard-server.log"

echo "🔍 TurboQuant 压缩率监控面板"
echo "================================"

# 检查是否已在运行
if pgrep -f "http.server 8888" > /dev/null; then
    echo "✓ 服务已在运行"
    ps aux | grep "http.server 8888" | grep -v grep | awk '{print "  PID:", $2}'
else
    echo "🚀 启动 HTTP 服务..."
    cd "$SCRIPT_DIR"
    nohup python3 -m http.server 8888 > "$LOG_FILE" 2>&1 &
    sleep 2
    
    if pgrep -f "http.server 8888" > /dev/null; then
        echo "✓ 服务已启动"
        ps aux | grep "http.server 8888" | grep -v grep | awk '{print "  PID:", $2}'
    else
        echo "✗ 服务启动失败"
        exit 1
    fi
fi

echo ""
echo "📊 访问地址:"
echo "  本地：http://localhost:8888/compression-monitor.html"
echo "  内网：http://192.168.2.242:8888/compression-monitor.html"
echo ""
echo "📁 数据文件：$SCRIPT_DIR/compression-data.json"
echo "📝 日志文件：$LOG_FILE"
echo ""
echo "🛑 停止服务：pkill -f 'http.server 8888'"
echo "📖 查看日志：tail -f $LOG_FILE"
