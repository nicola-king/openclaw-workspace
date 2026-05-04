#!/bin/bash
# update.sh - 跨境贸易 Agent 更新脚本

set -e

echo "=== 跨境贸易 Agent v9.0.0 更新 ==="

# 备份配置
if [ -f "config.json" ]; then
    echo "备份配置..."
    cp config.json config.json.bak
fi

# 拉取最新代码
echo "拉取最新代码..."
git pull origin main

# 更新依赖
echo "更新依赖..."
source venv/bin/activate
pip install -r requirements.txt

# 迁移数据库
if [ -f "migrate.sh" ]; then
    echo "迁移数据库..."
    bash migrate.sh
fi

# 恢复配置
if [ -f "config.json.bak" ]; then
    echo "恢复配置..."
    mv config.json.bak config.json
fi

# 重启服务
echo "重启服务..."
if pgrep -f "cross-border-core" > /dev/null; then
    pkill -f "cross-border-core"
fi

echo "✅ 更新完成"
