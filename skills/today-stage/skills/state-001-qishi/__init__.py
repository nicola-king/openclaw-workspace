#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情景状态 Skill 001 - 起势期
6 个阶段 × 心理学框架 × 行动建议
"""

import json
import os
from typing import Dict, List

class QishiStateSkill:
    """起势期情景状态 Skill"""
    
    def __init__(self):
        self.state_id = 1
        self.state_name = "起势期"
        self.core_insight = "潜力大于结果"
        
        # 加载 6 个阶段
        self.stages = self.load_stages()
        
        # 心理学框架
        self.psychology = {
            'adler': '价值感驱动你在积累期继续努力',
            'jung': '潜意识在为爆发做准备',
            'freud': '延迟满足的防御机制'
        }
        
        # 爆点句
        self.viral_headlines = [
            "我最近真的很努力，但就是没结果",
            "原来问题从来不是'我不够努力'",
            "潜力很大，但结果还没跟上"
        ]
    
    def load_stages(self) -> List[Dict]:
        """加载 6 个阶段数据"""
        return [
            {'stage': 1, 'name': '初始阶段', 'desc': '刚开始不对劲'},
            {'stage': 2, 'name': '发展阶段', 'desc': '逐渐察觉问题'},
            {'stage': 3, 'name': '强化阶段', 'desc': '开始怀疑路径'},
            {'stage': 4, 'name': '转化阶段', 'desc': '尝试调整方式'},
            {'stage': 5, 'name': '整合阶段', 'desc': '逐步适应'},
            {'stage': 6, 'name': '完成阶段', 'desc': '进入新状态'}
        ]
    
    def get_interpretation(self, current_stage: int) -> Dict:
        """生成情景状态解读"""
        stage_data = self.stages[current_stage - 1]
        
        return {
            'state_name': self.state_name,
            'current_stage': stage_data,
            'core_insight': self.core_insight,
            'psychology': self.psychology,
            'action_advice': self.get_action_advice(current_stage),
            'viral_headline': self.viral_headlines[0]
        }
    
    def get_action_advice(self, current_stage: int) -> Dict:
        """生成行动建议"""
        advice_map = {
            1: {'stop': '停止急于表现', 'look': '看清积累方向', 'change': '专注单点突破'},
            2: {'stop': '停止焦虑比较', 'look': '看清进步轨迹', 'change': '记录小成就'},
            3: {'stop': '停止自我怀疑', 'look': '看清积累价值', 'change': '调整评估标准'},
            4: {'stop': '停止盲目努力', 'look': '看清突破方向', 'change': '优化努力方式'},
            5: {'stop': '停止急躁', 'look': '看清适应进度', 'change': '保持节奏'},
            6: {'stop': '停止回顾过去', 'look': '看清新状态机会', 'change': '持续深耕'}
        }
        return advice_map.get(current_stage, {})


def main():
    """测试"""
    skill = QishiStateSkill()
    result = skill.get_interpretation(current_stage=3)
    
    print(f"情景状态：{result['state_name']}")
    print(f"当前阶段：{result['current_stage']['name']}")
    print(f"核心洞察：{result['core_insight']}")
    print(f"爆点句：{result['viral_headline']}")
    print(f"行动建议：{result['action_advice']}")


if __name__ == '__main__':
    main()
