"""
Auto-Exec Skill - 智能自动执行引擎

导出所有模块，提供统一 API
"""

from .core import AutoExecStatus, TaskDiscovery, status, discover_tasks, update_status
from .reporter import ProgressReporter

__version__ = "1.0.0"
__all__ = [
    "AutoExecStatus",
    "TaskDiscovery",
    "ProgressReporter",
    "status",
    "discover_tasks",
    "update_status"
]
