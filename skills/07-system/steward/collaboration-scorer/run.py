#!/usr/bin/env python3
"""协作评分 - 守藏吏 Skill - 事件驱动"""

from datetime import datetime
from pathlib import Path

SCORE_FILE = Path("/home/nicola/.openclaw/workspace/memory/bot-collaboration-scores.md")

def record_score(drill_id, scores):
    avg = sum(scores.values()) / len(scores)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"\n### {drill_id} - {timestamp}\n- 职责清晰度：{scores.get('clarity', 0)}/10\n- 响应速度：{scores.get('speed', 0)}/10\n- 输出质量：{scores.get('quality', 0)}/10\n- 自主率：{scores.get('autonomy', 0)}/10\n- **平均分：{avg:.1f}/10**\n\n---\n"
    with open(SCORE_FILE, 'a') as f:
        f.write(entry)
    return avg

def main():
    print("📊 守藏吏协作评分...")
    avg = record_score("DRILL-001", {"clarity": 9, "speed": 8, "quality": 9, "autonomy": 10})
    print(f"✅ 协作评分完成：平均分{avg:.1f}/10")

if __name__ == "__main__":
    main()
