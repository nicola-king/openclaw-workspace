#!/bin/bash
# 太一 9 大 Agent GitHub 部署脚本
# 使用 Token 认证

set -e

SKILLS_DIR="/home/nicola/.openclaw/workspace/skills"

echo "🚀 太一 9 大 Agent GitHub 部署"
echo "=============================="
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

# 遍历创建和推送
for dir in "${!AGENTS[@]}"; do
    repo="${AGENTS[$dir]}"
    
    echo "📦 部署：$repo"
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
    
    # 使用 Token 创建仓库 (通过 GitHub CLI)
    echo "🔧 创建/更新仓库..."
    
    if gh repo create "nicola-king/$repo" --public --source=. --push 2>&1; then
        echo "✅ 创建并推送成功！"
        ((SUCCESS_COUNT++))
        echo "🔗 https://github.com/nicola-king/$repo"
    else
        # 可能已存在，尝试直接推送
        echo "⚠️  仓库可能已存在，尝试推送..."
        
        git remote remove origin 2>/dev/null || true
        git remote set-url origin "https://$GITHUB_TOKEN@github.com/nicola-king/$repo.git" 2>/dev/null || \
        git remote add origin "https://$GITHUB_TOKEN@github.com/nicola-king/$repo.git"
        
        if git push -u origin main 2>&1; then
            echo "✅ 推送成功！"
            ((SUCCESS_COUNT++))
            echo "🔗 https://github.com/nicola-king/$repo"
        else
            echo "❌ 推送失败"
            ((FAIL_COUNT++))
        fi
    fi
    
    echo ""
done

echo "=============================="
echo "✅ 部署完成！"
echo ""
echo "📊 结果统计:"
echo "✅ 成功：$SUCCESS_COUNT 个"
echo "❌ 失败：$FAIL_COUNT 个"
echo ""
echo "🎉 查看仓库:"
echo "https://github.com/nicola-king?tab=repositories"
