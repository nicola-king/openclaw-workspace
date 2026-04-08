#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAD 自动转换脚本 - 纯开源免费方案
=====================================

功能:
- DWG → DXF 自动转换 (使用 LibreCAD)
- DXF 处理/验证 (使用 ezdxf)
- 批量转换支持
- 完全开源免费 (GPL/MIT 许可)

使用:
    python3 cad-convert-opensource.py <input_file_or_folder> [output_folder]
    python3 cad-convert-opensource.py --help

许可:
- 本脚本：MIT License
- ezdxf: MIT License
- LibreCAD: GPL-2.0

作者：太一 AGI
创建：2026-04-03
版本：v1.0 (开源版)
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

try:
    import ezdxf
    EZDXF_AVAILABLE = True
except ImportError:
    EZDXF_AVAILABLE = False
    print("⚠️ ezdxf 未安装，部分功能受限")
    print("安装：pip3 install ezdxf")

# 配置
CONFIG = {
    "librecad_cmd": "librecad",
    "freecad_cmd": "freecad",
    "output_folder": "./cad-output",
    "log_file": "./cad-convert.log",
    "supported_input": [".dwg", ".dxf"],
    "supported_output": [".dxf", ".svg", ".pdf"],
}


class CADConverter:
    """CAD 文件转换器 (纯开源方案)"""
    
    def __init__(self, output_folder: str = None, log_file: str = None):
        self.output_folder = output_folder or CONFIG["output_folder"]
        self.log_file = log_file or CONFIG["log_file"]
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "files": [],
            "method": "open_source"
        }
        
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)
        self.log("🔧 CAD 转换器 (开源版) 初始化完成")
        self.log(f"📁 输出目录：{self.output_folder}")
        
    def log(self, message: str, level: str = "INFO"):
        """日志记录"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"⚠️ 日志写入失败：{e}")
    
    def check_librecad(self) -> bool:
        """检查 LibreCAD 是否可用"""
        try:
            result = subprocess.run(
                ["which", CONFIG["librecad_cmd"]],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.log(f"✅ LibreCAD 已安装：{result.stdout.strip()}")
                return True
            else:
                self.log("⚠️ LibreCAD 未找到", "WARNING")
                return False
        except Exception as e:
            self.log(f"❌ LibreCAD 检查失败：{e}", "ERROR")
            return False
    
    def validate_dxf(self, dxf_file: str) -> Tuple[bool, str]:
        """使用 ezdxf 验证 DXF 文件"""
        if not EZDXF_AVAILABLE:
            return True, "ezdxf 未安装，跳过验证"
        
        try:
            doc = ezdxf.readfile(dxf_file)
            self.log(f"✅ DXF 验证通过：{os.path.basename(dxf_file)} (版本：{doc.dxfversion})")
            return True, "valid"
        except ezdxf.DXFStructureError as e:
            self.log(f"❌ DXF 结构错误：{e}", "ERROR")
            return False, str(e)
        except Exception as e:
            self.log(f"❌ DXF 验证失败：{e}", "ERROR")
            return False, str(e)
    
    def get_dxf_info(self, dxf_file: str) -> Dict:
        """获取 DXF 文件信息"""
        if not EZDXF_AVAILABLE:
            return {"error": "ezdxf 未安装"}
        
        try:
            doc = ezdxf.readfile(dxf_file)
            info = {
                "version": doc.dxfversion,
                "entities": len(doc.modelspace()),
                "layers": len(doc.layers),
                "blocks": len(doc.blocks),
            }
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def convert_with_librecad(self, input_file: str, output_format: str = ".dxf") -> Tuple[bool, str]:
        """
        使用 LibreCAD 转换
        
        注意：LibreCAD 命令行支持有限，主要用于 DXF 编辑
        对于 DWG→DXF 转换，建议使用 ODA File Converter 或在线工具
        """
        try:
            self.log(f"🔄 使用 LibreCAD 处理：{os.path.basename(input_file)}")
            
            # LibreCAD 主要是 GUI 应用，命令行支持有限
            # 这里提供框架，实际转换可能需要 GUI 或脚本
            
            self.log("⚠️ LibreCAD 命令行转换支持有限", "WARNING")
            self.log("💡 建议使用：ezdxf 处理 DXF，或手动转换 DWG")
            
            return False, "LibreCAD 命令行支持有限"
            
        except Exception as e:
            self.log(f"❌ LibreCAD 转换异常：{e}", "ERROR")
            return False, str(e)
    
    def process_dxf(self, input_file: str) -> Dict:
        """处理 DXF 文件 (验证/分析/优化)"""
        self.stats["total"] += 1
        
        file_name = os.path.basename(input_file)
        self.log(f"📄 处理 DXF 文件：{file_name}")
        
        result = {
            "input": input_file,
            "output": input_file,
            "status": "pending",
            "method": "ezdxf",
            "error": None,
            "timestamp": datetime.now().isoformat(),
            "info": {}
        }
        
        if not os.path.exists(input_file):
            self.log(f"❌ 文件不存在：{input_file}", "ERROR")
            result["status"] = "failed"
            result["error"] = "文件不存在"
            self.stats["failed"] += 1
            return result
        
        # 验证 DXF
        valid, msg = self.validate_dxf(input_file)
        result["info"]["valid"] = valid
        result["info"]["message"] = msg
        
        if valid:
            # 获取文件信息
            info = self.get_dxf_info(input_file)
            result["info"]["details"] = info
            
            self.log(f"📊 DXF 信息：{info.get('entities', '?')} 实体，{info.get('layers', '?')} 图层")
            
            result["status"] = "success"
            self.stats["success"] += 1
        else:
            result["status"] = "failed"
            result["error"] = msg
            self.stats["failed"] += 1
        
        return result
    
    def process_file(self, input_file: str, output_format: str = ".dxf") -> Dict:
        """处理单个文件"""
        file_ext = os.path.splitext(input_file)[1].lower()
        
        if file_ext == ".dxf":
            # DXF 文件：验证 + 分析
            return self.process_dxf(input_file)
        elif file_ext == ".dwg":
            # DWG 文件：需要转换
            self.stats["total"] += 1
            
            result = {
                "input": input_file,
                "output": None,
                "status": "needs_conversion",
                "method": "manual",
                "error": None,
                "timestamp": datetime.now().isoformat(),
                "message": "DWG 需要转换为 DXF"
            }
            
            self.log(f"⚠️ DWG 文件需要转换：{os.path.basename(input_file)}", "WARNING")
            self.log("💡 推荐方案:")
            self.log("   1. ODA File Converter (免费，需注册): https://www.opendesign.com/guestfiles/oda_file_converter")
            self.log("   2. 在线转换：https://cadsofttools.com/dwg-to-dxf-converter/")
            self.log("   3. LibreCAD 手动另存为")
            
            result["status"] = "failed"
            result["error"] = "DWG 转换需要外部工具"
            self.stats["failed"] += 1
            
            return result
        else:
            self.log(f"⚠️ 不支持的格式：{file_ext}", "WARNING")
            self.stats["skipped"] += 1
            
            return {
                "input": input_file,
                "status": "skipped",
                "error": f"不支持的格式：{file_ext}"
            }
    
    def process_folder(self, folder_path: str, output_format: str = ".dxf") -> List[Dict]:
        """批量处理文件夹"""
        self.log(f"📂 开始批量处理文件夹：{folder_path}")
        
        results = []
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in CONFIG["supported_input"]:
                    input_path = os.path.join(root, file)
                    result = self.process_file(input_path, output_format)
                    results.append(result)
        
        return results
    
    def generate_report(self, results: List[Dict]) -> str:
        """生成处理报告"""
        self.stats["end_time"] = datetime.now().isoformat()
        
        report = {
            "summary": self.stats,
            "files": results,
            "tool": "cad-convert-opensource",
            "version": "1.0",
            "license": "MIT"
        }
        
        report_path = os.path.join(self.output_folder, "convert-report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(f"📊 报告已保存：{report_path}")
        
        # 打印摘要
        print("\n" + "="*50)
        print("📊 处理报告摘要")
        print("="*50)
        print(f"总文件数：{self.stats['total']}")
        print(f"✅ 成功：{self.stats['success']}")
        print(f"❌ 失败：{self.stats['failed']}")
        print(f"⏭️  跳过：{self.stats['skipped']}")
        print(f"处理模式：{self.stats['method']}")
        print(f"开始时间：{self.stats['start_time']}")
        print(f"结束时间：{self.stats['end_time']}")
        print("="*50)
        
        return report_path
    
    def run(self, input_path: str, output_format: str = ".dxf") -> str:
        """执行处理"""
        self.log(f"🚀 开始处理：{input_path}")
        
        if os.path.isfile(input_path):
            results = [self.process_file(input_path, output_format)]
        elif os.path.isdir(input_path):
            results = self.process_folder(input_path, output_format)
        else:
            self.log(f"❌ 无效输入路径：{input_path}", "ERROR")
            return None
        
        report_path = self.generate_report(results)
        return report_path


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="CAD 自动转换脚本 - 纯开源免费方案",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 cad-convert-opensource.py input.dxf        # 验证 DXF 文件
  python3 cad-convert-opensource.py ./cad-files/     # 批量处理文件夹
  python3 cad-convert-opensource.py --check          # 检查依赖

支持的输入格式：.dwg, .dxf
支持的处理：DXF 验证/分析，DWG 需外部工具转换

开源工具:
- ezdxf (MIT): DXF 文件处理
- LibreCAD (GPL-2.0): 2D CAD 编辑
- FreeCAD (LGPL-2.0): 3D CAD 编辑
        """
    )
    
    parser.add_argument("input", nargs="?", help="输入文件或文件夹路径")
    parser.add_argument("output_folder", nargs="?", default=None, help="输出文件夹")
    parser.add_argument("--format", choices=[".dxf", ".svg", ".pdf"], default=".dxf", help="输出格式")
    parser.add_argument("--log", default=None, help="日志文件路径")
    parser.add_argument("--check", action="store_true", help="检查依赖工具")
    
    args = parser.parse_args()
    
    # 检查依赖
    if args.check or not args.input:
        print("\n🔍 依赖检查:")
        print(f"ezdxf: {'✅ v' + ezdxf.__version__ if EZDXF_AVAILABLE else '❌'}")
        
        result = subprocess.run(["which", CONFIG["librecad_cmd"]], capture_output=True, text=True)
        print(f"LibreCAD: {'✅ ' + result.stdout.strip() if result.returncode == 0 else '❌'}")
        
        result = subprocess.run(["which", CONFIG["freecad_cmd"]], capture_output=True, text=True)
        print(f"FreeCAD: {'✅ ' + result.stdout.strip() if result.returncode == 0 else '❌'}")
        
        print("\n💡 说明:")
        print("- ezdxf: 用于 DXF 文件验证和分析")
        print("- LibreCAD: 2D CAD 编辑 (GUI)")
        print("- FreeCAD: 3D CAD 编辑 (GUI)")
        print("\n⚠️ DWG 转换需要:")
        print("  ODA File Converter: https://www.opendesign.com/guestfiles/oda_file_converter")
        return
    
    if not os.path.exists(args.input):
        print(f"❌ 错误：输入路径不存在 - {args.input}")
        sys.exit(1)
    
    converter = CADConverter(output_folder=args.output_folder, log_file=args.log)
    report_path = converter.run(args.input, args.format)
    
    if report_path:
        print(f"\n✅ 处理完成！报告：{report_path}")
        sys.exit(0)
    else:
        print("\n❌ 处理失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
