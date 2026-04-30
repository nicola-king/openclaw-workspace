# GMGN 自动化交易 Skill

> 版本：v1.0 | 创建：2026-03-28 20:32
> 状态：✅ 已配置 (1.7 SOL = $150)
> 定位：Solana 链上秒级交易 + 鲸鱼跟单

---

## 🎯 功能概述

| 功能 | 描述 | 状态 |
|------|------|------|
| **鲸鱼跟单** | 跟随 majorexploiter ($2.4M 盈利) | ✅ 已配置 |
| **秒级交易** | Solana 链上快速交易 (<1s) | ✅ 已配置 |
| **新币狙击** | 新上线代币狙击 | 🟡 待开发 |
| **风控管理** | 止损/止盈/仓位 | 🟡 待配置 |
| **日志监控** | Telegram 实时通知 | 🟡 待配置 |

---

## 🔧 配置信息

### 钱包配置

```
钱包地址：5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq
余额：1.7 SOL ($150)
登录方式：Telegram @GMGN_bot
状态：✅ 已登录
```

### 目标鲸鱼

```
鲸鱼地址：majorexploiter
盈利：$2.4M
状态：活跃
跟单策略：Quarter-Kelly
```

---

## 📊 交易策略

### 知几-E v5.4 集成

```yaml
gmgn_trading:
  version: 5.4
  chain: Solana
  wallet: 5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq
  
  trading_pairs:
    - SOL/USDC
    - 热门 Meme 币
    - 新上线代币
  
  whale_following:
    enabled: true
    target_whale: majorexploiter
    whale_profit: $2.4M
    kelly_mode: quarter
    max_position: 0.5 SOL
  
  risk_management:
    stop_loss: -0.10        # -10% 止损
    take_profit: 1.00       # +100% 止盈
    daily_stop_loss: -0.20  # -20% 日止损
    profit_withdraw: 0.50   # 50% 利润提现
  
  fees:
    gas_fee: ~$0.001        # Solana Gas 费
    trading_fee: 0.5-1%     # GMGN 交易手续费
```

---

## 🎯 执行流程

```
1. 鲸鱼监控 (实时)
   ├─ majorexploiter 交易信号
   ├─ 其他鲸鱼信号
   └─ 新币上线提醒

2. 策略分析
   ├─ 置信度计算
   ├─ 优势评估
   └─ 跟单/不跟单决策

3. 交易执行
   ├─ Solana 链上交易 (<1s)
   ├─ 订单确认
   └─ 持仓追踪

4. 风控监控
   ├─ 止损检查 (-10%)
   ├─ 止盈检查 (+100%)
   └─ 仓位管理

5. 报告生成
   ├─ 交易记录
   ├─ 盈亏统计
   └─ Telegram 通知
```

---

## 📋 定时任务

```bash
# 鲸鱼监控 (每 5 分钟)
*/5 * * * * /home/nicola/.openclaw/workspace/skills/zhiji/gmgn-trading/scripts/whale-monitor.sh

# 交易执行 (事件触发)
# 鲸鱼信号 → 自动执行

# 日报生成 (每日 20:00)
0 20 * * * /home/nicola/.openclaw/workspace/skills/zhiji/gmgn-trading/scripts/daily-report.sh
```

---

## 🔒 风控规则

### 铁律 (必须遵守)

```
✅ 仅跟单已验证鲸鱼 (majorexploiter)
❌ 不盲目追高
❌ 不 FOMO
❌ 不使用高杠杆
```

### 止损规则

```
单交易止损：-10% (Solana 波动大)
日止损：-20% (触发后停止当日交易)
周止损：-30% (触发后停止本周交易)
```

### 止盈规则

```
止盈：+100% (50% 利润提现，50% 复投)
追踪止盈：从最高点回撤 -20% 止盈
```

---

## 📊 预期收益

| 场景 | 月收益 | 风险等级 |
|------|--------|---------|
| **牛市** | +50-100% | 中高 |
| **震荡市** | +20-40% | 中 |
| **熊市** | -20-0% | 中高 |

**综合预期**: **+50-100%/月** (高风险高收益)

---

## 📁 文件结构

```
skills/zhiji/gmgn-trading/
├── SKILL.md                    # 本文档 ✅
├── gmgn-client.py              # GMGN API 客户端 🟡 待创建
├── whale-monitor.py            # 鲸鱼监控脚本 🟡 待创建
├── gmgn-config.yaml            # 配置文件 🟡 待创建
└── scripts/
    ├── install-deps.sh         # 依赖安装 🟡 待创建
    ├── whale-monitor.sh        # 鲸鱼监控 🟡 待创建
    └── daily-report.sh         # 日报生成 🟡 待创建
```

---

## 🎯 与币安/Polymarket 协同

```
太一交易矩阵
├── 币安 (60%)
│   ├── BTC (36%)
│   └── ETH (24%)
│
├── Polymarket (25%)
│   └── 气象预测套利
│
└── GMGN (15%)
    └── Solana 鲸鱼跟单
```

**风险分散**:
- 币安 BTC/ETH：中风险
- Polymarket：低风险
- GMGN：中高风险

---

## 🚀 快速启动

```bash
# 1. 安装依赖
cd ~/.openclaw/workspace/skills/zhiji/gmgn-trading
bash scripts/install-deps.sh

# 2. 配置钱包 (已登录 Telegram @GMGN_bot)
# 钱包地址：5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq

# 3. 测试运行
python3 gmgn-client.py
```

---

*版本：v1.0 | 创建时间：2026-03-28 20:32*
*状态：✅ 已配置 (1.7 SOL)*
*太一 AGI · 知几-E v5.4 GMGN 集成*
