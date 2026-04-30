#!/bin/bash
# 自进化触发器脚本
# 每 15 分钟执行一次，检测能力涌现

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/nicola/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/evolution-trigger.log"

echo "🔮 自进化触发器启动..."
echo "时间：$(date)"
echo ""

# 确保日志目录存在
mkdir -p "$WORKSPACE/logs"

# 执行能力涌现检测
python3 << 'EOF' 2>&1 | tee -a "$LOG_FILE"
import sys
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/home/nicola/.openclaw/workspace/skills/03-automation/self-evolving-distillation-agent')

# 加载进化历史
evolution_file = Path('/home/nicola/.openclaw/workspace/.evolution/distillation_history.json')

if evolution_file.exists():
    with open(evolution_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        history = data.get('history', [])
        print(f"📊 加载进化历史：{len(history)} 次记录")
        
        if history:
            last_run = history[-1]
            print(f"  上次执行：{last_run.get('timestamp', 'unknown')}")
            print(f"  负熵增量：ΔS = {last_run.get('delta_s', 0):.2f}")
            print(f"  效率提升：{last_run.get('efficiency_improvement', 0):.1f}%")
else:
    print("📊 无进化历史")

# 检测能力涌现信号
print("\n🔮 检测能力涌现信号...")

skills_dir = Path('/home/nicola/.openclaw/workspace/skills/08-emerged')
if skills_dir.exists():
    today = datetime.now().strftime('%Y%m%d')
    new_skills = [d for d in skills_dir.iterdir() if d.is_dir() and today in d.name]
    
    if new_skills:
        print(f"✅ 检测到 {len(new_skills)} 个今日涌现技能:")
        for skill in new_skills:
            print(f"  - {skill.name}")
    else:
        print("✅ 无新涌现技能")

print("\n✅ 自进化触发器完成")
EOF

echo ""
echo "时间：$(date)"
