# 今日情景 Agent 架构

> 创建时间：2026-03-29 16:36
> 原名：易经 Agent
> 核心：64 个情景状态 × 384 种演进 = 情绪识别 + 决策映射

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────┐
│          今日情景 Agent                  │
│   "看清你正在经历什么"                   │
├─────────────────────────────────────────┤
│                                         │
│  输入：用户状态描述/测试答案             │
│   ↓                                     │
│  情景匹配算法                            │
│   ↓                                     │
│  加载情景 Skill (64 个之一)               │
│   ↓                                     │
│  加载演进步骤 (384 种之一)                │
│   ↓                                     │
│  应用心理学框架                          │
│   ↓                                     │
│  输出：核心洞察 + 行动建议               │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📊 64 个情景状态 Skills

### 情景状态分类 (4 大类型)

| 类型 | 数量 | 特征 | 代表情景 |
|------|------|------|---------|
| **调整型** | 16 个 | 需要内部重构 | 积累未显期/路径错配期 |
| **过渡型** | 16 个 | 耐心等待 | 时机未到期/慢速积累期 |
| **观察型** | 16 个 | 收集信息 | 机会临界期/观察判断期 |
| **决策型** | 16 个 | 果断行动 | 突破决策期/强制决策期 |

---

## 📁 文件结构 (去易经化)

```
skills/today-stage/
├── agent/
│   ├── today-stage-agent.py      # 今日情景 Agent 主程序
│   ├── emergence-engine.py       # 智能涌现引擎
│   └── stage-matcher.py          # 情景匹配算法
│
├── skills/
│   ├── stage-001-accumulation/   # 情景 001: 积累未显期
│   │   ├── __init__.py           # 情景主模块
│   │   ├── step-01.py            # Step 1: 刚开始不对劲
│   │   ├── step-02.py            # Step 2: 逐渐察觉问题
│   │   ├── step-03.py            # Step 3: 开始怀疑路径
│   │   ├── step-04.py            # Step 4: 尝试调整方式
│   │   ├── step-05.py            # Step 5: 逐步适应
│   │   ├── step-06.py            # Step 6: 进入新状态
│   │   └── stage-data.json       # 情景完整数据
│   │
│   ├── stage-002-path-mismatch/  # 情景 002: 路径错配期
│   ├── stage-003-timing/         # 情景 003: 时机未到期
│   └── ... (共 64 个情景 Skills)
│
├── helpers/
│   ├── psychology-framework.py   # 心理学框架 (阿德勒/荣格/弗洛伊德)
│   ├── action-advisor.py         # 行动建议生成器
│   └── viral-headlines.py        # 爆点句生成器
│
└── data/
    ├── stages-64.json            # 64 情景完整数据
    ├── steps-384.json            # 384 演进步骤数据
    └── headlines-viral.json      # 爆点句库
```

---

## 🔧 情景 Skill 结构示例

### stage-002-path-mismatch/__init__.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情景 Skill 002 - 路径错配期
6 步演进 × 心理学框架 × 行动建议
"""

import json
import os
from typing import Dict, List

class PathMismatchStage:
    """路径错配期情景 Skill"""
    
    def __init__(self):
        self.stage_id = 2
        self.stage_name = "路径错配期"
        self.stage_type = "调整型"
        self.core_insight = "你不是不够努力，只是方向一开始就不对"
        
        # 加载 6 步演进数据
        self.steps = self.load_steps()
        
        # 心理学框架
        self.psychology = {
            'adler': '价值感驱动你在错误路径上继续努力',
            'jung': '潜意识路径在影响你的选择',
            'freud': '防御机制在维持当前模式'
        }
        
        # 爆点句
        self.viral_headlines = [
            "突然意识到，我可能一开始就走错了",
            "我好像一直在用错误的方式努力",
            "原来问题从来不是'我不够努力'"
        ]
    
    def load_steps(self) -> List[Dict]:
        """加载 6 步演进数据"""
        return [
            {'step': 1, 'name': '努力没有回报', 'desc': '投入很多，但没有回报'},
            {'step': 2, 'name': '加大投入无效', 'desc': '更加努力，但依然无效'},
            {'step': 3, 'name': '产生焦虑', 'desc': '开始焦虑和自我怀疑'},
            {'step': 4, 'name': '意识方向问题', 'desc': '意识到可能是方向问题'},
            {'step': 5, 'name': '尝试切换', 'desc': '开始尝试新方向'},
            {'step': 6, 'name': '找到新路径', 'desc': '找到真正匹配的路径'}
        ]
    
    def get_interpretation(self, current_step: int) -> Dict:
        """
        生成情景解读
        
        Args:
            current_step: 当前步骤 (1-6)
        
        Returns:
            完整解读报告
        """
        step_data = self.steps[current_step - 1]
        
        return {
            'stage_name': self.stage_name,
            'stage_type': self.stage_type,
            'current_step': step_data,
            'core_insight': self.core_insight,
            'psychology': self.psychology,
            'action_advice': self.get_action_advice(current_step),
            'viral_headline': self.viral_headlines[0]
        }
    
    def get_action_advice(self, current_step: int) -> Dict:
        """生成行动建议"""
        advice_map = {
            1: {'stop': '停止加大无效投入', 'look': '看清路径是否匹配', 'change': '尝试切换方向'},
            2: {'stop': '停止自我怀疑', 'look': '看清自己的优势', 'change': '换一种评估方式'},
            3: {'stop': '停止焦虑', 'look': '看清焦虑来源', 'change': '换个环境放松'},
            4: {'stop': '停止旧路径', 'look': '看清真正适合的方向', 'change': '尝试新领域'},
            5: {'stop': '停止犹豫', 'look': '看清新路径的反馈', 'change': '坚定执行'},
            6: {'stop': '停止回顾过去', 'look': '看清新路径的机会', 'change': '持续深耕'}
        }
        return advice_map.get(current_step, {})


def main():
    """测试"""
    stage = PathMismatchStage()
    result = stage.get_interpretation(current_step=3)
    
    print(f"情景：{result['stage_name']}")
    print(f"类型：{result['stage_type']}")
    print(f"当前步骤：{result['current_step']['name']}")
    print(f"核心洞察：{result['core_insight']}")
    print(f"爆点句：{result['viral_headline']}")
    print(f"行动建议：{result['action_advice']}")


if __name__ == '__main__':
    main()
```

---

## 🧠 情景匹配算法

### stage-matcher.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情景匹配算法
功能：根据用户输入匹配最符合的情景状态
"""

from typing import Dict, List, Tuple

class StageMatcher:
    """情景匹配器"""
    
    def __init__(self):
        # 关键词 → 情景映射
        self.keyword_map = {
            '努力没结果': 1,  # 积累未显期
            '走错方向': 2,     # 路径错配期
            '时机未到': 3,     # 时机未到期
            '理解偏差': 4,     # 认知偏差期
            '混乱': 5,         # 启动混乱期
            '累/疲惫': 6,      # 过载停滞期
            '关系摩擦': 7,     # 关系阻力期
            '波动/不稳': 8,    # 上升不稳期
        }
        
        # 情绪 → 情景类型映射
        self.emotion_map = {
            '焦虑': '观察型',
            '疲惫': '过渡型',
            '困惑': '调整型',
            '犹豫': '决策型'
        }
    
    def match(self, user_input: str) -> Dict:
        """
        匹配情景
        
        Args:
            user_input: 用户输入 (测试答案/状态描述)
        
        Returns:
            匹配结果 {stage_id, stage_name, confidence, step}
        """
        # Step 1: 关键词匹配
        stage_scores = self.match_keywords(user_input)
        
        # Step 2: 情绪分析
        emotion_type = self.analyze_emotion(user_input)
        
        # Step 3: 综合评分
        best_stage = self.calculate_best_stage(stage_scores, emotion_type)
        
        # Step 4: 计算演进步骤
        step = self.calculate_step(user_input, best_stage)
        
        return {
            'stage_id': best_stage['id'],
            'stage_name': best_stage['name'],
            'stage_type': best_stage['type'],
            'step': step,
            'confidence': best_stage['confidence'],
            'core_insight': best_stage['insight']
        }
    
    def match_keywords(self, text: str) -> Dict[int, float]:
        """关键词匹配"""
        scores = {}
        for keyword, stage_id in self.keyword_map.items():
            if keyword in text:
                scores[stage_id] = scores.get(stage_id, 0) + 1.0
        return scores
    
    def analyze_emotion(self, text: str) -> str:
        """情绪分析"""
        for emotion in self.emotion_map:
            if emotion in text:
                return self.emotion_map[emotion]
        return '调整型'  # 默认
    
    def calculate_best_stage(self, scores: Dict, emotion: str) -> Dict:
        """计算最佳情景"""
        if not scores:
            return {'id': 2, 'name': '路径错配期', 'type': '调整型', 'confidence': 0.5, 'insight': '你不是不够努力，只是方向一开始就不对'}
        
        best_id = max(scores, key=scores.get)
        # 返回情景信息 (简化版)
        return {'id': best_id, 'name': f'情景{best_id}', 'type': emotion, 'confidence': scores[best_id], 'insight': '...'}
    
    def calculate_step(self, text: str, stage: Dict) -> int:
        """计算演进步骤"""
        # 简化版：根据文本长度/情绪强度估算
        if '刚开始' in text or '最近' in text:
            return 1
        elif '逐渐' in text or '开始' in text:
            return 2
        elif '焦虑' in text or '怀疑' in text:
            return 3
        elif '尝试' in text or '调整' in text:
            return 4
        elif '适应' in text or '稳定' in text:
            return 5
        else:
            return 6
```

---

## 📱 用户交互流程

```
用户进入
  ↓
选择测试类型
  - 快速测试 (3 题/30 秒)
  - 标准测试 (12 题/2 分钟)
  - 深度测试 (36 题/5 分钟)
  ↓
答题
  ↓
情景匹配算法
  ↓
加载情景 Skill
  ↓
生成解读报告
  ↓
输出:
- 情景名称
- 当前步骤
- 核心洞察 (爆点句)
- 心理学解读
- 行动建议 (停看换)
- 今日行动清单
  ↓
付费解锁完整解读 (¥1)
```

---

## 💰 变现设计

| 层级 | 内容 | 价格 |
|------|------|------|
| **免费** | 情景名称 + 步骤 + 爆点句 | ¥0 |
| **解锁** | 完整解读 + 心理学分析 + 行动建议 | ¥1 |
| **会员** | 无限解锁 + 情景轨迹 + 深度报告 | ¥19/月 |
| **咨询** | 1v1 情景解读 + 定制建议 | ¥99/次 |

---

## 📊 数据追踪

### 核心指标

| 指标 | 目标 | 说明 |
|------|------|------|
| **测试完成率** | >80% | 用户完成测试比例 |
| **情景匹配准确率** | >70% | 用户认可匹配结果 |
| **付费转化率** | >3% | 免费→付费 |
| **复购率** | >40% | 二次测试付费 |
| **分享率** | >5% | 卡片截图分享 |

---

## 🚀 上线计划

| 时间 | 里程碑 | 目标 |
|------|--------|------|
| **Week 1** | 64 情景 Skills 创建 | 完成核心内容 |
| **Week 2** | Agent 开发 + 测试 | 功能完整 |
| **Week 3** | 小程序上线 | 提交审核 |
| **Week 4** | 引爆内容矩阵 | 1000 种子用户 |

---

*创建时间：2026-03-29 16:36*
*太一 AGI · 今日情景 Agent 架构*
