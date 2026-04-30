#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日情景 Agent
原名：易经 Agent
功能：根据用户状态匹配 64 情景之一，生成解读报告
创建：2026-03-29 16:36
"""

import os
import sys
import json
from typing import Dict, List, Optional
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TodayStageAgent:
    """今日情景 Agent"""
    
    def __init__(self):
        self.stages = self.load_stages()
        self.psychology_framework = self.load_psychology()
        
    def load_stages(self) -> Dict:
        """加载 64 情景数据"""
        # 简化版：实际应从文件加载
        return {
            1: {
                'id': 1,
                'name': '积累未显期',
                'type': '调整型',
                'insight': '你最近的努力，暂时还看不到结果',
                'viral': '我最近真的很努力，但就是没结果'
            },
            2: {
                'id': 2,
                'name': '路径错配期',
                'type': '调整型',
                'insight': '你不是不够努力，只是方向一开始就不对',
                'viral': '突然意识到，我可能一开始就走错了'
            },
            3: {
                'id': 3,
                'name': '时机未到期',
                'type': '观察型',
                'insight': '准备已完成，只是环境还未匹配',
                'viral': '原来问题从来不是"我不够努力"'
            },
            6: {
                'id': 6,
                'name': '过载停滞期',
                'type': '过渡型',
                'insight': '精力下降，效率降低，意识需停',
                'viral': '我一直在努力，但越来越累'
            }
        }
    
    def load_psychology(self) -> Dict:
        """加载心理学框架"""
        return {
            'adler': '价值感驱动行为',
            'jung': '潜意识路径在影响选择',
            'freud': '防御机制在维持当前模式'
        }
    
    def match_stage(self, user_input: str) -> Dict:
        """
        匹配情景
        
        Args:
            user_input: 用户输入 (状态描述/测试答案)
        
        Returns:
            匹配结果
        """
        # 关键词匹配 (简化版)
        keyword_map = {
            '努力没结果': 1,
            '走错/方向错': 2,
            '时机/等待': 3,
            '累/疲惫': 6
        }
        
        for keyword, stage_id in keyword_map.items():
            if keyword in user_input:
                return self.stages.get(stage_id, self.stages[2])
        
        # 默认返回路径错配期 (最普适)
        return self.stages[2]
    
    def generate_report(self, stage: Dict, step: int = 3) -> Dict:
        """
        生成情景解读报告
        
        Args:
            stage: 情景数据
            step: 当前步骤 (1-6)
        
        Returns:
            完整报告
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'stage': {
                'id': stage['id'],
                'name': stage['name'],
                'type': stage['type'],
                'step': step,
                'step_name': self.get_step_name(step)
            },
            'core_insight': stage['insight'],
            'viral_headline': stage['viral'],
            'psychology': self.psychology_framework,
            'action_advice': {
                'stop': self.get_stop_advice(stage['id'], step),
                'look': self.get_look_advice(stage['id'], step),
                'change': self.get_change_advice(stage['id'], step)
            },
            'today_actions': self.get_today_actions(stage['id'], step),
            'encouragement': self.get_encouragement(stage['id'])
        }
    
    def get_step_name(self, step: int) -> str:
        """获取步骤名称"""
        step_names = {
            1: '刚开始不对劲',
            2: '逐渐察觉问题',
            3: '开始怀疑路径',
            4: '尝试调整方式',
            5: '逐步适应',
            6: '进入新状态'
        }
        return step_names.get(step, '未知')
    
    def get_stop_advice(self, stage_id: int, step: int) -> str:
        """停止建议"""
        return '停止加大无效投入'
    
    def get_look_advice(self, stage_id: int, step: int) -> str:
        """看清建议"""
        return '看清路径是否真正匹配'
    
    def get_change_advice(self, stage_id: int, step: int) -> str:
        """改变建议"""
        return '换一种努力方式或方向'
    
    def get_today_actions(self, stage_id: int, step: int) -> List[str]:
        """今日行动清单"""
        return [
            '写下 3 件今天做得好的事 (无论多小)',
            '和一个信任的人聊聊你的困惑',
            '给自己放个小假 (至少 30 分钟完全放松)',
            '问自己：如果放下"必须成功"，我会怎么做？'
        ]
    
    def get_encouragement(self, stage_id: int) -> str:
        """鼓励的话"""
        encouragements = {
            1: '你现在经历的不是失败，而是积累未显。继续浇水，继续等待，破土而出的时刻会到来。',
            2: '发现路径错配不是失败，是成长。及时调整，你比坚持错误的人更勇敢。',
            3: '等待不是被动，是主动选择。时机成熟时，你会感谢现在的耐心。',
            6: '累了就休息，不是放弃。休息是为了走更远的路。'
        }
        return encouragements.get(stage_id, '你正在经历一个结构与认知需要重新匹配的阶段。')


def main():
    """测试"""
    agent = TodayStageAgent()
    
    # 测试输入
    test_inputs = [
        '我最近真的很努力，但就是没结果',
        '突然意识到，我可能一开始就走错了',
        '我一直在努力，但越来越累'
    ]
    
    for user_input in test_inputs:
        print(f"\n{'='*60}")
        print(f"用户输入：{user_input}")
        print('='*60)
        
        stage = agent.match_stage(user_input)
        report = agent.generate_report(stage, step=3)
        
        print(f"\n📍 情景：{report['stage']['name']} (Step {report['stage']['step']})")
        print(f"🏷 类型：{report['stage']['type']}")
        print(f"\n💡 核心洞察：{report['core_insight']}")
        print(f"\n🔥 爆点句：{report['viral_headline']}")
        print(f"\n🧠 心理学解读:")
        print(f"  阿德勒：{report['psychology']['adler']}")
        print(f"  荣格：{report['psychology']['jung']}")
        print(f"  弗洛伊德：{report['psychology']['freud']}")
        print(f"\n💡 行动建议:")
        print(f"  停：{report['action_advice']['stop']}")
        print(f"  看：{report['action_advice']['look']}")
        print(f"  换：{report['action_advice']['change']}")
        print(f"\n🎯 今日行动:")
        for i, action in enumerate(report['today_actions'], 1):
            print(f"  {i}. {action}")
        print(f"\n🌟 {report['encouragement']}")


if __name__ == '__main__':
    main()
