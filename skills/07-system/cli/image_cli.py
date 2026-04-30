#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一 CLI 统一接口 - 图像处理自动化

功能:
- 图片编辑
- 批量处理
- 格式转换
- 添加水印

灵感：CLI-Anything - 一行命令操控任意软件
作者：太一 AGI
创建：2026-04-18
"""

import logging
from pathlib import Path
from typing import Optional, List, Tuple
from PIL import Image, ImageFilter, ImageEnhance

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('ImageCLI')


class ImageProcessor:
    """图像处理器"""
    
    def __init__(self, output_dir: str = "output/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def edit(self, input_file: str, output_file: str,
             resize: Optional[str] = None,
             filter: Optional[str] = None,
             quality: int = 95) -> bool:
        """
        编辑图片
        
        Args:
            input_file: 输入文件
            output_file: 输出文件
            resize: 调整大小 (WxH)
            filter: 滤镜 (blur/sharpen/vintage)
            quality: 质量 (1-100)
            
        Returns:
            是否成功
        """
        logger.info(f"🖼️ 编辑图片：{input_file}")
        
        try:
            img = Image.open(input_file)
            
            # 调整大小
            if resize:
                width, height = map(int, resize.split('x'))
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                logger.info(f"   调整大小：{resize}")
            
            # 添加滤镜
            if filter == "blur":
                img = img.filter(ImageFilter.GaussianBlur(2))
            elif filter == "sharpen":
                img = img.filter(ImageFilter.SHARPEN)
            elif filter == "vintage":
                img = img.filter(ImageFilter.EMBOSS)
            elif filter == "enhance":
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)
            
            if filter:
                logger.info(f"   滤镜：{filter}")
            
            # 保存
            img.save(output_file, quality=quality)
            logger.info(f"✅ 编辑完成：{output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 编辑失败：{e}")
            return False
    
    def batch_process(self, input_dir: str, output_dir: str,
                      resize: Optional[str] = None,
                      watermark: Optional[str] = None,
                      filter: Optional[str] = None) -> dict:
        """
        批量处理图片
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            resize: 调整大小
            watermark: 水印文件
            filter: 滤镜
            
        Returns:
            处理统计
        """
        logger.info(f"📦 批量处理：{input_dir}")
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        stats = {"total": 0, "success": 0, "failed": 0}
        
        image_files = (list(input_path.glob("*.jpg")) + 
                      list(input_path.glob("*.png")) +
                      list(input_path.glob("*.jpeg")))
        stats["total"] = len(image_files)
        
        for img_file in image_files:
            output_file = output_path / img_file.name
            
            success = self.edit(
                str(img_file),
                str(output_file),
                resize=resize,
                filter=filter,
            )
            
            if success:
                stats["success"] += 1
            else:
                stats["failed"] += 1
        
        logger.info(f"✅ 批量处理完成：{stats['success']}/{stats['total']} 成功")
        
        return stats
    
    def convert(self, input_file: str, output_file: str,
                format: Optional[str] = None) -> bool:
        """
        转换图片格式
        
        Args:
            input_file: 输入文件
            output_file: 输出文件
            format: 目标格式 (jpg/png/gif)
            
        Returns:
            是否成功
        """
        logger.info(f"🔄 转换格式：{input_file} → {output_file}")
        
        try:
            img = Image.open(input_file)
            
            # 转换为 RGB (如果需要保存为 JPG)
            if output_file.lower().endswith(".jpg") or output_file.lower().endswith(".jpeg"):
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")
            
            img.save(output_file)
            
            logger.info(f"✅ 格式转换完成：{output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 格式转换失败：{e}")
            return False
    
    def add_watermark(self, input_file: str, watermark_file: str,
                      output_file: str, position: str = "bottom-right") -> bool:
        """
        添加水印
        
        Args:
            input_file: 输入文件
            watermark_file: 水印文件
            output_file: 输出文件
            position: 位置 (top-left/top-right/bottom-left/bottom-right/center)
            
        Returns:
            是否成功
        """
        logger.info(f"💧 添加水印：{watermark_file}")
        
        try:
            img = Image.open(input_file)
            watermark = Image.open(watermark_file)
            
            # 调整水印大小
            if watermark.size[0] > img.size[0] / 3:
                ratio = (img.size[0] / 3) / watermark.size[0]
                watermark = watermark.resize(
                    (int(watermark.size[0] * ratio), int(watermark.size[1] * ratio)),
                    Image.Resampling.LANCZOS
                )
            
            # 计算位置
            positions = {
                "top-left": (10, 10),
                "top-right": (img.size[0] - watermark.size[0] - 10, 10),
                "bottom-left": (10, img.size[1] - watermark.size[1] - 10),
                "bottom-right": (img.size[0] - watermark.size[0] - 10, img.size[1] - watermark.size[1] - 10),
                "center": ((img.size[0] - watermark.size[0]) // 2, (img.size[1] - watermark.size[1]) // 2),
            }
            
            pos = positions.get(position, positions["bottom-right"])
            
            # 添加水印
            if watermark.mode != "RGBA":
                watermark = watermark.convert("RGBA")
            
            img.paste(watermark, pos, watermark)
            img.save(output_file)
            
            logger.info(f"✅ 水印添加完成：{output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 添加水印失败：{e}")
            return False


def main():
    """主函数 - CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("太一图像处理 CLI")
        print()
        print("用法:")
        print("  python3 image_cli.py edit <input> <output> [--resize WxH] [--filter FILTER]")
        print("  python3 image_cli.py convert <input> <output> [--format FORMAT]")
        print("  python3 image_cli.py watermark <input> <watermark> <output> [--pos POSITION]")
        print("  python3 image_cli.py batch <input_dir> <output_dir> [--resize WxH]")
        print()
        print("滤镜选项：blur/sharpen/vintage/enhance")
        print("水印位置：top-left/top-right/bottom-left/bottom-right/center")
        print()
        print("示例:")
        print("  python3 image_cli.py edit photo.jpg edited.jpg --resize 800x600 --filter vintage")
        print("  python3 image_cli.py convert photo.png photo.jpg")
        print("  python3 image_cli.py watermark photo.jpg logo.png watermarked.jpg --pos bottom-right")
        print("  python3 image_cli.py batch ./photos/ ./processed/ --resize 800x600")
        return
    
    processor = ImageProcessor()
    command = sys.argv[1]
    
    if command == "edit" and len(sys.argv) >= 4:
        resize = None
        filter = None
        if "--resize" in sys.argv:
            resize = sys.argv[sys.argv.index("--resize") + 1]
        if "--filter" in sys.argv:
            filter = sys.argv[sys.argv.index("--filter") + 1]
        processor.edit(sys.argv[2], sys.argv[3], resize=resize, filter=filter)
        
    elif command == "convert" and len(sys.argv) >= 4:
        format = None
        if "--format" in sys.argv:
            format = sys.argv[sys.argv.index("--format") + 1]
        processor.convert(sys.argv[2], sys.argv[3], format=format)
        
    elif command == "watermark" and len(sys.argv) >= 5:
        position = "bottom-right"
        if "--pos" in sys.argv:
            position = sys.argv[sys.argv.index("--pos") + 1]
        processor.add_watermark(sys.argv[2], sys.argv[3], sys.argv[4], position=position)
        
    elif command == "batch" and len(sys.argv) >= 4:
        resize = None
        filter = None
        if "--resize" in sys.argv:
            resize = sys.argv[sys.argv.index("--resize") + 1]
        if "--filter" in sys.argv:
            filter = sys.argv[sys.argv.index("--filter") + 1]
        processor.batch_process(sys.argv[2], sys.argv[3], resize=resize, filter=filter)
        
    else:
        print(f"❌ 未知命令或参数不足：{command}")


if __name__ == "__main__":
    main()
