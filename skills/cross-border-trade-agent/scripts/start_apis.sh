#!/bin/bash
# 启动买家情报 REST API
# 三轨接入：REST API / RSS / Agent CLI
# 建议配合 systemd 或 cron @reboot 使用

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="/tmp/buyer_intel_api.pid"
PORT=8100

case "${1:-start}" in
  start)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "✅ 买家情报 API 已在运行 (PID: $(cat $PID_FILE))"
      exit 0
    fi
    echo "🚀 启动买家情报 API → http://0.0.0.0:$PORT"
    nohup python3 "$BASE_DIR/modules/buyer-intel/api_server.py" --port $PORT \
      > "$BASE_DIR/logs/api_server.log" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 1
    if kill -0 $! 2>/dev/null; then
      echo "✅ 已启动 (PID: $!)"
    else
      echo "❌ 启动失败，检查日志: $BASE_DIR/logs/api_server.log"
      exit 1
    fi
    ;;
  stop)
    if [ -f "$PID_FILE" ]; then
      kill $(cat "$PID_FILE") 2>/dev/null
      rm -f "$PID_FILE"
      echo "🛑 已停止"
    else
      echo "ℹ️ 未在运行"
    fi
    ;;
  status)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "✅ 运行中 (PID: $(cat $PID_FILE), 端口: $PORT)"
      curl -s http://localhost:$PORT/health | python3 -m json.tool 2>/dev/null || echo "⚠️ 端口可达但健康检查异常"
    else
      echo "❌ 未运行"
      exit 1
    fi
    ;;
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
  *)
    echo "用法: $0 {start|stop|status|restart}"
    exit 1
    ;;
esac
