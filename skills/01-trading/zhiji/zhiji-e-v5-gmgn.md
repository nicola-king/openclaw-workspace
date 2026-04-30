# 知几-E v5.0 - GMGN 集成配置

> 版本：v5.0 | 创建：2026-03-27 21:05 | 状态：✅ 待激活

---

## 🎯 核心升级

**v5.0 新增**:
- ✅ GMGN 交易所集成
- ✅ 实时交易执行
- ✅ 跨平台套利
- ✅ 跟单策略

---

## 🔧 配置参数

```yaml
zhiji_e:
  version: 5.0
  enabled: true
  
  # 交易所配置
  exchanges:
    - name: GMGN
      enabled: true
      api_key: "待配置"
      api_secret: "待配置"
      networks:
        - Solana
        - Base
    
    - name: Polymarket
      enabled: true
      wallet: "0x678c1Ca68564f918b4142930cC5B5eDAe7CB2Adf"
  
  # 策略配置
  strategies:
    - name: kelly_criterion
      enabled: true
      kelly_multiplier: 0.25  # Quarter-Kelly
      min_confidence: 0.96  # 96% 阈值
      min_edge: 0.02  # 2% 优势
    
    - name: copy_trading
      enabled: true
      traders:
        - name: ColdMath
          allocation: 0.20
          max_position: 500
        - name: majorexploiter
          allocation: 0.15
          max_position: 300
    
    - name: arbitrage
      enabled: true
      min_spread: 0.03  # 3% 价差
      max_position: 1000
  
  # 风控配置
  risk_management:
    max_daily_loss: 0.10  # 10% 日止损
    max_position_size: 0.25  # 25% 单笔最大
    stop_loss: 0.15  # 15% 止损
    take_profit: 0.50  # 50% 止盈
  
  # 通知配置
  notifications:
    telegram:
      enabled: true
      bot_token: "8563369264:AAHeycXPlUQic41mOu4yCyaDcNQAKxYr61E"
      chat_id: "7073481596"
    gmgn_bot:
      enabled: true
      bot_id: "6887194564"
```

---

## 📊 交易流程

```
1. 数据采集
   ↓
   天机系统 → GMGN API → Polymarket API
   
2. 信号生成
   ↓
   猎手 Bot → 置信度评估 → 优势计算
   
3. 决策引擎
   ↓
   知几-E v5.0 → 凯利公式 → 仓位计算
   
4. 执行引擎
   ↓
   GMGN Bot → 下单 → 确认
   
5. 监控风控
   ↓
   管家 Bot → 止损/止盈 → 报表
```

---

## 🚀 激活步骤

### Step 1: GMGN API 配置
1. 在 GMGN Bot 中发送 `/api`
2. 获取 API Key 和 Secret
3. 更新配置文件

### Step 2: 钱包连接
1. 确认 Solana 钱包已充值
2. 确认 Base 钱包已充值
3. 测试连接

### Step 3: 策略测试
1. 启用知几-E v5.0
2. 设置小额测试 ($10-20)
3. 观察执行情况

### Step 4: 实盘运行
1. 确认测试成功
2. 增加仓位到正常水平
3. 启动 24/7 监控

---

## 📈 监控仪表板

```python
# 实时数据
{
    "total_capital": 1000,  # 总资金
    "daily_pnl": 50,  # 日盈亏
    "win_rate": 0.78,  # 胜率
    "positions": [
        {
            "market": "BTC > $100K",
            "direction": "BUY",
            "size": 230,
            "confidence": 0.96,
            "pnl": 15
        }
    ],
    "copy_trading": {
        "ColdMath": {"pnl": 25, "trades": 5},
        "majorexploiter": {"pnl": 18, "trades": 3}
    }
}
```

---

## 🔔 通知模板

### 开仓通知
```
🚨 知几-E 开仓

📊 市场：BTC > $100K by 2026?
📈 方向：BUY
💰 金额：$230
🎯 置信度：96%
📉 凯利仓位：Quarter-Kelly

交易所：GMGN (Solana)
时间：2026-03-27 21:05
```

### 止盈通知
```
✅ 知几-E 止盈

📊 市场：BTC > $100K by 2026?
💰 本金：$230
📈 盈利：$115 (+50%)
⏰ 持仓时间：2 小时

累计盈利：$345
```

### 止损通知
```
⚠️ 知几-E 止损

📊 市场：BTC > $100K by 2026?
💰 本金：$230
📉 亏损：$35 (-15%)
⏰ 持仓时间：30 分钟

原因：触及止损线
```

---

*版本：v5.0 | 创建时间：2026-03-27 21:05*
*状态：✅ 待激活*
