#!/bin/bash
# qq-email-backup.sh - QQ 邮箱定时备份脚本
# 用途：每周自动打包并发送备份到 QQ 邮箱

set -e

# ============ 配置区 ============
QQ_EMAIL="285915125@qq.com"
QQ_AUTH_CODE="czzbhqkqewqxcafd"
BACKUP_NAME="taiyi-backup"
BACKUP_DIRS=(
    "/home/nicola/.openclaw/workspace"
    "/home/nicola/.config/syncthing"
)
BACKUP_DEST="/tmp/backup"
MAX_ATTACHMENT_SIZE=45000000
# =================================

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
BACKUP_FILE="${BACKUP_DEST}/${BACKUP_NAME}-${TIMESTAMP}.tar.gz"

echo -e "${GREEN}=== QQ 邮箱定时备份 ===${NC}"
echo "时间：$(date)"
echo "目标邮箱：${QQ_EMAIL}"
echo ""

# 临时禁用代理 (SMTP 不需要代理)
export NO_PROXY="${NO_PROXY},smtp.qq.com"
unset HTTP_PROXY HTTPS_PROXY

# 创建备份目录
echo -e "${YELLOW}[1/4] 创建备份目录...${NC}"
mkdir -p "${BACKUP_DEST}"

# 打包备份
echo -e "${YELLOW}[2/4] 打包备份文件...${NC}"
tar -czf "${BACKUP_FILE}" "${BACKUP_DIRS[@]}" 2>/dev/null || {
    echo -e "${RED}打包失败，尝试逐个目录备份...${NC}"
    for dir in "${BACKUP_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            dir_name=$(basename "$dir")
            tar -czf "${BACKUP_DEST}/${BACKUP_NAME}-${dir_name}-${TIMESTAMP}.tar.gz" "$dir" 2>/dev/null && \
            echo -e "${GREEN}✓ 备份：$dir${NC}"
        else
            echo -e "${YELLOW}⚠ 跳过：$dir (不存在)${NC}"
        fi
    done
}

# 检查文件大小
BACKUP_SIZE=$(du -b "${BACKUP_FILE}" 2>/dev/null | cut -f1 || echo "0")
echo -e "${YELLOW}[3/4] 备份文件大小：$(du -h "${BACKUP_FILE}" | cut -f1)${NC}"

if [ "$BACKUP_SIZE" -gt "$MAX_ATTACHMENT_SIZE" ]; then
    echo -e "${RED}✗ 文件过大 (>45MB)，需要分卷压缩${NC}"
    exit 1
fi

# 使用 Python 发送
echo -e "${YELLOW}[4/4] 发送邮件...${NC}"
python3 << PYTHON
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

QQ_EMAIL = "${QQ_EMAIL}"
QQ_AUTH_CODE = "${QQ_AUTH_CODE}"
SUBJECT = "[太一备份] $(date '+%Y-%m-%d %H:%M')"
BODY = """太一系统自动备份

备份时间：$(date)
备份文件：$(basename ${BACKUP_FILE})
文件大小：$(du -h ${BACKUP_FILE} | cut -f1)

---
太一 AGI 系统 | 自动备份"""
BACKUP_FILE = "${BACKUP_FILE}"

msg = MIMEMultipart()
msg['From'] = QQ_EMAIL
msg['To'] = QQ_EMAIL
msg['Subject'] = SUBJECT
msg.attach(MIMEText(BODY, 'plain'))

try:
    with open(BACKUP_FILE, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(BACKUP_FILE)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)
    
    server = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=30)
    server.set_debuglevel(0)
    server.login(QQ_EMAIL, QQ_AUTH_CODE)
    server.send_message(msg)
    server.quit()
    print("✓ 邮件发送成功")
except Exception as e:
    print(f"✗ 邮件发送失败：{e}")
    exit(1)
PYTHON

# 清理旧备份 (保留最近 4 个)
echo -e "${YELLOW}清理旧备份...${NC}"
ls -t "${BACKUP_DEST}"/${BACKUP_NAME}-*.tar.gz 2>/dev/null | tail -n +5 | xargs rm -f 2>/dev/null || true

echo ""
echo -e "${GREEN}=== 备份完成 ===${NC}"
echo "备份文件：${BACKUP_FILE}"
