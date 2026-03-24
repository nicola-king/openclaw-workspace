# 知几-E (Zhiji-E)

太一 Polymarket 气象套利策略引擎 v2.1

## 🎯 策略逻辑

```
气象数据 (NOAA + WMO) → 预测模型 → 赔率对比 → 套利执行
```

## 📊 核心参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 置信度阈值 | 96% | 高分策略 |
| 优势阈值 | 2% | 最小套利空间 |
| 下注策略 | Quarter-Kelly | 保守策略 |
| 最大暴露 | 5% | 单笔风险上限 |

## 🚀 快速开始

```bash
git clone https://github.com/taiyi-ag/zhiji-e
cd zhiji-e
pip install -r requirements.txt
python strategy_v21.py
```

## 📈 预期表现

| 阶段 | 资金 | 月收益 |
|------|------|--------|
| 模拟盘 | $0 | 策略验证 |
| 小资金 | $100 | $20-50 |
| 扩大 | $500 | $100-250 |

## 🤝 贡献

欢迎 PR + Issue!

## 📝 许可

MIT License

## 🔗 链接

- Twitter: @SayelfTea
- Discord: sayelf
- 官网：taiyi.ag (coming soon)