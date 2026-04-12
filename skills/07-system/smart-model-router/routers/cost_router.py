"""
成本优先路由策略
目标：最小化成本，优先使用本地模型
"""

from typing import Dict, Any


class CostRouter:
    """成本优先路由器"""
    
    # 模型成本 (每 1000 tokens)
    MODEL_COSTS = {
        'local/qwen2.5:7b': 0.0,
        'local/qwen2.5-coder:7b': 0.0,
        'bailian/qwen3.5-plus': 0.004,
        'bailian/qwen3-coder-plus': 0.005,
        'google/gemini-2.5-pro': 0.025,
    }
    
    def __init__(self, daily_budget: float = 100.0):
        self.daily_budget = daily_budget
        self.spent_today = 0.0
    
    def route(self, task_info: Dict[str, Any]) -> str:
        """
        根据任务信息选择成本最优的模型
        
        Args:
            task_info: 任务信息 {type, complexity, token_estimate}
        
        Returns:
            模型名称
        """
        complexity = task_info.get('complexity', 'medium')
        task_type = task_info.get('type', 'chat')
        token_estimate = task_info.get('token_estimate', 1000)
        
        # 简单任务 → 本地模型
        if complexity == 'easy' and token_estimate < 8000:
            return 'local/qwen2.5:7b'
        
        # 代码任务 → 本地代码模型
        if task_type == 'code':
            return 'local/qwen2.5-coder:7b'
        
        # 长文本/复杂任务 → 云端模型
        if complexity == 'hard' or token_estimate >= 50000:
            # 检查预算
            estimated_cost = (token_estimate / 1000) * self.MODEL_COSTS['google/gemini-2.5-pro']
            if self.spent_today + estimated_cost <= self.daily_budget:
                return 'google/gemini-2.5-pro'
            else:
                # 预算不足，降级到主力模型
                return 'bailian/qwen3.5-plus'
        
        # 默认 → 主力模型
        return 'bailian/qwen3.5-plus'
    
    def record_cost(self, cost: float):
        """记录已花费成本"""
        self.spent_today += cost
    
    def get_remaining_budget(self) -> float:
        """获取剩余预算"""
        return max(0, self.daily_budget - self.spent_today)
