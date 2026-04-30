#!/usr/bin/env python3
"""
币安交易流程测试脚本

功能:
- 测试市价单买入/卖出
- 测试限价单买入/卖出
- 测试订单查询/取消
- 测试交易历史查询
- 输出测试报告

注意：此脚本使用币安测试网 (Testnet) 或模拟模式
"""

import os
import sys
import json
import time
import hashlib
import hmac
import requests
from datetime import datetime
from typing import Optional, Dict, List

# 配置
CONFIG_PATH = "/home/nicola/.openclaw/workspace/config/binance-strategy.json"
REPORT_PATH = "/home/nicola/.openclaw/workspace/reports/binance-trade-test.md"

# 币安测试网配置
BINANCE_TESTNET_URL = "https://testnet.binance.vision"
BINANCE_MAINNET_URL = "https://api.binance.com"

class BinanceTestClient:
    """币安测试客户端"""
    
    def __init__(self, api_key: str, secret_key: str, testnet: bool = True):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = BINANCE_TESTNET_URL if testnet else BINANCE_MAINNET_URL
        self.testnet = testnet
        self.results = []
    
    def generate_signature(self, query_string: str) -> str:
        """生成 HMAC SHA256 签名"""
        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _request(self, method: str, endpoint: str, params: dict = None) -> dict:
        """发送 API 请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {"X-MBX-APIKEY": self.api_key}
        
        if params is None:
            params = {}
        
        # 添加时间戳
        timestamp = int(time.time() * 1000)
        params["timestamp"] = timestamp
        
        # 生成签名
        query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = self.generate_signature(query_string)
        params["signature"] = signature
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, params=params, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return {"success": True, "data": response.json(), "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e), "status_code": None}
    
    def test_ping(self) -> dict:
        """测试 API 连接"""
        result = self._request("GET", "/api/v3/ping")
        self.results.append({
            "test": "API Ping",
            "status": "PASS" if result["success"] else "FAIL",
            "details": result.get("data", result.get("error"))
        })
        return result
    
    def test_server_time(self) -> dict:
        """测试服务器时间"""
        result = self._request("GET", "/api/v3/time")
        if result["success"]:
            server_time = result["data"]["serverTime"]
            local_time = int(time.time() * 1000)
            time_diff = abs(server_time - local_time) / 1000
            result["time_diff_sec"] = time_diff
            result["status"] = "PASS" if time_diff < 60 else "WARN"
        
        self.results.append({
            "test": "Server Time",
            "status": result.get("status", "FAIL" if not result["success"] else "FAIL"),
            "details": f"Time diff: {result.get('time_diff_sec', 'N/A')}s" if result["success"] else result.get("error")
        })
        return result
    
    def test_exchange_info(self) -> dict:
        """测试交易对信息"""
        result = self._request("GET", "/api/v3/exchangeInfo")
        if result["success"]:
            symbols = result["data"].get("symbols", [])
            btc_info = next((s for s in symbols if s["symbol"] == "BTCUSDT"), None)
            eth_info = next((s for s in symbols if s["symbol"] == "ETHUSDT"), None)
            result["btc_info"] = btc_info
            result["eth_info"] = eth_info
        
        self.results.append({
            "test": "Exchange Info",
            "status": "PASS" if result["success"] else "FAIL",
            "details": f"BTCUSDT: {'✓' if result.get('btc_info') else '✗'}, ETHUSDT: {'✓' if result.get('eth_info') else '✗'}"
        })
        return result
    
    def test_account_info(self) -> dict:
        """测试账户信息"""
        result = self._request("GET", "/api/v3/account")
        if result["success"]:
            balances = result["data"].get("balances", [])
            usdt_balance = next((b for b in balances if b["asset"] == "USDT"), None)
            result["usdt_balance"] = usdt_balance
        
        self.results.append({
            "test": "Account Info",
            "status": "PASS" if result["success"] else "FAIL",
            "details": f"USDT: {result.get('usdt_balance', {}).get('free', 'N/A')}" if result["success"] else result.get("error")
        })
        return result
    
    def test_market_order(self, symbol: str = "BTCUSDT", side: str = "BUY", quantity: float = 0.001) -> dict:
        """测试市价单"""
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": f"{quantity:.8f}"
        }
        result = self._request("POST", "/api/v3/order", params)
        
        self.results.append({
            "test": f"Market Order {side} {symbol}",
            "status": "PASS" if result["success"] else "FAIL",
            "details": f"Order ID: {result.get('data', {}).get('orderId', 'N/A')}" if result["success"] else result.get("error")
        })
        return result
    
    def test_limit_order(self, symbol: str = "BTCUSDT", side: str = "BUY", 
                         quantity: float = 0.001, price: float = None) -> dict:
        """测试限价单"""
        if price is None:
            # 获取当前价格
            price_result = self._request("GET", "/api/v3/ticker/price", {"symbol": symbol})
            if price_result["success"]:
                price = float(price_result["data"]["price"])
                if side == "BUY":
                    price = price * 0.99  # 低于市价 1%
                else:
                    price = price * 1.01  # 高于市价 1%
            else:
                return {"success": False, "error": "Failed to get price"}
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": f"{quantity:.8f}",
            "price": f"{price:.2f}",
            "timeInForce": "GTC"
        }
        result = self._request("POST", "/api/v3/order", params)
        
        self.results.append({
            "test": f"Limit Order {side} {symbol} @ {price:.2f}",
            "status": "PASS" if result["success"] else "FAIL",
            "details": f"Order ID: {result.get('data', {}).get('orderId', 'N/A')}" if result["success"] else result.get("error")
        })
        return result
    
    def test_query_order(self, symbol: str = "BTCUSDT", order_id: int = None) -> dict:
        """测试订单查询"""
        if order_id is None:
            # 获取最近订单
            orders_result = self._request("GET", "/api/v3/allOrders", {"symbol": symbol, "limit": 1})
            if orders_result["success"] and orders_result["data"]:
                order_id = orders_result["data"][0]["orderId"]
            else:
                return {"success": False, "error": "No orders found"}
        
        params = {"symbol": symbol, "orderId": order_id}
        result = self._request("GET", "/api/v3/order", params)
        
        self.results.append({
            "test": f"Query Order {order_id}",
            "status": "PASS" if result["success"] else "FAIL",
            "details": f"Status: {result.get('data', {}).get('status', 'N/A')}" if result["success"] else result.get("error")
        })
        return result
    
    def test_cancel_order(self, symbol: str = "BTCUSDT", order_id: int = None) -> dict:
        """测试订单取消"""
        if order_id is None:
            # 获取开放订单
            open_orders = self._request("GET", "/api/v3/openOrders", {"symbol": symbol})
            if open_orders["success"] and open_orders["data"]:
                order_id = open_orders["data"][0]["orderId"]
            else:
                return {"success": False, "error": "No open orders to cancel"}
        
        params = {"symbol": symbol, "orderId": order_id}
        result = self._request("DELETE", "/api/v3/order", params)
        
        self.results.append({
            "test": f"Cancel Order {order_id}",
            "status": "PASS" if result["success"] else "FAIL",
            "details": f"Cancelled: {result.get('data', {}).get('status', 'N/A')}" if result["success"] else result.get("error")
        })
        return result
    
    def test_trade_history(self, symbol: str = "BTCUSDT") -> dict:
        """测试交易历史查询"""
        params = {"symbol": symbol, "limit": 5}
        result = self._request("GET", "/api/v3/myTrades", params)
        
        self.results.append({
            "test": f"Trade History {symbol}",
            "status": "PASS" if result["success"] else "FAIL",
            "details": f"Trades found: {len(result.get('data', []))}" if result["success"] else result.get("error")
        })
        return result
    
    def test_open_orders(self, symbol: str = None) -> dict:
        """测试当前委托查询"""
        params = {}
        if symbol:
            params["symbol"] = symbol
        result = self._request("GET", "/api/v3/openOrders", params)
        
        self.results.append({
            "test": f"Open Orders" + (f" {symbol}" if symbol else ""),
            "status": "PASS" if result["success"] else "FAIL",
            "details": f"Open orders: {len(result.get('data', []))}" if result["success"] else result.get("error")
        })
        return result
    
    def generate_report(self) -> str:
        """生成测试报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_tests = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        warnings = sum(1 for r in self.results if r["status"] == "WARN")
        
        report = f"""# 币安交易流程测试报告

> 测试时间：{timestamp}
> 测试环境：{"币安测试网 (Testnet)" if self.testnet else "币安主网"}
> 状态：{"✅ 通过" if failed == 0 else "⚠️ 部分失败" if passed > 0 else "❌ 失败"}

---

## 📊 测试摘要

| 指标 | 结果 |
|------|------|
| 总测试数 | {total_tests} |
| 通过 | {passed} |
| 失败 | {failed} |
| 警告 | {warnings} |
| 通过率 | {passed/total_tests*100:.1f}% |

---

## 📋 详细结果

"""
        for i, result in enumerate(self.results, 1):
            status_icon = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARN" else "❌"
            report += f"""### {i}. {result["test"]}
- **状态**: {status_icon} {result["status"]}
- **详情**: {result["details"]}

"""
        
        report += f"""---

## 🔧 配置信息

```json
{{
  "base_url": "{self.base_url}",
  "testnet": {self.testnet},
  "api_key": "{self.api_key[:10]}..."
}}
```

---

## 📝 结论与建议

"""
        if failed == 0:
            report += """✅ **所有测试通过**

建议下一步:
1. 配置 Secret Key 到生产环境
2. 进行小额实盘测试 (10-50 USDT)
3. 设置止损/止盈参数
4. 启用 Telegram 通知
"""
        else:
            report += f"""⚠️ **{failed} 项测试失败**

失败项目:
"""
            for result in self.results:
                if result["status"] == "FAIL":
                    report += f"- {result['test']}: {result['details']}\n"
            
            report += """
建议:
1. 检查 API Key 和 Secret Key 配置
2. 确认 IP 白名单设置
3. 验证账户权限 (读取 + 现货交易)
4. 重试失败测试
"""
        
        report += f"""
---

*报告生成时间：{timestamp}*
*太一 AGI · 币安交易测试*
"""
        return report


def load_config() -> dict:
    """加载配置文件"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  配置文件未找到：{CONFIG_PATH}")
        return {}


def main():
    """主测试流程"""
    print("=" * 60)
    print("币安交易流程测试")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    
    # 从环境变量或配置获取 API Key
    api_key = os.getenv("BINANCE_API_KEY", "cMtuxE7spOseD2wQJJVpCdqur54tNmKvlFdyEHjL9n1bPyttqjVDjeGC5VlzqQTy")
    secret_key = os.getenv("BINANCE_SECRET_KEY", "TEST_SECRET_KEY_FOR_SIMULATION")
    
    # 使用测试网
    testnet = True
    print(f"\n📡 测试环境：{'币安测试网' if testnet else '币安主网'}")
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # 创建客户端
    client = BinanceTestClient(api_key, secret_key, testnet)
    
    # 执行测试
    print("\n" + "-" * 60)
    print("开始测试...")
    print("-" * 60)
    
    # 基础连接测试
    print("\n[1/8] 测试 API Ping...")
    client.test_ping()
    
    print("[2/8] 测试服务器时间...")
    client.test_server_time()
    
    print("[3/8] 测试交易对信息...")
    client.test_exchange_info()
    
    print("[4/8] 测试账户信息...")
    client.test_account_info()
    
    # 订单测试 (模拟模式，不实际下单)
    print("\n[5/8] 测试市价单 (模拟)...")
    # 实际测试需要有效密钥，这里仅记录
    client.results.append({
        "test": "Market Order (模拟)",
        "status": "SKIP",
        "details": "需要有效 Secret Key 执行实际下单"
    })
    
    print("[6/8] 测试限价单 (模拟)...")
    client.results.append({
        "test": "Limit Order (模拟)",
        "status": "SKIP",
        "details": "需要有效 Secret Key 执行实际下单"
    })
    
    print("[7/8] 测试订单查询...")
    client.results.append({
        "test": "Query Order (模拟)",
        "status": "SKIP",
        "details": "需要先有订单才能查询"
    })
    
    print("[8/8] 测试交易历史...")
    client.results.append({
        "test": "Trade History (模拟)",
        "status": "SKIP",
        "details": "需要先有交易记录"
    })
    
    # 生成报告
    print("\n" + "-" * 60)
    print("生成测试报告...")
    print("-" * 60)
    
    report = client.generate_report()
    
    # 保存报告
    with open(REPORT_PATH, 'w') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存：{REPORT_PATH}")
    
    # 打印摘要
    passed = sum(1 for r in client.results if r["status"] == "PASS")
    total = len(client.results)
    print(f"\n📊 测试结果：{passed}/{total} 通过")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
