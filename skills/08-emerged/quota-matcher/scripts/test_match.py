#!/usr/bin/env python3
"""
测试定额匹配引擎
"""

import sys
import os
import json

# 添加父目录到路径



sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matcher import QuotaMatcher

def main():
    if len(sys.argv) < 2:
        print("用法: python3 test_match.py <查询内容>")
        print("示例:")
        print("  python3 test_match.py DA0001")
        print("  python3 test_match.py 混凝土")
        print("  python3 test_match.py 安全文明施工费怎么算？")
        sys.exit(1)
    
    query = sys.argv[1]
    
    print(f"🔍 查询: {query}")
    print("=" * 60)
    
    matcher = QuotaMatcher()
    result = matcher.query(query)
    
    print(f"查询类型: {result['type']}")
    print()
    
    # 显示结果
    if result['type'] == 'quota_code':
        data = result['data']
        if data.get('quota'):
            q = data['quota']['data']
            print(f"📐 定额: {q.get('deh')} - {q.get('xmmc')}")
            print(f"   单位: {q.get('dw')} | 单价: {q.get('dj')}元")
            print(f"   章节: {q.get('chapter')}")
        
        if data.get('qa_matches'):
            print(f"\n📖 相关解释 ({len(data['qa_matches'])} 条):")
            for qa in data['qa_matches'][:3]:
                print(f"   Q: {qa['question'][:50]}...")
                print(f"   A: {qa['answer'][:50]}...")
        
        if data.get('doc_matches'):
            print(f"\n📜 相关文件 ({len(data['doc_matches'])} 份):")
            for doc in data['doc_matches'][:3]:
                print(f"   {doc['filename']}")
    
    elif result['type'] == 'keyword':
        data = result['data']
        if data.get('quota_matches'):
            print(f"📐 定额匹配 ({len(data['quota_matches'])} 条):")
            for m in data['quota_matches'][:5]:
                q = m['data']
                print(f"   {q.get('deh')} | {q.get('xmmc')[:30]} | {q.get('dw')} | {q.get('dj')}元 | 得分:{m['score']}")
        
        if data.get('qa_matches'):
            print(f"\n📖 Q&A 匹配 ({len(data['qa_matches'])} 条):")
            for m in data['qa_matches'][:3]:
                qa = m['data']
                print(f"   Q: {qa['question'][:50]}...")
                print(f"   A: {qa['answer'][:50]}...")
                print(f"   来源: {qa['source_file']}")
        
        if data.get('doc_matches'):
            print(f"\n📜 文档匹配 ({len(data['doc_matches'])} 份):")
            for m in data['doc_matches'][:3]:
                doc = m['data']
                print(f"   {doc['filename']} | 分类: {doc['category']} | 得分:{m['score']}")
    
    elif result['type'] == 'question':
        data = result['data']
        if data.get('qa_answer'):
            qa = data['qa_answer']
            print(f"📖 问题: {qa['question']}")
            print(f"📖 答案: {qa['answer']}")
            print(f"📖 来源: {qa['source_file']}")
        
        if data.get('related_quota'):
            print(f"\n📐 相关定额 ({len(data['related_quota'])} 条):")
            for q in data['related_quota'][:3]:
                print(f"   {q['data'].get('deh')} - {q['data'].get('xmmc')}")
        
        if data.get('related_docs'):
            print(f"\n📜 相关文件 ({len(data['related_docs'])} 份):")
            for doc in data['related_docs'][:3]:
                print(f"   {doc['filename']}")
    
    elif result['type'] == 'doc_number':
        data = result['data']
        if data.get('documents'):
            print(f"📜 找到 {len(data['documents'])} 份文件:")
            for doc in data['documents']:
                print(f"   {doc['filename']}")
                print(f"   分类: {doc['category']}")
                print(f"   文号: {', '.join(doc.get('doc_numbers', []))}")
    
    print("\n" + "=" * 60)
    print("✅ 查询完成")

if __name__ == '__main__':
    main()


---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 17:41