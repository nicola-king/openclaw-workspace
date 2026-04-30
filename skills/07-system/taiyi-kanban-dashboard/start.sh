#!/bin/bash
# 太一看板 Dashboard 启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🌟 太一看板 Dashboard 启动中..."
echo ""

# 检查依赖
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装"
    exit 1
fi

# 检查 Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask 未安装，正在安装..."
    pip3 install flask flask-cors --break-system-packages -q
fi

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "⚠️  依赖未安装，正在安装..."
    npm install
fi

# 构建前端 (如果 dist 不存在)
if [ ! -d "dist" ]; then
    echo "🔨 构建前端..."
    npm run build
fi

# 启动 API 服务器
echo ""
echo "✅ 启动 API 服务器..."
echo "🌐 访问地址：http://localhost:5001"
echo "📊 前端：http://localhost:5001"
echo "🔌 API: http://localhost:5001/api/*"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 api_server.py
