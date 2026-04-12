#!/bin/bash
# 技能安装脚本
# 用法：./install-skill.sh <source> <skill-name-or-url>

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE/skills"
LOG_FILE="$WORKSPACE/logs/skill-install.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 从 ClawHub 安装
install_from_clawhub() {
    local skill_name=$1
    log "从 ClawHub 安装：$skill_name"
    
    # 检查 clawhub CLI 是否可用
    if ! command -v clawhub &> /dev/null; then
        log "🔴 clawhub CLI 未安装"
        echo "请先安装：npm install -g clawhub"
        exit 1
    fi
    
    # 使用 clawhub 安装
    cd "$SKILLS_DIR"
    clawhub install "$skill_name"
    
    if [ $? -eq 0 ]; then
        log "✅ 安装成功：$skill_name"
        echo "🎉 技能 '$skill_name' 安装完成!"
        echo "📁 位置：$SKILLS_DIR/$skill_name"
    else
        log "🔴 安装失败：$skill_name"
        exit 1
    fi
}

# 从 GitHub 安装
install_from_github() {
    local repo_url=$1
    local skill_name=$(basename "$repo_url" .git)
    log "从 GitHub 安装：$repo_url"
    
    # 克隆仓库
    cd "$SKILLS_DIR"
    git clone "$repo_url" "$skill_name"
    
    # 检查是否有 SKILL.md
    if [ ! -f "$SKILLS_DIR/$skill_name/SKILL.md" ]; then
        log "🔴 未找到 SKILL.md，可能不是有效的 OpenClaw Skill"
        echo "⚠️ 警告：该仓库缺少 SKILL.md，可能不是有效的 OpenClaw Skill"
        read -p "是否继续安装？(y/N): " confirm
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            rm -rf "$SKILLS_DIR/$skill_name"
            exit 1
        fi
    fi
    
    # 安装依赖
    if [ -f "$SKILLS_DIR/$skill_name/requirements.txt" ]; then
        log "安装 Python 依赖..."
        pip install -r "$SKILLS_DIR/$skill_name/requirements.txt"
    fi
    
    # 设置执行权限
    find "$SKILLS_DIR/$skill_name" -name "*.sh" -exec chmod +x {} \;
    
    log "✅ 安装成功：$skill_name"
    echo "🎉 技能 '$skill_name' 安装完成!"
    echo "📁 位置：$SKILLS_DIR/$skill_name"
}

# 本地安装
install_from_local() {
    local source_path=$1
    local skill_name=$(basename "$source_path")
    log "从本地安装：$source_path"
    
    # 复制到 skills 目录
    cp -r "$source_path" "$SKILLS_DIR/$skill_name"
    
    # 检查 SKILL.md
    if [ ! -f "$SKILLS_DIR/$skill_name/SKILL.md" ]; then
        log "🔴 未找到 SKILL.md"
        echo "🔴 错误：缺少 SKILL.md"
        exit 1
    fi
    
    # 安装依赖
    if [ -f "$SKILLS_DIR/$skill_name/requirements.txt" ]; then
        log "安装 Python 依赖..."
        pip install -r "$SKILLS_DIR/$skill_name/requirements.txt"
    fi
    
    # 设置执行权限
    find "$SKILLS_DIR/$skill_name" -name "*.sh" -exec chmod +x {} \;
    
    log "✅ 安装成功：$skill_name"
    echo "🎉 技能 '$skill_name' 安装完成!"
    echo "📁 位置：$SKILLS_DIR/$skill_name"
}

# 安全扫描
security_scan() {
    local skill_name=$1
    log "执行安全扫描：$skill_name"
    
    if [ -f "$SKILLS_DIR/smart-skills-manager/modules/security/security-scan.py" ]; then
        python3 "$SKILLS_DIR/smart-skills-manager/modules/security/security-scan.py" "$SKILLS_DIR/$skill_name"
        
        if [ $? -ne 0 ]; then
            log "🔴 安全扫描失败"
            echo "🔴 安全扫描发现严重问题，安装中止"
            exit 1
        fi
    else
        log "⚠️ 安全扫描模块不可用，跳过扫描"
    fi
}

# 质量门禁
quality_gate() {
    local skill_name=$1
    log "执行质量门禁：$skill_name"
    
    if [ -f "$SKILLS_DIR/smart-skills-manager/modules/creator/quality-gate.py" ]; then
        python3 "$SKILLS_DIR/smart-skills-manager/modules/creator/quality-gate.py" "$SKILLS_DIR/$skill_name"
        
        if [ $? -ne 0 ]; then
            log "🔴 质量门禁失败"
            echo "🔴 质量门禁未通过，安装中止"
            exit 1
        fi
    else
        log "⚠️ 质量门禁模块不可用，跳过检查"
    fi
}

# 主流程
main() {
    local source=$1
    local target=$2
    
    if [ -z "$source" ] || [ -z "$target" ]; then
        echo "用法：$0 <source> <skill-name-or-url>"
        echo ""
        echo "source 选项:"
        echo "  clawhub   - 从 ClawHub 技能市场安装"
        echo "  github    - 从 GitHub 仓库安装"
        echo "  local     - 从本地路径安装"
        echo ""
        echo "示例:"
        echo "  $0 clawhub weather-plus"
        echo "  $0 github https://github.com/user/openclaw-skill-x"
        echo "  $0 local /path/to/skill"
        exit 1
    fi
    
    log "========== 技能安装开始 =========="
    log "来源：$source, 目标：$target"
    
    case $source in
        clawhub)
            install_from_clawhub "$target"
            ;;
        github)
            install_from_github "$target"
            ;;
        local)
            install_from_local "$target"
            ;;
        *)
            echo "🔴 未知来源：$source"
            exit 1
            ;;
    esac
    
    # 安装后检查
    skill_name=$(basename "$target" .git)
    
    log "执行安装后检查..."
    security_scan "$skill_name"
    quality_gate "$skill_name"
    
    log "========== 技能安装完成 =========="
    echo ""
    echo "✅ 技能 '$skill_name' 安装并验证完成!"
    echo ""
    echo "下一步:"
    echo "1. 查看使用说明：cat $SKILLS_DIR/$skill_name/SKILL.md"
    echo "2. 配置必要参数 (如有)"
    echo "3. 测试运行"
}

main "$@"
