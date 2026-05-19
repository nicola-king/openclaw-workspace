#!/usr/bin/env python3
"""钢结构折叠集成房屋 — 纯需求方PDF v3"""
import sys, os
sys.path.insert(0, "/home/sayelf/.openclaw/workspace/skills/art-agent/modules/shared")
from render_engine import render, verify_pdf

OUT = "/home/sayelf/.openclaw/workspace/output/geo-optimization"

HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page{size:A4;margin:20mm 18mm;@bottom-center{content:"太一跨境贸易 Agent — 需求方报告 | 钢结构折叠集成房屋";font-size:8pt;color:#8899aa;}}
@font-face{font-family:'Noto';src:url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');}
body{font-family:'Noto','Microsoft YaHei',sans-serif;color:#1a2a3a;line-height:1.6;font-size:10pt;}
.cover{page-break-after:always;text-align:center;padding-top:100px;}
.cover .tag{display:inline-block;background:#c0392b;color:#fff;padding:6px 20px;font-size:10pt;letter-spacing:3px;margin-bottom:30px;}
.cover h1{font-size:26pt;color:#0d1b2a;margin:20px 0;}
.cover h2{font-size:16pt;color:#c0392b;font-weight:normal;margin:10px 0 30px;}
.cover .divider{width:60px;height:3px;background:#c0392b;margin:20px auto;}
.cover .info{color:#8899aa;font-size:9pt;line-height:2;}
h3.section{background:#0d1b2a;color:#fff;padding:8px 14px;font-size:12pt;margin:24px 0 12px;border-left:4px solid #c0392b;}
h3.section-comp{background:#1a1a2e;color:#f39c12;padding:8px 14px;font-size:12pt;margin:24px 0 12px;border-left:4px solid #f39c12;}
h4{color:#0d1b2a;font-size:11pt;margin:16px 0 6px;border-bottom:1px solid #e0e8f0;padding-bottom:4px;}
.card{border:1px solid #d0d8e0;border-radius:4px;padding:10px 14px;margin:8px 0;page-break-inside:avoid;}
.card .name{font-size:11pt;font-weight:bold;color:#0d1b2a;}
.card .meta{font-size:8.5pt;color:#667788;margin:2px 0;}
.card .detail{font-size:9pt;margin:4px 0;}
.card .url{color:#2a7fc9;word-break:break-all;font-size:8.5pt;}
.card-comp{border:1px solid #e0d0a0;border-radius:4px;padding:8px 12px;margin:5px 0;page-break-inside:avoid;background:#fefaf0;}
.card-comp .name{font-size:10pt;font-weight:bold;color:#8a6d2b;}
.card-comp .detail{font-size:8.5pt;margin:3px 0;color:#666;}
.p0{display:inline-block;background:#e74c3c;color:#fff;padding:1px 8px;border-radius:3px;font-size:8pt;font-weight:bold;}
.p1{display:inline-block;background:#f39c12;color:#fff;padding:1px 8px;border-radius:3px;font-size:8pt;font-weight:bold;}
.p2{display:inline-block;background:#3498db;color:#fff;padding:1px 8px;border-radius:3px;font-size:8pt;font-weight:bold;}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:9pt;}
th{background:#0d1b2a;color:#fff;padding:6px 8px;text-align:center;}
td{padding:5px 8px;border-bottom:1px solid #e0e8f0;}
tr:nth-child(even) td{background:#f5f8fc;}
.insight-box{background:#f0f4f8;border-left:4px solid #c0392b;padding:10px 14px;margin:10px 0;font-size:9pt;}
.insight-box-comp{background:#fefaf0;border-left:4px solid #f39c12;padding:10px 14px;margin:10px 0;font-size:9pt;}
.footer{margin-top:20px;padding-top:10px;border-top:1px solid #d0d8e0;font-size:8pt;color:#8899aa;}
</style></head><body>

<div class="cover">
<div class="tag">需求方买家报告</div>
<h1>钢结构折叠集成房屋</h1>
<h2>🇦🇺 澳大利亚 · 🇳🇿 新西兰 纯需求方画像</h2>
<div class="divider"></div>
<div class="info">
<p>报告日期：2026-05-19</p>
<p>定义：需求方 = 终端使用/采购折叠房屋的主体，非供货方</p>
<p>数据来源：各公司官网 / 供应商门户 / 政府采购平台 / 公开情报</p>
</div>
</div>

<!-- ===== SECTION 1: DEMAND TYPES ===== -->
<h3 class="section">一、需求方类型总览</h3>

<table>
<tr><th>需求方类型</th><th>国家</th><th>采购量</th><th>利润</th><th>决策周期</th><th>触达方式</th><th>优先级</th></tr>
<tr><td><strong>大型矿业公司</strong></td><td>🇦🇺</td><td>🔴 批量营地</td><td>🔴 高</td><td>3-6月</td><td>供应商门户注册</td><td><span class="p0">P0</span></td></tr>
<tr><td><strong>政府/公共部门</strong></td><td>🇦🇺🇳🇿</td><td>🔴 批量招标</td><td>🟡 中</td><td>6-12月</td><td>招标平台</td><td><span class="p0">P0</span></td></tr>
<tr><td><strong>中小型矿业承包商</strong></td><td>🇦🇺</td><td>🟡 单次/小批量</td><td>🟡 中</td><td>1-3月</td><td>直接联系</td><td><span class="p1">P1</span></td></tr>
<tr><td><strong>地产开发商</strong></td><td>🇦🇺🇳🇿</td><td>🟡 项目制</td><td>🟡 中</td><td>3-6月</td><td>直接联系</td><td><span class="p1">P1</span></td></tr>
<tr><td><strong>个人/小企业</strong></td><td>🇦🇺🇳🇿</td><td>🟢 单品</td><td>🟢 低</td><td>1-3月</td><td>B2C平台/广告</td><td><span class="p2">P2</span></td></tr>
</table>

<!-- ===== SECTION 2: PURE DEMAND SIDE ===== -->
<h3 class="section">二、🇦🇺 澳大利亚 — 核心需求方</h3>

<h4>类型A：大型矿业公司（最大需求方）<span class="p0">P0</span></h4>
<div class="insight-box">
澳洲矿业营地是折叠房屋最大应用场景。Pilbara矿区工人总数超10万，所有营房需求持续5-10年。折叠房屋1箱=6套，运输效率3倍于传统模块，运到偏远矿区的成本优势巨大。
</div>

<div class="card">
<div class="name"><span class="p0">P0</span> BHP Billiton — 全球最大矿业公司</div>
<div class="meta">📍 总部墨尔本 | 👷 澳洲工人5万+ | 🏔️ Pilbara/NSW/QLD</div>
<div class="detail">需求：矿工营地住宿模块，持续采购</div>
<div class="url">供应商注册: bhp.com/suppliers | 采购系统: Ariba (bhp.procurement.ariba.com)</div>
<div class="url">Local Buying Program: app.c-res.com.au（小型供应商渠道）</div>
</div>

<div class="card">
<div class="name"><span class="p0">P0</span> Rio Tinto — 全球矿业巨头</div>
<div class="meta">📍 总部墨尔本 | 👷 澳洲工人4万+ | 🏔️ Pilbara WA</div>
<div class="detail">需求：矿工营地+远程基建住宿，长期大批量</div>
<div class="url">供应商门户: riotinto.com/en/suppliers</div>
</div>

<div class="card">
<div class="name"><span class="p0">P0</span> Fortescue Metals Group</div>
<div class="meta">📍 珀斯 East Perth | 👷 澳洲工人2万+ | 🏔️ Pilbara WA</div>
<div class="detail">需求：矿工营房+营地设施，快速部署需求大</div>
<div class="url">供应商中心: suppliers.fortescue.com</div>
<div class="detail"><strong>采购决策人线索：</strong> Dara Byrne (Group Manager, Contracts & Procurement - Projects) | Mark Cocks (Senior Contracts & Procurement Specialist) — 可通过LinkedIn触达</div>
</div>

<div class="card">
<div class="name"><span class="p1">P1</span> Newcrest Mining</div>
<div class="meta">📍 👷 澳洲1万+ | 🏔️ NSW/WA</div>
<div class="detail">需求：矿工营地+基建</div>
<div class="url">供应商注册: newcrest.com/suppliers</div>
</div>

<h4>类型B：政府采购/公共部门<span class="p0">P0</span></h4>
<div class="insight-box">
政府是澳洲最大的模块建筑单一采购方，用于应急住房/国防/学校/医疗。所有招标免费订阅。
</div>
<table>
<tr><th>平台</th><th>领域</th><th>搜索关键词</th></tr>
<tr><td>AusTender (austender.gov.au)</td><td>联邦政府 — 国防/应急/NBN</td><td>"prefabricated building" "modular accommodation"</td></tr>
<tr><td>tenders.nsw.gov.au</td><td>新州 — 学校/医疗/应急</td><td>"relocatable classroom" "temporary building"</td></tr>
<tr><td>tenders.vic.gov.au</td><td>维州 — 应急住房/基建</td><td>"temporary housing" "modular building"</td></tr>
<tr><td>qtenders.qld.gov.au</td><td>昆州 — 灾害重建/学校</td><td>"temporary housing" "prefab accommodation"</td></tr>
<tr><td>tenders.wa.gov.au</td><td>西澳 — 矿业基建/应急</td><td>"camp accommodation" "transportable building"</td></tr>
</table>

<h4>类型C：地产开发商<span class="p1">P1</span></h4>
<table>
<tr><th>开发商</th><th>领域</th><th>触达方式</th></tr>
<tr><td>Lendlease</td><td>大型综合开发</td><td>lendlease.com → 供应商注册</td></tr>
<tr><td>Mirvac</td><td>住宅/商业开发</td><td>mirvac.com → 供应商</td></tr>
<tr><td>Stockland</td><td>住宅社区开发</td><td>stockland.com.au → 采购</td></tr>
<tr><td>Frasers Property</td><td>住宅/商业</td><td>frasersproperty.com</td></tr>
</table>

<!-- ===== SECTION 3: NZ DEMAND SIDE ===== -->
<h3 class="section">三、🇳🇿 新西兰 — 核心需求方</h3>

<h4>类型A：政府住房署<span class="p0">P0</span></h4>
<div class="card">
<div class="name"><span class="p0">P0</span> Kāinga Ora — Homes and Communities</div>
<div class="meta">📍 新西兰全国 | 🏢 政府住房机构</div>
<div class="detail">新西兰最大住房供应商，负责保障房/社会住房建设。模块化建筑是其解决住房危机的核心方案之一。</div>
<div class="url">🌐 kaingaora.govt.nz | 供应商注册: kaingaora.govt.nz/suppliers</div>
</div>

<h4>类型B：政府采购平台<span class="p0">P0</span></h4>
<table>
<tr><th>平台</th><th>领域</th><th>搜索词</th></tr>
<tr><td>NZ Government Procurement (getting.govt.nz)</td><td>全国政府采购</td><td>"modular building" "transportable" "housing"</td></tr>
<tr><td>MBIE (mbie.govt.nz)</td><td>商业/创新/就业部采购</td><td>"emergency housing" "temporary accommodation"</td></tr>
</table>

<h4>类型C：地产开发商<span class="p1">P1</span></h4>
<table>
<tr><th>开发商</th><th>领域</th><th>触达方式</th></tr>
<tr><td>Fletcher Building</td><td>NZ最大建筑集团</td><td>fletcherbuilding.com → 供应链</td></tr>
<tr><td>Tawera Group</td><td>30年房地产开发+模块化</td><td>taweragroup.com</td></tr>
<tr><td>Oyster Property Group</td><td>商业地产</td><td>oysterproperty.com</td></tr>
</table>

<!-- ===== SECTION 4: DEMAND SCENARIOS ===== -->
<h3 class="section">四、六类需求场景匹配</h3>

<table>
<tr><th>场景</th><th>国家</th><th>需求量</th><th>折叠房屋优势</th><th>典型需求方</th></tr>
<tr><td>🏔️ 矿业营地</td><td>🇦🇺</td><td>🔴 最大</td><td>1箱=6套，运费省60%</td><td>BHP/Rio Tinto/Fortescue</td></tr>
<tr><td>🏛️ 政府采购</td><td>🇦🇺🇳🇿</td><td>🔴 大</td><td>快速部署+合规</td><td>AusTender/Kāinga Ora</td></tr>
<tr><td>🏘️ 保障房</td><td>🇦🇺🇳🇿</td><td>🟡 中</td><td>成本低30%+工期短50%</td><td>Kāinga Ora/州政府</td></tr>
<tr><td>🏚️ 灾后重建</td><td>🇦🇺🇳🇿</td><td>🟡 中</td><td>72小时部署</td><td>州政府/地方议会</td></tr>
<tr><td>🏨 旅游度假</td><td>🇳🇿</td><td>🟢 小</td><td>移动+环保</td><td>旅游开发商</td></tr>
<tr><td>🏠 个人自建</td><td>🇦🇺🇳🇿</td><td>🟢 单品</td><td>性价比高</td><td>个人买家</td></tr>
</table>

<!-- ===== SECTION 5: COMPETITOR ANALYSIS ===== -->
<h3 class="section-comp">五、竞品分析参考（供货方 — 非需求方）</h3>
<div class="insight-box-comp">
以下是与折叠房屋同领域的供货方/竞争对手，非需求方。标记在此用于竞品情报参考。
</div>

<table>
<tr><th>公司</th><th>国家</th><th>定位</th><th>与你关系</th></tr>
<tr><td>Ausco Modular</td><td>🇦🇺</td><td>模块建筑商（矿业/政府）</td><td>竞争/合作</td></tr>
<tr><td>ATCO Structures</td><td>🇦🇺</td><td>75年全球模块巨头</td><td>竞争对手</td></tr>
<tr><td>Northern Transportables</td><td>🇦🇺 NT/WA</td><td>矿业营地建筑商</td><td>竞品/可合作</td></tr>
<tr><td>EcoPrestige</td><td>🇦🇺</td><td>矿工住宿专业商</td><td>竞品</td></tr>
<tr><td>Australian Portable Camps</td><td>🇦🇺</td><td>营地方案垂直整合</td><td>竞品</td></tr>
<tr><td>Kiwi Modular</td><td>🇳🇿</td><td>模块化建筑</td><td>竞品</td></tr>
<tr><td>Expanders NZ</td><td>🇳🇿</td><td>可扩展便携建筑（350+单元）</td><td>直接竞品</td></tr>
<tr><td>Modern Modular NZ</td><td>🇳🇿</td><td>FE-30折叠房屋</td><td>直接竞品</td></tr>
<tr><td>Steeltec NZ</td><td>🇳🇿</td><td>钢框架制造商</td><td>供应链合作</td></tr>
<tr><td>ANZ Modular</td><td>🇳🇿</td><td>预制钢结构</td><td>竞品</td></tr>
<tr><td>Cargo Connect</td><td>🇦🇺</td><td>中国→澳洲物流</td><td>物流合作</td></tr>
<tr><td>LGS Solutions</td><td>🇦🇺</td><td>钢结构预制件</td><td>供应链</td></tr>
</table>

<!-- ===== SECTION 6: ACTION PLAN ===== -->
<h3 class="section">六、需求方触达行动建议</h3>

<h4>P0 — 本周（供应商门户注册）</h4>
<table>
<tr><th>顺序</th><th>需求方</th><th>动作</th></tr>
<tr><td>1 🔥</td><td><strong>BHP</strong></td><td>bhp.com/suppliers → 注册供应商 + Ariba注册</td></tr>
<tr><td>2 🔥</td><td><strong>Fortescue</strong></td><td>suppliers.fortescue.com → 注册供应商 + LinkedIn联系Dara Byrne</td></tr>
<tr><td>3 🔥</td><td><strong>Rio Tinto</strong></td><td>riotinto.com/en/suppliers → 注册</td></tr>
<tr><td>4 🔥</td><td><strong>AusTender</strong></td><td>注册+关键词RSS订阅</td></tr>
<tr><td>5 🔥</td><td><strong>Kāinga Ora NZ</strong></td><td>kaingaora.govt.nz/suppliers → 注册</td></tr>
</table>

<h4>P1 — 本月</h4>
<table>
<tr><th>顺序</th><th>需求方</th><th>动作</th></tr>
<tr><td>6</td><td>5个州级招标平台注册</td><td>NSW/VIC/QLD/WA/NZ Procurement</td></tr>
<tr><td>7</td><td>Newcrest Mining</td><td>供应商注册</td></tr>
<tr><td>8</td><td>Lendlease / Mirvac / Stockland</td><td>开发商供应商注册</td></tr>
<tr><td>9</td><td>Fletcher Building NZ</td><td>供应链注册</td></tr>
</table>

<h4>P2 — 持续</h4>
<table>
<tr><th>顺序</th><th>动作</th></tr>
<tr><td>10</td><td>NCC/CodeMark/NZBC认证评估启动</td></tr>
<tr><td>11</td><td>竞品产品监测（Expanders/FE-30等）</td></tr>
<tr><td>12</td><td>月度招标情报汇总</td></tr>
</table>

<div class="footer">
<p>报告生成：太一跨境贸易 Agent v3 — 纯需求方版本 | 数据源：各公司官网/供应商门户/政府采购</p>
<p>✅ 需求方 = 终端买家 | ❌ 供货方已移至竞品分析参考 | 联系方式需通过供应商门户注册获取</p>
</div>
</body></html>"""

os.makedirs(OUT, exist_ok=True)
out = os.path.join(OUT, "钢结构折叠房屋需求方买家.pdf")
print(f"🖨️ 生成: {out}")
r = render(body_html=HTML, output_path=out, content_type="chinese",
           verify_keywords=["BHP", "Rio Tinto", "Fortescue", "Kāinga Ora", "AusTender"])
if r.get("status") == "ok":
    print(f"✅ {os.path.getsize(out)//1024}KB | 验证: {verify_pdf(out, keywords=['BHP','Fortescue','Kāinga','矿业'])}")
else:
    print(f"❌ {r}")
