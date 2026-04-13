#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gua Skill - 坤为地 (第 2 卦)
创建：2026-03-29
"""

class GuaSkill:
    """坤卦 Skill"""
    
    def __init__(self):
        self.gua_number = 2
        self.gua_name = "坤为地"
        self.gua_image = "☷☷"
        self.gua_ci = "元亨，利牝马之贞"
        self.xiang_zhuan = "地势坤，君子以厚德载物"
        self.yao_cis = [
            "初六：履霜，坚冰至",
            "六二：直方大，不习无不利",
            "六三：含章可贞",
            "六四：括囊，无咎无誉",
            "六五：黄裳，元吉",
            "上六：龙战于野，其血玄黄"
        ]
        self.modern = "纯阴之卦，象征地道承载，厚德载物"
        self.advice = {
            '事业': '配合协作，不要强出头',
            '感情': '包容理解，柔中带刚',
            '财运': '稳定为主，不宜冒险',
            '健康': '注意脾胃和腹部'
        }
        
    def interpret(self, five_elements, gua_result, question):
        """解读卦象"""
        moving = gua_result.get('moving', 0)
        return {
            'gua_ci': self.gua_ci,
            'xiang_zhuan': self.xiang_zhuan,
            'yao_ci': self.yao_cis[moving] if moving < 6 else self.yao_cis[0],
            'modern': self.modern,
            'advice': self.advice
        }
    
    def get_advice(self, question_type):
        """根据问题类型给出建议"""
        return self.advice.get(question_type, '厚德载物，包容协作')
