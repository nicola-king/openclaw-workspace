#!/usr/bin/env python3
"""
The Well 样本下载脚本 (带 1GB 限制)

功能:
- 下载样本数据
- 大小限制检查 (>1GB 停止)
- 进度显示
- 断点续传支持
"""

import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm

# 配置
MAX_SIZE_GB = 1.0
MAX_SIZE_BYTES = MAX_SIZE_GB * 1024 * 1024 * 1024
OUTPUT_DIR = Path("/tmp/the-well-samples")
BASE_URL = "https://polymathic-ai.org/the_well/datasets"

# 样本数据集列表 (小样本)
SAMPLE_DATASETS = [
    {"name": "darcy_flow_sample.h5", "size_mb": 100},
    {"name": "navier_stokes_sample.h5", "size_mb": 150},
    {"name": "supernova_sample.h5", "size_mb": 200},
    {"name": "aerofoil_sample.h5", "size_mb": 80},
    {"name": "bioheat_sample.h5", "size_mb": 120},
]


def check_disk_space():
    """检查磁盘空间"""
    stat = os.statvfs(OUTPUT_DIR.parent)
    free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    print(f"可用磁盘空间：{free_gb:.2f} GB")
    return free_gb


def download_file(url, output_path, max_size_bytes):
    """下载文件 (带大小限制)"""
    
    # 创建目录
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 发送请求 (流式)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    # 检查是否超过限制
    if total_size > max_size_bytes:
        print(f"⚠️  文件过大：{total_size / (1024**3):.2f} GB > {MAX_SIZE_GB} GB")
        print("跳过下载")
        return False
    
    # 下载
    downloaded = 0
    with open(output_path, 'wb') as f:
        with tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc=output_path.name
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    pbar.update(len(chunk))
                    
                    # 实时检查大小
                    if downloaded > max_size_bytes:
                        print(f"\n⚠️  下载超过限制，停止下载")
                        f.truncate()  # 截断文件
                        output_path.unlink()  # 删除文件
                        return False
    
    print(f"✅ 下载完成：{output_path.name} ({downloaded / (1024**2):.2f} MB)")
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("The Well 样本下载 (限制 1GB)")
    print("=" * 60)
    
    # 检查磁盘空间
    if not check_disk_space():
        print("❌ 磁盘空间不足")
        sys.exit(1)
    
    # 下载样本
    total_downloaded = 0
    for dataset in SAMPLE_DATASETS:
        url = f"{BASE_URL}/{dataset['name']}"
        output_path = OUTPUT_DIR / dataset['name']
        
        # 检查是否已下载
        if output_path.exists():
            print(f"⏭️  已存在：{dataset['name']}")
            continue
        
        print(f"\n开始下载：{dataset['name']}")
        
        # 下载
        success = download_file(url, output_path, MAX_SIZE_BYTES - total_downloaded)
        
        if success:
            total_downloaded += output_path.stat().st_size
            print(f"累计下载：{total_downloaded / (1024**2):.2f} MB / {MAX_SIZE_GB * 1024:.0f} MB")
        else:
            print(f"⚠️  跳过：{dataset['name']}")
        
        # 检查总大小
        if total_downloaded >= MAX_SIZE_BYTES:
            print(f"\n⚠️  已达到总大小限制 ({MAX_SIZE_GB} GB)")
            break
    
    # 总结
    print("\n" + "=" * 60)
    print("下载完成")
    print(f"总下载量：{total_downloaded / (1024**2):.2f} MB")
    print(f"文件数量：{len(list(OUTPUT_DIR.glob('*.h5')))}")
    print("=" * 60)


if __name__ == "__main__":
    main()
