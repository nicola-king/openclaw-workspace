#!/bin/bash
# 太一 Scheduler Agent 紧急修复脚本
echo "🔧 启动 Scheduler Agent 守护进程..."
cd /home/nicola/.openclaw/workspace
python3 skills/scheduler-agent/src/scheduler.py --daemon
sleep 3
echo "✅ 守护进程已启动"
echo ""
echo "📊 验证状态..."
python3 skills/scheduler-agent/src/scheduler.py --status
