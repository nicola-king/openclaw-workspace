#!/usr/bin/env bash
# 太一跨境贸易 Bot 启动器 (V3 - file credential source)
set -euo pipefail

HANDLER="$HOME/.openclaw/workspace/scripts/lark-bot-handler.py"
LARK_CLI="$HOME/.npm-global/bin/lark-cli"
LOG_DIR="$HOME/.openclaw/workspace/logs"

mkdir -p "$LOG_DIR"

echo "[lark-bot] 启动太一跨境贸易 Bot 事件消费..."

# 启动事件消费者，使用 --timeout 0 表示永不超时
# 用 < <(tail -f /dev/null) 保持 stdin 打开
$LARK_CLI event consume im.message.receive_v1 --as bot --timeout 0 \
  < <(tail -f /dev/null) \
  | python3 "$HANDLER" >> "$LOG_DIR/lark-bot-handler.log" 2>&1

RC=$?
echo "[lark-bot] 进程退出, code=$RC"
exit $RC
