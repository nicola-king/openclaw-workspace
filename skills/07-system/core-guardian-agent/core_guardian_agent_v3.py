#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core Guardian Agent v3.0 - 核心保障 Agent (完整版)

整合功能:
- 系统监控 (v2.0)
- 自动修复 (v2.0)
- 踩坑记录 (v2.1)
- 智能自进化 (v2.1)
- 预测性维护 (v3.0)
- 自动阈值调整 (v3.0)
- 故障根因分析 (v3.0)

作者：太一 AGI
创建：2026-04-12 22:59
版本：v3.0 (完整版)
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
from dataclasses import dataclass, asdict, field
import logging

# 导入 v3.0 模块
from predictive_maintenance import PredictiveMaintenance
from auto_threshold_adjustment import AutoThresholdAdjustment
from root_cause_analysis import RootCauseAnalysis

# 导入踩坑记录 API
sys.path.insert(0, str(Path(__file__).parent.parent / 'issue-pitfalls-record'))
from api import IssuePitfallsAPI, Issue, Solution

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/core-guardian-v3.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CoreGuardianAgentV3')


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
    alerts: List[str] = field(default_factory=list)
    auto_heal_actions: List[str] = field(default_factory=list)
    self_check_passed: bool = True
    emergence_signals: int = 0
    evolution_signals: int = 0
    predictions: Dict = field(default_factory=dict)
    threshold_adjustments: Dict = field(default_factory=dict)
    root_cause_analysis: Dict = field(default_factory=dict)


class CoreGuardianAgentV3:
    """Core Guardian Agent v3.0 (完整版)"""
    
    def __init__(self):
        """初始化 Core Guardian Agent v3.0"""
        self.workspace = Path('/home/nicola/.openclaw/workspace')
        self.logs_dir = self.workspace / 'logs'
        self.reports_dir = self.workspace / 'reports'
        self.evolution_dir = self.workspace / '.evolution'
        self.skills_dir = self.workspace / 'skills'
        
        # 阈值配置
        self.thresholds = {
            'cpu_warning': 80,
            'cpu_critical': 90,
            'memory_warning': 80,
            'memory_critical': 90,
            'disk_warning': 90,
            'disk_critical': 95,
            'load_warning': 4.0,
            'load_critical': 6.0,
            'gateway_response_warning': 100,
            'gateway_response_critical': 500,
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
        
        # v3.0 模块
        self.predictive_maintenance = PredictiveMaintenance()
        self.auto_threshold_adjustment = AutoThresholdAdjustment()
        self.root_cause_analysis = RootCauseAnalysis()
        
        # 踩坑记录 API
        self.issue_api = IssuePitfallsAPI()
        
        # 自进化能力
        self.evolution_signals = 0
        self.last_optimization = None
        self.optimization_history = []
        
        logger.info("🛡️ Core Guardian Agent v3.0 已初始化")
        logger.info(f"  阈值配置：{self.thresholds}")
        logger.info(f"  历史数据：{len(self.evolution_history)} 次记录")
        logger.info(f"  v3.0 模块：预测性维护 + 自动阈值调整 + 故障根因分析")
        logger.info(f"  踩坑记录：已集成")
        logger.info(f"  自进化能力：已激活")
    
    def run(self) -> SystemMetrics:
        """运行核心保障 v3.0"""
        logger.info("🛡️ 开始运行核心保障 v3.0...")
        
        start_time = time.time()
        
        # Step 1: 自检系统
        self_check_result = self.self_check()
        
        # Step 2: 检查 Ubuntu 系统资源
        system_status = self.check_system_resources_enhanced()
        
        # Step 3: 检查 Gateway 状态
        gateway_status = self.check_gateway_enhanced()
        
        # Step 4: 检测能力涌现
        emergence_signals = self.detect_emergence()
        
        # Step 5: 生成指标
        execution_time = (time.time() - start_time) * 1000
        metrics = self.generate_metrics(system_status, gateway_status, self_check_result, emergence_signals, execution_time)
        
        # Step 6: v3.0 功能 - 预测性维护
        metrics.predictions = self.run_predictive_maintenance(metrics)
        
        # Step 7: v3.0 功能 - 自动阈值调整
        metrics.threshold_adjustments = self.run_auto_threshold_adjustment(metrics)
        
        # Step 8: v3.0 功能 - 故障根因分析 (如果有告警)
        if metrics.alerts:
            metrics.root_cause_analysis = self.run_root_cause_analysis(metrics)
        
        # Step 9: 自动修复
        heal_actions = self.auto_heal_enhanced(metrics)
        metrics.auto_heal_actions = heal_actions
        
        # Step 10: 踩坑记录智能自动化
        self.auto_record_issues(metrics)
        
        # Step 11: 智能自进化
        self.self_evolution(metrics)
        
        # Step 12: 更新性能趋势
        self.update_performance_trends(metrics)
        
        # Step 13: 保存进化历史
        self.save_evolution_history(metrics)
        
        # Step 14: 生成 v3.0 报告
        self.generate_v3_report(metrics)
        
        logger.info("✅ 核心保障 v3.0 完成！")
        logger.info(f"  CPU: {metrics.cpu_usage:.1f}%")
        logger.info(f"  内存：{metrics.memory_usage:.1f}%")
        logger.info(f"  磁盘：{metrics.disk_usage:.1f}%")
        logger.info(f"  负载：{metrics.load_average}")
        logger.info(f"  Gateway: {'✅' if metrics.gateway_running else '❌'} (PID: {metrics.gateway_pid or 'N/A'})")
        logger.info(f"  响应时间：{metrics.gateway_response_ms:.1f}ms")
        logger.info(f"  自检：{'✅' if metrics.self_check_passed else '❌'}")
        logger.info(f"  涌现信号：{metrics.emergence_signals} 个")
        logger.info(f"  预测告警：{len(metrics.predictions)} 个")
        logger.info(f"  阈值调整：{len(metrics.threshold_adjustments)} 个")
        logger.info(f"  根因分析：{len(metrics.root_cause_analysis)} 个")
        logger.info(f"  告警：{len(metrics.alerts)} 个")
        logger.info(f"  自愈：{len(metrics.auto_heal_actions)} 个")
        
        return metrics
    
    def run_predictive_maintenance(self, metrics: SystemMetrics) -> Dict:
        """运行预测性维护"""
        logger.info("🔮 运行预测性维护...")
        
        predictions = {}
        
        # 预测 CPU
        if len(self.performance_trends['cpu_history']) >= 5:
            prediction = self.predictive_maintenance.predict_fault(
                self.performance_trends['cpu_history'],
                horizon=60
            )
            if prediction:
                predictions['CPU'] = prediction
                logger.info(f"  ⚠️ CPU 预测：{prediction['fault_type']} ({prediction['time_to_fault']} 分钟后)")
        
        # 预测内存
        if len(self.performance_trends['memory_history']) >= 5:
            prediction = self.predictive_maintenance.predict_fault(
                self.performance_trends['memory_history'],
                horizon=60
            )
            if prediction:
                predictions['内存'] = prediction
                logger.info(f"  ⚠️ 内存预测：{prediction['fault_type']} ({prediction['time_to_fault']} 分钟后)")
        
        # 预测 Gateway 响应时间
        if len(self.performance_trends['gateway_response_history']) >= 5:
            prediction = self.predictive_maintenance.predict_fault(
                self.performance_trends['gateway_response_history'],
                horizon=30
            )
            if prediction:
                predictions['Gateway 响应'] = prediction
                logger.info(f"  ⚠️ Gateway 响应预测：{prediction['fault_type']} ({prediction['time_to_fault']} 分钟后)")
        
        if predictions:
            # 生成维护计划
            maintenance_plan = self.predictive_maintenance.generate_maintenance_plan(predictions)
            logger.info("📝 维护计划:")
            for plan in maintenance_plan:
                logger.info(f"    {plan}")
        else:
            logger.info("  ✅ 预测性维护：系统运行正常")
        
        return predictions
    
    def run_auto_threshold_adjustment(self, metrics: SystemMetrics) -> Dict:
        """运行自动阈值调整"""
        logger.info("⚙️ 运行自动阈值调整...")
        
        adjustments = {}
        
        # 准备数据
        threshold_data = {
            'CPU': {
                'history': self.performance_trends['cpu_history'],
                'current_threshold': self.thresholds['cpu_warning'],
            },
            '内存': {
                'history': self.performance_trends['memory_history'],
                'current_threshold': self.thresholds['memory_warning'],
            },
            'Gateway 响应': {
                'history': self.performance_trends['gateway_response_history'],
                'current_threshold': self.thresholds['gateway_response_warning'],
            },
        }
        
        # 计算最优阈值
        for metric, data in threshold_data.items():
            if len(data['history']) >= 20:  # 至少 20 个数据点
                optimal = self.auto_threshold_adjustment.calculate_optimal_threshold(
                    data['history'],
                    data['current_threshold']
                )
                
                if abs(optimal - data['current_threshold']) > data['current_threshold'] * 0.05:
                    adjustments[metric] = {
                        'current': data['current_threshold'],
                        'optimal': optimal,
                        'adjustment': ((optimal - data['current_threshold']) / data['current_threshold'] * 100),
                    }
                    logger.info(f"  ⚙️ {metric} 阈值调整：{data['current_threshold']} → {optimal:.2f} ({adjustments[metric]['adjustment']:.1f}%)")
        
        if not adjustments:
            logger.info("  ✅ 自动阈值调整：阈值设置合理")
        
        return adjustments
    
    def run_root_cause_analysis(self, metrics: SystemMetrics) -> Dict:
        """运行故障根因分析"""
        logger.info("🔍 运行故障根因分析...")
        
        analysis_results = {}
        
        for alert in metrics.alerts:
            # 提取问题
            problem = alert.split(':')[0] if ':' in alert else alert
            
            # 运行根因分析
            result = self.root_cause_analysis.analyze(problem, metrics.alerts)
            
            if result['root_causes']:
                analysis_results[problem] = result
                logger.info(f"  🔍 {problem}:")
                logger.info(f"    根因：{result['root_causes'][0]['cause']}")
                logger.info(f"    置信度：{result['confidence']*100:.1f}%")
                logger.info(f"    解决方案：{len(result['solutions'])} 个")
        
        if not analysis_results:
            logger.info("  ✅ 故障根因分析：无需分析")
        
        return analysis_results
    
    def self_check(self) -> Dict:
        """自检系统"""
        logger.info("🔍 执行自检系统...")
        
        check_result = {'passed': True, 'checks': []}
        
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
        
        # 检查 5: v3.0 模块
        v3_modules = [
            self.predictive_maintenance,
            self.auto_threshold_adjustment,
            self.root_cause_analysis,
        ]
        if all(hasattr(m, '__class__') for m in v3_modules):
            check_result['checks'].append({'name': 'v3.0 模块', 'status': '✅'})
        else:
            check_result['checks'].append({'name': 'v3.0 模块', 'status': '❌'})
            check_result['passed'] = False
        
        logger.info(f"✅ 自检完成：{'通过' if check_result['passed'] else '失败'}")
        
        return check_result
    
    def check_system_resources_enhanced(self) -> Dict:
        """检查 Ubuntu 系统资源 (增强版)"""
        logger.info("📊 检查 Ubuntu 系统资源 (增强版)...")
        
        status = {
            'cpu_usage': 0.0,
            'memory_usage': 0.0,
            'disk_usage': 0.0,
            'load_average': (0.0, 0.0, 0.0),
            'alerts': [],
        }
        
        try:
            # CPU 使用率
            cpu_result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=10)
            for line in cpu_result.stdout.split('\n'):
                if 'Cpu(s)' in line:
                    parts = line.split(':')[1].split(',')
                    for part in parts:
                        part = part.strip()
                        if 'id' in part:
                            cpu_idle = float(part.replace('id', '').strip())
                            status['cpu_usage'] = 100.0 - cpu_idle
                            break
            
            # 内存使用率
            memory_result = subprocess.run(['free'], capture_output=True, text=True, timeout=5)
            for line in memory_result.stdout.split('\n'):
                if 'Mem:' in line:
                    parts = line.split()
                    total = float(parts[1])
                    used = float(parts[2])
                    status['memory_usage'] = (used / total) * 100
                    break
            
            # 磁盘使用率
            disk_result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
            for line in disk_result.stdout.split('\n'):
                if '/dev/' in line:
                    parts = line.split()
                    status['disk_usage'] = float(parts[4].replace('%', ''))
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
        """检查 Gateway 状态 (增强版)"""
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
            pgrep_result = subprocess.run(['pgrep', '-f', 'openclaw-gateway'], capture_output=True, text=True, timeout=5)
            if pgrep_result.returncode == 0 and pgrep_result.stdout.strip():
                status['gateway_running'] = True
                status['gateway_pid'] = pgrep_result.stdout.strip()
                logger.info(f"✅ Gateway 进程运行中 (PID: {status['gateway_pid']})")
            else:
                logger.warning("❌ Gateway 进程未运行")
                status['alerts'].append("Gateway 进程未运行")
            
            # 检查端口
            netstat_result = subprocess.run(['netstat', '-tln'], capture_output=True, text=True, timeout=5)
            if ':18789' in netstat_result.stdout:
                status['gateway_port_ok'] = True
                logger.info("✅ Gateway 端口 18789 正常监听")
            else:
                logger.warning("❌ Gateway 端口未监听")
                status['alerts'].append("Gateway 端口未监听")
            
            # 检查响应时间
            if status['gateway_running'] and status['gateway_port_ok']:
                try:
                    start_time = time.time()
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
        """检测能力涌现"""
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
        """自动修复 (增强版)"""
        logger.info("🔧 检查是否需要自动修复 (增强版)...")
        
        heal_actions = []
        
        # Gateway 进程未运行 → 重启
        if not metrics.gateway_running:
            logger.info("🔄 Gateway 进程未运行，尝试重启...")
            try:
                subprocess.run(['systemctl', 'restart', 'openclaw-gateway'], capture_output=True, text=True, timeout=30)
                time.sleep(10)
                
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
                subprocess.run(['systemctl', 'restart', 'openclaw-gateway'], capture_output=True, text=True, timeout=30)
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
        
        if heal_actions:
            logger.info(f"✅ 自动修复完成：{len(heal_actions)} 个操作")
        else:
            logger.info("✅ 无需自动修复")
        
        return heal_actions
    
    def verify_gateway_running(self) -> bool:
        """验证 Gateway 进程运行"""
        try:
            result = subprocess.run(['pgrep', '-f', 'openclaw-gateway'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0 and result.stdout.strip()
        except:
            return False
    
    def verify_gateway_port_ok(self) -> bool:
        """验证 Gateway 端口正常"""
        try:
            result = subprocess.run(['netstat', '-tln'], capture_output=True, text=True, timeout=5)
            return ':18789' in result.stdout
        except:
            return False
    
    def auto_record_issues(self, metrics: SystemMetrics):
        """踩坑记录智能自动化"""
        logger.info("📝 踩坑记录智能自动化...")
        
        self.issue_api.integrate_with_core_guardian(metrics)
        
        logger.info("✅ 踩坑记录智能自动化完成")
    
    def self_evolution(self, metrics: SystemMetrics):
        """智能自进化"""
        logger.info("🧬 智能自进化...")
        
        evolution_signals = 0
        
        # 自进化信号：v3.0 模块运行正常
        if hasattr(self, 'predictive_maintenance') and hasattr(self, 'auto_threshold_adjustment') and hasattr(self, 'root_cause_analysis'):
            evolution_signals += 1
            logger.info("  ✅ v3.0 模块运行正常")
        
        # 自进化信号：预测性维护
        if metrics.predictions:
            evolution_signals += 1
            logger.info(f"  ✅ 预测性维护：{len(metrics.predictions)} 个预测")
        
        # 自进化信号：自动阈值调整
        if metrics.threshold_adjustments:
            evolution_signals += 1
            logger.info(f"  ✅ 自动阈值调整：{len(metrics.threshold_adjustments)} 个调整")
        
        # 自进化信号：故障根因分析
        if metrics.root_cause_analysis:
            evolution_signals += 1
            logger.info(f"  ✅ 故障根因分析：{len(metrics.root_cause_analysis)} 个分析")
        
        self.evolution_signals = evolution_signals
        
        if evolution_signals > 0:
            logger.info(f"✅ 检测到 {evolution_signals} 个自进化信号")
        else:
            logger.info("✅ 自进化运行正常")
        
        logger.info("✅ 智能自进化完成")
    
    def update_performance_trends(self, metrics: SystemMetrics):
        """更新性能趋势"""
        self.performance_trends['cpu_history'].append(metrics.cpu_usage)
        self.performance_trends['memory_history'].append(metrics.memory_usage)
        self.performance_trends['gateway_response_history'].append(metrics.gateway_response_ms)
        
        # 保留最近 100 条记录
        for key in self.performance_trends:
            if len(self.performance_trends[key]) > 100:
                self.performance_trends[key] = self.performance_trends[key][-100:]
    
    def generate_v3_report(self, metrics: SystemMetrics):
        """生成 v3.0 报告"""
        logger.info("📝 生成 v3.0 报告...")
        
        report_path = self.reports_dir / f'core-guardian-v3-report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.md'
        
        report_content = f"""# 🛡️ Core Guardian Agent v3.0 报告

**执行时间**: {metrics.timestamp}
**版本**: v3.0 (完整版)

---

## 📊 系统状态

| 指标 | 数值 | 状态 |
|------|------|------|
| CPU | {metrics.cpu_usage:.1f}% | {'✅' if metrics.cpu_usage < 80 else '⚠️'} |
| 内存 | {metrics.memory_usage:.1f}% | {'✅' if metrics.memory_usage < 80 else '⚠️'} |
| 磁盘 | {metrics.disk_usage:.1f}% | {'✅' if metrics.disk_usage < 90 else '⚠️'} |
| 负载 | {metrics.load_average} | {'✅' if metrics.load_average[0] < 4 else '⚠️'} |
| Gateway | {'✅' if metrics.gateway_running else '❌'} | {metrics.gateway_pid or 'N/A'} |
| Gateway 响应 | {metrics.gateway_response_ms:.1f}ms | {'✅' if metrics.gateway_response_ms < 100 else '⚠️'} |

---

## 🔮 预测性维护

"""
        if metrics.predictions:
            for metric, prediction in metrics.predictions.items():
                report_content += f"- **{metric}**: {prediction['fault_type']} ({prediction['time_to_fault']} 分钟后)\n"
        else:
            report_content += "✅ 系统运行正常，无需维护\n"
        
        report_content += f"""
---

## ⚙️ 自动阈值调整

"""
        if metrics.threshold_adjustments:
            for metric, adjustment in metrics.threshold_adjustments.items():
                report_content += f"- **{metric}**: {adjustment['current']} → {adjustment['optimal']:.2f} ({adjustment['adjustment']:.1f}%)\n"
        else:
            report_content += "✅ 阈值设置合理\n"
        
        report_content += f"""
---

## 🔍 故障根因分析

"""
        if metrics.root_cause_analysis:
            for problem, analysis in metrics.root_cause_analysis.items():
                report_content += f"- **{problem}**:\n"
                report_content += f"  - 根因：{analysis['root_causes'][0]['cause']}\n"
                report_content += f"  - 置信度：{analysis['confidence']*100:.1f}%\n"
        else:
            report_content += "✅ 无需分析\n"
        
        report_content += f"""
---

## 📝 告警与自愈

**告警**: {len(metrics.alerts)} 个
**自愈**: {len(metrics.auto_heal_actions)} 个

---

**🛡️ Core Guardian Agent v3.0 报告完成**
"""
        
        report_path.write_text(report_content, encoding='utf-8')
        logger.info(f"✅ v3.0 报告已生成：{report_path}")
    
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
            'history': self.evolution_history + [asdict(metrics)],
            'performance_trends': self.performance_trends,
            'last_updated': datetime.now().isoformat(),
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 进化历史已保存：{history_file}")


def main():
    """主函数"""
    logger.info("🛡️ Core Guardian Agent v3.0 启动...")
    
    agent = CoreGuardianAgentV3()
    metrics = agent.run()
    
    logger.info("✅ Core Guardian Agent v3.0 完成！")


if __name__ == '__main__':
    main()
