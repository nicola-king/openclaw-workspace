---
name: shanmu-reporter
description: 专业金融研报生成 - 规划→写作→编辑→图表自动化 pipeline
version: 1.0.0
author: 太一 (集成自 Awesome Finance Skills)
---

# 山木 - 研报生成技能

## 🎯 核心功能

将零散的金融信号自动转化为专业研报，完整 workflow：

```
信号输入 → 聚类主题 → 章节写作 → 最终组装 → 研报输出
   ↓           ↓           ↓           ↓           ↓
 原始数据    3-5 主题    深度分析    编辑校对    Markdown/PDF
```

## 📊 三阶段 Pipeline

### 阶段 1: Cluster Signals (规划师)

**输入**: 零散金融信号列表  
**输出**: 3-5 个核心主题聚类

**Prompt**:
```markdown
You are a senior financial report editor.
Cluster the following signals into 3-5 core logical themes.

### Input Signals
{signals_text}

### Output Format (JSON)
{
    "clusters": [
        {
            "theme_title": "Theme Name",
            "signal_ids": [1, 3, 5],
            "rationale": "These signals all point to..."
        }
    ]
}
```

---

### 阶段 2: Write Sections (分析师)

**输入**: 单个主题 + 对应信号  
**输出**: 深度分析章节 (含图表配置)

**Prompt**:
```markdown
You are a senior financial analyst.
Write deep analysis for: "{theme_title}"

### Requirements
1. Narrative: Macro → Industry → Stock impact
2. Quantification: Cite confidence scores
3. Charts: Insert 1-2 json-chart blocks

### Chart Example
```json-chart
{"type": "forecast", "ticker": "ETH", "title": "价格预测", "pred_len": 5}
```
```

---

### 阶段 3: Final Assembly (编辑)

**输入**: 所有章节草稿  
**输出**: 完整研报 (含摘要/风险/参考)

**Prompt**:
```markdown
You are a professional editor.
Assemble sections into final report.

### Requirements
1. Structure: H2/H3 hierarchy
2. Summary: Executive Summary + Quick Scan table
3. Risk: Risk Factors section
4. References: Source list
```

---

## 🔧 使用方法

### Python API

```python
from scripts.report_generator import ReportGenerator

generator = ReportGenerator()

# 1. 准备信号
signals = [
    {"id": 1, "text": "BTC 突破 10 万", "confidence": 0.95},
    {"id": 2, "text": "ETH  ETF 通过", "confidence": 0.88},
    # ...
]

# 2. 生成报告
report = generator.generate_report(signals)

# 3. 输出
print(report.markdown)
print(report.charts)  # json-chart 配置列表
```

### Bot 集成 (山木)

```python
# 山木 Bot 接收到创作请求
@shanmu.on("create_report")
async def handle_report_request(signals):
    generator = ReportGenerator()
    report = generator.generate_report(signals)
    
    # 发送到微信/Telegram
    await send_to_wechat(report.markdown)
    await send_charts(report.charts)
```

---

## 📦 输出示例

```markdown
# Polymarket 气象套利分析报告

## Executive Summary

| 主题 | 信号数 | 平均置信度 | 建议操作 |
|------|--------|-----------|---------|
| 极端天气频发 | 5 | 94% | 增持 YES |
| 模型准确性提升 | 3 | 97% | 维持仓位 |

## 主题 1: 极端天气频发

### 宏观背景
2026 年全球气候异常...

### 传导机制
极端天气 → 农业减产 → 食品价格 → 通胀预期

### 对 Polymarket 影响
气象类 YES 合约流动性提升 340%...

```json-chart
{"type": "line", "data": [...], "title": "气象合约流动性趋势"}
```

## 风险因素
1. 模型过拟合风险
2. 流动性风险
3. 黑天鹅事件

## 参考资料
[1] 来源 1
[2] 来源 2
```

---

## 🗄️ 数据库表

```sql
CREATE TABLE report_signals (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    source TEXT,
    confidence REAL,
    cluster_id INTEGER,
    created_at TIMESTAMP
);

CREATE TABLE generated_reports (
    id INTEGER PRIMARY KEY,
    title TEXT,
    markdown TEXT,
    charts_json TEXT,
    created_at TIMESTAMP
);
```

---

## 📦 依赖

- Python 3.10+
- sqlite3 (内置)
- json (内置)

---

## ⚠️ 注意事项

1. **信号质量**: 输入信号需包含 confidence 字段
2. **主题数量**: 自动控制在 3-5 个 (避免过于分散)
3. **图表格式**: json-chart 需符合前端渲染规范
4. **语言**: 默认中文输出，可配置为英文

---

## 📝 更新日志

- **v1.0.0** (2026-03-30): 初始版本，集成自 Awesome Finance Skills
