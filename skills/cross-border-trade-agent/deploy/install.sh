#!/bin/bash
# install.sh - 跨境贸易 Agent 安装脚本

set -e

echo "=== 跨境贸易 Agent v9.0.0 安装 ==="

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本：$python_version"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 创建目录
echo "创建目录..."
mkdir -p logs data output/reports output/cache

# 复制配置
if [ ! -f "config.json" ]; then
    echo "创建配置文件..."
    cp config.example.json config.json
fi

echo "✅ 安装完成"
echo ""
echo "使用方法："
echo "  source venv/bin/activate"
echo "  python modules/cross-border-core/core.py"
