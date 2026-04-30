#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core Guardian Agent - 核心保障 Agent

融合:
- Ubuntu 系统监控
- Gateway 健康检查
- 自动故障修复
- 自检自愈循环
- 告警通知
- 自进化能力

作者：太一 AGI
创建：2026-04-12
版本：v1.0 (P0 优先级)
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/core-guardian.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CoreGuardianAgent')


@dataclass
class SystemMetrics:
    """系统指标"""
    timestamp: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    gateway_running: bool
    gateway_port_ok: bool
    alerts: List[str]
    auto_heal_actions: List[str]


class CoreGuardianAgent:
    """核心保障 Agent"""
    
    def __init__(self):
        """初始化核心保障 Agent"""
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.logs_dir = self.workspace / 'logs'
        self.reports_dir = self.workspace / 'reports'
        self.evolution_dir = self.workspace / '.evolution'
        
        # 阈值配置
        self.thresholds = {
            'cpu_warning': 80,
            'cpu_critical': 90,
            'memory_warning': 80,
            'memory_critical': 90,
            'disk_warning': 90,
            'disk_critical': 95,
        }
        
        # 进化历史
        self.evolution_history = []
        self.load_evolution_history()
        
        logger.info("🛡️ Core Guardian Agent 已初始化")
        logger.info(f"  阈值配置：{self.thresholds}")
        logger.info(f"  历史数据：{len(self.evolution_history)} 次记录")
    
    def run(self) -> SystemMetrics:
        """运行核心保障"""
        logger.info("🛡️ 开始运行核心保障...")
        
        # Step 1: 检查 Ubuntu 系统资源
        system_status = self.check_system_resources()
        
        # Step 2: 检查 Gateway 状态
        gateway_status = self.check_gateway()
        
        # Step 3: 生成指标
        metrics = self.generate_metrics(system_status, gateway_status)
        
        # Step 4: 自动修复 (如果需要)
        heal_actions = self.auto_heal(metrics)
        metrics.auto_heal_actions = heal_actions
        
        # Step 5: 发送告警 (如果需要)
        self.send_alerts(metrics)
        
        # Step 6: 保存进化历史
        self.save_evolution_history(metrics)
        
        logger.info("✅ 核心保障完成！")
        logger.info(f"  CPU: {metrics.cpu_usage:.1f}%")
        logger.info(f"  内存：{metrics.memory_usage:.1f}%")
        logger.info(f"  磁盘：{metrics.disk_usage:.1f}%")
        logger.info(f"  Gateway: {'✅' if metrics.gateway_running else '❌'}")
        logger.info(f"  告警：{len(metrics.alerts)} 个")
        logger.info(f"  自愈：{len(metrics.auto_heal_actions)} 个")
        
        return metrics
    
    def check_system_resources(self) -> Dict:
        """检查 Ubuntu 系统资源"""
        logger.info("📊 检查 Ubuntu 系统资源...")
        
        status = {
            'cpu_usage': 0.0,
            'memory_usage': 0.0,
            'disk_usage': 0.0,
            'alerts': [],
        }
        
        try:
            # CPU 使用率
            cpu_result = subprocess.run(
                ['top', '-bn1'],
                capture_output=True,
                text=True,
                timeout=10
            )
            for line in cpu_result.stdout.split('\n'):
                if 'Cpu(s)' in line:
                    cpu_usage = line.split(',')[0].split(':')[1].strip().split('%')[0]
                    status['cpu_usage'] = float(cpu_usage)
                    break
            
            # 内存使用率
            memory_result = subprocess.run(
                ['free'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in memory_result.stdout.split('\n'):
                if 'Mem:' in line:
                    parts = line.split()
                    total = float(parts[1])
                    used = float(parts[2])
                    status['memory_usage'] = (used / total) * 100
                    break
            
            # 磁盘使用率
            disk_result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in disk_result.stdout.split('\n'):
                if '/dev/' in line:
                    parts = line.split()
                    disk_usage = parts[4].replace('%', '')
                    status['disk_usage'] = float(disk_usage)
                    break
            
            # 检查阈值告警
            if status['cpu_usage'] > self.thresholds['cpu_warning']:
                status['alerts'].append(f"CPU 使用率过高：{status['cpu_usage']:.1f}%")
            
            if status['memory_usage'] > self.thresholds['memory_warning']:
                status['alerts'].append(f"内存使用率过高：{status['memory_usage']:.1f}%")
            
            if status['disk_usage'] > self.thresholds['disk_warning']:
                status['alerts'].append(f"磁盘使用率过高：{status['disk_usage']:.1f}%")
            
            logger.info(f"✅ 系统资源检查完成")
            logger.info(f"    CPU: {status['cpu_usage']:.1f}%")
            logger.info(f"    内存：{status['memory_usage']:.1f}%")
            logger.info(f"    磁盘：{status['disk_usage']:.1f}%")
            
        except Exception as e:
            logger.error(f"❌ 系统资源检查失败：{e}")
            status['alerts'].append(f"系统资源检查失败：{e}")
        
        return status
    
    def check_gateway(self) -> Dict:
        """检查 Gateway 状态"""
        logger.info("🤖 检查 Gateway 状态...")
        
        status = {
            'gateway_running': False,
            'gateway_port_ok': False,
            'gateway_pid': None,
            'alerts': [],
        }
        
        try:
            # 检查进程
            pgrep_result = subprocess.run(
                ['pgrep', '-f', 'openclaw-gateway'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if pgrep_result.returncode == 0 and pgrep_result.stdout.strip():
                status['gateway_running'] = True
                status['gateway_pid'] = pgrep_result.stdout.strip()
                logger.info(f"✅ Gateway 进程运行中 (PID: {status['gateway_pid']})")
            else:
                logger.warning("❌ Gateway 进程未运行")
                status['alerts'].append("Gateway 进程未运行")
            
            # 检查端口
            netstat_result = subprocess.run(
                ['netstat', '-tln'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if ':18789' in netstat_result.stdout:
                status['gateway_port_ok'] = True
                logger.info("✅ Gateway 端口 18789 正常监听")
            else:
                logger.warning("❌ Gateway 端口未监听")
                status['alerts'].append("Gateway 端口未监听")
            
        except Exception as e:
            logger.error(f"❌ Gateway 检查失败：{e}")
            status['alerts'].append(f"Gateway 检查失败：{e}")
        
        return status
    
    def generate_metrics(self, system_status: Dict, gateway_status: Dict) -> SystemMetrics:
        """生成系统指标"""
        alerts = system_status.get('alerts', []) + gateway_status.get('alerts', [])
        
        metrics = SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_usage=system_status.get('cpu_usage', 0.0),
            memory_usage=system_status.get('memory_usage', 0.0),
            disk_usage=system_status.get('disk_usage', 0.0),
            gateway_running=gateway_status.get('gateway_running', False),
            gateway_port_ok=gateway_status.get('gateway_port_ok', False),
            alerts=alerts,
            auto_heal_actions=[],
        )
        
        return metrics
    
    def auto_heal(self, metrics: SystemMetrics) -> List[str]:
        """自动修复"""
        logger.info("🔧 检查是否需要自动修复...")
        
        heal_actions = []
        
        # Gateway 进程未运行 → 重启
        if not metrics.gateway_running:
            logger.info("🔄 Gateway 进程未运行，尝试重启...")
            try:
                subprocess.run(
                    ['systemctl', 'restart', 'openclaw-gateway'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                time.sleep(10)  # 等待重启
                
                # 验证重启成功
                if self.verify_gateway_running():
                    heal_actions.append("Gateway 进程已重启并恢复")
                    logger.info("✅ Gateway 重启成功")
                else:
                    heal_actions.append("Gateway 重启失败，需要人工干预")
                    logger.error("❌ Gateway 重启失败")
            except Exception as e:
                heal_actions.append(f"Gateway 重启异常：{e}")
                logger.error(f"❌ Gateway 重启异常：{e}")
        
        # Gateway 端口异常 → 重启
        if metrics.gateway_running and not metrics.gateway_port_ok:
            logger.info("🔄 Gateway 端口异常，尝试重启...")
            try:
                subprocess.run(
                    ['systemctl', 'restart', 'openclaw-gateway'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                time.sleep(10)
                
                if self.verify_gateway_port_ok():
                    heal_actions.append("Gateway 端口已恢复")
                    logger.info("✅ Gateway 端口恢复成功")
                else:
                    heal_actions.append("Gateway 端口恢复失败，需要人工干预")
                    logger.error("❌ Gateway 端口恢复失败")
            except Exception as e:
                heal_actions.append(f"Gateway 端口恢复异常：{e}")
                logger.error(f"❌ Gateway 端口恢复异常：{e}")
        
        # CPU 使用率过高 → 告警
        if metrics.cpu_usage > self.thresholds['cpu_critical']:
            heal_actions.append(f"CPU 使用率过高 ({metrics.cpu_usage:.1f}%)，建议清理进程")
        
        # 内存使用率过高 → 告警
        if metrics.memory_usage > self.thresholds['memory_critical']:
            heal_actions.append(f"内存使用率过高 ({metrics.memory_usage:.1f}%)，建议清理缓存")
        
        # 磁盘使用率过高 → 清理日志
        if metrics.disk_usage > self.thresholds['disk_critical']:
            logger.info("🗑️ 磁盘使用率过高，尝试清理日志...")
            try:
                self.cleanup_old_logs()
                heal_actions.append("已清理旧日志文件")
            except Exception as e:
                heal_actions.append(f"日志清理失败：{e}")
        
        if heal_actions:
            logger.info(f"✅ 自动修复完成：{len(heal_actions)} 个操作")
        else:
            logger.info("✅ 无需自动修复")
        
        return heal_actions
    
    def verify_gateway_running(self) -> bool:
        """验证 Gateway 进程运行"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'openclaw-gateway'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0 and result.stdout.strip()
        except:
            return False
    
    def verify_gateway_port_ok(self) -> bool:
        """验证 Gateway 端口正常"""
        try:
            result = subprocess.run(
                ['netstat', '-tln'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return ':18789' in result.stdout
        except:
            return False
    
    def cleanup_old_logs(self):
        """清理旧日志文件"""
        # 清理 30 天前的日志
        logs_dir = self.workspace / 'logs'
        if logs_dir.exists():
            for log_file in logs_dir.glob('*.log.*'):
                if log_file.stat().st_mtime < (time.time() - 30 * 24 * 3600):
                    log_file.unlink()
                    logger.info(f"🗑️ 清理旧日志：{log_file.name}")
    
    def send_alerts(self, metrics: SystemMetrics):
        """发送告警"""
        if not metrics.alerts and not metrics.auto_heal_actions:
            return
        
        logger.info("🚨 发送告警...")
        
        # 构建告警消息
        alert_message = f"""🛡️ Core Guardian 告警

时间：{metrics.timestamp}

系统状态:
- CPU: {metrics.cpu_usage:.1f}%
- 内存：{metrics.memory_usage:.1f}%
- 磁盘：{metrics.disk_usage:.1f}%
- Gateway: {'✅' if metrics.gateway_running else '❌'}

告警：{len(metrics.alerts)} 个
"""
        for alert in metrics.alerts:
            alert_message += f"- {alert}\n"
        
        if metrics.auto_heal_actions:
            alert_message += f"\n自愈操作：{len(metrics.auto_heal_actions)} 个\n"
            for action in metrics.auto_heal_actions:
                alert_message += f"- {action}\n"
        
        logger.info(f"🚨 告警消息:\n{alert_message}")
        
        # TODO: 实现 Telegram/邮件告警
        # 目前只记录日志
    
    def load_evolution_history(self):
        """加载进化历史"""
        history_file = self.evolution_dir / 'core-guardian_history.json'
        
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.evolution_history = data.get('history', [])
                    logger.info(f"  加载进化历史：{len(self.evolution_history)} 次记录")
            except Exception as e:
                logger.warning(f"  加载进化历史失败：{e}")
                self.evolution_history = []
        else:
            logger.info("  无进化历史，从头开始")
            self.evolution_history = []
    
    def save_evolution_history(self, metrics: SystemMetrics):
        """保存进化历史"""
        self.evolution_dir.mkdir(parents=True, exist_ok=True)
        history_file = self.evolution_dir / 'core-guardian_history.json'
        
        history_data = {
            'history': self.evolution_history + [{
                'timestamp': metrics.timestamp,
                'cpu_usage': metrics.cpu_usage,
                'memory_usage': metrics.memory_usage,
                'disk_usage': metrics.disk_usage,
                'gateway_running': metrics.gateway_running,
                'gateway_port_ok': metrics.gateway_port_ok,
                'alerts': metrics.alerts,
                'auto_heal_actions': metrics.auto_heal_actions,
            }],
            'last_updated': datetime.now().isoformat(),
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 进化历史已保存：{history_file}")


def main():
    """主函数"""
    logger.info("🛡️ Core Guardian Agent 启动...")
    
    agent = CoreGuardianAgent()
    metrics = agent.run()
    
    logger.info("✅ Core Guardian Agent 完成！")


if __name__ == '__main__':
    main()
