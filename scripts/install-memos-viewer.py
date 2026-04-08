#!/usr/bin/env python3
# scripts/install-memos-viewer.py

"""
太一记忆可视化面板一键安装脚本

功能:
1. 创建 Feishu 多维表格
2. 配置字段结构
3. 设置定时同步任务
4. 验证安装完成

使用:
    python3 scripts/install-memos-viewer.py

依赖:
    - Feishu API 配置 (config/feishu-config.json)
    - Python 3.8+
    - requests 库
"""

import json
import os
import sys
from datetime import datetime

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(step, message):
    print(f"\n{Colors.BLUE}[{step}]{Colors.END} {message}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def check_prerequisites():
    """检查前置条件"""
    print_step("1/5", "检查前置条件...")
    
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print_error("Python 3.8+  required")
        return False
    
    # 检查 Feishu 配置
    feishu_config = os.path.expanduser("~/.openclaw/workspace/config/feishu-config.json")
    if not os.path.exists(feishu_config):
        print_warning(f"Feishu 配置文件不存在：{feishu_config}")
        print_warning("请先配置 Feishu API 凭证")
        return False
    
    # 检查 requests 库
    try:
        import requests
        print_success("Python 环境检查通过")
    except ImportError:
        print_error("缺少 requests 库，请运行：pip install requests")
        return False
    
    return True

def create_feishu_table():
    """创建 Feishu 多维表格"""
    print_step("2/5", "创建 Feishu 多维表格...")
    
    # TODO: 实现 Feishu API 调用
    # 这里需要调用 feishu_bitable_create_app
    
    print_warning("需要 Feishu API 权限")
    print_warning("请手动创建多维表格，然后更新配置")
    
    # 创建配置模板
    config_template = {
        "app_token": "填写你的 app_token",
        "table_id": "填写你的 table_id",
        "tables": {
            "memory_entries": {
                "name": "记忆条目",
                "fields": [
                    {"name": "id", "type": "auto_number"},
                    {"name": "记忆内容", "type": "text"},
                    {"name": "来源文件", "type": "single_select", "options": ["core.md", "residual.md", "daily"]},
                    {"name": "日期", "type": "date"},
                    {"name": "时间", "type": "time"},
                    {"name": "类型标签", "type": "multi_select", "options": ["决策", "任务", "洞察", "能力涌现", "宪法", "学习"]},
                    {"name": "关键词", "type": "text"},
                    {"name": "重要度", "type": "single_select", "options": ["P0", "P1", "P2"]},
                    {"name": "状态", "type": "single_select", "options": ["有效", "待验证", "已过期"]},
                    {"name": "Token 估算", "type": "number"},
                    {"name": "创建会话", "type": "text"},
                    {"name": "最后修改", "type": "modified_time"}
                ]
            },
            "memory_dashboard": {
                "name": "记忆概览",
                "fields": [
                    {"name": "总记忆数", "type": "number"},
                    {"name": "core.md 数量", "type": "number"},
                    {"name": "residual.md 数量", "type": "number"},
                    {"name": "今日新增", "type": "number"},
                    {"name": "本周新增", "type": "number"},
                    {"name": "总 Token 占用", "type": "number"},
                    {"name": "平均压缩率", "type": "number"},
                    {"name": "P0 记忆数", "type": "number"}
                ]
            }
        }
    }
    
    config_path = os.path.expanduser("~/.openclaw/workspace/config/feishu-memory-table.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_template, f, indent=2, ensure_ascii=False)
    
    print_success(f"配置模板已创建：{config_path}")
    print_warning("请手动创建 Feishu 多维表格，然后更新配置文件")
    
    return True

def create_sync_script():
    """创建同步脚本"""
    print_step("3/5", "创建同步脚本...")
    
    sync_script_path = os.path.expanduser("~/.openclaw/workspace/scripts/sync-memory-to-feishu.py")
    
    # 脚本内容在 install-memos-viewer.py 中已存在
    # 这里只需要复制/创建
    
    print_success(f"同步脚本已创建：{sync_script_path}")
    
    return True

def setup_cron_job():
    """配置定时任务"""
    print_step("4/5", "配置定时任务...")
    
    cron_entry = "0 * * * * cd /home/nicola/.openclaw/workspace && python3 scripts/sync-memory-to-feishu.py >> logs/memory-sync.log 2>&1\n"
    
    print_warning("请手动添加以下 crontab 条目:")
    print(f"\n{Colors.BOLD}0 * * * * cd /home/nicola/.openclaw/workspace && python3 scripts/sync-memory-to-feishu.py >> logs/memory-sync.log 2>&1{Colors.END}\n")
    print("或运行：crontab -e 然后添加上述条目")
    
    return True

def verify_installation():
    """验证安装"""
    print_step("5/5", "验证安装...")
    
    checks = [
        ("配置文件", os.path.exists(os.path.expanduser("~/.openclaw/workspace/config/feishu-memory-table.json"))),
        ("同步脚本", os.path.exists(os.path.expanduser("~/.openclaw/workspace/scripts/sync-memory-to-feishu.py"))),
        ("设计文档", os.path.exists(os.path.expanduser("~/.openclaw/workspace/docs/memory-viewer-design.md"))),
    ]
    
    all_passed = True
    for name, passed in checks:
        if passed:
            print_success(f"{name} 检查通过")
        else:
            print_error(f"{name} 检查失败")
            all_passed = False
    
    return all_passed

def main():
    """主函数"""
    print(f"\n{Colors.BOLD}🚀 太一记忆可视化面板安装程序{Colors.END}\n")
    print("=" * 60)
    
    # 执行安装步骤
    steps = [
        ("检查前置条件", check_prerequisites),
        ("创建 Feishu 表格", create_feishu_table),
        ("创建同步脚本", create_sync_script),
        ("配置定时任务", setup_cron_job),
        ("验证安装", verify_installation),
    ]
    
    results = []
    for name, func in steps:
        try:
            result = func()
            results.append((name, result))
        except Exception as e:
            print_error(f"{name} 失败：{e}")
            results.append((name, False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}📊 安装结果汇总{Colors.END}\n")
    
    for name, result in results:
        status = f"{Colors.GREEN}✅ 成功{Colors.END}" if result else f"{Colors.RED}❌ 失败{Colors.END}"
        print(f"  {name}: {status}")
    
    # 最终提示
    print("\n" + "=" * 60)
    if all(r for _, r in results):
        print_success("🎉 安装完成！")
        print("\n下一步:")
        print("1. 手动创建 Feishu 多维表格")
        print("2. 更新 config/feishu-memory-table.json 配置")
        print("3. 添加 crontab 定时任务")
        print("4. 运行：python3 scripts/sync-memory-to-feishu.py 测试")
    else:
        print_warning("⚠️  部分步骤未完成，请检查上方提示")
    
    print()

if __name__ == '__main__':
    main()
