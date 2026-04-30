#!/bin/bash
# 太一宪法恢复脚本
# 用法：./restore-constitution.sh <backup-file.tar.gz>

set -e

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "用法：$0 <backup-file.tar.gz>"
    echo ""
    echo "示例:"
    echo "  $0 /opt/taiyi-backup/taiyi-backup-20260326-235200.tar.gz"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ 备份文件不存在：$BACKUP_FILE"
    exit 1
fi

echo "=========================================="
echo "太一宪法恢复"
echo "=========================================="
echo ""
echo "【警告】这将覆盖现有配置！"
echo ""
read -p "确认恢复？(yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ 取消恢复"
    exit 1
fi

# 1. 验证备份
echo "【1/5】验证备份完整性..."
if [ -f "${BACKUP_FILE}.sha256" ]; then
    cd $(dirname $BACKUP_FILE)
    if sha256sum -c "$(basename $BACKUP_FILE).sha256" > /dev/null 2>&1; then
        echo "✅ 备份验证通过"
    else
        echo "❌ 备份验证失败！文件可能已损坏"
        exit 1
    fi
else
    echo "⚠️  未找到 SHA256 文件，跳过验证"
fi
echo ""

# 2. 解压备份
echo "【2/5】解压备份..."
BACKUP_DIR=$(dirname $BACKUP_FILE)
TIMESTAMP=$(basename $BACKUP_FILE .tar.gz | sed 's/taiyi-backup-//')
TEMP_DIR="/tmp/taiyi-restore-$TIMESTAMP"

mkdir -p "$TEMP_DIR"
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
echo "✅ 解压完成：$TEMP_DIR"
echo ""

# 3. 备份现有配置
echo "【3/5】备份现有配置..."
OLD_BACKUP="/opt/taiyi-backup/pre-restore-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OLD_BACKUP"

cp -r /home/nicola/.openclaw/workspace/constitution "$OLD_BACKUP/" 2>/dev/null || true
cp -r /home/nicola/.openclaw/workspace/memory "$OLD_BACKUP/" 2>/dev/null || true
cp /home/nicola/.openclaw/workspace/*.md "$OLD_BACKUP/" 2>/dev/null || true

echo "✅ 现有配置已备份：$OLD_BACKUP"
echo ""

# 4. 恢复文件
echo "【4/5】恢复文件..."
WORKSPACE="/home/nicola/.openclaw/workspace"

# 恢复宪法文档
if [ -d "$TEMP_DIR/$TIMESTAMP/constitution" ]; then
    rm -rf "$WORKSPACE/constitution"
    cp -r "$TEMP_DIR/$TIMESTAMP/constitution" "$WORKSPACE/"
    echo "  ✅ 宪法文档"
fi

# 恢复记忆体系
if [ -d "$TEMP_DIR/$TIMESTAMP/memory" ]; then
    rm -rf "$WORKSPACE/memory"
    cp -r "$TEMP_DIR/$TIMESTAMP/memory" "$WORKSPACE/"
    echo "  ✅ 记忆体系"
fi

# 恢复核心文件
for file in MEMORY.md HEARTBEAT.md SOUL.md USER.md TOOLS.md AGENTS.md; do
    if [ -f "$TEMP_DIR/$TIMESTAMP/$file" ]; then
        cp "$TEMP_DIR/$TIMESTAMP/$file" "$WORKSPACE/"
        echo "  ✅ $file"
    fi
done

# 恢复技能目录
if [ -d "$TEMP_DIR/$TIMESTAMP/skills" ]; then
    rm -rf "$WORKSPACE/skills"
    cp -r "$TEMP_DIR/$TIMESTAMP/skills" "$WORKSPACE/"
    echo "  ✅ 技能目录"
fi

# 恢复脚本目录
if [ -d "$TEMP_DIR/$TIMESTAMP/scripts" ]; then
    rm -rf "$WORKSPACE/scripts"
    cp -r "$TEMP_DIR/$TIMESTAMP/scripts" "$WORKSPACE/"
    echo "  ✅ 脚本目录"
fi

echo ""

# 5. 清理
echo "【5/5】清理临时文件..."
rm -rf "$TEMP_DIR"
echo "✅ 临时文件已清理"
echo ""

echo "=========================================="
echo "✅ 恢复完成！"
echo "=========================================="
echo ""
echo "请重启 OpenClaw Gateway:"
echo "  openclaw gateway restart"
echo ""
echo "或者重新登录 Telegram Bot"
echo ""
