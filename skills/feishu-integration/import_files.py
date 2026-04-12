#!/usr/bin/env python3
"""
📥 文件导入工具

导入本地文件到飞书多维表格
支持 Excel/CSV/JSON 格式

作者：太一 AGI
创建：2026-04-12
"""

import sys
import os
from pathlib import Path

# 导入导入器
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/feishu-integration')
from bitable_importer import FeishuBitableImporter


def import_files(file_paths: list):
    """导入文件列表"""
    
    print("="*60)
    print("📥 文件导入工具")
    print("="*60)
    print()
    
    # 初始化导入器
    importer = FeishuBitableImporter()
    
    # 检查配置
    if not importer.app_id or not importer.table_id:
        print("❌ 未配置多维表格")
        print("\n请先运行:")
        print("   python3 /home/nicola/.openclaw/workspace/skills/feishu-integration/create_bitable.py")
        return 1
    
    # 测试连接
    print("1️⃣  测试连接...")
    if not importer.test_connection():
        print("❌ 连接失败")
        return 1
    
    print("✅ 连接成功\n")
    
    # 导入文件
    print("2️⃣  导入文件...\n")
    
    success_count = 0
    error_count = 0
    
    for file_path in file_paths:
        print(f"📄 处理：{file_path}")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"   ❌ 文件不存在")
            error_count += 1
            continue
        
        # 导入
        result = importer.import_file(file_path)
        
        if 'error' in result:
            print(f"   ❌ 导入失败：{result['error']}")
            error_count += 1
        else:
            print(f"   ✅ 导入成功")
            success_count += 1
        
        print()
    
    # 汇总
    print("="*60)
    print(f"📊 导入完成!")
    print(f"   成功：{success_count} 个")
    print(f"   失败：{error_count} 个")
    print("="*60)
    
    return 0 if error_count == 0 else 1


def import_directory(dir_path: str):
    """导入目录下所有支持的文件"""
    
    print(f"📂 扫描目录：{dir_path}\n")
    
    # 支持的扩展名
    extensions = ['.xlsx', '.xls', '.csv', '.json']
    
    # 扫描文件
    files = []
    for ext in extensions:
        files.extend(Path(dir_path).glob(f'*{ext}'))
    
    if not files:
        print(f"⚠️  未找到支持的文件 ({', '.join(extensions)})")
        return 1
    
    print(f"✅ 找到 {len(files)} 个文件\n")
    
    # 导入
    return import_files([str(f) for f in files])


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 import_files.py <文件路径> [文件路径 2] ...")
        print("  python3 import_files.py --dir <目录路径>")
        print()
        print("示例:")
        print("  python3 import_files.py data.xlsx")
        print("  python3 import_files.py file1.csv file2.json")
        print("  python3 import_files.py --dir /path/to/files")
        return 1
    
    # 目录模式
    if sys.argv[1] == '--dir' and len(sys.argv) >= 3:
        return import_directory(sys.argv[2])
    
    # 文件模式
    return import_files(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
