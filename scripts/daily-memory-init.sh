#!/bin/bash
# 每日 memory 文件预创建脚本
# 在 03:00 之前运行，确保 daily memory 文件存在
# 避免 Git 备份等 cron 的 edit 操作因 ENOENT 失败

MEMORY_DIR="/home/sayelf/.openclaw/workspace/memory"
DATE=$(date +%Y-%m-%d)
FILE="$MEMORY_DIR/$DATE.md"

if [ ! -f "$FILE" ]; then
    echo "# $DATE 日志" > "$FILE"
    echo "" >> "$FILE"
    echo "已创建 $FILE"
else
    echo "$FILE 已存在，跳过"
fi
