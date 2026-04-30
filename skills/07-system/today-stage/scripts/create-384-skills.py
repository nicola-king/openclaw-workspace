#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建 384 个状态 Skills 脚本
64 个情景状态 × 6 个阶段 = 384 个独立 Skill 文件
"""

import os
import json

# 64 个情景状态数据
STATES_DATA = {
    1: {"name": "起势期", "pinyin": "qishi", "insight": "潜力大于结果"},
    2: {"name": "承载期", "pinyin": "chengzai", "insight": "责任增加主动权低"},
    3: {"name": "启动混乱期", "pinyin": "hunduan", "insight": "刚开始不顺"},
    4: {"name": "认知盲区期", "pinyin": "mangqu", "insight": "理解有偏差"},
    5: {"name": "等待窗口期", "pinyin": "dengdai", "insight": "准备好未启动"},
    6: {"name": "冲突边缘期", "pinyin": "chongtu", "insight": "即将产生对抗"},
    7: {"name": "结构协同期", "pinyin": "xietong", "insight": "需要协作"},
    8: {"name": "资源整合期", "pinyin": "zhenghe", "insight": "寻找合作"},
    9: {"name": "小幅增长期", "pinyin": "zengzhang", "insight": "进步缓慢"},
    10: {"name": "规则适应期", "pinyin": "guze", "insight": "环境有要求"},
}

# 6 个阶段数据
STAGES_DATA = [
    {"id": 1, "name": "初始阶段", "desc": "刚开始"},
    {"id": 2, "name": "发展阶段", "desc": "发展中"},
    {"id": 3, "name": "强化阶段", "desc": "强化中"},
    {"id": 4, "name": "转化阶段", "desc": "转化中"},
    {"id": 5, "name": "整合阶段", "desc": "整合中"},
    {"id": 6, "name": "完成阶段", "desc": "完成中"},
]

def create_stage_skill(state_id, state_info, stage_id, stage_info):
    """创建单个阶段 Skill 文件"""
    
    state_name = state_info["name"]
    pinyin = state_info["pinyin"]
    stage_name = stage_info["name"]
    
    # 目录名
    dir_name = f"state-{state_id:03d}-{pinyin}"
    base_path = f"/home/nicola/.openclaw/workspace/skills/today-stage/skills/{dir_name}"
    os.makedirs(base_path, exist_ok=True)
    
    # 阶段文件名
    file_name = f"stage-{stage_id:02d}.py"
    file_path = f"{base_path}/{file_name}"
    
    # 生成 Skill 内容
    content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情景状态 Skill {state_id:03d}-{stage_id:02d}
状态：{state_name} - 阶段{stage_id}: {stage_name}
"""

class State{state_id:03d}Stage{stage_id:02d}Skill:
    """{state_name} - {stage_name} Skill"""
    
    def __init__(self):
        self.state_id = {state_id}
        self.state_name = "{state_name}"
        self.stage_id = {stage_id}
        self.stage_name = "{stage_name}"
        self.core_insight = "{state_info['insight']}"
    
    def get_interpretation(self) -> dict:
        """获取解读"""
        return {{
            'state': self.state_name,
            'stage': self.stage_name,
            'insight': self.core_insight,
            'description': '这是{state_name}的{stage_name}，需要特别关注当前状态的特点。'
        }}


def main():
    skill = State{state_id:03d}Stage{stage_id:02d}Skill()
    result = skill.get_interpretation()
    print(f"状态：{{result['state']}}")
    print(f"阶段：{{result['stage']}}")
    print(f"洞察：{{result['insight']}}")


if __name__ == '__main__':
    main()
'''
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return file_path


def main():
    """主函数"""
    print("开始创建 384 个状态 Skills...")
    
    created = 0
    
    # 创建前 10 个状态的 6 个阶段 (示例)
    for state_id in range(1, 11):
        state_info = STATES_DATA.get(state_id, {"name": f"状态{state_id}", "pinyin": f"state{state_id}"})
        
        for stage_id in range(1, 7):
            stage_info = STAGES_DATA[stage_id - 1]
            file_path = create_stage_skill(state_id, state_info, stage_id, stage_info)
            created += 1
            print(f"✅ 创建：{file_path}")
    
    print(f"\n✅ 完成！创建 {created} 个阶段 Skills")
    print(f"总计：64 状态 × 6 阶段 = 384 个 Skills")
    print(f"本次创建：10 状态 × 6 阶段 = 60 个 Skills (示例)")


if __name__ == '__main__':
    main()
