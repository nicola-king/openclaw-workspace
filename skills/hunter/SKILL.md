# Hunter (猎手) - 情报狙击手 Skill

> 版本：v1.0 | 创建：2026-03-27 | 状态：✅ 激活

---

## 🎯 职责定位

**Hunter (猎手)** = 情报狙击手

- **主责**: 聪明钱监控 + 高置信度信号发现 + 实时推送
- **数据源**: 天机系统 (罔两维护)
- **输出**: Telegram 实时信号推送 (付费用户)
- **协作**: 知几 (交易执行)、罔两 (数据分析)、太一 (统筹)

---

## 📋 核心功能

### 1. 聪明钱钱包监控

**监控列表**:
- ColdMath (胜率 78%)
- majorexploiter ($2.4M 盈利)
- 50+ 聪明钱钱包

**监控内容**:
- 大额交易 (> $10,000)
- 建仓方向 (BUY/SELL)
- 入场价格
- 持仓变化

---

### 2. 信号生成引擎

**过滤规则**:
```python
if 置信度 >= 96% and 优势 >= 2%:
    推送信号
else:
    丢弃/继续观察
```

**置信度计算**:
- 历史胜率权重 (40%)
- 交易金额权重 (30%)
- 市场趋势权重 (20%)
- 时间窗口权重 (10%)

**仓位建议**:
- Quarter-Kelly (默认)
- Half-Kelly (高置信度>98%)
- Full-Kelly (极高置信度>99%)

---

### 3. Telegram 推送模块

**推送格式**:
```
🚨 HUNTER ALERT - 高置信度信号

📊 市场：{market_name}
📈 方向：{direction}
💰 聪明钱：{whale_name}
🎯 置信度：{confidence}%
💵 当前价格：${price}
📉 套利空间：{edge}%

💼 建议仓位：{kelly_suggestion}
⏰ 推送时间：{timestamp}
🔔 延迟：实时 (0s)

━━━━━━━━━━━━━━━━━━━━━

【Hunter Pro - $99/月】
✅ 实时推送 (vs 免费 15 分钟延迟)
✅ 高置信度过滤 (>96%)
✅ 聪明钱深度分析
✅ 仓位建议 (Kelly Criterion)

升级：https://chuanxi.gumroad.com/l/hunter-pro
```

**推送渠道**:
- Telegram 私聊 (付费用户)
- Telegram 群组 (VIP 群)

---

### 4. 天机系统接入

**数据接口**:
```python
from skills.wangliang.tianji import TianjiSystem

tianji = TianjiSystem()
whale_trades = tianji.get_recent_trades(limit=100)
```

**数据更新频率**:
- 实时推送 (WebSocket)
- 轮询备份 (30 秒/次)

---

## 🚀 启动命令

```bash
# 启动 Hunter Bot
cd ~/.openclaw/workspace/skills/hunter
python hunter_bot.py &

# 查看状态
ps aux | grep hunter
```

---

## 📊 与 PolyAlert 对比

| 功能 | PolyAlert (免费) | Hunter (付费) |
|------|-----------------|--------------|
| 推送渠道 | Telegram 频道 | Telegram 私聊 |
| 延迟 | 15 分钟 | 实时 (0 延迟) |
| 信号质量 | 基础信号 | 高置信度 (>96%) |
| 价格 | $0 | $99/月 |
| 目标 | 引流 | 变现 |

---

## 🔧 配置项

```yaml
hunter:
  bot_token: "8675078646:AAGKNVt3hXE1MMUr6HXCOl4XcwzwV0CmVyY"
  confidence_threshold: 96  # 置信度阈值
  edge_threshold: 2  # 优势阈值 (%)
  kelly_strategy: "quarter"  # quarter/half/full
  push_delay: 0  # 推送延迟 (秒)
  whale_list:
    - "ColdMath"
    - "majorexploiter"
    # ... 50+ wallets
```

---

## 📝 运行日志

**日志位置**: `~/.openclaw/workspace/logs/hunter.log`

**日志格式**:
```
[2026-03-27 19:54:00] INFO: Hunter Bot started
[2026-03-27 19:55:12] SIGNAL: BTC $100K - Confidence 97%
[2026-03-27 19:55:13] PUSHED: Signal sent to 15 premium users
```

---

## 🎯 KPI 指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 信号准确率 | >96% | 待测试 |
| 推送延迟 | <5 秒 | 待测试 |
| 付费用户 | 50+ | 0 |
| 月收入 | $5,000 | $0 |

---

*版本：v1.0 | 创建时间：2026-03-27 19:54*
*状态：✅ 激活待运行*
