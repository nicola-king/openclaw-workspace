#!/bin/bash
# syncthing-restore.sh - Syncthing 按需恢复脚本
# 用途：从工作站拉取备份文件到工控机

set -e

# 配置
WORKSTATION_HOST="192.168.1.100"  # 工作站 IP
WORKSTATION_PORT="8384"
WORKSTATION_API_KEY="YOUR_API_KEY_HERE"  # 从工作站 Web 界面获取
LOCAL_SYNC_DIR="/home/nicola/Sync"
REMOTE_FOLDER_ID="default"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Syncthing 按需恢复 ===${NC}"
echo "工作站：${WORKSTATION_HOST}:${WORKSTATION_PORT}"
echo "本地目录：${LOCAL_SYNC_DIR}"
echo ""

# 检查连接
echo -e "${YELLOW}[1/4] 检查工作站连接...${NC}"
if curl -s "http://${WORKSTATION_HOST}:${WORKSTATION_PORT}/rest/system/status" > /dev/null; then
    echo -e "${GREEN}✓ 工作站连接成功${NC}"
else
    echo -e "${RED}✗ 工作站连接失败${NC}"
    exit 1
fi

# 获取远程文件列表
echo -e "${YELLOW}[2/4] 获取远程文件列表...${NC}"
curl -s "http://${WORKSTATION_HOST}:${WORKSTATION_PORT}/rest/db/files?folder=${REMOTE_FOLDER_ID}" \
    -H "X-API-Key: ${WORKSTATION_API_KEY}" | jq '. | length'

# 触发恢复
echo -e "${YELLOW}[3/4] 触发恢复操作...${NC}"
curl -X POST "http://${WORKSTATION_HOST}:${WORKSTATION_PORT}/rest/db/override" \
    -H "X-API-Key: ${WORKSTATION_API_KEY}" \
    -d "folder=${REMOTE_FOLDER_ID}"

# 等待同步
echo -e "${YELLOW}[4/4] 等待同步完成...${NC}"
sleep 5
echo -e "${GREEN}✓ 恢复触发完成${NC}"
echo ""
echo "请检查本地目录：${LOCAL_SYNC_DIR}"
