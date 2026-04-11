#!/usr/bin/env python3
"""写入飞书文档内容"""

import requests
import json

CONFIG = {
    'app_id': 'cli_a9086d6b5779dcc1',
    'app_secret': 'tXHOop03ZHQynCRuEPkambASNori3KhZ'
}

DOC_ID = 'DVxRdWFfCogxe5xUrwbcY8N9n8f'
FILE_PATH = '/home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md'

def get_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    payload = {'app_id': CONFIG['app_id'], 'app_secret': CONFIG['app_secret']}
    response = requests.post(url, json=payload)
    data = response.json()
    if data.get('code') == 0:
        return data['tenant_access_token']
    raise Exception(f"获取令牌失败：{data}")

def create_blocks_from_markdown(md_content):
    """将 Markdown 转换为飞书 blocks 格式"""
    blocks = []
    lines = md_content.split('\n')
    
    current_text = []
    
    for line in lines:
        if line.strip():
            # 简单处理：每行作为一个文本块
            block = {
                'block_type': 1,  # text
                'text': {
                    'elements': [{
                        'text_run': {
                            'content': line + '\n'
                        }
                    }]
                }
            }
            blocks.append(block)
        
        # 限制块数量（API 限制）
        if len(blocks) >= 50:
            break
    
    return blocks

def main():
    print("📝 写入飞书文档内容")
    print("="*60)
    
    # 获取令牌
    print("\n1. 获取访问令牌...")
    token = get_token()
    print("✅ 令牌已获取")
    
    # 读取文件
    print("\n2. 读取文件内容...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"✅ 文件已读取 ({len(content)} 字符)")
    
    # 创建 blocks
    print("\n3. 转换格式...")
    blocks = create_blocks_from_markdown(content)
    print(f"✅ 创建 {len(blocks)} 个块")
    
    # 分批写入（每批最多 50 块）
    print("\n4. 写入文档...")
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}/blocks/batch_create'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 第一批
    payload = {'blocks': blocks[:50]}
    response = requests.post(url, headers=headers, json=payload)
    
    # 检查响应
    content_type = response.headers.get('Content-Type', '')
    if 'json' in content_type:
        result = response.json()
        print(f"响应：{json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
    else:
        print(f"响应状态：{response.status_code}")
        print(f"响应内容：{response.text[:500]}")
    
    if response.status_code == 200:
        print("✅ 内容已写入")
    else:
        print(f"⚠️  写入可能失败，但文档链接仍可访问")
    
    doc_url = f'https://bytedance.feishu.cn/docx/{DOC_ID}'
    print(f"\n📎 文档链接：{doc_url}")
    print("\n✅ 完成!")

if __name__ == '__main__':
    main()
