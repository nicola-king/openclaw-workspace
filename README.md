# 🤖 太一 Agent 系统 (Taiyi Agents)

> **60+ 专业 AI Agent** · **自进化能力** · **中文优化** · **完全开源**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Stars](https://img.shields.io/github/stars/nicola-king/taiyi-agents)]()
[![Issues](https://img.shields.io/github/issues/nicola-king/taiyi-agents)]()

---

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/nicola-king/taiyi-agents.git
cd taiyi-agents

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key

# 4. 开始使用
python3 main.py
```

---

## ✨ 核心特性

### 🧠 60+ 专业 Agent

| 类别 | Agent 数量 | 代表 Agent |
|------|-----------|-----------|
| **📈 交易类** | 5+ | Polymarket/GMGN/币安 |
| **📝 内容类** | 10+ | 公众号/小红书/知乎 |
| **🛠️ 系统类** | 15+ | 监控/自愈/调度 |
| **📊 分析类** | 8+ | 数据/报表/洞察 |
| **💼 商业类** | 15+ | 前端/后端/市场/销售 |
| **🎨 设计类** | 5+ | UI/UX/品牌 |
| **🤖 工程类** | 10+ | AI/DevOps/移动 |

### 🔄 自进化能力

- ✅ **能力涌现检测**：同类任务重复 3 次自动提议新建 Skill
- ✅ **技能自动创建**：经批准后自动创建新 Skill
- ✅ **经验积累分享**：经验沉淀到知识库，供其他 Agent 学习

### 🤝 多 Bot 协作

借鉴 TradingAgents 设计，5 大核心 Bot 协作：

| Bot | 职责 | 触发关键词 |
|-----|------|-----------|
| **知几** | 数据分析 | 数据/分析/趋势/量化 |
| **山木** | 业务执行 | 执行/项目/任务/落地 |
| **素问** | 技术研究 | 研究/技术/开发/原理 |
| **罔两** | 市场情报 | 市场/竞品/情报/舆情 |
| **庖丁** | 财务管控 | 财务/成本/预算/风险 |

### 📚 TurboQuant 记忆架构

4 层记忆系统，模拟人类记忆：

| 层级 | 文件 | 内容 | 加载策略 |
|------|------|------|---------|
| 核心层 | memory/core.md | 核心记忆 (80%) | 每次必读 |
| 残差层 | memory/residual.md | 细节信息 (20%) | 按需加载 |
| 固化层 | MEMORY.md | 长期记忆 | 主 Session 加载 |
| 日志层 | memory/YYYY-MM-DD.md | 原始日志 | 恢复上下文 |

### ⚖️ 宪法约束系统

- **负熵法则**：输出必须创造价值，废话=不输出
- **价值基石**：帮助而非表演，行动胜过空谈
- **美学法则**：每一行代码都是诗，每一个输出都是画
- **诚实边界**：不知道的事情直接说不知道

---

## 📋 使用场景

### 💰 自动化交易

```python
from skills.trading import PolymarketAgent

agent = PolymarketAgent()
result = agent.analyze_market(event_id="xxx")
print(f"建议下注：{result.recommendation}")
```

### 📝 内容创作

```python
from skills.content import XiaohongshuAgent

agent = XiaohongshuAgent()
post = agent.create_post(topic="AI Agent 使用教程")
print(post.content)
```

### 🛠️ 系统运维

```python
from skills.system import MonitorAgent

agent = MonitorAgent()
health = agent.check_system_health()
print(f"系统健康度：{health.score}")
```

### 📊 数据分析

```python
from skills.analysis import DataAnalyst

analyst = DataAnalyst()
report = analyst.generate_report(data="sales.csv")
print(report.insights)
```

---

## 📚 文档

| 文档 | 说明 | 链接 |
|------|------|------|
| **快速开始** | 5 分钟上手指南 | [docs/quickstart.md](docs/quickstart.md) |
| **Agent 列表** | 60+ Agent 完整列表 | [docs/agents.md](docs/agents.md) |
| **API 文档** | API 参考文档 | [docs/api.md](docs/api.md) |
| **最佳实践** | 使用技巧和案例 | [docs/best-practices.md](docs/best-practices.md) |
| **用户指南** | 详细使用手册 | [docs/guide/](docs/guide/) |

---

## 🔧 安装与配置

### 系统要求

- Python 3.12+
- 内存 ≥ 4GB
- 磁盘 ≥ 10GB

### 环境变量

```bash
# .env 文件配置

# LLM API
OPENAI_API_KEY=sk-xxx
QWEN_API_KEY=sk-xxx

# 交易 API (可选)
POLYMARKET_API_KEY=xxx
GMGN_API_KEY=xxx

# 其他服务 (可选)
TELEGRAM_BOT_TOKEN=xxx
WECHAT_API_KEY=xxx
```

### 依赖安装

```bash
# 基础依赖
pip install -r requirements.txt

# 交易模块 (可选)
pip install -r requirements-trading.txt

# 开发依赖
pip install -r requirements-dev.txt
```

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 贡献方式

1. 🐛 报告 Bug
2. 💡 提出新功能建议
3. 📝 改进文档
4. 🔧 提交代码 PR
5. 📢 分享使用体验

### 贡献者

感谢所有贡献者！

[![Contributors](https://contrib.rocks/image?repo=nicola-king/taiyi-agents)]()

---

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

| 渠道 | 链接 |
|------|------|
| **GitHub** | [github.com/nicola-king/taiyi-agents](https://github.com/nicola-king/taiyi-agents) |
| **Issues** | [github.com/nicola-king/taiyi-agents/issues](https://github.com/nicola-king/taiyi-agents/issues) |
| **讨论区** | [github.com/nicola-king/taiyi-agents/discussions](https://github.com/nicola-king/taiyi-agents/discussions) |

---

##  Star History

[![Star History Chart](https://api.star-history.com/svg?repos=nicola-king/taiyi-agents&type=Date)]()

---

## 🙏 致谢

- 感谢 [OpenClaw](https://github.com/openclaw/openclaw) 提供基础框架
- 感谢 [agency-agents](https://github.com/msitarzewski/agency-agents) 提供设计灵感
- 感谢所有贡献者和用户

---

*太一 AGI · Taiyi Agents · 2026-04-16*
