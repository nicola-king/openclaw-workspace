#!/bin/bash
# OpenCode OpenClaw 集成技能
# 功能：调用 OpenCode 进行代码生成/审查/优化

set -e

OPENCODE_BIN="$HOME/.bun/bin/opencoder"

# 检查 OpenCode 是否安装
check_opencode() {
    if [ ! -f "$OPENCODE_BIN" ]; then
        echo "❌ OpenCode 未安装"
        echo "请运行：curl -fsSL https://bun.sh/install | bash"
        echo "然后运行：~/.bun/bin/bun install --global opencoder"
        exit 1
    fi
    echo "✅ OpenCode 已安装"
}

# 显示帮助
show_help() {
    cat << EOF
🤖 OpenCode - Claude Code 开源替代品

用法:
  $0 <命令> [参数]

命令:
  code <任务>     执行代码任务 (生成/审查/优化)
  review <文件>   审查代码
  generate <描述> 生成代码
  fix <文件>      修复代码错误
  optimize <文件> 优化代码
  help            显示帮助

示例:
  $0 code "创建一个 Python FastAPI 项目"
  $0 review src/main.py
  $0 generate "用户认证功能，包括登录/注册/JWT"
  $0 fix src/utils.py
  $0 optimize src/database.py

EOF
}

# 执行代码任务
run_code_task() {
    local task="$1"
    echo "🤖 执行代码任务：$task"
    echo "=================================="
    "$OPENCODE_BIN" "$task"
}

# 主函数
main() {
    check_opencode
    
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        code)
            run_code_task "$@"
            ;;
        review)
            run_code_task "审查这个文件：$*"
            ;;
        generate)
            run_code_task "生成代码：$*"
            ;;
        fix)
            run_code_task "修复这个文件的错误：$*"
            ;;
        optimize)
            run_code_task "优化这个文件：$*"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "❌ 未知命令：$command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
