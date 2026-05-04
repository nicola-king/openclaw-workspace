# payment-settlement Skill

## 描述
支付结算与汇率管理引擎：支付通道·汇率管理·结算优化·金融情报融合

## 蒸馏来源
- 金融情报 Agent：金融分析 + 量化回测
- 天机系统：市场趋势 + 汇率预测
- 交易引擎：价格对比 + 销售预测
- 太一系统：二阶思维（汇率风险对冲）

## 独立运行
```bash
python core.py --task settle --amount 50000 --from_currency CNY --to_currency AUD
```

## 依赖
- cross-border-core: ^10.0.0
- transaction-support: ^10.0.0

## 核心能力

### 1. 支付通道
- 多支付渠道接入 (TT/LC/D/PayPal/Stripe)
- 支付风险评估
- 支付路径优化
- 自动对账

### 2. 汇率管理
- 实时汇率监控
- 汇率走势预测
- 锁汇策略
- 多币种结算

### 3. 结算优化
- 结算周期优化
- 资金周转分析
- 信用证管理
- 保理服务推荐

### 4. 风控
- 支付欺诈检测
- 信用风险评估
- 汇率风险预警
- 资金安全监控

## API

### 输入
```json
{
  "task": "settle",
  "amount": 50000,
  "from_currency": "CNY",
  "to_currency": "AUD",
  "payment_method": "TT"
}
```

### 输出
```json
{
  "status": "success",
  "exchange_rate": 0.21,
  "converted_amount": 10500,
  "fee": 150,
  "net_amount": 10350,
  "payment_path": "TT via major bank",
  "risk_level": "LOW",
  "hedge_recommendation": null
}
```

## 配置
```json
{
  "payment": {
    "enabled": true,
    "default_method": "TT",
    "supported_methods": ["TT", "LC", "D/P", "PayPal", "Stripe"]
  },
  "exchange": {
    "auto_hedge": false,
    "hedge_threshold": 0.03,
    "monitor_interval": 3600
  },
  "risk": {
    "fraud_detection": true,
    "credit_check": true,
    "alert_threshold": 0.05
  }
}
```

## 使用示例
```python
from core import PaymentSettlement

ps = PaymentSettlement(config_path="config.json")

# 结算计算
result = ps.settle(
    amount=50000,
    from_currency="CNY",
    to_currency="AUD",
    payment_method="TT"
)

# 汇率监控
rate = ps.monitor_exchange_rate("CNY/AUD")

# 支付风险评估
risk = ps.assess_payment_risk(
    buyer="Aus Modular Homes",
    amount=50000,
    currency="AUD"
)
```
