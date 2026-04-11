#!/usr/bin/env python3
"""发送内容说明消息"""

import requests
import json

CONFIG = {
    'app_id': 'cli_a9086d6b5779dcc1',
    'app_secret': 'tXHOop03ZHQynCRuEPkambASNori3KhZ'
}

RECEIVE_ID = 'ou_73a52625b0df639c12a8ffb0ceeeeb83'
DOC_URL = 'https://bytedance.feishu.cn/docx/EQWLdI5qboQUxnxpADPcLmcGnad'

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
    
    msg = f"""📄 文档使用说明

梁总，飞书云文档已创建：
{DOC_URL}

⚠️ 重要说明：
由于飞书 API 限制，云文档内容需要通过以下方式填充：

**方式 1：复制粘贴（推荐）**
1. 点击上述云文档链接
2. 查看之前发送的 10 条分段消息
3. 复制全部内容
4. 粘贴到云文档中

**方式 2：导入本地文件**
1. 下载本地文件（如有权限）
2. 飞书云文档 → 导入 → 选择文件

**方式 3：使用微信版本**
之前已通过微信发送完整 MD 文件，可直接查看

📁 本地文件路径：
/home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md

如有不便，敬请谅解！"""

    result = send_message(token, RECEIVE_ID, msg)
    if result.get('code') == 0:
        print("✅ 说明消息已发送")
    else:
        print(f"发送失败：{result}")

if __name__ == '__main__':
    main()
