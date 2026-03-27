#!/bin/bash
# Syncthing 安全安装脚本
# 严格端口隔离，不影响 OpenClaw

set -e

echo "=========================================="
echo "Syncthing 安全安装脚本 (端口隔离版)"
echo "=========================================="
echo ""

# 1. 检查端口占用
echo "🔍 检查端口占用..."
CONFLICT=0
for port in 22000 21027 8384; do
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        echo "❌ 端口 $port 已被占用！"
        CONFLICT=1
    fi
done

if [ $CONFLICT -eq 1 ]; then
    echo ""
    echo "❌ 存在端口冲突，无法安装！"
    exit 1
fi
echo "✅ 端口无冲突 (22000, 21027, 8384)"
echo ""

# 2. 检查 OpenClaw 端口
echo "🔍 检查 OpenClaw 端口..."
if netstat -tlnp 2>/dev/null | grep -q ":18789 "; then
    echo "✅ OpenClaw Gateway 运行中 (18789)"
else
    echo "⚠️ OpenClaw Gateway 未运行"
fi
echo ""

# 3. 安装 Syncthing
echo "📦 安装 Syncthing..."
sudo apt update
sudo apt install -y syncthing
echo "✅ Syncthing 安装完成"
echo ""

# 4. 创建用户服务
echo "🔧 配置用户服务..."
systemctl --user enable syncthing
systemctl --user start syncthing
sleep 3
echo "✅ 服务已启动"
echo ""

# 5. 验证服务
echo "🔍 验证服务状态..."
if systemctl --user is-active syncthing > /dev/null 2>&1; then
    echo "✅ Syncthing 服务运行正常"
else
    echo "❌ Syncthing 服务启动失败"
    exit 1
fi
echo ""

# 6. 配置防火墙
echo "🔐 配置防火墙..."
sudo ufw allow 22000/tcp comment "Syncthing 文件传输" 2>/dev/null || true
sudo ufw allow 22000/udp comment "Syncthing 发现协议" 2>/dev/null || true
sudo ufw allow 21027/udp comment "Syncthing 本地发现" 2>/dev/null || true
echo "✅ 防火墙规则已配置"
echo ""

# 7. 验证 OpenClaw 不受影响
echo "🔍 验证 OpenClaw 不受影响..."
if curl -s http://127.0.0.1:18789/health > /dev/null 2>&1; then
    echo "✅ OpenClaw Gateway 正常"
else
    echo "⚠️ OpenClaw Gateway 无法访问 (可能是正常关闭)"
fi
echo ""

# 8. 显示访问信息
echo "=========================================="
echo "✅ Syncthing 安装完成！"
echo ""
echo "访问 Web 界面：http://127.0.0.1:8384"
echo "设备 ID: 在 Web 界面 → 操作 → 显示 ID"
echo ""
echo "使用端口:"
echo "  22000/tcp - 文件传输"
echo "  22000/udp - 发现协议"
echo "  21027/udp - 本地发现"
echo "  8384/tcp  - Web 界面 (仅本地)"
echo ""
echo "OpenClaw 端口:"
echo "  18789/tcp - Gateway (无冲突)"
echo "=========================================="
