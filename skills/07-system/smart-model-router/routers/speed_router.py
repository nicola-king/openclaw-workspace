"""
速度优先路由策略
目标：最小化延迟，优先使用本地模型
"""

from typing import Dict, Any


class SpeedRouter:
    """速度优先路由器"""
    
    # 模型延迟估计 (毫秒)
    MODEL_LATENCIES = {
        'local/qwen2.5:7b': 80,
        'local/qwen2.5-coder:7b': 100,
        'bailian/qwen3.5-plus': 500,
        'bailian/qwen3-coder-plus': 500,
        'google/gemini-2.5-pro': 1500,
    }
    
    def __init__(self, max_latency_ms: int = 1000):
        self.max_latency_ms = max_latency_ms
    
    def route(self, task_info: Dict[str, Any]) -> str:
        """
        根据任务信息选择速度最快的模型
        
        Args:
            task_info: 任务信息 {type, complexity, token_estimate}
        
        Returns:
            模型名称
        """
        complexity = task_info.get('complexity', 'medium')
        task_type = task_info.get('type', 'chat')
        token_estimate = task_info.get('token_estimate', 1000)
        
        # 简单任务 → 本地模型 (最快)
        if complexity == 'easy':
            if task_type == 'code':
                return 'local/qwen2.5-coder:7b'
            else:
                return 'local/qwen2.5:7b'
        
        # 代码任务 → 本地代码模型
        if task_type == 'code':
            return 'local/qwen2.5-coder:7b'
        
        # 复杂任务 → 检查延迟限制
        if complexity == 'hard' or token_estimate >= 50000:
            # Gemini 延迟超出限制，使用百炼
            if self.MODEL_LATENCIES['google/gemini-2.5-pro'] > self.max_latency_ms:
                return 'bailian/qwen3.5-plus'
            else:
                return 'google/gemini-2.5-pro'
        
        # 默认 → 主力模型
        return 'bailian/qwen3.5-plus'
