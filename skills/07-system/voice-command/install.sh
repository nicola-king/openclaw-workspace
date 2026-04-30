#!/bin/bash
# 太一语音命令安装脚本

set -e

echo "🎤 太一语音命令安装脚本"
echo "=========================================="
echo ""

# 1. 安装系统依赖
echo "📦 步骤 1: 安装系统依赖..."
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio espeak
echo "✅ 系统依赖安装完成"
echo ""

# 2. 安装 Python 依赖
echo "📦 步骤 2: 安装 Python 依赖..."
pip3 install --break-system-packages vosk pyaudio
echo "✅ Python 依赖安装完成"
echo ""

# 3. 下载语音模型
echo "📦 步骤 3: 下载语音模型 (约 500MB，可能需要几分钟)..."
MODEL_DIR="/home/nicola/.openclaw/workspace/models"
mkdir -p "$MODEL_DIR"
cd /tmp

if [ ! -d "$MODEL_DIR/vosk-model-cn-0.15" ]; then
    wget https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip
    unzip vosk-model-cn-0.15.zip
    mv vosk-model-cn-0.15 "$MODEL_DIR/"
    echo "✅ 语音模型下载完成"
else
    echo "✅ 语音模型已存在"
fi
echo ""

# 4. 测试
echo "📦 步骤 4: 测试安装..."
cd /home/nicola/.openclaw/workspace/skills/07-system/voice-command
python3 voice_command.py --test

echo ""
echo "=========================================="
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  cd /home/nicola/.openclaw/workspace/skills/07-system/voice-command"
echo "  python3 voice_command.py"
echo ""
echo "唤醒词：太一 或 Taiyi"
echo "=========================================="
