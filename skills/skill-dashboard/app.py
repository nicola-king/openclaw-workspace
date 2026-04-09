#!/usr/bin/env python3
"""
Skill Dashboard - 太一 Skill 可视化管理中心

作者：太一 AGI
创建：2026-04-09
"""

import os
import json
import subprocess
from pathlib import Path
from flask import Flask, render_template, jsonify, request

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"
APP = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# 缓存
SKILL_CACHE = {}

def get_skills_list():
    """获取 Skills 列表"""
    if SKILL_CACHE:
        return SKILL_CACHE
    
    skills = []
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('__'):
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                with open(skill_md, "r", encoding="utf-8") as f:
                    content = f.read()
                
                skill_info = {
                    "id": skill_dir.name,
                    "name": skill_dir.name,
                    "path": str(skill_dir),
                    "status": "active",
                    "files": len(list(skill_dir.glob("**/*"))),
                    "size": sum(f.stat().st_size for f in skill_dir.glob("**/*") if f.is_file())
                }
                
                for line in content.split('\n')[:30]:
                    if line.startswith('name:'):
                        skill_info["name"] = line.split(':', 1)[1].strip()
                    elif line.startswith('description:'):
                        skill_info["description"] = line.split(':', 1)[1].strip()
                    elif line.startswith('version:'):
                        skill_info["version"] = line.split(':', 1)[1].strip()
                    elif line.startswith('status:'):
                        skill_info["status"] = line.split(':', 1)[1].strip()
                
                skills.append(skill_info)
    
    SKILL_CACHE.update({s["id"]: s for s in skills})
    return skills

@APP.route('/')
def index():
    return render_template('index.html')

@APP.route('/api/skills')
def api_skills():
    skills = get_skills_list()
    return jsonify({"total": len(skills), "skills": skills})

@APP.route('/api/skills/<skill_id>')
def api_skill_detail(skill_id):
    skill_dir = SKILLS_DIR / skill_id
    if not skill_dir.exists():
        return jsonify({"error": "Skill not found"}), 404
    
    skill_md = skill_dir / "SKILL.md"
    content = ""
    if skill_md.exists():
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
    
    return jsonify({
        "id": skill_id,
        "path": str(skill_dir),
        "files": [str(f.relative_to(skill_dir)) for f in skill_dir.glob("**/*") if f.is_file()],
        "content": content
    })

@APP.route('/api/skills/<skill_id>/start', methods=['POST'])
def api_skill_start(skill_id):
    skill_dir = SKILLS_DIR / skill_id
    main_py = skill_dir / "main.py"
    app_py = skill_dir / "app.py"
    
    script = str(main_py) if main_py.exists() else (str(app_py) if app_py.exists() else None)
    
    if not script:
        return jsonify({"error": "No executable script found"}), 400
    
    try:
        subprocess.Popen(["python3", script], cwd=str(skill_dir),
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return jsonify({"status": "started", "script": script})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@APP.route('/api/skills/<skill_id>/stop', methods=['POST'])
def api_skill_stop(skill_id):
    try:
        subprocess.run(["pkill", "-f", skill_id], capture_output=True)
        return jsonify({"status": "stopped"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@APP.route('/api/skills/create', methods=['POST'])
def api_skill_create():
    data = request.json
    skill_name = data.get("name", "new-skill")
    skill_dir = SKILLS_DIR / skill_name
    
    if skill_dir.exists():
        return jsonify({"error": "Skill already exists"}), 400
    
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "config").mkdir(exist_ok=True)
    (skill_dir / "tests").mkdir(exist_ok=True)
    
    skill_md = skill_dir / "SKILL.md"
    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(f"""---
name: {skill_name}
version: 1.0.0
description: {data.get('description', 'New Skill')}
category: {data.get('category', 'general')}
tags: []
author: 太一 AGI
created: 2026-04-09
status: active
---

# {skill_name.replace('-', ' ').title()}

> **版本**: 1.0.0 | **创建**: 2026-04-09

---

## 🎯 职责

TODO

---

*创建：2026-04-09 | 太一 AGI*
""")
    
    SKILL_CACHE.clear()
    return jsonify({"status": "created", "path": str(skill_dir)})

@APP.route('/api/system/status')
def api_system_status():
    return jsonify({
        "gateway": "running",
        "skills_count": len(get_skills_list()),
        "workspace": str(WORKSPACE)
    })

if __name__ == '__main__':
    print("🎯 Skill Dashboard 启动中...")
    print("="*50)
    print(f"📁 Skills 目录：{SKILLS_DIR}")
    print(f"🌐 访问地址：http://localhost:5002")
    print()
    APP.run(host='0.0.0.0', port=5002, debug=False)
