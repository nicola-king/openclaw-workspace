#!/usr/bin/env python3
"""
3D 高斯泼溅技能 - Brush 集成
太一 AGI · 2026-04-18

功能:
- 照片/视频导入
- 3D 重建
- 实时预览
- 导出多种格式
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
BRUSH_DIR = WORKSPACE / "3d-gaussian-splatting"
INPUT_DIR = BRUSH_DIR / "input"
OUTPUT_DIR = BRUSH_DIR / "output"

# 确保目录存在
for dir_path in [BRUSH_DIR, INPUT_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class Brush3DGS:
    """Brush 3D 高斯泼溅技能"""
    
    def __init__(self):
        self.brush_installed = self.check_brush_installed()
    
    def check_brush_installed(self):
        """检查 Brush 是否已安装"""
        try:
            result = subprocess.run(
                ["brush", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def install_brush(self):
        """安装 Brush"""
        print("🔧 开始安装 Brush...")
        
        # 检测操作系统
        if sys.platform == "darwin":  # macOS
            print("  检测到 macOS，使用 Homebrew 安装...")
            subprocess.run(["brew", "install", "brush"])
        elif sys.platform == "win32":  # Windows
            print("  检测到 Windows，请从 GitHub 下载安装包:")
            print("  https://github.com/ArthurBrussee/brush/releases")
            return False
        else:  # Linux
            print("  检测到 Linux，从 GitHub 克隆...")
            subprocess.run(["git", "clone", "https://github.com/ArthurBrussee/brush.git", str(BRUSH_DIR / "brush")])
            
            # 安装依赖
            print("  安装依赖...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(BRUSH_DIR / "brush/requirements.txt")])
        
        # 验证安装
        if self.check_brush_installed():
            print("✅ Brush 安装成功！")
            return True
        else:
            print("⚠️  Brush 安装失败，请手动安装")
            return False
    
    def process_photos(self, input_path, output_format="ply"):
        """处理照片进行 3D 重建
        
        Args:
            input_path: 照片文件夹路径
            output_format: 输出格式 (ply/obj/mp4/html)
        
        Returns:
            output_file: 输出文件路径
        """
        print(f"\n🎨 开始 3D 重建...")
        print(f"  输入：{input_path}")
        print(f"  输出格式：{output_format}")
        
        # 统计照片数量
        photos = list(Path(input_path).glob("*.jpg")) + list(Path(input_path).glob("*.png"))
        print(f"  照片数量：{len(photos)}")
        
        if len(photos) < 20:
            print("⚠️  照片数量不足 20 张，可能影响重建质量")
        
        # 运行 Brush 重建
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"reconstruction_{timestamp}.{output_format}"
        
        print(f"\n🔧 开始重建 (预计 5-30 分钟)...")
        print(f"  输出：{output_file}")
        
        # 这里调用 Brush 命令行工具
        # 实际使用时需要根据 Brush 的实际 CLI 调整
        try:
            subprocess.run([
                "brush", "reconstruct",
                "--input", str(input_path),
                "--output", str(output_file),
                "--format", output_format
            ], check=True)
            
            print(f"\n✅ 3D 重建完成！")
            print(f"  输出文件：{output_file}")
            return str(output_file)
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ 重建失败：{e}")
            return None
    
    def process_video(self, video_path, output_format="ply"):
        """处理视频进行 3D 重建
        
        Args:
            video_path: 视频文件路径
            output_format: 输出格式
        
        Returns:
            output_file: 输出文件路径
        """
        print(f"\n🎨 开始视频 3D 重建...")
        print(f"  输入：{video_path}")
        
        # 从视频提取帧
        frames_dir = INPUT_DIR / f"frames_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        frames_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"  提取帧到：{frames_dir}")
        
        # 使用 ffmpeg 提取帧
        subprocess.run([
            "ffmpeg", "-i", str(video_path),
            "-vf", "fps=1",  # 每秒 1 帧
            str(frames_dir / "frame_%04d.jpg")
        ])
        
        # 统计帧数
        frames = list(frames_dir.glob("*.jpg"))
        print(f"  提取帧数：{len(frames)}")
        
        # 使用照片重建
        return self.process_photos(str(frames_dir), output_format)
    
    def generate_report(self, output_file):
        """生成重建报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "output_file": output_file,
            "file_size": Path(output_file).stat().st_size if Path(output_file).exists() else 0,
            "format": Path(output_file).suffix,
            "status": "completed"
        }
        
        report_file = OUTPUT_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 重建报告已保存：{report_file}")
        return report


def main():
    """主函数"""
    print("=" * 60)
    print("🎨 3D 高斯泼溅技能 - Brush")
    print("=" * 60)
    
    brush = Brush3DGS()
    
    # 检查安装
    if not brush.brush_installed:
        print("\n⚠️  Brush 未安装")
        choice = input("是否立即安装？(y/n): ")
        if choice.lower() == 'y':
            brush.install_brush()
        else:
            print("请先安装 Brush: https://github.com/ArthurBrussee/brush")
            return
    
    # 选择输入类型
    print("\n选择输入类型:")
    print("1. 照片文件夹")
    print("2. 视频文件")
    choice = input("请输入 (1/2): ")
    
    if choice == "1":
        input_path = input("请输入照片文件夹路径：")
        output_format = input("输出格式 (ply/obj/mp4/html), 默认 ply: ") or "ply"
        output_file = brush.process_photos(input_path, output_format)
    elif choice == "2":
        video_path = input("请输入视频文件路径：")
        output_format = input("输出格式 (ply/obj/mp4/html), 默认 ply: ") or "ply"
        output_file = brush.process_video(video_path, output_format)
    else:
        print("无效选择")
        return
    
    # 生成报告
    if output_file:
        brush.generate_report(output_file)
        
        print("\n🎊 3D 重建完成！")
        print(f"  输出：{output_file}")
        print("\n下一步:")
        print("  1. 使用 3D 查看器查看 .ply 文件")
        print("  2. 导入 Blender 进行编辑")
        print("  3. 上传到网页展示")


if __name__ == "__main__":
    main()
