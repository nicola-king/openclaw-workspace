#!/usr/bin/env python3
"""钢结构折叠集成房屋 — 需求方买家PDF v4（含真实联系人）"""
import sys, os
sys.path.insert(0, "/home/sayelf/.openclaw/workspace/skills/art-agent/modules/shared")
from render_engine import render, verify_pdf
OUT = "/home/sayelf/.openclaw/workspace/output/geo-optimization"

HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page{size:A4;margin:20mm 18mm;@bottom-center{content:"太一跨境贸易 Agent — 需求方报告";font-size:8pt;color:#8899aa;}}
@font-face{font-family:'Noto';src:url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');}
body{font-family:'Noto','Microsoft YaHei',sans-serif;color:#1a2a3a;line-height:1.6;font-size:10pt;}
.cover{page-break-after:always;text-align:center;padding-top:100px;}
.cover .tag{display:inline-block;background:#c0392b;color:#fff;padding:6px 20px;font-size:10pt;letter-spacing:3px;margin-bottom:30px;}
.cover h1{font-size:26pt;color:#0d1b2a;margin:20px 0;}
.cover h2{font-size:16pt;color:#c0392b;font-weight:normal;}
.cover .divider{width:60px;height:3px;background:#c0392b;margin:20px auto;}
.cover .info{color:#8899aa;font-size:9pt;line-height:2;}
h3.section{background:#0d1b2a;color:#fff;padding:8px 14px;font-size:12pt;margin:24px 0 12px;border-left:4px solid #c0392b;}
h4{color:#0d1b2a;font-size:11pt;margin:16px 0 6px;border-bottom:1px solid #e0e8f0;padding-bottom:4px;}
.card{border:1px solid #d0d8e0;border-radius:4px;padding:10px 14px;margin:8px 0;page-break-inside:avoid;}
.card .name{font-size:11pt;font-weight:bold;color:#0d1b2a;}
.card .meta{font-size:8.5pt;color:#667788;margin:2px 0;}
.card .detail{font-size:9pt;margin:4px 0;}
.card .url{color:#2a7fc9;word-break:break-all;font-size:8.5pt;}
.contact-row{background:#f0faf0;border-left:3px solid #2ecc71;padding:4px 10px;margin:3px 0;font-size:9pt;}
.p0{display:inline-block;background:#e74c3c;color:#fff;padding:1px 8px;border-radius:3px;font-size:8pt;font-weight:bold;}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:9pt;}
th{background:#0d1b2a;color:#fff;padding:6px 8px;text-align:center;}
td{padding:5px 8px;border-bottom:1px solid #e0e8f0;}
tr:nth-child(even) td{background:#f5f8fc;}
.insight-box{background:#f0f4f8;border-left:4px solid #c0392b;padding:10px 14px;margin:10px 0;font-size:9pt;}
.footer{margin-top:20px;padding-top:10px;border-top:1px solid #d0d8e0;font-size:8pt;color:#8899aa;}
</style></head><body>

<div class="cover">
<div class="tag">需求方买家报告</div>
<h1>钢结构折叠集成房屋</h1>
<h2>🇦🇺 澳大利亚 · 🇳🇿 新西兰 终端买家</h2>
<div class="divider"></div>
<div class="info">
<p>报告日期：2026-05-19 | 数据来源：LinkedIn / RocketReach / ZoomInfo / 供应商门户</p>
<p>联系方式通过公开商业媒体获取，需核实后触达</p>
</div>
</div>

<h3 class="section">一、🇦🇺 矿业公司（最大需求方）</h3>

<div class="card">
<div class="name"><span class="p0">P0</span> BHP Billiton</div>
<div class="meta">📍 墨尔本/Pilbara WA | 👷 5万+工人 | 🏔️ 矿工营房持续采购</div>
<div class="detail">BHP是澳洲最大矿业公司，Pilbara矿区+Olympic Dam等营地需大量模块化住宿。Fleetwood是现有供应商。</div>
<div class="contact-row"><strong>🔥 Luke King</strong> — Head of Procurement（采购主管）<br/>来源: RocketReach（2邮箱+2电话）| LinkedIn搜索获取详细联系</div>
<div class="contact-row"><strong>🔥 Kurt Benavides</strong> — Head of Procurement Operations（采购运营主管）<br/>来源: AroundDeal | LinkedIn搜索获取</div>
<div class="contact-row"><strong>🔥 Tajinder Bedi</strong> — Senior Procurement Manager（高级采购经理）<br/>来源: LinkedIn | au.linkedin.com/in/tejinder-bedi</div>
<div class="url">供应商注册: bhp.com/suppliers | 采购系统: bhp.procurement.ariba.com</div>
</div>

<div class="card">
<div class="name"><span class="p0">P0</span> Fortescue Metals Group</div>
<div class="meta">📍 珀斯/Pilbara WA | 👷 2万+工人</div>
<div class="contact-row"><strong>🔥 Dara Byrne</strong> — Group Manager, Contracts & Procurement - Projects（合同与采购项目群经理）<br/>来源: ZoomInfo / LinkedIn / RocketReach（有邮箱）</div>
<div class="contact-row"><strong>🔥 Mark Cocks</strong> — Senior Contracts & Procurement Specialist<br/>来源: Wiza / LinkedIn</div>
<div class="url">供应商中心: suppliers.fortescue.com</div>
</div>

<div class="card">
<div class="name"><span class="p0">P0</span> Rio Tinto</div>
<div class="meta">📍 墨尔本/Pilbara WA | 👷 4万+工人</div>
<div class="detail">采购部通过供应商门户管理。建议LinkedIn搜索"Rio Tinto Procurement Camp Accommodation"找到对口联系人。</div>
<div class="url">供应商门户: riotinto.com/en/suppliers</div>
</div>

<h3 class="section">二、🇳🇿 政府住房署</h3>

<div class="card">
<div class="name"><span class="p0">P0</span> Kāinga Ora — Homes and Communities</div>
<div class="meta">📍 新西兰全国 | 🏢 政府住房机构</div>
<div class="detail">新西兰最大住房供应商，模块化建筑是其解决住房危机的核心方案。通过ETender平台发布招标。</div>
<div class="contact-row"><strong>🔥 Andrea Morton</strong> — Director Procurement and Supplier Management（采购与供应商管理总监）<br/>邮箱: a*****@kainga***.govt.nz（Wiza, 需验证）</div>
<div class="url">供应商注册: kaingaora.govt.nz/suppliers</div>
<div class="url">招标平台: tenderlink.com/kaingaora | gets.govt.nz</div>
</div>

<h3 class="section">三、政府采购平台</h3>
<table>
<tr><th>平台</th><th>国家</th><th>搜索关键词</th></tr>
<tr><td>AusTender (austender.gov.au)</td><td>🇦🇺</td><td>"prefabricated building" "modular accommodation"</td></tr>
<tr><td>tenders.nsw.gov.au</td><td>🇦🇺 NSW</td><td>"relocatable classroom" "temporary building"</td></tr>
<tr><td>tenders.vic.gov.au</td><td>🇦🇺 VIC</td><td>"temporary housing" "modular building"</td></tr>
<tr><td>tenders.wa.gov.au</td><td>🇦🇺 WA</td><td>"camp accommodation" "transportable building"</td></tr>
<tr><td>qtenders.qld.gov.au</td><td>🇦🇺 QLD</td><td>"temporary housing" "prefab accommodation"</td></tr>
<tr><td>GETS + tenderlink/kaingaora</td><td>🇳🇿</td><td>"modular" "transportable" "housing"</td></tr>
</table>

<h3 class="section">四、触达行动</h3>
<table>
<tr><th>顺序</th><th>目标</th><th>联系人</th><th>动作</th></tr>
<tr><td>1 🔥</td><td>BHP</td><td>Luke King / Kurt Benavides / Tajinder Bedi</td><td>LinkedIn加好友+供应商门户注册</td></tr>
<tr><td>2 🔥</td><td>Fortescue</td><td>Dara Byrne / Mark Cocks</td><td>LinkedIn加好友+供应商门户注册+发inMail</td></tr>
<tr><td>3 🔥</td><td>Kāinga Ora</td><td>Andrea Morton</td><td>LinkedIn加好友+ETender注册+发inMail</td></tr>
<tr><td>4 🔥</td><td>Rio Tinto</td><td>采购部</td><td>供应商门户注册+LinkedIn搜对口人</td></tr>
<tr><td>5</td><td>AusTender</td><td>-</td><td>注册+RSS关键词订阅</td></tr>
<tr><td>6</td><td>6个招标平台</td><td>-</td><td>注册+关键词警报</td></tr>
</table>

<div class="footer">
<p>买家情报引擎 v4 | 数据源: LinkedIn / RocketReach / ZoomInfo / Wiza / AroundDeal / 各公司官网</p>
<p>⚠️ 联系方式来自公开商业媒体，建议通过LinkedIn核实后触达</p>
</div>
</body></html>"""

os.makedirs(OUT, exist_ok=True)
out = os.path.join(OUT, "钢结构折叠房屋需求方买家v4.pdf")
print(f"🖨️ {out}")
r = render(body_html=HTML, output_path=out, content_type="chinese",
           verify_keywords=["Luke King", "Dara Byrne", "Andrea Morton", "Fortescue", "Kāinga"])
if r.get("status") == "ok":
    print(f"✅ {os.path.getsize(out)//1024}KB | {verify_pdf(out, keywords=['Luke','Dara','Andrea'])}")
