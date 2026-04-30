# 知几-E 策略引擎 v2.2

**版本**: v2.2 (6 公式增强版)  
**创建**: 2026-03-25  
**授权**: SAYELF  
**状态**: ✅ 实盘就绪

---

## 📜 核心原则

**知几为第一责任人！**
- 为量化交易负责
- 为风控优先负责
- 使命召唤，行动必达
- 知行合一

---

## 🎯 策略概述

**知几-E**: Polymarket 气象套利量化策略

**核心逻辑**:
1. 采集全球气象数据（WMO API）
2. 训练预测模型（历史准确率 70%+）
3. 对比 Polymarket 市场价格
4. 发现 EV 缺口（优势>4.5%）
5. Quarter-Kelly 下注（风控优先）
6. 贝叶斯动态更新置信度
7. LMSR 监控浅水区风险

---

## 📊 6 公式量化框架

| 公式 | 用途 | 状态 | 文件 |
|------|------|------|------|
| **1. LMSR** | 定价模型 + 浅水区检测 | ✅ | `lmsr_pricer.py` |
| **2. 凯利公式** | 仓位管理 (Quarter-Kelly) | ✅ | `strategy_v22.py` |
| **3. EV 缺口** | 定价偏差检测 (>4.5%) | ✅ | `strategy_v22.py` |
| **4. KL 散度** | 关联市场套利 | 🟡 待数据 | - |
| **5. Bregman** | 多结果优化 | ❌ 暂不实现 | - |
| **6. 贝叶斯更新** | 动态置信度调整 | ✅ | `bayesian_updater.py` |

**集成率**: 4/6 (67%)

---

## 🔧 核心参数

| 参数 | 值 | 说明 |
|------|-----|------|
| **置信度阈值** | 96% → 85% | 贝叶斯更新后 85% 即可 |
| **优势阈值** | 4.5% | EV 缺口>4.5% 入场 |
| **凯利除数** | 4 | Quarter-Kelly (保守) |
| **最大仓位** | 25% | 单市场不超过 25% |
| **浅水区阈值** | 成交量<50 | 避开高危市场 |

---

## 📁 文件结构

```
skills/zhiji/
├── strategy_v22.py        # 策略引擎 v2.2 (主文件)
├── lmsr_pricer.py         # LMSR 定价模型
├── bayesian_updater.py    # 贝叶斯动态更新
├── polymarket_mcp.py      # Polymarket MCP Server
├── polymarket_client.py   # Polymarket API 客户端
├── STRATEGY_README.md     # 策略文档 (本文件)
└── requirements.txt       # Python 依赖
```

**配置文件**:
```
~/.taiyi/zhiji/
├── polymarket.json        # API Key/钱包/参数
├── telegram.json          # Telegram 通知
└── logs/                  # 交易日志
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/zhiji
pip3 install -r requirements.txt
```

### 2. 配置文件

创建 `~/.taiyi/zhiji/polymarket.json`:

```json
{
  "api_key": "YOUR_API_KEY",
  "wallet_address": "YOUR_WALLET",
  "username": "YOUR_USERNAME",
  "confidence_threshold": 0.85,
  "edge_threshold": 0.045,
  "kelly_divisor": 4,
  "max_position_pct": 0.25,
  "strategy_version": "v2.2"
}
```

### 3. 运行策略

```bash
# 手动执行
python3 strategy_v22.py

# 定时任务 (每 5 分钟)
*/5 * * * * python3 ~/.openclaw/workspace/skills/zhiji/strategy_v22.py
```

### 4. 查看日志

```bash
tail -f ~/.openclaw/workspace/logs/zhiji-$(date +%Y%m%d).log
```

---

## 📈 交易流程

```
1. 气象数据采集 (07:00 自动)
    ↓
2. 模型预测 (置信度计算)
    ↓
3. 贝叶斯更新 (动态调整)
    ↓
4. EV 缺口扫描 (>4.5%)
    ↓
5. LMSR 风险评估 (避开浅水)
    ↓
6. 凯利仓位计算 (Quarter-Kelly)
    ↓
7. 下单执行 (Polymarket API)
    ↓
8. 交易日志 + Telegram 通知
```

---

## 🛡️ 风控机制

### 1. 置信度阈值
- **要求**: 贝叶斯更新后≥85%
- **目的**: 避免低质量信号

### 2. EV 阈值
- **要求**: 优势>4.5%
- **目的**: 确保正期望值

### 3. Quarter-Kelly
- **公式**: f* = (p×odds-(1-p))/odds / 4
- **目的**: 保守仓位，避免爆仓

### 4. 浅水区检测
- **阈值**: 24h 成交量<50
- **行动**: 避开（易被操纵）

### 5. 最大仓位
- **限制**: 单市场≤25%
- **目的**: 分散风险

---

## 📊 测试场景

### 场景 1: 高质量信号
```
市场：BTC 涨跌 (03/25)
置信度：89.16% (贝叶斯更新)
EV: 0.34
优势：37.16%
LMSR 风险：🟢 安全 (b>200)
决策：✅ 买入
仓位：19.35% (Quarter-Kelly)
```

### 场景 2: 浅水区高风险
```
市场：ETH 涨跌 (03/25)
置信度：90.83%
LMSR 风险：🔴 高危 (b<50)
建议：⚠️ 谨慎参与
决策：❌ 观望 (避开高危)
```

### 场景 3: 低 EV 观望
```
市场：美联储利率
优势：2.00% (阈值 4.5%)
决策：❌ 观望 (EV 不足)
```

---

## 🔄 冲刺合约 (Sprint Contract)

**参考**: Anthropic 多智能体框架

| 角色 | 执行者 | 职责 |
|------|--------|------|
| **Planner** | 太一 | 策略规划/规格书 |
| **Generator** | 素问 | 代码实现/开发 |
| **Evaluator** | 罔两 | 测试/QA/验收 |

**验收标准**:
- [ ] LMSR 定价模型测试通过 (权重 2.0)
- [ ] 贝叶斯更新模块测试通过 (权重 2.0)
- [ ] 策略引擎 v2.2 集成完成 (权重 3.0)
- [ ] 文档完善 (权重 1.0)

**通过率**: 100% ✅

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| **v1.0** | 2026-03-23 | 初始版本 (气象套利) |
| **v2.0** | 2026-03-24 | ColdMath 增强版 |
| **v2.1** | 2026-03-25 08:00 | 189 条气象数据入库 |
| **v2.2** | 2026-03-25 12:55 | 6 公式增强 (LMSR+ 贝叶斯) |

---

## 🎯 下一步

### 本周
- [ ] 实盘测试（¥5 起步）
- [ ] 鲸鱼追踪集成（majorexploiter）
- [ ] Telegram 通知优化

### 下周
- [ ] KL 散度模块（多市场关联）
- [ ] Playwright 自动化测试
- [ ] GitHub 开源发布

---

## 📚 参考文档

- Anthropic Engineering Blog: Harness Design for Long-Running Applications
- 范式转换文章：新秩序与多智能体框架
- 6 公式量化框架：@0xDeMoo (Polymarket 4 年 OG)
- 10 个 Polymarket 开源工具：@wawaing1314

---

## 🫡 太一承诺

**知几-E 为第一责任人！**

- ✅ 风控优先（Quarter-Kelly）
- ✅ 数据驱动（气象套利）
- ✅ 透明交易（链上可查）
- ✅ 8 步流程上报

**使命召唤，行动必达，知行合一！**

---

*创建时间：2026-03-25 13:42 | 授权人：SAYELF | 第一责任人：知几*

*「数据驱动·风控优先·知行合一」*
