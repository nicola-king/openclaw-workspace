#!/bin/bash
# 跨境贸易 Agent - 定时任务配置脚本
# 太一 AGI · 2026-04-18

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/01-trading/cross-border-trade-agent"
LOG_DIR="$WORKSPACE/logs/cross-border"

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "🔧 配置跨境贸易 Agent 定时任务..."

# 备份现有 crontab
crontab -l > /tmp/crontab.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

# 添加定时任务
(crontab -l 2>/dev/null || echo "") | grep -v "cross-border" | { cat; cat << EOF

# 跨境贸易 Agent 定时任务
# 每日情报简报 (08:00)
0 8 * * * cd $SKILL_DIR && python3 intelligence_reporter.py --daily >> $LOG_DIR/daily-brief.log 2>&1

# 每周趋势分析 (周一 09:00)
0 9 * * 1 cd $SKILL_DIR && python3 product_trend_forecaster.py --weekly >> $LOG_DIR/weekly-trend.log 2>&1

# 每月战略报告 (月初 10:00)
0 10 1 * * cd $SKILL_DIR && python3 intelligence_reporter.py --monthly >> $LOG_DIR/monthly-strategy.log 2>&1

# 智能选品监控 (每 4 小时)
0 */4 * * * cd $SKILL_DIR && python3 intelligence_reporter.py --smart-product >> $LOG_DIR/smart-product-monitor.log 2>&1

# 竞品分析 (每日 18:00)
0 18 * * * cd $SKILL_DIR && python3 intelligence_reporter.py --competitor >> $LOG_DIR/competitor-analysis.log 2>&1

# 健康检查 (每小时)
0 * * * * cd $WORKSPACE && python3 scripts/hourly-health-check.py >> $LOG_DIR/health-check.log 2>&1

EOF
} | crontab -

echo "✅ 定时任务配置完成！"
echo ""
echo "📋 已配置的定时任务:"
echo "  • 每日情报简报 (08:00)"
echo "  • 每周趋势分析 (周一 09:00)"
echo "  • 每月战略报告 (月初 10:00)"
echo "  • 竞品监控 (每 4 小时)"
echo "  • 健康检查 (每小时)"
echo ""
echo "📁 日志目录：$LOG_DIR"
echo ""
echo "🔍 查看定时任务:"
echo "  crontab -l | grep cross-border"
echo ""
echo "📝 查看日志:"
echo "  tail -f $LOG_DIR/daily-brief.log"
