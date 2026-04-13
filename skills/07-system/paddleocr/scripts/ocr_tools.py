#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaddleOCR 工具集 - 太一 AGI 集成版

功能：
- 单图片 OCR 文字识别
- PDF 文档解析为 Markdown
- 表格提取
- 批量处理

创建时间：2026-04-06 08:15
依据：DEEP-LEARNING-EXECUTION.md 学习后立即执行原则
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Union

try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    print("⚠️  PaddleOCR 未安装，请运行：pip install paddleocr")


class OCRTools:
    """PaddleOCR 封装工具类"""
    
    def __init__(self, lang: str = 'ch', use_gpu: bool = False, use_angle_cls: bool = True):
        """
        初始化 OCR 工具
        
        Args:
            lang: 语言代码 ('ch', 'en', 'japan', 'korean' 等 111 种)
            use_gpu: 是否使用 GPU 加速
            use_angle_cls: 是否使用文字方向分类器
        """
        if not PADDLEOCR_AVAILABLE:
            raise ImportError("PaddleOCR 未安装")
        
        self.lang = lang
        self.use_gpu = use_gpu
        self.use_angle_cls = use_angle_cls
        
        # 初始化 PaddleOCR
        self.ocr = PaddleOCR(
            lang=lang,
            use_gpu=use_gpu,
            log_warn=False,
            det_db_thresh=0.3,
            det_db_box_thresh=0.5,
            rec_batch_num=6
        )
        
        print(f"✅ PaddleOCR 初始化完成 (语言：{lang}, GPU: {use_gpu})")
    
    def extract_text(self, image_path: str) -> str:
        """
        从图片提取文字
        
        Args:
            image_path: 图片路径或 URL
            
        Returns:
            识别的文字内容
        """
        result = self.ocr.ocr(image_path, cls=self.use_angle_cls)
        
        if not result or not result[0]:
            return ""
        
        # 提取文字内容
        texts = []
        for line in result[0]:
            if line and len(line) >= 2:
                texts.append(line[1][0])
        
        return "\n".join(texts)
    
    def extract_with_bbox(self, image_path: str) -> List[Dict]:
        """
        提取文字及边界框
        
        Args:
            image_path: 图片路径
            
        Returns:
            [{"text": str, "bbox": List, "confidence": float}, ...]
        """
        result = self.ocr.ocr(image_path, cls=self.use_angle_cls)
        
        if not result or not result[0]:
            return []
        
        extracted = []
        for line in result[0]:
            if line and len(line) >= 2:
                bbox, (text, confidence) = line
                extracted.append({
                    "text": text,
                    "bbox": bbox,
                    "confidence": confidence
                })
        
        return extracted
    
    def parse_to_markdown(self, pdf_path: str, output_dir: Optional[str] = None) -> str:
        """
        解析 PDF 文档为 Markdown
        
        Args:
            pdf_path: PDF 文件路径
            output_dir: 输出目录（可选）
            
        Returns:
            Markdown 格式内容
        """
        # 使用 PP-Structure 进行文档解析
        from ppstructure.utility import init_args
        from ppstructure.predict_system import StructureSystem
        
        args = init_args()
        args.lang = self.lang
        args.use_gpu = self.use_gpu
        args.output = output_dir or './output'
        
        engine = StructureSystem(args=args)
        
        # 解析 PDF
        result = engine(pdf_path)
        
        # 转换为 Markdown
        markdown_lines = []
        for item in result:
            if item['type'] == 'text':
                markdown_lines.append(item['text'])
            elif item['type'] == 'table':
                markdown_lines.append(self._table_to_markdown(item['cells']))
            elif item['type'] == 'title':
                markdown_lines.append(f"# {item['text']}")
            elif item['type'] == 'figure':
                markdown_lines.append(f"![Figure]({item.get('path', '')})")
        
        markdown_content = "\n\n".join(markdown_lines)
        
        # 保存到文件
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, Path(pdf_path).stem + '.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"✅ Markdown 已保存：{output_path}")
        
        return markdown_content
    
    def _table_to_markdown(self, cells: List[List[str]]) -> str:
        """将表格单元格转换为 Markdown 格式"""
        if not cells:
            return ""
        
        lines = []
        for i, row in enumerate(cells):
            line = "| " + " | ".join(str(cell) for cell in row) + " |"
            lines.append(line)
            if i == 0:
                # 添加分隔符
                separator = "|" + "|".join("---" for _ in row) + "|"
                lines.append(separator)
        
        return "\n".join(lines)
    
    def extract_table(self, image_path: str) -> List[List[str]]:
        """
        从图片提取表格
        
        Args:
            image_path: 图片路径
            
        Returns:
            二维列表 [[cell1, cell2, ...], ...]
        """
        from ppstructure.utility import init_args
        from ppstructure.predict_system import StructureSystem
        
        args = init_args()
        args.lang = self.lang
        args.use_gpu = self.use_gpu
        args.type = 'table'
        
        engine = StructureSystem(args=args)
        result = engine(image_path)
        
        tables = []
        for item in result:
            if item['type'] == 'table':
                tables.append(item['cells'])
        
        return tables if tables else []
    
    def batch_process(self, input_dir: str, output_dir: str, file_types: List[str] = None) -> Dict:
        """
        批量处理文件夹
        
        Args:
            input_dir: 输入文件夹
            output_dir: 输出文件夹
            file_types: 文件类型列表 ['.jpg', '.png', '.pdf']
            
        Returns:
            处理统计信息
        """
        if file_types is None:
            file_types = ['.jpg', '.jpeg', '.png', '.pdf', '.bmp']
        
        os.makedirs(output_dir, exist_ok=True)
        
        stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "files": []
        }
        
        # 遍历文件
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in file_types):
                    stats["total"] += 1
                    input_path = os.path.join(root, file)
                    output_name = Path(file).stem
                    
                    try:
                        if file.lower().endswith('.pdf'):
                            # PDF 解析
                            markdown = self.parse_to_markdown(
                                input_path, 
                                os.path.join(output_dir, output_name)
                            )
                        else:
                            # 图片 OCR
                            text = self.extract_text(input_path)
                            output_path = os.path.join(output_dir, output_name + '.txt')
                            with open(output_path, 'w', encoding='utf-8') as f:
                                f.write(text)
                        
                        stats["success"] += 1
                        stats["files"].append({
                            "file": file,
                            "status": "success",
                            "output": output_name
                        })
                        print(f"✅ 处理完成：{file}")
                        
                    except Exception as e:
                        stats["failed"] += 1
                        stats["files"].append({
                            "file": file,
                            "status": "failed",
                            "error": str(e)
                        })
                        print(f"❌ 处理失败：{file} - {e}")
        
        # 保存统计信息
        stats_path = os.path.join(output_dir, 'stats.json')
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 批量处理完成：{stats['success']}/{stats['total']} 成功")
        return stats


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PaddleOCR 工具集 - 太一 AGI')
    parser.add_argument('--image', type=str, help='图片路径')
    parser.add_argument('--pdf', type=str, help='PDF 文件路径')
    parser.add_argument('--batch', type=str, help='批量处理文件夹')
    parser.add_argument('--output', type=str, default='./output', help='输出目录')
    parser.add_argument('--lang', type=str, default='ch', help='语言代码')
    parser.add_argument('--gpu', action='store_true', help='使用 GPU 加速')
    
    args = parser.parse_args()
    
    # 初始化工具
    ocr = OCRTools(lang=args.lang, use_gpu=args.gpu)
    
    if args.image:
        # 单图片 OCR
        text = ocr.extract_text(args.image)
        print("\n" + "="*50)
        print("识别结果：")
        print("="*50)
        print(text)
        print("="*50)
    
    elif args.pdf:
        # PDF 解析
        markdown = ocr.parse_to_markdown(args.pdf, args.output)
        print(f"\n✅ PDF 已解析为 Markdown，保存到：{args.output}/")
    
    elif args.batch:
        # 批量处理
        stats = ocr.batch_process(args.batch, args.output)
        print(f"\n📊 统计：{stats['success']}/{stats['total']} 成功")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
