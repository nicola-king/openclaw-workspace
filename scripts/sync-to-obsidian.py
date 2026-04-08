#!/usr/bin/env python3
"""
太一记忆 → Obsidian 自动同步
每日 23:00 运行，同步 memory 文件到 Obsidian Vault

用法：
    python3 sync-to-obsidian.py
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
OBSIDIAN_VAULT = Path("/home/nicola/ObsidianVault/TaiyiMemory")

# 同步规则
SYNC_RULES = [
    # (源路径，目标路径，类型)
    ("memory", "Daily", "dir"),
    ("MEMORY.md", "Core/MEMORY.md", "file"),
    ("memory/core.md", "Core/core.md", "file"),
    ("memory/residual.md", "Core/residual.md", "file"),
]


def sync_file(src, dst):
    """同步单个文件"""
    if not src.exists():
        print(f"⚠️  源文件不存在：{src}")
        return False
    
    # 检查是否是软链接（避免 SameFileError）
    if src.resolve() == dst.resolve():
        print(f"⏭️  已是软链接：{src.name}")
        return True
    
    # 确保目标目录存在
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    # 复制文件
    shutil.copy2(src, dst)
    print(f"✅ {src.name} → {dst.relative_to(OBSIDIAN_VAULT)}")
    return True


def sync_directory(src_dir, dst_dir):
    """同步整个目录"""
    if not src_dir.exists():
        print(f"⚠️  源目录不存在：{src_dir}")
        return False
    
    # 确保目标目录存在
    dst_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制所有 .md 文件
    count = 0
    for md_file in src_dir.glob("*.md"):
        target = dst_dir / md_file.name
        shutil.copy2(md_file, target)
        count += 1
    
    print(f"✅ {src_dir.name} → {dst_dir.relative_to(OBSIDIAN_VAULT)} ({count} 文件)")
    return count > 0


def main():
    print("=" * 60)
    print("太一记忆 → Obsidian 同步")
    print("=" * 60)
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"目标：{OBSIDIAN_VAULT}")
    print("=" * 60)
    print()
    
    success = 0
    total = len(SYNC_RULES)
    
    for src_rel, dst_rel, sync_type in SYNC_RULES:
        src = WORKSPACE / src_rel
        dst = OBSIDIAN_VAULT / dst_rel
        
        if sync_type == "file":
            if sync_file(src, dst):
                success += 1
        elif sync_type == "dir":
            if sync_directory(src, dst):
                success += 1
    
    print()
    print("=" * 60)
    print(f"同步完成：{success}/{total}")
    print("=" * 60)


if __name__ == "__main__":
    main()
