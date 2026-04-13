# 今日情景 Agent · 64 个情景状态 Skills 架构

> 创建时间：2026-03-29 18:24
> 版本：7.0.0
> 描述：64 个情景状态 = 64 个 Skills，每个 Skill 包含 6 个阶段

---

## 📊 核心架构

```
今日情景 Agent (总管)
    ↓
64 个情景状态 Skills
    ↓
每个 Skill 包含 6 个阶段
    ↓
384 种状态组合
```

---

## 📁 文件结构

```
skills/today-stage/
├── agent/
│   ├── today-stage-agent.py      # 今日情景 Agent (总管)
│   ├── emergence-engine.py       # 智能涌现引擎
│   └── stage-matcher.py          # 情景状态匹配算法
│
├── skills/                       # 64 个情景状态 Skills
│   ├── state-001-qishi/          # 状态 001: 起势期
│   │   ├── __init__.py           # 状态主模块
│   │   ├── stage-01.py           # 阶段 1: 初始阶段
│   │   ├── stage-02.py           # 阶段 2: 发展阶段
│   │   ├── stage-03.py           # 阶段 3: 强化阶段
│   │   ├── stage-04.py           # 阶段 4: 转化阶段
│   │   ├── stage-05.py           # 阶段 5: 整合阶段
│   │   ├── stage-06.py           # 阶段 6: 完成阶段
│   │   └── state-data.json       # 状态完整数据
│   │
│   ├── state-002-chengzai/       # 状态 002: 承载期
│   ├── state-003-hunduan/        # 状态 003: 启动混乱期
│   └── ... (共 64 个情景状态 Skills)
│
├── helpers/
│   ├── psychology-framework.py   # 心理学框架
│   ├── action-advisor.py         # 行动建议生成器
│   └── viral-headlines.py        # 爆点句生成器
│
└── data/
    ├── stages-64-final.json      # 64 个情景状态数据
    ├── stages-384-mapping.json   # 384 状态映射
    └── design-decision-v7.json   # 设计决策文档
```

---

## 🎯 64 个情景状态 Skills 列表

### State 001-010

| 编号 | 状态名 | Skill 目录 | 核心主题 |
|------|--------|-----------|---------|
| 001 | 起势期 | state-001-qishi | 潜力大于结果 |
| 002 | 承载期 | state-002-chengzai | 责任增加主动权低 |
| 003 | 启动混乱期 | state-003-hunduan | 刚开始不顺 |
| 004 | 认知盲区期 | state-004-mangqu | 理解有偏差 |
| 005 | 等待窗口期 | state-005-dengdai | 准备好未启动 |
| 006 | 冲突边缘期 | state-006-chongtu | 即将产生对抗 |
| 007 | 结构协同期 | state-007-xietong | 需要协作 |
| 008 | 资源整合期 | state-008-zhenghe | 寻找合作 |
| 009 | 小幅增长期 | state-009-zengzhang | 进步缓慢 |
| 010 | 规则适应期 | state-010-guze | 环境有要求 |

### State 011-020

| 编号 | 状态名 | 核心主题 |
|------|--------|---------|
| 011 | 通畅期 | 流程顺畅 |
| 012 | 停滞期 | 进展受阻 |
| 013 | 关系深化期 | 关系加强 |
| 014 | 资源高位期 | 资源较多 |
| 015 | 收敛期 | 需要收敛 |
| 016 | 蓄势期 | 准备阶段 |
| 017 | 跟随期 | 参考他人路径 |
| 018 | 修正期 | 出现问题 |
| 019 | 接近期 | 接近机会 |
| 020 | 观察期 | 需要观察 |

### State 021-030

| 编号 | 状态名 | 核心主题 |
|------|--------|---------|
| 021 | 突破期 | 需要果断行动 |
| 022 | 表象期 | 注重呈现 |
| 023 | 剥离期 | 资源流失 |
| 024 | 回归期 | 重新开始 |
| 025 | 自然推进期 | 自然发展 |
| 026 | 能量储备期 | 力量积累 |
| 027 | 输入调整期 | 输入重要 |
| 028 | 压力过载期 | 压力过大 |
| 029 | 反复风险期 | 反复遇到问题 |
| 030 | 高曝光期 | 被关注 |

### State 031-040

| 编号 | 状态名 | 核心主题 |
|------|--------|---------|
| 031 | 吸引期 | 吸引他人 |
| 032 | 长期稳定期 | 稳定发展 |
| 033 | 主动退让期 | 需要后退 |
| 034 | 力量释放期 | 能量充足 |
| 035 | 上升期 | 正在上升 |
| 036 | 隐匿期 | 需要低调 |
| 037 | 内部结构期 | 关注内部 |
| 038 | 分歧期 | 意见不同 |
| 039 | 阻碍期 | 推进困难 |
| 040 | 释放期 | 问题缓解 |

### State 041-050

| 编号 | 状态名 | 核心主题 |
|------|--------|---------|
| 041 | 主动减负期 | 需要减少 |
| 042 | 收益增长期 | 收益提升 |
| 043 | 决断期 | 必须做决定 |
| 044 | 突发干扰期 | 出现干扰 |
| 045 | 聚集期 | 资源集中 |
| 046 | 稳步上升期 | 持续进步 |
| 047 | 受限期 | 受限明显 |
| 048 | 资源基础期 | 资源稳定 |
| 049 | 变革期 | 需要改变 |
| 050 | 结构成型期 | 系统成熟 |

### State 051-060

| 编号 | 状态名 | 核心主题 |
|------|--------|---------|
| 051 | 冲击期 | 突发冲击 |
| 052 | 暂停期 | 需要暂停 |
| 053 | 渐进期 | 逐步推进 |
| 054 | 依附期 | 依赖他人 |
| 055 | 高峰期 | 达到高点 |
| 056 | 流动期 | 处于变化中 |
| 057 | 渗透期 | 逐步影响 |
| 058 | 互动期 | 互动频繁 |
| 059 | 分散期 | 结构分散 |
| 060 | 限制优化期 | 受规则限制 |

### State 061-064

| 编号 | 状态名 | 核心主题 |
|------|--------|---------|
| 061 | 内在确认期 | 需要确认 |
| 062 | 细节处理期 | 细节重要 |
| 063 | 完成临界期 | 接近完成 |
| 064 | 未完成期 | 尚未完成 |

---

## 🔧 单个 Skill 结构示例

### state-001-qishi/__init__.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情景状态 Skill 001 - 起势期
6 个阶段 × 心理学框架 × 行动建议
"""

import json
import os
from typing import Dict, List

class QishiStateSkill:
    """起势期情景状态 Skill"""
    
    def __init__(self):
        self.state_id = 1
        self.state_name = "起势期"
        self.core_insight = "潜力大于结果"
        
        # 加载 6 个阶段
        self.stages = self.load_stages()
        
        # 心理学框架
        self.psychology = {
            'adler': '价值感驱动你在积累期继续努力',
            'jung': '潜意识在为爆发做准备',
            'freud': '延迟满足的防御机制'
        }
        
        # 爆点句
        self.viral_headlines = [
            "我最近真的很努力，但就是没结果",
            "原来问题从来不是'我不够努力'",
            "潜力很大，但结果还没跟上"
        ]
    
    def load_stages(self) -> List[Dict]:
        """加载 6 个阶段数据"""
        return [
            {'stage': 1, 'name': '初始阶段', 'desc': '刚开始不对劲'},
            {'stage': 2, 'name': '发展阶段', 'desc': '逐渐察觉问题'},
            {'stage': 3, 'name': '强化阶段', 'desc': '开始怀疑路径'},
            {'stage': 4, 'name': '转化阶段', 'desc': '尝试调整方式'},
            {'stage': 5, 'name': '整合阶段', 'desc': '逐步适应'},
            {'stage': 6, 'name': '完成阶段', 'desc': '进入新状态'}
        ]
    
    def get_interpretation(self, current_stage: int) -> Dict:
        """生成情景状态解读"""
        stage_data = self.stages[current_stage - 1]
        
        return {
            'state_name': self.state_name,
            'current_stage': stage_data,
            'core_insight': self.core_insight,
            'psychology': self.psychology,
            'action_advice': self.get_action_advice(current_stage),
            'viral_headline': self.viral_headlines[0]
        }
    
    def get_action_advice(self, current_stage: int) -> Dict:
        """生成行动建议"""
        advice_map = {
            1: {'stop': '停止急于表现', 'look': '看清积累方向', 'change': '专注单点突破'},
            2: {'stop': '停止焦虑比较', 'look': '看清进步轨迹', 'change': '记录小成就'},
            3: {'stop': '停止自我怀疑', 'look': '看清积累价值', 'change': '调整评估标准'},
            4: {'stop': '停止盲目努力', 'look': '看清突破方向', 'change': '优化努力方式'},
            5: {'stop': '停止急躁', 'look': '看清适应进度', 'change': '保持节奏'},
            6: {'stop': '停止回顾过去', 'look': '看清新状态机会', 'change': '持续深耕'}
        }
        return advice_map.get(current_stage, {})
```

---

## 🧠 今日情景 Agent 主程序

### today-stage-agent.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日情景 Agent
管理 64 个情景状态 Skills
"""

import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TodayStageAgent:
    """今日情景 Agent (总管)"""
    
    def __init__(self):
        self.state_skills = {}  # 64 个情景状态 Skills
        self.load_all_skills()
    
    def load_all_skills(self):
        """加载 64 个情景状态 Skills"""
        # 动态加载 64 个 Skills
        skills_dir = os.path.join(os.path.dirname(__file__), 'skills')
        for state_dir in os.listdir(skills_dir):
            if state_dir.startswith('state-'):
                # 加载每个 Skill
                skill = self.load_single_skill(state_dir)
                self.state_skills[state_dir] = skill
    
    def load_single_skill(self, state_dir: str):
        """加载单个情景状态 Skill"""
        # 动态导入
        skill_path = os.path.join(skills_dir, state_dir, '__init__.py')
        # ... 加载逻辑
    
    def match_state(self, user_input: str) -> Dict:
        """
        匹配情景状态
        
        Args:
            user_input: 用户输入
        
        Returns:
            匹配结果 {state_id, state_name, stage, interpretation}
        """
        # 1. 分析用户输入
        # 2. 匹配 64 个情景状态之一
        # 3. 确定当前阶段 (1-6)
        # 4. 调用对应 Skill 生成解读
        # 5. 返回完整报告
    
    def generate_report(self, state_id: int, stage: int) -> Dict:
        """生成完整解读报告"""
        skill = self.state_skills.get(f'state-{state_id:03d}-*')
        if skill:
            return skill.get_interpretation(stage)
        return {}
```

---

## 💰 变现结构

| 层级 | 内容 | 价格 |
|------|------|------|
| **免费** | 情景状态名 + 阶段 + 爆点句 | ¥0 |
| **解锁** | 完整解读 (心理学 + 建议 + 行动) | ¥1 |
| **趋势** | 7 天情景状态变化 | ¥9.9 |
| **会员** | 无限次解锁 + 深度报告 | ¥19/月 |

---

## 📈 384 种状态组合

```
64 个情景状态 × 6 个阶段 = 384 种状态组合

每个状态组合 = 独特的心理学解读 + 行动建议
```

---

## 🚀 开发优先级

### Phase 1: MVP (1-2 天)
- [ ] 创建前 10 个情景状态 Skills
- [ ] 今日情景 Agent 主程序
- [ ] 情景状态匹配算法

### Phase 2: 完整 (3-5 天)
- [ ] 创建剩余 54 个情景状态 Skills
- [ ] 智能涌现引擎
- [ ] 心理学框架集成

### Phase 3: 优化 (6-7 天)
- [ ] 爆点句生成器
- [ ] 行动建议优化
- [ ] 7 天趋势分析

---

*创建时间：2026-03-29 18:24*
*今日情景 Agent · 64 个情景状态 Skills 架构 v7.0*
