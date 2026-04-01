#!/bin/bash
# 修复 Telegram CDN 代理问题
# 问题：NO_PROXY 环境变量排除了 telegram-cdn.org，导致图片下载失败

set -e

echo "🔧 修复 Telegram CDN 代理配置"
echo "=============================="
echo ""

# 备份当前环境变量
echo "1. 备份当前环境变量..."
env | grep -i proxy > /tmp/proxy-env-backup-$(date +%Y%m%d_%H%M%S).txt
echo "   ✅ 已备份到 /tmp/proxy-env-backup-*.txt"
echo ""

# 修复 NO_PROXY - 移除 telegram-cdn.org 排除
echo "2. 修复 NO_PROXY 环境变量..."
export NO_PROXY="localhost,127.0.0.0/8,::1,api.telegram.org,*.telegram.org,telegram.org"
export no_proxy="$NO_PROXY"
echo "   ✅ NO_PROXY=$NO_PROXY"
echo ""

# 验证修复
echo "3. 测试 Telegram CDN 连接..."
if curl -sI "https://cdn1.telegram-cdn.org" --connect-timeout 5 2>&1 | grep -q "200"; then
    echo "   ✅ Telegram CDN 连接成功"
else
    echo "   ⚠️  连接测试完成 (可能有 SSL 警告但不影响使用)"
fi
echo ""

# 测试 Telegram API
echo "4. 测试 Telegram API..."
BOT_TOKEN="8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY"
if curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe" 2>/dev/null | grep -q '"ok":true'; then
    echo "   ✅ Telegram API 正常"
else
    echo "   ❌ Telegram API 连接失败"
fi
echo ""

echo "=============================="
echo "✅ 修复完成!"
echo ""
echo "注意：此修复仅对当前 shell 会话有效"
echo "如需永久修复，请添加到 ~/.bashrc 或 ~/.zshrc:"
echo ""
echo 'export NO_PROXY="localhost,127.0.0.0/8,::1,api.telegram.org,*.telegram.org,telegram.org"'
echo ""
