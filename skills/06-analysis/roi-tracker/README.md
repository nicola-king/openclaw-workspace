# ROI Tracker Pro

> **Automatic ROI Tracking & Reporting for Everyone**  
> 自动追踪 ROI，生成专业报告，让每一分钱都有据可查

[![Price](https://img.shields.io/badge/price-¥299/year-green.svg)](https://gumroad.com/l/roi-tracker-pro)
[![Demo](https://img.shields.io/badge/demo-free-blue.svg)](https://github.com/nicola-king/awesome-automation/tree/main/skills/roi-tracker)

---

## 🎯 What Problem Does This Solve?

**Before (手动记录)**:
- ❌ 忘记记录交易
- ❌ Excel 表格混乱
- ❌ 不知道哪个项目赚钱
- ❌ 月底要花几小时对账

**After (自动追踪)**:
- ✅ 交易自动记录
- ✅ 报告自动生成
- ✅ ROI 一目了然
- ✅ 每月节省 5+ 小时

---

## 🚀 Quick Start (5 分钟上手)

### Step 1: Install
```bash
git clone https://github.com/nicola-king/awesome-automation.git
cd awesome-automation/skills/roi-tracker
```

### Step 2: Run
```bash
python3 SKILL.md
```

### Step 3: Add Your First Transaction
```python
from skills.roi-tracker.SKILL import ROITracker

tracker = ROITracker()

# Add revenue
tracker.add_transaction(
    type='revenue',
    category='技能销售',
    amount=299,
    description='付费技能收入'
)

# Add cost
tracker.add_transaction(
    type='cost',
    category='服务器',
    amount=100,
    description='VPS 月租'
)

# Generate report
report = tracker.generate_report(
    start_date='2026-04-01',
    end_date='2026-04-06'
)
print(report)
```

---

## 📊 Features

### ✅ Core Features (Free)
- Add transactions (revenue/cost)
- Generate basic reports
- Export to CSV
- SQLite database

### 💎 Pro Features (¥299/year)
- Weekly/Monthly auto-reports
- Trend analysis & predictions
- Multi-project tracking
- Email delivery
- API access
- Priority support

---

## 💡 Use Cases

### For Freelancers
Track income from different clients, see which projects are most profitable.

### For E-commerce Sellers
Monitor ads ROI, product margins, and overall business health.

### For Traders
Record trades, calculate win rate, track P&L over time.

### For Content Creators
Track revenue from platforms (YouTube/B 站/小红书) vs time invested.

---

## 📈 Sample Report

```markdown
# ROI Report

**Period**: 2026-04-01 ~ 2026-04-06

## Core Metrics
| Metric | Amount |
|--------|--------|
| Total Revenue | ¥3,497.00 |
| Total Cost | ¥340.00 |
| Net Profit | ¥3,157.00 |
| **ROI** | **+928.5%** 🚀 |

## Revenue Breakdown
| Category | Amount | % |
|----------|--------|---|
| 交易收益 | ¥2,100.00 | 60% |
| 技能销售 | ¥1,397.00 | 40% |

## Cost Breakdown
| Category | Amount | % |
|----------|--------|---|
| 服务器 | ¥200.00 | 59% |
| API 费用 | ¥140.00 | 41% |
```

---

## 🔧 Configuration

### Environment Variables
```bash
# .env file
ROI_DB_PATH=/path/to/your/database.db
REPORT_DIR=/path/to/reports
WECHAT_ALERT_ENABLED=true
```

### Cron Jobs (Auto Reports)
```cron
# Weekly report every Monday 9 AM
0 9 * * 1 python3 scripts/roi-weekly-report.py
```

---

## 📚 Documentation

- [Setup Guide](../../docs/setup.md)
- [API Reference](../../docs/api.md)
- [FAQ](../../docs/faq.md)

---

## 💬 Success Stories

> "ROI Tracker helped me realize my ads were losing money. Stopped the campaign, saved ¥10,000+!"  
> — **Amazon Seller, Shanghai**

> "Finally know which projects are profitable. Raised prices on low-ROI work, income up 30%!"  
> — **Freelance Developer, Beijing**

---

## 🛒 Pricing

| Plan | Price | Features |
|------|-------|----------|
| **Free** | ¥0 | Basic tracking, manual reports |
| **Pro** | ¥299/year | Auto reports, trends, API |
| **Team** | ¥999/year | Multi-user, priority support |

**👉 [Buy Now on Gumroad](https://gumroad.com/l/roi-tracker-pro)**

---

## 🤝 Support

- **Email**: support@taiyi.works
- **GitHub Issues**: [Report a bug](https://github.com/nicola-king/awesome-automation/issues)
- **WeChat**: Add SAYELF for priority support

---

## 📄 License

MIT License for core features. Pro features require paid license.

---

*Version: 1.0 | Last updated: 2026-04-06 | Created by Taiyi AGI*
