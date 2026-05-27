#!/bin/bash
# Drawnix 渲染包装脚本
# 将 markdown 文本渲染为思维导图
# 依赖: curl, Drawnix 服务（本地或在线）

DRAWNIX_URL="${DRAWNIX_URL:-https://drawnix.com}"
OUTPUT_DIR="/home/sayelf/.openclaw/workspace/exports"

usage() {
    echo "用法:"
    echo "  bash drawnix.sh mindmap <markdown_file> [output_name]"
    echo "  bash drawnix.sh mermaid <mermaid_file> [output_name]"
    echo ""
    echo "示例:"
    echo "  bash drawnix.sh mindmap analysis.md market-analysis"
    exit 1
}

[ $# -lt 2 ] && usage

MODE="$1"
INPUT_FILE="$2"
OUTPUT_NAME="${3:-drawnix-output}"

if [ ! -f "$INPUT_FILE" ]; then
    echo "[DRAWNIX-ERROR] ❌ 文件不存在: $INPUT_FILE" >&2
    exit 1
fi

echo "[DRAWNIX] 📋 模式: $MODE"
echo "[DRAWNIX] 📂 输入: $INPUT_FILE"
echo "[DRAWNIX] 🎯 输出: $OUTPUT_NAME"
echo "[DRAWNIX] 🔗 服务: $DRAWNIX_URL"

case "$MODE" in
    mindmap)
        # 将 markdown 转换为 Drawnix 兼容的思维导图格式
        # Drawnix 原生支持 markdown → mindmap
        echo "[DRAWNIX] ✅ markdown → 思维导图"
        echo "[DRAWNIX] 💡 请打开 $DRAWNIX_URL 并将以下内容粘贴到白板:"
        echo ""
        cat "$INPUT_FILE"
        echo ""
        echo "[DRAWNIX] 💡 在 Drawnix 中点击 '文本转思维导图' 即可渲染"
        ;;
    mermaid)
        echo "[DRAWNIX] ✅ mermaid → 流程图"
        echo "[DRAWNIX] 💡 请打开 $DRAWNIX_URL 并将以下 mermaid 代码渲染:"
        echo ""
        cat "$INPUT_FILE"
        echo ""
        echo "[DRAWNIX] 💡 Drawnix 支持 mermaid 语法，直接粘贴即可"
        ;;
    *)
        usage
        ;;
esac

# 保存输出引用
echo "[DRAWNIX-OK] ✅ 渲染指令已生成" >&2
