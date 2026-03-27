#!/usr/bin/env python3
"""
智能模型调度器 v2.0
根据任务类型自动分配到最优模型（本地优先）
"""

import requests
import json
from datetime import datetime
from pathlib import Path

class SmartModelRouter:
    """智能模型路由器"""
    
    def __init__(self):
        self.local_endpoint = "http://localhost:11434"
        self.local_model = "qwen2.5:7b-instruct-q4_K_M"
        self.usage_log = Path.home() / ".openclaw" / "workspace" / "memory" / "model-usage-today.md"
        
    def classify_task(self, user_request: str) -> dict:
        """
        自动分类用户请求
        返回：task_type, complexity, token_estimate
        """
        request_lower = user_request.lower()
        
        # 代码任务
        if any(kw in request_lower for kw in ['写代码', '脚本', 'bug', '报错', '实现', 'function', 'def ']):
            return {'type': 'code', 'complexity': 'medium', 'tokens': 5000, 'model': 'qwen3-coder-plus'}
        
        # 简单任务（本地模型）
        if any(kw in request_lower for kw in ['你好', '谢谢', '再见', '翻译', '润色', '优化这句话']):
            return {'type': 'simple', 'complexity': 'easy', 'tokens': 1000, 'model': 'local'}
        
        # 计算/事实查询
        if any(kw in request_lower for kw in ['等于', '计算', '是多少', '首都是', '谁发明了']):
            return {'type': 'fact', 'complexity': 'easy', 'tokens': 500, 'model': 'local'}
        
        # 长文档/报告
        if any(kw in request_lower for kw in ['文档', '报告', '论文', '总结', '摘要']):
            if len(user_request) > 500:  # 长文本
                return {'type': 'long_text', 'complexity': 'hard', 'tokens': 50000, 'model': 'gemini'}
        
        # 搜索/联网
        if any(kw in request_lower for kw in ['搜索', '查找', '最新', '新闻', '天气']):
            return {'type': 'search', 'complexity': 'medium', 'tokens': 10000, 'model': 'qwen3.5-plus'}
        
        # 默认对话
        return {'type': 'chat', 'complexity': 'easy', 'tokens': 500, 'model': 'local'}
    
    def select_model(self, task_info: dict) -> str:
        """
        根据任务信息选择模型
        """
        # 本地模型优先策略
        if task_info['model'] == 'local':
            if task_info['tokens'] < 8000:  # 在本地模型上下文窗口内
                return self.local_model
        
        # 其他情况返回云端模型名称
        return task_info['model']
    
    def call_local_model(self, prompt: str, max_tokens: int = 2048) -> str:
        """调用本地 Qwen 2.5 7B"""
        try:
            response = requests.post(
                f"{self.local_endpoint}/api/generate",
                json={
                    'model': self.local_model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'num_predict': max_tokens,
                        'temperature': 0.7
                    }
                },
                timeout=30
            )
            result = response.json()
            return result.get('response', '')
        except Exception as e:
            # Fallback 到云端
            print(f"本地模型调用失败：{e}，切换到云端")
            return self.call_cloud_model('qwen3.5-plus', prompt)
    
    def call_cloud_model(self, model: str, prompt: str) -> str:
        """调用云端模型（伪代码，实际由 OpenClaw 路由）"""
        # 这里只是占位符，实际调用由 OpenClaw 框架处理
        return f"[云端模型 {model} 调用]"
    
    def log_usage(self, model: str, task_type: str, tokens: int):
        """记录模型使用"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"- {timestamp}: {model} ({task_type}) - {tokens} tokens\n"
        
        self.usage_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.usage_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def execute(self, user_request: str) -> str:
        """
        智能执行：分类 → 选择 → 调用 → 记录
        """
        # Step 1: 分类
        task_info = self.classify_task(user_request)
        
        # Step 2: 选择模型
        selected_model = self.select_model(task_info)
        
        # Step 3: 调用
        if selected_model == self.local_model:
            print(f"🎯 智能路由：本地模型 (Qwen 2.5 7B)")
            result = self.call_local_model(user_request)
        else:
            print(f"☁️ 智能路由：云端模型 ({selected_model})")
            result = self.call_cloud_model(selected_model, user_request)
        
        # Step 4: 记录
        self.log_usage(selected_model, task_info['type'], task_info['tokens'])
        
        return result

# 测试
if __name__ == '__main__':
    router = SmartModelRouter()
    
    print("=" * 60)
    print("  智能模型调度器 v2.0 测试")
    print("=" * 60)
    
    # 测试用例
    test_cases = [
        ("你好，介绍一下你自己", "简单对话 → 本地"),
        ("1+1 等于几？", "事实查询 → 本地"),
        ("把这句话翻译成英文", "翻译 → 本地"),
        ("写一个 Python 脚本计算斐波那契数列", "代码 → 云端"),
        ("总结这份 100 页的报告", "长文档 → Gemini"),
        ("搜索最新的 AI 新闻", "联网搜索 → 云端"),
    ]
    
    for prompt, expected in test_cases:
        print(f"\n测试：{prompt}")
        print(f"预期：{expected}")
        task_info = router.classify_task(prompt)
        model = router.select_model(task_info)
        print(f"路由：{model}")
