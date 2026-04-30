#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gua Skill - 水雷屯 (第 3 卦)
创建：2026-03-29
"""

class GuaSkill:
    """屯卦 Skill"""
    
    def __init__(self):
        self.gua_number = 3
        self.gua_name = "水雷屯"
        self.gua_image = "☵☳"
        self.gua_ci = "元亨利贞，勿用有攸往"
        self.xiang_zhuan = "云雷屯，君子以经纶"
        self.yao_cis = [
            "初九：磐桓，利居贞",
            "六二：屯如邅如，乘马班如",
            "六三：即鹿无虞，惟入于林中",
            "六四：乘马班如，求婚媾",
            "九五：屯其膏，小贞吉",
            "上六：乘马班如，泣血涟如"
        ]
        self.modern = "初创艰难，需要坚持和耐心"
        self.advice = {
            '事业': '创业初期，艰难但要坚持',
            '感情': '磨合期，需要耐心',
            '财运': '不宜大额投资',
            '健康': '注意肝胆'
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
        return self.advice.get(question_type, '艰难中坚持，不要放弃')
