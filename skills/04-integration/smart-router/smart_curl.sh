#!/bin/bash
# 智能 curl 封装 - 自动选择直连/代理
# 使用：source smart_curl.sh && smart_curl "https://api.weixin.qq.com/..."

# 检测目标服务并设置代理
detect_and_set_proxy() {
    local url="$1"
    
    case "$url" in
        # 国内服务 - 直连
        *api.weixin.qq.com*|*mp.weixin.qq.com*|*qyapi.weixin.qq.com*)
            unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
            export CURL_PROXY=""
            echo -n "🇨🇳 "
            ;;
        *open.feishu.cn*|*api.feishu.cn*|*feishu.cn*)
            unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
            export CURL_PROXY=""
            echo -n "🇨🇳 "
            ;;
        *aliyuncs.com*|*aliyun.com*)
            unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
            export CURL_PROXY=""
            echo -n "🇨🇳 "
            ;;
        # 海外服务 - 代理
        *telegram.org*|*telegram.me*)
            export HTTP_PROXY="http://127.0.0.1:7890"
            export HTTPS_PROXY="http://127.0.0.1:7890"
            export http_proxy="http://127.0.0.1:7890"
            export https_proxy="http://127.0.0.1:7890"
            export CURL_PROXY="--proxy http://127.0.0.1:7890"
            echo -n "🌐 "
            ;;
        *googleapis.com*|*googleapi.com*)
            export HTTP_PROXY="http://127.0.0.1:7890"
            export HTTPS_PROXY="http://127.0.0.1:7890"
            export http_proxy="http://127.0.0.1:7890"
            export https_proxy="http://127.0.0.1:7890"
            export CURL_PROXY="--proxy http://127.0.0.1:7890"
            echo -n "🌐 "
            ;;
        *github.com*|*openai.com*|*anthropic.com*)
            export HTTP_PROXY="http://127.0.0.1:7890"
            export HTTPS_PROXY="http://127.0.0.1:7890"
            export http_proxy="http://127.0.0.1:7890"
            export https_proxy="http://127.0.0.1:7890"
            export CURL_PROXY="--proxy http://127.0.0.1:7890"
            echo -n "🌐 "
            ;;
        *)
            # 默认使用代理
            export HTTP_PROXY="http://127.0.0.1:7890"
            export HTTPS_PROXY="http://127.0.0.1:7890"
            export http_proxy="http://127.0.0.1:7890"
            export https_proxy="http://127.0.0.1:7890"
            export CURL_PROXY="--proxy http://127.0.0.1:7890"
            echo -n "🌐 "
            ;;
    esac
}

# 智能 curl 函数
smart_curl() {
    local url="$1"
    shift
    
    detect_and_set_proxy "$url"
    
    echo "$url"
    
    if [ -n "$CURL_PROXY" ]; then
        curl $CURL_PROXY "$@" "$url"
    else
        curl "$@" "$url"
    fi
}

# 测试函数
test_smart_curl() {
    echo "=========================================="
    echo "🧪 智能 curl 测试"
    echo "=========================================="
    echo ""
    
    echo "1. 微信 API (应直连):"
    smart_curl "https://api.weixin.qq.com/" -I -s -o /dev/null -w "HTTP 状态：%{http_code}\n"
    
    echo ""
    echo "2. 飞书 API (应直连):"
    smart_curl "https://open.feishu.cn/" -I -s -o /dev/null -w "HTTP 状态：%{http_code}\n"
    
    echo ""
    echo "3. Telegram API (应代理):"
    smart_curl "https://api.telegram.org/" -I -s -o /dev/null -w "HTTP 状态：%{http_code}\n"
    
    echo ""
    echo "=========================================="
}

# 如果直接执行则运行测试
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    test_smart_curl
fi
