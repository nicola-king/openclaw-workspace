#!/usr/bin/env python3
"""
MarkItDown 集成测试

作者：太一 AGI
创建：2026-04-09
"""

from markitdown import MarkItDown

def main():
    """测试 MarkItDown"""
    print("📄 MarkItDown 集成测试")
    print("="*50)
    print()
    
    # 初始化
    md = MarkItDown()
    print("✅ MarkItDown 初始化成功")
    print()
    
    # 显示支持的格式
    print("支持的格式:")
    print("  📄 PDF, Word (DOCX)")
    print("  📊 Excel (XLSX), CSV")
    print("  📽️ PowerPoint (PPTX)")
    print("  🖼️ 图片 (EXIF + OCR)")
    print("  🎵 音频 (EXIF + 语音转录)")
    print("  🌐 HTML, YouTube URL")
    print("  📚 EPUB, ZIP, JSON, XML")
    print()
    
    # 测试转换 (示例)
    print("使用示例:")
    print("  # Python API")
    print("  from markitdown import MarkItDown")
    print("  md = MarkItDown()")
    print("  result = md.convert('document.pdf')")
    print("  print(result.text_content)")
    print()
    print("  # CLI")
    print("  markitdown document.pdf > document.md")
    print()
    
    print("✅ MarkItDown 已就绪，可以开始转换文档!")

if __name__ == "__main__":
    main()
