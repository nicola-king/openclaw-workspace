# 币安交易策略 - 核心底层逻辑

> 版本：v1.0
> 创建时间：2026-03-30
> 状态：✅ 实盘运行中
> 当前持仓：0.0147 ETH @ $2,034.79

---

## 📋 策略概述

### 策略类型
**多因子量化交易策略** = 技术分析 + 市场状态识别 + Kelly 仓位管理

### 核心理念
```
不预测市场，只响应信号
不追求完美，只执行纪律
不All-in 赌博，只科学下注
```

---

## 🏗️ 策略架构

```
┌─────────────────────────────────────────────────────────────┐
│                    币安交易策略引擎 v1.0                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   数据层     │    │   决策层     │    │   执行层     │  │
│  │              │    │              │    │              │  │
│  │ • K 线数据    │───→│ • 市场状态   │───→│ • 下单执行   │  │
│  │ • 技术指标   │    │ • 交易信号   │    │ • 仓位管理   │  │
│  │ • 订单簿     │    │ • 风险评估   │    │ • 止盈止损   │  │
│  │              │    │              │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │   币安交易所    │
                    │  (现货/杠杆)    │
                    └─────────────────┘
```

---

## 📊 核心模块详解

### 模块 1: 数据层

#### 1.1 K 线数据
```python
# 获取 K 线数据
klines = binance_client.klines(
    symbol='ETHUSDT',
    interval='1h',      # 1 小时 K 线
    limit=100           # 最近 100 根 K 线
)

# 数据结构
[
    [
        1711771200000,  # 开盘时间
        "2034.50",      # 开盘价
        "2040.00",      # 最高价
        "2030.00",      # 最低价
        "2035.75",      # 收盘价
        "1500.00",      # 成交量
        1711774799999,  # 收盘时间
        "3050000",      # 成交额
        150,            # 交易笔数
        "800.00",       # 主动买入成交量
        "1630000",      # 主动买入成交额
        "0"             # 忽略
    ],
    ...
]
```

#### 1.2 技术指标计算

```python
import talib
import numpy as np

class TechnicalIndicators:
    """技术指标计算器"""
    
    def __init__(self, close_prices, high_prices, low_prices, volumes):
        self.close = np.array(close_prices)
        self.high = np.array(high_prices)
        self.low = np.array(low_prices)
        self.volume = np.array(volumes)
    
    def calculate_all(self):
        """计算所有技术指标"""
        return {
            # 趋势指标
            'MA20': talib.SMA(self.close, timeperiod=20),
            'MA60': talib.SMA(self.close, timeperiod=60),
            'EMA12': talib.EMA(self.close, timeperiod=12),
            'EMA26': talib.EMA(self.close, timeperiod=26),
            
            # 动量指标
            'RSI': talib.RSI(self.close, timeperiod=14),
            'MACD': talib.MACD(self.close),  # (macd, signal, hist)
            'KDJ': self.calculate_kdj(),
            
            # 波动率指标
            'BOLL': talib.BBANDS(self.close),  # (upper, middle, lower)
            'ATR': talib.ATR(self.high, self.low, self.close, timeperiod=14),
            
            # 成交量指标
            'OBV': talib.OBV(self.close, self.volume),
            'VWAP': self.calculate_vwap()
        }
    
    def calculate_kdj(self):
        """计算 KDJ 指标"""
        high_9 = talib.MAX(self.high, timeperiod=9)
        low_9 = talib.MIN(self.low, timeperiod=9)
        
        rsv = (self.close - low_9) / (high_9 - low_9) * 100
        k = talib.SMA(rsv, timeperiod=3)
        d = talib.SMA(k, timeperiod=3)
        j = 3 * k - 2 * d
        
        return k, d, j
    
    def calculate_vwap(self):
        """计算成交量加权平均价"""
        typical_price = (self.high + self.low + self.close) / 3
        return np.cumsum(typical_price * self.volume) / np.cumsum(self.volume)
```

---

### 模块 2: 决策层

#### 2.1 市场状态识别

```python
class MarketRegimeDetector:
    """市场状态识别器"""
    
    def detect(self, indicators: dict) -> str:
        """
        识别当前市场状态
        
        返回："TREND_UP" | "TREND_DOWN" | "SIDEWAYS" | "VOLATILE"
        """
        # 趋势判断
        ma20 = indicators['MA20'][-1]
        ma60 = indicators['MA60'][-1]
        price = indicators['close'][-1]
        
        # ADX 判断趋势强度
        adx = self.calculate_adx(indicators)
        
        # 波动率判断
        atr = indicators['ATR'][-1]
        atr_pct = atr / price * 100
        
        # 市场状态分类
        if adx > 25:
            # 有趋势市场
            if ma20 > ma60 and price > ma20:
                return "TREND_UP"      # 上涨趋势
            elif ma20 < ma60 and price < ma20:
                return "TREND_DOWN"    # 下跌趋势
        else:
            # 震荡市场
            if atr_pct > 3:
                return "VOLATILE"      # 高波动震荡
            else:
                return "SIDEWAYS"      # 低波动震荡
        
        return "SIDEWAYS"
    
    def calculate_adx(self, indicators: dict) -> float:
        """计算 ADX 趋势强度指标"""
        # 简化版 ADX 计算
        high = indicators['high']
        low = indicators['low']
        close = indicators['close']
        
        plus_dm = np.zeros_like(high)
        minus_dm = np.zeros_like(low)
        
        for i in range(1, len(high)):
            plus_move = high[i] - high[i-1]
            minus_move = low[i-1] - low[i]
            
            if plus_move > minus_move and plus_move > 0:
                plus_dm[i] = plus_move
            elif minus_move > plus_move and minus_move > 0:
                minus_dm[i] = minus_move
        
        # 简化计算
        tr = talib.TRANGE(high, low, close)
        atr = talib.SMA(tr, timeperiod=14)
        
        plus_di = talib.SMA(plus_dm, timeperiod=14) / atr * 100
        minus_di = talib.SMA(minus_dm, timeperiod=14) / atr * 100
        
        dx = np.abs(plus_di - minus_di) / (plus_di + minus_di) * 100
        adx = talib.SMA(dx, timeperiod=14)
        
        return adx[-1] if len(adx) > 0 else 20
```

#### 2.2 交易信号生成

```python
class SignalGenerator:
    """交易信号生成器"""
    
    def __init__(self):
        self.confidence_threshold = 0.70  # 70% 置信度
        self.min_edge = 0.02  # 最小 2% 优势
    
    def generate(self, indicators: dict, market_regime: str) -> Signal:
        """
        生成交易信号
        
        返回：Signal 对象或 None
        """
        signals = []
        
        # 根据市场状态选择策略
        if market_regime == "TREND_UP":
            signals = self.trend_following_signals(indicators, direction="BUY")
        elif market_regime == "TREND_DOWN":
            signals = self.trend_following_signals(indicators, direction="SELL")
        elif market_regime == "SIDEWAYS":
            signals = self.mean_reversion_signals(indicators)
        elif market_regime == "VOLATILE":
            signals = self.breakout_signals(indicators)
        
        # 过滤低置信度信号
        valid_signals = [s for s in signals if s.confidence >= self.confidence_threshold]
        
        # 返回最强信号
        if valid_signals:
            return max(valid_signals, key=lambda s: s.confidence)
        return None
    
    def trend_following_signals(self, indicators: dict, direction: str) -> list:
        """趋势跟踪策略信号"""
        signals = []
        
        ma20 = indicators['MA20']
        ma60 = indicators['MA60']
        ema12 = indicators['EMA12']
        ema26 = indicators['EMA26']
        rsi = indicators['RSI']
        macd, signal_line, hist = indicators['MACD']
        
        # 金叉信号
        if direction == "BUY":
            # MA 金叉
            if ma20[-1] > ma60[-1] and ma20[-2] <= ma60[-2]:
                signals.append(Signal(
                    type="BUY",
                    reason="MA 金叉",
                    confidence=0.75,
                    edge=0.03
                ))
            
            # MACD 金叉
            if macd[-1] > signal_line[-1] and macd[-2] <= signal_line[-2]:
                signals.append(Signal(
                    type="BUY",
                    reason="MACD 金叉",
                    confidence=0.72,
                    edge=0.025
                ))
            
            # RSI 超卖反弹
            if rsi[-1] < 30 and rsi[-2] >= 30:
                signals.append(Signal(
                    type="BUY",
                    reason="RSI 超卖",
                    confidence=0.70,
                    edge=0.02
                ))
        
        return signals
    
    def mean_reversion_signals(self, indicators: dict) -> list:
        """均值回归策略信号"""
        signals = []
        
        close = indicators['close'][-1]
        boll_upper, boll_middle, boll_lower = indicators['BOLL']
        rsi = indicators['RSI'][-1]
        kdj_k, kdj_d, kdj_j = indicators['KDJ']
        
        # 布林带下轨买入
        if close < boll_lower[-1] and rsi < 30:
            signals.append(Signal(
                type="BUY",
                reason="布林带下轨 + RSI 超卖",
                confidence=0.75,
                edge=0.03
            ))
        
        # 布林带上轨卖出
        if close > boll_upper[-1] and rsi > 70:
            signals.append(Signal(
                type="SELL",
                reason="布林带上轨 + RSI 超买",
                confidence=0.75,
                edge=0.03
            ))
        
        return signals
    
    def breakout_signals(self, indicators: dict) -> list:
        """突破策略信号"""
        signals = []
        
        close = indicators['close'][-1]
        high_20 = talib.MAX(indicators['high'], timeperiod=20)[-1]
        low_20 = talib.MIN(indicators['low'], timeperiod=20)[-1]
        
        # 突破 20 日高点
        if close > high_20:
            signals.append(Signal(
                type="BUY",
                reason="突破 20 日高点",
                confidence=0.72,
                edge=0.025
            ))
        
        # 跌破 20 日低点
        if close < low_20:
            signals.append(Signal(
                type="SELL",
                reason="跌破 20 日低点",
                confidence=0.72,
                edge=0.025
            ))
        
        return signals
```

---

### 模块 3: 仓位管理 (Kelly 公式)

```python
class PositionSizer:
    """仓位管理器"""
    
    def __init__(self, account_balance: float):
        self.balance = account_balance
        self.kelly_mode = "quarter"  # quarter | half | full
    
    def calculate(self, signal: Signal) -> float:
        """
        计算交易仓位
        
        Kelly 公式：f* = (bp - q) / b
        
        其中:
        - b = 盈亏比 (止盈/止损)
        - p = 胜率 (置信度)
        - q = 1 - p (失败概率)
        """
        # 计算盈亏比
        win_rate = signal.confidence
        loss_rate = 1 - win_rate
        
        # 假设止盈 10%, 止损 5%, 盈亏比 = 2:1
        win_loss_ratio = 0.10 / 0.05  # = 2.0
        
        # Kelly 公式
        kelly = (win_loss_ratio * win_rate - loss_rate) / win_loss_ratio
        
        # 应用 Kelly 模式
        if self.kelly_mode == "quarter":
            position_pct = kelly * 0.25
        elif self.kelly_mode == "half":
            position_pct = kelly * 0.50
        else:
            position_pct = kelly
        
        # 限制范围
        position_pct = max(0.05, min(position_pct, 0.25))  # 5%-25%
        
        # 计算 USDT 金额
        position_usdt = self.balance * position_pct
        
        # 币安最小订单限制
        if position_usdt < 10:
            return 0
        
        return position_usdt
```

---

### 模块 4: 风险控制

```python
class RiskManager:
    """风险管理器"""
    
    def __init__(self):
        self.daily_pnl = 0.0
        self.daily_stop_loss = -0.05  # -5% 日止损
        self.single_stop_loss = -0.05  # -5% 单笔止损
        self.take_profit = 0.10  # +10% 止盈
        self.positions = {}  # {symbol: {entry_price, quantity, side}}
        self.max_positions = 3  # 最多同时持有 3 个仓位
    
    def can_open_position(self) -> bool:
        """检查是否可以开新仓"""
        # 日止损检查
        if self.daily_pnl <= self.daily_stop_loss:
            return False
        
        # 最大仓位数检查
        if len(self.positions) >= self.max_positions:
            return False
        
        return True
    
    def check_exit(self, symbol: str, current_price: float) -> tuple:
        """
        检查是否应该平仓
        
        返回：(should_exit: bool, reason: str)
        """
        if symbol not in self.positions:
            return False, ""
        
        position = self.positions[symbol]
        entry_price = position['entry_price']
        side = position['side']
        
        # 计算盈亏比例
        if side == "BUY":
            pnl_pct = (current_price - entry_price) / entry_price
        else:
            pnl_pct = (entry_price - current_price) / entry_price
        
        # 止损检查
        if pnl_pct <= self.single_stop_loss:
            return True, f"止损触发 ({pnl_pct:.2%})"
        
        # 止盈检查
        if pnl_pct >= self.take_profit:
            return True, f"止盈触发 ({pnl_pct:.2%})"
        
        return False, ""
    
    def update_pnl(self, realized_pnl: float):
        """更新当日盈亏"""
        self.daily_pnl += realized_pnl
    
    def reset_daily(self):
        """每日重置"""
        self.daily_pnl = 0.0
```

---

### 模块 5: 执行层

```python
class TradeExecutor:
    """交易执行器"""
    
    def __init__(self, binance_client):
        self.client = binance_client
        self.retry_attempts = 3
        self.retry_delay = 1  # 秒
    
    def execute_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        执行市价单
        
        返回：订单结果
        """
        for attempt in range(self.retry_attempts):
            try:
                # 下市价单
                order = self.client.create_market_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity
                )
                
                # 验证订单状态
                if order['status'] == 'FILLED':
                    return {
                        'success': True,
                        'order_id': order['orderId'],
                        'executed_qty': float(order['executedQty']),
                        'executed_amount': float(order['cummulativeQuoteQty']),
                        'price': float(order['cummulativeQuoteQty']) / float(order['executedQty'])
                    }
                else:
                    return {
                        'success': False,
                        'error': f"订单状态：{order['status']}"
                    }
            
            except Exception as e:
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay)
                else:
                    return {
                        'success': False,
                        'error': str(e)
                    }
        
        return {'success': False, 'error': '未知错误'}
    
    def execute_limit_order(self, symbol: str, side: str, quantity: float, 
                           price: float, time_in_force: str = 'GTC') -> dict:
        """
        执行限价单
        
        time_in_force:
        - GTC: Good Till Cancel (长期有效)
        - IOC: Immediate Or Cancel (立即成交或取消)
        - FOK: Fill Or Kill (全部成交或取消)
        """
        order = self.client.create_limit_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            timeInForce=time_in_force
        )
        
        return {
            'success': order['status'] in ['FILLED', 'PARTIALLY_FILLED'],
            'order_id': order['orderId'],
            'status': order['status']
        }
```

---

## 🔄 完整执行流程

```python
class TradingStrategy:
    """交易策略主引擎"""
    
    def __init__(self, config: dict):
        self.config = config
        self.client = BinanceClient(config['api_key'], config['secret_key'])
        self.indicators = TechnicalIndicators([], [], [], [])
        self.regime_detector = MarketRegimeDetector()
        self.signal_generator = SignalGenerator()
        self.position_sizer = PositionSizer(config['initial_balance'])
        self.risk_manager = RiskManager()
        self.executor = TradeExecutor(self.client)
    
    def run(self):
        """主循环"""
        while True:
            try:
                # 1. 获取数据
                klines = self.client.get_klines(
                    symbol='ETHUSDT',
                    interval='1h',
                    limit=100
                )
                
                # 2. 计算指标
                self.indicators = TechnicalIndicators(
                    close_prices=[float(k[4]) for k in klines],
                    high_prices=[float(k[2]) for k in klines],
                    low_prices=[float(k[3]) for k in klines],
                    volumes=[float(k[5]) for k in klines]
                )
                indicators = self.indicators.calculate_all()
                
                # 3. 识别市场状态
                market_regime = self.regime_detector.detect(indicators)
                
                # 4. 生成交易信号
                signal = self.signal_generator.generate(indicators, market_regime)
                
                # 5. 检查风控
                if signal and self.risk_manager.can_open_position():
                    # 6. 计算仓位
                    position_usdt = self.position_sizer.calculate(signal)
                    
                    if position_usdt > 0:
                        # 7. 执行交易
                        quantity = position_usdt / indicators['close'][-1]
                        result = self.executor.execute_market_order(
                            symbol='ETHUSDT',
                            side=signal.type,
                            quantity=quantity
                        )
                        
                        if result['success']:
                            # 8. 记录仓位
                            self.risk_manager.positions['ETHUSDT'] = {
                                'entry_price': result['price'],
                                'quantity': result['executed_qty'],
                                'side': signal.type
                            }
                            
                            # 9. 发送通知
                            self.send_notification(signal, result)
                
                # 10. 检查现有仓位
                for symbol in list(self.risk_manager.positions.keys()):
                    current_price = float(self.client.get_ticker(symbol)['price'])
                    should_exit, reason = self.risk_manager.check_exit(symbol, current_price)
                    
                    if should_exit:
                        # 平仓
                        position = self.risk_manager.positions[symbol]
                        self.executor.execute_market_order(
                            symbol=symbol,
                            side='SELL' if position['side'] == 'BUY' else 'BUY',
                            quantity=position['quantity']
                        )
                        del self.risk_manager.positions[symbol]
                
                # 11. 等待下次循环
                time.sleep(300)  # 5 分钟
                
            except Exception as e:
                self.log_error(e)
                time.sleep(60)
    
    def send_notification(self, signal: Signal, result: dict):
        """发送交易通知"""
        message = f"""
🚀 交易执行通知

交易对：ETHUSDT
方向：{signal.type}
置信度：{signal.confidence:.0%}
成交价：${result['price']:.2f}
成交量：{result['executed_qty']:.4f}
成交额：{result['executed_amount']:.2f} USDT
原因：{signal.reason}
        """
        # 发送 Telegram/微信通知
        pass
```

---

## 📊 当前持仓状态

| 项目 | 值 |
|------|-----|
| **交易对** | ETH/USDT |
| **方向** | 买入 (LONG) |
| **成本价** | $2,034.79 |
| **持仓量** | 0.0147 ETH |
| **持仓价值** | ~30 USDT |
| **仓位比例** | 50% |
| **止盈价** | $2,238 (+10%) |
| **止损价** | $1,933 (-5%) |
| **当前市价** | ~$2,035 |
| **未实现盈亏** | ~$0 (持平) |

---

## 📈 策略参数总结

| 类别 | 参数 | 值 |
|------|------|-----|
| **交易对** | 标的 | ETH/USDT, BTC/USDT |
| **周期** | K 线 | 1 小时 |
| **指标** | MA/EMA | 20/60, 12/26 |
| | RSI | 14 周期 |
| | MACD | 12/26/9 |
| | 布林带 | 20 周期，2 标准差 |
| **仓位** | Kelly 模式 | Quarter (1/4) |
| | 最大仓位 | 25% |
| | 最小订单 | 10 USDT |
| **风控** | 止损 | -5% |
| | 止盈 | +10% |
| | 日止损 | -5% |

---

## 🫡 太一执行状态

**✅ 已激活:**
- 币安 API 完全接入
- 现货交易权限开启
- 首笔交易已执行
- 24 小时监控运行

**🟡 待完善:**
- 自动止盈止损脚本
- Telegram/微信通知
- 历史数据回测
- 策略参数优化

---

*版本：v1.0*
*创建时间：2026-03-30 11:52*
*太一 AGI · 币安交易策略核心逻辑*
