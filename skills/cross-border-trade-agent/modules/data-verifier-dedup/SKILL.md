# P1 数据验证去重中心

> **版本**: 1.0.0
> **创建**: 2026-05-25 (P1 数据验证去重)
> **职责**: 数据验证 + 合并去重 + 质量评分 三位一体

---

## 核心能力

| # | 能力 | 类 | 描述 |
|---|------|-----|------|
| 1 | **验证** | `DataVerifier` | ABN/官网/电话/邮箱/名称 多源交叉验证 → 可信度评分 |
| 2 | **去重** | `DataDeduper` | 同名/同网址/同邮箱自动合并，保留最优字段 |
| 3 | **质量** | `DataQuality` | 完整度/新鲜度/唯一性/一致性 多维度评分 |
| 4 | **管道** | `DataVerifierDeduper` | 验证→去重→质量 全流程一键出报告 |

---

## 使用

```python
from modules.data-verifier-dedup.core import DataVerifier, DataDeduper, DataQuality

# 验证
result = DataVerifier.verify_company(
    name="Crystalbrook Collection Pty Ltd",
    website="crystalbrookcollection.com", 
    abn="12345678901"
)

# 去重
records = [{"name": "Aus Modular", "website": "ausmodular.com.au"}, ...]
result = DataDeduper.dedup_records(records)

# 质量评分
quality = DataQuality.assess_dataset(records)
```

## CLI

```bash
python3 core.py --test            # 测试
python3 core.py --verify '公司名'  # 验证公司
python3 core.py --dedup-file data.json  # 去重文件
```
