#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gua Skill - 乾为天 (第 1 卦)
创建：2026-03-29
结构：1 卦 +6 爻
"""

import os
import json
from typing import Dict, List, Optional

class QianGuaSkill:
    """乾卦 Skill - 包含 6 爻"""
    
    def __init__(self):
        self.gua_number = 1
        self.gua_name = "乾为天"
        self.gua_image = "☰☰"
        self.gua_ci = "元亨利贞"
        self.xiang_zhuan = "天行健，君子以自强不息"
        
        # 加载 6 爻数据
        self.yao_data = self.load_yao_data()
    
    def load_yao_data(self) -> Dict:
        """加载 6 爻完整数据"""
        data_file = os.path.join(os.path.dirname(__file__), 'yao-data.json')
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_yao(self, yao_index: int) -> Optional[Dict]:
        """获取指定爻的数据"""
        if 'yaos' in self.yao_data and 0 <= yao_index < len(self.yao_data['yaos']):
            return self.yao_data['yaos'][yao_index]
        return None
    
    def get_yao_ci(self, yao_index: int) -> str:
        """获取爻辞"""
        yao = self.get_yao(yao_index)
        if yao:
            return yao.get('yao_ci', '')
        return ""
    
    def interpret_yao(self, yao_index: int, question: str = "") -> Dict:
        """解读指定爻"""
        yao = self.get_yao(yao_index)
        if not yao:
            return {}
        
        advice = yao.get('advice', {})
        
        # 根据问题类型选择建议
        specific_advice = ''
        if '事业' in question or '工作' in question:
            specific_advice = advice.get('事业', '')
        elif '感情' in question or '恋爱' in question or '婚姻' in question:
            specific_advice = advice.get('感情', '')
        elif '财' in question or '投资' in question:
            specific_advice = advice.get('财运', '')
        elif '健康' in question:
            specific_advice = advice.get('健康', '')
        else:
            specific_advice = list(advice.values())[0] if advice else ''
        
        return {
            'yao_name': yao.get('name', ''),
            'yao_ci': yao.get('yao_ci', ''),
            'xiang': yao.get('xiang', ''),
            'modern': yao.get('modern', ''),
            'advice': specific_advice,
            'story': yao.get('story', '')
        }
    
    def interpret_gua(self, moving_yao: int = -1, question: str = "") -> Dict:
        """解读整卦 (可指定动爻)"""
        result = {
            'gua_name': self.gua_name,
            'gua_ci': self.gua_ci,
            'xiang_zhuan': self.xiang_zhuan,
            'moving_yao': moving_yao,
        }
        
        # 如果有动爻，重点解读该爻
        if 0 <= moving_yao < 6:
            result['yao_interpretation'] = self.interpret_yao(moving_yao, question)
        else:
            # 无动爻，解读卦辞
            result['gua_interpretation'] = {
                'modern': '纯阳之卦，象征天道运行，自强不息',
                'advice': '积极进取，但注意时机'
            }
        
        return result


def main():
    """测试"""
    skill = QianGuaSkill()
    
    print(f"卦名：{skill.gua_name}")
    print(f"卦辞：{skill.gua_ci}")
    print(f"象传：{skill.xiang_zhuan}")
    print()
    
    # 测试解读初九爻
    result = skill.interpret_yao(0, "事业发展")
    print(f"初九爻辞：{result['yao_ci']}")
    print(f"现代解读：{result['modern']}")
    print(f"建议：{result['advice']}")
    print(f"故事：{result['story']}")


if __name__ == '__main__':
    main()
