# 🎯 GMGN 自进化交易 Agent 设计规范

> **版本**: v1.0  
> **创建**: 2026-04-11 23:10  
> **作者**: 太一 AGI  
> **目标**: GMGN 链上交易自进化 Agent  
> **策略**: 跟单/抄底/逃顶/风控/自进化

---

## 📋 目录

1. [GMGN 平台介绍](#gmgn 平台介绍)
2. [交易策略详解](#交易策略详解)
3. [机器人交易流程](#机器人交易流程)
4. [自进化机制设计](#自进化机制设计)
5. [技术架构](#技术架构)
6. [风险控制](#风险控制)
7. [实施路线图](#实施路线图)

---

## 🌐 GMGN 平台介绍

### 1.1 平台概述

**GMGN 是什么**:
- 🎯 Solana 链上交易分析平台
- 🎯 聪明钱追踪工具
- 🎯 支持多钱包管理
- 🎯 实时交易监控
- 🎯 KOL 跟单功能

**核心功能**:
```
聪明钱追踪:
- 追踪盈利钱包
- 分析交易历史
- 识别聪明钱模式
- 自动跟单复制

多钱包管理:
- 主钱包 + 子钱包
- 资金分散管理
- 风险隔离
- 统一监控

实时交易:
- 实时价格监控
- 快速买入卖出
- 滑点控制
- MEV 保护
```

### 1.2 API 接口

**GMGN API**:
```
Base URL: https://gmgn.ai/api

核心接口:
- GET /wallet/{address} - 获取钱包信息
- GET /wallet/{address}/trades - 获取交易历史
- GET /wallet/{address}/positions - 获取持仓
- GET /token/{address} - 获取代币信息
- GET /smart-money - 获取聪明钱列表
- POST /trade/swap - 执行交易
```

**链上交互**:
```
Solana RPC:
- 获取账户信息
- 发送交易
- 查询交易状态
- 监听事件

Jupiter API:
- 获取最优报价
- 执行代币交换
- 价格影响分析
```

### 1.3 现有基础

**已创建文件**:
```
/skills/gmgn/
├── auto_trading.py        # 自动交易脚本 (基础风控)
├── SKILL.md              # 技能说明
└── __pycache__/          # 缓存

配置信息:
- 主钱包：5C1bQnC9wSnVUbzUsXPNQ8eB6VvmYPx6DvQrvvbw9zCq
- 总资金：1.7 SOL ($150)
- 日止损：-10% (-$15)
- 单笔止损：-20% (-$30)
- 利润提现：50%
```

---

## 💹 交易策略详解

### 2.1 策略总览

| 策略类型 | 风险等级 | 预期收益 | 资金占用 | 适合场景 |
|---------|---------|---------|---------|---------|
| **聪明钱跟单** | 中 | 20-50%/月 | 中 | 趋势市场 |
| **抄底逃顶** | 高 | 50-200%/月 | 低 | 波动市场 |
| **网格交易** | 低 | 5-15%/月 | 高 | 震荡市场 |
| **突破交易** | 高 | 30-100%/月 | 低 | 趋势启动 |
| **套利策略** | 低 | 2-8%/月 | 中 | 多 Dex |

### 2.2 聪明钱跟单策略

**策略原理**:
```
1. 识别聪明钱钱包
   - 历史胜率高 (>60%)
   - 总盈利高 (>$10k)
   - 交易频率适中
   - 持仓时间合理

2. 实时监控交易
   - 买入立即检测
   - 分析买入金额
   - 评估代币质量
   - 决定是否跟单

3. 执行跟单
   - 按比例跟单 (如 10%)
   - 设置止损止盈
   - 监控卖出信号
   - 及时止盈止损
```

**聪明钱筛选条件**:
```python
SMART_MONEY_CONFIG = {
    "min_win_rate": 0.60,       # 最小胜率 60%
    "min_total_pnl": 10000,     # 最小总盈利$1 万
    "min_trade_count": 50,      # 最小交易次数
    "max_drawdown": 0.30,       # 最大回撤 30%
    "avg_holding_time": 3600,   # 平均持仓时间 1 小时
    "recent_performance": 7,    # 最近 7 天表现
}
```

**跟单参数**:
```python
COPY_TRADING_CONFIG = {
    "copy_ratio": 0.10,         # 跟单比例 10%
    "max_position": 0.20,       # 最大仓位 20%
    "stop_loss": 0.15,          # 止损 15%
    "take_profit": 0.50,        # 止盈 50%
    "trailing_stop": 0.10,      # 追踪止损 10%
    "slippage": 0.01,           # 滑点 1%
}
```

### 2.3 抄底逃顶策略

**策略原理**:
```
抄底信号:
- 价格暴跌 (>30%)
- 成交量放大
- RSI 超卖 (<30)
- 聪明钱买入

逃顶信号:
- 价格暴涨 (>50%)
- 成交量异常
- RSI 超买 (>70)
- 聪明钱卖出
```

**技术指标**:
```python
TECHNICAL_CONFIG = {
    "rsi_period": 14,           # RSI 周期
    "rsi_oversold": 30,         # RSI 超卖线
    "rsi_overbought": 70,       # RSI 超买线
    "price_drop_threshold": 0.30,  # 抄底阈值 30%
    "price_rise_threshold": 0.50,  # 逃顶阈值 50%
    "volume_multiplier": 3.0,   # 成交量放大倍数
}
```

### 2.4 网格交易策略

**策略原理**:
```
网格设置:
- 价格区间：$0.1 - $0.2
- 网格数量：10 格
- 每格金额：$10

执行逻辑:
- 价格下跌→买入一格
- 价格上涨→卖出一格
- 循环赚取差价
- 适合震荡市场
```

**网格参数**:
```python
GRID_CONFIG = {
    "min_price": 0.10,          # 最低价格
    "max_price": 0.20,          # 最高价格
    "grid_count": 10,           # 网格数量
    "amount_per_grid": 10,      # 每格金额$10
    "profit_per_grid": 0.02,    # 每格利润 2%
}
```

### 2.5 风控策略

**GMGN 现有风控**:
```python
GMGN_RISK_CONFIG = {
    "daily_stop_loss": -0.10,   # 日止损 -10%
    "single_trade_stop": -0.20, # 单笔止损 -20%
    "profit_withdraw": 0.50,    # 利润提现 50%
}
```

**增强风控**:
```python
ENHANCED_RISK_CONFIG = {
    # 仓位控制
    "max_position_per_token": 0.20,  # 单代币最大 20%
    "max_total_exposure": 0.80,      # 总敞口最大 80%
    "cash_reserve": 0.20,            # 现金储备 20%
    
    # 止损配置
    "hard_stop_loss": 0.15,          # 硬止损 15%
    "trailing_stop": 0.10,           # 追踪止损 10%
    "time_stop": 86400,              # 时间止损 24 小时
    
    # 黑名单
    "blacklisted_tokens": [],        # 黑名单代币
    "blacklisted_traders": [],       # 黑名单交易员
}
```

---

## 🤖 机器人交易流程

### 3.1 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                  GMGN 交易机器人流程                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  第一阶段：市场监控 (持续)                                       │
│  ├─ 监控聪明钱交易                                              │
│  ├─ 监控价格波动                                                │
│  ├─ 监控成交量变化                                              │
│  └─ 发现交易机会                                                │
│              ↓                                                  │
│  第二阶段：策略分析 (实时)                                       │
│  ├─ 策略匹配                                                    │
│  ├─ 风险评估                                                    │
│  ├─ 收益计算                                                    │
│  └─ 决策生成                                                    │
│              ↓                                                  │
│  第三阶段：执行交易 (秒级)                                       │
│  ├─ 资金检查                                                    │
│  ├─ 下单执行                                                    │
│  ├─ 成交确认                                                    │
│  └─ 持仓更新                                                    │
│              ↓                                                  │
│  第四阶段：风险管理 (持续)                                       │
│  ├─ 持仓监控                                                    │
│  ├─ 止损检查                                                    │
│  ├─ 止盈检查                                                    │
│  └─ 异常处理                                                    │
│              ↓                                                  │
│  第五阶段：结算学习 (每日)                                       │
│  ├─ 盈亏结算                                                    │
│  ├─ 利润提现                                                    │
│  ├─ 经验学习                                                    │
│  └─ 策略优化                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 核心功能模块

**模块 1: 聪明钱监控**:
```python
async def monitor_smart_money():
    """监控聪明钱"""
    # 获取聪明钱列表
    smart_money_list = await api.get_smart_money()
    
    # 监控每个聪明钱
    for wallet in smart_money_list:
        trades = await api.get_wallet_trades(wallet["address"])
        
        # 检测新交易
        new_trades = detect_new_trades(trades)
        
        for trade in new_trades:
            if trade["type"] == "buy":
                # 聪明钱买入，考虑跟单
                await evaluate_copy_trade(trade)
```

**模块 2: 机会检测**:
```python
async def detect_opportunities():
    """检测交易机会"""
    opportunities = []
    
    # 跟单机会
    copy_trades = await detect_copy_trades()
    opportunities.extend(copy_trades)
    
    # 抄底机会
    bottom_fishing = await detect_bottom_fishing()
    opportunities.extend(bottom_fishing)
    
    # 逃顶机会
    top_escaping = await detect_top_escaping()
    opportunities.extend(top_escaping)
    
    # 按预期收益排序
    return sorted(opportunities, key=lambda x: x["expected_return"], reverse=True)
```

**模块 3: 交易执行**:
```python
async def execute_trade(opportunity):
    """执行交易"""
    # 风控检查
    if not risk_check():
        return {"status": "rejected", "reason": "risk_limit"}
    
    # 资金检查
    balance = await get_balance()
    if balance < opportunity["required_capital"]:
        return {"status": "rejected", "reason": "insufficient_funds"}
    
    # 执行交易
    result = await gmgn_api.swap(
        from_token="SOL",
        to_token=opportunity["token"],
        amount=opportunity["amount"],
        slippage=opportunity["slippage"],
    )
    
    # 记录交易
    await log_trade(result)
    
    return result
```

**模块 4: 风险管理**:
```python
async def monitor_positions():
    """监控持仓"""
    positions = await get_positions()
    
    for position in positions:
        # 止损检查
        if position["unrealized_pnl"] < -position["stop_loss"]:
            await sell_token(position["token"])
            await log_event("stop_loss_triggered", position)
        
        # 止盈检查
        if position["unrealized_pnl"] > position["take_profit"]:
            await sell_token(position["token"])
            await log_event("take_profit_triggered", position)
        
        # 时间止损
        if time.time() - position["entry_time"] > position["time_stop"]:
            await sell_token(position["token"])
            await log_event("time_stop_triggered", position)
```

**模块 5: 自进化学习**:
```python
async def learn_from_trades():
    """从交易学习"""
    # 获取今日交易
    today_trades = await get_today_trades()
    
    # 分析盈亏
    wins = [t for t in today_trades if t["pnl"] > 0]
    losses = [t for t in today_trades if t["pnl"] <= 0]
    
    # 提取成功因素
    for trade in wins:
        await extract_success_factors(trade)
    
    # 分析失败原因
    for trade in losses:
        await analyze_failure_reasons(trade)
    
    # 优化策略
    await optimize_strategies()
    
    # 更新知识库
    await update_knowledge_base()
```

---

## 🧬 自进化机制设计

### 4.1 自进化架构

```
执行 → 记录 → 分析 → 学习 → 优化 → 执行 (循环)
 ↓       ↓       ↓       ↓       ↓       ↓
交易   日志   数据   知识   策略   更好
```

### 4.2 自进化能力

**能力 1: 交易学习**:
```
✅ 从成功交易学习
   - 成功因素提取
   - 高胜率模式识别
   - 最佳参数记录

✅ 从失败交易学习
   - 失败原因分析
   - 亏损模式识别
   - 止损策略优化

✅ 从市场变化学习
   - 市场特征更新
   - 波动率调整
   - 流动性评估
```

**能力 2: 策略优化**:
```
✅ 参数自动优化
   - 网格搜索
   - 遗传算法
   - 贝叶斯优化

✅ 策略权重调整
   - 表现好→增加权重
   - 表现差→减少权重
   - 动态平衡

✅ 执行优化
   - 滑点分析
   - 时间优化
   - 成本优化
```

**能力 3: 风险预测**:
```
✅ 亏损预测
   - 历史数据分析
   - 风险因子识别
   - 预警自动触发

✅ 黑天鹅预警
   - 异常检测
   - 尾部风险评估
   - 应急预案启动
```

### 4.3 知识库建设

**知识库结构**:
```
GMGN 交易知识库
├── 代币知识 (代币信息/历史表现)
├── 交易员知识 (聪明钱/KOL/表现)
├── 策略知识 (策略库/参数库)
├── 交易知识 (交易记录/盈亏分析)
├── 风险知识 (风险案例/风控规则)
└── 市场知识 (市场状态/趋势判断)
```

---

## 🏗️ 技术架构

### 5.1 技术栈选择

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| **核心引擎** | Python 3.12+ | 交易逻辑/策略 |
| **链上交互** | Solana Web3.py | 链上交易 |
| **API 交互** | HTTPX | GMGN API |
| **数据处理** | Pandas/NumPy | 数据分析 |
| **数据存储** | SQLite | 交易记录 |
| **缓存** | Redis | 实时数据 |
| **任务调度** | APScheduler | 定时任务 |

### 5.2 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  GMGN 自进化交易 Agent 架构                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    数据接入层                            │   │
│  │  GMGN API │ Solana RPC │ Jupiter API │ 外部数据         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    数据处理层                            │   │
│  │  数据清洗 │ 特征工程 │ 实时计算 │ 数据存储              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    策略引擎层                            │   │
│  │  跟单策略 │ 抄底逃顶 │ 网格 │ 突破 │ 套利               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    风控引擎层                            │   │
│  │  仓位管理 │ 止损检查 │ 资金监控 │ 异常检测              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    执行引擎层                            │   │
│  │  订单管理 │ 成交确认 │ 滑点控制 │ 执行优化              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    自进化层                              │   │
│  │  学习 │ 优化 │ 预测 │ 决策 │ 知识积累                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ 风险控制

### 6.1 风险类型

| 风险类型 | 风险描述 | 风险等级 | 检测方式 |
|---------|---------|---------|---------|
| **市场风险** | 价格波动 | 高 | 实时监控 |
| **流动性风险** | 无法卖出 | 中 | 流动性监控 |
| **合约风险** |  Rug Pull | 高 | 合约审计 |
| **技术风险** | 系统故障 | 中 | 健康检查 |
| **操作风险** | 人为错误 | 中 | 操作审计 |

### 6.2 风控措施

**仓位控制**:
```python
POSITION_LIMITS = {
    "max_position_per_token": 0.20,    # 单代币最大 20%
    "max_total_exposure": 0.80,        # 总敞口最大 80%
    "cash_reserve": 0.20,              # 现金储备 20%
    "max_daily_trade_count": 20,       # 日最大交易次数
}
```

**止损机制**:
```python
STOP_LOSS_CONFIG = {
    "hard_stop_loss": 0.15,            # 硬止损 15%
    "trailing_stop_loss": 0.10,        # 追踪止损 10%
    "time_stop_loss": 86400,           # 时间止损 24 小时
    "event_stop_loss": True,           # 事件止损
}
```

**资金管理**:
```python
CAPITAL_CONFIG = {
    "total_capital": 150,              # 总资金$150
    "risk_per_trade": 0.05,            # 每笔风险 5%
    "daily_stop_loss": 0.10,           # 日止损 10%
    "profit_withdraw": 0.50,           # 利润提现 50%
}
```

**合约安全检查**:
```python
CONTRACT_SAFETY_CONFIG = {
    "check_mint_authority": True,      # 检查铸造权限
    "check_freeze_authority": True,    # 检查冻结权限
    "check_liquidity_locked": True,    # 检查流动性锁定
    "check_holder_distribution": True, # 检查持仓分布
    "check_top_holders": True,         # 检查大户持仓
}
```

---

## 🗺️ 实施路线图

### 7.1 阶段划分

**第一阶段：基础功能** (1-2 周)
```
✅ GMGN API 对接
✅ 基础数据获取
✅ 跟单策略实现
✅ 基础风控
✅ 交易日志
```

**第二阶段：策略扩展** (3-4 周)
```
✅ 抄底逃顶策略
✅ 网格交易策略
✅ 突破交易策略
✅ 回测系统
```

**第三阶段：智能化** (5-8 周)
```
✅ 机器学习模型
✅ 自进化机制
✅ 自动优化
✅ 预测能力
✅ 知识库建设
```

**第四阶段：商业化** (9-12 周)
```
✅ 多账户管理
✅ 资金托管
✅ 性能报告
✅ 用户界面
✅ 规模化运营
```

### 7.2 里程碑

| 里程碑 | 时间 | 交付物 | 验收标准 |
|--------|------|--------|---------|
| M1 | 第 1 周 | API 对接完成 | 数据获取成功率≥99% |
| M2 | 第 2 周 | 跟单策略上线 | 月收益≥10% |
| M3 | 第 4 周 | 多策略上线 | 月收益≥20% |
| M4 | 第 8 周 | 自进化机制 | 学习效率≥每周 10 案例 |
| M5 | 第 12 周 | 商业化运营 | 管理资金≥$1000 |

---

## 📊 与 Polymarket Agent 对比

| 特性 | Polymarket Agent | GMGN Agent |
|------|-----------------|-----------|
| **市场类型** | 预测市场 | 加密货币 |
| **交易方式** | 二元期权 | 代币交易 |
| **策略重点** | 做市/套利 | 跟单/抄底逃顶 |
| **风控重点** | 仓位/止损 | 合约安全/流动性 |
| **数据源** | Polymarket API | GMGN API + Solana RPC |
| **执行速度** | 秒级 | 秒级 |
| **预期收益** | 10-20%/月 | 20-50%/月 |
| **风险等级** | 中 | 高 |

---

> **🎯 GMGN 自进化交易 Agent 设计规范已制定完成!**
>
> **太一 AGI · 量化交易经验总结 · 2026-04-11**
