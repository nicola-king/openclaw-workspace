#!/usr/bin/env python3
"""发送飞书消息"""

import requests
import json

CONFIG = {
    'app_id': 'cli_a9086d6b5779dcc1',
    'app_secret': 'tXHOop03ZHQynCRuEPkambASNori3KhZ'
}

RECEIVE_ID = 'ou_73a52625b0df639c12a8ffb0ceeeeb83'
DOC_URL = 'https://bytedance.feishu.cn/docx/DVxRdWFfCogxe5xUrwbcY8N9n8f'

# 获取令牌
url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
payload = {'app_id': CONFIG['app_id'], 'app_secret': CONFIG['app_secret']}
response = requests.post(url, json=payload)
token_data = response.json()

if token_data.get('code') != 0:
    print(f"获取令牌失败：{token_data}")
    exit(1)

token = token_data['tenant_access_token']
print("✅ 令牌已获取")

# 发送文本消息
text = (
    "梁总，集成房屋跨境贸易出口全流程指南已生成！\n\n"
    "文档包含 7 个阶段完整流程：\n"
    "1️⃣ 商务洽谈 → 2️⃣ 生产准备 → 3️⃣ 生产制造\n"
    "4️⃣ 出口物流 → 5️⃣ 目的港清关 → 6️⃣ 运输安装 → 7️⃣ 售后\n\n"
    "另附风险提示、文件模板、流程时间轴\n\n"
    f"📎 文档链接：{DOC_URL}"
)

text_content = json.dumps({'text': text})

url = 'https://open.feishu.cn/open-apis/im/v1/messages'
params = {'receive_id_type': 'open_id'}
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
payload = {
    'receive_id': RECEIVE_ID,
    'msg_type': 'text',
    'content': text_content
}

response = requests.post(url, headers=headers, params=params, json=payload)
result = response.json()

if result.get('code') == 0:
    print(f"✅ 消息已发送成功！")
    print(f"📎 文档链接：{DOC_URL}")
else:
    print(f"❌ 消息发送失败：{result}")
    print(f"   错误：{result.get('msg')}")
