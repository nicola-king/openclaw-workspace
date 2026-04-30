#!/usr/bin/env python3
"""
Multi-Channel Geo Router - 多通道地理感知路由 v2.0

核心功能:
1. 国内流量走国内 (微信/飞书/钉钉 → 直连)
2. 国外流量走代理 (Telegram/Discord/Slack → 代理)
3. 通讯通道智能路由
4. 多通道统一调度

作者：太一 AGI
创建：2026-04-08
版本：v2.0 (多通道增强版)
"""

import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum

# 配置路径
CONFIG_DIR = Path(__file__).parent / "config"
CACHE_DIR = Path(__file__).parent / "cache"


class RouteType(Enum):
    """路由类型"""
    DOMESTIC = "domestic"  # 国内直连
    INTERNATIONAL = "international"  # 国外代理


class ChannelType(Enum):
    """通道类型"""
    WECHAT = "wechat"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    FEISHU = "feishu"
    SLACK = "slack"
    WHATSAPP = "whatsapp"
    UNKNOWN = "unknown"


@dataclass
class ChannelInfo:
    """通道信息"""
    name: str
    type: ChannelType
    route_type: RouteType
    plugin: str
    status: str
    priority: str
    use_proxy: bool


@dataclass
class RouteResult:
    """路由结果"""
    target: str
    channel: ChannelType
    route_type: RouteType
    proxy: Optional[str]
    plugin: str
    reason: str


class MultiChannelRouter:
    """多通道地理感知路由器"""
    
    def __init__(self):
        self.config = self.load_config()
        self.cache = self.load_cache()
        
        # 代理配置 (先于 load_channels)
        self.proxy_config = self.config.get("proxy_config", {})
        self.proxy_enabled = self.proxy_config.get("international", {}).get("use_proxy", True)
        self.proxy_host = self.proxy_config.get("international", {}).get("proxy_host", "127.0.0.1")
        self.proxy_port = self.proxy_config.get("international", {}).get("proxy_port", 7890)
        
        # 加载通道
        self.channels = self.load_channels()
        
        print(f"🌍 Multi-Channel Router v2.0 初始化完成")
        print(f"   代理：{self.proxy_host}:{self.proxy_port}")
        print(f"   通道：{len(self.channels)} 个")
        print()
    
    def load_config(self) -> Dict:
        """加载配置"""
        config_file = CONFIG_DIR / "communication_channels.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def load_channels(self) -> Dict[str, ChannelInfo]:
        """加载通道配置"""
        channels = {}
        name_to_type = {
            "微信": ChannelType.WECHAT,
            "企业微信": ChannelType.WECHAT,
            "飞书": ChannelType.FEISHU,
            "钉钉": ChannelType.UNKNOWN,
            "Telegram": ChannelType.TELEGRAM,
            "Discord": ChannelType.DISCORD,
            "Slack": ChannelType.SLACK,
            "WhatsApp": ChannelType.WHATSAPP,
        }
        
        for ch in self.config.get("channels", []):
            route_type = RouteType.DOMESTIC if ch.get("type") == "domestic" else RouteType.INTERNATIONAL
            # 从名称映射通道类型
            ch_name = ch.get("name", "")
            channel_type = name_to_type.get(ch_name.split()[0], ChannelType.UNKNOWN)
            
            channels[ch["name"]] = ChannelInfo(
                name=ch["name"],
                type=channel_type,
                route_type=route_type,
                plugin=ch.get("plugin", ""),
                status=ch.get("status", "standby"),
                priority=ch.get("priority", "P2"),
                use_proxy=(route_type == RouteType.INTERNATIONAL and self.proxy_enabled)
            )
        return channels
    
    def load_cache(self) -> Dict:
        """加载缓存"""
        cache_file = CACHE_DIR / "channel_cache.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_cache(self):
        """保存缓存"""
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / "channel_cache.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def get_channel_by_domain(self, domain: str) -> Optional[ChannelInfo]:
        """根据域名获取通道"""
        for channel_name, channel_info in self.channels.items():
            # 检查配置中的域名匹配
            ch_config = next(
                (ch for ch in self.config.get("channels", []) if ch["name"] == channel_name),
                None
            )
            if ch_config:
                for d in ch_config.get("domains", []):
                    if domain == d or domain.endswith("." + d):
                        return channel_info
        return None
    
    def detect_channel(self, url: str) -> RouteResult:
        """智能识别通讯通道"""
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # 检查缓存
        cache_key = f"channel:{domain}"
        now = time.time()
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if now - cached.get("timestamp", 0) < 300:
                return RouteResult(**cached["data"])
        
        # 1. 检查通道配置
        channel = self.get_channel_by_domain(domain)
        if channel:
            result = RouteResult(
                target=url,
                channel=channel.type,
                route_type=channel.route_type,
                proxy=f"socks5://{self.proxy_host}:{self.proxy_port}" if channel.use_proxy else None,
                plugin=channel.plugin,
                reason=f"通道匹配：{channel.name}"
            )
            self.save_to_cache(cache_key, result)
            return result
        
        # 2. 默认路由 (根据 TLD 判断)
        tld = domain.split(".")[-1]
        if tld in ["cn", "中国"]:
            route_type = RouteType.DOMESTIC
            reason = "国内 TLD"
        else:
            route_type = RouteType.INTERNATIONAL
            reason = "国外域名/未知通道"
        
        result = RouteResult(
            target=url,
            channel=ChannelType.UNKNOWN,
            route_type=route_type,
            proxy=f"socks5://{self.proxy_host}:{self.proxy_port}" if route_type == RouteType.INTERNATIONAL else None,
            plugin="unknown",
            reason=reason
        )
        self.save_to_cache(cache_key, result)
        return result
    
    def get_active_channels(self) -> List[ChannelInfo]:
        """获取活跃通道"""
        return [ch for ch in self.channels.values() if ch.status == "active"]
    
    def get_channel_status(self) -> Dict:
        """获取通道状态"""
        status = {}
        for name, ch in self.channels.items():
            status[name] = {
                "type": ch.type.value,
                "route": ch.route_type.value,
                "plugin": ch.plugin,
                "status": ch.status,
                "priority": ch.priority,
                "use_proxy": ch.use_proxy
            }
        return status
    
    def save_to_cache(self, key: str, result: RouteResult):
        """保存到缓存"""
        data = asdict(result)
        data["channel"] = result.channel.value
        data["route_type"] = result.route_type.value
        
        self.cache[key] = {
            "data": data,
            "timestamp": time.time()
        }
        self.save_cache()
    
    def clear_cache(self):
        """清除缓存"""
        self.cache = {}
        self.save_cache()
        print("🗑️ 缓存已清除")


def main():
    """主函数 - 测试"""
    router = MultiChannelRouter()
    
    print("\n=== 多通道地理感知路由 v2.0 ===\n")
    
    # 测试各通道
    test_urls = [
        # 微信
        "https://ilinkai.weixin.qq.com/api/message/send",
        "https://mp.weixin.qq.com/cgi-bin/appmsg",
        # 飞书
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        # Telegram
        "https://api.telegram.org/bot{token}/sendMessage",
        # Discord
        "https://discord.com/api/v10/channels/{id}/messages",
        # Slack
        "https://slack.com/api/chat.postMessage",
    ]
    
    print("📡 通道路由测试:\n")
    for url in test_urls:
        result = router.detect_channel(url)
        proxy_status = "🌐 代理" if result.proxy else "🇨🇳 直连"
        print(f"   {result.channel.value:12} | {proxy_status:8} | {result.reason}")
    
    print("\n\n📊 通道状态:\n")
    status = router.get_channel_status()
    for name, info in status.items():
        status_icon = "✅" if info["status"] == "active" else "🟡"
        proxy_icon = "🌐" if info["use_proxy"] else "🇨🇳"
        print(f"   {status_icon} {name:15} | {info['priority']:3} | {proxy_icon} {info['route']:15} | 插件：{info['plugin']}")


if __name__ == "__main__":
    main()
