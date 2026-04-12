#!/bin/bash
# 太一 9 大 Agent GitHub 仓库批量创建脚本
# 使用 GitHub API 创建公开仓库

set -e

echo "🎯 太一 9 大 Agent GitHub 仓库创建"
echo "=================================="
echo ""

# Agent 列表
AGENTS=(
    "polymarket-trading-agent:Polymarket Trading Agent - 太一预测市场交易 Agent"
    "gmgn-trading-agent:GMGN Trading Agent - 太一链上交易 Agent"
    "binance-trading-agent:Binance Trading Agent - 太一币安交易 Agent"
    "cross-border-trade-agent:Cross-Border Trade Agent - 太一跨境贸易 Agent"
    "taiyi-voice-agent:Taiyi Voice Agent - 太一全双工语音 Agent"
    "taiyi-memory-system-v3:Taiyi Memory System v3 - 太一记忆系统 (Mem0 融合)"
    "taiyi-education-agent:Taiyi Education Agent - 太一教育 Agent"
    "taiyi-office-agent:Taiyi Office Agent - 太一办公 Agent"
    "taiyi-diagram-agent:Taiyi Diagram Agent - 太一图表 Agent"
)

# 遍历创建
for agent in "${AGENTS[@]}"; do
    IFS=':' read -r repo desc <<< "$agent"
    
    echo "📦 创建：$repo"
    echo "   描述：$desc"
    
    # GitHub API 创建仓库
    curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d "{
            \"name\": \"$repo\",
            \"description\": \"$desc\",
            \"private\": false,
            \"auto_init\": false
        }" > /tmp/repo_$repo.json
    
    if [ $? -eq 0 ]; then
        echo "✅ 创建成功"
    else
        echo "⚠️  可能已存在或失败"
    fi
    
    echo ""
done

echo "✅ 仓库创建完成！"
echo ""
echo "📊 下一步:"
echo "运行发布脚本推送代码:"
echo "bash scripts/publish-all-agents.sh"
