# 🎨 Aesthetic Scorer - 美学评分引擎

> **版本**: 1.0.0  
> **创建时间**: 2026-04-25  
> **作者**: 太一 AGI  
> **定位**: 太一系统美学评分核心 - 多维度质量评估

---

## 🎯 核心使命

为太一系统所有输出提供多维度美学评分，确保输出品质。

### 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| **可读性** | 20% | 句子长度/段落结构/词汇多样性/留白比例 |
| **一致性** | 20% | 标题层级/列表格式/代码标注/缩进统一 |
| **美学** | 20% | 视觉层次/装饰适度/签名标识 |
| **功能性** | 20% | 信息完整/逻辑清晰/可执行性/数据支撑 |
| **结构性** | 10% | 标题层级/段落组织/导航元素/章节平衡 |
| **语义性** | 10% | 歧义检测/术语一致/表达精准/情感色彩 |

### 等级划分

| 等级 | 分数 | 说明 |
|------|------|------|
| **S 级** | ≥90 | 出版级 |
| **A 级** | ≥75 | 专业级 |
| **B 级** | ≥60 | 可用级 |
| **C 级** | <60 | 草稿级 |

---

## 📦 模块功能

### 评分引擎

```python
from aesthetic_scorer import AestheticScorer

scorer = AestheticScorer()
result = scorer.score(content, content_type="markdown")
print(f"评分：{result['score']}/100 ({result['level']})")
```

### 多维度分析

```python
dimensions = result['dimensions']
for dim_name, dim_score in dimensions.items():
    print(f"{dim_name}: {dim_score['score']}/100")
```

---

## 🚀 使用方式

### 1. 独立运行

```bash
python core.py --input report.md --type markdown --json
```

### 2. 太一系统集成

```python
from aesthetic_scorer import AestheticScorer

scorer = AestheticScorer()
result = scorer.score(report_content, type="report")
```

---

## 📋 自进化

- **版本**: 1.0.0
- **进化日志**: `memory/evolution/aesthetic-scorer.json`
- **反馈收集**: 用户评分 → 模型优化

---

*太一 Aesthetic Scorer v1.0 · 美学评分引擎*  
*创建时间：2026-04-25*
