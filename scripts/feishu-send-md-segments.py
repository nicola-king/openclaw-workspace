#!/usr/bin/env python3
"""
飞书分段发送 MD 文档
将长文档分成多段消息发送
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

def split_content(content, max_length=1800):
    """
    将内容分割成多段，每段不超过 max_length 字符
    尽量按章节分割
    """
    segments = []
    
    # 按章节分割 (## 标题)
    chapters = content.split('\n## ')
    
    current_segment = ""
    
    for chapter in chapters:
        if not chapter.strip():
            continue
        
        # 添加章节标记
        chapter_text = chapter if chapter.startswith('# ') else f"## {chapter}"
        
        if len(current_segment) + len(chapter_text) <= max_length:
            current_segment += chapter_text + "\n\n"
        else:
            if current_segment:
                segments.append(current_segment)
            current_segment = chapter_text + "\n\n"
    
    if current_segment:
        segments.append(current_segment)
    
    # 如果单段还是太长，强制分割
    final_segments = []
    for seg in segments:
        if len(seg) <= max_length:
            final_segments.append(seg)
        else:
            # 按行分割
            lines = seg.split('\n')
            temp_seg = ""
            for line in lines:
                if len(temp_seg) + len(line) <= max_length:
                    temp_seg += line + "\n"
                else:
                    if temp_seg:
                        final_segments.append(temp_seg)
                    temp_seg = line + "\n"
            if temp_seg:
                final_segments.append(temp_seg)
    
    return final_segments

def send_text_message(token, receive_id, text):
    """发送文本消息"""
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
    print("📱 飞书分段发送 MD 文档")
    print("="*60)
    
    # 1. 获取令牌
    print("\n1. 获取访问令牌...")
    token = get_token()
    print("✅ 令牌已获取")
    
    # 2. 读取 MD 文件
    print("\n2. 读取 MD 文件...")
    md_content = read_md_file()
    print(f"✅ 文件已读取 ({len(md_content)} 字符)")
    
    # 3. 分割内容
    print("\n3. 分割内容...")
    segments = split_content(md_content, max_length=1800)
    print(f"✅ 分割为 {len(segments)} 段")
    
    # 4. 发送引导消息
    print("\n4. 发送引导消息...")
    intro_text = (
        "📄 集成房屋跨境贸易出口全流程指南\n\n"
        "梁总，完整文档将分多条消息发送，包含：\n\n"
        "✅ 第一阶段：商务洽谈\n"
        "✅ 第二阶段：生产准备\n"
        "✅ 第三阶段：生产制造\n"
        "✅ 第四阶段：出口物流\n"
        "✅ 第五阶段：目的港清关\n"
        "✅ 第六阶段：内陆运输与安装\n"
        "✅ 第七阶段：售后服务\n\n"
        "另附：风险提示、文件模板、流程时间轴\n\n"
        f"共 {len(segments)} 条消息，以下是完整内容↓\n"
        "="*50
    )
    
    result = send_text_message(token, RECEIVE_ID, intro_text)
    if result.get('code') == 0:
        print("✅ 引导消息已发送")
    else:
        print(f"⚠️  引导消息发送失败：{result}")
    
    # 5. 分段发送
    print("\n5. 分段发送内容...")
    for i, segment in enumerate(segments, 1):
        msg_text = f"[{i}/{len(segments)}]\n\n{segment}"
        result = send_text_message(token, RECEIVE_ID, msg_text)
        
        if result.get('code') == 0:
            print(f"   ✅ 段 {i}/{len(segments)} 已发送")
        else:
            print(f"   ⚠️  段 {i}/{len(segments)} 发送失败：{result.get('msg')}")
        
        # 避免频率限制
        import time
        time.sleep(0.5)
    
    # 6. 发送结束消息
    print("\n6. 发送结束消息...")
    outro_text = (
        "=================================================="
        "\n✅ 完整文档已发送完毕！\n\n"
        "📁 本地文件位置：\n"
        "/home/nicola/.openclaw/workspace/reports/集成房屋跨境贸易出口全流程.md\n\n"
        "如有任何问题或需要调整，随时联系我！"
    )
    
    result = send_text_message(token, RECEIVE_ID, outro_text)
    if result.get('code') == 0:
        print("✅ 结束消息已发送")
    else:
        print(f"⚠️  结束消息发送失败：{result}")
    
    print("\n✅ 完成！共发送 {len(segments)+2} 条消息")

if __name__ == '__main__':
    main()
