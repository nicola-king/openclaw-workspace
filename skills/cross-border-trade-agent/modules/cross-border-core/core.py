#!/usr/bin/env python3
"""
跨境触达 Agent — 开发信生成引擎 v2
支持 --task generate_outreach 供 cron 调度
"""
import json, os, sys, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE / "data"
QUEUE_DIR = BASE.parent.parent / "notes" / "outreach-queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

# ── 产品库 ──
PRODUCTS = {
    "折叠房屋": {"en": "Folding/Expandable House", "hs": "9406.90", "usp": "快速安装、模块化设计、抗震达标"},
    "钢结构房屋": {"en": "Light Steel Structure House", "hs": "9406.90", "usp": "热镀锌防腐、25年质保、可定制"},
    "模块化建筑": {"en": "Modular Building", "hs": "9406.90", "usp": "工厂预制80%、现场组装快、成本可控"},
    "集装箱房屋": {"en": "Container House", "hs": "9406.90", "usp": "即装即用、灵活扩容、可搬迁重复使用"},
}

# ── 邮件模板 ──
TEMPLATES = {
    "distributor": """Subject: {product_en} - {company} | 工厂直供澳洲市场

Hi {contact},

I'm writing from {sender}, a leading Chinese manufacturer of {product_zh} with ISO9001/CE certifications.

We noticed {company} is active in the Australian {industry} space, and believe our products could be a strong fit for your portfolio:

• {product_zh}: {usp}
• MOQ: {moq} | Lead time: {lead_time}
• Competitive FOB pricing with exclusive territory protection
• Samples available for evaluation

We're looking for a reliable distributor/importer in Australia. Would you be interested in exploring this opportunity?

Best regards,
{signature}
""",

    "installer": """Subject: Partner with Us for {product_en} in Australia

Hi {contact},

{sender} is a {certified} manufacturer specializing in {product_zh} for the Australian market.

We're reaching out because your company's project portfolio in {industry} aligns with our product strengths:

• {usp}
• Full technical documentation (Structural, Thermal, NCC compliance)
• On-site installation support available
• Previous project references in Australia

We're looking for experienced installation partners. Would you be open to a preliminary discussion?

Best regards,
{signature}
""",

    "middle_east_project": """Subject: Saudi Mega Project Supplier Opportunity - {product_en}

Dear {contact},

This is {sender}, a Chinese manufacturer of {product_zh} certified with {certified}, writing to introduce our supply capabilities.

We have learned that the {project_name} in Saudi Arabia ({budget}B USD project, {workers} workers peak) has substantial procurement needs for {product_zh}. As a factory with proven export experience to the Middle East, we are well-positioned to supply:

• {usp}
• MOQ: {moq} | Lead time: {lead_time}
• Full technical documentation & compliance
• References from previous Middle East projects

We are looking for experienced partners to collaborate on supplying this mega project. Would you be interested in discussing this opportunity?

Best regards,
{signature}
""",

    "factory_lead": """Subject: {project_name} - {product_zh} Supply Opportunity

{contact} 您好，

我是 {sender} 的跨境业务对接人。近期获取到以下沙特项目采购需求，可能与贵司产品线高度匹配：

项目：{project_name}
预算：${budget}B USD
需求：{product_zh}（{need_detail}）
状态：{project_status}

我方已建立该项目相关渠道，需要寻找具备以下条件的供应商：
• {usp}
• 有中东出口经验
• 可提供技术文档和合规认证

如贵司有兴趣参与，请回复确认，我方将提供项目详细信息及对接方式。

此致，
{signature}
""",
}


_global_idx = [0]

def build_email(prospect, product, product_info, sender_info, template_type="distributor", extra_fields=None, today=None):
    """构建一封开发信"""
    if today is None:
        today = datetime.date.today()
    _global_idx[0] += 1
    template = TEMPLATES.get(template_type, TEMPLATES["distributor"])
    contact = prospect.get("contact_name", "Procurement Manager")
    contact_title = prospect.get("contact_title", "Procurement Manager")

    fields = {
        "company": prospect["name"],
        "contact": contact,
        "product_zh": product,
        "product_en": product_info["en"],
        "usp": product_info["usp"],
        "moq": sender_info.get("moq", "20 units / 40ft container"),
        "lead_time": sender_info.get("lead_time", "15-20 working days"),
        "industry": "prefabricated housing and modular construction",
        "certified": sender_info.get("certifications", "ISO9001/CE certified"),
        "sender": sender_info["name_en"],
        "signature": (
            f"{sender_info['name_en']}\n"
            f"{sender_info.get('email', '')}\n"
            f"{sender_info.get('phone', '')}\n"
            f"{sender_info.get('website', '')}"
        ),
    }
    if extra_fields:
        fields.update(extra_fields)

    email = template.format(**fields)

    pid = prospect.get('id','000').split('-')[-1]
    return {
        "id": f"OUT-{pid}-{today.strftime('%m%d')}-{_global_idx[0]}",
        "date": today.isoformat(),
        "target_company": prospect["name"],
        "website": prospect.get("website", ""),
        "contact_email": prospect.get("email", ""),
        "contact_name": contact,
        "contact_title": contact_title,
        "product": product,
        "sender_company": sender_info["name_en"],
        "subject": email.split("\n")[0].replace("Subject: ", ""),
        "body": email,
        "template_type": template_type,
        "status": "pending_review"
    }


def generate_outreach():
    """生成今日开发信队列"""
    today = datetime.date.today()
    today_str = today.isoformat()

    data_file = DATA_DIR / "real_companies.json"
    if not data_file.exists():
        return {"status": "error", "message": f"数据文件不存在: {data_file}"}

    with open(data_file) as f:
        data = json.load(f)

    senders = {m["id"]: m for m in data["manufacturers"]}
    prospects_list = data["prospects"]

    outreach_queue = []

    # ── 1-2: 澳洲分销商轮换触达（Aus Modular → Fsilon 钢结构房屋） ──
    outreach_queue.append(build_email(
        prospect={**prospects_list[0], "contact_name": "Michael Chen", "contact_title": "Procurement Director"},
        product="钢结构房屋",
        product_info=PRODUCTS["钢结构房屋"],
        sender_info=senders["MFG-001"],
        template_type="distributor",
        today=today,
    ))

    # Melbourne Prefab → Bangshan 集装箱房屋 (installer)
    outreach_queue.append(build_email(
        prospect={**prospects_list[1], "contact_name": "Sarah Williams", "contact_title": "Operations Manager"},
        product="集装箱房屋",
        product_info=PRODUCTS["集装箱房屋"],
        sender_info=senders["MFG-003"],
        template_type="installer",
        today=today,
    ))

    # ── 3-4: 新增澳洲潜在客户 ──
    extra_prospects = [
        {
            "id": "PROS-005",
            "name": "Apex Modular Construction (Queensland)",
            "website": "https://www.apexmodular.com.au",
            "email": "info@apexmodular.com.au",
            "contact_name": "Tom Henderson",
            "contact_title": "Director of Operations",
            "business_type": "Modular Builder",
        },
        {
            "id": "PROS-006",
            "name": "Pacific Prefab Supplies",
            "website": "https://www.pacificprefab.com",
            "email": "procurement@pacificprefab.com",
            "contact_name": "Angela Torres",
            "contact_title": "Procurement Manager",
            "business_type": "Building Materials Importer",
        },
    ]

    outreach_queue.append(build_email(
        prospect=extra_prospects[0],
        product="模块化建筑",
        product_info=PRODUCTS["模块化建筑"],
        sender_info=senders["MFG-002"],
        template_type="installer",
        today=today,
    ))

    outreach_queue.append(build_email(
        prospect=extra_prospects[1],
        product="钢结构房屋",
        product_info=PRODUCTS["钢结构房屋"],
        sender_info=senders["MFG-003"],
        template_type="distributor",
        today=today,
    ))

    # ── 5-6: 沙特项目机会推送（触达中国工厂） ──
    saudi_projects = [
        {
            "project": "Jewel of the Bride (吉达)",
            "budget_b": 2,
            "workers": "2-3万",
            "need_detail": "劳工营模块化住房，高峰期3万工人",
            "product": "折叠房屋",
            "product_info": PRODUCTS["折叠房屋"],
            "project_status": "2026年5月启动，5-8年工期",
        },
        {
            "project": "NEOM THE LINE",
            "budget_b": 500,
            "workers": "持续增长",
            "need_detail": "基建劳工营/钢结构/模块化建筑",
            "product": "模块化建筑",
            "product_info": PRODUCTS["模块化建筑"],
            "project_status": "建设中，长期采购需求",
        },
    ]

    # Fsilon → Jewel of the Bride
    outreach_queue.append(build_email(
        prospect={
            **senders["MFG-001"],
            "id": "MFG",
            "contact_name": "Export Manager",
            "contact_title": "Export Department",
            "email": senders["MFG-001"]["email"],
        },
        product="折叠房屋",
        product_info=PRODUCTS["折叠房屋"],
        sender_info={
            "name_en": "SAYELF Trading",
            "email": "sayelf.trading@gmail.com",
            "phone": "",
            "website": "",
            "certifications": "ISO9001/CE",
        },
        template_type="factory_lead",
        extra_fields={
            "project_name": "Jewel of the Bride (吉达)",
            "budget": "2",
            "need_detail": "劳工营模块化住房，高峰期3万工人",
            "project_status": "2026年5月启动，5-8年工期",
            "certified": senders["MFG-001"].get("certifications", "ISO9001/CE"),
        },
        today=today,
    ))

    # Bangshan → NEOM
    outreach_queue.append(build_email(
        prospect={
            **senders["MFG-003"],
            "id": "MFG",
            "contact_name": "Export Director",
            "contact_title": "Export Department",
            "email": senders["MFG-003"]["email"],
        },
        product="模块化建筑",
        product_info=PRODUCTS["模块化建筑"],
        sender_info={
            "name_en": "SAYELF Trading",
            "email": "sayelf.trading@gmail.com",
            "phone": "",
            "website": "",
            "certifications": "ISO9001/CE",
        },
        template_type="factory_lead",
        extra_fields={
            "project_name": "NEOM THE LINE",
            "budget": "500",
            "need_detail": "基建劳工营/钢结构/模块化建筑",
            "project_status": "建设中，长期采购需求",
            "certified": senders["MFG-003"].get("certifications", "ISO9001/CE"),
        },
        today=today,
    ))

    # ── 保存 ──
    queue_file = QUEUE_DIR / f"outreach-queue-{today_str}.json"
    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.datetime.now().isoformat(),
            "total": len(outreach_queue),
            "letters": outreach_queue,
        }, f, indent=2, ensure_ascii=False)

    for letter in outreach_queue:
        lf = QUEUE_DIR / f"{letter['id']}.md"
        with open(lf, "w", encoding="utf-8") as f:
            f.write(f"# {letter['id']} - {letter['subject']}\n\n")
            f.write(f"**日期**: {letter['date']}\n")
            f.write(f"**目标公司**: {letter['target_company']}\n")
            f.write(f"**网站**: {letter.get('website', 'N/A')}\n")
            f.write(f"**联系人**: {letter['contact_name']} ({letter['contact_title']})\n")
            f.write(f"**邮箱**: {letter['contact_email']}\n")
            f.write(f"**产品**: {letter['product']}\n")
            f.write(f"**发件方**: {letter['sender_company']}\n")
            f.write(f"**主题**: {letter['subject']}\n")
            f.write(f"**状态**: {letter['status']}\n\n")
            f.write("---\n\n")
            f.write(letter.get("body", "（待补充正文）"))
            f.write("\n")

    return {
        "status": "success",
        "date": today_str,
        "total": len(outreach_queue),
        "queue_file": str(queue_file),
        "letters": [
            {
                "id": l["id"],
                "target_company": l["target_company"],
                "contact_name": l["contact_name"],
                "subject": l["subject"],
            }
            for l in outreach_queue
        ],
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="跨境触达 Agent")
    parser.add_argument("--task", required=True, help="任务名称")
    args = parser.parse_args()

    if args.task == "generate_outreach":
        result = generate_outreach()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"status": "error", "message": f"未知任务: {args.task}"}))


if __name__ == "__main__":
    main()
