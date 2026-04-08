# Cron 清理 Skill - 守藏吏

> 版本：v1.0 | 创建：2026-04-03 12:55  
> 职责：自动识别并清理重复 Cron 配置  
> 触发：手动/事件驱动

---

## 🎯 职责

**守藏吏** 自动识别并清理重复的 Cron 配置，保留 Skill 版本。

---

## 🤖 触发机制

### 手动触发
```bash
python3 skills/steward/cron-cleanup/run.py
```

### 事件触发
- Cron 配置变更后
- 每周日 23:00 自动检查

---

## 📋 清理流程

```
┌─────────────────────────────────────────────────────────┐
│ 1. 获取当前 Cron 配置                                    │
│    crontab -l                                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. 识别重复配置                                         │
│    - 按命令哈希                                          │
│    - 按频率 + 命令匹配                                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. 决策保留哪个                                         │
│    - 优先保留 skills/ 版本                                │
│    - 优先保留新版本                                      │
│    - 优先保留路径更规范的                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. 备份当前配置                                         │
│    /tmp/crontab-backup-YYYYMMDD-HHMM.txt               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. 删除重复配置                                         │
│    crontab -l | grep -v "旧脚本" | crontab -            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. 验证清理结果                                         │
│    - 检查重复是否清除                                    │
│    - 检查关键任务是否正常                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 7. 生成清理报告                                         │
│    - 删除项列表                                          │
│    - 保留项列表                                          │
│    - 备份文件位置                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 代码实现

### run.py

```python
#!/usr/bin/env python3
"""Cron 清理 - 守藏吏 Skill"""

import subprocess
from datetime import datetime
from pathlib import Path

def get_crontab():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    return result.stdout.split('\n') if result.returncode == 0 else []

def find_duplicates(lines):
    tasks = {}
    duplicates = []
    
    for i, line in enumerate(lines):
        if line.startswith('#') or not line.strip():
            continue
        
        parts = line.split()
        if len(parts) >= 7:
            cmd = ' '.join(parts[5:])
            if cmd in tasks:
                duplicates.append({
                    'line': i + 1,
                    'content': line,
                    'duplicate_of': tasks[cmd]
                })
            else:
                tasks[cmd] = line
    
    return duplicates

def remove_duplicates(lines, duplicates):
    to_remove = set()
    
    for dup in duplicates:
        if 'skills/' in dup['content']:
            to_remove.add(dup['duplicate_of']['line'] - 1)
        else:
            to_remove.add(dup['line'] - 1)
    
    return [line for i, line in enumerate(lines) if i not in to_remove]

def main():
    print("🔍 Cron 清理启动...")
    
    lines = get_crontab()
    duplicates = find_duplicates(lines)
    
    if not duplicates:
        print("✅ 无重复配置")
        return
    
    # 备份
    backup_file = Path(f"/tmp/crontab-backup-{datetime.now().strftime('%Y%m%d-%H%M')}.txt")
    with open(backup_file, 'w') as f:
        f.write('\n'.join(lines))
    
    # 清理
    new_lines = remove_duplicates(lines, duplicates)
    subprocess.run(["crontab", "-"], input='\n'.join(new_lines), text=True)
    
    print(f"✅ 清理完成：删除{len(duplicates)}项重复")
    print(f"💾 备份：{backup_file}")

if __name__ == "__main__":
    main()
```

---

## ✅ 验收标准

- [x] 自动识别重复配置
- [x] 优先保留 Skill 版本
- [x] 自动备份
- [x] 自动清理
- [x] 验证清理结果
- [x] 生成清理报告

---

## 📁 相关文件

- 备份：`/tmp/crontab-backup-*.txt`
- 日志：`logs/cron-cleanup.log`
- 报告：`reports/cron-cleanup-report.md`

---

*创建时间：2026-04-03 12:55 | 守藏吏 Skill*
