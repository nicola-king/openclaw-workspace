# 64 卦 Skills 框架

> 创建时间：2026-03-29
> 总数：64 个 Skills (每卦一个)

---

## 📋 Skill 命名规范

```
gua-001-qian.py    # 乾卦
gua-002-kun.py     # 坤卦
gua-003-zhun.py    # 屯卦
...
gua-064-weiji.py   # 未济卦
```

---

## 📝 Skill 模板

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gua Skill - {卦名}
卦号：{序号}
卦象：{上卦}{下卦}
创建：2026-03-29
"""

class GuaSkill:
    """{卦名} Skill"""
    
    def __init__(self):
        self.gua_number = {序号}
        self.gua_name = "{卦名}"
        self.gua_image = "{卦象}"
        self.gua_ci = "{卦辞}"
        self.xiang_zhuan = "{象传}"
        
    def interpret(self, five_elements, gua_result, question):
        """
        解读卦象
        
        返回:
        - 卦辞
        - 象传
        - 爻辞 (根据动爻)
        - 现代解读
        - 应用建议
        """
        return {
            'gua_ci': self.gua_ci,
            'xiang_zhuan': self.xiang_zhuan,
            'yao_ci': self.get_yao_ci(gua_result['moving']),
            'modern': '现代解读...',
            'advice': '应用建议...'
        }
    
    def get_yao_ci(self, moving_yao: int) -> str:
        """获取动爻爻辞"""
        yao_cis = [
            '初九：潜龙勿用',
            '九二：见龙在田',
            '九三：君子终日乾乾',
            '九四：或跃在渊',
            '九五：飞龙在天',
            '上九：亢龙有悔'
        ]
        return yao_cis[moving_yao] if moving_yao < 6 else yao_cis[0]
    
    def get_advice(self, question_type: str) -> str:
        """根据问题类型给出建议"""
        advice_map = {
            '事业': '事业建议...',
            '感情': '感情建议...',
            '财运': '财运建议...',
            '健康': '健康建议...'
        }
        return advice_map.get(question_type, '综合建议...')
```

---

## 📊 64 卦 Skills 清单

### 上经 30 卦

| 序号 | 卦名 | 文件名 | 状态 |
|------|------|--------|------|
| 1 | 乾为天 | gua-001-qian.py | 🟡 待创建 |
| 2 | 坤为地 | gua-002-kun.py | 🟡 待创建 |
| 3 | 水雷屯 | gua-003-zhun.py | 🟡 待创建 |
| 4 | 山水蒙 | gua-004-meng.py | 🟡 待创建 |
| 5 | 水天需 | gua-005-xu.py | 🟡 待创建 |
| 6 | 天水讼 | gua-006-song.py | 🟡 待创建 |
| 7 | 地水师 | gua-007-shi.py | 🟡 待创建 |
| 8 | 水地比 | gua-008-bi.py | 🟡 待创建 |
| 9 | 风天小畜 | gua-009-xiaochu.py | 🟡 待创建 |
| 10 | 天泽履 | gua-010-lv.py | 🟡 待创建 |
| 11 | 地天泰 | gua-011-tai.py | 🟡 待创建 |
| 12 | 天地否 | gua-012-pi.py | 🟡 待创建 |
| 13 | 天火同人 | gua-013-tongren.py | 🟡 待创建 |
| 14 | 火天大有 | gua-014-dayou.py | 🟡 待创建 |
| 15 | 地山谦 | gua-015-qian.py | 🟡 待创建 |
| 16 | 雷地豫 | gua-016-yu.py | 🟡 待创建 |
| 17 | 泽雷随 | gua-017-sui.py | 🟡 待创建 |
| 18 | 山风蛊 | gua-018-gu.py | 🟡 待创建 |
| 19 | 地泽临 | gua-019-lin.py | 🟡 待创建 |
| 20 | 风地观 | gua-020-guan.py | 🟡 待创建 |
| 21 | 火雷噬嗑 | gua-021-shike.py | 🟡 待创建 |
| 22 | 山火贲 | gua-022-bi.py | 🟡 待创建 |
| 23 | 山地剥 | gua-023-bo.py | 🟡 待创建 |
| 24 | 地雷复 | gua-024-fu.py | 🟡 待创建 |
| 25 | 天雷无妄 | gua-025-wuwang.py | 🟡 待创建 |
| 26 | 山天大畜 | gua-026-dachu.py | 🟡 待创建 |
| 27 | 山雷颐 | gua-027-yi.py | 🟡 待创建 |
| 28 | 泽风大过 | gua-028-daguo.py | 🟡 待创建 |
| 29 | 坎为水 | gua-029-kan.py | 🟡 待创建 |
| 30 | 离为火 | gua-030-li.py | 🟡 待创建 |

### 下经 34 卦

| 序号 | 卦名 | 文件名 | 状态 |
|------|------|--------|------|
| 31 | 泽山咸 | gua-031-xian.py | 🟡 待创建 |
| 32 | 雷风恒 | gua-032-heng.py | 🟡 待创建 |
| 33 | 天山遁 | gua-033-dun.py | 🟡 待创建 |
| 34 | 雷天大壮 | gua-034-dazhuang.py | 🟡 待创建 |
| 35 | 火地晋 | gua-035-jin.py | 🟡 待创建 |
| 36 | 地火明夷 | gua-036-mingyi.py | 🟡 待创建 |
| 37 | 风火家人 | gua-037-jiaren.py | 🟡 待创建 |
| 38 | 火泽睽 | gua-038-kui.py | 🟡 待创建 |
| 39 | 水山蹇 | gua-039-jian.py | 🟡 待创建 |
| 40 | 雷水解 | gua-040-xie.py | 🟡 待创建 |
| 41 | 山泽损 | gua-041-sun.py | 🟡 待创建 |
| 42 | 风雷益 | gua-042-yi.py | 🟡 待创建 |
| 43 | 泽天夬 | gua-043-guai.py | 🟡 待创建 |
| 44 | 天风姤 | gua-044-gou.py | 🟡 待创建 |
| 45 | 泽地萃 | gua-045-cui.py | 🟡 待创建 |
| 46 | 地风升 | gua-046-sheng.py | 🟡 待创建 |
| 47 | 泽水困 | gua-047-kun.py | 🟡 待创建 |
| 48 | 水风井 | gua-048-jing.py | 🟡 待创建 |
| 49 | 泽火革 | gua-049-ge.py | 🟡 待创建 |
| 50 | 火风鼎 | gua-050-ding.py | 🟡 待创建 |
| 51 | 震为雷 | gua-051-zhen.py | 🟡 待创建 |
| 52 | 艮为山 | gua-052-gen.py | 🟡 待创建 |
| 53 | 风山渐 | gua-053-jian.py | 🟡 待创建 |
| 54 | 雷泽归妹 | gua-054-guimei.py | 🟡 待创建 |
| 55 | 雷火丰 | gua-055-feng.py | 🟡 待创建 |
| 56 | 火山旅 | gua-056-lv.py | 🟡 待创建 |
| 57 | 巽为风 | gua-057-xun.py | 🟡 待创建 |
| 58 | 兑为泽 | gua-058-dui.py | 🟡 待创建 |
| 59 | 风水涣 | gua-059-huan.py | 🟡 待创建 |
| 60 | 水泽节 | gua-060-jie.py | 🟡 待创建 |
| 61 | 风泽中孚 | gua-061-zhongfu.py | 🟡 待创建 |
| 62 | 雷山小过 | gua-062-xiaoguo.py | 🟡 待创建 |
| 63 | 水火既济 | gua-063-jiqi.py | 🟡 待创建 |
| 64 | 火水未济 | gua-064-weiji.py | 🟡 待创建 |

---

## 🚀 创建计划

| 批次 | Skills | 时间 | 负责 |
|------|--------|------|------|
| Batch 1 | 001-010 (乾坤等) | Day 1-3 | **素问** |
| Batch 2 | 011-020 | Day 4-6 | **素问** |
| Batch 3 | 021-030 | Day 7-9 | **素问** |
| Batch 4 | 031-040 | Day 10-12 | **素问** |
| Batch 5 | 041-050 | Day 13-15 | **素问** |
| Batch 6 | 051-064 | Day 16-18 | **素问** |

---

*创建时间：2026-03-29*
*太一 AGI · 易经 64 卦 Skills*
