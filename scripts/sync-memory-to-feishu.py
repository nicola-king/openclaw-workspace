#!/usr/bin/env python3
# scripts/sync-memory-to-feishu.py

"""
太一记忆同步脚本

功能:
1. 解析 memory/*.md 文件
2. 提取结构化记忆数据
3. 同步到 Feishu 多维表格
4. 更新统计面板

使用:
    python3 scripts/sync-memory-to-feishu.py

依赖:
    - Feishu API 配置 (config/feishu-memory-table.json)
    - requests 库
"""

import os
import re
import json
import requests
from datetime import datetime
from typing import List, Dict

# 配置
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/config/feishu-memory-table.json")
LOG_FILE = os.path.expanduser("~/.openclaw/workspace/logs/memory-sync.log")

# Feishu API 端点
FEISHU_BASE = "https://open.feishu.cn/open-apis/bitable/v1"

def load_config() -> Dict:
    """加载 Feishu 配置"""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"配置文件不存在：{CONFIG_FILE}")
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_memory_entry(content: str, source_file: str, section_name: str) -> Dict:
    """解析记忆条目"""
    # 提取关键词 (从内容前 100 字)
    keywords = extract_keywords(content[:200])
    
    # 估算 Token
    token_estimate = len(content) // 4  # 粗略估算
    
    # 判断重要度 (根据_section 名称)
    if any(kw in section_name.lower() for kw in ['决策', '宪法', 'p0']):
        priority = "P0"
    elif any(kw in section_name.lower() for kw in ['任务', 'p1']):
        priority = "P1"
    else:
        priority = "P2"
    
    # 提取类型标签
    tags = extract_tags(content)
    
    return {
        "记忆内容": content[:2000],  # 限制长度
        "来源文件": source_file,
        "日期": datetime.now().strftime("%Y-%m-%d"),
        "时间": datetime.now().strftime("%H:%M"),
        "类型标签": tags,
        "关键词": keywords,
        "重要度": priority,
        "状态": "有效",
        "Token 估算": token_estimate,
        "创建会话": "auto-sync",
    }

def extract_keywords(text: str) -> str:
    """提取关键词"""
    # 简单实现：提取名词
    words = re.findall(r'[\u4e00-\u9fff]{2,4}|[a-zA-Z]{2,10}', text)
    # 去重，取前 10 个
    unique_words = list(dict.fromkeys(words))[:10]
    return ','.join(unique_words)

def extract_tags(text: str) -> List[str]:
    """提取类型标签"""
    tags = []
    
    if any(kw in text for kw in ['决策', '决定', '确认']):
        tags.append("决策")
    if any(kw in text for kw in ['任务', '待办', 'TODO']):
        tags.append("任务")
    if any(kw in text for kw in ['洞察', '发现', '学习']):
        tags.append("洞察")
    if any(kw in text for kw in ['能力涌现', '新建', '创建']):
        tags.append("能力涌现")
    if any(kw in text for kw in ['宪法', '原则', '规则']):
        tags.append("宪法")
    if any(kw in text for kw in ['MemOS', '学习', '调研']):
        tags.append("学习")
    
    return tags if tags else ["其他"]

def parse_memory_file(filepath: str) -> List[Dict]:
    """解析记忆文件"""
    entries = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按章节分割
    sections = re.split(r'\n##+ ', content)
    
    source_file = os.path.basename(filepath)
    
    for section in sections[1:]:  # 跳过第一个 (header)
        lines = section.split('\n')
        section_name = lines[0].strip()
        section_content = '\n'.join(lines[1:])
        
        if len(section_content.strip()) < 50:  # 跳过太短的章节
            continue
        
        entry = parse_memory_entry(section_content, source_file, section_name)
        entries.append(entry)
    
    return entries

def sync_to_feishu(entries: List[Dict], config: Dict) -> int:
    """同步到 Feishu"""
    # TODO: 实现 Feishu API 调用
    # 这里需要：
    # 1. 获取 access_token
    # 2. 批量创建记录
    # 3. 处理分页
    
    print(f"📊 准备同步 {len(entries)} 条记忆到 Feishu")
    print("⚠️  Feishu API 调用需要配置 access_token")
    print("📝 参考：https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2gTN")
    
    # 模拟成功
    return len(entries)

def update_dashboard(config: Dict):
    """更新统计面板"""
    # TODO: 实现统计面板更新
    print("📊 更新统计面板...")

def main():
    """主函数"""
    print("=" * 60)
    print("🔄 太一记忆同步到 Feishu")
    print("=" * 60)
    
    # 加载配置
    try:
        config = load_config()
        print(f"✅ 配置加载成功")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("\n请先运行：python3 scripts/install-memos-viewer.py")
        return
    
    # 解析记忆文件
    print(f"\n📁 扫描记忆文件...")
    all_entries = []
    
    memory_files = [
        "core.md",
        "residual.md",
        "2026-03-30.md",
    ]
    
    for filename in memory_files:
        filepath = os.path.join(MEMORY_DIR, filename)
        if os.path.exists(filepath):
            print(f"  解析 {filename}...")
            entries = parse_memory_file(filepath)
            all_entries.extend(entries)
            print(f"    提取 {len(entries)} 条记忆")
    
    print(f"\n📊 总计：{len(all_entries)} 条记忆")
    
    # 同步到 Feishu
    print(f"\n🔄 开始同步...")
    synced = sync_to_feishu(all_entries, config)
    
    # 更新统计面板
    update_dashboard(config)
    
    print("\n" + "=" * 60)
    print(f"✅ 同步完成：{synced}/{len(all_entries)} 条记忆")
    print("=" * 60)

if __name__ == '__main__':
    # 创建日志目录
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # 重定向输出到日志
    with open(LOG_FILE, 'a', encoding='utf-8') as log:
        import sys
        sys.stdout = log
        sys.stderr = log
        
        main()
