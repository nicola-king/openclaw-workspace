# 🤖 太一智能调度中心 - 全 Agent/Skill 自动化调用指南

> **创建时间**: 2026-04-14 15:29  
> **状态**: ✅ 已完成  
> **功能**: 智能自动化调用所有 Agents/Skills

---

## 🚀 快速开始

### 方法 1: 直接调用

```python
from skills.07-system.taiyi-intelligent-scheduler import TaiyiIntelligentScheduler

scheduler = TaiyiIntelligentScheduler()

# 执行任务
result = scheduler.execute_task("token-optimization-analysis")

print(f"结果：{'✅ 成功' if result.success else '❌ 失败'}")
```

### 方法 2: 智能路由

```python
from skills.07-system.taiyi-intelligent-scheduler import TaiyiIntelligentScheduler

scheduler = TaiyiIntelligentScheduler()

# 根据任务描述自动选择最佳 Skill
task_desc = "我需要生成语音"
recommended = scheduler.intelligent_route(task_desc)

print(f"推荐使用：{recommended}")

# 执行
result = scheduler.execute_task(recommended)
```

### 方法 3: 批量执行

```python
from skills.07-system.taiyi-intelligent-scheduler import TaiyiIntelligentScheduler

scheduler = TaiyiIntelligentScheduler()

# 批量任务
tasks = [
    {"name": "token-optimization-analysis"},
    {"name": "memory-compression-algorithm"},
    {"name": "skill-confidence-evaluator"},
]

results = scheduler.batch_execute(tasks)

print(f"成功：{sum(1 for r in results if r.success)}/{len(results)}")
```

---

## 📋 API 参考

### TaiyiIntelligentScheduler

#### execute_task()
```python
def execute_task(
    task_name: str,
    **kwargs
) -> TaskResult
```

**参数**:
- `task_name`: 任务名称 (Skill/Agent/Script 名称)
- `**kwargs`: 传递给任务的参数

**返回**: TaskResult 对象

#### batch_execute()
```python
def batch_execute(
    tasks: List[Dict]
) -> List[TaskResult]
```

**参数**:
- `tasks`: 任务列表 `[{"name": "task1", "params": {...}}, ...]`

**返回**: TaskResult 列表

#### intelligent_route()
```python
def intelligent_route(
    task_description: str
) -> str
```

**参数**:
- `task_description`: 任务描述 (自然语言)

**返回**: 推荐的 Skill/Agent 名称

#### get_stats()
```python
def get_stats() -> Dict
```

**返回**: 统计信息字典

#### save_log()
```python
def save_log(
    output_path: Optional[Path] = None
)
```

**参数**:
- `output_path`: 日志输出路径 (可选)

---

## 🎯 使用场景

### 1. 自动化工作流

```python
scheduler = TaiyiIntelligentScheduler()

# 定义工作流
workflow = [
    {"name": "token-optimization-analysis"},
    {"name": "memory-compression-algorithm"},
    {"name": "skill-confidence-evaluator"},
    {"name": "experience-trend-generator"},
]

# 执行
results = scheduler.batch_execute(workflow)

# 保存日志
scheduler.save_log()
```

### 2. 智能路由

```python
scheduler = TaiyiIntelligentScheduler()

# 用户输入
user_requests = [
    "帮我生成语音",
    "分析一下 token 消耗",
    "评估一下技能质量",
    "生成趋势图",
]

for request in user_requests:
    # 智能路由
    skill = scheduler.intelligent_route(request)
    
    # 执行
    result = scheduler.execute_task(skill)
    
    print(f"{request} → {skill} → {'✅' if result.success else '❌'}")
```

### 3. 定时任务

```python
# crontab 配置
*/15 * * * * python3 /home/nicola/.openclaw/workspace/skills/07-system/taiyi-intelligent-scheduler.py --auto

# 或使用 Python 调度
import schedule
import time

scheduler = TaiyiIntelligentScheduler()

def scheduled_task():
    workflow = [...]
    scheduler.batch_execute(workflow)
    scheduler.save_log()

schedule.every(15).minutes.do(scheduled_task)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### 4. 错误自愈

```python
scheduler = TaiyiIntelligentScheduler()

# 执行任务
result = scheduler.execute_task("some-task")

# 失败重试
if not result.success:
    print(f"任务失败：{result.error}")
    
    # 重试 (最多 3 次)
    for i in range(3):
        result = scheduler.execute_task("some-task")
        if result.success:
            break
    
    if not result.success:
        print("重试失败，记录日志")
        scheduler.save_log()
```

---

## 📊 统计信息

**示例输出**:
```json
{
  "total_tasks": 10,
  "success_tasks": 9,
  "failed_tasks": 1,
  "success_rate": "90.0%",
  "avg_duration_seconds": "5.23",
  "total_skills": 471,
  "total_agents": 9,
  "total_scripts": 50
}
```

---

## 🔧 命令行调用

### 直接运行
```bash
python3 /home/nicola/.openclaw/workspace/skills/07-system/taiyi-intelligent-scheduler.py
```

### 执行特定任务
```bash
python3 /home/nicola/.openclaw/workspace/skills/07-system/taiyi-intelligent-scheduler.py \
    --task token-optimization-analysis
```

### 批量执行
```bash
python3 /home/nicola/.openclaw/workspace/skills/07-system/taiyi-intelligent-scheduler.py \
    --batch tasks.json
```

---

## 📈 性能优化

### 并发执行
```python
import concurrent.futures

def execute_concurrent(tasks):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(
            lambda t: scheduler.execute_task(t["name"], **t.get("params", {})),
            tasks
        ))
    return results
```

### 缓存结果
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_execute(task_name):
    return scheduler.execute_task(task_name)
```

---

## 🔗 相关文件

- **智能调度中心**: `skills/07-system/taiyi-intelligent-scheduler.py`
- **MOSS-TTS 调用**: `skills/07-system/moss-tts-nano/moss_tts_auto_caller.py`
- **太一 TTS 系统**: `skills/07-system/taiyi-tts-system.py`
- **Skill 评估**: `skills/07-system/skill-confidence-evaluator.py`

---

*太一智能调度中心 · 太一 AGI · 2026-04-14 15:29*
