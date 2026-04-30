#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自进化任务基类 - 所有定时任务的统一架构

版本：v1.0
创建：2026-04-23
指令：SAYELF - 全域自进化升级
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import time

@dataclass
class TaskResult:
    """任务执行结果"""
    task_id: str
    success: bool
    need_heal: bool
    error: Optional[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

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
            'history': self.evolution_history[-100:],
            'metrics': self.metrics.__dict__,
            'learned_patterns': self.learned_patterns,
            'last_updated': datetime.now().isoformat()
        }
        
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
    
    def get_status(self) -> Dict:
        """获取任务状态"""
        return {
            'task_id': self.task_id,
            'metrics': self.metrics.__dict__,
            'learned_patterns_count': len(self.learned_patterns),
            'last_run': self.evolution_history[-1]['timestamp'] if self.evolution_history else None
        }
