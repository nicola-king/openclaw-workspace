#!/bin/bash
# 每日 23:00 记忆提炼脚本
# 功能：扫描当日 memory/YYYY-MM-DD.md，提炼关键内容到 MEMORY.md

set -e

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$WORKSPACE/memory/$TODAY.md"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始记忆提炼..."

# 检查今日文件是否存在
if [ ! -f "$TODAY_FILE" ]; then
    echo "⚠️ 今日记忆文件不存在：$TODAY_FILE"
    exit 0
fi

# 提取关键内容（带标记的行）
KEY_DECISIONS=$(grep -E "^\[决策\]|^### \[|✅ |🟡 |🔴 " "$TODAY_FILE" 2>/dev/null | head -20 || echo "")

if [ -z "$KEY_DECISIONS" ]; then
    echo "⚠️ 未发现关键内容"
    exit 0
fi

# 追加到 MEMORY.md（如果存在）
if [ -f "$MEMORY_FILE" ]; then
    echo -e "\n## 📝 $TODAY 归档\n" >> "$MEMORY_FILE"
    echo "$KEY_DECISIONS" >> "$MEMORY_FILE"
    echo -e "\n*归档时间：$(date '+%Y-%m-%d %H:%M')*\n" >> "$MEMORY_FILE"
    echo "✅ 已提炼到 MEMORY.md"
else
    echo "⚠️ MEMORY.md 不存在，跳过"
    exit 0
fi

# 更新索引
echo "✅ 记忆提炼完成"
