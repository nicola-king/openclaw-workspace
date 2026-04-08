#!/bin/bash
# Zhiji-E Cron Job - Polymarket Hot Weather Markets (v5.2)
# Updated: 2026-03-28 13:05 | 改进版：实时热点追踪

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/zhiji-$(date +%Y%m%d).log"
ERROR_LOG="$WORKSPACE/logs/zhiji-error-$(date +%Y%m%d).log"

echo "========================================" >> $LOG_FILE
echo "[$(date)] Start Polymarket Hot Markets Data Collection..." >> $LOG_FILE

# Error Handling
set -e
trap 'echo "[$(date)] ERROR: Task failed at line $LINENO" >> $ERROR_LOG' ERR

# Step 1: Polymarket API - Fetch Top 5 Hot Markets
echo "[$(date)] Step 1: Fetching Polymarket hot markets..." >> $LOG_FILE
cd "$WORKSPACE/skills/zhiji"

python3 polymarket_hot_tracker.py << EOF >> $LOG_FILE 2>&1
Config:
  markets:
    - 2026_hottest_year_rank ($2M liquidity)
    - March_2026_temp_increase ($200K)
    - Cat4_hurricane_before_2027 ($305K)
    - NYC_March_precipitation ($125K)
    - 2026_March_1-3_hottest ($238K)
  interval: 30min
  confidence_threshold: 0.96
  edge_threshold: 0.02
EOF

# Step 2: Strategy Analysis with Real-time Data
echo "[$(date)] Step 2: Running strategy analysis..." >> $LOG_FILE
python3 zhiji_e_v5.py << EOF >> $LOG_FILE 2>&1
Config:
  version: 5.2
  data_source: Polymarket Real-time API
  p0_allocation: 60%
  p1_allocation: 30%
  p2_allocation: 10%
  daily_stop_loss: -10%
  single_market_stop: -20%
  profit_withdraw: 50%
EOF

# Step 3: Generate Report
echo "[$(date)] Step 3: Generating report..." >> $LOG_FILE
python3 generate_report.py --format markdown --output "$WORKSPACE/reports/zhiji-daily-$(date +%Y%m%d).md" >> $LOG_FILE 2>&1

# Step 4: Send Email Report (20:00 only)
if [ $(date +%H) -eq 20 ]; then
    echo "[$(date)] Step 4: Sending daily email report..." >> $LOG_FILE
    bash "$WORKSPACE/scripts/send-cron-notification.sh" "zhiji-daily-$(date +%Y%m%d).md" >> $LOG_FILE 2>&1
fi

# Success
echo "[$(date)] ✓ Polymarket hot markets task completed successfully" >> $LOG_FILE
echo "[$(date)] Log: $LOG_FILE" >> $LOG_FILE
echo "[$(date)] Error Log: $ERROR_LOG" >> $LOG_FILE

exit 0
