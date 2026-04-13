#!/bin/bash
# daily-wisdom.sh - 每日智慧推送脚本（卡片格式 + 自动发送）
# 用法：bash scripts/daily-wisdom.sh [--send]

WORKSPACE="$HOME/.openclaw/workspace"
WISDOM_FILE="$WORKSPACE/wisdom/dao-buddha-quotes.md"
DATE=$(date +%Y-%m-%d)
WEEKDAY_NUM=$(date +%u)
HOUR=$(date +%H)
SEND_FLAG="${1:-}"

# 星期映射（数字转中文）
case $WEEKDAY_NUM in
    1) WEEKDAY_CN="周一" ;;
    2) WEEKDAY_CN="周二" ;;
    3) WEEKDAY_CN="周三" ;;
    4) WEEKDAY_CN="周四" ;;
    5) WEEKDAY_CN="周五" ;;
    6) WEEKDAY_CN="周六" ;;
    7) WEEKDAY_CN="周日" ;;
esac

# 从智慧库中随机选择一句
get_random_quote() {
    local quotes=()
    local sources=()
    
    # 提取道德经
    while IFS= read -r line; do
        if [[ "$line" =~ ^[0-9]+\.[[:space:]]+(.*) ]]; then
            quotes+=("${BASH_REMATCH[1]}")
            sources+=("《道德经》")
        fi
    done < <(sed -n '/### 《道德经》/,/### 《庄子》/p' "$WISDOM_FILE")
    
    # 提取庄子
    while IFS= read -r line; do
        if [[ "$line" =~ ^[0-9]+\.[[:space:]]+(.*) ]]; then
            quotes+=("${BASH_REMATCH[1]}")
            sources+=("《庄子》")
        fi
    done < <(sed -n '/### 《庄子》/,/## 佛家智慧/p' "$WISDOM_FILE")
    
    # 提取心经
    while IFS= read -r line; do
        if [[ "$line" =~ ^[0-9]+\.[[:space:]]+(.*) ]]; then
            quotes+=("${BASH_REMATCH[1]}")
            sources+=("《心经》")
        fi
    done < <(sed -n '/### 《心经》/,/### 《金刚经》/p' "$WISDOM_FILE")
    
    # 提取金刚经
    while IFS= read -r line; do
        if [[ "$line" =~ ^[0-9]+\.[[:space:]]+(.*) ]]; then
            quotes+=("${BASH_REMATCH[1]}")
            sources+=("《金刚经》")
        fi
    done < <(sed -n '/### 《金刚经》/,/### 禅宗公案/p' "$WISDOM_FILE")
    
    # 提取禅宗公案
    while IFS= read -r line; do
        if [[ "$line" =~ ^[0-9]+\.[[:space:]]+(.*) ]]; then
            quotes+=("${BASH_REMATCH[1]}")
            sources+=("禅宗")
        fi
    done < <(sed -n '/### 禅宗公案/,/### 佛家箴言/p' "$WISDOM_FILE")
    
    # 随机选择
    local count=${#quotes[@]}
    if [ $count -gt 0 ]; then
        local idx=$((RANDOM % count))
        echo "${quotes[$idx]}|${sources[$idx]}"
    else
        echo "道可道，非常道。|《道德经》"
    fi
}

# 判断道家或佛家
get_type() {
    local source=$1
    if [[ "$source" == *"道德经"* ]] || [[ "$source" == *"庄子"* ]]; then
        echo "道家"
    else
        echo "佛家"
    fi
}

# 获取今日智慧
RESULT=$(get_random_quote)
QUOTE=$(echo "$RESULT" | cut -d'|' -f1)
SOURCE=$(echo "$RESULT" | cut -d'|' -f2)
TYPE=$(get_type "$SOURCE")

# 生成卡片格式消息（适合微信转发）
CARD_MESSAGE="━━━━━━━━━━━━━━━━━━
📿  晨间智慧  ·  $DATE  $WEEKDAY_CN
━━━━━━━━━━━━━━━━━━

$TYPE  ·  $SOURCE

╔══════════════════════╗
║
║   $QUOTE
║
╚══════════════════════╝

—— 太一  ·  晨起静心

━━━━━━━━━━━━━━━━━━
🙏 愿您今日  心安自在"

# 输出到 stdout（用于手动查看）
echo "$CARD_MESSAGE"

# 记录日志
echo "[$DATE $HOUR:00] $TYPE · $SOURCE: $QUOTE" >> "$WORKSPACE/memory/daily-wisdom-log.md"

# 如果带 --send 参数，通过 OpenClaw 发送
if [[ "$SEND_FLAG" == "--send" ]]; then
    # 方法 1: 通过 openclaw message send 发送
    if command -v openclaw &> /dev/null; then
        # 使用 openclaw-weixin 通道
        openclaw message send --channel openclaw-weixin --target "o9cq80yz80T13iCV5N_djDCSVo88@im.wechat" --message "$CARD_MESSAGE" 2>&1 | tee -a "$WORKSPACE/logs/wisdom-send.log"
        if [ ${PIPESTATUS[0]} -eq 0 ]; then
            echo "[$DATE $HOUR:00] ✅ 已发送微信" >> "$WORKSPACE/memory/daily-wisdom-log.md"
        else
            echo "[$DATE $HOUR:00] ❌ 发送失败" >> "$WORKSPACE/memory/daily-wisdom-log.md"
        fi
    # 方法 2: 保存到待发送队列（由主 session 处理）
    else
        echo "$CARD_MESSAGE" >> "$WORKSPACE/.pending-messages.md"
        echo "[$DATE $HOUR:00] ⏳ 已加入待发送队列" >> "$WORKSPACE/memory/daily-wisdom-log.md"
    fi
fi
