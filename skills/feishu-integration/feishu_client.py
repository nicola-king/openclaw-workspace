#!/usr/bin/env python3
"""
📱 飞书客户端

太一 AGI 飞书集成核心模块
支持消息收发/文档读写/多维表格操作

作者：太一 AGI
创建：2026-04-11
"""

import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class FeishuClient:
    """飞书客户端"""
    
    def __init__(self, config_path: str = None):
        """初始化客户端"""
        self.config_path = config_path or "/home/nicola/.openclaw/workspace/config/feishu/config.json"
        self.config = self._load_config()
        self.access_token = None
        self.token_expires_at = None
        
        print("📱 飞书客户端已初始化")
        print(f"   App ID: {self.config.get('app_id', 'N/A')}")
        print()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        config_file = Path(self.config_path)
        if not config_file.exists():
            print(f"⚠️  配置文件不存在：{config_file}")
            print(f"   请创建配置文件并填写 App ID 和 App Secret")
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_access_token(self) -> str:
        """获取访问令牌"""
        # 检查缓存
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # 请求新令牌
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.config['app_id'],
            "app_secret": self.config['app_secret']
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get('code') == 0:
            self.access_token = data['tenant_access_token']
            self.token_expires_at = datetime.now() + timedelta(seconds=data['expire'] - 60)
            print(f"✅ 访问令牌已获取 (有效期：{data['expire']}秒)")
            return self.access_token
        else:
            print(f"❌ 获取访问令牌失败：{data}")
            raise Exception(f"获取访问令牌失败：{data.get('msg')}")
    
    def _request(self, method: str, url: str, **kwargs) -> Dict:
        """发送 HTTP 请求"""
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f"Bearer {self._get_access_token()}"
        kwargs['headers'] = headers
        
        response = requests.request(method, url, **kwargs)
        return response.json()
    
    # ═══════════════════════════════════════════════════════════
    # 消息功能
    # ═══════════════════════════════════════════════════════════
    
    def send_message(self, receive_id: str, content: str, msg_type: str = "text") -> Dict:
        """发送消息"""
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        params = {"receive_id_type": "user_id"}
        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": content
        }
        
        result = self._request("POST", url, params=params, json=payload)
        
        if result.get('code') == 0:
            print(f"✅ 消息已发送：{receive_id}")
            return result
        else:
            print(f"❌ 消息发送失败：{result}")
            return result
    
    def send_text_message(self, receive_id: str, text: str) -> Dict:
        """发送文本消息"""
        content = json.dumps({"text": text})
        return self.send_message(receive_id, content, "text")
    
    def send_markdown_message(self, receive_id: str, markdown: str) -> Dict:
        """发送 Markdown 消息"""
        content = json.dumps({"title": "消息", "content": markdown})
        return self.send_message(receive_id, content, "post")
    
    def send_card_message(self, receive_id: str, card: Dict) -> Dict:
        """发送卡片消息"""
        content = json.dumps(card)
        return self.send_message(receive_id, content, "interactive")
    
    # ═══════════════════════════════════════════════════════════
    # 文档功能
    # ═══════════════════════════════════════════════════════════
    
    def read_document(self, document_id: str) -> Dict:
        """读取文档"""
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}"
        result = self._request("GET", url)
        
        if result.get('code') == 0:
            print(f"✅ 文档已读取：{document_id}")
            return result['data']
        else:
            print(f"❌ 文档读取失败：{result}")
            return result
    
    def write_document(self, document_id: str, content: str) -> Dict:
        """写入文档"""
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/content"
        payload = {
            "content": content
        }
        
        result = self._request("PUT", url, json=payload)
        
        if result.get('code') == 0:
            print(f"✅ 文档已写入：{document_id}")
            return result['data']
        else:
            print(f"❌ 文档写入失败：{result}")
            return result
    
    def create_document(self, title: str, folder_token: str = None) -> Dict:
        """创建文档"""
        url = "https://open.feishu.cn/open-apis/docx/v1/documents"
        payload = {
            "title": title
        }
        if folder_token:
            payload["folder_token"] = folder_token
        
        result = self._request("POST", url, json=payload)
        
        if result.get('code') == 0:
            print(f"✅ 文档已创建：{title}")
            return result['data']
        else:
            print(f"❌ 文档创建失败：{result}")
            return result
    
    # ═══════════════════════════════════════════════════════════
    # 多维表格功能
    # ═══════════════════════════════════════════════════════════
    
    def get_bitable_records(self, app_id: str, table_id: str) -> Dict:
        """获取多维表格记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
        result = self._request("GET", url)
        
        if result.get('code') == 0:
            print(f"✅ 表格记录已获取：{app_id}/{table_id}")
            return result['data']
        else:
            print(f"❌ 表格记录获取失败：{result}")
            return result
    
    def create_bitable_record(self, app_id: str, table_id: str, fields: Dict) -> Dict:
        """创建多维表格记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records"
        payload = {
            "fields": fields
        }
        
        result = self._request("POST", url, json=payload)
        
        if result.get('code') == 0:
            print(f"✅ 表格记录已创建：{app_id}/{table_id}")
            return result['data']
        else:
            print(f"❌ 表格记录创建失败：{result}")
            return result
    
    def update_bitable_record(self, app_id: str, table_id: str, record_id: str, fields: Dict) -> Dict:
        """更新多维表格记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records/{record_id}"
        payload = {
            "fields": fields
        }
        
        result = self._request("PUT", url, json=payload)
        
        if result.get('code') == 0:
            print(f"✅ 表格记录已更新：{app_id}/{table_id}/{record_id}")
            return result['data']
        else:
            print(f"❌ 表格记录更新失败：{result}")
            return result
    
    # ═══════════════════════════════════════════════════════════
    # 用户功能
    # ═══════════════════════════════════════════════════════════
    
    def get_user_info(self, user_id: str) -> Dict:
        """获取用户信息"""
        url = f"https://open.feishu.cn/open-apis/contact/v3/users/{user_id}"
        params = {"user_id_type": "user_id"}
        result = self._request("GET", url, params=params)
        
        if result.get('code') == 0:
            print(f"✅ 用户信息已获取：{user_id}")
            return result['data']
        else:
            print(f"❌ 用户信息获取失败：{result}")
            return result
    
    # ═══════════════════════════════════════════════════════════
    # 工具方法
    # ═══════════════════════════════════════════════════════════
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            token = self._get_access_token()
            print(f"✅ 飞书连接测试成功")
            return True
        except Exception as e:
            print(f"❌ 飞书连接测试失败：{e}")
            return False
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "config_loaded": bool(self.config),
            "token_cached": bool(self.access_token),
            "token_expires_at": self.token_expires_at.isoformat() if self.token_expires_at else None
        }


def main():
    """主函数 - 测试"""
    print("="*60)
    print("📱 飞书客户端测试")
    print("="*60)
    
    # 初始化客户端
    client = FeishuClient()
    
    # 测试连接
    print("\n1. 测试连接...")
    if client.test_connection():
        print("✅ 连接成功")
    else:
        print("❌ 连接失败")
        return 1
    
    # 获取统计
    print("\n2. 获取统计...")
    stats = client.get_statistics()
    print(f"   配置已加载：{stats['config_loaded']}")
    print(f"   令牌已缓存：{stats['token_cached']}")
    
    print("\n✅ 飞书客户端测试完成!")
    print("   请配置 ~/.openclaw/workspace/config/feishu/config.json 后使用完整功能")
    
    return 0


if __name__ == "__main__":
    from datetime import timedelta
    import sys
    sys.exit(main())
