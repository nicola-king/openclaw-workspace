# 太一自动交易控制器

> 版本：v1.0 | 创建：2026-03-27 22:25 | 授权：100% 自动执行

---

## 🎯 核心配置

```yaml
taiyi_controller:
  version: 1.0
  authorized_by: "SAYELF (nicola king)"
  authorized_at: "2026-03-27 22:25"
  principle: "结果论英雄"
  
  capital:
    total_sol: 1.7
    total_usd: 150
    sol_price: 88
  
  allocation:
    copy_trading:
      enabled: true
      wallets: 6
      total_sol: 1.02
      total_usd: 90
      percentage: 60%
    
    sniper:
      enabled: true
      wallets: 2
      total_sol: 0.51
      total_usd: 45
      percentage: 30%
    
    condition:
      enabled: true
      wallets: 1
      total_sol: 0.17
      total_usd: 15
      percentage: 10%
  
  risk_management:
    daily_stop_loss: -10%  # -$15
    single_wallet_stop: -40%  # -$60
    single_trade_stop: -20%  # -$30
    platform_stop: -15%  # -$22.5
  
  profit_withdraw:
    enabled: true
    ratio: 50%
    auto_execute: true
  
  reporting:
    enabled: true
    email: "285915125@qq.com"
    time: "20:00"
    timezone: "Asia/Shanghai"
```

---

## 📊 10 钱包配置

### 跟单钱包 (6 个)

```python
copy_wallets = [
    {"name": "ColdMath", "sol": 0.18, "usd": 16, "stop": -0.15, "take": 1.5},
    {"name": "majorexploiter", "sol": 0.18, "usd": 16, "stop": -0.15, "take": 1.5},
    {"name": "smarttrader", "sol": 0.12, "usd": 11, "stop": -0.18, "take": 1.2},
    {"name": "whale_hunter", "sol": 0.12, "usd": 11, "stop": -0.18, "take": 1.2},
    {"name": "defi_king", "sol": 0.12, "usd": 11, "stop": -0.18, "take": 1.2},
    {"name": "alpha_seeker", "sol": 0.08, "usd": 7, "stop": -0.20, "take": 1.0},
]
```

### 狙击钱包 (2 个)

```python
sniper_wallets = [
    {"name": "moon_shot", "sol": 0.255, "usd": 22.5, "gas": "high", "slippage": 0.2},
    {"name": "gem_finder", "sol": 0.255, "usd": 22.5, "gas": "high", "slippage": 0.2},
]
```

### 条件单 (1 个)

```python
condition_wallet = {
    "name": "trend_master",
    "sol": 0.17,
    "usd": 15,
    "buy_conditions": {"market_cap": 500000, "liquidity": 1000000},
    "sell_conditions": {"2x": 0.5, "5x": 0.3, "10x": 1.0}
}
```

---

## 🚀 自动执行流程

```
启动太一控制器
    ↓
连接 GMGN API
    ↓
配置 10 钱包参数
    ↓
启动监控循环 (每分钟)
    ↓
┌───────────────────┐
│  每分钟检查       │
│  • 钱包盈亏       │
│  • 止损/止盈      │
│  • 风控状态       │
└───────────────────┘
    ↓
┌───────────────────┐
│  每日 20:00       │
│  • 生成日报       │
│  • 发送邮件       │
│  • 收益统计       │
└───────────────────┘
    ↓
┌───────────────────┐
│  盈利达到 50%     │
│  • 自动提现       │
│  • 50% 复投        │
└───────────────────┘
```

---

## 📞 通知配置

**Telegram**: @nicola king (7073481596)
**邮箱**: 285915125@qq.com

**通知类型**:
- ✅ 开仓通知 (每笔交易)
- ✅ 平仓通知 (止盈/止损)
- ✅ 日报通知 (每日 20:00)
- ✅ 风控告警 (触及止损线)

---

*创建时间：2026-03-27 22:25*
*授权：100% 自动执行*
*原则：结果论英雄*
