# 太一 PDCA 定时任务自进化智能体

> **版本**: v3.0 (PDCA 循环版)  
> **创建时间**: 2026-04-15  
> **作者**: 太一 AGI

"""
太一 PDCA 定时任务自进化智能体

基于 PDCA 循环 (Plan-Do-Check-Act):
1. P - Plan: 计划引擎 - 任务规划与调度
2. D - Do: 执行引擎 - 任务自动执行
3. C - Check: 检查引擎 - 结果智能验证
4. A - Act: 纠偏引擎 - 异常自动修复 + 优化
5. 持续改进：经验沉淀 + 知识蒸馏 + 策略进化
"""

from .core import PDCAchedulerAgent, PlanEngine, DoEngine, CheckEngine, ActEngine

__version__ = "3.0.0"
__all__ = [
    "PDCAchedulerAgent",
    "PlanEngine",
    "DoEngine",
    "CheckEngine",
    "ActEngine"
]
