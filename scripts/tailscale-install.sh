#!/bin/bash
# Tailscale 一键安装脚本
# 适用：Ubuntu 22.04/24.04
# 账号：shanyejingling@gmail.com

set -e

echo "🌐 Tailscale 安装脚本"
echo "======================"
echo ""
echo "📝 将使用账号登录：shanyejingling@gmail.com"
echo ""

# 检查是否已安装
if command -v tailscale &> /dev/null; then
    echo "✅ Tailscale 已安装"
    tailscale --version
    echo ""
    echo "🔄 重新启动..."
    sudo tailscale up
else
    echo "📦 安装 Tailscale..."
    
    # 添加 GPG 密钥
    echo "  [1/4] 下载 GPG 密钥..."
    curl -fsSL https://tailscale.com/gpgkeys/tailscale.asc | \
      sudo gpg --dearmor -o /usr/share/keyrings/tailscale.gpg
    
    # 添加仓库
    echo "  [2/4] 添加仓库..."
    echo "deb [signed-by=/usr/share/keyrings/tailscale.gpg] \
      https://pkgs.tailscale.com/stable/ubuntu noble main" | \
      sudo tee /etc/apt/sources.list.d/tailscale.list
    
    # 更新并安装
    echo "  [3/4] 更新软件包..."
    sudo apt-get update -qq
    
    echo "  [4/4] 安装 Tailscale..."
    sudo apt-get install -y tailscale
    
    echo ""
    echo "✅ 安装完成!"
fi

# 启动 Tailscale
echo ""
echo "🚀 启动 Tailscale..."
echo ""
echo "⚠️  请在浏览器打开以下 URL 并登录:"
echo ""
sudo tailscale up

echo ""
echo "📊 查看状态:"
echo "  tailscale status"
echo ""
echo "🌐 查看 IP:"
echo "  tailscale ip"
echo ""
echo "📱 手机访问:"
echo "  1. 手机安装 Tailscale App"
echo "  2. 登录同一账号：shanyejingling@gmail.com"
echo "  3. 访问：http://[Tailscale IP]:5001"
echo ""
echo "✨ 配置完成!"
