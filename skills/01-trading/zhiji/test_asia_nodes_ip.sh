#!/bin/bash
# 亚洲节点 IP 测试脚本
# 测试日本 W01/W02/W03 + 新加坡 W01 的出口 IP

echo "========================================"
echo "亚洲节点 IP 测试"
echo "目标：日本 W01/W02/W03 + 新加坡 W01"
echo "========================================"
echo ""

# Clash API
CLASH_API="http://127.0.0.1:9090"

# 节点列表
declare -A NODES=(
    ["🇯🇵 日本 W01 | IEPL"]="🇯🇵 日本 W01 | IEPL"
    ["🇯🇵 日本 W02 | IEPL"]="🇯🇵 日本 W02 | IEPL"
    ["🇯🇵 日本 W03 | IEPL"]="🇯🇵 日本 W03 | IEPL"
    ["🇸🇬 新加坡 W01 | IEPL"]="🇸🇬 新加坡 W01 | IEPL | x2"
)

# 测试结果
declare -A RESULTS

echo "⚠️  注意：需要手动在 Clash 管理器中选择节点"
echo ""
echo "步骤:"
echo "1. 访问：http://localhost:9090/ui"
echo "2. 选择 Proxy 标签"
echo "3. 手动选择每个节点"
echo "4. 运行此脚本测试 IP"
echo ""
echo "或者使用自动切换功能 (如果支持)"
echo ""

# 测试函数
test_node() {
    local node_name="$1"
    local node_id="$2"
    
    echo "----------------------------------------"
    echo "测试节点：$node_name"
    echo "----------------------------------------"
    
    # 尝试切换节点 (需要 Clash API 支持)
    # curl -s -X PUT "$CLASH_API/proxies/🚀 自动选择" -d "{\"name\":\"$node_id\"}"
    
    echo "请在 Clash 管理器中选择：$node_name"
    echo "按回车键继续测试..."
    read
    
    # 测试 5 次 IP
    echo "测试出口 IP (5 次):"
    local ips=()
    for i in $(seq 1 5); do
        ip=$(curl -s -x http://127.0.0.1:7890 https://api.ipify.org 2>/dev/null)
        echo "  测试 $i: $ip"
        ips+=("$ip")
        sleep 0.5
    done
    
    # 测试延迟
    echo ""
    echo "测试延迟:"
    latency=$(curl -s -o /dev/null -w "%{time_total}s" -x http://127.0.0.1:7890 https://api.binance.com 2>/dev/null)
    echo "  币安 API 延迟：$latency"
    
    # 检查 IP 是否固定
    echo ""
    unique_ips=$(printf "%s\n" "${ips[@]}" | sort -u | wc -l)
    if [ "$unique_ips" -eq 1 ]; then
        echo "✅ IP 固定：${ips[0]}"
        RESULTS["$node_name"]="${ips[0]}"
    else
        echo "⚠️  IP 不固定 (发现 $unique_ips 个不同 IP)"
        printf '%s\n' "${ips[@]}" | sort -u
        RESULTS["$node_name"]="不固定"
    fi
    
    echo ""
}

# 主测试
echo "========================================"
echo "开始测试"
echo "========================================"
echo ""

for node_name in "${!NODES[@]}"; do
    node_id="${NODES[$node_name]}"
    test_node "$node_name" "$node_id"
done

# 输出结果
echo "========================================"
echo "测试结果汇总"
echo "========================================"
echo ""

for node_name in "${!RESULTS[@]}"; do
    ip="${RESULTS[$node_name]}"
    if [ "$ip" != "不固定" ]; then
        echo "✅ $node_name: $ip"
    else
        echo "⚠️  $node_name: IP 不固定"
    fi
done

echo ""
echo "========================================"
echo "币安 IP 白名单配置建议"
echo "========================================"
echo ""
echo "在币安后台添加以下 IP:"
echo ""

for node_name in "${!RESULTS[@]}"; do
    ip="${RESULTS[$node_name]}"
    if [ "$ip" != "不固定" ]; then
        echo "$node_name: $ip"
    fi
done

echo ""
echo "或者添加 IP 段 (如果连续):"
echo "x.x.x.0/24"
echo ""
echo "========================================"
