#!/bin/bash
# 电视控制依赖安装脚本

echo "🔧 安装电视控制依赖..."
echo ""

# 更新软件源
echo "📦 更新软件源..."
sudo apt-get update

# 安装 HDMI-CEC 工具
echo "📺 安装 HDMI-CEC 工具..."
sudo apt-get install -y cec-utils

# 安装音频工具
echo "🔊 安装音频工具..."
sudo apt-get install -y alsa-utils

# 安装显示工具
echo "🖥️ 安装显示工具..."
sudo apt-get install -y x11-xserver-utils

# 安装 Python 依赖
echo "🐍 安装 Python 依赖..."
pip3 install flask pyyaml requests

echo ""
echo "✅ 依赖安装完成！"
echo ""
echo "测试 CEC 连接："
echo "  echo \"scan\" | cec-client -s"
echo ""
echo "启动电视控制："
echo "  cd ~/.openclaw/workspace/skills/tv-control"
echo "  python3 main.py"
