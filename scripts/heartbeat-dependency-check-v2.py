#!/usr/bin/env python3
"""
HEARTBEAT 依赖检查脚本 v2
集成任务依赖追踪器到心跳检查

运行频率：每小时
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 直接导入文件
sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/task-orchestrator')
exec(open('/home/nicola/.openclaw/workspace/skills/task-orchestrator/dependency-tracker.py').read())

def main():
    tracker = DependencyTracker()
    
    print("=" * 60)
    print("💓 HEARTBEAT · 任务依赖检查")
    print("=" * 60)
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # 获取阻塞任务
    blocked = tracker.get_blocked_tasks()
    if blocked:
        print(f"🚨 被阻塞任务 ({len(blocked)})")
        for bt in blocked[:5]:
            print(f"\n  ❌ {bt['name']}")
            print(f"     原因：{bt['reason']}")
            if bt.get('unmet'):
                print(f"     未满足：{', '.join(bt['unmet'])}")
    else:
        print("✅ 无阻塞任务")
    
    # 获取即将到期任务
    due = tracker.get_due_tasks(days_ahead=3)
    if due:
        print(f"\n⏰ 即将到期 ({len(due)})")
        for dt in due[:5]:
            emoji = "🔴" if dt['days_left'] <= 1 else "🟡"
            print(f"\n  {emoji} {dt['name']} [{dt['priority']}]")
            print(f"     截止：{dt['deadline'][:10]} (剩余 {dt['days_left']} 天)")
    else:
        print("\n✅ 无即将到期任务")
    
    # 总体统计
    total = len(tracker.tasks)
    completed = sum(1 for t in tracker.tasks.values() if t['status'] == 'completed')
    pending = total - completed
    
    print(f"\n📊 总体状态")
    print(f"  总任务：{total}")
    print(f"  已完成：{completed} ({completed/total*100:.1f}%)")
    print(f"  待处理：{pending}")
    print(f"  阻塞：{len(blocked)}")
    
    # 告警
    if len(blocked) > 5:
        print("\n⚠️  告警：阻塞任务过多 (>5)")
    
    if any(d['days_left'] <= 1 for d in due):
        print("\n⚠️  告警：有任务 1 天内到期")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
