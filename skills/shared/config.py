#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块 - Configuration Manager

太一系统共享配置中心，统一管理所有模块的配置项。
支持环境变量、配置文件、动态重载。

@author: 太一
@version: 1.0.0
@created: 2026-04-07
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class DatabaseConfig:
    """数据库配置"""
    host: str = "localhost"
    port: int = 5432
    database: str = "taiyi"
    user: str = "taiyi"
    password: str = ""
    pool_size: int = 10
    max_overflow: int = 20


@dataclass
class CacheConfig:
    """缓存配置"""
    backend: str = "redis"  # redis | memory | sqlite
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    ttl_default: int = 3600  # 默认 TTL 1 小时
    max_size: int = 10000  # 内存缓存最大条目数


@dataclass
class EventBusConfig:
    """事件总线配置"""
    backend: str = "memory"  # memory | redis | kafka
    host: str = "localhost"
    port: int = 6379
    channel_prefix: str = "taiyi"
    max_queue_size: int = 10000


@dataclass
class SystemConfig:
    """系统级配置"""
    workspace: str = "/home/nicola/.openclaw/workspace"
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    timezone: str = "Asia/Shanghai"
    debug: bool = False


class ConfigManager:
    """
    配置管理器
    
    单例模式，提供全局配置访问和动态重载能力。
    
    使用示例:
        >>> config = ConfigManager.get_instance()
        >>> db_host = config.get("database.host")
        >>> config.set("debug", True)
        >>> config.reload()  # 从文件重新加载
    """
    
    _instance: Optional["ConfigManager"] = None
    _config_path: Path = Path(__file__).parent / "config.json"
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.cache = CacheConfig()
        self.event_bus = EventBusConfig()
        self.system = SystemConfig()
        self._dynamic: Dict[str, Any] = {}
        self._load_from_env()
    
    @classmethod
    def get_instance(cls) -> "ConfigManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """重置单例（用于测试）"""
        cls._instance = None
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        # 数据库配置
        if os.getenv("TAIYI_DB_HOST"):
            self.database.host = os.getenv("TAIYI_DB_HOST")
        if os.getenv("TAIYI_DB_PORT"):
            self.database.port = int(os.getenv("TAIYI_DB_PORT"))
        if os.getenv("TAIYI_DB_NAME"):
            self.database.database = os.getenv("TAIYI_DB_NAME")
        if os.getenv("TAIYI_DB_USER"):
            self.database.user = os.getenv("TAIYI_DB_USER")
        if os.getenv("TAIYI_DB_PASSWORD"):
            self.database.password = os.getenv("TAIYI_DB_PASSWORD")
        
        # 缓存配置
        if os.getenv("TAIYI_CACHE_HOST"):
            self.cache.host = os.getenv("TAIYI_CACHE_HOST")
        if os.getenv("TAIYI_CACHE_PORT"):
            self.cache.port = int(os.getenv("TAIYI_CACHE_PORT"))
        if os.getenv("TAIYI_CACHE_TTL"):
            self.cache.ttl_default = int(os.getenv("TAIYI_CACHE_TTL"))
        
        # 系统配置
        if os.getenv("TAIYI_WORKSPACE"):
            self.system.workspace = os.getenv("TAIYI_WORKSPACE")
        if os.getenv("TAIYI_LOG_LEVEL"):
            self.system.log_level = os.getenv("TAIYI_LOG_LEVEL")
        if os.getenv("TAIYI_DEBUG"):
            self.system.debug = os.getenv("TAIYI_DEBUG").lower() == "true"
    
    def load_from_file(self, path: Optional[Path] = None) -> bool:
        """
        从 JSON 文件加载配置
        
        Args:
            path: 配置文件路径，默认使用 config.json
            
        Returns:
            bool: 加载是否成功
        """
        config_path = path or self._config_path
        if not config_path.exists():
            return False
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "database" in data:
                for k, v in data["database"].items():
                    if hasattr(self.database, k):
                        setattr(self.database, k, v)
            
            if "cache" in data:
                for k, v in data["cache"].items():
                    if hasattr(self.cache, k):
                        setattr(self.cache, k, v)
            
            if "event_bus" in data:
                for k, v in data["event_bus"].items():
                    if hasattr(self.event_bus, k):
                        setattr(self.event_bus, k, v)
            
            if "system" in data:
                for k, v in data["system"].items():
                    if hasattr(self.system, k):
                        setattr(self.system, k, v)
            
            if "dynamic" in data:
                self._dynamic.update(data["dynamic"])
            
            return True
        except Exception as e:
            print(f"[Config] 加载配置文件失败：{e}")
            return False
    
    def save_to_file(self, path: Optional[Path] = None) -> bool:
        """保存配置到 JSON 文件"""
        config_path = path or self._config_path
        
        try:
            data = {
                "database": {k: v for k, v in vars(self.database).items() if not k.startswith("_")},
                "cache": {k: v for k, v in vars(self.cache).items() if not k.startswith("_")},
                "event_bus": {k: v for k, v in vars(self.event_bus).items() if not k.startswith("_")},
                "system": {k: v for k, v in vars(self.system).items() if not k.startswith("_")},
                "dynamic": self._dynamic
            }
            
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"[Config] 保存配置文件失败：{e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值（支持点号分隔的嵌套路径）
        
        Args:
            key: 配置键，如 "database.host" 或 "debug"
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        parts = key.split(".")
        
        # 动态配置
        if len(parts) == 1 and key in self._dynamic:
            return self._dynamic[key]
        
        # 预定义配置组
        if len(parts) >= 2:
            group_name = parts[0]
            attr_name = parts[1]
            
            if hasattr(self, group_name):
                group = getattr(self, group_name)
                if hasattr(group, attr_name):
                    return getattr(group, attr_name)
        
        return default
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self._dynamic[key] = value
    
    def reload(self) -> bool:
        """重新加载配置（从环境变量 + 文件）"""
        self._load_from_env()
        return self.load_from_file()
    
    def to_dict(self) -> Dict[str, Any]:
        """导出配置为字典"""
        return {
            "database": vars(self.database),
            "cache": vars(self.cache),
            "event_bus": vars(self.event_bus),
            "system": vars(self.system),
            "dynamic": self._dynamic
        }


# 全局配置实例
config = ConfigManager.get_instance()


if __name__ == "__main__":
    # 测试代码
    print("[Config] 测试配置模块")
    print(f"  工作目录：{config.system.workspace}")
    print(f"  日志级别：{config.system.log_level}")
    print(f"  调试模式：{config.system.debug}")
    print(f"  数据库：{config.database.host}:{config.database.port}/{config.database.database}")
    print(f"  缓存：{config.cache.backend}@{config.cache.host}:{config.cache.port}")
