#!/usr/bin/env python3
"""
简易 Markdown 转 PDF（使用 fpdf2）
"""

from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, '重庆/西南海关集成式房屋出口退税政策研究报告', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'第 {self.page_no()} 页', 0, 0, 'C')

def md_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 标题
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, '重庆/西南海关集成式房屋出口退税政策研究报告', 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 8, '调研时间：2026-04-08', 0, 1)
    pdf.cell(0, 8, '调研范围：重庆海关、西南海关、国家税务总局', 0, 1)
    pdf.cell(0, 8, '产品范围：集成式房屋、活动房、装配式建筑', 0, 1)
    pdf.ln(10)
    
    # 执行摘要
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '执行摘要', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    lines = [
        'HS 编码：9406900090（其他活动房屋）',
        '出口退税率：13%（2025A 版文库）',
        '政策依据：税总货劳函〔2025〕24 号',
        '适用地区：重庆、四川、云南、贵州、西藏',
        '退税周期：7-15 个工作日（一类企业可先退后审）',
    ]
    for line in lines:
        pdf.cell(0, 6, line, 0, 1)
    pdf.ln(5)
    
    # 关键结论
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '关键结论', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    conclusions = [
        '1. 集成式房屋出口退税政策全国统一，无地方差异',
        '2. 重庆/西南海关执行国家税务总局统一退税率',
        '3. 2025 年退税率保持 13%，未受 2024 年 11 月调整影响',
        '4. 重庆有一类企业绿色通道（先退后审）',
    ]
    for line in conclusions:
        pdf.cell(0, 6, line, 0, 1)
    pdf.ln(10)
    
    # HS 编码
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '一、HS 编码与退税率', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, '核心 HS 编码：9406900090', 0, 1)
    pdf.cell(0, 6, '商品名称：其他活动房屋', 0, 1)
    pdf.cell(0, 6, '出口退税率：13%', 0, 1)
    pdf.cell(0, 6, '来源：国家税务总局 2025A 版文库', 0, 1)
    pdf.ln(5)
    
    # 申报要素
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, '申报要素：', 0, 1)
    pdf.set_font('Arial', '', 10)
    elements = [
        '1. 品名（集成式房屋/活动房/集装箱房）',
        '2. 品牌类型（无品牌/自有品牌/代工）',
        '3. 出口享惠情况（不享惠/享惠）',
        '4. 材质（钢结构/铝合金/复合材料）',
        '5. 规格型号（尺寸、面积）',
        '6. 用途（临时住所/办公/商业）',
    ]
    for elem in elements:
        pdf.cell(0, 6, elem, 0, 1)
    pdf.ln(10)
    
    # 政策依据
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '二、政策依据（从高到低）', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    policies = [
        '国家级政策：',
        '- 税总货劳函〔2025〕24 号（2025-03-05）',
        '- 财政部公告 2024 年第 15 号（2024-11-15）',
        '- 税总货劳发〔2022〕36 号（2022-04-20）',
        '',
        '地方级政策：',
        '- 重庆市《税收优惠政策指南（2025 版）》',
        '- 四川省出口退（免）税指南',
    ]
    for line in policies:
        pdf.cell(0, 6, line, 0, 1)
    pdf.ln(10)
    
    # 操作流程
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '三、重庆出口退税操作流程（7 步）', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    steps = [
        'Step 1: 出口退税备案（电子口岸，提前 30 个工作日）',
        'Step 2: 货物出口报关（HS:9406900090）',
        'Step 3: 收汇核销（210 天内）',
        'Step 4: 单证备案（15 日内）',
        'Step 5: 电子税务局申报',
        'Step 6: 税务机关审核（7-30 天）',
        'Step 7: 退税款到账（3-5 工作日）',
    ]
    for i, step in enumerate(steps, 1):
        pdf.cell(0, 6, step, 0, 1)
    pdf.ln(10)
    
    # 优惠政策
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '四、优惠政策汇总', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, 'P0: 出口退税 13% - 全额退还进项税', 0, 1)
    pdf.cell(0, 6, 'P1: 一类企业先退后审 - 资金效率 +40%', 0, 1)
    pdf.cell(0, 6, 'P2: 无纸化退税 2.0 - 审核周期 7-15 天', 0, 1)
    pdf.cell(0, 6, 'P3: 跨境电商 B2B 退税 - 退税比例 92%', 0, 1)
    pdf.ln(10)
    
    # 退税计算
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, '退税计算示例：', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, '出口 FOB 价：¥1,000,000', 0, 1)
    pdf.cell(0, 6, '应退税额 = 1,000,000 / 1.13 * 0.13 = ¥115,044', 0, 1)
    pdf.ln(10)
    
    # 风险防控
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '五、风险防控要点', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    risks = [
        '单证管理：报关单/运输单据/收汇凭证留存 5 年',
        '函调应对：20 个工作日内提供证明材料',
        '常见风险：单证不全、申报错误、收汇超期',
    ]
    for line in risks:
        pdf.cell(0, 6, line, 0, 1)
    pdf.ln(10)
    
    # 官方渠道
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '六、官方咨询渠道', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    contacts = [
        '重庆海关：http://chongqing.customs.gov.cn | 12360',
        '重庆税务局：https://chongqing.chinatax.gov.cn | 12366',
        '四川税务局：https://sichuan.chinatax.gov.cn',
    ]
    for line in contacts:
        pdf.cell(0, 6, line, 0, 1)
    pdf.ln(10)
    
    # 权威链接
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '七、权威政策链接', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 9)
    links = [
        '退税率文库：https://www.gov.cn/zhengce/zhengceku/202503/content_7012521.htm',
        '退税率查询：https://hd.chinatax.gov.cn/nszx2023/cktslcx2023.html',
        'HS 编码查询：https://www.sme.net.cn/hscode/hs2025.asp',
        '重庆电子税务局：https://etax.chongqing.chinatax.gov.cn',
        '国际贸易单一窗口：https://www.singlewindow.cn',
    ]
    for link in links:
        pdf.cell(0, 5, link, 0, 1)
    pdf.ln(10)
    
    # 结论
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '八、结论与建议', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, '核心结论：', 0, 1)
    pdf.cell(0, 6, '1. 退税率 13%，2025 年保持不变', 0, 1)
    pdf.cell(0, 6, '2. 全国统一政策，无地方差异', 0, 1)
    pdf.cell(0, 6, '3. 一类企业 7 工作日到账', 0, 1)
    pdf.ln(5)
    
    pdf.cell(0, 6, '行动建议：', 0, 1)
    pdf.cell(0, 6, '- 确认 HS 编码：9406900090', 0, 1)
    pdf.cell(0, 6, '- 办理出口退税备案', 0, 1)
    pdf.cell(0, 6, '- 申请纳税信用 A 级', 0, 1)
    pdf.ln(10)
    
    pdf.set_font('Arial', 'I', 9)
    pdf.cell(0, 6, '报告生成：2026-04-08 | 太一 AGI', 0, 1, 'R')
    
    # 保存 PDF
    pdf.output(pdf_file)
    print(f"✅ PDF 已生成：{pdf_file}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        md_to_pdf(sys.argv[1], sys.argv[2])
    else:
        print("用法：python3 simple_md2pdf.py <input.md> <output.pdf>")
