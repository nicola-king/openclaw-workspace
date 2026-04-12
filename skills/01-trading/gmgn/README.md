# GMGN 链上交易技能

> **版本**: 2.0 | **更新时间**: 2026-04-07  
> **状态**: ✅ 整合完成 | **优先级**: P0

---

## 📋 概述

GMGN 技能提供完整的链上交易能力，支持 Solana、Base、BSC 等多条区块链。整合了市场数据、钱包组合、交易执行、代币信息和链上追踪五大模块。

---

## 🏗️ 架构

```
gmgn/
├── __init__.py          # 主入口，GMGN 类
├── SKILL.md             # 技能定义
├── api/                 # API 封装层
│   └── gmgn_api.py      # GMGN API 客户端
├── modules/             # 功能模块
│   ├── market.py        # 市场数据
│   ├── portfolio.py     # 钱包组合
│   ├── swap.py          # 交易执行
│   ├── token.py         # 代币信息
│   └── track.py         # 链上追踪
└── cooking/             # 代币发行
    └── launchpad.py     # Launchpad 平台
```

---

## 🚀 快速开始

### 初始化

```python
from skills.gmgn import GMGN

gmgn = GMGN()
gmgn.set_chain('sol')  # sol | bsc | base | eth | ton
```

### 市场数据

```python
# 获取 trending 代币
trending = gmgn.market.get_trending(limit=10)

# 获取 K 线数据
kline = gmgn.market.get_kline(
    token='So11111111111111111111111111111111111111112',
    interval='1h'
)
```

### 钱包组合

```python
# 获取持仓
holdings = gmgn.portfolio.get_holdings('WALLET_ADDRESS')

# 获取交易记录
transactions = gmgn.portfolio.get_transactions('WALLET_ADDRESS')

# 获取交易统计
stats = gmgn.portfolio.get_stats('WALLET_ADDRESS')
```

### 交易执行 ⚠️

```python
# 需要用户确认！
result = gmgn.swap.execute(
    from_token='SOL',
    to_token='TOKEN_ADDRESS',
    amount=1.0,
    slippage=0.5  # 滑点 %
)

# 查询订单状态
status = gmgn.swap.get_order_status(order_id)
```

### 代币信息

```python
# 基本信息
info = gmgn.token.get_info('TOKEN_ADDRESS')

# 安全检测
security = gmgn.token.get_security('TOKEN_ADDRESS')

# 池子信息
pool = gmgn.token.get_pool('TOKEN_ADDRESS')

# 前十大持仓
holders = gmgn.token.get_top_holders('TOKEN_ADDRESS')
```

### 链上追踪

```python
# 关注钱包交易
trades = gmgn.track.get_follow_wallet_trades(wallet_id)

# KOL 交易
kol_trades = gmgn.track.get_kol_trades()

# Smart Money
smart_money = gmgn.track.get_smart_money_trades()
```

---

## 🔐 安全配置

### 钱包配置

编辑 `.gmgn_config.yaml`:

```yaml
wallets:
  solana: "5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq"
  base: "0x73d6a5835ddf6f54480e28c8fdf399f8ec1b1c79"

security:
  max_slippage: 1.0  # 最大滑点 %
  max_amount_usd: 1000  # 单笔最大金额
  require_confirmation: true  # 需要确认
```

### API Key 配置

```yaml
api:
  key: "YOUR_API_KEY"
  secret: "YOUR_API_SECRET"
```

---

## ⚠️ 安全注意事项

### 交易执行

- ✅ 所有 swap 操作需要用户明确确认
- ✅ 设置滑点上限（默认 1%）
- ✅ 设置单笔金额上限
- ✅ 大额交易分多笔执行

### 风险控制

- ✅ 交易前检查代币安全
- ✅ 检查池子流动性
- ✅ 避免honeypot代币
- ✅ 设置止损点

---

## 📊 支持链

| 链 | 状态 | 功能 |
|------|------|------|
| **Solana** | ✅ | 全部功能 |
| **Base** | ✅ | 全部功能 |
| **BSC** | ✅ | 全部功能 |
| **Ethereum** | ✅ | 代币发行 |
| **TON** | ✅ | 代币发行 |

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest skills/gmgn/tests/ -v

# 测试市场数据
python3 -m pytest skills/gmgn/tests/test_market.py -v

# 测试交易（模拟）
python3 -m pytest skills/gmgn/tests/test_swap.py -v
```

---

## 📚 相关文档

- [GMGN 快速入门](gmgn-quickstart.md)
- [GMGN 配置指南](gmgn-setup-guide.md)
- [技能定义](SKILL.md)

---

## 🔗 外部链接

- [GMGN 官网](https://gmgn.ai)
- [GMGN Telegram Bot](https://t.me/GMGN_bot)
- [GMGN API 文档](https://docs.gmgn.ai)

---

*维护：太一 AGI | GMGN 技能 v2.0*
