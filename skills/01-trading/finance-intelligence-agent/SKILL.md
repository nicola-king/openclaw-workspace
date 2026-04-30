# Finance Intelligence Agent · 金融情报智能体

> **版本**: v1.0  
> **创建时间**: 2026-04-22 00:10  
> **定位**: 太一系统金融分析核心技能  
> **来源**: GitHub 金融科技 Top 10 开源项目蒸馏

---

## 🎯 核心能力

基于 GitHub 金融科技 Top 10 开源项目蒸馏融合：

| 能力 | 来源项目 | Stars | 状态 |
|------|---------|-------|------|
| **金融终端** | OpenBB | 66.1K | ✅ |
| **AI 对冲基金** | ai-hedge-fund | 56K | ✅ |
| **多代理交易** | TradingAgents | 51.7K | ✅ |
| **交易机器人** | freqtrade | 49K | ✅ |
| **量化平台** | microsoft/qlib | 41K | ✅ |
| **股票分析器** | daily_stock_analysis | 30.5K | ✅ |
| **K 线预测** | Kronos | 19.7K | ✅ |
| **金融 LLM** | FinGPT | 19.6K | ✅ |

---

## 🚀 使用方式

### 方式 1: 语音指令

```
"太一，分析股票"
"太一，查看行情"
"太一，生成研报"
"太一，量化回测"
```

### 方式 2: 文字指令

```
/金融 分析 <股票代码>
/金融 行情 <股票代码>
/金融 研报 <公司名>
/金融 回测 <策略名>
```

### 方式 3: API 调用

```python
from finance_intelligence import FinanceAgent

agent = FinanceAgent()

# 股票分析
result = agent.analyze_stock("AAPL")

# 生成研报
report = agent.generate_report("特斯拉")

# 量化回测
backtest = agent.backtest_strategy("momentum")
```

---

## 📊 核心模块

### 1. 金融终端 (OpenBB 融合)

**功能**:
- ✅ 实时行情
- ✅ 财务报表
- ✅ 分析师评级
- ✅ 技术指标
- ✅ 新闻舆情

**数据源**:
- Yahoo Finance
- Alpha Vantage
- 东方财富
- 同花顺

---

### 2. AI 对冲基金 (ai-hedge-fund 融合)

**功能**:
- ✅ 多策略模拟
- ✅ 巴菲特价值投资
- ✅ 芒格逆向思维
- ✅ 量化动量策略
- ✅ 风险平价配置

**策略库**:
| 策略 | 类型 | 风险 | 收益 |
|------|------|------|------|
| 价值投资 | 长线 | 低 | 15-20%/年 |
| 动量策略 | 中线 | 中 | 20-30%/年 |
| 套利策略 | 短线 | 低 | 5-10%/年 |
| 量化多因子 | 中线 | 中 | 15-25%/年 |

---

### 3. 多代理交易 (TradingAgents 融合)

**代理角色**:
| 代理 | 职责 | 分析维度 |
|------|------|---------|
| **基本面代理** | 财务分析 | 营收/利润/现金流 |
| **技术面代理** | 图表分析 | K 线/指标/形态 |
| **情绪代理** | 舆情分析 | 新闻/社交媒体 |
| **风险代理** | 风险评估 | 波动率/回撤 |

**决策流程**:
```
股票分析请求
    ↓
四代理并行分析
    ↓
汇总评分
    ↓
生成投资建议
```

---

### 4. 量化回测 (freqtrade + qlib 融合)

**功能**:
- ✅ 历史数据回测
- ✅ 策略优化
- ✅ 风险评估
- ✅ 绩效分析

**支持策略**:
- 均线交叉
- RSI 超买超卖
- MACD 动量
- 布林带突破
- 自定义策略

---

### 5. 智能研报 (daily_stock_analysis 融合)

**功能**:
- ✅ 自动收集数据
- ✅ LLM 分析生成
- ✅ 图表可视化
- ✅ 投资建议

**研报结构**:
```
1. 公司概况
2. 财务分析
3. 行业地位
4. 技术面分析
5. 风险评估
6. 投资建议
```

---

## 📐 配置参数

### 默认配置

```yaml
finance_agent:
  data_sources:
    - yahoo_finance
    - alpha_vantage
    - eastmoney
  analysis_modules:
    - fundamental
    - technical
    - sentiment
    - risk
  report_format: markdown
  chart_format: png
  language: zh-CN
```

### 可调节参数

```yaml
# 数据源配置
data:
  refresh_interval: 60      # 数据刷新间隔 (秒)
  cache_enabled: true       # 启用缓存
  cache_ttl: 3600           # 缓存时间 (秒)

# 分析配置
analysis:
  fundamental_weight: 0.4   # 基本面权重
  technical_weight: 0.3     # 技术面权重
  sentiment_weight: 0.2     # 情绪面权重
  risk_weight: 0.1          # 风险权重

# 回测配置
backtest:
  start_date: 2023-01-01
  end_date: 2026-04-22
  initial_capital: 100000
  commission: 0.001
```

---

## 📁 文件结构

```
skills/01-trading/finance-intelligence-agent/
├── SKILL.md                    # 技能定义
├── finance_agent.py            # 核心实现
├── data_sources/               # 数据源模块
│   ├── yahoo.py
│   ├── alpha_vantage.py
│   └── eastmoney.py
├── analysis/                   # 分析模块
│   ├── fundamental.py
│   ├── technical.py
│   ├── sentiment.py
│   └── risk.py
├── strategies/                 # 策略库
│   ├── momentum.py
│   ├── value.py
│   └── arbitrage.py
└── reports/                    # 研报输出
    └── templates/
```

---

## 🎯 使用场景

### 场景 1: 股票分析

```
1. 说"太一，分析 AAPL"
   → 四代理并行分析
   → 汇总评分
   → 生成投资建议

2. 输出:
   - 基本面评分：85/100
   - 技术面评分：72/100
   - 情绪面评分：90/100
   - 风险评分：60/100
   - 综合建议：买入
```

### 场景 2: 研报生成

```
1. 说"太一，生成特斯拉研报"
   → 收集财务数据
   → 分析行业地位
   → 技术面分析
   → LLM 生成报告
   → 输出 Markdown 研报

2. 输出:
   - 研报 PDF/Markdown
   - 关键图表
   - 投资建议
```

### 场景 3: 量化回测

```
1. 说"太一，回测动量策略"
   → 加载历史数据
   → 运行策略
   → 计算绩效
   → 风险评估

2. 输出:
   - 收益率曲线
   - 夏普比率
   - 最大回撤
   - 交易记录
```

---

## ⚙️ 系统要求

| 组件 | 最低要求 | 推荐配置 |
|------|---------|---------|
| **Python** | 3.8+ | 3.10+ |
| **内存** | 4GB | 8GB+ |
| **存储** | 1GB | 10GB+ |
| **网络** | 必需 | 稳定连接 |

### 依赖库

```bash
pip install yfinance pandas numpy ta-lib scikit-learn
pip install matplotlib seaborn plotly
pip install requests beautifulsoup4
```

---

## 📊 输出示例

### 股票分析报告

```markdown
# AAPL 股票分析报告

## 综合评分：78/100 🟡

### 基本面 (85/100) ✅
- 营收：$394B (+8% YoY)
- 净利润：$97B (+10% YoY)
- 现金流：$110B (强劲)
- 负债率：18% (健康)

### 技术面 (72/100) 🟡
- 趋势：上升通道
- 支撑位：$170
- 阻力位：$185
- RSI: 58 (中性)

### 情绪面 (90/100) ✅
- 新闻情绪：正面
- 社交媒体：乐观
- 分析师评级：买入 (25/30)

### 风险 (60/100) 🟠
- 波动率：中等
- 最大回撤：-15%
- Beta: 1.2

## 投资建议：买入
目标价：$195
止损价：$165
```

---

## 🔗 相关链接

| 项目 | 链接 |
|------|------|
| **OpenBB** | github.com/OpenBB-finance/OpenBB |
| **ai-hedge-fund** | github.com/virattt/ai-hedge-fund |
| **TradingAgents** | github.com/TauricResearch/TradingAgents |
| **freqtrade** | github.com/freqtrade/freqtrade |
| **qlib** | github.com/microsoft/qlib |

---

## 📝 更新日志

### v1.0 (2026-04-22)

- ✅ 初始版本
- ✅ 融合 GitHub Top 10 金融科技项目
- ✅ 四代理分析系统
- ✅ 量化回测框架
- ✅ 智能研报生成

---

*太一 AGI · Finance Intelligence Agent v1.0*  
*创建时间：2026-04-22 00:10*  
*基于：GitHub 金融科技开源项目 Top 10*  
*状态：✅ 已落地，可立即使用*
