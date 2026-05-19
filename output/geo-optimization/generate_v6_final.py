#!/usr/bin/env python3
"""钢结构折叠集成房屋 — 澳新终端买家完整版PDF v6（含酒店）"""
import sys, os
sys.path.insert(0, "/home/sayelf/.openclaw/workspace/skills/art-agent/modules/shared")
from render_engine import render, verify_pdf
OUT = "/home/sayelf/.openclaw/workspace/output/geo-optimization"

HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page{size:A4;margin:20mm 18mm;@bottom-center{content:"钢结构折叠房屋 — 终端买家 | 太一跨境贸易Agent";font-size:8pt;color:#8899aa;}}
@font-face{font-family:'Noto';src:url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');}
body{font-family:'Noto','Microsoft YaHei',sans-serif;color:#1a2a3a;line-height:1.6;font-size:10pt;}
.cover{page-break-after:always;text-align:center;padding-top:80px;}
.cover .tag{display:inline-block;background:#c0392b;color:#fff;padding:6px 20px;font-size:10pt;letter-spacing:3px;margin-bottom:30px;}
.cover h1{font-size:26pt;color:#0d1b2a;margin:20px 0;}
.cover h2{font-size:16pt;color:#c0392b;font-weight:normal;}
.cover .divider{width:60px;height:3px;background:#c0392b;margin:20px auto;}
.cover .info{color:#8899aa;font-size:9pt;line-height:2;}
h3.section{background:#0d1b2a;color:#fff;padding:8px 14px;font-size:12pt;margin:24px 0 12px;border-left:4px solid #c0392b;}
h3.section-hotels{background:#1a3a2a;color:#f07a1f;padding:8px 14px;font-size:12pt;margin:24px 0 12px;border-left:4px solid #f07a1f;}
h4{color:#0d1b2a;font-size:11pt;margin:16px 0 6px;border-bottom:1px solid #e0e8f0;padding-bottom:4px;}
.card{border:2px solid #d0d8e0;border-radius:6px;padding:12px 16px;margin:10px 0;page-break-inside:avoid;}
.card .name{font-size:12pt;font-weight:bold;color:#0d1b2a;}
.card .meta{font-size:8.5pt;color:#667788;margin:2px 0;}
.card-hotels{border:2px solid #e0c8a0;border-radius:6px;padding:12px 16px;margin:10px 0;page-break-inside:avoid;background:#fffcf5;}
.card-hotels .name{font-size:12pt;font-weight:bold;color:#6b4c2a;}
.person{border:1px solid #b8d8b8;border-radius:4px;background:#f5fff5;padding:8px 12px;margin:6px 0;}
.person .pname{font-size:11pt;font-weight:bold;color:#1a5a1a;}
.person .pemail{font-size:9pt;color:#2a7fc9;font-family:monospace;margin:2px 0;}
.person .plinkedin{font-size:8pt;color:#0a66c2;}
.person .psource{font-size:8pt;color:#888;}
.p0{display:inline-block;background:#e74c3c;color:#fff;padding:0 6px;border-radius:3px;font-size:7pt;font-weight:bold;}
.p1{display:inline-block;background:#f39c12;color:#fff;padding:0 6px;border-radius:3px;font-size:7pt;font-weight:bold;}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:9pt;}
th{background:#0d1b2a;color:#fff;padding:6px 8px;text-align:center;}
td{padding:5px 8px;border-bottom:1px solid #e0e8f0;}
tr:nth-child(even) td{background:#f5f8fc;}
.insight-box{background:#f0f4f8;border-left:4px solid #c0392b;padding:10px 14px;margin:10px 0;font-size:9pt;}
.insight-hotels{background:#fffaf0;border-left:4px solid #f07a1f;padding:10px 14px;margin:10px 0;font-size:9pt;}
.footer{margin-top:20px;padding-top:10px;border-top:1px solid #d0d8e0;font-size:8pt;color:#8899aa;}
</style></head><body>
<div class="cover">
<div class="tag">终端买家联系人报告 v6</div>
<h1>钢结构折叠集成房屋</h1>
<h2>🇦🇺 澳大利亚 · 🇳🇿 新西兰 — 全部10家终端买家</h2>
<div class="divider"></div>
<div class="info">
<p>报告日期：2026-05-20 | 矿业3家 + 酒店5家 + 政府/住房署2家</p>
<p>数据来源：LinkedIn / RocketReach / Wiza / ZoomInfo / CBRE / 酒店管理媒体</p>
</div>
</div>

<h3 class="section">一、🇦🇺 矿业公司（最大需求方）</h3>
<div class="card">
<div class="name"><span class="p0">P0</span> BHP Billiton</div>
<div class="meta">墨尔本/Pilbara WA | 5万+工人 | Fleetwood是现有模块营地供应商</div>
<div class="person"><div class="pname">Luke King — Head of Procurement</div><div class="pemail">📧 luke.king@bhp.com（推测，RocketReach有2邮箱+2电话记录）</div><div class="plinkedin">🔗 au.linkedin.com/in/lukeking</div></div>
<div class="person"><div class="pname">Kurt Benavides — Head of Procurement Operations</div><div class="pemail">📧 kurt.benavides@bhp.com（推测）</div></div>
<div class="person"><div class="pname">Tajinder Bedi — Senior Procurement Manager</div><div class="plinkedin">🔗 au.linkedin.com/in/tejinder-bedi</div></div>
<div>供应商注册: bhp.com/suppliers | 采购系统: bhp.procurement.ariba.com</div>
</div>
<div class="card">
<div class="name"><span class="p0">P0</span> Fortescue Metals Group</div>
<div class="meta">珀斯/Pilbara WA | 2万+工人</div>
<div class="person"><div class="pname">Dara Byrne — Group Manager, Contracts & Procurement - Projects</div><div class="pemail">📧 dara.byrne@fmgl.com.au（推测，Wiza可见部分，RocketReach有1邮箱）</div><div class="plinkedin">🔗 au.linkedin.com/in/dara-byrne-44a8b846</div></div>
<div class="person"><div class="pname">Mark Cocks — Sr Contracts & Procurement Specialist</div><div class="pemail">📧 m*****@fmgl.com.au</div></div>
<div>供应商中心: suppliers.fortescue.com</div>
</div>
<div class="card">
<div class="name"><span class="p0">P0</span> Rio Tinto</div>
<div class="meta">墨尔本/Pilbara WA | 4万+工人</div>
<div>供应商门户: riotinto.com/en/suppliers | LinkedIn搜索Rio Tinto Procurement Manager Camp</div>
</div>

<h3 class="section-hotels">二、🏨 酒店集团（新增！模块化酒店大趋势）</h3>
<div class="insight-hotels"><strong>趋势信号：</strong>Hilton已在澳洲Townsville建设首个190间模块化酒店（2026年完工），标志着澳洲酒店业开始大规模接受模块化建筑。折叠房屋在度假村/生态酒店/员工宿舍场景有明确需求。</div>

<div class="card-hotels">
<div class="name"><span class="p0">P0</span> Accor Pacific — 澳洲新西兰最大酒店集团</div>
<div class="meta">300+酒店 | 覆盖所有档次 | 模块化酒店扩张中</div>
<div>采购对接：LinkedIn搜索"Accor Pacific Development Manager"找到开发/采购负责人</div>
<div>官网: accor.com</div>
</div>

<div class="card-hotels">
<div class="name"><span class="p0">P0</span> Hilton Australia — 模块化酒店先行者</div>
<div class="meta">已签Townsville首个模块化酒店190间 (2026年完工) | 已验证模块化酒店可行</div>
<div>采购对接：LinkedIn搜索"Hilton Australia Development Director"</div>
<div>来源: hotelmanagement.com.au / builtoffsite.com.au</div>
</div>

<div class="card-hotels">
<div class="name"><span class="p1">P1</span> Meriton Group — 澳洲最大酒店业主</div>
<div class="meta">6,211间客房 | 持续扩张 | 酒店客房模块化采购潜力大</div>
<div>官网: meriton.com.au | LinkedIn搜索"Meriton Procurement"</div>
<div>来源: CBRE Top 10 Hotel Owners 2025报告</div>
</div>

<div class="card-hotels">
<div class="name"><span class="p1">P1</span> NZ Hotel Holdings</div>
<div class="meta">NZ Super Fund + Russell Property + Lockwood联合体 | 专注新西兰酒店资产转型</div>
<div>官网: nzhotelholdings.co.nz | 可直接通过官网联系</div>
</div>

<div class="card-hotels">
<div class="name"><span class="p1">P1</span> NZ Horizon Hospitality Group</div>
<div class="meta">专门开发新西兰南岛新一代酒店 | 看中模块化技术</div>
<div>官网: nzhhg.co.nz | 新西兰南岛旅游住宿缺口巨大</div>
</div>

<h3 class="section">三、🇳🇿 政府住房署</h3>
<div class="card">
<div class="name"><span class="p0">P0</span> Kāinga Ora — Homes and Communities</div>
<div class="meta">新西兰最大政府住房机构</div>
<div class="person"><div class="pname">Andrea Morton — Director Procurement & Supplier Management</div><div class="pemail">📧 andrea.morton@kaingaora.govt.nz（推测，Wiza可见部分邮箱）</div></div>
<div>供应商注册: kaingaora.govt.nz/suppliers | 招标: tenderlink.com/kaingaora</div>
</div>

<h3 class="section">四、政府采购招标平台</h3>
<table><tr><th>平台</th><th>区域</th><th>URL</th></tr>
<tr><td>AusTender</td><td>🇦🇺 联邦</td><td>austender.gov.au</td></tr>
<tr><td>tenders.nsw/vic/wa/qld</td><td>🇦🇺 各州</td><td>tenders.nsw.gov.au 等</td></tr>
<tr><td>GETS + tenderlink</td><td>🇳🇿 全国</td><td>gets.govt.nz</td></tr></table>

<h3 class="section">五、触达行动</h3>
<table><tr><th>顺序</th><th>目标</th><th>联系人/路径</th></tr>
<tr><td>1 🔥</td><td>Fortescue</td><td>Dara Byrne LinkedIn + suppliers.fortescue.com注册</td></tr>
<tr><td>2 🔥</td><td>BHP</td><td>Luke King LinkedIn + bhp.com/suppliers + Ariba注册</td></tr>
<tr><td>3 🔥</td><td>Hilton</td><td>LinkedIn搜Hilton Australia Development + 模块化酒店案例</td></tr>
<tr><td>4 🔥</td><td>Accor</td><td>LinkedIn搜Accor Pacific Development Manager</td></tr>
<tr><td>5 🔥</td><td>Kāinga Ora</td><td>Andrea Morton LinkedIn + tenderlink注册</td></tr>
<tr><td>6</td><td>Rio Tinto/招标平台</td><td>供应商门户注册+关键词RSS</td></tr>
<tr><td>7</td><td>Meriton/NZ Hotel/NZ Horizon</td><td>官网联系+LinkedIn搜对口人</td></tr></table>

<div class="footer">
<p>买家情报引擎 v6 | 🇦🇺🇳🇿 共10家终端买家: 矿业3 + 酒店5 + 政府2 | 2026-05-20</p>
<p>✅ 不含任何供货方/供应商 | 联系方式基于公开信息，建议LinkedIn核实后触达</p>
</div>
</body></html>"""

os.makedirs(OUT, exist_ok=True)
out = os.path.join(OUT, "钢结构折叠房屋终端买家联系人.pdf")
print(f"🖨️ {out}")
r = render(body_html=HTML, output_path=out, content_type="chinese",
           verify_keywords=["BHP", "Fortescue", "Accor", "Hilton", "Kāinga", "Meriton"])
if r.get("status") == "ok":
    print(f"✅ {os.path.getsize(out)//1024}KB | {verify_pdf(out, keywords=['BHP','Hilton','Accor'])}")
