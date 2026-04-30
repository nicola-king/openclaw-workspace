#!/usr/bin/env python3
"""
定时任务调度器 - 道 Agent & 悟 Agent
太一 AGI · 2026-04-15

定时推送:
- 道 Agent: 每日 08:00 (北京时间)
- 悟 Agent: 每日 20:00 (北京时间)
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

class WisdomScheduler:
    """智慧调度器"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.dao_script = self.workspace_root / "skills" / "05-content" / "dao-agent" / "src" / "dao_agent.py"
        self.wu_script = self.workspace_root / "skills" / "05-content" / "wu-agent" / "src" / "wu_agent.py"
        self.log_dir = self.workspace_root / "logs" / "wisdom-scheduler"
        
        # 创建日志目录
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def send_dao(self) -> bool:
        """发送道 Agent 每日智慧"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🌿 发送道 Agent 每日智慧...")
        
        if not self.dao_script.exists():
            print("❌ 道 Agent 脚本不存在")
            return False
        
        try:
            result = subprocess.run(
                ["python3", str(self.dao_script), "--daily"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.workspace_root)
            )
            
            if result.returncode == 0:
                print("✅ 道 Agent 发送成功")
                self._log("dao", "success", result.stdout)
                return True
            else:
                print(f"❌ 道 Agent 发送失败：{result.stderr[:200]}")
                self._log("dao", "error", result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ 道 Agent 发送异常：{str(e)}")
            self._log("dao", "exception", str(e))
            return False
    
    def send_wu(self) -> bool:
        """发送悟 Agent 每日智慧"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🪷 发送悟 Agent 每日智慧...")
        
        if not self.wu_script.exists():
            print("❌ 悟 Agent 脚本不存在")
            return False
        
        try:
            result = subprocess.run(
                ["python3", str(self.wu_script), "--daily"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.workspace_root)
            )
            
            if result.returncode == 0:
                print("✅ 悟 Agent 发送成功")
                self._log("wu", "success", result.stdout)
                return True
            else:
                print(f"❌ 悟 Agent 发送失败：{result.stderr[:200]}")
                self._log("wu", "error", result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ 悟 Agent 发送异常：{str(e)}")
            self._log("wu", "exception", str(e))
            return False
    
    def _log(self, agent: str, status: str, message: str):
        """记录日志"""
        log_file = self.log_dir / f"{agent}-{datetime.now().strftime('%Y-%m')}.log"
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{status}] {message}\n"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    
    def check_and_send(self):
        """检查时间并发送"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # 道 Agent: 08:00
        if current_time == "08:00":
            self.send_dao()
        
        # 悟 Agent: 20:00
        if current_time == "20:00":
            self.send_wu()
    
    def run_daemon(self):
        """运行守护进程 (每分钟检查)"""
        print("="*60)
        print("⏰ 智慧调度器启动")
        print("="*60)
        print(f"🌿 道 Agent: 每日 08:00 (北京时间)")
        print(f"🪷 悟 Agent: 每日 20:00 (北京时间)")
        print("="*60)
        
        last_dao = None
        last_wu = None
        
        while True:
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M")
            
            # 道 Agent: 08:00 (每天只发送一次)
            if current_time == "08:00" and last_dao != current_date:
                self.send_dao()
                last_dao = current_date
            
            # 悟 Agent: 20:00 (每天只发送一次)
            if current_time == "20:00" and last_wu != current_date:
                self.send_wu()
                last_wu = current_date
            
            # 每分钟检查
            time.sleep(60)
    
    def send_now(self, agent: str = "both"):
        """立即发送"""
        if agent in ["dao", "both"]:
            self.send_dao()
        
        if agent in ["wu", "both"]:
            self.send_wu()


def main():
    """主函数"""
    workspace_root = "/home/nicola/.openclaw/workspace"
    scheduler = WisdomScheduler(workspace_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--daemon":
            scheduler.run_daemon()
        elif command == "--dao":
            scheduler.send_dao()
        elif command == "--wu":
            scheduler.send_wu()
        elif command == "--now":
            scheduler.send_now("both")
        else:
            print(f"未知命令：{command}")
            print("用法：scheduler.py [--daemon|--dao|--wu|--now]")
    else:
        # 默认发送一次
        scheduler.send_now("both")


if __name__ == "__main__":
    main()
