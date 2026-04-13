#!/bin/bash
# 电视控制测试脚本

echo "🧪 电视控制测试..."
echo ""

# 检查 CEC
echo "📺 检查 HDMI-CEC..."
if command -v cec-client &> /dev/null; then
    echo "✅ cec-utils 已安装"
    echo "扫描设备："
    echo "scan" | cec-client -s 2>&1 | head -10
else
    echo "❌ cec-utils 未安装"
    echo "安装命令：sudo apt-get install cec-utils"
fi
echo ""

# 检查音频
echo "🔊 检查音频控制..."
if command -v amixer &> /dev/null; then
    echo "✅ alsa-utils 已安装"
    echo "当前音量："
    amixer get Master | head -3
else
    echo "❌ alsa-utils 未安装"
    echo "安装命令：sudo apt-get install alsa-utils"
fi
echo ""

# 检查显示
echo "🖥️ 检查显示控制..."
if command -v xset &> /dev/null; then
    echo "✅ xset 已安装"
    echo "显示器状态："
    xset q | grep "Monitor is"
else
    echo "❌ xset 未安装"
    echo "安装命令：sudo apt-get install x11-xserver-utils"
fi
echo ""

echo "✅ 测试完成！"
echo ""
echo "如所有检查通过，启动电视控制："
echo "  cd ~/.openclaw/workspace/skills/tv-control"
echo "  python3 main.py"
