#!/bin/bash
# 太一 Git 自动备份脚本
# 功能：推送关键配置到 GitHub 私有仓库
# 执行时间：每周日 23:00 (备份邮件前 1 小时)

set -e

WORKSPACE_DIR="/home/nicola/.openclaw/workspace"
BACKUP_REPO="https://github.com/nicola-king/taiyi-backup.git"
BACKUP_DIR="/tmp/taiyi-git-backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 创建临时备份目录
log_info "创建备份目录..."
rm -rf "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# 复制关键文件 (脱敏处理)
log_info "复制关键文件..."

# ✅ 复制：宪法/记忆/架构文档
cp -r "$WORKSPACE_DIR/constitution" "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$WORKSPACE_DIR/memory" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/MEMORY.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/AGENTS.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/SOUL.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/TAIYI-ARCHITECTURE.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/SMART-AUTOMATION-ARCHITECTURE.md" "$BACKUP_DIR/" 2>/dev/null || true

# ❌ 排除：敏感配置 (API Key/密码)
cat > "$BACKUP_DIR/.gitignore" << 'EOF'
# 敏感信息
*.env
**/config.json
**/credentials.json
**/*secret*
**/*password*
**/*token*
logs/
tmp/
.cache/
EOF

# 创建备份说明
cat > "$BACKUP_DIR/README.md" << EOF
# 太一 AGI 备份

**备份时间**: $TIMESTAMP
**版本**: v31.0 (协议版)
**用途**: 灾难恢复 + 版本控制

---

## 📦 备份内容

- ✅ 宪法文件 (constitution/)
- ✅ 记忆系统 (memory/)
- ✅ 核心配置 (AGENTS.md, SOUL.md)
- ✅ 架构文档 (TAIYI-ARCHITECTURE.md)

## ⚠️ 排除内容

- ❌ API Key (敏感信息)
- ❌ 环境变量
- ❌ 日志文件

---

## 🔄 恢复步骤

1. Clone 仓库
2. 手动配置 API Key
3. 运行 openclaw gateway start

---

*太一 AGI · 反脆弱备份系统*
EOF

# Git 推送
log_info "推送到 GitHub..."
cd "$BACKUP_DIR"
git init
git config user.email "285915125@qq.com"
git config user.name "Taiyi AGI"
git add .
git commit -m "📦 太一备份 $TIMESTAMP [自动]"

# 检查是否有远程仓库
if git remote | grep -q origin; then
    log_info "使用现有远程仓库..."
else
    log_info "添加远程仓库..."
    git remote add origin "$BACKUP_REPO" 2>/dev/null || log_warn "远程仓库已存在"
fi

# 推送 (需要 GitHub Token 或 SSH Key)
if git push -u origin main 2>/dev/null; then
    log_info "✅ Git 推送成功！"
    log_info "仓库：$BACKUP_REPO"
else
    log_warn "❌ Git 推送失败 (需要认证)"
    log_info "解决方案:"
    log_info "1. 配置 SSH Key: ssh-keygen && ssh-add"
    log_info "2. 或配置 GitHub Token: git remote set-url origin https://TOKEN@github.com/..."
    log_info "3. 备份文件保存在：$BACKUP_DIR"
fi

# 清理
log_info "清理临时文件..."
# 保留备份目录供检查
# rm -rf "$BACKUP_DIR"

log_info "✅ Git 备份完成！"
