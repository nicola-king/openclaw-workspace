#!/bin/bash
# O.E.R.V Silent Operator — 自媒体一人公司
# 自动启动分发服务器 + 保活

SKILL_DIR="/home/sayelf/.openclaw/workspace/skills/oerv-narrative-engine"
PID_FILE="/tmp/oerv_dispatch.pid"
LOG_DIR="$SKILL_DIR/logs"
mkdir -p "$LOG_DIR"

VENV_PYTHON="$SKILL_DIR/.venv/bin/python3"
PYTHON="${VENV_PYTHON:-python3}"

case "${1:-status}" in
  start)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      exit 0
    fi
    nohup $PYTHON "$SKILL_DIR/dispatch.py" --port 5200 \
      > "$LOG_DIR/dispatch.log" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 1
    if kill -0 $! 2>/dev/null; then
      echo "OERV dispatch: started (PID $!)"
    else
      echo "OERV dispatch: FAILED"
      exit 1
    fi
    ;;
  stop)
    [ -f "$PID_FILE" ] && kill $(cat "$PID_FILE") 2>/dev/null && rm -f "$PID_FILE"
    echo "OERV dispatch: stopped"
    ;;
  status)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "OERV dispatch: running (PID $(cat $PID_FILE))"
      curl -s http://localhost:5200/health 2>/dev/null || echo "(port check pending)"
      exit 0
    else
      echo "OERV dispatch: not running"
      exit 1
    fi
    ;;
  restart)
    $0 stop; sleep 1; $0 start
    ;;
  *)
    echo "Usage: $0 {start|stop|status|restart}"
    exit 1
    ;;
esac
