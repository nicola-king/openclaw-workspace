#!/usr/bin/env python3
"""
增强版智能自动化系统
改进错误处理和容错能力
"""

import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, Any, Callable
import sys
import requests

class EnhancedSmartAIRouter:
    def __init__(self):
        self.config = self.load_config()
        self.local_model_endpoint = "http://localhost:11434"
        self.cloud_providers = {
            'bailian': {
                'baseUrl': 'https://coding.dashscope.aliyuncs.com/v1',
                'apiKey': os.getenv('BAILIAN_API_KEY', self.config.get('models', {}).get('providers', {}).get('bailian', {}).get('apiKey', ''))
            },
            'google': {
                'baseUrl': 'https://generativelanguage.googleapis.com',
                'apiKey': os.getenv('GOOGLE_API_KEY', self.config.get('models', {}).get('providers', {}).get('google', {}).get('apiKey', ''))
            }
        }
        self.local_model_available = self.check_local_model_availability()
    
    def load_config(self) -> Dict:
        """加载 OpenClaw 配置"""
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"警告: 无法加载配置文件 {e}")
            return {}
    
    def check_local_model_availability(self) -> bool:
        """检查本地模型是否可用"""
        try:
            response = requests.get(f"{self.local_model_endpoint}/api/tags", timeout=10)
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                target_model = "qwen2.5:7b-instruct-q4_K_M"
                if target_model in models:
                    print(f"✅ 本地模型 {target_model} 可用")
                    return True
                else:
                    print(f"⚠️ 本地模型 {target_model} 未安装")
                    return False
            else:
                print(f"⚠️ 本地模型服务不可访问: {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️ 本地模型服务不可访问: {e}")
            return False
    
    def classify_task(self, user_request: str) -> tuple:
        """
        自动分类用户请求
        返回：task_type, complexity, token_estimate
        """
        # 关键词匹配简单任务
        simple_keywords = ['你好', '谢谢', '翻译', '总结', '润色', '计算', '换算', '等于', '首都', '天气']
        code_keywords = ['写代码', '脚本', 'bug', '编程', '开发', '函数', '类', 'API']
        long_text_keywords = ['文档', '报告', '分析', '研究', '论文', '书籍', '长文']
        
        # 估算 token 数量
        token_estimate = len(user_request) // 4  # 粗略估算
        
        # 分类逻辑
        if any(kw in user_request for kw in code_keywords):
            return 'code', 'medium', max(token_estimate, 5000)
        elif any(kw in user_request for kw in long_text_keywords):
            return 'long_text', 'hard', max(token_estimate, 50000)
        elif any(kw in user_request for kw in simple_keywords) or token_estimate < 1000:
            return 'simple', 'easy', token_estimate
        else:
            return 'chat', 'medium', token_estimate
    
    def select_model(self, task_type: str, complexity: str, token_estimate: int) -> str:
        """
        根据任务类型选择模型
        返回模型标识符
        """
        # 如果本地模型不可用，直接使用云端模型
        if not self.local_model_available:
            print("本地模型不可用，使用云端模型")
            if task_type == 'code':
                return 'bailian/qwen3-coder-plus'
            elif complexity == 'hard' or token_estimate >= 50000:
                return 'google/gemini-2.5-pro'
            else:
                return 'bailian/qwen3.5-plus'
        
        # 本地模型优先 (Qwen 2.5 7B)
        if complexity == 'easy' and token_estimate < 8000:
            if task_type in ['simple', 'chat']:
                return 'local/qwen2.5:7b-instruct-q4_K_M'
        
        # 代码任务专用
        if task_type == 'code':
            return 'bailian/qwen3-coder-plus'
        
        # 长文本任务
        if complexity == 'hard' or token_estimate >= 50000:
            return 'google/gemini-2.5-pro'
        
        # 默认使用主力模型
        return 'bailian/qwen3.5-plus'
    
    def call_local_model(self, prompt: str, model: str = "qwen2.5:7b-instruct-q4_K_M") -> str:
        """调用本地 Ollama 模型"""
        if not self.local_model_available:
            print("本地模型不可用，跳过调用")
            return ""
        
        try:
            # 检查模型是否可用
            models_response = requests.get(f"{self.local_model_endpoint}/api/tags", timeout=10)
            if models_response.status_code != 200:
                print("本地模型服务不可用")
                return ""
            
            available_models = [m['name'] for m in models_response.json().get('models', [])]
            if model not in available_models:
                print(f"指定模型 {model} 不在可用列表中")
                return ""
            
            response = requests.post(
                f"{self.local_model_endpoint}/api/generate",
                json={
                    'model': model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'num_predict': 2048,
                        'temperature': 0.7,
                        'num_ctx': 4096,
                        'num_gpu': 0  # 使用CPU
                    }
                },
                timeout=60  # 增加超时时间
            )
            if response.status_code == 200:
                result = response.json()
                if 'response' in result:
                    return result['response']
                else:
                    print(f"本地模型响应格式异常: {result}")
                    return ""
            else:
                print(f"本地模型调用失败: {response.status_code}, {response.text}")
                return ""
        except requests.exceptions.Timeout:
            print(f"本地模型调用超时，模型可能正在加载中")
            return ""  # 返回空字符串，让调用方决定是否使用备用方案
        except Exception as e:
            print(f"本地模型调用异常: {e}")
            return ""
    
    def call_cloud_model(self, provider: str, model: str, prompt: str) -> str:
        """调用云端模型"""
        try:
            if provider == 'bailian':
                headers = {
                    'Authorization': f"Bearer {self.cloud_providers['bailian']['apiKey']}",
                    'Content-Type': 'application/json'
                }
                data = {
                    'model': model,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 8192
                }
                response = requests.post(
                    f"{self.cloud_providers['bailian']['baseUrl']}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
                )
            elif provider == 'google':
                headers = {
                    'Content-Type': 'application/json'
                }
                data = {
                    'contents': [{'parts': [{'text': prompt}]}],
                    'generationConfig': {
                        'maxOutputTokens': 8192,
                        'temperature': 0.7
                    }
                }
                response = requests.post(
                    f"{self.cloud_providers['google']['baseUrl']}/v1beta/models/{model}:generateContent?key={self.cloud_providers['google']['apiKey']}",
                    headers=headers,
                    json=data,
                    timeout=60
                )
            
            if response.status_code == 200:
                # 解析响应
                result = response.json()
                if provider == 'bailian':
                    return result.get('choices', [{}])[0].get('message', {}).get('content', '')
                elif provider == 'google':
                    return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            else:
                print(f"云端模型调用失败: {response.status_code}")
                return ""
        except Exception as e:
            print(f"云端模型调用异常: {e}")
            return ""
    
    def route_request(self, user_request: str) -> str:
        """
        智能路由主函数 - 改进版
        """
        # 1. 任务分类
        task_type, complexity, tokens = self.classify_task(user_request)
        print(f"任务分类: {task_type}, 复杂度: {complexity}, 估算tokens: {tokens}")
        
        # 2. 模型选择
        model_spec = self.select_model(task_type, complexity, tokens)
        print(f"选择模型: {model_spec}")
        
        # 3. 执行调用
        if model_spec.startswith('local/'):
            model_name = model_spec.split('/', 1)[1]
            result = self.call_local_model(user_request, model_name)
            
            # 如果本地模型调用失败，自动切换到云端
            if not result.strip():
                print("本地模型调用失败，切换到云端模型...")
                # 根据任务类型选择合适的云端模型
                if task_type == 'code':
                    fallback_model = 'bailian/qwen3-coder-plus'
                elif complexity == 'hard' or tokens >= 50000:
                    fallback_model = 'google/gemini-2.5-pro'
                else:
                    fallback_model = 'bailian/qwen3.5-plus'
                
                print(f"使用备用模型: {fallback_model}")
                provider, model_name = fallback_model.split('/', 1)
                result = self.call_cloud_model(provider, model_name, user_request)
        else:
            provider, model_name = model_spec.split('/', 1)
            result = self.call_cloud_model(provider, model_name, user_request)
        
        return result

def main():
    print("=== 增强版智能自动化系统启动 ===\n")
    
    # 创建增强版 AI 路由器
    ai_router = EnhancedSmartAIRouter()
    
    print("测试增强版智能路由...")
    
    # 测试请求处理
    test_request = "简单自我介绍"
    result = ai_router.route_request(test_request)
    
    if result:
        print(f"✅ 请求处理成功!")
        print(f"响应内容: {result[:100]}...")
    else:
        print("❌ 请求处理失败")
    
    print("\n=== 增强版智能自动化系统准备就绪 ===")
    print("主要改进:")
    print("- 改进本地模型可用性检查")
    print("- 自动故障转移（本地→云端）")
    print("- 更好的错误处理和超时控制")
    print("- 改进的任务分类算法")

if __name__ == "__main__":
    main()