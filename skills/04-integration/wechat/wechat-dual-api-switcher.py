#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信通道双 API 服务自动切换

功能:
1. 主 API 失败时自动切换到备用 API
2. 健康检查 API 可用性
3. 自动记录 API 切换日志
4. 支持多个 API 服务轮询

灵感：ai-wechat 项目 (DeepSeek + 阿里百炼双 API)

作者：太一 AGI
创建：2026-04-14
"""

import os
import time
import logging
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime

# 日志配置
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('WechatDualAPI')


@dataclass
class APIConfig:
    """API 配置"""
    name: str
    base_url: str
    api_key: str
    model: str
    timeout: int = 30
    max_retries: int = 3


class WechatDualAPISwitcher:
    """微信双 API 切换器"""
    
    def __init__(self):
        self.primary_api: Optional[APIConfig] = None
        self.backup_api: Optional[APIConfig] = None
        self.current_api: Optional[APIConfig] = None
        self.switch_count = 0
        self.last_switch_time: Optional[datetime] = None
        
        # API 切换日志
        self.switch_log: List[Dict] = []
        
        # 加载配置
        self.load_config()
    
    def load_config(self):
        """加载 API 配置"""
        # 主 API (例如：DeepSeek)
        deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
        if deepseek_key:
            self.primary_api = APIConfig(
                name='DeepSeek',
                base_url='https://api.deepseek.com/v1',
                api_key=deepseek_key,
                model='deepseek-chat'
            )
            logger.info(f"✅ 主 API 已加载：{self.primary_api.name}")
        
        # 备用 API (例如：阿里百炼)
        bailian_key = os.getenv('BAILOIAN_API_KEY', '')
        if bailian_key:
            self.backup_api = APIConfig(
                name='阿里百炼',
                base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
                api_key=bailian_key,
                model='deepseek-chat'
            )
            logger.info(f"✅ 备用 API 已加载：{self.backup_api.name}")
        
        # 设置当前 API
        self.current_api = self.primary_api or self.backup_api
        
        if self.current_api:
            logger.info(f"🎯 当前 API: {self.current_api.name}")
        else:
            logger.warning("⚠️ 未配置任何 API")
    
    def check_api_health(self, api: APIConfig) -> bool:
        """检查 API 健康状态"""
        try:
            import requests
            
            response = requests.get(
                f"{api.base_url}/models",
                headers={'Authorization': f'Bearer {api.api_key}'},
                timeout=api.timeout
            )
            
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"❌ API 健康检查失败 {api.name}: {e}")
            return False
    
    def switch_api(self, reason: str = '自动切换'):
        """切换 API"""
        if not self.primary_api or not self.backup_api:
            logger.warning("⚠️ 只有一个 API，无法切换")
            return False
        
        # 切换
        if self.current_api == self.primary_api:
            self.current_api = self.backup_api
            logger.info(f"🔄 切换到备用 API: {self.backup_api.name}")
        else:
            self.current_api = self.primary_api
            logger.info(f"🔄 切换到主 API: {self.primary_api.name}")
        
        # 记录
        self.switch_count += 1
        self.last_switch_time = datetime.now()
        
        self.switch_log.append({
            'timestamp': self.last_switch_time.isoformat(),
            'from': self.current_api.name,
            'to': self.current_api.name,
            'reason': reason
        })
        
        logger.info(f"📊 累计切换次数：{self.switch_count}")
        return True
    
    def get_api(self) -> Optional[APIConfig]:
        """获取当前可用的 API"""
        if not self.current_api:
            logger.error("❌ 没有可用的 API")
            return None
        
        # 检查健康
        if self.check_api_health(self.current_api):
            return self.current_api
        
        # 尝试切换
        if self.switch_api('主 API 不可用'):
            return self.current_api
        
        logger.error("❌ 所有 API 都不可用")
        return None
    
    def request(self, endpoint: str, data: Dict, **kwargs) -> Optional[Dict]:
        """发送 API 请求（带自动切换）"""
        import requests
        
        api = self.get_api()
        if not api:
            return None
        
        # 重试逻辑
        for attempt in range(api.max_retries):
            try:
                logger.info(f"📡 发送请求到 {api.name} (尝试 {attempt + 1}/{api.max_retries})")
                
                response = requests.post(
                    f"{api.base_url}/{endpoint}",
                    headers={
                        'Authorization': f'Bearer {api.api_key}',
                        'Content-Type': 'application/json'
                    },
                    json=data,
                    timeout=api.timeout,
                    **kwargs
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ API 请求成功：{api.name}")
                    return response.json()
                else:
                    logger.warning(f"⚠️ API 返回错误：{response.status_code}")
                    
                    # 切换 API 重试
                    if attempt < api.max_retries - 1:
                        self.switch_api(f'HTTP {response.status_code}')
                        api = self.current_api
                    
            except Exception as e:
                logger.error(f"❌ API 请求失败：{e}")
                
                # 切换 API 重试
                if attempt < api.max_retries - 1:
                    self.switch_api(f'异常：{str(e)[:50]}')
                    api = self.current_api
        
        logger.error("❌ 所有 API 重试失败")
        return None
    
    def get_status(self) -> Dict:
        """获取 API 状态"""
        return {
            'primary_api': self.primary_api.name if self.primary_api else None,
            'backup_api': self.backup_api.name if self.backup_api else None,
            'current_api': self.current_api.name if self.current_api else None,
            'switch_count': self.switch_count,
            'last_switch_time': self.last_switch_time.isoformat() if self.last_switch_time else None,
            'total_switches': len(self.switch_log)
        }


# 全局实例
dual_api_switcher = WechatDualAPISwitcher()


def main():
    """测试"""
    print("🧪 测试双 API 切换器...")
    
    status = dual_api_switcher.get_status()
    print(f"\n📊 API 状态:")
    print(f"  主 API: {status['primary_api']}")
    print(f"  备用 API: {status['backup_api']}")
    print(f"  当前 API: {status['current_api']}")
    print(f"  切换次数：{status['switch_count']}")
    
    print("\n✅ 测试完成！")


if __name__ == '__main__':
    main()
