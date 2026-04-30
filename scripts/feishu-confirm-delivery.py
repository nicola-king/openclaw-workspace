#!/usr/bin/env python3
"""发送确认消息"""

import requests
import json

CONFIG = {
    'app_id': 'cli_a9086d6b5779dcc1',
    'app_secret': 'tXHOop03ZHQynCRuEPkambASNori3KhZ'
}

RECEIVE_ID = 'ou_73a52625b0df639c12a8ffb0ceeeeb83'

def get_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    payload = {'app_id': CONFIG['app_id'], 'app_secret': CONFIG['app_secret']}
    response = requests.post(url, json=payload)
    return response.json().get('tenant_access_token')

def send_message(token, receive_id, text):
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
    token = get_token()
    
    msg = """📄 文档交付确认

梁总，完整文档已通过 10 条飞书消息发送：

✅ 引导消息 ×1
✅ 正文内容 ×8 段
✅ 结束消息 ×1

内容包含：
• 7 个阶段完整流程
• 各方职责划分
• 关键文件模板
• 风险提示与应对
• 流程时间轴

📁 本地备份：
/home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md

⚠️ 飞书云文档 API 限制说明：
飞书企业版才支持通过 API 创建有内容的云文档。当前账号为免费版，只能通过消息发送内容。

如需飞书云文档格式，可：
1. 复制上述消息内容
2. 新建飞书云文档
3. 粘贴内容即可

请确认是否收到完整内容！"""

    result = send_message(token, RECEIVE_ID, msg)
    if result.get('code') == 0:
        print("✅ 确认消息已发送")
    else:
        print(f"发送失败：{result}")

if __name__ == '__main__':
    main()
