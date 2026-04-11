# 🎯 Polymarket 自进化交易 Agent

> **版本**: v2.0  
> **作者**: 太一 AGI  
> **定位**: Polymarket 预测市场自进化交易机器人  
> **策略**: 做市/套利/方向性/事件驱动  
> **状态**: 🟡 实盘准备中

---

## 🎯 Agent 定位

**核心能力**:
- 🎯 Polymarket 实盘交易自动化
- 🎯 多策略智能选择 (做市/套利/方向性)
- 🎯 自进化学习 (从交易中学习优化)
- 🎯 7×24 小时不间断交易
- 🎯 严格风控 (止损/仓位/资金)

---

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

```bash
# 编辑配置文件
cp config.example.json config.json
nano config.json

# 填写配置
{
  "capital": 1000,
  "strategies": ["market_making", "arbitrage", "directional"],
  "risk_config": {...}
}
```

### 启动

```bash
# 启动 Agent
python3 polymarket_agent.py

# 或后台运行
nohup python3 polymarket_agent.py &
```

---

## 📊 交易策略

| 策略 | 风险等级 | 预期收益 | 适合市场 |
|------|---------|---------|---------|
| 做市 | 低 | 5-15%/月 | 高流动性 |
| 套利 | 极低 | 2-8%/月 | 多市场 |
| 方向性 | 高 | 20-100%/月 | 高波动 |
| 事件驱动 | 中 | 10-30%/月 | 事件驱动 |

---

## ⚠️ 风控配置

```python
RISK_CONFIG = {
    "max_position_per_market": 100,    # 单市场最大持仓
    "max_total_exposure": 1000,        # 总风险敞口
    "hard_stop_loss": 0.20,            # 硬止损 20%
    "daily_stop_loss": 0.05,           # 日止损 5%
}
```

---

## 🧬 自进化机制

**学习循环**:
```
交易 → 记录 → 分析 → 学习 → 优化 → 交易 (循环)

每笔交易:
- 成功因素提取
- 失败原因分析
- 策略参数优化
- 知识库更新
```

---

## 📊 预期性能

| 指标 | 目标 |
|------|------|
| 月收益率 | 10-20% |
| 最大回撤 | <15% |
| 胜率 | >55% |
| 夏普比率 | >2.0 |

---

## 📁 文件结构

```
polymarket-trading-agent/
├── README.md
├── SKILL.md
├── polymarket_agent.py      # 主程序
├── strategies/              # 策略模块
│   ├── market_making.py
│   ├── arbitrage.py
│   └── directional.py
├── risk/                    # 风控模块
│   └── risk_manager.py
├── learning/                # 学习模块
│   └── knowledge_base.py
├── config/                  # 配置
│   └── config.example.json
└── requirements.txt
```

---

## 🔗 相关链接

- **Polymarket**: https://polymarket.com
- **文档**: `/home/nicola/.openclaw/workspace/content/Polymarket 自进化交易 Agent 设计规范.md`
- **太一 AGI**: https://github.com/nicola-king/openclaw-workspace

---

## 📞 联系

- **作者**: 太一 AGI
- **版本**: v2.0
- **创建**: 2026-04-11

---

**🎯 Polymarket 自进化交易 Agent - 让交易更智能！**

**太一 AGI · 2026-04-11**
