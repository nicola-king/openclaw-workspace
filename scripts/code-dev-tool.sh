#!/bin/bash
# OpenClaw 代码开发工具包装器
# 智能路由：太一模型路由 > Claw Code > OpenCode

set -e

# 工具路径
TAIYI_ROUTER="/home/nicola/.openclaw/workspace/skills/07-system/smart-model-router/router.py"
CLAW_CODE="/opt/claw-code/rust/target/debug/claw"
OPENCODE="$HOME/.bun/bin/opencoder"

# 检测工具
detect_tool() {
    # 优先使用太一智能路由系统
    if [ -f "$TAIYI_ROUTER" ]; then
        echo "taiyi_router"
        return 0
    elif [ -f "$CLAW_CODE" ]; then
        echo "claw_code"
        return 0
    elif [ -f "$OPENCODE" ]; then
        echo "opencoder"
        return 0
    else
        echo "none"
        return 1
    fi
}

# 执行代码任务
run_code_task() {
    local tool="$1"
    local task="$2"
    
    case "$tool" in
        taiyi_router)
            echo "🧠 使用太一智能路由系统执行任务..."
            echo "=================================="
            echo ""
            echo "任务：$task"
            echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
            echo ""
            echo "正在调度最优模型..."
            echo ""
            # 调用太一智能路由 (使用 OpenClaw 原生方式)
            python3 "$TAIYI_ROUTER" \
                --task "code" \
                --prompt "$task"
            ;;
        claw_code)
            echo "🦀 使用 Claw Code 执行任务..."
            echo "=================================="
            "$CLAW_CODE" prompt "$task"
            ;;
        opencoder)
            echo "🤖 使用 OpenCode 执行任务..."
            echo "=================================="
            "$OPENCODE" "$task"
            ;;
        *)
            echo "❌ 未找到可用的代码开发工具"
            echo "请确保太一智能路由系统已配置"
            exit 1
            ;;
    esac
}

# 显示帮助
show_help() {
    cat << EOF
🛠️ OpenClaw 代码开发工具

用法:
  $0 <代码任务>

工具优先级:
  1. 太一智能路由系统 (默认优先) ✅
  2. Claw Code (本地安装备用)
  3. OpenCode (备用)

示例:
  $0 "创建一个 Python FastAPI 项目"
  $0 "审查 src/main.py 的代码"
  $0 "修复这个文件的错误"
  $0 "优化这个文件的性能"

EOF
}

# 主函数
main() {
    local tool=$(detect_tool)
    
    if [ "$tool" = "none" ]; then
        echo "❌ 未找到可用的代码开发工具"
        echo ""
        echo "请确保以下工具之一已配置:"
        echo ""
        echo "  1. 太一智能路由系统 (推荐):"
        echo "     已集成到 OpenClaw"
        echo "     自动调度最优模型"
        echo ""
        echo "  2. Claw Code:"
        echo "     git clone https://github.com/ultraworkers/claw-code"
        echo "     cd claw-code/rust && cargo build --workspace"
        echo ""
        echo "  3. OpenCode:"
        echo "     curl -fsSL https://bun.sh/install | bash"
        echo "     ~/.bun/bin/bun install --global opencoder"
        exit 1
    fi
    
    echo "✅ 检测到代码开发工具：$tool"
    echo ""
    
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    run_code_task "$tool" "$*"
}

main "$@"
