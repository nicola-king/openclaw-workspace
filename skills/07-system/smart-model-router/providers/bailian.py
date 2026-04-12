"""
阿里云百炼模型供应商
国内模型，直连不走代理
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime


class BailianProvider:
    """阿里云百炼模型供应商"""
    
    # 模型端点映射
    MODEL_ENDPOINTS = {
        'qwen3.5-plus': 'qwen-plus',
        'qwen3-coder-plus': 'qwen-coder',
        'qwen-turbo': 'qwen-turbo',
        'qwen-max': 'qwen-max',
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('DASHSCOPE_API_KEY', '')
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        
        if not self.api_key:
            print("[BailianProvider] 警告：未设置 DASHSCOPE_API_KEY")
    
    def call(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        调用百炼模型
        
        Args:
            model: 模型名称 (如 'qwen3.5-plus')
            prompt: 提示词
            **kwargs: 其他参数
        
        Returns:
            响应字典
        """
        if not self.api_key:
            return {
                'model': model,
                'error': 'API key not configured',
                'provider': 'bailian'
            }
        
        # 映射模型名称
        model_name = self.MODEL_ENDPOINTS.get(model, model)
        
        url = f"{self.base_url}/services/aigc/text-generation/generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "input": {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "result_format": "message",
                **kwargs
            }
        }
        
        try:
            # 国内模型直连，不走代理
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # 解析响应
            output = result.get('output', {})
            usage = result.get('usage', {})
            
            return {
                'model': model,
                'response': output.get('choices', [{}])[0].get('message', {}).get('content', ''),
                'tokens_in': usage.get('input_tokens', 0),
                'tokens_out': usage.get('output_tokens', 0),
                'duration_ms': 500,  # 估计值
                'cost': self._calculate_cost(model, usage.get('input_tokens', 0), usage.get('output_tokens', 0)),
                'provider': 'bailian'
            }
        except Exception as e:
            return {
                'model': model,
                'error': str(e),
                'provider': 'bailian'
            }
    
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """计算成本 (元)"""
        # 百炼定价 (每 1000 tokens)
        prices = {
            'qwen-plus': {'input': 0.002, 'output': 0.006},
            'qwen-coder': {'input': 0.002, 'output': 0.006},
            'qwen-turbo': {'input': 0.001, 'output': 0.002},
            'qwen-max': {'input': 0.004, 'output': 0.012},
        }
        
        price = prices.get(model, {'input': 0.002, 'output': 0.006})
        cost = (input_tokens / 1000) * price['input'] + (output_tokens / 1000) * price['output']
        return round(cost, 4)
