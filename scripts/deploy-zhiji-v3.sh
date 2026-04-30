#!/bin/bash
# 知几-E v3.0 实盘部署脚本

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🚀 知几-E v3.0 实盘部署                                   ║"
echo "╚══════════════════════════════════════════════════════════╝"

# 1. 检查依赖
echo "📦 检查依赖..."
python3 -c "import transformers; print('  ✅ transformers')" 2>/dev/null || echo "  ❌ transformers 缺失"
python3 -c "import torch; print('  ✅ torch')" 2>/dev/null || echo "  ❌ torch 缺失"

# 2. 检查配置
echo "🔧 检查配置..."
if [ -f "/home/nicola/.openclaw/workspace/config/binance-config.json" ]; then
    echo "  ✅ 币安配置存在"
else
    echo "  ❌ 币安配置缺失"
    exit 1
fi

# 3. 检查数据库
echo "🗄️ 检查数据库..."
sqlite3 /home/nicola/.openclaw/workspace/polymarket-data/polymarket.db ".tables" | grep daily_news > /dev/null && echo "  ✅ daily_news 表存在" || echo "  ❌ daily_news 表缺失"

# 4. 启动监控
echo "📊 启动策略监控..."
nohup python3 /home/nicola/.openclaw/workspace/scripts/zhiji-e-v3-sentiment.py > /tmp/zhiji-v3-live.log 2>&1 &
echo "  ✅ 进程启动 (PID: $!)"

echo ""
echo "✅ 部署完成"
