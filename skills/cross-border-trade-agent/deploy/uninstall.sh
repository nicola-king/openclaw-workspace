#!/bin/bash
# uninstall.sh - 跨境贸易 Agent 卸载脚本

set -e

echo "=== 跨境贸易 Agent v9.0.0 卸载 ==="

# 停止服务
if pgrep -f "cross-border-core" > /dev/null; then
    echo "停止服务..."
    pkill -f "cross-border-core"
fi

# 删除虚拟环境
if [ -d "venv" ]; then
    echo "删除虚拟环境..."
    rm -rf venv
fi

# 删除日志
if [ -d "logs" ]; then
    echo "删除日志..."
    rm -rf logs
fi

# 删除输出
if [ -d "output" ]; then
    echo "删除输出..."
    rm -rf output
fi

echo "✅ 卸载完成"
