# 币安交易 Skill

> 版本：v1.0 | 创建：2026-03-30 10:32
> 状态：🟡 待配置 Secret Key
> 目标：知几-E 策略对接币安实盘

---

## 🎯 功能概述

| 功能 | 描述 | 状态 |
|------|------|------|
| **API 验证** | 验证币安 API Key 有效性 | ✅ 已完成 |
| **账户查询** | 获取余额/权限信息 | 🟡 待 Secret Key |
| **现货交易** | BTC/ETH 现货买卖 | 🟡 待 Secret Key |
| **策略对接** | 知几-E v5.4 集成 | 🟡 待开发 |
| **风控管理** | 止损/止盈/仓位控制 | 🟡 待开发 |
| **日志监控** | Telegram 实时通知 | 🔴 待开发 |

---

## 🔧 配置状态

### ✅ 已完成
- API Key 已保存：`cMtuxE7spO...lzqQTy`
- 基础连接测试通过
- 配置文件已创建：`config/binance-config.json`

### ⚠️ 待办事项
1. **补充 Secret Key** - 需要用户提供
2. 验证账户权限和余额
3. 配置 IP 白名单
4. 知几-E 策略集成

---

## 📁 文件结构

```
skills/binance-trader/
├── SKILL.md                    # 本文档 ✅
├── validate-api.py             # API 验证脚本 ✅
├── binance-client.py           # 币安 API 客户端 🟡 待创建
├── binance-strategy.py         # 交易策略 🟡 待创建
└── scripts/
    ├── test-connection.sh      # 连接测试 ✅
    └── execute-trade.sh        # 交易执行 🟡 待创建
```

---

## 🔐 安全配置

### API Key 权限要求

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
gpg -c /home/nicola/.openclaw/.env.binance
rm /home/nicola/.openclaw/.env.binance
```

---

## 🚀 快速启动

### Step 1: 补充 Secret Key

编辑配置文件：
```bash
nano /home/nicola/.openclaw/.env.binance
```

添加 Secret Key:
```
BINANCE_SECRET_KEY=你的 Secret Key
```

### Step 2: 验证 API

```bash
cd ~/.openclaw/workspace
python3 skills/binance-trader/validate-api.py
```

### Step 3: 测试交易

```bash
# 待创建交易脚本后执行
python3 skills/binance-trader/binance-client.py --test
```

---

## 📊 交易策略 (知几-E v5.4 集成)

### 交易规则

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
    max_position_usdt: 100    # 单交易最大仓位
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
   ├─ API 验证
   ├─ 订单执行
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

## 📋 定时任务 (待配置)

```bash
# 币安价格监控 (每 5 分钟)
*/5 * * * * /home/nicola/.openclaw/workspace/skills/binance-trader/scripts/price-monitor.sh

# 交易策略执行 (每 30 分钟)
*/30 * * * * /home/nicola/.openclaw/workspace/skills/binance-trader/scripts/execute-trade.sh

# 日报生成 (每日 20:00)
0 20 * * * /home/nicola/.openclaw/workspace/skills/binance-trader/scripts/daily-report.sh
```

---

## 📊 阶段目标

| 阶段 | 目标 | 时间 | 状态 |
|------|------|------|------|
| **Phase 1** | 配置保存 | 5 分钟 | ✅ 已完成 |
| **Phase 2** | API 验证 | 10 分钟 | 🟡 部分完成 (待 Secret Key) |
| **Phase 3** | Skill 集成 | 15 分钟 | 🟡 进行中 |
| **Phase 4** | 策略对接 | 30 分钟 | 🔴 待执行 |

---

## 🔗 相关链接

- 币安 API 文档：https://binance-docs.github.io/apidocs/
- 币安测试网：https://testnet.binance.vision/
- 知几-E 策略：`skills/zhiji/`

---

*版本：v1.0 | 创建时间：2026-03-30 10:32*
*状态：🟡 待配置 Secret Key*
*太一 AGI · 知几-E v5.4 币安集成*
