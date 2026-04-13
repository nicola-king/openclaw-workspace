#!/bin/bash
# Hermes Learning Loop - 启动脚本
# 用法：./run.sh [command]
#
# 命令:
#   run     - 执行学习循环 (默认)
#   track   - 仅任务追踪
#   status  - 查看状态
#   clean   - 清理缓存

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOOP_DIR="$SCRIPT_DIR/loop"
cd "$LOOP_DIR"

case "${1:-run}" in
    run|learn)
        echo "🧠 启动 Hermes 学习循环..."
        python3 learning_orchestrator.py
        ;;
    track)
        echo "📋 运行任务追踪器..."
        python3 task_tracker.py
        ;;
    status)
        echo "📊 学习循环状态"
        if [ -f "$SCRIPT_DIR/learning_state.json" ]; then
            cat "$SCRIPT_DIR/learning_state.json" | python3 -m json.tool | head -30
        else
            echo "  无状态文件"
        fi
        ;;
    clean)
        echo "🧹 清理缓存..."
        rm -rf "$LOOP_DIR/__pycache__"
        rm -f "$SCRIPT_DIR/pending_skills.json"
        echo "  ✅ 清理完成"
        ;;
    *)
        echo "用法：$0 [run|track|status|clean]"
        echo ""
        echo "命令:"
        echo "  run     - 执行完整学习循环"
        echo "  track   - 仅任务追踪"
        echo "  status  - 查看学习状态"
        echo "  clean   - 清理缓存文件"
        exit 1
        ;;
esac
