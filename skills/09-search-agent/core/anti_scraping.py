#!/usr/bin/env python3
"""
反反爬策略模块
版本：v1.0.0
作者：太一 AGI
"""

import time
import random
import json
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

@dataclass
class ProxyConfig:
    """代理配置"""
    server: str
    username: str = ""
    password: str = ""
    region: str = ""
    enabled: bool = True

class AntiScrapingStrategy:
    """反反爬策略"""
    
    def __init__(self, config: dict = None):
        """初始化反反爬策略"""
        self.config = config or {}
        self.proxies = self._load_proxies()
        self.current_proxy_index = 0
        self.request_count = 0
        self.last_request_time = 0
        
        logger.info("🛡️ 反反爬策略初始化完成")
    
    def _load_proxies(self) -> List[ProxyConfig]:
        """加载代理配置"""
        proxy_list = self.config.get("proxies", [])
        return [ProxyConfig(**p) if isinstance(p, dict) else p for p in proxy_list]
    
    def get_proxy(self) -> Optional[ProxyConfig]:
        """获取代理"""
        if not self.proxies:
            return None
        
        # 轮换代理
        proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
        self.current_proxy_index += 1
        
        return proxy if proxy.enabled else None
    
    def apply_delay(self):
        """应用请求延迟"""
        delay_range = self.config.get("delay_range", [1, 3])
        delay = random.uniform(delay_range[0], delay_range[1])
        
        time.sleep(delay)
        logger.debug(f"⏱️ 请求延迟: {delay:.2f}秒")
    
    def rotate_user_agent(self) -> str:
        """轮换 User-Agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
        ]
        
        return random.choice(user_agents)
    
    def create_playwright_context(self, proxy: ProxyConfig = None) -> dict:
        """创建 Playwright 浏览器上下文"""
        context_options = {
            "user_agent": self.rotate_user_agent(),
            "viewport": {"width": 1920, "height": 1080},
            "locale": "en-US",
            "timezone_id": "America/New_York",
            "permissions": ["geolocation"],
            "geolocation": {"latitude": 40.7128, "longitude": -74.0060},
            "color_scheme": "light",
            "extra_http_headers": {
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            }
        }
        
        # 添加代理
        if proxy:
            context_options["proxy"] = {
                "server": proxy.server,
                "username": proxy.username,
                "password": proxy.password
            }
        
        return context_options
    
    def handle_captcha(self, page) -> bool:
        """处理验证码"""
        try:
            # 检测验证码
            captcha_selectors = [
                "iframe[src*='recaptcha']",
                ".g-recaptcha",
                "#captcha",
                ".captcha-container",
                "[data-captcha]"
            ]
            
            for selector in captcha_selectors:
                if page.query_selector(selector):
                    logger.warning("🔒 检测到验证码")
                    return self._solve_captcha(page)
            
            return True
            
        except Exception as e:
            logger.error(f"验证码处理失败: {str(e)}")
            return False
    
    def _solve_captcha(self, page) -> bool:
        """解决验证码"""
        # 简单验证码处理
        try:
            # 等待验证码加载
            page.wait_for_timeout(2000)
            
            # 尝试点击验证
            verify_selectors = [
                "#verify-button",
                ".verify-btn",
                "[data-verify]",
                ".captcha-submit"
            ]
            
            for selector in verify_selectors:
                button = page.query_selector(selector)
                if button:
                    button.click()
                    page.wait_for_timeout(3000)
                    return True
            
            logger.warning("⚠️ 无法自动解决验证码")
            return False
            
        except Exception as e:
            logger.error(f"验证码解决失败: {str(e)}")
            return False
    
    def check_rate_limit(self, response) -> bool:
        """检查速率限制"""
        status_code = response.status_code if hasattr(response, 'status_code') else 0
        
        if status_code == 429:  # Too Many Requests
            logger.warning("⚠️ 触发速率限制")
            self._handle_rate_limit()
            return True
        
        return False
    
    def _handle_rate_limit(self):
        """处理速率限制"""
        # 增加延迟
        delay = random.uniform(5, 10)
        logger.info(f"⏱️ 速率限制，等待 {delay:.2f} 秒")
        time.sleep(delay)
        
        # 切换代理
        if self.proxies:
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
            logger.info("🔄 已切换代理")
    
    def fingerprint_spoofing(self, page) -> None:
        """指纹伪装"""
        try:
            # 隐藏 WebDriver
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            # 伪装 Chrome 插件
            page.add_init_script("""
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
            """)
            
            # 伪装语言
            page.add_init_script("""
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
            """)
            
            logger.debug("🎭 指纹伪装完成")
            
        except Exception as e:
            logger.error(f"指纹伪装失败: {str(e)}")
    
    def update_metrics(self, success: bool, response_time: float):
        """更新指标"""
        self.request_count += 1
        self.last_request_time = time.time()
        
        # 记录成功/失败
        if not success:
            logger.warning(f"❌ 请求失败 (第 {self.request_count} 次)")
        else:
            logger.debug(f"✅ 请求成功 (第 {self.request_count} 次, {response_time:.2f}秒)")
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_requests": self.request_count,
            "current_proxy": self.current_proxy_index % len(self.proxies) if self.proxies else None,
            "last_request_time": self.last_request_time,
            "proxies_available": len(self.proxies)
        }

class ProxyManager:
    """代理管理器"""
    
    def __init__(self, config_path: str = "config/proxy_config.json"):
        """初始化代理管理器"""
        self.config_path = config_path
        self.proxies = self._load_proxies()
        self.current_index = 0
        
        logger.info(f"🌐 代理管理器初始化: {len(self.proxies)} 个代理")
    
    def _load_proxies(self) -> List[ProxyConfig]:
        """加载代理配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return [ProxyConfig(**p) for p in config.get("proxies", [])]
        except FileNotFoundError:
            return []
    
    def get_next_proxy(self) -> Optional[ProxyConfig]:
        """获取下一个代理"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index % len(self.proxies)]
        self.current_index += 1
        
        return proxy if proxy.enabled else None
    
    def add_proxy(self, proxy: ProxyConfig):
        """添加代理"""
        self.proxies.append(proxy)
        logger.info(f"➕ 添加代理: {proxy.server}")
    
    def remove_proxy(self, server: str):
        """移除代理"""
        self.proxies = [p for p in self.proxies if p.server != server]
        logger.info(f"➖ 移除代理: {server}")
    
    def get_stats(self) -> dict:
        """获取代理统计"""
        enabled = [p for p in self.proxies if p.enabled]
        return {
            "total": len(self.proxies),
            "enabled": len(enabled),
            "current_index": self.current_index
        }

if __name__ == "__main__":
    # 测试代码
    strategy = AntiScrapingStrategy()
    
    # 测试代理轮换
    for i in range(5):
        proxy = strategy.get_proxy()
        print(f"代理 {i+1}: {proxy.server if proxy else '无'}")
    
    # 测试 User-Agent 轮换
    for i in range(3):
        ua = strategy.rotate_user_agent()
        print(f"User-Agent {i+1}: {ua[:50]}...")
    
    # 获取统计
    stats = strategy.get_stats()
    print(f"\n统计: {stats}")