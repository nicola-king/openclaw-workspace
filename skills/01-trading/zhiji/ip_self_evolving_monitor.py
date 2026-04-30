#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP 监控自进化智能体 - 统一架构版本

功能:
1. 条件触发 (IP 变化时触发)
2. 自动自愈 (自动切换 IP)
3. 学习能力 (分析 IP 变化模式)
4. 知识固化 (写入 PITFALLS.md)

作者：太一 AGI
创建：2026-04-23
版本：v2.0 (自进化智能体)
"""

import sys
import time
import requests
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
IP_FILE = Path("/tmp/last_export_ip.txt")
LOG_FILE = WORKSPACE / "logs" / "ip_self_evolving_monitor.log"
PROXY = "http://127.0.0.1:7890"

# 导入自进化基类
sys.path.insert(0, str(WORKSPACE / "skills" / "07-system"))
from self_evolving_task_base import SelfEvolvingTask, TaskResult

# 白名单 IP
WHITELISTED_IPS = [
    '141.11.146.70',
    '103.151.172.28',
    '103.151.173.206',
]

class IPSelfEvolvingMonitor(SelfEvolvingTask):
    """IP 监控自进化智能体"""
    
    def __init__(self):
        super().__init__("ip_monitor")
        self.last_ip = None
        self.current_ip = None
    
    def get_current_ip(self) -> str:
        """获取当前 IP"""
        try:
            response = requests.get(
                "https://api.ipify.org",
                proxies={'http': PROXY, 'https': PROXY},
                timeout=10
            )
            return response.text.strip()
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def get_last_ip(self) -> str:
        """读取上次 IP (只提取纯 IP 行)"""
        if IP_FILE.exists():
            content = IP_FILE.read_text().strip()
            for line in content.split('\n')[::-1]:
                line = line.strip()
                if len(line.split('.')) == 4 and all(p.isdigit() for p in line.split('.')):
                    return line
        return None
    
    def test_ip_stability(self, count: int = 5) -> tuple:
        """测试 IP 固定性"""
        ips = []
        for i in range(count):
            ip = self.get_current_ip()
            ips.append(ip)
            time.sleep(0.5)
        
        unique_ips = set(ips)
        if len(unique_ips) == 1:
            return True, ips[0]
        else:
            return False, f"IP 不固定 ({len(unique_ips)}个不同 IP)"
    
    def check(self) -> TaskResult:
        """条件检查 - IP 是否变化"""
        try:
            self.current_ip = self.get_current_ip()
            
            if self.current_ip.startswith("ERROR"):
                return TaskResult(
                    task_id=self.task_id,
                    success=False,
                    need_heal=True,
                    error=self.current_ip
                )
            
            self.last_ip = self.get_last_ip()
            
            if not self.last_ip:
                IP_FILE.write_text(self.current_ip)
                return TaskResult(
                    task_id=self.task_id,
                    success=True,
                    need_heal=False,
                    error=None
                )
            
            if self.current_ip != self.last_ip:
                is_stable, result = self.test_ip_stability()
                
                if not is_stable:
                    return TaskResult(
                        task_id=self.task_id,
                        success=False,
                        need_heal=True,
                        error=f"IP 飘浮：{result}"
                    )
                else:
                    return TaskResult(
                        task_id=self.task_id,
                        success=True,
                        need_heal=True,
                        error=f"IP 变化：{self.last_ip} → {self.current_ip}"
                    )
            else:
                return TaskResult(
                    task_id=self.task_id,
                    success=True,
                    need_heal=False,
                    error=None
                )
                
        except Exception as e:
            return TaskResult(
                task_id=self.task_id,
                success=False,
                need_heal=True,
                error=f"检查失败：{str(e)}"
            )
    
    def heal(self, error: str) -> bool:
        """自动自愈 - 更新 IP 文件"""
        try:
            if "IP 飘浮" in error:
                self.write_to_pitfalls(error, "IP 飘浮，需要锁定固定节点")
                return False
            elif "IP 变化" in error:
                IP_FILE.write_text(self.current_ip)
                
                if self.current_ip not in WHITELISTED_IPS:
                    self.write_to_pitfalls(
                        f"新 IP {self.current_ip} 不在白名单",
                        "请在币安后台添加此 IP 到白名单"
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
        status['current_ip'] = self.current_ip
        status['last_ip'] = self.last_ip
        status['whitelisted'] = self.current_ip in WHITELISTED_IPS if self.current_ip else False
        return status

if __name__ == '__main__':
    monitor = IPSelfEvolvingMonitor()
    result = monitor.execute()
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🌐 IP 监控自进化智能体")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"当前 IP: {monitor.current_ip}")
    print(f"上次 IP: {monitor.last_ip}")
    print(f"在白名单：{'✅' if monitor.current_ip in WHITELISTED_IPS else '⚠️'}")
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
    print(f"  学习模式：{monitor.metrics.learned_patterns}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
