#!/usr/bin/env python3
"""
Auto-Exec 进度汇报脚本（Cron 调用）
每 5 分钟自动执行，发送进度汇报到微信
"""

import sys
import json
from pathlib import Path

# 添加 skills 路径
sys.path.insert(0, str(Path.home() / ".openclaw" / "workspace" / "skills"))

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from core import AutoExecStatus
from reporter import ProgressReporter

def main():
    """生成并发送汇报"""
    reporter = ProgressReporter()
    report = reporter.generate_report()
    
    # 输出汇报（OpenClaw 会捕获 stdout 并发送）
    print(report)
    
    # 同时写入日志
    log_file = Path("/tmp/openclaw/auto-exec-report.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n--- {Path.home()} ---\n")
        f.write(report)
        f.write("\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
