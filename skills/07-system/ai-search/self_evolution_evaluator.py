#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一系统自进化算法 - AI 搜索 Skill Agent 智能涌现评估
太一 AGI · 2026-04-19

评估维度:
1. 使用频率 (调用次数/增长率)
2. 功能完整性 (核心功能/增强功能)
3. 复杂度 (代码行数/依赖关系)
4. 用户需求 (查询类型/复杂度)
5. 自进化程度 (结晶模式/技能记忆)
6. 协同需求 (与其他 Skills 协同)

决策标准:
- 综合评分 >= 80: 立即创建 Agent
- 综合评分 60-79: 本周创建 Agent
- 综合评分 40-59: 下周创建 Agent
- 综合评分 < 40: 暂不创建
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('SelfEvolutionEvaluator')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "07-system" / "ai-search"
EVOLUTION_DIR = SKILL_DIR / "evolution"


class SelfEvolutionEvaluator:
    """太一系统自进化评估器"""
    
    def __init__(self, skill_name: str = "taiyi_ai_search_evolution"):
        self.skill_name = skill_name
        self.skill_dir = SKILL_DIR
        self.evolution_dir = EVOLUTION_DIR
        
        # 评估维度权重
        self.weights = {
            "usage_frequency": 0.20,      # 使用频率 20%
            "functionality": 0.25,        # 功能完整性 25%
            "complexity": 0.15,           # 复杂度 15%
            "user_demand": 0.20,          # 用户需求 20%
            "evolution_degree": 0.15,     # 自进化程度 15%
            "collaboration": 0.05         # 协同需求 5%
        }
        
        # 评估结果
        self.evaluation_result = {}
    
    def evaluate(self) -> Dict:
        """执行完整评估"""
        logger.info("=" * 60)
        logger.info("🧬 太一系统自进化算法 - AI 搜索 Skill Agent 智能涌现评估")
        logger.info("=" * 60)
        
        # 1. 使用频率评估
        usage_score = self._evaluate_usage_frequency()
        
        # 2. 功能完整性评估
        functionality_score = self._evaluate_functionality()
        
        # 3. 复杂度评估
        complexity_score = self._evaluate_complexity()
        
        # 4. 用户需求评估
        demand_score = self._evaluate_user_demand()
        
        # 5. 自进化程度评估
        evolution_score = self._evaluate_evolution_degree()
        
        # 6. 协同需求评估
        collaboration_score = self._evaluate_collaboration()
        
        # 计算综合评分
        total_score = (
            usage_score * self.weights["usage_frequency"] +
            functionality_score * self.weights["functionality"] +
            complexity_score * self.weights["complexity"] +
            demand_score * self.weights["user_demand"] +
            evolution_score * self.weights["evolution_degree"] +
            collaboration_score * self.weights["collaboration"]
        )
        
        # 生成评估结果
        self.evaluation_result = {
            "skill_name": self.skill_name,
            "evaluated_at": datetime.now().isoformat(),
            "scores": {
                "usage_frequency": usage_score,
                "functionality": functionality_score,
                "complexity": complexity_score,
                "user_demand": demand_score,
                "evolution_degree": evolution_score,
                "collaboration": collaboration_score
            },
            "weights": self.weights,
            "total_score": round(total_score, 2),
            "decision": self._make_decision(total_score),
            "reasoning": self._generate_reasoning()
        }
        
        # 保存评估结果
        self._save_evaluation()
        
        # 输出评估报告
        self._print_evaluation_report()
        
        return self.evaluation_result
    
    def _evaluate_usage_frequency(self) -> float:
        """评估使用频率"""
        logger.info("\n📊 评估维度 1: 使用频率")
        
        stats_file = self.evolution_dir / "usage_stats.json"
        
        if not stats_file.exists():
            logger.info("  ⚠️ 使用统计文件不存在，使用默认值")
            return 50.0
        
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        total_calls = stats.get("total_calls", 0)
        
        # 评分标准
        if total_calls >= 1000:
            score = 100.0
            reason = "调用次数>=1000，使用频率极高"
        elif total_calls >= 500:
            score = 90.0
            reason = "调用次数>=500，使用频率高"
        elif total_calls >= 100:
            score = 70.0
            reason = "调用次数>=100，使用频率中等"
        elif total_calls >= 10:
            score = 50.0
            reason = "调用次数>=10，使用频率较低"
        else:
            score = 30.0
            reason = "调用次数<10，使用频率低"
        
        logger.info(f"  总调用次数：{total_calls}")
        logger.info(f"  评分：{score} - {reason}")
        
        return score
    
    def _evaluate_functionality(self) -> float:
        """评估功能完整性"""
        logger.info("\n📊 评估维度 2: 功能完整性")
        
        # 检查核心功能
        core_functions = [
            "smart_call",      # 智能调用
            "search",          # 搜索
            "crawl",           # 爬取
            "search_and_crawl" # 搜索 + 爬取
        ]
        
        # 检查增强功能
        enhanced_functions = [
            "multi_source_search",  # 7 大数据源搜索
            "interact",             # 交互功能
            "agent_query"           # Agent 自主查询
        ]
        
        # 读取源代码
        skill_file = self.skill_dir / "taiyi_ai_search_evolution.py"
        if not skill_file.exists():
            return 50.0
        
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计实现的功能
        core_implemented = sum(1 for func in core_functions if f"async def {func}" in content)
        enhanced_implemented = sum(1 for func in enhanced_functions if f"async def {func}" in content)
        
        # 评分
        core_score = (core_implemented / len(core_functions)) * 70
        enhanced_score = (enhanced_implemented / len(enhanced_functions)) * 30
        total_score = core_score + enhanced_score
        
        logger.info(f"  核心功能：{core_implemented}/{len(core_functions)}")
        logger.info(f"  增强功能：{enhanced_implemented}/{len(enhanced_functions)}")
        logger.info(f"  评分：{total_score:.1f}")
        
        return total_score
    
    def _evaluate_complexity(self) -> float:
        """评估复杂度"""
        logger.info("\n📊 评估维度 3: 复杂度")
        
        skill_file = self.skill_dir / "taiyi_ai_search_evolution.py"
        
        if not skill_file.exists():
            return 50.0
        
        # 读取源代码
        with open(skill_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        # 评分标准
        if total_lines >= 800:
            score = 100.0
            reason = "代码>=800 行，复杂度高"
        elif total_lines >= 500:
            score = 80.0
            reason = "代码>=500 行，复杂度中等"
        elif total_lines >= 200:
            score = 60.0
            reason = "代码>=200 行，复杂度较低"
        else:
            score = 40.0
            reason = "代码<200 行，复杂度低"
        
        logger.info(f"  代码行数：{total_lines}")
        logger.info(f"  评分：{score} - {reason}")
        
        return score
    
    def _evaluate_user_demand(self) -> float:
        """评估用户需求"""
        logger.info("\n📊 评估维度 4: 用户需求")
        
        # 分析技能记忆中的查询类型
        memory_file = self.evolution_dir.parent / "memory" / "skill_memories.json"
        
        if not memory_file.exists():
            # 基于搜索功能的重要性评估
            logger.info("  ⚠️ 技能记忆文件不存在，基于功能重要性评估")
            return 85.0  # 搜索是核心需求
        
        with open(memory_file, 'r', encoding='utf-8') as f:
            memories = json.load(f)
        
        # 分析查询复杂度
        complex_queries = 0
        total_queries = len(memories)
        
        for memory in memories:
            details = memory.get("details", "")
            if any(keyword in details.lower() for keyword in ["分析", "调研", "报告", "analyze", "research"]):
                complex_queries += 1
        
        # 评分
        if total_queries > 0:
            complex_ratio = complex_queries / total_queries
            score = 60.0 + (complex_ratio * 40)
        else:
            score = 85.0  # 搜索是核心需求
        
        logger.info(f"  总查询数：{total_queries}")
        logger.info(f"  复杂查询：{complex_queries}")
        logger.info(f"  评分：{score:.1f}")
        
        return score
    
    def _evaluate_evolution_degree(self) -> float:
        """评估自进化程度"""
        logger.info("\n📊 评估维度 5: 自进化程度")
        
        # 检查结晶模式
        pattern_file = self.evolution_dir / "crystallized_patterns.json"
        pattern_count = 0
        if pattern_file.exists():
            with open(pattern_file, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
                pattern_count = len(patterns)
        
        # 检查技能记忆
        memory_file = self.evolution_dir.parent / "memory" / "skill_memories.json"
        memory_count = 0
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                memories = json.load(f)
                memory_count = len(memories)
        
        # 评分
        evolution_score = min(100, (pattern_count * 10) + (memory_count * 2))
        
        # 基础分 (自进化系统已实现)
        base_score = 70.0
        total_score = base_score + evolution_score
        
        logger.info(f"  结晶模式：{pattern_count}个")
        logger.info(f"  技能记忆：{memory_count}条")
        logger.info(f"  评分：{min(100, total_score)}")
        
        return min(100, total_score)
    
    def _evaluate_collaboration(self) -> float:
        """评估协同需求"""
        logger.info("\n📊 评估维度 6: 协同需求")
        
        # 检查与其他 Skills 的协同
        # AI 搜索 Skill 需要与多个 Skills 协同
        potential_collaborations = [
            "cross-border-trade-agent",  # 跨境贸易
            "product-trend-researcher",  # 产品趋势
            "smart-router",              # 智能路由
            "taiyi-multi-agent"          # 多 Agent 系统
        ]
        
        # 检查 Bot 管理器
        bot_manager_file = self.skill_dir / "unified_search_bot_manager.py"
        has_bot_manager = bot_manager_file.exists()
        
        # 评分
        collaboration_score = 50.0  # 基础分
        
        if has_bot_manager:
            collaboration_score += 30.0
            logger.info("  ✅ 已创建 Bot 管理器")
        
        collaboration_score += len(potential_collaborations) * 5
        logger.info(f"  潜在协同：{len(potential_collaborations)}个")
        logger.info(f"  评分：{min(100, collaboration_score)}")
        
        return min(100, collaboration_score)
    
    def _make_decision(self, total_score: float) -> Dict:
        """做出决策"""
        if total_score >= 80:
            return {
                "action": "create_agent",
                "timing": "immediate",
                "priority": "P0",
                "reason": "综合评分>=80，立即创建 Agent"
            }
        elif total_score >= 60:
            return {
                "action": "create_agent",
                "timing": "this_week",
                "priority": "P1",
                "reason": "综合评分 60-79，本周创建 Agent"
            }
        elif total_score >= 40:
            return {
                "action": "create_agent",
                "timing": "next_week",
                "priority": "P2",
                "reason": "综合评分 40-59，下周创建 Agent"
            }
        else:
            return {
                "action": "wait",
                "timing": "later",
                "priority": "P3",
                "reason": "综合评分<40，暂不创建 Agent"
            }
    
    def _generate_reasoning(self) -> str:
        """生成推理说明"""
        scores = self.evaluation_result.get("scores", {})
        decision = self.evaluation_result.get("decision", {})
        
        reasoning = f"""
智能涌现推理:

1. 使用频率：{scores.get('usage_frequency', 0):.1f}分 (权重{self.weights['usage_frequency']*100:.0f}%)
2. 功能完整性：{scores.get('functionality', 0):.1f}分 (权重{self.weights['functionality']*100:.0f}%)
3. 复杂度：{scores.get('complexity', 0):.1f}分 (权重{self.weights['complexity']*100:.0f}%)
4. 用户需求：{scores.get('user_demand', 0):.1f}分 (权重{self.weights['user_demand']*100:.0f}%)
5. 自进化程度：{scores.get('evolution_degree', 0):.1f}分 (权重{self.weights['evolution_degree']*100:.0f}%)
6. 协同需求：{scores.get('collaboration', 0):.1f}分 (权重{self.weights['collaboration']*100:.0f}%)

综合评分：{self.evaluation_result.get('total_score', 0):.2f}分

决策：{decision.get('reason')}

建议：
- AI 搜索是太一系统核心基础设施
- 7 大数据源搜索是太一独有优势
- 自进化系统已完备
- 建议：{decision.get('action', 'wait').replace('_', ' ')}
"""
        return reasoning
    
    def _save_evaluation(self):
        """保存评估结果"""
        eval_file = self.evolution_dir / "agent_emergence_evaluation.json"
        with open(eval_file, 'w', encoding='utf-8') as f:
            json.dump(self.evaluation_result, f, indent=2, ensure_ascii=False)
        logger.info(f"\n💾 评估结果已保存：{eval_file}")
    
    def _print_evaluation_report(self):
        """打印评估报告"""
        logger.info("\n" + "=" * 60)
        logger.info("🧬 太一系统自进化算法 - 评估报告")
        logger.info("=" * 60)
        logger.info(self.evaluation_result["reasoning"])
        logger.info("=" * 60)


def main():
    """主函数"""
    evaluator = SelfEvolutionEvaluator()
    result = evaluator.evaluate()
    
    # 输出决策
    decision = result["decision"]
    logger.info("\n" + "=" * 60)
    logger.info("🤖 太一系统自主决策")
    logger.info("=" * 60)
    logger.info(f"决策：{decision['action']}")
    logger.info(f"时间：{decision['timing']}")
    logger.info(f"优先级：{decision['priority']}")
    logger.info(f"原因：{decision['reason']}")
    logger.info("=" * 60)
    
    return result


if __name__ == "__main__":
    main()
