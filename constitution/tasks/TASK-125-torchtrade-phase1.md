# TASK-125: TorchTrade Phase 1 - 环境搭建

> 创建时间：2026-04-04 08:12 | 截止：2026-04-18 | 负责：太一

---

## 📋 任务概述

**目标**：完成 TorchTrade 环境搭建 + Binance 集成验证

**周期**：2 周（14 天）

**验收标准**：
- [ ] TorchTrade v0.0.1 安装成功
- [ ] 虚拟环境隔离配置完成
- [ ] Binance API 连接测试通过
- [ ] SequentialTradingEnv 运行示例
- [ ] 输出验证报告

---

## 🗺️ 执行计划

### Week 1: 环境搭建

| 天数 | 任务 | 产出 |
|------|------|------|
| **D1** | TorchTrade 安装 + 依赖配置 | `requirements-torchtrade.txt` |
| **D2** | 虚拟环境创建 + 版本锁定 | `venv/torchtrade/` |
| **D3** | Binance API 配置（测试网） | `config/binance-test.yaml` |
| **D4** | 连接测试 + 数据获取验证 | 测试脚本 + 截图 |
| **D5** | 周总结 + 问题记录 | `reports/week1-summary.md` |

### Week 2: 集成验证

| 天数 | 任务 | 产出 |
|------|------|------|
| **D6** | SequentialTradingEnv 示例运行 | 运行日志 |
| **D7** | OneStepTradingEnv 对比测试 | 对比报告 |
| **D8** | RuleBasedActor 封装测试 | 测试代码 |
| **D9** | 实盘模拟（测试网） | 模拟交易记录 |
| **D10** | Phase 1 验收报告 | `reports/phase1-report.md` |
| **D11-14** | 缓冲/问题修复 | - |

---

## 🔧 技术配置

### 虚拟环境
```bash
python3.11 -m venv venv/torchtrade
source venv/torchtrade/bin/activate
```

### 依赖安装
```bash
pip install torchtrade==0.0.1
pip install torch torchvision torchaudio
pip install torchrl
pip install gymnasium
```

### Binance 测试网配置
```yaml
binance:
  testnet: true
  api_key: ${BINANCE_TESTNET_API_KEY}
  api_secret: ${BINANCE_TESTNET_API_SECRET}
  base_url: https://testnet.binance.vision
```

---

## 📁 文件结构

```
workspace/
├── skills/torchtrade-integration/
│   ├── SKILL.md
│   ├── env_config.py
│   ├── binance_adapter.py
│   └── rule_based_actor.py
├── config/
│   └── binance-test.yaml
├── scripts/
│   ├── install-torchtrade.sh
│   └── test-binance-connection.py
├── reports/
│   ├── phase1-report.md
│   └── week1-summary.md
└── venv/
    └── torchtrade/
```

---

## ⚠️ 风险缓解

| 风险 | 缓解措施 |
|------|---------|
| 依赖冲突 | 虚拟环境隔离 |
| API 不稳定 | 测试网先行，加重试逻辑 |
| 文档不全 | GitHub Issues + 源码阅读 |
| 单资产限制 | 先聚焦 BTC/USDT |

---

## 📊 进度追踪

| 日期 | 完成度 | 备注 |
|------|--------|------|
| 2026-04-04 | 35% | D1✅ 环境搭建 / D2✅ 版本锁定 / D3🟡 配置待 API Key |
| - | - | - |

---

## 🔗 相关链接

- TorchTrade GitHub: https://github.com/TorchTrade/torchtrade
- TorchTrade 文档: https://torchtrade.github.io/torchtrade/
- 知几-E 仓库: https://github.com/nicola-king/zhiji-e
- Phase 1 验收报告: `reports/phase1-report.md`

---

*创建时间：2026-04-04 08:12 | 太一 AGI · 自主执行*
