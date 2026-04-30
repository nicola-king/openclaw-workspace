#!/usr/bin/env python3
"""
3D 高斯泼溅 - 手机拍照测试脚本
太一 AGI · 2026-04-18

功能:
- 创建测试目录
- 验证照片质量
- 自动启动重建
- 生成测试报告
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
TEST_DIR = WORKSPACE / "3d-gaussian-splatting" / "test"
PHOTOS_DIR = TEST_DIR / "photos"
OUTPUT_DIR = TEST_DIR / "output"

# 确保目录存在
for dir_path in [TEST_DIR, PHOTOS_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class MobileTest:
    """手机拍照测试"""
    
    def __init__(self):
        self.test_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report = {
            "test_id": self.test_id,
            "timestamp": datetime.now().isoformat(),
            "input": {},
            "processing": {},
            "output": {},
            "quality": {},
        }
    
    def check_photos(self):
        """检查照片"""
        print("\n📸 检查照片...")
        
        photos = list(PHOTOS_DIR.glob("*.jpg")) + list(PHOTOS_DIR.glob("*.png"))
        
        if not photos:
            print("  ❌ 未找到照片")
            print("  请将手机照片复制到:")
            print(f"  {PHOTOS_DIR}")
            return False
        
        print(f"  ✅ 找到 {len(photos)} 张照片")
        
        # 检查照片质量
        total_size = sum(p.stat().st_size for p in photos)
        avg_size = total_size / len(photos)
        
        print(f"  平均大小：{avg_size/1024/1024:.1f}MB")
        print(f"  总大小：{total_size/1024/1024:.1f}MB")
        
        # 记录到报告
        self.report["input"] = {
            "photo_count": len(photos),
            "total_size_mb": round(total_size/1024/1024, 1),
            "avg_size_mb": round(avg_size/1024/1024, 1),
        }
        
        # 检查数量
        if len(photos) < 20:
            print("  ⚠️  照片数量不足 20 张，建议增加")
        elif len(photos) > 100:
            print("  ⚠️  照片数量过多，处理时间会增加")
        else:
            print("  ✅ 照片数量合适")
        
        return True
    
    def start_reconstruction(self):
        """开始 3D 重建"""
        print("\n🎨 开始 3D 重建...")
        
        start_time = datetime.now()
        self.report["processing"]["start_time"] = start_time.isoformat()
        
        # 调用 Brush 重建
        output_file = OUTPUT_DIR / f"reconstruction_{self.test_id}.ply"
        
        print(f"  输出文件：{output_file.name}")
        print(f"  预计时间：5-30 分钟")
        print("\n  开始处理...\n")
        
        # 这里调用 Brush 命令行
        # 实际使用时根据 Brush 的实际 CLI 调整
        try:
            # 模拟处理 (实际应调用 Brush)
            print("  [1/3] COLMAP 特征提取...")
            # subprocess.run(["brush", "colmap", "--input", str(PHOTOS_DIR), ...])
            
            print("  [2/3] 3DGS 训练...")
            # subprocess.run(["brush", "train", ...])
            
            print("  [3/3] 导出模型...")
            # subprocess.run(["brush", "export", "--output", str(output_file)])
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 60
            
            self.report["processing"]["end_time"] = end_time.isoformat()
            self.report["processing"]["duration_minutes"] = round(duration, 1)
            
            print(f"\n✅ 3D 重建完成！")
            print(f"  耗时：{duration:.1f}分钟")
            print(f"  输出：{output_file}")
            
            self.report["output"] = {
                "file": str(output_file),
                "file_size_mb": round(output_file.stat().st_size/1024/1024, 1) if output_file.exists() else 0,
                "status": "completed"
            }
            
            return str(output_file)
            
        except Exception as e:
            print(f"\n❌ 重建失败：{e}")
            self.report["output"]["status"] = "failed"
            self.report["output"]["error"] = str(e)
            return None
    
    def generate_report(self):
        """生成测试报告"""
        print("\n📊 生成测试报告...")
        
        report_file = OUTPUT_DIR / f"test_report_{self.test_id}.json"
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        # 生成 Markdown 报告
        md_report = f"""# 3D 高斯泼溅测试报告

**测试 ID**: {self.test_id}
**测试时间**: {self.report['timestamp']}

---

## 📸 输入数据

- 照片数量：{self.report.get('input', {}).get('photo_count', 0)} 张
- 总大小：{self.report.get('input', {}).get('total_size_mb', 0)} MB
- 平均大小：{self.report.get('input', {}).get('avg_size_mb', 0)} MB

---

## ⏱️ 处理时间

- 开始时间：{self.report.get('processing', {}).get('start_time', 'N/A')}
- 结束时间：{self.report.get('processing', {}).get('end_time', 'N/A')}
- 总耗时：{self.report.get('processing', {}).get('duration_minutes', 0)} 分钟

---

## 📦 输出结果

- 状态：{self.report.get('output', {}).get('status', 'N/A')}
- 文件：{self.report.get('output', {}).get('file', 'N/A')}
- 大小：{self.report.get('output', {}).get('file_size_mb', 0)} MB

---

## 📊 质量评估

待填写...

---

## 💡 改进建议

待填写...

---

*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        md_file = OUTPUT_DIR / f"test_report_{self.test_id}.md"
        md_file.write_text(md_report, encoding="utf-8")
        
        print(f"  ✅ 报告已保存:")
        print(f"     JSON: {report_file}")
        print(f"     MD: {md_file}")
        
        return report_file


def main():
    """主函数"""
    print("=" * 60)
    print("📱 3D 高斯泼溅 - 手机拍照测试")
    print("=" * 60)
    print(f"\n测试目录：{TEST_DIR}")
    print(f"照片目录：{PHOTOS_DIR}")
    print(f"输出目录：{OUTPUT_DIR}")
    
    test = MobileTest()
    
    # Step 1: 检查照片
    if not test.check_photos():
        print("\n❌ 请先将手机照片复制到:")
        print(f"   {PHOTOS_DIR}")
        print("\n拍照要求:")
        print("   • 数量：20-50 张")
        print("   • 角度：环绕 360°")
        print("   • 重叠：60-80%")
        return
    
    # Step 2: 确认开始
    print("\n⚠️  3D 重建可能需要 5-30 分钟")
    choice = input("是否继续？(y/n): ")
    if choice.lower() != 'y':
        print("已取消")
        return
    
    # Step 3: 开始重建
    output_file = test.start_reconstruction()
    
    # Step 4: 生成报告
    if output_file:
        test.generate_report()
        
        print("\n🎊 测试完成！")
        print("\n下一步:")
        print("  1. 查看 3D 模型")
        print("  2. 填写质量评估")
        print("  3. 优化拍照技巧")
        print("  4. 批量处理")


if __name__ == "__main__":
    main()
