#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
山木研报生成器 - PaddleOCR 集成模块

功能：
- PDF 研报自动解析
- 结构化内容提取
- Markdown 组装

创建时间：2026-04-06 08:15
依据：DEEP-LEARNING-EXECUTION.md 学习后立即执行原则

集成点：
- skills/shanmu-reporter/scripts/report_generator.py
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.ocr_tools import OCRTools


class ShanmuReportParser:
    """山木研报解析器 - PaddleOCR 增强版"""
    
    def __init__(self, lang: str = 'ch', use_gpu: bool = False):
        """
        初始化解析器
        
        Args:
            lang: 语言代码
            use_gpu: 是否使用 GPU
        """
        self.ocr = OCRTools(lang=lang, use_gpu=use_gpu)
        self.lang = lang
        self.use_gpu = use_gpu
        
        print(f"✅ 山木研报解析器初始化完成 (语言：{lang}, GPU: {use_gpu})")
    
    def parse_research_report(self, pdf_path: str) -> Dict:
        """
        解析券商研报
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            {
                "title": str,
                "analyst": str,
                "firm": str,
                "date": str,
                "summary": str,
                "sections": [...],
                "tables": [...],
                "charts": [...],
                "markdown": str
            }
        """
        print(f"📊 解析研报：{pdf_path}")
        
        # 使用 OCR 解析 PDF
        from ppstructure.utility import init_args
        from ppstructure.predict_system import StructureSystem
        
        args = init_args()
        args.lang = self.lang
        args.use_gpu = self.use_gpu
        args.output = './temp_output'
        args.log_warn = False
        
        engine = StructureSystem(args=args)
        result = engine(pdf_path)
        
        # 结构化提取
        parsed = {
            "source_file": pdf_path,
            "title": "",
            "analyst": "",
            "firm": "",
            "date": "",
            "summary": "",
            "sections": [],
            "tables": [],
            "charts": [],
            "markdown": "",
            "metadata": {
                "language": self.lang,
                "use_gpu": self.use_gpu,
                "parsed_at": datetime.now().isoformat(),
                "total_elements": len(result)
            }
        }
        
        # 遍历解析结果
        markdown_parts = []
        
        for i, item in enumerate(result):
            item_type = item.get('type', 'text')
            text = item.get('text', '')
            
            if not text:
                continue
            
            # 标题识别（通常在前 5 个元素中）
            if i < 5 and item_type == 'title':
                if not parsed['title']:
                    parsed['title'] = text
                    markdown_parts.append(f"# {text}\n")
                continue
            
            # 分析师/机构信息
            if '分析师' in text or '分析师:' in text:
                parsed['analyst'] = text
            if '证券' in text and '公司' in text:
                parsed['firm'] = text
            
            # 日期识别
            if any(x in text for x in ['年', '月', '日', '202', '203']):
                if not parsed['date']:
                    parsed['date'] = text
            
            # 内容分类
            if item_type == 'text':
                parsed['sections'].append({
                    "type": "text",
                    "content": text,
                    "order": len(parsed['sections'])
                })
                markdown_parts.append(text)
            
            elif item_type == 'table':
                table_data = {
                    "type": "table",
                    "cells": item.get('cells', []),
                    "order": len(parsed['tables'])
                }
                parsed['tables'].append(table_data)
                markdown_parts.append(self._table_to_markdown(table_data['cells']))
            
            elif item_type == 'figure':
                parsed['charts'].append({
                    "type": "figure",
                    "path": item.get('path', ''),
                    "order": len(parsed['charts'])
                })
                markdown_parts.append(f"![图表 {len(parsed['charts'])}]({item.get('path', '')})")
        
        # 组装 Markdown
        parsed['markdown'] = "\n\n".join(markdown_parts)
        
        # 智能摘要（取前 3 段）
        text_sections = [s for s in parsed['sections'] if s['type'] == 'text']
        if text_sections:
            parsed['summary'] = "\n".join([s['content'] for s in text_sections[:3]])
        
        print(f"✅ 研报解析完成")
        print(f"   标题：{parsed['title'][:50]}...")
        print(f"   章节数：{len(parsed['sections'])}")
        print(f"   表格数：{len(parsed['tables'])}")
        print(f"   图表数：{len(parsed['charts'])}")
        
        return parsed
    
    def _table_to_markdown(self, cells: List[List[str]]) -> str:
        """表格转 Markdown"""
        if not cells:
            return ""
        
        lines = []
        for i, row in enumerate(cells):
            line = "| " + " | ".join(str(cell) for cell in row) + " |"
            lines.append(line)
            if i == 0:
                separator = "|" + "|".join("---" for _ in row) + "|"
                lines.append(separator)
        
        return "\n".join(lines)
    
    def save_report(self, parsed: Dict, output_dir: str) -> str:
        """
        保存解析结果
        
        Args:
            parsed: 解析结果字典
            output_dir: 输出目录
            
        Returns:
            保存的 Markdown 文件路径
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        base_name = Path(parsed['source_file']).stem
        md_path = os.path.join(output_dir, f"{base_name}.md")
        json_path = os.path.join(output_dir, f"{base_name}.json")
        
        # 保存 Markdown
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(parsed['markdown'])
        
        # 保存 JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 报告已保存:")
        print(f"   - {md_path}")
        print(f"   - {json_path}")
        
        return md_path
    
    def batch_parse_reports(self, input_dir: str, output_dir: str) -> Dict:
        """
        批量解析研报文件夹
        
        Args:
            input_dir: 输入文件夹（包含 PDF）
            output_dir: 输出文件夹
            
        Returns:
            统计信息
        """
        stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "reports": []
        }
        
        # 遍历 PDF 文件
        for pdf_file in Path(input_dir).glob('*.pdf'):
            stats["total"] += 1
            
            try:
                print(f"\n📄 [{stats['total']}] 解析：{pdf_file.name}")
                
                # 解析单个报告
                parsed = self.parse_research_report(str(pdf_file))
                
                # 保存结果
                self.save_report(parsed, output_dir)
                
                stats["success"] += 1
                stats["reports"].append({
                    "file": pdf_file.name,
                    "status": "success",
                    "title": parsed['title']
                })
                
            except Exception as e:
                stats["failed"] += 1
                stats["reports"].append({
                    "file": pdf_file.name,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"❌ 解析失败：{pdf_file.name} - {e}")
        
        # 保存统计
        stats_path = os.path.join(output_dir, 'batch_stats.json')
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 批量解析完成：{stats['success']}/{stats['total']} 成功")
        return stats


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='山木研报解析器 - PaddleOCR 集成')
    parser.add_argument('--pdf', type=str, help='单个 PDF 文件路径')
    parser.add_argument('--batch', type=str, help='批量处理文件夹')
    parser.add_argument('--output', type=str, default='./output', help='输出目录')
    parser.add_argument('--lang', type=str, default='ch', help='语言代码')
    parser.add_argument('--gpu', action='store_true', help='使用 GPU')
    
    args = parser.parse_args()
    
    # 初始化解析器
    parser_obj = ShanmuReportParser(lang=args.lang, use_gpu=args.gpu)
    
    if args.pdf:
        # 单个 PDF
        if not os.path.exists(args.pdf):
            print(f"❌ 文件不存在：{args.pdf}")
            sys.exit(1)
        
        parsed = parser_obj.parse_research_report(args.pdf)
        parser_obj.save_report(parsed, args.output)
    
    elif args.batch:
        # 批量处理
        if not os.path.exists(args.batch):
            print(f"❌ 文件夹不存在：{args.batch}")
            sys.exit(1)
        
        stats = parser_obj.batch_parse_reports(args.batch, args.output)
        print(f"\n总计：{stats['success']} 成功，{stats['failed']} 失败")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
