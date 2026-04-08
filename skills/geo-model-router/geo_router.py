#!/usr/bin/env python3
"""
Geo-Model Router - 地理感知智能路由 v1.0

核心原则:
1. 国内流量走国内 (直连)
2. 国外流量走代理 (SOCKS5/HTTP)
3. 智能识别智能分流
4. 单独 Skill·自动执行

作者：太一 AGI
创建：2026-04-08
"""

import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# 配置路径
CONFIG_DIR = Path(__file__).parent / "config"
CACHE_DIR = Path(__file__).parent / "cache"


class RouteType(Enum):
    """路由类型"""
    DOMESTIC = "domestic"  # 国内直连
    INTERNATIONAL = "international"  # 国外代理
    UNKNOWN = "unknown"  # 未知


@dataclass
class RouteResult:
    """路由结果"""
    target: str
    route_type: RouteType
    proxy: Optional[str]
    reason: str
    detected_by: str


class GeoRouter:
    """地理感知智能路由器"""
    
    def __init__(self):
        self.config = self.load_config()
        self.cache = self.load_cache()
        
        # 代理配置
        self.proxy_enabled = self.config.get("proxy", {}).get("enabled", True)
        self.proxy_host = self.config.get("proxy", {}).get("host", "127.0.0.1")
        self.proxy_port = self.config.get("proxy", {}).get("port", 7890)
        self.proxy_protocol = self.config.get("proxy", {}).get("protocol", "socks5")
        
        # 加载服务白名单
        self.domestic_services = self.load_service_list("domestic")
        self.international_services = self.load_service_list("international")
        
        print(f"🌍 GeoRouter 初始化完成")
        print(f"   代理：{self.proxy_protocol}://{self.proxy_host}:{self.proxy_port}")
        print(f"   国内服务：{len(self.domestic_services)} 个")
        print(f"   国外服务：{len(self.international_services)} 个")
    
    def load_config(self) -> Dict:
        """加载配置"""
        config_file = CONFIG_DIR / "geo_config.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # 默认配置
        return {
            "proxy": {
                "enabled": True,
                "host": "127.0.0.1",
                "port": 7890,
                "protocol": "socks5"
            },
            "cache": {
                "enabled": True,
                "ttl": 300
            },
            "timeout": {
                "domestic": 10,
                "international": 30,
                "probe": 3
            }
        }
    
    def load_cache(self) -> Dict:
        """加载缓存"""
        cache_file = CACHE_DIR / "geo_cache.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_cache(self):
        """保存缓存"""
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / "geo_cache.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def load_service_list(self, list_type: str) -> Dict[str, Dict]:
        """加载服务白名单"""
        if list_type == "domestic":
            filename = "domestic_services.json"
        else:
            filename = "international_services.json"
        
        config_file = CONFIG_DIR / filename
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 转换为 {domain: route_info} 格式
                services = {}
                for service in data.get("services", []):
                    for domain in service.get("domains", []):
                        services[domain] = {
                            "name": service.get("name", domain),
                            "route": service.get("route", list_type)
                        }
                return services
        
        # 默认服务列表
        if list_type == "domestic":
            return {
                "dashscope.aliyuncs.com": {"name": "阿里百炼", "route": "domestic"},
                "open.bigmodel.cn": {"name": "智谱 AI", "route": "domestic"},
                "qianfan.baidubce.com": {"name": "百度千帆", "route": "domestic"},
                "open.feishu.cn": {"name": "飞书", "route": "domestic"},
                "qyapi.weixin.qq.com": {"name": "企业微信", "route": "domestic"},
                "mp.weixin.qq.com": {"name": "微信公众号", "route": "domestic"},
            }
        else:
            return {
                "api.openai.com": {"name": "OpenAI", "route": "international"},
                "api.anthropic.com": {"name": "Anthropic", "route": "international"},
                "generativelanguage.googleapis.com": {"name": "Google AI", "route": "international"},
                "api.telegram.org": {"name": "Telegram", "route": "international"},
                "api.github.com": {"name": "GitHub", "route": "international"},
            }
    
    def detect_route(self, url: str) -> RouteResult:
        """智能识别路由"""
        # 检查缓存
        now = time.time()
        cache_key = f"route:{url}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if now - cached.get("timestamp", 0) < self.config.get("cache", {}).get("ttl", 300):
                return RouteResult(**cached["data"])
        
        # 解析 URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # 1. 检查域名白名单
        route_info = self.check_whitelist(domain)
        if route_info:
            result = RouteResult(
                target=url,
                route_type=RouteType(route_info["route"]),
                proxy=self.get_proxy_url() if route_info["route"] == "international" else None,
                reason=f"白名单匹配：{route_info['name']}",
                detected_by="whitelist"
            )
            self.save_to_cache(cache_key, result)
            return result
        
        # 2. 检查 TLD
        route_type = self.check_tld(domain)
        if route_type:
            result = RouteResult(
                target=url,
                route_type=route_type,
                proxy=self.get_proxy_url() if route_type == RouteType.INTERNATIONAL else None,
                reason=f"TLD 检测：{domain.split('.')[-1]}",
                detected_by="tld"
            )
            self.save_to_cache(cache_key, result)
            return result
        
        # 3. 智能探测 (可选)
        # 生产环境可实现网络探测
        result = RouteResult(
            target=url,
            route_type=RouteType.INTERNATIONAL,  # 默认国外
            proxy=self.get_proxy_url(),
            reason="默认路由 (未知域名)",
            detected_by="default"
        )
        self.save_to_cache(cache_key, result)
        return result
    
    def check_whitelist(self, domain: str) -> Optional[Dict]:
        """检查白名单"""
        # 精确匹配
        if domain in self.domestic_services:
            return self.domestic_services[domain]
        if domain in self.international_services:
            return self.international_services[domain]
        
        # 后缀匹配
        for service_domain, info in list(self.domestic_services.items()) + list(self.international_services.items()):
            if domain.endswith("." + service_domain) or service_domain.endswith("." + domain):
                return info
        
        return None
    
    def check_tld(self, domain: str) -> Optional[RouteType]:
        """检查 TLD"""
        tld = domain.split(".")[-1]
        
        # 国内 TLD
        if tld in ["cn", "中国", "公司", "网络"]:
            return RouteType.DOMESTIC
        
        # 常见国外 TLD
        if tld in ["com", "org", "net", "io", "ai", "co"]:
            return RouteType.INTERNATIONAL
        
        return None
    
    def get_proxy_url(self) -> Optional[str]:
        """获取代理 URL"""
        if not self.proxy_enabled:
            return None
        
        if self.proxy_protocol == "socks5":
            return f"socks5://{self.proxy_host}:{self.proxy_port}"
        elif self.proxy_protocol == "http":
            return f"http://{self.proxy_host}:{self.proxy_port}"
        else:
            return f"{self.proxy_protocol}://{self.proxy_host}:{self.proxy_port}"
    
    def save_to_cache(self, key: str, result: RouteResult):
        """保存到缓存"""
        if not self.config.get("cache", {}).get("enabled", True):
            return
        
        # 转换为可序列化格式
        data = asdict(result)
        data["route_type"] = result.route_type.value
        
        self.cache[key] = {
            "data": data,
            "timestamp": time.time()
        }
        self.save_cache()
    
    def create_session(self, url: str, **kwargs):
        """创建 HTTP Session (自动配置代理)"""
        import requests
        
        route = self.detect_route(url)
        
        session = requests.Session()
        
        if route.proxy:
            session.proxies = {
                "http": route.proxy,
                "https": route.proxy
            }
            print(f"🌐 {url} → 使用代理：{route.proxy}")
        else:
            print(f"🇨🇳 {url} → 国内直连")
        
        return session
    
    def request(self, url: str, method: str = "GET", **kwargs) -> Dict:
        """发送请求 (自动路由)"""
        import requests
        
        route = self.detect_route(url)
        
        # 配置代理
        proxies = None
        if route.proxy:
            proxies = {
                "http": route.proxy,
                "https": route.proxy
            }
        
        # 发送请求
        try:
            response = requests.request(
                method=method,
                url=url,
                proxies=proxies,
                timeout=kwargs.get("timeout", 30),
                **kwargs
            )
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.text,
                "route_type": route.route_type.value,
                "proxy_used": route.proxy is not None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "route_type": route.route_type.value,
                "proxy_used": route.proxy is not None
            }
    
    def get_status(self) -> Dict:
        """获取路由器状态"""
        return {
            "proxy_enabled": self.proxy_enabled,
            "proxy_url": self.get_proxy_url(),
            "domestic_services": len(self.domestic_services),
            "international_services": len(self.international_services),
            "cache_size": len(self.cache)
        }
    
    def clear_cache(self):
        """清除缓存"""
        self.cache = {}
        self.save_cache()
        print("🗑️ 缓存已清除")


# 快捷函数
def detect_route(url: str) -> RouteResult:
    """快捷检测路由"""
    router = GeoRouter()
    return router.detect_route(url)


def request(url: str, method: str = "GET", **kwargs) -> Dict:
    """快捷发送请求"""
    router = GeoRouter()
    return router.request(url, method, **kwargs)


if __name__ == "__main__":
    # 测试
    router = GeoRouter()
    
    print("\n=== Geo-Model Router v1.0 ===")
    print()
    
    # 测试国内服务
    print("🇨🇳 测试国内服务:")
    test_urls = [
        "https://dashscope.aliyuncs.com/v1/services/aigc/text-generation/generation",
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    ]
    
    for url in test_urls:
        route = router.detect_route(url)
        print(f"   {url}")
        print(f"   → {route.route_type.value} ({route.reason})")
        print()
    
    # 测试国外服务
    print("🌐 测试国外服务:")
    test_urls = [
        "https://api.openai.com/v1/chat/completions",
        "https://api.telegram.org/bot{token}/sendMessage",
        "https://api.github.com/repos/nicola-king/openclaw-workspace"
    ]
    
    for url in test_urls:
        route = router.detect_route(url)
        print(f"   {url}")
        print(f"   → {route.route_type.value} ({route.reason})")
        print()
    
    # 获取状态
    print("📊 路由器状态:")
    status = router.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
