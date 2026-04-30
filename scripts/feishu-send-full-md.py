#!/usr/bin/env python3
"""
飞书发送完整 MD 内容
使用富文本消息格式发送完整文档内容
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
    """获取访问令牌"""
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    payload = {'app_id': CONFIG['app_id'], 'app_secret': CONFIG['app_secret']}
    response = requests.post(url, json=payload)
    data = response.json()
    if data.get('code') == 0:
        return data['tenant_access_token']
    raise Exception(f"获取令牌失败：{data}")

def read_md_file():
    """读取 MD 文件"""
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def create_post_content(md_content):
    """
    创建飞书 post 消息内容
    飞书 post 消息支持简单的富文本格式
    """
    # 将 MD 内容转换为飞书 post 格式
    # post 消息格式：{"title": "xxx", "content": [[{"tag": "text", "text": "内容"}]]}
    
    lines = md_content.split('\n')
    content_elements = []
    
    for line in lines[:100]:  # 限制行数，避免消息过长
        if line.strip():
            # 处理标题
            if line.startswith('# '):
                content_elements.append({"tag": "text", "text": f"\n📌 {line[2:]}\n"})
            elif line.startswith('## '):
                content_elements.append({"tag": "text", "text": f"\n📍 {line[3:]}\n"})
            elif line.startswith('### '):
                content_elements.append({"tag": "text", "text": f"\n🔹 {line[4:]}\n"})
            elif line.startswith('- '):
                content_elements.append({"tag": "text", "text": f"  • {line[2:]}\n"})
            elif line.startswith('|'):
                # 表格行，简单处理
                content_elements.append({"tag": "text", "text": f"  {line}\n"})
            else:
                content_elements.append({"tag": "text", "text": f"{line}\n"})
    
    # 组合内容
    full_text = ''.join([elem['text'] for elem in content_elements])
    
    # 如果内容太长，截断并添加提示
    if len(full_text) > 1800:  # 飞书消息限制
        full_text = full_text[:1800] + "\n\n... 内容过长，请查看附件或云文档"
    
    return {
        "title": "集成房屋跨境贸易出口全流程",
        "content": [[{"tag": "text", "text": full_text}]]
    }

def send_post_message(token, receive_id, content):
    """发送 post 消息"""
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    params = {'receive_id_type': 'open_id'}
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        'receive_id': receive_id,
        'msg_type': 'post',
        'content': json.dumps(content)
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    return response.json()

def send_file_via_cloud_drive(token, file_path, file_name):
    """
    上传文件到飞书云空间并获取分享链接
    """
    # 第一步：准备上传
    url = 'https://open.feishu.cn/open-apis/drive/v1/prepare_upload'
    headers = {'Authorization': f'Bearer {token}'}
    
    file_size = len(open(file_path, 'rb').read())
    payload = {
        'file_name': file_name,
        'parent_type': 'explorer',
        'size': file_size
    }
    
    response = requests.post(url, headers=headers, json=payload)
    prep_data = response.json()
    
    if prep_data.get('code') != 0:
        print(f"准备上传失败：{prep_data}")
        return None
    
    upload_id = prep_data['data']['upload_id']
    
    # 第二步：上传文件
    url = 'https://open.feishu.cn/open-apis/drive/v1/upload'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': open(file_path, 'rb')}
    data = {'upload_id': upload_id}
    
    response = requests.post(url, headers=headers, files=files, data=data)
    upload_data = response.json()
    
    if upload_data.get('code') != 0:
        print(f"上传失败：{upload_data}")
        return None
    
    file_token = upload_data['data']['file_token']
    
    # 第三步：获取分享链接
    url = f'https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/share'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'scope': 'public'}
    
    response = requests.post(url, headers=headers, json=payload)
    share_data = response.json()
    
    if share_data.get('code') == 0:
        return share_data['data']['share_url']
    
    return None

def main():
    print("="*60)
    print("📱 飞书发送完整 MD 文档")
    print("="*60)
    
    # 1. 获取令牌
    print("\n1. 获取访问令牌...")
    token = get_token()
    print("✅ 令牌已获取")
    
    # 2. 读取 MD 文件
    print("\n2. 读取 MD 文件...")
    md_content = read_md_file()
    print(f"✅ 文件已读取 ({len(md_content)} 字符)")
    
    # 3. 创建 post 消息内容
    print("\n3. 创建消息内容...")
    content = create_post_content(md_content)
    print(f"✅ 消息内容已创建")
    
    # 4. 发送 post 消息
    print("\n4. 发送富文本消息...")
    result = send_post_message(token, RECEIVE_ID, content)
    if result.get('code') == 0:
        print("✅ 富文本消息已发送")
    else:
        print(f"⚠️  富文本消息发送失败：{result}")
    
    # 5. 尝试上传文件到云空间
    print("\n5. 上传 MD 文件到云空间...")
    file_name = '集成房屋跨境贸易出口全流程.md'
    share_url = send_file_via_cloud_drive(token, FILE_PATH, file_name)
    
    if share_url:
        print(f"✅ 文件已上传：{share_url}")
        
        # 发送文件链接
        msg_text = f"\n📎 MD 文件下载链接：{share_url}\n\n可直接下载查看完整文档内容"
        url = 'https://open.feishu.cn/open-apis/im/v1/messages'
        params = {'receive_id_type': 'open_id'}
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        payload = {
            'receive_id': RECEIVE_ID,
            'msg_type': 'text',
            'content': json.dumps({'text': msg_text})
        }
        response = requests.post(url, headers=headers, params=params, json=payload)
        if response.json().get('code') == 0:
            print("✅ 文件链接已发送")
    else:
        print("⚠️  文件上传失败，仅发送了文本消息")
    
    print("\n✅ 完成!")

if __name__ == '__main__':
    main()
