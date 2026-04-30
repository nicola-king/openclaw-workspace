#!/bin/bash
# GMGN 依赖安装

echo "🔧 安装 GMGN 交易依赖..."

# Python 依赖
pip3 install requests aiohttp python-dotenv

echo "✅ 依赖安装完成！"
echo ""
echo "下一步:"
echo "1. 确认已登录 Telegram @GMGN_bot"
echo "2. 确认钱包地址：5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq"
echo "3. 确认余额：1.7 SOL ($150)"
echo "4. 测试运行：python3 gmgn-client.py"
