# yao-geo-panorama-audit

`yao-geo-panorama-audit` 是一个战略诊断类 GEO skill，用于建立品牌在国内 AI 平台中的可见性基线，并输出竞品差距、资产缺口、机会地图和优先级。

## 中文概述

这个 skill 负责项目启动前的第一层判断：AI 是否知道这个品牌，是否愿意推荐，描述是否准确，引用了哪些来源，竞品是否压过目标品牌，以及官网、内容和外部信源缺口在哪里。

它面向：

- 品牌负责人
- 增长负责人
- GEO 顾问
- 内容负责人

适合项目启动、季度复盘、竞品追赶和投放前评估。

## 核心能力

- 建立品牌实体档案：品牌名、别名、产品、服务、资质、客户、案例、价格、渠道和地域。
- 生成 AI 搜索问题样本：推荐、比较、替代、教程、价格、风险、真实性、购买决策和场景解决。
- 面向 DeepSeek、豆包、千问、Kimi、元宝做同题多轮采样。
- 诊断 AI 答案中的品牌出现、实体显著性、推荐位置、引用支持、竞品出现、事实错误、缺失信息和答案稳定性。
- 盘点官网、公众号、媒体、百科、社区、文档站和行业报告等信源。
- 按 8 个 GEO 特征评分：语义密度、结构规范性、可引用性、权威信号、可读性、鲁棒性、新颖性、跨域贡献。
- 输出快赢修复、内容补齐、页面重构、知识库补强、外部证据建设和监测闭环机会。

## 不负责什么

- 不负责单页结构诊断。
- 不负责直接写榜单、对比、科普文章或标题。
- 不负责 30/60/90 天执行路线图。
- 不负责后端归因字段、数据看板或转化追踪实现。

## 标准输出

- GEO 全景诊断报告。
- 方法依据与评分口径。
- 问题样本覆盖矩阵。
- AI 答案可见性与竞品对比表。
- GEO 机会地图与优先级矩阵。
- 页面与内容资产修复清单。
- 默认四格式交付：Word（`.docx`）、PDF（`.pdf`）、HTML（`.html` 或完整 HTML 包）、Markdown（`.md`）。
- 示例报告和正式报告都默认使用中文简体，字段、表头、状态值和模块名称也使用中文简体。
- 四种格式遵循 `kami` 的专业文档纪律，但使用白底背景；重点检查对齐、边框、分页、行距、长文本换行和内容溢出。
- 生成后必须先自 review，发现排版、字段英文化、格式缺失或内容不一致时，先修复再交付。

## 质量控制

这个 skill 的质量门集中在四件事：

- 不把 SEO 排名等同于 AI 推荐概率。
- 不把一次 AI 输出当成长期稳定结论。
- 不把品牌被提到等同于品牌被推荐。
- 不把引用数量等同于引用可信度；必须做断言级来源检查。
- 品牌事实、客户案例、数据、资质和价格必须有来源。
- 机会地图必须有资源约束和 P0/P1 优先级。

## 示例报告

### 岭序商机云合成示例

- [Markdown](../../skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/lingxu-panorama-audit.md)
- [HTML](../../skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/lingxu-panorama-audit.html)
- [Word](../../skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/lingxu-panorama-audit.docx)
- [PDF](../../skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/lingxu-panorama-audit.pdf)
- [自检记录](../../skills/yao-geo-panorama-audit/examples/lingxu-synthetic-panorama/review-notes.md)

### HubSpot 国内 AI 平台测试示例

- [Markdown](../../skills/yao-geo-panorama-audit/examples/hubspot-cn-panorama/hubspot-cn-panorama-audit.md)
- [HTML](../../skills/yao-geo-panorama-audit/examples/hubspot-cn-panorama/hubspot-cn-panorama-audit.html)
- [Word](../../skills/yao-geo-panorama-audit/examples/hubspot-cn-panorama/hubspot-cn-panorama-audit.docx)
- [PDF](../../skills/yao-geo-panorama-audit/examples/hubspot-cn-panorama/hubspot-cn-panorama-audit.pdf)
- [自检记录](../../skills/yao-geo-panorama-audit/examples/hubspot-cn-panorama/review-notes.md)

## Package Links

- Skill package: [skills/yao-geo-panorama-audit](../../skills/yao-geo-panorama-audit)
- Brief template: [templates/brief-template.md](../../skills/yao-geo-panorama-audit/templates/brief-template.md)
- Research foundation: [references/research-foundation.md](../../skills/yao-geo-panorama-audit/references/research-foundation.md)
- Method: [references/skill-method.md](../../skills/yao-geo-panorama-audit/references/skill-method.md)
- Platform sampling: [references/cn-platform-sampling.md](../../skills/yao-geo-panorama-audit/references/cn-platform-sampling.md)
- Quality model: [references/geo-quality-model.md](../../skills/yao-geo-panorama-audit/references/geo-quality-model.md)
