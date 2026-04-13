#!/usr/bin/env python3
"""
Syncthing 任务监控 - 工作站端
监控从太一传来的任务，执行后返回结果
"""

import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# 目录配置
JOBS_DIR = Path("~/syncthing-hub/from-taiyi/jobs").expanduser()
RESULTS_DIR = Path("~/syncthing-hub/to-taiyi/results").expanduser()
PROCESSING_DIR = Path("~/syncthing-hub/processing").expanduser()
LOG_FILE = Path("~/syncthing-hub/logs/job-monitor.log").expanduser()

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}\n"
    print(log_msg, end="")
    
    # 写入日志文件
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)

def process_job(job_file):
    """处理单个任务"""
    job_id = job_file.stem
    log(f"开始处理任务：{job_id}")
    
    try:
        # 读取任务
        with open(job_file) as f:
            job = json.load(f)
        
        # 移动到处理中
        processing_file = PROCESSING_DIR / job_file.name
        job_file.rename(processing_file)
        
        # 执行命令
        command = job.get('command', 'echo "No command"')
        log(f"执行命令：{command}")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=job.get('timeout', 3600)
        )
        
        # 写入结果
        result_file = RESULTS_DIR / f"result-{job_id}.json"
        with open(result_file, 'w') as f:
            json.dump({
                'job_id': job_id,
                'status': 'completed',
                'return_code': result.returncode,
                'stdout': result.stdout.decode()[:10000],  # 限制大小
                'stderr': result.stderr.decode()[:10000],
                'completed_at': datetime.now().isoformat()
            }, f, indent=2)
        
        log(f"任务完成：{job_id}, 返回码：{result.returncode}")
        
        # 清理处理中文件
        processing_file.unlink()
        
    except Exception as e:
        log(f"任务失败：{job_id}, 错误：{e}")
        
        # 写入错误
        result_file = RESULTS_DIR / f"result-{job_id}.json"
        with open(result_file, 'w') as f:
            json.dump({
                'job_id': job_id,
                'status': 'failed',
                'error': str(e),
                'failed_at': datetime.now().isoformat()
            }, f, indent=2)
        
        # 移动到错误目录
        error_dir = Path("~/syncthing-hub/errors").expanduser()
        error_dir.mkdir(parents=True, exist_ok=True)
        job_file.rename(error_dir / job_file.name)

def main():
    """主循环"""
    log("=" * 60)
    log("Syncthing 任务监控启动")
    log("=" * 60)
    
    # 创建必要目录
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
    
    # 主循环
    check_interval = 10  # 每 10 秒检查一次
    
    while True:
        try:
            # 检查新任务
            job_files = list(JOBS_DIR.glob('job-*.json'))
            
            if job_files:
                log(f"发现 {len(job_files)} 个新任务")
                
                for job_file in job_files:
                    process_job(job_file)
            else:
                log("无新任务，等待中...")
            
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            log("收到中断信号，停止监控")
            break
        except Exception as e:
            log(f"监控错误：{e}")
            time.sleep(60)  # 错误后等待 1 分钟

if __name__ == '__main__':
    main()
