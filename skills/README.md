# 🧠 太一技能库

> 最后更新：2026-03-30 22:22 | 技能数量：10+ | 状态：自主进化中

---

## 📊 技能分类

### 量化交易 (知几)

| 技能 | 版本 | 状态 | 用途 |
|------|------|------|------|
| **zhiji-e** | v2.1 | ✅ 实盘 | 气象套利策略 |
| **zhiji-sentiment** | v1.0 | ✅ 测试 | FinBERT 情绪分析 |
| **zhiji-e-v3** | v3.0 | 🟢 待部署 | 情绪增强策略 |

### 内容创作 (山木)

| 技能 | 版本 | 状态 | 用途 |
|------|------|------|------|
| **shanmu-reporter** | v1.0 | ✅ 测试 | 研报生成 pipeline |
| **shanmu-content** | v1.0 | ✅ 运行 | 内容创意生成 |

### 技术开发 (素问)

| 技能 | 版本 | 状态 | 用途 |
|------|------|------|------|
| **suwen-coder** | v1.0 | ✅ 运行 | 代码生成/审查 |
| **suwen-debug** | v1.0 | ✅ 运行 | 问题诊断 |

### 数据采集 (罔两)

| 技能 | 版本 | 状态 | 用途 |
|------|------|------|------|
| **wangliang-scraper** | v1.0 | ✅ 运行 | 数据采集 |
| **wangliang-tracker** | v1.0 | ✅ 运行 | 鲸鱼追踪 |

### 预算成本 (庖丁)

| 技能 | 版本 | 状态 | 用途 |
|------|------|------|------|
| **paoding-tracker** | v1.0 | ✅ 运行 | 成本追踪 |

### 监控信号 (羿)

| 技能 | 版本 | 状态 | 用途 |
|------|------|------|------|
| **yi-alert** | v1.0 | ✅ 运行 | 信号监控 |

---

## 🆕 新增技能 (2026-03-30)

### zhiji-sentiment (FinBERT 情绪分析)

**位置**: `skills/zhiji-sentiment/`  
**功能**: 金融新闻情绪分析 (-1.0 ~ +1.0)  
**依赖**: transformers, torch  
**集成**: 知几-E v3.0 策略引擎

```python
from skills.zhiji-sentiment.scripts.sentiment_tools import SentimentTools
sentiment = SentimentTools(db, mode="auto")
result = sentiment.analyze_sentiment("BTC 突破 10 万美元")
# {"score": 0.85, "label": "positive", "reason": "..."}
```

### shanmu-reporter (研报生成)

**位置**: `skills/shanmu-reporter/`  
**功能**: 三阶段研报生成 (聚类→写作→组装)  
**输出**: Markdown + json-chart 配置

```python
from skills.shanmu-reporter.scripts.report_generator import ReportGenerator
generator = ReportGenerator()
report = generator.generate_report(signals)
```

---

## 📈 技能进化路线

```
2026-03-27: 基础技能 (6 Bot 架构)
    ↓
2026-03-28: 能力涌现 v2.0 (动态触发)
    ↓
2026-03-29: 多 Bot 协作演练 (8 Bot 实战)
    ↓
2026-03-30: AGI 自主模式 (100% 授权)
    ↓
2026-04-01: FinBERT 情绪分析实盘
2026-04-02: 研报生成自动化
2026-04-03: 技能市场产品化
```

---

## 🔧 使用规范

### 调用技能

```python
# 方式 1: 直接导入
from skills.zhiji-sentiment.scripts.sentiment_tools import SentimentTools

# 方式 2: 通过 SKILL.md 描述
# Agent 根据 description 自动选择技能
```

### 创建新技能

```bash
mkdir -p skills/{name}/{scripts,references}
# 创建 SKILL.md (必需)
# 创建脚本文件
# 测试验证
# 更新 skills/README.md
```

---

*维护：太一 AGI | 自主进化中*
