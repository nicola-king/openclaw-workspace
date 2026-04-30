# Self-Improve Module - 自我优化模块

> 版本：v1.0 | 创建：2026-04-03 22:17 | 负责 Bot：太一 / 素问

---

## 🎯 职责

**技能性能监控 + 优化建议生成**，实现持续进化

---

## 📊 监控指标

### 1️⃣ 响应时间

**采集方式**: 每次执行记录开始/结束时间

```python
# performance-monitor.py
import time
import json
from datetime import datetime

class PerformanceMonitor:
    def __init__(self, skill_name):
        self.skill_name = skill_name
        self.log_file = f"logs/{skill_name}-performance.jsonl"
    
    def record_execution(self, start_time, end_time, success=True, error=None):
        """记录执行性能"""
        duration = end_time - start_time
        
        record = {
            'timestamp': datetime.now().isoformat(),
            'skill': self.skill_name,
            'duration_ms': duration * 1000,
            'success': success,
            'error': error
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(record) + '\n')
    
    def get_stats(self, hours=24):
        """获取统计信息 (默认最近 24 小时)"""
        from datetime import datetime, timedelta
        
        cutoff = datetime.now() - timedelta(hours=hours)
        records = []
        
        with open(self.log_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                record_time = datetime.fromisoformat(record['timestamp'])
                if record_time > cutoff:
                    records.append(record)
        
        if not records:
            return None
        
        durations = [r['duration_ms'] for r in records]
        success_count = sum(1 for r in records if r['success'])
        
        return {
            'total_executions': len(records),
            'success_rate': success_count / len(records) * 100,
            'avg_duration_ms': sum(durations) / len(durations),
            'p95_duration_ms': sorted(durations)[int(len(durations) * 0.95)] if len(durations) > 20 else max(durations),
            'max_duration_ms': max(durations),
            'error_count': len(records) - success_count
        }
```

---

### 2️⃣ 错误率

**告警阈值**:
| 错误率 | 级别 | 响应 |
|--------|------|------|
| <1% | ✅ 正常 | 无需操作 |
| 1-5% | 🟡 警告 | 记录日志 |
| 5-10% | 🟠 关注 | 生成优化建议 |
| >10% | 🔴 告警 | 立即通知 |

---

### 3️⃣ 资源占用

**监控脚本**:
```python
# resource-monitor.py
import psutil
import os

def get_skill_resource_usage(skill_name):
    """获取技能资源占用"""
    # 查找相关进程
    skill_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_percent', 'cpu_percent']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if skill_name in cmdline or skill_name in proc.info['name']:
                skill_processes.append({
                    'pid': proc.info['pid'],
                    'memory_percent': proc.info['memory_percent'],
                    'cpu_percent': proc.info['cpu_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if not skill_processes:
        return None
    
    return {
        'process_count': len(skill_processes),
        'total_memory_percent': sum(p['memory_percent'] for p in skill_processes),
        'total_cpu_percent': sum(p['cpu_percent'] for p in skill_processes),
        'processes': skill_processes
    }
```

---

## 🤖 优化建议生成

```python
# optimization-suggest.py
import json

class OptimizationSuggester:
    def __init__(self, skill_name):
        self.skill_name = skill_name
        self.monitor = PerformanceMonitor(skill_name)
    
    def analyze_and_suggest(self):
        """分析性能并生成优化建议"""
        stats = self.monitor.get_stats(hours=24)
        
        if not stats:
            return []
        
        suggestions = []
        
        # 响应时间优化
        if stats['avg_duration_ms'] > 10000:  # >10 秒
            suggestions.append({
                'type': '性能优化',
                'severity': '🟡',
                'issue': f"平均响应时间 {stats['avg_duration_ms']:.0f}ms > 10s",
                'suggestion': '建议：优化算法 / 增加缓存 / 异步执行',
                'priority': '中'
            })
        
        if stats['p95_duration_ms'] > 30000:  # P95 >30 秒
            suggestions.append({
                'type': '性能优化',
                'severity': '🟠',
                'issue': f"P95 响应时间 {stats['p95_duration_ms']:.0f}ms > 30s",
                'suggestion': '建议：识别慢查询 / 增加超时控制 / 降级策略',
                'priority': '高'
            })
        
        # 错误率优化
        if stats['error_rate'] > 10:
            suggestions.append({
                'type': '稳定性优化',
                'severity': '🔴',
                'issue': f"错误率 {stats['error_rate']:.1f}% > 10%",
                'suggestion': '建议：增加重试机制 / 完善错误处理 / 根因分析',
                'priority': '紧急'
            })
        elif stats['error_rate'] > 5:
            suggestions.append({
                'type': '稳定性优化',
                'severity': '🟡',
                'issue': f"错误率 {stats['error_rate']:.1f}% > 5%",
                'suggestion': '建议：增加日志 / 监控异常模式',
                'priority': '中'
            })
        
        # 执行频率优化
        if stats['total_executions'] > 1000 and stats['avg_duration_ms'] > 1000:
            suggestions.append({
                'type': '批量优化',
                'severity': '🟡',
                'issue': f"高频调用 ({stats['total_executions']}次/天) + 响应慢",
                'suggestion': '建议：批量处理 / 结果缓存 / 限流保护',
                'priority': '中'
            })
        
        return suggestions
    
    def generate_report(self):
        """生成优化建议报告"""
        suggestions = self.analyze_and_suggest()
        
        report = f"## {self.skill_name} 性能优化建议\n\n"
        report += f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        report += f"**数据范围**: 最近 24 小时\n\n"
        
        stats = self.monitor.get_stats(hours=24)
        report += "### 性能指标\n\n"
        report += f"| 指标 | 值 |\n"
        report += f"|------|-----|\n"
        report += f"| 执行次数 | {stats['total_executions']} |\n"
        report += f"| 成功率 | {stats['success_rate']:.1f}% |\n"
        report += f"| 平均响应 | {stats['avg_duration_ms']:.0f}ms |\n"
        report += f"| P95 响应 | {stats['p95_duration_ms']:.0f}ms |\n"
        report += f"| 最大响应 | {stats['max_duration_ms']:.0f}ms |\n\n"
        
        if suggestions:
            report += "### 优化建议\n\n"
            for i, sug in enumerate(suggestions, 1):
                report += f"**{i}. {sug['type']}** {sug['severity']}\n\n"
                report += f"- **问题**: {sug['issue']}\n"
                report += f"- **建议**: {sug['suggestion']}\n"
                report += f"- **优先级**: {sug['priority']}\n\n"
        else:
            report += "### 优化建议\n\n"
            report += "✅ 性能良好，暂无优化建议\n\n"
        
        return report

if __name__ == '__main__':
    import sys
    skill_name = sys.argv[1] if len(sys.argv) > 1 else 'self-check'
    
    suggester = OptimizationSuggester(skill_name)
    report = suggester.generate_report()
    print(report)
```

---

## 📋 使用命令

```bash
# 查看性能统计
python3 modules/self-improve/performance-monitor.py <skill-name>

# 生成优化建议
python3 modules/self-improve/optimization-suggest.py <skill-name>

# 查看资源占用
python3 modules/self-improve/resource-monitor.py <skill-name>
```

---

## 📊 输出格式

```markdown
## self-check 性能优化建议

**分析时间**: 2026-04-03 22:30
**数据范围**: 最近 24 小时

### 性能指标
| 指标 | 值 |
|------|-----|
| 执行次数 | 24 |
| 成功率 | 100% |
| 平均响应 | 2500ms |
| P95 响应 | 5000ms |
| 最大响应 | 15000ms |

### 优化建议

**1. 性能优化** 🟡

- **问题**: Gateway 重启时响应时间 >15s
- **建议**: 优化重启逻辑，使用并行启动
- **优先级**: 中

**2. 批量优化** 🟡

- **问题**: 每小时执行 + 响应>2s
- **建议**: 增加结果缓存，避免重复检查
- **优先级**: 中

### 下一步
- [ ] 实施优化建议
- [ ] 一周后重新评估
- [ ] 更新性能基线
```

---

## 🔄 持续改进循环

```
性能监控 (实时)
    ↓
数据分析 (每日)
    ↓
优化建议生成 (自动)
    ↓
人工审核/自动实施
    ↓
效果验证 (一周后)
    ↓
更新基线/继续优化
```

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `modules/self-improve/SKILL.md` | 本文档 |
| `modules/self-improve/performance-monitor.py` | 性能监控脚本 |
| `modules/self-improve/optimization-suggest.py` | 优化建议生成 |
| `modules/self-improve/resource-monitor.py` | 资源监控脚本 |

---

*创建：2026-04-03 22:17 | 太一 AGI · 持续进化*
