#!/usr/bin/env python3
"""
飞书知识库上传文档
使用知识库 API 创建有内容的页面
"""

import requests
import json
import base64

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

def create_wiki_node(token, space_id, title, parent_id=None):
    """创建知识库节点"""
    url = 'https://open.feishu.cn/open-apis/wiki/v1/nodes'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        'space_id': space_id,
        'title': title,
        'parent_id': parent_id,
        'node_type': 'doc'
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    print(f"创建知识库节点响应：{json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
    return data

def upload_file_to_drive(token, file_path, file_name):
    """上传文件到飞书云空间"""
    # 准备上传
    url = 'https://open.feishu.cn/open-apis/drive/v1/prepare_upload'
    headers = {'Authorization': f'Bearer {token}'}
    
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    payload = {
        'file_name': file_name,
        'parent_type': 'explorer',
        'size': len(file_content)
    }
    
    response = requests.post(url, headers=headers, json=payload)
    prep_data = response.json()
    print(f"准备上传响应：{json.dumps(prep_data, indent=2, ensure_ascii=False)[:300]}")
    
    if prep_data.get('code') != 0:
        return None
    
    upload_id = prep_data['data']['upload_id']
    
    # 上传文件
    url = 'https://open.feishu.cn/open-apis/drive/v1/upload'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': (file_name, file_content, 'text/markdown')}
    data = {'upload_id': upload_id}
    
    response = requests.post(url, headers=headers, files=files, data=data)
    upload_data = response.json()
    print(f"上传文件响应：{json.dumps(upload_data, indent=2, ensure_ascii=False)[:300]}")
    
    if upload_data.get('code') != 0:
        return None
    
    return upload_data['data']['file_token']

def get_file_share_url(token, file_token):
    """获取文件分享链接"""
    url = f'https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/share'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'scope': 'public'}
    
    response = requests.post(url, headers=headers, json=payload)
    share_data = response.json()
    print(f"分享链接响应：{json.dumps(share_data, indent=2, ensure_ascii=False)[:300]}")
    
    if share_data.get('code') == 0:
        return share_data['data']['share_url']
    return None

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
    print("📱 飞书上传 MD 文件")
    print("="*60)
    
    # 1. 获取令牌
    print("\n1. 获取令牌...")
    token = get_token()
    print("✅ 令牌已获取")
    
    # 2. 上传文件
    print("\n2. 上传 MD 文件到云空间...")
    file_name = '集成房屋跨境贸易出口全流程.md'
    file_token = upload_file_to_drive(token, FILE_PATH, file_name)
    
    if file_token:
        print(f"✅ 文件已上传，token: {file_token}")
        
        # 3. 获取分享链接
        print("\n3. 获取分享链接...")
        share_url = get_file_share_url(token, file_token)
        
        if share_url:
            print(f"✅ 分享链接：{share_url}")
            
            # 4. 发送消息
            print("\n4. 发送消息...")
            msg = (
                f"梁总，集成房屋跨境贸易出口全流程文档已上传！\n\n"
                f"📄 文件格式：Markdown\n"
                f"📎 下载/查看链接：{share_url}\n\n"
                f"文档包含 7 个阶段完整流程，可直接下载查看或导入飞书云文档。"
            )
            result = send_message(token, RECEIVE_ID, msg)
            if result.get('code') == 0:
                print("✅ 消息已发送")
            else:
                print(f"⚠️ 消息发送失败：{result}")
        else:
            print("⚠️ 获取分享链接失败")
    else:
        print("❌ 文件上传失败")
    
    print("\n✅ 完成!")

if __name__ == '__main__':
    main()
