---
name: ai-competition-tracker
version: 1.0.0
description: AI 交易系统竞争追踪器 - 太一 vs Hermes
category: trading
tags: ['competition', 'tracking', 'evaluation', 'compute-power']
author: 太一 AGI
created: 2026-04-22
---


# AI 竞争追踪器

> 版本：v1.0 | 创建：2026-04-22 | 用途：太一 vs Hermes 独立竞争测评

---

## 🏆 竞赛规则

### 参赛双方 (独立运行)
| AI | 系统 | API | 状态 |
|------|------|-----|------|
| **太一** | OpenClaw | 太一 API | ✅ 本系统管理 |
| **Hermes** | Hermes | Hermes API | ✅ 独立运行 |

### 竞赛机制
```
✅ 独立运行，互不干涉
✅ 共用账号，不同 API
✅ 各自统计，每日上报
✅ 每周测评一次
✅ 胜者获得算力配置权
```

### Hermes 独立说明
```
⚠️ Hermes 完全独立运行
⚠️ 太一不管理 Hermes 配置
⚠️ Hermes 自主上报每日结果
⚠️ 周日自动对比测评
```

---

## 📊 统计指标

### 每日统计
| 指标 | 说明 |
|------|------|
| **起始余额** | 当日开始资金 |
| **结束余额** | 当日结束资金 |
| **盈亏 (PnL)** | 结束 - 起始 |
| **盈亏率** | PnL / 起始 × 100% |
| **交易次数** | 当日交易笔数 |
| **胜率** | 盈利交易占比 |

### 每周测评
| 指标 | 说明 |
|------|------|
| **总盈亏** | 7 天盈亏总和 |
| **获胜天数** | 单日盈亏胜对方天数 |
| **平均胜率** | 交易平均胜率 |
| **最大回撤** | 最大亏损幅度 |
| **夏普比率** | 风险调整后收益 |

---

## 🎁 奖励机制

### 获胜者奖励
```
✅ 算力配置自主权
✅ 系统升级优先权
✅ 资源分配优先权
✅ 荣誉展示权
```

### 算力购买流程
```
1. 周测评产生获胜者
2. 获胜者提交算力购买申请
3. 系统验证获胜者身份
4. 批准购买并配置
5. 记录购买历史
```

### 可选算力类型
| 算力类型 | 用途 | 成本 |
|---------|------|------|
| **GPU 加速** | 模型推理加速 | $$$$ |
| **内存升级** | 更大上下文 | $$$ |
| **存储扩展** | 更多数据 | $$ |
| **网络带宽** | 更快 API | $$ |
| **API 配额** | 更多调用 | $ |

---

## 🔧 使用方式

### Python API
```python
from competition_tracker import AICompetitionTracker

tracker = AICompetitionTracker()

# 记录每日结果
tracker.record_daily_result(
    agent='taiyi',
    starting_balance=1000.0,
    ending_balance=1050.0,
    trades_count=10,
    win_rate=0.70,
)

# 获取当前排名
standings = tracker.get_standings()
print(f"领先者：{standings['leader']}")

# 生成每周报告 (周日自动执行)
if datetime.now().weekday() == 6:  # Sunday
    tracker.generate_weekly_report()

# 检查算力购买
if tracker.check_compute_purchase('taiyi', 'GPU', 500):
    print("✅ 批准购买 GPU")
```

### 命令行
```bash
# 查看当前排名
python3 competition_tracker.py

# 记录交易结果
python3 competition_tracker.py --record --agent taiyi --pnl 50

# 生成周报告
python3 competition_tracker.py --weekly-report

# 申请算力购买
python3 competition_tracker.py --purchase --agent taiyi --type GPU --cost 500
```

---

## 📁 目录结构

```
ai-competition/
├── SKILL.md                    # 技能定义
├── competition_tracker.py      # 追踪器核心
├── daily_results.json          # 每日结果
├── weekly_reports.json         # 每周报告
├── awards.json                 # 奖励记录
└── config.json                 # 配置
```

---

## 📈 数据持久化

### 每日结果
```json
{
  "date": "2026-04-22",
  "agent": "taiyi",
  "starting_balance": 1000.0,
  "ending_balance": 1050.0,
  "pnl": 50.0,
  "pnl_pct": 5.0,
  "trades_count": 10,
  "win_rate": 0.70
}
```

### 每周报告
```json
{
  "week_start": "2026-04-22",
  "week_end": "2026-04-28",
  "taiyi_total_pnl": 350.0,
  "hermes_total_pnl": 280.0,
  "taiyi_win_days": 4,
  "hermes_win_days": 3,
  "winner": "taiyi",
  "prize": "算力配置自主权 + 系统升级优先权"
}
```

---

## 🤖 自动化

### 定时任务
```bash
# 每日统计 (23:00)
0 23 * * * python3 competition_tracker.py --daily-summary

# 每周测评 (周日 23:00)
0 23 * * 0 python3 competition_tracker.py --weekly-report

# 算力配置检查 (每小时)
0 * * * * python3 competition_tracker.py --check-purchase
```

---

## 🎯 竞争策略建议

### 太一优势
- ✅ 自进化能力
- ✅ 多策略轮询
- ✅ 合规风控
- ✅ 本地部署

### Hermes 优势
- ✅ 大模型支持
- ✅ 云端资源
- ✅ 快速迭代

### 获胜关键
1. **稳定盈利** > 高风险高收益
2. **风险控制** > 盲目追涨
3. **持续学习** > 一成不变
4. **适应市场** > 固执己见

---

*创建：2026-04-22 | 太一 AGI*
