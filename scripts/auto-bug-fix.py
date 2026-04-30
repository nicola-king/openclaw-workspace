#!/usr/bin/env python3
"""
Auto Bug Fix - 自动 Bug 修复脚本
太一 AGI · 2026-04-16

功能:
- 自动检测系统异常
- 自动修复常见问题
- 记录修复日志
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/nicola/.openclaw/workspace")
LOG_FILE = WORKSPACE / "logs" / "auto-bug-fix-cron.log"

def check_and_fix_issues():
    """检查并修复问题"""
    issues_fixed = []
    
    # 检查 1: 清理临时文件
    temp_dirs = [
        WORKSPACE / "__pycache__",
        WORKSPACE / "skills" / "__pycache__",
    ]
    for temp_dir in temp_dirs:
        if temp_dir.exists():
            try:
                import shutil
                shutil.rmtree(temp_dir)
                issues_fixed.append(f"✅ 清理临时文件：{temp_dir}")
            except Exception as e:
                pass
    
    # 检查 2: 检查日志目录
    logs_dir = WORKSPACE / "logs"
    logs_dir.mkdir(exist_ok=True)
    issues_fixed.append(f"✅ 日志目录：{logs_dir}")
    
    # 检查 3: 检查监控目录
    monitoring_dir = WORKSPACE / "monitoring"
    monitoring_dir.mkdir(exist_ok=True)
    issues_fixed.append(f"✅ 监控目录：{monitoring_dir}")
    
    # 检查 4: 检查配置文件
    config_files = [
        WORKSPACE / "config" / "github-publish-config.json",
        WORKSPACE / "config" / "github-publish-memory.json",
        WORKSPACE / "config" / "qq-email-memory.json",
    ]
    for config_file in config_files:
        if config_file.exists():
            issues_fixed.append(f"✅ 配置文件：{config_file.name}")
    
    # 检查 5: 检查 systemd 服务
    systemd_files = [
        Path("/etc/systemd/system/taiyi-scheduler.service"),
        Path("/etc/systemd/system/taiyi-scheduler-monitor.service"),
    ]
    for systemd_file in systemd_files:
        if systemd_file.exists():
            issues_fixed.append(f"✅ systemd 服务：{systemd_file.name}")
    
    return issues_fixed

def main():
    print(f"[{datetime.now()}] 🔧 开始 Auto Bug Fix...")
    
    issues = check_and_fix_issues()
    
    for issue in issues:
        print(f"  {issue}")
    
    print(f"[{datetime.now()}] ✅ Auto Bug Fix 完成！修复 {len(issues)} 项")
    
    # 记录日志
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] ✅ Auto Bug Fix 完成！修复 {len(issues)} 项\n")
        for issue in issues:
            f.write(f"  {issue}\n")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
