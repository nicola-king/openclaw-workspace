#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海外互联网智能分流代理路由器
太一 AGI · 2026-04-21 00:16

功能:
- AI 请求智能分流 (日本/美国节点)
- 避免香港节点 (防止 AI 限制)
- 自动故障转移
- 健康检查
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('OverseasProxyRouter')


class OverseasProxyRouter:
    """海外互联网智能分流代理路由器"""
    
    # 代理节点配置
    PROXY_NODES = {
        "JP": {
            "name": "日本节点",
            "endpoint": "http://jp-proxy.internal:7890",
            "latency_ms": 50,
            "priority": 1,
            "ai_friendly": True,
            "blocked": False
        },
        "US": {
            "name": "美国节点",
            "endpoint": "http://us-proxy.internal:7891",
            "latency_ms": 120,
            "priority": 2,
            "ai_friendly": True,
            "blocked": False
        },
        "SG": {
            "name": "新加坡节点",
            "endpoint": "http://sg-proxy.internal:7892",
            "latency_ms": 80,
            "priority": 3,
            "ai_friendly": True,
            "blocked": False
        },
        "HK": {
            "name": "香港节点",
            "endpoint": "http://hk-proxy.internal:7893",
            "latency_ms": 30,
            "priority": 99,
            "ai_friendly": False,
            "blocked": True,
            "block_reason": "可能限制 AI 使用"
        },
        "CN": {
            "name": "大陆节点",
            "endpoint": "http://cn-proxy.internal:7894",
            "latency_ms": 10,
            "priority": 99,
            "ai_friendly": False,
            "blocked": True,
            "block_reason": "无法访问海外 AI"
        }
    }
    
    # AI 提供商路由规则
    AI_PROVIDER_ROUTING = {
        "google": {
            "preferred_region": "JP",
            "backup_region": "US",
            "models": ["gemini-*"],
            "reason": "日本节点延迟低，AI 访问无限制"
        },
        "openai": {
            "preferred_region": "US",
            "backup_region": "JP",
            "models": ["gpt-*"],
            "reason": "美国节点原生访问，无地域限制"
        },
        "anthropic": {
            "preferred_region": "US",
            "backup_region": "JP",
            "models": ["claude-*"],
            "reason": "美国节点原生访问，无地域限制"
        },
        "github": {
            "preferred_region": "JP",
            "backup_region": "US",
            "models": ["copilot-*"],
            "reason": "日本节点访问 GitHub 速度快"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or Path.home() / '.openclaw' / 'workspace' / 'data' / 'model-router-config.json'
        self.config = self._load_config()
        self.health_status = self._load_health_status()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "proxy_config": {
                "enabled": True,
                "strategy": "smart_routing",
                "avoid_regions": ["HK", "CN"],
                "preferred_regions": ["JP", "US"]
            }
        }
    
    def _load_health_status(self) -> Dict[str, Dict]:
        """加载节点健康状态"""
        health_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'proxy-health.json'
        if health_file.exists():
            with open(health_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认健康状态
        return {
            region: {"healthy": True, "last_check": datetime.now().isoformat()}
            for region in self.PROXY_NODES
        }
    
    def get_proxy_for_ai(self, provider: str, model: str) -> Dict:
        """获取 AI 请求的代理配置"""
        logger.info(f"🌐 获取 AI 代理：{provider} - {model}")
        
        # 检查提供商路由规则
        routing_rule = self.AI_PROVIDER_ROUTING.get(provider)
        
        if not routing_rule:
            # 默认使用日本节点
            return self._get_proxy_by_region("JP")
        
        # 获取首选区域
        preferred_region = routing_rule["preferred_region"]
        backup_region = routing_rule["backup_region"]
        
        # 检查首选节点是否可用
        if self._is_region_available(preferred_region):
            proxy = self._get_proxy_by_region(preferred_region)
            proxy["reason"] = routing_rule["reason"]
            logger.info(f"✅ 使用首选节点：{preferred_region}")
            return proxy
        
        # 使用备用节点
        if self._is_region_available(backup_region):
            proxy = self._get_proxy_by_region(backup_region)
            proxy["reason"] = f"备用节点 ({routing_rule['reason']})"
            logger.info(f"⚠️ 使用备用节点：{backup_region}")
            return proxy
        
        # 无可用节点
        logger.error(f"❌ 无可用代理节点")
        return {
            "enabled": False,
            "error": "No available proxy nodes"
        }
    
    def _get_proxy_by_region(self, region: str) -> Dict:
        """按区域获取代理"""
        node = self.PROXY_NODES.get(region)
        
        if not node:
            return {"enabled": False, "error": f"Unknown region: {region}"}
        
        if node.get("blocked", False):
            return {
                "enabled": False,
                "error": f"Region blocked: {node['block_reason']}"
            }
        
        return {
            "enabled": True,
            "region": region,
            "region_name": node["name"],
            "endpoint": node["endpoint"],
            "latency_ms": node["latency_ms"],
            "priority": node["priority"]
        }
    
    def _is_region_available(self, region: str) -> bool:
        """检查区域是否可用"""
        node = self.PROXY_NODES.get(region)
        
        if not node:
            return False
        
        if node.get("blocked", False):
            return False
        
        # 检查健康状态
        health = self.health_status.get(region, {})
        return health.get("healthy", True)
    
    def get_available_nodes(self) -> List[Dict]:
        """获取可用节点列表"""
        available = []
        
        for region, node in self.PROXY_NODES.items():
            if not node.get("blocked", False):
                health = self.health_status.get(region, {})
                if health.get("healthy", True):
                    available.append({
                        "region": region,
                        "name": node["name"],
                        "endpoint": node["endpoint"],
                        "latency_ms": node["latency_ms"],
                        "priority": node["priority"]
                    })
        
        # 按优先级排序
        available.sort(key=lambda x: x["priority"])
        
        return available
    
    def update_health_status(self, region: str, healthy: bool, latency_ms: int = None):
        """更新节点健康状态"""
        self.health_status[region] = {
            "healthy": healthy,
            "latency_ms": latency_ms,
            "last_check": datetime.now().isoformat()
        }
        
        # 保存健康状态
        health_file = Path.home() / '.openclaw' / 'workspace' / 'data' / 'proxy-health.json'
        health_file.parent.mkdir(parents=True, exist_ok=True)
        with open(health_file, 'w', encoding='utf-8') as f:
            json.dump(self.health_status, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 更新节点健康状态：{region} - {'健康' if healthy else '故障'}")
    
    def get_routing_summary(self) -> Dict:
        """获取路由摘要"""
        available_nodes = self.get_available_nodes()
        
        return {
            "total_nodes": len(self.PROXY_NODES),
            "available_nodes": len(available_nodes),
            "blocked_nodes": len([n for n in self.PROXY_NODES.values() if n.get("blocked", False)]),
            "preferred_regions": self.config.get("proxy_config", {}).get("preferred_regions", ["JP", "US"]),
            "avoid_regions": self.config.get("proxy_config", {}).get("avoid_regions", ["HK", "CN"]),
            "nodes": available_nodes
        }


def main():
    logger.info("=" * 60)
    logger.info("🌐 海外互联网智能分流代理路由器")
    logger.info("=" * 60)
    
    router = OverseasProxyRouter()
    
    # 演示获取 AI 代理
    logger.info(f"\n🤖 获取 AI 代理配置...")
    
    # Google Gemini
    gemini_proxy = router.get_proxy_for_ai("google", "gemini-2.5-pro")
    logger.info(f"  Google Gemini: {gemini_proxy.get('region_name', 'N/A')} - {gemini_proxy.get('endpoint', 'N/A')}")
    
    # OpenAI GPT
    gpt_proxy = router.get_proxy_for_ai("openai", "gpt-4o")
    logger.info(f"  OpenAI GPT: {gpt_proxy.get('region_name', 'N/A')} - {gpt_proxy.get('endpoint', 'N/A')}")
    
    # Anthropic Claude
    claude_proxy = router.get_proxy_for_ai("anthropic", "claude-3-sonnet")
    logger.info(f"  Anthropic Claude: {claude_proxy.get('region_name', 'N/A')} - {claude_proxy.get('endpoint', 'N/A')}")
    
    # 获取可用节点
    logger.info(f"\n📊 可用节点列表:")
    available = router.get_available_nodes()
    for node in available:
        logger.info(f"  • {node['name']} ({node['region']}): {node['endpoint']} - {node['latency_ms']}ms")
    
    # 获取路由摘要
    logger.info(f"\n📊 路由摘要:")
    summary = router.get_routing_summary()
    logger.info(f"  总节点数：{summary['total_nodes']}")
    logger.info(f"  可用节点：{summary['available_nodes']}")
    logger.info(f"  封锁节点：{summary['blocked_nodes']}")
    logger.info(f"  首选区域：{summary['preferred_regions']}")
    logger.info(f"  避免区域：{summary['avoid_regions']}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 海外智能分流代理演示完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
