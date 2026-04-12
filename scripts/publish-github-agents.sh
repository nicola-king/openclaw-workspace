#!/bin/bash
# 太一 Agent GitHub 发布脚本
# 发布 9 大 Agent 到 GitHub

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE/skills"

echo "🎯 太一 Agent GitHub 发布脚本"
echo "=============================="
echo ""

# Agent 列表
AGENTS=(
    "polymarket-trading-agent:polymarket-trading-agent"
    "gmgn-trading-agent:gmgn-trading-agent"
    "binance-trading-agent:binance-trading-agent"
    "cross-border-trade-agent:cross-border-trade-agent"
    "taiyi-voice-agent:taiyi-voice-agent"
    "taiyi-memory-v3:taiyi-memory-system-v3"
    "taiyi-education-agent:taiyi-education-agent"
    "taiyi-office-agent:taiyi-office-agent"
    "taiyi-diagram-agent:taiyi-diagram-agent"
)

# 遍历发布
for agent_pair in "${AGENTS[@]}"; do
    IFS=':' read -r dir repo <<< "$agent_pair"
    
    echo "📦 发布：$repo"
    echo "----------------------------"
    
    AGENT_PATH="$SKILLS_DIR/$dir"
    
    if [ ! -d "$AGENT_PATH" ]; then
        echo "⚠️  跳过：目录不存在 - $AGENT_PATH"
        continue
    fi
    
    cd "$AGENT_PATH"
    
    # 初始化 Git (如果未初始化)
    if [ ! -d ".git" ]; then
        git init
    fi
    
    # 添加所有文件
    git add -A
    
    # 提交
    git commit -m "🎯 $repo - 太一 Agent v1.0
    
功能:
✅ 核心功能实现
✅ 自进化学习
✅ 文档完善

太一 AGI · $(date +%Y-%m-%d)" || true
    
    # 设置主分支
    git branch -M main
    
    # 添加远程仓库 (如果未添加)
    if ! git remote get-url origin &>/dev/null; then
        git remote add origin git@github.com:nicola-king/$repo.git
    fi
    
    # 推送
    echo "🚀 推送到 GitHub: nicola-king/$repo"
    git push -u origin main || echo "⚠️  推送失败 (可能仓库不存在)"
    
    echo ""
done

echo "✅ 发布完成！"
echo ""
echo "📊 下一步:"
echo "1. 在 GitHub 创建对应仓库"
echo "2. 配置 README 和许可证"
echo "3. 添加 PyPI 发布配置"
