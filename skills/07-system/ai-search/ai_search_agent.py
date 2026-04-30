#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一 AI 搜索自进化 Agent - 智能涌现创建
太一 AGI · 2026-04-19 10:37

核心功能:
- 自主任务规划
- 多步骤搜索
- 结果分析总结
- 智能自动化执行

智能涌现依据:
- 综合评分：74.5 分
- 决策：CREATE_AGENT (本周)
- 优先级：P1 → 升级为 P0 (用户指令)
- 宪法：SELF-EVOLUTION-EMERGENCE.md
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import asyncio

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('TaiyiAISearchAgent')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
AGENT_DIR = WORKSPACE / "skills" / "07-system" / "ai-search"
AGENT_DIR.mkdir(parents=True, exist_ok=True)


class TaiyiAISearchAgent:
    """太一 AI 搜索自进化 Agent"""
    
    def __init__(self):
        self.agent_name = "taiyi_ai_search_agent"
        self.version = "1.0.0"
        self.description = "太一 AI 搜索自进化 Agent - 智能涌现创建"
        self.created_at = datetime.now().isoformat()
        
        # 核心能力
        self.capabilities = [
            "autonomous_planning",      # 自主任务规划
            "multi_step_search",        # 多步骤搜索
            "result_analysis",          # 结果分析总结
            "intelligent_execution",    # 智能自动化执行
            "self_evolution"            # 自进化
        ]
        
        # 导入 AI 搜索 Skill
        self.ai_search_skill = None
        self._init_ai_search_skill()
        
        # 统计
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "total_searches": 0
        }
        
        # 自进化
        self.task_memories = []
        self.planning_patterns = []
    
    def _init_ai_search_skill(self):
        """初始化 AI 搜索 Skill"""
        try:
            from taiyi_ai_search_evolution import TaiyiAISearchEvolution
            self.ai_search_skill = TaiyiAISearchEvolution()
            logger.info("✅ AI 搜索 Skill 初始化成功")
        except ImportError as e:
            logger.error(f"❌ AI 搜索 Skill 导入失败：{str(e)}")
            self.ai_search_skill = None
    
    async def plan_and_execute(self, user_query: str, context: Dict = None) -> Dict:
        """
        自主规划并执行
        
        Args:
            user_query: 用户查询
            context: 上下文信息
            
        Returns:
            执行结果
        """
        logger.info(f"🤖 AI 搜索 Agent 启动：{user_query[:50]}...")
        
        self.stats["total_tasks"] += 1
        
        # 1. 理解用户需求
        understanding = self._understand_user_need(user_query)
        
        # 2. 制定搜索计划
        plan = self._create_search_plan(understanding)
        
        # 3. 执行搜索
        results = await self._execute_search(plan)
        
        # 4. 分析结果
        analysis = self._analyze_results(results)
        
        # 5. 生成报告
        report = self._generate_report(understanding, plan, results, analysis)
        
        # 6. 记录记忆
        self._record_task_memory(user_query, plan, results, analysis)
        
        # 7. 自进化检查
        self._check_self_evolution()
        
        self.stats["completed_tasks"] += 1
        
        logger.info(f"✅ 任务完成：{user_query[:50]}...")
        
        return report
    
    def _understand_user_need(self, query: str) -> Dict:
        """理解用户需求"""
        logger.info("🧠 理解用户需求...")
        
        # 简单意图识别
        intent = "general_search"
        
        if any(word in query.lower() for word in ["分析", "调研", "report", "analyze"]):
            intent = "research_analysis"
        elif any(word in query.lower() for word in ["对比", "比较", "vs", "comparison"]):
            intent = "comparison"
        elif any(word in query.lower() for word in ["趋势", "trend", "预测", "forecast"]):
            intent = "trend_analysis"
        elif any(word in query.lower() for word in ["价格", "price", "成本", "cost"]):
            intent = "price_search"
        
        understanding = {
            "query": query,
            "intent": intent,
            "complexity": self._estimate_complexity(query),
            "expected_output": self._determine_expected_output(intent)
        }
        
        logger.info(f"  意图：{intent}")
        logger.info(f"  复杂度：{understanding['complexity']}")
        
        return understanding
    
    def _estimate_complexity(self, query: str) -> str:
        """估计复杂度"""
        words = len(query.split())
        
        if words <= 5:
            return "simple"
        elif words <= 15:
            return "medium"
        else:
            return "complex"
    
    def _determine_expected_output(self, intent: str) -> str:
        """确定期望输出"""
        output_map = {
            "general_search": "search_results",
            "research_analysis": "analysis_report",
            "comparison": "comparison_table",
            "trend_analysis": "trend_report",
            "price_search": "price_list"
        }
        return output_map.get(intent, "search_results")
    
    def _create_search_plan(self, understanding: Dict) -> Dict:
        """创建搜索计划"""
        logger.info("📋 制定搜索计划...")
        
        query = understanding["query"]
        intent = understanding["intent"]
        complexity = understanding["complexity"]
        
        # 根据复杂度制定计划
        if complexity == "simple":
            plan = {
                "steps": 1,
                "search_queries": [query],
                "methods": ["search"],
                "estimated_time": "1-2 分钟"
            }
        elif complexity == "medium":
            plan = {
                "steps": 2,
                "search_queries": [query, f"{query} 详细分析"],
                "methods": ["search_and_crawl"],
                "estimated_time": "3-5 分钟"
            }
        else:  # complex
            plan = {
                "steps": 3,
                "search_queries": [
                    query,
                    f"{query} 深度分析",
                    f"{query} 最新趋势 2026"
                ],
                "methods": ["multi_source_search", "search_and_crawl"],
                "estimated_time": "5-10 分钟"
            }
        
        logger.info(f"  步骤数：{plan['steps']}")
        logger.info(f"  预计时间：{plan['estimated_time']}")
        
        return plan
    
    async def _execute_search(self, plan: Dict) -> List[Dict]:
        """执行搜索"""
        logger.info("🔍 执行搜索...")
        
        if not self.ai_search_skill:
            logger.error("❌ AI 搜索 Skill 未初始化")
            return []
        
        results = []
        
        for i, query in enumerate(plan["search_queries"]):
            logger.info(f"  搜索 {i+1}/{len(plan['search_queries'])}: {query}")
            
            if plan["methods"][0] == "search":
                result = await self.ai_search_skill.search(query)
            elif plan["methods"][0] == "search_and_crawl":
                result = await self.ai_search_skill.search_and_crawl(query)
            elif plan["methods"][0] == "multi_source_search":
                result = await self.ai_search_skill.multi_source_search(query)
            else:
                result = await self.ai_search_skill.search(query)
            
            results.append(result)
            self.stats["total_searches"] += 1
        
        logger.info(f"✅ 搜索完成：{len(results)}个结果")
        
        return results
    
    def _analyze_results(self, results: List[Dict]) -> Dict:
        """分析结果"""
        logger.info("📊 分析结果...")
        
        analysis = {
            "total_results": len(results),
            "successful_searches": sum(1 for r in results if r.get("success")),
            "total_items": sum(r.get("count", 0) for r in results),
            "key_findings": [],
            "insights": []
        }
        
        # 提取关键发现
        for result in results:
            if result.get("success"):
                if "results" in result:
                    for item in result["results"][:3]:  # 前 3 个
                        analysis["key_findings"].append({
                            "title": item.get("title", ""),
                            "snippet": item.get("snippet", "")[:200]
                        })
        
        # 生成洞察
        if analysis["successful_searches"] > 0:
            analysis["insights"].append(f"成功完成{analysis['successful_searches']}次搜索")
            analysis["insights"].append(f"共找到{analysis['total_items']}个相关结果")
        
        logger.info(f"  关键发现：{len(analysis['key_findings'])}个")
        logger.info(f"  洞察：{len(analysis['insights'])}个")
        
        return analysis
    
    def _generate_report(self, understanding: Dict, plan: Dict, results: List[Dict], analysis: Dict) -> Dict:
        """生成报告"""
        logger.info("📄 生成报告...")
        
        report = {
            "agent": self.agent_name,
            "version": self.version,
            "generated_at": datetime.now().isoformat(),
            "query": understanding["query"],
            "intent": understanding["intent"],
            "plan": plan,
            "results": results,
            "analysis": analysis,
            "summary": self._generate_summary(understanding, analysis),
            "recommendations": self._generate_recommendations(analysis)
        }
        
        logger.info("✅ 报告生成完成")
        
        return report
    
    def _generate_summary(self, understanding: Dict, analysis: Dict) -> str:
        """生成摘要"""
        summary = f"""
【太一 AI 搜索 Agent 报告】

查询：{understanding['query']}
意图：{understanding['intent']}

执行结果:
- 成功搜索：{analysis['successful_searches']}次
- 找到结果：{analysis['total_items']}个
- 关键发现：{len(analysis['key_findings'])}个

核心洞察:
"""
        for insight in analysis["insights"][:3]:
            summary += f"- {insight}\n"
        
        return summary
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if analysis["total_items"] > 100:
            recommendations.append("建议进一步筛选关键信息")
        
        if analysis["successful_searches"] < len(analysis["total_results"]):
            recommendations.append("部分搜索失败，建议重试")
        
        if not recommendations:
            recommendations.append("搜索结果良好，可直接使用")
        
        return recommendations
    
    def _record_task_memory(self, query: str, plan: Dict, results: List[Dict], analysis: Dict):
        """记录任务记忆"""
        memory = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "plan": plan,
            "results_summary": {
                "total_results": len(results),
                "successful_searches": analysis["successful_searches"]
            },
            "success": analysis["successful_searches"] > 0
        }
        
        self.task_memories.append(memory)
        
        # 保留最近 100 条
        if len(self.task_memories) > 100:
            self.task_memories = self.task_memories[-100:]
    
    def _check_self_evolution(self):
        """自进化检查"""
        # 检查是否形成新模式
        if len(self.task_memories) >= 10:
            self._try_create_planning_pattern()
    
    def _try_create_planning_pattern(self):
        """尝试创建规划模式"""
        # 分析最近任务，找出共同模式
        recent_queries = [m["query"] for m in self.task_memories[-10:]]
        
        # 简单模式识别
        common_words = set()
        for query in recent_queries:
            words = set(query.lower().split())
            if not common_words:
                common_words = words
            else:
                common_words &= words
        
        if len(common_words) >= 2:
            pattern = {
                "name": f"pattern_{len(self.planning_patterns) + 1}",
                "common_words": list(common_words),
                "created_at": datetime.now().isoformat()
            }
            self.planning_patterns.append(pattern)
            logger.info(f"✨ 创建规划模式：{pattern['name']}")
    
    def get_agent_stats(self) -> Dict:
        """获取 Agent 统计"""
        return {
            "agent_name": self.agent_name,
            "version": self.version,
            "stats": self.stats,
            "task_memories": len(self.task_memories),
            "planning_patterns": len(self.planning_patterns),
            "capabilities": self.capabilities
        }
    
    def get_agent_report(self) -> Dict:
        """生成 Agent 报告"""
        return {
            "agent_name": self.agent_name,
            "version": self.version,
            "description": self.description,
            "created_at": self.created_at,
            "generated_at": datetime.now().isoformat(),
            "stats": self.get_agent_stats(),
            "capabilities": self.capabilities
        }


# 同步包装器
class TaiyiAISearchAgentSync:
    """太一 AI 搜索自进化 Agent 同步包装器"""
    
    def __init__(self):
        import asyncio
        self.loop = asyncio.new_event_loop()
        self.agent = TaiyiAISearchAgent()
    
    def plan_and_execute(self, user_query: str, context: Dict = None) -> Dict:
        """自主规划并执行 (同步)"""
        return self.loop.run_until_complete(self.agent.plan_and_execute(user_query, context))
    
    def get_stats(self) -> Dict:
        """获取统计 (同步)"""
        return self.loop.run_until_complete(self.agent.get_agent_stats())


def main():
    """主函数 - 演示"""
    logger.info("=" * 60)
    logger.info("🤖 太一 AI 搜索自进化 Agent - 智能涌现创建")
    logger.info("=" * 60)
    
    # 初始化 Agent
    agent = TaiyiAISearchAgent()
    
    # 生成 Agent 报告
    logger.info("\n📊 生成 Agent 报告...")
    report = agent.get_agent_report()
    
    logger.info(f"\nAgent 名称：{report['agent_name']}")
    logger.info(f"版本：{report['version']}")
    logger.info(f"描述：{report['description']}")
    logger.info(f"创建时间：{report['created_at']}")
    logger.info(f"\n核心能力:")
    for cap in report['capabilities']:
        logger.info(f"  • {cap}")
    
    logger.info(f"\n统计信息:")
    logger.info(f"  总任务数：{report['stats']['stats']['total_tasks']}")
    logger.info(f"  完成任务数：{report['stats']['stats']['completed_tasks']}")
    logger.info(f"  任务记忆：{report['stats']['task_memories']}条")
    logger.info(f"  规划模式：{report['stats']['planning_patterns']}个")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
