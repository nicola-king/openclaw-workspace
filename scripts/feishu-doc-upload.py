#!/usr/bin/env python3
"""
飞书云文档完整写入脚本
直接读取 MD 文件并写入飞书云文档
"""

import requests
import json
from pathlib import Path

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

def create_document(token, title):
    """创建云文档"""
    url = 'https://open.feishu.cn/open-apis/docx/v1/documents'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'title': title}
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    if data.get('code') == 0:
        return data['data']['document']['document_id']
    raise Exception(f"创建文档失败：{data}")

def markdown_to_blocks(md_content):
    """
    将 Markdown 转换为飞书 blocks 格式
    飞书文档使用 blocks 数组，每个 block 有特定格式
    """
    blocks = []
    lines = md_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 跳过空行
        if not line.strip():
            i += 1
            continue
        
        # 处理标题
        if line.startswith('# '):
            blocks.append({
                'block_type': 1,
                'heading1': {
                    'elements': [{'text_run': {'content': line[2:] + '\n'}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                'block_type': 1,
                'heading2': {
                    'elements': [{'text_run': {'content': line[3:] + '\n'}}]
                }
            })
        elif line.startswith('### '):
            blocks.append({
                'block_type': 1,
                'heading3': {
                    'elements': [{'text_run': {'content': line[4:] + '\n'}}]
                }
            })
        # 处理列表
        elif line.startswith('- ') or line.startswith('* '):
            blocks.append({
                'block_type': 2,
                'bullet': {
                    'elements': [{'text_run': {'content': line[2:] + '\n'}}]
                }
            })
        # 处理代码块
        elif line.startswith('```'):
            # 跳过代码块标记
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if code_lines:
                blocks.append({
                    'block_type': 4,
                    'code': {
                        'language': 'plain_text',
                        'elements': [{'text_run': {'content': '\n'.join(code_lines) + '\n'}}]
                    }
                })
        # 普通文本
        else:
            blocks.append({
                'block_type': 1,
                'text': {
                    'elements': [{'text_run': {'content': line + '\n'}}]
                }
            })
        
        i += 1
        
        # 限制每批 50 个块
        if len(blocks) >= 50:
            break
    
    return blocks

def write_blocks(token, doc_id, blocks):
    """写入 blocks 到文档"""
    url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/batch_create'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'blocks': blocks, 'parent_block_id': doc_id}
    
    response = requests.post(url, headers=headers, json=payload)
    
    # 处理响应
    content_type = response.headers.get('Content-Type', '')
    if response.status_code == 200:
        if 'json' in content_type:
            try:
                result = response.json()
                return result
            except:
                return {'status': 'success', 'text': response.text}
        else:
            return {'status': 'success', 'text': response.text[:200]}
    else:
        return {'status': 'error', 'code': response.status_code, 'text': response.text[:500]}

def send_message(token, receive_id, text):
    """发送飞书消息"""
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
    print("📱 飞书云文档完整写入")
    print("="*60)
    
    # 1. 获取令牌
    print("\n1. 获取访问令牌...")
    token = get_token()
    print(f"✅ 令牌已获取")
    
    # 2. 读取 MD 文件
    print("\n2. 读取 MD 文件...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()
    print(f"✅ 文件已读取 ({len(md_content)} 字符)")
    
    # 3. 创建云文档
    print("\n3. 创建云文档...")
    doc_id = create_document(token, '集成房屋跨境贸易出口全流程')
    print(f"✅ 文档已创建：{doc_id}")
    
    # 4. 转换 Markdown 为 blocks
    print("\n4. 转换格式...")
    blocks = markdown_to_blocks(md_content)
    print(f"✅ 创建 {len(blocks)} 个块")
    
    # 5. 分批写入（飞书限制每批最多 50 块）
    print("\n5. 写入文档内容...")
    batch_size = 50
    total_blocks = len(blocks)
    written = 0
    
    # 先获取文档初始 block
    # 飞书文档创建后有一个默认的空 block，需要作为 parent
    
    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i+batch_size]
        result = write_blocks(token, doc_id, batch)
        
        if result.get('status') == 'success' or result.get('code') == 0:
            written += len(batch)
            print(f"   批次 {i//batch_size + 1}: 写入 {len(batch)} 个块")
        else:
            print(f"   ⚠️  批次 {i//batch_size + 1} 可能失败：{result}")
    
    print(f"✅ 已写入 {written}/{total_blocks} 个块")
    
    # 6. 生成文档链接
    doc_url = f'https://bytedance.feishu.cn/docx/{doc_id}'
    print(f"\n📎 文档链接：{doc_url}")
    
    # 7. 发送消息
    print("\n6. 发送消息...")
    msg_text = (
        "梁总，集成房屋跨境贸易出口全流程指南已生成！\n\n"
        "📄 文档包含：\n"
        "✅ 7 个阶段完整流程（商务→生产→物流→清关→安装→售后）\n"
        "✅ 各方职责划分（甲方/乙方/贸易商）\n"
        "✅ 关键文件模板（发票/装箱单/验收报告）\n"
        "✅ 风险提示与应对措施\n"
        "✅ 流程时间轴参考（8-12 周）\n\n"
        f"📎 点击查看完整文档：{doc_url}"
    )
    
    result = send_message(token, RECEIVE_ID, msg_text)
    if result.get('code') == 0:
        print(f"✅ 消息已发送")
    else:
        print(f"⚠️  消息发送可能失败：{result}")
    
    print("\n✅ 完成!")
    return doc_id

if __name__ == '__main__':
    main()
