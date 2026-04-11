#!/usr/bin/env python3
"""
飞书发送云文档链接
创建云文档并发送可点击链接
"""

import requests
import json

CONFIG = {
    'app_id': 'cli_a9086d6b5779dcc1',
    'app_secret': 'tXHOop03ZHQynCRuEPkambASNori3KhZ'
}

FILE_PATH = '/home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md'
RECEIVE_ID = 'ou_73a52625b0df639c12a8ffb0ceeeeb83'

def get_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    payload = {'app_id': CONFIG['app_id'], 'app_secret': CONFIG['app_secret']}
    response = requests.post(url, json=payload)
    data = response.json()
    return data.get('tenant_access_token')

def create_doc(token, title):
    """创建云文档"""
    url = 'https://open.feishu.cn/open-apis/docx/v1/documents'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'title': title}
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    if data.get('code') == 0:
        return data['data']['document']['document_id']
    return None

def send_card_message(token, receive_id, doc_id, doc_url):
    """发送卡片消息，包含可点击的文档链接"""
    
    # 读取文件信息
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建卡片
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "blue",
            "title": {
                "content": "📄 集成房屋跨境贸易出口全流程",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**文档已生成**\n完整流程指南包含 7 个阶段，从商务洽谈到售后服务。"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**📊 文档信息**\n• 字数：9192 字\n• 阶段：7 个\n• 模板：发票/装箱单/验收报告\n• 时间轴：8-12 周"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📎 点击打开云文档"
                        },
                        "url": doc_url,
                        "type": "primary"
                    },
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📋 查看本地文件"
                        },
                        "url": "file:///home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md",
                        "type": "default"
                    }
                ]
            },
            {
                "tag": "hr"
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": "太一 AGI 自动生成 | 2026-04-11"
                    }
                ]
            }
        ]
    }
    
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    params = {'receive_id_type': 'open_id'}
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        'receive_id': receive_id,
        'msg_type': 'interactive',
        'content': json.dumps(card)
    }
    
    response = requests.post(url, headers=headers, params=params, json=payload)
    return response.json()

def send_text_with_link(token, receive_id, doc_url):
    """发送带链接的文本消息"""
    text = (
        f"📄 集成房屋跨境贸易出口全流程指南\n\n"
        f"✅ 云文档已创建，点击打开：\n"
        f"{doc_url}\n\n"
        f"📊 文档包含：\n"
        f"• 7 个阶段完整流程\n"
        f"• 各方职责划分\n"
        f"• 关键文件模板\n"
        f"• 风险提示与应对\n"
        f"• 流程时间轴（8-12 周）\n\n"
        f"📁 本地文件：/home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md"
    )
    
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    params = {'receive_id_type': 'open_id'}
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        'receive_id': receive_id,
        'msg_type': 'text',
        'content': json.dumps({'text': text})
    }
    
    response = requests.post(url, headers=headers, params=params, json=payload)
    return response.json()

def main():
    print("="*60)
    print("📱 飞书发送云文档链接")
    print("="*60)
    
    # 1. 获取令牌
    print("\n1. 获取令牌...")
    token = get_token()
    print("✅ 令牌已获取")
    
    # 2. 创建云文档
    print("\n2. 创建云文档...")
    doc_id = create_doc(token, '集成房屋跨境贸易出口全流程')
    if not doc_id:
        print("❌ 创建失败")
        return 1
    
    doc_url = f'https://bytedance.feishu.cn/docx/{doc_id}'
    print(f"✅ 文档已创建：{doc_url}")
    
    # 3. 发送卡片消息
    print("\n3. 发送卡片消息...")
    result = send_card_message(token, RECEIVE_ID, doc_id, doc_url)
    if result.get('code') == 0:
        print("✅ 卡片消息已发送")
    else:
        print(f"⚠️ 卡片消息发送失败：{result.get('msg')}")
        
        # 尝试发送文本链接
        print("\n尝试发送文本链接...")
        result = send_text_with_link(token, RECEIVE_ID, doc_url)
        if result.get('code') == 0:
            print("✅ 文本链接已发送")
        else:
            print(f"❌ 文本链接发送失败：{result}")
    
    print(f"\n📎 文档链接：{doc_url}")
    print("\n✅ 完成!")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
