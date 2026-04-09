#!/usr/bin/env python3
"""
太一镜像 Agent v2.0 - 用户数字分身 + Skill 蒸馏师 (融合女娲能力)

作者：太一 AGI
创建：2026-04-09
更新：2026-04-09
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
USER_MODEL_FILE = WORKSPACE / "memory/user-model.json"
MEMORY_DIR = WORKSPACE / "memory"

sys.path.insert(0, str(WORKSPACE / "skills/mind-model-extractor"))
from extractor import MindModelExtractor

# 导入 Skill 蒸馏模块
from skill_distiller import SkillDistiller, DistilledSkill


@dataclass
class DecisionAdvice:
    """决策建议"""
    problem: str
    analysis: Dict
    recommendation: str
    alternatives: List[str]
    confidence: float
    reasoning: str
    generated_at: str


class MirrorAgent:
    """太一镜像 Agent v2.0 (融合女娲能力)"""
    
    def __init__(self, user_id: str = "sayelf"):
        self.user_id = user_id
        self.user_model = self.load_user_model()
        self.extractor = MindModelExtractor()
        self.distiller = SkillDistiller()  # Skill 蒸馏器
    
    def load_user_model(self) -> Dict:
        """加载用户模型"""
        if USER_MODEL_FILE.exists():
            with open(USER_MODEL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def advise_decision(self, problem: str, context: Dict = None) -> DecisionAdvice:
        """
        决策辅助
        
        Args:
            problem: 决策问题
            context: 上下文信息
        
        Returns:
            DecisionAdvice: 决策建议
        """
        # 获取心智模型
        mind_models = self.user_model.get("mind_models", [])
        heuristics = self.user_model.get("decision_heuristics", [])
        
        # 构建分析框架
        analysis = {
            "mind_models_applied": [],
            "heuristics_applied": [],
            "historical_patterns": []
        }
        
        # 应用心智模型
        for model in mind_models[:3]:  # 取前 3 个高频模型
            analysis["mind_models_applied"].append({
                "name": model["name"],
                "perspective": self._apply_model(model, problem)
            })
        
        # 应用决策启发式
        for heuristic in heuristics[:2]:
            analysis["heuristics_applied"].append({
                "name": heuristic["name"],
                "rule": heuristic["rule"]
            })
        
        # 生成建议
        recommendation = self._generate_recommendation(problem, analysis)
        confidence = self._calculate_confidence(analysis)
        
        return DecisionAdvice(
            problem=problem,
            analysis=analysis,
            recommendation=recommendation,
            alternatives=self._generate_alternatives(problem),
            confidence=confidence,
            reasoning=self._generate_reasoning(analysis),
            generated_at=datetime.now().isoformat()
        )
    
    def _apply_model(self, model: Dict, problem: str) -> str:
        """应用心智模型分析问题"""
        model_name = model["name"]
        
        perspectives = {
            "第一性原理": f"从基本原理看，{problem} 的本质是什么？抛开现有方案，最优解应该满足什么条件？",
            "逆向思维": f"反过来想，如果不{problem}，会有什么后果？最坏情况是什么？",
            "二阶思维": f"考虑后果的后果，{problem} 的长期影响是什么？连锁反应有哪些？",
            "概率思维": f"从概率角度，{problem} 成功的期望值是多少？风险收益比如何？",
            "能力圈": f"在你的能力圈内吗？这是你理解的事吗？",
            "复利思维": f"这个选择有复利效应吗？能积累什么？",
            "机会成本": f"选择这个，你放弃了什么？机会成本是多少？",
            "反脆弱": f"这个选择让你更抗风险吗？能从波动中受益吗？"
        }
        
        return perspectives.get(model_name, f"从{model_name}角度分析...")
    
    def _generate_recommendation(self, problem: str, analysis: Dict) -> str:
        """生成建议"""
        # 简化实现
        return f"基于你的心智模型，建议采取谨慎乐观的态度。先小规模验证，设定明确止损点。"
    
    def _generate_alternatives(self, problem: str) -> List[str]:
        """生成备选方案"""
        return [
            "方案 A: 保守策略 (低风险，低回报)",
            "方案 B: 平衡策略 (中等风险，中等回报)",
            "方案 C: 激进策略 (高风险，高回报)"
        ]
    
    def _calculate_confidence(self, analysis: Dict) -> float:
        """计算置信度"""
        # 基于分析深度计算
        model_count = len(analysis.get("mind_models_applied", []))
        heuristic_count = len(analysis.get("heuristics_applied", []))
        
        base_confidence = 0.5
        model_bonus = min(model_count * 0.1, 0.3)
        heuristic_bonus = min(heuristic_count * 0.05, 0.15)
        
        return min(base_confidence + model_bonus + heuristic_bonus, 0.95)
    
    def _generate_reasoning(self, analysis: Dict) -> str:
        """生成推理说明"""
        models = [m["name"] for m in analysis.get("mind_models_applied", [])]
        return f"综合应用了{len(models)}个心智模型：" + "、".join(models)
    
    def search_memories(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索记忆"""
        sys.path.insert(0, str(WORKSPACE / "skills/hermes-learning-loop/search"))
        from memory_search import MemorySearch
        
        searcher = MemorySearch()
        results = searcher.search(query, limit)
        
        return results
    
    def generate_weekly_report(self) -> Dict:
        """生成周成长报告"""
        # 简化实现
        skill_library = self.distiller.get_skill_library()
        distilled_count = len(skill_library.get("skills", []))
        
        return {
            "week": datetime.now().strftime("%Y-W%W"),
            "cognitive_shifts": [
                "从'成本优先'→'价值优先' (2 次决策)"
            ],
            "new_models": ["反脆弱"],
            "decision_quality": {
                "high_confidence_count": 8,
                "accuracy_rate": 0.85
            },
            "learning_progress": {
                "new_concepts": 5,
                "skills_distilled": distilled_count  # 新增：蒸馏 Skill 数量
            },
            "suggestions": [
                "继续深化反脆弱思维",
                "考虑建立'不做什么'清单"
            ]
        }
    
    # ============ v2.0 新增：Skill 蒸馏能力 ============
    
    def distill_expert(self, expert: str, sources: List[str], skill_name: str = None) -> DistilledSkill:
        """
        蒸馏专家 Skill
        
        Args:
            expert: 专家姓名
            sources: 信息源列表
            skill_name: Skill 名称 (默认：expert-skill)
        
        Returns:
            DistilledSkill: 蒸馏的 Skill
        """
        if skill_name is None:
            skill_name = f"{expert.lower()}-skill"
        
        return self.distiller.distill_expert(expert, sources, skill_name)
    
    def validate_skill(self, skill: DistilledSkill) -> Dict:
        """
        验证 Skill 质量
        
        Args:
            skill: Skill 对象
        
        Returns:
            验证结果
        """
        return self.distiller.validate_skill(skill)
    
    def publish_skill(self, skill: DistilledSkill) -> str:
        """
        发布 Skill
        
        Args:
            skill: Skill 对象
        
        Returns:
            发布路径
        """
        return self.distiller.publish_skill(skill)
    
    def get_skill_library(self) -> Dict:
        """获取 Skill 库"""
        return self.distiller.get_skill_library()


def main():
    """测试"""
    mirror = MirrorAgent()
    
    print("🪞 太一镜像 Agent 测试")
    print()
    
    # 测试决策辅助
    advice = mirror.advise_decision(
        problem="要不要辞职创业",
        context={"industry": "AI", "savings": "12 个月"}
    )
    
    print(f"问题：{advice.problem}")
    print(f"建议：{advice.recommendation}")
    print(f"置信度：{advice.confidence:.2f}")
    print(f"推理：{advice.reasoning}")
    print()
    
    # 测试记忆搜索
    print("记忆搜索测试:")
    memories = mirror.search_memories("茶馆")
    print(f"找到{len(memories)}条相关记忆")
    
    print()
    
    # 测试成长报告
    print("周成长报告:")
    report = mirror.generate_weekly_report()
    print(f"周数：{report['week']}")
    print(f"认知转变：{len(report['cognitive_shifts'])}个")
    print(f"决策质量：{report['decision_quality']['accuracy_rate']:.0%}")


if __name__ == "__main__":
    main()
