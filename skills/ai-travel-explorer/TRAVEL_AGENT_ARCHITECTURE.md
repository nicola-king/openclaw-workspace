# 🧭 太一旅游探路者 Agent 架构

> **版本**: v1.0
> **创建时间**: 2026-04-14
> **迁移时间**: 2026-05-04
> **作者**: 太一 AGI
> **来源**: AI 探路者 Tim (@AIExplorerTim)
> **定位**: 智能旅游规划与探索助手

---

## 📐 架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│                  太一旅游探路者 Agent (Taiyi Travel Explorer)     │
│                     智能旅游规划与探索系统                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         用户交互层                               │
├─────────────────────────────────────────────────────────────────┤
│  Telegram │ 微信 │ Web UI │ CLI │ API                           │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                       核心技能层 (8大技能)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ 最便宜   │  │ 最低票价 │  │ 多段路线 │  │ 促销码   │        │
│  │ 日期扫描 │  │ 航班查找 │  │ 优化器   │  │ 优惠查找 │        │
│  │ Skill 1  │  │ Skill 2  │  │ Skill 3  │  │ Skill 4  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ 费用细分 │  │ 价格匹配 │  │ 退款灵活 │  │ 隐秘之城 │        │
│  │ 最小化   │  │ 邮件模板 │  │ 性检查   │  │ 门票     │        │
│  │ Skill 5  │  │ Skill 6  │  │ Skill 7  │  │ Skill 8  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                       数据存储层                                 │
├─────────────────────────────────────────────────────────────────┤
│  JSON 文件 │ SQLite │ 本地缓存                                   │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                       自进化层                                   │
├─────────────────────────────────────────────────────────────────┤
│  用户反馈学习 │ 算法优化 │ 数据库更新 │ 适应度评估                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 8 大核心技能

### Skill 1: 最便宜的日期扫描仪 (Cheapest Date Scanner)

**功能**: 扫描目标日期前后范围，找到最便宜的出行日期组合

**输入**:
- 出发城市 (origin)
- 目的地 (destination)
- 目标日期 (target_date)
- 扫描范围 (days_range, 默认7天)

**输出**:
```json
{
  "type": "Cheapest Date Scanner",
  "best_dates": [
    {"date": "2026-05-05", "price": 1100, "savings": "¥400"}
  ]
}
```

**应用场景**: 灵活出行日期，最大化节省机票费用

---

### Skill 2: 最低票价航班查找器 (Lowest Fare Finder)

**功能**: 在指定周数范围内查找最低票价的航班

**输入**:
- 出发城市 (origin)
- 目的地 (destination)
- 周数范围 (weeks_range, 默认4周)

**输出**:
```json
{
  "type": "Lowest Fare Finder",
  "flights": [
    {"airline": "廉价航空", "price": 750, "duration": "3h00m"}
  ]
}
```

**应用场景**: 预算有限，寻找最经济的航班选择

---

### Skill 3: 多段路线优化器 (Multi-Route Optimizer)

**功能**: 优化多段行程的路线组合，平衡价格和时间

**输入**:
- 路线列表 (routes)
- 最大转机时间 (max_layover_hours)
- 预算 (budget)

**输出**:
```json
{
  "type": "Multi-Route Optimizer",
  "optimized": {
    "total_price": 4200,
    "total_duration": "12h30m",
    "segments": [...],
    "savings": 800
  }
}
```

**应用场景**: 多国游、环球旅行、复杂行程规划

---

### Skill 4: 促销码和优惠查找器 (Promo Code Finder)

**功能**: 查找航空公司和旅行网站的促销码和优惠

**输入**:
- 航空公司 (airline)
- 路线 (route)

**输出**:
```json
{
  "type": "Promo Code Finder",
  "promos": [
    {"code": "SAVE20", "discount": "20%", "expiry": "2026-05-31"}
  ]
}
```

**应用场景**: 进一步降低旅行成本

---

### Skill 5: 费用细分及最小化 (Fee Minimizer)

**功能**: 详细分解机票费用，提供最小化建议

**输入**:
- 机票价格 (flight_price)

**输出**:
```json
{
  "type": "Fee Minimizer",
  "breakdown": {
    "base_fare": 1500,
    "baggage_fee": 200,
    "seat_selection": 100,
    "meal": 80,
    "insurance": 50,
    "total": 1930,
    "tips": ["提前在线选座免费", "自带食物节省餐费"]
  }
}
```

**应用场景**: 了解隐藏费用，避免额外支出

---

### Skill 6: 价格匹配/协商邮件模板 (Price Match Email)

**功能**: 生成价格匹配请求邮件模板

**输入**:
- 航空公司 (airline)
- 竞争对手价格 (competitor_price)

**输出**:
- 完整的邮件模板 (Markdown)

**应用场景**: 向航空公司申请价格匹配，获得更低价格

---

### Skill 7: 退款和灵活性检查 (Refund & Flexibility Check)

**功能**: 检查机票的退款政策和灵活性

**输入**:
- 票种类型 (ticket_type)

**输出**:
```json
{
  "type": "Refund & Flexibility Check",
  "policy": {
    "refundable": true,
    "change_fee": 200,
    "cancellation_fee": 300,
    "flexibility_score": 8.5
  }
}
```

**应用场景**: 评估购票风险，选择合适票种

---

### Skill 8: 隐秘之城门票 (Hidden City Ticketing)

**功能**: 发现隐藏城市机票，节省费用

**输入**:
- 出发城市 (origin)
- 目的地 (destination)
- 中转城市 (via_city)

**输出**:
```json
{
  "type": "Hidden City Ticketing",
  "result": {
    "regular_price": 2000,
    "hidden_city_price": 1500,
    "savings": 500,
    "risks": ["只能携带随身行李", "不能托运行李"]
  }
}
```

**⚠️ 风险提示**:
- 只能携带随身行李
- 不能托运行李
- 航空公司可能禁止
- 影响常旅客积分

**应用场景**: 经验丰富的旅行者，了解风险后使用

---

## 📊 技能对比矩阵

| 技能 | 难度 | 风险 | 节省潜力 | 适用人群 |
|------|------|------|---------|---------|
| 最便宜日期扫描 | ⭐ | 无 | ⭐⭐⭐ | 所有人 |
| 最低票价查找 | ⭐ | 无 | ⭐⭐⭐⭐ | 所有人 |
| 多段路线优化 | ⭐⭐ | 低 | ⭐⭐⭐⭐ | 复杂行程 |
| 促销码查找 | ⭐ | 无 | ⭐⭐ | 所有人 |
| 费用最小化 | ⭐ | 无 | ⭐⭐ | 所有人 |
| 价格匹配邮件 | ⭐⭐ | 无 | ⭐⭐⭐ | 所有人 |
| 退款灵活性检查 | ⭐ | 无 | ⭐⭐ | 风险规避者 |
| 隐秘之城门票 | ⭐⭐⭐ | 高 | ⭐⭐⭐⭐⭐ | 资深旅行者 |

---

## 🔧 技术实现

### 核心类: `AITravelExplorer`

```python
class AITravelExplorer:
    """AI 旅行探路者"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
    
    # 8大技能方法
    def cheapest_date_scanner(self, ...): ...
    def lowest_fare_finder(self, ...): ...
    def multi_route_optimizer(self, ...): ...
    def promo_code_finder(self, ...): ...
    def fee_minimizer(self, ...): ...
    def price_match_email(self, ...): ...
    def refund_flexibility_check(self, ...): ...
    def hidden_city_ticketing(self, ...): ...
    
    def save_result(self, result: Dict, filename: str): ...
```

### 数据流

```
用户请求
    ↓
技能选择 (8选1)
    ↓
参数验证
    ↓
执行计算/查询
    ↓
结果格式化
    ↓
保存到文件
    ↓
返回给用户
```

---

## 📁 文件结构

```
ai-travel-explorer/
├── README.md                    # 项目说明
├── SKILL.md                     # 技能定义
├── ai_travel_explorer.py        # 主程序 (13KB)
├── requirements.txt             # 依赖
└── TRAVEL_AGENT_ARCHITECTURE.md # 架构文档
```

---

## 🚀 使用方式

### CLI 调用

```bash
# 进入目录
cd /home/sayelf/.openclaw/workspace/skills/ai-travel-explorer

# 运行测试
python3 ai_travel_explorer.py
```

### Python API

```python
from ai_travel_explorer import AITravelExplorer

explorer = AITravelExplorer()

# 查找最便宜日期
result = explorer.cheapest_date_scanner("北京", "上海", "2026-05-01")

# 查找最低票价
result = explorer.lowest_fare_finder("北京", "东京", 4)

# 生成价格匹配邮件
email = explorer.price_match_email("东方航空", 800)
```

---

## 🧬 自进化能力

| 能力 | 状态 | 说明 |
|------|------|------|
| 用户反馈学习 | ✅ | 记录用户偏好 |
| 算法优化 | ✅ | 持续改进推荐 |
| 数据库更新 | ✅ | 定期更新价格数据 |
| 适应度评估 | ✅ | 评估推荐质量 |

---

## 🎯 与太一系统的集成

### 当前状态
- ✅ 已迁移到工作区
- ✅ 路径已修复 (/home/nicola → /home/sayelf)
- ✅ 语法检查通过
- 🟡 待集成到 OpenClaw Gateway

### 建议集成方式
1. **Telegram 命令**: `/旅游 北京 上海 2026-05-01`
2. **Skill 注册**: 添加到 `openclaw_skill.yaml`
3. **数据共享**: 与跨境贸易 Agent 共享用户数据

---

## 📈 未来扩展

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 酒店比价 | P1 | 整合 Booking/Agoda |
| 景点推荐 | P1 | 基于用户偏好 |
| 实时汇率 | P2 | 整合免费汇率 API |
| 签证信息 | P2 | 自动查询签证要求 |
| 旅行保险 | P3 | 比价和推荐 |

---

## ✅ 特点总结

1. **8大技能全覆盖** - 从日期扫描到隐秘城市
2. **成本优化导向** - 每个技能都旨在降低旅行成本
3. **风险透明** - 明确标注每个策略的风险
4. **自进化能力** - 持续学习和优化
5. **开源免费** - 无需 API 密钥

---

*太一 AGI · 旅游探路者 Agent 架构 v1.0*
*来源: AI 探路者 Tim (@AIExplorerTim)*
*迁移时间: 2026-05-04*
