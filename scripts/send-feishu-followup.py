#!/usr/bin/env python3
"""发送跟进消息"""

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
    data = response.json()
    return data.get('tenant_access_token')

def send_message(text):
    token = get_token()
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
    return response.json()

# 发送跟进消息
text = """📄 补充说明：

完整文档已保存至：
/home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md

文档内容包含：
✅ 7 个阶段完整流程（商务→生产→物流→清关→安装→售后）
✅ 各方职责划分（甲方/乙方/贸易商）
✅ 关键文件模板（发票/装箱单/验收报告）
✅ 风险提示与应对措施
✅ 流程时间轴参考（8-12 周）

如需飞书云文档版本，可手动复制上述文件内容到飞书文档。

有任何疑问随时联系我！"""

result = send_message(text)
if result.get('code') == 0:
    print("✅ 跟进消息已发送")
else:
    print(f"❌ 发送失败：{result}")
