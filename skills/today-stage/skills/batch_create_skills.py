#!/usr/bin/env python3
"""
情景 Agent - 批量创建 64 情景 Skills

作者：太一 AGI
创建：2026-04-09
"""

import json
from pathlib import Path
from datetime import datetime

# 配置
SKILLS_DIR = Path(__file__).parent
DATA_FILE = Path(__file__).parent.parent / "data" / "stages.json"

# 64 情景定义
SCENARIOS = [
    # 晨间情景 (001-008)
    {"id": "001", "name": "早起", "category": "morning"},
    {"id": "002", "name": "洗漱", "category": "morning"},
    {"id": "003", "name": "早餐", "category": "morning"},
    {"id": "004", "name": "通勤", "category": "morning"},
    {"id": "005", "name": "晨会", "category": "morning"},
    {"id": "006", "name": "晨练", "category": "morning"},
    {"id": "007", "name": "阅读", "category": "morning"},
    {"id": "008", "name": "规划", "category": "morning"},
    
    # 工作情景 (009-024)
    {"id": "009", "name": "会议", "category": "work"},
    {"id": "010", "name": "专注", "category": "work"},
    {"id": "011", "name": "协作", "category": "work"},
    {"id": "012", "name": "邮件", "category": "work"},
    {"id": "013", "name": "报告", "category": "work"},
    {"id": "014", "name": "演示", "category": "work"},
    {"id": "015", "name": "谈判", "category": "work"},
    {"id": "016", "name": "决策", "category": "work"},
    {"id": "017", "name": "创新", "category": "work"},
    {"id": "018", "name": "学习", "category": "work"},
    {"id": "019", "name": "培训", "category": "work"},
    {"id": "020", "name": "面试", "category": "work"},
    {"id": "021", "name": "复盘", "category": "work"},
    {"id": "022", "name": "规划", "category": "work"},
    {"id": "023", "name": "休息", "category": "work"},
    {"id": "024", "name": "社交", "category": "work"},
    
    # 生活情景 (025-040)
    {"id": "025", "name": "午餐", "category": "life"},
    {"id": "026", "name": "购物", "category": "life"},
    {"id": "027", "name": "家务", "category": "life"},
    {"id": "028", "name": "烹饪", "category": "life"},
    {"id": "029", "name": "清洁", "category": "life"},
    {"id": "030", "name": "维修", "category": "life"},
    {"id": "031", "name": "缴费", "category": "life"},
    {"id": "032", "name": "办事", "category": "life"},
    {"id": "033", "name": "医疗", "category": "life"},
    {"id": "034", "name": "健身", "category": "life"},
    {"id": "035", "name": "运动", "category": "life"},
    {"id": "036", "name": "按摩", "category": "life"},
    {"id": "037", "name": "美容", "category": "life"},
    {"id": "038", "name": "穿搭", "category": "life"},
    {"id": "039", "name": "整理", "category": "life"},
    {"id": "040", "name": "收纳", "category": "life"},
    
    # 学习情景 (041-048)
    {"id": "041", "name": "课程", "category": "study"},
    {"id": "042", "name": "阅读", "category": "study"},
    {"id": "043", "name": "笔记", "category": "study"},
    {"id": "044", "name": "练习", "category": "study"},
    {"id": "045", "name": "复习", "category": "study"},
    {"id": "046", "name": "考试", "category": "study"},
    {"id": "047", "name": "研究", "category": "study"},
    {"id": "048", "name": "写作", "category": "study"},
    
    # 社交情景 (049-056)
    {"id": "049", "name": "聊天", "category": "social"},
    {"id": "050", "name": "聚会", "category": "social"},
    {"id": "051", "name": "约会", "category": "social"},
    {"id": "052", "name": "相亲", "category": "social"},
    {"id": "053", "name": "拜访", "category": "social"},
    {"id": "054", "name": "接待", "category": "social"},
    {"id": "055", "name": "送礼", "category": "social"},
    {"id": "056", "name": "感谢", "category": "social"},
    
    # 晚间情景 (057-064)
    {"id": "057", "name": "晚餐", "category": "evening"},
    {"id": "058", "name": "娱乐", "category": "evening"},
    {"id": "059", "name": "追剧", "category": "evening"},
    {"id": "060", "name": "游戏", "category": "evening"},
    {"id": "061", "name": "洗漱", "category": "evening"},
    {"id": "062", "name": "护肤", "category": "evening"},
    {"id": "063", "name": "冥想", "category": "evening"},
    {"id": "064", "name": "睡眠", "category": "evening"}
]

# 6 个阶段定义
STAGES = [
    {"id": "1", "name": "感知", "description": "觉察当前状态"},
    {"id": "2", "name": "理解", "description": "理解情景需求"},
    {"id": "3", "name": "规划", "description": "规划行动方案"},
    {"id": "4", "name": "执行", "description": "执行行动计划"},
    {"id": "5", "name": "反思", "description": "反思执行效果"},
    {"id": "6", "name": "优化", "description": "优化下次表现"}
]


def create_skill_file(scenario: dict, stage: dict) -> str:
    """创建单个 Skill 文件"""
    skill_id = f"stage-{scenario['id']}-{stage['id']}"
    skill_name = f"{scenario['name']}-{stage['name']}"
    
    content = f"""---
name: {skill_id}
version: 1.0.0
description: 今日情景 Agent - {skill_name}
category: today-stage
tags: ['情景', '{scenario['category']}', '{stage['name']}']
author: 太一 AGI
created: {datetime.now().strftime('%Y-%m-%d')}
status: active
---

# 🎯 {skill_name}

> 情景：{scenario['name']} | 阶段：{stage['name']}

---

## 阶段描述

{stage['description']}

---

## 核心功能

1. 状态感知
2. 智能推荐
3. 行动指导
4. 进度追踪

---

## 使用方式

```python
from skills.today-stage.skills.{skill_id} import StageHandler

handler = StageHandler()
action = handler.recommend()
```

---

## 心理学框架

- 认知行为疗法 (CBT)
- 正念冥想
- 习惯养成理论

---

*创建：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 今日情景 Agent v10.0*
"""
    
    return content


def main():
    """批量创建 Skills"""
    print("🎯 情景 Agent - 批量创建 64 情景 Skills")
    print("=" * 50)
    print()
    
    created_count = 0
    
    for scenario in SCENARIOS:
        scenario_dir = SKILLS_DIR / f"state-{scenario['id']}-{scenario['name'].lower()}"
        scenario_dir.mkdir(exist_ok=True)
        
        for stage in STAGES:
            skill_file = scenario_dir / f"{stage['id']}-{stage['name'].lower()}.md"
            content = create_skill_file(scenario, stage)
            
            with open(skill_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            created_count += 1
    
    print(f"✅ 创建完成!")
    print(f"   情景数：{len(SCENARIOS)} 个")
    print(f"   阶段数：{len(STAGES)} 个/情景")
    print(f"   总 Skills: {created_count} 个")
    print()
    print(f"📁 文件位置：{SKILLS_DIR}")


if __name__ == "__main__":
    main()
