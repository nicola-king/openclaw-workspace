#!/usr/bin/env python3
"""意图准确 - 太一 Skill - 事件驱动"""

from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/home/nicola/.openclaw/workspace/memory/intent-accuracy-log.md")

def record_accuracy(task_id, accuracy, feedback=""):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"\n## {task_id} - {timestamp}\n- **准确率**: {accuracy}%\n- **反馈**: {feedback or '无'}\n- **是否需要追问**: {'是' if accuracy < 95 else '否'}\n\n---\n"
    with open(LOG_FILE, 'a') as f:
        f.write(entry)
    return accuracy

def main():
    print("🎯 太一意图准确记录...")
    acc = record_accuracy("TASK-001", 98, "准确理解用户意图")
    print(f"✅ 意图准确率：{acc}%")

if __name__ == "__main__":
    main()
