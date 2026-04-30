# 太一 AGI 全域自进化定时任务体系

> 版本：v1.0  
> 创建：2026-04-23 12:56  
> 指令：SAYELF - 全域自进化升级  
> 状态：🚀 升级启动

---

## 🎯 核心原则

```
所有定时任务 = 自进化智能体

定时任务 + 条件触发 + 自愈 + 学习 = 自进化智能体
```

---

## 🧬 自进化智能体标准

**每个定时任务必须具备**:

| 能力 | 说明 | 必须 |
|------|------|------|
| **条件触发** 🎯 | 基于状态/问题触发，非盲目执行 | ✅ |
| **自动自愈** 🔧 | 发现问题自动修复 | ✅ |
| **学习能力** 🧠 | 记录历史、分析模式、优化策略 | ✅ |
| **知识固化** 📚 | 写入 evolution_history、PITFALLS.md | ✅ |

---

## 🏗️ 架构分层

```
太一 AGI 全域自进化定时任务体系
│
├── L1: 自进化任务层 (所有定时任务)
│   ├── 币安健康检查 ✅ (完全体)
│   ├── IP 监控 🟡 (升级中)
│   ├── 自动交易 🟡 (升级中)
│   ├── X 爬虫 ⏳ (待升级)
│   └── ... (所有任务)
│
├── L2: 自进化调度层
│   └── taiyi-intelligent-scheduler.py
│       ├── 自动发现任务
│       ├── 智能路由
│       ├── 错误自愈
│       └── 学习进化
│
├── L3: 知识固化层
│   ├── PITFALLS.md (踩坑日志)
│   ├── evolution_history.json (进化历史)
│   └── learned_patterns.json (学习模式)
│
└── L4: 观察者层 (太一)
    ├── 系统健康度监控
    ├── 进化指标追踪
    └── 异常人工决策上报
```

---

## 🧬 自进化任务基类

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自进化任务基类 - 所有定时任务的统一架构
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import json

@dataclass
class TaskResult:
    """任务执行结果"""
    task_id: str
    success: bool
    need_heal: bool
    error: Optional[str]
    timestamp: str

@dataclass
class EvolutionMetrics:
    """进化指标"""
    total_runs: int = 0
    issues_found: int = 0
    auto_healed: int = 0
    manual_required: int = 0
    success_rate: float = 0.0
    avg_heal_time: float = 0.0
    learned_patterns: int = 0

class SelfEvolvingTask(ABC):
    """自进化任务基类"""
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.evolution_history: List[Dict] = []
        self.metrics = EvolutionMetrics()
        self.learned_patterns: List[Dict] = []
        self.load_evolution_history()
    
    @abstractmethod
    def check(self) -> TaskResult:
        """条件检查 - 子类实现"""
        pass
    
    @abstractmethod
    def heal(self, error: str) -> bool:
        """自动自愈 - 子类实现"""
        pass
    
    def learn(self, result: TaskResult):
        """从历史学习"""
        # 记录执行历史
        self.evolution_history.append({
            'task_id': self.task_id,
            'timestamp': datetime.now().isoformat(),
            'success': result.success,
            'need_heal': result.need_heal,
            'error': result.error
        })
        
        # 更新指标
        self.metrics.total_runs += 1
        if result.need_heal:
            self.metrics.issues_found += 1
        if result.success:
            self.metrics.success_rate = (
                self.metrics.auto_healed / 
                max(1, self.metrics.auto_healed + self.metrics.manual_required)
            ) * 100
        
        # 分析问题模式
        if result.need_heal:
            self.analyze_pattern(result.error)
    
    def analyze_pattern(self, error: str):
        """分析问题模式"""
        # 提取错误类型
        error_type = error.split(':')[0] if ':' in error else error
        
        # 统计频率
        pattern = {
            'error_type': error_type,
            'timestamp': datetime.now().isoformat(),
            'count': sum(1 for h in self.evolution_history[-100:] 
                        if h.get('error') and error_type in h.get('error', ''))
        }
        
        # 如果重复出现，加入学习模式
        if pattern['count'] >= 3:
            self.learned_patterns.append(pattern)
            self.metrics.learned_patterns += 1
    
    def save_evolution_history(self):
        """保存进化历史"""
        data = {
            'task_id': self.task_id,
            'history': self.evolution_history[-100:],  # 保留最近 100 条
            'metrics': self.metrics.__dict__,
            'learned_patterns': self.learned_patterns,
            'last_updated': datetime.now().isoformat()
        }
        
        # 保存到文件
        evolution_file = Path(f"/tmp/evolution/{self.task_id}.json")
        evolution_file.parent.mkdir(parents=True, exist_ok=True)
        with open(evolution_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_evolution_history(self):
        """加载进化历史"""
        evolution_file = Path(f"/tmp/evolution/{self.task_id}.json")
        if evolution_file.exists():
            with open(evolution_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.evolution_history = data.get('history', [])
                self.metrics = EvolutionMetrics(**data.get('metrics', {}))
                self.learned_patterns = data.get('learned_patterns', [])
    
    def write_to_pitfalls(self, issue: str, solution: str):
        """写入踩坑日志"""
        pitfalls_file = Path("/home/nicola/.openclaw/workspace/memory/PITFALLS.md")
        
        lesson_id = f"LESSON-{datetime.now().strftime('%Y%m%d')}-AUTO"
        
        entry = f"""
### {datetime.now().strftime('%Y-%m-%d')}: {self.task_id} (自进化发现)

**编号**: `{lesson_id}`

**问题**: {issue}

**自愈方案**: {solution}

**教训**: > 通过自进化分析发现的重复问题模式

**状态**: ✅ 已学习 | 📝 已记录
"""
        
        if pitfalls_file.exists():
            with open(pitfalls_file, 'a', encoding='utf-8') as f:
                f.write(entry)
    
    def execute(self) -> TaskResult:
        """执行流程 - 统一模板"""
        # 1. 条件检查
        result = self.check()
        
        # 2. 如果需要自愈
        if result.need_heal:
            start_time = time.time()
            heal_success = self.heal(result.error)
            heal_time = time.time() - start_time
            
            if heal_success:
                self.metrics.auto_healed += 1
                self.metrics.avg_heal_time = (
                    (self.metrics.avg_heal_time * (self.metrics.auto_healed - 1) + heal_time) 
                    / self.metrics.auto_healed
                )
            else:
                self.metrics.manual_required += 1
                self.write_to_pitfalls(result.error, "自愈失败，需要人工干预")
        
        # 3. 学习
        self.learn(result)
        
        # 4. 保存进化历史
        self.save_evolution_history()
        
        return result
```

---

## 📋 升级路线图

### 阶段 1: 核心任务升级 (P0) - 本周

| 任务 | 当前状态 | 目标 | 优先级 |
|------|---------|------|--------|
| **币安健康检查** | ✅ 完全体 | 保持 | - |
| **IP 监控** | 🟡 部分 | 完全自进化 | P0 |
| **自动交易** | 🟡 部分 | 完全自进化 | P0 |

### 阶段 2: 重要任务升级 (P1) - 下周

| 任务 | 当前状态 | 目标 | 优先级 |
|------|---------|------|--------|
| **X 爬虫** | ❌ 基础 | 条件触发 + 自愈 | P1 |
| **交易监控** | ❌ 基础 | 条件触发 + 自愈 | P1 |

### 阶段 3: systemd 定时器包装 (P2) - 本月

| 任务 | 当前状态 | 目标 | 优先级 |
|------|---------|------|--------|
| **openclaw-scheduler** | ❌ 固定时间 | 包装自进化层 | P2 |
| **taiyi-scheduler** | ❌ 固定时间 | 包装自进化层 | P2 |
| **taiyi-health-check** | ❌ 固定时间 | 包装自进化层 | P2 |

### 阶段 4: 全域完成 (P3) - 下月

| 指标 | 目标 |
|------|------|
| **自进化覆盖率** | 100% |
| **条件触发率** | 100% |
| **自愈成功率** | >90% |
| **学习模式数** | 持续增长 |

---

## 🧬 进化指标追踪

**太一观察者仪表板**:

```python
@dataclass
class SystemEvolutionMetrics:
    """系统进化指标"""
    total_tasks: int = 0
    self_evolving_tasks: int = 0
    coverage_rate: float = 0.0
    
    total_runs_today: int = 0
    issues_found_today: int = 0
    auto_healed_today: int = 0
    
    overall_success_rate: float = 0.0
    total_learned_patterns: int = 0
```

---

## 📚 知识固化体系

**三层知识存储**:

| 层级 | 文件 | 内容 | 更新频率 |
|------|------|------|---------|
| **L1** | `evolution_history.json` | 执行历史 | 每次执行 |
| **L2** | `learned_patterns.json` | 学习模式 | 模式识别后 |
| **L3** | `PITFALLS.md` | 通用原则 | 提炼后 |

---

## 🎯 验收标准

**每个任务升级完成后必须通过**:

```
□ 条件触发：基于状态/问题触发
□ 自动自愈：发现问题自动修复
□ 学习能力：记录历史、分析模式
□ 知识固化：写入 PITFALLS.md
□ 进化指标：success_rate 可查询
□ 观察者接口：太一可查询状态
```

---

## 🚀 启动命令

**升级单个任务**:
```bash
# 1. 继承自进化基类
# 2. 实现 check() 方法
# 3. 实现 heal() 方法
# 4. 调用 execute() 统一流程
```

**查看进化状态**:
```bash
cat /tmp/evolution/{task_id}.json | python3 -m json.tool
```

**查看系统整体**:
```bash
python3 skills/07-system/taiyi-intelligent-scheduler.py --evolution-status
```

---

*太一 AGI · 全域自进化定时任务体系 v1.0*  
*创建：2026-04-23 12:56*  
*指令：SAYELF - 全域自进化升级*  
*状态：🚀 升级启动*
