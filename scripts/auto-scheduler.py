#!/usr/bin/env python3
"""
自动化任务调度器
用途：定时执行数据采集、内容生成、系统检查等任务
"""

import schedule
import time
from datetime import datetime
import subprocess
import json

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.tasks = []
    
    def add_task(self, name: str, command: str, schedule_str: str):
        """添加任务"""
        self.tasks.append({
            "name": name,
            "command": command,
            "schedule": schedule_str
        })
        
        # 解析调度时间并注册
        if schedule_str.startswith("daily "):
            time_str = schedule_str.split()[1]
            schedule.every().day.at(time_str).do(self.run_task, name, command)
        elif schedule_str.startswith("every "):
            interval = int(schedule_str.split()[1])
            unit = schedule_str.split()[2]
            if unit == "hour":
                schedule.every(interval).hours.do(self.run_task, name, command)
            elif unit == "minute":
                schedule.every(interval).minutes.do(self.run_task, name, command)
    
    def run_task(self, name: str, command: str):
        """执行任务"""
        print(f"[{datetime.now()}] 执行任务：{name}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            print(f"[{datetime.now()}] 任务完成：{name}, 返回码：{result.returncode}")
        except Exception as e:
            print(f"[{datetime.now()}] 任务失败：{name}, 错误：{e}")
    
    def run(self):
        """运行调度器"""
        print(f"[{datetime.now()}] 调度器启动，{len(self.tasks)} 个任务")
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    """配置任务"""
    scheduler = TaskScheduler()
    
    # 每日任务
    scheduler.add_task(
        "宪法学习",
        "bash /home/nicola/.openclaw/workspace/scripts/daily-constitution.sh",
        "daily 06:00"
    )
    
    scheduler.add_task(
        "日报生成",
        "bash /opt/openclaw-report.sh daily",
        "daily 23:00"
    )
    
    scheduler.add_task(
        "系统自检",
        "openclaw gateway status",
        "every 1 hour"
    )
    
    scheduler.add_task(
        "API 健康检查",
        "curl -s http://localhost:8000/health",
        "every 5 minute"
    )
    
    # 启动调度器
    scheduler.run()


if __name__ == "__main__":
    main()
