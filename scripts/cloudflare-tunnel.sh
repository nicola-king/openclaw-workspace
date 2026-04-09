#!/bin/bash
# Cloudflare Tunnel 一键配置脚本
# 免 root 权限 | 快速临时访问
# 账号：shanyejingling@gmail.com

set -e

echo "☁️ Cloudflare Tunnel 配置脚本"
echo "=============================="
echo ""
echo "📝 将使用账号登录：shanyejingling@gmail.com"
echo ""

# 检查是否已下载
if [ ! -f ~/bin/cloudflared ]; then
    echo "📦 下载 cloudflared..."
    mkdir -p ~/bin
    curl -Lo ~/bin/cloudflared \
      https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    chmod +x ~/bin/cloudflared
    echo "✅ 下载完成：~/bin/cloudflared"
else
    echo "✅ cloudflared 已存在"
fi

echo ""
echo "🚀 启动 Tunnel..."
echo ""
echo "⚠️  请按以下步骤操作:"
echo ""
echo "1. 打开浏览器访问：https://dash.teams.cloudflare.com/"
echo "2. 登录账号：shanyejingling@gmail.com"
echo "3. 点击 'Zero Trust' → 'Access' → 'Tunnels'"
echo "4. 点击 'Create a tunnel'"
echo "5. 选择 'Public' 类型"
echo "6. 复制命令并在此粘贴执行"
echo ""
echo "或者，直接运行快速 Tunnel (临时 URL):"
echo ""
echo "  ~/bin/cloudflared tunnel --url http://localhost:5001"
echo ""
echo "输出会显示：https://xxx.trycloudflare.com"
echo "手机访问这个 URL 即可!"
echo ""

# 询问是否立即启动
read -p "是否立即启动快速 Tunnel? (y/n): " confirm
if [ "$confirm" = "y" ]; then
    echo ""
    echo "🌐 启动中..."
    ~/bin/cloudflared tunnel --url http://localhost:5001
fi
