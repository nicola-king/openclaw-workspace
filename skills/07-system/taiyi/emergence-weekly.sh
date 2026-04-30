#!/bin/bash
# 能力涌现每周触发脚本
# 触发条件：每周一 09:00 自动执行

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/emergence-weekly.log"
REPORT_DIR="$WORKSPACE/reports/emergence"

echo "========================================" >> $LOG_FILE
echo "[$(date)] 开始能力涌现周任务..." >> $LOG_FILE

# 创建周报目录
mkdir -p "$REPORT_DIR/$(date +%Y-W%V)"
cd "$REPORT_DIR/$(date +%Y-W%V)"

# 启动能力涌现流程
echo "[$(date)] 启动能力涌现 6 步流程..." >> $LOG_FILE

# Step 1: 全网搜索
echo "🔍 Step 1/6: 全网穿透性搜索..." >> $LOG_FILE
python3 "$WORKSPACE/skills/taiyi/emergence-search.py" --week $(date +%Y-W%V) >> $LOG_FILE 2>&1

# Step 2: 技术蒸馏
echo "🔬 Step 2/6: 技术蒸馏..." >> $LOG_FILE
python3 "$WORKSPACE/skills/taiyi/emergence-distill.py" --week $(date +%Y-W%V) >> $LOG_FILE 2>&1

# Step 3: 比对分析
echo "📊 Step 3/6: 比对分析..." >> $LOG_FILE
python3 "$WORKSPACE/skills/taiyi/emergence-compare.py" --week $(date +%Y-W%V) >> $LOG_FILE 2>&1

# Step 4: 风险评估
echo "⚖️ Step 4/6: 知识产权风险评估..." >> $LOG_FILE
python3 "$WORKSPACE/skills/taiyi/emergence-risk-assessment.py" --week $(date +%Y-W%V) >> $LOG_FILE 2>&1

# Step 5: 评估决策
echo "🎯 Step 5/6: 评估决策..." >> $LOG_FILE
python3 "$WORKSPACE/skills/taiyi/emergence-decision.py" --week $(date +%Y-W%V) >> $LOG_FILE 2>&1

# Step 6: 上架发布 (如决策通过)
echo "🚀 Step 6/6: 上架发布..." >> $LOG_FILE
python3 "$WORKSPACE/skills/taiyi/emergence-publish.py" --week $(date +%Y-W%V) >> $LOG_FILE 2>&1

echo "[$(date)] ✓ 能力涌现周任务完成" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

# 发送 Telegram 通知
echo "📱 发送 Telegram 通知..." >> $LOG_FILE
curl -s "https://api.telegram.org/bot8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY/sendMessage" \
  -d "chat_id=7073481596" \
  -d "text=🦞 能力涌现周报

周次：$(date +%Y-W%V)
状态：✅ 完成
报告：$REPORT_DIR/$(date +%Y-W%V)/

详情查看日志：$LOG_FILE" >> $LOG_FILE 2>&1

echo "✅ 能力涌现周报完成"
