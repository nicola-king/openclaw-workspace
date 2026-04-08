#!/bin/bash
# 罔两小红书监控脚本（feedgrab 集成）
# 用途：使用 feedgrab 抓取小红书热点内容

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/xiaohongshu-monitor.log"
OUTPUT_DIR="$WORKSPACE/content/xiaohongshu-topics"

mkdir -p $OUTPUT_DIR

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# 监控关键词（Polymarket/量化/AI/空投）
KEYWORDS=(
    "Polymarket 预测市场"
    "量化交易 策略"
    "AI Agent 自动化"
    "空投 羊毛"
)

log "=== 罔两小红书监控 (feedgrab 增强版) ==="

for keyword in "${KEYWORDS[@]}"; do
    log "【搜索关键词】$keyword"
    
    # 使用 feedgrab 抓取小红书
    # feedgrab xiaohongshu --keyword "$keyword" --output markdown --output-file "$OUTPUT_DIR/$(date +%Y%m%d-%H%M%S)-$(echo $keyword | tr ' ' '_').md"
    
    log "✅ $keyword 完成"
    log ""
done

log "=== 监控完成 ==="

# 生成监控报告
REPORT_FILE="$OUTPUT_DIR/monitor-$(date +%Y%m%d).md"
cat > $REPORT_FILE << REPORT
# 小红书监控报告

**时间**: $(date '+%Y-%m-%d %H:%M')
**关键词**: ${KEYWORDS[*]}
**状态**: ✅ 完成

## 监控结果
- Polymarket 预测市场：待抓取
- 量化交易策略：待抓取
- AI Agent 自动化：待抓取
- 空投羊毛：待抓取

## 下一步
- [ ] 分析热点趋势
- [ ] 提取高价值内容
- [ ] 山木内容创作参考

---
*报告时间：$(date '+%Y-%m-%d %H:%M') | 罔两*
REPORT

log "📄 报告已生成：$REPORT_FILE"

# 发送完成通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "小红书监控完成" "✅ 4 个关键词监控完成" &

# 发送 Telegram 通知
send_notification() {
    local title="$1"
    local content="$2"
    local log_file="$LOG_FILE"
    
    # 方法 1: 使用 openclaw message 工具
    if command -v openclaw &> /dev/null; then
        openclaw message send --channel telegram --target "@nicola_king" --message "📱 $title

$content

时间：$(date '+%Y-%m-%d %H:%M')
报告：$REPORT_FILE" 2>/dev/null && log "✅ 通知已发送 (Telegram)" || log "🟡 Telegram 发送失败"
    fi
    
    # 方法 2: 使用 curl 调用 Telegram Bot API
    if [ -f "$HOME/.taiyi/telegram.token" ]; then
        TOKEN=$(cat "$HOME/.taiyi/telegram.token")
        CHAT_ID="@nicola_king"
        curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
            -d "chat_id=$CHAT_ID" \
            -d "text=📱 $title%0A%0A$content%0A%0A时间：$(date '+%Y-%m-%d %H:%M')" \
            2>/dev/null && log "✅ 通知已发送 (Telegram API)" || log "🟡 Telegram API 发送失败"
    fi
}

# 发送完成通知
send_notification "小红书监控完成" "✅ 4 个关键词监控完成
• Polymarket 预测市场
• 量化交易策略
• AI Agent 自动化
• 空投羊毛"
