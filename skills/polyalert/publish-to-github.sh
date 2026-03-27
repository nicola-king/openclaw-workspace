#!/bin/bash
# PolyAlert Lite GitHub 发布脚本

set -e

echo "🚀 PolyAlert Lite GitHub 发布脚本"
echo "=================================="

# 检查 GitHub 认证
if ! gh auth status 2>&1 | grep -q "Logged in"; then
    echo "❌ GitHub 未认证，请先运行：gh auth login"
    exit 1
fi

echo "✅ GitHub 已认证"

# 创建/更新仓库
REPO_DIR="/home/nicola/.openclaw/workspace/skills/polyalert"
cd "$REPO_DIR"

echo "📁 准备发布文件..."

# Git 初始化
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/nicola-king/polymarket-alert.git
fi

# 添加文件
git add -A
git commit -m "Release v1.0 - PolyAlert Lite 🐋

Features:
- Real-time whale monitoring
- Telegram alerts
- Confidence score calculation
- Free & Open Source (MIT)

👉 Pro: https://chuanxi.gumroad.com/l/hunter-pro" || echo "No changes to commit"

# 推送
echo "📤 推送到 GitHub..."
git branch -M main 2>/dev/null || true
git push -u origin main --force

echo ""
echo "✅ 发布完成！"
echo "=================================="
echo "📦 GitHub 仓库：https://github.com/nicola-king/polymarket-alert"
echo "🛒 Gumroad 产品：https://chuanxi.gumroad.com/l/hunter-pro"
echo "💬 Telegram 群：https://t.me/taiyi_free"
echo ""
echo "🎯 下一步:"
echo "1. 在 GitHub 添加仓库描述"
echo "2. 设置仓库为 Public"
echo "3. Twitter/Reddit 推广"
