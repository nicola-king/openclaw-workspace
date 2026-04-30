#!/usr/bin/env python3
"""
智能自动化控制器 - 协调三大组件工作
统一调度·状态监控·故障恢复·性能优化
"""

import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, Any, Callable
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from smart_ai_router import SmartAIRouter
from smart_gateway import SmartGateway
from smart_communication import SmartCommunicationRouter

class SmartAutomationController:
    def __init__(self):
        self.ai_router = SmartAIRouter()
        self.gateway = SmartGateway()
        self.comm_router = SmartCommunicationRouter()
        self.components = {
            'ai_router': self.ai_router,
            'gateway': self.gateway,
            'comm_router': self.comm_router
        }
        self.system_status = {
            'initialized': False,
            'last_check': None,
            'health_score': 0,
            'components_status': {}
        }
        self.monitoring_thread = None
        self.auto_fix_enabled = True
        
    def initialize_system(self) -> bool:
        """初始化整个智能自动化系统"""
        print("正在初始化智能自动化系统...")
        
        try:
            # 初始化各组件
            components_init_status = {}
            
            # AI 路由器
            print("  初始化 AI 路由器...")
            ai_test = self.ai_router.route_request("测试请求")
            components_init_status['ai_router'] = bool(ai_test)
            
            # 网关路由器
            print("  初始化网关路由器...")
            gateway_test = self.gateway.test_all_connections()
            components_init_status['gateway'] = all(gateway_test.values()) if gateway_test else False
            
            # 通信路由器
            print("  初始化通信路由器...")
            comm_stats = self.comm_router.get_communication_stats()
            components_init_status['comm_router'] = bool(comm_stats)
            
            # 更新系统状态
            self.system_status['initialized'] = all(components_init_status.values())
            self.system_status['components_status'] = components_init_status
            self.system_status['last_check'] = datetime.now().isoformat()
            
            # 计算健康分数
            healthy_components = sum(1 for status in components_init_status.values() if status)
            self.system_status['health_score'] = (healthy_components / len(components_init_status)) * 100
            
            print(f"系统初始化完成: {'✅' if self.system_status['initialized'] else '❌'}")
            print(f"健康分数: {self.system_status['health_score']:.1f}%")
            
            return self.system_status['initialized']
            
        except Exception as e:
            print(f"系统初始化失败: {e}")
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """执行全面健康检查"""
        checks = {}
        
        # AI 路由器检查
        try:
            ai_test_result = self.ai_router.route_request("健康检查")
            checks['ai_router'] = {
                'status': bool(ai_test_result),
                'response_time': 'fast' if ai_test_result else 'slow',
                'last_check': time.time()
            }
        except Exception as e:
            checks['ai_router'] = {'status': False, 'error': str(e)}
        
        # 网关检查
        try:
            gateway_results = self.gateway.test_all_connections()
            checks['gateway'] = {
                'status': all(gateway_results.values()) if gateway_results else False,
                'details': gateway_results,
                'last_check': time.time()
            }
        except Exception as e:
            checks['gateway'] = {'status': False, 'error': str(e)}
        
        # 通信路由器检查
        try:
            comm_stats = self.comm_router.get_communication_stats()
            checks['comm_router'] = {
                'status': bool(comm_stats),
                'active_platforms': [p for p, s in comm_stats.get('platforms_enabled', {}).items() if s],
                'pending_messages': comm_stats.get('queue_stats', {}).get('pending_messages', 0),
                'last_check': time.time()
            }
        except Exception as e:
            checks['comm_router'] = {'status': False, 'error': str(e)}
        
        # 更新整体状态
        overall_status = all(check.get('status', False) for check in checks.values())
        
        return {
            'overall_status': overall_status,
            'checks': checks,
            'timestamp': datetime.now().isoformat(),
            'health_score': self.calculate_health_score(checks)
        }
    
    def calculate_health_score(self, checks: Dict[str, Any]) -> float:
        """计算系统健康分数"""
        score = 0
        total_checks = len(checks)
        
        for component, check in checks.items():
            if check.get('status', False):
                score += 1
        
        return (score / total_checks) * 100 if total_checks > 0 else 0
    
    def auto_fix_issues(self, health_report: Dict[str, Any]) -> Dict[str, Any]:
        """自动修复检测到的问题"""
        fixes_applied = []
        
        # AI 路由器修复
        if not health_report['checks'].get('ai_router', {}).get('status', False):
            print("尝试修复 AI 路由器...")
            try:
                # 重新加载配置
                self.ai_router.config = self.ai_router.load_config()
                fixes_applied.append('ai_router_config_reload')
            except Exception as e:
                print(f"AI 路由器修复失败: {e}")
        
        # 网关修复
        if not health_report['checks'].get('gateway', {}).get('status', False):
            print("尝试修复网关...")
            try:
                # 重新初始化端点
                self.gateway.init_endpoints()
                self.gateway.update_health_status()
                fixes_applied.append('gateway_reinit')
            except Exception as e:
                print(f"网关修复失败: {e}")
        
        # 通信路由器修复
        if not health_report['checks'].get('comm_router', {}).get('status', False):
            print("尝试修复通信路由器...")
            try:
                # 重新初始化平台
                self.comm_router.init_platforms()
                fixes_applied.append('comm_router_reinit')
            except Exception as e:
                print(f"通信路由器修复失败: {e}")
        
        return {
            'fixes_applied': fixes_applied,
            'timestamp': datetime.now().isoformat()
        }
    
    def start_monitoring(self, interval: int = 60):
        """启动后台监控"""
        def monitor_loop():
            while True:
                try:
                    health = self.health_check()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 监控: 健康分数 {health['health_score']:.1f}%")
                    
                    # 如果健康分数低于阈值，执行自动修复
                    if health['health_score'] < 80 and self.auto_fix_enabled:
                        print("健康分数低于80%，执行自动修复...")
                        fix_result = self.auto_fix_issues(health)
                        if fix_result['fixes_applied']:
                            print(f"已应用修复: {fix_result['fixes_applied']}")
                    
                    # 处理消息队列
                    queue_result = self.comm_router.process_queue()
                    if queue_result['processed'] > 0 or queue_result['failed'] > 0:
                        print(f"队列处理: {queue_result['processed']} 成功, {queue_result['failed']} 失败")
                    
                    time.sleep(interval)
                except Exception as e:
                    print(f"监控循环异常: {e}")
                    time.sleep(interval)
        
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
        print(f"后台监控已启动 (间隔 {interval} 秒)")
    
    def get_system_report(self) -> Dict[str, Any]:
        """获取完整系统报告"""
        health = self.health_check()
        
        return {
            'system_info': {
                'initialized': self.system_status['initialized'],
                'health_score': health['health_score'],
                'timestamp': datetime.now().isoformat()
            },
            'component_details': {
                'ai_router': {
                    'model_routing_active': True,
                    'local_model_available': self.check_local_model(),
                    'cloud_models_configured': self.check_cloud_models()
                },
                'gateway': {
                    'domestic_endpoints': len(self.gateway.domestic_endpoints),
                    'proxy_endpoints': len(self.gateway.proxy_endpoints),
                    'health_status': self.gateway.health_status
                },
                'communication': {
                    'active_platforms': [p for p, s in self.comm_router.platform_stats.items()],
                    'message_queue_size': len(self.comm_router.message_queue),
                    'platform_stats': self.comm_router.platform_stats
                }
            },
            'performance_metrics': {
                'uptime_minutes': (datetime.now() - datetime.fromisoformat(self.system_status['last_check'])) if self.system_status['last_check'] else 0,
                'total_requests_handled': self.get_total_requests()
            }
        }
    
    def check_local_model(self) -> bool:
        """检查本地模型是否可用"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_cloud_models(self) -> Dict[str, bool]:
        """检查云端模型配置"""
        config = self.ai_router.config
        providers = config.get('models', {}).get('providers', {})
        
        return {
            'bailian': 'bailian' in providers,
            'google': 'google' in providers,
            'configured': len(providers) > 0
        }
    
    def get_total_requests(self) -> int:
        """获取总请求数"""
        total = 0
        for platform, stats in self.comm_router.platform_stats.items():
            total += stats.get('sent', 0) + stats.get('failed', 0)
        return total
    
    def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理传入请求 - 统一入口"""
        try:
            # 根据请求类型路由到不同组件
            request_type = request_data.get('type', 'general')
            
            if request_type == 'ai_route':
                # AI 模型路由请求
                user_request = request_data.get('prompt', '')
                result = self.ai_router.route_request(user_request)
                return {
                    'success': True,
                    'type': 'ai_response',
                    'result': result,
                    'component_used': 'ai_router'
                }
            elif request_type == 'gateway_route':
                # 网关路由请求
                result = self.gateway.route_request(request_data)
                return {
                    'success': result.get('success', False),
                    'type': 'gateway_response',
                    'result': result,
                    'component_used': 'gateway'
                }
            elif request_type == 'message_send':
                # 消息发送请求
                message = request_data.get('message', '')
                target_platform = request_data.get('platform', 'weixin')
                result = self.comm_router.route_message(message, target_platform, **request_data)
                return {
                    'success': result.get('success', False),
                    'type': 'message_response',
                    'result': result,
                    'component_used': 'comm_router'
                }
            else:
                # 默认使用 AI 路由
                user_request = str(request_data)
                result = self.ai_router.route_request(user_request)
                return {
                    'success': True,
                    'type': 'general_response',
                    'result': result,
                    'component_used': 'ai_router'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'component_used': 'controller'
            }
    
    def save_state(self, filepath: str = None):
        """保存系统状态"""
        if filepath is None:
            filepath = os.path.expanduser("~/.openclaw/workspace/memory/smart-auto-state.json")
        
        state = {
            'timestamp': datetime.now().isoformat(),
            'system_status': self.system_status,
            'health_score': self.health_check()['health_score'],
            'components': {
                'ai_router_config_loaded': bool(self.ai_router.config),
                'gateway_endpoints_count': len(self.gateway.domestic_endpoints) + len(self.gateway.proxy_endpoints),
                'comm_router_platforms': list(self.comm_router.platforms.keys()),
                'message_queue_size': len(self.comm_router.message_queue)
            }
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            print(f"系统状态已保存到 {filepath}")
        except Exception as e:
            print(f"保存状态失败: {e}")

# 使用示例
if __name__ == "__main__":
    controller = SmartAutomationController()
    
    print("=== 智能自动化控制器测试 ===\n")
    
    # 1. 初始化系统
    print("1. 初始化系统...")
    init_success = controller.initialize_system()
    print(f"初始化结果: {'✅ 成功' if init_success else '❌ 失败'}\n")
    
    if init_success:
        # 2. 执行健康检查
        print("2. 执行健康检查...")
        health_report = controller.health_check()
        print(f"整体状态: {'✅ 正常' if health_report['overall_status'] else '❌ 异常'}")
        print(f"健康分数: {health_report['health_score']:.1f}%\n")
        
        # 3. 获取系统报告
        print("3. 获取系统报告...")
        report = controller.get_system_report()
        print(f"系统健康分数: {report['system_info']['health_score']:.1f}%")
        print(f"AI 路由器: 本地模型可用 - {report['component_details']['ai_router']['local_model_available']}")
        print(f"网关: 国内端点 {len(report['component_details']['gateway']['domestic_endpoints'])} 个, 代理端点 {len(report['component_details']['gateway']['proxy_endpoints'])} 个")
        print(f"通信: 活跃平台 {len(report['component_details']['communication']['active_platforms'])} 个\n")
        
        # 4. 测试请求处理
        print("4. 测试请求处理...")
        test_request = {
            'type': 'ai_route',
            'prompt': '简单自我介绍'
        }
        result = controller.process_request(test_request)
        print(f"请求处理结果: {result['success']}, 使用组件: {result['component_used']}\n")
        
        # 5. 启动监控
        print("5. 启动后台监控...")
        controller.start_monitoring(interval=30)  # 30秒检查一次
        
        # 6. 保存状态
        controller.save_state()
        
        print("\n智能自动化系统已就绪！")
        print("- 健康检查已启用")
        print("- 自动修复已启用") 
        print("- 后台监控已启动")
        print("- 状态持久化已配置")