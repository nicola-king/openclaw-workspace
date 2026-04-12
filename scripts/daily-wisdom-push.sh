#!/bin/bash
# 每日智慧推送脚本 (道家 + 佛家)
# 每天早晨 8 点执行

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🌅 开始运行每日智慧推送..." >> "$LOG_DIR/daily-wisdom-push.log"

# 推送道家智慧
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📿 推送道家智慧..." >> "$LOG_DIR/daily-wisdom-push.log"
python3 "$WORKSPACE/skills/dao-agent/daily_dao_wisdom.py" >> "$LOG_DIR/daily-wisdom-push.log" 2>&1

# 推送佛家智慧
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🪷 推送佛家智慧..." >> "$LOG_DIR/daily-wisdom-push.log"
python3 "$WORKSPACE/skills/wu-enlightenment/daily_buddhist_wisdom.py" >> "$LOG_DIR/daily-wisdom-push.log" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 每日智慧推送完成！" >> "$LOG_DIR/daily-wisdom-push.log"
echo "" >> "$LOG_DIR/daily-wisdom-push.log"
