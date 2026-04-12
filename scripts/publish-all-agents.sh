#!/bin/bash
# 太一 9 大 Agent 一键发布脚本
# 使用方法：bash scripts/publish-all-agents.sh

set -e

SKILLS_DIR="/home/nicola/.openclaw/workspace/skills"

echo "🎯 太一 9 大 Agent GitHub 发布脚本"
echo "=================================="
echo ""

# Agent 列表
declare -A AGENTS=(
    ["polymarket-trading-agent"]="polymarket-trading-agent"
    ["gmgn-trading-agent"]="gmgn-trading-agent"
    ["binance-trading-agent"]="binance-trading-agent"
    ["cross-border-trade-agent"]="cross-border-trade-agent"
    ["taiyi-voice-agent"]="taiyi-voice-agent"
    ["taiyi-memory-v3"]="taiyi-memory-system-v3"
    ["taiyi-education-agent"]="taiyi-education-agent"
    ["taiyi-office-agent"]="taiyi-office-agent"
    ["taiyi-diagram-agent"]="taiyi-diagram-agent"
)

# 遍历发布
for dir in "${!AGENTS[@]}"; do
    repo="${AGENTS[$dir]}"
    
    echo "📦 发布：$repo"
    echo "----------------------------"
    
    AGENT_PATH="$SKILLS_DIR/$dir"
    
    if [ ! -d "$AGENT_PATH" ]; then
        echo "⚠️  跳过：目录不存在 - $AGENT_PATH"
        continue
    fi
    
    cd "$AGENT_PATH"
    
    # 添加或更新远程仓库
    git remote remove origin 2>/dev/null || true
    git remote add origin git@github.com:nicola-king/$repo.git
    
    # 推送
    echo "🚀 推送到 GitHub: nicola-king/$repo"
    git push -u origin main 2>&1 && echo "✅ 成功" || echo "⚠️  需要先创建仓库"
    
    echo ""
done

echo "✅ 发布脚本执行完成！"
echo ""
echo "📊 下一步:"
echo "1. 在 GitHub 创建对应仓库（如推送失败）"
echo "2. 访问 https://github.com/new 创建仓库"
echo "3. 仓库名与上述列表一致"
echo "4. 再次运行此脚本完成推送"
