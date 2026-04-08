#!/usr/bin/env python3
"""Cron 清理 - 守藏吏 Skill - 自动识别并清理重复配置"""

import subprocess
from datetime import datetime
from pathlib import Path

def get_crontab():
    """获取当前 Cron 配置"""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    return result.stdout.split('\n') if result.returncode == 0 else []

def find_duplicates(lines):
    """查找重复配置"""
    tasks = {}
    duplicates = []
    
    for i, line in enumerate(lines):
        if line.startswith('#') or not line.strip():
            continue
        
        # 提取任务标识（频率 + 命令）
        parts = line.split()
        if len(parts) >= 7:
            # 简化：使用命令作为标识
            cmd = ' '.join(parts[5:])
            if cmd in tasks:
                duplicates.append({
                    'line': i + 1,
                    'content': line,
                    'duplicate_of': tasks[cmd],
                    'cmd': cmd
                })
            else:
                tasks[cmd] = line
    
    return duplicates

def remove_duplicates(lines, duplicates):
    """删除重复配置（保留 Skill 版本）"""
    to_remove = set()
    
    for dup in duplicates:
        # 优先保留 skills/ 版本
        if 'skills/' in dup['content']:
            # 删除旧版本
            old_line = dup['duplicate_of']['line']
            to_remove.add(old_line - 1)  # 转为 0 索引
        else:
            # 当前是旧版本，删除自己
            to_remove.add(dup['line'] - 1)
    
    # 生成新配置
    new_lines = [line for i, line in enumerate(lines) if i not in to_remove]
    return new_lines

def backup_crontab(content):
    """备份 Cron 配置"""
    backup_file = Path(f"/tmp/crontab-backup-{datetime.now().strftime('%Y%m%d-%H%M')}.txt")
    with open(backup_file, 'w') as f:
        f.write(content)
    return backup_file

def apply_crontab(lines):
    """应用新 Cron 配置"""
    content = '\n'.join(lines)
    result = subprocess.run(["crontab", "-"], input=content, text=True, capture_output=True)
    return result.returncode == 0

def main():
    print("🔍 Cron 清理启动...")
    
    # 1. 获取当前配置
    lines = get_crontab()
    print(f"📊 当前配置：{len(lines)} 行")
    
    # 2. 查找重复
    duplicates = find_duplicates(lines)
    print(f"⚠️  发现重复：{len(duplicates)} 项")
    
    if not duplicates:
        print("✅ 无重复配置")
        return
    
    # 3. 显示重复
    for dup in duplicates:
        print(f"\n  行 {dup['line']}: {dup['content'][:60]}...")
        print(f"  重复于：行 {dup['duplicate_of']['line']}")
    
    # 4. 备份
    backup_file = backup_crontab('\n'.join(lines))
    print(f"\n💾 已备份：{backup_file}")
    
    # 5. 清理
    new_lines = remove_duplicates(lines, duplicates)
    print(f"📊 清理后：{len(new_lines)} 行（删除{len(lines) - len(new_lines)}行）")
    
    # 6. 应用
    if apply_crontab(new_lines):
        print("✅ Cron 配置已更新")
    else:
        print("❌ 应用失败，恢复备份")
        subprocess.run(["crontab", str(backup_file)])
    
    # 7. 验证
    final_lines = get_crontab()
    final_dups = find_duplicates(final_lines)
    print(f"✅ 验证：剩余{len(final_dups)}项重复")

if __name__ == "__main__":
    main()
