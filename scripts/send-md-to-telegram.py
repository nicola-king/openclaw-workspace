#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
发送 MD 文件到 Telegram 会话

功能:
1. 读取 MD 文件
2. 通过 Telegram Bot API 发送文件到会话
3. 从 MD 文件动态提取内容生成说明
4. 消息去重 (防止重复发送)
5. 文件锁 (防止并发执行)

作者：太一 AGI
创建：2026-04-13
修订：2026-04-25 (添加去重 + 锁机制)
"""

import os
import sys
import json
import hashlib
import fcntl
import requests
from pathlib import Path
from datetime import datetime, timedelta

# 配置

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8351068758:AAGtRXv2u5fGAMuVY3d5hmeKgV9tAFpCMLY")
TELEGRAM_CHAT_ID = "7073481596"  # SAYELF 的 Telegram ID

# Telegram Bot API

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# 去重配置

DEDUP_DIR = WORKSPACE / "data" / "telegram-dedup"
DEDUP_FILE = DEDUP_DIR / "sent-messages.json"
LOCK_FILE = Path("/tmp/send-md-to-telegram.lock")
DEDUP_TTL_HOURS = 24  # 去重记录保留 24 小时


def ensure_dedup_dir():
    """确保去重目录存在"""
    DEDUP_DIR.mkdir(parents=True, exist_ok=True)


def load_sent_messages() -> dict:
    """加载已发送消息记录"""
    ensure_dedup_dir()
    if DEDUP_FILE.exists():
        try:
            with open(DEDUP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_sent_messages(records: dict):
    """保存已发送消息记录"""
    ensure_dedup_dir()
    # 清理过期记录
    cutoff = (datetime.now() - timedelta(hours=DEDUP_TTL_HOURS)).isoformat()
    records = {k: v for k, v in records.items() if v.get('sent_at', '') > cutoff}
    
    with open(DEDUP_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def compute_message_hash(file_path: str) -> str:
    """计算文件内容的哈希值（用于去重）"""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()[:16]
    except IOError:
        return ""


def is_already_sent(file_hash: str) -> bool:
    """检查消息是否已发送"""
    if not file_hash:
        return False
    records = load_sent_messages()
    return file_hash in records


def mark_as_sent(file_hash: str, file_path: str):
    """标记消息为已发送"""
    if not file_hash:
        return
    records = load_sent_messages()
    records[file_hash] = {
        'sent_at': datetime.now().isoformat(),
        'file': str(file_path)
    }
    save_sent_messages(records)


def acquire_lock(timeout: int = 30) -> bool:
    """获取文件锁，防止并发执行"""
    try:
        lock_fd = open(LOCK_FILE, 'w')
        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock_fd.write(str(os.getpid()))
        lock_fd.flush()
        return lock_fd
    except (IOError, OSError):
        return False


def release_lock(lock_fd):
    """释放文件锁"""
    if lock_fd:
        try:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
            lock_fd.close()
            LOCK_FILE.unlink(missing_ok=True)
        except (IOError, OSError):
            pass


def send_document(chat_id, file_path, caption=None):
    """发送文件到 Telegram"""
    url = f"{TELEGRAM_API_URL}/sendDocument"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': 'Markdown',
            }
            
            response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ 文件发送成功：{file_path}")
                return True
            else:
                print(f"❌ 发送失败：{response.status_code}")
                print(f"响应：{response.text}")
                return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def send_message(chat_id, text, parse_mode='Markdown'):
    """发送消息到 Telegram"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    
    try:
        data = {
            'chat_id': chat_id,
            'text': text[:4096],
            'parse_mode': parse_mode,
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ 消息发送成功")
            return True
        else:
            print(f"❌ 发送失败：{response.status_code}")
            print(f"响应：{response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def extract_content_from_md(md_file_path):
    """从 MD 文件动态提取内容"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # 提取标题
    title = ""
    for line in lines[:20]:
        if line.startswith('#'):
            title = line.replace('#', '').strip()
            break
    
    # 提取版本信息
    version = ""
    status = ""
    for line in lines[:20]:
        if '> **版本**:' in line or '> Version:' in line:
            version = line.split(':')[1].strip()
        if '> **状态**:' in line or '> Status:' in line:
            status = line.split(':')[1].strip()
    
    # 提取核心功能数量
    features = ""
    for line in lines[20:50]:
        if '核心功能' in line or 'Core Features' in line:
            if '18' in line:
                features = '18 个核心功能'
            elif '18+' in line:
                features = '18+ 核心功能'
            break
    
    # 提取关键成就
    achievements = []
    for line in lines[20:80]:
        if '✅' in line and ('功能' in line or '能力' in line or 'CLI' in line or '推送' in line or '蒸馏' in line):
            achievements.append(line.strip())
            if len(achievements) >= 5:
                break
    
    # 提取测试结果
    test_results = []
    for line in lines[80:150]:
        if '✅' in line and ('成功' in line or '通过' in line or '置信度' in line):
            test_results.append(line.strip())
            if len(test_results) >= 4:
                break
    
    return {
        'title': title,
        'version': version,
        'status': status,
        'features': features,
        'achievements': achievements,
        'test_results': test_results,
    }


def send_md_file(md_file_path, chat_id=TELEGRAM_CHAT_ID):
    """发送 MD 文件到 Telegram（带去重）"""
    
    # 1. 计算文件哈希
    file_hash = compute_message_hash(md_file_path)
    
    # 2. 检查是否已发送
    if is_already_sent(file_hash):
        records = load_sent_messages()
        sent_at = records.get(file_hash, {}).get('sent_at', 'unknown')
        print(f"⏭️  消息已发送过 (哈希: {file_hash})，跳过。上次发送时间: {sent_at}")
        return True
    
    print(f"📱 开始发送 MD 文件到 Telegram...")
    print(f"   文件：{md_file_path}")
    print(f"   哈希：{file_hash}")
    print(f"   Chat ID: {chat_id}")
    
    # 从 MD 文件动态提取内容
    content = extract_content_from_md(md_file_path)
    
    # 构建文件 caption（从 MD 文件内容提取）
    caption = f"""{content['title']}

{content['version']}
{content['status']}
{content['features']}

📄 点击文件直接打开查看

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 构建预览消息（从 MD 文件内容提取）
    achievements_text = '\n'.join(content['achievements'][:5]) if content['achievements'] else '内容详见文件'
    
    message = f"""{content['title']}

{content['version']}
{content['status']}
{content['features']}

📋 核心成就:
{achievements_text}

📄 点击文件直接打开查看

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 发送预览消息
    print("\n📝 发送说明消息...")
    msg_ok = send_message(chat_id, message)
    
    # 发送 MD 文件
    print("\n📄 发送 MD 文件...")
    doc_ok = send_document(chat_id, md_file_path, caption)
    
    # 标记为已发送
    if msg_ok or doc_ok:
        mark_as_sent(file_hash, md_file_path)
        print(f"✅ 已标记为已发送 (哈希: {file_hash})")
    
    print("\n✅ 发送完成！")
    return msg_ok and doc_ok


def main():
    """主函数"""
    # 获取文件锁
    lock_fd = acquire_lock()
    if not lock_fd:
        print("⚠️  另一个实例正在运行，跳过本次执行")
        sys.exit(0)
    
    try:
        if len(sys.argv) < 2:
            # 使用最新的需求报告
            md_file = WORKSPACE / 'share' / 'reports' / 'real-steel-structure-demand-20260413.md'
            if not md_file.exists():
                md_file = WORKSPACE / 'reports' / 'real-steel-structure-demand-20260413.md'
        else:
            md_file = Path(sys.argv[1])
        
        if not md_file.exists():
            print(f"❌ 文件不存在：{md_file}")
            sys.exit(1)
        
        send_md_file(md_file)
    finally:
        release_lock(lock_fd)


if __name__ == '__main__':
    main()
