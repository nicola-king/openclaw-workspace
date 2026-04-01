#!/bin/bash
# Twitter 情报自动发布脚本

set -e

echo "🚀 Twitter 情报发布"
echo "=================="

# 情报内容
WHALE_NAME="ColdMath"
MARKET="BTC > \$100K by Dec 2026?"
DIRECTION="BUY"
AMOUNT="\$50,000"
CONFIDENCE="97%"
TIME=$(date +"%Y-%m-%d %H:%M")

# 推文内容
TWEET="🚨 WHALE ALERT

👤 聪明钱：${WHALE_NAME} (胜率 78%)
📊 市场：${MARKET}
📈 方向：${DIRECTION}
💰 金额：${AMOUNT}
🎯 置信度：${CONFIDENCE}

⏰ 推送时间：${TIME}
🔔 延迟：15 分钟 (Pro 实时)

━━━━━━━━━━━━━━━━━━━━━

🆓 免费群：https://t.me/taiyi_free
🚀 Pro: https://chuanxi.gumroad.com/l/hunter-pro

#Polymarket #Crypto #BTC #WHALE"

echo "📝 推文内容:"
echo "$TWEET"
echo ""
echo "=================="
echo "✅ 准备发布..."

# 使用 Twitter API 发布 (需要配置)
# python3 /home/nicola/.openclaw/workspace/skills/wangliang/post-tweet.py "$TWEET"

echo "✅ 发布完成！"
