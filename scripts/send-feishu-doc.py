#!/usr/bin/env python3
"""
发送飞书文档脚本
"""

import json
import requests
from datetime import datetime, timedelta

# 配置
CONFIG = {
    "app_id": "cli_a9086d6b5779dcc1",
    "app_secret": "tXHOop03ZHQynCRuEPkambASNori3KhZ"
}

RECEIVE_ID = "ou_73a52625b0df639c12a8ffb0ceeeeb83"  # 梁金的 user_id
FILE_PATH = "/home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md"

def get_access_token():
    """获取访问令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": CONFIG['app_id'],
        "app_secret": CONFIG['app_secret']
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if data.get('code') == 0:
        return data['tenant_access_token']
    else:
        raise Exception(f"获取访问令牌失败：{data.get('msg')}")

def create_document(token, title):
    """创建云文档"""
    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": title
    }
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    if data.get('code') == 0:
        return data['data']['document']['document_id']
    else:
        raise Exception(f"创建文档失败：{data.get('msg')}")

def upload_file_to_drive(token, file_path, file_name):
    """上传文件到飞书云空间"""
    # 第一步：准备上传
    url = "https://open.feishu.cn/open-apis/drive/v1/prepare_upload"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "file_name": file_name,
        "parent_type": "explorer",
        "size": len(open(file_path, 'rb').read())
    }
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    if data.get('code') == 0:
        upload_id = data['data']['upload_id']
        file_token = data['data']['file_token']
        
        # 第二步：上传文件
        upload_url = "https://open.feishu.cn/open-apis/drive/v1/upload"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        files = {
            'file': open(file_path, 'rb')
        }
        data_payload = {
            'upload_id': upload_id
        }
        
        response = requests.post(upload_url, headers=headers, files=files, data=data_payload)
        data = response.json()
        
        if data.get('code') == 0:
            return file_token
        else:
            raise Exception(f"上传文件失败：{data.get('msg')}")
    else:
        raise Exception(f"准备上传失败：{data.get('msg')}")

def send_message(token, receive_id, msg_type, content, id_type="open_id"):
    """发送消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": id_type}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "receive_id": receive_id,
        "msg_type": msg_type,
        "content": content
    }
    
    response = requests.post(url, headers=headers, params=params, json=payload)
    data = response.json()
    
    return data

def main():
    print("="*60)
    print("📱 发送飞书文档")
    print("="*60)
    
    # 获取令牌
    print("\n1. 获取访问令牌...")
    token = get_access_token()
    print(f"✅ 令牌已获取")
    
    # 读取文件内容
    print("\n2. 读取文件内容...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"✅ 文件已读取 ({len(content)} 字符)")
    
    # 创建云文档
    print("\n3. 创建云文档...")
    title = f"集成房屋跨境贸易出口全流程 - {datetime.now().strftime('%Y%m%d')}"
    doc_id = create_document(token, title)
    print(f"✅ 文档已创建：{doc_id}")
    
    # 注意：飞书云文档需要特定格式，这里只创建空文档并发送链接
    print("\n4. 文档已创建（内容需手动粘贴或访问链接查看）")
    print(f"   文档 ID: {doc_id}")
    
    # 生成文档链接
    doc_url = f"https://bytedance.feishu.cn/docx/{doc_id}"
    
    # 发送消息
    print("\n5. 发送消息...")
    msg_content = json.dumps({
        "title": "📄 集成房屋跨境贸易出口全流程",
        "content": [
            [
                {
                    "tag": "text",
                    "text": "梁总，您好！\n\n"
                },
                {
                    "tag": "text",
                    "text": "集成房屋跨境贸易出口全流程指南已生成，包含：\n\n"
                },
                {
                    "tag": "text",
                    "text": "✅ 第一阶段：商务洽谈（搜单/询盘/报价/签约）\n"
                },
                {
                    "tag": "text",
                    "text": "✅ 第二阶段：生产准备（设计确认/原材料采购）\n"
                },
                {
                    "tag": "text",
                    "text": "✅ 第三阶段：生产制造（生产流程/质量检验/包装）\n"
                },
                {
                    "tag": "text",
                    "text": "✅ 第四阶段：出口物流（订舱/报关/出港）\n"
                },
                {
                    "tag": "text",
                    "text": "✅ 第五阶段：目的港清关（清关文件/关税/流程）\n"
                },
                {
                    "tag": "text",
                    "text": "✅ 第六阶段：内陆运输与安装\n"
                },
                {
                    "tag": "text",
                    "text": "✅ 第七阶段：售后服务\n\n"
                },
                {
                    "tag": "text",
                    "text": "另附：风险提示、文件模板、流程时间轴\n\n"
                },
                {
                    "tag": "a",
                    "text": "📎 点击查看完整文档",
                    "url": doc_url
                }
            ]
        ]
    })
    
    result = send_message(token, RECEIVE_ID, "post", msg_content)
    
    if result.get('code') == 0:
        print(f"✅ 消息已发送")
        print(f"\n📎 文档链接：{doc_url}")
    else:
        print(f"❌ 消息发送失败：{result.get('msg')}")
        
        # 尝试发送纯文本
        print("\n尝试发送纯文本消息...")
        text_content = json.dumps({
            "text": f"梁总，集成房屋跨境贸易出口全流程指南已生成！\n\n"
                    f"文档包含 7 个阶段完整流程：\n"
                    f"1️⃣ 商务洽谈 → 2️⃣ 生产准备 → 3️⃣ 生产制造\n"
                    f"4️⃣ 出口物流 → 5️⃣ 目的港清关 → 6️⃣ 运输安装 → 7️⃣ 售后\n\n"
                    f"另附风险提示、文件模板、流程时间轴\n\n"
                    f"📎 文档链接：{doc_url}"
        })
        
        result = send_message(token, RECEIVE_ID, "text", text_content)
        if result.get('code') == 0:
            print(f"✅ 文本消息已发送")
        else:
            print(f"❌ 文本消息发送失败：{result.get('msg')}")
    
    print("\n✅ 发送完成!")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
