#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易监控自进化智能体 - 统一架构版本

功能:
1. 条件触发 (交易异常时触发)
2. 自动自愈 (重启交易进程)
3. 学习能力 (分析交易失败模式)
4. 知识固化 (写入 PITFALLS.md)

作者：太一 AGI
创建：2026-04-23
版本：v2.0 (自进化智能体)
"""

import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
sys.path.insert(0, str(WORKSPACE / "skills" / "07-system"))
from self_evolving_task_base import SelfEvolvingTask, TaskResult

# 交易进程配置
TRADING_PROCESSES = [
    "zhiji_auto_evolution_trader.py",
    "binance_24h_auto_trader.py",
]

class TradeSelfEvolvingMonitor(SelfEvolvingTask):
    """交易监控自进化智能体"""
    
    def __init__(self):
        super().__init__("trade_monitor")
        self.process_status = {}
    
    def check_process(self, process_name: str) -> dict:
        """检查进程状态"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', process_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                return {
                    'running': True,
                    'pids': pids,
                    'error': None
                }
            else:
                return {
                    'running': False,
                    'pids': [],
                    'error': f'进程 {process_name} 未运行'
                }
        except Exception as e:
            return {
                'running': False,
                'pids': [],
                'error': str(e)
            }
    
    def check(self) -> TaskResult:
        """条件检查 - 交易进程是否正常"""
        try:
            all_running = True
            errors = []
            
            for process_name in TRADING_PROCESSES:
                status = self.check_process(process_name)
                self.process_status[process_name] = status
                
                if not status['running']:
                    all_running = False
                    errors.append(status['error'])
            
            if all_running:
                return TaskResult(
                    task_id=self.task_id,
                    success=True,
                    need_heal=False,
                    error=None
                )
            else:
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error='; '.join(errors)
                )
                
        except Exception as e:
            return TaskResult(
                task_id=self.task_id,
                success=False,
                need_heal=True,
                error=f'检查失败：{str(e)}'
            )
    
    def heal(self, error: str) -> bool:
        """自动自愈 - 重启交易进程"""
        try:
            restarted = 0
            
            for process_name in TRADING_PROCESSES:
                if process_name in self.process_status:
                    if not self.process_status[process_name]['running']:
                        # 重启进程
                        script = WORKSPACE / "scripts" / process_name
                        if script.exists():
                            log_file = WORKSPACE / "logs" / process_name.replace('.py', '.log')
                            
                            with open(log_file, 'a') as log:
                                subprocess.Popen(
                                    ['python3', str(script)],
                                    stdout=log,
                                    stderr=log,
                                    start_new_session=True
                                )
                            
                            restarted += 1
                            time.sleep(2)
            
            if restarted > 0:
                self.write_to_pitfalls(
                    f'交易进程停止：{error}',
                    f'自动重启 {restarted} 个进程'
                )
                return True
            else:
                return False
                
        except Exception as e:
            print(f"自愈失败：{str(e)}")
            return False
    
    def get_status(self) -> dict:
        """获取状态"""
        status = super().get_status()
        status['processes'] = {
            name: '✅' if s['running'] else '❌'
            for name, s in self.process_status.items()
        }
        return status

if __name__ == '__main__':
    monitor = TradeSelfEvolvingMonitor()
    result = monitor.execute()
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📈 交易监控自进化智能体")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for name, status in monitor.process_status.items():
        print(f"{name}: {'✅ 运行中' if status['running'] else '❌ 已停止'}")
    print(f"")
    print(f"执行结果：{'✅ 成功' if result.success else '❌ 失败'}")
    print(f"需要自愈：{'🔧 是' if result.need_heal else '❌ 否'}")
    if result.error:
        print(f"错误信息：{result.error}")
    print(f"")
    print(f"进化指标:")
    print(f"  总运行次数：{monitor.metrics.total_runs}")
    print(f"  发现问题：{monitor.metrics.issues_found}")
    print(f"  自愈成功：{monitor.metrics.auto_healed}")
    print(f"  成功率：{monitor.metrics.success_rate:.1f}%")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
