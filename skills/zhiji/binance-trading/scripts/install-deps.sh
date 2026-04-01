#!/bin/bash
# 币安测试网依赖安装

echo "🔧 安装币安交易依赖..."

# Python 依赖
pip3 install python-binance aiohttp python-dotenv

echo "✅ 依赖安装完成！"
echo ""
echo "下一步:"
echo "1. 访问 https://testnet.binance.vision/ 注册测试网账号"
echo "2. 获取测试网 API Key 和 Secret Key"
echo "3. 创建配置文件：/home/nicola/.openclaw/.env.binance-testnet"
echo "4. 测试运行：python3 binance-testnet-trader.py"
