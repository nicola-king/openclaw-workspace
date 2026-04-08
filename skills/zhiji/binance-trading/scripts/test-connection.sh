#!/bin/bash
# 币安测试网连接测试

echo "🧪 测试币安测试网连接..."

cd ~/.openclaw/workspace/skills/zhiji/binance-trading
python3 binance-testnet-trader.py

if [ $? -eq 0 ]; then
    echo "✅ 连接测试成功！"
else
    echo "❌ 连接测试失败，请检查 API Key 配置"
fi
