#!/bin/bash
# Gemini CLI 包装脚本 — 带限流检查 + 自动重试 + 配额管理
# 调用方式：bash gemini-cli.sh -p "你的问题"
# 遵守：60req/min, 1000req/day -> 实际上限 80%: 48req/min, 800req/day

# 加载环境变量
# GEMINI_API_KEY 从 bashrc 或已配置的 session 继承
export GEMINI_CLI_TRUST_WORKSPACE=true

# 如果 API Key 未设置，尝试从 bashrc 读取
if [ -z "$GEMINI_API_KEY" ]; then
    GEMINI_API_KEY=$(grep '^export GEMINI_API_KEY=' ~/.bashrc 2>/dev/null | head -1 | cut -d'"' -f2)
    [ -n "$GEMINI_API_KEY" ] && export GEMINI_API_KEY
fi

USAGE_FILE="$HOME/.gemini-cli-usage.json"
MAX_DAY=800        # 每日上限（留 20% 余量）
MAX_MINUTE=48      # 每分钟上限（留 20% 余量）
MODEL="gemini-2.5-flash"

# 初始化使用记录
init_usage() {
    local today
    today=$(date +%Y-%m-%d)
    if [ ! -f "$USAGE_FILE" ]; then
        echo "{\"date\":\"$today\",\"day_count\":0,\"timestamps\":[]}" > "$USAGE_FILE"
    fi
    # 检查日期是否已切换
    local saved_date
    saved_date=$(python3 -c "import json; print(json.load(open('$USAGE_FILE'))['date'])" 2>/dev/null)
    if [ "$saved_date" != "$today" ]; then
        echo "{\"date\":\"$today\",\"day_count\":0,\"timestamps\":[]}" > "$USAGE_FILE"
    fi
}

# 限流检查
check_limits() {
    local now day_count recent_count
    now=$(date +%s)
    day_count=$(python3 -c "import json; print(json.load(open('$USAGE_FILE'))['day_count'])" 2>/dev/null || echo 0)
    
    # 每日限额检查
    if [ "$day_count" -ge "$MAX_DAY" ]; then
        echo "[GEMINI-LIMIT] ⛔ 今日已用 $day_count 次，超上限 $MAX_DAY。切换 DeepSeek 处理。" >&2
        return 1
    fi
    
    # 每分钟限额检查（最近 60s 内的调用数）
    recent_count=$(python3 -c "
import json, time
data = json.load(open('$USAGE_FILE'))
cutoff = time.time() - 60
count = sum(1 for t in data.get('timestamps', []) if t > cutoff)
print(count)
" 2>/dev/null || echo 0)
    
    if [ "$recent_count" -ge "$MAX_MINUTE" ]; then
        echo "[GEMINI-LIMIT] ⏳ 最近 60s 已调用 $recent_count 次，等待中..." >&2
        sleep 5
        # 递归检查
        check_limits
        return $?
    fi
    
    return 0
}

# 记录调用
record_call() {
    local status="$1"
    python3 -c "
import json, time
data = json.load(open('$USAGE_FILE'))
data['day_count'] += 1
data['timestamps'].append(time.time())
# 只保留最近 5 分钟的时间戳
cutoff = time.time() - 300
data['timestamps'] = [t for t in data['timestamps'] if t > cutoff]
json.dump(data, open('$USAGE_FILE','w'))
" 2>/dev/null
}

# 调用 Gemini CLI（带自动重试）
call_gemini() {
    local prompt="$1"
    local max_retries=2
    local retry_delay=3
    local attempt=1
    
    while [ $attempt -le $max_retries ]; do
        # 捕获 stdout（JSON）+ stderr（日志）
        result=$(gemini -m "$MODEL" -p "$prompt" --output-format json 2>/dev/null)
        local exit_code=$?
        
        if [ $exit_code -eq 0 ] && [ -n "$result" ]; then
            # 提取 response 字段
            local response
            response=$(echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    resp = data.get('response', '')
    if resp:
        print(resp)
    else:
        print('(empty response)')
except Exception as e:
    print(f'(parse error: {e})')
" 2>/dev/null)
            echo "$response"
            return 0
        fi
        
        # 检查是否是 503（高负载）
        if echo "$result" | grep -q "503\|UNAVAILABLE\|429\|too many requests" 2>/dev/null; then
            echo "[GEMINI-RETRY] ⚠️ 第 $attempt 次失败（服务不可用），${retry_delay}s 后重试..." >&2
            sleep $retry_delay
            retry_delay=$((retry_delay * 2))
            attempt=$((attempt + 1))
        else
            # 其他错误，不重试
            echo "[GEMINI-ERROR] ❌ 调用失败 (exit=$exit_code)" >&2
            return 1
        fi
    done
    
    echo "[GEMINI-ERROR] ❌ 重试 $max_retries 次后仍然失败" >&2
    return 1
}

# 主流程
main() {
    init_usage
    
    # 解析参数
    local prompt=""
    while getopts "p:m:h" opt; do
        case $opt in
            p) prompt="$OPTARG" ;;
            m) MODEL="$OPTARG" ;;
            h)
                echo "用法: gemini-cli.sh -p <prompt> [-m <model>]"
                echo "  默认模型: gemini-2.5-flash"
                exit 0
                ;;
            *) 
                echo "无效参数"
                exit 1
                ;;
        esac
    done
    
    if [ -z "$prompt" ]; then
        echo "[GEMINI-ERROR] ❌ 必须指定 -p 参数" >&2
        exit 1
    fi
    
    # 限流检查
    if ! check_limits; then
        exit 1
    fi
    
    # 调用
    if call_gemini "$prompt"; then
        record_call "success"
        echo "[GEMINI-OK] ✅ 调用成功" >&2
    else
        echo "[GEMINI-OK] ⛔ 调用失败，回退 DeepSeek" >&2
        exit 1
    fi
}

main "$@"
