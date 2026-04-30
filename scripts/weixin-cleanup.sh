#!/bin/bash
# 微信账号自动清理脚本
# 功能：每个微信 userId 只保留最新的 token，删除重复的旧 token

set -e

ACCOUNTS_DIR="/home/nicola/.openclaw/openclaw-weixin/accounts"
ACCOUNTS_FILE="/home/nicola/.openclaw/openclaw-weixin/accounts.json"

echo "🧹 微信账号自动清理脚本"
echo "======================"
echo ""

# 检查目录是否存在
if [ ! -d "$ACCOUNTS_DIR" ]; then
    echo "❌ 微信账号目录不存在：$ACCOUNTS_DIR"
    exit 1
fi

# 收集所有 userId 和对应的 token 文件
declare -A userIdMap  # userId -> "latestToken:latestTime"

for file in "$ACCOUNTS_DIR"/*.json; do
    # 跳过 .sync.json 文件
    if [[ "$file" == *".sync.json" ]]; then
        continue
    fi
    
    # 跳过 accounts.json
    if [[ "$file" == *"accounts.json" ]]; then
        continue
    fi
    
    # 提取 userId 和 savedAt
    userId=$(grep -o '"userId"[[:space:]]*:[[:space:]]*"[^"]*"' "$file" | cut -d'"' -f4)
    savedAt=$(grep -o '"savedAt"[[:space:]]*:[[:space:]]*"[^"]*"' "$file" | cut -d'"' -f4)
    tokenBase=$(basename "$file" .json)
    
    if [ -z "$userId" ] || [ -z "$savedAt" ]; then
        continue
    fi
    
    # 检查是否已有该 userId 的记录
    existing="${userIdMap[$userId]}"
    
    if [ -z "$existing" ]; then
        # 第一个遇到的 token
        userIdMap[$userId]="$tokenBase:$savedAt"
    else
        # 比较时间，保留更新的
        existingTime="${existing#*:}"
        if [[ "$savedAt" > "$existingTime" ]]; then
            userIdMap[$userId]="$tokenBase:$savedAt"
        fi
    fi
done

# 输出结果
echo "📊 检测到以下微信账号："
echo ""

keptFiles=()
deletedCount=0

for userId in "${!userIdMap[@]}"; do
    latestInfo="${userIdMap[$userId]}"
    latestToken="${latestInfo%%:*}"
    latestTime="${latestInfo#*:}"
    
    echo "👤 userId: $userId"
    echo "   ✅ 保留：$latestToken ($latestTime)"
    keptFiles+=("$latestToken")
    
    # 删除该 userId 的其他旧 token
    for file in "$ACCOUNTS_DIR"/*.json; do
        if [[ "$file" == *".sync.json" ]]; then
            continue
        fi
        
        fileBase=$(basename "$file" .json)
        fileUserId=$(grep -o '"userId"[[:space:]]*:[[:space:]]*"[^"]*"' "$file" 2>/dev/null | cut -d'"' -f4)
        
        if [ "$fileUserId" == "$userId" ] && [ "$fileBase" != "$latestToken" ]; then
            fileTime=$(grep -o '"savedAt"[[:space:]]*:[[:space:]]*"[^"]*"' "$file" | cut -d'"' -f4)
            echo "   ❌ 删除：$fileBase ($fileTime)"
            rm -f "$file" "${file}.sync.json"
            ((deletedCount++))
        fi
    done
    echo ""
done

# 更新 accounts.json
echo "[" > "$ACCOUNTS_FILE"
first=true
for token in "${keptFiles[@]}"; do
    if [ "$first" = true ]; then
        echo "  \"$token-im-bot\"" >> "$ACCOUNTS_FILE"
        first=false
    else
        echo ", \"$token-im-bot\"" >> "$ACCOUNTS_FILE"
    fi
done
echo "]" >> "$ACCOUNTS_FILE"

# 修复 JSON 格式（移除逗号换行问题）
python3 -c "
import json
with open('$ACCOUNTS_FILE', 'r') as f:
    data = json.load(f)
with open('$ACCOUNTS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null || true

echo "======================"
echo "✅ 清理完成！"
echo "   保留账号：${#keptFiles[@]} 个"
echo "   删除重复：$deletedCount 个"
echo ""
echo "📁 accounts.json 已更新"
