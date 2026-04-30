#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涌现社区建设工具
参考：范式转换文章 - 新社区与涌现智慧
用途：评估/设计基于价值观 + 成长的新社区
"""

from datetime import datetime
from typing import Dict, List

class EmergentCommunity:
    """涌现社区"""
    
    def __init__(self, name: str = "新秩序建设者"):
        self.name = name
        self.members = []
        self.values = []
        self.projects = []
    
    def add_member(self, name: str, background: str, seeking: str, offering: str):
        """
        添加成员
        :param name: 姓名
        :param background: 背景
        :param seeking: 需要什么帮助
        :param offering: 能提供什么
        """
        self.members.append({
            'name': name,
            'background': background,
            'seeking': seeking,
            'offering': offering,
            'joined_at': datetime.now().isoformat(),
        })
    
    def add_value(self, value: str):
        """添加核心价值观"""
        self.values.append(value)
    
    def add_project(self, name: str, description: str, collaborators: List[str]):
        """添加协作项目"""
        self.projects.append({
            'name': name,
            'description': description,
            'collaborators': collaborators,
            'status': 'active',
        })
    
    def assess_diversity(self) -> Dict:
        """评估社区多样性（混沌边缘）"""
        backgrounds = [m['background'] for m in self.members]
        unique_backgrounds = len(set(backgrounds))
        
        # 多样性评分
        if len(self.members) == 0:
            diversity_score = 0
        else:
            diversity_score = min(unique_backgrounds / len(self.members) * 100, 100)
        
        # 共识评分（共同价值观）
        consensus_score = min(len(self.values) * 20, 100)
        
        # 混沌边缘评分（多样性 + 共识）
        edge_of_chaos = (diversity_score + consensus_score) / 2
        
        return {
            'diversity': diversity_score,
            'consensus': consensus_score,
            'edge_of_chaos': edge_of_chaos,
            'level': self._get_level(edge_of_chaos),
        }
    
    def _get_level(self, score: float) -> str:
        if score >= 80:
            return "🟢 混沌边缘 (最强创新)"
        elif score >= 60:
            return "🟡 有序 (需增加多样性)"
        else:
            return "🔴 混乱 (需建立共识)"
    
    def render_report(self) -> str:
        """生成社区报告"""
        assessment = self.assess_diversity()
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"  {self.name} - 涌现社区评估")
        lines.append("  新秩序社区建设工具")
        lines.append("=" * 60)
        lines.append("")
        
        lines.append("【核心价值观】")
        if self.values:
            for i, value in enumerate(self.values, 1):
                lines.append(f"  {i}. {value}")
        else:
            lines.append("  🟡 暂无价值观（需定义）")
        lines.append("")
        
        lines.append("【成员多样性】")
        if self.members:
            for member in self.members:
                lines.append(f"  - {member['name']} ({member['background']})")
                lines.append(f"    需要：{member['seeking']}")
                lines.append(f"    提供：{member['offering']}")
        else:
            lines.append("  🟡 暂无成员")
        lines.append("")
        
        lines.append("【协作项目】")
        if self.projects:
            for project in self.projects:
                lines.append(f"  - {project['name']}: {project['description']}")
                lines.append(f"    协作：{', '.join(project['collaborators'])}")
        else:
            lines.append("  🟡 暂无项目")
        lines.append("")
        
        lines.append("【混沌边缘评估】")
        lines.append(f"  多样性：{assessment['diversity']:.0f}/100")
        lines.append(f"  共识：{assessment['consensus']:.0f}/100")
        lines.append(f"  混沌边缘：{assessment['edge_of_chaos']:.0f}/100")
        lines.append(f"  等级：{assessment['level']}")
        lines.append("")
        
        lines.append("【改进建议】")
        if assessment['diversity'] < 60:
            lines.append("  💡 增加背景多样性（不同领域/年龄/文化）")
        if assessment['consensus'] < 60:
            lines.append("  💡 建立共同价值观（成长/探索/分享）")
        if not self.projects:
            lines.append("  💡 启动协作项目（在实践中进化）")
        
        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


# 测试 - 太一社区原型
if __name__ == "__main__":
    community = EmergentCommunity("太一新秩序社区")
    
    # 核心价值观
    community.add_value("成长优先于稳定")
    community.add_value("行动优先于空想")
    community.add_value("分享优先于占有")
    community.add_value("连接优先于孤立")
    community.add_value("反脆弱优先于确定性")
    
    # 成员（模拟 6 Bot + 人类）
    community.add_member('太一', 'AGI 总管', '更多变现路径', '6 Bot 协作网络')
    community.add_member('知几', '量化交易', '市场数据', '交易策略')
    community.add_member('山木', '内容创意', '分发渠道', '视频/图文工作流')
    community.add_member('素问', '技术开发', '项目需求', '代码/部署能力')
    community.add_member('罔两', '数据/CEO', '分析场景', '市场监控')
    community.add_member('庖丁', '预算成本', '财务场景', '成本控制')
    community.add_member('SAYELF', '市政建设', 'AI 落地', '战略方向')
    
    # 协作项目
    community.add_project('知几-E', 'Polymarket 量化交易', ['太一', '知几', '素问'])
    community.add_project('技能市场', 'Skills 变现平台', ['太一', '山木', '罔两'])
    community.add_project('CAD 服务', '跨境图纸处理', ['太一', '素问', '庖丁'])
    
    print(community.render_report())
