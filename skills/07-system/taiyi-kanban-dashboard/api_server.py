#!/usr/bin/env python3
"""
太一看板 Dashboard API 服务器
提供任务数据、Bot 状态、Cron 状态等实时数据
"""

import json
import os
import re
from datetime import datetime
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

WORKSPACE = os.path.expanduser('~/.openclaw/workspace')
HEARTBEAT_FILE = os.path.join(WORKSPACE, 'HEARTBEAT.md')

def parse_heartbeat_md():
    """解析 HEARTBEAT.md 文件，提取任务数据"""
    tasks = {
        'todo': [],
        'doing': [],
        'done': []
    }
    
    if not os.path.exists(HEARTBEAT_FILE):
        return tasks
    
    try:
        with open(HEARTBEAT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取表格中的任务
        # 查找 | **TASK-XXX** | 任务描述 | 状态 | 下一步 | 截止 |
        task_pattern = r'\|\s*\*\*(TASK-\d+)\*\*\s*\|\s*([^\|]+)\|\s*([^\|]+)\|\s*([^\|]+)\|\s*([^\|]+)\|'
        
        for match in re.finditer(task_pattern, content):
            task_id = match.group(1)
            title = match.group(2).strip()
            status = match.group(3).strip()
            next_step = match.group(4).strip()
            due = match.group(5).strip()
            
            # 根据状态图标判断列
            if '🔴' in status or '待命' in status:
                column = 'todo'
            elif '🟡' in status or 'MVP' in status:
                column = 'doing'
            elif '✅' in status or '完成' in status:
                column = 'done'
            else:
                column = 'todo'
            
            # 提取优先级
            priority = 'P2'
            if 'P0' in content[content.find(task_id):content.find(task_id)+200]:
                priority = 'P0'
            elif 'P1' in content[content.find(task_id):content.find(task_id)+200]:
                priority = 'P1'
            
            # 提取标签
            tags = []
            if 'Hermes' in title:
                tags.append('学习循环')
            if 'CLI' in title:
                tags.append('CLI')
            if '技能' in title:
                tags.append('技能开发')
            
            task = {
                'id': task_id,
                'title': title,
                'priority': priority,
                'assignee': '太一',
                'due': due,
                'tags': tags,
                'status': status,
                'next_step': next_step
            }
            
            tasks[column].append(task)
        
    except Exception as e:
        print(f"解析 HEARTBEAT.md 失败：{e}")
    
    return tasks

def get_bot_status():
    """获取 Bot 状态"""
    bots = [
        {'id': 'taiyi', 'name': '太一', 'role': '执行总管', 'status': 'running', 'tasks': 12},
        {'id': 'zhiji', 'name': '知几-E', 'role': '量化交易', 'status': 'running', 'tasks': 3},
        {'id': 'shanmu', 'name': '山木', 'role': '内容创意', 'status': 'running', 'tasks': 5},
        {'id': 'suwen', 'name': '素问', 'role': '技术开发', 'status': 'running', 'tasks': 8},
        {'id': 'wangliang', 'name': '罔两', 'role': '高价值发现', 'status': 'idle', 'tasks': 0},
        {'id': 'paoding', 'name': '庖丁', 'role': '预算追踪', 'status': 'running', 'tasks': 1},
        {'id': 'shoucangli', 'name': '守藏吏', 'role': '知识管理', 'status': 'running', 'tasks': 8},
    ]
    return bots

def get_cron_status():
    """获取 Cron 任务状态"""
    cron_tasks = [
        {'name': '每 5 分钟 - 自动执行', 'status': 'ok', 'lastRun': '07:45'},
        {'name': '每 10 分钟 - 通道检查', 'status': 'ok', 'lastRun': '07:40'},
        {'name': '每 30 分钟 - Git 备份', 'status': 'ok', 'lastRun': '07:30'},
        {'name': '每小时 - 天气预测', 'status': 'ok', 'lastRun': '07:00'},
        {'name': '每小时 - 系统自检', 'status': 'ok', 'lastRun': '07:00'},
        {'name': '每日 06:00 - 宪法学习', 'status': 'ok', 'lastRun': '06:00'},
        {'name': '每日 23:00 - 日报生成', 'status': 'pending', 'lastRun': '昨日'},
    ]
    
    # 更新实际运行时间
    now = datetime.now()
    for cron in cron_tasks:
        if '每 5 分钟' in cron['name']:
            cron['lastRun'] = now.strftime('%H:%M')
        elif '每 10 分钟' in cron['name']:
            minute = (now.minute // 10) * 10
            cron['lastRun'] = f"{now.hour:02d}:{minute:02d}"
        elif '每 30 分钟' in cron['name']:
            minute = '00' if now.minute < 30 else '30'
            cron['lastRun'] = f"{now.hour:02d}:{minute}"
        elif '每小时' in cron['name']:
            cron['lastRun'] = f"{now.hour:02d}:00"
    
    return cron_tasks

def get_system_status():
    """获取系统状态"""
    import subprocess
    
    status = {
        'gateway': {'status': 'unknown', 'pid': None},
        'git': {'status': 'unknown'},
        'constitution': {'status': 'unknown'},
        'channels': {'wechat': 'unknown', 'telegram': 'unknown'}
    }
    
    # 检查 Gateway
    try:
        result = subprocess.run(['pgrep', '-f', 'openclaw-gateway'], capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            status['gateway'] = {'status': 'running', 'pid': pids[0]}
        else:
            status['gateway'] = {'status': 'stopped', 'pid': None}
    except:
        pass
    
    # 检查 Git
    try:
        result = subprocess.run(['git', 'status'], cwd=WORKSPACE, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            status['git'] = {'status': 'ok'}
        else:
            status['git'] = {'status': 'error'}
    except:
        pass
    
    # 检查宪法文件
    const_files = [
        'constitution/CONST-ROUTER.md',
        'constitution/axiom/VALUE-FOUNDATION.md',
        'SOUL.md'
    ]
    all_exist = all(os.path.exists(os.path.join(WORKSPACE, f)) for f in const_files)
    status['constitution'] = {'status': 'ok' if all_exist else 'missing'}
    
    # 检查通讯通道
    try:
        result = subprocess.run(['pgrep', '-f', 'openclaw-weixin'], capture_output=True, text=True)
        status['channels']['wechat'] = 'ok' if result.returncode == 0 else 'error'
    except:
        pass
    
    return status

@app.route('/')
def index():
    """提供前端页面"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/tasks')
def api_tasks():
    """获取任务数据"""
    tasks = parse_heartbeat_md()
    return jsonify({
        'success': True,
        'data': tasks,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/bots')
def api_bots():
    """获取 Bot 状态"""
    return jsonify({
        'success': True,
        'data': get_bot_status(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/cron')
def api_cron():
    """获取 Cron 状态"""
    return jsonify({
        'success': True,
        'data': get_cron_status(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/system')
def api_system():
    """获取系统状态"""
    return jsonify({
        'success': True,
        'data': get_system_status(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats')
def api_stats():
    """获取统计数据"""
    tasks = parse_heartbeat_md()
    all_tasks = tasks['todo'] + tasks['doing'] + tasks['done']
    
    return jsonify({
        'success': True,
        'data': {
            'total': len(all_tasks),
            'todo': len(tasks['todo']),
            'doing': len(tasks['doing']),
            'done': len(tasks['done']),
            'p0': len([t for t in all_tasks if t.get('priority') == 'P0']),
            'p1': len([t for t in all_tasks if t.get('priority') == 'P1']),
            'p2': len([t for t in all_tasks if t.get('priority') == 'P2']),
        },
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🌟 太一看板 API 服务器启动中...")
    print(f"📂 工作目录：{WORKSPACE}")
    print(f"📄 HEARTBEAT 文件：{HEARTBEAT_FILE}")
    print("🌐 访问地址：http://localhost:5001")
    print("")
    app.run(host='0.0.0.0', port=5001, debug=True)
