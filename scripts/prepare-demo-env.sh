#!/bin/bash
# OpenClaw 演示环境准备脚本
# 太一 AGI · 2026-04-15

echo "========================================"
echo "OpenClaw 演示环境准备"
echo "========================================"

# 1. 检查 Gateway 状态
echo ""
echo "[1/6] 检查 Gateway 状态..."
openclaw gateway status

# 2. 启动 Gateway (如未运行)
echo ""
echo "[2/6] 启动 Gateway..."
openclaw gateway start

# 3. 检查守护进程
echo ""
echo "[3/6] 检查守护进程..."
ps aux | grep wisdom-scheduler | grep -v grep

# 4. 加载演示数据
echo ""
echo "[4/6] 加载演示数据..."
python3 /home/nicola/.openclaw/workspace/scripts/prepare-demo-data.py

# 5. 检查 Cron 配置
echo ""
echo "[5/6] 检查 Cron 配置..."
crontab -l | head -10

# 6. 显示系统状态
echo ""
echo "[6/6] 系统状态..."
openclaw status

echo ""
echo "========================================"
echo "✅ 演示环境准备完成！"
echo "========================================"
echo ""
echo "演示账号：demo@openclaw.ai"
echo "演示密码：demo2026"
echo ""
echo "WiFi: OpenClaw-Demo"
echo "密码：openclaw2026"
echo ""
