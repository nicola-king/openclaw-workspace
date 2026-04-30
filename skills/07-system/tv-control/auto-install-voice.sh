#!/bin/bash
# 语音控制 - 自动安装并启动

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo "🎤 语音控制电视 - 自动安装"
echo "========================================"
echo ""

# Step 1: 安装系统依赖
echo "📦 Step 1/3: 安装系统依赖..."
sudo apt-get update
sudo apt-get install -y python3-pyaudio portaudio19-dev espeak espeak-data libespeak-dev

# Step 2: 安装 Python 依赖
echo "🐍 Step 2/3: 安装 Python 依赖..."
pip3 install vosk

# Step 3: 下载语音模型
echo "📦 Step 3/3: 下载语音模型..."
cd "$SCRIPT_DIR"
mkdir -p models
cd models

if [ ! -d "vosk-model-cn-0.15" ]; then
    echo "下载 Vosk 中文模型 (约 40MB)..."
    wget -q --show-progress https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip
    unzip -q vosk-model-cn-0.15.zip
    rm vosk-model-cn-0.15.zip
    echo "✅ 模型下载完成"
else
    echo "✅ 模型已存在"
fi

echo ""
echo "========================================"
echo "✅ 语音控制安装完成！"
echo "========================================"
echo ""
echo "启动语音控制："
echo "  cd $SCRIPT_DIR"
echo "  python3 voice-control.py"
echo ""
echo "唤醒词：电视，太一"
echo "命令：开机，关机，增加音量，减少音量，静音"
echo ""
