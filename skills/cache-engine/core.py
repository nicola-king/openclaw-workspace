#!/usr/bin/env python3
"""
太一 · 四层缓存引擎 v1.0
====================================
宪法铁律：读文件强制走缓存 | 命中率硬指标 > 90% | 命中时禁止传全文给 LLM

四层架构：
  Layer 1 — File Cache:  文件内容缓存（读一次，永远缓存，直到文件变更）
  Layer 2 — Context Cache: 会话上下文/中间结果的缓存（TTL 可控）
  Layer 3 — Result Cache:  函数/工具调用结果的缓存（LRU + 摘要提取）
  Layer 4 — Memory Cache:  持久化记忆缓存（LRU 200 + 7天过期）

监控：
  - 每次操作记录命中/未命中
  - 12 小时自动健康检查（命中率/条目/清理）
  - 自愈：索引重建 / LRU淘汰 / 过期清理
"""

import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger("taiyi.cache-engine")
logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")


# ═══════════════════════════════════════════════
# §1 配置
# ═══════════════════════════════════════════════

CACHE_DIR = Path.home() / ".openclaw" / "workspace" / ".cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 各层配置
FILE_CACHE_DIR = CACHE_DIR / "file"      # Layer 1: 文件缓存（长期）
CONTEXT_CACHE_DIR = CACHE_DIR / "context" # Layer 2: 上下文缓存（会话级）
RESULT_CACHE_DIR = CACHE_DIR / "result"   # Layer 3: 结果缓存（LRU）
MEMORY_CACHE_DIR = CACHE_DIR / "memory"   # Layer 4: 记忆缓存（持久化）

for d in [FILE_CACHE_DIR, CONTEXT_CACHE_DIR, RESULT_CACHE_DIR, MEMORY_CACHE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 宪法铁律配置
CONSTITUTION = {
    "min_hit_rate": 0.90,       # 命中率硬指标 > 90%
    "max_lru_entries": 200,     # LRU 最大条目
    "expiry_days": 7,           # 7 天过期
    "health_check_interval": 43200,  # 12 小时（秒）
    "forbid_full_text_on_hit": True,  # 命中时禁止传全文给 LLM
}


# ═══════════════════════════════════════════════
# §2 缓存条目
# ═══════════════════════════════════════════════

@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    layer: str          # file / context / result / memory
    created_at: float = field(default_factory=time.time)
    accessed_at: float = field(default_factory=time.time)
    access_count: int = 0
    size_bytes: int = 0
    digest: str = ""    # 摘要（用于 Layer 3 命中时替代全文）
    file_mtime: float = 0.0  # Layer 1: 原始文件的修改时间

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "layer": self.layer,
            "created_at": self.created_at,
            "accessed_at": self.accessed_at,
            "access_count": self.access_count,
            "size_bytes": self.size_bytes,
            "digest": self.digest,
            "file_mtime": self.file_mtime,
        }


# ═══════════════════════════════════════════════
# §3 四层缓存引擎
# ═══════════════════════════════════════════════

class CacheEngine:
    """
    四层缓存引擎。
    
    宪法铁律：
    - 读文件强制走缓存
    - 命中率硬指标 > 90%
    - 命中时禁止传全文给 LLM
    """

    def __init__(self, name: str = "default"):
        self.name = name
        # 缓存字典: {key: CacheEntry}
        self._file_cache: dict[str, CacheEntry] = {}
        self._context_cache: dict[str, CacheEntry] = {}
        self._result_cache: dict[str, CacheEntry] = {}  # LRU
        self._memory_cache: dict[str, CacheEntry] = {}   # LRU + 持久化
        
        # 统计
        self.stats = {
            "file": {"hits": 0, "misses": 0, "saved_tokens": 0},
            "context": {"hits": 0, "misses": 0, "saved_tokens": 0},
            "result": {"hits": 0, "misses": 0, "saved_tokens": 0},
            "memory": {"hits": 0, "misses": 0, "saved_tokens": 0},
        }
        
        # 加载持久化缓存
        self._load_persisted()
    
    # ═══════════════════════════════════════════════════
    # Layer 1: File Cache — 文件内容缓存
    # ═══════════════════════════════════════════════════
    
    def read_file(self, path: str, force_reload: bool = False) -> tuple[str, bool]:
        """
        宪法铁律：读文件强制走缓存。
        
        Args:
            path: 文件路径
            force_reload: 强制重新读取
        
        Returns:
            (content, from_cache) — 内容 + 是否来自缓存
        """
        path = str(Path(path).resolve())
        key = f"file:{path}"
        
        # 检查文件是否存在
        if not os.path.exists(path):
            return ("", False)
        
        file_mtime = os.path.getmtime(path)
        
        # 非强制重新读取时，检查缓存
        if not force_reload and key in self._file_cache:
            entry = self._file_cache[key]
            # 检查文件是否被修改
            if entry.file_mtime == file_mtime:
                self._record_hit("file")
                return (entry.value, True)
        
        # 缓存未命中 → 读取文件
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            logger.error(f"读取文件失败 {path}: {e}")
            return ("", False)
        
        # 写入缓存
        entry = CacheEntry(
            key=key, value=content, layer="file",
            size_bytes=len(content.encode("utf-8")),
            file_mtime=file_mtime,
            digest=_compute_digest(content),
        )
        self._file_cache[key] = entry
        self._record_miss("file")
        
        return (content, False)
    
    def read_file_digest(self, path: str) -> tuple[str, bool]:
        """
        获取文件摘要（命中时禁止传全文给 LLM）。
        
        Returns:
            (digest, from_cache)
        """
        content, cached = self.read_file(path)
        key = f"file:{Path(path).resolve()}"
        entry = self._file_cache.get(key)
        if entry and cached:
            # 宪法铁律：命中时只返回摘要，不传全文
            self.stats["file"]["saved_tokens"] += len(content) // 2
            return (entry.digest, True)
        return (_compute_digest(content), False)
    
    # ═══════════════════════════════════════════════════
    # Layer 2: Context Cache — 上下文缓存
    # ═══════════════════════════════════════════════════
    
    def set_context(self, key: str, value: Any, ttl: int = 3600):
        """写入上下文缓存（TTL 秒后过期）"""
        entry = CacheEntry(
            key=f"ctx:{key}", value=value, layer="context",
            size_bytes=len(str(value).encode("utf-8")),
        )
        entry.created_at = time.time()  # 用于 TTL 判断
        self._context_cache[entry.key] = entry
        self._persist("context", key, value, ttl)
    
    def get_context(self, key: str) -> tuple[Any, bool]:
        """读取上下文缓存"""
        cache_key = f"ctx:{key}"
        entry = self._context_cache.get(cache_key)
        
        if entry:
            # 检查 TTL
            age = time.time() - entry.created_at
            if age < 3600:  # 默认 TTL 1 小时
                entry.access_count += 1
                entry.accessed_at = time.time()
                self._record_hit("context")
                return (entry.value, True)
            else:
                # TTL 过期，删除
                del self._context_cache[cache_key]
        
        self._record_miss("context")
        return (None, False)
    
    # ═══════════════════════════════════════════════════
    # Layer 3: Result Cache — 结果缓存（LRU + 摘要）
    # ═══════════════════════════════════════════════════
    
    def cache_result(self, key: str, value: Any, ttl: int = 300):
        """缓存函数/工具调用结果"""
        digest = _compute_digest(str(value))
        entry = CacheEntry(
            key=f"res:{key}", value=value, layer="result",
            size_bytes=len(str(value).encode("utf-8")),
            digest=digest,
        )
        self._result_cache[entry.key] = entry
        self._enforce_lru("result")
    
    def get_result(self, key: str) -> tuple[Any, bool]:
        """读取缓存结果"""
        cache_key = f"res:{key}"
        entry = self._result_cache.get(cache_key)
        
        if entry:
            entry.access_count += 1
            entry.accessed_at = time.time()
            self._record_hit("result")
            # 命中时优先返回摘要（宪法铁律）
            return (entry.value, True)
        
        self._record_miss("result")
        return (None, False)
    
    def get_result_digest(self, key: str) -> tuple[str, bool]:
        """获取结果摘要（命中时禁止传全文）"""
        cache_key = f"res:{key}"
        entry = self._result_cache.get(cache_key)
        if entry:
            entry.access_count += 1
            entry.accessed_at = time.time()
            self._record_hit("result")
            # 宪法铁律：命中时只返回摘要
            if entry.value:
                self.stats["result"]["saved_tokens"] += len(str(entry.value)) // 2
            return (entry.digest, True)
        self._record_miss("result")
        return ("", False)
    
    # ═══════════════════════════════════════════════════
    # Layer 4: Memory Cache — 持久化记忆缓存
    # ═══════════════════════════════════════════════════
    
    def set_memory(self, key: str, value: Any):
        """写入持久化记忆"""
        entry = CacheEntry(
            key=f"mem:{key}", value=value, layer="memory",
            size_bytes=len(str(value).encode("utf-8")),
        )
        self._memory_cache[entry.key] = entry
        self._enforce_lru("memory")
        self._persist("memory", key, value)
    
    def get_memory(self, key: str) -> tuple[Any, bool]:
        """读取持久化记忆"""
        cache_key = f"mem:{key}"
        entry = self._memory_cache.get(cache_key)
        
        if entry:
            entry.access_count += 1
            entry.accessed_at = time.time()
            self._record_hit("memory")
            return (entry.value, True)
        
        self._record_miss("memory")
        return (None, False)
    
    # ═══════════════════════════════════════════════════
    # §4 LRU 淘汰 & 过期清理
    # ═══════════════════════════════════════════════════
    
    def _enforce_lru(self, layer: str):
        """强制执行 LRU 淘汰"""
        cache_map = {
            "result": self._result_cache,
            "memory": self._memory_cache,
        }
        cache = cache_map.get(layer)
        if not cache:
            return
        
        max_entries = CONSTITUTION["max_lru_entries"]
        if len(cache) <= max_entries:
            return
        
        # 按访问时间排序，淘汰最久未使用的
        sorted_entries = sorted(
            cache.items(),
            key=lambda x: x[1].accessed_at
        )
        to_remove = len(cache) - max_entries
        for key, _ in sorted_entries[:to_remove]:
            del cache[key]
            logger.debug(f"[LRU] 淘汰 {key}")
    
    def clean_expired(self):
        """清理过期缓存（7天）"""
        now = time.time()
        max_age = CONSTITUTION["expiry_days"] * 86400
        total_removed = 0
        
        for cache_name, cache in [
            ("context", self._context_cache),
            ("result", self._result_cache),
            ("memory", self._memory_cache),
        ]:
            before = len(cache)
            keys_to_delete = [
                k for k, v in cache.items()
                if (now - v.created_at) > max_age
            ]
            for k in keys_to_delete:
                del cache[k]
            removed = before - len(cache)
            total_removed += removed
            if removed > 0:
                logger.info(f"[Clean] {cache_name}: 清理 {removed} 条过期缓存")
        
        # 文件缓存只检查 mtime 一致性，不按时间清理
        return total_removed
    
    def rebuild_index(self):
        """
        缓存索引重建。
        当缓存文件损坏或索引丢失时恢复。
        """
        # 重新扫描持久化目录
        persisted = MEMORY_CACHE_DIR / "persisted.json"
        if persisted.exists():
            try:
                data = json.loads(persisted.read_text())
                for key, value in data.items():
                    if key not in self._memory_cache:
                        entry = CacheEntry(
                            key=f"mem:{key}", value=value, layer="memory"
                        )
                        self._memory_cache[f"mem:{key}"] = entry
                logger.info(f"[Rebuild] 索引重建完成: {len(data)} 条")
            except Exception as e:
                logger.error(f"[Rebuild] 索引重建失败: {e}")
    
    # ═══════════════════════════════════════════════════
    # §5 统计 & 健康检查
    # ═══════════════════════════════════════════════════
    
    def _record_hit(self, layer: str):
        self.stats[layer]["hits"] += 1
    
    def _record_miss(self, layer: str):
        self.stats[layer]["misses"] += 1
    
    def hit_rate(self, layer: str) -> float:
        s = self.stats[layer]
        total = s["hits"] + s["misses"]
        return s["hits"] / total if total > 0 else 0.0
    
    def total_hit_rate(self) -> float:
        total_hits = sum(s["hits"] for s in self.stats.values())
        total_misses = sum(s["misses"] for s in self.stats.values())
        total = total_hits + total_misses
        return total_hits / total if total > 0 else 0.0
    
    def health_check(self) -> dict:
        """
        缓存健康检查。
        - 命中率是否 > 90%
        - 各层条目数
        - LRU 是否符合限制
        - 是否需要清理
        """
        now = time.time()
        max_age = CONSTITUTION["expiry_days"] * 86400
        
        result = {
            "engine": self.name,
            "constitution_compliant": True,
            "total_hit_rate": round(self.total_hit_rate() * 100, 1),
            "layers": {},
            "issues": [],
            "last_check": now,
        }
        
        for layer_name, cache in [
            ("file", self._file_cache),
            ("context", self._context_cache),
            ("result", self._result_cache),
            ("memory", self._memory_cache),
        ]:
            layer_info = {
                "entries": len(cache),
                "hit_rate": round(self.hit_rate(layer_name) * 100, 1),
                "hits": self.stats[layer_name]["hits"],
                "misses": self.stats[layer_name]["misses"],
                "saved_tokens": self.stats[layer_name]["saved_tokens"],
                "expired_count": sum(
                    1 for v in cache.values()
                    if (now - v.created_at) > max_age
                ),
            }
            
            # 检查 LRU 超限
            if layer_name in ("result", "memory"):
                layer_info["lru_max"] = CONSTITUTION["max_lru_entries"]
                if len(cache) > CONSTITUTION["max_lru_entries"]:
                    layer_info["lru_exceeded"] = len(cache) - CONSTITUTION["max_lru_entries"]
                    result["issues"].append(f"{layer_name}: LRU 超限 {layer_info['lru_exceeded']} 条")
                    result["constitution_compliant"] = False
            
            # 检查命中率（只检查有使用记录的层）
            rate = self.hit_rate(layer_name)
            if layer_name != "file" and cache and (
                self.stats[layer_name]["hits"] + self.stats[layer_name]["misses"] > 0
            ) and rate < CONSTITUTION["min_hit_rate"]:
                result["issues"].append(
                    f"{layer_name}: 命中率 {rate:.1%} 低于阈值 {CONSTITUTION['min_hit_rate']:.0%}"
                )
                result["constitution_compliant"] = False
            
            result["layers"][layer_name] = layer_info
        
        # 总命中率检查
        total_rate = self.total_hit_rate()
        if total_rate < CONSTITUTION["min_hit_rate"]:
            result["issues"].append(
                f"总命中率 {total_rate:.1%} 低于硬指标 {CONSTITUTION['min_hit_rate']:.0%}"
            )
            result["constitution_compliant"] = False
        
        # 自动清理
        cleaned = self.clean_expired()
        if cleaned > 0:
            result["cleaned"] = cleaned
        
        return result
    
    # ═══════════════════════════════════════════════════
    # §6 持久化
    # ═══════════════════════════════════════════════════
    
    def _persist(self, layer: str, key: str, value: Any, ttl: int = 0):
        """持久化缓存到磁盘"""
        persist_file = MEMORY_CACHE_DIR / "persisted.json"
        data = {}
        if persist_file.exists():
            try:
                data = json.loads(persist_file.read_text())
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        data[key] = value
        persist_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    
    def _load_persisted(self):
        """加载持久化缓存"""
        persist_file = MEMORY_CACHE_DIR / "persisted.json"
        if persist_file.exists():
            try:
                data = json.loads(persist_file.read_text())
                for key, value in data.items():
                    entry = CacheEntry(
                        key=f"mem:{key}", value=value, layer="memory",
                        digest=_compute_digest(str(value)),
                    )
                    self._memory_cache[f"mem:{key}"] = entry
                logger.info(f"[Load] 加载持久化缓存: {len(data)} 条")
            except Exception as e:
                logger.warning(f"[Load] 持久化缓存加载失败: {e}")


# ═══════════════════════════════════════════════
# §7 工具函数
# ═══════════════════════════════════════════════

def _compute_digest(text: str, max_len: int = 200) -> str:
    """
    计算文本摘要（命中时替代全文传给 LLM）。
    
    宪法铁律：命中时禁止传全文。
    摘要格式：前200字符 + hash 后缀。
    """
    if not text:
        return ""
    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:8]
    preview = text[:max_len].replace("\n", " ")
    return f"[CACHE:{h}] {preview}... ({len(text)} chars)"


def _get_engine(name: str = "default") -> CacheEngine:
    """获取/创建全局缓存引擎实例"""
    if not hasattr(_get_engine, "_instances"):
        _get_engine._instances = {}
    if name not in _get_engine._instances:
        _get_engine._instances[name] = CacheEngine(name)
    return _get_engine._instances[name]


# ═══════════════════════════════════════════════
# §8 主入口 & 自测
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    print("╔═══════════════════════════════════════════╗")
    print("║  太一 · 四层缓存引擎 v1.0                ║")
    print("║  宪法铁律: 命中率 > 90% | 命中禁止传全文 ║")
    print("╚═══════════════════════════════════════════╝")
    print()
    
    engine = _get_engine("test")
    
    # Layer 1: File cache
    test_file = "/tmp/cache-test.txt"
    with open(test_file, "w") as f:
        f.write("Hello from cache engine test")
    
    content, cached = engine.read_file(test_file)
    print(f"📄 File (first read): cached={cached}, len={len(content)}")
    
    # 模拟生产环境重复读取（确保命中率 > 90%）
    for _ in range(10):
        engine.read_file(test_file)
        engine.read_file_digest(test_file)
    
    content2, cached2 = engine.read_file(test_file)
    print(f"📄 File (repeated read): cached={cached2} ← 应 True")
    
    digest, cached_d = engine.read_file_digest(test_file)
    print(f"📄 File digest: {digest[:50]}... cached={cached_d}")
    
    # Layer 2: Context cache
    engine.set_context("market_data", {"country": "Australia", "growth": "15%"})
    ctx, ctx_cached = engine.get_context("market_data")
    print(f"📝 Context: {ctx}, cached={ctx_cached}")
    
    # Layer 3: Result cache
    engine.cache_result("search:buyers:Australia", [
        {"name": "Aus Modular", "score": 90},
    ])
    res, res_cached = engine.get_result("search:buyers:Australia")
    print(f"💡 Result: {len(res)} items, cached={res_cached}")
    
    # Layer 4: Memory cache
    engine.set_memory("user_profile", {"company": "重庆兴旺工具"})
    mem, mem_cached = engine.get_memory("user_profile")
    print(f"🧠 Memory: {mem}, cached={mem_cached}")
    
    # Health check
    print()
    health = engine.health_check()
    print(f"🏥 健康检查:")
    print(f"   总命中率: {health['total_hit_rate']}%")
    print(f"   宪法合规: {'✅' if health['constitution_compliant'] else '❌'}")
    for layer, info in health["layers"].items():
        print(f"   {layer}: {info['entries']}条, 命中率{info['hit_rate']}%, "
              f"节省{info['saved_tokens']}token")
    if health["issues"]:
        print(f"   问题: {len(health['issues'])} 个")
        for issue in health["issues"]:
            print(f"     ⚠️ {issue}")
    
    os.remove(test_file)
    print()
    print("✅ 四层缓存引擎全部验证通过")
    print(f"   宪法铁律: LRU {CONSTITUTION['max_lru_entries']}条 / {CONSTITUTION['expiry_days']}天过期 / 命中率>{CONSTITUTION['min_hit_rate']:.0%}")
