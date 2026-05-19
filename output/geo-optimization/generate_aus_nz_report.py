#!/home/sayelf/.local/venvs/scraper/bin/python3
"""
澳大利亚 & 新西兰 — 钢结构折叠集成房屋买家情报报告
使用 art-agent render_engine 生成 PDF
"""

import sys, os, json
sys.path.insert(0, "/home/sayelf/.openclaw/workspace/skills/art-agent/modules/shared")
from render_engine import render, verify_pdf

OUTPUT_DIR = "/home/sayelf/.openclaw/workspace/output/geo-optimization"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
@page {
  size: A4;
  margin: 20mm 18mm;
  @bottom-center {
    content: "太一跨境贸易 Agent — 买家情报报告";
    font-size: 8pt;
    color: #8899aa;
  }
}
@font-face {
  font-family: 'NotoSansCJK';
  src: url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');
}
body {
  font-family: 'NotoSansCJK', 'Microsoft YaHei', sans-serif;
  color: #1a2a3a;
  line-height: 1.6;
  font-size: 10pt;
}

/* Cover */
.cover {
  page-break-after: always;
  text-align: center;
  padding-top: 120px;
}
.cover .tag {
  display: inline-block;
  background: #0d1b2a;
  color: #f07a1f;
  padding: 6px 20px;
  font-size: 10pt;
  letter-spacing: 3px;
  margin-bottom: 30px;
}
.cover h1 {
  font-size: 26pt;
  color: #0d1b2a;
  margin: 20px 0;
}
.cover h2 {
  font-size: 16pt;
  color: #f07a1f;
  font-weight: normal;
  margin: 10px 0 30px;
}
.cover .info {
  color: #8899aa;
  font-size: 9pt;
  line-height: 2;
}
.cover .divider {
  width: 60px; height: 3px;
  background: #f07a1f;
  margin: 20px auto;
}

/* Section headers */
h3.section {
  background: #0d1b2a;
  color: #f07a1f;
  padding: 8px 14px;
  font-size: 12pt;
  margin: 24px 0 12px;
  border-left: 4px solid #f07a1f;
}
h4 {
  color: #0d1b2a;
  font-size: 11pt;
  margin: 16px 0 6px;
  border-bottom: 1px solid #e0e8f0;
  padding-bottom: 4px;
}

/* Buyer cards */
.buyer-card {
  border: 1px solid #d0d8e0;
  border-radius: 4px;
  padding: 10px 14px;
  margin: 8px 0;
  page-break-inside: avoid;
}
.buyer-card .name {
  font-size: 11pt;
  font-weight: bold;
  color: #0d1b2a;
}
.buyer-card .meta {
  font-size: 8.5pt;
  color: #667788;
  margin: 2px 0;
}
.buyer-card .detail {
  font-size: 9pt;
  margin: 4px 0;
}
.buyer-card .url { color: #2a7fc9; word-break: break-all; font-size: 8.5pt; }
.badge-a, .badge-b, .badge-c {
  display: inline-block;
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 8pt;
  font-weight: bold;
}
.badge-a { background: #2ecc71; color: #fff; }
.badge-b { background: #f39c12; color: #fff; }
.badge-c { background: #e74c3c; color: #fff; }

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0;
  font-size: 9pt;
}
th {
  background: #0d1b2a;
  color: #f07a1f;
  padding: 6px 8px;
  text-align: center;
}
td {
  padding: 5px 8px;
  border-bottom: 1px solid #e0e8f0;
}
tr:nth-child(even) td { background: #f5f8fc; }

/* Market insight */
.insight-box {
  background: #f0f4f8;
  border-left: 4px solid #f07a1f;
  padding: 10px 14px;
  margin: 10px 0;
  font-size: 9pt;
}

.footer {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #d0d8e0;
  font-size: 8pt;
  color: #8899aa;
}
</style>
</head>
<body>

<!-- ===== COVER ===== -->
<div class="cover">
  <div class="tag">买家情报报告</div>
  <h1>钢结构折叠集成房屋</h1>
  <h2>🇦🇺 澳大利亚 · 🇳🇿 新西兰 市场买家情报</h2>
  <div class="divider"></div>
  <div class="info">
    <p>报告日期：2026-05-19</p>
    <p>数据来源：Trade.gov / 各国政府采购平台 / 行业公开情报</p>
    <p>情报引擎：太一穿透式搜索核 v1.0</p>
    <p>覆盖产品：钢结构折叠房屋 / 预制集成建筑 / 模块化房屋</p>
  </div>
</div>

<!-- ===== SECTION 1: MARKET OVERVIEW ===== -->
<h3 class="section">一、市场概览</h3>

<h4>🇦🇺 澳大利亚市场</h4>
<table>
  <tr><th>指标</th><th>数据</th><th>来源</th></tr>
  <tr><td>住房短缺</td><td>2026年缺口约10万套</td><td>澳国家住房金融投资公司</td></tr>
  <tr><td>模块化进口增长</td><td>来自亚洲的预制建筑进口逐年显著增长</td><td>BuildOffsite Australia</td></tr>
  <tr><td>主要驱动</td><td>住房危机 + 基建需求 + 矿工营房</td><td>行业分析</td></tr>
  <tr><td>认证要求</td><td>NCC合规 / CodeMark认证</td><td>ArchiEng</td></tr>
  <tr><td>竞争格局</td><td>进口主要来自中国、日本、韩国、东南亚</td><td>行业报告</td></tr>
  <tr><td>关税</td><td>中澳FTA → 钢结构产品零关税（原产地证）</td><td>DFAT</td></tr>
</table>

<h4>🇳🇿 新西兰市场</h4>
<table>
  <tr><th>指标</th><th>数据</th><th>来源</th></tr>
  <tr><td>住房危机</td><td>严重供应不足，政府推动快速建房方案</td><td>NZ政府住房政策</td></tr>
  <tr><td>地震要求</td><td>NZ53604抗震标准 — 钢结构天然优势</td><td>Gear Steel Buildings</td></tr>
  <tr><td>折叠房屋认知</td><td>已有Expandable Folding House入市(FE-30)</td><td>Modern Modular NZ</td></tr>
  <tr><td>市场准入</td><td>Council consent + NZBC合规</td><td>MBIE</td></tr>
  <tr><td>竞争</td><td>本地企业为主（Steeltec/Kiwi Modular/ANZ Modular）</td><td>行业公开</td></tr>
</table>

<div class="insight-box">
  <strong>核心判断：</strong>澳大利亚和新西兰都面临严重的住房短缺问题，预制/模块化建筑成为政府推动的解决方案。钢结构折叠房屋在抗震（新西兰）、快速部署（澳洲矿业营地）、成本控制（住房危机）场景下具备明确市场需求。中澳FTA零关税是中国供应商的核心竞争优势。
</div>

<!-- ===== SECTION 2: AUSTRALIA BUYERS ===== -->
<h3 class="section">二、🇦🇺 澳大利亚真实买家线索</h3>


<div class="buyer-card">
  <div class="name"><span class="badge-a">A</span> Kiwi Modular Structures — <span style="color:#e74c3c">✅ 有真实联系方式</span></div>
  <div class="meta">📍 Level 8, 139 Quay Street, Auckland 1010, NZ | 🏢 模块化建筑商</div>
  <div class="detail"><strong>Gareth O&#39;Keeffe</strong> — 董事 (Director)</div>
  <div class="url">📧 gareth@kiwimodularstructures.com | 📞 027 205 7243</div>
  <div class="detail"><strong>Samantha Zeta</strong> — 商务拓展主管 (Head of Business Development)</div>
  <div class="url">📧 samantha@kiwimodularstructures.com | 📞 09 886 7205</div>
  <div class="detail">新西兰模块化建筑专业公司，应用多样化。直接联系董事Gareth, 探讨钢结构折叠房屋供应链合作。</div>
  <div class="url">🌐 kiwimodularstructures.com</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-a">A</span> Expanders NZ — <span style="color:#e74c3c">✅ 有真实联系方式</span></div>
  <div class="meta">📍 Christchurch, NZ (2026年6月开设奥克兰) | 🏢 可扩展便携建筑供应商</div>
  <div class="detail"><strong>Taylor</strong> — 联系人</div>
  <div class="url">📧 info@expanders.co.nz | 📞 027 210 6839</div>
  <div class="detail">已交付350+单元到9个国家！主营可扩展便携建筑，与折叠房屋概念高度重合。正在扩张奥克兰市场。可直接联系合作。</div>
  <div class="url">🌐 expanders.co.nz | 💰 24,500 NZD起</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-a">A</span> LGS Solutions — <span style="color:#e74c3c">✅ 有真实联系方式</span></div>
  <div class="meta">📍 124-128 Williams Rd, Dandenong South, VIC 3175, Australia | 🏢 钢结构建筑方案商</div>
  <div class="url">📧 info@lgssolutions.com.au | 📞 1300 941 481</div>
  <div class="detail">BlueScope Steel合作伙伴，专业预制钢结构。2026年发布预制钢结构建筑指南，业务扩张中。可直接联系供应合作。</div>
  <div class="url">🌐 lgssolutions.com.au</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-a">A</span> Cargo Connect — <span style="color:#e74c3c">✅ 有真实联系方式</span></div>
  <div class="meta">📍 布里斯班/悉尼/墨尔本/珀斯 | 🏢 中国→澳洲预制房物流+进口代理</div>
  <div class="url">📞 1300 580 838</div>
  <div class="detail">4个办公室：
  • 布里斯班: bne@cargoconnect.com.au | 11/720 Macarthur Ave, Pinkenba QLD 4008
  • 悉尼: syd@cargoconnect.com.au | Suite 6/702-710 Botany Rd, Mascot NSW 2020
  • 墨尔本: mel@cargoconnect.com.au | 16 Butler Way, Tullamarine VIC 3043
  • 珀斯: per@cargoconnect.com.au | Building 3/130 Fauntleroy Ave, Perth Airport WA 6105</div>
  <div class="detail">专门从事中国→澳大利亚预制房屋进口物流的货运公司。可作为物流合作伙伴+市场引荐渠道。</div>
  <div class="url">🌐 cargoconnect.com.au</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-b">B</span> ACS Steel Construction</div>
  <div class="meta">📍 墨尔本, Keysborough, VIC | 🏢 钢结构建筑商</div>
  <div class="detail">住宅/商业/工业钢结构加工安装。官网有明显合作意向，但联系方式仅提供联系表单。需通过官网联系表或LinkedIn触达。</div>
  <div class="url">🌐 acsteelconstruction.com.au | 🔗 联系表: /contact-us/</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-b">B</span> Modern Modular NZ</div>
  <div class="meta">📍 新西兰 | 🏢 模块化房屋供应商</div>
  <div class="detail">已引入FE-30可折叠房屋（Expandable Folding House），表明新西兰市场对折叠房屋有认知和需求。100%新西兰运营。需通过官网联系表触达。</div>
  <div class="url">🌐 modernmodular.co.nz</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-b">B</span> Steeltec NZ</div>
  <div class="meta">📍 Waimate, NZ | 🏢 轻钢结构制造商</div>
  <div class="detail">新西兰领先钢框架制造商，全国免费配送。有模块化房屋钢结构业务。联系方式：官网Enquiry Form。</div>
  <div class="url">🌐 steeltec.co.nz</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-b">B</span> ANZ Modular</div>
  <div class="meta">📍 新西兰 | 🏢 预制钢结构建筑商</div>
  <div class="detail">创始人Barry Ramsay，45年钢结构建筑经验，预制钢框架系统专家。需通过官网联系表或LinkedIn触达。</div>
  <div class="url">🌐 anzmodular.com</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-b">B</span> TradeWheel — 澳大利亚钢结构买家列表</div>
  <div class="meta">📍 在线B2B平台 | B2B平台批量线索</div>
  <div class="detail">TradeWheel平台上活跃的澳大利亚钢结构买家列表，包含多家进口商和采购商。可以直接在平台发送询盘。</div>
  <div class="url">🌐 tradewheel.com/buyers/steel-structures/australia/</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-c">C</span> Bullocks Freightmasters International</div>
  <div class="meta">📍 澳大利亚 | 🏢 货运代理</div>
  <div class="detail">海运模块化房屋进口专家，清楚澳大利亚进口合规。需进一步触达获取直接联系方式。</div>
  <div class="url">🌐 bullocks.net.au</div>
</div>

<div class="buyer-card">
  <div class="name"><span class="badge-c">C</span> Platinum Freight</div>
  <div class="meta">📍 澳大利亚 | 🏢 货运代理</div>
  <div class="detail">提供模块化房屋进口到澳洲的物流方案。需进一步触达。</div>
  <div class="url">🌐 platinumfreight.com.au</div>
</div>


<!-- ===== SECTION 3: TENDER PLATFORMS ===== -->
<h3 class=section>三、政府采购/招标平台（免费注册+批量RFQ）</h3>

<table>
  <tr><th>平台</th><th>国家</th><th>注册</th><th>搜索建议</th></tr>
  <tr><td>AusTender (austender.gov.au)</td><td>🇦🇺</td><td>免费</td><td>"prefabricated building" "modular" "steel structure"</td></tr>
  <tr><td>tenders.nsw.gov.au</td><td>🇦🇺 新州</td><td>免费</td><td>"relocatable" "accommodation" "modular"</td></tr>
  <tr><td>tenders.vic.gov.au</td><td>🇦🇺 维州</td><td>免费</td><td>"modular building" "steel frame"</td></tr>
  <tr><td>qtenders.qld.gov.au</td><td>🇦🇺 昆州</td><td>免费</td><td>"temporary housing" "prefab"</td></tr>
  <tr><td>tenders.wa.gov.au</td><td>🇦🇺 西澳</td><td>免费</td><td>"camp accommodation" "mining camp"</td></tr>
  <tr><td>NZ Government Procurement (getting.govt.nz)</td><td>🇳🇿</td><td>免费</td><td>"modular building" "transportable" "housing"</td></tr>
</table>

<div class="insight-box">
  <strong>关键提示：</strong>中澳FTA下钢结构产品进口关税为0。新西兰钢结构建筑需满足NZ53604抗震标准。上述平台全部免费注册，可设置关键词RSS订阅自动接收招标通知。
</div>

<!-- ===== SECTION 4: ACTION PLAN ===== -->
<h3 class="section">四、触达行动建议（按优先级）</h3>

<h4>P0 — 本周可立即触达（有真实联系方式）</h4>
<table>
  <tr><th>顺序</th><th>目标</th><th>联系方式</th><th>触达方式</th></tr>
  <tr><td>1 🔥</td><td><strong>Kiwi Modular NZ</strong> — Gareth O''Keeffe (董事)</td><td>gareth@kiwimodularstructures.com</td><td>直接发邮件：探讨钢结构折叠房屋NZ供应链合作</td></tr>
  <tr><td>2 🔥</td><td><strong>Expanders NZ</strong> — Taylor</td><td>info@expanders.co.nz / 027 210 6839</td><td>发邮件+打电话：产品高度互补，可推更多折叠型号</td></tr>
  <tr><td>3 🔥</td><td><strong>LGS Solutions AU</strong></td><td>info@lgssolutions.com.au / 1300 941 481</td><td>发邮件：钢结构预制件供应合作</td></tr>
  <tr><td>4 🔥</td><td><strong>Cargo Connect AU</strong> — 4个办公室</td><td>bne/mel/syd/per@cargoconnect.com.au</td><td>发邮件：评估物流合作+市场引荐</td></tr>
  <tr><td>5</td><td><strong>TradeWheel</strong> AU买家列表</td><td>tradewheel.com/buyers/steel-structures/australia/</td><td>注册+直接联系列表中活跃买家</td></tr>
  <tr><td>6</td><td><strong>Kiwi Modular NZ</strong> — Samantha Zeta (商务主管)</td><td>samantha@kiwimodularstructures.com</td><td>同步cc邮件，确认商务细节</td></tr>
</table>

<h4>P1 — 本月触达（需通过联系表或LinkedIn）</h4>
<table>
  <tr><th>顺序</th><th>目标</th><th>方式</th></tr>
  <tr><td>7</td><td>ACS Steel Construction AU</td><td>官网联系表提交供应合作询盘</td></tr>
  <tr><td>8</td><td>Modern Modular NZ (FE-30折叠房屋)</td><td>官网联系表+LinkedIn找负责人</td></tr>
  <tr><td>9</td><td>ANZ Modular (Barry Ramsay)</td><td>LinkedIn搜索Barry Ramsay直接联系</td></tr>
  <tr><td>10</td><td>Steeltec NZ</td><td>官网Enquiry Form+LinkedIn</td></tr>
</table>

<h4>P2 — 持续</h4>
<table>
  <tr><th>顺序</th><th>目标</th><th>方式</th></tr>
  <tr><td>11</td><td>6个招标平台注册</td><td>设置关键词警报，定时检查</td></tr>
  <tr><td>12</td><td>Bullocks/Platinum Freight</td><td>作为备选物流方案</td></tr>
  <tr><td>13</td><td>合规认证评估</td><td>NCC/CodeMark/NZBC</td></tr>
</table>

<div class="footer">
  <p>报告生成：太一跨境贸易 Agent | 数据源：各公司官网公开信息 / Trade.gov / 招标平台</p>
  <p>⚠️ 所有信息来源于公开渠道，建议发送合作意向前核实联系人最新状态</p>
  <p>✅ 标红联系人：已验证真实邮箱/电话 | 标黄：需进一步触达</p>
</div>

</body>
</html>