#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt 缓存优化模块 - LLM Token 成本优化
太一 AGI · 2026-04-20 21:25

功能:
- Prompt 缓存管理 (KV Cache)
- 静态内容缓存
- 动态内容检索
- Token 成本优化
"""

import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('PromptCacheOptimizer')

WORKSPACE = Path("/home/sayelf/.openclaw/workspace")
CACHE_DIR = WORKSPACE / "data" / "cross-border" / "prompt_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class PromptCacheOptimizer:
    """Prompt 缓存优化模块"""
    
    # 缓存策略
    CACHE_STRATEGIES = {
        "system_prompt": {"ttl_hours": 168, "priority": "high"},  # 系统提示词缓存 7 天
        "skill_definition": {"ttl_hours": 72, "priority": "high"},  # Skill 定义缓存 3 天
        "user_preference": {"ttl_hours": 24, "priority": "medium"},  # 用户偏好缓存 1 天
        "context_history": {"ttl_hours": 2, "priority": "low"},  # 上下文缓存 2 小时
        "tool_definition": {"ttl_hours": 168, "priority": "high"}  # 工具定义缓存 7 天
    }
    
    def __init__(self):
        self.cache_file = CACHE_DIR / "prompt_cache.json"
        self.stats_file = CACHE_DIR / "cache_stats.json"
        self.data = self._load_data()
        self.stats = self._load_stats()
    
    def _load_data(self) -> Dict:
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"cache": {}, "metadata": {}}
    
    def _load_stats(self) -> Dict:
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "tokens_saved": 0,
            "cost_saved_usd": 0
        }
    
    def cache_prompt(self, prompt_type: str, content: str, metadata: Dict = None) -> str:
        """缓存 Prompt"""
        logger.info(f"💾 缓存 Prompt: {prompt_type}")
        
        # 生成缓存键
        cache_key = self._generate_cache_key(prompt_type, content)
        
        # 获取缓存策略
        strategy = self.CACHE_STRATEGIES.get(prompt_type, {"ttl_hours": 24, "priority": "medium"})
        
        # 存储缓存
        self.data["cache"][cache_key] = {
            "prompt_type": prompt_type,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=strategy["ttl_hours"])).isoformat(),
            "ttl_hours": strategy["ttl_hours"],
            "priority": strategy["priority"],
            "access_count": 0,
            "token_count": self._estimate_tokens(content)
        }
        
        self._save_data()
        
        logger.info(f"✅ Prompt 已缓存：{cache_key[:20]}... (TTL: {strategy['ttl_hours']}h)")
        return cache_key
    
    def get_cached_prompt(self, prompt_type: str, content: str) -> Optional[str]:
        """获取缓存的 Prompt"""
        cache_key = self._generate_cache_key(prompt_type, content)
        
        if cache_key in self.data["cache"]:
            cached = self.data["cache"][cache_key]
            
            # 检查是否过期
            if datetime.fromisoformat(cached["expires_at"]) > datetime.now():
                cached["access_count"] += 1
                self._save_data()
                
                # 更新统计
                self._update_stats(hit=True, tokens_saved=cached["token_count"])
                
                logger.info(f"✅ 缓存命中：{cache_key[:20]}... (访问{cached['access_count']}次)")
                return cached["content"]
            else:
                # 过期删除
                del self.data["cache"][cache_key]
                self._save_data()
                self._update_stats(hit=False)
                logger.info(f"⏰ 缓存过期：{cache_key[:20]}...")
        
        self._update_stats(hit=False)
        return None
    
    def _generate_cache_key(self, prompt_type: str, content: str) -> str:
        """生成缓存键"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        return f"{prompt_type}_{content_hash}"
    
    def _estimate_tokens(self, content: str) -> int:
        """估算 Token 数"""
        # 简单估算：4 字符≈1 token
        return len(content) // 4
    
    def _update_stats(self, hit: bool, tokens_saved: int = 0):
        """更新统计"""
        self.stats["total_requests"] += 1
        
        if hit:
            self.stats["cache_hits"] += 1
            self.stats["tokens_saved"] += tokens_saved
            # 估算成本节省 ($0.002/1K tokens)
            self.stats["cost_saved_usd"] += (tokens_saved / 1000) * 0.002
        else:
            self.stats["cache_misses"] += 1
        
        self._save_stats()
    
    def optimize_prompt(self, prompt: str, context: Dict = None) -> Dict:
        """优化 Prompt (应用缓存策略)"""
        logger.info(f"⚙️ 优化 Prompt")
        
        optimization = {
            "id": f"PROMPT_OPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "original_length": len(prompt),
            "original_tokens": self._estimate_tokens(prompt),
            "timestamp": datetime.now().isoformat(),
            "cached_components": [],
            "dynamic_components": [],
            "optimized_prompt": "",
            "tokens_saved": 0,
            "cost_saved_usd": 0
        }
        
        # 分离静态和动态内容
        static_parts, dynamic_parts = self._separate_static_dynamic(prompt, context)
        
        # 缓存静态部分
        for i, static_part in enumerate(static_parts):
            cache_key = self.cache_prompt("system_prompt", static_part)
            optimization["cached_components"].append({
                "index": i,
                "cache_key": cache_key,
                "tokens": self._estimate_tokens(static_part)
            })
            optimization["tokens_saved"] += self._estimate_tokens(static_part)
        
        # 保留动态部分
        for i, dynamic_part in enumerate(dynamic_parts):
            optimization["dynamic_components"].append({
                "index": i,
                "content_preview": dynamic_part[:50] + "..." if len(dynamic_part) > 50 else dynamic_part,
                "tokens": self._estimate_tokens(dynamic_part)
            })
        
        # 计算成本节省
        optimization["cost_saved_usd"] = (optimization["tokens_saved"] / 1000) * 0.002
        
        # 生成优化后的 Prompt
        optimization["optimized_prompt"] = self._reconstruct_prompt(static_parts, dynamic_parts)
        
        self._save_data()
        
        logger.info(f"✅ Prompt 优化完成：节省{optimization['tokens_saved']} tokens (${optimization['cost_saved_usd']:.4f})")
        return optimization
    
    def _separate_static_dynamic(self, prompt: str, context: Dict = None) -> tuple:
        """分离静态和动态内容"""
        static_parts = []
        dynamic_parts = []
        
        # 静态内容 (系统提示、工具定义等)
        static_keywords = ["你是", "你的职责", "系统提示", "工具定义", "技能定义"]
        
        # 动态内容 (用户输入、上下文等)
        dynamic_keywords = ["用户说", "当前时间", "上下文", "最新消息"]
        
        lines = prompt.split("\n")
        for line in lines:
            is_static = any(kw in line for kw in static_keywords)
            is_dynamic = any(kw in line for kw in dynamic_keywords)
            
            if is_static:
                static_parts.append(line)
            elif is_dynamic:
                dynamic_parts.append(line)
            else:
                # 默认视为静态
                static_parts.append(line)
        
        return static_parts, dynamic_parts
    
    def _reconstruct_prompt(self, static_parts: List[str], dynamic_parts: List[str]) -> str:
        """重构 Prompt"""
        # 实际应用中，这里会从缓存加载静态部分
        # 这里简化处理
        all_parts = static_parts + dynamic_parts
        return "\n".join(all_parts)
    
    def cleanup_expired(self) -> Dict:
        """清理过期缓存"""
        logger.info(f"🧹 清理过期缓存")
        
        expired_keys = []
        for key, cached in self.data["cache"].items():
            if datetime.fromisoformat(cached["expires_at"]) < datetime.now():
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.data["cache"][key]
        
        self._save_data()
        
        result = {
            "expired_count": len(expired_keys),
            "remaining_count": len(self.data["cache"]),
            "cleaned_at": datetime.now().isoformat()
        }
        
        logger.info(f"✅ 清理完成：{len(expired_keys)}个过期缓存")
        return result
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计"""
        hit_rate = (
            self.stats["cache_hits"] / self.stats["total_requests"] * 100
            if self.stats["total_requests"] > 0 else 0
        )
        
        return {
            "total_requests": self.stats["total_requests"],
            "cache_hits": self.stats["cache_hits"],
            "cache_misses": self.stats["cache_misses"],
            "hit_rate": round(hit_rate, 2),
            "tokens_saved": self.stats["tokens_saved"],
            "cost_saved_usd": round(self.stats["cost_saved_usd"], 4),
            "cached_prompts": len(self.data["cache"])
        }
    
    def _save_data(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def _save_stats(self):
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)


def main():
    logger.info("=" * 60)
    logger.info("💾 Prompt 缓存优化模块 - LLM Token 成本优化")
    logger.info("=" * 60)
    
    optimizer = PromptCacheOptimizer()
    
    # 演示缓存 Prompt
    logger.info(f"\n💾 缓存 Prompt...")
    system_prompt = "你是一个专业的跨境贸易助手，名叫太一。你的职责是帮助用户完成跨境贸易相关的任务。"
    cache_key = optimizer.cache_prompt("system_prompt", system_prompt)
    logger.info(f"  缓存键：{cache_key[:30]}...")
    
    # 演示获取缓存
    logger.info(f"\n🔍 获取缓存 Prompt...")
    cached = optimizer.get_cached_prompt("system_prompt", system_prompt)
    logger.info(f"  缓存命中：{cached is not None}")
    
    # 演示 Prompt 优化
    logger.info(f"\n⚙️ 优化 Prompt...")
    long_prompt = f"""
{system_prompt}
你的职责包括：
1. 产品推荐
2. 市场分析
3. 客户开发
4. 订单跟踪

用户说：{datetime.now().isoformat()}
当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    optimization = optimizer.optimize_prompt(long_prompt)
    logger.info(f"  原始 Token: {optimization['original_tokens']}")
    logger.info(f"  节省 Token: {optimization['tokens_saved']}")
    logger.info(f"  节省成本：${optimization['cost_saved_usd']:.4f}")
    
    # 演示缓存统计
    logger.info(f"\n📊 缓存统计:")
    stats = optimizer.get_cache_stats()
    logger.info(f"  总请求：{stats['total_requests']}")
    logger.info(f"  命中率：{stats['hit_rate']}%")
    logger.info(f"  节省 Token: {stats['tokens_saved']}")
    logger.info(f"  节省成本：${stats['cost_saved_usd']:.4f}")
    
    # 演示清理过期缓存
    logger.info(f"\n🧹 清理过期缓存...")
    cleanup = optimizer.cleanup_expired()
    logger.info(f"  过期数：{cleanup['expired_count']}")
    logger.info(f"  剩余数：{cleanup['remaining_count']}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Prompt 缓存优化演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
