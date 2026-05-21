<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-intent-miner
Created by: 姚金刚
Date: 2026-05-21
X: https://x.com/yaojingang
-->

# 方法与报告完整度升级记录

## 升级原因

本次迭代将 `yao-geo-intent-miner` 从基础意图拓词升级为系统化 AI 搜索意图挖掘与报告生成 skill。重点修复三个问题：

- 方法依据不够显式，容易退化为关键词扩展。
- 报告模块不够完整，缺少证据缺口、合规边界、落地路线和附录资产。
- 示例输出依赖手工产物，HTML 没有 sticky 菜单，四格式一致性缺少自动检查。

## 新增能力

- 新增 `references/research-foundation.md`：沉淀搜索意图、会话式查询重写、LLM 查询扩展、检索评测和内容可信度的参考基线。
- 新增 `references/report-module-contract.md`：规定正文 14 个核心模块和附录资产下限。
- 新增 `scripts/render_intent_miner_report.py`：从 JSON 输入生成 Markdown、HTML、DOCX、PDF 和 `quality-report.json`。
- HTML 报告新增 sticky 目录菜单，下拉时固定跟随。
- DOCX 默认横向 A4、固定表格布局、表格总宽不超过 `15138 dxa`，并对长 URL/英文 token 加软换行。
- PDF 默认横向 A4，表格固定布局、长文本换行、右侧边缘防溢出。

## HubSpot 示例更新

- 正文模块：14 个。
- 问题库：18 条。
- 评分矩阵：18 条，十维评分。
- 追问链路：9 条。
- 监测 Prompt：7 条，覆盖 DeepSeek、豆包、千问、Kimi、元宝。
- 附录：问题库、评分矩阵、追问链路、监测 Prompt、内容选题、FAQ、知识库条目、证据来源、落地路线。

## 验证结果

- `python3 -m py_compile skills/yao-geo-intent-miner/scripts/render_intent_miner_report.py skills/yao-geo-intent-miner/scripts/check_report_layout.py`：通过。
- `python3 scripts/validate_repository.py`：通过。
- `quality-report.json`：`failed_checks: []`，`overall_score: 100`。
- `check_report_layout.py`：DOCX 可读、24 张表均为 fixed layout、最大表宽和最大 grid 宽均为 `15138 dxa`、PDF 为 A4 横向。
- PDF PNG 渲染检查：右侧 3 像素边缘无非页面背景色贴边内容。
- Chrome headless HTML 截图：页面可渲染，非空白。

## 后续迭代方向

- 接入真实 AI 平台采样结果，替代示例中的静态 Prompt 库。
- 增加 CSV/Excel 问题库导出。
- 增加基于真实搜索量、站内搜索和客服问答的评分校准脚本。
