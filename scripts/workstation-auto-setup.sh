#!/bin/bash
# 工作站一键配置脚本
# 功能：Tailscale + Syncthing + SMB 共享 + 任务监控

set -e

echo "=========================================="
echo "工作站一键配置脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 1. 检查 root 权限
if [ "$EUID" -ne 0 ]; then
    log_error "请使用 sudo 运行此脚本"
    exit 1
fi

# 2. 安装 Tailscale
log_info "安装 Tailscale..."
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
    log_info "✅ Tailscale 安装完成"
else
    log_info "✅ Tailscale 已安装"
fi

# 启动 Tailscale
if ! systemctl is-active --quiet tailscaled; then
    systemctl start tailscaled
    systemctl enable tailscaled
    log_info "✅ Tailscale 服务已启动"
fi
echo ""

# 3. 安装 Syncthing
log_info "安装 Syncthing..."
apt update
apt install -y syncthing
log_info "✅ Syncthing 安装完成"

# 配置用户服务
USER_HOME=$(eval echo ~$SUDO_USER)
sudo -u $SUDO_USER bash -c "
    systemctl --user enable syncthing
    systemctl --user start syncthing
"
sleep 3
log_info "✅ Syncthing 服务已启动"
echo ""

# 4. 创建 D 盘目录结构
log_info "创建 D 盘目录结构..."
D_MOUNT="/mnt/d"

# 检查 D 盘是否挂载
if [ ! -d "$D_MOUNT" ]; then
    log_warn "D 盘未挂载到 $D_MOUNT"
    log_info "尝试创建挂载点..."
    mkdir -p "$D_MOUNT"
    log_warn "请手动挂载 D 盘到 $D_MOUNT"
fi

# 创建 Syncthing 目录 (严格单向同步)
SYNC_HUB="$D_MOUNT/syncthing-hub"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/from-taiyi/backup"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/from-taiyi/commands"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/to-taiyi/results"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/to-taiyi/data"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/from-laptop/data"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/from-laptop/requests"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/to-laptop/all-data"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/to-laptop/results"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/shared/public"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/shared/projects"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/shared/archives"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/processing"
sudo -u $SUDO_USER mkdir -p "$SYNC_HUB/logs"

# 设置只读权限 (防止工作站主动写入)
log_info "设置只读权限..."
chmod 555 "$SYNC_HUB/from-taiyi"        # 只读 (太一写入)
chmod 555 "$SYNC_HUB/from-laptop"       # 只读 (笔记本写入)
chmod 755 "$SYNC_HUB/to-taiyi"          # 工作站可写入结果
chmod 755 "$SYNC_HUB/to-laptop"         # 工作站可写入共享数据
chmod 755 "$SYNC_HUB/shared"            # 工作站可写入共享
log_info "✅ 权限设置完成"

log_info "✅ D 盘目录创建完成"
echo "  位置：$SYNC_HUB"
echo ""

# 5. 配置 SMB 共享 (笔记本访问)
log_info "安装 Samba..."
apt install -y samba samba-common-bin

# 备份原配置
cp /etc/samba/smb.conf /etc/samba/smb.conf.bak 2>/dev/null || true

# 创建 SMB 配置 (笔记本可访问所有数据)
cat > /etc/samba/smb.conf << EOF
[global]
   workgroup = WORKGROUP
   server string = Workstation Share
   security = user
   map to guest = Bad User
   dns proxy = no

[Shared]
   path = $SYNC_HUB/shared
   browseable = yes
   read only = no
   guest ok = no
   create mask = 0644
   directory mask = 0755
   valid users = $SUDO_USER

[All-Data]
   path = $SYNC_HUB/to-laptop/all-data
   browseable = yes
   read only = yes
   guest ok = no
   create mask = 0644
   directory mask = 0755
   valid users = $SUDO_USER

[Projects]
   path = $SYNC_HUB/shared/projects
   browseable = yes
   read only = no
   guest ok = no
   create mask = 0644
   directory mask = 0755
   valid users = $SUDO_USER
EOF

# 设置 Samba 密码
log_info "设置 Samba 用户密码..."
smbpasswd -a $SUDO_USER 2>/dev/null || log_warn "Samba 密码设置失败，请手动执行：sudo smbpasswd -a $SUDO_USER"

# 重启 Samba
systemctl restart smbd
systemctl enable smbd
log_info "✅ SMB 共享配置完成"
echo "  共享路径：\\\\工作站 IP\\shared"
echo "  用户名：$SUDO_USER"
echo ""

# 6. 部署任务监控脚本
log_info "部署任务监控脚本..."
MONITOR_SCRIPT="$SYNC_HUB/scripts/command-monitor.py"

# 创建监控脚本
cat > "$MONITOR_SCRIPT" << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
"""
工作站任务监控 - 执行太一命令
"""

import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

SYNC_HUB = Path("/mnt/d/syncthing-hub")
COMMANDS_DIR = SYNC_HUB / "from-taiyi/commands"
RESULTS_DIR = SYNC_HUB / "to-taiyi/results"
PROCESSING_DIR = SYNC_HUB / "processing"
LOG_FILE = SYNC_HUB / "logs/command-monitor.log"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}\n"
    print(log_msg, end="")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)

def execute_command(cmd_file):
    cmd_id = cmd_file.stem
    log(f"执行命令：{cmd_id}")
    
    try:
        with open(cmd_file) as f:
            cmd = json.load(f)
        
        command = cmd.get('command', 'echo "No command"')
        timeout = cmd.get('timeout', 3600)
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=timeout
        )
        
        result_file = RESULTS_DIR / f"result-{cmd_id}.json"
        with open(result_file, 'w') as f:
            json.dump({
                'command_id': cmd_id,
                'status': 'completed' if result.returncode == 0 else 'failed',
                'return_code': result.returncode,
                'stdout': result.stdout.decode()[:10000],
                'stderr': result.stderr.decode()[:10000],
                'executed_at': datetime.now().isoformat()
            }, f, indent=2)
        
        cmd_file.unlink()
        log(f"命令完成：{cmd_id}")
        
    except Exception as e:
        log(f"命令失败：{cmd_id}, 错误：{e}")

COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSING_DIR.mkdir(parents=True, exist_ok=True)

log("=" * 60)
log("工作站任务监控启动")
log("=" * 60)

while True:
    try:
        for cmd_file in COMMANDS_DIR.glob('cmd-*.json'):
            execute_command(cmd_file)
        time.sleep(10)
    except KeyboardInterrupt:
        log("停止监控")
        break
PYTHON_SCRIPT

chmod +x "$MONITOR_SCRIPT"
log_info "✅ 监控脚本已部署"
echo ""

# 7. 创建 systemd 服务
log_info "创建 systemd 服务..."
cat > /home/$SUDO_USER/.config/systemd/user/workstation-monitor.service << EOF
[Unit]
Description=Workstation Command Monitor
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
    systemctl --user enable workstation-monitor
    systemctl --user start workstation-monitor
"
log_info "✅ 监控服务已启动"
echo ""

# 8. 配置防火墙
log_info "配置防火墙..."
ufw allow 22000/tcp comment "Syncthing 文件传输" 2>/dev/null || true
ufw allow 22000/udp comment "Syncthing 发现协议" 2>/dev/null || true
ufw allow 21027/udp comment "Syncthing 本地发现" 2>/dev/null || true
ufw allow 41641/udp comment "Tailscale" 2>/dev/null || true
ufw allow 139/tcp comment "SMB NetBIOS" 2>/dev/null || true
ufw allow 445/tcp comment "SMB TCP" 2>/dev/null || true
ufw allow 137/udp comment "SMB NetBIOS UDP" 2>/dev/null || true
ufw allow 138/udp comment "SMB NetBIOS UDP" 2>/dev/null || true
log_info "✅ 防火墙规则已配置"
echo ""

# 9. 显示配置信息
echo "=========================================="
log_info "✅ 工作站配置完成！"
echo "=========================================="
echo ""
echo "【Tailscale】"
echo "  登录：sudo tailscale up"
echo "  状态：$(systemctl is-active tailscaled)"
echo ""
echo "【Syncthing】"
echo "  Web 界面：http://127.0.0.1:8384"
echo "  状态：$(systemctl --user is-active syncthing)"
echo ""
echo "【SMB 共享】"
echo "  共享路径：\\\\工作站 IP\\shared"
echo "  所有数据：\\\\工作站 IP\\All-Data"
echo "  用户名：$SUDO_USER"
echo ""
echo "【同步目录】"
echo "  位置：$SYNC_HUB"
echo "  从太一接收：$SYNC_HUB/from-taiyi/"
echo "  发送给太一：$SYNC_HUB/to-taiyi/"
echo "  笔记本访问：$SYNC_HUB/shared/"
echo ""
echo "【监控服务】"
echo "  状态：$(systemctl --user is-active workstation-monitor)"
echo "  日志：journalctl --user -u workstation-monitor -f"
echo ""
echo "【下一步】"
echo "  1. 登录 Tailscale: sudo tailscale up"
echo "  2. 访问 Syncthing Web: http://127.0.0.1:8384"
echo "  3. 添加太一和笔记本设备 ID"
echo "  4. 配置单向同步文件夹"
echo "  5. 笔记本访问 SMB: \\\\工作站 IP\\shared"
echo ""
echo "=========================================="
