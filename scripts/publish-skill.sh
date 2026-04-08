#!/bin/bash
# Skill 发布脚本 - 太一 AGI v5.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SKILLS_DIR="/home/nicola/.openclaw/workspace/skills"
PUBLISH_DIR="/tmp/skill-publish"

usage() {
    echo "用法：$0 <skill-name> [github-repo]"
    echo ""
    echo "示例:"
    echo "  $0 git-integration"
    echo "  $0 docker-ctl https://github.com/nicola-king/openclaw-docker-ctl.git"
    echo ""
    echo "可用 Skills:"
    ls "$SKILLS_DIR" | head -20
    exit 1
}

# 检查参数
if [ -z "$1" ]; then
    usage
fi

SKILL_NAME=$1
GITHUB_REPO=$2

SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"

# 检查 Skill 是否存在
if [ ! -d "$SKILL_PATH" ]; then
    log_error "Skill 不存在：$SKILL_NAME"
    exit 1
fi

# 检查 SKILL.md
if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
    log_error "缺少 SKILL.md 文件"
    exit 1
fi

log_info "准备发布 Skill: $SKILL_NAME"

# 创建临时目录
rm -rf "$PUBLISH_DIR"
mkdir -p "$PUBLISH_DIR"
cd "$PUBLISH_DIR"

# 复制 Skill 文件
log_info "复制 Skill 文件..."
cp -r "$SKILL_PATH/"* .

# 创建 clawhub.yaml（如果不存在）
if [ ! -f "clawhub.yaml" ]; then
    log_info "创建 clawhub.yaml..."
    cat > clawhub.yaml <<EOF
name: $SKILL_NAME
version: 1.0.0
description: $SKILL_NAME Skill for OpenClaw
author: 太一 AGI <taiyi@sayelf.com>
license: MIT
tags:
  - $SKILL_NAME
  - openclaw
category: Tools
min_openclaw_version: 2026.3.28
pricing:
  type: free
  price: 0
  currency: CNY
EOF
fi

# 创建 README.md（如果不存在）
if [ ! -f "README.md" ]; then
    log_info "创建 README.md..."
    cat > README.md <<EOF
# $SKILL_NAME Skill

$SKILL_NAME Skill for OpenClaw

## Installation

\`\`\`bash
# Clone to skills directory
git clone <repository-url> ~/.openclaw/workspace/skills/$SKILL_NAME

# Or use clawhub
clawhub install $SKILL_NAME
\`\`\`

## Usage

\`\`\`bash
# Use with Taiyi AGI
<command examples>
\`\`\`

## License

MIT
EOF
fi

# Git 初始化
if [ -n "$GITHUB_REPO" ]; then
    log_info "初始化 Git 仓库..."
    git init
    git add .
    git commit -m "feat: $SKILL_NAME skill v1.0.0"
    
    log_info "添加远程仓库..."
    git remote add origin "$GITHUB_REPO"
    
    log_info "推送到 GitHub..."
    git push -u origin main
    
    log_success "发布完成!"
    echo ""
    echo "GitHub 仓库：$GITHUB_REPO"
    echo "ClawHub 页面：https://clawhub.ai/skill/$SKILL_NAME"
else
    log_info "打包 Skill..."
    cd "$PUBLISH_DIR"
    tar -czf "/tmp/${SKILL_NAME}.tar.gz" .
    
    log_success "打包完成!"
    echo ""
    echo "压缩包：/tmp/${SKILL_NAME}.tar.gz"
    echo ""
    echo "下一步:"
    echo "  1. 创建 GitHub 仓库并推送"
    echo "  2. 或发布到 ClawHub: clawhub publish $SKILL_NAME"
    echo "  3. 或直接分享压缩包"
fi

# 清理
cd /
# rm -rf "$PUBLISH_DIR"

log_info "完成!"
