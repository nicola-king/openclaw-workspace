#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新秩序技能包 - 范式转换后的核心能力
参考：范式转换文章
用途：个人 + AI 工作流能力评估
"""

from datetime import datetime
from typing import Dict, List

class NewOrderSkillset:
    """新秩序技能包"""
    
    def __init__(self):
        self.skills = {
            # 核心能力（密度优先）
            'ai_workflow': {'name': 'AI 工作流', 'level': 0, 'max': 10},
            'prompt_engineering': {'name': '提示工程', 'level': 0, 'max': 10},
            'system_design': {'name': '系统设计', 'level': 0, 'max': 10},
            'rapid_prototyping': {'name': '快速原型', 'level': 0, 'max': 10},
            
            # 根茎协作
            'multi_agent_coordination': {'name': '多 Agent 协作', 'level': 0, 'max': 10},
            'delegation': {'name': '任务委派', 'level': 0, 'max': 10},
            
            # 可验证成果
            'open_source': {'name': '开源贡献', 'level': 0, 'max': 10},
            'portfolio_building': {'name': '作品集建设', 'level': 0, 'max': 10},
            
            # 适应性
            'learning_agility': {'name': '学习敏捷性', 'level': 0, 'max': 10},
            'paradigm_shifting': {'name': '范式转换思维', 'level': 0, 'max': 10},
        }
    
    def assess(self) -> Dict:
        """评估当前技能水平"""
        total = sum(s['level'] for s in self.skills.values())
        max_total = sum(s['max'] for s in self.skills.values())
        
        return {
            'total_score': total,
            'max_score': max_total,
            'completion_rate': f"{total/max_total*100:.1f}%",
            'top_skills': sorted(self.skills.items(), key=lambda x: x[1]['level'], reverse=True)[:3],
            'weak_skills': sorted(self.skills.items(), key=lambda x: x[1]['level'])[:3],
        }
    
    def render_report(self) -> str:
        """生成技能报告"""
        assessment = self.assess()
        
        lines = []
        lines.append("=" * 60)
        lines.append("  新秩序技能包评估")
        lines.append("  范式转换后的核心能力")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append("【核心能力】（密度优先）")
        lines.append(f"  - AI 工作流：{self.skills['ai_workflow']['level']}/10")
        lines.append(f"  - 提示工程：{self.skills['prompt_engineering']['level']}/10")
        lines.append(f"  - 系统设计：{self.skills['system_design']['level']}/10")
        lines.append(f"  - 快速原型：{self.skills['rapid_prototyping']['level']}/10")
        lines.append("")
        
        lines.append("【根茎协作】")
        lines.append(f"  - 多 Agent 协作：{self.skills['multi_agent_coordination']['level']}/10")
        lines.append(f"  - 任务委派：{self.skills['delegation']['level']}/10")
        lines.append("")
        
        lines.append("【可验证成果】")
        lines.append(f"  - 开源贡献：{self.skills['open_source']['level']}/10")
        lines.append(f"  - 作品集建设：{self.skills['portfolio_building']['level']}/10")
        lines.append("")
        
        lines.append("【适应性】")
        lines.append(f"  - 学习敏捷性：{self.skills['learning_agility']['level']}/10")
        lines.append(f"  - 范式转换思维：{self.skills['paradigm_shifting']['level']}/10")
        lines.append("")
        
        lines.append("【评估结果】")
        lines.append(f"  总分：{assessment['total_score']}/{assessment['max_score']}")
        lines.append(f"  完成率：{assessment['completion_rate']}")
        lines.append("")
        
        lines.append("【优势技能】")
        for skill, data in assessment['top_skills']:
            lines.append(f"  ✅ {data['name']}: {data['level']}/10")
        lines.append("")
        
        lines.append("【待提升】")
        for skill, data in assessment['weak_skills']:
            lines.append(f"  🟡 {data['name']}: {data['level']}/10")
        lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    skillset = NewOrderSkillset()
    
    # 模拟太一当前水平
    skillset.skills['ai_workflow']['level'] = 9
    skillset.skills['prompt_engineering']['level'] = 8
    skillset.skills['system_design']['level'] = 9
    skillset.skills['rapid_prototyping']['level'] = 10  # 14 文件/4 分钟
    skillset.skills['multi_agent_coordination']['level'] = 9  # 6 Bot
    skillset.skills['delegation']['level'] = 9
    skillset.skills['open_source']['level'] = 8
    skillset.skills['portfolio_building']['level'] = 7
    skillset.skills['learning_agility']['level'] = 9
    skillset.skills['paradigm_shifting']['level'] = 10  # 范式转换验证
    
    print(skillset.render_report())
