#!/bin/bash
# 太一语音功能一键配置脚本
# 用法：bash ~/workspace/scripts/voice-setup.sh

set -e

echo "🎤 太一语音功能一键配置"
echo "=========================================="
echo ""

# 1. 检查麦克风
echo "📦 步骤 1: 检查麦克风..."
if arecord -l 2>/dev/null | grep -q "card"; then
    echo "✅ 麦克风已检测到"
else
    echo "⚠️  未检测到麦克风"
fi
echo ""

# 2. 配置 Telegram Bot (可选)
echo "📦 步骤 2: Telegram Bot 配置 (可选)"
echo "如需配置 Telegram 语音识别，请输入 Bot Token:"
echo "按回车跳过..."
read -p "Telegram Bot Token: " TELEGRAM_TOKEN

if [ -n "$TELEGRAM_TOKEN" ]; then
    echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_TOKEN" >> ~/.openclaw/.env
    echo "✅ Telegram Bot Token 已保存"
else
    echo "⏭️  跳过 Telegram 配置"
fi
echo ""

# 3. 创建快速启动脚本
echo "📦 步骤 3: 创建快速启动脚本..."

# 麦克风语音控制
cat > ~/workspace/scripts/voice-command-start.sh << 'EOF'
#!/bin/bash
cd /home/nicola/.openclaw/workspace/skills/07-system/voice-command
python3 voice_command.py
EOF
chmod +x ~/workspace/scripts/voice-command-start.sh

# Telegram 语音处理
cat > ~/workspace/scripts/telegram-voice-start.sh << 'EOF'
#!/bin/bash
cd /home/nicola/.openclaw/workspace/skills/07-system/telegram-voice-handler
python3 voice_handler.py
EOF
chmod +x ~/workspace/scripts/telegram-voice-start.sh

echo "✅ 快速启动脚本已创建"
echo ""

# 4. 微信语音输入指南
echo "📦 步骤 4: 微信语音输入方案"
cat << 'WECHAT_GUIDE'

==========================================
💬 微信语音输入 (立即可用)

方案：手机语音输入法 → 微信文字 → 太一

步骤:
1. 打开微信聊天
2. 点击输入框旁边的麦克风图标
3. 说话 (自动转文字)
4. 发送给太一

优点:
✅ 无需开发
✅ 准确率高 (95%+)
✅ 支持中文
✅ 立即可用

==========================================
WECHAT_GUIDE

echo ""
echo "=========================================="
echo "✅ 配置完成！"
echo ""
echo "使用方法:"
echo "  麦克风语音：bash ~/workspace/scripts/voice-command-start.sh"
echo "  Telegram 语音：bash ~/workspace/scripts/telegram-voice-start.sh"
echo "  微信语音：手机语音输入法 (立即可用)"
echo "=========================================="
