<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-comparison-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 示例说明

本目录存放 `yao-geo-comparison-builder` 的公开示例。

当前示例：

- `hubspot-cn-demo/`：以 HubSpot 为目标品牌，对比 Salesforce、Zoho CRM 和自建 CRM/表格方案，输出中文简体四格式报告。

每个示例必须满足：

- 真实品牌事实必须来自官网、产品目录、价格页、帮助中心、新闻稿或用户提供的可引用资料。
- 自建方案、传统方案、表格方案只能作为方案类型处理，不得伪造外部来源。
- 每个示例文件夹必须同时包含 Word（`.docx`）、PDF（`.pdf`）、HTML（`.html`）和 Markdown（`.md`）。
- 真实品牌示例必须包含 `sources.json`、`report_input.json` 和 `quality-report.json`。
- 启用公共网页核验时，示例必须包含 `source-verification.json`，记录来源访问方式、HTTP 状态、验证结果和访问日期。
- 完整报告示例必须包含执行摘要、决策维度模型、方案评分矩阵、来源质量分级、风险与治理地图和落地核验清单。
- HTML 示例必须按 Kami 长文档风格排版，包含暖米纸底、ivory 内容面、油墨蓝强调和固定目录栏；页面下拉时目录跟随，且锚点不遮挡章节标题。
- Word 必须检查右侧溢出：`quality-report.json` 中的 `docx_layout_profile.right_overflow_detected` 必须为 `false`。
