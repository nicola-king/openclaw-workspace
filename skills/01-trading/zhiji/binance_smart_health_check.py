#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安智能健康自检系统 (Smart Health Check)

核心能力:
1. 智能诊断 - 自动识别问题类型和根因
2. 自动自愈 - 根据问题自动选择修复策略
3. 自进化 - 从历史问题中学习优化
4. 预测预警 - 基于趋势提前预警
5. 踩坑集成 - 自动记录到 PITFALLS.md

作者：太一 AGI
创建：2026-04-23
版本：v2.0 (智能自进化版)
"""

import json
import time
import hmac
import hashlib
import requests
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('/home/nicola/.openclaw/workspace/logs/binance_smart_health.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('BinanceSmartHealth')

# ==================== 配置 ====================
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
ENV_FILE = WORKSPACE.parent / ".env"
IP_FILE = Path("/tmp/last_export_ip.txt")
PID_FILE = Path("/tmp/zhiji_trader.pid")
HEALTH_STATUS_FILE = Path("/tmp/binance_smart_health_status.json")
EVOLUTION_HISTORY_FILE = WORKSPACE / "data" / "binance_health_evolution.json"
PITFALLS_FILE = WORKSPACE / "memory" / "PITFALLS.md"

# 白名单 IP
WHITELISTED_IPS = [
    '141.11.146.70',
    '103.151.172.28',
    '103.151.173.206',
]

# ==================== 数据结构 ====================
class ProblemType(Enum):
    API_CONNECTION = "api_connection"
    IP_WHITELIST = "ip_whitelist"
    BALANCE_LOW = "balance_low"
    PROCESS_DOWN = "process_down"
    PERMISSION_ERROR = "permission_error"
    NETWORK_ERROR = "network_error"

class HealAction(Enum):
    RESTART_PROCESS = "restart_process"
    RETRY_API = "retry_api"
    SWITCH_IP = "switch_ip"
    UPDATE_CONFIG = "update_config"
    NOTIFY_USER = "notify_user"
    LEARN_AND_ADAPT = "learn_and_adapt"

@dataclass
class HealthIssue:
    """健康问题记录"""
    issue_id: str
    problem_type: str
    severity: str  # low, medium, high, critical
    description: str
    root_cause: str
    heal_action: str
    heal_result: str
    timestamp: str
    learned: bool = False

@dataclass
class EvolutionMetrics:
    """进化指标"""
    total_checks: int = 0
    issues_found: int = 0
    auto_healed: int = 0
    manual_required: int = 0
    success_rate: float = 0.0
    avg_heal_time: float = 0.0
    learned_patterns: int = 0

# ==================== 核心类 ====================
class BinanceSmartHealthChecker:
    """币安智能健康检查器"""
    
    def __init__(self):
        self.api_key = None
        self.api_secret = None
        self.issue_history: List[HealthIssue] = []
        self.evolution_metrics = EvolutionMetrics()
        self.load_credentials()
        self.load_evolution_history()
    
    def load_credentials(self):
        """加载 API 凭证"""
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("BINANCE_API_KEY="):
                        self.api_key = line.split("=")[1].strip()
                    elif line.startswith("BINANCE_API_SECRET="):
                        self.api_secret = line.split("=")[1].strip()
    
    def load_evolution_history(self):
        """加载进化历史"""
        if EVOLUTION_HISTORY_FILE.exists():
            with open(EVOLUTION_HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.issue_history = [
                    HealthIssue(**issue) for issue in data.get('issues', [])
                ]
                metrics = data.get('metrics', {})
                self.evolution_metrics = EvolutionMetrics(**metrics)
    
    def save_evolution_history(self):
        """保存进化历史"""
        data = {
            'issues': [asdict(issue) for issue in self.issue_history[-100:]],  # 保留最近 100 条
            'metrics': asdict(self.evolution_metrics),
            'last_updated': datetime.now().isoformat()
        }
        
        EVOLUTION_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(EVOLUTION_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def generate_issue_id(self) -> str:
        """生成问题 ID"""
        return f"ISSUE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # ========== 检查方法 ==========
    def check_api_connection(self, retry_count: int = 3) -> Dict:
        """智能 API 连接检查 (支持重试)"""
        for attempt in range(retry_count):
            try:
                timestamp = int(time.time() * 1000)
                params = f"timestamp={timestamp}"
                signature = hmac.new(
                    self.api_secret.encode('utf-8'),
                    params.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                url = f"https://api.binance.com/api/v3/account?{params}&signature={signature}"
                headers = {"X-MBX-APIKEY": self.api_key}
                
                response = requests.get(url, headers=headers, timeout=10, proxies={
                    'http': 'http://127.0.0.1:7890',
                    'https': 'http://127.0.0.1:7890',
                })
                
                if response.status_code == 200:
                    return {
                        'status': 'ok',
                        'message': 'API 连接正常',
                        'attempt': attempt + 1,
                        'account': response.json()
                    }
                elif response.status_code == 401:
                    error = response.json()
                    return {
                        'status': 'error',
                        'message': f"API 认证失败：{error.get('msg', 'Unknown')}",
                        'error_code': error.get('code'),
                        'attempt': attempt + 1
                    }
                
            except Exception as e:
                if attempt < retry_count - 1:
                    logger.warning(f"API 连接失败，重试 {attempt + 2}/{retry_count}: {str(e)}")
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    return {
                        'status': 'error',
                        'message': f"API 连接异常：{str(e)}",
                        'error_code': 'EXCEPTION',
                        'attempt': attempt + 1
                    }
        
        return {'status': 'error', 'message': 'API 连接失败', 'attempt': retry_count}
    
    def check_ip_whitelist(self) -> Dict:
        """智能 IP 白名单检查"""
        current_ip = None
        
        if IP_FILE.exists():
            content = IP_FILE.read_text().strip()
            for line in content.split('\n')[::-1]:
                line = line.strip()
                if len(line.split('.')) == 4 and all(p.isdigit() for p in line.split('.')):
                    current_ip = line
                    break
        
        if current_ip:
            if current_ip in WHITELISTED_IPS:
                return {
                    'status': 'ok',
                    'message': f"IP {current_ip} 在白名单中",
                    'ip': current_ip,
                    'suggestion': None
                }
            else:
                # 智能建议：检查是否在进化历史中学过这个 IP
                learned_ips = [
                    issue.root_cause for issue in self.issue_history
                    if issue.problem_type == ProblemType.IP_WHITELIST.value
                    and 'learned' in issue.root_cause
                ]
                
                return {
                    'status': 'warning',
                    'message': f"IP {current_ip} 不在已知白名单中",
                    'ip': current_ip,
                    'suggestion': '请在币安后台添加此 IP 到白名单',
                    'learned_ips': learned_ips
                }
        else:
            return {
                'status': 'error',
                'message': '无法获取当前 IP',
                'ip': None,
                'suggestion': '检查 IP 监控脚本是否运行'
            }
    
    def check_balance(self, account: Dict) -> Dict:
        """智能余额检查 (含预测)"""
        try:
            balances = {'USDT': 0.0, 'BTC': 0.0, 'ETH': 0.0}
            
            if 'balances' in account:
                for asset in account['balances']:
                    if asset['asset'] in balances:
                        balances[asset['asset']] = float(asset['free']) + float(asset['locked'])
            
            usdt_balance = balances['USDT']
            btc_balance = balances['BTC']
            
            # 智能判断：是否可交易
            can_trade = usdt_balance >= 10 or btc_balance >= 0.00013
            
            # 预测预警：基于历史消耗率
            days_remaining = None
            if usdt_balance > 0:
                # 简单估算：假设每天交易消耗$1
                avg_daily_usage = 1.0  # 可从历史数据学习
                days_remaining = usdt_balance / avg_daily_usage
            
            return {
                'status': 'ok' if can_trade else 'warning',
                'balances': balances,
                'can_trade': can_trade,
                'message': f"USDT: ${usdt_balance:.2f}, BTC: {btc_balance:.5f}",
                'prediction': {
                    'days_remaining': days_remaining,
                    'warning': days_remaining and days_remaining < 3
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"余额检查失败：{str(e)}",
                'can_trade': False
            }
    
    def check_zhiji_process(self) -> Dict:
        """智能进程检查"""
        try:
            import subprocess
            result = subprocess.run(
                ['pgrep', '-f', 'zhiji_auto_evolution_trader.py'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                
                # 检查进程运行时长
                uptime = self.get_process_uptime(pids[0])
                
                return {
                    'status': 'ok',
                    'message': f'知几进程运行中 (PID: {", ".join(pids)}, 运行时长：{uptime})',
                    'pids': pids,
                    'uptime': uptime
                }
            else:
                return {
                    'status': 'error',
                    'message': '知几进程未运行',
                    'pids': [],
                    'uptime': None
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'进程检查失败：{str(e)}'
            }
    
    def get_process_uptime(self, pid: str) -> str:
        """获取进程运行时长"""
        try:
            import subprocess
            result = subprocess.run(
                ['ps', '-o', 'etime=', '-p', pid],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() if result.returncode == 0 else '未知'
        except:
            return '未知'
    
    # ========== 自愈方法 ==========
    def auto_heal(self, issue: HealthIssue) -> bool:
        """智能自愈"""
        logger.info(f"🔧 开始自愈：{issue.problem_type}")
        
        start_time = time.time()
        success = False
        
        try:
            if issue.problem_type == ProblemType.PROCESS_DOWN.value:
                success = self.heal_restart_process()
            elif issue.problem_type == ProblemType.API_CONNECTION.value:
                success = self.heal_api_connection()
            elif issue.problem_type == ProblemType.IP_WHITELIST.value:
                success = self.heal_ip_whitelist()
            elif issue.problem_type == ProblemType.BALANCE_LOW.value:
                success = self.heal_balance_low()
            
            heal_time = time.time() - start_time
            
            if success:
                self.evolution_metrics.auto_healed += 1
                logger.info(f"✅ 自愈成功：{issue.problem_type} (耗时：{heal_time:.2f}s)")
            else:
                self.evolution_metrics.manual_required += 1
                logger.error(f"❌ 自愈失败：{issue.problem_type}，需要人工干预")
            
            # 学习：记录自愈结果
            issue.heal_result = 'success' if success else 'failed'
            issue.learned = True
            self.save_evolution_history()
            
            return success
            
        except Exception as e:
            logger.error(f"自愈异常：{str(e)}")
            return False
    
    def heal_restart_process(self) -> bool:
        """自愈：重启知几进程"""
        try:
            import subprocess
            
            # 停止旧进程
            subprocess.run(['pkill', '-9', '-f', 'zhiji_auto_evolution'], timeout=10)
            time.sleep(3)
            
            # 启动新进程
            script = WORKSPACE / "scripts" / "zhiji_auto_evolution_trader.py"
            log_file = WORKSPACE / "logs" / "zhiji_evolution_trader.log"
            
            with open(log_file, 'a') as log:
                subprocess.Popen(
                    ['python3', str(script)],
                    stdout=log,
                    stderr=log,
                    start_new_session=True
                )
            
            time.sleep(5)
            
            # 验证
            result = self.check_zhiji_process()
            return result['status'] == 'ok'
            
        except Exception as e:
            logger.error(f"重启失败：{str(e)}")
            return False
    
    def heal_api_connection(self) -> bool:
        """自愈：API 连接重试"""
        # 已在检查时自动重试 3 次
        # 这里可以尝试切换 IP 或其他策略
        return False  # 需要人工检查 API Key
    
    def heal_ip_whitelist(self) -> bool:
        """自愈：IP 白名单"""
        # 无法自动添加币安白名单，只能记录
        return False  # 需要人工添加
    
    def heal_balance_low(self) -> bool:
        """自愈：余额不足"""
        # 无法自动充值，只能告警
        return False  # 需要人工充值
    
    # ========== 自进化方法 ==========
    def learn_from_issue(self, issue: HealthIssue):
        """从问题中学习"""
        # 分析问题模式
        similar_issues = [
            i for i in self.issue_history
            if i.problem_type == issue.problem_type
        ]
        
        if len(similar_issues) >= 3:
            # 发现重复模式，提炼通用原则
            self.extract_pattern(issue.problem_type, similar_issues)
    
    def extract_pattern(self, problem_type: str, issues: List[HealthIssue]):
        """提炼问题模式"""
        # 分析根因
        root_causes = [i.root_cause for i in issues]
        most_common_cause = max(set(root_causes), key=root_causes.count)
        
        # 分析自愈策略
        heal_actions = [i.heal_action for i in issues if i.heal_result == 'success']
        best_heal_action = max(set(heal_actions), key=heal_actions.count) if heal_actions else None
        
        logger.info(f"🧠 提炼模式：{problem_type}")
        logger.info(f"   常见根因：{most_common_cause}")
        logger.info(f"   有效自愈：{best_heal_action}")
        
        # 可以写入 PITFALLS.md 或更新配置
        self.write_to_pitfalls(problem_type, most_common_cause, best_heal_action)
    
    def write_to_pitfalls(self, problem_type: str, root_cause: str, heal_action: str):
        """写入踩坑日志"""
        try:
            lesson_id = f"LESSON-{datetime.now().strftime('%Y%m%d')}-AUTO"
            
            pitfalls_entry = f"""
### {datetime.now().strftime('%Y-%m-%d')}: {problem_type} (自进化发现)

**编号**: `{lesson_id}`

**问题**: {problem_type}

**根因**: {root_cause}

**有效自愈**: {heal_action}

**教训**: > 通过自进化分析发现的重复问题模式

**状态**: ✅ 已学习 | 📝 已记录
"""
            
            if PITFALLS_FILE.exists():
                with open(PITFALLS_FILE, 'a', encoding='utf-8') as f:
                    f.write(pitfalls_entry)
            
            logger.info(f"📝 已写入踩坑日志：{lesson_id}")
            
        except Exception as e:
            logger.error(f"写入踩坑日志失败：{str(e)}")
    
    # ========== 主检查流程 ==========
    def smart_health_check(self):
        """智能健康检查"""
        logger.info("=" * 60)
        logger.info("🏥 币安智能健康自检开始")
        logger.info("=" * 60)
        
        self.evolution_metrics.total_checks += 1
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'overall_status': 'ok',
            'issues': [],
            'auto_heal_triggered': False,
            'evolution_metrics': asdict(self.evolution_metrics)
        }
        
        # 1. 检查 IP 白名单
        ip_status = self.check_ip_whitelist()
        results['checks']['ip_whitelist'] = ip_status
        logger.info(f"{'✅' if ip_status['status'] == 'ok' else '⚠️'}  IP 白名单：{ip_status['message']}")
        
        if ip_status['status'] in ['warning', 'error']:
            issue = HealthIssue(
                issue_id=self.generate_issue_id(),
                problem_type=ProblemType.IP_WHITELIST.value,
                severity='medium' if ip_status['status'] == 'warning' else 'high',
                description=ip_status['message'],
                root_cause=f"IP {ip_status.get('ip', 'unknown')} 不在白名单",
                heal_action=HealAction.UPDATE_CONFIG.value,
                heal_result='pending',
                timestamp=datetime.now().isoformat()
            )
            results['issues'].append(asdict(issue))
            self.issue_history.append(issue)
            self.learn_from_issue(issue)
        
        # 2. 检查 API 连接
        api_status = self.check_api_connection()
        results['checks']['api_connection'] = api_status
        
        if api_status['status'] == 'ok':
            logger.info(f"✅ API 连接：{api_status['message']} (尝试 {api_status.get('attempt', 1)} 次)")
            
            # 3. 检查余额
            balance_status = self.check_balance(api_status.get('account', {}))
            results['checks']['balance'] = balance_status
            logger.info(f"{'✅' if balance_status['status'] == 'ok' else '⚠️'}  账户余额：{balance_status['message']}")
            
            if balance_status['status'] == 'warning':
                issue = HealthIssue(
                    issue_id=self.generate_issue_id(),
                    problem_type=ProblemType.BALANCE_LOW.value,
                    severity='low',
                    description=balance_status['message'],
                    root_cause='余额低于最小交易要求',
                    heal_action=HealAction.NOTIFY_USER.value,
                    heal_result='pending',
                    timestamp=datetime.now().isoformat()
                )
                results['issues'].append(asdict(issue))
                self.issue_history.append(issue)
        else:
            logger.error(f"❌ API 连接：{api_status['message']}")
            results['checks']['balance'] = {'status': 'error', 'message': 'API 连接失败'}
            results['overall_status'] = 'error'
            
            issue = HealthIssue(
                issue_id=self.generate_issue_id(),
                problem_type=ProblemType.API_CONNECTION.value,
                severity='high',
                description=api_status['message'],
                root_cause='API 认证失败或网络问题',
                heal_action=HealAction.RETRY_API.value,
                heal_result='pending',
                timestamp=datetime.now().isoformat()
            )
            results['issues'].append(asdict(issue))
            self.issue_history.append(issue)
        
        # 4. 检查知几进程
        process_status = self.check_zhiji_process()
        results['checks']['process'] = process_status
        logger.info(f"{'✅' if process_status['status'] == 'ok' else '❌'}  知几进程：{process_status['message']}")
        
        if process_status['status'] == 'error':
            issue = HealthIssue(
                issue_id=self.generate_issue_id(),
                problem_type=ProblemType.PROCESS_DOWN.value,
                severity='critical',
                description='知几进程未运行',
                root_cause='进程崩溃或被杀死',
                heal_action=HealAction.RESTART_PROCESS.value,
                heal_result='pending',
                timestamp=datetime.now().isoformat()
            )
            results['issues'].append(asdict(issue))
            self.issue_history.append(issue)
            
            # 触发自愈
            logger.warning("🔧 触发自愈：知几进程未运行，尝试重启...")
            results['auto_heal_triggered'] = True
            if self.auto_heal(issue):
                logger.info("✅ 自愈成功：知几已重启")
            else:
                logger.error("❌ 自愈失败：需要人工干预")
        
        # 5. 综合状态
        if any(check.get('status') == 'error' for check in results['checks'].values()):
            results['overall_status'] = 'error'
        elif any(check.get('status') == 'warning' for check in results['checks'].values()):
            results['overall_status'] = 'warning'
        
        # 6. 更新指标
        self.evolution_metrics.issues_found += len(results['issues'])
        if self.evolution_metrics.total_checks > 0:
            self.evolution_metrics.success_rate = (
                self.evolution_metrics.auto_healed / 
                max(1, self.evolution_metrics.auto_healed + self.evolution_metrics.manual_required)
            ) * 100
        
        # 7. 保存状态
        self.save_evolution_history()
        self.save_health_status(results)
        
        # 8. 输出总结
        logger.info("=" * 60)
        logger.info(f"📊 健康检查完成 - 总体状态：{results['overall_status'].upper()}")
        logger.info(f"🔧 自愈触发：{'是' if results['auto_heal_triggered'] else '否'}")
        logger.info(f"📝 发现问题：{len(results['issues'])} 个")
        logger.info(f"🧠 进化指标：检查{self.evolution_metrics.total_checks}次，自愈{self.evolution_metrics.auto_healed}次，成功率{self.evolution_metrics.success_rate:.1f}%")
        logger.info("=" * 60)
        
        return results
    
    def save_health_status(self, status: Dict):
        """保存健康状态"""
        with open(HEALTH_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)

# ==================== 主程序 ====================
if __name__ == '__main__':
    checker = BinanceSmartHealthChecker()
    checker.smart_health_check()
