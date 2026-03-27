#!/bin/bash
# Cron 任务监控脚本
# 功能：检查定时任务执行情况，失败时发送告警

LOG_DIR="$HOME/.openclaw/workspace/logs"
ALERT_LOG="$LOG_DIR/cron-alerts.log"
WECHAT_LOG="$LOG_DIR/wechat.log"

# 检查任务日志（最近 2 小时）
check_task() {
    local bot=$1
    local task=$2
    local expected_time=$3
    local log_file="$LOG_DIR/cron-$bot.log"
    
    if [ ! -f "$log_file" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $bot-$task: 日志文件不存在" >> "$ALERT_LOG"
        return 1
    fi
    
    # 检查最近是否有执行记录（支持多个关键词）
    local keywords="$task"
    case "$task" in
        "鲸鱼追踪") keywords="鲸鱼";;
        "健康检查") keywords="健康";;
        "支出记录") keywords="支出";;
        "交易日报") keywords="日报";;
        "财务报表") keywords="财务";;
        "晚间汇总") keywords="晚间";;
    esac
    
    local last_run=$(grep -i "$keywords" "$log_file" 2>/dev/null | grep "2026-03-25" | tail -1)
    if [ -z "$last_run" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $bot-$task: 未找到执行记录 (预期：$expected_time)" >> "$ALERT_LOG"
        return 1
    fi
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $bot-$task: 正常" >> "$ALERT_LOG"
    return 0
}

# 主检查流程
echo "=== Cron 任务监控检查 ===" >> "$ALERT_LOG"
echo "检查时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$ALERT_LOG"

# 检查今日应执行的任务
current_hour=$(date +%H)

if [ "$current_hour" -ge 9 ]; then
    check_task "suwen" "健康检查" "09:00"
    check_task "paoding" "支出记录" "09:00"
fi

if [ "$current_hour" -ge 14 ]; then
    check_task "zhiji" "鲸鱼追踪" "14:00"
fi

# 注：以下任务已移除或时间调整，暂时注释
# if [ "$current_hour" -ge 17 ]; then
#     check_task "taiyi" "晚间汇总" "17:00"
# fi

# if [ "$current_hour" -ge 18 ]; then
#     check_task "zhiji" "交易日报" "18:00"
#     check_task "paoding" "财务报表" "18:00"
# fi

# 输出告警摘要并发送微信通知
alert_count=$(grep "❌" "$ALERT_LOG" 2>/dev/null | grep "$(date '+%Y-%m-%d')" | wc -l)
today=$(date '+%Y-%m-%d %H:%M')

if [ "$alert_count" -gt 0 ]; then
    msg="⚠️ 定时任务告警\n时间：$today\n发现 $alert_count 个任务异常\n详见：$ALERT_LOG"
    echo ""
    echo "⚠️  发现 $alert_count 个任务异常，详见：$ALERT_LOG"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  发现 $alert_count 个任务异常" >> "$WECHAT_LOG"
    # 发送微信通知
    echo "$msg" | openclaw message send --channel openclaw-weixin --target "$(whoami)@im.wechat" 2>/dev/null || true
else
    msg="✅ 定时任务检查\n时间：$today\n所有任务正常运行"
    echo "✅ 所有任务正常"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 所有任务正常" >> "$WECHAT_LOG"
    # 发送微信通知（仅异常时发送，正常时不打扰）
    # echo "$msg" | openclaw message send --channel openclaw-weixin --target "$(whoami)@im.wechat" 2>/dev/null || true
fi
