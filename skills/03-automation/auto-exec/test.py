#!/usr/bin/env python3
"""
Auto-Exec Skill 测试脚本
验证所有功能正常
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".openclaw" / "workspace" / "skills"))

from pathlib import Path

# 导入模块
import importlib.util
spec = importlib.util.spec_from_file_location("auto_exec.core", Path(__file__).parent / "core.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

spec2 = importlib.util.spec_from_file_location("auto_exec.reporter", Path(__file__).parent / "reporter.py")
reporter_mod = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(reporter_mod)

AutoExecStatus = core.AutoExecStatus
TaskDiscovery = core.TaskDiscovery
ProgressReporter = reporter_mod.ProgressReporter

def test_status_engine():
    """测试状态引擎"""
    print("📊 测试状态引擎...")
    engine = AutoExecStatus()
    
    # 获取状态
    status = engine.get_status()
    assert "status" in status
    print(f"  ✅ 状态读取正常：{status['status']}")
    
    # 更新状态
    engine.update_status(progress=50, nextStep="测试中")
    status = engine.get_status()
    assert status["progress"] == 50
    print(f"  ✅ 状态更新正常：{status['progress']}%")
    
    # 设置任务
    engine.set_task("TEST-001", "测试任务", progress=10)
    status = engine.get_status()
    assert status["currentTask"] == "TEST-001"
    print(f"  ✅ 任务设置正常：{status['currentTask']}")
    
    # 完成步骤
    engine.complete_step("环境准备")
    status = engine.get_status()
    assert any("环境准备" in s for s in status["completedSteps"])
    print(f"  ✅ 步骤完成标记正常")
    
    return True

def test_discovery():
    """测试任务发现"""
    print("\n🔍 测试任务发现...")
    discovery = TaskDiscovery()
    
    tasks = discovery.discover()
    print(f"  ✅ 发现 {len(tasks)} 个任务")
    
    if tasks:
        print(f"  示例：{tasks[0]['id']}: {tasks[0]['name']} [{tasks[0]['priority']}]")
    
    return True

def test_reporter():
    """测试汇报生成"""
    print("\n📝 测试汇报生成...")
    reporter = ProgressReporter()
    
    report = reporter.generate_report()
    assert "自动执行进度汇报" in report
    print(f"  ✅ 汇报生成正常 ({len(report)} 字符)")
    print("\n" + report)
    
    return True

def main():
    """运行所有测试"""
    print("=" * 50)
    print("Auto-Exec Skill 功能测试")
    print("=" * 50)
    
    tests = [
        test_status_engine,
        test_discovery,
        test_reporter
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ 失败：{e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
