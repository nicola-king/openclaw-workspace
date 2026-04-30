# 优惠发现模块 (deals)



> **名称**: taiyi-travel-deals  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 机票/酒店优惠扫描与推荐


## 🎯 职责域



**核心功能**: 机票优惠发现、酒店优惠发现、比价推荐

**适用场景**:
- 搜索出发地→目的地的最便宜机票
- 搜索目的地酒店优惠
- 跨平台比价


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `finder.py` | 优惠发现引擎 |


## 🚀 使用方式



```python
from src.deals.finder import DealFinder

finder = DealFinder()
deals = finder.find_deals(origin="北京", destination="东京", dates=["2026-05-01"])
```


## 🔌 依赖



- 无外部依赖


## 📦 发布



```bash
clawhub publish taiyi-travel-deals
```


*太一旅行探路者 · 优惠发现模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48