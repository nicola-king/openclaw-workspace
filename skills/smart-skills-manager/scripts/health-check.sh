#!/bin/bash
# 技能健康检查脚本
# 用法：./health-check.sh <skill-name> [--all] [--report]

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE/skills"
LOG_FILE="$WORKSPACE/logs/skill-health.log"
REPORT_FILE="$WORKSPACE/reports/skill-health-$(date +%Y%m%d-%H%M).md"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查技能健康度
check_skill_health() {
    local skill_name=$1
    local skill_path="$SKILLS_DIR/$skill_name"
    local status="✅"
    local issues=()
    
    if [ ! -d "$skill_path" ]; then
        echo "🔴 技能不存在：$skill_name"
        return 1
    fi
    
    # 1. 检查 SKILL.md
    if [ ! -f "$skill_path/SKILL.md" ]; then
        issues+=("缺少 SKILL.md")
        status="🔴"
    fi
    
    # 2. 检查 Python 语法
    for py_file in "$skill_path"/*.py "$skill_path"/**/*.py; do
        if [ -f "$py_file" ]; then
            if ! python3 -m py_compile "$py_file" 2>/dev/null; then
                issues+=("Python 语法错误：$(basename $py_file)")
                status="🔴"
            fi
        fi
    done
    
    # 3. 检查依赖
    if [ -f "$skill_path/requirements.txt" ]; then
        # 简单检查：是否有 requirements.txt
        :
    fi
    
    # 4. 检查执行权限
    for sh_file in "$skill_path"/*.sh "$skill_path"/**/*.sh; do
        if [ -f "$sh_file" ] && [ ! -x "$sh_file" ]; then
            issues+=("缺少执行权限：$(basename $sh_file)")
            if [ "$status" = "✅" ]; then
                status="🟡"
            fi
        fi
    done
    
    # 5. 检查日志文件
    # (可选)
    
    # 输出结果
    if [ ${#issues[@]} -eq 0 ]; then
        echo "$status $skill_name - 健康"
    else
        echo "$status $skill_name - ${#issues[@]} 个问题"
        for issue in "${issues[@]}"; do
            echo "    - $issue"
        done
    fi
    
    return 0
}

# 检查所有技能
check_all() {
    log "========== 开始健康检查 =========="
    echo "## 技能健康检查报告\n"
    echo "**时间**: $(date '+%Y-%m-%d %H:%M')\n"
    
    local total=0
    local healthy=0
    local warning=0
    local critical=0
    
    # 跳过假目录
    SKIP_DIRS=("__pycache__" "templates" "scenarios")
    
    echo "| 技能 | 状态 | 问题 |"
    echo "|------|------|------|"
    
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            
            # 跳过假目录
            skip=false
            for skip_dir in "${SKIP_DIRS[@]}"; do
                if [ "$skill_name" = "$skip_dir" ]; then
                    skip=true
                    break
                fi
            done
            
            if [ "$skip" = true ]; then
                continue
            fi
            
            total=$((total + 1))
            
            # 跳过 smart-skills-manager 自身
            if [ "$skill_name" = "smart-skills-manager" ]; then
                continue
            fi
            
            # 检查并统计
            result=$(check_skill_health "$skill_name" 2>&1)
            if [[ "$result" == *"✅"* ]]; then
                healthy=$((healthy + 1))
                echo "| $skill_name | ✅ | 无 |"
            elif [[ "$result" == *"🟡"* ]]; then
                warning=$((warning + 1))
                issue_count=$(echo "$result" | grep -oP '\d+(?= 个问题)')
                echo "| $skill_name | 🟡 | ${issue_count:-1} |"
            else
                critical=$((critical + 1))
                issue_count=$(echo "$result" | grep -oP '\d+(?= 个问题)')
                echo "| $skill_name | 🔴 | ${issue_count:-1} |"
            fi
        fi
    done
    
    echo ""
    echo "### 统计"
    echo "| 指标 | 数值 |"
    echo "|------|------|"
    echo "| 总技能数 | $total |"
    echo "| 健康 | $healthy |"
    echo "| 警告 | $warning |"
    echo "| 严重 | $critical |"
    echo "| 健康率 | $(echo "scale=1; $healthy * 100 / $total" | bc)% |"
    
    log "========== 检查完成 =========="
}

# 生成详细报告
generate_report() {
    local report_file=$1
    
    echo "生成详细报告：$report_file"
    
    {
        echo "# 技能健康检查报告"
        echo ""
        echo "**生成时间**: $(date '+%Y-%m-%d %H:%M')"
        echo "**检查范围**: 所有技能"
        echo ""
        check_all
        echo ""
        echo "### 建议操作"
        echo ""
        echo "1. 修复🔴严重问题"
        echo "2. 关注🟡警告项"
        echo "3. 定期执行健康检查"
        echo ""
        echo "---"
        echo "*报告生成：smart-skills-manager health-check*"
    } > "$report_file"
    
    echo "✅ 报告已保存：$report_file"
}

# 主流程
main() {
    if [ "$1" = "--all" ] || [ "$1" = "--report" ]; then
        if [ "$1" = "--report" ]; then
            check_all | tee "$REPORT_FILE"
            echo ""
            echo "📄 报告已保存：$REPORT_FILE"
        else
            check_all
        fi
    elif [ -z "$1" ]; then
        echo "用法：$0 <skill-name> | --all | --report"
        echo ""
        echo "选项:"
        echo "  <skill-name>  检查指定技能"
        echo "  --all         检查所有技能"
        echo "  --report      检查并生成报告"
        echo ""
        echo "示例:"
        echo "  $0 weather-plus"
        echo "  $0 --all"
        echo "  $0 --report"
        exit 1
    else
        check_skill_health "$1"
    fi
}

main "$@"
