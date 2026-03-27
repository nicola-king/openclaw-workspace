#!/bin/bash
# 任务执行确认通知脚本
# 功能：任务执行后发送微信通知

LOG_DIR="$HOME/.openclaw/workspace/logs"
NOTIFY_LOG="$LOG_DIR/task-notify.log"
WECHAT_LOG="$LOG_DIR/wechat.log"

# 参数：$1=Bot 名称，$2=任务名称，$3=状态 (success/failed)，$4=详情
bot=$1
task=$2
status=$3
detail=$4

timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# 生成通知消息
if [ "$status" = "success" ]; then
    emoji="✅"
    title="任务完成"
else
    emoji="❌"
    title="任务失败"
fi

message="$emoji【$bot · $task】$title
时间：$timestamp
状态：$status
详情：$detail"

# 记录通知日志
echo "[$timestamp] $message" >> "$NOTIFY_LOG"

# 输出到微信日志（Gateway 会读取）
echo "[$timestamp] $message" >> "$WECHAT_LOG"

# 输出到标准输出
echo "$message"
