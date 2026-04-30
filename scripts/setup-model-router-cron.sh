#!/bin/bash
# 设置模型路由器 Cron 定时任务

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK_SCRIPT="$SCRIPT_DIR/check-bailian-quota.py"
PYTHON_CMD="python3"

echo "🔧 设置模型路由器 Cron 任务..."
echo ""

# 检查 Python
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Python3 未找到"
    exit 1
fi

# 检查脚本
if [ ! -f "$CHECK_SCRIPT" ]; then
    echo "❌ 脚本不存在：$CHECK_SCRIPT"
    exit 1
fi

# 显示当前 crontab
echo "📋 当前 crontab:"
crontab -l 2>/dev/null || echo "(空)"
echo ""

# 添加到 crontab
CRON_ENTRY="*/5 * * * * $PYTHON_CMD $CHECK_SCRIPT >> /home/nicola/.openclaw/workspace/logs/model-router-cron.log 2>&1"

echo "✅ 将添加以下 Cron 任务:"
echo "   $CRON_ENTRY"
echo ""

# 备份当前 crontab
(crontab -l 2>/dev/null | grep -v "check-bailian-quota.py"; echo "$CRON_ENTRY") | crontab -

echo ""
echo "✅ Cron 任务已添加"
echo ""
echo "📋 验证:"
crontab -l | grep "check-bailian-quota"
echo ""
echo "📝 日志文件：/home/nicola/.openclaw/workspace/logs/model-router-cron.log"
echo ""
echo "🔍 手动测试:"
echo "   $PYTHON_CMD $CHECK_SCRIPT"
