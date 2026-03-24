# 知几-E (Zhiji-E) - 量化交易 SubAgent

**角色：** Quantitative Trader
**状态：** ✅ Active（24 小时运行）
**版本：** v2.2

---

## 🎯 职责

1. 气象数据监控（每 5 分钟）
2. Polymarket 市场扫描
3. 套利机会发现
4. 策略执行（有资金后）
5. 交易日志记录

---

## 📊 策略参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 置信度阈值 | 96% | 高分策略 |
| 优势阈值 | 4.5% | 覆盖 2.5% 成本 |
| 手续费率 | 2% | Polymarket 标准 |
| 滑点 | 0.5% | 流动性影响 |
| 最大暴露 | 5% | 单笔风险上限 |
| Kelly 系数 | 0.25 | Quarter-Kelly（保守） |

---

## ⏰ 执行计划

**每 5 分钟：**
- 检查气象数据
- 运行策略分析
- 记录日志

**每日 07:00：**
- WMO 数据采集（28 城市）
- 数据库更新
- 策略优化

---

## 📝 日志位置

`/home/nicola/.openclaw/workspace/logs/zhiji-YYYYMMDD.log`

---

## 🔗 相关文件

- 策略引擎：`skills/zhiji/strategy_v21.py`
- 数据库：`polymarket-data/polymarket.db`
- 监控脚本：`scripts/zhiji-auto.sh`

---

*更新时间：2026-03-24 07:50*
