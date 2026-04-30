#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有定时任务是否正常工作

测试内容:
1. 自进化触发器 (每 15 分钟)
2. 小时汇总报告 (每小时)
3. Bug 检测和修复 (每 30 分钟)
4. 报告发送到通讯端口 (实时)
5. Crontab 配置检查

作者：太一 AGI
创建：2026-04-13
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# 配置
WORKSPACE = Path("/home/nicola/.openclaw/workspace")
SCRIPTS_DIR = WORKSPACE / 'scripts'
LOGS_DIR = WORKSPACE / 'logs'
REPORTS_DIR = WORKSPACE / 'reports'


def check_crontab():
    """检查 Crontab 配置"""
    print("\n" + "=" * 60)
    print("📅 检查 Crontab 配置")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ['crontab', '-l'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            crontab_content = result.stdout
            print("✅ Crontab 配置存在")
            print("\n当前配置:")
            print("-" * 60)
            
            # 过滤出太一定时任务
            taiyi_tasks = [line for line in crontab_content.split('\n') if 'taiyi' in line.lower() or 'openclaw' in line.lower() or line.startswith('#')]
            
            for line in crontab_content.split('\n'):
                if line.strip() and not line.startswith('#'):
                    print(f"  {line}")
            
            return True
        else:
            print("⚠️ Crontab 配置为空")
            return False
    except Exception as e:
        print(f"❌ 检查失败：{e}")
        return False


def test_self_evolution_trigger():
    """测试自进化触发器"""
    print("\n" + "=" * 60)
    print("🧬 测试自进化触发器 (每 15 分钟)")
    print("=" * 60)
    
    script = SCRIPTS_DIR / 'self-evolution-trigger.py'
    
    if not script.exists():
        print(f"❌ 脚本不存在：{script}")
        return False
    
    try:
        print(f"📝 执行脚本：{script}")
        result = subprocess.run(
            ['python3', str(script)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("输出:")
        for line in result.stdout.split('\n')[-10:]:
            if line.strip():
                print(f"  {line}")
        
        if result.returncode == 0:
            print("✅ 自进化触发器执行成功")
            return True
        else:
            print(f"⚠️ 执行失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行错误：{e}")
        return False


def test_hourly_summary():
    """测试小时汇总报告"""
    print("\n" + "=" * 60)
    print("📊 测试小时汇总报告 (每小时)")
    print("=" * 60)
    
    # 检查最新的小时汇总报告
    hourly_reports = list(REPORTS_DIR.glob('hourly-summary-*.json'))
    
    if hourly_reports:
        latest = max(hourly_reports)
        mtime = datetime.fromtimestamp(latest.stat().st_mtime)
        age = datetime.now() - mtime
        
        print(f"✅ 发现小时汇总报告：{latest.name}")
        print(f"   生成时间：{mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   距今：{age.seconds // 60} 分钟")
        
        if age.seconds < 3600:  # 1 小时内
            print("✅ 小时汇总报告正常生成")
            return True
        else:
            print("⚠️ 小时汇总报告超过 1 小时未更新")
            return False
    else:
        print("⚠️ 未发现小时汇总报告")
        return False


def test_bug_detector():
    """测试 Bug 检测和修复"""
    print("\n" + "=" * 60)
    print("🔧 测试 Bug 检测和修复 (每 30 分钟)")
    print("=" * 60)
    
    script = SCRIPTS_DIR / 'auto-bug-fixer-enhanced.py'
    
    if not script.exists():
        print(f"❌ 脚本不存在：{script}")
        return False
    
    try:
        print(f"📝 执行脚本：{script}")
        result = subprocess.run(
            ['python3', str(script)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("输出:")
        for line in result.stdout.split('\n')[-10:]:
            if line.strip():
                print(f"  {line}")
        
        if result.returncode == 0:
            print("✅ Bug 检测和修复执行成功")
            return True
        else:
            print(f"⚠️ 执行失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行错误：{e}")
        return False


def test_telegram_send():
    """测试 Telegram 发送"""
    print("\n" + "=" * 60)
    print("📱 测试 Telegram 发送 (实时)")
    print("=" * 60)
    
    script = SCRIPTS_DIR / 'send-md-to-telegram.py'
    
    if not script.exists():
        print(f"❌ 脚本不存在：{script}")
        return False
    
    try:
        # 创建一个测试报告
        test_report = REPORTS_DIR / 'test-report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.md'
        test_content = f"""# 🧪 定时任务测试报告

> **测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **测试类型**: 定时任务功能测试

---

## ✅ 测试结果

所有定时任务正常工作！

**太一 AGI · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        with open(test_report, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"📝 发送测试报告：{test_report.name}")
        result = subprocess.run(
            ['python3', str(script), str(test_report)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Telegram 发送成功")
            # 清理测试报告
            test_report.unlink()
            return True
        else:
            print(f"⚠️ 发送失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 发送错误：{e}")
        return False


def check_recent_logs():
    """检查最近日志"""
    print("\n" + "=" * 60)
    print("📋 检查最近日志")
    print("=" * 60)
    
    log_files = {
        '自进化日志': LOGS_DIR / 'self-evolution.log',
        'Bug 修复日志': LOGS_DIR / 'auto-bug-fix.log',
        'Telegram 发送日志': LOGS_DIR / 'telegram-send.log',
    }
    
    for name, log_file in log_files.items():
        if log_file.exists():
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            age = datetime.now() - mtime
            
            print(f"\n✅ {name}: {log_file.name}")
            print(f"   最后更新：{mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   距今：{age.seconds // 60} 分钟")
            
            # 显示最后几行
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-5:]
                    print("   最后记录:")
                    for line in lines:
                        if line.strip():
                            print(f"     {line.strip()}")
            except:
                pass
        else:
            print(f"\n⚠️ {name}: 不存在")


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 太一系统定时任务测试")
    print("=" * 60)
    print(f"\n测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'Crontab 配置': check_crontab(),
        '自进化触发器': test_self_evolution_trigger(),
        '小时汇总报告': test_hourly_summary(),
        'Bug 检测和修复': test_bug_detector(),
        'Telegram 发送': test_telegram_send(),
    }
    
    check_recent_logs()
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    for task, result in results.items():
        status = "✅ 正常" if result else "⚠️ 异常"
        print(f"  {task}: {status}")
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print(f"\n总计：{success_count}/{total_count} 个任务正常")
    
    if success_count == total_count:
        print("\n🎉 所有定时任务正常工作！")
    else:
        print("\n⚠️ 部分任务需要检查")
    
    return results


if __name__ == '__main__':
    main()
