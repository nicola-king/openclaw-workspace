---
name: qa-supervisor
version: 1.0.0
description: qa-supervisor skill
category: other
tags: []
author: 太一 AGI
created: 2026-04-07
---


# 质量监督器（QA Supervisor）

> 创建时间：2026-04-02 16:45  
> 版本：v1.0.0  
> 负责 Bot：素问（技术开发）+ 罔两（数据）  
> 状态：✅ 已创建，执行中

---

## 🎯 职责

**质量监督器** - 太一 v4.0 监督层核心组件，负责任务执行的质量验收和自动重试决策。

**灵感来源**：Claude Code 监督 Codex 架构

**核心功能**：
- ✅ 任务质量门禁验收
- ✅ 自动重试决策（2-5 次）
- ✅ 失败原因分析
- ✅ 5 次失败后上报人类
- ✅ ROI 验证（庖丁集成）

---

## 📋 架构设计

### 监督层位置

```
┌─────────────────────────────────────────┐
│         决策层（太一 + 宪法）            │
│  - 意图理解 / 目标拆解 / 价值判断         │
└─────────────────┬───────────────────────┘
                  │ 任务分发
┌─────────────────▼───────────────────────┐
│         监督层（QA Supervisor）          │ ← 本组件
│  - 质量门禁验收                          │
│  - 自动重试决策                          │
│  - 失败原因分析                          │
│  - ROI 验证                              │
└─────────────────┬───────────────────────┘
                  │ 执行指令
┌─────────────────▼───────────────────────┐
│         执行层（8 Bot 专业舰队）          │
│  - 知几/山木/素问/罔两/庖丁/羿/守藏吏    │
└─────────────────────────────────────────┘
```

---

## 🔧 核心 API

### 质量门禁验收

```python
from skills.qa_supervisor import QASupervisor

# 初始化监督器
supervisor = QASupervisor()

# 验收任务结果
validation = await supervisor.validate(
    task_type='trading',
    result={
        'status': 200,
        'order_id': '123',
        'amount': 5
    }
)

if validation['passed']:
    print("✅ 验收通过")
else:
    print(f"❌ 验收失败：{validation['error']}")
```

### 质量门禁规则

```python
class QASupervisor:
    """质量监督器"""
    
    def __init__(self):
        self.quality_gates = self._load_quality_gates()
    
    def _load_quality_gates(self) -> dict:
        """加载质量门禁规则"""
        return {
            'trading': {
                'required_fields': ['status', 'order_id', 'amount'],
                'validators': {
                    'status': lambda x: x == 200,
                    'order_id': lambda x: len(x) > 0,
                    'amount': lambda x: x > 0
                }
            },
            'content': {
                'required_fields': ['title', 'content', 'platform'],
                'validators': {
                    'title': lambda x: 5 <= len(x) <= 100,
                    'content': lambda x: len(x) > 50,
                    'platform': lambda x: x in ['wechat', 'xiaohongshu', 'twitter']
                }
            },
            'coding': {
                'required_fields': ['files', 'tests_passed'],
                'validators': {
                    'files': lambda x: len(x) > 0,
                    'tests_passed': lambda x: x == True
                }
            }
        }
    
    async def validate(self, task_type: str, result: dict) -> dict:
        """
        质量门禁验收
        
        返回:
            {
                'passed': bool,
                'error': str (optional),
                'warnings': list (optional),
                'score': float (0-100)
            }
        """
        if task_type not in self.quality_gates:
            return {
                'passed': True,
                'warning': f'未知任务类型：{task_type}，默认通过'
            }
        
        gate = self.quality_gates[task_type]
        
        # 检查必填字段
        for field in gate['required_fields']:
            if field not in result:
                return {
                    'passed': False,
                    'error': f'缺少必填字段：{field}'
                }
        
        # 执行验证器
        for field, validator in gate['validators'].items():
            if not validator(result[field]):
                return {
                    'passed': False,
                    'error': f'字段验证失败：{field}'
                }
        
        # 计算质量分数
        score = self._calculate_score(result, gate)
        
        return {
            'passed': True,
            'score': score,
            'warnings': []
        }
    
    def _calculate_score(self, result: dict, gate: dict) -> float:
        """计算质量分数（0-100）"""
        # 基础分数：100 分
        score = 100.0
        
        # 根据结果质量扣分
        # ...（实现细节）
        
        return score
```

---

## 🔄 自动重试决策

### 重试逻辑

```python
from skills.qa_supervisor import QASupervisor

async def execute_with_qa_loop(task, config):
    """
    带 QA 监督的执行循环
    
    流程：
    1. 执行任务
    2. QA 验收
    3. 通过 → 归档
    4. 失败 → 重试（最多 5 次）
    5. 5 次失败 → 上报人类
    """
    supervisor = QASupervisor()
    max_retries = 5
    
    for attempt in range(1, max_retries + 1):
        # 执行任务
        result = await execute_task(task)
        
        # QA 验收
        validation = await supervisor.validate(
            task_type=task['type'],
            result=result
        )
        
        if validation['passed']:
            # 验收通过，归档
            await archive_task(task, result, validation['score'])
            return {
                'status': 'success',
                'attempts': attempt,
                'score': validation['score']
            }
        
        # 验收失败，记录原因
        log_failure(task, result, validation['error'], attempt)
        
        # 指数退避
        if attempt < max_retries:
            wait_time = 2 ** attempt
            await asyncio.sleep(wait_time)
    
    # 5 次失败后上报
    await escalate_to_human(task, failure_log)
    
    return {
        'status': 'failed',
        'attempts': max_retries,
        'error': 'max_retries_exceeded'
    }
```

---

## 📊 失败原因分析

### 失败分类

```python
class FailureAnalyzer:
    """失败原因分析器（罔两负责）"""
    
    def __init__(self):
        self.failure_categories = {
            'network_error': '网络错误',
            'validation_error': '验证失败',
            'timeout': '超时',
            'api_error': 'API 错误',
            'browser_error': '浏览器错误',
            'unknown': '未知错误'
        }
    
    def analyze(self, failure_log: list) -> dict:
        """
        分析失败原因
        
        返回:
            {
                'primary_cause': str,
                'category': str,
                'suggestions': list,
                'retry_recommended': bool
            }
        """
        # 分析失败模式
        # ...
        
        return {
            'primary_cause': '网络超时',
            'category': 'timeout',
            'suggestions': [
                '增加超时时间',
                '检查网络连接',
                '使用代理'
            ],
            'retry_recommended': True
        }
```

### 失败日志结构

```json
{
  "task_id": "TASK-050",
  "task_name": "知几首笔下注",
  "failure_log": [
    {
      "attempt": 1,
      "timestamp": "2026-04-02T16:45:00+08:00",
      "error": "状态码错误：401",
      "category": "api_error",
      "suggestions": ["检查 API Key", "验证签名"]
    },
    {
      "attempt": 2,
      "timestamp": "2026-04-02T16:45:10+08:00",
      "error": "状态码错误：401",
      "category": "api_error",
      "suggestions": ["检查 API Key", "验证签名"]
    }
  ],
  "analysis": {
    "primary_cause": "API Key 无效",
    "category": "api_error",
    "retry_recommended": false,
    "human_intervention_required": true
  }
}
```

---

## 📋 质量门禁模板

### 交易任务（知几）

```python
TRADING_GATE = {
    'required_fields': ['status', 'order_id', 'amount', 'market', 'outcome'],
    'validators': {
        'status': lambda x: x == 200,
        'order_id': lambda x: len(x) > 10,
        'amount': lambda x: x > 0 and x <= 100,
        'market': lambda x: len(x) > 0,
        'outcome': lambda x: x in ['YES', 'NO']
    },
    'score_weights': {
        'status': 40,
        'order_id': 20,
        'amount': 20,
        'market': 10,
        'outcome': 10
    }
}
```

### 内容任务（山木）

```python
CONTENT_GATE = {
    'required_fields': ['title', 'content', 'platform', 'status'],
    'validators': {
        'title': lambda x: 5 <= len(x) <= 100,
        'content': lambda x: len(x) > 100,
        'platform': lambda x: x in ['wechat', 'xiaohongshu', 'twitter'],
        'status': lambda x: x == 'published'
    },
    'score_weights': {
        'title': 20,
        'content': 40,
        'platform': 10,
        'status': 30
    }
}
```

### 代码任务（素问）

```python
CODING_GATE = {
    'required_fields': ['files', 'tests_passed', 'lint_passed', 'git_commit'],
    'validators': {
        'files': lambda x: len(x) > 0,
        'tests_passed': lambda x: x == True,
        'lint_passed': lambda x: x == True,
        'git_commit': lambda x: len(x) >= 7
    },
    'score_weights': {
        'files': 20,
        'tests_passed': 40,
        'lint_passed': 20,
        'git_commit': 20
    }
}
```

---

## 📊 ROI 验证（庖丁集成）

```python
from skills.paoding import calculate_roi

async def validate_roi(task_id: str, result: dict) -> dict:
    """
    ROI 验证
    
    验收标准：
    - ROI > 100%（至少翻倍）
    - 成本 < ¥10（单次任务）
    - 时间节省 > 50%
    """
    roi_result = calculate_roi(
        task_id=task_id,
        token_input=result.get('input_tokens', 0),
        token_output=result.get('output_tokens', 0),
        api_calls=result.get('api_calls', 0),
        exec_time_sec=result.get('exec_time_sec', 0),
        manual_time_hours=0.5,
        hourly_rate_cny=100
    )
    
    # 验收标准
    if roi_result['roi'] < 100:
        return {
            'passed': False,
            'error': f"ROI 过低：{roi_result['roi']:.0f}% < 100%"
        }
    
    if roi_result['ai_cost'] > 10:
        return {
            'passed': False,
            'error': f"成本过高：¥{roi_result['ai_cost']:.2f} > ¥10"
        }
    
    return {
        'passed': True,
        'roi': roi_result['roi'],
        'cost': roi_result['ai_cost']
    }
```

---

## 🚀 实施路线图

### Phase 1：基础框架（2026-04-02）

| 任务 | 负责 | 工时 | 状态 |
|------|------|------|------|
| QA 监督器框架 | 素问 | 30 分钟 | ✅ 完成 |
| 质量门禁模板 | 素问 | 20 分钟 | 🟡 执行中 |
| 失败原因分析 | 罔两 | 20 分钟 | ⚪ 待创建 |

### Phase 2：集成测试（2026-04-03）

| 任务 | 负责 | 工时 | 状态 |
|------|------|------|------|
| 交易任务验收测试 | 知几 | 20 分钟 | ⚪ 待创建 |
| 内容任务验收测试 | 山木 | 20 分钟 | ⚪ 待创建 |
| 代码任务验收测试 | 素问 | 20 分钟 | ⚪ 待创建 |

### Phase 3：生产上线（2026-04-04）

| 任务 | 负责 | 工时 | 状态 |
|------|------|------|------|
| 集成到自动循环执行器 | 素问 | 15 分钟 | ⚪ 待创建 |
| 集成到任务保障 v3.0 | 太一 | 15 分钟 | ⚪ 待创建 |
| 文档更新 | 山木 | 20 分钟 | ⚪ 待创建 |

---

## 📊 预期效果

| 指标 | 当前 | QA 监督器 | 提升 |
|------|------|-----------|------|
| **验收通过率** | 🟡 人工 | ✅ 自动 | **100% 自动化** |
| **失败原因分析** | ❌ 手动 | ✅ 自动 | **新能力** |
| **重试决策** | ❌ 人工 | ✅ 自动 | **新能力** |
| **ROI 验证** | 🟡 事后 | ✅ 实时 | **新能力** |

---

*创建时间：2026-04-02 16:45 | 素问 + 罔两 AGI | 质量监督器*
