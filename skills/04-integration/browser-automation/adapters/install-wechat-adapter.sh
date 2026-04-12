#!/bin/bash
# 个人微信 RPA 适配器 - 安装脚本

echo "🔧 安装个人微信 RPA 适配器依赖..."

# 检查 pip3
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装，请先执行:"
    echo "   sudo apt update && sudo apt install -y python3-pip"
    exit 1
fi

# 安装 Playwright
echo "📦 安装 Playwright..."
pip3 install playwright

# 安装 Chromium 浏览器
echo "🌐 安装 Chromium 浏览器..."
playwright install chromium

# 安装系统依赖
echo "📦 安装系统依赖..."
sudo apt install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    || echo "⚠️ 部分依赖可能已安装"

echo ""
echo "✅ 安装完成！"
echo ""
echo "📱 使用示例:"
echo "   # 首次扫码登录"
echo "   python3 skills/browser-automation/adapters/wechat_personal_adapter.py --account main --login"
echo ""
echo "   # 发送消息"
echo "   python3 skills/browser-automation/adapters/wechat_personal_adapter.py --account main --message '测试' --contact 'filehelper'"
echo ""
