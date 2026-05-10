#!/bin/bash

# ═══════════════════════════════════════════════════

# 美学过滤器 - Cron 兜底扫描 (每 30 分钟)

# 扫描所有未过滤文件，自动处理

# ═══════════════════════════════════════════════════


set -e

WORKSPACE="/home/sayelf/.openclaw/workspace"
FILTER_SCRIPT="$WORKSPACE/skills/art-agent/modules/aesthetic-filter/core.py"
STATE_FILE="$WORKSPACE/memory/aesthetic-scan-state.json"
LOG_FILE="$WORKSPACE/memory/aesthetic-filter.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ═══ Cron 兜底扫描 ═══" >> "$LOG_FILE" 2>/dev/null

# 扫描目录

SCAN_DIRS=(
    "memory"
    "skills"
    "constitution"
    "rules"
    "extensions"
)

FILTERED=0
SKIPPED=0
ERRORS=0
TOTAL=0

for dir in "${SCAN_DIRS[@]}"; do
    FULL_DIR="$WORKSPACE/$dir"
    [ -d "$FULL_DIR" ] || continue
    
    # 查找文本文件
    while IFS= read -r -d '' file; do
        TOTAL=$((TOTAL+1))
        
        # 跳过目录
        [[ "$file" == *"node_modules/"* ]] && { SKIPPED=$((SKIPPED+1)); continue; }
        [[ "$file" == *"__pycache__/"* ]] && { SKIPPED=$((SKIPPED+1)); continue; }
        [[ "$file" == *".pyc" ]] && { SKIPPED=$((SKIPPED+1)); continue; }
        
        # 检查上次过滤时间（跳过最近 10 分钟已过滤的）
        if [ -f "$STATE_FILE" ]; then
            LAST_FILTER=$(grep -o "\"$(basename "$file")\":[0-9]*" "$STATE_FILE" 2>/dev/null | cut -d: -f2)
            if [ -n "$LAST_FILTER" ]; then
                NOW=$(date +%s)
                DIFF=$((NOW - LAST_FILTER))
                if [ "$DIFF" -lt 600 ]; then
                    SKIPPED=$((SKIPPED+1))
                    continue
                fi
            fi
        fi
        
        # 执行美学过滤
        if python3 "$FILTER_SCRIPT" --input "$file" --output "$file" 2>/dev/null; then
            FILTERED=$((FILTERED+1))
            echo "  ✅ 已过滤: $file" >> "$LOG_FILE" 2>/dev/null
        else
            ERRORS=$((ERRORS+1))
            echo "  ❌ 过滤失败: $file" >> "$LOG_FILE" 2>/dev/null
        fi
        
    done < <(find "$FULL_DIR" -type f \( -name "*.md" -o -name "*.py" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.sh" -o -name "*.txt" \) -print0 2>/dev/null)
done

# 更新状态文件

echo "{" > "$STATE_FILE"
echo "  \"lastScan\": \"$(date '+%Y-%m-%d %H:%M:%S')\"," >> "$STATE_FILE"
echo "  \"total\": $TOTAL," >> "$STATE_FILE"
echo "  \"filtered\": $FILTERED," >> "$STATE_FILE"
echo "  \"skipped\": $SKIPPED," >> "$STATE_FILE"
echo "  \"errors\": $ERRORS" >> "$STATE_FILE"
echo "}" >> "$STATE_FILE"

echo "  统计: 总文件=$TOTAL 过滤=$FILTERED 跳过=$SKIPPED 错误=$ERRORS" >> "$LOG_FILE" 2>/dev/null
echo "" >> "$LOG_FILE" 2>/dev/null

# 如果有过滤结果，提交到 git

if [ "$FILTERED" -gt 0 ]; then
    cd "$WORKSPACE"
    git add -A 2>/dev/null
    git commit -m "🎨 美学过滤自动处理 ($FILTERED 文件)" --allow-empty 2>/dev/null || true
fi

exit 0
