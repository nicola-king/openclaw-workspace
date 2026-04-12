#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信搜索命令处理器

集成语义搜索到微信通道
"""

import sys
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/semantic-search')

from searcher import SemanticSearcher


def handle_search_command(query: str) -> str:
    """处理搜索命令"""
    searcher = SemanticSearcher()
    
    try:
        # 执行搜索
        results = searcher.search(query)
        
        if not results:
            return f"🔍 未找到与「{query}」相关的内容"
        
        # 生成摘要
        summary = searcher.generate_summary(results, query)
        
        # 格式化结果（微信友好）
        response = format_wechat_results(results, query)
        
        return response
    
    finally:
        searcher.close()


def format_wechat_results(results: list, query: str) -> str:
    """格式化微信搜索结果"""
    lines = [
        f"🔍 搜索「{query}」",
        f"找到 {len(results)} 个相关文件：",
        ""
    ]
    
    # 显示前 5 个结果
    for i, result in enumerate(results[:5], 1):
        title = result.get('title', result.get('name', '未知'))
        relevance = result.get('relevance', 0)
        file_path = result.get('file_path', '')
        
        # 提取文件名
        filename = file_path.split('/')[-1] if file_path else '未知'
        
        lines.append(f"{i}. {title}")
        lines.append(f"   📁 {filename}")
        lines.append(f"   📊 相关性：{relevance:.0%}")
        lines.append("")
    
    # 添加使用说明
    lines.append("💡 使用：回复文件编号查看详细内容")
    lines.append("   例如：回复「1」查看第一个文件")
    
    return '\n'.join(lines)


def handle_file_request(file_index: int, results: list) -> str:
    """处理文件查看请求"""
    if file_index < 1 or file_index > len(results):
        return f"❌ 文件编号无效（1-{len(results)}）"
    
    result = results[file_index - 1]
    file_path = result.get('file_path', '')
    
    if not file_path:
        return "❌ 文件路径不存在"
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 截取前 1000 字
        preview = content[:1000]
        if len(content) > 1000:
            preview += "\n\n...（内容过长，已截取前 1000 字）"
        
        return f"📄 {file_path.split('/')[-1]}\n\n{preview}"
    
    except Exception as e:
        return f"❌ 读取失败：{str(e)}"


# 测试
if __name__ == '__main__':
    # 测试搜索
    response = handle_search_command("hermes 技能")
    print(response)
    print("\n" + "="*60 + "\n")
    
    # 测试文件查看
    searcher = SemanticSearcher()
    results = searcher.search("hermes 技能")
    searcher.close()
    
    if results:
        file_content = handle_file_request(1, results)
        print(file_content)
