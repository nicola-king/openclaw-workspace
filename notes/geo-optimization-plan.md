# GEO 优化融合执行计划

> 基于 2026-05-16 14:00 GEO 日报建议 + 已完成的 .edu/.gov 拓展
> 生成：2026-05-16 15:23 CST

---

## 优先级重排（已融合今日已完成工作）

### 已完成
- [x] .edu/.gov 高信任渠道发现（已入库 10 个）
- [x] GEO 配置更新（academic/gov 平台 + 优先策略）
- [x] 策略文档（notes/academic-gov-opportunities.md）

### 立即执行（今日~明日）

**1. Top 3 媒体 Pitch 外联**
目标：Practicalecommerce / Digitalcommerce360 / Supplychaindive
输出：3 篇英文 pitch email + 行业洞察稿
工具：cross-border-core 触达模块

**2. LinkedIn 内容矩阵启动**
主题：「中国折叠房屋出口指南」系列
频次：每周 2 篇英文 post
输出：首批 2 篇 + 加入 3 个行业群组
工具：linkedin_content_module.py

**3. Perplexity/SearchGPT 专项优化**
方向：FAQ 内容收录 + 长尾问答布局
输出：3 篇长尾词落地页内容
关键词：
- "affordable modular container house with solar panel" (难度 20, 3K/月)
- "modular container house battery life comparison" (难度 15)
- "how to choose modular container house" (难度 30)

### 本周执行

**4. 竞品价格应对**
动作：评估竞品 A 储能降价 15% 的应对策略
输出：定价建议报告（跟进/差异化/跳过）

**5. 内容日历编排**
工具：content_calendar_generator.py
输出：下两周内容日历 + CTA 优化

**6. YouTube 频道规划**
第一期主题："How Modular Container Houses Are Built in 2026"
工具：html_video_generator.py → YouTube + B站

---

## 成本控制

所有内容生成优先使用本地脚本工具（零 token 成本）：
- LinkedIn 帖子 → linkedin_content_module.py
- 内容日历 → content_calendar_generator.py
- FAQ 内容 → faq_content_library.py
- 视频文案 → html_video_generator.py

仅需要高质量/品牌化输出时使用 html-agent.py（Tier 2）
