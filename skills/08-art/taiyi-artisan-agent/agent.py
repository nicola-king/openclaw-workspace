#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiyi Artisan Agent - 太一艺术 Agent

智能自进化艺术管理系统
学习 → 吸收 → 进化 → 管理
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from skills.taiyi_artisan import Artisan, DesignTokens


class LearningEngine:
    """学习引擎"""
    
    def __init__(self):
        self.knowledge_base = {}
        self.learning_log = []
    
    def absorb(self, source: str, knowledge: Dict) -> Dict:
        """
        吸收新知识
        
        Args:
            source: 知识来源 (apple_design/google_material/...)
            knowledge: 知识内容
        
        Returns:
            吸收后的知识
        """
        absorbed = {
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'content': knowledge,
            'absorbed': True
        }
        
        self.knowledge_base[source] = absorbed
        self.learning_log.append(absorbed)
        
        return absorbed
    
    def get_progress(self) -> Dict:
        """获取学习进度"""
        return {
            'total_learned': len(self.knowledge_base),
            'recent_sources': list(self.knowledge_base.keys())[-5:],
            'last_learning': self.learning_log[-1]['timestamp'] if self.learning_log else None
        }


class SkillManager:
    """Skill 管理器"""
    
    def __init__(self):
        self.managed_skills = ['taiyi-artisan']
    
    def count(self) -> int:
        """获取管理的 Skill 数量"""
        return len(self.managed_skills)
    
    def add_skill(self, skill_name: str):
        """添加管理的 Skill"""
        if skill_name not in self.managed_skills:
            self.managed_skills.append(skill_name)
    
    def get_skills(self) -> List[str]:
        """获取所有管理的 Skill"""
        return self.managed_skills.copy()


class ArtisanAgent:
    """太一艺术 Agent 主类"""
    
    def __init__(self, workspace: str = "~/.openclaw/workspace"):
        """
        初始化艺术 Agent
        
        Args:
            workspace: 工作目录
        """
        self.workspace = Path(workspace).expanduser()
        self.artisan = Artisan(workspace)
        self.learning = LearningEngine()
        self.evolution = self.artisan.evolution
        self.manager = SkillManager()
        
        # 状态跟踪
        self.today_output = {
            'wisdom_cards': 0,
            'charts': 0,
            'cards': 0,
            'reviews': 0
        }
    
    def generate_wisdom_card(self, category: Optional[str] = None) -> str:
        """
        生成智慧卡片
        
        Args:
            category: 分类（道家/佛家，默认随机）
        
        Returns:
            输出文件路径
        """
        path = self.artisan.generate_daily_wisdom(category)
        self.today_output['wisdom_cards'] += 1
        return path
    
    def create_chart(self, chart_type: str, **kwargs) -> str:
        """
        生成图表
        
        Args:
            chart_type: 图表类型
            **kwargs: 图表参数
        
        Returns:
            输出文件路径
        """
        path = self.artisan.create_chart(chart_type, **kwargs)
        self.today_output['charts'] += 1
        return path
    
    def create_info_card(self, title: str, points: List[str], **kwargs) -> str:
        """
        生成信息卡片
        
        Args:
            title: 标题
            points: 要点列表
            **kwargs: 其他参数
        
        Returns:
            输出文件路径
        """
        path = self.artisan.create_info_card(title, points, **kwargs)
        self.today_output['cards'] += 1
        return path
    
    def review_design(self, content: str, content_type: str = 'ui'):
        """
        设计审核
        
        Args:
            content: 待审核内容
            content_type: 内容类型
        
        Returns:
            审核结果
        """
        result = self.artisan.review_design(content, content_type)
        self.today_output['reviews'] += 1
        return result
    
    def learn(self, source: str, knowledge: Dict) -> Dict:
        """
        学习新知识
        
        Args:
            source: 知识来源
            knowledge: 知识内容
        
        Returns:
            吸收后的知识
        """
        absorbed = self.learning.absorb(source, knowledge)
        
        # 触发进化
        if absorbed:
            self.evolution.collect_feedback({
                'output_type': 'learning',
                'output_id': source,
                'reaction': 'positive',
                'details': f'吸收新知识：{source}'
            })
        
        return absorbed
    
    def get_design_tokens(self) -> DesignTokens:
        """获取设计令牌"""
        return self.artisan.get_design_tokens()
    
    def get_css_variables(self) -> str:
        """生成 CSS 变量"""
        return self.artisan.get_css_variables()
    
    def get_design_principles(self) -> Dict:
        """获取设计原则"""
        return self.artisan.get_design_principles()
    
    def get_status(self) -> Dict:
        """获取状态报告"""
        return {
            'managed_skills': self.manager.count(),
            'today_output': self.today_output,
            'learning_progress': self.learning.get_progress(),
            'evolution_state': self.evolution.get_evolution_report()
        }
    
    def get_daily_report(self) -> str:
        """生成日报"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        report = f"""【太一艺术 Agent · 日报】
日期：{today}

今日输出:
- 智慧卡片：{self.today_output['wisdom_cards']} 张
- 图表生成：{self.today_output['charts']} 次
- 信息卡片：{self.today_output['cards']} 张
- 设计审核：{self.today_output['reviews']} 次

学习进度:
- 已吸收：{self.learning.get_progress()['total_learned']} 项
- 最近学习：{', '.join(self.learning.get_progress()['recent_sources']) or '无'}

进化状态:
- L5 进度：{self.evolution.get_evolution_report()['l5_progress']:.1f}%
- 反馈总数：{self.evolution.get_evolution_report()['total_feedbacks']}

明日计划:
- [ ] 收集用户反馈
- [ ] 学习最新设计趋势
- [ ] 更新设计令牌
"""
        return report
    
    def get_weekly_report(self) -> str:
        """生成周报"""
        week = datetime.now().isocalendar()[1]
        year = datetime.now().year
        
        report = f"""【太一艺术 Agent · 周报】
周次：{year}-W{week}

本周学习:
- 新吸收知识：{self.learning.get_progress()['total_learned']} 项
- 设计趋势：待统计
- 用户反馈：待收集

进化成果:
- 设计令牌更新：待统计
- 风格参数调整：待统计
- 新范式探索：待统计

下周计划:
- [ ] 完成 Google Material 模板
- [ ] 启动跨领域学习
- [ ] 建立设计预测模型
"""
        return report


# 快捷函数
def create_agent(workspace: str = "~/.openclaw/workspace") -> ArtisanAgent:
    """创建艺术 Agent 实例"""
    return ArtisanAgent(workspace)


def generate_wisdom(category: str = None):
    """快速生成智慧卡片"""
    agent = create_agent()
    return agent.generate_wisdom_card(category)


def review_design(content: str, type: str = 'ui'):
    """快速设计审核"""
    agent = create_agent()
    return agent.review_design(content, type)


# CLI 入口
if __name__ == '__main__':
    agent = create_agent()
    
    # 测试生成智慧卡片
    print("🎨 太一艺术 Agent 已启动")
    print(f"管理 Skill 数：{agent.manager.count()}")
    print(f"状态：{agent.get_status()}")
    
    # 生成日报
    print("\n" + agent.get_daily_report())
