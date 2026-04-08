#!/bin/bash
# scripts/setup-crontab.sh

"""
太一 Crontab 定时任务配置

功能:
1. 配置记忆同步定时任务 (每小时)
2. 配置日报生成定时任务 (每日 23:00)
3. 配置宪法学习定时任务 (每日 06:00)
4. 配置模型使用统计 (每日 09:00)

使用:
    bash scripts/setup-crontab.sh

注意:
    - 需要手动确认 crontab 配置
    - 可通过 crontab -e 手动编辑
"""

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
CRON_BACKUP="$WORKSPACE/config/crontab.backup.$(date +%Y%m%d%H%M)"

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "============================================================"
echo "🕐 太一 Crontab 定时任务配置"
echo "============================================================"

# 备份现有 crontab
if crontab -l > /dev/null 2>&1; then
    echo ""
    echo "📋 备份现有 crontab..."
    crontab -l > "$CRON_BACKUP"
    echo "✅ 已备份到：$CRON_BACKUP"
else
    echo "⚠️  无现有 crontab"
fi

echo ""
echo "📋 当前 crontab 内容:"
echo "------------------------------------------------------------"
crontab -l 2>/dev/null || echo "(空)"
echo "------------------------------------------------------------"

# 定义新任务
cat << 'EOF' > /tmp/taiyi_cron_tasks.txt
# 太一定时任务 (由 setup-crontab.sh 生成)

# 每日 06:00 - 宪法学习 + 记忆提炼
0 6 * * * cd /home/nicola/.openclaw/workspace && bash scripts/daily-constitution.sh >> logs/constitution.log 2>&1

# 每日 09:00 - 模型使用统计
0 9 * * * cd /home/nicola/.openclaw/workspace && python3 scripts/model-usage-stats.py >> logs/model-stats.log 2>&1

# 每小时 - 记忆同步到 Feishu
0 * * * * cd /home/nicola/.openclaw/workspace && python3 scripts/sync-memory-to-feishu.py >> logs/memory-sync.log 2>&1

# 每日 23:00 - 日报生成 + 记忆归档
0 23 * * * cd /home/nicola/.openclaw/workspace && bash /opt/openclaw-report.sh daily >> logs/daily-report.log 2>&1

# 每周一 09:00 - 周报生成
0 9 * * 1 cd /home/nicola/.openclaw/workspace && bash /opt/openclaw-report.sh weekly >> logs/weekly-report.log 2>&1

# 每月 1 日 09:00 - 月报生成
0 9 1 * * cd /home/nicola/.openclaw/workspace && bash /opt/openclaw-report.sh monthly >> logs/monthly-report.log 2>&1
EOF

echo ""
echo "📝 新定时任务:"
echo "------------------------------------------------------------"
cat /tmp/taiyi_cron_tasks.txt
echo "------------------------------------------------------------"

# 合并 crontab
echo ""
echo "🔧 合并 crontab..."

# 移除旧的太一任务 (如果有)
crontab -l 2>/dev/null | grep -v "太一" | grep -v "taiyi" | grep -v "openclaw-report" | grep -v "daily-constitution" | grep -v "sync-memory" | grep -v "model-usage" > /tmp/cron_existing.txt || true

# 合并新任务
cat /tmp/cron_existing.txt /tmp/taiyi_cron_tasks.txt > /tmp/cron_merged.txt

# 显示预览
echo ""
echo "👁️  合并后预览:"
echo "------------------------------------------------------------"
cat /tmp/cron_merged.txt
echo "------------------------------------------------------------"

# 询问确认
echo ""
read -p "✅ 确认安装这些定时任务？(y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    crontab /tmp/cron_merged.txt
    echo ""
    echo "✅ 定时任务已安装!"
    echo ""
    echo "📋 验证安装:"
    crontab -l
    echo ""
    echo "📝 日志文件位置:"
    echo "  - $LOG_DIR/constitution.log"
    echo "  - $LOG_DIR/model-stats.log"
    echo "  - $LOG_DIR/memory-sync.log"
    echo "  - $LOG_DIR/daily-report.log"
    echo "  - $LOG_DIR/weekly-report.log"
    echo "  - $LOG_DIR/monthly-report.log"
else
    echo "❌ 已取消安装"
fi

# 清理临时文件
rm -f /tmp/taiyi_cron_tasks.txt /tmp/cron_existing.txt /tmp/cron_merged.txt

echo ""
echo "============================================================"
echo "✅ 配置完成"
echo "============================================================"
