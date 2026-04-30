#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 Markdown 文件添加 Front Matter (微信友好格式)

用法:
    python3 add-frontmatter.py <文件路径> [标题] [标签...]

示例:
    python3 add-frontmatter.py reports/test.md "测试报告" 修复 测试
"""

import sys
from pathlib import Path
from datetime import datetime

def add_frontmatter(file_path: str, title: str = None, tags: list = None):
    """为 Markdown 文件添加 Front Matter"""
    
    path = Path(file_path)
    if not path.exists():
        print(f"❌ 文件不存在：{file_path}")
        return False
    
    # 读取原文件
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有 Front Matter
    if content.strip().startswith('---'):
        print(f"⚠️  文件已有 Front Matter: {file_path}")
        return False
    
    # 生成 Front Matter
    if not title:
        # 从文件名提取标题
        title = path.stem.replace('-', ' ').replace('_', ' ').title()
    
    if not tags:
        tags = ['报告']
    
    frontmatter = f"""---
title: {title}
author: 太一 AGI
date: {datetime.now().strftime('%Y-%m-%d')}
type: report
tags: [{', '.join([f"'{t}'" for t in tags])}]
---

"""
    
    # 写入新内容
    with open(path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    
    print(f"✅ 已添加 Front Matter: {file_path}")
    print(f"   标题：{title}")
    print(f"   标签：{', '.join(tags)}")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    file_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None
    tags = sys.argv[3:] if len(sys.argv) > 3 else None
    
    success = add_frontmatter(file_path, title, tags)
    sys.exit(0 if success else 1)
