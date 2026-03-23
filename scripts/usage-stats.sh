#!/bin/bash
# 太一用量统计脚本
# 用法：./usage-stats.sh [days]

DAYS=${1:-7}
SESSION_DIR="/home/nicola/.openclaw/agents/taiyi/sessions"

echo "📊 太一模型用量统计 (过去 $DAYS 天)"
echo "================================"
echo ""

# 查找最近的 session 文件
find "$SESSION_DIR" -name "*.jsonl" -mtime -$DAYS | while read file; do
    # 提取 usage 数据 (如果有)
    INPUT=$(grep -o '"input":[0-9]*' "$file" | awk -F: '{sum+=$2} END {print sum+0}')
    OUTPUT=$(grep -o '"output":[0-9]*' "$file" | awk -F: '{sum+=$2} END {print sum+0}')
    TOTAL=$((INPUT + OUTPUT))
    
    if [ $TOTAL -gt 0 ]; then
        BASENAME=$(basename "$file")
        echo "📄 $BASENAME"
        echo "   输入：$INPUT tokens | 输出：$OUTPUT tokens | 合计：$TOTAL tokens"
    fi
done

echo ""
echo "💰 成本估算 (qwen3.5-plus: ¥0.004/1K 输入，¥0.012/1K 输出)"
echo "   注：日志中 usage 数据可能不完整，以阿里云后台为准"
echo ""
echo "🔗 阿里云百炼控制台：https://bailian.console.aliyun.com/"
