#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gua Skill - 乾为天 (第 1 卦)
创建：2026-03-29
"""

class GuaSkill:
    """乾卦 Skill"""
    
    def __init__(self):
        self.gua_number = 1
        self.gua_name = "乾为天"
        self.gua_image = "☰☰"
        self.gua_ci = "元亨利贞"
        self.xiang_zhuan = "天行健，君子以自强不息"
        self.yao_cis = [
            "初九：潜龙勿用",
            "九二：见龙在田，利见大人",
            "九三：君子终日乾乾，夕惕若厉",
            "九四：或跃在渊，无咎",
            "九五：飞龙在天，利见大人",
            "上九：亢龙有悔"
        ]
        self.modern = "纯阳之卦，象征天道运行，自强不息"
        self.advice = {
            '事业': '积极进取，但注意时机',
            '感情': '真诚相待，不要过于强势',
            '财运': '正财有利，偏财谨慎',
            '健康': '注意头部和心脏'
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
        return self.advice.get(question_type, '自强不息，积极进取')
