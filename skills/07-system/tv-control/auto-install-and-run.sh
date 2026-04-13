#!/bin/bash
# 电视控制 - 自动安装并启动脚本
# 用法：bash auto-install-and-run.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/install-$(date +%Y%m%d-%H%M%S).log"

echo "========================================"
echo "🚀 太一电视控制 - 自动安装并启动"
echo "========================================"
echo ""
echo "📂 安装目录：$SCRIPT_DIR"
echo "📝 日志文件：$LOG_FILE"
echo ""

# 创建日志目录
mkdir -p "$SCRIPT_DIR/logs"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Step 1: 更新软件源
log "📦 Step 1/5: 更新软件源..."
sudo apt-get update >> "$LOG_FILE" 2>&1
log "✅ 软件源更新完成"

# Step 2: 安装系统依赖
log "🔧 Step 2/5: 安装系统依赖..."
{
    sudo apt-get install -y cec-utils >> "$LOG_FILE" 2>&1
    sudo apt-get install -y alsa-utils >> "$LOG_FILE" 2>&1
    sudo apt-get install -y x11-xserver-utils >> "$LOG_FILE" 2>&1
} || {
    log "⚠️ 部分依赖安装失败，继续..."
}
log "✅ 系统依赖安装完成"

# Step 3: 安装 Python 依赖
log "🐍 Step 3/5: 安装 Python 依赖..."
{
    pip3 install -r "$SCRIPT_DIR/requirements.txt" >> "$LOG_FILE" 2>&1
} || {
    log "⚠️ Python 依赖安装失败，尝试系统包..."
    sudo apt-get install -y python3-flask python3-yaml python3-requests >> "$LOG_FILE" 2>&1
}
log "✅ Python 依赖安装完成"

# Step 4: 测试 CEC 连接
log "📺 Step 4/5: 测试 CEC 连接..."
{
    echo "scan" | cec-client -s >> "$LOG_FILE" 2>&1
    log "✅ CEC 设备检测完成"
} || {
    log "⚠️ CEC 设备未检测到，检查电视连接"
}

# Step 5: 启动服务
log "🚀 Step 5/5: 启动电视控制服务..."

# 检查是否已在运行
if pgrep -f "tv-control.*main.py" > /dev/null; then
    log "⚠️ 服务已在运行，停止旧进程..."
    pkill -f "tv-control.*main.py" || true
    sleep 2
fi

# 后台启动
cd "$SCRIPT_DIR"
nohup python3 main.py >> "$LOG_FILE" 2>&1 &
PID=$!

sleep 3

# 检查启动状态
if ps -p $PID > /dev/null; then
    log "✅ 服务启动成功！PID: $PID"
    echo ""
    echo "========================================"
    echo "✅ 安装完成！"
    echo "========================================"
    echo ""
    echo "📺 电视控制服务已启动"
    echo "🔧 进程 ID: $PID"
    echo "📝 日志文件：$LOG_FILE"
    echo ""
    echo "📱 Telegram Bot: @taiyi_bot"
    echo "🌐 HTTP API: http://0.0.0.0:5001"
    echo ""
    echo "可用指令:"
    echo "  /tv on      - 开机"
    echo "  /tv off     - 关机"
    echo "  /tv vol+    - 音量+"
    echo "  /tv vol-    - 音量-"
    echo "  /tv mute    - 静音"
    echo "  /tv status  - 查询状态"
    echo ""
    echo "停止服务：kill $PID"
    echo "查看日志：tail -f $LOG_FILE"
    echo ""
else
    log "❌ 服务启动失败，请查看日志：$LOG_FILE"
    echo ""
    echo "========================================"
    echo "❌ 安装失败"
    echo "========================================"
    echo ""
    echo "请检查日志文件：$LOG_FILE"
    exit 1
fi
