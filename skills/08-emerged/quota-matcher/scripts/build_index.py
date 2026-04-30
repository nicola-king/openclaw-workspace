#!/usr/bin/env python3
"""
构建定额匹配索引
"""

import sys
import os

# 添加父目录到路径



sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matcher import QuotaMatcher

def main():
    print("🔨 构建定额匹配索引...")
    
    matcher = QuotaMatcher()
    matcher.load_all()
    
    print(f"✅ 定额数据: {sum(len(v) for v in matcher.quota_data.values())} 条")
    print(f"✅ Q&A 对: {len(matcher.qa_pairs)} 条")
    print(f"✅ 政府文件: {len(matcher.gov_docs)} 份")
    
    print("\n📊 索引统计:")
    for skill_name, records in matcher.quota_data.items():
        print(f"  {skill_name}: {len(records)} 条")
    
    print("\n✅ 索引构建完成！")

if __name__ == '__main__':
    main()


---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 17:41