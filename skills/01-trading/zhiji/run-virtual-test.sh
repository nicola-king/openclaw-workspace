#!/bin/bash
# 知几-E 虚拟盘测试脚本
# 用法：bash run-virtual-test.sh [days] [balance]

DAYS=${1:-30}
BALANCE=${2:-1000}

cd /home/nicola/.openclaw/workspace/skills/zhiji

echo "======================================================================"
echo "  知几-E 虚拟盘策略验证"
echo "======================================================================"
echo ""
echo "参数配置:"
echo "  模拟天数：  $DAYS 天"
echo "  初始资金：  \$$BALANCE"
echo "  每日交易：  5 笔"
echo "  策略版本：  v2.1 (ColdMath 增强版)"
echo ""
echo "策略阈值:"
echo "  置信度：    >= 96%"
echo "  优势：      >= 2%"
echo "  下注金额：  \$10/笔"
echo ""
echo "======================================================================"
echo ""

python3 virtual-trader.py --mode auto --days $DAYS --trades-per-day 5 --balance $BALANCE

echo ""
echo "💡 下一步:"
echo "  1. 查看完整交易记录：cat ~/.taiyi/zhiji/virtual-trader.json | jq"
echo "  2. 重置虚拟盘：python3 virtual-trader.py --mode reset"
echo "  3. 手动模式：python3 virtual-trader.py --mode manual"
echo ""
