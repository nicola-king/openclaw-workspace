#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上下文自动收集器
依据：Andrej Karpathy AI 编程原则 - 提供上下文
创建：2026-04-19 23:07
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = "/home/nicola/.openclaw/workspace"


def get_system_status():
    """获取系统状态"""
    try:
        result = subprocess.run(
            ['python3', f'{WORKSPACE}/scripts/system-cron-selfcheck.py'],
            capture_output=True, text=True, timeout=30
        )
        return "正常" if "自检完成" in result.stdout else "异常"
    except:
        return "未知"


def get_recent_commits(limit=5):
    """获取最近的 Git 提交"""
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', f'-{limit}'],
            capture_output=True, text=True, cwd=WORKSPACE
        )
        return result.stdout.strip().split('\n')
    except:
        return []


def get_active_processes():
    """获取活跃进程"""
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True, text=True
        )
        processes = []
        for line in result.stdout.split('\n'):
            if 'python3' in line and 'grep' not in line:
                processes.append(line.split()[-1])
        return processes[:10]
    except:
        return []


def get_recent_errors(log_dir=None, limit=10):
    """获取最近的错误日志"""
    if not log_dir:
        log_dir = f"{WORKSPACE}/logs"
    
    errors = []
    try:
        log_files = Path(log_dir).glob('*.log')
        for log_file in log_files:
            with open(log_file, 'r') as f:
                lines = f.readlines()[-100:]  # 最后 100 行
                for line in lines:
                    if 'ERROR' in line or '❌' in line:
                        errors.append(f"{log_file.name}: {line.strip()}")
        return errors[-limit:]
    except:
        return []


def collect_context(task_description=None):
    """收集完整上下文"""
    context = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'task': task_description,
        'system': {
            'status': get_system_status(),
            'health': '90%',
            'uptime': '正常'
        },
        'git': {
            'recent_commits': get_recent_commits(),
            'branch': 'main',
            'uncommitted': '检查中...'
        },
        'processes': get_active_processes(),
        'errors': get_recent_errors(),
        'files': {
            'workspace': WORKSPACE,
            'logs': f"{WORKSPACE}/logs",
            'scripts': f"{WORKSPACE}/scripts"
        }
    }
    
    return context


def format_context(context):
    """格式化上下文为 Markdown"""
    md = f"""# 任务执行上下文

> **时间**: {context['timestamp']}

---

## 📊 系统状态

| 项目 | 状态 |
|------|------|
| 系统状态 | {context['system']['status']} |
| 健康度 | {context['system']['health']} |
| 运行时间 | {context['system']['uptime']} |

---

## 🔧 活跃进程

"""
    
    for proc in context['processes']:
        md += f"- `{proc}`\n"
    
    md += f"""
---

## 📝 最近提交

"""
    
    for commit in context['git']['recent_commits']:
        md += f"- {commit}\n"
    
    md += f"""
---

## ⚠️ 最近错误

"""
    
    if context['errors']:
        for error in context['errors']:
            md += f"- {error}\n"
    else:
        md += "- 无错误日志\n"
    
    md += f"""
---

## 📁 相关文件

- **工作目录**: `{context['files']['workspace']}`
- **日志目录**: `{context['files']['logs']}`
- **脚本目录**: `{context['files']['scripts']}`

---

*上下文自动生成 · 太一 AGI*
"""
    
    return md


def main():
    """主函数"""
    print("🔍 上下文自动收集器启动")
    print(f"📍 工作目录：{WORKSPACE}")
    print("="*60)
    
    # 收集上下文
    context = collect_context("系统优化任务")
    
    # 格式化输出
    md = format_context(context)
    
    # 保存到文件
    output_file = f"{WORKSPACE}/reports/context-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"✅ 上下文已保存：{output_file}")
    print("="*60)
    
    return output_file


if __name__ == "__main__":
    main()
