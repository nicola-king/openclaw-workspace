#!/bin/bash

# Claude Code + 百炼 Qwen 集成技能

# 调用方式：bash claw-skill.sh "你的任务描述"


set -e

CLAUDE_BIN="/usr/bin/claude"

# 环境变量注入（openclaw 子进程不继承 ~/.bashrc）

export ANTHROPIC_AUTH_TOKEN="sk-sp-ffbb0fbec7314eb08f9a616e0fda59e7"
export ANTHROPIC_BASE_URL="https://coding.dashscope.aliyuncs.com/apps/anthropic"
export ANTHROPIC_MODEL="qwen3.6-plus"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="qwen3.6-plus"
export ANTHROPIC_DEFAULT_SONNET_MODEL="qwen3.6-plus"
export ANTHROPIC_DEFAULT_OPUS_MODEL="qwen3.6-plus"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

check_claude() {
    if [ ! -f "$CLAUDE_BIN" ]; then
        echo "❌ Claude Code 未找到：$CLAUDE_BIN"
        exit 1
    fi
}

show_help() {
    cat << HELP
Claude Code + 百炼 Qwen 集成技能

用法：
  $0 "<任务描述>"
  $0 --file <文件路径> "<任务>"

示例：
  $0 "分析 ~/projects/art-agent/core.py 的逻辑"
  $0 "帮我写一个 Python 爬虫"
  $0 "审查并修复 main.py 的 bug"
HELP
}

run_task() {
    local task="$1"
    local workdir="${2:-$HOME}"
    
    echo "🤖 Claude Code (Qwen3.6-plus) 执行中..."
    echo "任务：$task"
    echo "=================================="
    
    cd "$workdir"
    "$CLAUDE_BIN" --print "$task"
}

main() {
    check_claude

    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    case "$1" in
        --file)
            local file="$2"
            local task="$3"
            local workdir
            workdir=$(dirname "$file")
            run_task "$task，文件路径：$file" "$workdir"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            run_task "$*"
            ;;
    esac
}

main "$@"
