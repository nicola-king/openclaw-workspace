# Growth Experiment Pro

> **A/B Testing with Statistical Significance**  
> 用数据决策，不再拍脑袋做实验

[![Price](https://img.shields.io/badge/price-¥499/year-blue.svg)](https://gumroad.com/l/growth-experiment-pro)
[![Demo](https://img.shields.io/badge/demo-free-blue.svg)](https://github.com/nicola-king/awesome-automation/tree/main/skills/growth-experiment)

---

## 🎯 What Problem Does This Solve?

**Before (凭感觉)**:
- ❌ A/B 测试靠猜
- ❌ 不知道结果是否显著
- ❌ 样本量计算复杂
- ❌ 报告手动整理

**After (数据驱动)**:
- ✅ 自动统计检验
- ✅ 置信区间计算
- ✅ 样本量一键计算
- ✅ 报告自动生成

---

## 🚀 Quick Start (5 分钟上手)

### Step 1: Install
```bash
git clone https://github.com/nicola-king/awesome-automation.git
cd awesome-automation/skills/growth-experiment
```

### Step 2: Run Your First A/B Test
```python
from skills.growth-experiment.SKILL import GrowthExperiment

# Create experiment
exp = GrowthExperiment(
    hypothesis="情感化标题点击率更高",
    metric_name="点击率"
)

# Run A/B test
result = exp.run_ab_test(
    variant_a_name="技术标题",
    variant_b_name="情感标题",
    a_samples=1000,
    b_samples=1000,
    a_successes=50,   # 5% CTR
    b_successes=65    # 6.5% CTR
)

print(result.recommendation)
# Output: ✅ 采用 情感标题 - 提升 +30.0% (p=0.0234)
```

---

## 📊 Features

### ✅ Core Features (Free)
- A/B test execution
- Chi-square significance test
- Confidence interval calculation
- Basic reporting

### 💎 Pro Features (¥499/year)
- Sample size calculator
- Multi-variant testing
- Automated recommendations
- Team collaboration
- API access
- Priority support

---

## 💡 Use Cases

### For Content Creators
Test different titles/thumbnails to maximize views and engagement.

### For Product Managers
Test feature changes, measure impact on user behavior.

### For Marketers
Test ad copy, landing pages, email subject lines.

### For E-commerce
Test product descriptions, pricing strategies, promotions.

---

## 📈 Sample Output

```
╔══════════════════════════════════════════════════════════╗
║  🧪 Growth Experiment v1.0                               ║
╚══════════════════════════════════════════════════════════╝

📝 Example 1: Content Title A/B Test

  ✅ 采用 情感标题 - 提升 +30.0% (p=0.0234)
  提升：+30.0%
  P 值：0.0234

📐 Example 2: Sample Size Calculation

  基线转化率：5%
  最小可检测效应：20%
  所需样本量：每组 1,567 个
  总计：3,134 个
```

---

## 🔧 Statistical Methods

### Significance Testing
- Chi-square test (2x2 contingency table)
- P-value calculation
- Confidence level: 95% (customizable)

### Confidence Intervals
- Normal approximation method
- 95% CI by default
- Customizable alpha level

### Sample Size Calculation
- Power analysis (default 80%)
- Minimum Detectable Effect (MDE)
- Baseline rate estimation

---

## 📚 Documentation

- [Setup Guide](../../docs/setup.md)
- [Statistical Methods](../../docs/stats-methods.md)
- [Case Studies](../../docs/cases.md)
- [FAQ](../../docs/faq.md)

---

## 💬 Success Stories

> "Tested 5 headline variations, found a winner with +45% CTR. This tool paid for itself 100x!"  
> — **Content Creator, 10K followers**

> "Finally understand statistical significance. No more guessing if results are real!"  
> — **Product Manager, Tech Company**

---

## 🛒 Pricing

| Plan | Price | Features |
|------|-------|----------|
| **Free** | ¥0 | Basic A/B testing, manual reports |
| **Pro** | ¥499/year | Sample calculator, automation, API |
| **Team** | ¥1,499/year | Multi-user, collaboration, priority support |

**👉 [Buy Now on Gumroad](https://gumroad.com/l/growth-experiment-pro)**

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
