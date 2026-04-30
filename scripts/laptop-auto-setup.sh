#!/bin/bash
# 笔记本一键配置脚本
# 功能：Tailscale + Syncthing + SMB 客户端

set -e

echo "=========================================="
echo "笔记本一键配置脚本"
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

# 1. 安装 Tailscale
log_info "安装 Tailscale..."
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
    log_info "✅ Tailscale 安装完成"
else
    log_info "✅ Tailscale 已安装"
fi

# 启动 Tailscale
if ! systemctl is-active --quiet tailscaled 2>/dev/null; then
    sudo systemctl start tailscaled
    sudo systemctl enable tailscaled
    log_info "✅ Tailscale 服务已启动"
fi
echo ""

# 2. 安装 Syncthing
log_info "安装 Syncthing..."
sudo apt update
sudo apt install -y syncthing
log_info "✅ Syncthing 安装完成"

# 配置用户服务
sudo -u $SUDO_USER bash -c "
    systemctl --user enable syncthing
    systemctl --user start syncthing
"
sleep 3
log_info "✅ Syncthing 服务已启动"
echo ""

# 3. 创建同步目录
log_info "创建同步目录..."
LAPTOP_SYNC="$HOME/laptop-sync"
mkdir -p "$LAPTOP_SYNC/sync-to-workstation/data"
mkdir -p "$LAPTOP_SYNC/sync-to-workstation/requests"
mkdir -p "$LAPTOP_SYNC/sync-from-workstation/results"
mkdir -p "$LAPTOP_SYNC/sync-from-workstation/data"
mkdir -p "$LAPTOP_SYNC/local"
log_info "✅ 同步目录创建完成"
echo "  位置：$LAPTOP_SYNC"
echo ""

# 4. 配置 SMB 客户端
log_info "安装 SMB 客户端..."
sudo apt install -y cifs-utils smbclient
log_info "✅ SMB 客户端安装完成"
echo ""

# 5. 创建工作站访问脚本
log_info "创建工作站访问脚本..."
ACCESS_SCRIPT="$HOME/access-workstation.sh"
cat > "$ACCESS_SCRIPT" << 'EOF'
#!/bin/bash
# 访问工作站共享

WORKSTATION_IP=""  # 请填写工作站 Tailscale IP
USERNAME="$USER"

echo "=========================================="
echo "访问工作站共享"
echo "=========================================="

# 检查是否已输入工作站 IP
if [ -z "$WORKSTATION_IP" ]; then
    read -p "请输入工作站 Tailscale IP: " WORKSTATION_IP
fi

echo ""
echo "【SMB 共享访问】"
echo "  工作站 IP: $WORKSTATION_IP"
echo "  共享路径：\\\\$WORKSTATION_IP\\shared"
echo "  所有数据：\\\\$WORKSTATION_IP\\All-Data"
echo ""

# 创建挂载点
MOUNT_DIR="$HOME/workstation-share"
mkdir -p "$MOUNT_DIR"

# 挂载共享
echo "挂载共享到：$MOUNT_DIR"
sudo mount -t cifs "//$WORKSTATION_IP/shared" "$MOUNT_DIR" -o user=$USERNAME

if [ $? -eq 0 ]; then
    echo "✅ 挂载成功！"
    echo ""
    echo "访问共享文件：cd $MOUNT_DIR"
    echo "卸载共享：sudo umount $MOUNT_DIR"
else
    echo "❌ 挂载失败，请检查："
    echo "  1. 工作站 IP 是否正确"
    echo "  2. SMB 服务是否运行"
    echo "  3. 用户名密码是否正确"
fi

echo ""
echo "【直接访问命令】"
echo "  浏览共享：smbclient //$WORKSTATION_IP/shared -U $USERNAME"
echo "  复制文件：smbclient //$WORKSTATION_IP/shared -U $USERNAME -c 'get filename'"
echo ""
EOF

chmod +x "$ACCESS_SCRIPT"
log_info "✅ 访问脚本已创建"
echo "  位置：$ACCESS_SCRIPT"
echo "  使用：运行 ./access-workstation.sh"
echo ""

# 6. 创建数据调取脚本
log_info "创建数据调取脚本..."
REQUEST_SCRIPT="$HOME/request-from-workstation.sh"
cat > "$REQUEST_SCRIPT" << 'EOF'
#!/bin/bash
# 从工作站调取数据

SYNC_DIR="$HOME/laptop-sync/sync-to-workstation/requests"
mkdir -p "$SYNC_DIR"

echo "=========================================="
echo "从工作站调取数据"
echo "=========================================="
echo ""

read -p "请输入要调取的文件路径 (相对于工作站共享目录): " FILE_PATH
read -p "请输入备注 (可选): " MEMO

REQUEST_ID="req-$(date +%Y%m%d-%H%M%S)"

cat > "$SYNC_DIR/$REQUEST_ID.json" << REQUEST
{
  "request_id": "$REQUEST_ID",
  "type": "data_retrieval",
  "files": ["$FILE_PATH"],
  "memo": "$MEMO",
  "created_at": "$(date -Iseconds)"
}
REQUEST

echo ""
echo "✅ 请求已创建！"
echo "  请求 ID: $REQUEST_ID"
echo "  文件：$SYNC_DIR/$REQUEST_ID.json"
echo ""
echo "等待工作站处理后，结果将同步到："
echo "  \$HOME/laptop-sync/sync-from-workstation/results/"
echo ""
EOF

chmod +x "$REQUEST_SCRIPT"
log_info "✅ 调取脚本已创建"
echo "  位置：$REQUEST_SCRIPT"
echo "  使用：运行 ./request-from-workstation.sh"
echo ""

# 7. 配置防火墙
log_info "配置防火墙..."
sudo ufw allow 22000/tcp comment "Syncthing 文件传输" 2>/dev/null || true
sudo ufw allow 22000/udp comment "Syncthing 发现协议" 2>/dev/null || true
sudo ufw allow 21027/udp comment "Syncthing 本地发现" 2>/dev/null || true
sudo ufw allow 41641/udp comment "Tailscale" 2>/dev/null || true
log_info "✅ 防火墙规则已配置"
echo ""

# 8. 显示配置信息
echo "=========================================="
log_info "✅ 笔记本配置完成！"
echo "=========================================="
echo ""
echo "【Tailscale】"
echo "  登录：sudo tailscale up"
echo "  状态：$(systemctl is-active tailscaled 2>/dev/null || echo "未运行")"
echo ""
echo "【Syncthing】"
echo "  Web 界面：http://127.0.0.1:8384"
echo "  状态：$(systemctl --user is-active syncthing 2>/dev/null || echo "未运行")"
echo ""
echo "【同步目录】"
echo "  位置：$LAPTOP_SYNC"
echo "  发送到工作站：$LAPTOP_SYNC/sync-to-workstation/"
echo "  从工作站接收：$LAPTOP_SYNC/sync-from-workstation/"
echo ""
echo "【访问工作站】"
echo "  脚本 1: $ACCESS_SCRIPT (SMB 共享访问)"
echo "  脚本 2: $REQUEST_SCRIPT (数据调取请求)"
echo ""
echo "【下一步】"
echo "  1. 登录 Tailscale: sudo tailscale up"
echo "  2. 访问 Syncthing Web: http://127.0.0.1:8384"
echo "  3. 添加工作站设备 ID"
echo "  4. 配置单向同步文件夹"
echo "  5. 运行 ./access-workstation.sh 访问工作站共享"
echo ""
echo "=========================================="
