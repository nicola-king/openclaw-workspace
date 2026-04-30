#!/bin/bash
# 太一 Scheduler Agent 紧急修复脚本
# 创建时间：2026-04-16 18:16

echo "=============================================="
echo "太一 Scheduler Agent 紧急修复"
echo "=============================================="
echo ""

# 加载环境变量
if [ -f /home/nicola/.openclaw/.env ]; then
    export $(cat /home/nicola/.openclaw/.env | grep -v '^#' | xargs)
    echo "✅ 环境变量已加载"
else
    echo "⚠️  .env 文件不存在"
fi

echo ""
echo "1️⃣ 启动 Scheduler Agent 守护进程..."
cd /home/nicola/.openclaw/workspace
python3 skills/scheduler-agent/src/scheduler.py --daemon
sleep 2

echo ""
echo "2️⃣ 手动触发 PDCA 循环..."
python3 skills/scheduler-agent/src/pdca-simple.py
sleep 2

echo ""
echo "3️⃣ 手动触发自进化引擎..."
python3 skills/scheduler-agent/src/self-evolution-engine-v2.py
sleep 2

echo ""
echo "4️⃣ 验证运行状态..."
ps aux | grep scheduler.py | grep -v grep
python3 skills/scheduler-agent/src/scheduler.py --status

echo ""
echo "=============================================="
echo "修复完成！"
echo "=============================================="
