HubSpot 国内 AI 平台 GEO Signal Monitor 系统测试报告

中⽂简体测试样例。官⽅事实来⾃公开⽹⻚；国内 AI 平台结果为合成采样回放，不代表真实登录采样。

1. 执⾏摘要与关键判断

判断

监测⽬标

真实数据状态

结论

证据

下步动作

建⽴ AI 答案可⻅性、引⽤质量、事实准

五平台 Prompt、指标、来源账本、证据

进⼊周期性采样、证据⼊库和复盘。

确、纠偏和谨慎归因闭环。

等级和纠偏任务均已定义。

本次示例未接⼊ DeepSeek、⾖包、千

问、Kimi、元宝的真实 live 采样；所有
平台指标为合成回放，⽤于验证 skill 的

sample_mode =
synthetic_replay ，evidence_level
=  E0/E1 。

如需真实⽉报，先接⼊ M1-M4 的可审计

答案样本。

分析和排版能⼒。

当前⻛险

不能只看品牌出现率，必须同时看推荐、

出现率与推荐率、引⽤召回率存在差距。 建⽴阈值告警和 P0 纠偏机制。

引⽤、事实、稳定性和证据等级。

报告完整性

本报告按系统性、详细度、完整性三层⾃

覆盖来源、场景、Prompt、数据接⼊、

⽉报沿⽤同⼀结构。

检。

采样、六层分析、治理和附录。

2. 任务范围、边界和采样声明

项⽬

语⾔

平台

说明

中⽂简体

DeepSeek、⾖包、千问、Kimi、元宝

项⽬

采样声明

边界

真实数据要求

3. 权威参考与来源账本

类型

官⽅

source_id

H1

H2

H3

H4

说明

本次示例未接⼊ DeepSeek、⾖包、千问、Kimi、元宝的真实 live 采样；所有平台指
标为合成回放，⽤于验证 skill 的分析和排版能⼒。

不绕过登录、验证码、限流、付费或平台条款；归因默认从观察相关开始。

必须提供答案原⽂、Prompt、时间、平台、账号/地区/联⽹状态和截图、导出或接⼝

⽇志。

标题/事实

URL/来源

⽤途

置信度

HubSpot 官⽹

https://www.hubspot.co

产品线、平台定位

m/

官⽅⽂档

Breeze 知识库

https://knowledge.hubsp

AI 功能与计费边界

ot.com/ai/use-breeze?
lang=en

投资者关系

Q1 2026 results

https://ir.hubspot.com/n
ews-releases/news-

客户数、集成⽣态、官⽅
表述

release-details/hubspot-
reports-strong-q1-

2026-results

⾼

⾼

⾼

官⽅产品⻚

HubSpot AEO

https://www.hubspot.co

AEO / AI visibility 场景

⾼

m/products/aeo

4. 公司/品牌事实基线

事实

官⽅来源或核验⽅式

⻛险

HubSpot 定位为 agentic customer platform，包含

https://www.hubspot.com/

国内答案可能只写成免费 CRM。

Smart CRM 和多个 Hub。

Breeze 是 AI 能⼒集合，部分功能涉及 credits、seat

https://knowledge.hubspot.com/ai/use-breeze?

容易被误写成完全免费 AI。

或订阅边界。

lang=en

截⾄ 2026 年 3 ⽉ 31 ⽇，HubSpot Q1 2026 官⽅披露

HubSpot IR Q1 2026 results

动态数字容易被旧资料覆盖。

客户数为 299,458，并有 2,000+ App Marketplace
integrations。

HubSpot AEO ⽤于观察品牌在 answer engines 中如何
出现。

5. 公司测试场景发现

https://www.hubspot.com/products/aeo

国内答案可能只谈 SEO，不谈 AEO/GEO。

场景

HS-01

HS-02

HS-03

HS-04

HS-05

业务含义

对应 Prompt 组

⻛险

正确答案应覆盖

出海 B2B 选择 CRM 与客户平

推荐、⽐较

只推荐国内 CRM

Smart CRM、

台

营销⾃动化与线索培育

推荐、场景问法

简化为邮件群发

Marketing/Sales/Service
Hub、集成⽣态

表单、落地⻚、⾃动化、CRM
数据闭环

Breeze AI 与计费边界

价格、品牌验证

写成完全免费

credits、seat、订阅边界

AEO 与 AI 搜索可⻅性

推荐、品牌验证

只谈 SEO

AEO、AI visibility、监测闭环

产品命名和动态事实更新

⻛险、品牌验证

复述旧名称或旧客户数

Content Hub、Data Hub、
299,458 客户数的⽇期边界

6. 监测 Prompt 库与对照组

组别

推荐

⽐较

替代

价格

⻛险

品牌验证

场景问法

核⼼ Prompt

对照 Prompt

观测重点

适合HubSpot⽬标⽤户的⽅案有哪些？

不含品牌名的同类推荐

候选率、推荐率、排序。

HubSpot 与主要竞品怎么选？

调换品牌顺序

排序、优劣描述、引⽤源。

竞品有哪些替代⽅案？

只问竞品

品牌是否被召回。

HubSpot 价格、套餐或成本如何？

只问贵不贵

价格事实、适⽤边界。

HubSpot 有什么限制或⻛险？

⾏业通⽤⻛险问法

负⾯表述、误解来源。

HubSpot 是什么？有哪些产品/能⼒？

只问品牌是否正规

事实准确率、引⽤质量。

具体业务场景如何选择⼯具？

不含品牌名场景问法

场景召回、推荐理由。

7. 真实数据接⼊模式与证据等级

模式

M0 合成回放

当前状态

已⽤于本示例

M1 ⽤户提供真实样本

可接⼊

M2 ⼈⼯授权采样

M3 授权 API/连接器

M4 浏览器辅助合规采样

可接⼊

条件可⽤

条件可⽤

进⼊正式指标条件

报告措辞

仅⽤于流程验证，不进⼊真实⽉报指标

⽅法演示，不代表真实平台表现。

答案⽂本 + Prompt + 采样环境 + 截图/
导出

可作为客户样本分析。

⼈⼯采样记录 + 频率边界 + 复核⼈

可作为⼩规模真实样本。

API 权限、接⼝⽇志、频率、失败重试

可进⼊看板趋势。

⼈⼯授权登录、⽆绕过、截图和采样⽇志 可⽤于复核和截图证据。

M5 CRM/转化数据导⼊

可接⼊⽤户授权数据

脱敏、字段⼝径、时间窗⼝、拥有⽅授权 只能辅助归因，不能替代 AI 答案样本。

证据等级

条件

当前样例状态

E0

E1

E2

E3

E4

8. 五平台采样⼜径

⽆原始答案和环境字段

不作为真实平台数据。

有答案⽂本但缺少截图或完整环境

可作为线索。

有答案⽂本、Prompt、平台、时间、地区、联⽹状态

可作为单次真实样本。

E2 + 截图、导出⽂件、引⽤链接或接⼝⽇志

可审计真实样本。

E3 + 多轮复采、对照 Prompt、复核⼈和去重记录

可进⼊⽉报统计。

平台

重点

样本量建议

必填环境字段

质检重点

DeepSeek

结论稳定性、证据链、联⽹状态 40+

时间、设备、地区、联⽹、

多次答案是否⼀致。

sample_mode

⾖包

千问

Kimi

元宝

9. 核⼼指标总览

指标

品牌出现率

⼝语问答、图⽂输出、短答案

40+

设备、账号、地区、联⽹、截图 是否省略来源或过度简化。

引⽤源、追问路径、⽣态信源

40+

轮次、追问、联⽹、引⽤链接

引⽤是否⽀持说法。

深度研究、⻓⽂引⽤、⽂档站

40+

⻓⽂模式、联⽹、引⽤段落

引⽤召回和事实更新。

微信⽣态、公众号、视频号

40+

账号、地区、⽣态来源、可访问
路径

⼆⼿中⽂来源是否可靠。

合成结果

88%

解释

CRM/营销⾃动化问题中品牌认知⾼。

指标

候选率

推荐率

平均排序

描述准确率

引⽤召回率

引⽤准确率

负⾯表述率

10. 平台差异分析

平台

DeepSeek

⾖包

千问

Kimi

元宝

合成结果

解释

74%

57%

2.4

81%

52%

76%

9%

差异

多数平台会把 HubSpot 放⼊候选，但场景差异⼤。

推荐低于候选，说明需要更强中⽂场景证据。

常与 Salesforce、Zoho、国产 CRM 同列。

产品命名、客户数、Breeze 计费边界存在⻛险。

关键事实仍常⽆引⽤。

官⽅来源⽀持度较好，但⼆⼿中⽂资料会稀释。

价格、本地化、实施成本是主要负⾯。

动作

结构化⽐较好，但引⽤链弱

强化官⽅来源账本。

短答案容易简化品牌定位

增加短事实卡。

引⽤表现较好，追问后竞品增多

保留追问链路和 turn_index。

⻓⽂能覆盖研究和⽂档站

检查旧数字和⻓引⽤⽀持度。

中⽂⽣态召回强

防⽌公众号⼆⼿内容替代官⽅来源。

11. 引⽤源追踪与证据质量

来源类型

官⽅⽹站/⽂档

官⽅中⽂资料

投资者/公告/标准

媒体/评测/社区

竞品⻚⾯

12. 答案事实性与描述准确率

⽀持等级

判断规则

纠偏动作

A

A/B

A

B/C

C

直接⽀持答案事实

优先作为事实卡和纠偏锚点。

中⽂可读且⽀持说法

⽤于国内平台引⽤优化。

⽀持动态数字或治理要求

写绝对⽇期，避免旧数据。

可辅助⽐较但不⼀定⽀持事实

仅作辅助，不作主事实。

⽤于对照，不验证本品牌事实

标注为竞品来源。

事实类型

产品/能⼒

价格/套餐

客户/案例

市场/适配

典型错误

核验⽅法

优先级

⽤旧名称、少列产品、夸⼤ AI 能⼒

对照官⽹和官⽅⽂档

把付费能⼒写成免费

对照定价、知识库和公告

使⽤旧数字或未授权案例

对照官⽅公告和案例⻚

过度绝对化国内或海外适⽤性

对照场景和竞品

P0

P0

P1

P1

13. 竞品、替代和负⾯表述分析

维度

竞品出现

替代关系

监测点

⻛险

输出

竞品频率、排序、推荐理由

品牌被替代或弱推荐

竞品矩阵。

国产替代、海外替代、传统⽅案

不同场景混在⼀起

场景化替代表。

维度

负⾯表述

监测点

⻛险

输出

价格、本地化、数据、实施成本

被⼆⼿内容放⼤

⻛险澄清⻚。

14. 稳定性、波动和置信度

置信度

⾼

中

低

15. 答案差异与谨慎归因

⼲预

内容发布

⻚⾯修复

外部信源

CRM/转化

基线窗⼝

T-14 ⾄ T0

T-14 ⾄ T0

T-30 ⾄ T0

T-30 ⾄ T0

条件

报告措辞

多平台、多轮次、⼀致引⽤、E3+ 证据和对照⽀持

可作为稳定判断。

有样本和引⽤，但平台间有差异或证据等级不⾜

作为⽅向判断。

只有单次样本、合成回放或缺少引⽤

仅作为观察线索。

观察窗⼝

对照

归因规则

T+7/T+14/T+30

不相关 Prompt / 竞品 Prompt

默认观察相关。

T+7/T+14

T+14/T+30

T+30/T+60

未修复⻚⾯组

有对照改善才升置信。

未发布主题

检查索引延迟和外部事件。

⾮ GEO ⼊⼝或未曝光组

只能辅助解释，不能替代 AI 答
案采样。

16. 纠偏任务与路线图

优先级

问题

映射资产

验收指标

P0

P0

P1

P1

客户数量被复述为旧数据

中⽂事实卡 + IR 引⽤

最新客户数错误率低于 5%

Breeze AI 被误写为完全免费

Breeze AI 中⽂说明⻚

AI 计费边界准确率⾼于 90%

HubSpot 被简化为免费 CRM

Customer platform 中⽂⻚

customer platform 表述提升 20pp

AEO 场景缺少中⽂证据

AEO/AI visibility 中⽂解释⻚

AEO 问法候选率⾼于 60%

17. 告警规则和复盘节奏

告警

事实错误

引⽤不⾜

证据等级不⾜

推荐下降

负⾯上升

阈值

处理

P0 错误连续两轮出现或描述准确率低于 80%

建 P0 纠偏，14 天内复采。

引⽤召回率低于 50%

补官⽅证据⻚和中⽂承接⻚。

正式样本低于 E2 或截图/导出缺失

降级为待复核，不进⼊正式指标。

推荐率环⽐下降超过 10pp

检查平台更新、竞品动作和 Prompt 分布。

负⾯表述率⾼于 18%

建⻛险澄清⻚和销售⼝径。

18. 仪表盘字段、数据库表和 API 草案

表/接⼝

字段或路径

⽤途

monitor_prompts

scenario_id、group、query_text、control_flag、

管理 Prompt 和对照组。

prompt_version

表/接⼝

answer_samples

字段或路径

sample_mode、evidence_level、platform、
sampled_at、region、network_enabled、

answer_text

⽤途

保存采样答案。

sample_evidence

raw_answer_path、screenshot_path、api_log_id、

保存真实数据证据。

collector、permission_basis

citations

source_type、source_url、claim_text、

追踪引⽤质量。

support_level

correction_tasks

priority、mapped_asset、owner、

管理纠偏闭环。

acceptance_metric

API

GET /api/geo-monitor/monthly-report

拉取⽉报聚合。

19. 治理、合规、数据质量和风险控制

⻛险

平台条款

数据隐私

数据质量

⽣成式 AI ⻛险

真实数据误⽤

控制

不绕过登录、验证码、付费和限流；批量采样需授权。

CRM、转化、账号、截图和接⼝⽇志脱敏；示例只⽤合成数据。

记录采样环境、来源账本、复核⼈、证据等级和置信度。

标注幻觉、过时事实、引⽤不⽀持和过度归因。

没有可审计样本时，报告必须标注为合成或待复核。

20. ⾃ review 结果

检查项

系统性

详细度

完整性

HTML 菜单

横向溢出

Pandoc 默认 CSS

kami UI

结果

通过

通过

通过

通过

通过

通过

通过

21. 附录：Prompt 全表、指标字典、来源账本、采样字段

附录

Prompt 全表

指标字典

来源账本

采样字段

说明

覆盖来源、场景、Prompt、数据接⼊、采样、指标、引

⽤、归因、纠偏、治理和附录。

每个模块有字段、阈值、动作、证据等级或验收标准。

结论可回到 Prompt、样本、来源、证据和纠偏任务。

浏览器检查确认桌⾯端 fixed 菜单、移动端 sticky 菜

单。

桌⾯ 1440px 与移动 390px 视⼝均⽆横向溢出。

HTML ⽣成时禁⽤默认⽂档 CSS，并显式覆盖 body 窄
栏约束。

⽩底优先，采⽤油墨蓝、暖灰、紧凑层级、稳定表格边
框。

内容

七组 Prompt、对照 Prompt、场景 ID、版本。

出现率、候选率、推荐率、排序、描述准确、引⽤召回、引⽤准确、稳定性。

source_id、source_type、url、fact_supported、freshness_risk、confidence。

sample_mode、evidence_level、platform、sampled_at、device、
account_state、region、network_enabled、turn_index。

附录

真实数据证据

内容

raw_answer_path、screenshot_path、api_log_id、collector、
permission_basis、review_status。

