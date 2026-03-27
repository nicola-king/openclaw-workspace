#!/bin/bash
# 采集框架安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 开始安装多平台内容采集框架..."
echo ""

# 1. 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip install playwright loguru pandas --break-system-packages --quiet
echo "✅ Python 依赖安装完成"

# 2. 安装 Playwright 浏览器
echo "🌐 安装 Chromium 浏览器..."
playwright install chromium
echo "✅ Chromium 安装完成"

# 3. 创建输出目录
echo "📁 创建输出目录..."
mkdir -p output/{raw,processed,logs,reports}
echo "✅ 目录创建完成"

# 4. 添加定时任务
echo "⏰ 配置 OpenClaw 定时任务..."
CRON_CONFIG="config/openclaw-cron.json"
if [ -f "$CRON_CONFIG" ]; then
    echo "   定时任务配置：$CRON_CONFIG"
    echo "   运行以下命令添加定时任务:"
    echo "   openclaw cron add $CRON_CONFIG"
else
    echo "⚠️ 未找到定时任务配置"
fi

# 5. 测试运行
echo ""
echo "🧪 运行测试..."
bash run.sh test

echo ""
echo "================================"
echo "✅ 安装完成！"
echo "================================"
echo ""
echo "快速开始:"
echo "  bash run.sh test    # 测试采集器"
echo "  bash run.sh x       # 采集 X 平台"
echo "  bash run.sh all     # 采集所有平台"
echo ""
echo "配置采集目标:"
echo "  编辑 config/targets.json"
echo ""
echo "添加定时任务:"
echo "  openclaw cron add config/openclaw-cron.json"
echo ""
