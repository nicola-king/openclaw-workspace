#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情景状态 Skill 001-02
状态：起势期 - 阶段 2: 发展阶段
"""

class State001Stage02Skill:
    """起势期 - 发展阶段 Skill"""
    
    def __init__(self):
        self.state_id = 1
        self.state_name = "起势期"
        self.stage_id = 2
        self.stage_name = "发展阶段"
        self.core_insight = "潜力大于结果"
        self.description = "逐渐察觉问题"
        
        # 心理学框架
        self.psychology = {
            'adler': '价值感驱动你继续投入',
            'jung': '开始意识到路径问题',
            'freud': '焦虑作为防御信号'
        }
        
        # 爆点句
        self.viral_headlines = [
            "努力了一段时间，还是没看到结果",
            "开始怀疑是不是方向有问题",
            "明明在进步，但还是很焦虑"
        ]
    
    def get_interpretation(self) -> dict:
        """获取完整解读"""
        return {
            'state': self.state_name,
            'stage': self.stage_name,
            'insight': self.core_insight,
            'description': self.description,
            'psychology': self.psychology,
            'viral_headline': self.viral_headlines[0],
            'action_advice': {
                'stop': '停止焦虑比较',
                'look': '看清进步轨迹',
                'change': '记录小成就'
            }
        }


def main():
    skill = State001Stage02Skill()
    result = skill.get_interpretation()
    print(f"状态：{result['state']}")
    print(f"阶段：{result['stage']}")
    print(f"洞察：{result['insight']}")


if __name__ == '__main__':
    main()
