#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
起卦算法模块
创建：2026-03-29
"""

from datetime import datetime
from typing import Dict

class DivinationHelper:
    """起卦辅助类"""
    
    # 八卦数字映射
    BAGUA_MAP = {
        1: '乾', 2: '兑', 3: '离', 4: '震',
        5: '巽', 6: '坎', 7: '艮', 8: '坤'
    }
    
    # 64 卦映射表 (上卦，下卦) -> 卦号
    GUA_MAP = {
        (1, 1): 1, (8, 8): 2, (6, 4): 3, (7, 6): 4,
        (6, 1): 5, (1, 6): 6, (8, 6): 7, (6, 8): 8,
        (5, 1): 9, (1, 2): 10, (8, 1): 11, (1, 8): 12,
        (1, 3): 13, (3, 1): 14, (8, 7): 15, (4, 8): 16,
        (2, 4): 17, (7, 5): 18, (8, 2): 19, (5, 8): 20,
        (3, 4): 21, (7, 3): 22, (7, 8): 23, (8, 4): 24,
        (1, 4): 25, (7, 1): 26, (7, 4): 27, (2, 5): 28,
        (6, 6): 29, (3, 3): 30, (2, 7): 31, (4, 5): 32,
        (1, 7): 33, (4, 1): 34, (3, 8): 35, (8, 3): 36,
        (5, 3): 37, (3, 2): 38, (6, 7): 39, (4, 6): 40,
        (7, 2): 41, (5, 4): 42, (2, 1): 43, (1, 5): 44,
        (2, 8): 45, (8, 5): 46, (2, 6): 47, (6, 5): 48,
        (2, 3): 49, (3, 5): 50, (4, 4): 51, (7, 7): 52,
        (5, 7): 53, (4, 2): 54, (4, 3): 55, (3, 7): 56,
        (5, 5): 57, (2, 2): 58, (5, 6): 59, (6, 2): 60,
        (5, 2): 61, (4, 7): 62, (6, 3): 63, (3, 6): 64
    }
    
    # 64 卦名
    GUA_NAMES = {
        1: '乾为天', 2: '坤为地', 3: '水雷屯', 4: '山水蒙',
        5: '水天需', 6: '天水讼', 7: '地水师', 8: '水地比',
        9: '风天小畜', 10: '天泽履', 11: '地天泰', 12: '天地否',
        13: '天火同人', 14: '火天大有', 15: '地山谦', 16: '雷地豫',
        17: '泽雷随', 18: '山风蛊', 19: '地泽临', 20: '风地观',
        21: '火雷噬嗑', 22: '山火贲', 23: '山地剥', 24: '地雷复',
        25: '天雷无妄', 26: '山天大畜', 27: '山雷颐', 28: '泽风大过',
        29: '坎为水', 30: '离为火', 31: '泽山咸', 32: '雷风恒',
        33: '天山遁', 34: '雷天大壮', 35: '火地晋', 36: '地火明夷',
        37: '风火家人', 38: '火泽睽', 39: '水山蹇', 40: '雷水解',
        41: '山泽损', 42: '风雷益', 43: '泽天夬', 44: '天风姤',
        45: '泽地萃', 46: '地风升', 47: '泽水困', 48: '水风井',
        49: '泽火革', 50: '火风鼎', 51: '震为雷', 52: '艮为山',
        53: '风山渐', 54: '雷泽归妹', 55: '雷火丰', 56: '火山旅',
        57: '巽为风', 58: '兑为泽', 59: '风水涣', 60: '水泽节',
        61: '风泽中孚', 62: '雷山小过', 63: '水火既济', 64: '火水未济'
    }
    
    def time_to_gua(self, year: int, month: int, day: int,
                    hour: int, minute: int) -> Dict:
        """
        时间起卦法
        
        上卦 = (年 + 月 + 日) % 8
        下卦 = (年 + 月 + 日 + 时) % 8
        动爻 = (年 + 月 + 日 + 时 + 分) % 6
        """
        
        # 计算上下卦
        upper = (year + month + day) % 8
        lower = (year + month + day + hour) % 8
        moving = (year + month + day + hour + minute) % 6
        
        # 处理 0 的情况 (余数为 0 代表 8)
        if upper == 0: upper = 8
        if lower == 0: lower = 8
        if moving == 0: moving = 6
        
        # 获取卦号和卦名
        gua_number = self.GUA_MAP.get((upper, lower), 1)
        gua_name = self.GUA_NAMES.get(gua_number, '乾为天')
        
        return {
            'upper': self.BAGUA_MAP[upper],
            'lower': self.BAGUA_MAP[lower],
            'upper_num': upper,
            'lower_num': lower,
            'moving': moving,
            'gua_name': gua_name,
            'gua_number': gua_number
        }
    
    def get_gua_info(self, gua_number: int) -> Dict:
        """获取卦象完整信息"""
        return {
            'number': gua_number,
            'name': self.GUA_NAMES.get(gua_number, '乾为天')
        }


def main():
    """测试"""
    helper = DivinationHelper()
    now = datetime.now()
    
    result = helper.time_to_gua(
        now.year, now.month, now.day,
        now.hour, now.minute
    )
    
    print(f"📊 起卦结果:")
    print(f"上卦：{result['upper']}")
    print(f"下卦：{result['lower']}")
    print(f"卦名：{result['gua_name']}")
    print(f"卦号：{result['gua_number']}")
    print(f"动爻：{result['moving']}")


if __name__ == '__main__':
    main()
