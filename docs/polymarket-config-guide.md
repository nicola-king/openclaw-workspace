# Polymarket 配置指南 (2026)

> 最后更新：2026-03-31 | 状态：✅ 已验证 | 版本：v3.0

---

## 📋 目录

1. [快速开始](#快速开始)
2. [API Key 获取](#api-key-获取)
3. [配置文件结构](#配置文件结构)
4. [Python 客户端配置](#python-客户端配置)
5. [常见错误排查](#常见错误排查)

---

## 🚀 快速开始

### 前置条件
- ✅ Polygon 钱包 (MetaMask 等)
- ✅ USDC (Polygon 网络)
- ✅ Polymarket 账户 (已完成 KYC)

### 三步配置
```bash
# 1. 创建配置目录
mkdir -p ~/.taiyi/zhiji

# 2. 创建配置文件
cat > ~/.taiyi/zhiji/polymarket.json << 'EOF'
{
  "polymarket": {
    "api_key": "YOUR_API_KEY_HERE",
    "wallet_address": "0xYOUR_WALLET_ADDRESS",
    "chain_id": 137,
    "signer_private_key": "YOUR_PRIVATE_KEY"  // 可选，仅下单需要
  }
}
EOF

# 3. 测试连接
python3 scripts/zhiji-first-bet-v2.py
```

---

## 🔑 API Key 获取

### 方法 1: Polymarket 官网 (推荐)
1. 访问 https://polymarket.com
2. 登录账户
3. 进入 **Settings** → **API**
4. 点击 **Create API Key**
5. 设置权限：
   - ✅ Read (只读)
   - ✅ Trade (交易)
   - ⏸️ Withdraw (提现，建议禁用)
6. 保存 API Key (仅显示一次！)

### 方法 2: CLOB API 直接注册
1. 访问 https://clob.polymarket.com
2. 使用钱包签名登录
3. 在 Dashboard 生成 API Key

### 权限说明
| 权限 | 用途 | 风险 |
|------|------|------|
| **Read** | 查询市场/余额/订单 | 低 |
| **Trade** | 下单/取消订单 | 中 |
| **Withdraw** | 资金转出 | 高 (建议禁用) |

---

## 📁 配置文件结构

### 完整配置 (~/.taiyi/zhiji/polymarket.json)
```json
{
  "polymarket": {
    "api_key": "019d1b31-787e-7829-87b7-f8382effbab2",
    "wallet_address": "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf",
    "chain_id": 137,
    "signer_private_key": "",
    "proxy": {
      "enabled": false,
      "http": "http://127.0.0.1:7890",
      "https": "http://127.0.0.1:7890"
    }
  },
  "trading": {
    "confidence_threshold": 0.96,
    "edge_threshold": 0.02,
    "kelly_fraction": 0.25,
    "max_position_usd": 100,
    "min_liquidity_usd": 50000
  },
  "data": {
    "storage_path": "~/polymarket-data",
    "cache_ttl_seconds": 300
  }
}
```

### 字段说明
| 字段 | 必填 | 说明 |
|------|------|------|
| `api_key` | ✅ | Polymarket API Key |
| `wallet_address` | ✅ | Polygon 钱包地址 |
| `chain_id` | ⏸️ | 链 ID (Polygon=137) |
| `signer_private_key` | ⏸️ | 私钥 (仅下单需要) |
| `proxy.enabled` | ⏸️ | 是否启用代理 |
| `proxy.http` | ⏸️ | HTTP 代理地址 |
| `confidence_threshold` | ⏸️ | 置信度阈值 (0.96=96%) |
| `edge_threshold` | ⏸️ | 优势阈值 (0.02=2%) |
| `kelly_fraction` | ⏸️ | Kelly 比例 (0.25=Quarter-Kelly) |

---

## 🐍 Python 客户端配置

### 安装依赖
```bash
pip install py-clob-client
pip install polymarket-apis  # 可选，增强版
```

### 基础用法 (只读模式)
```python
from py_clob_client.client import ClobClient

API_KEY = "019d1b31-787e-7829-87b7-f8382effbab2"

client = ClobClient(
    host="https://clob.polymarket.com",
    key=API_KEY,
    chain_id=137,
)

# 测试连接
print(client.get_ok())  # "ok"

# 获取服务器时间
print(client.get_server_time())

# 获取市场
markets = client.get_sampling_simplified_markets()
print(f"Found {len(markets)} markets")

# 获取余额
balance = client.get_balance()
print(f"USDC Balance: {balance}")
```

### 交易模式 (需要私钥)
```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType, Side

PRIVATE_KEY = "YOUR_PRIVATE_KEY"

client = ClobClient(
    host="https://clob.polymarket.com",
    key=API_KEY,
    chain_id=137,
    signature=PRIVATE_KEY,  # 私钥签名
)

# 下单
order = OrderArgs(
    token_id="TOKEN_ID_HERE",
    price=0.50,  # 价格 (0-1)
    size=100.0,  # 数量 (USDC)
    side=Side.BUY,  # BUY or SELL
    order_type=OrderType.GTC,  # GTC=Good Till Cancel
)

order_id = client.create_and_post_order(order)
print(f"Order ID: {order_id}")
```

### 代理配置 (中国大陆)
```python
import os
import httpx

# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

# 或使用自定义 HTTP 客户端
from py_clob_client.client import ClobClient
import httpx

proxy_client = httpx.Client(
    proxies={
        "http://": "http://127.0.0.1:7890",
        "https://": "http://127.0.0.1:7890",
    }
)

client = ClobClient(
    host="https://clob.polymarket.com",
    key=API_KEY,
    chain_id=137,
    http_client=proxy_client,
)
```

---

## 🔧 常见错误排查

### 错误 1: `AuthenticationError`
```
❌ py_clob_client.exceptions.AuthenticationError: Invalid API credentials
```
**原因**: API Key 无效或过期
**解决**:
1. 检查 API Key 是否正确复制
2. 在 Polymarket 官网重新生成 API Key
3. 确认 API Key 权限包含所需操作

### 错误 2: `ConnectionError`
```
❌ httpx.ConnectError: Connection refused
```
**原因**: 网络问题或需要代理
**解决**:
```bash
# 检查代理
curl -I https://clob.polymarket.com

# 配置代理
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```

### 错误 3: `InsufficientBalance`
```
❌ py_clob_client.exceptions.InsufficientBalance: Not enough USDC
```
**原因**: 钱包 USDC 余额不足
**解决**:
1. 在 Polygon 网络充值 USDC
2. 检查钱包地址是否正确
3. 确认 USDC 已桥接到 Polygon

### 错误 4: `MarketClosedError`
```
❌ Market is closed for trading
```
**原因**: 市场已关闭或结算
**解决**:
1. 检查市场状态
2. 选择活跃市场 (liquidity > $50K)
3. 使用 `get_sampling_simplified_markets()` 获取活跃市场

---

## 📊 API 端点参考

### 市场数据
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/sampling-simplified-markets` | GET | 获取热门市场 |
| `/api/markets/{condition_id}` | GET | 获取市场详情 |
| `/api/orderbook` | GET | 获取订单簿 |
| `/api/tickers` | GET | 获取行情 |

### 账户数据
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/balance` | GET | 获取余额 |
| `/api/positions` | GET | 获取持仓 |
| `/api/orders` | GET | 获取订单列表 |
| `/api/trades` | GET | 获取成交记录 |

### 交易操作
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/order` | POST | 创建订单 |
| `/api/cancel` | POST | 取消订单 |
| `/api/cancel-all` | POST | 取消所有订单 |
| `/api/withdraw` | POST | 提现 (需权限) |

---

## 🛡️ 安全建议

### API Key 管理
- ✅ 使用环境变量或加密配置文件
- ✅ 禁用不需要的权限 (如 Withdraw)
- ✅ 定期轮换 API Key
- ❌ 不要提交到 Git
- ❌ 不要分享给他人

### 配置文件权限
```bash
# 设置配置文件权限 (仅所有者可读写)
chmod 600 ~/.taiyi/zhiji/polymarket.json

# 设置目录权限
chmod 700 ~/.taiyi/zhiji
```

### Git 忽略
```bash
# .gitignore
.taiyi/
*.json  # 配置文件
.env    # 环境变量
```

---

## 🔗 相关链接

- **官方文档**: https://docs.polymarket.com
- **CLOB API**: https://clob.polymarket.com
- **GitHub SDK**: https://github.com/polymarket/py-clob-client
- **Discord 社区**: https://discord.gg/polymarket
- **Polygon 浏览器**: https://polygonscan.com

---

## 📝 知几-E 配置示例

当前生效配置 (MEMORY.md):
```json
{
  "api_key": "019d1b31-787e-7829-87b7-f8382effbab2",
  "wallet_address": "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf",
  "username": "SAYELF",
  "email": "chuanxituzhu@gmail.com"
}
```

**策略配置**:
- 置信度阈值：96%
- 优势阈值：2%
- 下注策略：Quarter-Kelly
- 数据：189 条气象记录入库

**状态**: 🟡 基础设施就绪，待实盘

---

*文档版本：v3.0 | 最后更新：2026-03-31 | 维护者：太一*
