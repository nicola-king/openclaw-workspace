# yao-geo-intent-miner

`yao-geo-intent-miner` 用于把种子词、品牌词、产品线、竞品词、区域词、人群词和业务材料扩展为 AI 搜索问题集、意图簇、追问链路、查询重写清单、内容选题、FAQ 和监测 Prompt 库。

## 示例报告

- [HubSpot 中文测试输入](../../skills/yao-geo-intent-miner/examples/hubspot-cn-demo/input/report_input.json)
- [HTML](../../skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/hubspot-cn-ai-intent-miner-demo.html)
- [Word](../../skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/hubspot-cn-ai-intent-miner-demo.docx)
- [PDF](../../skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/hubspot-cn-ai-intent-miner-demo.pdf)
- [Markdown](../../skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/hubspot-cn-ai-intent-miner-demo.md)
- [质量报告](../../skills/yao-geo-intent-miner/examples/hubspot-cn-demo/expected-output/quality-report.json)

## 质量门

- 输出完整自然语言问题，不是短关键词列表。
- 每个核心问题都有意图类型、问题簇、查询重写、证据查询和资产映射。
- 追问链路保留父子关系、上下文依赖和独立重写。
- Word 宽表不得向右溢出；PDF 默认横向 A4。
- `quality-report.json` 的 `failed_checks` 必须为空。
