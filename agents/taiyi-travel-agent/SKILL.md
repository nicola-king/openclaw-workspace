# 太一旅行探路者 Agent v2.0


> **名称**: taiyi-travel-agent
> **版本**: 2.0.0
> **作者**: 太一 AGI
> **描述**: 模块化自进化旅行规划系统

---

## 📋 模块列表


| 模块 | 路径 | 描述 |
|------|------|------|
| 智能行程规划 | `src/planner/` | 核心规划引擎、预算管理、旅行清单、天气 |
| 多城路线优化 | `src/router_core/` | TSP/VRP 路线优化 |
| 优惠发现 | `src/deals/` | 机票/酒店优惠扫描 |
| 地接服务 | `src/ground/` | 包车/接机/导游/租车/全包套餐 |
| 供应商管理 | `src/provider/` | 供应商注册/审核/搜索 |
| 信息蒸馏 | `src/distill/` | 9源融合（马蜂窝/穷游/携程/小红书/知乎/TripAdvisor/Lonely Planet/Booking/Airbnb） |
| 自进化引擎 | `src/evolve/` | 经验存储/模式识别/自动优化/涌现检测/技能生成 |
| 多平台推送 | `src/push/` | Telegram/微信推送 |
| 目的地注意事项 | `src/destination/` | 民俗/法律/禁忌/安全 |
| 双模式策略 | `src/dual_mode/` | 国内/国际模式切换 |
| 知识自动学习 | `src/learn/` | 博主内容/网站内容学习 |

---

## 🚀 使用方式


### 安装


```bash
cd agents/taiyi-travel-agent
pip install -e .
```

### 统一入口


```python
from src.router import TravelRouter, IntentCategory
from src.planner.engine import PlannerEngine
from src.evolve.experience_store import ExperienceStore

# 初始化

router = TravelRouter()
planner = PlannerEngine()
store = ExperienceStore()

# 路由规划

plan = planner.plan_trip(
    origin="北京", destination="东京",
    start_date="2026-05-01", end_date="2026-05-07",
    budget=15000, travelers=2,
)

# 记录经验

store.record_trip(
    destination="东京", origin="北京",
    budget=15000, travelers=2,
    start_date="2026-05-01", end_date="2026-05-07",
    rating=4.8, feedback="非常好",
)
```

## CLI


```bash

# 供应商管理

python -m src.provider.cli register hotel --name "东京大酒店" --location "东京" --price 800

# 运行测试

python -m pytest tests/
```

---

## 🧬 自进化机制


### 经验存储 (`src/evolve/experience_store.py`)

- 每次旅行后自动记录决策、结果、用户反馈
- JSONL 追加写入 + SQLite 查询
- 支持按目的地/时间/评分查询

### 模式识别 (`src/evolve/pattern_recognition.py`)

- 分析历史经验，发现规律
- "XX 季节去 XX 预算最优"
- "XX 目的地评分最高"
- "XX 预算区间最受欢迎"

### 自动优化 (`src/evolve/auto_optimizer.py`)

- 根据模式自动调整推荐权重
- 热门目的地 + 高评分 = 高推荐

### 涌现检测 (`src/evolve/emergence_detector.py`)

- 目的地请求频率 > 阈值 → 创建新目的地模块
- 预算模式异常 → 创建预算优化技能
- 高评分目的地 → 创建推荐技能

### 技能生成 (`src/evolve/skill_generator.py`)

- 自动创建新 Skill 文件 (SKILL.md + Python 代码)
- 记录到 `data/experience/skills/`

---

## 📁 目录结构


```
agents/taiyi-travel-agent/
├── SKILL.md                    # 本文件
├── pyproject.toml              # 包管理
├── src/                        # 源代码
│   ├── router.py               # 统一路由
│   ├── planner/                # 智能行程规划
│   ├── router_core/            # 多城路线优化
│   ├── deals/                  # 优惠发现
│   ├── ground/                 # 地接服务
│   ├── provider/               # 供应商管理
│   ├── distill/                # 信息蒸馏
│   ├── evolve/                 # 自进化引擎 ⭐
│   ├── push/                   # 多平台推送
│   ├── destination/            # 目的地注意事项
│   ├── dual_mode/              # 双模式策略
│   └── learn/                  # 知识自动学习
├── destinations/               # 目的地数据
│   ├── domestic/               # 国内目的地
│   └── international/          # 国际目的地
├── data/                       # 运行时数据
│   ├── experience/             # 经验存储 ⭐
│   ├── providers/              # 供应商数据
│   ├── distillation/           # 蒸馏结果
│   ├── evolution/              # 进化数据
│   ├── auto-learning/          # 学习数据
│   └── attractions/            # 景点数据
├── emerged-skills/             # 涌现技能（保留）
├── examples/                   # 示例
├── reports/                    # 报告
├── tests/                      # 测试
└── scripts/                    # 脚本
```

---

## 📄 模块 SKILL.md


每个子模块都有独立的 `SKILL.md`，可单独发布：
- `src/planner/SKILL.md`
- `src/router_core/SKILL.md`
- `src/deals/SKILL.md`
- `src/ground/SKILL.md`
- `src/provider/SKILL.md`
- `src/distill/SKILL.md`
- `src/evolve/SKILL.md`
- `src/push/SKILL.md`
- `src/destination/SKILL.md`
- `src/dual_mode/SKILL.md`
- `src/learn/SKILL.md`

---

*太一旅行探路者 Agent · v2.0.0 · 太一 AGI*


---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 17:41