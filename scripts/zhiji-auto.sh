#!/bin/bash
# 知几-E 24 小时自动化脚本
# 每 5 分钟执行一次，监控市场机会
# 安全增强：随机延迟 + 限速

set -e

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/zhiji-$(date +%Y%m%d).log"
PROXY="http://127.0.0.1:7890"

# 随机延迟 0-30 秒（避免并发，快速响应）
DELAY=$((RANDOM % 30))
echo "[$(date)] 随机延迟 ${DELAY}秒..." >> $LOG_FILE
sleep $DELAY

echo "[$(date)] 知几-E 自动检查开始..." >> $LOG_FILE

# 设置代理环境变量
export http_proxy=$PROXY
export https_proxy=$PROXY

# 1. 检查气象数据
cd $WORKSPACE/polymarket-data
python3 -c "from db_connector import get_stats; print(get_stats())" >> $LOG_FILE 2>&1

# 2. 运行策略分析
cd $WORKSPACE/skills/zhiji
python3 -c "
from strategy_v21 import ZhijiE_v21
import json
from datetime import datetime

engine = ZhijiE_v21()

# 模拟数据（实际应从数据库读取）
weather_data = {
    'noaa': {'temp': 25, 'precip': 0.3},
    'wmo': {'temp': 24, 'precip': 0.35}
}

market_data = {
    'rain_tomorrow': 2.5,
    'temp_above_25': 1.8
}

result = engine.execute(weather_data, market_data)
print(f'[{datetime.now()}] 策略分析：{json.dumps(result)}')
" >> $LOG_FILE 2>&1

# 3. 记录状态
echo "[$(date)] 知几-E 自动检查完成" >> $LOG_FILE
