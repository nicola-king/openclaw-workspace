#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太极→两仪→四象→八卦→64 卦 演化演示
创建：2026-03-29
"""

class TaijiEvolution:
    """太极演化演示"""
    
    # 符号
    SYMBOLS = {
        'taiji': '☯',
        'yang': '⚊',
        'yin': '⚋',
        'taiyang': '⚌',
        'shaoyin': '⚍',
        'shaoyang': '⚎',
        'taiyin': '⚏',
        'qian': '☰', 'kun': '☷', 'zhen': '☳', 'xun': '☴',
        'kan': '☵', 'li': '☲', 'gen': '☶', 'dui': '☱'
    }
    
    def __init__(self):
        self.level = 0
        
    def show_evolution(self):
        """展示完整演化过程"""
        
        print("=" * 60)
        print("太极→两仪→四象→八卦→64 卦 演化演示")
        print("=" * 60)
        
        # Level 0: 太极
        print(f"\n【Level 0】太极")
        print(f"  {self.SYMBOLS['taiji']} 太极")
        print(f"  无极而太极，包含阴阳")
        
        # Level 1: 两仪
        print(f"\n【Level 1】两仪 (2)")
        print(f"  {self.SYMBOLS['yang']} 阳")
        print(f"  {self.SYMBOLS['yin']} 阴")
        print(f"  太极生两仪")
        
        # Level 2: 四象
        print(f"\n【Level 2】四象 (4)")
        print(f"  {self.SYMBOLS['taiyang']} 太阳 (阳 + 阳)")
        print(f"  {self.SYMBOLS['shaoyin']} 少阴 (阳 + 阴)")
        print(f"  {self.SYMBOLS['shaoyang']} 少阳 (阴 + 阳)")
        print(f"  {self.SYMBOLS['taiyin']} 太阴 (阴 + 阴)")
        print(f"  两仪生四象")
        
        # Level 3: 八卦
        print(f"\n【Level 3】八卦 (8)")
        bagua_names = [
            ('qian', '乾', '天'), ('dui', '兑', '泽'),
            ('li', '离', '火'), ('zhen', '震', '雷'),
            ('xun', '巽', '风'), ('kan', '坎', '水'),
            ('gen', '艮', '山'), ('kun', '坤', '地')
        ]
        for symbol, name, nature in bagua_names:
            print(f"  {self.SYMBOLS[symbol]} {name} ({nature})")
        print(f"  四象生八卦")
        
        # Level 4: 64 卦
        print(f"\n【Level 4】64 卦 (64)")
        print(f"  八卦两两相重 = 8 × 8 = 64 卦")
        print(f"  上经 30 卦 + 下经 34 卦 = 64 卦")
        print(f"  每卦 6 爻，共 384 爻")
        print(f"  八卦生 64 卦")
        
        print("\n" + "=" * 60)
        print("演化完成!")
        print("=" * 60)
    
    def get_gua(self, upper: str, lower: str) -> dict:
        """根据上下卦获取 64 卦信息"""
        
        gua_map = {
            ('qian', 'qian'): {'number': 1, 'name': '乾为天'},
            ('kun', 'kun'): {'number': 2, 'name': '坤为地'},
            ('kan', 'zhen'): {'number': 3, 'name': '水雷屯'},
            # ... 可以扩展完整 64 卦映射
        }
        
        key = (upper, lower)
        return gua_map.get(key, {'number': 1, 'name': '乾为天'})


def main():
    """主函数"""
    evolution = TaijiEvolution()
    evolution.show_evolution()
    
    # 示例：获取特定卦
    print("\n📊 示例：地天泰卦")
    result = evolution.get_gua('kun', 'qian')
    print(f"卦号：{result['number']}")
    print(f"卦名：{result['name']}")


if __name__ == '__main__':
    main()
