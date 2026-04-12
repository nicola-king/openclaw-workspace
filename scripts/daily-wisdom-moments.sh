#!/bin/bash
# daily-wisdom-moments.sh - 朋友圈智慧卡片
# 用法：bash scripts/daily-wisdom-moments.sh

WORKSPACE="$HOME/.openclaw/workspace"
WISDOM_FILE="$WORKSPACE/wisdom/dao-buddha-quotes.md"
DATE=$(date +%Y-%m-%d)
WEEKDAY_NUM=$(date +%u)
HOUR=$(date +%H)

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

# 朋友圈格式 1 - 简约风
MOMENTS_V1="📅 $DATE  ·  $WEEKDAY_CN
━━━━━━━━━━━━━━━━

📿 晨间智慧

$QUOTE

—— $SOURCE

🙏 太一 · 晨起静心"

# 朋友圈格式 2 - 禅意风
MOMENTS_V2="╭ ◜◝ ͡ ◜◝ ͡ ◜◝ ╮
   晨间智慧
╰ ◟◞ ͜ ◟◞ ͜ ◟◞ ╯

$DATE  ·  $WEEKDAY_CN

$QUOTE

  $SOURCE
  
🌿 太一"

# 朋友圈格式 3 - 竖排古风
MOMENTS_V3="【晨间智慧】
$DATE  $WEEKDAY_CN
──────────
$QUOTE
──────────
$SOURCE
🙏"

# 朋友圈格式 4 - 极简风
MOMENTS_V4="$QUOTE

—— $SOURCE · $TYPE

📿 $DATE"

# 输出所有格式
echo "═══════════════════════════════════"
echo "📱 朋友圈格式 1 - 简约风"
echo "═══════════════════════════════════"
echo "$MOMENTS_V1"
echo ""
echo "═══════════════════════════════════"
echo "📱 朋友圈格式 2 - 禅意风"
echo "═══════════════════════════════════"
echo "$MOMENTS_V2"
echo ""
echo "═══════════════════════════════════"
echo "📱 朋友圈格式 3 - 竖排古风"
echo "═══════════════════════════════════"
echo "$MOMENTS_V3"
echo ""
echo "═══════════════════════════════════"
echo "📱 朋友圈格式 4 - 极简风"
echo "═══════════════════════════════════"
echo "$MOMENTS_V4"
echo ""

# 记录日志
echo "[$DATE] 朋友圈：$QUOTE ($SOURCE)" >> "$WORKSPACE/memory/daily-wisdom-log.md"

# 保存各格式到文件（方便复制）
echo "$MOMENTS_V1" > "$WORKSPACE/wisdom/moments-v1.txt"
echo "$MOMENTS_V2" > "$WORKSPACE/wisdom/moments-v2.txt"
echo "$MOMENTS_V3" > "$WORKSPACE/wisdom/moments-v3.txt"
echo "$MOMENTS_V4" > "$WORKSPACE/wisdom/moments-v4.txt"

echo ""
echo "✅ 已保存到 wisdom/moments-v{1,2,3,4}.txt"
