#!/bin/bash
# 太一 9 大 Agent GitHub SSH 部署脚本
# 使用 SSH 认证，无需 GitHub CLI

set -e

SKILLS_DIR="/home/nicola/.openclaw/workspace/skills"

echo "🚀 太一 9 大 Agent GitHub SSH 部署"
echo "=================================="
echo ""
echo "✅ 使用 SSH 认证 (nicola-king)"
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

SUCCESS_COUNT=0
FAIL_COUNT=0

# 遍历推送
for dir in "${!AGENTS[@]}"; do
    repo="${AGENTS[$dir]}"
    
    echo "📦 推送：$repo"
    echo "----------------------------"
    
    AGENT_PATH="$SKILLS_DIR/$dir"
    
    if [ ! -d "$AGENT_PATH" ]; then
        echo "⚠️  跳过：目录不存在"
        ((FAIL_COUNT++))
        continue
    fi
    
    cd "$AGENT_PATH"
    
    # 确保是 main 分支
    git branch -M main 2>/dev/null || true
    
    # 设置远程仓库
    git remote remove origin 2>/dev/null || true
    git remote add origin git@github.com:nicola-king/$repo.git
    
    # 推送
    echo "🚀 推送到 GitHub: nicola-king/$repo"
    
    if git push -u origin main 2>&1; then
        echo "✅ 推送成功！"
        ((SUCCESS_COUNT++))
        echo "🔗 https://github.com/nicola-king/$repo"
    else
        echo "⚠️  推送失败"
        echo "   可能原因：仓库不存在，请先在 GitHub 创建仓库"
        echo "   创建链接：https://github.com/new?name=$repo"
        ((FAIL_COUNT++))
    fi
    
    echo ""
done

echo "===================================="
echo "✅ 部署完成！"
echo ""
echo "📊 结果统计:"
echo "✅ 成功：$SUCCESS_COUNT 个"
echo "⚠️  失败：$FAIL_COUNT 个"
echo ""
echo "📝 失败处理:"
echo "1. 访问 https://github.com/new"
echo "2. 创建对应名称的仓库 (Public)"
echo "3. 重新运行此脚本"
echo ""
echo "🎉 查看仓库:"
echo "https://github.com/nicola-king?tab=repositories"
