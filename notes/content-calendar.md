# 内容日历 — 下两周编排

> GEO 优化 — 内容日历编排
> 生成：2026-05-16 15:27 CST
> 工具：`content_calendar_generator.py` — 2 个月内容日历已生成
> 输出文件：`/home/sayelf/.openclaw/workspace/data/cross-border/content_calendar/content_calendar.json`

---

## 执行摘要

| 指标 | 数值 |
|------|------|
| 生成月数 | 2 个月（8 周） |
| 开始日期 | 2026-05-18 |
| 总帖子数 | 48 篇 |
| 每周帖子 | 6 篇（周一至周六） |
| 特殊事件 | 5 个 |

---

## 下周内容日历 (Week 1: 2026-05-18 ~ 2026-05-24)

| 日期 | 星期 | 主题 | 平台 | 内容小标题 |
|------|------|------|------|-----------|
| 05-18 | 周一 | ✨ Industry Insight | LinkedIn | 「Why Global Buyers Are Choosing Chinese Modular Containers」 |
| 05-19 | 周二 | 📢 Company News | Facebook | 公司动态/工厂新产线或认证通过公告 |
| 05-20 | 周三 | 📊 Case Study | LinkedIn | 「如何用模块化房屋 30 天建成海外营地」 |
| 05-21 | 周四 | ❓ FAQ | Facebook | 「常见问题：模块化房屋的 MOQ 和物流成本」 |
| 05-22 | 周五 | 📝 Weekly Summary | LinkedIn | 本周行业洞察汇总 |
| 05-23 | 周六 | 🏢 Team Culture | Facebook | 团队风采/工厂实拍 |

### 内容要点

**周一 (LinkedIn):** 使用 `linkedin_content_module.py` 的 generate_industry_insight() 方法。聚焦：中国工厂的规模化生产优势、价格竞争力、认证进展。

**周三 (LinkedIn):** 最好有一个真实的项目案例（中东/非洲/东南亚项目）。展示施工前后对比图。

**周五 (LinkedIn):** 汇总本周对模块化建筑行业的观察，突出 1-2 个数据点。

---

## 下下周内容日历 (Week 2: 2026-05-25 ~ 2026-05-31)

| 日期 | 星期 | 主题 | 平台 | 内容小标题 |
|------|------|------|------|-----------|
| 05-25 | 周一 | ✨ Industry Insight | LinkedIn | 「The Real Cost of a Container House: $25K vs $50K」 |
| 05-26 | 周二 | 📢 Company News | Facebook | 新合作/订单/展会预告 |
| 05-27 | 周三 | 📊 Case Study | LinkedIn | 「便携式储能在偏远地区应用的 3 个真实案例」 |
| 05-28 | 周四 | ❓ FAQ | Facebook | 「模块化房屋的定制流程和周期解释」 |
| 05-29 | 周五 | 📝 Weekly Summary | LinkedIn | 模块化建筑全球市场动态周报 |
| 05-30 | 周六 | 🏢 Team Culture | Facebook | 车间/质检/产品实拍 |

### 内容要点

**周一 (LinkedIn):** 从长尾词内容（`notes/long-tail-content.md`）提取「Total Cost of Ownership」部分，精炼成 LinkedIn 帖子。

**周四 (Facebook):** 使用 `faq_content_library.py` 的 FAQ 内容，聚焦质量控制流程和认证体系。

---

## CTA 优化策略

### LinkedIn CTA 文案选项

| 帖子类型 | CTA 选项 1 | CTA 选项 2 |
|---------|-----------|-----------|
| Industry Insight | "Follow for more modular construction insights →" | "Which market do you see growing fastest? Drop a comment." |
| Case Study | "DM for the full case study PDF →" | "Want to see the project specs? Comment 'SPECS'" |
| Weekly Summary | "Save this post for reference →" | "Share with your supply chain team →" |

### Facebook CTA 文案选项

| 帖子类型 | CTA 选项 |
|---------|---------|
| Company News | "Message us for factory tour schedule →" |
| FAQ | "Got more questions? Drop them below ↓" |
| Team Culture | "Want to visit our factory? Send us a message!" |

---

## 8 周内容节奏

| 周次 | 日期 | 重点主题 | 平台分布 |
|------|------|---------|---------|
| W1 | 05-18 | Market entry strategy | LI(3) + FB(3) |
| W2 | 05-25 | Cost comparison | LI(3) + FB(3) |
| W3 | 06-01 | Technical specs (steel, insulation) | LI(3) + FB(3) |
| W4 | 06-08 | Logistics & shipping | LI(3) + FB(3) |
| W5 | 06-15 | Solar + storage integration | LI(3) + FB(3) |
| W6 | 06-22 | Regional market deep dives | LI(3) + FB(3) |
| W7 | 06-29 | Factory audit & quality | LI(3) + FB(3) |
| W8 | 07-06 | Industry event coverage | LI(3) + FB(3) |

---

## 脚本运行记录

```bash
$ python3 -c "
from content.content_calendar_generator import ContentCalendarGenerator
gen = ContentCalendarGenerator()
calendar = gen.generate_calendar(months=2, start_date='2026-05-18')
"
```

✅ 2 个月内容日历已生成，总计 48 篇帖子，保存至 `data/cross-border/content_calendar/content_calendar.json`
