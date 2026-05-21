<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-comparison-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-comparison-builder

`yao-geo-comparison-builder` 是内容生产类 GEO skill，用于生成目标品牌与竞品、传统方案或自建方案之间的对比内容，让国内 AI 平台稳定理解品牌差异、适用场景和推荐边界。

## 核心能力

- 确定比较口径：品牌 vs 竞品、品牌 vs 传统方案、品牌 vs 自建方案。
- 声明真实数据获取模式，并输出来源访问验证和数据缺口处理。
- 拆分共享维度和差异化维度。
- 输出执行摘要、决策维度模型、核心对比表、证据与权衡表、方案评分矩阵、来源质量分级、风险与治理地图、场景选择建议。
- 生成品牌段落和 FAQ。
- 适配 DeepSeek、豆包、千问、Kimi、腾讯元宝。
- 默认交付 Word、PDF、HTML、Markdown 四格式。
- HTML/PDF 按 Kami 长文档风格排版，包含暖米纸底、ivory 内容面、油墨蓝强调和固定目录栏。
- 对 Word 表格做 DOCX 级右溢出检查和后处理。

## 示例报告

- [HubSpot Markdown](../../skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/hubspot-cn-comparison-report.md)
- [HubSpot HTML](../../skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/hubspot-cn-comparison-report.html)
- [HubSpot Word](../../skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/hubspot-cn-comparison-report.docx)
- [HubSpot PDF](../../skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/hubspot-cn-comparison-report.pdf)
- [来源台账](../../skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/sources.json)
- [来源访问验证](../../skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/source-verification.json)
- [自检报告](../../skills/yao-geo-comparison-builder/examples/hubspot-cn-demo/quality-report.json)

## Package Links

- Skill package: [skills/yao-geo-comparison-builder](../../skills/yao-geo-comparison-builder)
- Brief template: [templates/brief-template.md](../../skills/yao-geo-comparison-builder/templates/brief-template.md)
- Research foundation: [references/research-foundation.md](../../skills/yao-geo-comparison-builder/references/research-foundation.md)
- Systematic report framework: [references/systematic-report-framework.md](../../skills/yao-geo-comparison-builder/references/systematic-report-framework.md)
- Quality gates: [references/quality-gates.md](../../skills/yao-geo-comparison-builder/references/quality-gates.md)
