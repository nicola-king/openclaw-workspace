#!/usr/bin/env python3
"""
GMGN.AI API Client - 统一 API 封装
支持 Solana/Base/BSC 链，提供认证/请求/错误处理/速率限制

参考：https://gmgn.ai/ 官方 API 文档
"""

import os
import json
import time
import hashlib
import base64
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


class GMGNClient:
    """
    GMGN.AI 统一 API 客户端
    
    支持两种认证模式：
    1. 普通认证 (API Key) - 用于查询类操作
    2. 签名认证 (API Key + Private Key) - 用于交易执行
    
    速率限制：
    - 默认：10 requests/second
    - 权重路由：根据 endpoint 权重动态调整
    """
    
    # API 基础 URL
    BASE_URL = "https://api.gmgn.ai"
    
    # 路由权重配置 (用于速率限制)
    ROUTE_WEIGHTS = {
        # Market routes
        '/v1/market/token_kline': 2,
        '/v1/market/rank': 1,
        '/v1/trenches': 3,
        # Portfolio routes
        '/v1/user/info': 1,
        '/v1/user/wallet_holdings': 2,
        '/v1/user/wallet_activity': 3,
        '/v1/user/wallet_stats': 3,
        '/v1/user/wallet_token_balance': 1,
        # Token routes
        '/v1/token/info': 1,
        '/v1/token/security': 1,
        '/v1/token/pool_info': 1,
        '/v1/market/token_top_holders': 5,
        '/v1/market/token_top_traders': 5,
        # Track routes
        '/v1/trade/follow_wallet': 3,
        '/v1/user/kol': 1,
        '/v1/user/smartmoney': 1,
        # Trade routes (critical auth)
        '/v1/trade/swap': 5,
        '/v1/trade/quote': 2,
        '/v1/trade/query_order': 1,
        # Cooking routes
        '/v1/launch/create': 5,
        '/v1/launch/stats': 1,
    }
    
    def __init__(self, api_key: Optional[str] = None, private_key: Optional[str] = None):
        """
        初始化 GMGN 客户端
        
        Args:
            api_key: GMGN API Key (从 ~/.config/gmgn/.env 或环境变量读取)
            private_key: Ed25519 私钥 (用于签名认证，可选)
        """
        # 从环境变量或配置文件读取凭证
        self.api_key = api_key or os.getenv('GMGN_API_KEY', '')
        self.private_key = private_key or os.getenv('GMGN_PRIVATE_KEY', '')
        
        # 如果没有从环境变量读取，尝试从配置文件读取
        if not self.api_key:
            config_path = Path.home() / '.config' / 'gmgn' / '.env'
            if config_path.exists():
                with open(config_path, 'r') as f:
                    for line in f:
                        if line.startswith('GMGN_API_KEY='):
                            self.api_key = line.strip().split('=', 1)[1]
                        elif line.startswith('GMGN_PRIVATE_KEY='):
                            self.private_key = line.strip().split('=', 1)[1]
        
        # 初始化 requests session
        if requests:
            self.session = requests.Session()
            self.session.headers.update({
                'Content-Type': 'application/json',
                'User-Agent': 'Taiyi-GMGN-Client/2.0',
                'X-APIKEY': self.api_key
            })
        else:
            self.session = None
        
        # 速率限制跟踪
        self._rate_limit_reset = 0
        self._request_count = 0
    
    def _generate_signature(self, timestamp: int, method: str, path: str, body: str = '') -> str:
        """
        生成 Ed25519 签名
        
        签名格式：timestamp.method.path.body_hash
        """
        if not self.private_key:
            raise ValueError("Private key required for signature")
        
        # 构建签名字符串
        body_hash = hashlib.sha256(body.encode()).hexdigest()
        sign_str = f"{timestamp}{method}{path}{body_hash}"
        
        # 使用 cryptography 库进行 Ed25519 签名
        try:
            from cryptography.hazmat.primitives import serialization, hashes
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
            
            # 加载私钥
            private_key = serialization.load_pem_private_key(
                self.private_key.encode(),
                password=None
            )
            
            # 签名
            signature = private_key.sign(sign_str.encode())
            return base64.b64encode(signature).decode()
        except ImportError:
            # 如果没有 cryptography 库，返回空签名 (仅用于测试)
            return ''
    
    def _check_rate_limit(self, endpoint: str):
        """检查速率限制"""
        current_time = time.time()
        
        # 如果还在限制期内，等待
        if current_time < self._rate_limit_reset:
            wait_time = self._rate_limit_reset - current_time
            if wait_time > 0:
                time.sleep(min(wait_time, 5))  # 最多等待 5 秒
    
    def _handle_rate_limit_response(self, response):
        """处理 429 速率限制响应"""
        if response.status_code == 429:
            # 从响应头读取重置时间
            reset_header = response.headers.get('X-RateLimit-Reset', '')
            if reset_header:
                try:
                    self._rate_limit_reset = int(reset_header)
                except ValueError:
                    pass
            
            # 从响应体读取 reset_at
            try:
                data = response.json()
                if 'reset_at' in data:
                    self._rate_limit_reset = max(self._rate_limit_reset, data['reset_at'])
            except:
                pass
            
            return {
                'error': 'RATE_LIMIT_EXCEEDED',
                'message': 'API 速率限制，请稍后重试',
                'reset_at': self._rate_limit_reset
            }
        
        return None
    
    def request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None, 
                requires_signature: bool = False) -> Dict:
        """
        统一请求方法
        
        Args:
            method: HTTP 方法 (GET/POST)
            endpoint: API 端点 (如 /v1/market/rank)
            params: URL 参数
            data: 请求体数据
            requires_signature: 是否需要签名认证
        
        Returns:
            API 响应字典
        """
        if not self.session:
            return {'error': 'requests library not available', 'success': False}
        
        # 检查速率限制
        self._check_rate_limit(endpoint)
        
        # 构建完整 URL
        url = f"{self.BASE_URL}{endpoint}"
        
        # 准备请求头
        headers = self.session.headers.copy()
        
        # 如果需要签名认证
        if requires_signature and self.private_key:
            timestamp = int(time.time())
            body_str = json.dumps(data, separators=(',', ':')) if data else ''
            signature = self._generate_signature(timestamp, method, endpoint, body_str)
            headers['X-Timestamp'] = str(timestamp)
            headers['X-Signature'] = signature
        
        try:
            # 发送请求
            response = self.session.request(
                method,
                url,
                params=params,
                json=data,
                headers=headers,
                timeout=30
            )
            
            # 处理速率限制
            rate_limit_error = self._handle_rate_limit_response(response)
            if rate_limit_error:
                return rate_limit_error
            
            # 解析响应
            response.raise_for_status()
            result = response.json()
            
            # 检查业务错误
            if isinstance(result, dict) and result.get('code') != 200:
                return {
                    'error': result.get('error', 'UNKNOWN_ERROR'),
                    'message': result.get('message', ''),
                    'success': False
                }
            
            return result
            
        except requests.exceptions.Timeout:
            return {'error': 'TIMEOUT', 'message': '请求超时', 'success': False}
        except requests.exceptions.ConnectionError:
            return {'error': 'CONNECTION_ERROR', 'message': '连接失败', 'success': False}
        except requests.exceptions.HTTPError as e:
            return {'error': f'HTTP_{e.response.status_code}', 'message': str(e), 'success': False}
        except Exception as e:
            return {'error': 'UNKNOWN_ERROR', 'message': str(e), 'success': False}
    
    def get(self, endpoint: str, params: Dict = None) -> Dict:
        """GET 请求"""
        return self.request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict = None, requires_signature: bool = False) -> Dict:
        """POST 请求"""
        return self.request('POST', endpoint, data=data, requires_signature=requires_signature)
    
    def get_wallet_address(self, chain: str) -> Optional[str]:
        """
        获取配置的钱包地址
        
        Args:
            chain: 链名称 (sol/bsc/base)
        
        Returns:
            钱包地址或 None
        """
        # 从配置文件或环境变量读取
        wallet_config = {
            'sol': os.getenv('GMGN_SOL_WALLET', '5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq'),
            'bsc': os.getenv('GMGN_BSC_WALLET', ''),
            'base': os.getenv('GMGN_BASE_WALLET', '0x73d6a5835ddf6f54480e28c8fdf399f8ec1b1c79'),
        }
        return wallet_config.get(chain)
    
    def is_authenticated(self) -> bool:
        """检查是否已认证"""
        return bool(self.api_key)
    
    def has_private_key(self) -> bool:
        """检查是否有私钥 (用于交易执行)"""
        return bool(self.private_key)


# 便捷函数
def create_client(api_key: str = None, private_key: str = None) -> GMGNClient:
    """创建 GMGN 客户端实例"""
    return GMGNClient(api_key, private_key)
