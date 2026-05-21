<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-intent-miner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 示例

## `hubspot-cn-demo`

以 HubSpot 为测试对象，模拟国内 AI 平台上的中文简体意图挖掘场景。

- 输入：`hubspot-cn-demo/input/report_input.json`
- 输出：`hubspot-cn-demo/expected-output/`
- 质量报告：`hubspot-cn-demo/expected-output/quality-report.json`

四格式输出包含 Markdown、HTML、Word 和 PDF。HTML/PDF 使用 kami 风格的暖纸底、油墨蓝和暖灰边框；Word/PDF 已按 `references/four-format-output.md` 执行防右侧溢出约束。

示例报告已区分真实数据状态：官方公开事实已校准，国内 AI 平台真实回答、搜索量、CRM、客服和销售数据仍标注为未采样或待授权，不会把预测意图空间冒充为真实监测结果。
