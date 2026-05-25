# 服务层 v1.0 — P1 合并

> **合并来源**: quote-engine, product-catalog, supplier-matcher, contract-legal, compliance-engine, risk-manager, payment-settlement, transaction-support, supply-chain
> **创建**: 2026-05-25 (P1 合并)
> **状态**: ✅ 3个子服务 → 1个入口

---

## 服务结构

```
service-layer/
  core.py        # 统一入口
  docs/          # 文档
```

### 3 个子服务

| 服务 | 类 | 合并的旧模块 |
|------|-----|------------|
| **Trade** | `TradeService` | quote-engine, product-catalog, supplier-matcher |
| **Legal** | `LegalService` | contract-legal, compliance-engine, risk-manager |
| **Payment** | `PaymentService` | payment-settlement, transaction-support, supply-chain |

### 一键报告

`ServiceLayer.service_report()` — 报价+合规+支付 三合一报告

---

## 使用

```python
from modules.service-layer.core import ServiceLayer, TradeService, LegalService, PaymentService

# 一键报价
quote = TradeService.quote("折叠房屋", 100, "Australia")

# 一键合规三件套
legal = LegalService.full_legal_package("折叠房屋", "Saudi Arabia", 500000)

# 一键报告
report = ServiceLayer.service_report("折叠房屋", 100, "Saudi Arabia",
                                     specs={"total_price_cny": 500000})
```

---

## 旧模块状态

旧模块保留原位（兼容现有引用），但标记为 `[MERGED → service-layer]`。
新代码统一走 `service-layer.core`，不要直接 import 旧模块。
