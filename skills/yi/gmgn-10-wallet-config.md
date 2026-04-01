# GMGN 10 钱包配置列表 (1 主 9 辅)

> 版本：v1.0 | 创建：2026-03-27 21:40 | 太一统筹 · 羿执行

---

## 🏗️ 钱包架构总览

```
┌─────────────────────────────────────────┐
│         主钱包 (Master Wallet)          │
│  地址：5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq │
│  资金：1.0 SOL ($150)                   │
│  用途：跟单 + 狙击 + 条件单              │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ↓                       ↓
┌───────────────┐       ┌───────────────┐
│  辅钱包 1-3   │       │  辅钱包 4-9    │
│  聪明钱跟单   │       │  狙击 + 条件单  │
│  (高胜率)     │       │  (高风险)      │
└───────────────┘       └───────────────┘
```

---

## 📊 10 钱包详细配置

### 主钱包 (#1 - Master)

| 项目 | 配置 |
|------|------|
| **地址** | `5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq` |
| **类型** | 主钱包 (Master) |
| **总资金** | 1.0 SOL ($150) |
| **用途** | 统筹 10 钱包资金分配 |
| **止损** | -10%/日 (总账户) |
| **止盈** | +50% 提现 |
| **状态** | ✅ 运行中 |

**资金分配**:
```yaml
master_wallet:
  total: 1.0 SOL  # $150
  allocation:
    copy_trading: 0.6 SOL   # 60% ($90)
    sniper: 0.3 SOL         # 30% ($45)
    condition: 0.1 SOL      # 10% ($15)
```

---

### 辅钱包 #2-4 (S 级 · 聪明钱跟单)

| 编号 | 钱包名称 | 地址 | 胜率 | 资金 | 止损 | 止盈 | 状态 |
|------|---------|------|------|------|------|------|------|
| **#2** | ColdMath | `ColdMath` | 78% | 0.18 SOL ($27) | -15% | +150% | ✅ |
| **#3** | majorexploiter | `majorexploiter` | 72% | 0.18 SOL ($27) | -15% | +150% | ✅ |
| **#4** | smarttrader | `smarttrader` | 69% | 0.12 SOL ($18) | -18% | +120% | ✅ |

**配置参数**:
```yaml
wallet_2:
  name: "ColdMath"
  address: "ColdMath"
  type: "S级 - 聪明钱"
  allocation: 0.18 SOL  # $27
  stop_loss: -15%
  take_profit: +150%
  max_positions: 10
  copy_mode: "fixed_amount"

wallet_3:
  name: "majorexploiter"
  address: "majorexploiter"
  type: "S级 - 聪明钱"
  allocation: 0.18 SOL
  stop_loss: -15%
  take_profit: +150%
  max_positions: 10
  copy_mode: "fixed_amount"

wallet_4:
  name: "smarttrader"
  address: "smarttrader"
  type: "A 级 - 聪明钱"
  allocation: 0.12 SOL
  stop_loss: -18%
  take_profit: +120%
  max_positions: 10
  copy_mode: "fixed_amount"
```

---

### 辅钱包 #5-7 (A 级 · 稳定收益)

| 编号 | 钱包名称 | 地址 | 胜率 | 资金 | 止损 | 止盈 | 状态 |
|------|---------|------|------|------|------|------|------|
| **#5** | whale_hunter | `whale_hunter` | 76% | 0.12 SOL ($18) | -18% | +120% | ✅ |
| **#6** | defi_king | `defi_king` | 74% | 0.12 SOL ($18) | -18% | +120% | ✅ |
| **#7** | alpha_seeker | `alpha_seeker` | 73% | 0.08 SOL ($12) | -20% | +100% | ✅ |

**配置参数**:
```yaml
wallet_5:
  name: "whale_hunter"
  address: "whale_hunter"
  type: "A 级 - 稳定收益"
  allocation: 0.12 SOL
  stop_loss: -18%
  take_profit: +120%

wallet_6:
  name: "defi_king"
  address: "defi_king"
  type: "A 级 - 稳定收益"
  allocation: 0.12 SOL
  stop_loss: -18%
  take_profit: +120%

wallet_7:
  name: "alpha_seeker"
  address: "alpha_seeker"
  type: "B 级 - 稳定收益"
  allocation: 0.08 SOL
  stop_loss: -20%
  take_profit: +100%
```

---

### 辅钱包 #8-10 (B 级 · 高风险狙击)

| 编号 | 钱包名称 | 地址 | 胜率 | 资金 | 止损 | 止盈 | 状态 |
|------|---------|------|------|------|------|------|------|
| **#8** | moon_shot | `moon_shot` | 71% | 0.08 SOL ($12) | -20% | +100% | ✅ |
| **#9** | gem_finder | `gem_finder` | 70% | 0.08 SOL ($12) | -20% | +100% | ✅ |
| **#10** | trend_master | `trend_master` | 72% | 0.1 SOL ($15) | -20% | +100% | ✅ |

**配置参数**:
```yaml
wallet_8:
  name: "moon_shot"
  address: "moon_shot"
  type: "B 级 - 高风险"
  allocation: 0.08 SOL
  stop_loss: -20%
  take_profit: +100%

wallet_9:
  name: "gem_finder"
  address: "gem_finder"
  type: "B 级 - 高风险"
  allocation: 0.08 SOL
  stop_loss: -20%
  take_profit: +100%

wallet_10:
  name: "trend_master"
  address: "trend_master"
  type: "B 级 - 高风险"
  allocation: 0.1 SOL  # 含条件单资金
  stop_loss: -20%
  take_profit: +100%
```

---

## 📋 完整配置列表

```yaml
# GMGN 10 钱包完整配置
gmgn_wallets:
  master:
    address: "5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq"
    total_allocation: 1.0 SOL  # $150
    daily_stop_loss: -10%
    profit_withdraw: 50%
  
  copy_trading:  # 跟单钱包 (#2-#7)
    enabled: true
    total_allocation: 0.6 SOL  # $90
    wallets:
      - id: 2
        name: "ColdMath"
        address: "ColdMath"
        tier: "S"
        allocation: 0.18 SOL
        stop_loss: -15%
        take_profit: +150%
      
      - id: 3
        name: "majorexploiter"
        address: "majorexploiter"
        tier: "S"
        allocation: 0.18 SOL
        stop_loss: -15%
        take_profit: +150%
      
      - id: 4
        name: "smarttrader"
        address: "smarttrader"
        tier: "A"
        allocation: 0.12 SOL
        stop_loss: -18%
        take_profit: +120%
      
      - id: 5
        name: "whale_hunter"
        address: "whale_hunter"
        tier: "A"
        allocation: 0.12 SOL
        stop_loss: -18%
        take_profit: +120%
      
      - id: 6
        name: "defi_king"
        address: "defi_king"
        tier: "A"
        allocation: 0.12 SOL
        stop_loss: -18%
        take_profit: +120%
      
      - id: 7
        name: "alpha_seeker"
        address: "alpha_seeker"
        tier: "B"
        allocation: 0.08 SOL
        stop_loss: -20%
        take_profit: +100%
  
  sniper:  # 狙击钱包 (#8-#9)
    enabled: true
    total_allocation: 0.3 SOL  # $45
    wallets:
      - id: 8
        name: "moon_shot"
        address: "moon_shot"
        tier: "B"
        allocation: 0.08 SOL
        stop_loss: -20%
        take_profit: +100%
        sniper_params:
          gas_priority: "high"
          slippage: 20%
          anti_mev: true
      
      - id: 9
        name: "gem_finder"
        address: "gem_finder"
        tier: "B"
        allocation: 0.08 SOL
        stop_loss: -20%
        take_profit: +100%
        sniper_params:
          gas_priority: "high"
          slippage: 20%
          anti_mev: true
  
  condition:  # 条件单钱包 (#10)
    enabled: true
    total_allocation: 0.1 SOL  # $15
    wallets:
      - id: 10
        name: "trend_master"
        address: "trend_master"
        tier: "B"
        allocation: 0.1 SOL
        stop_loss: -20%
        take_profit: +100%
        condition_params:
          buy_conditions:
            - market_cap < 500000
            - liquidity > 1000000
          sell_conditions:
            - 2x: sell 50%
            - 5x: sell 30%
            - 10x: sell 100%
```

---

## 📊 资金分配总览

| 钱包类型 | 钱包数 | 总资金 (SOL) | 总资金 (USD) | 比例 |
|---------|--------|-------------|-------------|------|
| **主钱包** | 1 | 1.0 SOL | $150 | 100% |
| **跟单钱包** | 6 | 0.6 SOL | $90 | 60% |
| **狙击钱包** | 2 | 0.3 SOL | $45 | 30% |
| **条件单** | 1 | 0.1 SOL | $15 | 10% |
| **备用金** | - | 0 SOL | $0 | 0% |

---

## 🎯 GMGN 配置步骤

### Step 1: 打开 GMGN 跟单页面

```
GMGN Web → 聪明钱 → 跟单配置
```

### Step 2: 添加 6 个跟单钱包

**逐个添加**:
```
点击「添加钱包」→ 输入地址/名称 → 配置参数 → 确认
```

**配置参数**:
| 钱包 | 金额 (SOL) | 止损 | 止盈 |
|------|-----------|------|------|
| ColdMath | 0.18 | -15% | +150% |
| majorexploiter | 0.18 | -15% | +150% |
| smarttrader | 0.12 | -18% | +120% |
| whale_hunter | 0.12 | -18% | +120% |
| defi_king | 0.12 | -18% | +120% |
| alpha_seeker | 0.08 | -20% | +100% |

### Step 3: 配置狙击钱包

```
GMGN Web → 狙击 → 添加钱包
```

**配置参数**:
| 钱包 | 金额 (SOL) | Gas | 滑点 | Anti-MEV |
|------|-----------|-----|------|---------|
| moon_shot | 0.08 | 高 | 20% | ✅ |
| gem_finder | 0.08 | 高 | 20% | ✅ |

### Step 4: 配置条件单钱包

```
GMGN Web → 条件单 → 添加钱包
```

**配置参数**:
| 钱包 | 金额 (SOL) | 买单条件 | 卖单条件 |
|------|-----------|---------|---------|
| trend_master | 0.1 | 市值<$500k<br>流动性>$1M | 2x 卖 50%<br>5x 卖 30%<br>10x 清仓 |

---

## 📈 实时监控仪表板

### 每日检查清单

| 检查项 | 频率 | 主钱包 | 跟单 | 狙击 | 条件单 |
|--------|------|--------|------|------|--------|
| 总盈亏 | 每日 | ✅ | ✅ | ✅ | ✅ |
| 单钱包盈亏 | 每日 | ✅ | ✅ | ✅ | ✅ |
| 胜率变化 | 每周 | ✅ | ✅ | - | - |
| 最大回撤 | 每周 | ✅ | ✅ | ✅ | ✅ |
| 交易频率 | 每周 | - | ✅ | ✅ | ✅ |

### 周报模板

```markdown
【GMGN 10 钱包周报 #001】

时间：2026-03-27 ~ 2026-04-02

主钱包：1.0 SOL ($150)
本周盈亏：+$22.5 (+15%)
累计盈亏：+$22.5 (+15%)

┌──────┬────────────┬───────┬───────┬────────┬────────┐
│ 编号 │ 钱包名称   │ 类型  │ 盈亏  │ 回报率 │ 状态   │
├──────┼────────────┼───────┼───────┼────────┼────────┤
│ #1   │ 主钱包     │ Master│ +$22.5│ +15%   │ ✅ 良好 │
│ #2   │ ColdMath   │ S 级  │ +$8.1 │ +30%   │ ✅ 优秀 │
│ #3   │ major      │ S 级  │ +$6.5 │ +24%   │ ✅ 良好 │
│ #4   │ smart      │ A 级  | -$1.8 | -10%   │ ⚠️ 观察 │
│ #5   │ whale      │ A 级  │ +$3.6 │ +20%   │ ✅ 良好 │
│ #6   │ defi       │ A 级  │ +$2.7 │ +15%   │ ✅ 良好 │
│ #7   │ alpha      │ B 级  │ +$1.2 │ +10%   │ ✅ 良好 │
│ #8   │ moon       │ B 级  │ +$1.8 │ +15%   │ ✅ 良好 │
│ #9   │ gem        │ B 级  │ +$0.9 │ +7.5%  │ ✅ 良好 │
│ #10  │ trend      │ B 级  │ -$0.5 | -3%    │ ⚠️ 观察 │
└──────┴────────────┴───────┴───────┴────────┴────────┘

跟单总计：+$20.3 (+22.6%)
狙击总计：+$2.7 (+15%)
条件单：-$0.5 (-3%)

调整建议:
- #4 smarttrader 胜率下降，减仓 50%
- #10 trend_master 条件单优化参数
- 提现$11.25 (50% 利润)
```

---

## 🚨 风险管理规则

### 止损规则

| 级别 | 止损线 | 操作 |
|------|--------|------|
| **单钱包** | -20% | 自动止损 |
| **跟单钱包** | -15%~-20% | 暂停 + 替换 |
| **狙击钱包** | -20% | 停止狙击 24h |
| **主钱包** | -10%/日 | 停止所有交易 72h |

### 动态调整规则

```python
# 钱包调整逻辑
def adjust_wallet(wallet_id, win_rate, pnl, consecutive_losses):
    # 连续亏损 3 次 → 暂停
    if consecutive_losses >= 3:
        pause_wallet(wallet_id)
        return "暂停跟单 (3 连亏)"
    
    # 胜率下降>10% → 减仓 50%
    if win_rate < (initial_win_rate - 0.10):
        reduce_allocation(wallet_id, 0.5)
        return "减仓 50% (胜率下降)"
    
    # 最大回撤超过 -40% → 清仓替换
    if pnl < -0.40:
        close_and_replace(wallet_id)
        return "清仓替换 (最大回撤)"
    
    # 盈利达到 +100% → 提现 50%
    if pnl > 1.00:
        withdraw_profit(wallet_id, 0.5)
        return "提现 50% 利润"
    
    return "保持现状"
```

---

## 📞 Bot 协作

| Bot | 职责 | 频率 |
|-----|------|------|
| **太一** | 统筹决策 + 资金分配 | 每日 |
| **羿** | 聪明钱筛选 + 跟单配置 | 每周 |
| **天机** | 数据追踪 + 盈亏统计 | 实时 |
| **罔两** | 新币调研 + 安全分析 | 每日 |
| **管家** | 收益统计 + 报表生成 | 每日 |

---

*版本：v1.0 | 创建时间：2026-03-27 21:40*
*状态：✅ 待配置*
