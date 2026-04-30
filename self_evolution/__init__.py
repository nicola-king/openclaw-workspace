# OpenClaw 全域自进化模块

> **版本**: v1.0  
> **创建时间**: 2026-04-14  
> **作者**: 太一 AGI

"""
OpenClaw 全域自进化模块

包含 5 大进化维度:
1. 配置自进化
2. 技能自进化
3. 会话自进化
4. 工作流自进化
5. 记忆自进化
"""

from .core import OpenClawEvolution, ConfigEvolution, SkillEvolution, SessionEvolution, WorkflowEvolution, MemoryEvolution

__version__ = "1.0.0"
__all__ = [
    "OpenClawEvolution",
    "ConfigEvolution",
    "SkillEvolution",
    "SessionEvolution",
    "WorkflowEvolution",
    "MemoryEvolution"
]
