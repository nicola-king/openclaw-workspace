# 今日情景 Agent · 完整架构 v9.0

> 创建时间：2026-03-29 19:41
> 核心：64 个情景状态 × 6 个阶段 = 384 个独立 Skills
> 定位：心理认知工具 / 情境映射 / 认知辅助

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                  今日情景 Agent (总管)                    │
│  今日情景 = 64 个情景状态 × 6 个阶段 = 384 种状态组合        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  输入：用户状态描述/困惑/问题                            │
│   ↓                                                     │
│  情景状态匹配算法 (Stage Matcher)                        │
│   ↓                                                     │
│  动态加载对应 Skill (State XXX Stage XX Skill)           │
│   ↓                                                     │
│  生成完整解读报告                                        │
│   ↓                                                     │
│  输出：核心洞察 + 心理学框架 + 行动建议 + 爆点句          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 完整文件结构

```
skills/today-stage/
├── ARCHITECTURE-V9.md              # 本文档
├── 384-SKILLS-ARCHITECTURE.md      # 384 Skills 架构
├│
├── agent/                          # Agent 主程序
│   ├── today-stage-agent.py        # 今日情景 Agent (总管)
│   ├── emergence-engine.py         # 智能涌现引擎
│   └── stage-matcher.py            # 情景状态匹配算法
│
├── skills/                         # 384 个阶段 Skills
│   ├── state-001-qishi/            # 状态 001: 起势期
│   │   ├── stage-01.py             # 阶段 1: 初始阶段
│   │   ├── stage-02.py             # 阶段 2: 发展阶段
│   │   ├── stage-03.py             # 阶段 3: 强化阶段
│   │   ├── stage-04.py             # 阶段 4: 转化阶段
│   │   ├── stage-05.py             # 阶段 5: 整合阶段
│   │   └── stage-06.py             # 阶段 6: 完成阶段
│   │
│   ├── state-002-chengzai/         # 状态 002: 承载期
│   │   └── stage-01.py ~ stage-06.py
│   │
│   └── ... (共 64 个状态目录，384 个阶段 Skills)
│
├── helpers/                        # 辅助工具
│   ├── psychology-framework.py     # 心理学框架
│   ├── action-advisor.py           # 行动建议生成器
│   └── viral-headlines.py          # 爆点句生成器
│
├── data/                           # 数据文件
│   ├── stages-64-final.json        # 64 个情景状态数据
│   ├── stages-384-mapping.json     # 384 状态映射
│   └── design-decision-v9.json     # 设计决策文档
│
└── scripts/                        # 工具脚本
    ├── create-all-384-skills.py    # 批量创建脚本
    └── test-all-skills.py          # 测试脚本
```

---

## 🎯 64 个情景状态列表

### State 001-010

| 编号 | 状态名 | 核心洞察 | 阶段数 |
|------|--------|---------|--------|
| 001 | 起势期 | 潜力大于结果 | 6 |
| 002 | 承载期 | 责任增加主动权低 | 6 |
| 003 | 启动混乱期 | 刚开始不顺 | 6 |
| 004 | 认知盲区期 | 理解有偏差 | 6 |
| 005 | 等待窗口期 | 准备好未启动 | 6 |
| 006 | 冲突边缘期 | 即将产生对抗 | 6 |
| 007 | 结构协同期 | 需要协作 | 6 |
| 008 | 资源整合期 | 寻找合作 | 6 |
| 009 | 小幅增长期 | 进步缓慢 | 6 |
| 010 | 规则适应期 | 环境有要求 | 6 |

### State 011-020

| 编号 | 状态名 | 核心洞察 |
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

| 编号 | 状态名 | 核心洞察 |
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

| 编号 | 状态名 | 核心洞察 |
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

| 编号 | 状态名 | 核心洞察 |
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

| 编号 | 状态名 | 核心洞察 |
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

| 编号 | 状态名 | 核心洞察 |
|------|--------|---------|
| 061 | 内在确认期 | 需要确认 |
| 062 | 细节处理期 | 细节重要 |
| 063 | 完成临界期 | 接近完成 |
| 064 | 未完成期 | 尚未完成 |

---

## 🔧 单个 Skill 结构

### 标准模板

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情景状态 Skill XXX-XX
状态：[状态名] - 阶段 X: [阶段名]
"""

class StateXXXStageXXSkill:
    """[状态名] - [阶段名] Skill"""
    
    def __init__(self):
        self.state_id = XXX
        self.state_name = "[状态名]"
        self.stage_id = XX
        self.stage_name = "[阶段名]"
        self.core_insight = "[核心洞察]"
        self.description = "[阶段描述]"
        
        # 心理学框架
        self.psychology = {
            'adler': '[阿德勒解读]',
            'jung': '[荣格解读]',
            'freud': '[弗洛伊德解读]'
        }
        
        # 爆点句
        self.viral_headlines = [
            "[爆点句 1]",
            "[爆点句 2]",
            "[爆点句 3]"
        ]
    
    def get_interpretation(self) -> dict:
        """获取完整解读"""
        return {
            'state': self.state_name,
            'stage': self.stage_name,
            'insight': self.core_insight,
            'description': self.description,
            'psychology': self.psychology,
            'viral_headline': self.viral_headlines[0],
            'action_advice': {
                'stop': '停止...',
                'look': '看清...',
                'change': '换...'
            }
        }
```

---

## 🧠 今日情景 Agent 主程序

### today-stage-agent.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日情景 Agent
管理 384 个阶段 Skills (64 状态 × 6 阶段)
"""

import os
import sys
import importlib.util
from typing import Dict, List, Optional

class TodayStageAgent:
    """今日情景 Agent (总管)"""
    
    def __init__(self):
        self.skills_cache = {}  # 缓存已加载的 Skills
        self.skills_dir = os.path.join(os.path.dirname(__file__), 'skills')
    
    def load_skill(self, state_id: int, stage_id: int):
        """动态加载指定状态和阶段的 Skill"""
        cache_key = f"{state_id}-{stage_id}"
        
        # 检查缓存
        if cache_key in self.skills_cache:
            return self.skills_cache[cache_key]
        
        # 构建文件路径
        state_dir = self._get_state_dir(state_id)
        skill_file = os.path.join(state_dir, f"stage-{stage_id:02d}.py")
        
        if not os.path.exists(skill_file):
            return None
        
        # 动态导入
        spec = importlib.util.spec_from_file_location(
            f"state_{state_id}_stage_{stage_id}",
            skill_file
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 获取 Skill 类
        class_name = f"State{state_id:03d}Stage{stage_id:02d}Skill"
        skill_class = getattr(module, class_name)
        skill = skill_class()
        
        # 缓存
        self.skills_cache[cache_key] = skill
        return skill
    
    def _get_state_dir(self, state_id: int) -> str:
        """获取状态目录"""
        # 需要状态名映射表
        state_names = {
            1: 'qishi', 2: 'chengzai', 3: 'hunduan',
            # ... 64 个状态拼音
        }
        pinyin = state_names.get(state_id, f"state{state_id}")
        return os.path.join(self.skills_dir, f"state-{state_id:03d}-{pinyin}")
    
    def match_state(self, user_input: str) -> Dict:
        """
        匹配情景状态
        
        Args:
            user_input: 用户输入
        
        Returns:
            匹配结果 {state_id, stage_id, interpretation}
        """
        # 简单关键词匹配 (实际应该用更复杂的算法)
        keyword_map = {
            '努力没结果': (1, 3),  # 起势期 - 强化阶段
            '累': (28, 2),  # 压力过载期 - 发展阶段
            '方向错': (2, 3),  # 承载期 - 强化阶段
            '混乱': (3, 1),  # 启动混乱期 - 初始阶段
        }
        
        for keyword, (state_id, stage_id) in keyword_map.items():
            if keyword in user_input:
                return self.generate_report(state_id, stage_id)
        
        # 默认返回
        return self.generate_report(1, 1)
    
    def generate_report(self, state_id: int, stage_id: int) -> Dict:
        """生成完整解读报告"""
        skill = self.load_skill(state_id, stage_id)
        if not skill:
            return {'error': 'Skill not found'}
        
        return skill.get_interpretation()


def main():
    """测试"""
    agent = TodayStageAgent()
    
    # 测试输入
    test_inputs = [
        "我最近真的很努力，但就是没结果",
        "我一直在努力，但越来越累",
        "感觉方向有问题"
    ]
    
    for user_input in test_inputs:
        print(f"\n用户输入：{user_input}")
        report = agent.match_state(user_input)
        print(f"状态：{report.get('state')}")
        print(f"阶段：{report.get('stage')}")
        print(f"洞察：{report.get('insight')}")
        print(f"爆点句：{report.get('viral_headline')}")


if __name__ == '__main__':
    main()
```

---

## 💰 变现结构

| 层级 | 内容 | 价格 | 说明 |
|------|------|------|------|
| **免费** | 状态名 + 阶段 + 爆点句 | ¥0 | 引流 |
| **解锁** | 完整解读 (心理学 + 建议 + 行动) | ¥1 | 主力 |
| **趋势** | 7 天状态变化分析 | ¥9.9 | 增值 |
| **会员** | 无限次解锁 + 深度报告 | ¥19/月 | 忠诚 |

---

## 📈 转化漏斗

```
曝光 (10 万)
  ↓ 15% 点击
点击 (1.5 万)
  ↓ 50% 测试完成
测试完成 (7500)
  ↓ 3% 付费
1 元解锁 (225) → ¥225
  ↓ 15% 升级
7 天趋势 (34) → ¥336
  ↓ 10% 会员
会员 (3) → ¥57/月

首周收入：¥618+
```

---

## 🎨 用户界面流程

```
首页
  ↓
输入困惑 / 随机抽取
  ↓
测试页 (分析中...)
  ↓
结果页 (免费：状态名 + 阶段 + 爆点句)
  ↓ [解锁按钮 ¥1]
解锁页 (付费：完整解读)
  ↓ [趋势按钮 ¥9.9]
趋势页 (7 天变化)
  ↓ [会员按钮 ¥19/月]
会员页 (无限次)
```

---

## ⚠️ 合规设计

### 术语对照表

| 易经原词 | v9.0 合规表述 |
|---------|------------|
| 64 卦 | **64 个情景状态** |
| 卦名 | **状态名** (如"路径错配期") |
| 爻 | **阶段** (6 个) |
| 初爻/二爻... | **阶段 1/2/3/4/5/6** |
| 卦辞 | **核心洞察** |
| 爻辞 | **阶段描述** |
| 太极 | **无限♾️** |
| 卦象 | **移除** |

### 监管语言

| 内部概念 | 对外表述 |
|---------|---------|
| 64 卦 | 64 个情景状态 |
| 占卜 | 心理认知工具 |
| 算命 | 情境映射 |
| 起卦 | 随机抽取 |

---

## 🚀 部署流程

### 1. 本地测试

```bash
cd /home/nicola/.openclaw/workspace/skills/today-stage
python3 agent/today-stage-agent.py
```

### 2. 小程序集成

```javascript
// 小程序调用
wx.request({
  url: 'https://api.example.com/today-stage/match',
  data: { input: userInput },
  success: (res) => {
    const report = res.data
    // 显示结果
  }
})
```

### 3. API 部署

```python
# FastAPI 示例
from fastapi import FastAPI
app = FastAPI()
agent = TodayStageAgent()

@app.post("/match")
async def match_state(input: str):
    return agent.match_state(input)
```

---

## 📊 核心指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| **Skills 总数** | 384 | 64 状态 × 6 阶段 |
| **匹配准确率** | >70% | 用户认可匹配结果 |
| **付费转化率** | >3% | 免费→付费 |
| **复购率** | >40% | 二次测试付费 |
| **分享率** | >5% | 卡片截图分享 |

---

## 📁 文件统计

| 类别 | 文件数 | 大小 |
|------|--------|------|
| **Agent 主程序** | 3 | ~10KB |
| **384 Skills** | 384 | ~600KB |
| **辅助工具** | 3 | ~10KB |
| **数据文件** | 3 | ~50KB |
| **脚本** | 2 | ~10KB |
| **文档** | 2 | ~20KB |
| **总计** | **397** | **~700KB** |

---

*创建时间：2026-03-29 19:41*
*今日情景 Agent · 完整架构 v9.0*
