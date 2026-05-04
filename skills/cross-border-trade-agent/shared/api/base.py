"""
shared/api/base.py
模块基类定义
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseModule(ABC):
    """所有模块必须继承此类"""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """初始化模块
        
        Args:
            config: 模块配置
            
        Returns:
            初始化是否成功
        """
        pass
    
    @abstractmethod
    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        """执行任务
        
        Args:
            task: 任务类型
            **kwargs: 任务参数
            
        Returns:
            执行结果
        """
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """健康检查
        
        Returns:
            健康状态
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """模块名"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """模块版本"""
        pass
    
    @property
    @abstractmethod
    def dependencies(self) -> List[str]:
        """依赖模块列表"""
        pass


class TaskResult:
    """任务结果封装"""
    
    def __init__(self, status: str, data: Any = None, message: str = ""):
        self.status = status
        self.data = data
        self.message = message
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "data": self.data,
            "message": self.message
        }
    
    @classmethod
    def success(cls, data: Any = None, message: str = "成功") -> 'TaskResult':
        return cls(status="success", data=data, message=message)
    
    @classmethod
    def error(cls, message: str = "失败", data: Any = None) -> 'TaskResult':
        return cls(status="error", data=data, message=message)
