#!/usr/bin/env python3
"""
Auto-Exec Skill - 进度汇报模块
每 5 分钟自动汇报执行进度
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from core import AutoExecStatus

class ProgressReporter:
    """进度汇报器"""
    
    def __init__(self):
        self.status_engine = AutoExecStatus()
    
    def generate_report(self) -> str:
        """生成进度汇报"""
        status = self.status_engine.get_status()
        tracker = self.status_engine.get_tracker()
        
        # 进度条
        progress = status.get("progress", 0)
        bars = int(progress / 10)
        progress_bar = "█" * bars + "░" * (10 - bars)
        
        # 构建汇报
        report = []
        report.append("🔄 自动执行进度汇报")
        report.append("")
        
        # 当前任务
        if status.get("currentTask"):
            report.append(f"【当前任务】{status['currentTask']}")
        else:
            report.append("【当前任务】无")
        
        report.append(f"【进度】{progress_bar} {progress}%")
        report.append(f"【状态】{self._translate_status(status.get('status', 'idle'))}")
        
        if status.get("nextStep"):
            report.append(f"【下一步】{status['nextStep']}")
        
        if status.get("eta"):
            report.append(f"【预计完成】{status['eta']}")
        
        report.append("")
        
        # 今日完成
        completed = tracker.get("completedToday", [])
        if completed:
            report.append("【今日完成】")
            for task in completed[-5:]:  # 最近 5 个
                report.append(f"✅ {task}")
        else:
            report.append("【今日完成】暂无")
        
        report.append("")
        
        # 阻塞任务
        blocked = status.get("blockedSteps", [])
        if blocked:
            report.append("【阻塞任务】")
            for b in blocked[-3:]:
                if isinstance(b, dict):
                    report.append(f"🚨 {b.get('id', 'Unknown')}: {b.get('reason', '未知原因')}")
                else:
                    report.append(f"🚨 {b}")
        else:
            report.append("【阻塞任务】无")
        
        report.append("")
        report.append(f"_最后更新：{status.get('lastUpdate', '未知')}_")
        
        return "\n".join(report)
    
    def _translate_status(self, status: str) -> str:
        """翻译状态"""
        mapping = {
            "idle": "空闲",
            "running": "执行中",
            "blocked": "阻塞",
            "completed": "已完成"
        }
        return mapping.get(status, status)
    
    def send_report(self, channel: str = "openclaw-weixin", account: str = "taiyi"):
        """发送汇报（需要 OpenClaw message 工具）"""
        report = self.generate_report()
        
        # 通过 OpenClaw 发送
        # 实际使用时会调用 openclaw message send
        print(report)
        return report


if __name__ == "__main__":
    reporter = ProgressReporter()
    report = reporter.generate_report()
    print(report)
