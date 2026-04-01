#!/bin/bash
# 华为电视 CEC 测试脚本

echo "🔍 华为电视 CEC 测试..."
echo ""

# 检查 cec-client
if ! command -v cec-client &> /dev/null; then
    echo "❌ cec-utils 未安装"
    echo "安装命令：sudo apt-get install cec-utils"
    exit 1
fi

echo "✅ cec-utils 已安装"
echo ""

# 扫描 CEC 设备
echo "📺 扫描 CEC 设备..."
echo "scan" | cec-client -s 2>&1 | head -20
echo ""

# 测试开机
echo "🔌 测试开机..."
echo "on" | cec-client -s
sleep 2
echo ""

# 测试关机
echo "🔌 测试关机..."
echo "standby" | cec-client -s
sleep 2
echo ""

# 测试音量+
echo "🔊 测试音量+..."
echo "volup" | cec-client -s
sleep 1
echo ""

# 测试音量-
echo "🔉 测试音量-..."
echo "voldown" | cec-client -s
sleep 1
echo ""

# 测试静音
echo "🔇 测试静音..."
echo "mute" | cec-client -s
sleep 1
echo ""

# 检查音频
echo "📊 检查音频状态..."
amixer get Master | head -5
echo ""

echo "✅ 华为电视 CEC 测试完成！"
echo ""
echo "如测试成功，启动太一电视控制："
echo "cd ~/.openclaw/workspace/skills/taiyi"
echo "python3 tv-control-ipc.py &"
