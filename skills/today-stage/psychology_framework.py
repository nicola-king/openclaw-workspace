#!/usr/bin/env python3
"""
情景 Agent - 心理学框架集成

作者：太一 AGI
创建：2026-04-09
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class PsychologyIntervention:
    """心理学干预方案"""
    name: str
    framework: str  # CBT/正念/习惯养成
    steps: List[str]
    expected_outcome: str


class PsychologyFramework:
    """心理学框架集成"""
    
    def __init__(self):
        self.frameworks = {
            "CBT": self._load_cbt(),
            "Mindfulness": self._load_mindfulness(),
            "HabitFormation": self._load_habit_formation()
        }
    
    def _load_cbt(self) -> Dict:
        """加载认知行为疗法框架"""
        return {
            "name": "认知行为疗法 (CBT)",
            "principles": [
                "想法影响情绪和行为",
                "识别自动思维",
                "挑战认知扭曲",
                "建立适应性思维"
            ],
            "techniques": [
                "思维记录",
                "认知重构",
                "行为实验",
                "渐进式暴露"
            ],
            "interventions": {
                "焦虑": PsychologyIntervention(
                    name="焦虑缓解",
                    framework="CBT",
                    steps=[
                        "1. 识别焦虑触发点",
                        "2. 记录自动思维",
                        "3. 挑战灾难化思维",
                        "4. 制定应对计划"
                    ],
                    expected_outcome="焦虑水平降低 50%"
                ),
                "拖延": PsychologyIntervention(
                    name="拖延克服",
                    framework="CBT",
                    steps=[
                        "1. 识别拖延原因",
                        "2. 分解任务",
                        "3. 设定小目标",
                        "4. 奖励完成"
                    ],
                    expected_outcome="任务完成率提升 80%"
                )
            }
        }
    
    def _load_mindfulness(self) -> Dict:
        """加载正念冥想框架"""
        return {
            "name": "正念冥想",
            "principles": [
                "觉察当下",
                "不加评判",
                "接纳现实",
                "专注呼吸"
            ],
            "techniques": [
                "呼吸冥想",
                "身体扫描",
                "正念行走",
                "正念饮食"
            ],
            "interventions": {
                "压力": PsychologyIntervention(
                    name="压力缓解",
                    framework="Mindfulness",
                    steps=[
                        "1. 找到安静空间",
                        "2. 专注呼吸 10 分钟",
                        "3. 身体扫描放松",
                        "4. 接纳当下状态"
                    ],
                    expected_outcome="压力水平降低 60%"
                ),
                "分心": PsychologyIntervention(
                    name="专注力提升",
                    framework="Mindfulness",
                    steps=[
                        "1. 设定专注目标",
                        "2. 觉察分心念头",
                        "3. 温和拉回注意力",
                        "4. 渐进延长专注时间"
                    ],
                    expected_outcome="专注时长提升 100%"
                )
            }
        }
    
    def _load_habit_formation(self) -> Dict:
        """加载习惯养成框架"""
        return {
            "name": "习惯养成理论",
            "principles": [
                "提示→渴望→反应→奖励",
                "让提示显而易见",
                "让习惯有吸引力",
                "让行动简便易行",
                "让奖励令人满足"
            ],
            "techniques": [
                "习惯叠加",
                "环境设计",
                "两分钟规则",
                "追踪打卡"
            ],
            "interventions": {
                "早起": PsychologyIntervention(
                    name="早起习惯",
                    framework="HabitFormation",
                    steps=[
                        "1. 设定固定起床时间",
                        "2. 前一晚准备好",
                        "3. 起床后立即行动",
                        "4. 奖励自己"
                    ],
                    expected_outcome="21 天形成习惯"
                ),
                "运动": PsychologyIntervention(
                    name="运动习惯",
                    framework="HabitFormation",
                    steps=[
                        "1. 从 2 分钟开始",
                        "2. 固定时间地点",
                        "3. 准备运动装备",
                        "4. 记录完成情况"
                    ],
                    expected_outcome="66 天形成习惯"
                )
            }
        }
    
    def get_intervention(self, problem: str) -> PsychologyIntervention:
        """
        获取干预方案
        
        Args:
            problem: 问题描述
        
        Returns:
            PsychologyIntervention
        """
        problem = problem.lower()
        
        # 匹配问题
        if "焦虑" in problem or "紧张" in problem:
            return self.frameworks["CBT"]["interventions"]["焦虑"]
        elif "拖延" in problem:
            return self.frameworks["CBT"]["interventions"]["拖延"]
        elif "压力" in problem or "累" in problem:
            return self.frameworks["Mindfulness"]["interventions"]["压力"]
        elif "分心" in problem or "专注" in problem:
            return self.frameworks["Mindfulness"]["interventions"]["分心"]
        elif "早起" in problem:
            return self.frameworks["HabitFormation"]["interventions"]["早起"]
        elif "运动" in problem or "健身" in problem:
            return self.frameworks["HabitFormation"]["interventions"]["运动"]
        else:
            # 默认返回 CBT 焦虑干预
            return self.frameworks["CBT"]["interventions"]["焦虑"]
    
    def recommend_framework(self, scenario: str) -> str:
        """
        推荐心理学框架
        
        Args:
            scenario: 情景名称
        
        Returns:
            推荐框架名称
        """
        # 根据情景推荐框架
        if "工作" in scenario or "学习" in scenario:
            return "CBT"
        elif "休息" in scenario or "睡眠" in scenario:
            return "Mindfulness"
        elif "晨" in scenario or "习惯" in scenario:
            return "HabitFormation"
        else:
            return "CBT"  # 默认


def main():
    """测试心理学框架"""
    print("🧠 情景 Agent - 心理学框架测试")
    print("=" * 50)
    print()
    
    framework = PsychologyFramework()
    
    # 测试 1: 获取干预方案
    print("测试 1: 获取干预方案")
    intervention = framework.get_intervention("工作时分心怎么办？")
    print(f"  方案：{intervention.name}")
    print(f"  框架：{intervention.framework}")
    print(f"  步骤:")
    for step in intervention.steps:
        print(f"    {step}")
    print(f"  预期效果：{intervention.expected_outcome}")
    print()
    
    # 测试 2: 推荐框架
    print("测试 2: 推荐心理学框架")
    scenarios = ["工作 - 专注", "晚间 - 睡眠", "晨间 - 早起"]
    for scenario in scenarios:
        rec = framework.recommend_framework(scenario)
        print(f"  {scenario} → {rec}")
    
    print()
    print("✅ 心理学框架测试通过!")


if __name__ == "__main__":
    main()
