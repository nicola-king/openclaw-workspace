#!/usr/bin/env python3
"""
10D 评分系统实现

功能:
1. 10 维度评分算法
2. 加权平均计算
3. 职位/项目/技能评估
4. 推荐等级系统

作者：太一 AGI
创建：2026-04-10
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ScoreResult:
    """评分结果"""
    total: float
    breakdown: Dict[str, float]
    recommendation: str
    details: Dict


class TenDScore:
    """10D 评分系统"""
    
    def __init__(self):
        self.weights = {
            "match": 0.15,          # 匹配度
            "growth": 0.15,         # 成长性
            "impact": 0.10,         # 影响力
            "learning": 0.10,       # 学习价值
            "team": 0.10,           # 团队质量
            "tech_stack": 0.10,     # 技术栈
            "company": 0.10,        # 公司前景
            "compensation": 0.10,   # 薪资福利
            "wlb": 0.05,            # 工作生活平衡
            "location": 0.05        # 地理位置
        }
    
    def score(self, target: Dict, dimensions: List[str] = None) -> ScoreResult:
        """
        10D 评分
        
        Args:
            target: 评估目标 (职位/项目/技能)
            dimensions: 评分维度 (默认全部)
        
        Returns:
            ScoreResult 评分结果
        """
        if dimensions is None:
            dimensions = list(self.weights.keys())
        
        # 各维度评分
        scores = {}
        for dim in dimensions:
            scores[dim] = self._evaluate(target, dim)
        
        # 加权平均
        total_score = sum(
            scores[dim] * self.weights[dim]
            for dim in dimensions
        )
        
        # 推荐等级
        recommendation = self._get_recommendation(total_score)
        
        return ScoreResult(
            total=round(total_score, 2),
            breakdown=scores,
            recommendation=recommendation,
            details=target
        )
    
    def _evaluate(self, target: Dict, dimension: str) -> float:
        """评估单个维度"""
        
        evaluators = {
            "match": self._eval_match,
            "growth": self._eval_growth,
            "impact": self._eval_impact,
            "learning": self._eval_learning,
            "team": self._eval_team,
            "tech_stack": self._eval_tech_stack,
            "company": self._eval_company,
            "compensation": self._eval_compensation,
            "wlb": self._eval_wlb,
            "location": self._eval_location
        }
        
        evaluator = evaluators.get(dimension)
        if evaluator:
            return evaluator(target)
        return 5.0  # 默认中等分数
    
    def _eval_match(self, target: Dict) -> float:
        """匹配度评分"""
        match_rate = target.get("match_rate", 0.5)
        if match_rate > 0.9:
            return 9.5
        elif match_rate > 0.7:
            return 8.0
        elif match_rate > 0.5:
            return 6.0
        elif match_rate > 0.3:
            return 4.0
        else:
            return 2.0
    
    def _eval_growth(self, target: Dict) -> float:
        """成长性评分"""
        growth_potential = target.get("growth_potential", "medium")
        scores = {"low": 3.0, "medium": 6.0, "high": 8.5, "explosive": 9.5}
        return scores.get(growth_potential, 6.0)
    
    def _eval_impact(self, target: Dict) -> float:
        """影响力评分"""
        impact_level = target.get("impact_level", "medium")
        scores = {"low": 3.0, "medium": 6.0, "high": 8.5, "massive": 9.5}
        return scores.get(impact_level, 6.0)
    
    def _eval_learning(self, target: Dict) -> float:
        """学习价值评分"""
        learning_opportunities = target.get("learning_opportunities", [])
        if len(learning_opportunities) > 5:
            return 9.0
        elif len(learning_opportunities) > 3:
            return 7.5
        elif len(learning_opportunities) > 1:
            return 6.0
        else:
            return 4.0
    
    def _eval_team(self, target: Dict) -> float:
        """团队质量评分"""
        team_quality = target.get("team_quality", "medium")
        scores = {"low": 3.0, "medium": 6.0, "high": 8.5, "excellent": 9.5}
        return scores.get(team_quality, 6.0)
    
    def _eval_tech_stack(self, target: Dict) -> float:
        """技术栈评分"""
        tech_stack = target.get("tech_stack", [])
        if len(tech_stack) > 5:
            return 9.0
        elif len(tech_stack) > 3:
            return 7.5
        elif len(tech_stack) > 1:
            return 6.0
        else:
            return 4.0
    
    def _eval_company(self, target: Dict) -> float:
        """公司前景评分"""
        company_stage = target.get("company_stage", "growth")
        scores = {"startup": 7.0, "growth": 8.5, "mature": 7.5, "decline": 3.0}
        return scores.get(company_stage, 7.0)
    
    def _eval_compensation(self, target: Dict) -> float:
        """薪资福利评分"""
        compensation_level = target.get("compensation_level", "market")
        scores = {"below": 3.0, "market": 6.0, "above": 8.0, "excellent": 9.5}
        return scores.get(compensation_level, 6.0)
    
    def _eval_wlb(self, target: Dict) -> float:
        """工作生活平衡评分"""
        wlb_rating = target.get("wlb_rating", "medium")
        scores = {"poor": 2.0, "fair": 5.0, "good": 7.5, "excellent": 9.0}
        return scores.get(wlb_rating, 6.0)
    
    def _eval_location(self, target: Dict) -> float:
        """地理位置评分"""
        location_score = target.get("location_score", 6.0)
        return min(10.0, max(1.0, location_score))
    
    def _get_recommendation(self, score: float) -> str:
        """获取推荐等级"""
        if score >= 8.0:
            return "⭐⭐⭐⭐⭐ 强烈推荐 - 立即执行"
        elif score >= 6.0:
            return "⭐⭐⭐⭐ 推荐 - 建议执行"
        elif score >= 4.0:
            return "⭐⭐⭐ 中性 - 观望"
        elif score >= 2.0:
            return "⭐⭐ 谨慎 - 谨慎考虑"
        else:
            return "⭐ 不推荐 - 跳过"


def main():
    """主函数 - 测试"""
    print("📊 10D 评分系统测试")
    print("="*60)
    
    scorer = TenDScore()
    
    # 测试用例
    test_target = {
        "match_rate": 0.85,
        "growth_potential": "high",
        "impact_level": "high",
        "learning_opportunities": ["新技术", "新领域", "跨团队协作"],
        "team_quality": "excellent",
        "tech_stack": ["Python", "React", "AI/ML", "Cloud"],
        "company_stage": "growth",
        "compensation_level": "above",
        "wlb_rating": "good",
        "location_score": 8.0
    }
    
    result = scorer.score(test_target)
    
    print(f"\n总分：{result.total}/10")
    print(f"推荐：{result.recommendation}")
    print("\n维度评分:")
    for dim, score in result.breakdown.items():
        print(f"  {dim}: {score}/10")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
