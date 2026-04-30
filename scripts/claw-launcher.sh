#!/bin/bash
# Claw Code 交互式启动包装器
# 支持直接交流对话

# 进入工作目录
cd /home/nicola/.openclaw/workspace

# 检查 API 密钥
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$ANTHROPIC_AUTH_TOKEN" ]; then
    echo "⚠️  未检测到 API 密钥"
    echo ""
    echo "请先配置 API 密钥:"
    echo "  export ANTHROPIC_API_KEY=\"sk-ant-你的密钥\""
    echo ""
    echo "获取密钥：https://console.anthropic.com/"
    echo ""
    echo "按回车继续，或 Ctrl+C 退出..."
    read -r
fi

# 启动 Claw Code 交互式模式
echo "🦀 启动 Claw Code 交互式对话..."
echo "=================================="
echo ""
echo "提示:"
echo "  - 直接输入问题或任务"
echo "  - 使用 /help 查看可用命令"
echo "  - 使用 /quit 或 Ctrl+D 退出"
echo ""
/opt/claw-code/rust/target/debug/claw "$@"
