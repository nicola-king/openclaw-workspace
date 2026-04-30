# Polymarket 模拟盘配置

> 创建时间：2026-04-04 13:32 | 用途：知几-E v3.0 策略模拟测试

---

## 🎯 模拟盘目标

**阶段：** 模拟盘测试 (2 周)  
**策略：** 知几-E v3.0 (气象套利)  
**初始资金：** 虚拟 $10,000 USDC  
**目标：** 验证策略逻辑 + 监控风控触发

---

## 🔑 API 配置

### 方式 1：使用现有 API Key (推荐)

从 `MEMORY.md` 获取：
- **API Key:** `019d2561-d2df-785c-b619-852216ccc00d`
- **钱包地址:** `0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5`

### 方式 2：创建新 API Key

1. 访问：https://polymarket.com/profile/api
2. 点击 "Create API Key"
3. 保存 API Key (仅显示一次)
4. 更新 `.env.polymarket-paper`

---

## 📁 配置文件

### .env.polymarket-paper

```bash
# 模拟盘环境配置
POLYMARKET_MODE=paper

# API 配置
POLYMARKET_API_KEY=019d2561-d2df-785c-b619-852216ccc00d
POLYMARKET_WALLET=0x6e0c80c90ea6c15917308F820Eac91Ce2724B5b5

# 模拟资金
PAPER_INITIAL_BALANCE=10000

# 策略配置 (v3.0 最佳参数)
STRATEGY_VERSION=v3.0
CONFIDENCE_THRESHOLD=0.60
KELLY_DIVISOR=3
MAX_POSITION_PCT=0.15

# 风控配置
DAILY_STOP_LOSS=0.10
CONSECUTIVE_LOSS_LIMIT=3
LOSS_REDUCTION_FACTOR=0.5

# 流动性分层
LOW_LIQUIDITY_THRESHOLD=2000
HIGH_LIQUIDITY_THRESHOLD=10000

# API 端点
POLYMARKET_BASE_URL=https://gamma-api.polymarket.com
POLYMARKET_CLOB_URL=https://clob.polymarket.com
POLYMARKET_RELAYER_URL=https://relayer-v2.polymarket.com

# 日志
LOG_LEVEL=INFO
LOG_FILE=/home/nicola/.openclaw/workspace/logs/paper-trading.log
```

---

## 🚀 启动流程

### 1. 环境准备

```bash
# 复制配置文件
cd /home/nicola/.openclaw/workspace/skills/zhiji
cp .env.polymarket.template .env.polymarket-paper

# 编辑配置 (填入 API Key)
nano .env.polymarket-paper

# 安装依赖
pip3 install requests python-dotenv numpy
```

### 2. 启动模拟盘

```bash
# 方式 1: 手动运行
cd /home/nicola/.openclaw/workspace
python3 scripts/zhiji-e-paper-trading.py

# 方式 2: Cron 自动运行 (每小时检查)
# 已配置：0 * * * * /home/nicola/.openclaw/workspace/scripts/zhiji-e-paper-trading.py
```

### 3. 监控面板

```bash
# 查看实时状态
tail -f /home/nicola/.openclaw/workspace/logs/paper-trading.log

# 查看交易记录
cat /home/nicola/.openclaw/workspace/logs/paper-trades.jsonl

# 查看日报
cat /home/nicola/.openclaw/workspace/reports/paper-trading-daily.md
```

---

## 📊 监控指标

### 每日检查清单

- [ ] 账户余额变化
- [ ] 当日交易数
- [ ] 当日盈亏
- [ ] 风控触发次数
- [ ] 策略信号质量

### 周度检查清单

- [ ] 周收益率
- [ ] 胜率
- [ ] 夏普比率
- [ ] 最大回撤
- [ ] 与回测对比差异

---

## 🎯 验收标准

### 进入实盘条件

| 指标 | 要求 | 当前 |
|------|------|------|
| 模拟盘周期 | ≥2 周 | 0 天 |
| 夏普比率 | >1.0 | - |
| 最大回撤 | <30% | - |
| 胜率 | >50% | - |
| 风控触发 | 正常 | - |

### 停止模拟盘条件

- [ ] 连续 3 天亏损
- [ ] 回撤超过 30%
- [ ] 发现策略逻辑 bug
- [ ] 实盘环境准备好

---

## 📁 文件结构

```
/home/nicola/.openclaw/workspace/
├── skills/zhiji/
│   ├── .env.polymarket-paper      # 模拟盘配置
│   ├── polymarket_client.py       # API 客户端
│   └── paper_trading_monitor.py   # 监控脚本
├── scripts/
│   ├── zhiji-e-paper-trading.py   # 模拟盘主程序 🆕
│   └── zhiji-e-backtest-v3.py     # 回测引擎
├── logs/
│   ├── paper-trading.log          # 运行日志
│   └── paper-trades.jsonl         # 交易记录
└── reports/
    ├── paper-trading-daily.md     # 日报
    └── paper-trading-weekly.md    # 周报
```

---

## 🛡️ 风控规则

### 每日止损
- **阈值：** 单日亏损 ≥10%
- **动作：** 停止当日所有交易
- **恢复：** 次日自动重置

### 连败保护
- **阈值：** 连续亏损 ≥3 笔
- **动作：** 仓位减半
- **恢复：** 获胜后恢复正常

### 流动性过滤
- **阈值：** 流动性 <$2,000
- **动作：** 跳过该市场
- **原因：** 避免滑点

---

## 📝 日志格式

### 交易记录 (JSONL)

```json
{"timestamp":"2026-04-04T13:32:00","market":"TEMP-NYC-APR4","side":"YES","price":0.60,"size":150,"confidence":0.65,"ev":0.08,"result":"PENDING"}
```

### 运行日志

```
[2026-04-04 13:32:00] [INFO] 知几-E 模拟盘启动
[2026-04-04 13:32:01] [INFO] 加载策略 v3.0
[2026-04-04 13:32:02] [INFO] 扫描气象市场...
[2026-04-04 13:32:03] [INFO] 发现 3 个高置信度机会
[2026-04-04 13:32:04] [INFO] 执行下注：TEMP-NYC-APR4 YES @0.60 $150
```

---

## 🔗 相关文档

- 回测报告：`reports/backtest-report-v3.md`
- 策略对比：`reports/strategy-comparison-v2-vs-v3.md`
- 任务完成：`reports/task-125-p3-optimization-complete.md`

---

*配置：太一 AGI | 知几-E 模拟盘 v3.0*
