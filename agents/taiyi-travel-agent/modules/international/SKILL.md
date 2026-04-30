# 国外游模块 (international)

> **版本**: 1.0.0  
> **创建时间**: 2026-04-24  
> **作者**: 太一 AGI  
> **类别**: 跨国旅行/目的地模块

---

## 🎯 职责域

**核心功能**: 国外游目的地规划、酒店预订、交通、导游

**适用场景**:
- 跨国城市旅行规划
- 国外酒店/包车/导游搜索
- 国外信息源收集 (TripAdvisor/Lonely Planet/Booking/Airbnb)

---

## 📋 目的地模块

| 模块 | 位置 | 状态 |
|------|------|------|
| 东京 | `international/tokyo/` | ✅ 待创建 |
| 首尔 | `international/seoul/` | ✅ 待创建 |
| 曼谷 | `international/bangkok/` | ✅ 待创建 |
| 新加坡 | `international/singapore/` | ✅ 待创建 |
| 大阪 | `international/osaka/` | ✅ 待创建 |
| 京都 | `international/kyoto/` | ✅ 待创建 |
| 普吉岛 | `international/phuket/` | ✅ 待创建 |
| 巴厘岛 | `international/bali/` | ✅ 待创建 |

---

## 🚀 使用方式

```python
# 东京模块
from modules.international.tokyo.planner import TokyoPlanner
planner = TokyoPlanner()
plan = planner.plan_trip("北京", "东京", "2026-05-01", "2026-05-07")

# 首尔模块
from modules.international.seoul.planner import SeoulPlanner
planner = SeoulPlanner()
plan = planner.plan_trip("北京", "首尔", "2026-05-01", "2026-05-06")
```

---

*太一旅行探路者 Agent · 国外游模块 · 太一 AGI · 2026-04-24*
