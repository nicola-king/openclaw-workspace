# 币安自动化交易 Skill

> 版本：v1.0 | 创建：2026-03-28 20:25
> 状态：🟡 测试网模式 (待配置 API Key)
> 目标：零风险验证 → 小资金实盘 → 策略优化

---

## 🎯 功能概述

| 功能 | 描述 | 状态 |
|------|------|------|
| **测试网交易** | 币安测试网模拟交易 | 🟡 待配置 |
| **实盘交易** | 币安主网真实交易 | 🔴 待开发 |
| **策略执行** | 知几-E v5.4 策略 | 🟡 待集成 |
| **风控管理** | 止损/止盈/仓位 | 🟡 待配置 |
| **日志监控** | Telegram 实时通知 | 🟡 待配置 |

---

## 🔧 配置步骤

### Step 1: 注册币安测试网 (5 分钟)

**网址**: https://testnet.binance.vision/

```
1. 访问测试网
2. GitHub 账号登录 (推荐)
3. 点击 "API Key" → "Generate HMAC_SHA256 Key"
4. 保存 API Key 和 Secret Key
```

**测试资金**:
- 现货测试网：10,000 USDT
- 合约测试网：100,000 USDT

---

### Step 2: 配置太一环境变量

**创建配置文件**:
```bash
cat > /home/nicola/.openclaw/.env.binance-testnet << EOF
# 币安测试网 API
BINANCE_TESTNET=true
BINANCE_API_KEY=你的测试网 API Key
BINANCE_SECRET_KEY=你的测试网 Secret Key
BINANCE_BASE_URL=https://testnet.binance.vision

# 测试资金
TESTNET_INITIAL_BALANCE=10000

# 交易配置
KELLY_MODE=quarter
CONFIDENCE_THRESHOLD=0.96
MAX_POSITION_USDT=500
EOF

# 设置权限
chmod 600 /home/nicola/.openclaw/.env.binance-testnet
```

---

### Step 3: 安装依赖

```bash
pip install python-binance aiohttp python-dotenv
```

---

### Step 4: 测试连接

```bash
cd ~/.openclaw/workspace/skills/zhiji
python3 binance-testnet-trader.py
```

**预期输出**:
```
🧪 币安测试网交易验证启动...
📊 获取账户信息...
💰 当前余额：10000.00 USDT
📈 执行测试交易...
✅ 测试订单已下：BUY 0.001 BTCUSDT @ 50000
✅ 测试订单已下：SELL 0.01 ETHUSDT @ 3000
📝 生成测试报告...
✅ 测试报告已生成
```

---

## 📊 交易策略 (BTC/ETH 双币种)

### 知几-E v5.4 集成

```yaml
zhiji_e_binance:
  version: 5.4
  trading_pairs:
    - BTCUSDT    # 仅交易 BTC
    - ETHUSDT    # 仅交易 ETH
  
  data_sources:
    - Polymarket 热度前 5 (天气预测)
    - 币安 BTC/ETH 价格
    - 市场情绪分析 (FinBERT)
  
  trading_rules:
    confidence_threshold: 0.96
    advantage_threshold: 0.02
    kelly_mode: quarter
    max_position_usdt: 500    # 单交易最大仓位
    stop_loss: -0.02          # -2% 止损
    take_profit: 0.50         # +50% 止盈
  
  risk_management:
    daily_stop_loss: -0.05    # -5% 日止损
    single_trade_stop: -0.02  # -2% 单交易止损
    profit_withdraw: 0.50     # 50% 利润提现
    btc_allocation: 0.60      # BTC 60% 仓位
    eth_allocation: 0.40      # ETH 40% 仓位
  
  iron_rule:
    - 仅交易 BTC 和 ETH
    - 不交易山寨币
    - 现货杠杆 2-3 倍 (合理开)
    - 不开合约 (Futures)
    - 不玩高杠杆 (>5 倍)
```

---

## 🎯 执行流程

```
1. 数据采集 (每 30 分钟)
   ├─ Polymarket 天气预测
   ├─ 币安 BTC/ETH 价格
   └─ 市场情绪分析

2. 策略分析
   ├─ 置信度计算
   ├─ 优势评估
   └─ 下注比例 (Kelly)

3. 交易执行
   ├─ 测试网验证
   ├─ 实盘执行 (如配置)
   └─ 订单追踪

4. 风控监控
   ├─ 止损检查
   ├─ 止盈检查
   └─ 仓位管理

5. 报告生成
   ├─ 交易记录
   ├─ 盈亏统计
   └─ Telegram 通知
```

---

## 📋 定时任务

```bash
# 币安价格监控 (每 5 分钟)
*/5 * * * * /home/nicola/.openclaw/workspace/skills/zhiji/binance-trading/price-monitor.sh

# 交易策略执行 (每 30 分钟)
*/30 * * * * /home/nicola/.openclaw/workspace/skills/zhiji/binance-trading/execute-trade.sh

# 日报生成 (每日 20:00)
0 20 * * * /home/nicola/.openclaw/workspace/skills/zhiji/binance-trading/daily-report.sh
```

---

## 🔒 安全配置

### API Key 权限

```
✅ Enable Reading (读取权限)
✅ Spot & Margin Trading (现货交易)
❌ Withdrawals (禁止提现) ← 重要！
```

### IP 白名单

```
限制仅允许工控机 IP 访问
例如：123.45.67.89/32
```

### 加密存储

```bash
# 使用 gpg 加密配置文件
gpg -c .env.binance-testnet
rm .env.binance-testnet
```

---

## 📊 测试网 vs 实盘

| 维度 | 测试网 | 实盘 |
|------|--------|------|
| **资金** | 10,000 USDT (模拟) | 真实 USDT |
| **风险** | 零风险 | 有亏损风险 |
| **用途** | 策略验证 | 真实盈利 |
| **建议** | 先测试 30 笔交易 | 测试稳定后实盘 |

---

## 🎯 阶段目标

| 阶段 | 目标 | 时间 | 状态 |
|------|------|------|------|
| **Phase 1** | 测试网配置完成 | 30 分钟 | 🟡 待执行 |
| **Phase 2** | 测试网交易 30 笔 | 1 天 | 🔴 待执行 |
| **Phase 3** | 胜率>60% | 3 天 | 🔴 待执行 |
| **Phase 4** | 小资金实盘 ($50) | 1 周 | 🔴 待执行 |
| **Phase 5** | 策略优化 + 扩大 | 1 月 | 🔴 待执行 |

---

## 📁 文件结构

```
skills/zhiji/binance-trading/
├── SKILL.md                    # 本文档
├── binance-testnet-trader.py   # 测试网交易脚本 ✅
├── binance-client.py           # 币安 API 客户端 🟡 待创建
├── binance-strategy.py         # 交易策略 🟡 待创建
├── binance-risk-management.py  # 风控模块 🟡 待创建
├── binance-config.yaml         # 配置文件 🟡 待创建
└── scripts/
    ├── install-deps.sh         # 依赖安装 🟡 待创建
    ├── test-connection.sh      # 连接测试 🟡 待创建
    ├── price-monitor.sh        # 价格监控 🟡 待创建
    └── daily-report.sh         # 日报生成 🟡 待创建
```

---

## 🚀 快速启动

```bash
# 1. 安装依赖
pip install python-binance aiohttp python-dotenv

# 2. 配置 API Key
# 访问 https://testnet.binance.vision/ 获取测试网 Key

# 3. 创建配置文件
cat > /home/nicola/.openclaw/.env.binance-testnet << EOF
BINANCE_API_KEY=你的 Key
BINANCE_SECRET_KEY=你的 Secret
BINANCE_BASE_URL=https://testnet.binance.vision
EOF

# 4. 测试运行
cd ~/.openclaw/workspace/skills/zhiji
python3 binance-testnet-trader.py
```

---

*版本：v1.0 | 创建时间：2026-03-28 20:25*
*状态：🟡 测试网模式 (待配置 API Key)*
*太一 AGI · 知几-E v5.4 币安集成*
