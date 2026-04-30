#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能 HTTP 适配器 - 自动选择直连/代理

功能:
- 根据目标域名自动选择是否使用代理
- 支持飞书/微信/Telegram 等服务的智能分流
- 无缝集成 requests 库

使用示例:
    from smart_http_adapter import smart_get, smart_post
    
    # 微信 API (自动直连)
    response = smart_get("https://api.weixin.qq.com/...")
    
    # Telegram API (自动代理)
    response = smart_post("https://api.telegram.org/...")
"""

import requests
from typing import Dict, Optional, Set
from urllib.parse import urlparse
import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SmartHTTP')

# ========== 配置区域 ==========

# 国内服务白名单 (直连)
DIRECT_DOMAINS: Set[str] = {
    # 微信
    "api.weixin.qq.com",
    "mp.weixin.qq.com",
    "qyapi.weixin.qq.com",
    "weixin.qq.com",
    "wechat.com",
    
    # 飞书
    "open.feishu.cn",
    "api.feishu.cn",
    "feishu.cn",
    "feishucdn.com",
    "bytedance.com",
    
    # 阿里云 (国内服务)
    "dashscope.aliyuncs.com",
    "aliyun.com",
    "aliyuncs.com",
    
    # 腾讯云
    "tencent.com",
    "qq.com",
    
    # 国内 CDN
    "bdstatic.com",
    "tbcdn.cn",
}

# 海外服务名单 (强制代理)
PROXY_DOMAINS: Set[str] = {
    # Telegram
    "api.telegram.org",
    "telegram.org",
    "telegram.me",
    
    # Google
    "googleapis.com",
    "googleapi.com",
    "google.com",
    "youtube.com",
    
    # GitHub
    "github.com",
    "api.github.com",
    "raw.githubusercontent.com",
    
    # AI API
    "openai.com",
    "api.openai.com",
    "anthropic.com",
    "api.anthropic.com",
    "perplexity.ai",
    "api.perplexity.ai",
    
    # 其他海外服务
    "notion.so",
    "api.notion.com",
    "slack.com",
    "api.slack.com",
}

# 代理配置
PROXY_CONFIG = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

# 国内 IP 段 (直连)
CN_IP_PREFIXES = (
    "127.",  # localhost
    "192.168.",  # 内网
    "10.",  # 内网
    "172.16.",  # 内网
    "172.17.",
    "172.18.",
    "172.19.",
    "172.20.",
    "172.21.",
    "172.22.",
    "172.23.",
    "172.24.",
    "172.25.",
    "172.26.",
    "172.27.",
    "172.28.",
    "172.29.",
    "172.30.",
    "172.31.",
    "100.64.",  # CGNAT
    "17.0.",  # Apple
)

# ========== 核心功能 ==========


def should_use_proxy(url: str) -> bool:
    """
    判断是否需要使用代理
    
    Args:
        url: 目标 URL
        
    Returns:
        bool: True=使用代理，False=直连
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.split(":")[0].lower()
        
        # 1. 检查是否在强制代理名单
        if domain in PROXY_DOMAINS:
            logger.debug(f"🌐 强制代理：{domain}")
            return True
        
        # 2. 检查是否在直连白名单
        if domain in DIRECT_DOMAINS:
            logger.debug(f"🇨🇳 直连白名单：{domain}")
            return False
        
        # 3. 检查域名后缀匹配
        for proxy_domain in PROXY_DOMAINS:
            if domain.endswith(f".{proxy_domain}"):
                logger.debug(f"🌐 代理 (后缀匹配): {domain}")
                return True
        
        for direct_domain in DIRECT_DOMAINS:
            if domain.endswith(f".{direct_domain}"):
                logger.debug(f"🇨🇳 直连 (后缀匹配): {domain}")
                return False
        
        # 4. 检查是否为国内 IP
        try:
            ip = socket.gethostbyname(domain)
            if ip.startswith(CN_IP_PREFIXES):
                logger.debug(f"🇨🇳 直连 (国内 IP): {domain} → {ip}")
                return False
        except socket.gaierror:
            logger.debug(f"⚠️  DNS 解析失败：{domain}")
            pass
        
        # 5. 默认使用代理 (安全优先)
        logger.debug(f"🌐 默认代理：{domain}")
        return True
        
    except Exception as e:
        logger.error(f"❌ 判断失败：{url} - {e}")
        return True  # 失败时默认使用代理


def get_proxies(url: str) -> Optional[Dict[str, str]]:
    """
    获取代理配置
    
    Args:
        url: 目标 URL
        
    Returns:
        dict or None: 代理配置或 None(直连)
    """
    if should_use_proxy(url):
        return PROXY_CONFIG
    return None


def smart_request(method: str, url: str, **kwargs) -> requests.Response:
    """
    智能 HTTP 请求
    
    Args:
        method: HTTP 方法 (GET/POST/PUT/DELETE)
        url: 目标 URL
        **kwargs: 传递给 requests 的其他参数
        
    Returns:
        requests.Response: 响应对象
    """
    proxies = get_proxies(url)
    mode = "🌐 代理" if proxies else "🇨🇳 直连"
    
    logger.info(f"{mode} → {method} {url}")
    
    # 执行请求
    session = kwargs.pop('session', None)
    if session:
        response = session.request(method, url, proxies=proxies, **kwargs)
    else:
        response = requests.request(method, url, proxies=proxies, **kwargs)
    
    return response


def smart_get(url: str, **kwargs) -> requests.Response:
    """智能 GET 请求"""
    return smart_request("GET", url, **kwargs)


def smart_post(url: str, **kwargs) -> requests.Response:
    """智能 POST 请求"""
    return smart_request("POST", url, **kwargs)


def smart_put(url: str, **kwargs) -> requests.Response:
    """智能 PUT 请求"""
    return smart_request("PUT", url, **kwargs)


def smart_delete(url: str, **kwargs) -> requests.Response:
    """智能 DELETE 请求"""
    return smart_request("DELETE", url, **kwargs)


# ========== 测试功能 ==========


def run_tests():
    """运行测试"""
    print("\n" + "=" * 70)
    print("🧪 智能 HTTP 适配器测试")
    print("=" * 70 + "\n")
    
    test_cases = [
        # (URL, 预期结果)
        ("https://api.weixin.qq.com/cgi-bin/token", "🇨🇳 直连"),
        ("https://mp.weixin.qq.com/cgi-bin/home", "🇨🇳 直连"),
        ("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", "🇨🇳 直连"),
        ("https://api.feishu.cn/v1/users", "🇨🇳 直连"),
        ("https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generate", "🇨🇳 直连"),
        ("https://api.telegram.org/bot123/getMe", "🌐 代理"),
        ("https://www.googleapis.com/oauth2/v4/token", "🌐 代理"),
        ("https://api.github.com/repos/test/test", "🌐 代理"),
        ("https://api.openai.com/v1/models", "🌐 代理"),
        ("https://api.anthropic.com/v1/messages", "🌐 代理"),
        ("https://api.perplexity.ai/chat/completions", "🌐 代理"),
    ]
    
    passed = 0
    failed = 0
    
    for url, expected in test_cases:
        result = "🌐 代理" if should_use_proxy(url) else "🇨🇳 直连"
        status = "✅" if result == expected else "❌"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {result:8} | {url[:60]}")
    
    print("\n" + "=" * 70)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 70 + "\n")
    
    return failed == 0


# ========== 主函数 ==========


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = run_tests()
        sys.exit(0 if success else 1)
    else:
        # 交互模式
        print("智能 HTTP 适配器 - 交互模式")
        print("输入 URL 测试分流规则 (输入 q 退出)\n")
        
        while True:
            try:
                url = input("URL > ").strip()
                if url.lower() in ("q", "quit", "exit"):
                    break
                
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
                
                use_proxy = should_use_proxy(url)
                mode = "🌐 代理" if use_proxy else "🇨🇳 直连"
                proxies = get_proxies(url)
                
                print(f"  模式：{mode}")
                if proxies:
                    print(f"  代理：{proxies['https']}")
                else:
                    print(f"  代理：无 (直连)")
                print()
                
            except KeyboardInterrupt:
                print("\n再见！")
                break
            except Exception as e:
                print(f"  错误：{e}\n")
