#!/usr/bin/env python3
"""
升级守护脚本 - 整合版
功能：OpenClaw 版本检查、自动升级、升级历史、回滚支持
执行：python skills/monitoring/upgrade_guard.py [check|upgrade|history|rollback]
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
import argparse
import re

# ============================================================================
# 配置
# ============================================================================

WORKSPACE = Path('/home/nicola/.openclaw/workspace')
LOG_FILE = Path('/home/nicola/.openclaw/logs/upgrade-guard.log')
HISTORY_FILE = Path('/tmp/upgrade-history.json')
BACKUP_DIR = Path('/home/nicola/.openclaw/backups')

# npm 包名
NPM_PACKAGE = 'openclaw'

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
# 版本管理
# ============================================================================

def get_current_version():
    """获取当前安装的版本"""
    try:
        result = subprocess.run(
            ['npm', 'list', '-g', NPM_PACKAGE],
            capture_output=True, text=True, timeout=10
        )
        
        # 解析输出：openclaw@1.2.3 /path/to/package
        output = result.stdout.strip()
        match = re.search(r'openclaw@([\d.]+)', output)
        
        if match:
            version = match.group(1)
            log(f"当前版本：v{version}")
            return version
        else:
            log("无法获取当前版本")
            return None
    except Exception as e:
        log(f"获取版本失败：{e}")
        return None

def get_latest_version():
    """获取 npm 最新版本"""
    try:
        result = subprocess.run(
            ['npm', 'view', NPM_PACKAGE, 'version'],
            capture_output=True, text=True, timeout=10
        )
        
        version = result.stdout.strip()
        log(f"最新版本：v{version}")
        return version
    except Exception as e:
        log(f"获取最新版本失败：{e}")
        return None

def compare_versions(v1, v2):
    """比较版本号"""
    def normalize(v):
        return [int(x) for x in re.sub(r'[^0-9.]', '', v).split('.')]
    
    n1, n2 = normalize(v1), normalize(v2)
    
    for i in range(max(len(n1), len(n2))):
        a = n1[i] if i < len(n1) else 0
        b = n2[i] if i < len(n2) else 0
        
        if a < b:
            return -1  # v1 < v2
        elif a > b:
            return 1   # v1 > v2
    
    return 0  # v1 == v2

# ============================================================================
# 升级历史
# ============================================================================

def load_history():
    """加载升级历史"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    """保存升级历史"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2, default=str)

def record_upgrade(old_version, new_version, success=True):
    """记录升级历史"""
    history = load_history()
    
    history.append({
        'timestamp': datetime.now().isoformat(),
        'old_version': old_version,
        'new_version': new_version,
        'success': success
    })
    
    # 保留最近 20 条
    if len(history) > 20:
        history = history[-20:]
    
    save_history(history)

def show_history():
    """显示升级历史"""
    history = load_history()
    
    if not history:
        log("无升级历史")
        return
    
    log("=" * 50)
    log("📋 升级历史")
    log("=" * 50)
    
    for record in reversed(history[-10:]):  # 显示最近 10 条
        status = "✅" if record['success'] else "❌"
        time_str = datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M')
        log(f"{status} {time_str}: v{record['old_version']} → v{record['new_version']}")
    
    log("=" * 50)

# ============================================================================
# 备份管理
# ============================================================================

def create_backup():
    """创建当前版本备份"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    backup_path = BACKUP_DIR / f"openclaw-{timestamp}"
    
    log(f"创建备份：{backup_path}")
    
    try:
        # 备份配置文件
        config_dir = Path.home() / '.openclaw'
        if config_dir.exists():
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # 复制配置
            subprocess.run(
                ['cp', '-r', str(config_dir), str(backup_path / 'config')],
                timeout=30
            )
            
            log(f"✅ 备份完成：{backup_path}")
            return backup_path
        else:
            log("🟡 配置目录不存在，跳过备份")
            return None
    except Exception as e:
        log(f"❌ 备份失败：{e}")
        return None

def list_backups():
    """列出可用备份"""
    if not BACKUP_DIR.exists():
        log("无可用备份")
        return []
    
    backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir()])
    
    if not backups:
        log("无可用备份")
        return []
    
    log("可用备份:")
    for backup in backups[-5:]:  # 显示最近 5 个
        log(f"  - {backup.name}")
    
    return backups

# ============================================================================
# 升级操作
# ============================================================================

def check_upgrade():
    """检查是否有可用升级"""
    log("=" * 50)
    log("🔍 检查升级")
    log("=" * 50)
    
    current = get_current_version()
    latest = get_latest_version()
    
    if not current or not latest:
        log("❌ 无法获取版本信息")
        return None
    
    cmp = compare_versions(current, latest)
    
    if cmp < 0:
        log(f"🟡 发现新版本：v{current} → v{latest}")
        return latest
    elif cmp == 0:
        log(f"✅ 已是最新版本：v{current}")
        return None
    else:
        log(f"🟢 当前版本超前：v{current} (可能是开发版)")
        return None

def do_upgrade(auto=False):
    """执行升级"""
    log("=" * 50)
    log("⬆️  执行升级")
    log("=" * 50)
    
    # 检查新版本
    new_version = check_upgrade()
    
    if not new_version:
        log("无需升级")
        return False
    
    current_version = get_current_version()
    
    # 自动模式直接升级，手动模式需要确认
    if not auto:
        log(f"\n准备升级：v{current_version} → v{new_version}")
        log("提示：升级前会自动备份配置文件")
        # 实际使用时可以添加确认提示
    
    # 创建备份
    backup = create_backup()
    
    # 执行 npm 升级
    log(f"\n执行：npm install -g {NPM_PACKAGE}@latest")
    
    try:
        result = subprocess.run(
            ['npm', 'install', '-g', f'{NPM_PACKAGE}@latest'],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            log("✅ 升级成功")
            record_upgrade(current_version, new_version, success=True)
            
            # 验证升级
            verified = get_current_version()
            if verified == new_version:
                log(f"✅ 验证成功：v{verified}")
            else:
                log(f"🟡 验证警告：期望 v{new_version}, 实际 v{verified}")
            
            return True
        else:
            log(f"❌ 升级失败：{result.stderr}")
            record_upgrade(current_version, new_version, success=False)
            return False
    except subprocess.TimeoutExpired:
        log("❌ 升级超时")
        record_upgrade(current_version, new_version, success=False)
        return False
    except Exception as e:
        log(f"❌ 升级异常：{e}")
        record_upgrade(current_version, new_version, success=False)
        return False

def rollback(target_version=None):
    """回滚到指定版本"""
    log("=" * 50)
    log("🔙 执行回滚")
    log("=" * 50)
    
    if not target_version:
        # 回滚到上一个版本
        history = load_history()
        if len(history) >= 2:
            target_version = history[-2]['old_version']
            log(f"回滚到上一版本：v{target_version}")
        else:
            log("❌ 无可用回滚版本")
            return False
    
    current_version = get_current_version()
    
    log(f"执行：npm install -g {NPM_PACKAGE}@{target_version}")
    
    try:
        result = subprocess.run(
            ['npm', 'install', '-g', f'{NPM_PACKAGE}@{target_version}'],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            log(f"✅ 回滚成功：v{target_version}")
            record_upgrade(current_version, target_version, success=True)
            return True
        else:
            log(f"❌ 回滚失败：{result.stderr}")
            return False
    except Exception as e:
        log(f"❌ 回滚异常：{e}")
        return False

# ============================================================================
# 每日检查 (Cron 调用)
# ============================================================================

def daily_check():
    """每日自动检查升级"""
    log("=" * 50)
    log("📅 每日升级检查")
    log("=" * 50)
    
    new_version = check_upgrade()
    
    if new_version:
        log(f"\n🟡 发现新版本：可用 v{new_version}")
        log("提示：运行以下命令升级:")
        log(f"  npm install -g {NPM_PACKAGE}@latest")
        
        # 可以添加通知
        # send_alert('normal', f"OpenClaw 新版本可用：v{new_version}")
    else:
        log("✅ 已是最新版本")
    
    return new_version is not None

# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='升级守护脚本')
    parser.add_argument('action', nargs='?', default='check',
                       choices=['check', 'upgrade', 'history', 'rollback', 'daily'],
                       help='操作：check(检查) | upgrade(升级) | history(历史) | rollback(回滚) | daily(每日检查)')
    parser.add_argument('--auto', action='store_true', help='自动模式 (无需确认)')
    parser.add_argument('--version', type=str, help='指定版本 (用于 rollback)')
    args = parser.parse_args()
    
    if args.action == 'check':
        check_upgrade()
    
    elif args.action == 'upgrade':
        do_upgrade(auto=args.auto)
    
    elif args.action == 'history':
        show_history()
    
    elif args.action == 'rollback':
        rollback(target_version=args.version)
    
    elif args.action == 'daily':
        daily_check()

if __name__ == '__main__':
    main()
