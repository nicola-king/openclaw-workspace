#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一 AaaS 平台 - API Gateway

Agent as a Service 统一入口
认证/鉴权/计费/限流

作者：太一 AGI
创建：2026-04-12
"""

import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('AAASGateway')


@dataclass
class APIKey:
    """API Key 数据结构"""
    key: str
    user_id: str
    tier: str  # free, personal, pro, enterprise
    created_at: str
    expires_at: str
    calls_remaining: int
    calls_limit: int


class AAASGateway:
    """AaaS API 网关"""
    
    def __init__(self):
        """初始化网关"""
        self.api_keys: Dict[str, APIKey] = {}
        self.rate_limits = {
            "free": 100,          # 100 次/月
            "personal": 10000,    # 10,000 次/月
            "pro": 100000,        # 100,000 次/月
            "enterprise": 1000000, # 1,000,000 次/月
        }
        
        logger.info("🚀 AaaS Gateway 已初始化")
        logger.info(f"📊 速率限制：{self.rate_limits}")
    
    async def authenticate(self, api_key: str) -> Optional[APIKey]:
        """认证 API Key"""
        if api_key not in self.api_keys:
            logger.warning(f"⚠️ 无效 API Key: {api_key[:8]}...")
            return None
        
        key_info = self.api_keys[api_key]
        
        # 检查过期
        if datetime.now().isoformat() > key_info.expires_at:
            logger.warning(f"⚠️ API Key 已过期：{key_info.user_id}")
            return None
        
        # 检查配额
        if key_info.calls_remaining <= 0:
            logger.warning(f"⚠️ 配额用尽：{key_info.user_id}")
            return None
        
        logger.info(f"✅ 认证成功：{key_info.user_id} ({key_info.tier})")
        
        return key_info
    
    async def consume_quota(self, api_key: str) -> bool:
        """消耗配额"""
        if api_key not in self.api_keys:
            return False
        
        key_info = self.api_keys[api_key]
        
        if key_info.calls_remaining <= 0:
            return False
        
        key_info.calls_remaining -= 1
        
        logger.debug(f"📊 配额剩余：{key_info.calls_remaining}/{key_info.calls_limit}")
        
        return True
    
    async def create_api_key(self, user_id: str, tier: str = "free") -> APIKey:
        """创建 API Key"""
        import secrets
        
        key = secrets.token_urlsafe(32)
        
        api_key = APIKey(
            key=key,
            user_id=user_id,
            tier=tier,
            created_at=datetime.now().isoformat(),
            expires_at="2027-01-01T00:00:00",  # 默认 1 年
            calls_remaining=self.rate_limits.get(tier, 100),
            calls_limit=self.rate_limits.get(tier, 100),
        )
        
        self.api_keys[key] = api_key
        
        logger.info(f"✅ API Key 已创建：{user_id} ({tier})")
        
        return api_key
    
    async def get_usage_stats(self, api_key: str) -> Dict:
        """获取使用统计"""
        if api_key not in self.api_keys:
            return {"error": "Invalid API Key"}
        
        key_info = self.api_keys[api_key]
        
        return {
            "user_id": key_info.user_id,
            "tier": key_info.tier,
            "calls_used": key_info.calls_limit - key_info.calls_remaining,
            "calls_remaining": key_info.calls_remaining,
            "calls_limit": key_info.calls_limit,
            "usage_percent": (key_info.calls_limit - key_info.calls_remaining) / key_info.calls_limit * 100,
        }


async def main():
    """测试主函数"""
    logger.info("🚀 AaaS Gateway 测试...")
    
    gateway = AAASGateway()
    
    # 创建 API Key
    api_key = await gateway.create_api_key("user_001", "personal")
    logger.info(f" API Key: {api_key.key[:8]}...")
    
    # 认证
    result = await gateway.authenticate(api_key.key)
    logger.info(f"✅ 认证结果：{result}")
    
    # 消耗配额
    await gateway.consume_quota(api_key.key)
    
    # 使用统计
    stats = await gateway.get_usage_stats(api_key.key)
    logger.info(f"📊 使用统计：{stats}")


if __name__ == '__main__':
    asyncio.run(main())
