#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaddleOCR 批量处理脚本

用途：
- 批量 OCR 图片文件夹
- 批量解析 PDF 文件夹
- 自动生成统计报告

创建时间：2026-04-06 08:15
依据：DEEP-LEARNING-EXECUTION.md 学习后立即执行原则

使用示例：
    python batch_processor.py --input ./images/ --output ./results/
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.ocr_tools import OCRTools


class BatchProcessor:
    """批量 OCR 处理器"""
    
    def __init__(self, lang: str = 'ch', use_gpu: bool = False):
        """
        初始化批量处理器
        
        Args:
            lang: 语言代码
            use_gpu: 是否使用 GPU
        """
        self.ocr = OCRTools(lang=lang, use_gpu=use_gpu)
        self.lang = lang
        self.use_gpu = use_gpu
    
    def process_images(self, input_dir: str, output_dir: str) -> Dict:
        """
        批量处理图片文件夹
        
        Args:
            input_dir: 输入文件夹
            output_dir: 输出文件夹
            
        Returns:
            统计信息
        """
        stats = {
            "type": "images",
            "total": 0,
            "success": 0,
            "failed": 0,
            "files": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 支持的图片格式
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        
        # 遍历文件
        for file_path in Path(input_dir).rglob('*'):
            if file_path.suffix.lower() not in image_extensions:
                continue
            
            stats["total"] += 1
            output_name = file_path.stem
            
            try:
                # OCR 识别
                text = self.ocr.extract_text(str(file_path))
                
                # 保存结果
                output_path = os.path.join(output_dir, f"{output_name}.txt")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # 保存详细信息（含边界框）
                details = self.ocr.extract_with_bbox(str(file_path))
                details_path = os.path.join(output_dir, f"{output_name}.json")
                with open(details_path, 'w', encoding='utf-8') as f:
                    json.dump(details, f, ensure_ascii=False, indent=2)
                
                stats["success"] += 1
                stats["files"].append({
                    "file": file_path.name,
                    "status": "success",
                    "output": f"{output_name}.txt",
                    "char_count": len(text)
                })
                
                print(f"✅ [{stats['success']}] {file_path.name}")
                
            except Exception as e:
                stats["failed"] += 1
                stats["files"].append({
                    "file": file_path.name,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"❌ [{stats['failed']}] {file_path.name} - {e}")
        
        stats["completed_at"] = datetime.now().isoformat()
        
        # 保存统计
        stats_path = os.path.join(output_dir, 'batch_stats.json')
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        # 生成汇总报告
        self._generate_report(stats, output_dir)
        
        return stats
    
    def process_pdfs(self, input_dir: str, output_dir: str) -> Dict:
        """
        批量处理 PDF 文件夹
        
        Args:
            input_dir: 输入文件夹
            output_dir: 输出文件夹
            
        Returns:
            统计信息
        """
        stats = {
            "type": "pdfs",
            "total": 0,
            "success": 0,
            "failed": 0,
            "files": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 遍历 PDF 文件
        for pdf_path in Path(input_dir).rglob('*.pdf'):
            stats["total"] += 1
            output_name = pdf_path.stem
            
            try:
                # PDF 解析
                pdf_output_dir = os.path.join(output_dir, output_name)
                markdown = self.ocr.parse_to_markdown(str(pdf_path), pdf_output_dir)
                
                stats["success"] += 1
                stats["files"].append({
                    "file": pdf_path.name,
                    "status": "success",
                    "output_dir": output_name
                })
                
                print(f"✅ [{stats['success']}] {pdf_path.name}")
                
            except Exception as e:
                stats["failed"] += 1
                stats["files"].append({
                    "file": pdf_path.name,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"❌ [{stats['failed']}] {pdf_path.name} - {e}")
        
        stats["completed_at"] = datetime.now().isoformat()
        
        # 保存统计
        stats_path = os.path.join(output_dir, 'batch_stats.json')
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        # 生成汇总报告
        self._generate_report(stats, output_dir)
        
        return stats
    
    def _generate_report(self, stats: Dict, output_dir: str):
        """生成处理报告"""
        report_path = os.path.join(output_dir, 'report.md')
        
        duration = None
        if stats['completed_at']:
            start = datetime.fromisoformat(stats['started_at'])
            end = datetime.fromisoformat(stats['completed_at'])
            duration = (end - start).total_seconds()
        
        success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        report = f"""# PaddleOCR 批量处理报告

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> 太一 AGI - PaddleOCR Skill v1.0

---

## 📊 统计概览

| 指标 | 数值 |
|------|------|
| **处理类型** | {stats['type']} |
| **总文件数** | {stats['total']} |
| **成功** | {stats['success']} |
| **失败** | {stats['failed']} |
| **成功率** | {success_rate:.1f}% |
| **耗时** | {duration:.2f}秒 (如有) |

---

## 📁 文件列表

| # | 文件名 | 状态 | 详情 |
|---|--------|------|------|
"""
        
        for i, file_info in enumerate(stats['files'], 1):
            status = "✅" if file_info['status'] == 'success' else "❌"
            detail = file_info.get('output', file_info.get('error', 'N/A'))
            report += f"| {i} | {file_info['file']} | {status} | {detail} |\n"
        
        report += f"\n---\n\n*报告生成：太一 AGI | {datetime.now().strftime('%Y-%m-%d')}*\n"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 报告已保存：{report_path}")


def main():
    parser = argparse.ArgumentParser(description='PaddleOCR 批量处理器')
    parser.add_argument('--input', type=str, required=True, help='输入文件夹')
    parser.add_argument('--output', type=str, default='./output', help='输出目录')
    parser.add_argument('--type', type=str, choices=['auto', 'images', 'pdfs'], default='auto', help='处理类型')
    parser.add_argument('--lang', type=str, default='ch', help='语言代码')
    parser.add_argument('--gpu', action='store_true', help='使用 GPU')
    
    args = parser.parse_args()
    
    # 检查输入文件夹
    if not os.path.exists(args.input):
        print(f"❌ 文件夹不存在：{args.input}")
        sys.exit(1)
    
    # 初始化处理器
    processor = BatchProcessor(lang=args.lang, use_gpu=args.gpu)
    
    # 自动检测或指定类型
    if args.type == 'auto':
        # 检测主要文件类型
        pdf_count = len(list(Path(args.input).rglob('*.pdf')))
        image_count = len(list(Path(args.input).rglob('*.jpg'))) + \
                     len(list(Path(args.input).rglob('*.png')))
        
        process_type = 'pdfs' if pdf_count > image_count else 'images'
        print(f"🔍 自动检测：{process_type} (PDF: {pdf_count}, 图片：{image_count})")
    else:
        process_type = args.type
    
    # 执行处理
    if process_type == 'images':
        stats = processor.process_images(args.input, args.output)
    else:
        stats = processor.process_pdfs(args.input, args.output)
    
    # 打印汇总
    print(f"\n{'='*50}")
    print(f"📊 处理完成")
    print(f"{'='*50}")
    print(f"总计：{stats['total']} 文件")
    print(f"成功：{stats['success']} ({stats['success']/stats['total']*100:.1f}%)")
    print(f"失败：{stats['failed']}")
    print(f"输出：{args.output}/")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
