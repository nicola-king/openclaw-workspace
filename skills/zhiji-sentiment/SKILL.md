---
name: zhiji-sentiment
description: 金融情绪分析 (FinBERT/LLM) - 为知几-E 策略提供情绪因子增强
version: 1.0.0
author: 太一 (集成自 Awesome Finance Skills)
category: other
---



# 知几 - 情绪分析技能

## 🎯 核心功能

为知几-E 量化交易策略提供情绪分析能力，支持两种模式：

| 模式 | 速度 | 准确度 | 使用场景 |
|------|------|--------|---------|
| **FinBERT** | ⚡ 快 (本地) | 85% | 批量新闻分析 |
| **LLM** | 🐢 慢 (API) | 95% | 关键决策分析 |

## 📊 情绪评分标准

```
-1.0 ~ -0.1: 负面情绪 (利空)
-0.1 ~ +0.1: 中性情绪
+0.1 ~ +1.0: 正面情绪 (利多)
```

## 🔧 使用方法

### 模式 1: FinBERT 批量分析 (推荐)

```python
from scripts.sentiment_tools import SentimentTools
from scripts.database_manager import DatabaseManager

db = DatabaseManager("polymarket.db")
sentiment = SentimentTools(db, mode="auto")

# 单条分析
result = sentiment.analyze_sentiment("BTC 突破 10 万美元大关")
# 返回：{"score": 0.85, "label": "positive", "reason": "BERT automated analysis"}

# 批量分析
texts = ["新闻 1", "新闻 2", "新闻 3"]
results = sentiment.analyze_sentiment_bert(texts)
```

### 模式 2: LLM 手动分析 (高准确度)

```python
# Agent 直接使用 Prompt 分析
prompt = """
请分析以下金融/新闻文本的情绪极性。
返回严格的 JSON 格式:
{"score": <float: -1.0 到 1.0>, "label": "<positive/negative/neutral>", "reason": "<简短理由>"}

文本：{text}
"""

# 保存结果到数据库
sentiment.update_single_news_sentiment(news_id=123, score=0.75, reason="利多消息")
```

## 🧠 集成到知几-E 策略

### 综合置信度计算

```python
def calculate_enhanced_confidence(weather_confidence, sentiment_score, news_weight=0.1):
    """
    气象置信度 + 新闻情绪综合计算
    
    Args:
        weather_confidence: 气象数据置信度 (0-1)
        sentiment_score: 新闻情绪分数 (-1 到 1)
        news_weight: 情绪权重 (默认 0.1)
    
    Returns:
        enhanced_confidence: 综合置信度 (0-1)
    """
    sentiment_boost = sentiment_score * news_weight
    return min(1.0, max(0.0, weather_confidence + sentiment_boost))
```

### 动态阈值调整

```python
def get_dynamic_threshold(base_threshold=0.96, sentiment_score):
    """
    根据情绪动态调整下注阈值
    
    正面情绪 → 降低阈值 (更激进)
    负面情绪 → 提高阈值 (更保守)
    """
    adjustment = -sentiment_score * 0.05  # 情绪影响±5%
    return max(0.90, min(0.98, base_threshold + adjustment))
```

## 📦 依赖安装

```bash
pip install transformers torch --break-system-packages
```

## 🗄️ 数据库表结构

```sql
CREATE TABLE daily_news (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    source TEXT,
    sentiment_score REAL,  -- 情绪分数 (-1.0 ~ 1.0)
    meta_data TEXT,        -- JSON: {"sentiment_reason": "..."}
    created_at TIMESTAMP
);
```

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `scripts/sentiment_tools.py` | 情绪分析核心工具 |
| `scripts/database_manager.py` | 数据库管理 |
| `references/prompts.md` | LLM 分析 Prompt 模板 |

## ⚠️ 注意事项

1. **首次运行**: BERT 模型会自动下载 (~400MB)，后续使用本地缓存
2. **内存占用**: FinBERT 推理约需 1GB RAM
3. **速度**: 单条分析 ~50ms (CPU), 批量分析可并行
4. **模式选择**: 
   - 日常批量：用 FinBERT (快)
   - 关键决策：用 LLM (准)

## 📝 更新日志

- **v1.0.0** (2026-03-30): 初始版本，集成自 Awesome Finance Skills
