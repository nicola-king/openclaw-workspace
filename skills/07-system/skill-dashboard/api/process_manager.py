#!/usr/bin/env python3
"""
进程管理器 - 管理 Skill 应用的启动/停止/状态

作者：太一 AGI
创建：2026-04-10
"""

import os
import json
import signal
import subprocess
from datetime import datetime
from pathlib import Path

# 进程存储文件
PROCESS_FILE = Path("/tmp/skill-dashboard-processes.json")

def load_processes():
    """加载进程列表"""
    if PROCESS_FILE.exists():
        try:
            with open(PROCESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_processes(processes):
    """保存进程列表"""
    with open(PROCESS_FILE, "w", encoding="utf-8") as f:
        json.dump(processes, f, indent=2, ensure_ascii=False)

def find_executable(skill_dir):
    """查找可执行文件"""
    priority_files = [
        "main.py",
        "app.py", 
        "server.py",
        "run.py",
        "index.py",
        "dashboard.py",
        "web.py",
        "api.py"
    ]
    
    for filename in priority_files:
        script = skill_dir / filename
        if script.exists():
            return str(script), filename
    
    # 查找可执行的 shell 脚本
    for filename in ["run.sh", "start.sh", "launch.sh"]:
        script = skill_dir / filename
        if script.exists() and os.access(script, os.X_OK):
            return str(script), filename
    
    return None, None

def get_port_from_script(script_path):
    """从脚本中检测端口号"""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 查找常见的端口配置
        import re
        patterns = [
            r'port\s*=\s*(\d+)',
            r'PORT\s*=\s*(\d+)',
            r'app\.run\([^)]*port\s*=\s*(\d+)',
            r':(\d{4,5})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return int(match.group(1))
        
        # 默认端口映射
        if "5000" in content:
            return 5000
        elif "3000" in content:
            return 3000
        elif "8080" in content:
            return 8080
        elif "8000" in content:
            return 8000
            
    except:
        pass
    
    return None

def is_process_running(pid):
    """检查进程是否运行"""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False

def start_skill(skill_id, skill_dir):
    """启动 Skill 应用"""
    processes = load_processes()
    
    # 检查是否已在运行
    if skill_id in processes:
        pid = processes[skill_id].get("pid")
        if pid and is_process_running(pid):
            return {"error": "应用已在运行", "pid": pid}
    
    # 查找可执行文件
    script_path, script_name = find_executable(skill_dir)
    
    if not script_path:
        return {"error": "未找到可执行文件 (需要 main.py/app.py/server.py/run.py 等)"}
    
    # 检测端口
    port = get_port_from_script(script_path)
    
    # 启动进程
    try:
        # 创建日志文件
        log_file = Path(f"/tmp/skill-{skill_id}.log")
        
        # 启动命令
        if script_path.endswith('.py'):
            cmd = ["python3", script_path]
        else:
            cmd = ["bash", script_path]
        
        # 启动进程
        proc = subprocess.Popen(
            cmd,
            cwd=str(skill_dir),
            stdout=open(log_file, "w"),
            stderr=subprocess.STDOUT,
            start_new_session=True
        )
        
        # 等待一下看是否启动成功
        import time
        time.sleep(2)
        
        if proc.poll() is not None:
            # 进程已退出，读取错误日志
            with open(log_file, "r") as f:
                error = f.read()
            return {"error": f"启动失败：{error[:500]}"}
        
        # 保存进程信息
        processes[skill_id] = {
            "pid": proc.pid,
            "script": script_name,
            "path": script_path,
            "port": port,
            "started_at": datetime.now().isoformat(),
            "log_file": str(log_file)
        }
        save_processes(processes)
        
        return {
            "status": "started",
            "pid": proc.pid,
            "script": script_name,
            "port": port,
            "url": f"http://localhost:{port}" if port else None
        }
        
    except Exception as e:
        return {"error": str(e)}

def stop_skill(skill_id):
    """停止 Skill 应用"""
    processes = load_processes()
    
    if skill_id not in processes:
        return {"error": "应用未运行"}
    
    proc_info = processes[skill_id]
    pid = proc_info.get("pid")
    
    if not pid or not is_process_running(pid):
        del processes[skill_id]
        save_processes(processes)
        return {"status": "not_running"}
    
    try:
        # 尝试优雅停止
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        
        # 等待 5 秒
        import time
        for _ in range(5):
            time.sleep(1)
            if not is_process_running(pid):
                break
        else:
            # 强制停止
            os.killpg(os.getpgid(pid), signal.SIGKILL)
        
        del processes[skill_id]
        save_processes(processes)
        
        return {"status": "stopped"}
        
    except Exception as e:
        return {"error": str(e)}

def get_skill_status(skill_id):
    """获取 Skill 运行状态"""
    processes = load_processes()
    
    if skill_id not in processes:
        return {"running": False}
    
    proc_info = processes[skill_id]
    pid = proc_info.get("pid")
    
    if not pid or not is_process_running(pid):
        if skill_id in processes:
            del processes[skill_id]
            save_processes(processes)
        return {"running": False}
    
    return {
        "running": True,
        "pid": pid,
        "script": proc_info.get("script"),
        "port": proc_info.get("port"),
        "started_at": proc_info.get("started_at"),
        "url": f"http://localhost:{proc_info.get('port')}" if proc_info.get("port") else None
    }

def get_all_status():
    """获取所有 Skill 状态"""
    processes = load_processes()
    status = {}
    
    for skill_id, proc_info in processes.items():
        pid = proc_info.get("pid")
        if pid and is_process_running(pid):
            status[skill_id] = {
                "running": True,
                "pid": pid,
                "port": proc_info.get("port"),
                "url": f"http://localhost:{proc_info.get('port')}" if proc_info.get("port") else None
            }
        else:
            status[skill_id] = {"running": False}
    
    return status

def get_logs(skill_id, lines=100):
    """获取应用日志"""
    processes = load_processes()
    
    if skill_id not in processes:
        return {"error": "应用未运行"}
    
    log_file = processes[skill_id].get("log_file")
    
    if not log_file or not Path(log_file).exists():
        return {"logs": [], "error": "日志文件不存在"}
    
    try:
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            all_lines = f.readlines()
            logs = all_lines[-lines:]
        
        return {"logs": "".join(logs)}
        
    except Exception as e:
        return {"error": str(e)}
