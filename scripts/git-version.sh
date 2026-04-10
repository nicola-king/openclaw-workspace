#!/bin/bash
#
# Git Version Script (Git 版本管理)
#
# 功能:
# 1. 自动创建 CalVer 版本标签
# 2. 检测同日迭代版本
# 3. 推送标签到远程
# 4. 生成发布说明框架
#
# 灵感来源：OpenClaw v2026.4.9 iOS Version Pinning
#
# 作者：太一 AGI
# 创建：2026-04-10
#

set -e

# 配置
WORKSPACE="/home/nicola/.openclaw/workspace"
RELEASES_DIR="${WORKSPACE}/reports/releases"
LOG_FILE="${WORKSPACE}/logs/git-version-$(date +%Y%m%d-%H%M%S).log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

success() {
    echo -e "${GREEN}[OK]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$RELEASES_DIR"

log "═══════════════════════════════════════════════════════════"
log "Git 版本管理 - CalVer Versioning"
log "═══════════════════════════════════════════════════════════"
log ""

# 生成版本号
VERSION="v$(date +%Y.%m.%d)"
ITERATION=1

log "基础版本：$VERSION"

# 检查今日是否已有标签
log "检查现有标签..."
while git rev-parse "${VERSION}-${ITERATION}" >/dev/null 2>&1; do
    ITERATION=$((ITERATION + 1))
done

if [ $ITERATION -gt 1 ]; then
    FULL_VERSION="${VERSION}-${ITERATION}"
    warn "检测到今日已有 $((ITERATION - 1)) 个发布，使用迭代版本：$FULL_VERSION"
else
    FULL_VERSION="${VERSION}"
    success "今日首次发布"
fi

log ""
log "完整版本号：$FULL_VERSION"
log ""

# 检查 Git 状态
log "检查 Git 状态..."
if [ -n "$(git status --porcelain)" ]; then
    warn "工作区有未提交的变更"
    echo ""
    git status --short
    echo ""
    read -p "是否继续发布？(y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        error "发布已取消"
    fi
else
    success "工作区干净"
fi
log ""

# 创建标签
log "创建版本标签..."
git tag -a "$FULL_VERSION" -m "太一 AGI 发布 $FULL_VERSION"
success "标签创建成功"
log ""

# 推送标签
log "推送标签到远程..."
if git push origin "$FULL_VERSION" 2>&1 | tee -a "$LOG_FILE"; then
    success "标签推送成功"
else
    error "标签推送失败"
fi
log ""

# 生成发布说明框架
RELEASE_NOTE="${RELEASES_DIR}/release-${FULL_VERSION}.md"
log "生成发布说明框架..."

cat > "$RELEASE_NOTE" << EOF
# 太一 AGI 发布 · ${FULL_VERSION}

> **发布日期**: $(date +%Y-%m-%d)  
> **类型**: 功能发布

---

## 🎯 核心更新

### 新增功能
- 

### 功能增强
- 

### Bug 修复
- 

### 文档更新
- 

---

## 📊 统计

| 指标 | 数值 |
|------|------|
| Git 提交 | $(git rev-list --count HEAD) |
| 新增文件 | $(git diff-tree --no-commit-id --name-only -r ${FULL_VERSION} 2>/dev/null | wc -l || echo "N/A") |

---

## 🙏 致谢

- 灵感来源：OpenClaw v2026.4.9

---

*太一 AGI · 自动发布系统*
EOF

success "发布说明已生成：$RELEASE_NOTE"
log ""

# 显示版本信息
log "═══════════════════════════════════════════════════════════"
log "版本发布完成"
log "═══════════════════════════════════════════════════════════"
log "版本号：$FULL_VERSION"
log "标签：$(git show-ref --tags | grep "$FULL_VERSION" | head -1 | cut -d' ' -f1)"
log "发布说明：$RELEASE_NOTE"
log "日志文件：$LOG_FILE"
log ""

success "✅ 版本发布完成"
echo ""
echo "下一步:"
echo "  1. 编辑发布说明：$RELEASE_NOTE"
echo "  2. 查看版本历史：git tag -l \"v$(date +%Y.%m).*\" | sort -V"
echo "  3. 查看版本差异：git diff $(git describe --tags --abbrev=0 HEAD^)..$FULL_VERSION"
echo ""

exit 0
