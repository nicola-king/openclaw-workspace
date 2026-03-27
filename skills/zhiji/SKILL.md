# 知几 - 量化交易技能

> Polymarket 量化交易师，专注于预测市场套利和自动化交易

---

## 📋 技能信息

| 项目 | 内容 |
|------|------|
| **名称** | 知几 (Zhiji) |
| **版本** | v2.2 |
| **创建时间** | 2026-03-24 |
| **作者** | 太一 |
| **状态** | ✅ 运行中 |
| **Bot** | @sayelf_bot |

---

## 🎯 功能描述

**核心功能**:
- Polymarket 市场数据采集
- 气象套利策略执行
- 鲸鱼地址追踪
- 自动化下注
- 收益统计报告

**策略模块**:
| 策略 | 状态 | 说明 |
|------|------|------|
| 气象套利 | ✅ 就绪 | 置信度>96%，优势>2% |
| 鲸鱼跟随 | 🟡 待验证 | 追踪高胜率地址 |
| 空投套利 | ⏳ 调研完成 | OpenLedger 等 |

---

## 🔧 技术架构

```
zhiji-e/
├── strategy_v22.py      # 策略引擎 v2.2
├── polymarket_client.py # API 客户端
├── requirements.txt     # 依赖
└── README.md           # 使用文档
```

**核心策略**:
- ColdMath 增强版
- Quarter-Kelly 下注
- 置信度阈值 96%
- 优势阈值 2%

---

## 📖 使用方法

### 启动策略

```bash
cd ~/.openclaw/workspace/github/zhiji-e
python3 strategy_v22.py
```

### 查看日志

```bash
tail -f logs/zhiji.log
```

### 查看收益

```bash
python3 -c "from polymarket_client import PolymarketClient; c = PolymarketClient(); print(c.get_balance())"
```

---

## 📊 性能指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 置信度阈值 | 96% | 96% ✅ |
| 优势阈值 | 2% | 2% ✅ |
| 下注策略 | Quarter-Kelly | ✅ |
| 数据记录 | 189 条 | 189 条 ✅ |
| 首笔下注 | 待执行 | 🟡 |

---

## 📞 支持与反馈

**GitHub**: github.com/nicola-king/zhiji-e
**文档**: github/zhiji-e/README.md

---

*版本：v2.2 | 更新时间：2026-03-24 | 状态：就绪待命*
