#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能 AI 路由器 - 根据任务和额度自动选择最优模型

功能:
- 任务类型识别
- 复杂度评估
- 额度监控
- 成本优化
- 自动降级
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SmartAIRouter')

class TaskType(Enum):
    """任务类型"""
    CODE = "code"
    TECHNICAL = "technical"
    DOCUMENT = "document"
    ANALYSIS = "analysis"
    SIMPLE = "simple"
    COMPLEX = "complex"
    OFFLINE = "offline"

class Complexity(Enum):
    """任务复杂度"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ModelPriority(Enum):
    """模型优先级"""
    BAILIAN = 1  # 百炼 (已付费 40 元/月，最高优先级)
    GEMINI = 2   # Gemini (免费 1500 次/天)
    LOCAL = 3    # 本地 qwen2.5:7b (完全免费)
    CLAUDE = 4   # Claude (付费，仅特殊场景)
    GPT = 5      # GPT (付费，仅特殊场景)

class SmartAIRouter:
    """智能 AI 路由器"""
    
    def __init__(self):
        # 额度配置
        self.bailian_monthly_fee = 40  # 40 元/月
        self.bailian_monthly_limit = 10000  # 月度额度 (需确认实际值)
        self.bailian_usage_target = 0.90  # 90% 使用目标
        
        self.gemini_daily_limit = 1500  # 1500 次/天
        self.gemini_reserved = 200  # 保留 200 次备用
        
        # 今日使用量
        self.bailian_used_today = 0
        self.gemini_used_today = 0
        
        # 日期追踪
        self.last_reset_date = datetime.now().date()
    
    def reset_if_new_day(self):
        """新的一天重置计数器"""
        today = datetime.now().date()
        if today > self.last_reset_date:
            logger.info("新的一天，重置额度计数器")
            self.bailian_used_today = 0
            self.gemini_used_today = 0
            self.last_reset_date = today
    
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        分析任务
        
        返回:
        {
            'type': TaskType,
            'complexity': Complexity,
            'estimated_tokens': int
        }
        """
        task_lower = task_description.lower()
        
        # 任务类型识别
        if any(kw in task_lower for kw in ['代码', 'code', '编程', 'debug', '函数', 'class', 'def ']):
            task_type = TaskType.CODE
        elif any(kw in task_lower for kw in ['技术', 'technical', '架构', 'api', '文档']):
            task_type = TaskType.TECHNICAL
        elif any(kw in task_lower for kw in ['文档', 'document', '写作', '文章', '文案']):
            task_type = TaskType.DOCUMENT
        elif any(kw in task_lower for kw in ['分析', 'analysis', '数据', '统计', '报表']):
            task_type = TaskType.ANALYSIS
        elif any(kw in task_lower for kw in ['简单', 'simple', '你好', '问候']):
            task_type = TaskType.SIMPLE
        elif any(kw in task_lower for kw in ['复杂', 'complex', '战略', '决策', '多步']):
            task_type = TaskType.COMPLEX
        elif any(kw in task_lower for kw in ['离线', 'offline', '无网络']):
            task_type = TaskType.OFFLINE
        else:
            task_type = TaskType.DOCUMENT  # 默认
        
        # 复杂度评估 (基于长度和关键词)
        task_length = len(task_description)
        if task_length < 50 or task_type == TaskType.SIMPLE:
            complexity = Complexity.LOW
        elif task_length < 500 or task_type in [TaskType.CODE, TaskType.DOCUMENT]:
            complexity = Complexity.MEDIUM
        else:
            complexity = Complexity.HIGH
        
        # 估算 token 数 (粗略估计：1 中文字≈2 tokens)
        estimated_tokens = len(task_description) * 2
        
        result = {
            'type': task_type,
            'complexity': complexity,
            'estimated_tokens': estimated_tokens,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"任务分析：{result}")
        return result
    
    def get_bailian_usage_rate(self) -> float:
        """获取百炼使用率"""
        if self.bailian_monthly_limit <= 0:
            return 0
        return self.bailian_used_today / self.bailian_monthly_limit
    
    def should_use_bailian(self) -> bool:
        """是否应该使用百炼 (已付费，优先使用)"""
        self.reset_if_new_day()
        usage_rate = self.get_bailian_usage_rate()
        
        # 使用率<90%，优先使用 (已付费)
        if usage_rate < self.bailian_usage_target:
            return True
        
        # 还有剩余额度
        remaining = self.bailian_monthly_limit - self.bailian_used_today
        return remaining > 100  # 保留 100 次备用
    
    def should_use_gemini(self) -> bool:
        """是否应该使用 Gemini (免费额度)"""
        self.reset_if_new_day()
        remaining = self.gemini_daily_limit - self.gemini_used_today
        
        # 保留 200 次备用
        return remaining > self.gemini_reserved
    
    def select_model(self, task_description: str) -> str:
        """
        智能选择模型
        
        规则:
        1. 已付费额度优先 (百炼)
        2. 免费额度充分利用 (Gemini)
        3. 本地备用 (qwen2.5:7b)
        4. 付费高端仅特殊场景 (Claude/GPT)
        
        返回:
        'bailian', 'gemini', 'local', 'claude', 或 'gpt'
        """
        # 分析任务
        task_info = self.analyze_task(task_description)
        task_type = task_info['type']
        complexity = task_info['complexity']
        
        # 离线任务 → 本地
        if task_type == TaskType.OFFLINE:
            logger.info("离线任务 → 本地模型")
            return 'local'
        
        # 简单任务 → 本地 (节省额度)
        if task_type == TaskType.SIMPLE or complexity == Complexity.LOW:
            logger.info("简单任务 → 本地模型")
            return 'local'
        
        # 代码/技术任务 → 百炼优先 (已付费)
        if task_type in [TaskType.CODE, TaskType.TECHNICAL]:
            if self.should_use_bailian():
                self.bailian_used_today += 1
                logger.info(f"代码/技术任务 → 百炼 (已付费，使用率{self.get_bailian_usage_rate()*100:.1f}%)")
                return 'bailian'
            else:
                logger.info("百炼额度不足 → 本地降级")
                return 'local'
        
        # 文档/分析 → Gemini (免费)
        if task_type in [TaskType.DOCUMENT, TaskType.ANALYSIS]:
            if self.should_use_gemini():
                self.gemini_used_today += 1
                logger.info(f"文档/分析任务 → Gemini (免费，剩余{self.gemini_daily_limit - self.gemini_used_today}次)")
                return 'gemini'
            else:
                logger.info("Gemini 额度不足 → 本地降级")
                return 'local'
        
        # 复杂战略任务 → Claude/GPT (付费高端)
        if task_type == TaskType.COMPLEX or complexity == Complexity.HIGH:
            logger.info("复杂战略任务 → Claude/GPT (付费高端)")
            return 'claude'  # 默认 Claude
        
        # 默认 → Gemini
        if self.should_use_gemini():
            self.gemini_used_today += 1
            logger.info(f"默认任务 → Gemini")
            return 'gemini'
        else:
            logger.info("默认任务 → 本地降级")
            return 'local'
    
    def get_status_report(self) -> str:
        """获取状态报告"""
        self.reset_if_new_day()
        
        bailian_usage_rate = self.get_bailian_usage_rate()
        gemini_remaining = self.gemini_daily_limit - self.gemini_used_today
        
        report = f"""
🤖 智能 AI 路由器状态
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━ 额度使用情况 ━━━

百炼 Coding (40 元/月):
  已用：{self.bailian_used_today}/{self.bailian_monthly_limit}
  使用率：{bailian_usage_rate*100:.1f}%
  目标：90%
  状态：{'✅ 充分利用' if bailian_usage_rate >= 0.85 else '⚠️ 需增加使用'}

Gemini (免费):
  已用：{self.gemini_used_today}/{self.gemini_daily_limit}
  剩余：{gemini_remaining}
  状态：{'✅ 充足' if gemini_remaining > 500 else '⚠️ 紧张'}

━━━ 调度策略 ━━━

优先级:
1. 百炼 (已付费 40 元) ⭐⭐⭐⭐⭐
2. Gemini (免费) ⭐⭐⭐⭐⭐
3. 本地 qwen2.5:7b ⭐⭐⭐⭐
4. Claude/GPT (付费) ⭐

成本估算:
  百炼：40 元/月 (已付费)
  Gemini: ¥0 (免费)
  本地：¥0 (免费)
  月度总成本：≈40 元
"""
        return report


def main():
    """测试主函数"""
    router = SmartAIRouter()
    
    # 测试用例
    test_tasks = [
        "写一个 Python 函数，计算斐波那契数列",
        "分析这份销售数据，找出趋势",
        "你好",
        "写一篇关于 AI 的技术文档",
        "制定公司 3 年战略规划，考虑市场、技术、人才等多因素",
        "离线模式下如何备份数据",
    ]
    
    print("🤖 智能 AI 路由器测试\n")
    print("=" * 60)
    
    for task in test_tasks:
        print(f"\n任务：{task}")
        print("-" * 60)
        model = router.select_model(task)
        print(f"✅ 选择模型：{model}")
    
    print("\n" + "=" * 60)
    print("\n📊 状态报告:")
    print(router.get_status_report())


if __name__ == '__main__':
    main()
