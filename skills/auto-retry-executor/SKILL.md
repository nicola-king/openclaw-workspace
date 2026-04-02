# 自动循环执行器 Skill

> 创建时间：2026-04-02 16:21  
> 版本：v1.0.0  
> 负责 Bot：素问（技术开发）  
> 状态：✅ 已创建，待测试

---

## 🎯 职责

**自动循环执行器** - 融合 Claude Code 的自动重试机制，实现任务的无人值守执行。

**核心功能**：
- ✅ 2-8 次自动重试
- ✅ 每次失败记录原因
- ✅ 8 次失败后上报人类
- ✅ ROI 实时计算（庖丁集成）
- ✅ 版本锁定校验（skills-lock.json）

---

## 📋 使用方式

```python
from skills.auto_retry_executor import execute_with_auto_retry

# 执行任务（自动重试 2-8 次）
result = await execute_with_auto_retry(
    task_id="TASK-050",
    task_name="知几首笔下注",
    executor_func=place_bet,
    validate_func=validate_bet,
    max_retries=8,
    roi_config={
        'manual_time_hours': 0.5,
        'hourly_rate_cny': 100
    }
)
```

---

## 🔧 核心 API

### `execute_with_auto_retry()`

```python
async def execute_with_auto_retry(
    task_id: str,
    task_name: str,
    executor_func: Callable,
    validate_func: Callable,
    max_retries: int = 5,  # Claude Code 精华：5 次后上报人类
    roi_config: Optional[Dict] = None,
    backoff_base: float = 2.0
) -> Dict[str, Any]:
    """
    自动循环执行器（融合 Claude Code 精华）
    
    参数:
        task_id: 任务 ID
        task_name: 任务名称
        executor_func: 执行函数
        validate_func: 验收函数
        max_retries: 最大重试次数（默认 8 次）
        roi_config: ROI 计算配置
        backoff_base: 指数退避基数（默认 2 秒）
    
    返回:
        {
            'status': 'success' | 'failed',
            'attempts': int,
            'roi': float,  # ROI 百分比
            'result': Any,  # 执行结果
            'error': str  # 失败原因（如果有）
        }
    """
```

---

## 📊 验收标准

### 成功标准

- ✅ 任务在 2-8 次内成功
- ✅ ROI 自动计算并归档
- ✅ 日志完整记录

### 失败标准

- ❌ 8 次尝试全部失败
- ❌ 自动上报人类
- ❌ 失败原因详细记录

---

## 🎯 集成点

### 1. 任务保障 v3.0

更新 `constitution/directives/TASK-GUARANTEE.md`：
- 添加自动循环执行器
- 阻塞自动跳过增强

### 2. 庖丁 ROI 计算

更新 `skills/paoding/SKILL.md`：
- 添加 ROI 计算公式
- 实时追踪任务成本

### 3. 版本锁定系统

更新 `skills-lock.json`：
- 激活为活跃配置
- 执行前校验

---

## 📋 测试计划

### 单元测试

```bash
python3 -m pytest tests/test_auto_retry.py -v
```

### 集成测试

```bash
python3 scripts/test_bet_executor.py
```

---

## 🚀 下一步

1. ✅ 创建 Skill 框架（完成）
2. ⚪ 编写核心代码（素问，30 分钟）
3. ⚪ 集成到任务保障 v3.0（太一，15 分钟）
4. ⚪ 庖丁 ROI 计算集成（庖丁，20 分钟）
5. ⚪ 版本锁定激活（素问，15 分钟）

---

*创建时间：2026-04-02 16:21 | 素问 AGI | 自动循环执行器*
