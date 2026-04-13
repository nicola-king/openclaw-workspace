#!/usr/bin/env python3
"""
Quota-Aware Model Router - 额度感知智能路由 v1.0

核心原则:
1. 百炼 coding plan 为主 (优先级 1)
2. 百炼≥95% → 切换 Gemini+ 本地
3. Gemini≥95% → 切换本地 + 百炼
4. 百炼恢复 → 强制切回 (不管 Gemini)
5. 双耗尽 → 强制本地兜底
6. 自动监控·自动切换·自动通知

作者：太一 AGI
创建：2026-04-08
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum

# 配置路径
CONFIG_DIR = Path(__file__).parent / "config"
CACHE_DIR = Path(__file__).parent / "cache"


class ModelState(Enum):
    """模型状态"""
    BAILIAN_PRIMARY = "bailian_primary"
    GEMINI_BACKUP = "gemini_backup"
    LOCAL_FALLBACK = "local_fallback"


@dataclass
class QuotaStatus:
    """额度状态"""
    model: str
    used: int
    limit: int
    usage_rate: float
    available: bool
    reset_time: Optional[str] = None


@dataclass
class SystemStatus:
    """系统状态"""
    state: ModelState
    bailian: QuotaStatus
    gemini: QuotaStatus
    current_model: str
    last_switch_time: Optional[str] = None
    switch_count_today: int = 0


class QuotaRouter:
    """额度感知智能路由器"""
    
    def __init__(self):
        self.config = self.load_config()
        self.cache = self.load_cache()
        self.state = ModelState.BAILIAN_PRIMARY
        self.last_check = 0
        self.switch_count = 0
        
        self.bailian_key = os.getenv("BAILIAN_API_KEY", "")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        
        self.WARNING_THRESHOLD = 0.90
        self.SWITCH_THRESHOLD = 0.95
        
    def load_config(self) -> Dict:
        """加载配置"""
        config_file = CONFIG_DIR / "quota_config.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "bailian": {"enabled": True, "daily_limit": 100000},
            "gemini": {"enabled": True, "daily_limit": 1000},
            "local": {"enabled": True, "model": "qwen2.5:7b"},
            "monitor": {"check_interval": 300, "auto_switch": True}
        }
    
    def load_cache(self) -> Dict:
        """加载缓存"""
        cache_file = CACHE_DIR / "quota_cache.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"bailian": {}, "gemini": {}}
    
    def save_cache(self):
        """保存缓存"""
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / "quota_cache.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def check_bailian_quota(self) -> QuotaStatus:
        """检查百炼额度"""
        now = time.time()
        if now - self.last_check < 60:
            if "bailian" in self.cache and "status" in self.cache["bailian"]:
                cached = self.cache["bailian"]["status"]
                if cached.get("timestamp", 0) + 60 > now:
                    return QuotaStatus(**cached["data"])
        
        used = self.cache.get("bailian", {}).get("used", 0)
        limit = self.config["bailian"]["daily_limit"]
        usage_rate = used / limit if limit > 0 else 0
        
        status = QuotaStatus(
            model="bailian/qwen3.5-plus",
            used=used,
            limit=limit,
            usage_rate=usage_rate,
            available=usage_rate < 0.95,
            reset_time="00:00:00"
        )
        
        self.cache["bailian"] = {
            "status": {"data": asdict(status), "timestamp": now},
            "used": used
        }
        self.save_cache()
        self.last_check = now
        
        return status
    
    def check_gemini_quota(self) -> QuotaStatus:
        """检查 Gemini 额度"""
        now = time.time()
        
        if "gemini" in self.cache and "status" in self.cache["gemini"]:
            cached = self.cache["gemini"]["status"]
            if cached.get("timestamp", 0) + 60 > now:
                return QuotaStatus(**cached["data"])
        
        used = self.cache.get("gemini", {}).get("used", 0)
        limit = self.config["gemini"]["daily_limit"]
        usage_rate = used / limit if limit > 0 else 0
        
        status = QuotaStatus(
            model="gemini/gemini-2.5-flash",
            used=used,
            limit=limit,
            usage_rate=usage_rate,
            available=usage_rate < 0.95,
            reset_time="00:00:00 (UTC)"
        )
        
        self.cache["gemini"] = {
            "status": {"data": asdict(status), "timestamp": now},
            "used": used
        }
        self.save_cache()
        
        return status
    
    def select_model(self, task_type: str = "conversation", complexity: str = "normal") -> str:
        """根据额度自动选择模型"""
        bailian_status = self.check_bailian_quota()
        gemini_status = self.check_gemini_quota()
        
        if bailian_status.available:
            self.state = ModelState.BAILIAN_PRIMARY
            if task_type == "code":
                return "bailian/qwen3-coder-plus"
            return "bailian/qwen3.5-plus"
        
        elif gemini_status.available:
            self.state = ModelState.GEMINI_BACKUP
            return "gemini/gemini-2.5-flash"
        
        else:
            self.state = ModelState.LOCAL_FALLBACK
            if task_type == "code":
                return "local/qwen2.5-coder:7b"
            return "local/qwen2.5:7b"
    
    def force_switch_to(self, model: str):
        """强制切换到指定模型"""
        print(f"🔄 强制切换：{model}")
        self.switch_count += 1
        self.send_notification("force_switch", model)
    
    def check_and_switch(self):
        """检查额度并自动切换"""
        bailian_status = self.check_bailian_quota()
        gemini_status = self.check_gemini_quota()
        
        if bailian_status.available and self.state != ModelState.BAILIAN_PRIMARY:
            self.force_switch_to("bailian/qwen3.5-plus")
            print(f"✅ 百炼额度恢复，强制切回百炼")
            return
        
        if bailian_status.usage_rate >= self.SWITCH_THRESHOLD:
            if gemini_status.available:
                self.force_switch_to("gemini/gemini-2.5-flash")
                print(f"⚠️ 百炼额度达 {bailian_status.usage_rate:.1%}, 切换到 Gemini")
            else:
                self.force_switch_to("local/qwen2.5:7b")
                print(f"🚨 百炼 +Gemini 均不可用，切换到本地")
            return
        
        if gemini_status.usage_rate >= self.SWITCH_THRESHOLD:
            if bailian_status.available:
                self.force_switch_to("bailian/qwen3.5-plus")
                print(f"⚠️ Gemini 额度达 {gemini_status.usage_rate:.1%}, 切回百炼")
            else:
                self.force_switch_to("local/qwen2.5:7b")
                print(f"🚨 Gemini 额度耗尽，切换到本地")
            return
    
    def track_usage(self, model: str, tokens_in: int, tokens_out: int):
        """记录额度使用"""
        total_tokens = tokens_in + tokens_out
        
        if model.startswith("bailian"):
            self.cache.setdefault("bailian", {"used": 0})
            self.cache["bailian"]["used"] = self.cache["bailian"].get("used", 0) + total_tokens
        elif model.startswith("gemini"):
            self.cache.setdefault("gemini", {"used": 0})
            self.cache["gemini"]["used"] = self.cache["gemini"].get("used", 0) + 1
        
        self.save_cache()
    
    def send_notification(self, event_type: str, message: str):
        """发送通知"""
        print(f"📢 通知 [{event_type}]: {message}")
    
    def get_status(self) -> Dict:
        """获取系统状态"""
        bailian = self.check_bailian_quota()
        gemini = self.check_gemini_quota()
        
        return {
            "state": self.state.value,
            "bailian": {"usage_rate": f"{bailian.usage_rate:.1%}", "available": bailian.available},
            "gemini": {"usage_rate": f"{gemini.usage_rate:.1%}", "available": gemini.available},
            "current_model": self.select_model(),
            "switch_count_today": self.switch_count
        }
    
    def reset_daily_quota(self):
        """重置日额度"""
        self.cache["bailian"]["used"] = 0
        self.cache["gemini"]["used"] = 0
        self.switch_count = 0
        self.save_cache()
        print("📊 日额度已重置")


def select_model(task_type: str = "conversation", complexity: str = "normal") -> str:
    """快捷选择模型"""
    router = QuotaRouter()
    return router.select_model(task_type, complexity)


def get_status() -> Dict:
    """快捷获取状态"""
    router = QuotaRouter()
    return router.get_status()


if __name__ == "__main__":
    router = QuotaRouter()
    
    print("=== Quota-Aware Model Router v1.0 ===")
    print()
    print("📊 当前状态:")
    status = router.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    print()
    print("📈 模拟额度使用:")
    router.track_usage("bailian/qwen3.5-plus", 1000, 2000)
    print(f"百炼已用：{router.cache.get('bailian', {}).get('used', 0)} tokens")
    print()
    print("🔄 检查并切换:")
    router.check_and_switch()
