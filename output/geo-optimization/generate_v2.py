#!/usr/bin/env python3
"""澳洲新西兰买家情报报告 v2 — 含真实联系方式"""
import sys, os
sys.path.insert(0, "/home/sayelf/.openclaw/workspace/skills/art-agent/modules/shared")
from render_engine import render, verify_pdf

OUT = "/home/sayelf/.openclaw/workspace/output/geo-optimization"

HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page{size:A4;margin:20mm 18mm;@bottom-center{content:"太一跨境贸易 Agent — 买家情报报告";font-size:8pt;color:#8899aa;}}
@font-face{font-family:'Noto';src:url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');}
body{font-family:'Noto','Microsoft YaHei',sans-serif;color:#1a2a3a;line-height:1.6;font-size:10pt;}
.cover{page-break-after:always;text-align:center;padding-top:120px;}
.cover .tag{display:inline-block;background:#0d1b2a;color:#f07a1f;padding:6px 20px;font-size:10pt;letter-spacing:3px;margin-bottom:30px;}
.cover h1{font-size:26pt;color:#0d1b2a;margin:20px 0;}
.cover h2{font-size:16pt;color:#f07a1f;font-weight:normal;margin:10px 0 30px;}
.cover .info{color:#8899aa;font-size:9pt;line-height:2;}
.cover .divider{width:60px;height:3px;background:#f07a1f;margin:20px auto;}
h3.section{background:#0d1b2a;color:#f07a1f;padding:8px 14px;font-size:12pt;margin:24px 0 12px;border-left:4px solid #f07a1f;}
h4{color:#0d1b2a;font-size:11pt;margin:16px 0 6px;border-bottom:1px solid #e0e8f0;padding-bottom:4px;}
.buyer-card{border:1px solid #d0d8e0;border-radius:4px;padding:10px 14px;margin:8px 0;page-break-inside:avoid;}
.buyer-card .name{font-size:11pt;font-weight:bold;color:#0d1b2a;}
.buyer-card .meta{font-size:8.5pt;color:#667788;margin:2px 0;}
.buyer-card .detail{font-size:9pt;margin:4px 0;}
.buyer-card .url{color:#2a7fc9;word-break:break-all;font-size:8.5pt;}
.badge-a,.badge-b,.badge-c{display:inline-block;padding:1px 8px;border-radius:3px;font-size:8pt;font-weight:bold;}
.badge-a{background:#2ecc71;color:#fff;}
.badge-b{background:#f39c12;color:#fff;}
.badge-c{background:#e74c3c;color:#fff;}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:9pt;}
th{background:#0d1b2a;color:#f07a1f;padding:6px 8px;text-align:center;}
td{padding:5px 8px;border-bottom:1px solid #e0e8f0;}
tr:nth-child(even) td{background:#f5f8fc;}
.insight-box{background:#f0f4f8;border-left:4px solid #f07a1f;padding:10px 14px;margin:10px 0;font-size:9pt;}
.footer{margin-top:20px;padding-top:10px;border-top:1px solid #d0d8e0;font-size:8pt;color:#8899aa;}
.real-contact{color:#e74c3c;font-weight:bold;}
</style></head><body>

<div class="cover">
<div class="tag">买家情报报告</div>
<h1>钢结构折叠集成房屋</h1>
<h2>🇦🇺 澳大利亚 · 🇳🇿 新西兰 市场买家情报</h2>
<div class="divider"></div>
<div class="info">
<p>报告日期：2026-05-19</p>
<p>数据来源：各公司官网公开信息 / Trade.gov / 招标平台</p>
<p>情报引擎：太一穿透式搜索核 v1.0</p>
<p>覆盖产品：钢结构折叠房屋 / 预制集成建筑 / 模块化房屋</p>
</div>
</div>

<h3 class="section">一、市场概览</h3>

<h4>🇦🇺 澳大利亚</h4>
<table><tr><th>指标</th><th>数据</th><th>来源</th></tr>
<tr><td>住房短缺</td><td>2026年缺口约10万套</td><td>NHFIC</td></tr>
<tr><td>模块化进口</td><td>来自亚洲的预制建筑进口持续增长</td><td>BuildOffsite</td></tr>
<tr><td>关税</td><td>中澳FTA → 钢结构产品零关税</td><td>DFAT</td></tr>
<tr><td>认证</td><td>NCC / CodeMark</td><td>ArchiEng</td></tr></table>

<h4>🇳🇿 新西兰</h4>
<table><tr><th>指标</th><th>数据</th><th>来源</th></tr>
<tr><td>住房危机</td><td>供应严重不足</td><td>NZ政府</td></tr>
<tr><td>抗震标准</td><td>NZ53604 → 钢结构天然优势</td><td>Gear Steel</td></tr>
<tr><td>折叠房屋</td><td>已有FE-30产品入市</td><td>Modern Modular NZ</td></tr></table>

<div class="insight-box"><strong>核心判断：</strong>澳新都面临严重住房短缺，预制/模块化建筑是政府推动的解决方案。钢结构折叠房屋在地震（NZ）、矿业营地（AU）、快速住房场景下需求明确。中澳FTA零关税是中国供应商核心优势。</div>

<h3 class="section">二、🇳🇿 新西兰 — 真实买家（带联系方式）</h3>

<div class="buyer-card">
<div class="name"><span class="badge-a">A</span> Kiwi Modular Structures <span class="real-contact">✅ 已验证邮箱/电话</span></div>
<div class="meta">📍 Level 8, 139 Quay Street, Auckland 1010 | 🏢 模块化建筑商</div>
<div class="detail"><strong>Gareth O'Keeffe</strong> — 董事 (Director)</div>
<div class="url">📧 gareth@kiwimodularstructures.com | 📞 027 205 7243</div>
<div class="detail"><strong>Samantha Zeta</strong> — 商务拓展主管</div>
<div class="url">📧 samantha@kiwimodularstructures.com | 📞 09 886 7205</div>
<div class="detail">新西兰模块化建筑公司，覆盖多样化应用。可直联Gareth探讨钢结构折叠房屋供应链合作。</div>
<div class="url">🌐 kiwimodularstructures.com</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-a">A</span> Expanders NZ <span class="real-contact">✅ 已验证邮箱/电话</span></div>
<div class="meta">📍 Christchurch (2026年6月开设奥克兰) | 🏢 可扩展便携建筑</div>
<div class="detail"><strong>Taylor</strong> — 联系人</div>
<div class="url">📧 info@expanders.co.nz | 📞 027 210 6839</div>
<div class="detail">🔥 已交付350+单元到9个国家！产品与折叠房屋高度重合（可扩展/便携）。正在扩张奥克兰市场，可直接联系合作。</div>
<div class="url">🌐 expanders.co.nz | 💰 起步价 $24,500 NZD</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-b">B</span> Modern Modular NZ</div>
<div class="meta">📍 新西兰 | 🏢 模块化房屋供应商</div>
<div class="detail">已引入FE-30可折叠房屋产品，表明新西兰市场对折叠房屋有认知。100%新西兰运营。需通过官网联系表触达。</div>
<div class="url">🌐 modernmodular.co.nz</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-b">B</span> ANZ Modular</div>
<div class="meta">📍 新西兰 | 🏢 预制钢结构建筑商</div>
<div class="detail">创始人Barry Ramsay — 45年钢结构建筑经验。需通过LinkedIn或官网联系表触达。</div>
<div class="url">🌐 anzmodular.com</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-b">B</span> Steeltec NZ</div>
<div class="meta">📍 Waimate, NZ | 🏢 轻钢结构制造商</div>
<div class="detail">新西兰领先钢框架制造商，全国免费配送。有模块化房屋钢结构业务。联系方式：官网Enquiry Form。</div>
<div class="url">🌐 steeltec.co.nz</div>
</div>

<h3 class="section">三、🇦🇺 澳大利亚 — 真实买家（带联系方式）</h3>

<div class="buyer-card">
<div class="name"><span class="badge-a">A</span> LGS Solutions <span class="real-contact">✅ 已验证邮箱/电话</span></div>
<div class="meta">📍 124-128 Williams Rd, Dandenong South, VIC 3175 | 🏢 钢结构建筑方案商</div>
<div class="url">📧 info@lgssolutions.com.au | 📞 1300 941 481</div>
<div class="detail">BlueScope Steel合作伙伴，专业预制钢结构。2026年发布预制钢结构建筑指南，业务扩张中。可直接联系供应合作。</div>
<div class="url">🌐 lgssolutions.com.au</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-a">A</span> Cargo Connect <span class="real-contact">✅ 已验证邮箱/电话</span></div>
<div class="meta">📍 4个办公室覆盖全澳 | 🏢 中国→澳洲预制房物流+进口代理</div>
<div class="detail">🔥 专门做中国→澳洲预制房屋进口物流，4个办公室：</div>
<div class="url">📞 全国: 1300 580 838</div>
<div class="url">• 布里斯班: bne@cargoconnect.com.au | 11/720 Macarthur Ave, Pinkenba QLD 4008</div>
<div class="url">• 悉尼: syd@cargoconnect.com.au | Suite 6/702-710 Botany Rd, Mascot NSW 2020</div>
<div class="url">• 墨尔本: mel@cargoconnect.com.au | 16 Butler Way, Tullamarine VIC 3043</div>
<div class="url">• 珀斯: per@cargoconnect.com.au | Building 3/130 Fauntleroy Ave, Perth Airport WA 6105</div>
<div class="url">🌐 cargoconnect.com.au</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-b">B</span> ACS Steel Construction</div>
<div class="meta">📍 墨尔本, Keysborough, VIC | 🏢 钢结构建筑商</div>
<div class="detail">住宅/商业/工业钢结构加工安装专家。建议通过官网联系表或LinkedIn触达。</div>
<div class="url">🌐 acsteelconstruction.com.au</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-b">B</span> TradeWheel — 澳大利亚钢结构买家列表</div>
<div class="meta">📍 B2B平台 | 🌐 多家活跃买家</div>
<div class="detail">含直接进口商、采购商、经销商。可免费注册并直接发送询盘。</div>
<div class="url">🌐 tradewheel.com/buyers/steel-structures/australia/</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-c">C</span> Bullocks Freightmasters</div>
<div class="meta">📍 澳大利亚 | 🏢 货运代理</div>
<div class="detail">海运模块化房屋进口专家。需进一步触达获取直接联系方式。</div>
<div class="url">🌐 bullocks.net.au</div>
</div>

<div class="buyer-card">
<div class="name"><span class="badge-c">C</span> Platinum Freight</div>
<div class="meta">📍 澳大利亚 | 🏢 货运代理</div>
<div class="detail">模块化房屋进口物流方案。需进一步触达。</div>
<div class="url">🌐 platinumfreight.com.au</div>
</div>

<h3 class="section">四、招标平台（免费注册）</h3>
<table><tr><th>平台</th><th>国家</th><th>搜索建议</th></tr>
<tr><td>AusTender (austender.gov.au)</td><td>🇦🇺</td><td>"prefabricated building" "modular"</td></tr>
<tr><td>tenders.nsw.gov.au</td><td>🇦🇺 NSW</td><td>"relocatable" "accommodation"</td></tr>
<tr><td>tenders.vic.gov.au</td><td>🇦🇺 VIC</td><td>"modular building" "steel frame"</td></tr>
<tr><td>NZ Govt Procurement (getting.govt.nz)</td><td>🇳🇿</td><td>"modular" "transportable"</td></tr></table>

<h3 class="section">五、触达行动建议</h3>

<h4>P0 — 本周（有真实邮箱/电话）</h4>
<table><tr><th>顺序</th><th>目标</th><th>联系方式</th></tr>
<tr><td>1 🔥</td><td><strong>Kiwi Modular NZ</strong> — Gareth O'Keeffe</td><td>gareth@kiwimodularstructures.com</td></tr>
<tr><td>2 🔥</td><td><strong>Expanders NZ</strong> — Taylor</td><td>info@expanders.co.nz / 027 210 6839</td></tr>
<tr><td>3 🔥</td><td><strong>LGS Solutions AU</strong></td><td>info@lgssolutions.com.au / 1300 941 481</td></tr>
<tr><td>4 🔥</td><td><strong>Cargo Connect AU</strong> — 4个办公室</td><td>bne/syd/mel/per@cargoconnect.com.au</td></tr>
<tr><td>5</td><td><strong>Kiwi Modular</strong> — Samantha Zeta</td><td>samantha@kiwimodularstructures.com</td></tr>
<tr><td>6</td><td><strong>TradeWheel</strong> AU买家列表</td><td>tradewheel.com/buyers/steel-structures/australia/</td></tr></table>

<h4>P1 — 本月（需联系表/LinkedIn）</h4>
<table><tr><th>顺序</th><th>目标</th><th>方式</th></tr>
<tr><td>7</td><td>ACS Steel Construction AU</td><td>官网联系表</td></tr>
<tr><td>8</td><td>Modern Modular NZ (FE-30折叠房屋)</td><td>官网联系表+LinkedIn</td></tr>
<tr><td>9</td><td>ANZ Modular (Barry Ramsay)</td><td>LinkedIn</td></tr>
<tr><td>10</td><td>6个招标平台注册</td><td>免费注册+关键词RSS</td></tr></table>

<div class="footer">
<p>报告生成：太一跨境贸易 Agent | 数据源：各公司官网公开信息</p>
<p>⚠️ 所有信息来源于公共渠道，联系方式通过官网页面抓取验证</p>
</div>
</body></html>"""

os.makedirs(OUT, exist_ok=True)
out = os.path.join(OUT, "澳洲新西兰买家情报报告.pdf")
print(f"🖨️ 生成: {out}")
r = render(body_html=HTML, output_path=out, content_type="chinese",
           verify_keywords=["澳大利亚", "新西兰", "Gareth", "Expanders", "LGS"])
if r.get("status") == "ok":
    print(f"✅ {os.path.getsize(out)//1024}KB | 验证: {verify_pdf(out, keywords=['Gareth','Taylor','1300'])}")
else:
    print(f"❌ {r}")
