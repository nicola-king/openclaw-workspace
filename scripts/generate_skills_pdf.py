#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一 AGI Skills 功能汇总 PDF 生成器

功能：
- 扫描所有 SKILL.md 文件
- 提取技能信息
- 生成表格
- 导出 PDF

创建时间：2026-04-06 09:00
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 技能数据
SKILLS_DATA = [
    # 核心 Bot Skills
    {"id": 1, "name": "知几 (Zhiji)", "name_en": "Zhiji Quant Bot", "desc": "量化交易执行 - Polymarket 预测市场 + GMGN 链上交易", "desc_en": "Quantitative trading execution - Polymarket + GMGN on-chain trading", "keywords": "量化/交易/Polymarket/GMGN/Quant/Trading"},
    {"id": 2, "name": "山木 (Shanmu)", "name_en": "Shanmu Content Bot", "desc": "内容创意生成 - 文章/帖子/视频脚本/创意素材", "desc_en": "Content creation - Articles/Posts/Video scripts/Creative materials", "keywords": "内容/创意/文章/视频/Content/Creative/Article"},
    {"id": 3, "name": "素问 (Suwen)", "name_en": "Suwen Tech Bot", "desc": "技术开发 + 代码审查 + 工具集成", "desc_en": "Tech development + Code review + Tool integration", "keywords": "技术/代码/开发/工具/Tech/Code/Development"},
    {"id": 4, "name": "罔两 (Wangliang)", "name_en": "Wangliang Data Bot", "desc": "数据采集 + CEO 视角分析 - 网页爬虫/API 调用/数据分析", "desc_en": "Data collection + CEO analysis - Web scraping/API/Data analysis", "keywords": "数据/采集/爬虫/分析/Data/Collection/Scraper"},
    {"id": 5, "name": "庖丁 (Paoding)", "name_en": "Paoding Finance Bot", "desc": "预算成本分析与财务追踪", "desc_en": "Budget cost analysis and financial tracking", "keywords": "预算/成本/财务/预算/Budget/Cost/Finance"},
    {"id": 6, "name": "天机 (Tianji)", "name_en": "Tianji Smart Money", "desc": "聪明钱追踪与市场机会分析", "desc_en": "Smart money tracking and market opportunity analysis", "keywords": "聪明钱/市场/交易/Smart Money/Market/Trading"},
    {"id": 7, "name": "羿 (Yi)", "name_en": "Yi Alert Bot", "desc": "监控信号与告警系统", "desc_en": "Monitoring signals and alert system", "keywords": "监控/告警/信号/Monitoring/Alert/Signal"},
    {"id": 8, "name": "守藏吏 (Shoucangli)", "name_en": "Shoucangli Steward", "desc": "资源调度与管家服务", "desc_en": "Resource scheduling and steward service", "keywords": "管家/资源/调度/Steward/Resource/Scheduler"},
    
    # 交易与金融 Skills
    {"id": 9, "name": "GMGN", "name_en": "GMGN Trading", "desc": "GMGN.AI 链上交易 - Solana/Base/BSC", "desc_en": "GMGN.AI on-chain trading - Solana/Base/BSC", "keywords": "GMGN/链上/Solana/Base/GMGN/On-chain"},
    {"id": 10, "name": "Binance Trader", "name_en": "Binance Trader", "desc": "币安交易所 API 集成与交易执行", "desc_en": "Binance exchange API integration and trading execution", "keywords": "币安/交易所/交易/Binance/Exchange/Trading"},
    {"id": 11, "name": "Polymarket", "name_en": "Polymarket", "desc": "Polymarket 预测市场交易与监控", "desc_en": "Polymarket prediction market trading and monitoring", "keywords": "Polymarket/预测/市场/Prediction/Market"},
    {"id": 12, "name": "CoinGecko Price", "name_en": "CoinGecko Price", "desc": "加密货币价格查询 - 免费无需 API Key", "desc_en": "Cryptocurrency price query - Free, no API key required", "keywords": "加密货币/价格/CoinGecko/Crypto/Price"},
    {"id": 13, "name": "Portfolio Tracker", "name_en": "Portfolio Tracker", "desc": "投资组合实时追踪与分析 (Yahoo Finance)", "desc_en": "Real-time portfolio tracking and analysis (Yahoo Finance)", "keywords": "投资组合/股票/分析/Portfolio/Stocks/Analysis"},
    {"id": 14, "name": "Cost Tracker", "name_en": "Cost Tracker", "desc": "ROI 与成本追踪", "desc_en": "ROI and cost tracking", "keywords": "ROI/成本/追踪/ROI/Cost/Tracking"},
    
    # 数据采集 Skills
    {"id": 15, "name": "News Fetcher", "name_en": "News Fetcher", "desc": "新闻采集 - NewsAPI (100 请求/天免费)", "desc_en": "News collection - NewsAPI (100 requests/day free)", "keywords": "新闻/媒体/头条/News/Media/Headlines"},
    {"id": 16, "name": "Weather", "name_en": "Weather Forecast", "desc": "天气预报采集 - wttr.in / Open-Meteo", "desc_en": "Weather forecast collection - wttr.in / Open-Meteo", "keywords": "天气/预报/Weather/Forecast"},
    {"id": 17, "name": "Unsplash Image", "name_en": "Unsplash Image", "desc": "免费高质量图片搜索 - Unsplash API", "desc_en": "Free high-quality image search - Unsplash API", "keywords": "图片/搜索/免费/Image/Search/Free"},
    {"id": 18, "name": "Alpha Vantage", "name_en": "Alpha Vantage", "desc": "股票/外汇数据 - Alpha Vantage API", "desc_en": "Stock/Forex data - Alpha Vantage API", "keywords": "股票/外汇/AlphaVantage/Stock/Forex"},
    {"id": 19, "name": "Public APIs Index", "name_en": "Public APIs Index", "desc": "公共 API 发现与集成 (400K+ stars)", "desc_en": "Public API discovery and integration (400K+ stars)", "keywords": "API/公共/发现/API/Public/Discovery"},
    {"id": 20, "name": "Flowsint Integration", "name_en": "Flowsint Integration", "desc": "OSINT 开源情报集成", "desc_en": "OSINT open-source intelligence integration", "keywords": "OSINT/情报/开源/OSINT/Intel/Open-source"},
    
    # 内容创作 Skills
    {"id": 21, "name": "Shanmu Reporter", "name_en": "Shanmu Reporter", "desc": "专业金融研报生成 - 规划→写作→编辑→图表", "desc_en": "Professional financial report generation - Plan→Write→Edit→Chart", "keywords": "研报/金融/报告/Report/Finance/Document"},
    {"id": 22, "name": "Social Media Scheduler", "name_en": "Social Media Scheduler", "desc": "社交媒体内容规划与排期", "desc_en": "Social media content planning and scheduling", "keywords": "社交/媒体/排期/Social/Media/Schedule"},
    {"id": 23, "name": "Social Publisher", "name_en": "Social Publisher", "desc": "自媒体多平台一键发布", "desc_en": "One-click multi-platform publishing for self-media", "keywords": "发布/自媒体/多平台/Publish/Self-media/Multi-platform"},
    {"id": 24, "name": "Content Scheduler", "name_en": "Content Scheduler", "desc": "内容排期与智能轮换", "desc_en": "Content scheduling and smart rotation", "keywords": "内容/排期/轮换/Content/Schedule/Rotation"},
    {"id": 25, "name": "Hot Topic Generator", "name_en": "Hot Topic Generator", "desc": "热门话题发现与生成", "desc_en": "Hot topic discovery and generation", "keywords": "热门/话题/生成/Hot/Topic/Generator"},
    {"id": 26, "name": "PPT Chart Generator", "name_en": "PPT Chart Generator", "desc": "PPT 图表自动生成", "desc_en": "Automatic PPT chart generation", "keywords": "PPT/图表/生成/PPT/Chart/Generate"},
    {"id": 27, "name": "Video Factory", "name_en": "Video Factory", "desc": "视频批量生成工厂", "desc_en": "Video batch generation factory", "keywords": "视频/批量/生成/Video/Batch/Factory"},
    {"id": 28, "name": "TTS", "name_en": "Text-to-Speech", "desc": "文字转语音", "desc_en": "Text to speech conversion", "keywords": "语音/TTS/转换/TTS/Speech/Voice"},
    
    # 技术开发 Skills
    {"id": 29, "name": "Browser Automation", "name_en": "Browser Automation", "desc": "浏览器自动化 - Playwright", "desc_en": "Browser automation - Playwright", "keywords": "浏览器/自动化/Playwright/Browser/Automation"},
    {"id": 30, "name": "PaddleOCR", "name_en": "PaddleOCR", "desc": "智能 OCR 与文档解析 (73.3K Stars)", "desc_en": "Smart OCR and document parsing (73.3K Stars)", "keywords": "OCR/文档/解析/OCR/Document/Parsing"},
    {"id": 31, "name": "Git Integration", "name_en": "Git Integration", "desc": "Git 版本控制集成", "desc_en": "Git version control integration", "keywords": "Git/版本/控制/Git/Version/Control"},
    {"id": 32, "name": "Docker CTL", "name_en": "Docker Control", "desc": "Docker 容器管理", "desc_en": "Docker container management", "keywords": "Docker/容器/管理/Docker/Container/Manage"},
    {"id": 33, "name": "K8s Deploy", "name_en": "Kubernetes Deploy", "desc": "Kubernetes 部署自动化", "desc_en": "Kubernetes deployment automation", "keywords": "K8s/Kubernetes/部署/K8s/Deploy"},
    {"id": 34, "name": "Terraform Apply", "name_en": "Terraform Apply", "desc": "基础设施即代码 (IaC)", "desc_en": "Infrastructure as Code (IaC)", "keywords": "Terraform/IaC/基础设施/Terraform/IaC"},
    {"id": 35, "name": "Rust Bridge", "name_en": "Rust Bridge", "desc": "Rust 语言桥接与编译", "desc_en": "Rust language bridging and compilation", "keywords": "Rust/编译/桥接/Rust/Compile/Bridge"},
    {"id": 36, "name": "LLM Finetune", "name_en": "LLM Fine-tuning", "desc": "大模型微调训练", "desc_en": "Large language model fine-tuning", "keywords": "LLM/微调/训练/LLM/Fine-tune/Train"},
    {"id": 37, "name": "Vector DB", "name_en": "Vector Database", "desc": "向量数据库操作", "desc_en": "Vector database operations", "keywords": "向量/数据库/Vector/Database/DB"},
    {"id": 38, "name": "RAG Pipeline", "name_en": "RAG Pipeline", "desc": "检索增强生成流水线", "desc_en": "Retrieval-Augmented Generation pipeline", "keywords": "RAG/检索/生成/RAG/Retrieval/Generation"},
    
    # 云服务 CLI Skills
    {"id": 39, "name": "AWS CLI", "name_en": "AWS CLI", "desc": "亚马逊云服务命令行", "desc_en": "Amazon Web Services command line", "keywords": "AWS/云/CLI/AWS/Cloud/CLI"},
    {"id": 40, "name": "Azure CLI", "name_en": "Azure CLI", "desc": "微软 Azure 云服务命令行", "desc_en": "Microsoft Azure cloud services command line", "keywords": "Azure/云/CLI/Azure/Cloud/CLI"},
    {"id": 41, "name": "GCP CLI", "name_en": "GCP CLI", "desc": "谷歌云服务命令行", "desc_en": "Google Cloud Platform command line", "keywords": "GCP/谷歌/云/GCP/Google/Cloud"},
    
    # 工具集成 Skills
    {"id": 42, "name": "Feishu", "name_en": "Feishu/Lark", "desc": "飞书消息/文档/多维表格操作", "desc_en": "Feishu messages/docs/bitable operations", "keywords": "飞书/文档/表格/Feishu/Lark/Doc"},
    {"id": 43, "name": "Notion DB", "name_en": "Notion Database", "desc": "Notion 数据库操作", "desc_en": "Notion database operations", "keywords": "Notion/数据库/Notion/Database"},
    {"id": 44, "name": "Airtable Sync", "name_en": "Airtable Sync", "desc": "Airtable 数据同步", "desc_en": "Airtable data synchronization", "keywords": "Airtable/同步/数据/Airtable/Sync/Data"},
    {"id": 45, "name": "Slack Notify", "name_en": "Slack Notify", "desc": "Slack 消息通知", "desc_en": "Slack message notifications", "keywords": "Slack/通知/消息/Slack/Notify/Message"},
    {"id": 46, "name": "Zapier Trigger", "name_en": "Zapier Trigger", "desc": "Zapier 自动化触发器", "desc_en": "Zapier automation triggers", "keywords": "Zapier/自动化/触发/Zapier/Automation/Trigger"},
    {"id": 47, "name": "SSH", "name_en": "SSH Remote", "desc": "SSH 远程控制", "desc_en": "SSH remote control", "keywords": "SSH/远程/控制/SSH/Remote/Control"},
    {"id": 48, "name": "Webhook Relay", "name_en": "Webhook Relay", "desc": "Webhook 中继与转发", "desc_en": "Webhook relay and forwarding", "keywords": "Webhook/中继/转发/Webhook/Relay/Forward"},
    
    # 系统管理 Skills
    {"id": 49, "name": "Bot Dashboard", "name_en": "Bot Dashboard", "desc": "Bot 状态监控面板", "desc_en": "Bot status monitoring dashboard", "keywords": "Bot/监控/面板/Bot/Monitor/Dashboard"},
    {"id": 50, "name": "Crontab Manager", "name_en": "Crontab Manager", "desc": "定时任务管理", "desc_en": "Scheduled task management", "keywords": "Cron/定时/任务/Cron/Schedule/Task"},
    {"id": 51, "name": "Self Check", "name_en": "Self Check", "desc": "系统自检", "desc_en": "System self-check", "keywords": "自检/系统/检查/Self-check/System/Check"},
    {"id": 52, "name": "Upgrade Guard", "name_en": "Upgrade Guard", "desc": "系统升级保护", "desc_en": "System upgrade protection", "keywords": "升级/保护/系统/Upgrade/Guard/System"},
    {"id": 53, "name": "NPM Audit", "name_en": "NPM Audit", "desc": "NPM 包安全审计", "desc_en": "NPM package security audit", "keywords": "NPM/安全/审计/NPM/Security/Audit"},
    {"id": 54, "name": "QA Supervisor", "name_en": "QA Supervisor", "desc": "质量监督", "desc_en": "Quality assurance supervision", "keywords": "QA/质量/监督/QA/Quality/Supervise"},
    
    # 场景与状态 Skills
    {"id": 55, "name": "Scenarios", "name_en": "Scenarios", "desc": "64 种心理/业务场景识别", "desc_en": "64 psychological/business scenario recognition", "keywords": "场景/心理/业务/Scenario/Psychology/Business"},
    {"id": 56, "name": "Today Stage", "name_en": "Today Stage", "desc": "今日阶段识别", "desc_en": "Today's stage recognition", "keywords": "今日/阶段/识别/Today/Stage/Recognize"},
    {"id": 57, "name": "Heal State", "name_en": "Heal State", "desc": "状态修复", "desc_en": "State healing and recovery", "keywords": "修复/状态/恢复/Heal/State/Recovery"},
    {"id": 58, "name": "Undercover Mode", "name_en": "Undercover Mode", "desc": "潜伏模式", "desc_en": "Undercover mode", "keywords": "潜伏/模式/隐藏/Undercover/Mode/Hide"},
    {"id": 59, "name": "Auto Exec", "name_en": "Auto Exec", "desc": "自动执行", "desc_en": "Automatic execution", "keywords": "自动/执行/Auto/Exec/Execute"},
    {"id": 60, "name": "Auto Retry Executor", "name_en": "Auto Retry Executor", "desc": "自动重试执行器", "desc_en": "Automatic retry executor", "keywords": "重试/自动/执行/Retry/Auto/Executor"},
    
    # 增长与变现 Skills
    {"id": 61, "name": "Growth Experiment", "name_en": "Growth Experiment", "desc": "A/B 测试 + 统计检验", "desc_en": "A/B testing + statistical validation", "keywords": "增长/A/B 测试/实验/Growth/AB-Test/Experiment"},
    {"id": 62, "name": "ROI Tracker", "name_en": "ROI Tracker", "desc": "收入/成本追踪", "desc_en": "Revenue/cost tracking", "keywords": "ROI/收入/追踪/ROI/Revenue/Track"},
    {"id": 63, "name": "Gumroad", "name_en": "Gumroad", "desc": "Gumroad 产品上架与销售", "desc_en": "Gumroad product listing and sales", "keywords": "Gumroad/销售/产品/Gumroad/Sales/Product"},
    {"id": 64, "name": "Marketplace", "name_en": "Skills Marketplace", "desc": "技能市场管理", "desc_en": "Skills marketplace management", "keywords": "市场/技能/管理/Marketplace/Skills/Manage"},
    
    # 其他工具 Skills
    {"id": 65, "name": "ASCII Art", "name_en": "ASCII Art", "desc": "ASCII 艺术生成", "desc_en": "ASCII art generation", "keywords": "ASCII/艺术/生成/ASCII/Art/Generate"},
    {"id": 66, "name": "Easter Egg", "name_en": "Easter Egg", "desc": "彩蛋功能", "desc_en": "Easter egg features", "keywords": "彩蛋/惊喜/功能/Easter-Egg/Surprise/Feature"},
    {"id": 67, "name": "Pet Companion", "name_en": "Pet Companion", "desc": "宠物陪伴", "desc_en": "Pet companion", "keywords": "宠物/陪伴/娱乐/Pet/Companion/Fun"},
    {"id": 68, "name": "TV Control", "name_en": "TV Control", "desc": "电视控制", "desc_en": "TV control", "keywords": "电视/控制/智能/TV/Control/Smart"},
    {"id": 69, "name": "Yijing", "name_en": "Yijing (I Ching)", "desc": "易经占卜", "desc_en": "I Ching divination", "keywords": "易经/占卜/传统/Yijing/I-Ching/Divination"},
    {"id": 70, "name": "Model Empathy Router", "name_en": "Model Empathy Router", "desc": "模型共情路由", "desc_en": "Model empathy routing", "keywords": "模型/共情/路由/Model/Empathy/Router"},
    
    # 工作流 Skills
    {"id": 71, "name": "Task Orchestrator", "name_en": "Task Orchestrator", "desc": "任务编排与调度", "desc_en": "Task orchestration and scheduling", "keywords": "任务/编排/调度/Task/Orchestrate/Schedule"},
    {"id": 72, "name": "Ecommerce Workflow", "name_en": "Ecommerce Workflow", "desc": "电商工作流 (Medusa)", "desc_en": "Ecommerce workflow (Medusa)", "keywords": "电商/工作流/Medusa/Ecommerce/Workflow"},
    {"id": 73, "name": "Arc Reel Workflow", "name_en": "Arc Reel Workflow", "desc": "短视频工作流", "desc_en": "Short video workflow", "keywords": "短视频/工作流/视频/Short-Video/Workflow"},
    {"id": 74, "name": "The Well Processor", "name_en": "The Well Processor", "desc": "The Well 数据集处理", "desc_en": "The Well dataset processing", "keywords": "数据集/处理/The-Well/Dataset/Process"},
    {"id": 75, "name": "China Textbook Search", "name_en": "China Textbook Search", "desc": "中文教材检索", "desc_en": "Chinese textbook search", "keywords": "教材/检索/中文/Textbook/Search/Chinese"},
    
    # 地理自动化 Skills
    {"id": 76, "name": "Geo Automation", "name_en": "Geo Automation", "desc": "地理空间自动化", "desc_en": "Geospatial automation", "keywords": "地理/空间/自动化/Geo/Spatial/Automation"},
    {"id": 77, "name": "GEO SEO Optimizer", "name_en": "GEO SEO Optimizer", "desc": "生成式 AI 搜索引擎优化", "desc_en": "Generative AI search engine optimization", "keywords": "GEO/SEO/优化/GEO/SEO/Optimize"},
]

def create_pdf(output_path: str):
    """创建 PDF 文档"""
    
    # 创建文档（横向 A4）
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    # 标题
    title = Paragraph("太一 AGI · Skills 功能汇总", title_style)
    elements.append(title)
    
    subtitle = Paragraph(f"Taiyi AGI · Skills Function Summary | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.5*cm))
    
    # 统计信息
    stats_text = f"""
    <b>技能总数:</b> {len(SKILLS_DATA)} | 
    <b>核心 Bot:</b> 8 | 
    <b>交易金融:</b> 6 | 
    <b>数据采集:</b> 6 | 
    <b>内容创作:</b> 8 | 
    <b>技术开发:</b> 10 | 
    <b>云服务:</b> 3 | 
    <b>工具集成:</b> 8 | 
    <b>系统管理:</b> 6 | 
    <b>其他:</b> 16
    """
    stats = Paragraph(stats_text, styles['Normal'])
    elements.append(stats)
    elements.append(Spacer(1, 0.5*cm))
    
    # 表格数据
    table_data = [["序号", "技能名称 (中文)", "Skill Name (EN)", "功能描述 (中文)", "Function Description (EN)", "关键词 (Keywords)"]]
    
    for skill in SKILLS_DATA:
        table_data.append([
            str(skill['id']),
            skill['name'],
            skill['name_en'],
            skill['desc'],
            skill['desc_en'],
            skill['keywords']
        ])
    
    # 创建表格
    table = Table(table_data, colWidths=[0.8*cm, 3*cm, 3*cm, 5*cm, 5*cm, 5*cm])
    
    # 表格样式
    table.setStyle(TableStyle([
        # 背景色
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#34495e')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
        
        # 文字颜色
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),
        
        # 对齐
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        
        # 字体
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTNAME', (0, 2), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Oblique'),
        
        # 字体大小
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        ('FONTSIZE', (0, 2), (-1, -1), 8),
        
        # 行高
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#34495e')),
        ('LINEBELOW', (0, 1), (-1, 1), 1, colors.HexColor('#bdc3c7')),
        ('LINEBELOW', (0, 2), (-1, -2), 0.5, colors.HexColor('#ecf0f1')),
        
        # 内边距
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(table)
    
    # 页脚
    elements.append(Spacer(1, 1*cm))
    footer = Paragraph(
        f"<i>太一 AGI 系统 · 技能总数：{len(SKILLS_DATA)} · 最后更新：{datetime.now().strftime('%Y-%m-%d')}</i>",
        styles['Normal']
    )
    elements.append(footer)
    
    # 构建 PDF
    doc.build(elements)
    print(f"✅ PDF 已生成：{output_path}")


def main():
    output_dir = Path("/home/nicola/.openclaw/workspace/reports")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"skills-summary_{timestamp}.pdf"
    
    create_pdf(str(output_path))
    print(f"\n📄 文件位置：{output_path}")
    print(f"📊 技能总数：{len(SKILLS_DATA)}")


if __name__ == '__main__':
    main()
