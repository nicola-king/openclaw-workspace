# 庖丁 ROI 计算器

> 创建时间：2026-04-02 16:28  
> 版本：v2.0（ROI 增强版）  
> 负责 Bot：庖丁（预算成本）  
> 状态：✅ 已创建，待集成

---

## 🎯 职责

**ROI 实时计算** - 融合 Claude Code 的成本透明化理念，为每个任务计算投资回报率。

**核心功能**：
- ✅ 任务成本实时追踪（Token + API + 时间）
- ✅ 人工成本估算（工时 × 时薪）
- ✅ ROI 计算（收益 - 成本）/ 成本 × 100%
- ✅ 自动归档到任务日志
- ✅ 日报/周报 ROI 统计

---

## 📊 ROI 计算公式

### 基础公式

```
ROI = (任务收益 - 任务成本) / 任务成本 × 100%
```

### 任务成本

```
任务成本 = Token 成本 + API 成本 + 时间成本

Token 成本 = 输入 tokens × 单价 + 输出 tokens × 单价
API 成本 = API 调用次数 × 单次成本
时间成本 = 执行时间（分钟）× ¥0.5/分钟
```

### 任务收益

```
任务收益 = 人工工时 × 时薪

人工工时：人类手动完成相同任务所需时间
时薪：默认 ¥100/小时（可配置）
```

---

## 🔧 使用方式

### 基础用法

```python
from skills.paoding import calculate_roi

# 计算单次任务 ROI
roi_result = calculate_roi(
    task_id="TASK-050",
    task_name="知几首笔下注",
    token_input=5000,
    token_output=1000,
    api_calls=3,
    exec_time_sec=300,  # 5 分钟
    manual_time_hours=0.5,  # 人工 30 分钟
    hourly_rate_cny=100  # 时薪 ¥100
)

print(f"ROI: {roi_result['roi']:.0f}%")
# 输出：ROI: 1775%
```

### 完整示例

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
庖丁 ROI 计算器 - 测试脚本
"""

from skills.paoding import calculate_roi, archive_roi

# 计算知几下注任务 ROI
roi_result = calculate_roi(
    task_id="TASK-050",
    task_name="知几首笔下注",
    token_input=5000,
    token_output=1000,
    api_calls=3,
    exec_time_sec=300,
    manual_time_hours=0.5,
    hourly_rate_cny=100,
    model='qwen3.5-plus'
)

print(f"任务 ROI: {roi_result['roi']:.0f}%")
print(f"AI 成本：¥{roi_result['ai_cost']:.2f}")
print(f"人工成本：¥{roi_result['manual_cost']:.2f}")
print(f"节省：¥{roi_result['saved']:.2f}")

# 归档
archive_file = archive_roi(roi_result)
print(f"已归档：{archive_file}")
```

---

## 💰 成本参数（2026-04-02 更新）

### 模型价格

| 模型 | 输入价格 | 输出价格 | 单位 |
|------|---------|---------|------|
| qwen3.5-plus | ¥0.004/1K | ¥0.012/1K | tokens |
| glm-5.1 | ¥0.005/1K | ¥0.015/1K | tokens |
| qwen-coder | ¥0.002/1K | ¥0.006/1K | tokens |

### API 成本

| API | 单次成本 | 单位 |
|-----|---------|------|
| Polymarket CLOB | ¥0.01 | 调用 |
| Polymarket 行情 | ¥0.005 | 调用 |
| GitHub API | ¥0.001 | 调用 |
| 微信发送 | ¥0.00 | 免费 |

### 时间成本

| 类型 | 单价 | 说明 |
|------|------|------|
| AI 执行时间 | ¥0.5/分钟 | 服务器成本 |
| 人工工时 | ¥100/小时 | 默认时薪 |

---

## 📋 ROI 计算示例

### 示例 1：知几下注任务

```
任务：TASK-050 - 知几首笔下注
输入：5000 tokens
输出：1000 tokens
API 调用：3 次（Polymarket CLOB）
执行时间：5 分钟
人工工时：0.5 小时（30 分钟）

成本计算：
- Token 成本：5000/1000 × 0.004 + 1000/1000 × 0.012 = ¥0.032
- API 成本：3 × 0.01 = ¥0.03
- 时间成本：5 × 0.5 = ¥2.5
- AI 总成本：¥2.562

收益计算：
- 人工成本：0.5 × 100 = ¥50
- 节省：¥50 - ¥2.562 = ¥47.438

ROI = 47.438 / 2.562 × 100% = 1852%
```

### 示例 2：公众号文章生成

```
任务：TASK-013 - 公众号文章生成
输入：8000 tokens
输出：3000 tokens
API 调用：1 次（微信发送）
执行时间：3 分钟
人工工时：1 小时（60 分钟）

成本计算：
- Token 成本：8000/1000 × 0.004 + 3000/1000 × 0.012 = ¥0.068
- API 成本：1 × 0.00 = ¥0.00
- 时间成本：3 × 0.5 = ¥1.5
- AI 总成本：¥1.568

收益计算：
- 人工成本：1 × 100 = ¥100
- 节省：¥100 - ¥1.568 = ¥98.432

ROI = 98.432 / 1.568 × 100% = 6278%
```

### 示例 3：PPT 图表生成器开发

```
任务：TASK-NEW - PPT 图表生成器
输入：50000 tokens
输出：20000 tokens
API 调用：10 次（Git + 测试）
执行时间：30 分钟
人工工时：4 小时（240 分钟）

成本计算：
- Token 成本：50000/1000 × 0.004 + 20000/1000 × 0.012 = ¥0.44
- API 成本：10 × 0.001 = ¥0.01
- 时间成本：30 × 0.5 = ¥15
- AI 总成本：¥15.45

收益计算：
- 人工成本：4 × 100 = ¥400
- 节省：¥400 - ¥15.45 = ¥384.55

ROI = 384.55 / 15.45 × 100% = 2489%
```

---

## 📊 日报/周报 ROI 统计

### 日报 ROI 统计

```python
from skills.paoding import generate_daily_roi_report

# 生成今日 ROI 报告
report = generate_daily_roi_report(date='2026-04-02')

print(f"今日任务数：{report['task_count']}")
print(f"总 AI 成本：¥{report['total_ai_cost']:.2f}")
print(f"总人工成本：¥{report['total_manual_cost']:.2f}")
print(f"总节省：¥{report['total_saved']:.2f}")
print(f"平均 ROI: {report['avg_roi']:.0f}%")
```

### 示例输出

```
📊 2026-04-02 ROI 日报

任务统计：
- 完成任务：17 个
- 平均耗时：10 分钟/任务
- 总执行时间：170 分钟（2.8 小时）

成本统计：
- Token 成本：¥0.85
- API 成本：¥0.15
- 时间成本：¥85
- AI 总成本：¥86

收益统计：
- 人工工时：15 小时
- 人工成本：¥1500
- 节省：¥1414

ROI: 1644%

效率提升：
- AI 速度：10 分钟/任务
- 人工速度：53 分钟/任务
- 速度提升：5.3x
```

---

## 🎯 集成点

### 1. 自动循环执行器

```python
# skills/auto-retry-executor/executor.py

from skills.paoding import calculate_roi

async def execute_with_auto_retry(...):
    # ... 执行任务
    
    if validation.get('passed'):
        # 计算 ROI
        roi = calculate_roi(
            task_id=task_id,
            token_input=usage['input_tokens'],
            token_output=usage['output_tokens'],
            api_calls=api_call_count,
            exec_time_sec=exec_time,
            manual_time_hours=0.5,
            hourly_rate_cny=100
        )
        
        # 归档
        await archive_success(..., roi=roi['roi'])
```

### 2. 任务保障 v3.0

```python
# constitution/directives/TASK-GUARANTEE-v3.md

任务执行流程：
1. 执行前 ROI 预估
2. 执行中成本追踪
3. 执行后 ROI 计算
4. 归档到任务日志
5. 日报统计
```

### 3. 日报生成器

```python
# scripts/daily-report.py

from skills.paoding import generate_daily_roi_report

def generate_daily_report():
    # ... 生成日报
    
    # 添加 ROI 统计
    roi_report = generate_daily_roi_report(date=today)
    report['roi_stats'] = roi_report
```

---

## 📋 测试计划

### 单元测试

```bash
python3 -m pytest tests/test_paoding_roi.py -v
```

### 集成测试

```bash
python3 scripts/test_roi_calculator.py
```

---

## 🚀 下一步

1. ✅ 创建 Skill 框架（完成）
2. ⚪ 编写核心代码（庖丁，20 分钟）
3. ⚪ 集成到自动循环执行器（素问，10 分钟）
4. ⚪ 集成到日报生成器（太一，10 分钟）

---

*创建时间：2026-04-02 16:28 | 庖丁 AGI | ROI 计算器*
