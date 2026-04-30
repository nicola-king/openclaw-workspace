#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反脆弱人生设计工具
参考：范式转换文章 - 新秩序生存法则
用途：评估个人反脆弱性，设计多元收入/可迁移技能/低固定成本
"""

from datetime import datetime
from typing import Dict, List

class AntifragileLifeDesign:
    """反脆弱人生设计"""
    
    def __init__(self):
        # 多元收入评估
        self.income_streams = []
        
        # 可迁移技能评估
        self.transferable_skills = {
            'computational_thinking': {'name': '计算思维', 'level': 0, 'max': 10},
            'communication': {'name': '沟通能力', 'level': 0, 'max': 10},
            'learning_agility': {'name': '学习敏捷性', 'level': 0, 'max': 10},
            'problem_solving': {'name': '问题解决', 'level': 0, 'max': 10},
            'ai_workflow': {'name': 'AI 工作流', 'level': 0, 'max': 10},
        }
        
        # 固定成本评估
        self.fixed_costs = {
            'housing': 0,  # 房贷/房租
            'transportation': 0,
            'subscriptions': 0,
            'other': 0,
        }
        
        # 连接网络评估
        self.network_connections = 0
        self.active_projects = 0
    
    def add_income_stream(self, name: str, monthly_income: float, stability: str):
        """添加收入来源"""
        self.income_streams.append({
            'name': name,
            'monthly_income': monthly_income,
            'stability': stability,  # 'stable', 'variable', 'experimental'
        })
    
    def assess_antifragility(self) -> Dict:
        """评估反脆弱性"""
        # 收入多元化评分
        income_score = min(len(self.income_streams) * 20, 100)
        
        # 技能可迁移性评分
        skill_total = sum(s['level'] for s in self.transferable_skills.values())
        skill_max = sum(s['max'] for s in self.transferable_skills.values())
        skill_score = skill_total / skill_max * 100
        
        # 固定成本评分（越低越好）
        total_fixed = sum(self.fixed_costs.values())
        if total_fixed < 5000:
            cost_score = 100
        elif total_fixed < 10000:
            cost_score = 80
        elif total_fixed < 20000:
            cost_score = 60
        else:
            cost_score = 40
        
        # 网络连接评分
        network_score = min(self.network_connections * 5 + self.active_projects * 10, 100)
        
        # 综合反脆弱性
        total_score = (income_score + skill_score + cost_score + network_score) / 4
        
        return {
            'income_diversification': income_score,
            'skill_transferability': skill_score,
            'fixed_cost_efficiency': cost_score,
            'network_connectivity': network_score,
            'total_antifragility': total_score,
            'level': self._get_level(total_score),
        }
    
    def _get_level(self, score: float) -> str:
        if score >= 80:
            return "🟢 反脆弱 (Antifragile)"
        elif score >= 60:
            return "🟡 坚韧 (Resilient)"
        else:
            return "🔴 脆弱 (Fragile)"
    
    def render_report(self) -> str:
        """生成反脆弱人生报告"""
        assessment = self.assess_antifragility()
        
        lines = []
        lines.append("=" * 60)
        lines.append("  反脆弱人生设计评估")
        lines.append("  新秩序生存工具")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append("【多元收入】")
        if self.income_streams:
            for stream in self.income_streams:
                lines.append(f"  - {stream['name']}: ¥{stream['monthly_income']}/月 ({stream['stability']})")
        else:
            lines.append("  🟡 暂无收入来源")
        lines.append(f"  评分：{assessment['income_diversification']}/100")
        lines.append("")
        
        lines.append("【可迁移技能】")
        for skill_id, skill in self.transferable_skills.items():
            lines.append(f"  - {skill['name']}: {skill['level']}/{skill['max']}")
        lines.append(f"  评分：{assessment['skill_transferability']:.0f}/100")
        lines.append("")
        
        lines.append("【固定成本】")
        lines.append(f"  - 房贷/房租：¥{self.fixed_costs['housing']}/月")
        lines.append(f"  - 交通：¥{self.fixed_costs['transportation']}/月")
        lines.append(f"  - 订阅：¥{self.fixed_costs['subscriptions']}/月")
        lines.append(f"  - 其他：¥{self.fixed_costs['other']}/月")
        lines.append(f"  总计：¥{sum(self.fixed_costs.values())}/月")
        lines.append(f"  评分：{assessment['fixed_cost_efficiency']}/100")
        lines.append("")
        
        lines.append("【连接网络】")
        lines.append(f"  - 网络节点：{self.network_connections}个")
        lines.append(f"  - 活跃项目：{self.active_projects}个")
        lines.append(f"  评分：{assessment['network_connectivity']}/100")
        lines.append("")
        
        lines.append("=" * 60)
        lines.append(f"【综合反脆弱性】")
        lines.append(f"  总分：{assessment['total_antifragility']:.1f}/100")
        lines.append(f"  等级：{assessment['level']}")
        lines.append("=" * 60)
        
        # 改进建议
        lines.append("")
        lines.append("【改进建议】")
        if assessment['income_diversification'] < 60:
            lines.append("  💡 增加收入来源（副业/产品/内容）")
        if assessment['skill_transferability'] < 60:
            lines.append("  💡 提升可迁移技能（AI 工作流/沟通/学习）")
        if assessment['fixed_cost_efficiency'] < 60:
            lines.append("  💡 降低固定成本（轻装上阵，保留选择权）")
        if assessment['network_connectivity'] < 60:
            lines.append("  💡 建立更多连接（项目/社区/同行者）")
        
        lines.append("")
        return "\n".join(lines)


# 测试 - 太一原型
if __name__ == "__main__":
    life = AntifragileLifeDesign()
    
    # 模拟太一收入来源
    life.add_income_stream('Skills 变现', 5000, 'variable')
    life.add_income_stream('CAD 服务', 3000, 'experimental')
    life.add_income_stream('Polymarket', 2000, 'variable')
    life.add_income_stream('内容创作', 1000, 'experimental')
    
    # 可迁移技能
    life.transferable_skills['computational_thinking']['level'] = 9
    life.transferable_skills['communication']['level'] = 8
    life.transferable_skills['learning_agility']['level'] = 10
    life.transferable_skills['problem_solving']['level'] = 9
    life.transferable_skills['ai_workflow']['level'] = 10
    
    # 固定成本（假设）
    life.fixed_costs = {
        'housing': 0,  # 无房贷
        'transportation': 500,
        'subscriptions': 200,
        'other': 1000,
    }
    
    # 网络连接
    life.network_connections = 6  # 6 Bot
    life.active_projects = 5  # 多个项目
    
    print(life.render_report())
