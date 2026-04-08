#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文件发送处理器

生成文件后自动发送内容到微信
"""

from pathlib import Path


def send_file_content(file_path: str, max_chars: int = 2000) -> str:
    """发送文件内容到微信"""
    
    path = Path(file_path)
    
    if not path.exists():
        return f"❌ 文件不存在：{file_path}"
    
    try:
        # 读取文件内容
        content = path.read_text(encoding='utf-8')
        
        # 截取内容（微信消息长度限制）
        if len(content) > max_chars:
            preview = content[:max_chars]
            summary = f"\n\n...（内容过长，已显示前{max_chars}字）\n📁 完整文件：{file_path}"
            return preview + summary
        
        # 添加文件信息
        file_info = f"📄 {path.name}\n📊 {len(content)}字\n📁 {file_path}\n\n"
        
        return file_info + content
    
    except Exception as e:
        return f"❌ 读取失败：{str(e)}"


def send_file_archive(file_path: str) -> str:
    """发送文件归档通知"""
    
    path = Path(file_path)
    
    # 获取文件大小
    size_kb = path.stat().st_size / 1024 if path.exists() else 0
    
    # 生成归档通知
    message = f"""✅ 文件已归档

📄 文件：{path.name}
📊 大小：{size_kb:.1f}KB
📁 路径：{file_path}

💡 查看方式:
1. SSH: cat {file_path}
2. 编辑器：code {file_path}
3. Web: Dashboard 文件浏览器"""
    
    return message


# 测试
if __name__ == '__main__':
    # 测试发送报告内容
    test_file = '/home/nicola/.openclaw/workspace/reports/2026-04-09-p1-complete.md'
    content = send_file_content(test_file)
    print(content)
