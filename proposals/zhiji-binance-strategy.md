# 知几-E 币安交易策略方案

> 版本：v1.0
> 创建时间：2026-03-30 11:14
> 状态：🟡 待 Secret Key 配置
> 策略类型：天气预测套利

---

## 📋 执行摘要

### 策略核心
利用 Polymarket 天气预测市场的高置信度信号 (>96%)，在币安交易所执行 BTC/ETH 现货交易，通过 Kelly 公式优化仓位管理。

### 关键参数
| 参数 | 值 | 说明 |
|------|-----|------|
| 交易对 | BTCUSDT, ETHUSDT | 仅主流币种 |
| 置信度阈值 | 96% | Polymarket 预测置信度 |
| 优势阈值 | 2% | 最小预期优势 |
| 仓位管理 | Quarter-Kelly | 1/4 Kelly 公式 |
| 最大仓位 | 25% | 单次交易上限 |
| 止损 | -5% | 单笔交易止损 |
| 止盈 | +10% | 单笔交易止盈 |

### 预期收益
- **目标月收益**: 10-20%
- **最大回撤**: <15%
- **胜率目标**: >60%
- **夏普比率**: >1.5

---

## 🏗️ 策略架构

```
┌─────────────────────────────────────────────────────────────┐
│                      知几-E v5.4 策略引擎                    │
├─────────────────────────────────────────────────────────────┤
│  数据层                                                      │
│  ├─ Polymarket 天气预测 API                                 │
│  │   └─ 置信度计算 (加权平均)                               │
│  ├─ 币安实时价格 API                                        │
│  │   └─ BTCUSDT, ETHUSDT 市价                              │
│  └─ 市场情绪分析 (FinBERT)                                  │
│      └─ 新闻/社交媒体情绪评分                              │
├─────────────────────────────────────────────────────────────┤
│  决策层                                                      │
│  ├─ 置信度过滤：≥96%                                        │
│  ├─ 优势评估：预期收益 >2%                                  │
│  ├─ Kelly 计算：f* = (bp - q) / b × 0.25                   │
│  └─ 风控检查：日止损、单交易止损                            │
├─────────────────────────────────────────────────────────────┤
│  执行层                                                      │
│  ├─ 币安 API 客户端                                         │
│  │   ├─ 市价单/限价单                                       │
│  │   ├─ 订单查询/取消                                       │
│  │   └─ 余额查询                                            │
│  ├─ 仓位管理                                                │
│  │   ├─ BTC 60% / ETH 40%                                  │
│  │   └─ 最大 100 USDT/单                                   │
│  └─ 风控监控                                                │
│      ├─ 止损触发：-5% 自动卖出                             │
│      └─ 止盈触发：+10% 自动卖出                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        币安交易所                            │
│  现货交易 (Spot)                                             │
│  ├─ BTCUSDT                                                  │
│  └─ ETHUSDT                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 策略逻辑

### 1. 信号生成

```python
def generate_signal(polymarket_data: dict) -> Signal:
    """
    从 Polymarket 数据生成交易信号
    
    参数:
    - polymarket_data: {
        "market": "Will it rain in Beijing on 2026-04-01?",
        "yes_price": 0.96,  # 96% 置信度
        "no_price": 0.04,
        "volume_24h": 100000,
        "btc_correlation": 0.65  # 历史相关性
      }
    
    返回:
    - Signal: {
        "symbol": "BTCUSDT",
        "side": "BUY" if yes_price > 0.5 else "SELL",
        "confidence": 0.96,
        "edge": 0.05,  # 预期优势
        "kelly_ratio": 0.23  # Kelly 比例
      }
    """
    confidence = polymarket_data["yes_price"]
    
    # 置信度过滤
    if confidence < 0.96:
        return None
    
    # 计算优势 (简化版)
    edge = confidence - 0.50  # 超过 50% 的部分
    
    if edge < 0.02:  # 最小优势阈值
        return None
    
    # 计算 Kelly 比例
    full_kelly = 2 * confidence - 1  # 简化公式
    quarter_kelly = full_kelly * 0.25
    
    return Signal(
        symbol="BTCUSDT",
        side="BUY" if confidence > 0.5 else "SELL",
        confidence=confidence,
        edge=edge,
        kelly_ratio=min(quarter_kelly, 0.25)  # 最大 25%
    )
```

### 2. 仓位计算

```python
def calculate_position(signal: Signal, account_balance: float) -> float:
    """
    计算交易仓位
    
    参数:
    - signal: 交易信号
    - account_balance: USDT 余额
    
    返回:
    - position_usdt: 交易金额 (USDT)
    """
    # Kelly 仓位
    kelly_position = account_balance * signal.kelly_ratio
    
    # 应用最大仓位限制
    max_position = 100  # USDT
    position = min(kelly_position, max_position)
    
    # 应用交易对分配
    if signal.symbol == "BTCUSDT":
        position *= 0.60  # BTC 60%
    elif signal.symbol == "ETHUSDT":
        position *= 0.40  # ETH 40%
    
    # 最小订单检查
    if position < 10:  # 币安最小 10 USDT
        return 0
    
    return position
```

### 3. 风控规则

```python
class RiskManager:
    def __init__(self):
        self.daily_pnl = 0.0
        self.daily_stop_loss = -0.05  # -5%
        self.single_stop_loss = -0.05  # -5%
        self.take_profit = 0.10  # +10%
        self.entry_prices = {}
    
    def should_trade_today(self) -> bool:
        """检查今日是否可交易"""
        if self.daily_pnl <= self.daily_stop_loss:
            return False  # 触及日止损
        return True
    
    def check_exit(self, symbol: str, current_price: float) -> str:
        """
        检查是否应该平仓
        
        返回: "HOLD", "SELL_STOP", "SELL_PROFIT"
        """
        if symbol not in self.entry_prices:
            return "HOLD"
        
        entry_price = self.entry_prices[symbol]
        pnl = (current_price - entry_price) / entry_price
        
        if pnl <= self.single_stop_loss:
            return "SELL_STOP"
        elif pnl >= self.take_profit:
            return "SELL_PROFIT"
        else:
            return "HOLD"
```

---

## 🔧 配置文件

### 策略配置 (`config/binance-strategy.json`)

```json
{
  "version": "v1.0",
  "strategy_name": "知几-E 币安天气策略",
  
  "trading_config": {
    "trading_pairs": ["BTCUSDT", "ETHUSDT"],
    "confidence_threshold": 0.96,
    "edge_threshold": 0.02,
    "position_sizing": "quarter_kelly",
    "max_position_pct": 0.25,
    "max_position_usdt": 100,
    "btc_allocation": 0.60,
    "eth_allocation": 0.40
  },
  
  "risk_management": {
    "stop_loss_pct": 0.05,
    "take_profit_pct": 0.10,
    "daily_stop_loss": -0.05,
    "single_trade_stop": -0.02
  },
  
  "execution_rules": {
    "order_type": "LIMIT",
    "time_in_force": "GTC",
    "min_order_size_usdt": 10,
    "retry_attempts": 3
  }
}
```

### 环境变量 (`.env.binance`)

```bash
# 币安 API 配置
BINANCE_API_KEY=cMtuxE7spOseD2wQJJVpCdqur54tNmKvlFdyEHjL9n1bPyttqjVDjeGC5VlzqQTy
BINANCE_SECRET_KEY=你的 Secret Key

# Polymarket 配置 (如需)
POLYMARKET_API_KEY=optional

# 通知配置
TELEGRAM_BOT_TOKEN=optional
TELEGRAM_CHAT_ID=optional
```

---

## 📈 回测框架

### 回测参数
```python
backtest_config = {
    "start_date": "2025-01-01",
    "end_date": "2026-03-30",
    "initial_capital": 1000,  # USDT
    "trading_pairs": ["BTCUSDT", "ETHUSDT"],
    "confidence_threshold": 0.96,
    "kelly_mode": "quarter",
    "commission": 0.001,  # 0.1% 手续费
}
```

### 回测指标
| 指标 | 目标 | 计算方法 |
|------|------|----------|
| 总收益 | >50% | (最终资金 - 初始资金) / 初始资金 |
| 年化收益 | >100% | 总收益年化 |
| 最大回撤 | <15% | 最大峰值到谷底跌幅 |
| 夏普比率 | >1.5 | (年化收益 - 无风险利率) / 波动率 |
| 胜率 | >60% | 盈利交易数 / 总交易数 |
| 盈亏比 | >2.0 | 平均盈利 / 平均亏损 |

---

## 🚀 部署流程

### Phase 1: 准备 (已完成 ✅)
- [x] API Key 配置
- [x] 策略参数设计
- [x] 测试脚本编写
- [ ] Secret Key 补充 ⚠️

### Phase 2: 测试 (进行中 🟡)
- [ ] API 连接验证
- [ ] 账户权限检查
- [ ] 小额测试单 (10 USDT)
- [ ] 订单管理测试

### Phase 3: 模拟 (待执行 🔴)
- [ ] 历史数据回测
- [ ] 纸面交易验证
- [ ] 参数优化

### Phase 4: 实盘 (待执行 🔴)
- [ ] 小资金实盘 ($100)
- [ ] 监控和日志
- [ ] Telegram 通知
- [ ] 日报生成

---

## 🔒 安全清单

### API 安全
- [x] API Key 权限：仅读取 + 现货交易
- [x] API Key 权限：**禁用提现** ✅
- [ ] IP 白名单：仅工控机 IP ⚠️
- [ ] 配置文件加密：gpg 加密 ⚠️
- [ ] Secret Key：不提交到 Git ✅

### 交易安全
- [x] 止损设置：-5% 自动止损
- [x] 止盈设置：+10% 自动止盈
- [x] 日止损：-5% 停止交易
- [x] 最大仓位：100 USDT/单
- [ ] 紧急停止开关 ⚠️

### 监控安全
- [ ] 异常交易告警 ⚠️
- [ ] 余额不足告警 ⚠️
- [ ] API 错误率监控 ⚠️
- [ ] Telegram 通知 ⚠️

---

## 📝 运维手册

### 启动策略
```bash
cd /home/nicola/.openclaw/workspace
python3 scripts/zhiji-binance-strategy.py --mode live
```

### 停止策略
```bash
# 优雅停止 (平掉所有仓位)
python3 scripts/zhiji-binance-strategy.py --stop

# 紧急停止 (立即停止，保留仓位)
python3 scripts/zhiji-binance-strategy.py --emergency-stop
```

### 查看状态
```bash
# 当前仓位
python3 scripts/zhiji-binance-strategy.py --status

# 今日盈亏
python3 scripts/zhiji-binance-strategy.py --pnl

# 日志查看
tail -f /home/nicola/.openclaw/workspace/logs/binance-trades.log
```

### 定时任务 (cron)
```bash
# 编辑 crontab
crontab -e

# 添加策略执行 (每 5 分钟检查信号)
*/5 * * * * cd /home/nicola/.openclaw/workspace && python3 scripts/zhiji-binance-strategy.py --cron >> logs/strategy.log 2>&1

# 日报生成 (每天 23:00)
0 23 * * * cd /home/nicola/.openclaw/workspace && python3 scripts/generate-daily-report.py >> logs/reports.log 2>&1
```

---

## 📊 监控仪表板

### 实时指标
- 当前仓位 (BTC/ETH)
- 未实现盈亏
- 今日已实现盈亏
- 置信度热力图
- 最近交易记录

### 日报内容
- 今日交易次数
- 胜率
- 总盈亏
- 最大回撤
- 仓位使用率

---

## ⚠️ 风险提示

1. **市场风险**: 天气预测与加密货币价格相关性不确定
2. **技术风险**: API 故障、网络延迟可能导致执行偏差
3. **流动性风险**: 极端行情下可能无法及时平仓
4. **模型风险**: 置信度计算可能存在偏差
5. **监管风险**: 加密货币监管政策变化

**建议**: 首次实盘资金 ≤100 USDT，逐步验证策略有效性后再增加资金。

---

## 📚 参考文档

- [币安 API 文档](https://binance-docs.github.io/apidocs/)
- [Polymarket API](https://docs.polymarket.com/)
- [Kelly 公式详解](https://en.wikipedia.org/wiki/Kelly_criterion)
- [知几-E v5.4 架构](./binance-zhiji-integration.md)

---

*版本：v1.0*
*创建时间：2026-03-30 11:14*
*太一 AGI · 知几-E 币安交易策略*
