#!/bin/bash
# html-anything 本地服务启动脚本
DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${1:-3777}"
cd "$DIR"
exec npx next start -p "$PORT"
