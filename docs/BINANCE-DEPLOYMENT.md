# 币安交易机器人部署指南

> 创建时间：2026-03-31 | 状态：🟡 待 API Key 配置 | 类型：现货网格交易

---

## 📋 目录

1. [快速开始](#快速开始)
2. [API Key 配置](#api-key-配置)
3. [机器人部署](#机器人部署)
4. [实盘配置](#实盘配置)
5. [风险控制](#风险控制)

---

## 🚀 快速开始

### 前置条件
- ✅ 币安账户 (已完成 KYC)
- ✅ API Key + Secret
- ✅ 账户有 USDT 余额

### 三步部署
```bash
# 1. 设置 API Key
export BINANCE_API_KEY='your_api_key'
export BINANCE_API_SECRET='your_secret'

# 2. 运行测试
python3 scripts/binance-grid-bot.py

# 3. 启动实盘
python3 scripts/binance-grid-bot.py --live
```

---

## 🔑 API Key 配置

### 步骤

**1. 登录币安**
- 官网：https://www.binance.com
- API 管理：https://www.binance.com/my/settings/api-management

**2. 创建 API Key**
- 点击 **Create API**
- 输入标签：`Taiyi-AGI-Bot`
- 完成安全验证 (邮箱 + 手机 + Google Auth)

**3. 配置权限**
- ✅ **Enable Reading** (必需)
- ✅ **Enable Spot & Margin Trading** (必需)
- ❌ **Enable Withdrawals** (禁用，安全)

**4. 设置 IP 白名单**
```
推荐启用 IP 白名单
添加：103.172.182.26 (当前服务器公网 IP)
```

**5. 保存凭证**
- API Key: `xH...5k` (公开)
- Secret Key: `8j...m2` (仅显示一次！立即保存)

**6. 设置环境变量**
```bash
# 临时设置 (当前 session)
export BINANCE_API_KEY='your_api_key'
export BINANCE_API_SECRET='your_api_secret'

# 永久设置 (~/.bashrc)
echo "export BINANCE_API_KEY='your_api_key'" >> ~/.bashrc
echo "export BINANCE_API_SECRET='your_api_secret'" >> ~/.bashrc
source ~/.bashrc
```

---

## 🤖 机器人部署

### 方式 1: 直接运行 (推荐新手)

```bash
# 测试模式 (不下单)
python3 scripts/binance-grid-bot.py

# 实盘模式 (真实交易)
python3 scripts/binance-grid-bot.py --live
```

### 方式 2: systemd 服务 (后台运行)

**1. 创建服务文件**
```bash
sudo nano /etc/systemd/system/binance-bot.service
```

**2. 配置内容**
```ini
[Unit]
Description=Binance Grid Trading Bot
After=network.target

[Service]
Type=simple
User=nicola
WorkingDirectory=/home/nicola/.openclaw/workspace
Environment="BINANCE_API_KEY=your_api_key"
Environment="BINANCE_API_SECRET=your_api_secret"
ExecStart=/usr/bin/python3 scripts/binance-grid-bot.py --live
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**3. 启动服务**
```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start binance-bot

# 开机自启
sudo systemctl enable binance-bot

# 查看状态
sudo systemctl status binance-bot

# 查看日志
sudo journalctl -u binance-bot -f
```

### 方式 3: Docker 部署 (隔离环境)

**1. 创建 Dockerfile**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts/ ./scripts/
CMD ["python3", "scripts/binance-grid-bot.py", "--live"]
```

**2. 构建并运行**
```bash
docker build -t binance-bot .
docker run -d \
  -e BINANCE_API_KEY=your_key \
  -e BINANCE_API_SECRET=your_secret \
  --name bot \
  binance-bot
```

---

## 📊 实盘配置

### 网格参数配置

**编辑配置文件** `config/grid_config.json`:
```json
{
  "symbol": "BTCUSDT",
  "grid_num": 10,
  "investment_usdt": 100,
  "price_range": {
    "low": 80000,
    "high": 120000
  },
  "stop_loss": 0.10,
  "take_profit": 0.20
}
```

### 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `symbol` | 交易对 | BTCUSDT, ETHUSDT |
| `grid_num` | 网格数量 | 10-20 |
| `investment_usdt` | 投资金额 | 100-1000 USDT |
| `low` | 价格下限 | 当前价 -20% |
| `high` | 价格上限 | 当前价 +20% |
| `stop_loss` | 止损比例 | 10% |
| `take_profit` | 止盈比例 | 20% |

### 推荐交易对

| 交易对 | 波动性 | 流动性 | 风险 |
|--------|--------|--------|------|
| BTCUSDT | 中 | 高 | 低 |
| ETHUSDT | 中 | 高 | 低 |
| BNBUSDT | 中高 | 高 | 中 |
| SOLUSDT | 高 | 中 | 中高 |

---

## ⚠️ 风险控制

### 资金管理

**建议配置**:
- 单笔投资：≤ 总资金的 5%
- 日损上限：10%
- 周损上限：20%
- 最大回撤：15%

**示例**:
```
总资金：1000 USDT
单笔投资：50 USDT (5%)
日损上限：100 USDT (10%)
触发后停止交易 24 小时
```

### 安全建议

**API Key 安全**:
- ✅ 使用环境变量存储
- ✅ 禁用提现权限
- ✅ 设置 IP 白名单
- ✅ 定期轮换 (每月)
- ❌ 不要提交到 Git
- ❌ 不要分享给他人

**交易安全**:
- ✅ 设置止损
- ✅ 小额测试开始
- ✅ 监控账户余额
- ✅ 定期检查挂单
- ❌ 不要全仓交易
- ❌ 不要频繁修改策略

### 监控告警

**Telegram 通知**:
```python
# 配置通知
TELEGRAM_BOT_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID = 'your_chat_id'

# 触发条件
- 订单成交
- 止损触发
- 余额不足
- API 错误
```

---

## 🔧 常见问题

### Q1: API 返回 -2015 错误
```
{"code":-2015,"msg":"Invalid API-key, IP, or permissions for key"}
```
**解决**:
1. 检查 API Key 是否正确
2. 确认启用 Spot Trading 权限
3. 检查 IP 白名单

### Q2: 订单失败 - 数量过小
```
{"code":-2010,"msg":"Filter failure: LOT_SIZE"}
```
**解决**:
- BTC 最小交易量：0.00001
- 调整网格投资金额

### Q3: 时间戳错误
```
{"code":-1021,"msg":"Timestamp ahead of server"}
```
**解决**:
```bash
sudo ntpdate pool.ntp.org
```

---

## 📁 文件结构

```
/home/nicola/.openclaw/workspace/
├── scripts/
│   ├── binance-grid-bot.py    # 主程序
│   ├── binance-test.py        # 测试脚本
│   └── binance-live.py        # 实盘脚本
├── config/
│   └── grid_config.json       # 网格配置
├── logs/
│   └── binance-bot.log        # 运行日志
└── docs/
    └── BINANCE-DEPLOYMENT.md  # 本文档
```

---

## 🔗 相关链接

- **币安官网**: https://www.binance.com
- **API 文档**: https://developers.binance.com/docs/binance-spot-api-docs
- **GitHub SDK**: https://github.com/binance/binance-connector-python
- **API 电报群**: https://t.me/binance_api_announcements

---

## 📝 当前状态

| 组件 | 状态 |
|------|------|
| 测试脚本 | ✅ 已创建 |
| 网格机器人 | ✅ 已创建 |
| 部署文档 | ✅ 已创建 |
| API Key | 🔴 待配置 |
| 测试网测试 | 🔴 待执行 |
| 实盘交易 | 🔴 待启动 |

---

*创建时间：2026-03-31 | 维护者：太一*
