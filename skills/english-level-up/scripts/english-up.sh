#!/bin/bash
# English Level-Up 包装脚本
# AI 英语学习助手 — 底层调用 Gemini CLI

cd "$(dirname "$0")/.."
SKILL_DIR="$PWD"
CONFIG_DIR="$SKILL_DIR/config"

usage() {
    echo "用法:"
    echo "  bash scripts/english-up.sh write <content>     — 英文写作"
    echo "  bash scripts/english-up.sh polish <content>    — 润色改写"
    echo "  bash scripts/english-up.sh email <content>     — 开发信/邮件"
    echo "  bash scripts/english-up.sh vocab <word>        — 词汇解析"
    echo "  bash scripts/english-up.sh speak <scene>        — 口语场景"
    exit 1
}

[ $# -lt 2 ] && usage

MODE="$1"
shift
CONTENT="$*"

# 加载指南知识库作为 system prompt
AI_GUIDE=$(cat "$CONFIG_DIR/ai-learning-guide.md" 2>/dev/null | head -100)

case "$MODE" in
    write)
        PROMPT="你是一个英语写作教练。请帮助我写一段英文内容：$CONTENT
要求：自然地道、符合英语母语表达习惯。
参考方法论：以引导式学习为主，给出写作思路和修改建议。
请先写初稿，然后标注可以改进的地方。"
        ;;
    polish)
        PROMPT="请帮我润色以下英文内容，使其更自然地道。请给出：
1. 修改后的版本
2. 关键修改点解释
3. 可选的更优表达

原文：$CONTENT"
        ;;
    email)
        PROMPT="你是一个外贸英语专家。请帮我写一封专业的英文商务邮件/开发信。
场景/内容：$CONTENT
要求：专业、地道、有针对性（不模板化）。
请分成：主题行、正文、签名三部分。"
        ;;
    vocab)
        PROMPT="你是一个英语词汇教练。请深度解析这个词：$CONTENT
给出：
1. 词义和用法
2. 搭配和例句
3. 记忆技巧（词根/联想）
4. 外贸场景常用表达"
        ;;
    speak)
        PROMPT="你是一个英语口语教练。请为以下场景提供口语练习提纲：$CONTENT
给出：
1. 关键表达
2. 对话范例
3. 常见错误提示
4. 练习建议"
        ;;
    *)
        usage
        ;;
esac

# 调用 Gemini CLI
bash "$SKILL_DIR/../gemini-cli/scripts/gemini-cli.sh" -p "$PROMPT" 2>/dev/null
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "[ENGLISH-UP] ✅ 完成"
else
    echo "[ENGLISH-UP] ⛔ Gemini CLI 不可用，使用太一内置处理" >&2
fi

exit $EXIT_CODE