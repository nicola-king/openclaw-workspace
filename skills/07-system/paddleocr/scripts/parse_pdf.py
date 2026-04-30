#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 文档解析脚本 - 太一 AGI 集成版

用途：
- 将 PDF 研报/文档解析为 Markdown
- 提取表格、图表、公式
- 输出结构化 JSON

创建时间：2026-04-06 08:15
依据：DEEP-LEARNING-EXECUTION.md 学习后立即执行原则

使用示例：
    python scripts/parse_pdf.py --pdf ./report.pdf --output ./output/
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.ocr_tools import OCRTools


def parse_pdf_report(pdf_path: str, output_dir: str, lang: str = 'ch', use_gpu: bool = False):
    """
    解析 PDF 研报
    
    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录
        lang: 语言代码
        use_gpu: 是否使用 GPU
    """
    print(f"🔍 开始解析 PDF: {pdf_path}")
    print(f"📁 输出目录：{output_dir}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化 OCR 工具
    ocr = OCRTools(lang=lang, use_gpu=use_gpu)
    
    # 解析 PDF
    start_time = datetime.now()
    markdown_content = ocr.parse_to_markdown(pdf_path, output_dir)
    end_time = datetime.now()
    
    # 生成元数据
    metadata = {
        "source_file": str(pdf_path),
        "output_directory": output_dir,
        "language": lang,
        "use_gpu": use_gpu,
        "processing_time_seconds": (end_time - start_time).total_seconds(),
        "timestamp": datetime.now().isoformat(),
        "tool_version": "1.0",
        "created_by": "太一 AGI - PaddleOCR Skill"
    }
    
    # 保存元数据
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 解析完成！")
    print(f"⏱️  耗时：{metadata['processing_time_seconds']:.2f} 秒")
    print(f"📄 输出文件:")
    print(f"   - {output_dir}/{Path(pdf_path).stem}.md")
    print(f"   - {metadata_path}")
    
    return metadata


def main():
    parser = argparse.ArgumentParser(
        description='PDF 文档解析 - 太一 AGI PaddleOCR Skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 解析单个 PDF
  python parse_pdf.py --pdf ./report.pdf --output ./output/
  
  # 使用 GPU 加速
  python parse_pdf.py --pdf ./report.pdf --output ./output/ --gpu
  
  # 指定语言（英文）
  python parse_pdf.py --pdf ./report.pdf --output ./output/ --lang en
        """
    )
    
    parser.add_argument('--pdf', type=str, required=True, help='PDF 文件路径')
    parser.add_argument('--output', type=str, default='./output', help='输出目录')
    parser.add_argument('--lang', type=str, default='ch', choices=['ch', 'en', 'japan', 'korean'], help='语言代码')
    parser.add_argument('--gpu', action='store_true', help='使用 GPU 加速')
    parser.add_argument('--verbose', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.pdf):
        print(f"❌ 文件不存在：{args.pdf}")
        sys.exit(1)
    
    # 执行解析
    try:
        metadata = parse_pdf_report(
            pdf_path=args.pdf,
            output_dir=args.output,
            lang=args.lang,
            use_gpu=args.gpu
        )
        
        if args.verbose:
            print(f"\n📊 元数据:")
            print(json.dumps(metadata, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 解析失败：{e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
