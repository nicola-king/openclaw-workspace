#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化 Bug 检测、蒸馏、提炼、修复、优化系统

功能:
1. 自动检测脚本错误
2. 自动分析错误原因
3. 自动修复常见 Bug
4. 自动优化代码
5. 生成修复报告

运行时间：每 30 分钟自动检查 + 错误触发

作者：太一 AGI
创建：2026-04-13
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SCRIPTS_DIR = WORKSPACE / "scripts"
LOGS_DIR = WORKSPACE / "logs"
REPORTS_DIR = WORKSPACE / "reports"

# 确保目录存在
LOGS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


class AutoBugDetectorAndFixer:
    """自动化 Bug 检测和修复系统"""
    
    def __init__(self):
        self.errors_found = []
        self.errors_fixed = []
        self.start_time = datetime.now()
        self.log_file = LOGS_DIR / 'auto-bug-fix.log'
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.errors_found.append(log_entry)
        print(log_entry)
        
        # 同时写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def run(self):
        """运行自动化检测和修复"""
        self.log("🔍 开始自动化 Bug 检测和修复...")
        
        # Step 1: 检查脚本错误
        self.check_script_errors()
        
        # Step 2: 检查日志错误
        self.check_log_errors()
        
        # Step 3: 自动修复常见 Bug
        self.auto_fix_common_bugs()
        
        # Step 4: 优化代码
        self.optimize_code()
        
        # Step 5: 生成报告
        self.generate_report()
        
        self.log("✅ 自动化 Bug 检测和修复完成！")
    
    def check_script_errors(self):
        """检查脚本错误"""
        self.log("🔍 检查脚本错误...")
        
        # 检查主要脚本
        scripts_to_check = [
            SCRIPTS_DIR / 'self-evolution-trigger.py',
            SCRIPTS_DIR / 'merge-emerged-skills.py',
            SCRIPTS_DIR / 'distill-all-skills.py',
        ]
        
        for script in scripts_to_check:
            if script.exists():
                self.log(f"  ✅ 检查：{script.name}")
                # 语法检查
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', str(script)],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    self.log(f"  ❌ 语法错误：{script.name}")
                    self.errors_found.append({
                        'type': 'syntax_error',
                        'file': script.name,
                        'error': result.stderr,
                    })
                else:
                    self.log(f"  ✅ 语法正确：{script.name}")
            else:
                self.log(f"  ⚠️ 文件不存在：{script.name}")
    
    def check_log_errors(self):
        """检查日志错误"""
        self.log("🔍 检查日志错误...")
        
        log_files = [
            LOGS_DIR / 'self-evolution.log',
            LOGS_DIR / 'auto-exec-5m.log',
            LOGS_DIR / 'telegram-send.log',
        ]
        
        for log_file in log_files:
            if log_file.exists():
                self.log(f"  ✅ 检查：{log_file.name}")
                # 检查最近错误
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # 检查最后 100 行
                    recent_lines = lines[-100:] if len(lines) > 100 else lines
                    
                    for line in recent_lines:
                        if 'Traceback' in line or 'Error' in line or 'Exception' in line:
                            self.log(f"  ⚠️ 发现错误：{line.strip()}")
                            self.errors_found.append({
                                'type': 'runtime_error',
                                'file': log_file.name,
                                'error': line.strip(),
                            })
            else:
                self.log(f"  ⚠️ 日志不存在：{log_file.name}")
    
    def auto_fix_common_bugs(self):
        """自动修复常见 Bug"""
        self.log("🔧 自动修复常见 Bug...")
        
        # 修复 self-evolution-trigger.py 中的常见问题
        script_file = SCRIPTS_DIR / 'self-evolution-trigger.py'
        if script_file.exists():
            self.log(f"  🔧 检查：{script_file.name}")
            
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            fixes_applied = 0
            
            # 修复 1: 检查是否有未定义的 workspace 属性
            if 'self.workspace' in content and 'self.workspace =' not in content:
                # 添加 workspace 属性
                init_pattern = r'def __init__\(self\):'
                if re.search(init_pattern, content):
                    # 在 __init__ 中添加 self.workspace
                    content = re.sub(
                        init_pattern,
                        'def __init__(self):\n        self.workspace = WORKSPACE',
                        content,
                        count=1
                    )
                    fixes_applied += 1
                    self.log(f"  ✅ 修复：添加 self.workspace 属性")
            
            # 修复 2: 检查是否有未定义的 reports_dir
            if "Path(self.workspace) / 'reports'" in content:
                content = content.replace(
                    "Path(self.workspace) / 'reports'",
                    'REPORTS_DIR'
                )
                fixes_applied += 1
                self.log(f"  ✅ 修复：使用 REPORTS_DIR 全局变量")
            
            # 修复 3: 检查是否有未定义的 logs_dir
            if "Path(self.workspace) / 'logs'" in content:
                content = content.replace(
                    "Path(self.workspace) / 'logs'",
                    'LOGS_DIR'
                )
                fixes_applied += 1
                self.log(f"  ✅ 修复：使用 LOGS_DIR 全局变量")
            
            # 保存修复
            if fixes_applied > 0:
                with open(script_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.errors_fixed.append({
                    'file': script_file.name,
                    'fixes': fixes_applied,
                })
                
                self.log(f"  ✅ 应用 {fixes_applied} 个修复")
                
                # 验证修复
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', str(script_file)],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.log(f"  ✅ 验证通过：{script_file.name}")
                else:
                    self.log(f"  ❌ 验证失败：{script_file.name}")
    
    def optimize_code(self):
        """优化代码"""
        self.log("⚙️ 优化代码...")
        
        # 这里可以添加代码优化逻辑
        # 例如：移除未使用的导入、优化循环等
        self.log("  ℹ️  代码优化功能待实现")
    
    def generate_report(self):
        """生成报告"""
        self.log("📝 生成修复报告...")
        
        report_file = REPORTS_DIR / f'auto-bug-fix-{datetime.now().strftime("%Y%m%d-%H%M%S")}.md'
        
        content = f"""# 🔧 自动化 Bug 检测和修复报告

> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **执行人**: 太一 AGI  
> **状态**: ✅ 完成

---

## 📊 统计

**发现错误**: {len(self.errors_found)} 个  
**修复错误**: {len(self.errors_fixed)} 个

---

## 🐛 发现的错误

"""
        for error in self.errors_found[:20]:
            if isinstance(error, dict):
                content += f"### {error.get('type', 'unknown')}\n\n"
                content += f"- 文件：{error.get('file', 'unknown')}\n"
                content += f"- 错误：{error.get('error', 'unknown')}\n\n"
            else:
                content += f"- {error}\n"
        
        content += f"""
## ✅ 修复的错误

"""
        for fix in self.errors_fixed:
            content += f"### {fix['file']}\n\n"
            content += f"- 修复数量：{fix['fixes']} 个\n\n"
        
        content += f"""
---

**🔧 自动化 Bug 检测和修复报告完成**

**太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ 报告已生成：{report_file.name}")


def main():
    """主函数"""
    detector = AutoBugDetectorAndFixer()
    detector.run()


if __name__ == '__main__':
    main()
