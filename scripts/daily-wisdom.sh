#!/bin/bash
# daily-wisdom.sh - 每日智慧推送脚本
# 用法：bash scripts/daily-wisdom.sh

WORKSPACE="$HOME/.openclaw/workspace"
WISDOM_FILE="$WORKSPACE/wisdom/dao-buddha-quotes.md"
DATE=$(date +%Y-%m-%d)
HOUR=$(date +%H)

# 从智慧库中随机选择一句
get_random_quote() {
    # 读取智慧库，提取所有语录
    local quotes=()
    
    # 提取道家智慧
    while IFS= read -r line; do
        if [[ "$line" =~ ^[0-9]+\.[[:space:]]+(.*) ]]; then
            quotes+=("${BASH_REMATCH[1]}")
        fi
    done < <(sed -n '/## 《道德经》/,/## 《庄子》/p' "$WISDOM_FILE" | head -20)
    
    # 随机选择
    local count=${#quotes[@]}
    if [ $count -gt 0 ]; then
        local idx=$((RANDOM % count))
        echo "${quotes[$idx]}"
    else
        echo "道可道，非常道。"
    fi
}

# 获取今日智慧
QUOTE=$(get_random_quote)
SOURCE="《道德经》"
TYPE="道家"

# 随机选择道家或佛家
if [ $((RANDOM % 2)) -eq 0 ]; then
    TYPE="道家"
    SOURCE="《道德经》"
else
    TYPE="佛家"
    SOURCE="《心经》"
fi

# 推送消息
MESSAGE="📿 晨间智慧 · $DATE

$TYPE · $SOURCE

「$QUOTE」

—— 太一 · 晨起静心"

echo "$MESSAGE"

# 通过 OpenClaw 发送（需要配置微信通道）
# openclaw send "SAYELF" "$MESSAGE"

# 记录日志
echo "[$DATE $HOUR:00] 推送：$QUOTE" >> "$WORKSPACE/memory/daily-wisdom-log.md"
