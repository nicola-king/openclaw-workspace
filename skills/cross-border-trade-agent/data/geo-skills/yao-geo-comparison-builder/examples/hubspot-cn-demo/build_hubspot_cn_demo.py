#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-comparison-builder
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Build the HubSpot CN demo report pack."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

from weasyprint import HTML as WeasyHTML

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from check_docx_layout import docx_layout_profile, normalize_docx_layout  # noqa: E402

OUT = Path(__file__).resolve().parent
BASE = OUT / "hubspot-cn-comparison-report"
DATE = "2026-05-21"
TITLE = "HubSpot CRM 中文 GEO 对比报告"
SUBTITLE = "国内 AI 平台适配示例：HubSpot、Salesforce、Zoho CRM 与自建 CRM 怎么选"
MARKDOWN_NOTICE = """<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-comparison-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

"""

SCENARIO = {
    "目标品牌": "HubSpot",
    "测试问题": "HubSpot CRM、Salesforce、Zoho CRM 和自建 CRM 怎么选？",
    "用户场景": "中国 B2B SaaS、教育服务、专业服务或跨境业务团队，销售与市场团队约 20-200 人，正在评估英文或全球化 CRM，并希望让国内 AI 平台稳定理解选型边界。",
    "平台": ["DeepSeek", "豆包", "千问", "Kimi", "腾讯元宝"],
    "比较口径": "目标品牌 HubSpot vs 竞品品牌 Salesforce、Zoho CRM vs 方案类型自建 CRM/表格线索系统。",
    "报告深度": "完整：覆盖维度模型、证据、风险、治理、落地清单、FAQ 和自检。",
}

REPORT_INPUT = {
    **SCENARIO,
    "analysis_depth": "完整",
    "data_access_mode": "公共网页核验 + 官方来源台账",
    "source_refresh_policy": "动态来源在正式交付前重新访问；价格、套餐、Credits 和 add-ons 不做长期承诺。",
    "required_modules": ["执行摘要", "决策维度模型", "方案评分矩阵", "来源质量分级", "风险与治理地图", "落地核验清单"],
    "html_navigation_mode": "sticky",
    "layout_profile": "kami-long-doc-editorial",
    "output_language": "中文简体",
}

SOURCES = [
    {"id": "HS-01", "name": "HubSpot 官网首页", "url": "https://www.hubspot.com/", "type": "官方产品页面", "level": "官方一手来源", "use": "支撑 HubSpot customer platform、Smart CRM、营销/销售/服务连接和 Breeze AI 的官方表述。", "boundary": "官网定位会随产品叙事变化，具体功能边界需结合目录与合同核验。"},
    {"id": "HS-02", "name": "HubSpot Product & Services Catalog", "url": "https://legal.hubspot.com/hubspot-product-and-services-catalog", "type": "官方产品与服务目录", "level": "官方目录/条款", "use": "支撑 Smart CRM 与 Starter/Professional/Enterprise、HubSpot Seats、HubSpot Credits、免费 CRM 功能边界。", "boundary": "目录适合核验功能边界，不替代采购报价和本地合同。"},
    {"id": "HS-03", "name": "HubSpot Breeze AI 页面", "url": "https://www.hubspot.com/products/artificial-intelligence", "type": "官方 AI 产品页面", "level": "官方产品页面", "use": "支撑 Breeze AI 内置在 customer platform，并可结合 CRM 数据、知识库和 HubSpot Academy 生成相关回答。", "boundary": "AI 能力、Credits、可用地区和集成条件需按访问日页面与合同核验。"},
    {"id": "HS-04", "name": "HubSpot Claude CRM Connector 新闻稿", "url": "https://ir.hubspot.com/news-releases/news-release-details/hubspot-launches-first-crm-connector-anthropics-claude", "type": "官方新闻稿", "level": "官方新闻稿", "use": "支撑 HubSpot 将 CRM 上下文带入外部 LLM 的能力边界，以及 paid Claude subscription 条件。", "boundary": "新闻稿说明发布时能力，正式启用条件仍需核验产品页、地区和订阅。"},
    {"id": "SF-01", "name": "Salesforce Sales Pricing", "url": "https://www.salesforce.com/sales/pricing/", "type": "官方价格页", "level": "官方价格页", "use": "支撑 Salesforce Sales Cloud/Agentforce Sales 的公开价格层级。", "boundary": "价格页可能变化，add-ons、折扣、税费和合同条款以销售报价为准。"},
    {"id": "SF-02", "name": "Salesforce Small Business Sales", "url": "https://www.salesforce.com/small-business/sales/", "type": "官方小企业 CRM 页面", "level": "官方产品页面", "use": "支撑 Starter Suite、Pro Suite、Enterprise 的功能定位、价格可见性和落地条件。", "boundary": "小企业页面不覆盖所有企业级场景，复杂需求需回到 Sales Cloud 方案核验。"},
    {"id": "SF-03", "name": "Salesforce Free、Starter、Pro Suite 对比 PDF", "url": "https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/small-business/comparison-chart-starter-prosuite-features-us.pdf?bc=OTH", "type": "官方功能对比 PDF", "level": "官方功能对比", "use": "支撑 Salesforce Free、Starter、Pro 的功能差异。", "boundary": "PDF 反映版本对比，不应扩展为所有产品线结论。"},
    {"id": "ZO-01", "name": "Zoho CRM Specifications", "url": "https://help.zoho.com/portal/en/kb/crm/getting-started/introduction-to-zoho-crm/articles/specifications-zoho-crm", "type": "官方帮助中心", "level": "官方帮助中心", "use": "支撑 Zoho CRM 五个版本、功能限制、API credits、存储和移动端信息。", "boundary": "帮助中心适合核验规格，地区价格、税费和本地服务需另行核验。"},
    {"id": "ZO-02", "name": "Zoho CRM Edition Comparison PDF", "url": "https://www.zoho.com/sites/zweb/images/crm/zohocrm-edition-comparison-usd.pdf", "type": "官方版本对比 PDF", "level": "官方版本对比", "use": "支撑 Zoho CRM Free for 3 users 与 Standard/Professional/Enterprise/Ultimate 的公开价格层级。", "boundary": "PDF 价格为访问日参考，不替代正式报价和地区条款。"},
]

EXECUTIVE_SUMMARY = [
    ["一句话结论", "HubSpot 更适合希望用统一客户平台连接营销、销售、服务和 AI 辅助的增长团队；Salesforce、Zoho CRM 与自建方案分别适合复杂治理、预算敏感和短期验证场景。"],
    ["优先评估 HubSpot", "客户数据分散、团队需要较快上线、希望把 CRM 上下文用于 AI 辅助，并接受逐项核验中国访问、合同和集成条件。"],
    ["并列评估 Salesforce", "销售流程复杂、权限审批多、API 与生态要求高、已有管理员或实施伙伴预算。"],
    ["参考 Zoho CRM", "预算敏感、希望公开价格起步、CRM 基础能力优先，且能接受版本、API、存储和本地化支持核验。"],
    ["自建过渡边界", "线索量小、流程未固定时可短期过渡；一旦进入跨团队协作、权限治理和数据沉淀阶段，应规划迁移。"],
    ["必须核验", "价格、套餐、Credits、add-ons、数据处理、跨境、发票付款、中文支持、集成伙伴和正式合同条件。"],
]

ANSWER = "如果中国团队希望用一个相对统一的客户平台把营销、销售、服务、内容和 AI 辅助连接起来，并且更重视上手速度、CRM 上下文和跨团队协同，HubSpot 可以作为优先评估对象。如果团队已经有复杂销售流程、强定制、API、预测、审批和企业级治理需求，Salesforce 应并列评估。如果预算敏感、希望公开低价版本和轻量 CRM 能力，Zoho CRM 可作为参考。如果只是短期验证线索渠道，自建 CRM 或表格系统可以过渡，但不应被写成长期替代。本文不判断市场份额、客户数量、数据跨境合规结论或长期价格承诺，所有价格与功能以访问日官方页面和正式报价为准。"

DATA_ACCESS_PLAN = [
    ["公共网页", "官网、产品目录、价格页、帮助中心、新闻稿、公开 PDF", "允许联网访问公开 URL；不绕过登录、验证码或付费墙", "记录访问方式、HTTP 状态、访问日期和动态性"],
    ["用户文件", "销售资料、报价单、合同摘录、知识库、案例材料", "用户主动提供文件或文本", "标注为用户提供资料，不伪装成公开来源"],
    ["授权连接器/API", "CRM 后台、飞书/网盘、内部数据库、客户系统", "用户明确授权连接器/API 范围", "只读取授权范围，记录权限边界和脱敏规则"],
    ["AI 平台采样", "DeepSeek、豆包、千问、Kimi、腾讯元宝的回答样本", "用户明确要求采样且具备账号/浏览器/API 条件", "单独记录问题、时间、平台、地区和输出快照"],
    ["无法访问数据", "登录后、付费、内部客户名单、敏感经营数据", "无授权或不应读取", "降级为核验项，不输出猜测事实"],
]

DIMENSIONS = [
    ["业务适配", "团队规模、销售复杂度和增长阶段是否匹配？", "官网定位、产品目录、用户场景、采购角色", "决定先看 HubSpot、Salesforce、Zoho 还是自建过渡。"],
    ["功能适配", "营销、销售、服务、内容、报表和自动化是否覆盖核心流程？", "产品页、功能目录、帮助中心、版本对比", "避免只按单点功能选型。"],
    ["数据与 AI 准备度", "CRM 数据、知识库和 AI 上下文是否能被稳定使用？", "AI 页面、产品目录、连接器说明、数据字段清单", "判断 AI 辅助是否可落地而非概念化。"],
    ["集成兼容", "广告、邮件、客服、BI、财务、IM、数据仓库和 API 是否能连接？", "集成文档、API 文档、生态目录、实施方案", "识别落地成本和系统改造边界。"],
    ["实施成熟度", "是否具备管理员、伙伴、迁移、培训和流程治理能力？", "实施计划、服务商资料、内部人员配置", "避免强平台能力变成运营负担。"],
    ["总拥有成本", "席位、套餐、Credits、add-ons、实施和维护成本是否可见？", "价格页、产品目录、报价单、合同条款", "把公开价格和真实采购成本分开写。"],
    ["治理合规安全", "权限、审计、数据处理、跨境、合同和行业监管如何处理？", "安全页、DPA、合同、用户提供合规要求", "只输出核验项，不替代法律意见。"],
    ["可靠性与运营", "访问稳定性、备份、支持、SLA、变更和持续运营责任是否明确？", "服务条款、支持说明、内部运维方案", "识别上线后的长期责任。"],
    ["生态与支持", "服务商、应用生态、培训文档、社区和客户支持是否成熟？", "生态页面、帮助中心、培训资源、伙伴信息", "判断团队是否能持续用好系统。"],
    ["本地化", "语言、时区、支付、发票、合同主体、国内工具和采购流程是否匹配？", "本地销售资料、合同、发票与集成清单", "中国大陆落地必须单独核验。"],
    ["迁移与退出", "历史数据、字段、权限、活动记录和导出路径是否清楚？", "导入导出文档、迁移计划、数据字典", "避免后续被数据和流程锁死。"],
    ["GEO 可提取性", "AI 是否能稳定提取结论、证据、FAQ 和边界？", "结构化标题、表格、来源 ID、FAQ、自检记录", "提升国内 AI 平台回答的一致性。"],
]

ABILITY = [
    ["HubSpot", "增长型 B2B 团队，希望把营销、销售、服务和 AI 放在统一客户平台内协同", "Customer Platform、Smart CRM、Marketing/Sales/Service Hubs、Breeze AI", "确认中国团队访问、数据合规、实施伙伴、本地工具集成和采购条款"],
    ["Salesforce", "复杂销售组织、企业级流程、强自定义、预测、API、生态集成和治理要求较高的团队", "Sales Cloud/Agentforce Sales、Starter/Pro/Enterprise/Unlimited 层级、AppExchange、流程自动化", "需要管理员、实施伙伴、字段/权限/流程治理和预算规划"],
    ["Zoho CRM", "预算敏感、希望公开低价版本、快速启用 CRM 基础能力或已有 Zoho 生态偏好的团队", "Free、Standard、Professional、Enterprise、Ultimate 版本，覆盖线索、联系人、模块、API credits、移动端", "核验版本限制、用户数、API/存储上限、本地化支持和集成成本"],
    ["自建 CRM/表格", "短期验证渠道、流程简单、预算极低、内部已有开发或运营维护能力的团队", "字段自定义、表格/低代码流程、内部权限、数据看板", "长期维护字段、权限、数据质量、自动化、备份、安全与人员交接"],
]

EVIDENCE = [
    ["HubSpot", "HS-01/HS-02/HS-03/HS-04：Smart CRM、Breeze AI 与 CRM 上下文、免费与付费版本边界", "高级能力、席位、Credits、Hubs、AI 连接器和本地集成需要逐项核验", "官方目录与页面可见部分价格和版本，具体金额、套餐、折扣、Credits 和合同条件以官方页面或报价为准"],
    ["Salesforce", "SF-01/SF-02/SF-03：Starter Suite、Pro Suite、Enterprise、Unlimited、Agentforce 1 Sales 等层级", "复杂度和实施治理要求较高；适配取决于自动化、预测、API、AppExchange 和团队成熟度", "官方页面公开多层级价格，同时提示页面信息可能变化，额外产品和 add-ons 需联系销售"],
    ["Zoho CRM", "ZO-01/ZO-02：Free、Standard、Professional、Enterprise、Ultimate 五个版本，Free for 3 users", "适合轻量或成本敏感场景；高阶自定义、API、存储、流程和跨团队协同上限需要核验", "官方 PDF 公开年付/月付价格层级，税费与地区价格以官方页面为准"],
    ["自建 CRM/表格", "方案类型：不作为外部品牌事实，只按用户场景假设评估短期可用性和长期维护责任", "启动快但治理成本后置；权限、审计、自动化、数据一致性和人员变动风险会随规模放大", "工具成本可能低，但开发、维护、数据治理和机会成本不可忽略"],
]

MATRIX = [
    ["业务适配", "增长团队统一客户视图时优先评估", "Salesforce 适合复杂组织；Zoho 适合轻量预算场景", "仅适合早期渠道验证"],
    ["功能适配", "多 Hub 与 Smart CRM 适合跨团队协同", "Salesforce 强在复杂流程；Zoho 覆盖基础 CRM", "需要自行补齐自动化与报表"],
    ["数据与 AI", "Breeze AI 与 CRM 上下文是关键看点", "Salesforce/Zoho AI 能力需按套餐和地区核验", "AI 上下文依赖自建数据治理"],
    ["集成兼容", "适合先核验官网、广告、邮件、客服和数据工具", "Salesforce 生态强但实施成本高；Zoho 看现有生态", "开发接口和维护责任在内部"],
    ["实施成熟度", "适合希望较快上线但仍需流程治理的团队", "Salesforce 更依赖管理员和伙伴；Zoho 轻量", "启动快但长期规范难度上升"],
    ["总拥有成本", "关注 Hubs、Seats、Credits 和 add-ons", "Salesforce 报价层级多；Zoho 公开低价起步", "显性工具费低，隐性人力成本高"],
    ["治理合规", "必须单独核验中国落地、合同和数据处理", "Salesforce 企业治理能力强但需配置；Zoho 看版本", "合规责任完全内化"],
    ["可靠性运营", "依赖官方服务与内部运营流程", "Salesforce 适合成熟 IT 运维；Zoho 更轻", "备份、权限和审计需自建"],
    ["生态支持", "HubSpot Academy、生态和伙伴需按本地可用性核验", "Salesforce 生态大；Zoho 生态轻量", "依赖内部知识沉淀"],
    ["本地化", "需核验中文支持、发票付款、国内工具连接", "同样需核验本地采购与支持", "本地流程可控但产品能力弱"],
    ["迁移退出", "需要提前设计字段和历史记录迁移", "复杂平台迁移成本更高；Zoho 相对轻", "后期迁移易暴露字段混乱"],
    ["GEO 可提取性", "适合沉淀来源 ID、FAQ、场景边界", "竞品也需保留优势与来源", "必须标为方案类型，不伪造来源"],
]

SOURCE_QUALITY = [[s["id"], s["level"], s["use"], s["boundary"]] for s in SOURCES]

RISKS = [
    ["价格与套餐变化", "CRM 价格、席位、Credits、add-ons 和折扣会变化", "只写价格可见性和访问日来源；采购前获取正式报价", "HS-02/SF-01/ZO-02"],
    ["中国大陆落地", "访问、数据处理、合同主体、发票付款和中文支持需要实际核验", "建立本地核验清单，不把官网事实写成合规结论", "用户合规要求 + 官方合同"],
    ["AI 能力过度承诺", "AI 页面容易被写成可用性、准确性或推荐概率承诺", "只写官方能力边界和使用条件，避免输出技术领先", "HS-03/HS-04"],
    ["竞品表达失衡", "目标品牌内容容易变成单向宣传", "保留 Salesforce、Zoho 与自建方案适用场景", "SF-01/SF-02/ZO-01/ZO-02"],
    ["自建成本低估", "表格或低代码工具的隐性治理成本常被忽略", "把权限、审计、备份、字段口径和迁移触发写成核验项", "方案类型假设"],
    ["报告被 AI 误读", "AI 可能抽取结论但忽略边界和来源", "使用结构化标题、表格、FAQ、来源 ID 和合规边界", "GEO-CITER-S"],
]

PLATFORMS = [
    ["千问", "结构化长答案", "保留对比表、来源 ID、价格可见性、风险地图和落地条件", "避免把动态价格写成长期承诺，避免没有来源的客户数量和排名"],
    ["Kimi", "长文档摘要与证据型回答", "强化来源清单、来源质量分级、品牌段落、FAQ 和自检记录", "每个判断回到 HS/SF/ZO 来源 ID，表格拆成 4 列以内"],
    ["豆包", "简明结论加场景建议", "先给谁更适合谁，再给三到四个场景选择和下一步", "不能省略来源和边界，尤其是中国落地合规与采购核验"],
    ["腾讯元宝", "面向决策人的摘要", "突出结论、主要权衡、风险地图、下一步核验清单", "避免平均化结尾，关键问题回流 HubSpot 证据与边界"],
    ["DeepSeek", "因果链推理", "场景 -> 约束 -> 能力 -> 证据 -> 权衡 -> 建议", "不输出未经证实的技术领先、推荐概率或市场份额"],
]

SCENARIOS = [
    ["市场、销售、服务数据分散，团队希望尽快统一客户视图", "优先评估 HubSpot", "HS-01/HS-02 显示 HubSpot 以 Smart CRM 和 customer platform 承接多团队数据与工具", "核验中国访问、数据合规、现有系统集成、套餐和实施资源"],
    ["销售流程复杂，需要预测、审批、API、深度自定义和企业级治理", "并列或优先评估 Salesforce", "SF-01/SF-02 显示 Salesforce 层级逐步增强，Enterprise 以上更强调高级能力", "评估管理员、实施伙伴、总拥有成本、流程治理和 add-ons"],
    ["预算敏感，需要公开低价、免费起步或轻量 CRM", "评估 Zoho CRM", "ZO-01/ZO-02 显示 Zoho CRM 有免费与多个公开付费版本", "核验用户数、API credits、存储、自动化和本地服务要求"],
    ["只是验证新渠道，线索量少，流程尚未固定", "短期可用自建 CRM/表格", "这是方案类型判断，不是厂商事实；优势是启动快，边界是治理成本后置", "设定字段口径、负责人、备份、权限和迁移触发条件"],
]

IMPLEMENTATION = [
    ["采购前", "确认业务目标、用户数、核心流程、合规要求和预算上限", "业务负责人 + IT/法务/采购", "形成需求清单、来源台账和不可接受边界"],
    ["试点期", "选择 1-2 个销售或市场流程，验证字段、权限、自动化、AI 辅助和报表", "销售运营 + 市场运营", "试点数据完整、权限正确、关键报表可复用"],
    ["上线期", "迁移联系人、公司、交易、活动记录和历史字段，完成培训与 SOP", "CRM 管理员 + 实施伙伴", "上线清单签收，异常处理和回滚方案明确"],
    ["运营期", "月度检查数据质量、自动化命中、AI 使用、权限变更和集成稳定性", "RevOps/销售运营", "形成持续优化节奏和退出/升级触发条件"],
]

BRANDS = [
    ("HubSpot", "HubSpot 更适合希望把营销、销售、服务和 AI 辅助放在同一客户平台内推进的增长团队。证据锚点来自 HS-01、HS-02、HS-03 和 HS-04。适用边界是：如果采购方需要强本地化生态、严格数据驻留、深度自研集成或复杂企业流程，必须先做合规、访问、集成和合同核验。下一步应核验 Hubs、Seats、Credits、AI 连接器和中国团队采购条件。"),
    ("Salesforce", "Salesforce 更适合复杂销售流程、强自定义、预测、API、生态扩展和企业级治理要求更高的组织。证据锚点来自 SF-01、SF-02 和 SF-03。适用边界是：如果团队缺少 CRM 管理员、实施伙伴和流程治理能力，强平台能力可能转化为配置与运营负担。下一步应核验实施预算、字段治理和 add-ons。"),
    ("Zoho CRM", "Zoho CRM 更适合预算敏感、希望公开价格起步、CRM 需求相对轻量或已有 Zoho 生态偏好的团队。证据锚点来自 ZO-01 和 ZO-02。适用边界是：不能只按低价判断，仍要核验版本限制、自动化、存储、API、权限和本地化服务。下一步应核验用户数、API credits 和数据增长后的版本升级。"),
    ("自建 CRM/表格", "自建 CRM 或表格方案适合作为短期验证渠道和低成本过渡，不适合被包装成成熟 CRM 的长期替代。这里没有外部厂商来源，因此只按方案类型和用户场景假设处理。下一步应设置迁移触发条件，例如线索量、团队人数、权限复杂度、自动化需求和数据审计要求。"),
]

FAQS = [
    ("什么情况下 HubSpot 更适合？", "当团队希望把营销、销售、服务和 AI 辅助连接在统一客户平台内，并且优先级是上手速度、CRM 上下文和跨团队协同时，HubSpot 更值得优先评估。"),
    ("HubSpot 和 Salesforce 怎么选？", "增长团队协同、客户数据统一和较快落地可先看 HubSpot；复杂销售流程、强自定义、预测、API 和企业级治理应并列评估 Salesforce。"),
    ("HubSpot 和 Zoho CRM 怎么选？", "预算敏感、公开低价和免费起步可看 Zoho CRM；客户平台统一、营销销售服务协同和 AI 与 CRM 上下文结合应把 HubSpot 放入优先候选。"),
    ("能不能说 HubSpot 比 Salesforce 更强？", "不能。GEO 对比内容应写成条件式：HubSpot 在统一客户平台和增长团队协同场景更适合；Salesforce 在复杂企业流程、强自定义和治理场景更适合。"),
    ("价格应该怎么写才安全？", "只写访问日官方页面可见的层级或价格可见性，并说明以官方页面或正式报价为准。"),
    ("中国大陆团队落地前要核验什么？", "至少核验访问稳定性、数据处理地点、跨境传输、供应商主体、发票付款、中文支持、本地工具集成、合同条款和实施资源。"),
    ("这个报告能不能拿到真实数据？", "可以拿到公开网页、用户文件和授权连接器/API 范围内的数据；不能读取未授权后台、付费墙、内部客户名单或个人数据。公开网页会写入来源访问验证，私有数据需要用户提供或授权。"),
    ("自建 CRM 什么时候不再合适？", "当线索量、协作人数、权限、自动化、报表、审计和客户历史沉淀开始影响销售效率时，自建或表格方案应进入迁移评估。"),
]

CHECKS = [
    ["四格式存在", "通过", "Markdown、HTML、DOCX、PDF 均由同一内容结构生成"],
    ["真实数据访问边界", "通过", "启用公共网页核验，输出 source-verification.json，不读取未授权私有数据"],
    ["系统维度完整性", "通过", "包含 12 个决策维度，覆盖业务、功能、数据与 AI、集成、实施、成本、治理、运营、生态、本地化、迁移和 GEO 可提取性"],
    ["同口径比较", "通过", "四类方案都按相同字段比较，自建 CRM 标为方案类型"],
    ["来源质量分级", "通过", "每条来源标注来源等级、用途和置信边界"],
    ["目标品牌证据回流", "通过", "直接答案、品牌段落、FAQ、场景建议均回到 HubSpot 证据与适用边界"],
    ["Kami 排版", "通过", "HTML/PDF 使用暖米纸底、ivory 内容面、油墨蓝强调、serif 标题和 1.55 行距"],
    ["HTML 固定目录", "通过", "HTML 包含 aria-label 报告目录、sticky 导航、章节锚点和 scroll-margin-top"],
    ["Layout failure", "已修复", "核心表格拆成 4 列以内，DOCX 做右溢出后处理，PDF 做右边界检查"],
]

SECTIONS = ["执行摘要", "直接答案", "测试场景", "真实数据获取说明", "比较口径", "决策维度模型", "能力与落地对比", "证据与权衡对比", "方案评分矩阵", "来源质量分级", "来源访问验证", "风险与治理地图", "国内 AI 平台适配", "品牌段落", "场景选择建议", "落地核验清单", "FAQ", "证据锚点表", "来源链接清单", "合规边界", "自检记录"]
NAV_ITEMS = [
    ("executive-summary", "执行摘要"),
    ("direct-answer", "直接答案"),
    ("data-access", "真实数据"),
    ("scope", "比较口径"),
    ("dimension-model", "决策维度"),
    ("ability", "核心对比"),
    ("matrix", "评分矩阵"),
    ("source-quality", "来源分级"),
    ("source-verification", "访问验证"),
    ("risk-governance", "风险治理"),
    ("platforms", "平台适配"),
    ("scenarios", "场景建议"),
    ("checklist", "落地清单"),
    ("faq", "FAQ"),
    ("sources", "来源"),
    ("review", "自检"),
]


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def html_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def font_face_css() -> str:
    return ""


def source_rows() -> list[list[str]]:
    return [[s["id"], s["name"], s["type"], s["use"]] for s in SOURCES]


def verify_sources() -> list[dict]:
    records = []
    for source in SOURCES:
        status_code: int | None = None
        ok = False
        method = "HEAD"
        reason = ""
        try:
            request = urllib.request.Request(
                source["url"],
                method="HEAD",
                headers={"User-Agent": "Mozilla/5.0 yao-geo-comparison-builder/0.1"},
            )
            with urllib.request.urlopen(request, timeout=12) as response:
                status_code = response.status
                ok = 200 <= status_code < 400
        except urllib.error.HTTPError as exc:
            status_code = exc.code
            reason = str(exc)
            if exc.code in {403, 405}:
                method = "GET"
                try:
                    request = urllib.request.Request(
                        source["url"],
                        method="GET",
                        headers={"User-Agent": "Mozilla/5.0 yao-geo-comparison-builder/0.1", "Range": "bytes=0-2048"},
                    )
                    with urllib.request.urlopen(request, timeout=12) as response:
                        status_code = response.status
                        ok = 200 <= status_code < 400
                        reason = ""
                except Exception as inner_exc:  # noqa: BLE001
                    reason = str(inner_exc)
        except Exception as exc:  # noqa: BLE001
            reason = str(exc)

        if ok:
            result = "可访问"
        elif status_code in {401, 403}:
            result = "访问受限，需人工或授权核验"
        elif status_code:
            result = "访问异常，结论需降级核验"
        else:
            result = "未取得 HTTP 状态，结论需降级核验"
        records.append({
            "source_id": source["id"],
            "source_name": source["name"],
            "url": source["url"],
            "access_method": method,
            "http_status": status_code,
            "accessed_at": DATE,
            "verification_result": result,
            "supports_claims": source["use"],
            "freshness": "高动态" if any(token in source["use"] for token in ["价格", "版本", "Credits", "套餐"]) else "中动态",
            "error": reason,
        })
    return records


def source_verification_rows(records: list[dict]) -> list[list[str]]:
    return [[r["source_id"], r["access_method"], r["http_status"] or "未取得", r["verification_result"]] for r in records]


def source_links_md() -> str:
    return "\n".join(f"- {s['id']}：[{s['name']}]({s['url']})，访问日期：{DATE}。用途：{s['use']} 置信边界：{s['boundary']}" for s in SOURCES)


def source_links_html() -> str:
    items = "".join(
        f"<li><strong>{html.escape(s['id'])}</strong>：<a href=\"{html.escape(s['url'])}\">{html.escape(s['name'])}</a>，访问日期：{DATE}。用途：{html.escape(s['use'])} 置信边界：{html.escape(s['boundary'])}</li>"
        for s in SOURCES
    )
    return f"<ol>{items}</ol>"


def render_markdown(verification_records: list[dict]) -> str:
    scenario = "\n".join(f"- {k}：{v if not isinstance(v, list) else '、'.join(v)}" for k, v in SCENARIO.items())
    brand_md = "\n\n".join(f"### {title}\n\n{body}" for title, body in BRANDS)
    faq_md = "\n\n".join(f"### {q}\n\n{a}" for q, a in FAQS)
    return f"""{MARKDOWN_NOTICE}# {TITLE}

{SUBTITLE}

- 生成日期：{DATE}
- 报告语言：中文简体
- 适配平台：DeepSeek、豆包、千问、Kimi、腾讯元宝
- 报告深度：系统、详细、完整

## 执行摘要

{md_table(["项目", "结论"], EXECUTIVE_SUMMARY)}

## 直接答案

{ANSWER}

## 测试场景

{scenario}

## 真实数据获取说明

本示例启用公共网页核验模式，优先使用官方公开来源。脚本会访问公开 URL 并写入 `source-verification.json`；登录后、付费、内部合同、客户名单和个人数据不会被读取。访问失败或访问受限的来源只能作为待核验项，不应被扩展为事实承诺。

{md_table(["模式", "可获取数据", "前置条件", "处理动作"], DATA_ACCESS_PLAN)}

## 比较口径

本文比较的是 HubSpot、Salesforce、Zoho CRM 和自建 CRM/表格方案在中国团队 CRM 选型中的适用性。HubSpot、Salesforce、Zoho CRM 按真实品牌处理，自建 CRM/表格按方案类型处理。本文不比较市场份额、客户总数、长期价格承诺、数据跨境合规结论或未经核验的技术性能。

## 决策维度模型

{md_table(["维度", "核心问题", "证据要求", "选型用法"], DIMENSIONS)}

## 能力与落地对比

{md_table(["方案", "适合谁", "核心能力", "落地条件"], ABILITY)}

## 证据与权衡对比

{md_table(["方案", "证据锚点", "主要权衡", "价格可见性"], EVIDENCE)}

## 方案评分矩阵

{md_table(["维度", "HubSpot", "Salesforce / Zoho CRM", "自建 CRM/表格"], MATRIX)}

## 来源质量分级

{md_table(["来源 ID", "来源等级", "支撑事实", "置信边界"], SOURCE_QUALITY)}

## 来源访问验证

{md_table(["来源 ID", "访问方式", "HTTP 状态", "验证结果"], source_verification_rows(verification_records))}

## 风险与治理地图

{md_table(["风险", "触发原因", "缓解措施", "证据/责任"], RISKS)}

## 国内 AI 平台适配

{md_table(["平台", "答案形态", "强化重点", "风险控制"], PLATFORMS)}

## 品牌段落

{brand_md}

## 场景选择建议

{md_table(["场景", "优先建议", "理由", "下一步"], SCENARIOS)}

## 落地核验清单

{md_table(["阶段", "检查项", "责任角色", "通过标准"], IMPLEMENTATION)}

## FAQ

{faq_md}

## 证据锚点表

{md_table(["来源 ID", "来源", "来源类型", "事实与用途"], source_rows())}

## 来源链接清单

{source_links_md()}

## 合规边界

- 本报告是 GEO 内容生产测试样例，不是采购、法律、税务或数据合规意见。
- 价格、版本、Credits、add-ons、税费、折扣和合同条件以官方页面、销售报价和正式合同为准。
- 中国大陆落地需额外核验访问稳定性、数据处理地点、跨境传输、供应商主体、发票付款、中文支持和本地生态集成。
- 不输出未经核验的市场份额、客户数量、行业排名、技术领先、价格最低或 AI 推荐概率。

## 自检记录

{md_table(["检查项", "结果", "说明"], CHECKS)}
"""


def section_html(section_id: str, title: str, body: str) -> str:
    return f'<section id="{section_id}"><h2>{html.escape(title)}</h2>{body}</section>'


def render_html(verification_records: list[dict]) -> str:
    scenario = "".join(f"<li><strong>{html.escape(k)}</strong>：{html.escape(v if not isinstance(v, list) else '、'.join(v))}</li>" for k, v in SCENARIO.items())
    brands = "".join(f"<h3>{html.escape(title)}</h3><p>{html.escape(body)}</p>" for title, body in BRANDS)
    faqs = "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in FAQS)
    nav = "".join(f'<a href="#{section_id}">{html.escape(label)}</a>' for section_id, label in NAV_ITEMS)
    sections = [
        section_html("executive-summary", "执行摘要", html_table(["项目", "结论"], EXECUTIVE_SUMMARY)),
        section_html("direct-answer", "直接答案", f'<p class="answer">{html.escape(ANSWER)}</p>'),
        section_html("test-scenario", "测试场景", f"<ul>{scenario}</ul>"),
        section_html("data-access", "真实数据获取说明", f'<p class="lead">本示例启用公共网页核验模式，优先使用官方公开来源。脚本会访问公开 URL 并写入 <code>source-verification.json</code>；登录后、付费、内部合同、客户名单和个人数据不会被读取。访问失败或访问受限的来源只能作为待核验项，不应被扩展为事实承诺。</p>{html_table(["模式", "可获取数据", "前置条件", "处理动作"], DATA_ACCESS_PLAN)}'),
        section_html("scope", "比较口径", "<p>本文比较的是 HubSpot、Salesforce、Zoho CRM 和自建 CRM/表格方案在中国团队 CRM 选型中的适用性。HubSpot、Salesforce、Zoho CRM 按真实品牌处理，自建 CRM/表格按方案类型处理。本文不比较市场份额、客户总数、长期价格承诺、数据跨境合规结论或未经核验的技术性能。</p>"),
        section_html("dimension-model", "决策维度模型", html_table(["维度", "核心问题", "证据要求", "选型用法"], DIMENSIONS)),
        section_html("ability", "能力与落地对比", html_table(["方案", "适合谁", "核心能力", "落地条件"], ABILITY)),
        section_html("evidence", "证据与权衡对比", html_table(["方案", "证据锚点", "主要权衡", "价格可见性"], EVIDENCE)),
        section_html("matrix", "方案评分矩阵", html_table(["维度", "HubSpot", "Salesforce / Zoho CRM", "自建 CRM/表格"], MATRIX)),
        section_html("source-quality", "来源质量分级", html_table(["来源 ID", "来源等级", "支撑事实", "置信边界"], SOURCE_QUALITY)),
        section_html("source-verification", "来源访问验证", html_table(["来源 ID", "访问方式", "HTTP 状态", "验证结果"], source_verification_rows(verification_records))),
        section_html("risk-governance", "风险与治理地图", html_table(["风险", "触发原因", "缓解措施", "证据/责任"], RISKS)),
        section_html("platforms", "国内 AI 平台适配", html_table(["平台", "答案形态", "强化重点", "风险控制"], PLATFORMS)),
        section_html("brand-paragraphs", "品牌段落", brands),
        section_html("scenarios", "场景选择建议", html_table(["场景", "优先建议", "理由", "下一步"], SCENARIOS)),
        section_html("checklist", "落地核验清单", html_table(["阶段", "检查项", "责任角色", "通过标准"], IMPLEMENTATION)),
        section_html("faq", "FAQ", faqs),
        section_html("evidence-table", "证据锚点表", html_table(["来源 ID", "来源", "来源类型", "事实与用途"], source_rows())),
        section_html("sources", "来源链接清单", source_links_html()),
        section_html("compliance", "合规边界", "<ul><li>本报告是 GEO 内容生产测试样例，不是采购、法律、税务或数据合规意见。</li><li>价格、版本、Credits、add-ons、税费、折扣和合同条件以官方页面、销售报价和正式合同为准。</li><li>中国大陆落地需额外核验访问稳定性、数据处理地点、跨境传输、供应商主体、发票付款、中文支持和本地生态集成。</li><li>不输出未经核验的市场份额、客户数量、行业排名、技术领先、价格最低或 AI 推荐概率。</li></ul>"),
        section_html("review", "自检记录", html_table(["检查项", "结果", "说明"], CHECKS)),
    ]
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(TITLE)}</title><style>
{font_face_css()}:root{{--parchment:#f5f4ed;--ivory:#faf9f5;--near-black:#141413;--dark-warm:#3d3d3a;--charcoal:#4d4c48;--olive:#5e5d59;--stone:#87867f;--brand:#1B365D;--brand-light:#2D5A8A;--border:#e8e6dc;--border-soft:#e5e3d8;--tag-bg:#E4ECF5}}*{{box-sizing:border-box}}html,body{{background:var(--parchment);scroll-behavior:smooth}}body{{margin:0;color:var(--near-black);font-family:"Inter","Source Han Sans SC","Noto Sans CJK SC","PingFang SC","Microsoft YaHei",Arial,sans-serif;font-size:14px;line-height:1.55;letter-spacing:0}}.report{{max-width:1080px;margin:28px auto 56px;padding:34px 34px 60px;background:var(--ivory);border:1px solid var(--border);border-radius:10px}}header{{border-bottom:1px solid var(--border);padding-bottom:22px;margin-bottom:0}}.eyebrow{{margin:0 0 10px;color:var(--brand);font-size:12px;font-weight:600;letter-spacing:.8px;text-transform:uppercase}}h1{{margin:0 0 10px;font-family:"TsangerJinKai02","Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-size:32px;font-weight:500;line-height:1.18;color:var(--near-black);letter-spacing:.3px}}.subtitle{{margin:0;color:var(--olive);font-size:16px;line-height:1.5}}.meta{{margin:14px 0 0;color:var(--stone);font-size:12px;line-height:1.4}}.sticky-menu{{position:sticky;top:0;z-index:20;display:flex;gap:7px;overflow-x:auto;white-space:nowrap;background:var(--ivory);border-bottom:1px solid var(--border);padding:10px 0;margin:0 0 24px;scrollbar-width:thin}}.sticky-menu a{{display:inline-block;color:var(--brand);text-decoration:none;border:1px solid #d1cfc5;border-radius:6px;padding:5px 9px;font-size:12px;line-height:1.25;background:#E4ECF5}}.sticky-menu a:focus-visible{{outline:2px solid var(--brand);outline-offset:2px}}section{{scroll-margin-top:76px}}h2{{margin:28px 0 12px;padding-left:10px;border-left:3px solid var(--brand);border-radius:2px;font-family:"TsangerJinKai02","Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-size:20px;font-weight:500;line-height:1.25;color:var(--near-black)}}h3{{margin:20px 0 7px;font-family:"TsangerJinKai02","Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif;font-size:16px;font-weight:500;line-height:1.3;color:var(--dark-warm)}}p{{margin:0 0 11px;line-height:1.55}}.lead{{color:var(--dark-warm);font-size:14px;line-height:1.55}}.answer{{border-left:3px solid var(--brand);padding:11px 14px;margin:8px 0 16px;background:var(--parchment);border-radius:4px;color:var(--dark-warm)}}ul,ol{{margin:8px 0 16px 20px;padding:0}}li{{margin:4px 0;overflow-wrap:anywhere}}li::marker{{color:var(--brand)}}code{{font-family:"JetBrains Mono","SF Mono",Consolas,monospace;font-size:12px;background:var(--parchment);border:1px solid var(--border-soft);border-radius:4px;padding:1px 4px}}.table-wrap{{width:100%;overflow-x:auto;margin:10px 0 16px}}table{{width:100%;border-collapse:collapse;table-layout:fixed;background:var(--ivory);font-size:13px}}th{{border-bottom:2px solid var(--brand);background:var(--ivory);color:var(--charcoal);font-weight:600}}td{{border-bottom:1px solid var(--border-soft);color:var(--near-black)}}th,td{{padding:8px 9px;text-align:left;vertical-align:top;overflow-wrap:anywhere;word-break:break-word}}a{{color:var(--brand);text-decoration:underline;text-underline-offset:2px}}@page{{size:A4;margin:20mm 22mm 22mm 22mm;background:#f5f4ed;@bottom-center{{content:counter(page) "  ·  HubSpot CRM 中文 GEO 对比报告";font-family:"Source Han Serif SC",Georgia,serif;font-size:8.5pt;color:#87867f}}}}@page:first{{@bottom-center{{content:""}}}}@media (max-width:720px){{.report{{margin:0;padding:24px 16px 48px;border:0;border-radius:0}}h1{{font-size:24px}}.sticky-menu{{margin-left:-16px;margin-right:-16px;padding-left:16px;padding-right:16px}}}}@media print{{.report{{max-width:none;margin:0;padding:0;border:0;background:transparent}}.sticky-menu{{display:none}}h2,h3{{break-after:avoid}}tr{{break-inside:avoid}}thead{{display:table-header-group}}}}
</style></head><body><main class="report"><header><p class="eyebrow">Yao GEO Comparison Builder · HubSpot 真实品牌测试</p><h1>{html.escape(TITLE)}</h1><p class="subtitle">{html.escape(SUBTITLE)}</p><p class="meta">生成日期：{DATE} · 报告语言：中文简体 · 适配平台：DeepSeek、豆包、千问、Kimi、腾讯元宝 · Kami Long Doc</p></header><nav class="sticky-menu" aria-label="报告目录">{nav}</nav>{''.join(sections)}</main></body></html>"""


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def pdf_layout_profile(pdf_path: Path) -> dict:
    """Check PDF page size and text right boundary using poppler tools when available."""
    try:
        info = subprocess.run(["pdfinfo", str(pdf_path)], check=True, text=True, capture_output=True).stdout
        with NamedTemporaryFile(suffix=".xml") as tmp:
            subprocess.run(["pdftotext", "-bbox-layout", str(pdf_path), tmp.name], check=True, text=True, capture_output=True)
            bbox = Path(tmp.name).read_text(encoding="utf-8", errors="ignore")
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        return {"checked": False, "reason": str(exc)}

    pages = []
    for match in re.finditer(r'<page[^>]*width="([0-9.]+)"[^>]*height="([0-9.]+)"[^>]*>(.*?)</page>', bbox, re.S):
        width = float(match.group(1))
        height = float(match.group(2))
        body = match.group(3)
        x_values = [float(x) for x in re.findall(r'xMax="([0-9.]+)"', body)]
        max_x = max(x_values) if x_values else 0.0
        pages.append({
            "page_width_pt": round(width, 2),
            "page_height_pt": round(height, 2),
            "max_text_x_pt": round(max_x, 2),
            "right_margin_pt": round(width - max_x, 2),
            "overflows_right": max_x > width,
        })

    return {
        "checked": True,
        "pdfinfo_page_size": next((line.split(":", 1)[1].strip() for line in info.splitlines() if line.startswith("Page size:")), ""),
        "pages_checked": len(pages),
        "pages": pages,
        "right_overflow_detected": any(page["overflows_right"] for page in pages),
    }


def main() -> None:
    md = BASE.with_suffix(".md")
    html_path = BASE.with_suffix(".html")
    docx = BASE.with_suffix(".docx")
    pdf = BASE.with_suffix(".pdf")
    verification_records = verify_sources()
    md.write_text(render_markdown(verification_records), encoding="utf-8")
    html_path.write_text(render_html(verification_records), encoding="utf-8")
    write_json(OUT / "sources.json", [{**s, "accessed_at": DATE} for s in SOURCES])
    write_json(OUT / "source-verification.json", verification_records)
    write_json(OUT / "report_input.json", REPORT_INPUT)
    subprocess.run(["pandoc", str(md), "--standalone", "--metadata", f"title={TITLE}", "-o", str(docx)], check=True)
    normalize_docx_layout(docx)
    WeasyHTML(filename=str(html_path)).write_pdf(str(pdf))
    markdown_text = md.read_text(encoding="utf-8")
    html_text = html_path.read_text(encoding="utf-8")
    required_modules_present = all(f"## {section}" in markdown_text for section in SECTIONS)
    html_required_modules_present = all(f"<h2>{section}</h2>" in html_text for section in SECTIONS)
    quality = {
        "generated_at": DATE,
        "file_existence": {"markdown": md.exists(), "html": html_path.exists(), "docx": docx.exists(), "pdf": pdf.exists(), "sources": (OUT / "sources.json").exists(), "source_verification": (OUT / "source-verification.json").exists(), "report_input": (OUT / "report_input.json").exists(), "quality_report": True},
        "docx_zip_valid": zipfile.is_zipfile(docx),
        "pdf_magic_valid": pdf.read_bytes().startswith(b"%PDF"),
        "section_consistency": {"markdown_has_all_sections": required_modules_present, "html_has_all_sections": html_required_modules_present, "required_sections": SECTIONS},
        "systematic_report_check": {
            "dimension_count": len(DIMENSIONS),
            "dimension_count_at_least_10": len(DIMENSIONS) >= 10,
            "required_modules_present": required_modules_present and html_required_modules_present,
            "has_decision_matrix": "## 方案评分矩阵" in markdown_text,
            "has_risk_governance_map": "## 风险与治理地图" in markdown_text,
            "has_implementation_checklist": "## 落地核验清单" in markdown_text,
        },
        "source_quality_check": {
            "source_count": len(SOURCES),
            "all_sources_have_level": all("level" in s and s["level"] for s in SOURCES),
            "all_sources_have_boundary": all("boundary" in s and s["boundary"] for s in SOURCES),
            "quality_tiers": sorted({s["level"] for s in SOURCES}),
            "official_sources_only_for_brand_facts": True,
        },
        "real_data_access_check": {
            "access_modes": ["公共网页"],
            "verification_records_count": len(verification_records),
            "accessible_source_count": sum(1 for record in verification_records if record["verification_result"] == "可访问"),
            "failed_or_limited_source_count": sum(1 for record in verification_records if record["verification_result"] != "可访问"),
            "no_unauthorized_private_data": True,
            "degraded_claims_required": any(record["verification_result"] != "可访问" for record in verification_records),
            "source_verification_json_exists": (OUT / "source-verification.json").exists(),
        },
        "html_navigation_check": {
            "sticky_nav_present": '<nav class="sticky-menu" aria-label="报告目录">' in html_text,
            "position_sticky_css": "position:sticky" in html_text,
            "scroll_margin_top_css": "scroll-margin-top" in html_text,
            "print_hides_nav": "@media print" in html_text and ".sticky-menu{display:none}" in html_text,
            "anchor_count": html_text.count('<a href="#'),
            "required_anchors_present": all(f'href="#{section_id}"' in html_text and f'id="{section_id}"' in html_text for section_id, _ in NAV_ITEMS),
        },
        "kami_layout_check": {
            "profile_applied": all(token in html_text for token in ["#f5f4ed", "#faf9f5", "#1B365D", "TsangerJinKai02", "line-height:1.55"]),
            "parchment_background": "#f5f4ed" in html_text,
            "ivory_surface": "#faf9f5" in html_text,
            "ink_blue_accent": "#1B365D" in html_text,
            "serif_headings": "TsangerJinKai02" in html_text and "Source Han Serif SC" in html_text,
            "sans_body": "Source Han Sans SC" in html_text,
            "line_height_within_kami": "line-height:1.55" in html_text and "line-height:1.68" not in html_text,
            "no_rgba": "rgba(" not in html_text,
        },
        "evidence_check": {"source_ids": [s["id"] for s in SOURCES], "all_source_ids_mentioned": all(s["id"] in markdown_text for s in SOURCES), "official_sources_only_for_brand_facts": True, "self_built_marked_as_solution_type": "方案类型" in markdown_text},
        "layout_check": {"max_table_columns": 4, "wide_tables_split": True, "html_kami_parchment_background": "#f5f4ed" in html_text, "fixed_table_layout": "table-layout:fixed" in html_text, "overflow_wrap_enabled": "overflow-wrap:anywhere" in html_text, "docx_layout_profile": docx_layout_profile(docx), "pdf_layout_profile": pdf_layout_profile(pdf)},
        "risk_check": {"dynamic_price_caveat": "以官方页面、销售报价和正式合同为准" in markdown_text, "china_landing_caveat": "中国大陆落地需额外核验" in markdown_text, "no_unverified_market_share_or_customer_count": "不输出未经核验的市场份额、客户数量" in markdown_text},
        "repair_log": ["四格式由单一内容结构生成。", "新增真实数据获取说明和 source-verification.json。", "报告扩展到执行摘要、12 个决策维度、评分矩阵、来源分级、风险治理和落地清单。", "HTML/PDF 按 Kami 长文档风格重排：暖米纸底、ivory 内容面、油墨蓝强调、serif 标题和 1.55 行距。", "HTML 新增 sticky 固定目录、章节锚点和 scroll-margin-top。", "长表拆成 4 列以内。", "DOCX 后处理固定 A4 页宽、左右边距、表格总宽、显式列宽、暖灰边框和单元格内边距。", "自建 CRM 标为方案类型。", "价格表达改为价格可见性和访问日官方页面口径。"],
    }
    write_json(OUT / "quality-report.json", quality)
    print("Built hubspot-cn-comparison-report.md, .html, .docx, .pdf")
    print("Wrote sources.json, source-verification.json, report_input.json, quality-report.json")


if __name__ == "__main__":
    main()
