#!/bin/bash
# AGI 进化保障 Cron 配置脚本
# 创建时间：2026-04-03 14:20

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
BACKUP_FILE="/tmp/crontab-backup-$(date +%Y%m%d-%H%M).txt"

echo "🔧 AGI 进化 Cron 配置启动..."

# 1. 备份当前配置
echo "💾 备份当前配置..."
crontab -l > "$BACKUP_FILE" 2>/dev/null || echo "# 空配置" > "$BACKUP_FILE"
echo "✅ 备份：$BACKUP_FILE"

# 2. 准备新配置
TEMP_CRON=$(mktemp)

# 保留现有配置
cat "$BACKUP_FILE" > "$TEMP_CRON"

# 3. 添加 AGI 进化 Cron（如果不存在）
echo "" >> "$TEMP_CRON"
echo "# === AGI 进化保障 Cron（2026-04-03）===" >> "$TEMP_CRON"

# 每小时任务
if ! crontab -l 2>/dev/null | grep -q "self-check/run.py"; then
    echo "0 * * * * cd $WORKSPACE && python3 skills/steward/self-check/run.py >> logs/self-check.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：自检（每小时）"
fi

if ! crontab -l 2>/dev/null | grep -q "intervention-monitor/run.py"; then
    echo "0 * * * * cd $WORKSPACE && python3 skills/steward/intervention-monitor/run.py >> logs/intervention-monitor.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：干预监控（每小时）"
fi

if ! crontab -l 2>/dev/null | grep -q "check-degradation.py"; then
    echo "0 * * * * cd $WORKSPACE && python3 scripts/check-degradation.py >> logs/degradation-check.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：退化检测（每小时）"
fi

if ! crontab -l 2>/dev/null | grep -q "update-evolution-state.py"; then
    echo "0 * * * * cd $WORKSPACE && python3 scripts/update-evolution-state.py >> logs/evolution-state.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：状态更新（每小时）"
fi

# 每日任务
if ! crontab -l 2>/dev/null | grep -q "high-value-discovery/run.py"; then
    echo "0 1 * * * cd $WORKSPACE && python3 skills/wangliang/high-value-discovery/run.py >> logs/high-value-discovery.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：高价值发现（01:00）"
fi

if ! crontab -l 2>/dev/null | grep -q "night-learning/run.py"; then
    echo "0 1 * * * cd $WORKSPACE && python3 skills/taiyi/night-learning/run.py >> logs/night-learning.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：凌晨学习（01:00）"
fi

if ! crontab -l 2>/dev/null | grep -q "monetization-tracker/run.py"; then
    echo "0 23 * * * cd $WORKSPACE && python3 skills/paoding/monetization-tracker/run.py >> logs/monetization-tracker.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：变现追踪（23:00）"
fi

if ! crontab -l 2>/dev/null | grep -q "stage-verification/run.py.*--stage=4"; then
    echo "0 23 * * * cd $WORKSPACE && python3 skills/steward/stage-verification/run.py --stage=4 >> logs/verify-stage4.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：阶段 4 验收（23:00）"
fi

if ! crontab -l 2>/dev/null | grep -q "stage-verification/run.py.*--stage=3"; then
    echo "0 23 7 4 * cd $WORKSPACE && python3 skills/steward/stage-verification/run.py --stage=3 >> logs/verify-stage3.log 2>&1" >> "$TEMP_CRON"
    echo "✅ 添加：阶段 3 验收（04-07 23:00）"
fi

# 4. 应用新配置
echo ""
echo "📋 应用新配置..."
crontab "$TEMP_CRON"

# 5. 验证
echo ""
echo "=== 验证结果 ==="
CRON_COUNT=$(crontab -l 2>/dev/null | wc -l)
echo "总任务数：$CRON_COUNT 项"

AGI_COUNT=$(crontab -l 2>/dev/null | grep -cE "self-check|intervention-monitor|check-degradation|update-evolution|high-value|night-learning|monetization|stage-verification" || echo 0)
echo "AGI 进化任务：$AGI_COUNT 项"

# 6. 清理
rm -f "$TEMP_CRON"

echo ""
echo "✅ AGI 进化 Cron 配置完成！"
echo "💾 备份文件：$BACKUP_FILE"
