#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
易经 Agent - 统一调度管理 64 卦 Skills
版本：v2.0 (更新版)
创建：2026-03-29
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from typing import Dict, List, Optional

# 导入辅助模块
from helpers.divination import DivinationHelper

class YijingAgent:
    """易经 Agent - 总管 64 卦 Skills"""
    
    def __init__(self):
        self.gua_skills = {}  # 64 卦 Skills
        self.helper = DivinationHelper()
        self.initialized = False
        
    def initialize(self):
        """初始化所有 Skills"""
        print("[INFO] 初始化易经 Agent...")
        
        # 动态加载已创建的 Skills
        skills_dir = os.path.join(os.path.dirname(__file__), 'skills')
        if os.path.exists(skills_dir):
            for file in os.listdir(skills_dir):
                if file.startswith('gua-') and file.endswith('.py'):
                    gua_num = int(file.split('-')[1])
                    self.gua_skills[gua_num] = file
                    print(f"[INFO] 加载 Skill: {file}")
        
        self.initialized = True
        print(f"[INFO] ✅ 易经 Agent 初始化完成 (已加载 {len(self.gua_skills)} Skills)")
        
    def time_to_gua(self, year: int, month: int, day: int,
                    hour: int, minute: int) -> Dict:
        """时间起卦法"""
        return self.helper.time_to_gua(year, month, day, hour, minute)
    
    def analyze(self, birth_info: Optional[Dict] = None,
                query_time: Optional[datetime] = None,
                question: str = "") -> Dict:
        """
        完整分析流程
        
        1. 根据时间起卦
        2. 获取卦象信息
        3. 生成解读和建议
        """
        
        if not query_time:
            query_time = datetime.now()
        
        # Step 1: 时间起卦
        gua_result = self.time_to_gua(
            query_time.year,
            query_time.month,
            query_time.day,
            query_time.hour,
            query_time.minute
        )
        
        # Step 2: 获取卦象解读
        interpretation = self.get_interpretation(gua_result)
        
        # Step 3: 生成建议
        advice = self.generate_advice(gua_result, question)
        
        return {
            'gua': gua_result,
            'interpretation': interpretation,
            'advice': advice,
            'timestamp': query_time.isoformat()
        }
    
    def get_interpretation(self, gua_result: Dict) -> Dict:
        """获取卦象解读"""
        gua_number = gua_result['gua_number']
        gua_name = gua_result['gua_name']
        
        # 尝试加载对应 Skill
        if gua_number in self.gua_skills:
            # TODO: 动态导入 Skill
            pass
        
        # 返回基础解读
        return {
            'gua_ci': '待补充',
            'xiang_zhuan': '待补充',
            'yao_ci': f'动爻：{gua_result["moving"]}',
            'modern': f'{gua_name} - 详见完整解读',
            'advice': '请参考具体卦象解读'
        }
    
    def generate_advice(self, gua_result: Dict, question: str) -> str:
        """根据问题生成建议"""
        gua_name = gua_result['gua_name']
        
        base_advice = f"当前卦象：{gua_name}。"
        
        if question:
            return f"{base_advice}针对您的问题：{question}，建议结合卦象智慧灵活应对。"
        else:
            return f"{base_advice}建议参考卦辞和象传的指导。"
    
    def get_daily_gua(self) -> Dict:
        """获取每日卦象"""
        now = datetime.now()
        return self.time_to_gua(now.year, now.month, now.day, 12, 0)


def main():
    """测试主函数"""
    agent = YijingAgent()
    agent.initialize()
    
    # 测试分析
    result = agent.analyze(question="事业发展")
    
    print(f"\n📊 分析结果:")
    print(f"卦象：{result['gua']['gua_name']}")
    print(f"上卦：{result['gua']['upper']}")
    print(f"下卦：{result['gua']['lower']}")
    print(f"动爻：{result['gua']['moving']}")
    print(f"建议：{result['advice']}")


if __name__ == '__main__':
    main()
