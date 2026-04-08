#!/bin/bash
# 山木公众号助手 - 一键配置脚本

echo "======================================"
echo "山木公众号助手 - 配置向导"
echo "======================================"
echo ""

# 创建配置目录
mkdir -p ~/.taiyi/wechat-assistant

# 引导用户输入
echo "请按提示输入以下信息："
echo ""

# 输入 QQ 邮箱
read -p "你的 QQ 邮箱（用于发送邮件）：" SENDER_EMAIL
echo ""

# 输入授权码
read -s -p "QQ 邮箱授权码（不是 QQ 密码，去邮箱设置获取）：" SMTP_PASSWORD
echo ""
echo ""

# 输入收件邮箱
read -p "收件邮箱（默认 285915125@qq.com）：" RECIPIENT_EMAIL
RECIPIENT_EMAIL=${RECIPIENT_EMAIL:-285915125@qq.com}
echo ""

# 创建配置文件
cat > ~/.taiyi/wechat-assistant/config.json << EOF
{
  "sender_email": "$SENDER_EMAIL",
  "smtp_password": "$SMTP_PASSWORD",
  "recipient_email": "$RECIPIENT_EMAIL"
}
EOF

echo "======================================"
echo "✅ 配置完成！"
echo "======================================"
echo ""
echo "配置文件：~/.taiyi/wechat-assistant/config.json"
echo ""
echo "测试发送："
echo "  python3 ~/.openclaw/workspace/skills/shanmu/wechat-assistant/wechat_sender.py --topic \"AI 管家\""
echo ""
echo "查看配置："
echo "  cat ~/.taiyi/wechat-assistant/config.json"
echo ""
echo "======================================"
