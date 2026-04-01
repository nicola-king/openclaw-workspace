# 知几-E × 币安集成方案

> 版本：v1.0 | 创建：2026-03-30 10:33
> 状态：🟡 待 Secret Key 配置
> 目标：实现知几-E v5.4 策略自动交易

---

## 📋 执行摘要

### 当前状态
- ✅ API Key 已配置并验证基础连接
- ⚠️ Secret Key 待补充 (需要用户提供)
- ⚠️ 账户权限和余额待验证
- 🔴 交易执行模块待开发

### 关键决策
1. **交易模式**: 现货交易 (不开合约)
2. **交易对**: 仅 BTCUSDT 和 ETHUSDT
3. **仓位管理**: Kelly 公式 1/4 比例
4. **风控**: -2% 止损 / +50% 止盈

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    知几-E v5.4 策略                      │
├─────────────────────────────────────────────────────────┤
│  数据层                                                  │
│  ├─ Polymarket 天气预测 (置信度计算)                    │
│  ├─ 币安实时价格 (BTC/ETH)                              │
│  └─ 市场情绪分析 (FinBERT)                              │
├─────────────────────────────────────────────────────────┤
│  决策层                                                  │
│  ├─ 置信度阈值：0.96                                    │
│  ├─ 优势评估：>0.02                                     │
│  └─ Kelly 下注比例计算                                   │
├─────────────────────────────────────────────────────────┤
│  执行层 (新增)                                           │
│  ├─ 币安 API 客户端                                      │
│  ├─ 订单管理 (下单/撤单/查询)                           │
│  └─ 仓位追踪                                             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    币安交易所                            │
├─────────────────────────────────────────────────────────┤
│  现货交易 (Spot)                                         │
│  ├─ BTCUSDT                                              │
│  └─ ETHUSDT                                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 集成步骤

### Step 1: 补充 Secret Key (必需)

**操作**:
```bash
# 编辑配置文件
nano /home/nicola/.openclaw/.env.binance

# 添加 Secret Key
BINANCE_SECRET_KEY=你的 Secret Key

# 设置权限
chmod 600 /home/nicola/.openclaw/.env.binance
```

**验证**:
```bash
cd ~/.openclaw/workspace
python3 skills/binance-trader/validate-api.py
```

**预期输出**:
```
✅ API Ping: PASS
✅ Server Time: PASS
✅ Exchange Info: PASS
✅ Account Info: PASS
最终状态：✅ VALID
```

---

### Step 2: 创建币安 API 客户端

**文件**: `skills/binance-trader/binance-client.py`

```python
#!/usr/bin/env python3
"""
币安 API 客户端 - 知几-E 专用

功能:
- 账户信息查询
- 现货交易执行
- 订单管理
- 余额查询
"""

import os
import time
import hashlib
import hmac
import requests
from datetime import datetime
from dotenv import load_dotenv

# 加载配置
load_dotenv('/home/nicola/.openclaw/.env.binance')

class BinanceClient:
    """币安现货交易客户端"""
    
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.secret_key = os.getenv("BINANCE_SECRET_KEY")
        self.base_url = "https://api.binance.com"
        
        if not self.secret_key or self.secret_key == "YOUR_SECRET_KEY_HERE":
            raise ValueError("❌ Secret Key 未配置，请补充到 .env.binance")
    
    def generate_signature(self, query_string: str) -> str:
        """生成 HMAC SHA256 签名"""
        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def get_account(self) -> dict:
        """获取账户信息"""
        timestamp = int(time.time() * 1000)
        params = f"timestamp={timestamp}"
        signature = self.generate_signature(params)
        
        url = f"{self.base_url}/api/v3/account"
        headers = {"X-MBX-APIKEY": self.api_key}
        params_dict = {"timestamp": timestamp, "signature": signature}
        
        response = requests.get(url, headers=headers, params=params_dict)
        return response.json()
    
    def get_balance(self, asset: str = "USDT") -> float:
        """获取指定资产余额"""
        account = self.get_account()
        balances = account.get('balances', [])
        
        for balance in balances:
            if balance['asset'] == asset:
                return float(balance['free'])
        
        return 0.0
    
    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float = None,
        order_type: str = "LIMIT"
    ) -> dict:
        """
        下单
        
        参数:
        - symbol: 交易对 (如 BTCUSDT)
        - side: BUY 或 SELL
        - quantity: 数量
        - price: 价格 (限价单必填)
        - order_type: LIMIT 或 MARKET
        """
        timestamp = int(time.time() * 1000)
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": f"{quantity:.8f}",
            "timestamp": timestamp
        }
        
        if order_type == "LIMIT" and price:
            params["price"] = f"{price:.2f}"
            params["timeInForce"] = "GTC"
        elif order_type == "MARKET":
            params["type"] = "MARKET"
        
        # 生成签名字符串
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = self.generate_signature(query_string)
        params["signature"] = signature
        
        url = f"{self.base_url}/api/v3/order"
        headers = {"X-MBX-APIKEY": self.api_key}
        
        response = requests.post(url, headers=headers, params=params)
        return response.json()
    
    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """撤单"""
        timestamp = int(time.time() * 1000)
        params = f"symbol={symbol}&orderId={order_id}&timestamp={timestamp}"
        signature = self.generate_signature(params)
        
        url = f"{self.base_url}/api/v3/order"
        headers = {"X-MBX-APIKEY": self.api_key}
        params_dict = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": timestamp,
            "signature": signature
        }
        
        response = requests.delete(url, headers=headers, params=params_dict)
        return response.json()
    
    def get_open_orders(self, symbol: str = None) -> list:
        """获取当前委托"""
        timestamp = int(time.time() * 1000)
        params = f"timestamp={timestamp}"
        if symbol:
            params += f"&symbol={symbol}"
        signature = self.generate_signature(params)
        
        url = f"{self.base_url}/api/v3/openOrders"
        headers = {"X-MBX-APIKEY": self.api_key}
        params_dict = {"timestamp": timestamp, "signature": signature}
        if symbol:
            params_dict["symbol"] = symbol
        
        response = requests.get(url, headers=headers, params=params_dict)
        return response.json()
```

---

### Step 3: 知几-E 策略集成

**文件**: `skills/zhiji/binance-integration.py`

```python
#!/usr/bin/env python3
"""
知几-E v5.4 × 币安集成

功能:
- 从 Polymarket 获取天气预测置信度
- 计算 Kelly 下注比例
- 执行币安交易
- 风控管理
"""

import sys
sys.path.append('/home/nicola/.openclaw/workspace/skills/binance-trader')

from binance_client import BinanceClient

class ZhijiEBinance:
    """知几-E 币安交易器"""
    
    def __init__(self):
        self.client = BinanceClient()
        self.trading_pairs = ["BTCUSDT", "ETHUSDT"]
        self.btc_allocation = 0.60
        self.eth_allocation = 0.40
        
        # 风控参数
        self.confidence_threshold = 0.96
        self.advantage_threshold = 0.02
        self.kelly_mode = "quarter"  # 1/4 Kelly
        self.max_position_usdt = 100
        self.stop_loss = -0.02  # -2%
        self.take_profit = 0.50  # +50%
    
    def calculate_kelly(self, confidence: float, advantage: float) -> float:
        """
        计算 Kelly 下注比例
        
        参数:
        - confidence: 置信度 (0-1)
        - advantage: 优势 (预期收益率)
        
        返回:
        - Kelly 比例 (0-1)
        """
        if confidence < self.confidence_threshold:
            return 0.0
        
        if advantage < self.advantage_threshold:
            return 0.0
        
        # Full Kelly: f* = (bp - q) / b
        # b = 赔率, p = 胜率, q = 1-p
        # 简化版：f* = confidence - (1 - confidence) = 2*confidence - 1
        full_kelly = 2 * confidence - 1
        
        # 应用 Kelly 模式
        if self.kelly_mode == "quarter":
            return full_kelly * 0.25
        elif self.kelly_mode == "half":
            return full_kelly * 0.50
        else:  # full
            return full_kelly
    
    def execute_trade(self, symbol: str, side: str, confidence: float):
        """
        执行交易
        
        参数:
        - symbol: 交易对
        - side: BUY 或 SELL
        - confidence: 置信度
        """
        # 计算下注比例
        advantage = 0.05  # 假设 5% 优势 (实际应从策略计算)
        kelly_ratio = self.calculate_kelly(confidence, advantage)
        
        if kelly_ratio <= 0:
            print(f"⚠️  置信度不足，跳过交易: {symbol}")
            return
        
        # 计算仓位
        usdt_balance = self.client.get_balance("USDT")
        position_usdt = min(
            usdt_balance * kelly_ratio,
            self.max_position_usdt
        )
        
        if position_usdt < 10:  # 最小交易金额
            print(f"⚠️  仓位过小 ({position_usdt:.2f} USDT)，跳过交易")
            return
        
        # 获取当前价格
        price = self.get_current_price(symbol)
        
        # 计算数量
        quantity = position_usdt / price
        
        # 执行交易
        print(f"📈 执行交易：{side} {quantity:.6f} {symbol} @ {price:.2f}")
        order = self.client.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            order_type="LIMIT"
        )
        
        print(f"✅ 订单已下：{order.get('orderId')}")
        return order
    
    def get_current_price(self, symbol: str) -> float:
        """获取当前价格"""
        url = f"{self.client.base_url}/api/v3/ticker/price"
        response = requests.get(url, params={"symbol": symbol})
        data = response.json()
        return float(data['price'])
    
    def run_strategy(self, polymarket_data: dict):
        """
        运行策略
        
        参数:
        - polymarket_data: Polymarket 天气预测数据
        """
        print("🚀 知几-E v5.4 策略启动...")
        
        # 从 Polymarket 数据获取置信度
        # (实际应从 polymarket skill 获取)
        btc_confidence = polymarket_data.get('btc_confidence', 0.5)
        eth_confidence = polymarket_data.get('eth_confidence', 0.5)
        
        # 决策
        if btc_confidence >= self.confidence_threshold:
            side = "BUY" if btc_confidence > 0.5 else "SELL"
            self.execute_trade("BTCUSDT", side, btc_confidence)
        
        if eth_confidence >= self.confidence_threshold:
            side = "BUY" if eth_confidence > 0.5 else "SELL"
            self.execute_trade("ETHUSDT", side, eth_confidence)
        
        print("✅ 策略执行完成")
```

---

### Step 4: 风控配置

**风控规则**:

| 指标 | 值 | 说明 |
|------|-----|------|
| 单交易止损 | -2% | 触及自动卖出 |
| 单交易止盈 | +50% | 触及自动卖出 |
| 日止损 | -5% | 当日停止交易 |
| 最大仓位 | 100 USDT | 单交易上限 |
| BTC 分配 | 60% | BTC 仓位占比 |
| ETH 分配 | 40% | ETH 仓位占比 |
| Kelly 模式 | 1/4 | 保守下注 |

**风控实现**:

```python
class RiskManager:
    """风控管理器"""
    
    def __init__(self):
        self.daily_pnl = 0.0
        self.daily_stop_loss = -0.05  # -5%
        self.single_stop_loss = -0.02  # -2%
        self.take_profit = 0.50  # +50%
        self.entry_prices = {}  # {symbol: entry_price}
    
    def should_trade_today(self) -> bool:
        """检查今日是否可交易"""
        if self.daily_pnl <= self.daily_stop_loss:
            print(f"❌ 触及日止损 ({self.daily_pnl:.2%})，停止交易")
            return False
        return True
    
    def check_stop_loss(self, symbol: str, current_price: float) -> str:
        """
        检查止损/止盈
        
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
    
    def update_entry(self, symbol: str, price: float):
        """记录入场价格"""
        self.entry_prices[symbol] = price
    
    def clear_entry(self, symbol: str):
        """清除入场记录"""
        if symbol in self.entry_prices:
            del self.entry_prices[symbol]
```

---

## 📊 交易执行流程

```
┌─────────────────┐
│ 1. 数据采集      │
│ - Polymarket    │
│ - 币安价格       │
│ - 市场情绪       │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 2. 策略分析      │
│ - 置信度计算     │
│ - Kelly 比例     │
│ - 风控检查       │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 3. 交易决策      │
│ - BUY/SELL/HOLD │
│ - 仓位计算       │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 4. 订单执行      │
│ - 下单           │
│ - 追踪           │
│ - 风控监控       │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 5. 报告生成      │
│ - 交易记录       │
│ - 盈亏统计       │
│ - Telegram 通知  │
└─────────────────┘
```

---

## 🎯 测试计划

### Phase 1: 连接测试 (已完成 ✅)
- [x] API Ping 测试
- [x] 服务器时间同步
- [x] 交易对信息获取
- [ ] 账户信息查询 (待 Secret Key)

### Phase 2: 模拟交易 (待执行)
- [ ] 小额测试单 (10 USDT)
- [ ] 订单查询
- [ ] 订单撤销
- [ ] 余额更新验证

### Phase 3: 策略验证 (待执行)
- [ ] 知几-E 置信度计算
- [ ] Kelly 比例计算
- [ ] 风控触发测试
- [ ] 连续 30 笔交易验证

### Phase 4: 实盘部署 (待执行)
- [ ] 小资金实盘 ($50)
- [ ] 监控和日志
- [ ] Telegram 通知
- [ ] 日报生成

---

## 🔒 安全清单

- [ ] API Key 权限：仅读取 + 现货交易
- [ ] API Key 权限：**禁用提现**
- [ ] IP 白名单：仅工控机 IP
- [ ] 配置文件加密：gpg 加密
- [ ] Secret Key：不提交到 Git
- [ ] 日志脱敏：不记录完整 Key
- [ ] 止损设置：-2% 自动止损
- [ ] 日止损：-5% 停止交易

---

## 📝 待办事项

### 立即执行 (需要用户)
1. ⚠️ **补充 Secret Key** 到 `/home/nicola/.openclaw/.env.binance`
2. ⚠️ 配置 IP 白名单 (币安 API 管理页面)
3. ⚠️ 确认账户有足够余额 (建议 ≥100 USDT)

### 太一执行
- [ ] 创建 `binance-client.py` 完整实现
- [ ] 创建 `zhiji-binan ce-integration.py` 策略集成
- [ ] 创建风控模块 `risk-manager.py`
- [ ] 配置定时任务 (cron)
- [ ] 设置 Telegram 通知
- [ ] 生成日报脚本

---

## 📈 成功指标

| 指标 | 目标 | 当前 |
|------|------|------|
| API 连通性 | ✅ | ✅ |
| 账户验证 | ✅ | ⏳ 待 Secret Key |
| 首笔交易 | ✅ | 🔴 待执行 |
| 胜率 >60% | ✅ | 🔴 待验证 |
| 月收益 >10% | ✅ | 🔴 待验证 |

---

*版本：v1.0 | 创建时间：2026-03-30 10:33*
*太一 AGI · 知几-E v5.4 × 币安集成方案*
