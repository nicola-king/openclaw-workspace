# 🚀 太一全量智能自动化调用指南

> **创建时间**: 2026-04-14 15:38  
> **状态**: ✅ 已完成  
> **功能**: 全量智能自动化调用所有 Scripts/Skills

---

## 🚀 快速开始

### 方法 1: 命令行执行

```bash
# 执行所有 Scripts 和 Skills
python3 /home/nicola/.openclaw/workspace/scripts/full-auto-executor.py
```

### 方法 2: Python 调用

```python
from scripts.full-auto-executor import TaiyiFullAutoExecutor

executor = TaiyiFullAutoExecutor(
    max_retries=2,
    timeout_seconds=300
)

# 执行所有
executor.execute_all(
    include_scripts=True,
    include_skills=True
)

# 生成报告
report_path = executor.generate_report()

# 保存 JSON 日志
json_path = executor.save_json_log()
```

### 方法 3: 智能调度中心

```python
from skills.07-system.taiyi-intelligent-scheduler import TaiyiIntelligentScheduler

scheduler = TaiyiIntelligentScheduler()

# 批量执行
tasks = [
    {"name": "token-optimization-analysis"},
    {"name": "memory-compression-algorithm"},
    {"name": "skill-confidence-evaluator"},
    # ... 更多任务
]

results = scheduler.batch_execute(tasks)
```

---

## 📋 配置选项

### TaiyiFullAutoExecutor

```python
executor = TaiyiFullAutoExecutor(
    max_retries=2,          # 最大重试次数
    timeout_seconds=300     # 超时时间 (秒)
)
```

### execute_all()

```python
executor.execute_all(
    include_scripts=True,   # 是否执行 Scripts
    include_skills=True     # 是否执行 Skills
)
```

---

## 📊 执行结果

### 输出文件

**报告**: `reports/full-auto-execution_report_YYYYMMDD_HHMMSS.md`

**日志**: `logs/full-auto-execution_YYYYMMDD_HHMMSS.json`

### 报告内容

```markdown
# 太一全量智能自动化调用报告

## 执行汇总
- 总任务：X 个
- 成功：Y 个 (Z%)
- 失败：W 个
- 总耗时：X 秒

## 按类型统计
- Scripts: X 个
- Skills: Y 个

## 失败任务详情
| 名称 | 类型 | 错误信息 | 重试次数 |
|------|------|---------|---------|

## 成功任务列表
- ✅ task1 (script, 0.03s)
- ✅ task2 (skill, 0.11s)
...
```

---

## 🔧 高级用法

### 只执行 Scripts

```python
executor.execute_all(
    include_scripts=True,
    include_skills=False
)
```

### 只执行 Skills

```python
executor.execute_all(
    include_scripts=False,
    include_skills=True
)
```

### 自定义超时

```python
executor = TaiyiFullAutoExecutor(
    max_retries=3,
    timeout_seconds=600  # 10 分钟
)
```

---

## 📈 性能优化

### 并发执行

```python
import concurrent.futures

def execute_concurrent(tasks):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(
            lambda t: executor.execute_task(t),
            tasks
        ))
    return results
```

### 任务分组

```python
# 按优先级分组
high_priority = ["critical-task-1", "critical-task-2"]
normal_priority = ["normal-task-1", "normal-task-2"]

# 先执行高优先级
executor.execute_all(tasks=high_priority)

# 再执行普通优先级
executor.execute_all(tasks=normal_priority)
```

---

## 🔗 相关文件

- **全量执行器**: `scripts/full-auto-executor.py`
- **智能调度中心**: `skills/07-system/taiyi-intelligent-scheduler.py`
- **MOSS-TTS 调用**: `skills/07-system/moss-tts-nano/moss_tts_auto_caller.py`

---

*太一全量智能自动化调用指南 · 太一 AGI · 2026-04-14 15:38*
