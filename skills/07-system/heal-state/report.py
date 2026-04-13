#!/usr/bin/env python3
"""
Heal-State Skill - Cron 汇报脚本
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core import HealState
from reporter import HealReporter

def main():
    """生成并发送汇报"""
    reporter = HealReporter()
    report = reporter.generate_report()
    
    print(report)
    
    # 写入日志
    log_file = Path("/tmp/openclaw/heal-report.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n--- {Path.home()} ---\n")
        f.write(report)
        f.write("\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
