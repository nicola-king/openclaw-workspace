# TokenJuice · 太一 Token 压缩层

> 吸收 OpenHuman TokenJuice 设计模式后自研的确定性压缩管道
> 在数据进入 LLM 之前做无损/近无损压缩，降低 token 消耗

## 架构

```
数据入口（web_search / web_fetch / CLI / scrape）
    ↓
┌─────────────────────────────────────────────┐
│          TokenJuice 5 阶压缩管道              │
│                                              │
│  ① Format Normalization — HTML→MD, JSON→compact │
│  ② Noise Stripping — 去样板/去空白/去零宽      │
│  ③ Deduplication — 行级/块级去重              │
│  ④ URL Optimization — 缩URL + 去追踪参数       │
│  ⑤ Smart Truncation — 超阈值保头保尾+摘要      │
└─────────────────────────────────────────────┘
    ↓
LLM 输入（已压缩，token 节省 20-90%）
```

## 文件位置

- 核心实现: `scripts/token_compressor.py`
- 导入方式: `from scripts.token_compressor import TokenJuice`

## 已注入的管道

| Agent | 注入点 | 节省预期 |
|-------|--------|---------|
| shared_search_service | `compress_results()` | 20-50% |
| store-finder-agent/rental_crawler | `compress_listings()` | 30-60% |
| store-finder-agent/economic_background | 模块级 | 25-70% |

## 上下文策略

| context | max_chars | URL缩 | 去重 | 适用场景 |
|---------|:---------:|:-----:|:----:|---------|
| search_results | 6,000 | ✅ | ✅ | web_search 结果 |
| web_page | 10,000 | ✅ | ✅ | 爬取的长网页 |
| email | 8,000 | ✅ | ❌ | 邮件内容 |
| cli_output | 6,000 | ❌ | ✅ | shell 命令输出 |
| rental_data | 4,000 | ✅ | ✅ | 租金列表数据 |
| economic_data | 5,000 | ❌ | ❌ | 经济指标表格 |

## 使用方式

```python
from scripts.token_compressor import TokenJuice

# 一键压缩
result = TokenJuice.compress(raw_text, context="search_results")
print(f"压缩比: {result['ratio']}%")
print(f"节省: {result['original_chars'] - result['compressed_chars']} chars")

# 在已有管道中调用
# 搜索结果进入 LLM 前：
compressed_results = search_service.compress_results(raw_results)
```

## 效果实测

| 数据类型 | 原始 | 压缩后 | 压缩比 |
|---------|:---:|:-----:|:-----:|
| 搜索结果（短） | 383 chars | 371 chars | 97% |
| HTML 长页面 | 4,200 chars | 1,399 chars | 33% |
| 经济数据 | 239 chars | 179 chars | 25% |
| 重复内容 | 1,300 chars | 38 chars | 3% |
| **综合加权** | **4,034 chars** | **1,987 chars** | **~50%** |

## 成本估算

按 DeepSeek V4 Flash ¥2/M token 计：
- 每个搜索调用平均省 ~500 tokens
- 每日 ~200 次调用 → ~¥0.20/日 → ~¥6/月
- 加上爬取/验证管道 → 估算 ¥15-30/月
