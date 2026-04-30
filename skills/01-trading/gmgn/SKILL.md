---
name: gmgn
version: 2.0.0
description: GMGN.AI 统一链上交易技能 - 市场数据/钱包组合/交易执行/代币信息/链上追踪
category: trading
tags: ['gmgn', 'defi', 'trading', 'solana', 'base', 'bsc']
author: 太一 AGI
created: 2026-04-03
updated: 2026-04-07
status: active
priority: P0
---

# GMGN v2.0 - 统一链上交易技能

> **版本**: 2.0.0 (整合版) | **创建**: 2026-04-03 | **整合**: 2026-04-07  
> **负责 Bot**: 知几 | **状态**: ✅ 已激活

---

## 📋 功能概述

统一 GMGN.AI 链上交易技能，整合 6 个原始技能为模块化架构。

**整合内容**:
- ✅ 原始技能：`gmgn-market` / `gmgn-portfolio` / `gmgn-swap` / `gmgn-token` / `gmgn-track` / `gmgn-cooking`
- ✅ 统一 API 封装：`api/client.py`
- ✅ 5 功能模块：`modules/(market/portfolio/swap/token/track)`
- ✅ 独立子模块：`cooking/` (代币发射)

---

## 🏗️ 架构设计

```
skills/gmgn/
├── SKILL.md              # 主文档
├── __init__.py           # 统一入口
├── api/
│   ├── __init__.py
│   └── client.py         # GMGNClient (认证/请求/速率限制)
├── modules/
│   ├── __init__.py
│   ├── market.py         # 市场数据 (K 线/热度榜/Trenches)
│   ├── portfolio.py      # 钱包组合 (持仓/交易/统计)
│   ├── swap.py           # 交易执行 ⚠️ (需要确认)
│   ├── token.py          # 代币信息 (安全检测/持仓分布)
│   └── track.py          # 链上追踪 (Smart Money/KOL)
└── cooking/              # 代币发射 (独立子模块)
    └── → gmgn-cooking    # symlink to original
```

---

## 🚀 快速开始

### Python API

```python
from skills.gmgn import GMGN

# 初始化
gmgn = GMGN()
gmgn.set_chain('sol')  # sol/bsc/base

# 市场数据
trending = gmgn.market.get_trending(limit=20)
kline = gmgn.market.get_kline('TOKEN_ADDRESS', '1h')
trenches = gmgn.market.get_trenches(types=['new_creation'])

# 钱包组合
holdings = gmgn.portfolio.get_holdings('WALLET_ADDRESS')
stats = gmgn.portfolio.get_stats('WALLET_ADDRESS', period='30d')

# 代币信息 + 安全检测 ⚠️
info = gmgn.token.get_info('TOKEN_ADDRESS')
security = gmgn.token.get_security('TOKEN_ADDRESS')
score = gmgn.token.quick_score('TOKEN_ADDRESS')  # 快速评分

# 链上追踪
smart_money = gmgn.track.get_smart_money_trades(limit=20)
kol_trades = gmgn.track.get_kol_trades(limit=20)
```

### ⚠️ 交易执行 (需要用户确认)

```python
from skills.gmgn import GMGN

gmgn = GMGN()
gmgn.set_chain('sol')

# 1. 获取报价
quote = gmgn.swap.get_quote(
    wallet_address='WALLET',
    input_token='SOL_ADDRESS',
    output_token='TOKEN_ADDRESS',
    amount=10000000  # 0.01 SOL in lamports
)

# 2. 用户确认后执行
# ⚠️ 必须用户明确确认！
confirm = input("确认买入？(yes/no): ")
if confirm == 'yes':
    result = gmgn.swap.swap(
        wallet_address='WALLET',
        input_token='SOL_ADDRESS',
        output_token='TOKEN_ADDRESS',
        amount=10000000,
        auto_slippage=True,
        anti_mev=True
    )
    
    # 3. 轮询订单状态
    final = gmgn.swap.poll_order(result['order_id'])
```

---

## 📊 模块说明

### 1. Market Module - 市场数据

| 方法 | 功能 | 参数 |
|------|------|------|
| `get_kline()` | K 线数据 | token_address, resolution, from_ts, to_ts |
| `get_trending()` | 热度榜单 | interval, limit, order_by, filters, platforms |
| `get_trenches()` | Trenches 列表 | types, launchpad_platforms, filter_preset |
| `get_token_rank()` | 代币排名 | token_address |

### 2. Portfolio Module - 钱包组合

| 方法 | 功能 | 参数 |
|------|------|------|
| `get_wallet_info()` | 钱包信息 | - |
| `get_holdings()` | 持仓 | wallet_address, limit, order_by |
| `get_activity()` | 交易记录 | wallet_address, token, type, cursor |
| `get_stats()` | 交易统计 | wallet_address, period |
| `get_token_balance()` | 代币余额 | wallet_address, token_address |
| `batch_get_stats()` | 批量统计 | wallet_addresses, period |

### 3. Swap Module - 交易执行 ⚠️

| 方法 | 功能 | 参数 |
|------|------|------|
| `get_quote()` | 获取报价 | wallet, input_token, output_token, amount |
| `swap()` | 执行交换 ⚠️ | wallet, input_token, output_token, amount/percent |
| `get_order_status()` | 订单查询 | order_id |
| `poll_order()` | 轮询状态 | order_id, max_attempts |
| `create_strategy_order()` | 策略订单 | wallet, base_token, check_price |
| `cancel_strategy_order()` | 取消订单 | wallet, order_id |

### 4. Token Module - 代币信息

| 方法 | 功能 | 参数 |
|------|------|------|
| `get_info()` | 基本信息 | token_address |
| `get_security()` | 安全检测 ⚠️ | token_address |
| `get_pool()` | 池子信息 | token_address |
| `get_holders()` | 持仓分布 | token_address, tag |
| `get_traders()` | 交易排行 | token_address, tag |
| `quick_score()` | 快速评分 | token_address |

### 5. Track Module - 链上追踪

| 方法 | 功能 | 参数 |
|------|------|------|
| `get_follow_wallet_trades()` | 关注钱包 | wallet, side, limit |
| `get_kol_trades()` | KOL 交易 | side, limit |
| `get_smart_money_trades()` | Smart Money | side, limit |
| `detect_cluster_signals()` | 集群信号 | trades, time_window |

### 6. Cooking Module - 代币发射 ⚠️

独立子模块，保留原始 `gmgn-cooking` 技能。

```bash
# 使用 CLI
gmgn-cli cooking create --chain sol --dex pump --from WALLET --name "Token" --symbol TK --buy-amt 0.01
```

---

## ⚠️ 安全警告

### 金融执行操作

**Swap/Cooking 模块涉及真实资金**:
- ✅ 必须用户明确确认
- ✅ 记录所有交易日志
- ✅ 设置滑点限制
- ✅ 小额测试优先

### 代币安全检测

**买入前必须执行安全检测**:
```python
security = gmgn.token.get_security('TOKEN_ADDRESS')
score = gmgn.token.quick_score('TOKEN_ADDRESS')

if score['risk_level'] == 'high':
    print("⚠️ 高风险，谨慎买入")
if score.get('hard_stop'):
    print("🚫 HONEYPOT - 禁止买入")
```

---

## 🔌 CLI 使用

所有功能可通过 `gmgn-cli` 直接使用：

```bash
# 市场数据
gmgn-cli market kline --chain sol --address TOKEN --resolution 1h
gmgn-cli market trending --chain sol --interval 1h --order-by volume
gmgn-cli market trenches --chain sol --type new_creation --filter-preset safe

# 钱包组合
gmgn-cli portfolio holdings --chain sol --wallet WALLET
gmgn-cli portfolio stats --chain sol --wallet WALLET --period 30d

# 代币信息
gmgn-cli token info --chain sol --address TOKEN
gmgn-cli token security --chain sol --address TOKEN

# 链上追踪
gmgn-cli track smartmoney --chain sol --limit 20
gmgn-cli track kol --chain sol --limit 20

# ⚠️ 交易执行 (需要私钥)
gmgn-cli swap --chain sol --from WALLET --input-token SOL --output-token TOKEN --amount 10000000

# ⚠️ 代币发射 (需要私钥)
gmgn-cli cooking create --chain sol --dex pump --from WALLET --name "Token" --symbol TK --buy-amt 0.01
```

---

## 📋 配置信息

### 钱包地址

| 链 | 地址 |
|------|------|
| **Solana** | `5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq` |
| **Base** | `0x73d6a5835ddf6f54480e28c8fdf399f8ec1b1c79` |
| **BSC** | (待配置) |

### 登录状态

- ✅ Telegram 账号登录
- ✅ Bot 已连接 (@GMGN_bot)
- ✅ API Key 已配置
- ⚠️ 私钥已配置 (用于交易执行)

---

## 🎯 使用场景

### 场景 1: 发现热门代币

```python
trending = gmgn.market.get_trending(limit=20, order_by='volume')
for token in trending.get('data', {}).get('rank', [])[:10]:
    print(f"{token['symbol']}: +{token['price_change_percent']}%")
```

### 场景 2: 安全检测

```python
score = gmgn.token.quick_score('TOKEN_ADDRESS')
print(f"Risk: {score['risk_level']}")
print(f"Verdict: {score['verdict']}")
```

### 场景 3: 追踪 Smart Money

```python
smart_trades = gmgn.track.get_smart_money_trades(limit=20)
clusters = gmgn.track.detect_cluster_signals(smart_trades.get('list', []))

for cluster in clusters:
    print(f"🔥 Cluster: {cluster['token']} - {cluster['signal_strength']}")
```

### 场景 4: 分析钱包

```python
holdings = gmgn.portfolio.get_holdings('WALLET_ADDRESS')
stats = gmgn.portfolio.get_stats('WALLET_ADDRESS', period='30d')

print(f"PnL: {stats.get('pnl', 0):.2f}x")
print(f"Win Rate: {stats.get('winrate', 0)*100:.1f}%")
```

---

## 📚 相关文档

- [GMGN 官方文档](https://gmgn.ai/docs)
- [交易安全指南](../../docs/TRADING-SECURITY.md)
- [链上数据分析](../../docs/ONCHAIN-ANALYSIS.md)
- [工作流：代币研究](../../docs/workflow-token-research.md)
- [工作流：钱包分析](../../docs/workflow-wallet-analysis.md)
- [工作流：Smart Money 追踪](../../docs/workflow-smart-money-profile.md)

---

## 📋 变更日志

### v2.0.0 (2026-04-07) - 整合版
- ✅ 整合 6 个原始技能 (market/portfolio/swap/token/track/cooking)
- ✅ 创建统一 API 封装 (api/client.py)
- ✅ 模块化设计 (modules/*)
- ✅ 保留 cooking 为独立子模块
- ✅ 备份原始技能到 /tmp/gmgn-backup/

### v1.0.0 (2026-04-03)
- ✅ 初始版本

---

*维护：知几 AGI | GMGN v2.0 整合版*
