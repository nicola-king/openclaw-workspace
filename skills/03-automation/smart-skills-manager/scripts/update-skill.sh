#!/bin/bash
# 技能更新脚本
# 用法：./update-skill.sh <skill-name> [--all]

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE/skills"
LOG_FILE="$WORKSPACE/logs/skill-update.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 更新单个技能
update_skill() {
    local skill_name=$1
    local skill_path="$SKILLS_DIR/$skill_name"
    
    if [ ! -d "$skill_path" ]; then
        log "🔴 技能不存在：$skill_name"
        echo "🔴 错误：技能 '$skill_name' 不存在"
        return 1
    fi
    
    log "更新技能：$skill_name"
    echo "🔄 更新技能：$skill_name"
    
    # 检查是否是 Git 仓库
    if [ -d "$skill_path/.git" ]; then
        cd "$skill_path"
        
        # 拉取最新代码
        git fetch origin
        LOCAL=$(git rev-parse HEAD)
        REMOTE=$(git rev-parse @{u})
        
        if [ "$LOCAL" != "$REMOTE" ]; then
            echo "  发现更新，拉取中..."
            git pull origin $(git rev-parse --abbrev-ref HEAD)
            
            # 安装新依赖
            if [ -f "requirements.txt" ]; then
                echo "  安装 Python 依赖..."
                pip install -r requirements.txt -q
            fi
            
            # 重新设置权限
            find . -name "*.sh" -exec chmod +x {} \;
            
            log "✅ 更新成功：$skill_name"
            echo "  ✅ 更新完成"
        else
            echo "  ✅ 已是最新版本"
            log "已是最新版本：$skill_name"
        fi
    else
        echo "  ⚠️ 非 Git 仓库，跳过更新"
        log "非 Git 仓库，跳过：$skill_name"
    fi
    
    return 0
}

# 更新所有技能
update_all() {
    log "========== 开始更新所有技能 =========="
    echo "🔄 开始更新所有技能...\n"
    
    local count=0
    local updated=0
    local failed=0
    
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            count=$((count + 1))
            
            echo "[$count] $skill_name"
            if update_skill "$skill_name"; then
                updated=$((updated + 1))
            else
                failed=$((failed + 1))
            fi
            echo ""
        fi
    done
    
    log "========== 更新完成 =========="
    echo "==============================="
    echo "✅ 更新完成"
    echo "  总计：$count 个技能"
    echo "  成功：$updated 个"
    echo "  失败：$failed 个"
    echo "==============================="
}

# 更新后验证
verify_update() {
    local skill_name=$1
    local skill_path="$SKILLS_DIR/$skill_name"
    
    echo "🔍 验证更新..."
    
    # 检查 SKILL.md
    if [ ! -f "$skill_path/SKILL.md" ]; then
        echo "  🔴 SKILL.md 丢失"
        return 1
    fi
    
    # 质量门禁
    if [ -f "$SKILLS_DIR/smart-skills-manager/modules/creator/quality-gate.py" ]; then
        echo "  执行质量门禁..."
        python3 "$SKILLS_DIR/smart-skills-manager/modules/creator/quality-gate.py" "$skill_path"
        
        if [ $? -ne 0 ]; then
            echo "  🔴 质量门禁失败"
            return 1
        fi
    fi
    
    echo "  ✅ 验证通过"
    return 0
}

# 主流程
main() {
    if [ "$1" = "--all" ]; then
        update_all
    elif [ -z "$1" ]; then
        echo "用法：$0 <skill-name> | --all"
        echo ""
        echo "选项:"
        echo "  <skill-name>  更新指定技能"
        echo "  --all         更新所有技能"
        echo ""
        echo "示例:"
        echo "  $0 weather-plus"
        echo "  $0 --all"
        exit 1
    else
        update_skill "$1"
        if [ $? -eq 0 ]; then
            verify_update "$1"
        fi
    fi
}

main "$@"
