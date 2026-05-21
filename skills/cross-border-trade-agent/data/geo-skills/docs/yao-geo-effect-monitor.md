<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-effect-monitor

`yao-geo-effect-monitor` 是一个监测闭环类 GEO skill，用于设计 GEO Signal Monitor：长期采样 AI 答案、追踪引用来源、纠偏品牌事实、输出客户月报、设置告警规则，并对内容发布、页面修复和外部信源建设后的变化做谨慎归因。

## 适用场景

- GEO 项目长期运营
- 客户月报和季度复盘
- 内容迭代和页面优化后的效果观察
- 品牌事实错误纠偏
- AI 答案引用源追踪
- 监测看板、数据库表和 API 草案设计

## 国内平台适配

| 平台 | 独立采样重点 |
|---|---|
| DeepSeek | 结论稳定性、证据链、联网状态 |
| 豆包 | 口语问答、图文输出、短答案推荐 |
| 千问 | 引用源、追问路径、阿里生态或电商信源 |
| Kimi | 深度研究、长文引用、文档站 |
| 元宝 | 微信生态来源、公众号内容、视频号线索 |

## 核心输出

- GEO 后端监测方案
- 监测指标体系与 Prompt 库
- 五平台采样口径
- 引用源追踪规则
- 月报模板、告警规则和纠偏任务表
- 仪表盘字段说明
- 数据库表结构和 API 草案
- 默认四件套：Word、PDF、HTML、Markdown

## 研究增强

- GEO 黑盒可见性：同时监测出现、候选、推荐、排序和引用。
- 生成式搜索可验证性：引用质量拆成引用召回率和引用准确率。
- 生成式相关反馈：Prompt 库用实体、事实、场景和追问做可复采扩展。
- AgenticGEO 与 citation failure diagnosis：纠偏任务先诊断“为什么没被引用”，再映射到页面、知识库或外部信源。
- Causal impact：归因必须有基线窗口、观察窗口、处理 Prompt、对照 Prompt、竞品对照和混杂因素记录。

## 示例报告

四个示例文件均由同一份 Markdown 源生成：

- [Markdown](../../skills/yao-geo-effect-monitor/examples/synthetic-demo/xinglan-effect-monitor-demo.md)
- [HTML](../../skills/yao-geo-effect-monitor/examples/synthetic-demo/xinglan-effect-monitor-demo.html)
- [Word](../../skills/yao-geo-effect-monitor/examples/synthetic-demo/xinglan-effect-monitor-demo.docx)
- [PDF](../../skills/yao-geo-effect-monitor/examples/synthetic-demo/xinglan-effect-monitor-demo.pdf)

HubSpot 国内 AI 平台公司专项测试四件套：

- [Markdown](../../skills/yao-geo-effect-monitor/examples/hubspot-cn-signal-monitor/hubspot-cn-effect-monitor.md)
- [HTML](../../skills/yao-geo-effect-monitor/examples/hubspot-cn-signal-monitor/hubspot-cn-effect-monitor.html)
- [Word](../../skills/yao-geo-effect-monitor/examples/hubspot-cn-signal-monitor/hubspot-cn-effect-monitor.docx)
- [PDF](../../skills/yao-geo-effect-monitor/examples/hubspot-cn-signal-monitor/hubspot-cn-effect-monitor.pdf)

## 质量门

- 四格式文件必须真实存在并可读。
- HTML、Word、PDF、Markdown 必须保持章节和关键表格一致。
- 不只看品牌出现率，还要看候选率、推荐率、描述准确率和引用质量。
- 引用质量必须同时判断召回和准确。
- 归因不能只看前后变化，必须有时间窗口和对照组。
- 纠偏任务必须有负责人、验收指标和复采日期。

## 包路径

- Skill package: [skills/yao-geo-effect-monitor](../../skills/yao-geo-effect-monitor)
