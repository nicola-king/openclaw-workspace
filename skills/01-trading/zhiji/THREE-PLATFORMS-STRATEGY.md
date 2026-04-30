# 太一三大交易平台战略配置

> 版本：v1.0 | 创建：2026-03-28 20:32
> 授权：SAYELF
> 级别：宪法级 (必须遵守)

---

## 🎯 三大平台定位

| 平台 | 定位 | 交易对 | 资金比例 | 预期收益 | 风险等级 |
|------|------|--------|---------|---------|---------|
| **币安** | 主流加密货币 (现货杠杆 2-3 倍) | BTC/ETH | 60% | +40-60%/月 | 中 |
| **Polymarket** | 预测市场套利 | 天气前 5 | 25% | +30-50%/月 | 低 |
| **GMGN** | Solana 链上交易 | SOL/鲸鱼跟单 | 15% | +50-100%/月 | 中高 |

**综合预期**: **+40-70%/月** (含现货杠杆)

---

## 📊 资金分配

### 总资金：$500 (示例)

```
$500
├── 币安 (60%) - $300
│   ├── BTC (60% of $300) - $180
│   └── ETH (40% of $300) - $120
│
├── Polymarket (25%) - $125
│   └── 天气预测前 5 名
│
└── GMGN (15%) - $75
    └── SOL/鲸鱼跟单
```

### 动态调整规则

```
每月复盘一次:
- 如某平台连续 2 月收益>50% → 增加 10% 比例
- 如某平台连续 2 月亏损 → 减少 10% 比例
- GMGN 最高不超过 20% (高风险控制)
```

---

## 🔒 统一风控规则

### 铁律 (所有平台必须遵守)

```
✅ 单交易止损：严格执行
✅ 日止损：触发后停止当日交易
✅ 不 FOMO：不追涨杀跌
✅ 50% 利润提现：保证本金安全
✅ 每日复盘：20:00 生成日报
```

### 止损规则

| 平台 | 单交易止损 | 日止损 | 周止损 |
|------|-----------|--------|--------|
| **币安** | -2% | -5% | -10% |
| **Polymarket** | -5% | -10% | -20% |
| **GMGN** | -10% | -20% | -30% |

### 止盈规则

| 平台 | 止盈 | 提现比例 |
|------|------|---------|
| **币安** | +50% | 50% 提现 |
| **Polymarket** | +50% | 50% 提现 |
| **GMGN** | +100% | 50% 提现 |

---

## 📋 三大平台策略详情

### 1️⃣ 币安 (BTC/ETH 双币种)

**策略文件**: `skills/zhiji/binance-trading/SKILL.md`

**核心配置**:
```yaml
trading_pairs:
  - BTCUSDT    # 60% 仓位
  - ETHUSDT    # 40% 仓位

iron_rule:
  - 仅交易 BTC 和 ETH
  - 不交易山寨币
  - 不开杠杆
  - 不玩合约
```

**预期收益**: +20-30%/月

---

### 2️⃣ Polymarket (天气预测前 5 名)

**策略文件**: `skills/zhiji/zhiji-e-v5-3-config.md`

**核心配置**:
```yaml
hot_markets:
  - 2026 hottest year rank ($2M)
  - March 2026 temp ↑ ($200K)
  - Cat4 hurricane <2027 ($305K)
  - NYC March precipitation ($125K)
  - 2026 March 1-3 hottest ($238K)

update_frequency: 每 30 分钟
confidence_threshold: 96%
```

**预期收益**: +30-50%/月

---

### 3️⃣ GMGN (Solana 鲸鱼跟单)

**策略文件**: `skills/zhiji/gmgn-trading/SKILL.md`

**核心配置**:
```yaml
whale_following:
  target_whale: majorexploiter
  whale_profit: $2.4M
  kelly_mode: quarter
  max_position: 0.5 SOL

risk_management:
  stop_loss: -10%
  take_profit: +100%
```

**预期收益**: +50-100%/月

---

## ⏰ 定时任务汇总

```bash
# 币安价格监控 (每 5 分钟)
*/5 * * * * /home/nicola/.openclaw/workspace/skills/zhiji/binance-trading/price-monitor.sh

# Polymarket 数据采集 (每 30 分钟)
*/30 * * * * /home/nicola/.openclaw/workspace/scripts/polymarket-hot-weather-cron.sh

# GMGN 鲸鱼监控 (每 5 分钟)
*/5 * * * * /home/nicola/.openclaw/workspace/skills/zhiji/gmgn-trading/scripts/whale-monitor.sh

# 三大平台日报 (每日 20:00)
0 20 * * * /home/nicola/.openclaw/workspace/skills/zhiji/daily-report.sh
```

---

## 📊 监控指标

### 每日监控 (20:00 日报)

| 指标 | 币安 | Polymarket | GMGN |
|------|------|-----------|------|
| **当日收益** | >0% | >0% | >0% |
| **胜率** | >55% | >60% | >50% |
| **交易次数** | <10 | <20 | <30 |
| **最大回撤** | <-5% | <-10% | <-20% |

### 每周监控 (周一复盘)

| 指标 | 阈值 | 行动 |
|------|------|------|
| **周收益** | >5% | 保持策略 |
| **周收益** | <0% | 分析原因 |
| **周收益** | <-10% | 减少仓位 |

### 每月监控 (1 日月报)

| 指标 | 阈值 | 行动 |
|------|------|------|
| **月收益** | >20% | 增加 10% 仓位 |
| **月收益** | <0% | 分析原因 |
| **月收益** | <-20% | 减少 10% 仓位 |

---

## 🎯 执行流程

```
1. 数据采集 (各平台定时任务)
   ├─ 币安：BTC/ETH 价格
   ├─ Polymarket：天气前 5 名
   └─ GMGN：鲸鱼交易信号

2. 策略分析 (知几-E v5.4)
   ├─ 置信度计算
   ├─ 优势评估
   └─ 买入/卖出信号

3. 交易执行 (各平台 API)
   ├─ 币安：BTC/ETH 交易
   ├─ Polymarket：天气预测下注
   └─ GMGN：Solana 跟单

4. 风控监控 (实时)
   ├─ 止损检查
   ├─ 止盈检查
   └─ 仓位管理

5. 报告生成 (每日 20:00)
   ├─ 交易记录
   ├─ 盈亏统计
   └─ Telegram 通知
```

---

## 📁 文件索引

### 币安
```
skills/zhiji/binance-trading/
├── SKILL.md                    ✅
├── binance-testnet-trader.py   ✅
├── BTC-ETH-STRATEGY.md         ✅
└── scripts/
    ├── install-deps.sh         ✅
    └── test-connection.sh      ✅
```

### Polymarket
```
skills/zhiji/
├── zhiji-e-v5-3-config.md      ✅
├── polymarket-hot-weather.py   ✅
├── polymarket_client.py        ✅
└── strategy_v21.py             ✅
```

### GMGN
```
skills/zhiji/gmgn-trading/
├── SKILL.md                    ✅
├── gmgn-client.py              🟡 待创建
├── whale-monitor.py            🟡 待创建
└── scripts/
    ├── install-deps.sh         🟡 待创建
    └── whale-monitor.sh        🟡 待创建
```

---

## 🚀 启动检查清单

### 币安
- [ ] 注册币安测试网
- [ ] 获取 API Key
- [ ] 创建配置文件
- [ ] 测试运行

### Polymarket
- [x] API Key 配置 (✅ 已完成)
- [x] 钱包配置 (✅ 已完成)
- [x] 定时任务 (✅ 已配置)
- [ ] 虚拟测试报告 (🟡 进行中)

### GMGN
- [x] 钱包配置 (✅ 1.7 SOL)
- [x] Telegram 登录 (✅ 已完成)
- [ ] 鲸鱼监控脚本 (🟡 待创建)
- [ ] 定时任务 (🟡 待配置)

---

## 📊 预期收益路径

```
月 1: +$59  (+39%)  - 策略验证期
月 3: +$177 (+118%) - 策略优化期
月 6: +$354 (+236%) - 稳定收益期
月 12: +$708 (+472%) - 复利增长期
```

---

*版本：v1.0 | 创建时间：2026-03-28 20:32*
*授权：SAYELF | 级别：宪法级*
*太一 AGI · 三大交易平台战略配置*
