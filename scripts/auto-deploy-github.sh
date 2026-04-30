#!/bin/bash
# 太一 9 大 Agent GitHub 自动化部署脚本
# 结合方式 2 (GitHub CLI) + 方式 3 (GitHub API)

set -e

SKILLS_DIR="/home/nicola/.openclaw/workspace/skills"

echo "🚀 太一 9 大 Agent GitHub 自动化部署"
echo "===================================="
echo ""

# Agent 列表
declare -A AGENTS=(
    ["polymarket-trading-agent"]="Polymarket Trading Agent - 太一预测市场交易 Agent"
    ["gmgn-trading-agent"]="GMGN Trading Agent - 太一链上交易 Agent"
    ["binance-trading-agent"]="Binance Trading Agent - 太一币安交易 Agent"
    ["cross-border-trade-agent"]="Cross-Border Trade Agent - 太一跨境贸易 Agent"
    ["taiyi-voice-agent"]="Taiyi Voice Agent - 太一全双工语音 Agent"
    ["taiyi-memory-v3"]="Taiyi Memory System v3 - 太一记忆系统 (Mem0 融合)"
    ["taiyi-education-agent"]="Taiyi Education Agent - 太一教育 Agent"
    ["taiyi-office-agent"]="Taiyi Office Agent - 太一办公 Agent"
    ["taiyi-diagram-agent"]="Taiyi Diagram Agent - 太一图表 Agent"
)

# 检查 GitHub CLI 认证
echo "📋 检查 GitHub CLI 认证状态..."
if ! gh auth status &>/dev/null; then
    echo "⚠️  GitHub CLI 未认证"
    echo ""
    echo "请选择认证方式:"
    echo "1. 手动认证：gh auth login"
    echo "2. 使用 Token: export GITHUB_TOKEN='your_token'"
    echo ""
    
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "✅ 检测到 GITHUB_TOKEN，使用 API 方式创建仓库"
        USE_API=true
    else
        echo "❌ 未检测到认证信息，退出"
        exit 1
    fi
else
    echo "✅ GitHub CLI 已认证"
    USE_API=false
fi

echo ""
echo "📦 开始创建并推送 9 大 Agent..."
echo ""

# 遍历创建和推送
for dir in "${!AGENTS[@]}"; do
    desc="${AGENTS[$dir]}"
    repo=$dir
    
    # 特殊处理：taiyi-memory-v3 → taiyi-memory-system-v3
    if [ "$dir" = "taiyi-memory-v3" ]; then
        repo="taiyi-memory-system-v3"
    fi
    
    echo "🔵 [$dir] → $repo"
    echo "   描述：$desc"
    
    AGENT_PATH="$SKILLS_DIR/$dir"
    
    if [ ! -d "$AGENT_PATH" ]; then
        echo "⚠️  跳过：目录不存在"
        continue
    fi
    
    cd "$AGENT_PATH"
    
    # 确保是 main 分支
    git branch -M main 2>/dev/null || true
    
    # 方式 A: 使用 GitHub CLI
    if [ "$USE_API" = false ]; then
        echo "   使用 GitHub CLI 创建..."
        
        # 尝试创建仓库
        if gh repo create "nicola-king/$repo" --public --source=. --push &>/dev/null; then
            echo "   ✅ 创建并推送成功"
        else
            # 可能已存在，尝试直接推送
            git remote remove origin 2>/dev/null || true
            git remote add origin git@github.com:nicola-king/$repo.git
            
            if git push -u origin main 2>&1 | grep -q "error"; then
                echo "   ⚠️  推送失败，需要手动创建仓库"
            else
                echo "   ✅ 推送成功"
            fi
        fi
    
    # 方式 B: 使用 GitHub API + Git 推送
    else
        echo "   使用 GitHub API 创建..."
        
        # API 创建仓库
        CREATE_RESPONSE=$(curl -s -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/user/repos \
            -d "{
                \"name\": \"$repo\",
                \"description\": \"$desc\",
                \"private\": false,
                \"auto_init\": false
            }")
        
        # 检查创建结果
        if echo "$CREATE_RESPONSE" | grep -q "\"name\":\"$repo\""; then
            echo "   ✅ 仓库创建成功"
        elif echo "$CREATE_RESPONSE" | grep -q "already exists"; then
            echo "   ℹ️  仓库已存在"
        else
            echo "   ⚠️  创建可能失败：$CREATE_RESPONSE"
        fi
        
        # Git 推送
        echo "   推送代码..."
        git remote remove origin 2>/dev/null || true
        git remote add origin git@github.com:nicola-king/$repo.git
        
        if git push -u origin main 2>&1; then
            echo "   ✅ 推送成功"
        else
            echo "   ⚠️  推送失败"
        fi
    fi
    
    echo ""
done

echo "===================================="
echo "✅ 自动化部署完成！"
echo ""
echo "📊 查看仓库:"
echo "https://github.com/nicola-king?tab=repositories"
echo ""
echo "📝 后续操作:"
echo "1. 检查仓库是否创建成功"
echo "2. 添加 LICENSE (MIT)"
echo "3. 完善 README"
echo "4. 添加 Topics 标签"
