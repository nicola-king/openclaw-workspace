---
skill: ecommerce-workflow
version: 1.0.0
author: 太一 AGI
created: 2026-04-06
status: active
tags: ['电商，工作流，Medusa，n8n，changedetection，Chatwoot']
category: general
---



# 电商工作流 Skill

> 一人电商团队自动化工作流

---

## 📊 功能概述

整合电商工具链，实现:
- 竞品监控 (changedetection)
- 商品管理 (Medusa)
- 工作流自动化 (n8n)
- 客服自动化 (Chatwoot)

---

## 🛠️ 技术栈

| 组件 | 用途 | 状态 |
|------|------|------|
| Medusa | 电商后台 | ✅ API 封装完成 |
| changedetection | 价格监控 | 🟡 待集成 |
| n8n | 工作流引擎 | 🟡 待部署 |
| Chatwoot | 客服系统 | 🟡 待集成 |

---

## 🔧 核心功能

### 1. 商品管理
```python
from medusa_client import MedusaClient

client = MedusaClient(
    base_url="https://your-store.com",
    api_token="your_token"
)

# 创建商品
product = await client.create_product({
    "title": "T-Shirt",
    "price": 2999
})

# 更新库存
await client.update_inventory(product_id, quantity=100)
```

### 2. 竞品监控
```python
# changedetection 集成
async def monitor_competitor_prices():
    urls = [
        "https://competitor1.com/product/123",
        "https://competitor2.com/product/456"
    ]
    
    for url in urls:
        price = await get_price(url)
        if price_change_detected(price):
            await notify_price_change(url, price)
```

### 3. 自动工作流
```python
# n8n 工作流触发
async def auto_workflow(event):
    if event == "new_order":
        await send_confirmation_email()
        await update_inventory()
        await notify_shipping()
    elif event == "low_stock":
        await create_purchase_order()
```

### 4. 客服自动化
```python
# Chatwoot 集成
async def handle_customer_message(message):
    intent = classify_intent(message)
    
    if intent == "order_status":
        response = await get_order_status(message.user_id)
    elif intent == "return_request":
        response = await process_return(message)
    else:
        response = await forward_to_human(message)
    
    await send_response(response)
```

---

## 📋 使用示例

### 场景 1: 新品上架
```python
# 1. 创建商品
product = await client.create_product({
    "title": "新款 T 恤",
    "description": "100% 纯棉",
    "price": 2999,
    "images": ["img1.jpg", "img2.jpg"]
})

# 2. 设置竞品监控
await monitor_competitor_prices([
    "https://competitor.com/similar-product"
])

# 3. 配置自动工作流
await n8n.create_workflow("new_product_launch")
```

### 场景 2: 价格调整
```python
# 监控到竞品降价
competitor_price = await get_competitor_price()

if competitor_price < our_price * 0.9:
    # 自动调价
    await client.update_product(product_id, {
        "price": int(competitor_price * 0.95)
    })
    # 通知运营
    await notify_team("价格已自动调整")
```

---

## 🔗 集成文档

- Medusa API: `integrations/medusa/medusa_client_full.py`
- 工作流计划：`skills/ecommerce-workflow/PLAN.md`
- 分析报告：`reports/github-daily-deep-analysis-20260406.md`

---

## 📝 待办事项

- [ ] changedetection 集成
- [ ] n8n Docker 部署
- [ ] Chatwoot API 封装
- [ ] 端到端测试

---

*创建时间：2026-04-06 01:00 | 太一 AGI*
