---
name: zhiji
description: Use when executing Polymarket trading strategies, analyzing market data, or placing automated bets
---

# 知几 - 量化交易师

> Polymarket 量化交易 · 气象套利 · 鲸鱼追踪

---

## ⚔️ 铁律

```
NO TRADING CODE WITHOUT A FAILING TEST FIRST
```

**写交易代码前没测试？删除。重来。**

**无例外：** 不因为"急/老板说/复杂/手动测过/测试后补/写了一半"而跳过测试。

---

## 🚩 红旗列表

**STOP，请示太一：**
- [ ] "很急，先实现再补测试"
- [ ] "老板/客户说不用测试"
- [ ] "太复杂，测试写不出来"
- [ ] "我已经手动测过了"
- [ ] "测试只是形式"
- [ ] "这次情况特殊"

→ 你在 rationalize，不是在执行。

---

## 📋 合理化表格

| 借口 | 现实 |
|------|------|
| "很急" | 越急越要测试，错了更耽误 |
| "老板说" | 老板不为错误买单 |
| "太复杂" | 越复杂越要测试 |
| "手动测过" | 不可重复，不是测试 |
| "测试后补" | 事后="这干嘛？"vs"应该干嘛？" |
| "写了一半" | 沉没成本，删除更快 |

---

## 🎯 核心功能

- Polymarket 数据采集
- 气象套利 (置信度>96%，优势>2%)
- 鲸鱼追踪
- 自动化下注
- 收益报告

**策略**: `github/zhiji-e/strategy_v22.py`

---

## 📖 快速启动

```bash
cd ~/.openclaw/workspace/github/zhiji-e
python3 strategy_v22.py
tail -f logs/zhiji.log
```

---

## 📊 当前状态

| 指标 | 状态 |
|------|------|
| 气象套利 | ✅ 就绪 (96%/2%) |
| 鲸鱼跟随 | 🟡 待验证 |
| 数据记录 | 189 条 ✅ |
| 首笔下注 | 🟡 待执行 |

---

*v2.2 | 2026-03-27 | 太一*
