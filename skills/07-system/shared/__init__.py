#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一共享层 - Taiyi Shared Layer

所有技能共享的底层基础设施，提供配置、数据库、缓存、事件总线能力。

@author: 太一
@version: 1.0.0
@created: 2026-04-07

使用示例:
    >>> from skills.shared import config, db, cache, bus
    >>> 
    >>> # 配置
    >>> db_host = config.get("database.host")
    >>> 
    >>> # 数据库
    >>> await db.connect()
    >>> await db.insert("users", {"name": "Alice"})
    >>> 
    >>> # 缓存
    >>> await cache.initialize()
    >>> await cache.set("key", "value", ttl=3600)
    >>> 
    >>> # 事件总线
    >>> await bus.start()
    >>> await bus.publish("user.created", {"name": "Alice"})
"""

from .config import config, ConfigManager
from .database import db, DatabasePool
from .cache import cache, CacheManager
from .event_bus import bus, EventBus, Event, EventPriority

__all__ = [
    # 配置
    'config',
    'ConfigManager',
    
    # 数据库
    'db',
    'DatabasePool',
    
    # 缓存
    'cache',
    'CacheManager',
    
    # 事件总线
    'bus',
    'EventBus',
    'Event',
    'EventPriority',
]

__version__ = '1.0.0'
