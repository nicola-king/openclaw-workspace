#!/bin/bash
# feedgrab 测试脚本
# 用途：测试 X/Twitter 热点抓取

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/feedgrab-test.log"

echo "[$(date)] 开始测试 feedgrab..." >> $LOG_FILE

# 测试 1: CLI 方式
echo "[$(date)] 测试 CLI 方式..." >> $LOG_FILE
# feedgrab twitter --keyword "Polymarket" --output markdown >> $LOG_FILE 2>&1

# 测试 2: Python 库方式
echo "[$(date)] 测试 Python 库方式..." >> $LOG_FILE
python3 << 'PYEOF' >> $LOG_FILE 2>&1
try:
    import feedgrab
    print("✅ feedgrab 库导入成功")
except ImportError as e:
    print(f"🟡 feedgrab 库导入失败：{e}")
PYEOF

echo "[$(date)] 测试完成" >> $LOG_FILE
cat $LOG_FILE
