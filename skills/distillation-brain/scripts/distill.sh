#!/bin/bash
# 蒸馏大脑 — 六层蒸馏提炼流水线
# 用法: bash distill.sh <mode> <content>

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
    echo "用法:"
    echo "  bash distill.sh full <content>      — 完整六层蒸馏"
    echo "  bash distill.sh understand <content> — 理解层"
    echo "  bash distill.sh relate <content>     — 关联层"
    echo "  bash distill.sh review <content>     — 点评层"
    echo "  bash distill.sh question <content>   — 拷问层"
    echo "  bash distill.sh polish <content>     — 打磨层"
    echo "  bash distill.sh output <content> <platform> — 产出层"
    echo ""
    echo "平台: xiaohongshu / wechat / moment / report"
    exit 1
}

[ $# -lt 2 ] && usage

MODE="$1"
shift
CONTENT="$*"

case "$MODE" in
    full)
        echo "=== 🧠 蒸馏大脑 完整流程 ==="
        echo ""
        echo "--- [第1层] 理解 ---"
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请提取以下内容的核心要点，输出结构化摘要（3-5个要点），并给出关键词标签。\n\n内容：$CONTENT" 2>/dev/null
        echo ""
        echo "--- [第2层] 关联 ---"
        echo "(关联历史记忆需要太一上下文，暂用 AI 分析)"
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "基于以下素材，分析它的背景、潜在关联领域、已知相关知识领域。如果这是商业/外贸相关内容，输出行业分析视角。\n\n素材：$CONTENT" 2>/dev/null
        echo ""
        echo "--- [第3层] 点评 ---"
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请客观点评以下内容：找到其中的闪光点、独特价值、值得深入的方向。\n\n内容：$CONTENT" 2>/dev/null
        echo ""
        echo "--- [第4层] 拷问 ---"
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请严格拷问以下内容：指出其中的漏洞、盲点、未考虑的角度、需要补充的信息、可能的反方观点。\n\n内容：$CONTENT" 2>/dev/null
        echo ""
        echo "--- [第5层] 打磨 ---"
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请将以下原始素材打磨成一篇通顺、有观点、有价值的内容。保留核心思想，优化表达和逻辑。\n\n原始素材：$CONTENT" 2>/dev/null
        echo ""
        echo "--- [第6层] 成果 ---"
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请将以下内容分别适配为：1) 小红书风格 2) 公众号风格 3) 朋友圈风格。\n\n内容：$CONTENT" 2>/dev/null
        echo ""
        echo "=== ✅ 蒸馏完成 ==="
        ;;

    understand)
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请提取以下内容的核心要点，输出结构化摘要和关键词标签。\n\n$CONTENT" 2>/dev/null
        ;;

    review)
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请客观点评以下内容：找到闪光点、独特价值、值得深入的方向。\n\n$CONTENT" 2>/dev/null
        ;;

    question)
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请严格拷问以下内容：指出漏洞、盲点、未考虑的角度、反方观点。\n\n$CONTENT" 2>/dev/null
        ;;

    polish)
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请将以下内容打磨成通顺、有观点、有价值的内容。保留核心思想，优化表达和逻辑。\n\n$CONTENT" 2>/dev/null
        ;;

    output)
        PLATFORM="${3:-xiaohongshu}"
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请将以下内容适配为${PLATFORM}风格的内容输出。\n\n$CONTENT" 2>/dev/null
        ;;

    relate)
        bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "请分析以下素材的潜在关联领域、已知相关知识、背景信息。\n\n$CONTENT" 2>/dev/null
        ;;

    *)
        usage
        ;;
esac