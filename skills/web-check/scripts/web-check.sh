#!/bin/bash
# Web-Check CLI 包装器 — 智能自动化调用
# 用法: bash web-check.sh <host> [module]
# 模块: all|ip|dns|ssl|headers|ports|tech|cookies|location|security|redirects
# 默认: all（完整分析）

REPO_DIR="$(cd "$(dirname "$0")/../repo" && pwd)"
SERVER_URL="http://localhost:3001"
HOST="$1"
MODULE="${2:-all}"

if [ -z "$HOST" ]; then
    echo "用法: bash web-check.sh <host> [module]"
    echo "模块: all(默认), ip, dns, ssl, headers, ports, tech, cookies, location"
    exit 1
fi

# 检查服务是否运行
health_check() {
    curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL/api/status?host=example.com" 2>/dev/null
}

check_and_start() {
    if [ "$(health_check)" != "200" ]; then
        echo "[web-check] ⚠️ 服务未运行，启动中..."
        cd "$REPO_DIR" && PORT=3001 node server.js &
        sleep 3
        if [ "$(health_check)" != "200" ]; then
            echo "[web-check] ❌ 服务启动失败"
            exit 1
        fi
        echo "[web-check] ✅ 服务已启动"
    fi
}

call_api() {
    local endpoint="$1"
    local host="$2"
    local result
    result=$(curl -s "$SERVER_URL/api/$endpoint?host=$host" 2>/dev/null)
    echo "$result"
}

print_header() {
    echo ""
    echo "═══════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════"
}

print_json() {
    echo "$1" | python3 -m json.tool 2>/dev/null || echo "$1"
}

check_and_start

if [ "$MODULE" = "all" ] || [ "$MODULE" = "ip" ]; then
    print_header "🖥️  IP 情报"
    print_json "$(call_api "get-ip" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "dns" ]; then
    print_header "🌐  DNS 记录"
    print_json "$(call_api "dns" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "ssl" ]; then
    print_header "🔐  SSL 证书"
    print_json "$(call_api "ssl" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "headers" ]; then
    print_header "📋  HTTP 头"
    print_json "$(call_api "headers" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "ports" ]; then
    print_header "🔌  端口扫描"
    print_json "$(call_api "ports" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "tech" ]; then
    print_header "🧩  技术栈"
    print_json "$(call_api "tech-stack" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "location" ]; then
    print_header "📍  服务器位置"
    print_json "$(call_api "location" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "cookies" ]; then
    print_header "🍪  Cookies"
    print_json "$(call_api "cookies" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "security" ]; then
    print_header "🛡️  安全头"
    print_json "$(call_api "http-security" "$HOST")"
fi

if [ "$MODULE" = "all" ] || [ "$MODULE" = "redirects" ]; then
    print_header "🔄  重定向链"
    print_json "$(call_api "redirects" "$HOST")"
fi

if [ "$MODULE" = "all" ]; then
    print_header "📸  网站截图"
    echo "截图: http://localhost:3001/api/screenshot?host=$HOST"
    
    print_header "🌱  碳排放"
    print_json "$(call_api "carbon" "$HOST")"
fi

echo ""
echo "✅ Web-Check 分析完成: $HOST"
