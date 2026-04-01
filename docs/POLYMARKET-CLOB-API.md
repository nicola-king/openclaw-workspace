# Polymarket CLOB API 接入文档

> 创建时间：2026-03-31 | 状态：✅ 公开 API 已接入 | 🟡 待充值实盘

---

## 📋 目录

1. [环境配置](#环境配置)
2. [API 功能测试](#api 功能测试)
3. [认证流程](#认证流程)
4. [交易流程](#交易流程)
5. [配置模板](#配置模板)

---

## 🔧 环境配置

### 安装依赖

```bash
pip install py-clob-client
```

### 环境变量

```bash
# 私钥（用于生成 API 凭证）
export POLYMARKET_PRIVATE_KEY='your_private_key'

# 钱包地址
export POLYMARKET_WALLET='0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5'
```

### 配置文件

位置：`/home/nicola/.openclaw/workspace/credentials/polymarket.conf`

```ini
# Polymarket CLOB API 凭证
api_key=YOUR_API_KEY
api_secret=YOUR_API_SECRET
api_passphrase=YOUR_API_PASSPHRASE

# 钱包配置
wallet_address=0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5
chain_id=137
rpc_url=https://polygon-rpc.com
```

---

## ✅ API 功能测试

### 测试结果 (2026-03-31 11:16)

| 功能 | 状态 | 说明 |
|------|------|------|
| 创建客户端 | ✅ | 无认证模式 |
| 市场详情查询 | ✅ | get_market() |
| 订单簿查询 | ✅ | get_order_book() |
| 中间价查询 | ✅ | get_midpoint() |
| 活跃市场列表 | ✅ | Gamma API |
| API 凭证创建 | ⏳ | 需要私钥 |
| 下单交易 | ⏳ | 需要认证 + 充值 |

### 测试市场数据

**BitBoy convicted?** (ID: 531202)
- 流动性：$5,404.00
- 成交量：$350,964.71
- 最小 tick: 0.001
- 中间价：0.4055 (40.55% 概率)
- 买盘：5 档 | 卖盘：5 档

---

## 🔐 认证流程

### 方法 1: 使用私钥自动生成 (推荐)

```python
from py_clob_client.client import ClobClient

HOST = "https://clob.polymarket.com"
CHAIN_ID = 137
private_key = "your_private_key"

# 创建临时客户端
temp_client = ClobClient(HOST, key=private_key, chain_id=CHAIN_ID)

# 创建或派生 API 凭证
api_creds = temp_client.create_or_derive_api_creds()
print(f"API Key: {api_creds.api_key}")
print(f"API Secret: {api_creds.api_secret}")
print(f"API Passphrase: {api_creds.api_passphrase}")

# 创建交易客户端
client = ClobClient(
    HOST,
    key=private_key,
    chain_id=CHAIN_ID,
    creds=api_creds,
    signature_type=0,  # EOA 签名
)
```

### 方法 2: 手动配置 API 凭证

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds

HOST = "https://clob.polymarket.com"

api_creds = ApiCreds(
    api_key="your_api_key",
    api_secret="your_api_secret",
    api_passphrase="your_api_passphrase"
)

client = ClobClient(HOST, creds=api_creds)
```

---

## 💰 交易流程

### 1. 获取市场信息

```python
market = client.get_market(condition_id)
tick_size = market["minimum_tick_size"]  # e.g., "0.01"
neg_risk = market["neg_risk"]  # e.g., False
```

### 2. 获取订单簿

```python
book = client.get_order_book(token_id)
print(f"买盘：{book.bids[:5]}")
print(f"卖盘：{book.asks[:5]}")
```

### 3. 创建并下单

```python
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

response = client.create_and_post_order(
    OrderArgs(
        token_id=token_id,  # Yes 或 No token
        price=0.50,  # 价格 (0-1)
        size=10,  # 数量 (USDC)
        side=BUY,  # BUY 或 SELL
        order_type=OrderType.GTC,  # GTC = Good Till Cancel
    ),
    options={
        "tick_size": tick_size,
        "neg_risk": neg_risk,
    },
)

print(f"Order ID: {response['orderID']}")
print(f"Status: {response['status']}")
```

### 4. 查询余额

```python
balances = client.get_balances()
print(f"USDC 余额：{balances['USDC']}")
print(f"可用余额：{balances['POLY']}")
```

### 5. 查询订单

```python
# 查询所有订单
orders = client.get_orders()

# 查询特定市场订单
orders = client.get_orders(market_id="531202")
```

### 6. 取消订单

```python
response = client.cancel_order(order_id)
```

---

## 📁 配置模板

### 测试脚本

位置：`/home/nicola/.openclaw/workspace/scripts/poly-clob-test.py`

```bash
# 运行测试
python3 scripts/poly-clob-test.py
```

### 知几-E 集成

位置：`/home/nicola/.openclaw/workspace/skills/zhiji/polymarket_client.py`

```python
# 已集成 CLOB API 客户端
from skills.zhiji.polymarket_client import PolymarketClient

client = PolymarketClient(
    private_key=os.getenv("POLYMARKET_PRIVATE_KEY"),
    chain_id=137
)

# 查询市场
market = client.get_market("531202")

# 下单
order = client.place_order(
    market_id="531202",
    side="BUY",
    price=0.40,
    size=10
)
```

---

## 🚀 实盘启动清单

### 前置条件

- [x] py-clob-client 已安装
- [x] 公开 API 测试通过
- [ ] 私钥配置 (`POLYMARKET_PRIVATE_KEY`)
- [ ] 钱包充值 USDC (Polygon 网络)
- [ ] 测试网测试完成

### 启动步骤

1. **配置私钥**
   ```bash
   export POLYMARKET_PRIVATE_KEY='your_private_key'
   ```

2. **充值 USDC**
   - 网络：Polygon (Chain ID: 137)
   - 地址：`0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5`
   - 代币：USDC (0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174)

3. **测试下单**
   ```bash
   python3 scripts/poly-clob-test.py
   ```

4. **启动知几-E**
   ```bash
   python3 skills/zhiji/zhiji-e.py
   ```

---

## 📊 当前市场数据 (2026-03-31 11:16)

| 市场 | 流动性 | 成交量 | 中间价 |
|------|--------|--------|--------|
| BitBoy convicted? | $5,404 | $350,965 | 0.4055 |
| Russia-Ukraine Ceasefire | $48,953 | $1,408,108 | - |
| New Rihanna Album | $42,254 | $677,389 | - |
| New Playboi Carti Album | $33,286 | $711,892 | - |
| Jesus Christ return | $711,772 | $10,367,361 | - |

---

## 🔗 相关链接

- Polymarket 官网：https://polymarket.com
- CLOB API 文档：https://docs.polymarket.com/api-reference
- GitHub: https://github.com/polymarket/py-clob-client
- Polygon Scan: https://polygonscan.com

---

*创建时间：2026-03-31 11:17 | 太一 AGI*
