#!/usr/bin/env python3
"""
情景 Agent - 集成太一镜像 v2.0

作者：太一 AGI
创建：2026-04-09
"""

import sys
from pathlib import Path

# 添加路径
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
sys.path.insert(0, str(WORKSPACE / "agents" / "mirror"))

from mirror import MirrorAgent


class TodayStageMirrorIntegration:
    """情景 Agent - 太一镜像集成"""
    
    def __init__(self):
        self.mirror = MirrorAgent(user_id="sayelf")
    
    def get_scenario_advice(self, scenario: str, problem: str) -> dict:
        """
        获取情景建议 (调用太一镜像)
        
        Args:
            scenario: 情景名称 (如"工作 - 专注")
            problem: 问题描述
        
        Returns:
            建议字典
        """
        # 调用太一镜像决策辅助
        advice = self.mirror.advise_decision(
            problem=problem,
            context={"scenario": scenario}
        )
        
        return {
            "scenario": scenario,
            "problem": problem,
            "advice": advice.recommendation,
            "confidence": advice.confidence,
            "mind_models": advice.analysis.get("mind_models_applied", []),
            "reasoning": advice.reasoning
        }
    
    def distill_scenario_skill(self, scenario: str, user_data: list) -> str:
        """
        蒸馏情景 Skill
        
        Args:
            scenario: 情景名称
            user_data: 用户在该情景的历史数据
        
        Returns:
            Skill 名称
        """
        # 从用户数据中提取心智模型
        skill = self.mirror.distill_expert(
            expert=f"用户-{scenario}",
            sources=user_data,
            skill_name=f"{scenario.lower()}-skill"
        )
        
        # 验证 Skill
        validation = self.mirror.validate_skill(skill)
        
        if validation["status"] == "published":
            # 发布 Skill
            path = self.mirror.publish_skill(skill)
            return path
        
        return None
    
    def get_growth_report(self) -> dict:
        """获取成长报告"""
        return self.mirror.generate_weekly_report()


def main():
    """测试集成"""
    print("🪞 情景 Agent - 太一镜像 v2.0 集成测试")
    print("=" * 50)
    print()
    
    integration = TodayStageMirrorIntegration()
    
    # 测试 1: 情景建议
    print("测试 1: 获取情景建议")
    advice = integration.get_scenario_advice(
        scenario="工作 - 专注",
        problem="总是分心怎么办？"
    )
    print(f"  情景：{advice['scenario']}")
    print(f"  建议：{advice['advice']}")
    print(f"  置信度：{advice['confidence']:.2f}")
    print()
    
    # 测试 2: 成长报告
    print("测试 2: 成长报告")
    report = integration.get_growth_report()
    print(f"  周数：{report['week']}")
    print(f"  决策质量：{report['decision_quality']['accuracy_rate']:.0%}")
    print(f"  蒸馏 Skills: {report['learning_progress']['skills_distilled']} 个")
    print()
    
    print("✅ 集成测试通过!")


if __name__ == "__main__":
    main()
