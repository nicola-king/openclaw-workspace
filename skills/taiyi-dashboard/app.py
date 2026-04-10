#!/usr/bin/env python3
"""
太一 Dashboard - 综合总览

作者：太一 AGI
创建：2026-04-10
"""

import os
import json
import subprocess
from pathlib import Path
from flask import Flask, render_template, jsonify
from datetime import datetime

# 配置
APP = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

WORKSPACE = Path("/home/nicola/.openclaw/workspace")

def get_system_status():
    """获取系统状态"""
    status = {
        "gateway": False,
        "bot_dashboard": False,
        "roi_dashboard": False,
        "skill_dashboard": False,
        "baidu_netdisk": False
    }
    
    # 检查 Gateway
    try:
        result = subprocess.run(["pgrep", "-f", "openclaw-gateway"], capture_output=True)
        status["gateway"] = result.returncode == 0
    except:
        pass
    
    # 检查 Bot Dashboard
    try:
        result = subprocess.run(["pgrep", "-f", "vite.*3000"], capture_output=True)
        status["bot_dashboard"] = result.returncode == 0
    except:
        pass
    
    # 检查 ROI Dashboard
    try:
        result = subprocess.run(["pgrep", "-f", "roi_dashboard"], capture_output=True)
        status["roi_dashboard"] = result.returncode == 0
    except:
        pass
    
    # 检查 Skill Dashboard
    try:
        result = subprocess.run(["pgrep", "-f", "skill-dashboard.*5002"], capture_output=True)
        status["skill_dashboard"] = result.returncode == 0
    except:
        pass
    
    # 检查百度网盘
    try:
        result = subprocess.run(["pgrep", "-f", "baidunetdisk"], capture_output=True)
        status["baidu_netdisk"] = result.returncode == 0
    except:
        pass
    
    return status

def get_skills_count():
    """获取技能数量"""
    skills_dir = WORKSPACE / "skills"
    if not skills_dir.exists():
        return 0
    
    count = 0
    for item in skills_dir.iterdir():
        if item.is_dir() and not item.name.startswith('__'):
            count += 1
    return count

def get_memory_usage():
    """获取内存使用情况"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        total = int(lines[0].split()[1])
        available = int(lines[2].split()[1])
        used = total - available
        
        return {
            "total_gb": round(total / 1024 / 1024, 2),
            "used_gb": round(used / 1024 / 1024, 2),
            "percent": round((used / total) * 100, 1)
        }
    except:
        return {"total_gb": 0, "used_gb": 0, "percent": 0}

def get_disk_usage():
    """获取磁盘使用情况"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(str(WORKSPACE))
        return {
            "total_gb": round(total / 1024 / 1024 / 1024, 2),
            "used_gb": round(used / 1024 / 1024 / 1024, 2),
            "free_gb": round(free / 1024 / 1024 / 1024, 2),
            "percent": round((used / total) * 100, 1)
        }
    except:
        return {"total_gb": 0, "used_gb": 0, "free_gb": 0, "percent": 0}

def get_recent_reports():
    """获取最近的报告"""
    reports_dir = WORKSPACE / "reports"
    if not reports_dir.exists():
        return []
    
    reports = []
    for f in sorted(reports_dir.glob("*.md"), reverse=True)[:5]:
        reports.append({
            "name": f.name,
            "created": datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        })
    
    return reports

def get_google_services():
    """获取 Google 服务状态"""
    return {
        "gemini": True,  # API 已配置
        "notebooklm": True,  # 已配置
        "drive": False,  # 待凭证
        "chromium": True  # 已安装
    }

@APP.route('/')
def index():
    return render_template('index.html')

@APP.route('/service/<service_id>')
def service_detail(service_id):
    """服务详情页"""
    return render_template('service_detail.html', service_id=service_id)

@APP.route('/google')
def google_services():
    """Google 服务详情页"""
    return render_template('google_services.html')

@APP.route('/skills')
def skills_list():
    """技能列表页"""
    return render_template('skills_list.html')

@APP.route('/baidu')
def baidu_manager():
    """百度网盘管理页"""
    return render_template('baidu_manager.html')

@APP.route('/api/status')
def api_status():
    return jsonify({
        "system": get_system_status(),
        "skills_count": get_skills_count(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage(),
        "google_services": get_google_services(),
        "timestamp": datetime.now().isoformat()
    })

@APP.route('/api/service/<service_id>')
def api_service_detail(service_id):
    """获取服务详情"""
    services = {
        "gateway": {"name": "Gateway", "port": 18789, "description": "OpenClaw 网关服务"},
        "bot": {"name": "Bot Dashboard", "port": 3000, "url": "http://localhost:3000", "description": "Bot 状态仪表盘"},
        "roi": {"name": "ROI Dashboard", "port": 8080, "url": "http://localhost:8080", "description": "收益追踪器"},
        "skill": {"name": "Skill Dashboard", "port": 5002, "url": "http://localhost:5002", "description": "技能管理中心"},
        "baidu": {"name": "百度网盘", "path": "/opt/baidunetdisk", "description": "云存储客户端"}
    }
    
    if service_id not in services:
        return jsonify({"error": "Service not found"}), 404
    
    service = services[service_id]
    status = get_system_status()
    
    running = False
    if service_id == "gateway":
        running = status["gateway"]
    elif service_id == "bot":
        running = status["bot_dashboard"]
    elif service_id == "roi":
        running = status["roi_dashboard"]
    elif service_id == "skill":
        running = status["skill_dashboard"]
    elif service_id == "baidu":
        running = status["baidu_netdisk"]
    
    service["running"] = running
    return jsonify(service)

@APP.route('/api/reports')
def api_reports():
    return jsonify(get_recent_reports())

if __name__ == '__main__':
    print("🎯 太一 Dashboard 启动中...")
    print("="*50)
    print(f"📁 工作区：{WORKSPACE}")
    print(f"🌐 访问地址：http://localhost:5001")
    print()
    APP.run(host='0.0.0.0', port=5001, debug=False)
