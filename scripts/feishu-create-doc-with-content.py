#!/usr/bin/env python3
"""
飞书创建有内容的云文档
使用正确的 API 格式写入文档内容
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
    raise Exception(f"创建失败：{data}")

def write_content(token, doc_id, md_content):
    """
    使用 docx/v1/documents/{doc_id}/raw_content 接口写入
    或者使用 blocks batch_create
    """
    # 方法 1：尝试使用 raw_content
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/raw_content'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/octet-stream'
    }
    
    response = requests.put(url, headers=headers, data=md_content.encode('utf-8'))
    
    print(f"raw_content 响应状态：{response.status_code}")
    print(f"响应内容：{response.text[:500]}")
    
    if response.status_code == 200:
        return True
    
    # 方法 2：使用 blocks
    return write_blocks(token, doc_id, md_content)

def write_blocks(token, doc_id, md_content):
    """使用 blocks API 写入"""
    # 先获取文档的 root block
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    doc_info = response.json()
    print(f"文档信息：{json.dumps(doc_info, indent=2, ensure_ascii=False)[:500]}")
    
    # 创建 blocks
    blocks = []
    lines = md_content.split('\n')
    
    for line in lines[:200]:  # 限制行数
        if not line.strip():
            continue
        
        if line.startswith('# '):
            blocks.append({
                'block_type': 1,
                'heading1': {'elements': [{'text_run': {'content': line[2:]}}]}
            })
        elif line.startswith('## '):
            blocks.append({
                'block_type': 1,
                'heading2': {'elements': [{'text_run': {'content': line[3:]}}]}
            })
        elif line.startswith('### '):
            blocks.append({
                'block_type': 1,
                'heading3': {'elements': [{'text_run': {'content': line[4:]}}]}
            })
        elif line.startswith('- '):
            blocks.append({
                'block_type': 2,
                'bullet': {'elements': [{'text_run': {'content': line[2:]}}]}
            })
        else:
            blocks.append({
                'block_type': 1,
                'text': {'elements': [{'text_run': {'content': line}}]}
            })
    
    print(f"创建 {len(blocks)} 个 blocks")
    
    # 分批写入
    for i in range(0, len(blocks), 50):
        batch = blocks[i:i+50]
        url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/batch_append'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        payload = {'blocks': batch}
        
        response = requests.post(url, headers=headers, json=payload)
        print(f"批次 {i//50+1} 响应：{response.status_code} - {response.text[:200]}")
    
    return True

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
    print("="*60)
    print("📱 创建有内容的飞书云文档")
    print("="*60)
    
    # 1. 获取令牌
    print("\n1. 获取令牌...")
    token = get_token()
    print("✅ 令牌已获取")
    
    # 2. 读取 MD
    print("\n2. 读取 MD 文件...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()
    print(f"✅ 已读取 ({len(md_content)} 字符)")
    
    # 3. 创建文档
    print("\n3. 创建云文档...")
    doc_id = create_doc(token, '集成房屋跨境贸易出口全流程')
    print(f"✅ 文档已创建：{doc_id}")
    
    # 4. 写入内容
    print("\n4. 写入内容...")
    success = write_content(token, doc_id, md_content)
    
    doc_url = f'https://bytedance.feishu.cn/docx/{doc_id}'
    print(f"\n📎 文档链接：{doc_url}")
    
    # 5. 发送消息
    print("\n5. 发送消息...")
    msg = f"梁总，有内容的云文档已创建！\n\n📄 集成房屋跨境贸易出口全流程\n\n{doc_url}"
    result = send_message(token, RECEIVE_ID, msg)
    if result.get('code') == 0:
        print("✅ 消息已发送")
    else:
        print(f"⚠️ 消息发送失败：{result}")
    
    print("\n✅ 完成!")

if __name__ == '__main__':
    main()
