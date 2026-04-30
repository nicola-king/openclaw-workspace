# 🧠 Awesome Finance Skills 代码结构分析报告

**分析时间**: 2026-03-30 22:12  
**来源**: https://github.com/RKiding/Awesome-finance-skills  
**分析负责**: 素问 (技术开发 Bot)

---

## 📦 技能模块清单

| 技能 | 核心功能 | 关键文件 | 依赖 |
|------|---------|---------|------|
| **alphaear-sentiment** | FinBERT/LLM 情绪分析 | `scripts/sentiment_tools.py` | transformers, torch |
| **alphaear-reporter** | 研报生成 pipeline | `references/PROMPTS.md` | sqlite3 |
| **alphaear-news** | 新闻聚合 (10+ 信源) | `scripts/news_tools.py` | sqlite3, requests |
| **alphaear-predictor** | Kronos 时序预测 | `scripts/kronos_predictor.py` | kronos-model |
| **alphaear-stock** | A 股/港股数据 | `scripts/stock_tools.py` | akshare/yfinance |
| **alphaear-signal-tracker** | 信号演化追踪 | `scripts/signal_tracker.py` | sqlite3 |
| **alphaear-logic-visualizer** | 逻辑链路可视化 | `scripts/visualizer.py` | graphviz |
| **alphaear-search** | 搜索 RAG | `scripts/search_tools.py` | jina/ddg |

---

## 🔍 核心模块深度分析

### 1. alphaear-sentiment (情绪分析)

**架构**:
```
SentimentTools (类)
├── __init__(db, mode)
│   ├── mode: "auto" | "bert" | "llm"
│   └── 初始化 BERT pipeline (从本地缓存或网络下载)
├── analyze_sentiment(text)
│   └── 返回：{"score": float, "label": str, "reason": str}
├── analyze_sentiment_bert(texts)
│   └── 批量高速分析 (FinBERT)
└── update_single_news_sentiment(id, score, reason)
    └── 保存 LLM 手动分析结果到数据库
```

**关键代码**:
```python
# 情绪分析模式
DEFAULT_SENTIMENT_MODE = os.getenv("SENTIMENT_MODE", "auto")

# BERT 模型 (中文财经)
bert_model = "uer/roberta-base-finetuned-chinanews-chinese"

# 评分范围：-1.0 (负面) ~ +1.0 (正面)
# 中性：-0.1 ~ +0.1
```

**太一集成方案**:
```python
# 集成到知几-E 策略引擎
class ZhijiEStrategy:
    def calculate_confidence(self, weather_data, news_sentiment):
        # 原：仅气象置信度
        # 新：气象置信度 + 新闻情绪综合
        base_confidence = weather_data['confidence']
        sentiment_boost = news_sentiment['score'] * 0.1  # 情绪加成
        return min(1.0, base_confidence + sentiment_boost)
```

---

### 2. alphaear-reporter (研报生成)

**工作流程**:
```
1. Cluster Signals (Planner)
   ↓
2. Write Sections (Writer)
   ↓
3. Final Assembly (Editor)
```

**核心 Prompt**:

**Cluster Signals Prompt**:
```markdown
You are a senior financial report editor.
Cluster scattered financial signals into 3-5 core logical themes.

Output Format (JSON):
{
    "clusters": [
        {
            "theme_title": "Theme Name",
            "signal_ids": [1, 3, 5],
            "rationale": "..."
        }
    ]
}
```

**Write Section Prompt**:
```markdown
You are a senior financial analyst.
Write deep analysis for theme: "{theme_title}"

Requirements:
1. Narrative: Macro → Industry → Stock impact
2. Quantification: Cite ISQ scores
3. Charts: Insert 1-2 json-chart blocks
```

**太一集成方案**:
```python
# 集成到山木内容创作
class ShanmuReporter:
    def generate_report(self, signals):
        # 1. 聚类信号
        clusters = self.cluster_signals(signals)
        # 2. 生成章节
        sections = [self.write_section(c) for c in clusters]
        # 3. 组装报告
        return self.assemble_report(sections)
```

---

### 3. alphaear-predictor (Kronos 时序预测)

**架构**:
```
KronosPredictorUtility
├── get_base_forecast(df, lookback, pred_len, news_text)
│   └── 返回：List[KLinePoint]
└── adjust_forecast(base_forecast, news_sentiment)
    └── Agent 根据新闻主观调整
```

**与 TimesFM 对比**:

| 特性 | Kronos | TimesFM |
|------|--------|---------|
| 新闻感知 | ✅ 内置 | 🟡 需外部集成 |
| 中文支持 | ✅ 优化 | ✅ 支持 |
| 模型大小 | ~100MB | ~300MB |
| 推理速度 | 快 | 中 |

**太一决策**: 保留 TimesFM (已集成), 参考 Kronos 新闻感知设计

---

## 🎯 太一集成优先级

### P0: FinBERT 情绪分析 (知几-E)

**集成步骤**:
1. 安装依赖：`pip install transformers torch`
2. 创建 `skills/zhiji-sentiment/SKILL.md`
3. 复制 `sentiment_tools.py` 到 `skills/zhiji-sentiment/scripts/`
4. 修改知几-E 策略引擎，调用情绪分析
5. 测试：气象 + 新闻综合置信度

**预期效果**:
- 当前：仅气象置信度 (96% 阈值)
- 增强：+ 新闻情绪因子 → 动态阈值 (90-98%)

---

### P0: 研报生成 pipeline (山木)

**集成步骤**:
1. 创建 `skills/shanmu-reporter/SKILL.md`
2. 复制 `PROMPTS.md` 到 `skills/shanmu-reporter/references/`
3. 创建 `scripts/report_generator.py` (实现 3 阶段 workflow)
4. 集成到山木 Bot 内容创作流程
5. 测试：自动生成 Polymarket 分析报告

**预期效果**:
- 当前：手动撰写研报
- 增强：自动化 (信号→聚类→章节→报告)

---

### P1: 逻辑链路可视化 (罔两)

**集成步骤**:
1. 创建 `skills/wangliang-visualizer/SKILL.md`
2. 复制 `visualizer.py` 到 `skills/wangliang-visualizer/scripts/`
3. 集成到罔两数据报告流程
4. 测试：生成市场影响传导链图

---

## 📊 代码质量评估

| 维度 | 评分 | 备注 |
|------|------|------|
| 代码结构 | 4.5/5 | 模块化清晰 |
| 文档完整 | 4/5 | SKILL.md 详细 |
| 依赖管理 | 4/5 | 标准 Python 库 |
| 可移植性 | 4.5/5 | 易集成到 OpenClaw |
| 中文支持 | 5/5 | 针对中文优化 |

**综合评分**: 4.4/5 ⭐⭐⭐⭐

---

## 🚀 立即执行计划

| 任务 | 负责 Bot | 预计时间 | 状态 |
|------|---------|---------|------|
| 1. 安装 transformers/torch | 素问 | 5 分钟 | 🔴 待执行 |
| 2. 创建 zhiji-sentiment 技能 | 素问 | 10 分钟 | 🔴 待执行 |
| 3. 修改知几-E 策略引擎 | 知几 | 15 分钟 | 🔴 待执行 |
| 4. 创建 shanmu-reporter 技能 | 素问 | 15 分钟 | 🔴 待执行 |
| 5. 测试情绪分析模块 | 知几 | 10 分钟 | 🔴 待执行 |
| 6. 测试研报生成 pipeline | 山木 | 15 分钟 | 🔴 待执行 |

**总预计**: 70 分钟 (AGI 并行执行可压缩至 20 分钟)

---

**标签**: [分析] [代码] [Awesome Finance Skills] [集成方案]  
**分类**: P0 高价值任务  
**归档**: memory/2026-03-30.md
