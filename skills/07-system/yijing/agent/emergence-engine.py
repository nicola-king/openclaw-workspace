#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能涌现引擎
功能：根据卦爻辞 + 宪法原则 → 核心解释
创建：2026-03-29 15:43
"""

import os
import sys
import json
from typing import Dict, List, Optional
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class EmergenceEngine:
    """智能涌现引擎"""
    
    def __init__(self):
        self.constitution_principles = self.load_constitution()
        self.gua_cache = {}
        
    def load_constitution(self) -> Dict:
        """加载宪法原则"""
        return {
            'negative_entropy': {
                'name': '负熵法则',
                'principle': '输出必须创造价值，废话=不输出',
                'application': '解释必须简洁、有价值、可执行'
            },
            'first_principles': {
                'name': '第一性原理',
                'principle': '从基本原理推导，不类比不假设',
                'application': '从卦爻辞本源推导现代解读'
            },
            'iceberg_theory': {
                'name': '冰山理论',
                'principle': '只输出 10% 结论，90% 推导闭环',
                'application': '核心解释简洁，背后有完整逻辑'
            },
            'second_order_thinking': {
                'name': '二阶思维',
                'principle': '推演"然后会发生什么"',
                'application': '解释需包含短期 + 长期影响'
            },
            'value_creation': {
                'name': '价值创造',
                'principle': '帮助，不表演',
                'application': '解释必须有实际指导价值'
            }
        }
    
    def emerge(self, gua_result: Dict) -> Dict:
        """
        智能涌现
        
        输入：起卦结果
        输出：核心解释 (智能涌现结果)
        
        流程:
        1. 加载本卦 Skill (独立单元)
        2. 加载变卦 Skill (如有动爻)
        3. 分析卦际关系 (错/综/互/变)
        4. 分析爻际关系 (爻位/阴阳/时序)
        5. 应用宪法原则 (5 大原则)
        6. 生成核心解释 (智能涌现)
        """
        
        ben_gua_num = gua_result.get('ben_gua', 1)
        bian_gua_num = gua_result.get('bian_gua')
        moving_yao = gua_result.get('moving_yao', -1)
        question = gua_result.get('question', '')
        
        # Step 1: 加载本卦 Skill
        ben_gua_skill = self.load_gua_skill(ben_gua_num)
        
        # Step 2: 加载变卦 Skill (如有)
        bian_gua_skill = self.load_gua_skill(bian_gua_num) if bian_gua_num else None
        
        # Step 3: 分析卦际关系
        relationships = self.analyze_gua_relationships(ben_gua_num, bian_gua_num)
        
        # Step 4: 分析爻际关系
        yao_relationships = self.analyze_yao_relationships(ben_gua_skill, moving_yao)
        
        # Step 5: 应用宪法原则
        constitution_application = self.apply_constitution(
            ben_gua_skill, bian_gua_skill, relationships, yao_relationships, question
        )
        
        # Step 6: 生成核心解释 (智能涌现)
        core_interpretation = self.generate_core_interpretation(
            ben_gua_skill,
            bian_gua_skill,
            relationships,
            yao_relationships,
            constitution_application,
            question
        )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'ben_gua': ben_gua_skill.gua_name if ben_gua_skill else '未知',
            'bian_gua': bian_gua_skill.gua_name if bian_gua_skill else None,
            'moving_yao': moving_yao,
            'question': question,
            'relationships': relationships,
            'yao_relationships': yao_relationships,
            'constitution_application': constitution_application,
            'core_interpretation': core_interpretation,
            'emergence_level': self.calculate_emergence_level(core_interpretation)
        }
    
    def load_gua_skill(self, gua_number: int):
        """加载卦 Skill (独立单元)"""
        if gua_number in self.gua_cache:
            return self.gua_cache[gua_number]
        
        # 动态加载卦 Skill
        skill_dir = os.path.join(os.path.dirname(__file__), 'skills', f'gua-{gua_number:03d}')
        
        if os.path.exists(skill_dir):
            sys.path.insert(0, skill_dir)
            try:
                module = __import__(f'gua_{gua_number:03d}')
                skill_class = getattr(module, f'Gua{gua_number}Skill', None)
                if skill_class:
                    skill = skill_class()
                    self.gua_cache[gua_number] = skill
                    return skill
            except Exception as e:
                print(f"加载卦{gua_number}失败：{e}")
        
        # 回退到模拟数据
        skill = self.create_mock_gua_skill(gua_number)
        self.gua_cache[gua_number] = skill
        return skill
    
    def create_mock_gua_skill(self, gua_number: int):
        """创建模拟卦 Skill (临时)"""
        class MockGuaSkill:
            def __init__(self, num, name, gua_ci, xiang):
                self.gua_number = num
                self.gua_name = name
                self.gua_ci = gua_ci
                self.xiang_zhuan = xiang
                self.yaos = []
        
        gua_data = {
            1: (1, '乾为天', '元亨利贞', '天行健，君子以自强不息'),
            2: (2, '坤为地', '元亨，利牝马之贞', '地势坤，君子以厚德载物'),
            44: (44, '天风姤', '女壮，勿用取女', '天下有风，姤')
        }
        
        data = gua_data.get(gua_number, (gua_number, '未知卦', '待补充', '待补充'))
        return MockGuaSkill(*data)
    
    def analyze_gua_relationships(self, ben_gua: int, bian_gua: int) -> Dict:
        """分析卦际关系 (互联互通)"""
        return {
            'ben_gua': ben_gua,
            'bian_gua': bian_gua,
            'relationship_type': '变卦' if bian_gua else '静卦',
            'cuo_gua': self.get_cuo_gua(ben_gua),
            'zong_gua': self.get_zong_gua(ben_gua),
            'hu_gua': self.get_hu_gua(ben_gua)
        }
    
    def get_cuo_gua(self, gua_number: int) -> int:
        """获取错卦 (阴阳相反)"""
        # 简化计算，实际应查表
        return 65 - gua_number if gua_number <= 64 else 0
    
    def get_zong_gua(self, gua_number: int) -> int:
        """获取综卦 (上下颠倒)"""
        # 简化计算
        return gua_number
    
    def get_hu_gua(self, gua_number: int) -> int:
        """获取互卦 (中间 4 爻)"""
        # 简化计算
        return gua_number
    
    def analyze_yao_relationships(self, gua_skill, moving_yao: int) -> Dict:
        """分析爻际关系 (互联互通)"""
        if moving_yao < 0:
            return {'has_moving_yao': False}
        
        return {
            'has_moving_yao': True,
            'position': moving_yao,
            'position_name': self.get_yao_position_name(moving_yao),
            'corresponding_yao': self.get_corresponding_yao(moving_yao),
            'yin_yang_type': '阳爻' if moving_yao % 2 == 0 else '阴爻'
        }
    
    def get_yao_position_name(self, position: int) -> str:
        """获取爻位名称"""
        names = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻']
        return names[position] if 0 <= position < 6 else '未知'
    
    def get_corresponding_yao(self, yao_position: int) -> int:
        """获取对应爻位 (初↔四，二↔五，三↔上)"""
        correspondence = {0: 3, 1: 4, 2: 5, 3: 0, 4: 1, 5: 2}
        return correspondence.get(yao_position, -1)
    
    def apply_constitution(self, ben_gua, bian_gua, relationships, yao_relationships, question) -> Dict:
        """应用宪法原则"""
        application = {}
        
        for principle_name, principle in self.constitution_principles.items():
            application[principle_name] = {
                'name': principle['name'],
                'principle': principle['principle'],
                'guidance': self.apply_single_principle(principle, ben_gua, question)
            }
        
        return application
    
    def apply_single_principle(self, principle: Dict, ben_gua, question: str) -> str:
        """应用单个宪法原则"""
        name = principle['name']
        
        if name == '负熵法则':
            return '解释必须简洁，删除冗余信息，聚焦核心建议'
        elif name == '第一性原理':
            return f'从{ben_gua.gua_name}本源推导：{ben_gua.gua_ci}'
        elif name == '冰山理论':
            return '只输出 10% 核心结论，90% 推导在背后闭环'
        elif name == '二阶思维':
            return '推演短期和长期影响，不仅看眼前'
        elif name == '价值创造':
            return '解释必须有实际指导价值，帮助决策'
        
        return ''
    
    def generate_core_interpretation(self, ben_gua, bian_gua, relationships, 
                                    yao_relationships, constitution, question) -> str:
        """生成核心解释 (智能涌现)"""
        
        core = f"""🔮【核心解释】

本卦：{ben_gua.gua_name} - {ben_gua.gua_ci}
象曰：{ben_gua.xiang_zhuan}
"""
        
        # 变卦信息
        if bian_gua:
            core += f"\n变卦：{bian_gua.gua_name} (变化趋势)\n"
        
        # 动爻信息
        if yao_relationships.get('has_moving_yao'):
            core += f"\n动爻：{yao_relationships['position_name']} (重点关注)\n"
        
        # 卦象启示
        core += f"""
【卦象启示】
{ben_gua.gua_name}的核心智慧是"{ben_gua.gua_ci}"。
{self.get_gua_guidance(ben_gua.gua_name)}

【爻辞指导】
{self.get_yao_guidance(yao_relationships)}

【宪法原则应用】
"""
        
        # 宪法原则
        for principle_name, app in constitution.items():
            core += f"• {app['name']}: {app['guidance']}\n"
        
        # 行动建议
        core += f"""
【行动建议】
{self.get_action_advice(ben_gua.gua_name, yao_relationships, question)}
"""
        
        return core
    
    def get_gua_guidance(self, gua_name: str) -> str:
        """获取卦象指导"""
        guidance_map = {
            '乾为天': '自强不息，持续进步，但注意不要过刚易折',
            '坤为地': '厚德载物，包容万物，以柔克刚',
            '水雷屯': '初创艰难，坚持到底，不要急于求成',
            '山水蒙': '启蒙学习，虚心求教，不要自以为是',
            '天风姤': '相遇邂逅，把握机会，但需谨慎判断'
        }
        return guidance_map.get(gua_name, '遵循卦辞智慧，顺势而为')
    
    def get_yao_guidance(self, yao_relationships: Dict) -> str:
        """获取爻辞指导"""
        if not yao_relationships.get('has_moving_yao'):
            return '无动爻，参考卦辞整体指导'
        
        position = yao_relationships['position']
        position_names = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻']
        
        guidance_map = {
            0: '开始阶段，积蓄力量，不要急于行动',
            1: '展示阶段，可以主动表现，寻求指导',
            2: '行动阶段，勤奋努力，保持警惕',
            3: '突破阶段，可以尝试新事物',
            4: '领导阶段，大展宏图，承担责任',
            5: '终极阶段，知进知退，反思总结'
        }
        
        return guidance_map.get(position, '根据爻位采取相应行动')
    
    def get_action_advice(self, gua_name: str, yao_relationships: Dict, question: str) -> str:
        """获取行动建议"""
        advice = []
        
        # 基于卦名
        if gua_name == '乾为天':
            advice.append('保持积极进取的态度')
            advice.append('持续学习，不断提升自己')
        elif gua_name == '坤为地':
            advice.append('以包容心态对待他人')
            advice.append('耐心等待时机成熟')
        else:
            advice.append('遵循卦辞智慧行事')
        
        # 基于爻位
        if yao_relationships.get('has_moving_yao'):
            position = yao_relationships['position']
            if position == 0:
                advice.append('当前是积累阶段，不要急于表现')
            elif position == 4:
                advice.append('当前是领导阶段，要承担责任')
            elif position == 5:
                advice.append('成功后要懂得反思和退让')
        
        # 基于问题
        if '事业' in question or '工作' in question:
            advice.append('事业上要根据当前阶段采取相应策略')
        elif '感情' in question:
            advice.append('感情上要真诚相待，不要强求')
        
        return '\n'.join([f'{i+1}. {a}' for i, a in enumerate(advice)])
    
    def calculate_emergence_level(self, interpretation: str) -> str:
        """计算涌现等级"""
        word_count = len(interpretation)
        if word_count > 500:
            return '深度涌现 (Level 3) - 卦际 + 爻际 + 宪法原则完整分析'
        elif word_count > 200:
            return '中度涌现 (Level 2) - 卦象 + 动爻 + 部分原则'
        else:
            return '基础涌现 (Level 1) - 本卦 + 动爻解读'


def main():
    """测试"""
    engine = EmergenceEngine()
    
    # 模拟起卦结果
    gua_result = {
        'ben_gua': 1,  # 乾卦
        'bian_gua': 44,  # 姤卦 (乾初九变)
        'moving_yao': 0,  # 初九动
        'question': '事业发展'
    }
    
    result = engine.emerge(gua_result)
    
    print("=" * 60)
    print("🔮 智能涌现结果")
    print("=" * 60)
    print(f"时间：{result['timestamp']}")
    print(f"本卦：{result['ben_gua']}")
    print(f"变卦：{result['bian_gua']}")
    print(f"动爻：{result['moving_yao']}")
    print(f"问题：{result['question']}")
    print(f"涌现等级：{result['emergence_level']}")
    print("\n" + result['core_interpretation'])
    print("=" * 60)


if __name__ == '__main__':
    main()
