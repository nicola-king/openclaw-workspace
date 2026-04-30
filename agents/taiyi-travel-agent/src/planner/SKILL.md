# 智能行程规划模块 (planner)



> **名称**: taiyi-travel-planner  
> **版本**: 2.0.0  
> **作者**: 太一 AGI  
> **描述**: 智能旅行规划引擎——预算管理、旅行清单、天气集成


## 🎯 职责域



**核心功能**: 旅行行程规划、预算分配、旅行清单生成、天气查询

**适用场景**:
- 根据出发地/目的地/日期/预算自动生成行程
- 预算分配（交通/住宿/餐饮/景点/购物）
- 旅行清单生成（证件/衣物/药品/电子）
- 目的地天气查询


## 📋 模块结构



| 文件 | 职责 |
|------|------|
| `engine.py` | 核心规划引擎（行程生成、景点排期） |
| `budget.py` | 预算管理（预算分配、费用估算） |
| `checklist.py` | 旅行清单（证件/衣物/药品/电子） |
| `weather.py` | 天气集成（目的地天气查询） |


## 🚀 使用方式



### 作为 Skill 加载



```python
from src.planner.engine import PlannerEngine
from src.planner.budget import BudgetManager
from src.planner.checklist import ChecklistGenerator
from src.planner.weather import WeatherChecker

planner = PlannerEngine()
plan = planner.plan_trip(
    origin="北京", destination="东京",
    start_date="2026-05-01", end_date="2026-05-07",
    budget=15000, travelers=2
)
```

### 独立使用



```python

# 预算管理


budget = BudgetManager()
allocation = budget.allocate(budget=15000, days=7, travelers=2)

# 旅行清单


checklist = ChecklistGenerator()
items = checklist.generate(destination="东京", season="春", days=7)

# 天气查询


weather = WeatherChecker()
forecast = weather.get_weather(destination="东京", dates=["2026-05-01", "2026-05-02"])
```


## 🔌 依赖



- 无外部依赖（纯 Python）
- 可选：APILayer API（天气/汇率）


## 📦 发布



可作为独立 Skill 发布到 ClawHub：

```bash
clawhub publish taiyi-travel-planner
```


*太一旅行探路者 · 智能行程规划模块 · 太一 AGI · 2026-04-25*



> 美学过滤器自动处理 · 2026-04-25 18:48

---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48