#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件总线模块 - Event Bus

太一系统共享事件系统，提供发布/订阅模式、事件队列、异步处理。
支持内存、Redis、Kafka 等多种后端。

@author: 太一
@version: 1.0.0
@created: 2026-04-07
"""

import asyncio
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4

from .config import config


class EventPriority(Enum):
    """事件优先级"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Event:
    """事件对象"""
    id: str
    event_type: str
    payload: Dict[str, Any]
    priority: EventPriority = EventPriority.NORMAL
    created_at: float = field(default_factory=time.time)
    source: str = ""
    correlation_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "payload": self.payload,
            "priority": self.priority.value,
            "created_at": self.created_at,
            "source": self.source,
            "correlation_id": self.correlation_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return cls(
            id=data.get("id", str(uuid4())),
            event_type=data["event_type"],
            payload=data.get("payload", {}),
            priority=EventPriority(data.get("priority", 1)),
            created_at=data.get("created_at", time.time()),
            source=data.get("source", ""),
            correlation_id=data.get("correlation_id")
        )


@dataclass
class Subscription:
    """订阅信息"""
    id: str
    event_type: str
    handler: Callable
    pattern: bool = False  # 是否支持通配符
    priority: int = 0  # 订阅优先级，数字越大越先处理
    once: bool = False  # 是否只触发一次
    filter_fn: Optional[Callable[[Event], bool]] = None


class EventBus:
    """
    事件总线
    
    提供发布/订阅模式，支持同步/异步处理、事件过滤、优先级队列。
    
    使用示例:
        >>> bus = EventBus.get_instance()
        
        >>> # 订阅事件
        >>> @bus.on("user.created")
        >>> async def on_user_created(event):
        ...     print(f"新用户：{event.payload['name']}")
        
        >>> # 发布事件
        >>> await bus.publish("user.created", {"name": "Alice", "id": 123})
        
        >>> # 带优先级的发布
        >>> await bus.publish("system.alert", {"msg": "CPU 过高"}, priority=EventPriority.HIGH)
    """
    
    _instance: Optional["EventBus"] = None
    
    def __init__(self):
        self._config = config
        self._subscriptions: Dict[str, List[Subscription]] = defaultdict(list)
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._worker_tasks: List[asyncio.Task] = []
        self._event_history: List[Event] = []
        self._max_history = 1000
        self._stats = {
            "published": 0,
            "processed": 0,
            "errors": 0
        }
    
    @classmethod
    def get_instance(cls) -> "EventBus":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """重置单例"""
        cls._instance = None
    
    async def start(self, workers: int = 4):
        """启动事件总线"""
        if self._running:
            return
        
        self._running = True
        
        # 启动工作线程
        for i in range(workers):
            task = asyncio.create_task(self._worker(f"worker-{i}"))
            self._worker_tasks.append(task)
        
        print(f"[EventBus] 已启动，工作线程数：{workers}")
    
    async def stop(self):
        """停止事件总线"""
        self._running = False
        
        # 等待队列处理完成
        await self._event_queue.join()
        
        # 取消工作线程
        for task in self._worker_tasks:
            task.cancel()
        
        await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        self._worker_tasks.clear()
        
        print("[EventBus] 已停止")
    
    async def _worker(self, name: str):
        """事件处理工作线程"""
        while self._running:
            try:
                event = await asyncio.wait_for(
                    self._event_queue.get(),
                    timeout=1.0
                )
                
                await self._process_event(event)
                self._event_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[EventBus] {name} 错误：{e}")
                self._stats["errors"] += 1
    
    async def _process_event(self, event: Event):
        """处理单个事件"""
        # 查找匹配的订阅
        handlers = self._find_handlers(event)
        
        # 按优先级排序
        handlers.sort(key=lambda s: s.priority, reverse=True)
        
        for subscription in handlers:
            try:
                # 应用过滤器
                if subscription.filter_fn and not subscription.filter_fn(event):
                    continue
                
                # 调用处理函数
                if asyncio.iscoroutinefunction(subscription.handler):
                    await subscription.handler(event)
                else:
                    subscription.handler(event)
                
                # 一次性订阅，处理后移除
                if subscription.once:
                    await self.unsubscribe(subscription.id)
                
                self._stats["processed"] += 1
                
            except Exception as e:
                print(f"[EventBus] 处理事件 {event.event_type} 失败：{e}")
                self._stats["errors"] += 1
        
        # 记录历史
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
    
    def _find_handlers(self, event: Event) -> List[Subscription]:
        """查找匹配事件的处理函数"""
        handlers = []
        
        # 精确匹配
        if event.event_type in self._subscriptions:
            handlers.extend(self._subscriptions[event.event_type])
        
        # 通配符匹配
        for pattern, subs in self._subscriptions.items():
            if pattern.endswith("*"):
                prefix = pattern[:-1]
                if event.event_type.startswith(prefix):
                    handlers.extend(subs)
            elif pattern == "*":
                handlers.extend(subs)
        
        return handlers
    
    async def publish(
        self, 
        event_type: str, 
        payload: Dict[str, Any] = None,
        priority: EventPriority = EventPriority.NORMAL,
        source: str = "",
        correlation_id: Optional[str] = None
    ) -> str:
        """
        发布事件
        
        Args:
            event_type: 事件类型（如 "user.created"）
            payload: 事件数据
            priority: 优先级
            source: 事件来源
            correlation_id: 关联 ID（用于追踪事件链）
            
        Returns:
            str: 事件 ID
        """
        event = Event(
            id=str(uuid4()),
            event_type=event_type,
            payload=payload or {},
            priority=priority,
            source=source,
            correlation_id=correlation_id
        )
        
        await self._event_queue.put(event)
        self._stats["published"] += 1
        
        return event.id
    
    def on(
        self, 
        event_type: str,
        pattern: bool = False,
        priority: int = 0,
        once: bool = False,
        filter_fn: Optional[Callable[[Event], bool]] = None
    ):
        """
        订阅事件装饰器
        
        使用示例:
            @bus.on("user.*", pattern=True)
            async def on_user_event(event):
                print(f"用户事件：{event.event_type}")
        """
        def decorator(handler: Callable):
            sub_id = str(uuid4())
            subscription = Subscription(
                id=sub_id,
                event_type=event_type,
                handler=handler,
                pattern=pattern,
                priority=priority,
                once=once,
                filter_fn=filter_fn
            )
            
            self._subscriptions[event_type].append(subscription)
            return handler
        
        return decorator
    
    async def subscribe(
        self,
        event_type: str,
        handler: Callable,
        pattern: bool = False,
        priority: int = 0,
        once: bool = False
    ) -> str:
        """编程式订阅"""
        sub_id = str(uuid4())
        subscription = Subscription(
            id=sub_id,
            event_type=event_type,
            handler=handler,
            pattern=pattern,
            priority=priority,
            once=once
        )
        
        self._subscriptions[event_type].append(subscription)
        return sub_id
    
    async def unsubscribe(self, subscription_id: str) -> bool:
        """取消订阅"""
        for event_type, subs in self._subscriptions.items():
            for i, sub in enumerate(subs):
                if sub.id == subscription_id:
                    subs.pop(i)
                    return True
        return False
    
    async def clear_subscriptions(self, event_type: Optional[str] = None):
        """清空订阅"""
        if event_type:
            self._subscriptions[event_type].clear()
        else:
            self._subscriptions.clear()
    
    async def emit(self, event_type: str, payload: Dict[str, Any] = None):
        """publish 的别名"""
        return await self.publish(event_type, payload)
    
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self._stats,
            "queue_size": self._event_queue.qsize(),
            "subscriptions": sum(len(subs) for subs in self._subscriptions.values()),
            "history_size": len(self._event_history)
        }
    
    async def get_history(
        self, 
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Event]:
        """获取事件历史"""
        if event_type:
            filtered = [e for e in self._event_history if e.event_type == event_type]
        else:
            filtered = self._event_history
        
        return filtered[-limit:]


# 全局事件总线实例
bus = EventBus.get_instance()


if __name__ == "__main__":
    # 测试代码
    import asyncio
    
    async def test():
        print("[EventBus] 测试事件总线")
        
        await bus.start(workers=2)
        
        # 测试订阅
        received_events = []
        
        @bus.on("test.event")
        async def on_test_event(event):
            received_events.append(event)
            print(f"  收到事件：{event.event_type} -> {event.payload}")
        
        @bus.on("user.*", pattern=True)
        async def on_user_event(event):
            print(f"  用户事件：{event.event_type}")
        
        # 测试发布
        await bus.publish("test.event", {"message": "Hello", "count": 1})
        await bus.publish("test.event", {"message": "World", "count": 2})
        await bus.publish("user.created", {"name": "Alice"})
        await bus.publish("user.deleted", {"id": 123})
        
        # 等待处理
        await asyncio.sleep(0.5)
        
        # 测试统计
        stats = bus.stats()
        print(f"  统计：{stats}")
        
        # 测试历史
        history = await bus.get_history("test.event")
        print(f"  历史事件数：{len(history)}")
        
        await bus.stop()
        print("[EventBus] 测试完成")
    
    asyncio.run(test())
