#!/usr/bin/env python3
"""
系统自检脚本 - 整合版
功能：Gateway 检查、进程清理、Cron 验证、Bot 状态、资源监控、宪法文件检查
执行：python skills/monitoring/self_check.py [--full|--report]
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
import argparse

# ============================================================================
# 配置
# ============================================================================

WORKSPACE = Path('/home/nicola/.openclaw/workspace')
REPORT_DIR = WORKSPACE / 'reports'
LOG_FILE = Path('/home/nicola/.openclaw/logs/self-check.log')

# Bot 列表
BOTS = ['taiyi', 'zhiji', 'shanmu', 'suwen', 'wangliang', 'paoding', 'yi', 'shoucangli']

# 核心宪法文件
CORE_FILES = [
    'constitution/CONST-ROUTER.md',
    'constitution/axiom/VALUE-FOUNDATION.md',
    'constitution/directives/NEGENTROPY.md',
    'constitution/directives/AGI-TIMELINE.md',
    'constitution/directives/OBSERVER.md',
    'constitution/directives/SELF-LOOP.md',
    'constitution/skills/MODEL-ROUTING.md',
    'constitution/directives/ASK-PROTOCOL.md',
    'constitution/COLLABORATION.md',
    'constitution/extensions/DELEGATION.md',
    'constitution/directives/TURBOQUANT.md',
    'SOUL.md',
    'USER.md',
    'HEARTBEAT.md'
]

# 自检项目
CHECKS = [
    {"name": "Gateway 状态", "type": "process", "pattern": "openclaw gateway"},
    {"name": "Cron 任务", "type": "cron", "expected": 10, "command": "crontab -l 2>/dev/null | grep -E 'skills/|scripts/.*evolution|scripts/.*degradation' | wc -l"},
    {"name": "Bot 配置", "type": "bot_config"},
    {"name": "磁盘空间", "type": "disk"},
    {"name": "内存使用", "type": "memory"},
    {"name": "宪法文件", "type": "constitution"},
    {"name": "网络连通", "type": "network", "condition": "full"}
]

# ============================================================================
# 日志函数
# ============================================================================

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}\n"
    print(log_line.strip())
    
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(log_line)
    except Exception as e:
        pass

# ============================================================================
# 检查函数
# ============================================================================

def check_gateway():
    """检查 Gateway 状态"""
    log("检查 Gateway 状态...")
    
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'openclaw gateway'],
            capture_output=True, text=True, timeout=5
        )
        
        pid = result.stdout.strip().split('\n')[0] if result.stdout.strip() else None
        
        if pid:
            log(f"✅ Gateway 运行中 (PID: {pid})")
            return {'status': '✅', 'detail': f'PID: {pid}'}
        else:
            log("🔴 Gateway 已停止")
            
            # 尝试重启
            log("尝试重启 Gateway...")
            restart_script = WORKSPACE / 'scripts' / 'gateway-quick-restart.sh'
            if restart_script.exists():
                subprocess.run([str(restart_script)], shell=True, timeout=30)
                
                # 检查是否重启成功
                result = subprocess.run(
                    ['pgrep', '-f', 'openclaw gateway'],
                    capture_output=True, text=True, timeout=5
                )
                pid = result.stdout.strip().split('\n')[0] if result.stdout.strip() else None
                
                if pid:
                    log(f"✅ Gateway 重启成功 (PID: {pid})")
                    return {'status': '✅', 'detail': f'重启成功，PID: {pid}'}
                else:
                    log("🔴 Gateway 重启失败")
                    return {'status': '❌', 'detail': '重启失败'}
            else:
                log("🔴 重启脚本不存在")
                return {'status': '❌', 'detail': '已停止'}
    except Exception as e:
        log(f"❌ Gateway 检查异常：{e}")
        return {'status': '❌', 'detail': str(e)}

def cleanup_processes():
    """清理残留进程"""
    log("检查残留进程...")
    
    try:
        # 获取当前 PID
        pid_file = Path.home() / '.openclaw' / 'gateway.pid'
        current_pid = pid_file.read_text().strip() if pid_file.exists() else None
        
        # 查找所有 openclaw 进程
        result = subprocess.run(
            ['ps', 'aux'], capture_output=True, text=True, timeout=5
        )
        
        count = 0
        for line in result.stdout.split('\n'):
            if 'openclaw' in line and 'grep' not in line:
                if current_pid and current_pid not in line:
                    count += 1
        
        if count > 0:
            log(f"🟡 发现 {count} 个残留进程，清理中...")
            subprocess.run(['pkill', '-f', 'openclaw.*session'], timeout=5)
            log("✅ 清理完成")
            return {'status': '✅', 'detail': f'清理 {count} 个残留进程'}
        else:
            log("✅ 无残留进程")
            return {'status': '✅', 'detail': '无残留'}
    except Exception as e:
        log(f"❌ 进程清理异常：{e}")
        return {'status': '❌', 'detail': str(e)}

def check_crons():
    """检查 Cron 任务"""
    log("检查 Cron 任务...")
    
    try:
        result = subprocess.run(
            'crontab -l 2>/dev/null | wc -l',
            shell=True, capture_output=True, text=True, timeout=5
        )
        
        count = int(result.stdout.strip())
        
        if count >= 10:
            log(f"✅ Cron 任务：{count}项")
            return {'status': '✅', 'detail': f'{count}项'}
        else:
            log(f"🟡 Cron 任务：{count}项 (目标≥10)")
            return {'status': '🟡', 'detail': f'{count}项'}
    except Exception as e:
        log(f"❌ Cron 检查异常：{e}")
        return {'status': '❌', 'detail': str(e)}

def check_bot_configs():
    """检查 Bot 配置"""
    log("检查 Bot 配置...")
    
    results = []
    missing = []
    
    for bot in BOTS:
        config_file = WORKSPACE / 'config' / f'bot-{bot}.json'
        if config_file.exists():
            results.append({'status': '✅', 'name': bot})
        else:
            results.append({'status': '🟡', 'name': bot})
            missing.append(bot)
    
    if missing:
        log(f"🟡 Bot 配置缺失：{', '.join(missing)}")
    else:
        log(f"✅ Bot 配置：{len(BOTS)}/{len(BOTS)}")
    
    return {
        'status': '✅' if not missing else '🟡',
        'detail': f'{len(BOTS) - len(missing)}/{len(BOTS)}',
        'bots': results
    }

def check_resources():
    """检查系统资源"""
    log("检查系统资源...")
    
    results = {}
    
    # 磁盘
    try:
        result = subprocess.run(
            ['df', '-h', '/'], capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            disk_usage = int(parts[4].replace('%', ''))
            disk_avail = parts[3]
            
            if disk_usage < 80:
                results['disk'] = {'status': '✅', 'detail': f'{disk_usage}% (剩余 {disk_avail})'}
                log(f"✅ 磁盘：{disk_usage}% (剩余 {disk_avail})")
            elif disk_usage < 90:
                results['disk'] = {'status': '🟡', 'detail': f'{disk_usage}% (剩余 {disk_avail})'}
                log(f"🟡 磁盘告警：{disk_usage}% (剩余 {disk_avail})")
            else:
                results['disk'] = {'status': '🔴', 'detail': f'{disk_usage}% (剩余 {disk_avail})'}
                log(f"🔴 磁盘紧急：{disk_usage}% (剩余 {disk_avail})")
    except Exception as e:
        results['disk'] = {'status': '❌', 'detail': str(e)}
    
    # 内存
    try:
        result = subprocess.run(
            ['free'], capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            mem_total = int(parts[1])
            mem_used = int(parts[2])
            mem_avail = parts[6] if len(parts) > 6 else 'N/A'
            mem_usage = int((mem_used / mem_total) * 100)
            
            if mem_usage < 70:
                results['memory'] = {'status': '✅', 'detail': f'{mem_usage}% (剩余 {mem_avail})'}
                log(f"✅ 内存：{mem_usage}% (剩余 {mem_avail})")
            elif mem_usage < 85:
                results['memory'] = {'status': '🟡', 'detail': f'{mem_usage}% (剩余 {mem_avail})'}
                log(f"🟡 内存告警：{mem_usage}% (剩余 {mem_avail})")
            else:
                results['memory'] = {'status': '🔴', 'detail': f'{mem_usage}% (剩余 {mem_avail})'}
                log(f"🔴 内存紧急：{mem_usage}% (剩余 {mem_avail})")
    except Exception as e:
        results['memory'] = {'status': '❌', 'detail': str(e)}
    
    return results

def check_constitution():
    """检查宪法文件"""
    log("检查宪法文件...")
    
    results = []
    missing = []
    
    for file_path in CORE_FILES:
        full_path = WORKSPACE / file_path
        if full_path.exists():
            results.append({'status': '✅', 'name': os.path.basename(file_path)})
        else:
            results.append({'status': '🔴', 'name': os.path.basename(file_path)})
            missing.append(file_path)
    
    if missing:
        log(f"🔴 缺失宪法文件：{', '.join(os.path.basename(f) for f in missing)}")
    else:
        log(f"✅ 宪法文件：{len(CORE_FILES)}/{len(CORE_FILES)}")
    
    return {
        'status': '✅' if not missing else '🔴',
        'detail': f'{len(CORE_FILES) - len(missing)}/{len(CORE_FILES)}',
        'files': results
    }

def check_network():
    """检查网络连通性"""
    log("检查网络连通性...")
    
    results = {}
    
    # 外网
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '2', '8.8.8.8'],
            capture_output=True, timeout=5
        )
        if result.returncode == 0:
            results['internet'] = {'status': '✅', 'detail': '连通'}
            log("✅ 外网连通")
        else:
            results['internet'] = {'status': '🔴', 'detail': '不通'}
            log("🔴 外网不通")
    except:
        results['internet'] = {'status': '🔴', 'detail': '检查失败'}
    
    # 代理
    try:
        result = subprocess.run(
            ['curl', '-s', '--connect-timeout', '3', '-x', 'http://127.0.0.1:7890', 'https://www.google.com'],
            capture_output=True, timeout=5
        )
        if result.returncode == 0:
            results['proxy'] = {'status': '✅', 'detail': '正常 (7890)'}
            log("✅ 代理正常 (7890)")
        else:
            results['proxy'] = {'status': '🟡', 'detail': '异常 (7890)'}
            log("🟡 代理异常 (7890)")
    except:
        results['proxy'] = {'status': '❌', 'detail': '检查失败'}
    
    return results

# ============================================================================
# 报告生成
# ============================================================================

def generate_report(results, full_mode=False):
    """生成 Markdown 报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    report = f"""## 🔍 系统自检报告

**时间**: {timestamp}
**执行 Bot**: 太一
**模式**: {'完整' if full_mode else '快速'}

### 检查结果

"""
    
    # Gateway
    if 'gateway' in results:
        r = results['gateway']
        report += f"- {r['status']} **Gateway**: {r['detail']}\n"
    
    # 进程清理
    if 'cleanup' in results:
        r = results['cleanup']
        report += f"- {r['status']} **进程清理**: {r['detail']}\n"
    
    # Cron
    if 'crons' in results:
        r = results['crons']
        report += f"- {r['status']} **Cron 任务**: {r['detail']}\n"
    
    # Bot 配置
    if 'bots' in results:
        r = results['bots']
        report += f"- {r['status']} **Bot 配置**: {r['detail']}\n"
    
    # 资源
    if 'resources' in results:
        res = results['resources']
        if 'disk' in res:
            report += f"- {res['disk']['status']} **磁盘**: {res['disk']['detail']}\n"
        if 'memory' in res:
            report += f"- {res['memory']['status']} **内存**: {res['memory']['detail']}\n"
    
    # 宪法
    if 'constitution' in results:
        r = results['constitution']
        report += f"- {r['status']} **宪法文件**: {r['detail']}\n"
    
    # 网络 (仅完整模式)
    if full_mode and 'network' in results:
        net = results['network']
        if 'internet' in net:
            report += f"- {net['internet']['status']} **外网**: {net['internet']['detail']}\n"
        if 'proxy' in net:
            report += f"- {net['proxy']['status']} **代理**: {net['proxy']['detail']}\n"
    
    # 统计
    report += "\n### 📊 统计\n\n"
    
    total = sum(1 for v in results.values() if isinstance(v, dict) and 'status' in v)
    ok = sum(1 for v in results.values() if isinstance(v, dict) and v.get('status') == '✅')
    
    report += f"- **总检查项**: {total}\n"
    report += f"- **通过**: {ok}\n"
    report += f"- **通过率**: {ok*100//total if total > 0 else 0}%\n"
    
    # 下一步
    report += """
### 下一步

- [ ] 自检完成，系统正常

---
"""
    report += f"*执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 太一 AGI | Self-Check v1.0*"
    
    return report

# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='系统自检脚本')
    parser.add_argument('--full', action='store_true', help='完整模式 (含网络检查)')
    parser.add_argument('--report', action='store_true', help='生成报告文件')
    args = parser.parse_args()
    
    log("=" * 50)
    log("🔍 系统自检启动")
    log("=" * 50)
    
    results = {}
    
    # 执行检查
    results['gateway'] = check_gateway()
    results['cleanup'] = cleanup_processes()
    results['crons'] = check_crons()
    results['bots'] = check_bot_configs()
    results['resources'] = check_resources()
    results['constitution'] = check_constitution()
    
    # 完整模式增加网络检查
    if args.full:
        log("")
        results['network'] = check_network()
    
    # 生成报告
    log("")
    report = generate_report(results, args.full)
    print(report)
    
    # 保存报告
    if args.report:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_file = REPORT_DIR / f"self-check-{datetime.now().strftime('%Y%m%d-%H%M')}.md"
        report_file.write_text(report)
        log(f"\n📄 报告已保存：{report_file}")
    
    log("=" * 50)
    log("✅ 自检完成")
    log("=" * 50)

if __name__ == '__main__':
    main()
