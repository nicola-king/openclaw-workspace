#!/usr/bin/env python3
"""
Taiyi NotebookLM CLI 测试脚本

> 版本：v2.0 | 创建：2026-04-06 12:30
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.nlm import NotebookLMClient

def test_auth():
    """测试认证"""
    print("=" * 50)
    print("🔑 测试认证")
    print("=" * 50)
    
    try:
        client = NotebookLMClient()
        print("✅ 认证成功")
        return client
    except Exception as e:
        print(f"❌ 认证失败：{e}")
        return None

def test_list_notebooks(client):
    """测试列出笔记本"""
    print("\n" + "=" * 50)
    print("📖 测试列出笔记本")
    print("=" * 50)
    
    notebooks = client.list_notebooks()
    print(f"✅ 找到 {len(notebooks)} 个笔记本")
    for nb in notebooks:
        print(f"  - {nb.id}: {nb.title}")

def test_create_notebook(client):
    """测试创建笔记本"""
    print("\n" + "=" * 50)
    print("📝 测试创建笔记本")
    print("=" * 50)
    
    title = f"测试笔记本_{int(os.time())}"
    nb = client.create_notebook(title)
    print(f"✅ 创建成功：{nb.id}")
    return nb.id

def test_sources(client, notebook_id):
    """测试源文件管理"""
    print("\n" + "=" * 50)
    print("📁 测试源文件管理")
    print("=" * 50)
    
    # 列出源文件
    sources = client.list_sources(notebook_id)
    print(f"✅ 找到 {len(sources)} 个源文件")
    
    # 添加 URL 源文件
    source = client.add_source_url(
        notebook_id,
        "https://example.com"
    )
    if source:
        print(f"✅ 添加 URL 成功：{source.id}")

def test_notes(client, notebook_id):
    """测试笔记管理"""
    print("\n" + "=" * 50)
    print("📝 测试笔记管理")
    print("=" * 50)
    
    # 列出笔记
    notes = client.list_notes(notebook_id)
    print(f"✅ 找到 {len(notes)} 个笔记")
    
    # 创建笔记
    note = client.create_note(
        notebook_id,
        "测试笔记",
        "这是测试内容"
    )
    if note:
        print(f"✅ 创建笔记成功：{note.id}")

def test_chat(client, notebook_id):
    """测试对话"""
    print("\n" + "=" * 50)
    print("💬 测试对话")
    print("=" * 50)
    
    response = client.chat(
        notebook_id,
        "请用中文总结这个笔记本的核心内容"
    )
    print(f"✅ AI 回复：{response[:200]}...")

def test_audio(client, notebook_id):
    """测试音频"""
    print("\n" + "=" * 50)
    print("🎧 测试音频概览")
    print("=" * 50)
    
    audio_id = client.generate_audio(
        notebook_id,
        "生成播客风格的音频概览"
    )
    if audio_id:
        print(f"✅ 音频生成中：{audio_id}")
        
        status = client.get_audio_status(notebook_id, audio_id)
        print(f"📊 音频状态：{status}")

def main():
    """主测试函数"""
    print("\n" + "=" * 50)
    print("🧪 Taiyi NotebookLM CLI 测试套件")
    print("=" * 50 + "\n")
    
    # 测试认证
    client = test_auth()
    if not client:
        print("\n❌ 认证失败，终止测试")
        return
    
    # 测试笔记本
    test_list_notebooks(client)
    
    # 可选：创建新笔记本测试
    # notebook_id = test_create_notebook(client)
    
    # 使用现有笔记本测试
    notebooks = client.list_notebooks()
    if not notebooks:
        print("\n❌ 没有笔记本，请先创建")
        return
    
    notebook_id = notebooks[0].id
    print(f"\n使用笔记本：{notebook_id}")
    
    # 测试源文件
    test_sources(client, notebook_id)
    
    # 测试笔记
    test_notes(client, notebook_id)
    
    # 测试对话
    test_chat(client, notebook_id)
    
    # 测试音频
    test_audio(client, notebook_id)
    
    print("\n" + "=" * 50)
    print("✅ 所有测试完成！")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
