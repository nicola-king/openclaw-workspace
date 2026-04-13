# 64 卦 Skills 爻挂载架构

> 创建时间：2026-03-29 15:38
> 总结构：64 卦 × 6 爻 = 384 爻
> 挂载方式：每卦 Skill 包含 6 爻数据

---

## 📁 文件结构设计

```
skills/yijing/
├── agent/
│   └── yijing-agent-v2.py          # 易经 Agent 总管
│
├── skills/
│   ├── gua-001-qian/               # 乾卦 Skill (目录式)
│   │   ├── __init__.py             # 乾卦主模块
│   │   ├── yao-01-chujiu.py        # 初九：潜龙勿用
│   │   ├── yao-02-jiuer.py         # 九二：见龙在田
│   │   ├── yao-03-jiusan.py        # 九三：君子终日乾乾
│   │   ├── yao-04-jiusi.py         # 九四：或跃在渊
│   │   ├── yao-05-jiuwu.py         # 九五：飞龙在天
│   │   ├── yao-06-shangjiu.py      # 上九：亢龙有悔
│   │   └── yao-data.json           # 6 爻完整数据
│   │
│   ├── gua-002-kun/                # 坤卦 Skill
│   │   ├── __init__.py
│   │   ├── yao-01-chuliu.py        # 初六：履霜坚冰至
│   │   ├── yao-06-shangliu.py      # 上六：龙战于野
│   │   └── yao-data.json
│   │
│   ├── gua-003-zhun/               # 屯卦 Skill
│   │   └── ...
│   │
│   └── ... (64 个卦目录)
│
├── helpers/
│   ├── divination.py               # 起卦算法
│   ├── taiji-evolution.py          # 演化演示
│   └── yao-interpreter.py          # 爻辞解读器 🆕
│
└── data/
    ├── 64-gua-data.json            # 64 卦框架数据
    └── 384-yao-data.json           # 384 爻完整数据 🆕
```

---

## 📖 单个卦 Skill 结构示例 (乾卦)

### gua-001-qian/__init__.py

```python
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

# 导入 6 爻
from .yao-01-chujiu import Yao01
from .yao-02-jiuer import Yao02
from .yao-03-jiusan import Yao03
from .yao-04-jiusi import Yao04
from .yao-05-jiuwu import Yao05
from .yao-06-shangjiu import Yao06

class QianGuaSkill:
    """乾卦 Skill - 包含 6 爻"""
    
    def __init__(self):
        self.gua_number = 1
        self.gua_name = "乾为天"
        self.gua_image = "☰☰"
        self.gua_ci = "元亨利贞"
        self.xiang_zhuan = "天行健，君子以自强不息"
        
        # 加载 6 爻
        self.yaos = [
            Yao01(),  # 初九
            Yao02(),  # 九二
            Yao03(),  # 九三
            Yao04(),  # 九四
            Yao05(),  # 九五
            Yao06(),  # 上九
        ]
        
        # 加载爻数据
        self.yao_data = self.load_yao_data()
    
    def load_yao_data(self) -> Dict:
        """加载 6 爻完整数据"""
        data_file = os.path.join(os.path.dirname(__file__), 'yao-data.json')
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_yao(self, yao_index: int):
        """
        获取指定爻
        
        Args:
            yao_index: 爻位 (0-5，从下往上)
        
        Returns:
            对应爻的实例
        """
        if 0 <= yao_index < 6:
            return self.yaos[yao_index]
        return None
    
    def get_yao_ci(self, yao_index: int) -> str:
        """获取爻辞"""
        yao = self.get_yao(yao_index)
        if yao:
            return yao.yao_ci
        return ""
    
    def interpret_yao(self, yao_index: int, question: str = "") -> Dict:
        """
        解读指定爻
        
        Args:
            yao_index: 爻位 (0-5)
            question: 问题
        
        Returns:
            解读结果
        """
        yao = self.get_yao(yao_index)
        if not yao:
            return {}
        
        return {
            'yao_name': yao.yao_name,
            'yao_ci': yao.yao_ci,
            'xiang': yao.xiang,
            'modern': yao.modern_interpretation,
            'advice': yao.get_advice(question),
            'story': yao.story if hasattr(yao, 'story') else None
        }
    
    def interpret_gua(self, moving_yao: int = -1, question: str = "") -> Dict:
        """
        解读整卦 (可指定动爻)
        
        Args:
            moving_yao: 动爻位置 (0-5，-1 表示无动爻)
            question: 问题
        
        Returns:
            完整解读
        """
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
```

---

### gua-001-qian/yao-01-chujiu.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
乾卦 - 初九爻
爻辞：潜龙勿用
"""

class Yao01:
    """初九：潜龙勿用"""
    
    def __init__(self):
        self.yao_position = 0  # 爻位 (0-5)
        self.yao_name = "初九"
        self.yao_ci = "潜龙勿用"
        self.xiang = "潜龙勿用，阳在下也"
        self.modern_interpretation = "龙潜伏在水中，暂时不要行动。象征积蓄力量，等待时机。"
    
    def get_advice(self, question: str = "") -> str:
        """根据问题给出建议"""
        advice_map = {
            '事业': '新人入职或创业初期，不要急于表现，先学习和积累',
            '感情': '缘分未到，不要强求，先提升自己',
            '财运': '不宜大额投资，以储蓄为主',
            '健康': '注意调养，不要过度消耗',
            '学习': '打好基础，不要急于求成'
        }
        
        if question:
            for key in advice_map:
                if key in question:
                    return advice_map[key]
        
        return '现在是积蓄力量的时候，不要急于行动。等待时机成熟再出击。'
    
    def get_story(self) -> str:
        """爻辞故事"""
        return """
        姜子牙 72 岁前一直在渭水边钓鱼，看似无所作为，
        实际上在观察时局，积累智慧。
        直到周文王来访，他才出山辅佐，最终帮助周朝建立。
        
        这就是"潜龙勿用"的典范：在时机未到时，耐心潜伏。
        """
```

---

### gua-001-qian/yao-02-jiuer.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
乾卦 - 九二爻
爻辞：见龙在田，利见大人
"""

class Yao02:
    """九二：见龙在田，利见大人"""
    
    def __init__(self):
        self.yao_position = 1
        self.yao_name = "九二"
        self.yao_ci = "见龙在田，利见大人"
        self.xiang = "见龙在田，德施普也"
        self.modern_interpretation = "龙出现在田野上，利于见贵人。象征初露锋芒，寻求指导。"
    
    def get_advice(self, question: str = "") -> str:
        advice_map = {
            '事业': '能力开始展现，适合寻找导师或贵人提携',
            '感情': '可以主动展示自己，参加社交活动',
            '财运': '有小额收益，可以适度投资',
            '健康': '身体状况良好，保持锻炼',
            '学习': '展示学习成果，寻求老师指导'
        }
        
        if question:
            for key in advice_map:
                if key in question:
                    return advice_map[key]
        
        return '你的能力开始被认可，适合主动展示自己，寻找贵人指导。'
    
    def get_story(self) -> str:
        return """
        诸葛亮 27 岁前在隆中躬耕，看似隐居，
        实际上广交名士，学习兵法。
        直到刘备三顾茅庐，他才出山，
        这就是"见龙在田，利见大人"的体现。
        """
```

---

### gua-001-qian/yao-data.json

```json
{
  "gua_number": 1,
  "gua_name": "乾为天",
  "yaos": [
    {
      "position": 0,
      "name": "初九",
      "yao_ci": "潜龙勿用",
      "xiang": "潜龙勿用，阳在下也",
      "modern": "积蓄力量，等待时机",
      "advice": {
        "事业": "新人入职或创业初期，不要急于表现",
        "感情": "缘分未到，不要强求",
        "财运": "不宜大额投资，以储蓄为主",
        "健康": "注意调养，不要过度消耗",
        "学习": "打好基础，不要急于求成"
      },
      "story": "姜子牙 72 岁前渭水钓鱼的故事"
    },
    {
      "position": 1,
      "name": "九二",
      "yao_ci": "见龙在田，利见大人",
      "xiang": "见龙在田，德施普也",
      "modern": "初露锋芒，寻求指导",
      "advice": {
        "事业": "能力开始展现，适合寻找导师",
        "感情": "可以主动展示自己",
        "财运": "有小额收益，可以适度投资",
        "健康": "身体状况良好",
        "学习": "展示学习成果，寻求老师指导"
      },
      "story": "诸葛亮 27 岁前隆中躬耕的故事"
    },
    {
      "position": 2,
      "name": "九三",
      "yao_ci": "君子终日乾乾，夕惕若厉",
      "xiang": "终日乾乾，反复道也",
      "modern": "勤奋努力，保持警惕",
      "advice": {
        "事业": "职场上升期，努力工作但要保持警惕",
        "感情": "用心经营，不要疏忽",
        "财运": "谨慎投资，注意风险",
        "健康": "注意劳逸结合",
        "学习": "持续努力，不要松懈"
      },
      "story": "曾国藩每日自省的故事"
    },
    {
      "position": 3,
      "name": "九四",
      "yao_ci": "或跃在渊，无咎",
      "xiang": "或跃在渊，进无咎也",
      "modern": "尝试突破，即使失败也无妨",
      "advice": {
        "事业": "可以尝试职业转型或创业",
        "感情": "可以主动表白或推进关系",
        "财运": "可以适度冒险投资",
        "健康": "可以尝试新的运动方式",
        "学习": "可以挑战更高难度的内容"
      },
      "story": "马云创建阿里巴巴前的尝试"
    },
    {
      "position": 4,
      "name": "九五",
      "yao_ci": "飞龙在天，利见大人",
      "xiang": "飞龙在天，大人造也",
      "modern": "事业巅峰，施展抱负",
      "advice": {
        "事业": "领导岗位，大展宏图",
        "感情": "关系稳定，可以考虑婚姻",
        "财运": "财运亨通，可以大额投资",
        "健康": "状态最佳，保持锻炼",
        "学习": "可以教授他人，教学相长"
      },
      "story": "李世民玄武门之变后登基"
    },
    {
      "position": 5,
      "name": "上九",
      "yao_ci": "亢龙有悔",
      "xiang": "亢龙有悔，盈不可久也",
      "modern": "物极必反，知进知退",
      "advice": {
        "事业": "考虑退休或权力交接",
        "感情": "不要过于强势，给对空间",
        "财运": "见好就收，不要贪心",
        "健康": "注意过度消耗的问题",
        "学习": "学会放下，不要执着"
      },
      "story": "范蠡功成身退的故事"
    }
  ]
}
```

---

## 🔧 爻解读器 (helpers/yao-interpreter.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爻辞解读器
功能：根据爻位和问题生成解读
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class YaoInterpreter:
    """爻辞解读器"""
    
    def __init__(self):
        self.yao_positions = {
            0: '初爻 - 开始/基础',
            1: '二爻 - 地位/展示',
            2: '三爻 - 人位/行动',
            3: '四爻 - 臣位/辅佐',
            4: '五爻 - 君位/领导',
            5: '上爻 - 终极/反思'
        }
    
    def interpret(self, gua_name: str, yao_position: int, 
                  yao_ci: str, question: str = "") -> dict:
        """
        解读爻辞
        
        Args:
            gua_name: 卦名
            yao_position: 爻位 (0-5)
            yao_ci: 爻辞
            question: 问题
        
        Returns:
            解读结果
        """
        return {
            'gua_name': gua_name,
            'yao_position': self.yao_positions.get(yao_position, '未知'),
            'yao_ci': yao_ci,
            'question': question,
            'advice': self.get_advice(yao_position, question),
            'story': self.get_story(gua_name, yao_position)
        }
    
    def get_advice(self, yao_position: int, question: str) -> str:
        """根据爻位给出建议"""
        position_advice = {
            0: '开始阶段，要谨慎行事，打好基础',
            1: '展示阶段，可以主动表现，寻求指导',
            2: '行动阶段，要勤奋努力，保持警惕',
            3: '突破阶段，可以尝试新事物',
            4: '领导阶段，可以大展宏图',
            5: '终极阶段，要知进知退，反思总结'
        }
        return position_advice.get(yao_position, '请提供具体爻位')
    
    def get_story(self, gua_name: str, yao_position: int) -> str:
        """获取爻辞故事"""
        # TODO: 从数据库加载故事
        return '故事加载中...'


def main():
    """测试"""
    interpreter = YaoInterpreter()
    
    result = interpreter.interpret(
        gua_name='乾为天',
        yao_position=0,
        yao_ci='潜龙勿用',
        question='事业发展'
    )
    
    print(f"卦名：{result['gua_name']}")
    print(f"爻位：{result['yao_position']}")
    print(f"爻辞：{result['yao_ci']}")
    print(f"问题：{result['question']}")
    print(f"建议：{result['advice']}")
    print(f"故事：{result['story']}")


if __name__ == '__main__':
    main()
```

---

## 📊 批量创建脚本

### scripts/create-64-gua-skills.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建 64 卦 Skills (每卦 6 爻)
"""

import os
import json

# 64 卦数据
GUA_DATA = {
    1: {'name': '乾为天', 'pinyin': 'qian', 'yaos': ['初九', '九二', '九三', '九四', '九五', '上九']},
    2: {'name': '坤为地', 'pinyin': 'kun', 'yaos': ['初六', '六二', '六三', '六四', '六五', '上六']},
    3: {'name': '水雷屯', 'pinyin': 'zhun', 'yaos': ['初九', '六二', '六三', '六四', '九五', '上六']},
    # ... 继续 64 卦
}

def create_gua_skill(gua_number: int, gua_info: dict):
    """创建单个卦 Skill 目录"""
    
    gua_name = gua_info['name']
    pinyin = gua_info['pinyin']
    yaos = gua_info['yaos']
    
    # 创建目录
    dir_name = f"gua-{gua_number:03d}-{pinyin}"
    base_path = f"/home/nicola/.openclaw/workspace/skills/yijing/skills/{dir_name}"
    os.makedirs(base_path, exist_ok=True)
    
    # 创建 __init__.py
    init_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gua Skill - {gua_name} (第{gua_number}卦)
"""

from .yao-data import YAO_DATA

class {pinyin.capitalize()}GuaSkill:
    """{gua_name} Skill"""
    
    def __init__(self):
        self.gua_number = {gua_number}
        self.gua_name = "{gua_name}"
        self.yaos = YAO_DATA
'''
    
    with open(f"{base_path}/__init__.py", 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    # 创建 yao-data.json
    yao_data = {
        'gua_number': gua_number,
        'gua_name': gua_name,
        'yaos': []
    }
    
    for i, yao_name in enumerate(yaos):
        yao_data['yaos'].append({
            'position': i,
            'name': yao_name,
            'yao_ci': '待补充',
            'xiang': '待补充',
            'modern': '待补充',
            'advice': {
                '事业': '待补充',
                '感情': '待补充',
                '财运': '待补充',
                '健康': '待补充'
            }
        })
    
    with open(f"{base_path}/yao-data.json", 'w', encoding='utf-8') as f:
        json.dump(yao_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建：{dir_name}")

def main():
    """主函数"""
    print("开始创建 64 卦 Skills...")
    
    for gua_number, gua_info in GUA_DATA.items():
        create_gua_skill(gua_number, gua_info)
    
    print(f"✅ 完成！创建 {len(GUA_DATA)} 个卦 Skills")

if __name__ == '__main__':
    main()
```

---

## 🎯 执行计划

| 批次 | 卦数 | 爻数 | 时间 | 负责 |
|------|------|------|------|------|
| Batch 1 | 卦 001-010 | 60 爻 | 今日 18:00 | **素问** |
| Batch 2 | 卦 011-020 | 60 爻 | 今日 20:00 | **素问** |
| Batch 3 | 卦 021-030 | 60 爻 | 明日 12:00 | **素问** |
| Batch 4 | 卦 031-040 | 60 爻 | 明日 18:00 | **素问** |
| Batch 5 | 卦 041-050 | 60 爻 | 明日 20:00 | **素问** |
| Batch 6 | 卦 051-064 | 84 爻 | 3 月 30 日 | **素问** |

---

*创建时间：2026-03-29 15:38*
*太一 AGI · 64 卦 Skills 爻挂载架构*
