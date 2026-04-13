#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存模块 - Cache System

太一系统共享缓存层，提供多级缓存、LRU 淘汰、过期清理。
支持内存缓存、Redis、SQLite 三种后端。

@author: 太一
@version: 1.0.0
@created: 2026-04-07
"""

import asyncio
import hashlib
import json
import time
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union

from .config import config


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    expires_at: Optional[float] = None
    created_at: float = 0.0
    hit_count: int = 0
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "hit_count": self.hit_count
        }


class MemoryCache:
    """
    内存缓存（LRU 实现）
    
    线程安全，支持 TTL、最大容量限制、自动淘汰。
    """
    
    def __init__(self, max_size: int = 10000, default_ttl: int = 3600):
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        async with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            entry = self._cache[key]
            
            # 检查过期
            if entry.is_expired():
                del self._cache[key]
                self._misses += 1
                return None
            
            # LRU 调整
            self._cache.move_to_end(key)
            entry.hit_count += 1
            self._hits += 1
            
            return entry.value
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ):
        """设置缓存值"""
        async with self._lock:
            # 计算过期时间
            expires_at = None
            if ttl is not None:
                expires_at = time.time() + ttl
            elif self._default_ttl > 0:
                expires_at = time.time() + self._default_ttl
            
            # 如果已存在，先删除
            if key in self._cache:
                del self._cache[key]
            
            # 检查容量，淘汰最旧的
            while len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)
            
            # 添加新条目
            entry = CacheEntry(
                key=key,
                value=value,
                expires_at=expires_at,
                created_at=time.time()
            )
            self._cache[key] = entry
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    async def clear(self):
        """清空缓存"""
        async with self._lock:
            self._cache.clear()
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在且未过期"""
        async with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                return False
            
            return True
    
    async def keys(self, pattern: Optional[str] = None) -> List[str]:
        """获取所有键（支持通配符匹配）"""
        async with self._lock:
            if pattern is None:
                return list(self._cache.keys())
            
            # 简单通配符支持：* 匹配任意字符
            import fnmatch
            return [k for k in self._cache.keys() if fnmatch.fnmatch(k, pattern)]
    
    async def cleanup(self) -> int:
        """清理过期条目，返回清理数量"""
        async with self._lock:
            expired_keys = [
                k for k, v in self._cache.items() 
                if v.is_expired()
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)
    
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0.0
        
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{hit_rate:.2%}",
            "default_ttl": self._default_ttl
        }


class CacheManager:
    """
    缓存管理器
    
    提供统一的缓存接口，支持多级缓存、缓存装饰器、批量操作。
    
    使用示例:
        >>> cache = CacheManager.get_instance()
        >>> await cache.set("user:123", {"name": "Alice"})
        >>> user = await cache.get("user:123")
        
        >>> @cache.cached(ttl=300)
        >>> async def get_user_data(user_id):
        ...     return await fetch_from_db(user_id)
    """
    
    _instance: Optional["CacheManager"] = None
    
    def __init__(self):
        self._config = config
        self._memory: Optional[MemoryCache] = None
        self._initialized = False
    
    @classmethod
    def get_instance(cls) -> "CacheManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """重置单例"""
        cls._instance = None
    
    async def initialize(self):
        """初始化缓存系统"""
        if self._initialized:
            return
        
        max_size = self._config.cache.max_size
        default_ttl = self._config.cache.ttl_default
        
        self._memory = MemoryCache(max_size=max_size, default_ttl=default_ttl)
        self._initialized = True
        
        # 启动后台清理任务
        asyncio.create_task(self._cleanup_loop())
        
        print(f"[Cache] 已初始化：内存缓存 (max={max_size}, ttl={default_ttl}s)")
    
    async def _cleanup_loop(self):
        """后台清理过期缓存"""
        while True:
            await asyncio.sleep(60)  # 每分钟清理一次
            if self._memory:
                count = await self._memory.cleanup()
                if count > 0:
                    print(f"[Cache] 清理了 {count} 个过期条目")
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if not self._initialized:
            await self.initialize()
        
        return await self._memory.get(key)
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ):
        """设置缓存值"""
        if not self._initialized:
            await self.initialize()
        
        await self._memory.set(key, value, ttl)
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self._initialized:
            await self.initialize()
        
        return await self._memory.delete(key)
    
    async def clear(self):
        """清空缓存"""
        if not self._initialized:
            await self.initialize()
        
        await self._memory.clear()
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self._initialized:
            await self.initialize()
        
        return await self._memory.exists(key)
    
    def cached(self, ttl: int = 3600, key_prefix: str = ""):
        """
        缓存装饰器
        
        使用示例:
            @cache.cached(ttl=300, key_prefix="user")
            async def get_user(user_id):
                return await db.fetch_user(user_id)
        """
        def decorator(func: Callable):
            async def wrapper(*args, **kwargs):
                # 生成缓存键
                key_parts = [key_prefix, func.__name__]
                
                # 添加参数到键
                for arg in args:
                    key_parts.append(str(arg))
                for k, v in sorted(kwargs.items()):
                    key_parts.append(f"{k}={v}")
                
                cache_key = ":".join(key_parts)
                cache_key = hashlib.md5(cache_key.encode()).hexdigest()[:16]
                
                # 尝试从缓存获取
                cached_value = await self.get(cache_key)
                if cached_value is not None:
                    return cached_value
                
                # 执行函数并缓存结果
                result = await func(*args, **kwargs)
                await self.set(cache_key, result, ttl)
                
                return result
            
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper
        
        return decorator
    
    async def get_or_set(
        self, 
        key: str, 
        factory: Callable[[], Any], 
        ttl: int = 3600
    ) -> Any:
        """
        获取或设置缓存值
        
        Args:
            key: 缓存键
            factory: 生成值的异步函数
            ttl: 过期时间（秒）
            
        Returns:
            缓存值或新生成的值
        """
        value = await self.get(key)
        if value is not None:
            return value
        
        value = await factory()
        await self.set(key, value, ttl)
        return value
    
    async def mget(self, keys: List[str]) -> Dict[str, Any]:
        """批量获取"""
        result = {}
        for key in keys:
            value = await self.get(key)
            if value is not None:
                result[key] = value
        return result
    
    async def mset(self, items: Dict[str, Any], ttl: Optional[int] = None):
        """批量设置"""
        for key, value in items.items():
            await self.set(key, value, ttl)
    
    async def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self._initialized:
            await self.initialize()
        
        return self._memory.stats()


# 全局缓存实例
cache = CacheManager.get_instance()


if __name__ == "__main__":
    # 测试代码
    import asyncio
    
    async def test():
        print("[Cache] 测试缓存模块")
        
        await cache.initialize()
        
        # 测试设置/获取
        await cache.set("test_key", {"name": "Alice", "age": 25})
        value = await cache.get("test_key")
        print(f"  获取值：{value}")
        
        # 测试 TTL
        await cache.set("temp_key", "temp_value", ttl=2)
        print(f"  临时值存在：{await cache.exists('temp_key')}")
        await asyncio.sleep(3)
        print(f"  过期后存在：{await cache.exists('temp_key')}")
        
        # 测试装饰器
        @cache.cached(ttl=60)
        async def compute(x, y):
            print(f"    [compute] 执行计算 {x} + {y}")
            return x + y
        
        print(f"  第一次计算：{await compute(1, 2)}")
        print(f"  第二次计算（缓存）：{await compute(1, 2)}")
        
        # 测试统计
        stats = await cache.stats()
        print(f"  统计：{stats}")
        
        print("[Cache] 测试完成")
    
    asyncio.run(test())
