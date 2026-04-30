#!/usr/bin/env python3
"""
🔒 安全加固配置

OpenClaw 4.10 安全增强
SSRF 防御/主机名允许列表/Exec 预检/插件扫描

作者：太一 AGI
创建：2026-04-11
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class SecurityHardening:
    """安全加固配置"""
    
    def __init__(self):
        """初始化安全配置"""
        self.config = self._load_config()
        
        print("🔒 安全加固配置已加载")
        print(f"   SSRF 防御：{self.config.get('ssrf_defense', 'enabled')}")
        print(f"   主机名允许列表：{len(self.config.get('hostname_allowlist', []))} 个")
        print(f"   Exec 预检：{self.config.get('exec_preflight', 'enabled')}")
        print()
    
    def _load_config(self) -> Dict:
        """加载安全配置"""
        config_file = Path("/home/nicola/.openclaw/workspace/config/security/config.json")
        
        if not config_file.exists():
            # 创建默认安全配置
            default_config = {
                "ssrf_defense": {
                    "enabled": True,
                    "strict_defaults": True,
                    "interaction_driven_redirects": True
                },
                "hostname_allowlist": {
                    "enabled": True,
                    "hosts": [
                        "api.telegram.org",
                        "open.feishu.cn",
                        "discord.com",
                        "api.openai.com",
                        "generativelanguage.googleapis.com"
                    ]
                },
                "exec_preflight": {
                    "enabled": True,
                    "hardened_reads": True,
                    "host_env_denylist": ["PASSWORD", "SECRET", "KEY", "TOKEN"],
                    "node_output_boundaries": True
                },
                "plugin_scanning": {
                    "enabled": True,
                    "scan_dependencies": True,
                    "reject_malicious": True
                },
                "websocket_budget": {
                    "enabled": True,
                    "max_connections": 100,
                    "upgrade_budget_seconds": 30
                }
            }
            
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            return default_config
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_ssrf_defense(self) -> Dict:
        """检查 SSRF 防御"""
        ssrf = self.config.get('ssrf_defense', {})
        
        return {
            "enabled": ssrf.get('enabled', False),
            "strict_defaults": ssrf.get('strict_defaults', False),
            "interaction_driven_redirects": ssrf.get('interaction_driven_redirects', False),
            "status": "✅ enabled" if ssrf.get('enabled') else "❌ disabled"
        }
    
    def check_hostname_allowlist(self) -> Dict:
        """检查主机名允许列表"""
        allowlist = self.config.get('hostname_allowlist', {})
        
        return {
            "enabled": allowlist.get('enabled', False),
            "hosts": allowlist.get('hosts', []),
            "count": len(allowlist.get('hosts', [])),
            "status": f"✅ {len(allowlist.get('hosts', []))} hosts" if allowlist.get('enabled') else "❌ disabled"
        }
    
    def check_exec_preflight(self) -> Dict:
        """检查 Exec 预检"""
        preflight = self.config.get('exec_preflight', {})
        
        return {
            "enabled": preflight.get('enabled', False),
            "hardened_reads": preflight.get('hardened_reads', False),
            "host_env_denylist": preflight.get('host_env_denylist', []),
            "node_output_boundaries": preflight.get('node_output_boundaries', False),
            "status": "✅ enabled" if preflight.get('enabled') else "❌ disabled"
        }
    
    def check_plugin_scanning(self) -> Dict:
        """检查插件扫描"""
        scanning = self.config.get('plugin_scanning', {})
        
        return {
            "enabled": scanning.get('enabled', False),
            "scan_dependencies": scanning.get('scan_dependencies', False),
            "reject_malicious": scanning.get('reject_malicious', False),
            "status": "✅ enabled" if scanning.get('enabled') else "❌ disabled"
        }
    
    def check_websocket_budget(self) -> Dict:
        """检查 WebSocket 预算"""
        budget = self.config.get('websocket_budget', {})
        
        return {
            "enabled": budget.get('enabled', False),
            "max_connections": budget.get('max_connections', 0),
            "upgrade_budget_seconds": budget.get('upgrade_budget_seconds', 0),
            "status": f"✅ {budget.get('max_connections', 0)} connections" if budget.get('enabled') else "❌ disabled"
        }
    
    def get_security_report(self) -> Dict:
        """获取安全报告"""
        return {
            "ssrf_defense": self.check_ssrf_defense(),
            "hostname_allowlist": self.check_hostname_allowlist(),
            "exec_preflight": self.check_exec_preflight(),
            "plugin_scanning": self.check_plugin_scanning(),
            "websocket_budget": self.check_websocket_budget(),
            "generated_at": datetime.now().isoformat()
        }
    
    def export_report(self, output_file: str):
        """导出安全报告"""
        report = self.get_security_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 安全报告已导出：{output_file}")


def main():
    """主函数 - 测试"""
    print("="*60)
    print("🔒 安全加固配置测试")
    print("="*60)
    
    # 初始化
    security = SecurityHardening()
    
    # 获取安全报告
    print("\n1. 安全报告...")
    report = security.get_security_report()
    
    print(f"\n   SSRF 防御：{report['ssrf_defense']['status']}")
    print(f"   主机名允许列表：{report['hostname_allowlist']['status']}")
    print(f"   Exec 预检：{report['exec_preflight']['status']}")
    print(f"   插件扫描：{report['plugin_scanning']['status']}")
    print(f"   WebSocket 预算：{report['websocket_budget']['status']}")
    
    # 导出报告
    print("\n2. 导出报告...")
    output_file = "/home/nicola/.openclaw/workspace/skills/security-hardening/security_report.json"
    security.export_report(output_file)
    
    print("\n✅ 安全加固配置测试完成!")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
