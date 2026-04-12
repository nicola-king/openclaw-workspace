"""
Google Gemini 模型供应商
海外模型，需要代理
"""

import os
import json
import requests
from typing import Dict, Any, Optional


class GoogleProvider:
    """Google Gemini 模型供应商"""
    
    # 模型版本映射
    MODEL_VERSIONS = {
        'gemini-2.5-pro': 'gemini-2.5-pro-preview-05-06',
        'gemini-pro': 'gemini-pro',
        'gemini': 'gemini-pro',
    }
    
    def __init__(self, api_key: Optional[str] = None, proxy_url: Optional[str] = None):
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY', '')
        self.proxy_url = proxy_url or os.environ.get('HTTP_PROXY', 'http://127.0.0.1:7890')
        
        if not self.api_key:
            print("[GoogleProvider] 警告：未设置 GOOGLE_API_KEY")
    
    def call(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        调用 Gemini 模型
        
        Args:
            model: 模型名称 (如 'gemini-2.5-pro')
            prompt: 提示词
            **kwargs: 其他参数
        
        Returns:
            响应字典
        """
        if not self.api_key:
            return {
                'model': model,
                'error': 'API key not configured',
                'provider': 'google'
            }
        
        # 映射模型版本
        model_version = self.MODEL_VERSIONS.get(model, 'gemini-pro')
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_version}:generateContent"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                **kwargs
            }
        }
        
        params = {"key": self.api_key}
        
        # 海外模型走代理
        proxies = {
            "http": self.proxy_url,
            "https": self.proxy_url
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, params=params, proxies=proxies, timeout=120)
            response.raise_for_status()
            result = response.json()
            
            # 解析响应
            candidates = result.get('candidates', [])
            if not candidates:
                return {
                    'model': model,
                    'error': 'No candidates in response',
                    'provider': 'google'
                }
            
            content = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            usage_metadata = result.get('usageMetadata', {})
            
            return {
                'model': model,
                'response': content,
                'tokens_in': usage_metadata.get('promptTokenCount', 0),
                'tokens_out': usage_metadata.get('candidatesTokenCount', 0),
                'duration_ms': 1000,  # 估计值
                'cost': self._calculate_cost(model, usage_metadata.get('promptTokenCount', 0), usage_metadata.get('candidatesTokenCount', 0)),
                'provider': 'google'
            }
        except Exception as e:
            return {
                'model': model,
                'error': str(e),
                'provider': 'google'
            }
    
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """计算成本 (美元转人民币，汇率 7.2)"""
        # Gemini 定价 (每 1000 tokens)
        prices = {
            'gemini-2.5-pro': {'input': 0.0025, 'output': 0.0075},
            'gemini-pro': {'input': 0.0005, 'output': 0.0015},
        }
        
        price = prices.get(model, {'input': 0.0005, 'output': 0.0015})
        cost_usd = (input_tokens / 1000) * price['input'] + (output_tokens / 1000) * price['output']
        cost_cny = cost_usd * 7.2  # 美元转人民币
        return round(cost_cny, 4)
