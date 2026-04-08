#!/usr/bin/env python3
"""
企业微信消息发送器

用法:
    python3 wecom_sender.py --corp_id "wwxxx" --agent_id "1001" --secret "xxx" --user "nicola" --message "测试"
"""

import json
import argparse
import requests
from pathlib import Path

class WeComSender:
    """企业微信发送器"""
    
    def __init__(self, corp_id, agent_id, secret):
        self.corp_id = corp_id
        self.agent_id = agent_id
        self.secret = secret
        self.access_token = None
        
    def get_access_token(self):
        """获取访问令牌"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.corp_id,
            "corpsecret": self.secret
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("errcode") == 0:
            self.access_token = data["access_token"]
            return True
        else:
            print(f"❌ 获取 Token 失败：{data}")
            return False
    
    def send_message(self, user_id, message, msg_type="text"):
        """发送消息"""
        if not self.access_token:
            if not self.get_access_token():
                return False
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        
        payload = {
            "touser": user_id,
            "msgtype": msg_type,
            "agentid": int(self.agent_id),
            "text": {
                "content": message
            },
            "safe": 0
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get("errcode") == 0:
            print(f"✅ 消息已发送给 {user_id}")
            return True
        else:
            print(f"❌ 发送失败：{data}")
            return False

def main():
    parser = argparse.ArgumentParser(description="企业微信消息发送器")
    parser.add_argument("--corp_id", required=True, help="企业 ID")
    parser.add_argument("--agent_id", required=True, help="应用 ID")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--message", required=True, help="消息内容")
    
    args = parser.parse_args()
    
    sender = WeComSender(args.corp_id, args.agent_id, args.secret)
    sender.send_message(args.user, args.message)

if __name__ == "__main__":
    main()
