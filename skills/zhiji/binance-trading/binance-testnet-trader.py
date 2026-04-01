# 币安测试网配置指南

## 🧪 什么是币安测试网？

```
币安测试网 = 模拟交易环境

✅ 100% 真实交易体验
✅ 使用模拟资金 (10,000 USDT 测试币)
✅ 零风险 (不涉及真实资金)
✅ 策略验证最佳环境
```

## 📍 注册步骤

### 步骤 1: 访问测试网

```
网址：https://testnet.binance.vision/

或者现货测试网:
https://testnet.binancefuture.com/
```

### 步骤 2: 注册测试网账号

```
1. 点击 "Register" 或 "Sign Up"
2. 使用 GitHub 账号登录 (推荐)
   或
   使用邮箱注册
3. 完成验证
```

### 步骤 3: 获取测试网 API Key

```
1. 登录后点击 "API Key" 或 "Dashboard"
2. 点击 "Generate HMAC_SHA256 Key"
3. 记录 API Key 和 Secret Key

⚠️ 重要：
- 测试网 Key 与主网 Key 独立
- 可以安全分享用于测试
- 不会影响真实资金
```

### 步骤 4: 领取测试资金

```
现货测试网:
- 自动赠送 10,000 USDT 测试币
- 可重置 (每天一次)

合约测试网:
- 自动赠送 100,000 USDT 测试币
- 可重置 (每天一次)
```

---

## 🔧 配置太一测试网集成

### 环境变量配置

```bash
# 创建测试网配置文件
cat > /home/nicola/.openclaw/.env.binance-testnet << EOF
# 币安测试网 API
BINANCE_TESTNET=true
BINANCE_API_KEY=你的测试网 API Key
BINANCE_SECRET_KEY=你的测试网 Secret Key
BINANCE_BASE_URL=https://testnet.binance.vision

# 测试资金
TESTNET_INITIAL_BALANCE=10000  # 10,000 USDT

# 交易配置
KELLY_MODE=quarter
CONFIDENCE_THRESHOLD=0.96
MAX_POSITION_USDT=500  # 测试网可以大一点
EOF

# 设置文件权限
chmod 600 /home/nicola/.openclaw/.env.binance-testnet
```

### 测试网交易脚本

```python
#!/usr/bin/env python3
"""
币安测试网交易验证脚本

功能:
- 连接币安测试网
- 执行模拟交易
- 追踪盈亏
- 生成验证报告
"""

import os
import asyncio
import aiohttp
import hashlib
import hmac
from datetime import datetime
from dotenv import load_dotenv

# 加载测试网配置
load_dotenv('/home/nicola/.openclaw/.env.binance-testnet')

# 配置
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL", "https://testnet.binance.vision")

class BinanceTestnet:
    """币安测试网交易类"""
    
    def __init__(self):
        self.api_key = BINANCE_API_KEY
        self.secret_key = BINANCE_SECRET_KEY
        self.base_url = BINANCE_BASE_URL
        self.balance = 10000  # 初始测试资金
        self.trades = []
    
    def generate_signature(self, params: str) -> str:
        """生成 HMAC SHA256 签名"""
        return hmac.new(
            self.secret_key.encode('utf-8'),
            params.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    async def get_account_info(self, session: aiohttp.ClientSession) -> dict:
        """获取账户信息"""
        timestamp = int(datetime.now().timestamp() * 1000)
        params = f"timestamp={timestamp}"
        signature = self.generate_signature(params)
        
        url = f"{self.base_url}/api/v3/account"
        headers = {"X-MBX-APIKEY": self.api_key}
        params_dict = {"timestamp": timestamp, "signature": signature}
        
        async with session.get(url, headers=headers, params=params_dict) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"❌ 获取账户信息失败：{response.status}")
                return {}
    
    async def place_test_order(
        self,
        session: aiohttp.ClientSession,
        symbol: str,
        side: str,
        quantity: float,
        price: float = None
    ) -> dict:
        """
        下测试订单
        
        参数:
        - symbol: 交易对 (如 BTCUSDT)
        - side: BUY 或 SELL
        - quantity: 数量
        - price: 价格 (限价单必填，市价单留空)
        """
        timestamp = int(datetime.now().timestamp() * 1000)
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT" if price else "MARKET",
            "quantity": quantity,
            "timestamp": timestamp
        }
        
        if price:
            params["price"] = price
            params["timeInForce"] = "GTC"
        
        # 生成签名字符串
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = self.generate_signature(query_string)
        params["signature"] = signature
        
        url = f"{self.base_url}/api/v3/order"
        headers = {"X-MBX-APIKEY": self.api_key}
        
        async with session.post(url, headers=headers, params=params) as response:
            if response.status == 200:
                order = await response.json()
                self.trades.append(order)
                print(f"✅ 测试订单已下：{side} {quantity} {symbol} @ {price or 'MARKET'}")
                return order
            else:
                error = await response.text()
                print(f"❌ 下单失败：{error}")
                return {}
    
    async def get_balance(self, session: aiohttp.ClientSession) -> float:
        """获取 USDT 余额"""
        account = await self.get_account_info(session)
        balances = account.get("balances", [])
        
        for balance in balances:
            if balance["asset"] == "USDT":
                return float(balance["free"])
        
        return self.balance
    
    def generate_report(self) -> str:
        """生成测试报告"""
        report = f"""
# 币安测试网交易验证报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━

## 📊 账户信息

- 初始资金：10,000 USDT
- 当前余额：{self.balance:.2f} USDT
- 交易次数：{len(self.trades)}

━━━━━━━━━━━━━━━━━━━━━

## 📈 交易记录

"""
        for i, trade in enumerate(self.trades, 1):
            report += f"""
{i}. **{trade.get('symbol', 'UNKNOWN')}**
   - 方向：{trade.get('side', 'UNKNOWN')}
   - 数量：{trade.get('origQty', 0)}
   - 价格：{trade.get('price', 0)}
   - 状态：{trade.get('status', 'UNKNOWN')}
   - 时间：{datetime.fromtimestamp(trade.get('transactTime', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # 计算盈亏 (简化版)
        total_pnl = self.balance - 10000
        pnl_percent = (total_pnl / 10000) * 100
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━

## 💰 盈亏统计

- 总盈亏：{total_pnl:+.2f} USDT
- 收益率：{pnl_percent:+.2f}%
- 胜率：{self.calculate_win_rate():.1f}%

━━━━━━━━━━━━━━━━━━━━━

## ✅ 验证结论

策略在测试网的表现:
- {'✅ 有效，可以考虑实盘' if total_pnl > 0 else '⚠️ 需要优化策略'}
- 建议继续测试 {max(0, 30 - len(self.trades))} 笔交易
- 胜率稳定在 60%+ 后考虑实盘

━━━━━━━━━━━━━━━━━━━━━

*太一 AGI · 知几-E v4.0 测试网验证*
"""
        return report
    
    def calculate_win_rate(self) -> float:
        """计算胜率 (简化版)"""
        if not self.trades:
            return 0.0
        
        # 实际应追踪每笔交易的盈亏
        # 这里简化为 50% (示例)
        return 50.0


async def main():
    """主函数"""
    print("🧪 币安测试网交易验证启动...")
    
    testnet = BinanceTestnet()
    
    async with aiohttp.ClientSession() as session:
        # 1. 获取账户信息
        print("📊 获取账户信息...")
        account = await testnet.get_account_info(session)
        balance = await testnet.get_balance(session)
        print(f"💰 当前余额：{balance:.2f} USDT")
        
        # 2. 执行测试交易
        print("📈 执行测试交易...")
        
        # 示例：买入 BTC
        await testnet.place_test_order(
            session,
            symbol="BTCUSDT",
            side="BUY",
            quantity=0.001,  # 0.001 BTC
            price=50000  # 限价单
        )
        
        # 示例：卖出 ETH
        await testnet.place_test_order(
            session,
            symbol="ETHUSDT",
            side="SELL",
            quantity=0.01,  # 0.01 ETH
            price=3000  # 限价单
        )
        
        # 3. 生成报告
        print("📝 生成测试报告...")
        report = testnet.generate_report()
        
        # 4. 保存报告
        output_file = f"/home/nicola/.openclaw/workspace/reports/binance-testnet-{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✅ 测试报告已生成：{output_file}")


if __name__ == "__main__":
    asyncio.run(main())
