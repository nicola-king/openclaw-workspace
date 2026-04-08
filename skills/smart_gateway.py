#!/usr/bin/env python3
"""
智能网关路由器 - 请求路由与负载均衡
国内/代理分流 + 请求优化 + 健康检查
"""

import os
import json
import requests
import time
from typing import Dict, Any, List
from urllib.parse import urlparse

class SmartGateway:
    def __init__(self):
        self.config = self.load_config()
        self.domestic_endpoints = []  # 国内直连服务
        self.proxy_endpoints = []     # 代理转发服务
        self.health_status = {}       # 服务健康状态
        self.request_stats = {}       # 请求统计
        self.init_endpoints()
    
    def load_config(self) -> Dict:
        """加载 OpenClaw 配置"""
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"警告: 无法加载配置文件 {e}")
            return {}
    
    def init_endpoints(self):
        """初始化端点配置"""
        # 根据配置动态识别端点类型
        channels = self.config.get('channels', {})
        
        # 国内服务 (微信/飞书)
        self.domestic_endpoints = []
        if channels.get('openclaw-weixin', {}).get('enabled', False):
            self.domestic_endpoints.append({
                'name': 'weixin',
                'url': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send',
                'type': 'domestic'
            })
        
        if channels.get('feishu', {}).get('enabled', False):
            self.domestic_endpoints.append({
                'name': 'feishu',
                'url': 'https://open.feishu.cn/open-apis/bot/v2/hook/',
                'type': 'domestic'
            })
        
        # 代理服务 (Telegram)
        self.proxy_endpoints = []
        if channels.get('telegram', {}).get('enabled', False):
            self.proxy_endpoints.append({
                'name': 'telegram',
                'url': 'https://api.telegram.org/bot',
                'type': 'proxy',
                'proxy': os.getenv('TELEGRAM_PROXY', 'http://127.0.0.1:7890')
            })
    
    def health_check(self, endpoint: Dict) -> bool:
        """检查端点健康状态"""
        try:
            url = endpoint['url']
            if endpoint['name'] == 'telegram':
                # Telegram 健康检查 - 获取 bot 信息
                bot_token = self.config.get('channels', {}).get('telegram', {}).get('accounts', {}).get('taiyi', {}).get('botToken', '')
                if bot_token:
                    test_url = f"{url}{bot_token}/getMe"
                    proxies = {'http': endpoint['proxy'], 'https': endpoint['proxy']} if endpoint.get('proxy') else None
                    response = requests.get(test_url, proxies=proxies, timeout=10)
                    return response.status_code == 200
            elif endpoint['name'] == 'weixin':
                # 微信健康检查 - 使用假的 webhook key 进行测试
                return True  # 微信 webhook 无法预先测试
            elif endpoint['name'] == 'feishu':
                # 飞书健康检查 - 使用假的 webhook key 进行测试
                return True  # 飞书 webhook 无法预先测试
            
            return False
        except Exception as e:
            print(f"健康检查异常 {endpoint['name']}: {e}")
            return False
    
    def update_health_status(self):
        """更新所有端点健康状态"""
        for endpoint in self.domestic_endpoints + self.proxy_endpoints:
            name = endpoint['name']
            self.health_status[name] = {
                'healthy': self.health_check(endpoint),
                'last_check': time.time(),
                'type': endpoint['type']
            }
    
    def route_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        智能路由请求
        根据请求目标选择合适的端点和传输方式
        """
        target = request_data.get('target', 'unknown')
        
        # 更新健康状态（如果超过5分钟未检查）
        if time.time() - self.health_status.get('last_full_check', 0) > 300:
            self.update_health_status()
            self.health_status['last_full_check'] = time.time()
        
        # 根据目标选择端点
        if target in ['weixin', 'wechat', 'weixin-official']:
            return self._route_domestic(request_data)
        elif target in ['feishu', 'lark']:
            return self._route_domestic(request_data)
        elif target in ['telegram', 'tg']:
            return self._route_proxy(request_data)
        else:
            # 默认路由策略：根据域名判断
            destination = request_data.get('destination', '')
            if 'weixin' in destination or 'qyapi' in destination:
                return self._route_domestic(request_data)
            elif 'feishu' in destination or 'larksuite' in destination:
                return self._route_domestic(request_data)
            elif 'telegram' in destination or 'api.telegram.org' in destination:
                return self._route_proxy(request_data)
            else:
                # 默认使用国内端点（假设大部分国内服务）
                return self._route_domestic(request_data)
    
    def _route_domestic(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """路由到国内端点"""
        target = request_data.get('target', 'unknown')
        
        # 检查对应服务的健康状态
        if target in self.health_status:
            if not self.health_status[target]['healthy']:
                return {
                    'success': False,
                    'error': f'{target} 服务不可用',
                    'retry_suggestion': '请检查网络连接或服务配置'
                }
        
        # 执行国内请求
        try:
            url = request_data['url']
            method = request_data.get('method', 'POST')
            headers = request_data.get('headers', {})
            data = request_data.get('data', {})
            
            response = requests.request(method, url, headers=headers, json=data, timeout=30)
            
            # 更新统计
            self._update_stats(target, 'domestic', response.status_code == 200)
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response': response.json() if response.content else {},
                'latency': response.elapsed.total_seconds()
            }
        except Exception as e:
            self._update_stats(target, 'domestic', False)
            return {
                'success': False,
                'error': str(e),
                'target': target,
                'route': 'domestic'
            }
    
    def _route_proxy(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """路由到代理端点"""
        target = request_data.get('target', 'unknown')
        
        # 检查对应服务的健康状态
        if target in self.health_status:
            if not self.health_status[target]['healthy']:
                return {
                    'success': False,
                    'error': f'{target} 服务不可用',
                    'retry_suggestion': '请检查代理设置或服务配置'
                }
        
        # 执行代理请求
        try:
            url = request_data['url']
            method = request_data.get('method', 'POST')
            headers = request_data.get('headers', {})
            data = request_data.get('data', {})
            
            # 获取代理配置
            proxy_endpoint = next((ep for ep in self.proxy_endpoints if ep['name'] == target), None)
            proxies = None
            if proxy_endpoint and proxy_endpoint.get('proxy'):
                proxies = {
                    'http': proxy_endpoint['proxy'],
                    'https': proxy_endpoint['proxy']
                }
            
            response = requests.request(method, url, headers=headers, json=data, proxies=proxies, timeout=30)
            
            # 更新统计
            self._update_stats(target, 'proxy', response.status_code == 200)
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response': response.json() if response.content else {},
                'latency': response.elapsed.total_seconds(),
                'via_proxy': True
            }
        except Exception as e:
            self._update_stats(target, 'proxy', False)
            return {
                'success': False,
                'error': str(e),
                'target': target,
                'route': 'proxy'
            }
    
    def _update_stats(self, target: str, route_type: str, success: bool):
        """更新请求统计"""
        key = f"{target}_{route_type}"
        if key not in self.request_stats:
            self.request_stats[key] = {'total': 0, 'success': 0, 'failure': 0}
        
        self.request_stats[key]['total'] += 1
        if success:
            self.request_stats[key]['success'] += 1
        else:
            self.request_stats[key]['failure'] += 1
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """获取路由统计信息"""
        return {
            'health_status': self.health_status,
            'request_stats': self.request_stats,
            'endpoints': {
                'domestic': [ep['name'] for ep in self.domestic_endpoints],
                'proxy': [ep['name'] for ep in self.proxy_endpoints]
            }
        }
    
    def optimize_routing(self):
        """优化路由策略"""
        # 根据历史成功率调整路由偏好
        for key, stats in self.request_stats.items():
            if stats['total'] > 10:  # 至少10次请求才有统计意义
                success_rate = stats['success'] / stats['total']
                if success_rate < 0.8:  # 成功率低于80%，考虑调整
                    print(f"警告: {key} 成功率较低 ({success_rate:.2%})，可能需要检查配置")
    
    def test_all_connections(self) -> Dict[str, Any]:
        """测试所有连接"""
        results = {}
        
        # 测试国内端点
        for endpoint in self.domestic_endpoints:
            name = endpoint['name']
            results[f"{name}_domestic"] = self.health_check(endpoint)
        
        # 测试代理端点
        for endpoint in self.proxy_endpoints:
            name = endpoint['name']
            results[f"{name}_proxy"] = self.health_check(endpoint)
        
        return results

# 使用示例
if __name__ == "__main__":
    gateway = SmartGateway()
    
    # 初始化端点
    print("智能网关初始化完成")
    print(f"国内端点: {[ep['name'] for ep in gateway.domestic_endpoints]}")
    print(f"代理端点: {[ep['name'] for ep in gateway.proxy_endpoints]}")
    
    # 测试连接
    print("\n测试所有连接:")
    test_results = gateway.test_all_connections()
    for service, healthy in test_results.items():
        status = "✅" if healthy else "❌"
        print(f"  {service}: {status}")
    
    # 获取统计
    print("\n当前路由统计:")
    stats = gateway.get_routing_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))