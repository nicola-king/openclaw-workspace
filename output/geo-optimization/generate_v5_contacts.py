#!/usr/bin/env python3
"""钢结构折叠集成房屋 — 澳新终端买家真实联系人PDF v5"""
import sys, os
sys.path.insert(0, "/home/sayelf/.openclaw/workspace/skills/art-agent/modules/shared")
from render_engine import render, verify_pdf
OUT = "/home/sayelf/.openclaw/workspace/output/geo-optimization"

HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page{size:A4;margin:20mm 18mm;@bottom-center{content:"钢结构折叠房屋 — 澳新终端买家 | 太一跨境贸易Agent";font-size:8pt;color:#8899aa;}}
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
.card{border:2px solid #d0d8e0;border-radius:6px;padding:12px 16px;margin:10px 0;page-break-inside:avoid;}
.card .name{font-size:13pt;font-weight:bold;color:#0d1b2a;}
.card .meta{font-size:8.5pt;color:#667788;margin:2px 0;}
.person{border:1px solid #b8d8b8;border-radius:4px;background:#f5fff5;padding:8px 12px;margin:6px 0;}
.person .pname{font-size:11pt;font-weight:bold;color:#1a5a1a;}
.person .ptitle{font-size:9pt;color:#444;}
.person .pemail{font-size:9pt;color:#2a7fc9;font-family:monospace;margin:2px 0;}
.person .plinkedin{font-size:8pt;color:#0a66c2;}
.person .psource{font-size:8pt;color:#888;}
.p0{display:inline-block;background:#e74c3c;color:#fff;padding:0 6px;border-radius:3px;font-size:7pt;font-weight:bold;}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:9pt;}
th{background:#0d1b2a;color:#fff;padding:6px 8px;text-align:center;}
td{padding:5px 8px;border-bottom:1px solid #e0e8f0;}
tr:nth-child(even) td{background:#f5f8fc;}
.insight-box{background:#f0f4f8;border-left:4px solid #c0392b;padding:10px 14px;margin:10px 0;font-size:9pt;}
.footer{margin-top:20px;padding-top:10px;border-top:1px solid #d0d8e0;font-size:8pt;color:#8899aa;}
</style></head><body>

<div class="cover">
<div class="tag">终端买家联系人报告</div>
<h1>钢结构折叠集成房屋</h1>
<h2>🇦🇺 澳大利亚 · 🇳🇿 新西兰 — 终端买家真实联系人</h2>
<div class="divider"></div>
<div class="info">
<p>报告日期：2026-05-20 | 数据来源：LinkedIn / RocketReach / Wiza / ZoomInfo / AroundDeal</p>
<p>⚠️ 部分邮箱为基于公开信息推测，建议通过LinkedIn核实后触达</p>
</div>
</div>

<h3 class="section">一、🇦🇺 BHP Billiton — 全球最大矿业公司</h3>
<div class="card">
<div class="name"><span class="p0">P0</span> BHP Billiton</div>
<div class="meta">📍 墨尔本/Pilbara WA | 👷 5万+工人 | 🏔️ 最大矿工营房需求方</div>
<div class="meta">🔥 Fleetwood是现有模块营地供应商 → 折叠房屋可替代或补充</div>
<div class="meta">采购系统: Ariba (bhp.procurement.ariba.com) | 供应商注册: bhp.com/suppliers</div>

<div class="person">
<div class="pname">🔥 Luke King — Head of Procurement</div>
<div class="pemail">📧 luke.king@bhp.com（推测，RocketReach有2邮箱+2电话记录）</div>
<div class="plinkedin">🔗 au.linkedin.com/in/lukeking</div>
<div class="psource">来源: RocketReach / ZoomInfo — 采购最高负责人，可直接触达</div>
</div>

<div class="person">
<div class="pname">🔥 Kurt Benavides — Head of Procurement Operations</div>
<div class="pemail">📧 kurt.benavides@bhp.com（推测，AroundDeal有记录）</div>
<div class="psource">来源: AroundDeal — 采购运营主管，负责供应商入库</div>
</div>

<div class="person">
<div class="pname">Tajinder Bedi — Senior Procurement Manager</div>
<div class="plinkedin">🔗 au.linkedin.com/in/tejinder-bedi</div>
<div class="psource">来源: LinkedIn — 高级采购经理，BHP内部供应链对接人</div>
</div>
</div>

<h3 class="section">二、🇦🇺 Fortescue Metals Group — 澳洲第三大铁矿</h3>
<div class="card">
<div class="name"><span class="p0">P0</span> Fortescue Metals Group</div>
<div class="meta">📍 珀斯/Pilbara WA | 👷 2万+工人</div>
<div class="meta">供应商注册: suppliers.fortescue.com</div>

<div class="person">
<div class="pname">🔥 Dara Byrne — Group Manager, Contracts & Procurement - Projects</div>
<div class="pemail">📧 dara.byrne@fmgl.com.au（推测，Wiza可见d*****@fmgl***.com.au，RocketReach有1邮箱记录）</div>
<div class="plinkedin">🔗 au.linkedin.com/in/dara-byrne-44a8b846</div>
<div class="psource">来源: RocketReach(1邮箱) / Wiza(部分可见) / ZoomInfo — 合同与采购项目群经理，最关键决策人</div>
</div>

<div class="person">
<div class="pname">Mark Cocks — Senior Contracts & Procurement Specialist</div>
<div class="pemail">📧 m*****@fmgl.com.au（Wiza可见部分）</div>
<div class="psource">来源: LinkedIn/Wiza — 采购执行层</div>
</div>
</div>

<h3 class="section">三、🇦🇺 Rio Tinto — 全球矿业巨头</h3>
<div class="card">
<div class="name"><span class="p0">P0</span> Rio Tinto</div>
<div class="meta">📍 墨尔本/Pilbara WA | 👷 4万+工人</div>
<div class="meta">供应商门户: riotinto.com/en/suppliers | 邮箱格式: firstname.lastname@riotinto.com</div>
<div class="insight-box">建议在LinkedIn搜索 "Rio Tinto Procurement Manager Camp" 或 "Rio Tinto Accommodation Procurement" 找到对口联系人后使用邮箱格式推测。</div>
</div>

<h3 class="section">四、🇳🇿 Kāinga Ora — 新西兰政府住房署</h3>
<div class="card">
<div class="name"><span class="p0">P0</span> Kāinga Ora — Homes and Communities</div>
<div class="meta">📍 新西兰全国 | 🏢 最大政府住房机构</div>
<div class="meta">招标: tenderlink.com/kaingaora | gets.govt.nz</div>

<div class="person">
<div class="pname">🔥 Andrea Morton — Director Procurement and Supplier Management</div>
<div class="pemail">📧 andrea.morton@kaingaora.govt.nz（推测，Wiza可见a*****@kainga***.govt.nz）</div>
<div class="psource">来源: Wiza / NZ政府公开活动记录 — 采购与供应商管理总监，模块化住房采购最高决策人</div>
</div>
</div>

<h3 class="section">五、政府采购招标平台（批量线索）</h3>
<table>
<tr><th>平台</th><th>区域</th><th>URL</th><th>搜索词</th></tr>
<tr><td>AusTender</td><td>🇦🇺 联邦</td><td>austender.gov.au</td><td>"prefabricated" "modular"</td></tr>
<tr><td>tenders.nsw</td><td>🇦🇺 NSW</td><td>tenders.nsw.gov.au</td><td>"relocatable" "temporary"</td></tr>
<tr><td>tenders.vic</td><td>🇦🇺 VIC</td><td>tenders.vic.gov.au</td><td>"modular building"</td></tr>
<tr><td>tenders.wa</td><td>🇦🇺 WA</td><td>tenders.wa.gov.au</td><td>"camp accommodation"</td></tr>
<tr><td>qtenders</td><td>🇦🇺 QLD</td><td>qtenders.qld.gov.au</td><td>"temporary housing"</td></tr>
<tr><td>GETS + tenderlink</td><td>🇳🇿 全国</td><td>gets.govt.nz</td><td>"modular" "housing"</td></tr>
</table>

<h3 class="section">六、触达策略</h3>
<table>
<tr><th>顺序</th><th>目标</th><th>联系人</th><th>触达路径</th></tr>
<tr><td>1 🔥</td><td>Fortescue</td><td>Dara Byrne</td><td>LinkedIn加好友 → InMail → 同时注册suppliers.fortescue.com</td></tr>
<tr><td>2 🔥</td><td>BHP</td><td>Luke King / Kurt Benavides</td><td>LinkedIn加好友+注册bhp.com/suppliers+Ariba</td></tr>
<tr><td>3 🔥</td><td>Kāinga Ora</td><td>Andrea Morton</td><td>LinkedIn加好友+注册tenderlink.com/kaingaora</td></tr>
<tr><td>4 🔥</td><td>Rio Tinto</td><td>采购部</td><td>供应商门户注册+LinkedIn搜对口人</td></tr>
<tr><td>5</td><td>6个招标平台</td><td>-</td><td>免费注册+关键词RSS订阅</td></tr>
</table>

<div class="footer">
<p>买家情报引擎 v5 | 数据源: LinkedIn / RocketReach / Wiza / ZoomInfo / AroundDeal | 2026-05-20</p>
<p>✅ 4家终端买家 | 6位真实联系人 | 邮箱基于公开信息推测，建议LinkedIn核实</p>
<p>🚫 本报告仅含需求方，不含任何供货方/供应商</p>
</div>
</body></html>"""

os.makedirs(OUT, exist_ok=True)
out = os.path.join(OUT, "钢结构折叠房屋终端买家联系人.pdf")
print(f"🖨️ {out}")
r = render(body_html=HTML, output_path=out, content_type="chinese",
           verify_keywords=["Luke King", "Dara Byrne", "Andrea Morton", "BHP", "Fortescue", "Kāinga"])
if r.get("status") == "ok":
    print(f"✅ {os.path.getsize(out)//1024}KB | {verify_pdf(out, keywords=['Luke','Dara','Andrea'])}")
