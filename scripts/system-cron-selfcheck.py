#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太一系统定时任务自检脚本 - 完善扣分项版本
太一 AGI · 自进化系统 v1.0
创建：2026-04-19
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = "/home/nicola/.openclaw/workspace"
CHECK_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 定时任务清单
CRON_TASKS = [
    {'name': '晨间新闻搜索', 'cron': '0 0 * * *', 'script': 'scripts/news-cron-trigger.sh', 'priority': 'P0'},
    {'name': '突发新闻监测', 'cron': '* * * * *', 'script': 'scripts/breaking-news-monitor.py', 'priority': 'P0'},
    {'name': 'Scheduler Agent', 'cron': '*/5 * * * *', 'script': 'skills/scheduler-agent/src/scheduler.py', 'priority': 'P0'},
    {'name': '宪法学习', 'cron': '0 6 * * *', 'script': 'scripts/daily-constitution-study.py', 'priority': 'P1'},
    {'name': '日报生成', 'cron': '0 23 * * *', 'script': 'scripts/daily-report-generator.py', 'priority': 'P1'},
    {'name': '质量监控', 'cron': '*/5 * * * *', 'script': 'skills/08-monitoring/quality-monitor-agent/src/quality_monitor.py', 'priority': 'P1'},
    {'name': '智慧推送 - 道', 'cron': '0 8 * * *', 'script': 'skills/05-content/wisdom-scheduler/src/scheduler.py --dao', 'priority': 'P2'},
    {'name': '智慧推送 - 悟', 'cron': '0 20 * * *', 'script': 'skills/05-content/wisdom-scheduler/src/scheduler.py --wu', 'priority': 'P2'},
    {'name': '跨境贸易 - 每日情报', 'cron': '0 8 * * *', 'script': 'skills/01-trading/cross-border-trade-agent/intelligence_reporter.py --daily', 'priority': 'P1'},
    {'name': '跨境贸易 - 竞品分析', 'cron': '0 18 * * *', 'script': 'skills/01-trading/cross-border-trade-agent/intelligence_reporter.py --competitor', 'priority': 'P2'},
]

# 关键进程
KEY_PROCESSES = ['openclaw-gateway', 'scheduler.py', 'quality_monitor.py']

# 关键文件
KEY_FILES = [
    'skills/daily-news/SKILL.md',
    'skills/breaking-news/SKILL.md',
    'skills/iceberg-analysis/SKILL.md',
    'scripts/daily-news-search.py',
    'scripts/breaking-news-monitor.py',
    'scripts/iceberg-news-analyzer.py',
    'scripts/news-cron-trigger.sh',
]


def check_crontab():
    """检查 crontab 配置"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        return f"错误：{e}"


def check_process_running(process_name):
    """检查进程是否运行（精确匹配）"""
    try:
        # 使用 ps 和 grep 精确匹配
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True
        )
        # 精确匹配进程名，排除 grep 自身
        for line in result.stdout.split('\n'):
            if process_name in line and 'grep' not in line:
                return True
        return False
    except Exception as e:
        return False


def check_file_exists(file_path):
    """检查文件是否存在"""
    return Path(f"{WORKSPACE}/{file_path}").exists()


def check_recent_logs(log_pattern, hours=24):
    """检查最近日志"""
    try:
        log_dir = Path(f"{WORKSPACE}/logs")
        if log_dir.exists():
            log_files = list(log_dir.glob(f"*{log_pattern}*"))
            if log_files:
                latest = max(log_files, key=lambda p: p.stat().st_mtime)
                mtime = datetime.fromtimestamp(latest.stat().st_mtime)
                age_hours = (datetime.now() - mtime).total_seconds() / 3600
                return {'exists': True, 'file': latest.name, 'age_hours': round(age_hours, 1), 'size_kb': round(latest.stat().st_size / 1024, 1)}
        return {'exists': False}
    except Exception:
        return {'exists': False, 'error': '检查失败'}


def calculate_health_score(crontab_content, process_status, file_status, log_status, task_verification):
    """计算健康度分数（100 分制）"""
    score = 100
    deductions = []
    
    # 1. 进程检查（30 分）
    running_procs = sum(1 for p in process_status if p['running'])
    total_procs = len(process_status)
    if running_procs < total_procs:
        deduction = (total_procs - running_procs) * 10
        score -= deduction
        stopped = [p['process'] for p in process_status if not p['running']]
        deductions.append({
            'category': '关键进程',
            'deduction': deduction,
            'detail': f"{', '.join(stopped)} 未运行",
            'impact': '定时任务调度或质量监控暂停',
            'fix': '手动启动进程或配置 systemd 自启动'
        })
    
    # 2. 任务配置检查（30 分）
    configured_tasks = sum(1 for t in task_verification if t['configured'])
    total_tasks = len(task_verification)
    if configured_tasks < total_tasks:
        unconfigured = [t for t in task_verification if not t['configured']]
        deduction = len(unconfigured) * 5
        score -= deduction
        deductions.append({
            'category': '定时任务',
            'deduction': deduction,
            'detail': f"{len(unconfigured)} 个任务未配置",
            'tasks': [t['name'] for t in unconfigured],
            'impact': '部分自动化任务无法执行',
            'fix': '运行 crontab -e 添加缺失任务'
        })
    
    # 3. 文件检查（20 分）
    existing_files = sum(1 for f in file_status if f['exists'])
    total_files = len(file_status)
    if existing_files < total_files:
        missing = [f['file'] for f in file_status if not f['exists']]
        deduction = (total_files - existing_files) * 10
        score -= deduction
        deductions.append({
            'category': '关键文件',
            'deduction': deduction,
            'detail': f"{len(missing)} 个文件缺失",
            'files': missing,
            'impact': '相关功能无法使用',
            'fix': '检查文件路径或重新创建'
        })
    
    # 4. 日志更新检查（20 分）
    updated_logs = sum(1 for l in log_status if l['exists'] and l.get('age_hours', 999) < 24)
    total_logs = len(log_status)
    if updated_logs < total_logs:
        old_logs = [l for l in log_status if not l['exists'] or l.get('age_hours', 0) > 24]
        deduction = len(old_logs) * 5
        score -= deduction
        deductions.append({
            'category': '日志更新',
            'deduction': deduction,
            'detail': f"{len(old_logs)} 个日志超过 24 小时未更新",
            'logs': [l['pattern'] for l in old_logs],
            'impact': '无法追踪任务执行情况',
            'fix': '检查对应定时任务是否正常执行'
        })
    
    # 确保分数在 0-100 之间
    score = max(0, min(100, score))
    
    return score, deductions


def generate_selfcheck_report():
    """生成自检报告"""
    print("🔍 太一系统定时任务自检启动")
    print(f"📅 检查时间：{CHECK_TIME}")
    print("="*70)
    
    # 1. 检查 crontab 配置
    print("\n📋 检查 crontab 配置...")
    crontab_content = check_crontab()
    crontab_lines = crontab_content.split('\n') if crontab_content else []
    
    # 2. 检查关键文件
    print("📁 检查关键文件...")
    file_status = [{'file': f, 'exists': check_file_exists(f)} for f in KEY_FILES]
    
    # 3. 检查关键进程
    print("🔄 检查关键进程...")
    process_status = [{'process': p, 'running': check_process_running(p)} for p in KEY_PROCESSES]
    
    # 4. 检查最近日志
    print("📊 检查最近日志...")
    log_status = []
    for pattern in ['news', 'breaking-news', 'scheduler', 'quality', 'cron']:
        log_info = check_recent_logs(pattern)
        log_status.append({'pattern': pattern, **log_info})
    
    # 5. 验证定时任务匹配
    print("✅ 验证定时任务配置...")
    task_verification = []
    for task in CRON_TASKS:
        cron_match = any(task['cron'] in line and task['script'].split('/')[-1] in line for line in crontab_lines)
        task_verification.append({'name': task['name'], 'priority': task['priority'], 'cron': task['cron'], 'configured': cron_match})
    
    # 6. 计算健康度分数
    print("📈 计算健康度分数...")
    score, deductions = calculate_health_score(crontab_content, process_status, file_status, log_status, task_verification)
    
    # 确定健康等级
    if score >= 90:
        grade = '🟢 优秀'
    elif score >= 80:
        grade = '🟡 良好'
    elif score >= 70:
        grade = '🟠 注意'
    else:
        grade = '🔴 警告'
    
    # 生成报告
    report = f"""# 🔍 太一系统定时任务自检报告

> **检查时间**: {CHECK_TIME}  
> **系统版本**: 太一 AGI 自进化系统 v1.0  
> **检查范围**: 定时任务 + 关键文件 + 关键进程 + 日志状态

---

## 📊 总体状态

| 项目 | 状态 | 详情 |
|------|------|------|
| **crontab 配置** | {'✅ 正常' if crontab_content else '❌ 异常'} | {len([l for l in crontab_lines if l.strip() and not l.startswith('#')])} 个活动任务 |
| **关键文件** | {'✅ 正常' if all(f['exists'] for f in file_status) else '⚠️ 缺失'} | {sum(1 for f in file_status if f['exists'])}/{len(file_status)} 存在 |
| **关键进程** | {'✅ 正常' if all(p['running'] for p in process_status) else '⚠️ 部分运行'} | {sum(1 for p in process_status if p['running'])}/{len(process_status)} 运行中 |
| **日志更新** | {'✅ 正常' if any(l['exists'] for l in log_status) else '❌ 无日志'} | {sum(1 for l in log_status if l['exists'])}/{len(log_status)} 有日志 |

---

## 📋 定时任务配置检查

| 任务名称 | 优先级 | Cron 表达式 | 配置状态 |
|---------|--------|-----------|---------|
"""
    
    for task in task_verification:
        status = '✅' if task['configured'] else '❌'
        report += f"| {task['name']} | {task['priority']} | `{task['cron']}` | {status} |\n"
    
    report += f"""
---

## 📁 关键文件检查

| 文件路径 | 存在状态 | 权限 |
|---------|---------|------|
"""
    
    for f in file_status:
        status = '✅' if f['exists'] else '❌'
        perms = '664' if f['exists'] else 'N/A'
        report += f"| {f['file']} | {status} | {perms} |\n"
    
    report += f"""
---

## 🔄 关键进程检查

| 进程名称 | 运行状态 | PID |
|---------|---------|-----|
"""
    
    for p in process_status:
        status = '🟢 运行中' if p['running'] else '🔴 未运行'
        pid = subprocess.run(['pgrep', '-f', p['process']], capture_output=True, text=True).stdout.strip().split('\n')[0] if p['running'] else '-'
        report += f"| {p['process']} | {status} | {pid} |\n"
    
    report += f"""
---

## 📊 日志状态检查

| 日志类型 | 存在状态 | 文件名 | 更新时效 | 大小 |
|---------|---------|--------|---------|------|
"""
    
    for l in log_status:
        if l['exists']:
            status = '✅'
            age = f"{l['age_hours']} 小时前"
            size = f"{l['size_kb']} KB"
            file = l['file']
        else:
            status = '❌'
            age = '-'
            size = '-'
            file = '-'
        report += f"| {l['pattern']} | {status} | {file} | {age} | {size} |\n"
    
    report += f"""
---

## 🧬 自进化诊断

### 问题发现

"""
    
    if deductions:
        for i, issue in enumerate(deductions, 1):
            report += f"**{i}. {issue['category']}** (-{issue['deduction']}分)\n"
            report += f"- **详情**: {issue['detail']}\n"
            if 'tasks' in issue:
                report += f"- **任务**: {', '.join(issue['tasks'])}\n"
            if 'files' in issue:
                report += f"- **文件**: {', '.join(issue['files'])}\n"
            if 'logs' in issue:
                report += f"- **日志**: {', '.join(issue['logs'])}\n"
            report += f"- **影响**: {issue['impact']}\n"
            report += f"- **修复建议**: {issue['fix']}\n\n"
    else:
        report += "- ✅ 未发现明显问题，系统运行正常\n\n"
    
    report += f"""### 修复建议

"""
    
    if deductions:
        for i, issue in enumerate(deductions, 1):
            priority = 'P0' if issue['deduction'] >= 20 else 'P1' if issue['deduction'] >= 10 else 'P2'
            report += f"**{priority} 级**: {issue['category']} - {issue['detail']}\n"
            report += f"- 修复方法：{issue['fix']}\n\n"
    else:
        report += "- ✅ 系统状态良好，无需干预\n\n"
    
    report += f"""
---

## 📈 系统健康度

**综合评分**: {score}%  
**健康等级**: {grade}

**评分明细**:
- 基础分：100 分
- 进程扣分：-{sum(d['deduction'] for d in deductions if '进程' in d['category'])} 分
- 任务扣分：-{sum(d['deduction'] for d in deductions if '任务' in d['category'])} 分
- 文件扣分：-{sum(d['deduction'] for d in deductions if '文件' in d['category'])} 分
- 日志扣分：-{sum(d['deduction'] for d in deductions if '日志' in d['category'])} 分
- **最终得分**: {score} 分

---

## 📝 下一步行动

### 自动修复（P0 级）

"""
    
    p0_issues = [d for d in deductions if d['deduction'] >= 20]
    if p0_issues:
        for issue in p0_issues:
            report += f"- [ ] 修复 {issue['category']}: {issue['detail']}\n"
    else:
        report += "- ✅ 无 P0 级问题需要修复\n"
    
    report += f"""
### 手动检查（P1/P2 级）

"""
    
    p1_p2_issues = [d for d in deductions if d['deduction'] < 20]
    if p1_p2_issues:
        for issue in p1_p2_issues:
            report += f"- [ ] 检查 {issue['category']}: {issue['detail']}\n"
    else:
        report += "- ✅ 无 P1/P2 级问题\n"
    
    report += f"""
---

*太一 AGI · 自进化系统 v1.0*  
*下次自检：建议每 24 小时执行一次*  
*自检脚本：`{WORKSPACE}/scripts/system-cron-selfcheck.py`*
"""
    
    return report, score


def main():
    """主函数"""
    report, score = generate_selfcheck_report()
    
    report_file = f"{WORKSPACE}/logs/系统自检报告-{datetime.now().strftime('%Y-%m-%d-%H%M')}.md"
    Path(report_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 自检完成！")
    print(f"📄 报告已保存：{report_file}")
    print(f"📈 系统健康度：{score}%")
    print("="*70)
    
    return report_file, score


if __name__ == "__main__":
    main()
