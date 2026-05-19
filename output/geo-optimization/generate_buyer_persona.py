#!/usr/bin/env python3
"""钢结构折叠集成房屋 — 购买方画像报告 v2"""
import sys, os
sys.path.insert(0, "/home/sayelf/.openclaw/workspace/skills/art-agent/modules/shared")
from render_engine import render, verify_pdf

OUT = "/home/sayelf/.openclaw/workspace/output/geo-optimization"

HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
@page{size:A4;margin:20mm 18mm;@bottom-center{content:"太一跨境贸易 Agent — 购买方画像报告";font-size:8pt;color:#8899aa;}}
@font-face{font-family:'Noto';src:url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');}
body{font-family:'Noto','Microsoft YaHei',sans-serif;color:#1a2a3a;line-height:1.6;font-size:10pt;}
.cover{page-break-after:always;text-align:center;padding-top:100px;}
.cover .tag{display:inline-block;background:#0d1b2a;color:#f07a1f;padding:6px 20px;font-size:10pt;letter-spacing:3px;margin-bottom:30px;}
.cover h1{font-size:26pt;color:#0d1b2a;margin:20px 0;}
.cover h2{font-size:16pt;color:#f07a1f;font-weight:normal;margin:10px 0 30px;}
.cover .divider{width:60px;height:3px;background:#f07a1f;margin:20px auto;}
.cover .info{color:#8899aa;font-size:9pt;line-height:2;}
h3.section{background:#0d1b2a;color:#f07a1f;padding:8px 14px;font-size:12pt;margin:24px 0 12px;border-left:4px solid #f07a1f;}
h4{color:#0d1b2a;font-size:11pt;margin:16px 0 6px;border-bottom:1px solid #e0e8f0;padding-bottom:4px;}
.buyer-card{border:1px solid #d0d8e0;border-radius:4px;padding:10px 14px;margin:8px 0;page-break-inside:avoid;}
.buyer-card .name{font-size:11pt;font-weight:bold;color:#0d1b2a;}
.buyer-card .meta{font-size:8.5pt;color:#667788;margin:2px 0;}
.buyer-card .detail{font-size:9pt;margin:4px 0;}
.buyer-card .url{color:#2a7fc9;word-break:break-all;font-size:8.5pt;}
.badge-a{background:#2ecc71;color:#fff;display:inline-block;padding:1px 8px;border-radius:3px;font-size:8pt;font-weight:bold;}
.badge-b{background:#f39c12;color:#fff;display:inline-block;padding:1px 8px;border-radius:3px;font-size:8pt;font-weight:bold;}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:9pt;}
th{background:#0d1b2a;color:#f07a1f;padding:6px 8px;text-align:center;}
td{padding:5px 8px;border-bottom:1px solid #e0e8f0;}
tr:nth-child(even) td{background:#f5f8fc;}
.insight-box{background:#f0f4f8;border-left:4px solid #f07a1f;padding:10px 14px;margin:10px 0;font-size:9pt;}
.footer{margin-top:20px;padding-top:10px;border-top:1px solid #d0d8e0;font-size:8pt;color:#8899aa;}
.tag-a{display:inline-block;background:#2ecc71;color:#fff;padding:0 6px;border-radius:3px;font-size:7pt;}
.tag-b{display:inline-block;background:#f39c12;color:#fff;padding:0 6px;border-radius:3px;font-size:7pt;}
.tag-c{display:inline-block;background:#e74c3c;color:#fff;padding:0 6px;border-radius:3px;font-size:7pt;}
</style></head><body>

<div class="cover">
<div class="tag">购买方画像报告</div>
<h1>钢结构折叠集成房屋</h1>
<h2>🇦🇺 澳大利亚 · 🇳🇿 新西兰 购买方画像</h2>
<div class="divider"></div>
<div class="info">
<p>报告日期：2026-05-19</p>
<p>覆盖：矿业公司 / 模块建筑商 / 开发商 / 政府 / 物流商 / 个人</p>
<p>数据来源：各公司官网 / 行业平台 / 政府采购 / 公开情报</p>
<p>情报引擎：太一穿透式搜索核 v1.0</p>
</div>
</div>

<h3 class="section">一、购买方类型总览</h3>

<table>
<tr><th>购买方类型</th><th>规模</th><th>采购量</th><th>利润</th><th>决策周期</th><th>优先级</th></tr>
<tr><td><strong>矿业公司</strong> — 矿工营地/远程住宿</td><td>🔴 最大</td><td>🔴 批量</td><td>🔴 高</td><td>3-6月</td><td><span class="tag-a">P0</span></td></tr>
<tr><td><strong>模块建筑商</strong> — 预制建筑供应商/进口商</td><td>🔴 大</td><td>🔴 批量</td><td>🟡 中</td><td>1-3月</td><td><span class="tag-a">P0</span></td></tr>
<tr><td><strong>政府机构</strong> — 应急住房/学校/医疗/国防</td><td>🟡 中</td><td>🔴 批量</td><td>🟡 中</td><td>6-12月</td><td><span class="tag-a">P0</span></td></tr>
<tr><td><strong>开发商/建筑商</strong> — 住宅/商业开发</td><td>🟡 中</td><td>🟡 单次</td><td>🟡 中</td><td>3-6月</td><td><span class="tag-b">P1</span></td></tr>
<tr><td><strong>物流进口商</strong> — 中国→澳新货运代理</td><td>🟢 小</td><td>🟡 持续</td><td>🟢 低</td><td>1月</td><td><span class="tag-b">P1</span></td></tr>
<tr><td><strong>个人买家</strong> — 自建房/祖母房/度假屋</td><td>🟢 小</td><td>🟢 单品</td><td>🟢 低</td><td>1-3月</td><td><span class="tag-c">P2</span></td></tr>
</table>

<h3 class="section">二、🇦🇺 澳大利亚 — 核心购买方</h3>

<h4>类型1：矿业公司（最大需求方）</h4>
<div class="insight-box">澳洲矿业营房是折叠房屋最大应用场景。Pilbara/NT/WA/QLD 矿区需要大量快速部署的工人住宿。折叠房屋1箱=6套，运输效率3倍于传统模块，对偏远矿区极具吸引力。</div>

<table>
<tr><th>公司</th><th>矿区</th><th>工人规模</th><th>营地需求</th></tr>
<tr><td>BHP</td><td>Pilbara WA</td><td>5万+</td><td>🔴 大量营房</td></tr>
<tr><td>Rio Tinto</td><td>Pilbara WA</td><td>4万+</td><td>🔴 大量营房</td></tr>
<tr><td>Fortescue Metals</td><td>Pilbara WA</td><td>2万+</td><td>🔴 大量</td></tr>
<tr><td>Newcrest Mining</td><td>NSW/WA</td><td>1万+</td><td>🟡 中</td></tr>
</table>

<h4>类型2：模块建筑商（直接采购方+转售渠道）</h4>
<table>
<tr><th>公司</th><th>类型</th><th>联系方式</th></tr>
<tr><td><strong>Ausco Modular</strong></td><td>澳洲最大模块建筑商之一</td><td>ausco.com.au → 官网联系</td></tr>
<tr><td><strong>ATCO Structures</strong></td><td>75年经验，全球模块建筑巨头</td><td>structures.atco.com/en-au.html</td></tr>
<tr><td><strong>Northern Transportables</strong></td><td>NT/WA矿业模块建筑商</td><td>northerntransportables.com.au</td></tr>
<tr><td><strong>EcoPrestige</strong></td><td>矿工住宿专业采购商</td><td>ecoprestige.com.au</td></tr>
<tr><td><strong>Australian Portable Camps</strong></td><td>垂直整合营地方案商</td><td>australianportablecamps.com.au</td></tr>
<tr><td><strong>Outback Builders WA</strong></td><td>西澳矿业营地专家</td><td>outbackbuilderswa.com.au</td></tr>
<tr><td><strong>Aussie Modular Solutions</strong></td><td>WA预制建筑制造商</td><td>ams-group.com.au</td></tr>
<tr><td><strong>Froth Build</strong></td><td>模块化矿业建筑</td><td>frothbuild.com.au</td></tr>
</table>

<div class="insight-box">这些模块建筑商本身可能既是竞争对手（自己做模块建筑），也是潜在合作方（采购折叠房屋作为补充产品线，或代工组装）。建议：优先接触 Northern Transportables / EcoPrestige / Australian Portable Camps 作为产品采购合作方。</div>

<h4>类型3：政府/招标（批量采购）</h4>
<table>
<tr><th>平台</th><th>用途</th><th>搜索关键词</th></tr>
<tr><td>AusTender</td><td>联邦政府采购</td><td>"prefabricated building" "modular accommodation"</td></tr>
<tr><td>tenders.nsw.gov.au</td><td>新州学校/医疗</td><td>"relocatable classroom" "modular"</td></tr>
<tr><td>tenders.vic.gov.au</td><td>维州应急住房</td><td>"temporary housing" "modular building"</td></tr>
<tr><td>tenders.wa.gov.au</td><td>西澳矿业/基建</td><td>"camp accommodation" "mining camp"</td></tr>
<tr><td>qtenders.qld.gov.au</td><td>昆州灾害重建</td><td>"temporary housing" "prefab"</td></tr>
</table>

<h3 class="section">三、🇳🇿 新西兰 — 核心购买方</h3>

<h4>类型1：模块/预制建筑商（直接采购方）</h4>
<table>
<tr><th>公司</th><th>联系人</th><th>联系方式</th><th>合作方向</th></tr>
<tr><td><strong>Kiwi Modular</strong></td><td>Gareth O'Keeffe<br/>Samantha Zeta</td><td>gareth@kiwimodularstructures.com<br/>samantha@kiwimodularstructures.com</td><td>钢结构折叠房屋供应合作</td></tr>
<tr><td><strong>Expanders NZ</strong></td><td>Taylor</td><td>info@expanders.co.nz<br/>027 210 6839</td><td>已做可扩展建筑，可推更多折叠型号</td></tr>
<tr><td><strong>Modern Modular NZ</strong></td><td>团队</td><td>官网联系表</td><td>已引入FE-30折叠房屋，直接竞品/合作伙伴</td></tr>
<tr><td><strong>Steeltec NZ</strong></td><td>团队</td><td>官网Enquiry Form</td><td>全国配送钢框架，可做本地组装</td></tr>
<tr><td><strong>ANZ Modular</strong></td><td>Barry Ramsay</td><td>LinkedIn / 官网</td><td>45年钢结构经验</td></tr>
<tr><td><strong>Laing Properties</strong></td><td>团队</td><td>laing.co.nz</td><td>40年+，500+预制房，8000+搬迁</td></tr>
<tr><td><strong>Module Made</strong></td><td>团队</td><td>modulemade.co.nz</td><td>预制建筑设计+建造</td></tr>
<tr><td><strong>Makespace</strong></td><td>团队</td><td>makespace.build</td><td>建筑设计模块化，全国配送</td></tr>
<tr><td><strong>Tawera Group</strong></td><td>团队</td><td>taweragroup.com</td><td>30年房地产开发+模块化建筑</td></tr>
</table>

<div class="insight-box">新西兰市场特殊优势：① 钢结构抗震（NZ53604标准）→ 钢结构折叠房屋天然符合 ② 住房危机严重 → 政府推动快速建房 ③ FE-30已入市 → 折叠房屋概念已被当地市场接受。</div>

<h3 class="section">四、场景化需求匹配</h3>

<table>
<tr><th>场景</th><th>国家</th><th>需求描述</th><th>折叠房屋优势</th><th>目标买家</th></tr>
<tr><td>🏗️ 矿业营地</td><td>🇦🇺</td><td>Pilbara矿区工人住宿，快速部署+搬迁</td><td>1箱=6套，运输效率3x，拆装快</td><td>矿业公司/营地建筑商</td></tr>
<tr><td>🏠 应急住房</td><td>🇦🇺🇳🇿</td><td>洪灾/火灾后快速安置</td><td>可折叠运输，3天完成部署</td><td>政府/救援机构</td></tr>
<tr><td>🏘️ 保障房</td><td>🇦🇺🇳🇿</td><td>解决住房危机</td><td>成本比传统低30%，工期短50%</td><td>政府/Kāinga Ora/开发商</td></tr>
<tr><td>🏨 旅游度假</td><td>🇳🇿</td><td>度假屋/生态酒店</td><td>可移动+环保+快速</td><td>旅游开发商</td></tr>
<tr><td>🏫 临时校舍</td><td>🇦🇺</td><td>学校扩容/灾后教学</td><td>快速部署+可扩展</td><td>州教育部</td></tr>
<tr><td>🏪 商业办公</td><td>🇦🇺🇳🇿</td><td>工地办公室/临时商业</td><td>模块化+可搬迁</td><td>建筑公司/开发商</td></tr>
</table>

<h3 class="section">五、触达策略</h3>

<h4>P0 — 本周（已验证联系方式，直接发邮件）</h4>
<table>
<tr><th>目标</th><th>邮件</th><th>切入点</th></tr>
<tr><td>Kiwi Modular — Gareth</td><td>gareth@kiwimodularstructures.com</td><td>"钢结构折叠房屋NZ市场合作"</td></tr>
<tr><td>Expanders NZ — Taylor</td><td>info@expanders.co.nz</td><td>"产品互补，推更多折叠型号"</td></tr>
<tr><td>LGS Solutions AU</td><td>info@lgssolutions.com.au</td><td>"钢结构预制件供应合作"</td></tr>
<tr><td>Cargo Connect AU</td><td>bne/syd/mel/per@cargoconnect.com.au</td><td>"物流+市场引荐"</td></tr>
<tr><td>TradeWheel AU买家列表</td><td>tradewheel.com</td><td>直接发询盘</td></tr>
</table>

<h4>P1 — 本月（需官网联系表/LinkedIn）</h4>
<table>
<tr><th>目标</th><th>方式</th><th>切入点</th></tr>
<tr><td>Northern Transportables</td><td>官网联系表</td><td>"NT/WA矿业营地折叠房屋方案"</td></tr>
<tr><td>EcoPrestige AU</td><td>官网联系表</td><td>"矿工住宿模块供应"</td></tr>
<tr><td>Australian Portable Camps</td><td>官网联系表</td><td>"垂直整合营地方案折叠产品线"</td></tr>
<tr><td>Modern Modular NZ</td><td>官网+LinkedIn</td><td>"FE-30供应商合作/更多型号"</td></tr>
<tr><td>ANZ Modular — Barry Ramsay</td><td>LinkedIn</td><td>"钢结构建筑45年经验交流"</td></tr>
<tr><td>Laing Properties NZ</td><td>官网</td><td>"500+预制房供应链合作"</td></tr>
<tr><td>Tawera Group NZ</td><td>官网</td><td>"30年开发+模块化建筑采购"</td></tr>
</table>

<h4>P2 — 持续</h4>
<table>
<tr><th>目标</th><th>方式</th></tr>
<tr><td>6个招标平台注册</td><td>免费注册+关键词RSS</td></tr>
<tr><td>BHP/ Rio Tinto/ Fortescue 供应链注册</td><td>矿业公司供应商门户注册</td></tr>
<tr><td>Ausco/ATCO 合作评估</td><td>评估竞争对手vs合作伙伴</td></tr>
<tr><td>NCC/CodeMark/NZBC认证启动</td><td>合规认证评估</td></tr>
</table>

<div class="footer">
<p>报告生成：太一跨境贸易 Agent | 购买方画像 v2 | 数据源：各公司官网 / 行业平台 / 政府采购</p>
<p>⚠️ 联系方式来源于公开渠道，发送合作意向前建议核实最新状态</p>
</div>
</body></html>"""

os.makedirs(OUT, exist_ok=True)
out = os.path.join(OUT, "钢结构折叠房屋购买方画像.pdf")
print(f"🖨️ 生成: {out}")
r = render(body_html=HTML, output_path=out, content_type="chinese",
           verify_keywords=["矿业", "矿业公司", "模块建筑", "Kiwi Modular", "Expanders"])
if r.get("status") == "ok":
    print(f"✅ {os.path.getsize(out)//1024}KB | 验证: {verify_pdf(out, keywords=['矿业','模块建筑','Kiwi','Expanders'])}")
else:
    print(f"❌ {r}")
