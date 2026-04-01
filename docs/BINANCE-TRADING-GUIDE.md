# 币安交易配置指南

> 创建时间：2026-03-31 | 状态：🟡 待配置 API Key

---

## 📋 目录

1. [快速开始](#快速开始)
2. [API Key 获取](#api-key-获取)
3. [测试网 vs 实盘](#测试网 vs 实盘)
4. [Python 客户端配置](#python-客户端配置)
5. [常见错误排查](#常见错误排查)

---

## 🚀 快速开始

### 前置条件
- ✅ 币安账户 (已完成 KYC)
- ✅ API Key + Secret
- ✅ IP 白名单配置 (可选)

### 三步配置
```bash
# 1. 设置环境变量
export BINANCE_API_KEY='your_api_key'
export BINANCE_API_SECRET='your_api_secret'

# 2. 运行测试脚本
python3 scripts/binance-test.py

# 3. 检查输出
# ✅ API Key 有效
# ✅ 账户余额查询成功
```

---

## 🔑 API Key 获取

### 步骤

1. **登录币安**
   - 实盘：https://www.binance.com
   - 测试网：https://testnet.binance.vision

2. **进入 API 管理**
   - 右上角头像 → API Management
   - 或：https://www.binance.com/my/settings/api-management

3. **创建 API Key**
   - 点击 **Create API**
   - 输入标签 (如：Taiyi-AGI)
   - 完成安全验证

4. **配置权限**
   - ✅ **Enable Reading** (读取账户信息)
   - ✅ **Enable Spot & Margin Trading** (现货交易)
   - ❌ **Enable Withdrawals** (提现，建议禁用)

5. **设置 IP 白名单 (推荐)**
   - 添加当前服务器 IP
   - 公网 IP: `103.172.182.26`

6. **保存凭证**
   - API Key (公开，可重置)
   - Secret Key (仅显示一次！立即保存)

---

## 🧪 测试网 vs 实盘

### 测试网 (推荐先用)

| 项目 | 配置 |
|------|------|
| URL | `https://testnet.binance.vision` |
| API Key | 需单独创建 (testnet.binance.vision) |
| 资金 | 虚拟资金 (免费 faucet) |
| 风险 | 无风险 |

**获取测试币**:
```bash
curl -X POST "https://testnet.binance.vision/faucet/withdraw" \
  -d "coin=USDT" \
  -d "amount=1000" \
  -H "X-MBX-APIKEY: your_testnet_api_key"
```

### 实盘

| 项目 | 配置 |
|------|------|
| URL | `https://api.binance.com` |
| API Key | 主站创建 |
| 资金 | 真实资金 |
| 风险 | 有资金风险 |

---

## 🐍 Python 客户端配置

### 基础用法 (REST API)

```python
import hmac
import hashlib
import time
import requests

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
BASE_URL = "https://testnet.binance.vision"  # 或 https://api.binance.com

def generate_signature(query_string):
    return hmac.new(
        API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

# 获取账户信息
url = f"{BASE_URL}/api/v3/account"
params = {"timestamp": int(time.time() * 1000)}
query_string = "&".join([f"{k}={v}" for k, v in params.items()])
params["signature"] = generate_signature(query_string)

headers = {"X-MBX-APIKEY": API_KEY}
resp = requests.get(url, headers=headers, params=params)
account = resp.json()
print(account)
```

### 下单示例 (限价单)

```python
# 下单
url = f"{BASE_URL}/api/v3/order"
params = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 0.001,
    "price": 50000.00,
    "timestamp": int(time.time() * 1000)
}

query_string = "&".join([f"{k}={v}" for k, v in params.items()])
params["signature"] = generate_signature(query_string)

resp = requests.post(url, headers=headers, params=params)
order = resp.json()
print(f"订单 ID: {order['orderId']}")
```

### 使用 CCXT (简化版)

```python
import ccxt

exchange = ccxt.binance({
    'apiKey': 'your_api_key',
    'secret': 'your_api_secret',
    'sandbox': True,  # 测试网
})

# 获取余额
balance = exchange.fetch_balance()
print(balance['total'])

# 下单
order = exchange.create_limit_buy_order('BTC/USDT', 0.001, 50000)
print(order)
```

---

## 🔧 常见错误排查

### 错误 1: `Invalid API-key`
```
❌ {"code":-2015,"msg":"Invalid API-key, IP, or permissions for key"}
```
**原因**: API Key 无效或权限不足
**解决**:
1. 检查 API Key 是否正确复制
2. 确认启用 **Spot & Margin Trading**
3. 检查 IP 白名单

### 错误 2: `Timestamp ahead of server`
```
❌ {"code":-1021,"msg":"Timestamp for this request is ahead of server's timestamp"}
```
**原因**: 系统时间不同步
**解决**:
```bash
# 同步系统时间
sudo ntpdate pool.ntp.org
```

### 错误 3: `Account has insufficient balance`
```
❌ {"code":-2010,"msg":"Account has insufficient balance for this action"}
```
**原因**: 账户余额不足
**解决**:
1. 充值到币安账户
2. 检查交易对最小交易量

### 错误 4: `Filter failure: LOT_SIZE`
```
❌ {"code":-2010,"msg":"Filter failure: LOT_SIZE"}
```
**原因**: 交易量不符合要求
**解决**:
- BTC/USDT 最小交易量：0.00001 BTC
- 调整下单数量

---

## 📊 API 端点参考

### 市场数据 (无需认证)
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v3/ticker/24hr` | GET | 24 小时行情 |
| `/api/v3/depth` | GET | 订单簿 |
| `/api/v3/klines` | GET | K 线数据 |
| `/api/v3/trades` | GET | 最近成交 |

### 账户数据 (需要认证)
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v3/account` | GET | 账户信息 |
| `/api/v3/balance` | GET | 余额 ( futures) |
| `/api/v3/myTrades` | GET | 成交历史 |

### 交易操作 (需要认证)
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v3/order` | POST | 创建订单 |
| `/api/v3/order` | DELETE | 取消订单 |
| `/api/v3/openOrders` | GET | 当前挂单 |

---

## 🛡️ 安全建议

### API Key 管理
- ✅ 使用环境变量存储
- ✅ 禁用提现权限
- ✅ 设置 IP 白名单
- ✅ 定期轮换
- ❌ 不要提交到 Git
- ❌ 不要分享给他人

### 配置文件权限
```bash
# 设置权限
chmod 600 ~/.taiyi/zhiji/binance.json

# Git 忽略
echo ".taiyi/" >> .gitignore
echo "*.json" >> .gitignore
```

---

## 📁 测试脚本

位置：`/home/nicola/.openclaw/workspace/scripts/binance-test.py`

**测试项目**:
1. API Key 连通性
2. 账户余额查询
3. 市场行情 (BTC/USDT)
4. 订单簿查询
5. 下单测试 (限价单)
6. 当前挂单查询

**运行**:
```bash
export BINANCE_API_KEY='your_key'
export BINANCE_API_SECRET='your_secret'
python3 scripts/binance-test.py
```

---

## 🔗 相关链接

- **币安官网**: https://www.binance.com
- **测试网**: https://testnet.binance.vision
- **API 文档**: https://binance-docs.github.io/apidocs/
- **GitHub SDK**: https://github.com/binance/binance-connector-python
- **CCXT**: https://github.com/ccxt/ccxt

---

## 📝 知几-E 集成计划

### 策略配置
- 交易对：BTC/USDT, ETH/USDT
- 置信度阈值：96%
- 下注策略：Quarter-Kelly
- 风控：日损 10%, 周损 20%

### 状态
- 🟡 测试脚本已创建
- 🔴 待 API Key 配置
- 🔴 待测试网测试
- 🔴 待实盘启动

---

*创建时间：2026-03-31 | 维护者：太一*
