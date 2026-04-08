# Model Empathy 对比测试脚本

> 创建时间：2026-04-06 01:00 | P1 任务执行

---

## 🧠 测试设计

**假设**: 同模型组合 (meta + task) 效果优于跨模型组合

**测试组合**:
1. 同模型：qwen3.5-plus meta + qwen3.5-plus task
2. 跨模型：qwen3.5-plus meta + Gemini task
3. 跨模型：Gemini meta + qwen3.5-plus task

---

## 📋 测试用例

```python
TEST_CASES = [
    {
        "id": "test-001",
        "name": "复杂推理",
        "prompt": "如果所有 A 都是 B，有些 B 是 C，那么有些 A 是 C 吗？",
        "expected": "不一定。需要分析集合关系。"
    },
    {
        "id": "test-002",
        "name": "代码优化",
        "prompt": "优化递归 fib(n) 函数",
        "expected": "使用记忆化或动态规划"
    },
    {
        "id": "test-003",
        "name": "内容创作",
        "prompt": "写 AI 管家短文 (300 字)",
        "expected": "包含引言/功能/场景/结论"
    }
]
```

---

## 🔧 执行脚本

```python
#!/usr/bin/env python3
"""Model Empathy 对比测试"""

import json
from datetime import datetime

MODEL_COMBINATIONS = [
    {"name": "同模型", "meta": "qwen3.5-plus", "task": "qwen3.5-plus"},
    {"name": "跨模型 1", "meta": "qwen3.5-plus", "task": "gemini-2.5-pro"},
    {"name": "跨模型 2", "meta": "gemini-2.5-pro", "task": "qwen3.5-plus"}
]

def run_comparison_test():
    """运行对比测试"""
    results = []
    
    for combo in MODEL_COMBINATIONS:
        for test in TEST_CASES:
            # 调用模型 API
            response = call_model(
                meta_model=combo["meta"],
                task_model=combo["task"],
                prompt=test["prompt"]
            )
            
            # 评分 (1-5 分)
            score = evaluate_response(response, test["expected"])
            
            results.append({
                "combination": combo["name"],
                "test": test["name"],
                "score": score,
                "response": response
            })
    
    # 保存结果
    save_results(results)
    return results
```

---

## 📊 评分标准

| 维度 | 权重 | 说明 |
|------|------|------|
| 准确性 | 40% | 答案正确性 |
| 完整性 | 25% | 覆盖关键点 |
| 逻辑性 | 20% | 推理清晰 |
| 创造性 | 15% | 独特见解 |

---

## 📋 执行计划

### 今天 (P0)
- [x] 基线测试完成
- [x] 对比测试脚本创建
- [ ] 运行 3 种组合测试
- [ ] 人工评分

### 本周 (P1)
- [ ] 每种组合 3 次测试
- [ ] 统计分析
- [ ] 验证假设
- [ ] 优化模型路由

---

*创建时间：2026-04-06 01:00 | 太一 AGI*
