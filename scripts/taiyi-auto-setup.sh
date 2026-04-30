#!/bin/bash
# 太一工控机自动配置脚本
# 功能：Tailscale + Syncthing + 任务监控 一键安装

set -e

echo "=========================================="
echo "太一工控机自动配置脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 1. 检查 root 权限
if [ "$EUID" -ne 0 ]; then
    log_error "请使用 sudo 运行此脚本"
    exit 1
fi

# 2. 检查端口占用
log_info "检查端口占用..."
CONFLICT=0
for port in 22000 21027 8384; do
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        log_error "端口 $port 已被占用！"
        CONFLICT=1
    fi
done
if [ $CONFLICT -eq 1 ]; then
    exit 1
fi
log_info "✅ 端口无冲突"
echo ""

# 3. 安装 Tailscale (如未安装)
log_info "检查 Tailscale..."
if ! command -v tailscale &> /dev/null; then
    log_info "安装 Tailscale..."
    curl -fsSL https://tailscale.com/install.sh | sh
    log_info "✅ Tailscale 安装完成"
else
    log_info "✅ Tailscale 已安装"
fi
echo ""

# 4. 启动 Tailscale
log_info "启动 Tailscale..."
if ! systemctl is-active --quiet tailscaled; then
    sudo systemctl start tailscaled
    sudo systemctl enable tailscaled
    log_info "✅ Tailscale 服务已启动"
else
    log_info "✅ Tailscale 服务运行中"
fi
echo ""

# 5. 显示 Tailscale 状态
log_info "Tailscale 状态:"
tailscale status 2>/dev/null | head -5 || log_warn "Tailscale 未登录，请执行：sudo tailscale up"
echo ""

# 6. 安装 Syncthing
log_info "安装 Syncthing..."
apt update
apt install -y syncthing
log_info "✅ Syncthing 安装完成"
echo ""

# 7. 配置 Syncthing 用户服务
log_info "配置 Syncthing 用户服务..."
USER_HOME=$(eval echo ~$SUDO_USER)
sudo -u $SUDO_USER bash -c "
    systemctl --user enable syncthing
    systemctl --user start syncthing
"
sleep 3
log_info "✅ Syncthing 服务已启动"
echo ""

# 8. 创建同步目录
log_info "创建同步目录..."
SYNC_BASE="/home/$SUDO_USER/.openclaw/workspace"
sudo -u $SUDO_USER mkdir -p "$SYNC_BASE/sync-to-workstation/{backup,commands,results}"
sudo -u $SUDO_USER mkdir -p "$SYNC_BASE/sync-from-workstation/{results,data,requests}"
sudo -u $SUDO_USER mkdir -p "$SYNC_BASE/sync-processing"
sudo -u $SUDO_USER mkdir -p "$SYNC_BASE/logs"
log_info "✅ 目录创建完成"
echo ""

# 9. 部署监控脚本
log_info "部署监控脚本..."
WORKSPACE="/home/$SUDO_USER/.openclaw/workspace"
MONITOR_SCRIPT="$WORKSPACE/skills/suwen/syncthing-workstation-monitor.py"

if [ -f "$MONITOR_SCRIPT" ]; then
    # 创建 systemd 服务文件
    cat > /home/$SUDO_USER/.config/systemd/user/syncthing-monitor.service << EOF
[Unit]
Description=Syncthing Workstation Monitor
After=syncthing.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 $MONITOR_SCRIPT
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

    sudo -u $SUDO_USER bash -c "
        systemctl --user daemon-reload
        systemctl --user enable syncthing-monitor
        systemctl --user start syncthing-monitor
    "
    log_info "✅ 监控服务已部署"
else
    log_warn "监控脚本不存在：$MONITOR_SCRIPT"
fi
echo ""

# 10. 配置防火墙
log_info "配置防火墙..."
ufw allow 22000/tcp comment "Syncthing 文件传输" 2>/dev/null || true
ufw allow 22000/udp comment "Syncthing 发现协议" 2>/dev/null || true
ufw allow 21027/udp comment "Syncthing 本地发现" 2>/dev/null || true
ufw allow 41641/udp comment "Tailscale" 2>/dev/null || true
log_info "✅ 防火墙规则已配置"
echo ""

# 11. 验证 OpenClaw
log_info "验证 OpenClaw 不受影响..."
if curl -s http://127.0.0.1:18789/health > /dev/null 2>&1; then
    log_info "✅ OpenClaw Gateway 正常"
else
    log_warn "OpenClaw Gateway 未响应 (可能是正常关闭)"
fi
echo ""

# 12. 显示配置信息
echo "=========================================="
log_info "✅ 太一工控机配置完成！"
echo "=========================================="
echo ""
echo "【Tailscale】"
echo "  状态：$(systemctl is-active tailscaled)"
echo "  登录：执行 'sudo tailscale up' 获取登录链接"
echo ""
echo "【Syncthing】"
echo "  Web 界面：http://127.0.0.1:8384"
echo "  状态：$(systemctl --user is-active syncthing)"
echo "  设备 ID: 在 Web 界面 → 操作 → 显示 ID"
echo ""
echo "【同步目录】"
echo "  发送到工作站：$SYNC_BASE/sync-to-workstation/"
echo "  从工作站接收：$SYNC_BASE/sync-from-workstation/"
echo ""
echo "【监控服务】"
echo "  状态：$(systemctl --user is-active syncthing-monitor)"
echo "  日志：journalctl --user -u syncthing-monitor -f"
echo ""
echo "【下一步】"
echo "  1. 登录 Tailscale: sudo tailscale up"
echo "  2. 访问 Syncthing Web: http://127.0.0.1:8384"
echo "  3. 添加工作站设备 ID"
echo "  4. 配置单向同步文件夹"
echo ""
echo "=========================================="
