"""
本地模型供应商 (Ollama)
零成本，低延迟
"""

import requests
import json
from typing import Dict, Any, Optional
from pathlib import Path


class LocalProvider:
    """本地 Ollama 模型供应商"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self._check_connection()
    
    def _check_connection(self):
        """检查 Ollama 连接"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.available_models = [model['name'] for model in data.get('models', [])]
                print(f"[LocalProvider] 已连接 Ollama，可用模型：{self.available_models}")
            else:
                print(f"[LocalProvider] Ollama 连接失败：{response.status_code}")
        except Exception as e:
            print(f"[LocalProvider] Ollama 不可用：{e}")
            self.available_models = []
    
    def is_available(self) -> bool:
        """检查本地模型是否可用"""
        return len(self.available_models) > 0
    
    def call(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        调用本地模型
        
        Args:
            model: 模型名称 (如 'qwen2.5:7b')
            prompt: 提示词
            **kwargs: 其他参数 (temperature, max_tokens 等)
        
        Returns:
            响应字典
        """
        if not self.is_available():
            raise RuntimeError("Ollama 本地模型不可用")
        
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            return {
                'model': model,
                'response': result.get('response', ''),
                'tokens_in': result.get('prompt_eval_count', 0),
                'tokens_out': result.get('eval_count', 0),
                'duration_ms': result.get('total_duration', 0) // 1000000,
                'cost': 0.0,
                'provider': 'local'
            }
        except Exception as e:
            return {
                'model': model,
                'error': str(e),
                'provider': 'local'
            }
    
    def list_models(self) -> List[str]:
        """列出可用模型"""
        return self.available_models
