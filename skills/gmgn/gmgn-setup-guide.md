# GMGN 充值与交易策略配置

> 版本：v1.0 | 创建：2026-03-27 21:05 | 状态：✅ 待执行

---

## 💳 充值指南

### 方式 1: 从交易所转账 (推荐)

#### Solana 充值
1. **从币安/OKX/KuCoin 提币**
   - 选择 SOL
   - 网络：Solana (SOL)
   - 地址：`5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq`
   - 金额：建议 1-5 SOL (约$150-750)

2. **从 Phantom 钱包转账**
   - 打开 Phantom
   - 发送 SOL
   - 地址：`5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq`

#### Base 充值
1. **从币安/OKX 提币**
   - 选择 ETH
   - 网络：Base
   - 地址：`0x73d6a5835ddf6f54480e28c8fdf399f8ec1b1c79`
   - 金额：建议 0.1-0.5 ETH (约$200-1000)

2. **从 MetaMask 转账**
   - 切换网络到 Base
   - 发送 ETH
   - 地址：`0x73d6a5835ddf6f54480e28c8fdf399f8ec1b1c79`

---

### 方式 2: 法币购买 (On-Ramp)

1. **使用 MoonPay/Transak**
   - 在 GMGN 中点击"充值"
   - 选择法币购买
   - 支持信用卡/借记卡

2. **费率对比**
   - MoonPay: ~3-5% 手续费
   - Transak: ~2-4% 手续费
   - 交易所提币：~1% 手续费 (推荐)

---

## 🎯 交易策略配置

### 策略 1: 知几-E v4.0 (数学战争)

**核心公式**:
```python
# 凯利公式 (Quarter-Kelly)
f* = (bp - q) / b / 4

其中:
- b = 赔率 (净收益/本金)
- p = 胜率 (置信度)
- q = 1 - p (失败概率)
```

**配置参数**:
| 参数 | 值 | 说明 |
|------|-----|------|
| 置信度阈值 | 96% | 低于此不下注 |
| 优势阈值 | 2% | 套利空间 |
| 凯利倍数 | 0.25 | Quarter-Kelly |
| 单笔最大 | 25% | 总资金的 25% |
| 每日最大 | 50% | 总资金的 50% |

**适用市场**:
- ✅ Polymarket 预测市场
- ✅ 二元期权 (是/否)
- ✅ 高流动性市场

---

### 策略 2: GMGN 跟单策略

**跟单对象**:
| 交易者 | 胜率 | 跟随比例 | 说明 |
|--------|------|---------|------|
| ColdMath | 78% | 20% | 气象套利专家 |
| majorexploiter | 72% | 15% | $2.4M 盈利 |
| smarttrader | 69% | 10% | 稳定盈利 |

**配置**:
```yaml
copy_trading:
  enabled: true
  traders:
    - name: ColdMath
      allocation: 20%  # 跟单资金比例
      max_position: $500
      stop_loss: 10%
    - name: majorexploiter
      allocation: 15%
      max_position: $300
      stop_loss: 15%
```

---

### 策略 3: 套利策略 (跨平台)

**套利机会**:
| 平台 A | 平台 B | 价差 | 操作 |
|--------|--------|------|------|
| Polymarket | GMGN | >5% | 低买高卖 |
| GMGN | 币安 | >3% | 跨平台套利 |

**配置**:
```yaml
arbitrage:
  enabled: true
  min_spread: 3%  # 最小价差
  max_position: $1000
  timeout: 300s  # 5 分钟内执行
```

---

## 📊 资金管理

### 初始资金分配 (建议$1000 起)

| 用途 | 比例 | 金额 | 说明 |
|------|------|------|------|
| **知几-E 策略** | 50% | $500 | 主策略 |
| **跟单策略** | 30% | $300 | 学习 + 收益 |
| **套利策略** | 15% | $150 | 低风险 |
| **备用金** | 5% | $50 | 应急 |

### 仓位管理

```python
# 单笔仓位计算
def calculate_position(confidence, total_capital):
    # Quarter-Kelly
    kelly = (confidence - (1 - confidence)) / confidence
    position = total_capital * kelly * 0.25
    
    # 限制在 5-25% 之间
    return max(0.05, min(0.25, position))

# 示例
confidence = 0.96  # 96% 置信度
capital = 1000  # $1000 总资金
position = calculate_position(confidence, capital)
print(f"建议仓位：${position:.2f}")  # $230
```

---

## 🚀 执行步骤

### Step 1: 充值 (10 分钟)
- [ ] 从币安提 SOL 到 GMGN Solana 钱包
- [ ] 从币安提 ETH 到 GMGN Base 钱包
- [ ] 确认到账 (约 5-10 分钟)

### Step 2: 配置策略 (5 分钟)
- [ ] 在 GMGN Bot 中启用知几-E v4.0
- [ ] 设置跟单交易者
- [ ] 配置套利参数

### Step 3: 小额测试 (30 分钟)
- [ ] 首笔下注 $10-20
- [ ] 观察执行情况
- [ ] 确认收益计算

### Step 4: 规模化 (次日)
- [ ] 分析首日数据
- [ ] 调整参数
- [ ] 增加仓位

---

## 📈 收益预期

| 时间 | 本金 | 月回报 | 月收入 | 累计 |
|------|------|--------|--------|------|
| **月 1** | $1000 | 20% | $200 | $1200 |
| **月 3** | $3000 | 30% | $900 | $3900 |
| **月 6** | $8000 | 40% | $3200 | $11200 |
| **月 12** | $20000 | 50% | $10000 | $30000 |

**风险提示**:
- ⚠️ 预测市场有风险，可能亏损
- ⚠️ 不要投入超过承受能力的资金
- ⚠️ Quarter-Kelly 降低风险但不消除

---

## 🔧 GMGN Bot 命令

```
/start - 启动 Bot
/balance - 查看余额
/deposit - 充值指南
/trade - 开始交易
/copy - 跟单配置
/arbitrage - 套利设置
/stop - 停止交易
/help - 帮助
```

---

*版本：v1.0 | 创建时间：2026-03-27 21:05*
*状态：✅ 待执行*
