"""
太一旅行探路者 - 模块化自进化旅行规划系统 v2.0

模块列表:
- planner: 智能行程规划
- router_core: 多城路线优化
- deals: 优惠发现
- ground: 地接服务
- provider: 供应商管理
- distill: 信息蒸馏（9源融合）
- evolve: 自进化引擎
- push: 多平台推送
- destination: 目的地注意事项
- dual_mode: 双模式策略
- learn: 知识自动学习
"""

__version__ = "2.0.0"
__author__ = "太一 AGI"

from src.router import TravelRouter
from src.planner.engine import PlannerEngine
from src.evolve.experience_store import ExperienceStore

__all__ = [
    "TravelRouter",
    "PlannerEngine",
    "ExperienceStore",
]
