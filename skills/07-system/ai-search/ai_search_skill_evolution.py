#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 搜索 Skill - 智能自动化调用 + 自进化版本
太一 AGI · 2026-04-19

功能:
- 智能自动化调用 (根据任务类型自动选择方法)
- 自进化功能 (使用统计/技能结晶/自动优化)
- 网络搜索 (Firecrawl)
- 网页爬取 (Crawl4AI)
- 页面交互 (Firecrawl)
- Agent 自主查询 (Firecrawl)

架构位置：太一 Skills 系统 → AI 搜索 Skill (自进化版)
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('AISearchSkillEvolution')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "07-system" / "ai-search"
EVOLUTION_DIR = SKILL_DIR / "evolution"
MEMORY_DIR = SKILL_DIR / "memory"
SKILL_DIR.mkdir(parents=True, exist_ok=True)
EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


class AISearchSkillEvolution:
    """AI 搜索 Skill - 智能自动化调用 + 自进化版本"""
    
    def __init__(self):
        """初始化 AI 搜索 Skill (自进化版)"""
        self.skill_name = "ai_search_evolution"
        self.version = "2.0.0"
        self.description = "AI 搜索技能 - 智能自动化调用 + 自进化"
        
        # 配置
        self.config = self._load_config()
        
        # 核心组件
        self.crawler = None
        self.search_api = None
        self._init_components()
        
        # 自进化系统
        self.usage_stats = self._load_usage_stats()
        self.skill_memories = self._load_skill_memories()
        self.crystallized_patterns = self._load_crystallized_patterns()
        
        # 智能调用策略
        self.call_strategies = self._init_call_strategies()
    
    def _init_components(self):
        """初始化核心组件"""
        # Crawl4AI 爬虫
        try:
            from crawl4ai import AsyncWebCrawler
            self.crawler = AsyncWebCrawler()
            logger.info("✅ Crawl4AI 爬虫初始化成功")
        except ImportError:
            logger.warning("⚠️ Crawl4AI 未安装，爬虫功能不可用")
            self.crawler = None
        
        # Firecrawl 搜索 API
        try:
            from firecrawl import Firecrawl
            api_key = self.config.get("firecrawl_api_key", "")
            if api_key:
                self.search_api = Firecrawl(api_key=api_key)
                logger.info("✅ Firecrawl 搜索 API 初始化成功")
            else:
                logger.warning("⚠️ Firecrawl API Key 未配置")
                self.search_api = None
        except ImportError:
            logger.warning("⚠️ Firecrawl 未安装")
            self.search_api = None
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_file = SKILL_DIR / "skill_config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"local_mode": True, "auto_evolution": True}
    
    def _load_usage_stats(self) -> Dict:
        """加载使用统计"""
        stats_file = EVOLUTION_DIR / "usage_stats.json"
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "total_calls": 0,
            "by_method": {},
            "success_rate": 0.0,
            "average_latency": 0.0,
            "last_evolution": None
        }
    
    def _load_skill_memories(self) -> List[Dict]:
        """加载技能记忆"""
        memory_file = MEMORY_DIR / "skill_memories.json"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _load_crystallized_patterns(self) -> List[Dict]:
        """加载结晶模式"""
        pattern_file = EVOLUTION_DIR / "crystallized_patterns.json"
        if pattern_file.exists():
            with open(pattern_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _init_call_strategies(self) -> Dict:
        """初始化调用策略"""
        return {
            "search_only": {
                "keywords": ["搜索", "查找", "search", "find"],
                "method": "search",
                "description": "仅搜索"
            },
            "crawl_only": {
                "keywords": ["爬取", "抓取", "crawl", "scrape"],
                "method": "crawl",
                "description": "仅爬取"
            },
            "search_and_crawl": {
                "keywords": ["搜索并爬取", "完整信息", "full", "complete"],
                "method": "search_and_crawl",
                "description": "搜索 + 爬取"
            },
            "agent_query": {
                "keywords": ["分析", "调研", "报告", "analyze", "research", "report"],
                "method": "agent_query",
                "description": "Agent 自主查询"
            },
            "interact": {
                "keywords": ["交互", "点击", "输入", "interact", "click", "type"],
                "method": "interact",
                "description": "页面交互"
            }
        }
    
    def _auto_select_method(self, query: str, context: Dict = None) -> str:
        """
        智能自动选择调用方法
        
        Args:
            query: 查询内容
            context: 上下文信息
            
        Returns:
            推荐的方法
        """
        logger.info(f"🧠 智能选择调用方法：{query[:50]}...")
        
        # 1. 检查结晶模式 (历史成功经验)
        for pattern in self.crystallized_patterns:
            if self._match_pattern(query, pattern["query_pattern"]):
                logger.info(f"✅ 匹配结晶模式：{pattern['name']}")
                self._record_evolution_event("pattern_matched", pattern["name"])
                return pattern["method"]
        
        # 2. 关键词匹配
        query_lower = query.lower()
        for strategy_name, strategy in self.call_strategies.items():
            for keyword in strategy["keywords"]:
                if keyword.lower() in query_lower:
                    logger.info(f"✅ 关键词匹配：{strategy_name}")
                    self._record_evolution_event("keyword_matched", strategy_name)
                    return strategy["method"]
        
        # 3. 默认策略 (搜索 + 爬取)
        logger.info("✅ 使用默认策略：search_and_crawl")
        return "search_and_crawl"
    
    def _match_pattern(self, query: str, pattern: str) -> bool:
        """检查查询是否匹配模式"""
        # 简单相似度计算
        query_words = set(query.lower().split())
        pattern_words = set(pattern.lower().split())
        intersection = query_words & pattern_words
        return len(intersection) / max(len(pattern_words), 1) > 0.5
    
    async def smart_call(self, query: str, context: Dict = None) -> Dict:
        """
        智能自动化调用
        
        Args:
            query: 查询内容
            context: 上下文信息
            
        Returns:
            调用结果
        """
        start_time = datetime.now()
        
        # 1. 智能选择方法
        method = self._auto_select_method(query, context)
        logger.info(f"🎯 选择方法：{method}")
        
        # 2. 执行调用
        result = await self._execute_method(method, query, context)
        
        # 3. 记录使用统计
        self._record_usage(method, result, start_time)
        
        # 4. 自进化检查
        self._check_evolution(query, method, result)
        
        return result
    
    async def _execute_method(self, method: str, query: str, context: Dict = None) -> Dict:
        """执行具体方法"""
        try:
            if method == "search":
                return await self.search(query)
            elif method == "crawl":
                return await self.crawl(query)
            elif method == "search_and_crawl":
                return await self.search_and_crawl(query)
            elif method == "agent_query":
                return await self.agent_query(query)
            elif method == "interact":
                return await self.interact(query, context.get("actions", []))
            else:
                return {"success": False, "error": f"Unknown method: {method}"}
        except Exception as e:
            logger.error(f"❌ 执行失败：{str(e)}")
            return {"success": False, "error": str(e)}
    
    async def search(self, query: str, limit: int = 10) -> Dict:
        """搜索功能"""
        logger.info(f"🔍 搜索：{query}")
        
        if not self.search_api:
            return {"success": False, "error": "Search API not initialized"}
        
        try:
            results = await self.search_api.search(query, limit=limit)
            self._record_success("search")
            return {"success": True, "method": "search", "results": results, "count": len(results)}
        except Exception as e:
            self._record_failure("search")
            return {"success": False, "error": str(e)}
    
    async def crawl(self, url: str) -> Dict:
        """爬取功能"""
        logger.info(f"🕷️ 爬取：{url}")
        
        if not self.crawler:
            return {"success": False, "error": "Crawler not initialized"}
        
        try:
            async with self.crawler:
                result = await self.crawler.arun(url=url)
                self._record_success("crawl")
                return {
                    "success": True,
                    "method": "crawl",
                    "url": url,
                    "markdown": result.markdown,
                    "length": len(result.markdown)
                }
        except Exception as e:
            self._record_failure("crawl")
            return {"success": False, "error": str(e)}
    
    async def search_and_crawl(self, query: str, limit: int = 5) -> Dict:
        """搜索 + 爬取"""
        logger.info(f"🔍️ 搜索 + 爬取：{query}")
        
        if not self.search_api or not self.crawler:
            return {"success": False, "error": "Components not initialized"}
        
        try:
            # 搜索
            search_results = await self.search_api.search(query, limit=limit)
            
            # 爬取前 3 个结果
            crawled_contents = []
            async with self.crawler:
                for result in search_results[:3]:
                    url = result.get("url")
                    if url:
                        crawl_result = await self.crawler.arun(url=url)
                        crawled_contents.append({
                            "url": url,
                            "title": result.get("title"),
                            "content": crawl_result.markdown[:1000]  # 前 1000 字符
                        })
            
            self._record_success("search_and_crawl")
            return {
                "success": True,
                "method": "search_and_crawl",
                "query": query,
                "results": crawled_contents,
                "count": len(crawled_contents)
            }
        except Exception as e:
            self._record_failure("search_and_crawl")
            return {"success": False, "error": str(e)}
    
    async def agent_query(self, prompt: str) -> Dict:
        """Agent 自主查询"""
        logger.info(f"🤖 Agent 查询：{prompt[:50]}...")
        
        if not self.search_api:
            return {"success": False, "error": "Search API not initialized"}
        
        try:
            result = await self.search_api.agent(prompt)
            self._record_success("agent_query")
            return {"success": True, "method": "agent_query", "result": result}
        except Exception as e:
            self._record_failure("agent_query")
            return {"success": False, "error": str(e)}
    
    async def interact(self, url: str, actions: List[Dict]) -> Dict:
        """页面交互"""
        logger.info(f"🖱️ 页面交互：{url}")
        
        if not self.search_api:
            return {"success": False, "error": "Search API not initialized"}
        
        try:
            scrape_result = await self.search_api.scrape(url)
            scrape_id = scrape_result.get("metadata", {}).get("scrape_id")
            
            if not scrape_id:
                return {"success": False, "error": "Failed to get scrape_id"}
            
            # 执行交互
            for action in actions:
                action_type = action.get("type")
                if action_type == "click":
                    await self.search_api.interact(scrape_id, prompt=f"Click {action.get('target')}")
                elif action_type == "scroll":
                    await self.search_api.interact(scrape_id, prompt="Scroll down")
                elif action_type == "type":
                    await self.search_api.interact(scrape_id, prompt=f"Type '{action.get('text')}'")
            
            self._record_success("interact")
            return {"success": True, "method": "interact", "actions_completed": len(actions)}
        except Exception as e:
            self._record_failure("interact")
            return {"success": False, "error": str(e)}
    
    # ========== 自进化系统 ==========
    
    def _record_usage(self, method: str, result: Dict, start_time: datetime):
        """记录使用情况"""
        self.usage_stats["total_calls"] += 1
        
        # 按方法统计
        if method not in self.usage_stats["by_method"]:
            self.usage_stats["by_method"][method] = {
                "calls": 0,
                "successes": 0,
                "failures": 0
            }
        
        self.usage_stats["by_method"][method]["calls"] += 1
        
        if result.get("success"):
            self.usage_stats["by_method"][method]["successes"] += 1
        else:
            self.usage_stats["by_method"][method]["failures"] += 1
        
        # 计算成功率
        total = self.usage_stats["by_method"][method]["calls"]
        successes = self.usage_stats["by_method"][method]["successes"]
        self.usage_stats["by_method"][method]["success_rate"] = successes / total if total > 0 else 0
        
        # 计算延迟
        latency = (datetime.now() - start_time).total_seconds()
        self.usage_stats["average_latency"] = (
            self.usage_stats["average_latency"] * 0.9 + latency * 0.1
        )
        
        # 保存统计
        self._save_usage_stats()
    
    def _record_success(self, method: str):
        """记录成功"""
        pass  # 已在_record_usage 中处理
    
    def _record_failure(self, method: str):
        """记录失败"""
        pass  # 已在_record_usage 中处理
    
    def _record_evolution_event(self, event_type: str, details: str):
        """记录进化事件"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        }
        
        # 添加到记忆
        self.skill_memories.append(event)
        
        # 保留最近 100 条
        if len(self.skill_memories) > 100:
            self.skill_memories = self.skill_memories[-100:]
        
        self._save_skill_memories()
    
    def _check_evolution(self, query: str, method: str, result: Dict):
        """检查是否需要进化"""
        # 1. 检查是否形成新模式
        if result.get("success"):
            self._try_crystallize_pattern(query, method)
        
        # 2. 检查是否需要优化策略
        self._check_strategy_optimization()
        
        # 3. 定期保存进化状态
        if self.usage_stats["total_calls"] % 10 == 0:
            self._save_evolution_state()
    
    def _try_crystallize_pattern(self, query: str, method: str):
        """尝试结晶模式"""
        # 检查是否已存在相似模式
        for pattern in self.crystallized_patterns:
            if self._match_pattern(query, pattern["query_pattern"]):
                pattern["usage_count"] += 1
                pattern["last_used"] = datetime.now().isoformat()
                return
        
        # 创建新模式 (使用 3 次后结晶)
        new_pattern = {
            "name": f"pattern_{len(self.crystallized_patterns) + 1}",
            "query_pattern": query,
            "method": method,
            "usage_count": 1,
            "created_at": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat()
        }
        
        self.crystallized_patterns.append(new_pattern)
        logger.info(f"✨ 创建新模式：{new_pattern['name']}")
        
        # 保存结晶模式
        self._save_crystallized_patterns()
    
    def _check_strategy_optimization(self):
        """检查策略优化"""
        # 分析各方法成功率
        for method, stats in self.usage_stats["by_method"].items():
            success_rate = stats.get("success_rate", 0)
            calls = stats.get("calls", 0)
            
            # 成功率低于 50% 且调用次数>10，标记需要优化
            if success_rate < 0.5 and calls > 10:
                logger.warning(f"⚠️ 方法 {method} 成功率低 ({success_rate:.1%}), 需要优化")
                self._record_evolution_event("optimization_needed", method)
    
    def _save_usage_stats(self):
        """保存使用统计"""
        stats_file = EVOLUTION_DIR / "usage_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.usage_stats, f, indent=2, ensure_ascii=False)
    
    def _save_skill_memories(self):
        """保存技能记忆"""
        memory_file = MEMORY_DIR / "skill_memories.json"
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.skill_memories, f, indent=2, ensure_ascii=False)
    
    def _save_crystallized_patterns(self):
        """保存结晶模式"""
        pattern_file = EVOLUTION_DIR / "crystallized_patterns.json"
        with open(pattern_file, 'w', encoding='utf-8') as f:
            json.dump(self.crystallized_patterns, f, indent=2, ensure_ascii=False)
    
    def _save_evolution_state(self):
        """保存进化状态"""
        state_file = EVOLUTION_DIR / "evolution_state.json"
        state = {
            "last_saved": datetime.now().isoformat(),
            "total_calls": self.usage_stats["total_calls"],
            "crystallized_patterns_count": len(self.crystallized_patterns),
            "memories_count": len(self.skill_memories)
        }
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 进化状态已保存")
    
    def get_evolution_report(self) -> Dict:
        """生成进化报告"""
        return {
            "skill_name": self.skill_name,
            "version": self.version,
            "generated_at": datetime.now().isoformat(),
            "usage_stats": self.usage_stats,
            "crystallized_patterns": len(self.crystallized_patterns),
            "skill_memories": len(self.skill_memories),
            "call_strategies": len(self.call_strategies),
            "top_methods": sorted(
                self.usage_stats["by_method"].items(),
                key=lambda x: x[1]["calls"],
                reverse=True
            )[:5]
        }


# 同步包装器
class AISearchSkillEvolutionSync:
    """AI 搜索 Skill 同步包装器"""
    
    def __init__(self):
        import asyncio
        self.loop = asyncio.new_event_loop()
        self.skill = AISearchSkillEvolution()
    
    def smart_call(self, query: str, context: Dict = None) -> Dict:
        """智能调用 (同步)"""
        return self.loop.run_until_complete(self.skill.smart_call(query, context))
    
    def search(self, query: str, limit: int = 10) -> Dict:
        """搜索 (同步)"""
        return self.loop.run_until_complete(self.skill.search(query, limit))
    
    def crawl(self, url: str) -> Dict:
        """爬取 (同步)"""
        return self.loop.run_until_complete(self.skill.crawl(url))
    
    def search_and_crawl(self, query: str, limit: int = 5) -> Dict:
        """搜索 + 爬取 (同步)"""
        return self.loop.run_until_complete(self.skill.search_and_crawl(query, limit))
    
    def agent_query(self, prompt: str) -> Dict:
        """Agent 查询 (同步)"""
        return self.loop.run_until_complete(self.skill.agent_query(prompt))


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🤖 AI 搜索 Skill (自进化版) - 演示")
    logger.info("=" * 60)
    
    # 初始化 Skill
    skill = AISearchSkillEvolution()
    
    # 生成进化报告
    logger.info("\n📊 生成进化报告...")
    report = skill.get_evolution_report()
    
    logger.info(f"\nSkill 名称：{report['skill_name']}")
    logger.info(f"版本：{report['version']}")
    logger.info(f"结晶模式：{report['crystallized_patterns']}个")
    logger.info(f"技能记忆：{report['skill_memories']}条")
    logger.info(f"调用策略：{report['call_strategies']}个")
    
    logger.info(f"\nTop 调用方法:")
    for method, stats in report['top_methods']:
        logger.info(f"  {method}: {stats['calls']}次 (成功率{stats['success_rate']:.1%})")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
