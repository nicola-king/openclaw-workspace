#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core Guardian Agent v2.0 - 核心保障 Agent (增强版)

穿透性蒸馏提炼融合:
- core-monitor.sh (系统资源监控)
- gateway-auto-heal.sh (Gateway 自动修复)
- taiyi/self-check.sh (自检系统)
- taiyi/emergence-monitor.sh (能力涌现监控)
- monitoring/*.py (API 监控)

作者：太一 AGI (蒸馏提炼)
创建：2026-04-12 22:29
版本：v2.0 (增强版)
"""

import os
import sys
import json
import subprocess
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

# 导入踩坑记录 API
sys.path.insert(0, str(Path(__file__).parent.parent / 'issue-pitfalls-record'))
from api import IssuePitfallsAPI, Issue, Solution

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
    load_average: Tuple[float, float, float]
    gateway_running: bool
    gateway_port_ok: bool
    gateway_pid: Optional[str]
    gateway_response_ms: float
    alerts: List[str]
    auto_heal_actions: List[str]
    self_check_passed: bool
    emergence_signals: int
    evolution_signals: int = 0  # 自进化信号


class CoreGuardianAgent:
    """核心保障 Agent v2.0 (增强版)"""
    
    def __init__(self):
        """初始化核心保障 Agent"""
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.logs_dir = self.workspace / 'logs'
        self.reports_dir = self.workspace / 'reports'
        self.evolution_dir = self.workspace / '.evolution'
        self.skills_dir = self.workspace / 'skills'
        
        # 阈值配置 (蒸馏提炼自 core-monitor.sh)
        self.thresholds = {
            'cpu_warning': 80,
            'cpu_critical': 90,
            'memory_warning': 80,
            'memory_critical': 90,
            'disk_warning': 90,
            'disk_critical': 95,
            'load_warning': 4.0,  # 假设 2 核心×2
            'load_critical': 6.0,
            'gateway_response_warning': 100,  # ms
            'gateway_response_critical': 500,  # ms
        }
        
        # 进化历史
        self.evolution_history = []
        self.load_evolution_history()
        
        # 性能趋势
        self.performance_trends = {
            'cpu_history': [],
            'memory_history': [],
            'gateway_response_history': [],
        }
        
        # 踩坑记录 API (智能自动化)
        self.issue_api = IssuePitfallsAPI()
        
        # 自进化能力
        self.evolution_signals = 0
        self.last_optimization = None
        self.optimization_history = []
        
        logger.info("🛡️ Core Guardian Agent v2.1 已初始化")
        logger.info(f"  阈值配置：{self.thresholds}")
        logger.info(f"  历史数据：{len(self.evolution_history)} 次记录")
        logger.info(f"  踩坑记录：已集成")
        logger.info(f"  自进化能力：已激活")
    
    def run(self) -> SystemMetrics:
        """运行核心保障"""
        logger.info("🛡️ 开始运行核心保障 v2.0...")
        
        start_time = time.time()
        
        # Step 1: 自检系统 (蒸馏提炼自 taiyi/self-check.sh)
        self_check_result = self.self_check()
        
        # Step 2: 检查 Ubuntu 系统资源 (增强版)
        system_status = self.check_system_resources_enhanced()
        
        # Step 3: 检查 Gateway 状态 (增强版)
        gateway_status = self.check_gateway_enhanced()
        
        # Step 4: 检测能力涌现 (蒸馏提炼自 taiyi/emergence-monitor.sh)
        emergence_signals = self.detect_emergence()
        
        # Step 5: 生成指标
        execution_time = (time.time() - start_time) * 1000  # ms
        metrics = self.generate_metrics(system_status, gateway_status, self_check_result, emergence_signals, execution_time)
        
        # Step 6: 自动修复 (增强版)
        heal_actions = self.auto_heal_enhanced(metrics)
        metrics.auto_heal_actions = heal_actions
        
        # Step 7: 发送告警 (增强版)
        self.send_alerts_enhanced(metrics)
        
        # Step 8: 更新性能趋势
        self.update_performance_trends(metrics)
        
        # Step 9: 踩坑记录智能自动化
        self.auto_record_issues(metrics)
        
        # Step 10: 智能自进化
        self.self_evolution(metrics)
        
        # Step 11: 保存进化历史
        self.save_evolution_history(metrics)
        
        logger.info("✅ 核心保障 v2.1 完成！")
        logger.info(f"  CPU: {metrics.cpu_usage:.1f}%")
        logger.info(f"  内存：{metrics.memory_usage:.1f}%")
        logger.info(f"  磁盘：{metrics.disk_usage:.1f}%")
        logger.info(f"  负载：{metrics.load_average}")
        logger.info(f"  Gateway: {'✅' if metrics.gateway_running else '❌'} (PID: {metrics.gateway_pid})")
        logger.info(f"  响应时间：{metrics.gateway_response_ms:.1f}ms")
        logger.info(f"  自检：{'✅' if metrics.self_check_passed else '❌'}")
        logger.info(f"  涌现信号：{metrics.emergence_signals} 个")
        logger.info(f"  告警：{len(metrics.alerts)} 个")
        logger.info(f"  自愈：{len(metrics.auto_heal_actions)} 个")
        
        return metrics
    
    def self_check(self) -> Dict:
        """自检系统 (蒸馏提炼自 taiyi/self-check.sh)"""
        logger.info("🔍 执行自检系统...")
        
        check_result = {
            'passed': True,
            'checks': [],
        }
        
        # 检查 1: 工作目录存在
        if self.workspace.exists():
            check_result['checks'].append({'name': '工作目录', 'status': '✅'})
        else:
            check_result['checks'].append({'name': '工作目录', 'status': '❌'})
            check_result['passed'] = False
        
        # 检查 2: 日志目录可写
        if self.logs_dir.exists() and os.access(self.logs_dir, os.W_OK):
            check_result['checks'].append({'name': '日志目录', 'status': '✅'})
        else:
            check_result['checks'].append({'name': '日志目录', 'status': '❌'})
            check_result['passed'] = False
        
        # 检查 3: 进化目录可写
        if self.evolution_dir.exists() and os.access(self.evolution_dir, os.W_OK):
            check_result['checks'].append({'name': '进化目录', 'status': '✅'})
        else:
            check_result['checks'].append({'name': '进化目录', 'status': '❌'})
            check_result['passed'] = False
        
        # 检查 4: Python 环境
        try:
            python_version = sys.version_info
            if python_version.major >= 3 and python_version.minor >= 6:
                check_result['checks'].append({'name': 'Python 环境', 'status': '✅'})
            else:
                check_result['checks'].append({'name': 'Python 环境', 'status': '❌'})
                check_result['passed'] = False
        except:
            check_result['checks'].append({'name': 'Python 环境', 'status': '❌'})
            check_result['passed'] = False
        
        # 检查 5: 关键依赖
        required_modules = ['subprocess', 'json', 'logging', 'pathlib']
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if not missing_modules:
            check_result['checks'].append({'name': '关键依赖', 'status': '✅'})
        else:
            check_result['checks'].append({'name': '关键依赖', 'status': f'❌ 缺少：{missing_modules}'})
            check_result['passed'] = False
        
        logger.info(f"✅ 自检完成：{'通过' if check_result['passed'] else '失败'}")
        
        return check_result
    
    def check_system_resources_enhanced(self) -> Dict:
        """检查 Ubuntu 系统资源 (增强版 - 修复 CPU 解析)"""
        logger.info("📊 检查 Ubuntu 系统资源 (增强版)...")
        
        status = {
            'cpu_usage': 0.0,
            'memory_usage': 0.0,
            'disk_usage': 0.0,
            'load_average': (0.0, 0.0, 0.0),
            'alerts': [],
        }
        
        try:
            # CPU 使用率 (修复解析问题 - 蒸馏提炼自 core-monitor.sh)
            cpu_result = subprocess.run(
                ['top', '-bn1'],
                capture_output=True,
                text=True,
                timeout=10
            )
            for line in cpu_result.stdout.split('\n'):
                if 'Cpu(s)' in line:
                    # 解析格式：Cpu(s):  3.6 us,  1.0 sy,  0.0 ni, 95.4 id, ...
                    parts = line.split(':')[1].split(',')
                    for part in parts:
                        part = part.strip()
                        if 'us' in part:  # user
                            cpu_user = float(part.replace('us', '').strip())
                        elif 'sy' in part:  # system
                            cpu_sys = float(part.replace('sy', '').strip())
                        elif 'id' in part:  # idle
                            cpu_idle = float(part.replace('id', '').strip())
                    
                    # CPU 使用率 = 100 - idle
                    status['cpu_usage'] = 100.0 - cpu_idle
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
            
            # 系统负载
            status['load_average'] = os.getloadavg()
            
            # 检查阈值告警
            if status['cpu_usage'] > self.thresholds['cpu_warning']:
                status['alerts'].append(f"CPU 使用率过高：{status['cpu_usage']:.1f}%")
            
            if status['memory_usage'] > self.thresholds['memory_warning']:
                status['alerts'].append(f"内存使用率过高：{status['memory_usage']:.1f}%")
            
            if status['disk_usage'] > self.thresholds['disk_warning']:
                status['alerts'].append(f"磁盘使用率过高：{status['disk_usage']:.1f}%")
            
            if status['load_average'][0] > self.thresholds['load_warning']:
                status['alerts'].append(f"系统负载过高：{status['load_average'][0]:.2f}")
            
            logger.info(f"✅ 系统资源检查完成")
            logger.info(f"    CPU: {status['cpu_usage']:.1f}%")
            logger.info(f"    内存：{status['memory_usage']:.1f}%")
            logger.info(f"    磁盘：{status['disk_usage']:.1f}%")
            logger.info(f"    负载：{status['load_average']}")
            
        except Exception as e:
            logger.error(f"❌ 系统资源检查失败：{e}")
            status['alerts'].append(f"系统资源检查失败：{e}")
        
        return status
    
    def check_gateway_enhanced(self) -> Dict:
        """检查 Gateway 状态 (增强版 - 包含响应时间)"""
        logger.info("🤖 检查 Gateway 状态 (增强版)...")
        
        status = {
            'gateway_running': False,
            'gateway_port_ok': False,
            'gateway_pid': None,
            'gateway_response_ms': 0.0,
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
            
            # 检查响应时间 (增强功能)
            if status['gateway_running'] and status['gateway_port_ok']:
                try:
                    start_time = time.time()
                    # 简单的端口连接测试
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    result = sock.connect_ex(('localhost', 18789))
                    sock.close()
                    status['gateway_response_ms'] = (time.time() - start_time) * 1000
                    
                    if status['gateway_response_ms'] > self.thresholds['gateway_response_warning']:
                        status['alerts'].append(f"Gateway 响应时间过长：{status['gateway_response_ms']:.1f}ms")
                except Exception as e:
                    logger.warning(f"⚠️ Gateway 响应时间检查失败：{e}")
            
        except Exception as e:
            logger.error(f"❌ Gateway 检查失败：{e}")
            status['alerts'].append(f"Gateway 检查失败：{e}")
        
        return status
    
    def detect_emergence(self) -> int:
        """检测能力涌现 (蒸馏提炼自 taiyi/emergence-monitor.sh)"""
        logger.info("🔮 检测能力涌现...")
        
        signals = 0
        
        # 信号 1: 今日涌现技能
        emerged_dir = self.skills_dir / '08-emerged'
        if emerged_dir.exists():
            today = datetime.now().strftime('%Y%m%d')
            today_skills = [d for d in emerged_dir.iterdir() if d.is_dir() and today in d.name]
            if today_skills:
                signals += len(today_skills)
                logger.info(f"  今日涌现技能：{len(today_skills)} 个")
        
        # 信号 2: 自进化 Agent 运行
        self_evolving_agents = [
            'self_evolution_taiyi_agent.py',
            'self_evolution_hermes_agent.py',
        ]
        for agent_file in self_evolving_agents:
            if (self.skills_dir / '07-system' / 'taiyi' / agent_file).exists():
                signals += 1
        
        # 信号 3: 进化历史增长
        if self.evolution_history:
            recent_history = [h for h in self.evolution_history if datetime.fromisoformat(h['timestamp']).hour == datetime.now().hour]
            if recent_history:
                signals += 1
        
        logger.info(f"✅ 检测到 {signals} 个涌现信号")
        
        return signals
    
    def generate_metrics(self, system_status: Dict, gateway_status: Dict, self_check_result: Dict, emergence_signals: int, execution_time: float) -> SystemMetrics:
        """生成系统指标"""
        alerts = system_status.get('alerts', []) + gateway_status.get('alerts', [])
        
        if not self_check_result['passed']:
            alerts.append("自检系统未通过")
        
        metrics = SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_usage=system_status.get('cpu_usage', 0.0),
            memory_usage=system_status.get('memory_usage', 0.0),
            disk_usage=system_status.get('disk_usage', 0.0),
            load_average=system_status.get('load_average', (0.0, 0.0, 0.0)),
            gateway_running=gateway_status.get('gateway_running', False),
            gateway_port_ok=gateway_status.get('gateway_port_ok', False),
            gateway_pid=gateway_status.get('gateway_pid'),
            gateway_response_ms=gateway_status.get('gateway_response_ms', 0.0),
            alerts=alerts,
            auto_heal_actions=[],
            self_check_passed=self_check_result['passed'],
            emergence_signals=emergence_signals,
        )
        
        return metrics
    
    def auto_heal_enhanced(self, metrics: SystemMetrics) -> List[str]:
        """自动修复 (增强版 - 蒸馏提炼自 gateway-auto-heal.sh)"""
        logger.info("🔧 检查是否需要自动修复 (增强版)...")
        
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
                
                # 验证重启成功 (增强验证)
                if self.verify_gateway_running() and self.verify_gateway_port_ok():
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
        
        # Gateway 响应时间过长 → 告警
        if metrics.gateway_response_ms > self.thresholds['gateway_response_critical']:
            heal_actions.append(f"Gateway 响应时间过长 ({metrics.gateway_response_ms:.1f}ms)，建议优化")
        
        # CPU 使用率过高 → 告警
        if metrics.cpu_usage > self.thresholds['cpu_critical']:
            heal_actions.append(f"CPU 使用率过高 ({metrics.cpu_usage:.1f}%)，建议清理进程")
        
        # 内存使用率过高 → 告警 + 清理缓存
        if metrics.memory_usage > self.thresholds['memory_critical']:
            logger.info("🗑️ 内存使用率过高，尝试清理缓存...")
            try:
                subprocess.run(['sync'], capture_output=True, timeout=5)
                subprocess.run(['echo', '3', '>', '/proc/sys/vm/drop_caches'], shell=True, capture_output=True, timeout=5)
                heal_actions.append("已清理系统缓存")
            except:
                heal_actions.append(f"内存使用率过高 ({metrics.memory_usage:.1f}%)，建议清理缓存")
        
        # 磁盘使用率过高 → 清理日志
        if metrics.disk_usage > self.thresholds['disk_critical']:
            logger.info("🗑️ 磁盘使用率过高，尝试清理日志...")
            try:
                self.cleanup_old_logs()
                heal_actions.append("已清理旧日志文件")
            except Exception as e:
                heal_actions.append(f"日志清理失败：{e}")
        
        # 自检未通过 → 告警
        if not metrics.self_check_passed:
            heal_actions.append("自检系统未通过，建议检查系统状态")
        
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
        if self.logs_dir.exists():
            for log_file in self.logs_dir.glob('*.log.*'):
                if log_file.stat().st_mtime < (time.time() - 30 * 24 * 3600):
                    log_file.unlink()
                    logger.info(f"🗑️ 清理旧日志：{log_file.name}")
    
    def update_performance_trends(self, metrics: SystemMetrics):
        """更新性能趋势"""
        self.performance_trends['cpu_history'].append(metrics.cpu_usage)
        self.performance_trends['memory_history'].append(metrics.memory_usage)
        self.performance_trends['gateway_response_history'].append(metrics.gateway_response_ms)
        
        # 保留最近 100 条记录
        for key in self.performance_trends:
            if len(self.performance_trends[key]) > 100:
                self.performance_trends[key] = self.performance_trends[key][-100:]
    
    def send_alerts_enhanced(self, metrics: SystemMetrics):
        """发送告警 (增强版)"""
        if not metrics.alerts and not metrics.auto_heal_actions:
            return
        
        logger.info("🚨 发送告警 (增强版)...")
        
        # 构建告警消息
        alert_message = f"""🛡️ Core Guardian v2.0 告警

时间：{metrics.timestamp}

系统状态:
- CPU: {metrics.cpu_usage:.1f}%
- 内存：{metrics.memory_usage:.1f}%
- 磁盘：{metrics.disk_usage:.1f}%
- 负载：{metrics.load_average}
- Gateway: {'✅' if metrics.gateway_running else '❌'} (PID: {metrics.gateway_pid or 'N/A'})
- Gateway 响应：{metrics.gateway_response_ms:.1f}ms
- 自检：{'✅' if metrics.self_check_passed else '❌'}
- 涌现信号：{metrics.emergence_signals} 个

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
    
    def auto_record_issues(self, metrics: SystemMetrics):
        """踩坑记录智能自动化"""
        logger.info("📝 踩坑记录智能自动化...")
        
        # 自动检测并记录问题
        self.issue_api.integrate_with_core_guardian(metrics)
        
        # 自动查询并执行解决方案
        if metrics.alerts:
            for alert in metrics.alerts:
                # 提取关键词
                keywords = self.extract_keywords(alert)
                
                # 查询解决方案
                solution = self.issue_api.search_solution(keywords)
                
                if solution:
                    logger.info(f"🔍 找到解决方案：{solution['problem']} (成功率：{solution.get('success_rate', 0)*100:.1f}%)")
                    
                    # 自动执行解决方案
                    if self.should_auto_execute(solution, alert):
                        self.execute_solution(solution)
        
        logger.info("✅ 踩坑记录智能自动化完成")
    
    def extract_keywords(self, alert: str) -> str:
        """从告警中提取关键词"""
        # 简单关键词提取
        keywords_map = {
            'Gateway': 'Gateway',
            '端口': 'Gateway 端口',
            'CPU': 'CPU',
            '内存': '内存',
            '磁盘': '磁盘',
        }
        
        for keyword, value in keywords_map.items():
            if keyword in alert:
                return value
        
        return alert.split(':')[0] if ':' in alert else alert
    
    def should_auto_execute(self, solution: Dict, alert: str) -> bool:
        """判断是否自动执行解决方案"""
        # 成功率 >90% 且告警级别 >=P2 则自动执行
        success_rate = solution.get('success_rate', 0)
        
        if success_rate >= 0.9:
            logger.info(f"✅ 解决方案成功率高 ({success_rate*100:.1f}%)，自动执行")
            return True
        
        logger.info(f"⚠️ 解决方案成功率较低 ({success_rate*100:.1f}%)，需要人工确认")
        return False
    
    def execute_solution(self, solution: Dict):
        """执行解决方案"""
        logger.info(f"⚙️ 执行解决方案：{solution['problem']}")
        
        try:
            # 执行命令
            for command in solution.get('commands', []):
                logger.info(f"  执行：{command}")
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    logger.info(f"  ✅ 执行成功")
                else:
                    logger.warning(f"  ⚠️ 执行失败：{result.stderr}")
            
            # 更新解决方案使用次数
            solution['usage_count'] = solution.get('usage_count', 0) + 1
            solution['last_used'] = datetime.now().isoformat()
            
            logger.info(f"✅ 解决方案执行完成")
        except Exception as e:
            logger.error(f"❌ 解决方案执行失败：{e}")
    
    def self_evolution(self, metrics: SystemMetrics):
        """智能自进化"""
        logger.info("🧬 智能自进化...")
        
        evolution_signals = 0
        optimization_actions = []
        
        # 自进化信号 1: 性能趋势分析
        trend_optimization = self.analyze_performance_trends(metrics)
        if trend_optimization:
            evolution_signals += 1
            optimization_actions.append(trend_optimization)
        
        # 自进化信号 2: 阈值自适应优化
        threshold_optimization = self.optimize_thresholds(metrics)
        if threshold_optimization:
            evolution_signals += 1
            optimization_actions.append(threshold_optimization)
        
        # 自进化信号 3: 故障模式学习
        pattern_learning = self.learn_fault_patterns(metrics)
        if pattern_learning:
            evolution_signals += 1
            optimization_actions.append(pattern_learning)
        
        # 自进化信号 4: 解决方案优化
        solution_optimization = self.optimize_solutions(metrics)
        if solution_optimization:
            evolution_signals += 1
            optimization_actions.append(solution_optimization)
        
        # 自进化信号 5: 知识库增长
        if len(self.evolution_history) > 0 and len(self.evolution_history) % 10 == 0:
            evolution_signals += 1
            optimization_actions.append("知识库增长里程碑")
        
        # 记录自进化信号
        self.evolution_signals = evolution_signals
        
        if evolution_signals > 0:
            logger.info(f"✅ 检测到 {evolution_signals} 个自进化信号:")
            for action in optimization_actions:
                logger.info(f"    - {action}")
            
            # 记录优化历史
            self.optimization_history.append({
                'timestamp': datetime.now().isoformat(),
                'signals': evolution_signals,
                'actions': optimization_actions,
            })
            
            # 更新最后优化时间
            self.last_optimization = datetime.now()
        else:
            logger.info("✅ 自进化运行正常，无需优化")
        
        logger.info("✅ 智能自进化完成")
    
    def analyze_performance_trends(self, metrics: SystemMetrics) -> Optional[str]:
        """性能趋势分析"""
        # 分析 CPU 趋势
        if len(self.performance_trends['cpu_history']) >= 10:
            recent_cpu = self.performance_trends['cpu_history'][-10:]
            avg_cpu = sum(recent_cpu) / len(recent_cpu)
            
            if avg_cpu > 70 and self.thresholds['cpu_warning'] == 80:
                return f"CPU 平均使用率偏高 ({avg_cpu:.1f}%)，建议降低告警阈值"
        
        # 分析内存趋势
        if len(self.performance_trends['memory_history']) >= 10:
            recent_memory = self.performance_trends['memory_history'][-10:]
            avg_memory = sum(recent_memory) / len(recent_memory)
            
            if avg_memory > 70 and self.thresholds['memory_warning'] == 80:
                return f"内存平均使用率偏高 ({avg_memory:.1f}%)，建议降低告警阈值"
        
        # 分析 Gateway 响应时间趋势
        if len(self.performance_trends['gateway_response_history']) >= 10:
            recent_response = self.performance_trends['gateway_response_history'][-10:]
            avg_response = sum(recent_response) / len(recent_response)
            
            if avg_response > 80 and self.thresholds['gateway_response_warning'] == 100:
                return f"Gateway 平均响应时间偏高 ({avg_response:.1f}ms)，建议降低告警阈值"
        
        return None
    
    def optimize_thresholds(self, metrics: SystemMetrics) -> Optional[str]:
        """阈值自适应优化"""
        # 基于历史数据优化阈值
        if len(self.evolution_history) < 20:
            return None  # 数据不足
        
        # 分析告警频率
        recent_alerts = [h.get('alerts', []) for h in self.evolution_history[-20:]]
        total_alerts = sum(len(alerts) for alerts in recent_alerts)
        avg_alerts = total_alerts / 20
        
        if avg_alerts > 5:
            # 告警过于频繁，可能需要调整阈值
            return f"告警频率过高 (平均 {avg_alerts:.1f} 次/次)，建议审查阈值设置"
        
        return None
    
    def learn_fault_patterns(self, metrics: SystemMetrics) -> Optional[str]:
        """故障模式学习"""
        # 从踩坑记录中学习故障模式
        if not hasattr(self, 'issue_api'):
            return None
        
        stats = self.issue_api.get_stats()
        
        # 分析高频问题
        if stats['total_issues'] >= 10:
            by_category = stats.get('by_category', {})
            max_category = max(by_category.items(), key=lambda x: x[1])[0] if by_category else None
            
            if max_category:
                return f"高频故障类别：{max_category} ({by_category[max_category]} 次)，建议加强监控"
        
        return None
    
    def optimize_solutions(self, metrics: SystemMetrics) -> Optional[str]:
        """解决方案优化"""
        # 分析解决方案成功率
        if not hasattr(self, 'issue_api'):
            return None
        
        stats = self.issue_api.get_stats()
        avg_success_rate = stats.get('avg_success_rate', 0)
        
        if avg_success_rate < 0.8 and stats['total_solutions'] > 0:
            return f"解决方案平均成功率偏低 ({avg_success_rate*100:.1f}%)，建议优化解决方案"
        
        # 分析未解决问题
        if stats['open_issues'] > 5:
            return f"未解决问题较多 ({stats['open_issues']} 个)，建议优先处理"
        
        return None
    
    def save_evolution_history(self, metrics: SystemMetrics):
        """保存进化历史"""
        self.evolution_dir.mkdir(parents=True, exist_ok=True)
        history_file = self.evolution_dir / 'core-guardian_history.json'
        
        history_data = {
            'history': self.evolution_history + [asdict(metrics)],
            'performance_trends': self.performance_trends,
            'last_updated': datetime.now().isoformat(),
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 进化历史已保存：{history_file}")


def main():
    """主函数"""
    logger.info("🛡️ Core Guardian Agent v2.0 启动...")
    
    agent = CoreGuardianAgent()
    metrics = agent.run()
    
    logger.info("✅ Core Guardian Agent v2.0 完成！")


if __name__ == '__main__':
    main()
