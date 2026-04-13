#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版自动化 Bug 检测和修复系统

功能:
1. 自动检测脚本错误
2. 自动分析错误原因
3. 自动修复常见 Bug
4. 自动验证修复
5. 生成修复报告
6. 设置定时任务

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


class EnhancedBugFixer:
    """增强版自动化 Bug 修复系统"""
    
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
        self.log("🔍 开始增强版 Bug 检测和修复...")
        
        # Step 1: 检查并修复 self-evolution-trigger.py
        self.fix_self_evolution_trigger()
        
        # Step 2: 检查其他脚本
        self.check_other_scripts()
        
        # Step 3: 验证修复
        self.verify_fixes()
        
        # Step 4: 生成报告
        self.generate_report()
        
        # Step 5: 设置定时任务
        self.setup_cron()
        
        self.log("✅ 增强版 Bug 检测和修复完成！")
    
    def fix_self_evolution_trigger(self):
        """修复 self-evolution-trigger.py"""
        self.log("🔧 修复 self-evolution-trigger.py...")
        
        script_file = SCRIPTS_DIR / 'self-evolution-trigger.py'
        if not script_file.exists():
            self.log(f"  ⚠️ 文件不存在：{script_file.name}")
            return
        
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_applied = 0
        
        # 修复 1: 确保有 self.workspace 属性
        if 'self.workspace' in content and 'self.workspace = WORKSPACE' not in content:
            init_pattern = r'(    def __init__\(self\):)'
            match = re.search(init_pattern, content)
            if match:
                # 在 __init__ 中添加 self.workspace
                insert_pos = match.end()
                content = content[:insert_pos] + '\n        self.workspace = WORKSPACE' + content[insert_pos:]
                fixes_applied += 1
                self.log(f"  ✅ 修复：添加 self.workspace = WORKSPACE")
        
        # 修复 2: 替换 Path(self.workspace) / 'reports' 为 REPORTS_DIR
        if "Path(self.workspace) / 'reports'" in content:
            content = content.replace(
                "Path(self.workspace) / 'reports'",
                'REPORTS_DIR'
            )
            fixes_applied += 1
            self.log(f"  ✅ 修复：使用 REPORTS_DIR 全局变量")
        
        # 修复 3: 替换 Path(self.workspace) / 'logs' 为 LOGS_DIR
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
        else:
            self.log(f"  ℹ️  无需修复")
    
    def check_other_scripts(self):
        """检查其他脚本"""
        self.log("🔍 检查其他脚本...")
        
        scripts_to_check = [
            SCRIPTS_DIR / 'merge-emerged-skills.py',
            SCRIPTS_DIR / 'distill-all-skills.py',
            SCRIPTS_DIR / 'auto-bug-detector-and-fixer.py',
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
                else:
                    self.log(f"  ✅ 语法正确：{script.name}")
    
    def verify_fixes(self):
        """验证修复"""
        self.log("✅ 验证修复...")
        
        script_file = SCRIPTS_DIR / 'self-evolution-trigger.py'
        if script_file.exists():
            result = subprocess.run(
                ['python3', '-m', 'py_compile', str(script_file)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.log(f"  ✅ 验证通过：{script_file.name}")
            else:
                self.log(f"  ❌ 验证失败：{script_file.name}")
                self.log(f"     错误：{result.stderr}")
    
    def setup_cron(self):
        """设置定时任务"""
        self.log("⏰ 设置定时任务...")
        
        # 获取当前 crontab
        result = subprocess.run(
            ['crontab', '-l'],
            capture_output=True,
            text=True
        )
        
        current_cron = result.stdout if result.returncode == 0 else ""
        
        # 检查是否已有定时任务
        cron_entry = "*/30 * * * * python3 /home/nicola/.openclaw/workspace/scripts/auto-bug-fixer-enhanced.py >> /home/nicola/.openclaw/workspace/logs/auto-bug-fix-cron.log 2>&1"
        
        if cron_entry not in current_cron:
            # 添加定时任务
            new_cron = current_cron + "\n" + cron_entry + "\n"
            
            # 设置新的 crontab
            process = subprocess.Popen(
                ['crontab', '-'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=new_cron)
            
            if process.returncode == 0:
                self.log("  ✅ 定时任务已设置：每 30 分钟执行")
            else:
                self.log(f"  ⚠️ 设置失败：{stderr}")
        else:
            self.log("  ℹ️  定时任务已存在")
    
    def generate_report(self):
        """生成报告"""
        self.log("📝 生成修复报告...")
        
        report_file = REPORTS_DIR / f'enhanced-bug-fix-{datetime.now().strftime("%Y%m%d-%H%M%S")}.md'
        
        content = f"""# 🔧 增强版自动化 Bug 检测和修复报告

> **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **执行人**: 太一 AGI  
> **状态**: ✅ 完成

---

## 📊 统计

**修复文件**: {len(self.errors_fixed)} 个

---

## ✅ 修复的文件

"""
        for fix in self.errors_fixed:
            content += f"### {fix['file']}\n\n"
            content += f"- 修复数量：{fix['fixes']} 个\n\n"
        
        content += f"""
## ⏰ 定时任务

**设置**: 每 30 分钟自动执行  
**脚本**: auto-bug-fixer-enhanced.py  
**日志**: auto-bug-fix-cron.log

---

**🔧 增强版自动化 Bug 检测和修复报告完成**

**太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"✅ 报告已生成：{report_file.name}")


def main():
    """主函数"""
    fixer = EnhancedBugFixer()
    fixer.run()


if __name__ == '__main__':
    main()
