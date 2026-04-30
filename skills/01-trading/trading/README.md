# Trading 交易引擎

> **版本**: 2.0 | **更新时间**: 2026-04-07  
> **状态**: ✅ 整合完成 | **优先级**: P1

---

## 📋 概述

交易引擎整合了币安现货/合约、Polymarket 预测市场和其他交易平台的统一接口。提供策略执行、风险管理和仓位追踪能力。

---

## 🏗️ 架构

```
trading/
├── __init__.py              # 主入口，Trading 类
├── SKILL.md                 # 技能定义
├── binance/                 # 币安模块
│   ├── spot.py              # 现货交易
│   └── futures.py           # 合约交易
├── polymarket/              # Polymarket 模块
│   └── prediction.py        # 预测市场
└── torchtrade/              # TorchTrade 模块
    └── executor.py          # 交易执行器
```

---

## 🚀 快速开始

### 初始化

```python
from skills.trading import Trading

trading = Trading()
```

### 币安现货交易

```python
# 获取余额
balance = trading.binance.spot.get_balance()

# 获取价格
price = trading.binance.spot.get_price('BTCUSDT')

# 市价买入
order = trading.binance.spot.market_buy(
    symbol='BTCUSDT',
    quantity=0.001,
    confirm=True  # 需要确认
)

# 市价卖出
order = trading.binance.spot.market_sell(
    symbol='ETHUSDT',
    quantity=0.01,
    confirm=True
)

# 限价单
order = trading.binance.spot.limit_order(
    symbol='BTCUSDT',
    side='buy',
    quantity=0.001,
    price=95000,
    time_in_force='GTC'
)

# 取消订单
trading.binance.spot.cancel_order('BTCUSDT', order_id)

# 查询订单
order_status = trading.binance.spot.get_order('BTCUSDT', order_id)
```

### 币安合约交易

```python
# 获取持仓
positions = trading.binance.futures.get_positions()

# 开多
order = trading.binance.futures.open_long(
    symbol='BTCUSDT',
    quantity=0.001,
    leverage=10,
    confirm=True
)

# 开空
order = trading.binance.futures.open_short(
    symbol='ETHUSDT',
    quantity=0.01,
    leverage=10,
    confirm=True
)

# 平仓
order = trading.binance.futures.close_position('BTCUSDT')

# 调整杠杆
trading.binance.futures.set_leverage('BTCUSDT', leverage=20)

# 设置止损止盈
trading.binance.futures.set_stop_loss(
    symbol='BTCUSDT',
    stop_price=90000,
    position_side='LONG'
)
```

### Polymarket 预测市场

```python
# 获取市场列表
markets = trading.polymarket.get_markets(category='crypto')

# 获取市场价格
prices = trading.polymarket.get_prices('btc-100k-2024')

# 买入份额
order = trading.polymarket.buy(
    market='btc-100k-2024',
    outcome='Yes',
    amount=100,  # USD
    confirm=True
)

# 卖出份额
order = trading.polymarket.sell(
    market='btc-100k-2024',
    shares=50,
    confirm=True
)

# 获取持仓
positions = trading.polymarket.get_positions()

# 结算结果
result = trading.polymarket.get_result('market-id')
```

### 策略执行

```python
# 定投策略
trading.strategy.dca(
    symbol='BTCUSDT',
    amount=100,  # USD
    interval='daily',  # daily | weekly | monthly
    start_date='2026-04-07'
)

# 网格交易
trading.strategy.grid(
    symbol='BTCUSDT',
    lower_price=90000,
    upper_price=100000,
    grids=10,
    investment=1000
)

# 止盈止损策略
trading.strategy.stop_loss(
    symbol='BTCUSDT',
    stop_loss_pct=5,  # 5% 止损
    take_profit_pct=10  # 10% 止盈
)
```

### 风险管理

```python
# 设置最大仓位
trading.risk.set_max_position(
    symbol='BTCUSDT',
    max_amount=1000  # USD
)

# 设置日交易限额
trading.risk.set_daily_limit(5000)  # USD

# 获取风险报告
report = trading.risk.get_report()

# 风险检查
risk_check = trading.risk.check_order(
    symbol='BTCUSDT',
    amount=5000
)
```

---

## ⚠️ 安全注意事项

### 交易安全

- ✅ 所有实盘交易需要明确确认
- ✅ 设置单笔交易上限
- ✅ 设置日交易限额
- ✅ 使用 API Key 白名单

### 风险控制

- ✅ 设置止损点
- ✅ 控制仓位大小
- ✅ 避免过度杠杆
- ✅ 定期提取利润

### API 安全

- ✅ 使用子账户 API
- ✅ 限制 IP 白名单
- ✅ 只开启必要权限
- ✅ 定期轮换密钥

---

## 🔧 配置

### 币安配置

```yaml
# ~/.openclaw/config/binance.yaml
binance:
  api_key: "xxx"
  secret_key: "xxx"
  testnet: false
  
  trading:
    max_order_size: 1000  # USD
    daily_limit: 5000  # USD
    default_leverage: 10
    max_leverage: 20
```

### Polymarket 配置

```yaml
# ~/.openclaw/config/polymarket.yaml
polymarket:
  api_key: "xxx"
  
  trading:
    max_bet: 500  # USD
    daily_limit: 2000  # USD
```

### 风险配置

```yaml
# ~/.openclaw/config/risk.yaml
risk:
  max_position_per_symbol: 1000  # USD
  max_total_exposure: 5000  # USD
  daily_loss_limit: 500  # USD
  stop_loss_default: 5  # %
  take_profit_default: 10  # %
```

---

## 📊 交易报告

```python
# 获取交易历史
history = trading.report.get_history(days=30)

# 获取盈亏统计
pnl = trading.report.get_pnl(days=30)

# 生成报告
report = trading.report.generate(
    period='weekly',
    format='markdown'
)
```

---

## 🧪 测试

```bash
# 运行测试（模拟交易）
python3 -m pytest skills/trading/tests/ -v

# 测试币安（testnet）
python3 -m pytest skills/trading/tests/test_binance.py -v

# 测试 Polymarket
python3 -m pytest skills/trading/tests/test_polymarket.py -v
```

---

## 📚 相关文档

- [技能定义](SKILL.md)
- [币安 API 文档](https://binance-docs.github.io/apidocs/)
- [Polymarket API](https://polymarket.com/api)
- [知几量化策略](../zhiji/SKILL.md)

---

*维护：太一 AGI | Trading Engine v2.0*
