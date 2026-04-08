"""
太一技能库 - 智能模型路由引擎
语义分析 · 模型选择 · 成本优化 · 自动执行
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime


class SmartRouter:
    """智能模型路由引擎"""
    
    # 模型分类
    DOMESTIC_MODELS = {
        # 阿里云百炼
        "qwen": "bailian",
        "qwen-turbo": "bailian",
        "qwen-plus": "bailian",
        "qwen-max": "bailian",
        "qwen-coder": "bailian",
        "qwen3.5-plus": "bailian",
        "qwen3-coder-plus": "bailian",
        # DeepSeek
        "deepseek": "deepseek",
        "deepseek-chat": "deepseek",
        "deepseek-coder": "deepseek",
        # Kimi (月之暗面)
        "kimi": "moonshot",
        "kimi-chat": "moonshot",
    }
    
    OVERSEAS_MODELS = {
        # Google
        "gemini": "google",
        "gemini-pro": "google",
        "gemini-2.5-pro": "google",
        # OpenAI
        "gpt": "openai",
        "gpt-4": "openai",
        "gpt-4o": "openai",
        "gpt-3.5-turbo": "openai",
        # Claude (Anthropic)
        "claude": "anthropic",
        "claude-3": "anthropic",
        "claude-sonnet": "anthropic",
    }
    
    # 本地模型
    LOCAL_MODELS = [
        "qwen2.5:7b",
        "qwen2.5-coder:7b",
        "llama3:8b",
    ]
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = Path.home() / '.openclaw' / 'workspace' / 'data' / 'model-router-config.json'
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.usage_stats = self._load_usage_stats()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "default_model": "bailian/qwen3.5-plus",
            "local_priority": True,
            "cost_limit_daily": 100.0,
            "proxy_enabled": True,
            "proxy_url": "http://127.0.0.1:7890",
        }
    
    def _load_usage_stats(self) -> Dict[str, Dict[str, Any]]:
        """加载使用统计"""
        stats_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'model-usage-stats.json'
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_usage_stats(self):
        """保存使用统计"""
        stats_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'model-usage-stats.json'
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.usage_stats, f, indent=2, ensure_ascii=False)
    
    def classify_task(self, user_request: str) -> Dict[str, Any]:
        """
        任务分类
        
        返回：{type, complexity, token_estimate, needs_empathy}
        """
        # 代码任务
        code_keywords = ['写代码', '脚本', 'bug', '编程', 'python', 'javascript', '函数', '类', 'api']
        if any(kw in user_request.lower() for kw in code_keywords):
            return {
                'type': 'code',
                'complexity': self._estimate_complexity(user_request),
                'token_estimate': self._estimate_tokens(user_request),
                'needs_empathy': False
            }
        
        # 长文本任务
        long_text_keywords = ['文档', '报告', '分析', '论文', '文章', '总结', '翻译']
        if any(kw in user_request for kw in long_text_keywords):
            return {
                'type': 'long_text',
                'complexity': 'hard',
                'token_estimate': self._estimate_tokens(user_request) * 5,
                'needs_empathy': False
            }
        
        # 情感支持场景
        emotion_keywords = ['心情', '情绪', '难过', '开心', '压力', '焦虑', '安慰', '鼓励']
        if any(kw in user_request for kw in emotion_keywords):
            return {
                'type': 'emotional',
                'complexity': 'medium',
                'token_estimate': self._estimate_tokens(user_request),
                'needs_empathy': True
            }
        
        # 简单任务
        if len(user_request) < 100 or any(kw in user_request for kw in ['你好', '谢谢', '再见', '帮助']):
            return {
                'type': 'simple',
                'complexity': 'easy',
                'token_estimate': self._estimate_tokens(user_request),
                'needs_empathy': False
            }
        
        # 默认聊天
        return {
            'type': 'chat',
            'complexity': 'medium',
            'token_estimate': self._estimate_tokens(user_request),
            'needs_empathy': False
        }
    
    def _estimate_complexity(self, text: str) -> str:
        """估计任务复杂度"""
        if len(text) < 100:
            return 'easy'
        elif len(text) < 500:
            return 'medium'
        else:
            return 'hard'
    
    def _estimate_tokens(self, text: str) -> int:
        """估计 token 数量 (简单估算：中文字符*1.5 + 英文字符*0.25)"""
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
        return int(chinese_chars * 1.5 + english_chars * 0.25)
    
    def select_model(self, user_request: str, strategy: str = 'balanced') -> str:
        """
        根据任务描述自动选择模型
        
        Args:
            user_request: 任务描述
            strategy: 路由策略 ('cost', 'speed', 'balanced', 'empathy')
        
        Returns:
            最佳模型名称
        """
        # 1. 任务分类
        task_info = self.classify_task(user_request)
        
        # 2. 根据策略选择模型
        if strategy == 'empathy' or task_info['needs_empathy']:
            return self._select_empathy_model(task_info)
        elif strategy == 'cost':
            return self._select_cost_model(task_info)
        elif strategy == 'speed':
            return self._select_speed_model(task_info)
        else:  # balanced
            return self._select_balanced_model(task_info)
    
    def _select_cost_model(self, task_info: Dict[str, Any]) -> str:
        """成本优先：本地模型优先"""
        if task_info['complexity'] == 'easy' and task_info['token_estimate'] < 8000:
            return 'local/qwen2.5:7b'
        elif task_info['type'] == 'code':
            return 'local/qwen2.5-coder:7b'
        else:
            return 'bailian/qwen3.5-plus'
    
    def _select_speed_model(self, task_info: Dict[str, Any]) -> str:
        """速度优先：本地模型优先"""
        if task_info['complexity'] == 'easy':
            return 'local/qwen2.5:7b'
        elif task_info['type'] == 'code':
            return 'local/qwen2.5-coder:7b'
        else:
            return 'bailian/qwen3.5-plus'
    
    def _select_balanced_model(self, task_info: Dict[str, Any]) -> str:
        """平衡策略：成本和质量兼顾"""
        if task_info['complexity'] == 'easy' and task_info['token_estimate'] < 8000:
            return 'local/qwen2.5:7b'
        elif task_info['type'] == 'code':
            return 'bailian/qwen3-coder-plus'
        elif task_info['complexity'] == 'hard' or task_info['token_estimate'] >= 50000:
            return 'google/gemini-2.5-pro'
        else:
            return 'bailian/qwen3.5-plus'
    
    def _select_empathy_model(self, task_info: Dict[str, Any]) -> str:
        """共情路由：选择更温暖的模型配置"""
        # 情感支持场景使用主力模型，确保质量
        return 'bailian/qwen3.5-plus'
    
    def call_model(self, model: str, prompt: str, **kwargs) -> Any:
        """
        调用模型
        
        Args:
            model: 模型名称 (如 'bailian/qwen3.5-plus')
            prompt: 提示词
            **kwargs: 其他参数
        
        Returns:
            模型响应
        """
        # 这里应该调用实际的模型 API
        # 目前返回占位响应
        start_time = time.time()
        
        # 模拟调用
        response = {
            'model': model,
            'prompt': prompt,
            'response': f"[模拟响应] 模型 {model} 已收到请求",
            'tokens_in': self._estimate_tokens(prompt),
            'tokens_out': 100,
            'duration_ms': int((time.time() - start_time) * 1000) + 100,
        }
        
        # 记录用量
        self.record_usage(
            model=model,
            tokens_in=response['tokens_in'],
            tokens_out=response['tokens_out'],
            cost=0.01,  # 模拟成本
            duration_ms=response['duration_ms']
        )
        
        return response
    
    def record_usage(self, model: str, tokens_in: int, tokens_out: int, 
                    cost: float, duration_ms: int):
        """记录模型使用"""
        if model not in self.usage_stats:
            self.usage_stats[model] = {
                'total_calls': 0,
                'total_tokens_in': 0,
                'total_tokens_out': 0,
                'total_cost': 0.0,
                'total_duration_ms': 0,
                'last_used': None,
            }
        
        stats = self.usage_stats[model]
        stats['total_calls'] += 1
        stats['total_tokens_in'] += tokens_in
        stats['total_tokens_out'] += tokens_out
        stats['total_cost'] += cost
        stats['total_duration_ms'] += duration_ms
        stats['last_used'] = datetime.now().isoformat()
        
        # 更新衍生统计
        stats['avg_tokens_in'] = stats['total_tokens_in'] / stats['total_calls']
        stats['avg_tokens_out'] = stats['total_tokens_out'] / stats['total_calls']
        stats['avg_cost'] = stats['total_cost'] / stats['total_calls']
        stats['avg_duration_ms'] = stats['total_duration_ms'] / stats['total_calls']
        
        self._save_usage_stats()
    
    def get_usage_stats(self) -> Dict[str, Dict[str, Any]]:
        """获取使用统计"""
        return self.usage_stats
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        """获取模型信息"""
        # 检查是否为国内模型
        for key, provider in self.DOMESTIC_MODELS.items():
            if key in model.lower():
                return {
                    'name': model,
                    'provider': provider,
                    'type': 'domestic',
                    'requires_proxy': False
                }
        
        # 检查是否为海外模型
        for key, provider in self.OVERSEAS_MODELS.items():
            if key in model.lower():
                return {
                    'name': model,
                    'provider': provider,
                    'type': 'overseas',
                    'requires_proxy': self.config.get('proxy_enabled', True)
                }
        
        # 检查是否为本地模型
        if any(local in model for local in self.LOCAL_MODELS):
            return {
                'name': model,
                'provider': 'local',
                'type': 'local',
                'requires_proxy': False
            }
        
        return {
            'name': model,
            'provider': 'unknown',
            'type': 'unknown',
            'requires_proxy': False
        }


# 便捷函数
def route_request(user_request: str, strategy: str = 'balanced') -> str:
    """便捷函数：路由请求到最佳模型"""
    router = SmartRouter()
    return router.select_model(user_request, strategy)


if __name__ == '__main__':
    # 测试
    router = SmartRouter()
    
    test_cases = [
        "你好",
        "写个 Python 脚本抓取网页",
        "我今天心情不好",
        "分析这份 100 页的文档",
    ]
    
    for task in test_cases:
        model = router.select_model(task)
        print(f"任务：{task}")
        print(f"→ 模型：{model}")
        print()
