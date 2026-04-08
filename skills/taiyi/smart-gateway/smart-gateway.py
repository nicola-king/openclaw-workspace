#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能网关路由器 - 自动选择国内/代理流量

功能:
- 域名智能识别
- 自动路由选择
- 代理自动切换
"""

import os
import logging
from urllib.parse import urlparse
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SmartGateway')

class SmartGateway:
    """智能网关路由器"""
    
    def __init__(self):
        # 国内域名白名单
        self.domestic_domains = [
            # 云服务 (百炼 API)
            'aliyun.com',
            'aliyuncs.com',
            'dashscope.aliyun.com',
            'oss.aliyuncs.com',
            
            # 社交媒体
            'wechat.com',
            'weibo.com',
            'zhihu.com',
            'bilibili.com',
            'douyin.com',
            
            # 开发服务
            'gitee.com',
            'coding.net',
            
            # 其他国内服务
            'qq.com',
            '163.com',
            'baidu.com',
            'jd.com',
            'taobao.com',
        ]
        
        # 代理配置 (Clash 默认端口)
        self.proxy_config = {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }
        
        # 代理状态
        self.proxy_enabled = self._check_proxy_available()
    
    def _check_proxy_available(self) -> bool:
        """检查代理是否可用"""
        import socket
        try:
            # 尝试连接代理端口
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', 7890))
            sock.close()
            return result == 0
        except:
            return False
    
    def is_domestic(self, url: str) -> bool:
        """判断是否为国内域名"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # localhost 和本地 IP
            if domain in ['localhost', '127.0.0.1', '0.0.0.0']:
                return True
            
            # 检查是否在白名单中
            for domestic in self.domestic_domains:
                if domestic in domain:
                    return True
            
            # 检查.cn 域名
            if domain.endswith('.cn'):
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"域名判断失败：{e}")
            return False  # 默认走代理
    
    def get_proxies(self, url: str) -> Optional[Dict[str, str]]:
        """根据 URL 获取代理配置"""
        if self.is_domestic(url):
            # 国内流量，不使用代理
            logger.info(f"🇨🇳 国内流量：{url}")
            return None
        else:
            # 国外流量，使用代理
            if self.proxy_enabled:
                logger.info(f"🌐 代理流量：{url}")
                return self.proxy_config
            else:
                logger.warning(f"⚠️ 代理不可用，直接访问：{url}")
                return None
    
    def request(self, method, url, **kwargs):
        """智能请求 (自动选择路由)"""
        import requests
        
        proxies = self.get_proxies(url)
        
        # 设置超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 30
        
        try:
            response = requests.request(method, url, proxies=proxies, **kwargs)
            logger.info(f"✅ 请求成功：{url} (状态码：{response.status_code})")
            return response
        except requests.exceptions.ProxyError as e:
            logger.error(f"❌ 代理错误：{e}")
            # 尝试降级直接访问
            if proxies:
                logger.info("尝试降级直接访问...")
                return requests.request(method, url, **kwargs)
            raise
        except Exception as e:
            logger.error(f"❌ 请求失败：{e}")
            raise
    
    def get(self, url, **kwargs):
        """GET 请求"""
        return self.request('GET', url, **kwargs)
    
    def post(self, url, **kwargs):
        """POST 请求"""
        return self.request('POST', url, **kwargs)
    
    def get_status(self) -> str:
        """获取状态报告"""
        status = f"""
🌐 智能网关状态

代理状态：{'✅ 可用' if self.proxy_enabled else '❌ 不可用'}
代理地址：{self.proxy_config['http']}

国内域名白名单 ({len(self.domestic_domains)}个):
"""
        for i, domain in enumerate(self.domestic_domains[:10], 1):
            status += f"  {i}. {domain}\n"
        
        if len(self.domestic_domains) > 10:
            status += f"  ... 还有{len(self.domestic_domains) - 10}个\n"
        
        return status


def main():
    """测试主函数"""
    gateway = SmartGateway()
    
    # 测试用例
    test_urls = [
        'https://dashscope.aliyun.com/api/v1/services/aigc/text-generation/generation',  # 百炼 API (国内)
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',  # Gemini API (代理)
        'https://api.weixin.qq.com/cgi-bin/token',  # 微信 API (国内)
        'https://api.github.com/repos/nicola-king/zhiji-e',  # GitHub API (代理)
        'http://localhost:11434/api/generate',  # Ollama 本地 (本地)
        'https://www.baidu.com',  # 百度 (国内)
        'https://www.google.com',  # Google (代理)
    ]
    
    print("🌐 智能网关测试\n")
    print("=" * 60)
    
    for url in test_urls:
        print(f"\n测试：{url}")
        print("-" * 60)
        is_domestic = gateway.is_domestic(url)
        proxies = gateway.get_proxies(url)
        print(f"路由：{'🇨🇳 国内流量' if is_domestic else '🌐 代理流量'}")
    
    print("\n" + "=" * 60)
    print("\n📊 状态报告:")
    print(gateway.get_status())


if __name__ == '__main__':
    main()
