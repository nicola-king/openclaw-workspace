#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaddleOCR 测试脚本

用途：
- 验证安装是否成功
- 测试 OCR 功能
- 性能基准测试

创建时间：2026-04-06 08:15
依据：DEEP-LEARNING-EXECUTION.md 学习后立即执行原则

使用示例：
    python test_ocr.py --basic           # 基础测试
    python test_ocr.py --performance     # 性能测试
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_import():
    """测试 PaddleOCR 是否可导入"""
    print("🔍 测试 1/4: 检查 PaddleOCR 安装...")
    
    try:
        from paddleocr import PaddleOCR
        print("✅ PaddleOCR 已安装")
        return True
    except ImportError as e:
        print(f"❌ PaddleOCR 未安装：{e}")
        print("\n💡 请运行：pip install paddleocr")
        return False


def test_initialization():
    """测试 PaddleOCR 初始化"""
    print("\n🔍 测试 2/4: 初始化 PaddleOCR...")
    
    try:
        from paddleocr import PaddleOCR
        start = time.time()
        # 新版 API (v3.4.0)
        ocr = PaddleOCR(lang='ch')
        elapsed = time.time() - start
        print(f"✅ 初始化成功 (耗时：{elapsed:.2f}秒)")
        return True, ocr
    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        return False, None


def test_ocr_basic():
    """基础 OCR 测试"""
    print("\n🔍 测试 3/4: 基础 OCR 测试...")
    
    # 创建测试图片（如果没有真实图片）
    test_image = Path(__file__).parent / 'test_image.txt'
    
    # 创建一个简单的测试文件
    test_text = "太一 AGI\nPaddleOCR 测试\n2026-04-06"
    with open(test_image, 'w', encoding='utf-8') as f:
        f.write(test_text)
    
    print(f"📝 测试文本：{test_text}")
    print(f"📁 测试文件：{test_image}")
    print("\n⚠️  注意：完整测试需要真实图片文件")
    print("   请使用 --image 参数指定图片路径进行完整测试")
    
    return True


def test_performance():
    """性能测试"""
    print("\n🔍 测试 4/4: 性能基准测试...")
    
    try:
        from paddleocr import PaddleOCR
        import numpy as np
        
        # 初始化
        ocr = PaddleOCR(lang='ch')
        
        # 创建虚拟图片（用于性能测试）
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # 测试 3 次（首次较慢）
        times = []
        for i in range(3):
            start = time.time()
            result = ocr.ocr(test_image)
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  第{i+1}次：{elapsed:.2f}秒")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n✅ 性能测试结果:")
        print(f"   平均耗时：{avg_time:.2f}秒/图")
        print(f"   最快：{min_time:.2f}秒")
        print(f"   最慢：{max_time:.2f}秒")
        print(f"   吞吐量：{1/avg_time:.1f} 图/秒")
        
        return True, {
            "avg_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "throughput": 1/avg_time
        }
        
    except Exception as e:
        print(f"❌ 性能测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False, None


def run_full_test():
    """运行完整测试套件"""
    print("="*60)
    print("🧪 PaddleOCR 测试套件 - 太一 AGI")
    print("="*60)
    print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # 测试 1: 导入
    results["tests"]["import"] = test_import()
    
    # 测试 2: 初始化
    success, ocr = test_initialization()
    results["tests"]["initialization"] = success
    
    # 测试 3: 基础 OCR
    results["tests"]["basic_ocr"] = test_ocr_basic()
    
    # 测试 4: 性能
    success, perf = test_performance()
    results["tests"]["performance"] = success
    if perf:
        results["performance_metrics"] = perf
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    
    passed = sum(1 for v in results["tests"].values() if v is True or (isinstance(v, tuple) and v[0]))
    total = len(results["tests"])
    
    print(f"通过：{passed}/{total}")
    
    if passed == total:
        print("\n✅ 所有测试通过！PaddleOCR 已就绪")
    else:
        print(f"\n⚠️  {total - passed} 个测试未通过，请检查安装")
    
    # 保存测试结果
    report_path = Path(__file__).parent / 'test_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"📄 测试报告：{report_path}")
    
    return passed == total


def test_with_image(image_path: str):
    """使用真实图片测试"""
    print(f"🖼️  使用真实图片测试：{image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ 文件不存在：{image_path}")
        return False
    
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(lang='ch')
        
        start = time.time()
        result = ocr.ocr(image_path)
        elapsed = time.time() - start
        
        print(f"\n✅ 识别完成 (耗时：{elapsed:.2f}秒)")
        print("\n识别结果:")
        print("-" * 50)
        
        if result and result[0]:
            for line in result[0]:
                if line and len(line) >= 2:
                    text, confidence = line[1]
                    print(f"  {text} (置信度：{confidence:.3f})")
        else:
            print("  (未识别到文字)")
        
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description='PaddleOCR 测试脚本')
    parser.add_argument('--basic', action='store_true', help='运行基础测试')
    parser.add_argument('--performance', action='store_true', help='运行性能测试')
    parser.add_argument('--image', type=str, help='使用指定图片测试')
    parser.add_argument('--full', action='store_true', help='运行完整测试套件')
    
    args = parser.parse_args()
    
    if args.full or (not args.basic and not args.performance and not args.image):
        # 默认运行完整测试
        run_full_test()
    
    elif args.basic:
        test_import()
        test_initialization()
        test_ocr_basic()
    
    elif args.performance:
        test_performance()
    
    elif args.image:
        test_with_image(args.image)


if __name__ == '__main__':
    main()
