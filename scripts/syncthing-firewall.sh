#!/bin/bash
# syncthing-firewall.sh - Syncthing 单向传输防火墙配置
# 用途：禁止外部设备主动向工控机传输文件

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Syncthing 单向传输防火墙配置 ===${NC}"
echo ""

# 检查 sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用 sudo 运行此脚本${NC}"
    echo "sudo ./syncthing-firewall.sh"
    exit 1
fi

# 安装 UFW
echo -e "${YELLOW}[1/5] 安装 UFW...${NC}"
apt install -y ufw

# 配置 UFW 默认策略
echo -e "${YELLOW}[2/5] 配置默认策略...${NC}"
ufw default deny incoming  # 拒绝所有入站
ufw default allow outgoing # 允许所有出站

# 允许 SSH (如果需要远程管理)
echo -e "${YELLOW}[3/5] 允许 SSH...${NC}"
ufw allow 22/tcp comment "SSH remote management"

# 允许 Syncthing 出站 (工控机主动推送)
echo -e "${YELLOW}[4/5] 配置 Syncthing 规则...${NC}"
# 拒绝 Syncthing 入站 (禁止外部主动连接)
ufw deny in 22000/tcp comment "Block Syncthing incoming file transfer"
ufw deny in 21027/udp comment "Block Syncthing incoming discovery"
# 允许 Syncthing 出站 (工控机主动推送)
ufw allow out 22000/tcp comment "Allow Syncthing outgoing file transfer"
ufw allow out 21027/udp comment "Allow Syncthing outgoing discovery"

# 允许本地回环
ufw allow in on lo comment "Allow localhost"
ufw allow out on lo comment "Allow localhost"

# 启用 UFW
echo -e "${YELLOW}[5/5] 启用 UFW...${NC}"
echo "y" | ufw enable

# 显示状态
echo ""
echo -e "${GREEN}=== 配置完成 ===${NC}"
ufw status verbose

echo ""
echo -e "${YELLOW}Syncthing 单向传输规则:${NC}"
echo "✅ 工控机可以主动向外推送文件"
echo "❌ 外部设备无法主动向工控机传输文件"
echo ""
echo "Web 界面仍可本地访问：http://localhost:8384"
