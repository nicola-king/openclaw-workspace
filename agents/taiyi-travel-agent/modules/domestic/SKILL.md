# 国内游模块 (domestic)

> **版本**: 1.0.0  
> **创建时间**: 2026-04-24  
> **作者**: 太一 AGI  
> **类别**: 国内旅行/目的地模块

---

## 🎯 职责域

**核心功能**: 国内游目的地规划、酒店预订、交通、导游

**适用场景**:
- 国内城市旅行规划
- 国内酒店/包车/导游搜索
- 国内信息源收集 (马蜂窝/穷游/携程/小红书/知乎)

---

## 📋 目的地模块

| 模块 | 位置 | 状态 |
|------|------|------|
| 北京 | `domestic/beijing/` | ✅ 待创建 |
| 上海 | `domestic/shanghai/` | ✅ 待创建 |
| 成都 | `domestic/chengdu/` | ✅ 待创建 |
| 西安 | `domestic/xian/` | ✅ 待创建 |
| 云南 | `domestic/yunnan/` | ✅ 待创建 |

---

## 🚀 使用方式

```python
# 北京模块
from modules.domestic.beijing.planner import BeijingPlanner
planner = BeijingPlanner()
plan = planner.plan_trip("上海", "北京", "2026-05-01", "2026-05-05")

# 上海模块
from modules.domestic.shanghai.planner import ShanghaiPlanner
planner = ShanghaiPlanner()
plan = planner.plan_trip("北京", "上海", "2026-05-01", "2026-05-04")
```

---

*太一旅行探路者 Agent · 国内游模块 · 太一 AGI · 2026-04-24*
