#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 搜索 Skill - 网络搜索 + 网页爬取 + 交互 + Agent
太一 AGI · 2026-04-19

功能:
- 网络搜索 (Firecrawl)
- 网页爬取 (Crawl4AI)
- 页面交互 (Firecrawl)
- Agent 自主查询 (Firecrawl)
- Markdown 输出
- 结构化数据提取

架构位置：太一 Skills 系统 → AI 搜索 Skill
灵感来源：Crawl4AI (58k+ ⭐) + Firecrawl (70k+ ⭐)
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('AISearchSkill')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "07-system" / "ai-search"
SKILL_DIR.mkdir(parents=True, exist_ok=True)


class AISearchSkill:
    """AI 搜索技能 - 供太一系统调用"""
    
    def __init__(self):
        """初始化 AI 搜索 Skill"""
        self.skill_name = "ai_search"
        self.version = "1.0.0"
        self.description = "AI 搜索技能 - 网络搜索 + 网页爬取 + 交互 + Agent"
        
        # 配置
        self.config = self._load_config()
        
        # 爬虫 (Crawl4AI)
        self.crawler = None
        self._init_crawler()
        
        # 搜索 API (Firecrawl)
        self.search_api = None
        self._init_search_api()
        
        # 统计
        self.stats = {
            "total_searches": 0,
            "total_crawls": 0,
            "total_interactions": 0,
            "total_agent_queries": 0
        }
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_file = SKILL_DIR / "skill_config.json"
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "crawler": "crawl4ai",
            "search": "firecrawl",
            "local_mode": True,
            "api_mode": False,
            "max_results": 10,
            "timeout": 30
        }
    
    def _init_crawler(self):
        """初始化爬虫 (Crawl4AI)"""
        try:
            from crawl4ai import AsyncWebCrawler
            self.crawler = AsyncWebCrawler()
            logger.info("✅ Crawl4AI 爬虫初始化成功")
        except ImportError:
            logger.warning("⚠️ Crawl4AI 未安装，爬虫功能不可用")
            logger.info("安装：pip install crawl4ai")
            self.crawler = None
    
    def _init_search_api(self):
        """初始化搜索 API (Firecrawl)"""
        try:
            from firecrawl import Firecrawl
            api_key = self.config.get("firecrawl_api_key", "")
            if api_key:
                self.search_api = Firecrawl(api_key=api_key)
                logger.info("✅ Firecrawl 搜索 API 初始化成功")
            else:
                logger.warning("⚠️ Firecrawl API Key 未配置，搜索功能不可用")
                logger.info("配置：在 skill_config.json 中添加 firecrawl_api_key")
                self.search_api = None
        except ImportError:
            logger.warning("⚠️ Firecrawl 未安装，搜索功能不可用")
            logger.info("安装：pip install firecrawl-py")
            self.search_api = None
    
    async def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        搜索功能 (Firecrawl)
        
        Args:
            query: 搜索查询
            limit: 结果数量
            
        Returns:
            搜索结果列表
        """
        logger.info(f"🔍 搜索：{query} (limit={limit})")
        
        if not self.search_api:
            logger.error("❌ 搜索 API 未初始化")
            return []
        
        try:
            results = await self.search_api.search(query, limit=limit)
            self.stats["total_searches"] += 1
            logger.info(f"✅ 搜索完成，{len(results)}个结果")
            return results
        except Exception as e:
            logger.error(f"❌ 搜索失败：{str(e)}")
            return []
    
    async def crawl(self, url: str, options: Dict = None) -> Dict:
        """
        爬取功能 (Crawl4AI)
        
        Args:
            url: 目标 URL
            options: 爬取选项
            
        Returns:
            爬取结果
        """
        logger.info(f"🕷️ 爬取：{url}")
        
        if not self.crawler:
            logger.error("❌ 爬虫未初始化")
            return {"success": False, "error": "Crawler not initialized"}
        
        try:
            async with self.crawler:
                result = await self.crawler.arun(url=url, **(options or {}))
                self.stats["total_crawls"] += 1
                logger.info(f"✅ 爬取完成，Markdown 长度：{len(result.markdown)}")
                return {
                    "success": True,
                    "url": url,
                    "markdown": result.markdown,
                    "html": result.html,
                    "metadata": result.metadata
                }
        except Exception as e:
            logger.error(f"❌ 爬取失败：{str(e)}")
            return {"success": False, "error": str(e)}
    
    async def search_and_crawl(self, query: str, limit: int = 5) -> List[Dict]:
        """
        搜索 + 爬取组合功能
        
        Args:
            query: 搜索查询
            limit: 结果数量
            
        Returns:
            搜索结果 + 完整内容
        """
        logger.info(f"🔍️ 搜索 + 爬取：{query} (limit={limit})")
        
        # 1. 搜索
        search_results = await self.search(query, limit)
        
        # 2. 爬取每个结果
        results = []
        for search_result in search_results:
            url = search_result.get("url")
            if url:
                crawl_result = await self.crawl(url)
                if crawl_result.get("success"):
                    results.append({
                        **search_result,
                        "content": crawl_result["markdown"],
                        "crawl_status": "success"
                    })
                else:
                    results.append({
                        **search_result,
                        "content": None,
                        "crawl_status": "failed"
                    })
        
        logger.info(f"✅ 搜索 + 爬取完成，{len(results)}个完整结果")
        return results
    
    async def agent_query(self, prompt: str) -> Dict:
        """
        Agent 自主查询 (Firecrawl)
        
        Args:
            prompt: 查询描述
            
        Returns:
            查询结果
        """
        logger.info(f"🤖 Agent 查询：{prompt[:50]}...")
        
        if not self.search_api:
            logger.error("❌ 搜索 API 未初始化")
            return {"success": False, "error": "Search API not initialized"}
        
        try:
            result = await self.search_api.agent(prompt)
            self.stats["total_agent_queries"] += 1
            logger.info(f"✅ Agent 查询完成")
            return result
        except Exception as e:
            logger.error(f"❌ Agent 查询失败：{str(e)}")
            return {"success": False, "error": str(e)}
    
    async def interact(self, url: str, actions: List[Dict]) -> Dict:
        """
        页面交互功能 (Firecrawl)
        
        Args:
            url: 目标 URL
            actions: 交互动作列表
            
        Returns:
            交互结果
        """
        logger.info(f"🖱️ 页面交互：{url} ({len(actions)}个动作)")
        
        if not self.search_api:
            logger.error("❌ 搜索 API 未初始化")
            return {"success": False, "error": "Search API not initialized"}
        
        try:
            # 1. 先爬取页面
            scrape_result = await self.search_api.scrape(url)
            scrape_id = scrape_result.get("metadata", {}).get("scrape_id")
            
            if not scrape_id:
                return {"success": False, "error": "Failed to get scrape_id"}
            
            # 2. 执行交互动作
            for action in actions:
                action_type = action.get("type")
                if action_type == "click":
                    await self.search_api.interact(scrape_id, prompt=f"Click {action.get('target')}")
                elif action_type == "scroll":
                    await self.search_api.interact(scrape_id, prompt="Scroll down")
                elif action_type == "type":
                    await self.search_api.interact(scrape_id, prompt=f"Type '{action.get('text')}'")
            
            self.stats["total_interactions"] += 1
            logger.info(f"✅ 页面交互完成")
            
            return {"success": True, "actions_completed": len(actions)}
        except Exception as e:
            logger.error(f"❌ 页面交互失败：{str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            **self.stats,
            "skill_name": self.skill_name,
            "version": self.version,
            "crawler_status": "ready" if self.crawler else "not_initialized",
            "search_api_status": "ready" if self.search_api else "not_initialized"
        }
    
    def save_config(self):
        """保存配置"""
        config_file = SKILL_DIR / "skill_config.json"
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 配置已保存：{config_file}")
    
    def generate_skill_report(self) -> Dict:
        """生成 Skill 报告"""
        logger.info("📊 生成 Skill 报告...")
        
        report = {
            "skill_name": self.skill_name,
            "version": self.version,
            "description": self.description,
            "generated_at": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "config": self.config,
            "endpoints": [
                "/search - 网络搜索",
                "/crawl - 网页爬取",
                "/search_and_crawl - 搜索 + 爬取",
                "/agent_query - Agent 自主查询",
                "/interact - 页面交互"
            ]
        }
        
        logger.info(f"✅ Skill 报告生成完成")
        
        return report


# 同步包装器 (供非异步代码调用)
class AISearchSkillSync:
    """AI 搜索 Skill 同步包装器"""
    
    def __init__(self):
        import asyncio
        self.loop = asyncio.new_event_loop()
        self.skill = AISearchSkill()
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索功能 (同步)"""
        return self.loop.run_until_complete(self.skill.search(query, limit))
    
    def crawl(self, url: str) -> Dict:
        """爬取功能 (同步)"""
        return self.loop.run_until_complete(self.skill.crawl(url))
    
    def search_and_crawl(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索 + 爬取 (同步)"""
        return self.loop.run_until_complete(self.skill.search_and_crawl(query, limit))
    
    def agent_query(self, prompt: str) -> Dict:
        """Agent 查询 (同步)"""
        return self.loop.run_until_complete(self.skill.agent_query(prompt))


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🤖 AI 搜索 Skill - 演示")
    logger.info("=" * 60)
    
    # 初始化 Skill
    skill = AISearchSkill()
    
    # 生成报告
    logger.info("\n📊 生成 Skill 报告...")
    report = skill.generate_skill_report()
    
    logger.info(f"\nSkill 名称：{report['skill_name']}")
    logger.info(f"版本：{report['version']}")
    logger.info(f"描述：{report['description']}")
    logger.info(f"\n可用端点:")
    for endpoint in report['endpoints']:
        logger.info(f"  {endpoint}")
    
    # 保存配置
    logger.info("\n💾 保存配置...")
    skill.save_config()
    
    # 获取统计
    logger.info("\n📊 统计信息:")
    stats = skill.get_stats()
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
