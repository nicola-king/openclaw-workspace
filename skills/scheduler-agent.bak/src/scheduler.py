#!/usr/bin/env python3
"""
Scheduler Agent - 定时任务自进化智能体 v3.0
太一 AGI · 2026-04-15

管理所有 Cron 定时任务，按照 PDCA 循环策略严格执行，主动发现问题自主解决：
- Cron 配置管理
- 定时任务调度
- PDCA 循环执行
- 自进化优化
- 任务监控告警
- 主动问题发现
- 自主问题解决
"""

import os
import json
import time
import subprocess
import signal
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SchedulerAgent:
    """智能调度智能体"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.scripts_dir = self.workspace_root / "scripts"
        self.monitoring_dir = self.workspace_root / "monitoring"
        self.config_path = self.workspace_root / "skills" / "scheduler-agent" / "config" / "scheduler-config.json"
        self.state_path = self.monitoring_dir / "scheduler-state.json"
        self.log_path = self.monitoring_dir / "scheduler-log.json"
        self.pdca_log_path = self.monitoring_dir / "pdca-cycle-log.json"
        self.crontab_path = self.workspace_root / "final-crontab.txt"
        
        # 定时任务配置
        self.scheduled_tasks = [
            {"time": "06:00", "name": "宪法学习", "script": "daily-constitution-study.py"},
            {"time": "07:00", "name": "周易研习", "script": "yijing-daily-study.py"},
            {"time": "07:00", "name": "天气预报", "script": "weather-forecast.py"},
            {"time": "07:30", "name": "先秦经典", "script": "xianqin-daily-study.py"},
            {"time": "08:00", "name": "道 Agent", "script": "wisdom-scheduler --dao"},
            {"time": "09:00", "name": "微信报告", "script": "wechat-metrics-dashboard.py"},
            {"time": "18:00", "name": "微信发布", "script": "wechat_sender.py"},
            {"time": "20:00", "name": "悟 Agent", "script": "wisdom-scheduler --wu"},
            {"time": "23:00", "name": "日报生成", "script": "daily-report-generator.py"},
            {"time": "每小时", "name": "健康检查", "script": "hourly-health-check.py"},
            {"time": "每 30 分钟", "name": "Auto Bug Fix", "script": "auto-bug-fixer-enhanced.py"},
        ]
        
        # 主动验证机制
        self.verification_results = {
            "scripts": {},
            "logs": {},
            "daemons": {},
            "data": {},
            "cron": {},
        }
        
        # 默认配置
        self.config = {
            "default_interval": 3600,  # 默认 1 小时
            "min_interval": 1800,      # 最小 30 分钟
            "max_interval": 7200,      # 最大 2 小时
            "lag_threshold": 0.5,      # 滞后阈值 50%
            "ahead_threshold": 0.2,    # 超前阈值 20%
            "max_concurrent": 3,       # 最大并发数
            "memory_limit": "512MB",   # 内存限制
        }
        
        # 加载配置
        self._load_config()
        
        # 状态
        self.state = {
            "last_run": None,
            "next_run": None,
            "current_interval": self.config["default_interval"],
            "tasks_completed": 0,
            "tasks_failed": 0,
            "consecutive_success": 0,
            "running": False,
        }
        
        # 加载状态
        self._load_state()
        
        # 任务队列
        self.task_queue = []
        self.running_processes = []
    
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text(encoding="utf-8"))
                self.config.update(config_data)
            except:
                pass
        
        # 保存配置
        self.config_path.parent.mkdir(exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def _load_state(self):
        """加载状态"""
        if self.state_path.exists():
            try:
                state_data = json.loads(self.state_path.read_text(encoding="utf-8"))
                self.state.update(state_data)
            except:
                pass
    
    def _save_state(self):
        """保存状态"""
        self.state["last_updated"] = datetime.now().isoformat()
        self.state_path.parent.mkdir(exist_ok=True)
        self.state_path.write_text(json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def _log_execution(self, task: str, success: bool, duration: float):
        """记录执行日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "success": success,
            "duration_seconds": duration,
        }
        
        # 加载历史日志
        if self.log_path.exists():
            try:
                logs = json.loads(self.log_path.read_text(encoding="utf-8"))
            except:
                logs = []
        else:
            logs = []
        
        # 添加新日志，保留最近 100 条
        logs.append(log_entry)
        logs = logs[-100:]
        
        self.log_path.parent.mkdir(exist_ok=True)
        self.log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def get_goal_progress(self) -> float:
        """获取目标进度"""
        tracker_path = self.monitoring_dir / "goal-tracker.json"
        if tracker_path.exists():
            try:
                tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
                # 计算平均进度
                goals = tracker.get("goals", {}).get("short_term", {}).get("targets", {})
                progresses = []
                for key, value in goals.items():
                    if isinstance(value, dict) and "current" in value and "target" in value:
                        current = value["current"]
                        target = value["target"]
                        if target > 0:
                            progress = current / target
                            progresses.append(progress)
                
                if progresses:
                    return sum(progresses) / len(progresses)
            except:
                pass
        
        return 0.0
    
    def calculate_interval(self) -> int:
        """智能计算执行间隔"""
        progress = self.get_goal_progress()
        
        # 根据进度动态调整间隔
        if progress < self.config["lag_threshold"]:
            # 滞后：加速执行
            interval = self.config["min_interval"]
            print(f"🔴 目标滞后 ({progress:.1%})，加速到每{interval//60}分钟")
        elif progress > (1 + self.config["ahead_threshold"]):
            # 超前：减速执行
            interval = self.config["max_interval"]
            print(f"🟢 目标超前 ({progress:.1%})，减速到每{interval//60}分钟")
        else:
            # 正常：保持默认
            interval = self.config["default_interval"]
            print(f"🟡 目标正常 ({progress:.1%})，保持每{interval//60}分钟")
        
        return interval
    
    def execute_task(self, task_name: str, script: str) -> bool:
        """执行任务"""
        print(f"\n🚀 执行任务：{task_name}")
        
        start_time = datetime.now()
        script_path = self.scripts_dir / script
        
        if not script_path.exists():
            print(f"❌ 脚本不存在：{script_path}")
            return False
        
        try:
            # 执行脚本
            result = subprocess.run(
                ["python3", str(script_path)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 分钟超时
                cwd=str(self.workspace_root)
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            # 记录日志
            success = result.returncode == 0
            self._log_execution(task_name, success, duration)
            
            # 更新状态
            if success:
                self.state["tasks_completed"] += 1
                self.state["consecutive_success"] += 1
                print(f"✅ {task_name} 执行成功 (耗时：{duration:.1f}秒)")
            else:
                self.state["tasks_failed"] += 1
                self.state["consecutive_success"] = 0
                print(f"❌ {task_name} 执行失败：{result.stderr[:200]}")
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"❌ {task_name} 执行超时")
            self._log_execution(task_name, False, 300)
            return False
        except Exception as e:
            print(f"❌ {task_name} 执行异常：{str(e)[:200]}")
            self._log_execution(task_name, False, 0)
            return False
    
    def run_pdca(self) -> bool:
        """执行 PDCA 循环"""
        return self.execute_task("PDCA Cycle", "pdca-simple.py")
    
    def run_evolution(self) -> bool:
        """执行自进化引擎"""
        return self.execute_task("Evolution Engine", "self-evolution-engine-v2.py")
    
    def run_standardization(self) -> bool:
        """执行技能标准化"""
        return self.execute_task("Skill Standardization", "standardize-emerged-skills.py")
    
    def run_all_tasks(self):
        """执行所有任务"""
        print("\n" + "="*60)
        print("🚀 Scheduler Agent - 执行所有任务")
        print("="*60)
        
        tasks = [
            ("PDCA 循环", "pdca-simple.py"),
            ("自进化引擎", "self-evolution-engine-v2.py"),
            ("技能标准化", "standardize-emerged-skills.py"),
        ]
        
        results = []
        for task_name, script in tasks:
            result = self.execute_task(task_name, script)
            results.append(result)
            time.sleep(2)  # 任务间隔
        
        # 总结
        success_count = sum(results)
        print(f"\n{'='*60}")
        print(f"✅ 执行完成：{success_count}/{len(tasks)} 成功")
        print(f"{'='*60}")
        
        return success_count == len(tasks)
    
    def run_pdca_cycle(self) -> Dict:
        """执行完整 PDCA 循环"""
        print("\n" + "="*60)
        print("🔄 Scheduler Agent - PDCA 循环")
        print("="*60)
        
        pdca_result = {
            "timestamp": datetime.now().isoformat(),
            "phases": {},
        }
        
        # Plan 阶段
        print("\n[Plan] 计划阶段...")
        plan_result = self._pdca_plan()
        pdca_result["phases"]["plan"] = plan_result
        
        # Do 阶段
        print("\n[Do] 执行阶段...")
        do_result = self._pdca_do()
        pdca_result["phases"]["do"] = do_result
        
        # Check 阶段
        print("\n[Check] 检查阶段...")
        check_result = self._pdca_check(do_result)
        pdca_result["phases"]["check"] = check_result
        
        # Act 阶段
        print("\n[Act] 处理阶段...")
        act_result = self._pdca_act(check_result)
        pdca_result["phases"]["act"] = act_result
        
        # 保存 PDCA 日志
        self._save_pdca_log(pdca_result)
        
        print(f"\n{'='*60}")
        print("✅ PDCA 循环完成！")
        print(f"{'='*60}")
        
        return pdca_result
    
    def _pdca_plan(self) -> Dict:
        """PDCA - Plan 阶段：设定目标"""
        # 获取当前状态
        progress = self.get_goal_progress()
        
        # 设定目标
        if progress < self.config["lag_threshold"]:
            target = "accelerate"  # 加速
            interval = self.config["min_interval"]
        elif progress > (1 + self.config["ahead_threshold"]):
            target = "decelerate"  # 减速
            interval = self.config["max_interval"]
        else:
            target = "maintain"  # 保持
            interval = self.config["default_interval"]
        
        plan = {
            "current_progress": progress,
            "target": target,
            "next_interval": interval,
            "timestamp": datetime.now().isoformat(),
        }
        
        print(f"  当前进度：{progress:.1%}")
        print(f"  目标：{target}")
        print(f"  下次间隔：{interval//60}分钟")
        
        return plan
    
    def _pdca_do(self) -> Dict:
        """PDCA - Do 阶段：执行任务"""
        # 执行所有任务
        result = self.run_all_tasks()
        
        do_result = {
            "executed": True,
            "success": result,
            "timestamp": datetime.now().isoformat(),
        }
        
        return do_result
    
    def _pdca_check(self, do_result: Dict) -> Dict:
        """PDCA - Check 阶段：验证结果"""
        # 获取新进度
        new_progress = self.get_goal_progress()
        
        # 计算成功率
        success_rate = 1.0 if do_result["success"] else 0.0
        
        check_result = {
            "new_progress": new_progress,
            "success_rate": success_rate,
            "effectiveness": "high" if success_rate > 0.8 else "medium" if success_rate > 0.5 else "low",
            "timestamp": datetime.now().isoformat(),
        }
        
        print(f"  新进度：{new_progress:.1%}")
        print(f"  成功率：{success_rate:.1%}")
        print(f"  效果：{check_result['effectiveness']}")
        
        return check_result
    
    def _pdca_act(self, check_result: Dict) -> Dict:
        """PDCA - Act 阶段：处理改进"""
        # 根据检查结果调整策略
        if check_result["effectiveness"] == "low":
            # 效果差，调整策略
            action = "adjust_strategy"
            self.config["default_interval"] = max(
                self.config["min_interval"],
                self.config["default_interval"] - 600
            )
        elif check_result["effectiveness"] == "high":
            # 效果好，保持策略
            action = "maintain_strategy"
        else:
            action = "monitor"
        
        act_result = {
            "action": action,
            "new_interval": self.config["default_interval"],
            "timestamp": datetime.now().isoformat(),
        }
        
        print(f"  行动：{action}")
        print(f"  新间隔：{self.config['default_interval']//60}分钟")
        
        # 保存配置
        self._save_config()
        
        return act_result
    
    def _save_pdca_log(self, pdca_result: Dict):
        """保存 PDCA 日志"""
        # 加载历史
        if self.pdca_log_path.exists():
            try:
                data = json.loads(self.pdca_log_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    logs = data
                else:
                    logs = [data]
            except:
                logs = []
        else:
            logs = []
        
        # 添加新日志
        logs.append(pdca_result)
        logs = logs[-100:]  # 保留最近 100 条
        
        self.pdca_log_path.parent.mkdir(exist_ok=True)
        self.pdca_log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def _save_config(self):
        """保存配置"""
        self.config_path.parent.mkdir(exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False), encoding="utf-8")
    
    def run_scheduler_loop(self):
        """运行调度循环"""
        print("\n" + "="*60)
        print("🤖 Scheduler Agent 启动")
        print("="*60)
        
        self.state["running"] = True
        self._save_state()
        
        try:
            while self.state["running"]:
                # 计算智能间隔
                interval = self.calculate_interval()
                self.state["current_interval"] = interval
                
                # 设置下次执行时间
                next_run = datetime.now() + timedelta(seconds=interval)
                self.state["next_run"] = next_run.isoformat()
                self._save_state()
                
                print(f"\n⏰ 下次执行：{next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"📊 状态：完成={self.state['tasks_completed']}, 失败={self.state['tasks_failed']}, 连续成功={self.state['consecutive_success']}")
                
                # 执行任务
                self.run_all_tasks()
                
                # 等待下次执行
                print(f"\n💤 等待{interval}秒...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  收到中断信号，停止调度...")
            self.state["running"] = False
            self._save_state()
        except Exception as e:
            print(f"\n❌ 调度异常：{str(e)}")
            self.state["running"] = False
            self._save_state()
            raise
        
        print("\n✅ Scheduler Agent 已停止")
    
    def show_status(self):
        """显示状态"""
        print("\n" + "="*60)
        print("📊 Scheduler Agent 状态")
        print("="*60)
        
        self._load_state()
        
        print(f"运行中：{self.state['running']}")
        print(f"上次执行：{self.state.get('last_run', '无')}")
        print(f"下次执行：{self.state.get('next_run', '无')}")
        print(f"当前间隔：{self.state.get('current_interval', 3600)//60} 分钟")
        print(f"完成任务：{self.state.get('tasks_completed', 0)}")
        print(f"失败任务：{self.state.get('tasks_failed', 0)}")
        print(f"连续成功：{self.state.get('consecutive_success', 0)}")
        
        # 显示最近日志
        if self.log_path.exists():
            try:
                logs = json.loads(self.log_path.read_text(encoding="utf-8"))
                print(f"\n最近执行 ({len(logs)}条):")
                for log in logs[-5:]:
                    status = "✅" if log["success"] else "❌"
                    print(f"  {status} {log['task']} ({log['duration_seconds']:.1f}s) - {log['timestamp'][:19]}")
            except:
                pass
        
        print(f"\n{'='*60}")
    
    def stop(self):
        """停止调度"""
        print("\n⚠️  停止 Scheduler Agent...")
        self.state["running"] = False
        self._save_state()
        print("✅ Scheduler Agent 已停止")


def main():
    """主函数"""
    workspace_root = "/home/nicola/.openclaw/workspace"
    scheduler = SchedulerAgent(workspace_root)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--status":
            scheduler.show_status()
        elif command == "--stop":
            scheduler.stop()
        elif command == "--run-pdca":
            scheduler.run_pdca_cycle()
        elif command == "--run-all":
            scheduler.run_all_tasks()
        else:
            print(f"未知命令：{command}")
            print("用法：scheduler.py [--status|--stop|--run-pdca|--run-all]")
    else:
        # 默认运行调度循环
        scheduler.run_scheduler_loop()


if __name__ == "__main__":
    main()
