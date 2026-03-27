#!/bin/bash
# 发送宪法备份到邮箱
# 用法：./email-constitution.sh <backup-file>

BACKUP_FILE=${1:-$(ls -t /opt/taiyi-backup/taiyi-backup-*.tar.gz | head -1)}
TO_EMAIL="285915125@qq.com"
TIMESTAMP=$(basename $BACKUP_FILE .tar.gz | sed 's/taiyi-backup-//')
SHA256=$(cat "${BACKUP_FILE}.sha256" 2>/dev/null | awk '{print $1}')

echo "=========================================="
echo "发送宪法备份到邮箱"
echo "=========================================="
echo ""
echo "收件人：$TO_EMAIL"
echo "备份文件：$BACKUP_FILE"
echo "序列号：TY-CONSTITUTION-$TIMESTAMP"
echo ""

# 检查 mutt 是否安装
if command -v mutt &> /dev/null; then
    echo "使用 mutt 发送..."
    
    cat << EOF | mutt -s "太一宪法备份 - $TIMESTAMP" -a "$BACKUP_FILE" -- "$TO_EMAIL"
太一宪法备份

序列号：TY-CONSTITUTION-$TIMESTAMP
创建时间：$(date -Iseconds)
文件大小：$(du -h "$BACKUP_FILE" | cut -f1)
SHA256: $SHA256

备份内容:
- ✅ 宪法文档 (constitution/)
- ✅ 记忆体系 (memory/)
- ✅ 核心文件 (MEMORY.md, HEARTBEAT.md, SOUL.md, ...)
- ✅ 技能目录 (skills/)
- ✅ 脚本目录 (scripts/)

恢复指南:
  tar -xzf $(basename $BACKUP_FILE)
  cd $TIMESTAMP
  bash restore.sh

请妥善保存此邮件和备份文件，用于系统恢复。

--
太一 AGI 自动备份系统
EOF
    
    echo "✅ 邮件已发送到 $TO_EMAIL"
else
    echo "❌ mutt 未安装"
    echo ""
    echo "安装命令：sudo apt install mutt"
    echo ""
    echo "或者手动发送:"
    echo "  1. 复制备份文件"
    echo "  2. 打开邮箱客户端"
    echo "  3. 发送到：$TO_EMAIL"
    echo "  4. 主题：太一宪法备份 - $TIMESTAMP"
fi

echo ""
