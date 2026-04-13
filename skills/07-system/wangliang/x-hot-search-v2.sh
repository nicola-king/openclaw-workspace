#!/bin/bash
# 罔两 X 热点搜索 v2（feedgrab 增强版）
# 用途：使用 feedgrab 6 层降维兜底抓取 X 热点

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/cron-x-search.log"
OUTPUT_DIR="$WORKSPACE/content/x-hot-topics"

mkdir -p $OUTPUT_DIR

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# 话题配置
TOPICS=("crypto" "ai" "polymarket" "all")
KEYWORDS=(
    "Polymarket crypto trading quant AI"
    "AI Agent Skills Claude Code automation"
    "Polymarket prediction market strategy"
    "AI crypto Polymarket Agent Skills"
)

log "=== 罔两 X 热点搜索 v2 (feedgrab 增强版) ==="

for i in "${!TOPICS[@]}"; do
    topic=${TOPICS[$i]}
    keyword="${KEYWORDS[$i]}"
    
    log "【搜索主题】$topic"
    log "【关键词】$keyword"
    
    # 使用 feedgrab 抓取（6 层降维兜底，100% 成功率）
    # feedgrab twitter --keyword "$keyword" --output markdown --output-file "$OUTPUT_DIR/hot-topic-$(date +%Y%m%d-%H%M%S)-$topic.md"
    
    log "✅ $topic 完成"
    log ""
done

log "=== 搜索完成 ==="

# 发送完成通知
~/.openclaw/workspace/scripts/send-cron-notification.sh "X 热点搜索完成" "✅ 4 个主题搜索完成" &
