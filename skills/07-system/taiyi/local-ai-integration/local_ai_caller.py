#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地 AI 调用器 - Qwen3.5-9B Opus V2

功能:
- 调用 Ollama API
- 智能任务调度
- 复杂任务降级处理
"""

import requests
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('LocalAICaller')

class LocalAICaller:
    """本地 AI 调用器"""
    
    def __init__(self, base_url='http://localhost:11434'):
        self.base_url = base_url
        self.model = 'qwen2.5:7b-instruct-q4_K_M'  # 使用现有模型
    
    def generate(self, prompt: str, max_tokens: int = 1024) -> Optional[str]:
        """
        生成文本
        
        参数:
        - prompt: 输入提示
        - max_tokens: 最大生成长度
        
        返回:
        - 生成的文本
        """
        try:
            response = requests.post(
                f'{self.base_url}/api/generate',
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'num_predict': max_tokens
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"API 错误：{response.status_code} - {response.text}")
                return None
        
        except requests.exceptions.ConnectionError:
            logger.error("无法连接到 Ollama 服务，请检查是否运行")
            return None
        
        except Exception as e:
            logger.error(f"调用失败：{e}")
            return None
    
    def chat(self, messages: list, max_tokens: int = 1024) -> Optional[str]:
        """
        对话模式
        
        参数:
        - messages: 对话历史
        - max_tokens: 最大生成长度
        
        返回:
        - AI 回复
        """
        try:
            response = requests.post(
                f'{self.base_url}/api/chat',
                json={
                    'model': self.model,
                    'messages': messages,
                    'stream': False,
                    'options': {
                        'num_predict': max_tokens
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', '')
            else:
                logger.error(f"API 错误：{response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            logger.error(f"调用失败：{e}")
            return None
    
    def is_available(self) -> bool:
        """检查服务是否可用"""
        try:
            response = requests.get(f'{self.base_url}/api/tags', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> list:
        """列出可用模型"""
        try:
            response = requests.get(f'{self.base_url}/api/tags', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [m['name'] for m in data.get('models', [])]
            return []
        except:
            return []


def main():
    """测试主函数"""
    caller = LocalAICaller()
    
    # 检查服务
    print("检查 Ollama 服务...")
    if not caller.is_available():
        print("❌ Ollama 服务未运行，请先启动：ollama serve")
        return
    
    print("✅ Ollama 服务运行中")
    
    # 列出模型
    print("\n可用模型:")
    models = caller.list_models()
    for model in models:
        print(f"  - {model}")
    
    # 测试生成
    print("\n测试生成:")
    response = caller.generate("太一是什么？请用一句话回答")
    if response:
        print(f"AI: {response}")
    else:
        print("❌ 生成失败")


if __name__ == '__main__':
    main()
