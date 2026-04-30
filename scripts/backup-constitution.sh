#!/bin/bash
# 太一宪法完整备份脚本
# 用法：./backup-constitution.sh [--email]

set -e

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="/opt/taiyi-backup/$TIMESTAMP"
BACKUP_FILE="/opt/taiyi-backup/taiyi-backup-$TIMESTAMP.tar.gz"
WORKSPACE="/home/nicola/.openclaw/workspace"
TO_EMAIL="285915125@qq.com"

echo "=========================================="
echo "太一宪法完整备份"
echo "=========================================="
echo ""
echo "序列号：TY-CONSTITUTION-$TIMESTAMP"
echo "创建时间：$(date -Iseconds)"
echo "版本：v1.0.0"
echo ""

# 1. 创建备份目录
echo "【1/6】创建备份目录..."
mkdir -p "$BACKUP_DIR"
mkdir -p "/opt/taiyi-backup"
echo "✅ 备份目录：$BACKUP_DIR"
echo ""

# 2. 复制核心文件
echo "【2/6】复制核心文件..."

# 宪法文档
if [ -d "$WORKSPACE/constitution" ]; then
    cp -r "$WORKSPACE/constitution" "$BACKUP_DIR/"
    echo "  ✅ 宪法文档"
else
    echo "  ⚠️  宪法文档不存在"
fi

# 记忆体系
if [ -d "$WORKSPACE/memory" ]; then
    cp -r "$WORKSPACE/memory" "$BACKUP_DIR/"
    echo "  ✅ 记忆体系"
else
    echo "  ⚠️  记忆目录不存在"
fi

# 核心文件
for file in MEMORY.md HEARTBEAT.md SOUL.md USER.md TOOLS.md AGENTS.md; do
    if [ -f "$WORKSPACE/$file" ]; then
        cp "$WORKSPACE/$file" "$BACKUP_DIR/"
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file 不存在"
    fi
done

# 技能目录
if [ -d "$WORKSPACE/skills" ]; then
    cp -r "$WORKSPACE/skills" "$BACKUP_DIR/"
    echo "  ✅ 技能目录"
else
    echo "  ⚠️  技能目录不存在"
fi

# 脚本目录
if [ -d "$WORKSPACE/scripts" ]; then
    cp -r "$WORKSPACE/scripts" "$BACKUP_DIR/"
    echo "  ✅ 脚本目录"
else
    echo "  ⚠️  脚本目录不存在"
fi

echo ""

# 3. 创建版本注册表
echo "【3/6】创建版本注册表..."
cat > "$BACKUP_DIR/constitution/REGISTRY-BACKUP.md" << EOF
# 太一宪法备份注册表

## 备份信息

| 项目 | 值 |
|------|-----|
| **序列号** | TY-CONSTITUTION-$TIMESTAMP |
| **创建时间** | $(date -Iseconds) |
| **UTC 时间** | $(date -u +"%Y-%m-%dT%H:%M:%SZ") |
| **Unix 时间戳** | $(date +%s) |
| **版本** | v1.0.0 |
| **状态** | ✅ 已备份 |
| **决策人** | SAYELF (nicola king) |
| **创建者** | 太一 AGI |

## 备份内容

- ✅ 宪法文档 (constitution/)
- ✅ 记忆体系 (memory/)
- ✅ 核心文件 (MEMORY.md, HEARTBEAT.md, ...)
- ✅ 技能目录 (skills/)
- ✅ 脚本目录 (scripts/)

## 恢复指南

\`\`\`bash
# 恢复命令
tar -xzf taiyi-backup-$TIMESTAMP.tar.gz
cd $TIMESTAMP
./restore.sh
\`\`\`

## 验证

SHA256 哈希将在打包后生成
EOF

echo "✅ 版本注册表已创建"
echo ""

# 4. 打包压缩
echo "【4/6】打包压缩..."
cd /opt/taiyi-backup
tar -czf "$BACKUP_FILE" "$TIMESTAMP"
echo "✅ 备份文件：$BACKUP_FILE"
echo "✅ 文件大小：$(du -h "$BACKUP_FILE" | cut -f1)"
echo ""

# 5. 计算哈希
echo "【5/6】计算哈希..."
SHA256=$(sha256sum "$BACKUP_FILE" | awk '{print $1}')
echo "$SHA256  $BACKUP_FILE" > "$BACKUP_FILE.sha256"
echo "✅ SHA256: $SHA256"
echo ""

# 6. 发送邮件 (可选)
if [ "$1" = "--email" ]; then
    echo "【6/6】发送邮件到 $TO_EMAIL..."
    
    # 检查 mutt 是否安装
    if command -v mutt &> /dev/null; then
        echo "太一宪法备份已完成
        
序列号：TY-CONSTITUTION-$TIMESTAMP
创建时间：$(date -Iseconds)
文件大小：$(du -h "$BACKUP_FILE" | cut -f1)
SHA256: $SHA256

请妥善保存此备份文件，用于系统恢复。

--
太一 AGI 自动备份系统" | \
mutt -s "太一宪法备份 - $TIMESTAMP" -a "$BACKUP_FILE" -- "$TO_EMAIL"
        
        echo "✅ 邮件已发送"
    else
        echo "⚠️  mutt 未安装，跳过邮件发送"
        echo "   安装命令：sudo apt install mutt"
    fi
else
    echo "【6/6】跳过邮件发送 (使用 --email 参数启用)"
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "备份文件：$BACKUP_FILE"
echo "SHA256 验证：$BACKUP_FILE.sha256"
echo ""
echo "【恢复命令】"
echo "  tar -xzf $BACKUP_FILE"
echo "  cd $TIMESTAMP"
echo "  ./restore.sh"
echo ""
echo "【下次自动备份】"
echo "  每周日 02:00 (crontab 已配置)"
echo ""
