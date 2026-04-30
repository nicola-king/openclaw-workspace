# 地接服务模块 (ground)



> **名称**: taiyi-travel-ground  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 落地服务——包车/接机/导游/租车/全包套餐


## 🎯 职责域



**核心功能**: 包车服务、接机服务、导游服务、租车服务、全包套餐

**适用场景**:
- 目的地包车/导游搜索
- 机场接机安排
- 租车预订
- 全包套餐推荐


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `charter.py` | 包车服务 |
| `airport_pickup.py` | 接机服务 |
| `guide.py` | 导游服务 |
| `car_rental.py` | 租车服务 |
| `packages.py` | 全包套餐 |


## 🚀 使用方式



```python
from src.ground.charter import CharterService
from src.ground.guide import GuideService

charter = CharterService()
options = charter.search(destination="东京", days=5, car_type="舒适型")

guide = GuideService()
guides = guide.search(destination="东京", language="中文/英文")
```


## 🔌 依赖



- 无外部依赖


## 📦 发布



```bash
clawhub publish taiyi-travel-ground
```


*太一旅行探路者 · 地接服务模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48