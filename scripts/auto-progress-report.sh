#!/bin/bash
# 自动进度汇报脚本 v3 - 使用 Python 调用 message tool
# 每 5 分钟自动发送进度更新到微信

WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
PROGRESS_FILE="/tmp/cli-progress.json"
LOG_FILE="$LOG_DIR/progress-report.log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "自动进度汇报 v3 启动"

while true; do
    if [ -f "$PROGRESS_FILE" ]; then
        # 读取进度数据
        PERCENT=$(grep -o '"percent":[0-9]*' "$PROGRESS_FILE" | cut -d: -f2)
        STEP=$(grep -o '"step":"[^"]*"' "$PROGRESS_FILE" | cut -d'"' -f4)
        STATUS=$(grep -o '"status":"[^"]*"' "$PROGRESS_FILE" | cut -d'"' -f4)
        ELAPSED=$(grep -o '"elapsed_minutes":[0-9]*' "$PROGRESS_FILE" | cut -d: -f2)
        
        # 生成进度条
        FILLED=$((PERCENT / 5))
        EMPTY=$((20 - FILLED))
        BAR=""
        for i in $(seq 1 $FILLED); do BAR+="█"; done
        for i in $(seq 1 $EMPTY); do BAR+="░"; done
        
        # 生成消息
        MSG="CLI-Anything 进度 ${PERCENT}% | ${STEP} | ${STATUS} | 已用${ELAPSED}分钟 | 下次汇报：$(( $(date +%s) + 300 ))"
        
        # 使用 Python 调用 openclaw message
        python3 << PYEOF
import subprocess
import json

msg = """$MSG"""
target = "o9cq80-xCy8pt54Dz3jqOJHAgVZ8@im.wechat"

# 调用 openclaw message send
cmd = [
    "openclaw", "message", "send",
    "--channel", "openclaw-weixin",
    "--target", target,
    "--message", msg
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print("SUCCESS")
    else:
        print(f"FAILED: {result.stderr}")
except Exception as e:
    print(f"ERROR: {e}")
PYEOF
        
        log "进度汇报：$PERCENT%"
    else
        log "进度文件不存在"
    fi
    
    # 等待 5 分钟
    sleep 300
done
