#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建 384 个阶段 Skills
64 个情景状态 × 6 个阶段 = 384 个独立 Skill 文件
"""

import os
import json

# 64 个情景状态完整数据
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
    11: {"name": "通畅期", "pinyin": "tongchang", "insight": "流程顺畅"},
    12: {"name": "停滞期", "pinyin": "zhiting", "insight": "进展受阻"},
    13: {"name": "关系深化期", "pinyin": "guanxi", "insight": "关系加强"},
    14: {"name": "资源高位期", "pinyin": "ziyuan", "insight": "资源较多"},
    15: {"name": "收敛期", "pinyin": "shoulian", "insight": "需要收敛"},
    16: {"name": "蓄势期", "pinyin": "xushi", "insight": "准备阶段"},
    17: {"name": "跟随期", "pinyin": "gensui", "insight": "参考他人路径"},
    18: {"name": "修正期", "pinyin": "xiuzheng", "insight": "出现问题"},
    19: {"name": "接近期", "pinyin": "jiejin", "insight": "接近机会"},
    20: {"name": "观察期", "pinyin": "guancha", "insight": "需要观察"},
    21: {"name": "突破期", "pinyin": "tupo", "insight": "需要果断行动"},
    22: {"name": "表象期", "pinyin": "biaoxiang", "insight": "注重呈现"},
    23: {"name": "剥离期", "pinyin": "boli", "insight": "资源流失"},
    24: {"name": "回归期", "pinyin": "hui gui", "insight": "重新开始"},
    25: {"name": "自然推进期", "pinyin": "ziran", "insight": "自然发展"},
    26: {"name": "能量储备期", "pinyin": "nengliang", "insight": "力量积累"},
    27: {"name": "输入调整期", "pinyin": "shuru", "insight": "输入重要"},
    28: {"name": "压力过载期", "pinyin": "yali", "insight": "压力过大"},
    29: {"name": "反复风险期", "pinyin": "fanfu", "insight": "反复遇到问题"},
    30: {"name": "高曝光期", "pinyin": "gaobaoguang", "insight": "被关注"},
    31: {"name": "吸引期", "pinyin": "xiyin", "insight": "吸引他人"},
    32: {"name": "长期稳定期", "pinyin": "changqi", "insight": "稳定发展"},
    33: {"name": "主动退让期", "pinyin": "tui rang", "insight": "需要后退"},
    34: {"name": "力量释放期", "pinyin": "liliang", "insight": "能量充足"},
    35: {"name": "上升期", "pinyin": "shangsheng", "insight": "正在上升"},
    36: {"name": "隐匿期", "pinyin": "yinni", "insight": "需要低调"},
    37: {"name": "内部结构期", "pinyin": "neibu", "insight": "关注内部"},
    38: {"name": "分歧期", "pinyin": "fenqi", "insight": "意见不同"},
    39: {"name": "阻碍期", "pinyin": "zuai", "insight": "推进困难"},
    40: {"name": "释放期", "pinyin": "shi fang", "insight": "问题缓解"},
    41: {"name": "主动减负期", "pinyin": "jianfu", "insight": "需要减少"},
    42: {"name": "收益增长期", "pinyin": "shouyi", "insight": "收益提升"},
    43: {"name": "决断期", "pinyin": "jueduan", "insight": "必须做决定"},
    44: {"name": "突发干扰期", "pinyin": "ganrao", "insight": "出现干扰"},
    45: {"name": "聚集期", "pinyin": "juji", "insight": "资源集中"},
    46: {"name": "稳步上升期", "pinyin": "wenbu", "insight": "持续进步"},
    47: {"name": "受限期", "pinyin": "shouxian", "insight": "受限明显"},
    48: {"name": "资源基础期", "pinyin": "jichu", "insight": "资源稳定"},
    49: {"name": "变革期", "pinyin": "biange", "insight": "需要改变"},
    50: {"name": "结构成型期", "pinyin": "ji egou", "insight": "系统成熟"},
    51: {"name": "冲击期", "pinyin": "chongji", "insight": "突发冲击"},
    52: {"name": "暂停期", "pinyin": "zanting", "insight": "需要暂停"},
    53: {"name": "渐进期", "pinyin": "jianjin", "insight": "逐步推进"},
    54: {"name": "依附期", "pinyin": "yifu", "insight": "依赖他人"},
    55: {"name": "高峰期", "pinyin": "gaofeng", "insight": "达到高点"},
    56: {"name": "流动期", "pinyin": "liudong", "insight": "处于变化中"},
    57: {"name": "渗透期", "pinyin": "shentou", "insight": "逐步影响"},
    58: {"name": "互动期", "pinyin": "hudong", "insight": "互动频繁"},
    59: {"name": "分散期", "pinyin": "fensan", "insight": "结构分散"},
    60: {"name": "限制优化期", "pinyin": "xianzhi", "insight": "受规则限制"},
    61: {"name": "内在确认期", "pinyin": "neizai", "insight": "需要确认"},
    62: {"name": "细节处理期", "pinyin": "xijie", "insight": "细节重要"},
    63: {"name": "完成临界期", "pinyin": "wancheng", "insight": "接近完成"},
    64: {"name": "未完成期", "pinyin": "weiwancheng", "insight": "尚未完成"},
}

# 6 个阶段数据
STAGES_DATA = [
    {"id": 1, "name": "初始阶段", "desc": "刚开始", "stop": "停止急于求成", "look": "看清当前状态", "change": "调整心态"},
    {"id": 2, "name": "发展阶段", "desc": "发展中", "stop": "停止焦虑", "look": "看清进步轨迹", "change": "持续投入"},
    {"id": 3, "name": "强化阶段", "desc": "强化中", "stop": "停止自我怀疑", "look": "看清价值", "change": "调整策略"},
    {"id": 4, "name": "转化阶段", "desc": "转化中", "stop": "停止旧模式", "look": "看清新方向", "change": "尝试新方法"},
    {"id": 5, "name": "整合阶段", "desc": "整合中", "stop": "停止急躁", "look": "看清整合进度", "change": "保持节奏"},
    {"id": 6, "name": "完成阶段", "desc": "完成中", "stop": "停止回顾", "look": "看清新机会", "change": "持续深耕"},
]

# 爆点句库
VIRAL_HEADLINES = [
    "我最近真的很努力，但就是没结果",
    "突然意识到，我可能一开始就走错了",
    "我以为是我不够好，其实不是",
    "今天有点崩，但好像找到原因了",
    "我一直在努力，但越来越累",
    "有一瞬间突然觉得，不是我的问题",
    "我好像一直在用错误的方式努力",
    "最近状态很奇怪，说不上来哪里不对",
    "我突然不想再证明自己了",
    "原来问题从来不是'我不够努力'",
]

def create_stage_skill(state_id, state_info, stage_info):
    """创建单个阶段 Skill 文件"""
    
    state_name = state_info["name"]
    pinyin = state_info["pinyin"]
    stage_id = stage_info["id"]
    stage_name = stage_info["name"]
    stage_desc = stage_info["desc"]
    
    # 目录名
    dir_name = f"state-{state_id:03d}-{pinyin}"
    base_path = f"/home/nicola/.openclaw/workspace/skills/today-stage/skills/{dir_name}"
    os.makedirs(base_path, exist_ok=True)
    
    # 阶段文件名
    file_name = f"stage-{stage_id:02d}.py"
    file_path = f"{base_path}/{file_name}"
    
    # 心理学框架
    psychology = {
        'adler': f'价值感驱动你在{state_name}继续{stage_desc}',
        'jung': f'潜意识在{stage_desc}中影响你的选择',
        'freud': f'防御机制在维持当前{stage_desc}模式'
    }
    
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
        self.description = "{stage_desc}"
        
        # 心理学框架
        self.psychology = {{
            'adler': "{psychology['adler']}",
            'jung': "{psychology['jung']}",
            'freud': "{psychology['freud']}"
        }}
        
        # 爆点句
        self.viral_headlines = [
            "{VIRAL_HEADLINES[0]}",
            "{VIRAL_HEADLINES[1]}",
            "{VIRAL_HEADLINES[2]}"
        ]
    
    def get_interpretation(self) -> dict:
        """获取完整解读"""
        return {{
            'state': self.state_name,
            'stage': self.stage_name,
            'insight': self.core_insight,
            'description': self.description,
            'psychology': self.psychology,
            'viral_headline': self.viral_headlines[0],
            'action_advice': {{
                'stop': "{stage_info['stop']}",
                'look': "{stage_info['look']}",
                'change': "{stage_info['change']}"
            }}
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
    print("=" * 60)
    print("批量创建 384 个阶段 Skills")
    print("64 个情景状态 × 6 个阶段 = 384 个独立 Skill 文件")
    print("=" * 60)
    print()
    
    created = 0
    failed = 0
    
    # 创建所有 64 个状态的 6 个阶段
    for state_id in range(1, 65):
        state_info = STATES_DATA.get(state_id)
        if not state_info:
            print(f"❌ 状态{state_id}: 数据缺失")
            failed += 1
            continue
        
        for stage_info in STAGES_DATA:
            try:
                file_path = create_stage_skill(state_id, state_info, stage_info)
                created += 1
                if created % 50 == 1:
                    print(f"✅ 已创建 {created}/384 个 Skills")
            except Exception as e:
                print(f"❌ 创建失败 {state_id}-{stage_info['id']}: {e}")
                failed += 1
    
    print()
    print("=" * 60)
    print(f"✅ 完成！成功创建 {created}/384 个阶段 Skills")
    if failed > 0:
        print(f"❌ 失败 {failed} 个")
    print("=" * 60)


if __name__ == '__main__':
    main()
