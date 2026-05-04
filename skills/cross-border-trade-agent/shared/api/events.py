"""
shared/api/events.py
事件总线 - 模块间通信
"""

import logging
from typing import Dict, Any, List, Callable, Optional
from collections import defaultdict


class EventBus:
    """事件总线"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._logger = logging.getLogger("event-bus")
    
    def subscribe(self, event: str, callback: Callable):
        """订阅事件
        
        Args:
            event: 事件名
            callback: 回调函数
        """
        self._subscribers[event].append(callback)
        self._logger.info(f"订阅事件：{event}")
    
    def unsubscribe(self, event: str, callback: Callable):
        """取消订阅
        
        Args:
            event: 事件名
            callback: 回调函数
        """
        if event in self._subscribers:
            self._subscribers[event].remove(callback)
    
    def publish(self, event: str, data: Any = None):
        """发布事件
        
        Args:
            event: 事件名
            data: 事件数据
        """
        self._logger.info(f"发布事件：{event}")
        
        if event in self._subscribers:
            for callback in self._subscribers[event]:
                try:
                    callback(data)
                except Exception as e:
                    self._logger.error(f"事件回调执行失败：{e}")
    
    def get_subscribers(self, event: str) -> List[Callable]:
        """获取订阅者列表
        
        Args:
            event: 事件名
            
        Returns:
            回调函数列表
        """
        return self._subscribers.get(event, [])
    
    def clear(self):
        """清空所有订阅"""
        self._subscribers.clear()


# 全局事件总线实例
event_bus = EventBus()
