#!/usr/bin/env python3
# scripts/auto-task-summarizer.py

"""
太一任务自动总结器

功能:
1. Session 结束时自动总结任务
2. 提取关键决策和行动项
3. 写入 memory/2026-03-30.md
4. 更新 HEARTBEAT.md 待办

使用:
    python3 scripts/auto-task-summarizer.py [session_log]

集成:
    - OpenClaw lifecycle hook (onAfterRun)
    - crontab 定时执行 (每小时)
"""

import os
import re
import json
from datetime import datetime
from typing import List, Dict

# 配置
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
TODAY_FILE = os.path.join(MEMORY_DIR, "2026-03-30.md")
HEARTBEAT_FILE = os.path.expanduser("~/.openclaw/workspace/HEARTBEAT.md")

def extract_decisions(text: str) -> List[str]:
    """提取决策项"""
    decisions = []
    
    # 匹配模式：**决策**: 或 [决策] 或 ### [决策]
    patterns = [
        r'\*\*决策\*\*:\s*(.+?)(?=\n|$)',
        r'\[决策\]\s*(.+?)(?=\n|$)',
        r'### \[决策\]\s*(.+?)(?=\n|$)',
        r'决策[:：]\s*(.+?)(?=\n|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        decisions.extend(matches)
    
    return [d.strip() for d in decisions if d.strip()]

def extract_tasks(text: str) -> List[Dict]:
    """提取任务项"""
    tasks = []
    
    # 匹配模式：- [ ] 任务描述 或 🔴 待执行
    patterns = [
        r'- \[([ x])\] (.+?)(?:\s*-\s*(.+?))?(?=\n|$)',
        r'([🔴🟡🟢✅])\s*(.+?)(?:\s*[-→]\s*(.+?))?(?=\n|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) == 3:
                status, task, deadline = match
                tasks.append({
                    "status": "done" if status in ['x', '✅', '🟢'] else "pending",
                    "task": task.strip(),
                    "deadline": deadline.strip() if deadline else None
                })
    
    return tasks

def extract_insights(text: str) -> List[str]:
    """提取洞察/学习"""
    insights = []
    
    patterns = [
        r'\*\*洞察\*\*:\s*(.+?)(?=\n|$)',
        r'\[洞察\]\s*(.+?)(?=\n|$)',
        r'核心洞察[:：]\s*(.+?)(?=\n|$)',
        r'关键洞察[:：]\s*(.+?)(?=\n|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        insights.extend(matches)
    
    return [i.strip() for i in insights if i.strip()]

def summarize_session(session_text: str) -> Dict:
    """
    总结 Session
    
    Returns:
        {
            "decisions": [...],
            "tasks": [...],
            "insights": [...],
            "summary": str
        }
    """
    return {
        "decisions": extract_decisions(session_text),
        "tasks": extract_tasks(session_text),
        "insights": extract_insights(session_text),
        "summary": generate_summary(session_text)
    }

def generate_summary(text: str) -> str:
    """生成一句话总结"""
    # 简单实现：提取第一个段落的前 100 字
    paragraphs = text.split('\n\n')
    if paragraphs:
        first_para = paragraphs[0].strip()
        return first_para[:200] + "..." if len(first_para) > 200 else first_para
    return "无总结"

def append_to_today_file(summary: Dict):
    """追加到今日记忆文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = f"\n---\n\n## 📝 Session 总结 ({timestamp})\n\n"
    
    if summary["decisions"]:
        content += "### 决策\n"
        for decision in summary["decisions"]:
            content += f"- {decision}\n"
        content += "\n"
    
    if summary["tasks"]:
        content += "### 任务\n"
        for task in summary["tasks"]:
            status = "✅" if task["status"] == "done" else "🔴"
            deadline = f" (截止：{task['deadline']})" if task["deadline"] else ""
            content += f"- {status} {task['task']}{deadline}\n"
        content += "\n"
    
    if summary["insights"]:
        content += "### 洞察\n"
        for insight in summary["insights"]:
            content += f"- {insight}\n"
        content += "\n"
    
    # 追加到文件
    with open(TODAY_FILE, 'a', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已追加到 {TODAY_FILE}")

def update_heartbeat(tasks: List[Dict]):
    """更新 HEARTBEAT.md 待办"""
    pending_tasks = [t for t in tasks if t["status"] == "pending"]
    
    if not pending_tasks:
        return
    
    # 读取现有 HEARTBEAT.md
    if os.path.exists(HEARTBEAT_FILE):
        with open(HEARTBEAT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# HEARTBEAT.md - 核心待办\n\n"
    
    # 追加新任务
    new_section = f"\n## 🆕 新增待办 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
    for task in pending_tasks[:5]:  # 最多 5 个
        new_section += f"- [ ] {task['task']}\n"
    
    # 写回文件
    with open(HEARTBEAT_FILE, 'w', encoding='utf-8') as f:
        f.write(content + new_section)
    
    print(f"✅ 已更新 {HEARTBEAT_FILE}")

def main():
    """主函数"""
    import sys
    
    # 从 stdin 或文件读取 session 日志
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            session_text = f.read()
    else:
        session_text = sys.stdin.read()
    
    if not session_text.strip():
        print("⚠️  无输入内容")
        return
    
    print("🔍 开始 Session 总结...")
    print("=" * 60)
    
    summary = summarize_session(session_text)
    
    print(f"\n📊 提取结果:")
    print(f"  决策：{len(summary['decisions'])} 项")
    print(f"  任务：{len(summary['tasks'])} 项")
    print(f"  洞察：{len(summary['insights'])} 项")
    
    # 写入文件
    append_to_today_file(summary)
    update_heartbeat(summary["tasks"])
    
    print("\n" + "=" * 60)
    print("✅ Session 总结完成")
    
    # 输出摘要
    print(f"\n📝 摘要:")
    print(summary["summary"])

if __name__ == '__main__':
    main()
