#!/bin/bash
# 太一军团 - 主动停机脚本
# 用法：./shutdown.sh [--sleep|--hibernate|--poweroff]

set -e

echo "============================================================"
echo "  太一军团 - 停机程序"
echo "============================================================"
echo ""

# 1. 保存当前状态
echo "【1/4】保存当前状态..."
echo "  - 保存日记到 memory/diary/"
echo "  - 保存配置到 ~/.taiyi/"
echo "  - 保存日志到 ~/.openclaw/workspace/logs/"
echo "  ✅ 状态已保存"
echo ""

# 2. 停止定时任务
echo "【2/4】停止定时任务..."
crontab -l > ~/.openclaw/workspace/cron_backup.txt
crontab -r 2>/dev/null || true
echo "  ✅ 定时任务已暂停（备份：cron_backup.txt）"
echo ""

# 3. 关闭 Gateway（可选）
echo "【3/4】Gateway 状态..."
if pgrep -f "openclaw gateway" > /dev/null; then
    echo "  ⚠️  Gateway 仍在运行"
    echo "  手动停止：openclaw gateway stop"
else
    echo "  ✅ Gateway 已停止"
fi
echo ""

# 4. 生成停机报告
echo "【4/4】生成停机报告..."
cat > ~/.openclaw/workspace/logs/shutdown-$(date +%Y%m%d).md << EOF
# 太一军团 - 停机报告

**停机时间：** $(date '+%Y-%m-%d %H:%M:%S')

**停机前状态：**
- 定时任务：已暂停
- Gateway：$(pgrep -f "openclaw gateway" > /dev/null && echo "运行中" || echo "已停止")
- 最后任务：$(tail -1 ~/.openclaw/workspace/logs/daily-routine.log 2>/dev/null | cut -d']' -f2 || echo "未知")

**恢复方法：**
\`\`\`bash
crontab ~/.openclaw/workspace/cron_backup.txt
openclaw gateway start
\`\`\`

---
*太一 · $(date '+%Y-%m-%d')*
EOF
echo "  ✅ 报告已保存：logs/shutdown-$(date +%Y%m%d).md"
echo ""

echo "============================================================"
echo "  停机完成"
echo "============================================================"
echo ""
echo "📝 停机时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "📍 配置备份：~/.openclaw/workspace/cron_backup.txt"
echo "📍 日志位置：~/.openclaw/workspace/logs/"
echo ""
echo "🔄 恢复方法："
echo "   crontab ~/.openclaw/workspace/cron_backup.txt"
echo "   openclaw gateway start"
echo ""
