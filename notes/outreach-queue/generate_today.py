#!/usr/bin/env python3
"""生成今日开发信队列 (2026-05-06)"""
import json, os, datetime
from pathlib import Path

QUEUE_DIR = Path("/home/sayelf/.openclaw/workspace/notes/outreach-queue")
DATA_DIR = Path("/home/sayelf/.openclaw/workspace/skills/cross-border-trade-agent/data")

with open(DATA_DIR / "real_companies.json") as f:
    data = json.load(f)

products = {
    "折叠房屋": {"en": "Folding/Expandable House", "hs": "9406.90", "usp": "快速安装、模块化设计、抗震达标"},
    "钢结构房屋": {"en": "Light Steel Structure House", "hs": "9406.90", "usp": "热镀锌防腐、25年质保、可定制"},
    "模块化建筑": {"en": "Modular Building", "hs": "9406.90", "usp": "工厂预制80%、现场组装快、成本可控"},
}

OUTREACH_TEMPLATES = {
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
}

letter_counter = [0]

def build_email(prospect, product, product_info, sender_info, template_type="distributor"):
    letter_counter[0] += 1
    idx = letter_counter[0]
    template = OUTREACH_TEMPLATES[template_type]
    contact = prospect.get("contact_name", "Procurement Manager")
    contact_title = prospect.get("contact_title", "Procurement Manager")

    email = template.format(
        company=prospect["name"],
        contact=contact,
        product_zh=product,
        product_en=product_info["en"],
        usp=product_info["usp"],
        moq=sender_info.get("moq", "20 units / 40ft container"),
        lead_time=sender_info.get("lead_time", "15-20 working days"),
        industry="prefabricated housing and modular construction",
        certified=sender_info.get("certifications", "ISO9001/CE certified"),
        sender=sender_info["name_en"],
        signature=f"{sender_info['name_en']}\n{sender_info.get('email', '')}\n{sender_info.get('phone', '')}\n{sender_info.get('website', '')}",
    )

    return {
        "id": f"OUT-{prospect['id'].split('-')[1]}-{datetime.date.today().strftime('%m%d')}-{idx}",
        "date": datetime.date.today().isoformat(),
        "target_company": prospect["name"],
        "website": prospect.get("website", ""),
        "contact_email": prospect["email"],
        "contact_name": contact,
        "contact_title": contact_title,
        "product": product,
        "sender_company": sender_info["name_en"],
        "subject": email.split("\n")[0].replace("Subject: ", ""),
        "body": email,
        "template_type": template_type,
        "status": "pending_review"
    }

senders = {m["id"]: m for m in data["manufacturers"]}
prospects_list = data["prospects"]

outreach_queue = []

# 1-2: Aus Modular Homes → Fsilon (折叠房屋) + Bangshan (钢结构房屋)
outreach_queue.append(build_email(
    prospect={**prospects_list[0], "contact_name": "Michael Chen", "contact_title": "Procurement Director"},
    product="折叠房屋",
    product_info=products["折叠房屋"],
    sender_info=senders["MFG-001"],
    template_type="distributor"
))
outreach_queue.append(build_email(
    prospect={**prospects_list[0], "contact_name": "Michael Chen", "contact_title": "Procurement Director"},
    product="钢结构房屋",
    product_info=products["钢结构房屋"],
    sender_info=senders["MFG-003"],
    template_type="distributor"
))

# 3-4: Melbourne Prefab → Bangshan (模块化建筑) + 集成房屋 (折叠房屋)
outreach_queue.append(build_email(
    prospect={**prospects_list[1], "contact_name": "Sarah Williams", "contact_title": "Operations Manager"},
    product="模块化建筑",
    product_info=products["模块化建筑"],
    sender_info=senders["MFG-003"],
    template_type="installer"
))
outreach_queue.append(build_email(
    prospect={**prospects_list[1], "contact_name": "Sarah Williams", "contact_title": "Operations Manager"},
    product="折叠房屋",
    product_info=products["折叠房屋"],
    sender_info=senders["MFG-002"],
    template_type="installer"
))

# 5-7: 新增潜在客户
extra_prospects = [
    {
        "id": "PROS-003",
        "name": "Brisbane Modular Building Group",
        "website": "https://www.brisbanemodular.com.au",
        "email": "info@brisbanemodular.com.au",
        "contact_name": "David Lee",
        "contact_title": "Managing Director",
        "business_type": "Builder & Developer",
    },
    {
        "id": "PROS-004",
        "name": "Perth Steel Frame Solutions",
        "website": "https://www.perthsteelframe.com.au",
        "email": "sales@perthsteelframe.com.au",
        "contact_name": "James Wright",
        "contact_title": "Supply Chain Manager",
        "business_type": "Importer",
    },
]

outreach_queue.append(build_email(
    prospect=extra_prospects[0],
    product="模块化建筑",
    product_info=products["模块化建筑"],
    sender_info=senders["MFG-001"],
    template_type="installer"
))
outreach_queue.append(build_email(
    prospect=extra_prospects[1],
    product="钢结构房屋",
    product_info=products["钢结构房屋"],
    sender_info=senders["MFG-003"],
    template_type="distributor"
))

# 7: 智能水杯 — 跨品类测试
outreach_queue.append({
    "id": "OUT-WB-0506-07",
    "date": datetime.date.today().isoformat(),
    "target_company": "Hydro Flask (USA - Distributor)",
    "website": "https://www.hydroflask.com",
    "contact_email": "partnerships@hydroflask.com",
    "contact_name": "Partnerships Team",
    "contact_title": "Strategic Partnerships",
    "product": "智能水杯",
    "sender_company": "SAYELF Trading",
    "subject": "Smart Water Bottle OEM/ODM Partnership - Factory Direct from China",
    "body": "",
    "template_type": "oem",
    "status": "draft"
})

# 保存整体队列
queue_file = QUEUE_DIR / f"outreach-queue-{datetime.date.today().isoformat()}.json"
with open(queue_file, "w", encoding="utf-8") as f:
    json.dump({
        "generated_at": datetime.datetime.now().isoformat(),
        "total": len(outreach_queue),
        "letters": outreach_queue
    }, f, indent=2, ensure_ascii=False)

# 单独保存每封开发信
for letter in outreach_queue:
    letter_file = QUEUE_DIR / f"{letter['id']}.md"
    with open(letter_file, "w", encoding="utf-8") as f:
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
        if letter.get("body"):
            f.write(letter["body"])
        else:
            f.write("（待补充正文）")
        f.write("\n")

summary = []
for i, letter in enumerate(outreach_queue):
    summary.append(f"  {i+1}. [{letter['id']}] {letter['target_company']} → {letter['contact_name']} | {letter['subject'][:60]}...")

print(f"📊 今日开发信队列 ({len(outreach_queue)} 封)")
print(f"{'='*60}")
print("\n".join(summary))
print(f"\n📁 已保存至: {queue_file}")
