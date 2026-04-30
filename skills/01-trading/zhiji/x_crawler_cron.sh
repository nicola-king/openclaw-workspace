#!/bin/bash
# X 社交媒体爬虫定时任务脚本
# 用途：每小时爬取币安广场数据，生成交易信号

set -e

# 加载环境变量
source /home/nicola/.openclaw/load-env.sh

# 日志文件
LOG_FILE="/home/nicola/.openclaw/workspace/logs/x_crawler_cron.log"

# 时间戳
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] ️ 开始执行 X 社交媒体爬虫..." | tee -a "$LOG_FILE"

# 运行爬虫
cd /home/nicola/.openclaw/workspace
python3 skills/01-trading/zhiji/x_social_crawler.py >> "$LOG_FILE" 2>&1

# 检查执行结果
if [ $? -eq 0 ]; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] ✅ 爬虫执行成功" | tee -a "$LOG_FILE"
    
    # 检查是否有新的交易信号
    LATEST_SIGNALS="/home/nicola/.openclaw/workspace/data/x-social-crawler/latest_trading_signals.json"
    if [ -f "$LATEST_SIGNALS" ]; then
        SIGNAL_COUNT=$(python3 -c "import json; print(len(json.load(open('$LATEST_SIGNALS'))))" 2>/dev/null || echo "0")
        if [ "$SIGNAL_COUNT" -gt "0" ]; then
            echo "[$TIMESTAMP] 🎯 发现 $SIGNAL_COUNT 个交易信号！" | tee -a "$LOG_FILE"
            # 这里可以添加 Telegram 通知
        fi
    fi
else
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] ❌ 爬虫执行失败！" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
