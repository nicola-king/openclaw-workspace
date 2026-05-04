# 📈 跨境贸易 Agent - 智能选品发现规则

> **版本**: v1.0  
> **创建**: 2026-04-18 20:40  
> **状态**: ✅ 规则已有，待配置定时

---

## 📊 现有规则总结

### 1. 产品趋势预测引擎

**文件**: `product_trend_forecaster.py`

**核心功能**:
```
✅ 时间序列分析 (12 个月历史数据)
✅ 趋势阶段判断 (上升期/成熟期/衰退期/季节性)
✅ 生命周期预测
✅ 季节性波动检测
✅ 智能推送频率判断
```

---

### 推送频率规则

| 趋势阶段 | 增长率 | 推送频率 | 紧急程度 | 原因 |
|---------|--------|---------|---------|------|
| **上升期** | >20% | **每日** | 🔴 高 | 快速增长期，需密切监控 |
| **上升期** | 10-20% | **每周** | 🟡 中 | 上升期，定期关注 |
| **成熟期** | -5-10% | **每周** | 🟢 低 | 成熟期，稳定监控 |
| **衰退期** | <-5% | **每月** | 🟢 低 | 衰退期，准备退出 |

---

### 季节性调整规则

```python
# Q4 旺季 (10-12 月)
if current_month in [10, 11, 12]:
    if frequency == "weekly":
        frequency = "daily"  # 增加监控频率
        urgency = "high"
        reason = "Q4 旺季，增加监控频率"
```

**旺季系数**:
| 季度 | 月份 | 系数 | 名称 |
|------|------|------|------|
| Q1 | 1-3 月 | 0.9x | 淡季 (春节) |
| Q2 | 4-6 月 | 1.0x | 平稳期 |
| Q3 | 7-9 月 | 1.1x | 旺季前奏 |
| Q4 | 10-12 月 | 1.5x | 旺季 (黑五/圣诞) |

---

### 产品类型判断

```python
# 夏季产品
if "杯" in product or "water" in product.lower():
    peak_season = "Q3"  # 夏季旺季

# 冬季产品
if "暖" in product or "heater" in product.lower():
    peak_season = "Q4"  # 冬季旺季

# 默认
else:
    peak_season = "Q4"  # 黑五/圣诞
```

---

### 2. 情报汇报系统

**文件**: `intelligence_reporter.py`

**汇报类型**:

| 类型 | 时间 | 内容 | 状态 |
|------|------|------|------|
| **每日简报** | 08:00 | 今日热点/价格波动/竞品动态 | ⏳ 待配置 |
| **每周汇总** | 周一 09:00 | 周报/趋势分析/策略建议 | ⏳ 待配置 |
| **每月战略** | 月初 10:00 | 月报/市场战略/产品规划 | ⏳ 待配置 |
| **重要情报** | 实时 | 紧急竞品动态/价格异常 | ⏳ 待配置 |

---

### 智能选品监控内容

```
🔥 今日热点

1️⃣ 智能选品动态
   • 监控产品：3 个
   • 上升趋势：2 个
   • 下降趋势：1 个

2️⃣ 价格波动
   • 原材料价格：稳定
   • 物流成本：-5%
   • 平台佣金：无变化

3️⃣ 智能选品动态
   • 新进入者：2 家
   • 价格调整：1 家
   • 促销活动：3 家

📊 今日数据
销量：150 件 (+12%)
收入：$5,999 (+15%)
利润：$3,599 (+18%)
```

---

## 🎯 推送规则详解

### 规则 1: 趋势阶段判断

```python
if growth_rate > 0.1:
    trend_stage = "rising"      # 上升期
elif growth_rate > -0.05:
    trend_stage = "peak"        # 成熟期
else:
    trend_stage = "declining"   # 衰退期
```

**计算公式**:
```
增长率 = (近 3 月平均需求 - 前 3 月平均需求) / 前 3 月平均需求
```

---

### 规则 2: 推送频率生成

```python
if trend_stage == "rising" and growth_rate > 0.2:
    frequency = "daily"    # 每日
    urgency = "high"
elif trend_stage == "rising":
    frequency = "weekly"   # 每周
    urgency = "medium"
elif trend_stage == "peak":
    frequency = "weekly"   # 每周
    urgency = "low"
else:  # declining
    frequency = "monthly"  # 每月
    urgency = "low"
```

---

### 规则 3: 行动项目生成

```python
# 高紧急度
if urgency == "high":
    items = [
        "每日监控销量变化",
        "关注竞争对手动态",
        "准备快速补货",
    ]

# 中紧急度
elif urgency == "medium":
    items = [
        "每周审查销售数据",
        "优化产品 listing",
        "调整广告策略",
    ]

# 低紧急度
else:
    items = [
        "每月审查整体表现",
        "评估是否继续",
        "准备替代产品",
    ]
```

---

## 📋 定时任务配置建议

### Cron 配置

```bash
# 每日情报简报 (08:00)
0 8 * * * cd /home/sayelf/.openclaw/workspace && python3 skills/01-trading/cross-border-trade-agent/intelligence_reporter.py --daily

# 每周趋势分析 (周一 09:00)
0 9 * * 1 cd /home/sayelf/.openclaw/workspace && python3 skills/01-trading/cross-border-trade-agent/product_trend_forecaster.py --weekly

# 每月战略报告 (月初 10:00)
0 10 1 * * cd /home/sayelf/.openclaw/workspace && python3 skills/01-trading/cross-border-trade-agent/intelligence_reporter.py --monthly

# 竞品监控 (每 4 小时)
0 */4 * * * cd /home/sayelf/.openclaw/workspace && python3 skills/01-trading/cross-border-trade-agent/intelligence_reporter.py --competitor
```

---

### 监控产品列表

```json
{
  "products": [
    {
      "name": "智能水杯",
      "category": "家居",
      "trend_stage": "rising",
      "growth_rate": 0.25,
      "frequency": "daily",
      "monitor_since": "2026-03-01"
    },
    {
      "name": "瑜伽垫",
      "category": "运动",
      "trend_stage": "rising",
      "growth_rate": 0.15,
      "frequency": "weekly",
      "monitor_since": "2026-03-15"
    },
    {
      "name": "LED 台灯",
      "category": "家居",
      "trend_stage": "peak",
      "growth_rate": 0.05,
      "frequency": "weekly",
      "monitor_since": "2026-02-01"
    }
  ]
}
```

---

## 🚀 使用示例

### 手动执行趋势分析

```bash
# 分析单个产品
python3 product_trend_forecaster.py --product "智能水杯"

# 分析多个产品
python3 product_trend_forecaster.py --products "智能水杯，瑜伽垫，LED 台灯"

# 生成完整报告
python3 product_trend_forecaster.py --report "智能水杯"
```

---

### 输出示例

```
📈 分析时间序列：智能水杯 (12 个月)

   近 3 月平均需求：1250
   增长率：25.3%
   趋势阶段：上升期
   建议行动：立即进入
   置信度：85%

🔄 预测产品生命周期
   当前阶段：rising
   剩余时间：6 个月
   生命周期进度：67%
   退出策略：在衰退期前 1 个月退出

🌤️ 检测季节性
   旺季：7-9 月
   旺季系数：1.1x
   最佳上架时间：Q3 前 2-3 个月

📮 生成推送建议
   推送频率：每日
   紧急程度：高
   原因：快速增长期，需密切监控
   下次审查：2026-04-19
```

---

## 📊 报告存储

**位置**: `/home/sayelf/.openclaw/workspace/data/cross-border/product-trends/`

**格式**: `{产品名}-{日期}.json`

**示例**:
```
data/cross-border/product-trends/
├── 智能水杯 -20260418.json
├── 瑜伽垫 -20260418.json
└── LED 台灯 -20260418.json
```

---

## 🎊 总结

### 现有规则

```
✅ 趋势分析规则 - product_trend_forecaster.py
✅ 推送频率规则 - 根据增长率动态调整
✅ 季节性规则 - Q4 旺季系数 1.5x
✅ 情报汇报规则 - intelligence_reporter.py
✅ 竞品监控规则 - 每日/每周/每月
```

---

### 待配置

```
⏳ Cron 定时任务
⏳ Telegram 推送集成
⏳ 监控产品列表配置
⏳ 数据源接入 (真实销售数据)
```

---

### 下一步行动

```
1. 配置 Cron 定时任务
2. 测试 Telegram 推送
3. 添加监控产品列表
4. 接入真实数据源
```

---

**📈 跨境贸易 Agent - 竞品/畅销品发现规则 v1.0 · 2026-04-18 20:40**

**✅ 规则已有！待配置定时任务！**
