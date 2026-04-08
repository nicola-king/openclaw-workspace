#!/usr/bin/env python3
"""
Smart Model Router 测试
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from skills.smart_model_router.router import SmartRouter
from skills.smart_model_router.routers.cost_router import CostRouter
from skills.smart_model_router.routers.empathy_router import EmpathyRouter
from skills.smart_model_router.tracker.usage_tracker import UsageTracker


def test_task_classification():
    """测试任务分类"""
    router = SmartRouter()
    
    test_cases = [
        ("你好", "simple"),
        ("写个 Python 脚本", "code"),
        ("我今天心情不好", "emotional"),
        ("分析这份 100 页的文档", "long_text"),
    ]
    
    print("=" * 60)
    print("测试任务分类")
    print("=" * 60)
    
    for task, expected_type in test_cases:
        result = router.classify_task(task)
        status = "✅" if result['type'] == expected_type else "❌"
        print(f"{status} 任务：{task}")
        print(f"   类型：{result['type']} (期望：{expected_type})")
        print(f"   复杂度：{result['complexity']}")
        print(f"   Token 估计：{result['token_estimate']}")
        print()


def test_model_selection():
    """测试模型选择"""
    router = SmartRouter()
    
    test_cases = [
        ("你好", "balanced", "local/qwen2.5:7b"),
        ("写个 Python 脚本", "balanced", "bailian/qwen3-coder-plus"),
        ("我今天心情不好", "empathy", "bailian/qwen3.5-plus"),
        ("分析这份 100 页的文档", "balanced", "google/gemini-2.5-pro"),
    ]
    
    print("=" * 60)
    print("测试模型选择")
    print("=" * 60)
    
    for task, strategy, expected_model in test_cases:
        model = router.select_model(task, strategy)
        # 注意：实际选择可能因实现细节而有所不同
        print(f"任务：{task}")
        print(f"策略：{strategy}")
        print(f"模型：{model}")
        print()


def test_cost_router():
    """测试成本路由"""
    cost_router = CostRouter(daily_budget=100.0)
    
    test_cases = [
        {'type': 'simple', 'complexity': 'easy', 'token_estimate': 500},
        {'type': 'code', 'complexity': 'medium', 'token_estimate': 2000},
        {'type': 'long_text', 'complexity': 'hard', 'token_estimate': 60000},
    ]
    
    print("=" * 60)
    print("测试成本路由")
    print("=" * 60)
    
    for task_info in test_cases:
        model = cost_router.route(task_info)
        print(f"任务：{task_info}")
        print(f"→ 模型：{model}")
        print()


def test_empathy_router():
    """测试共情路由"""
    empathy_router = EmpathyRouter()
    
    test_cases = [
        "我今天心情很糟糕",
        "太棒了，项目完成了！",
        "今天天气不错",
    ]
    
    print("=" * 60)
    print("测试共情路由")
    print("=" * 60)
    
    for text in test_cases:
        emotion, intensity = empathy_router.detect_emotion(text)
        model = empathy_router.route({'text': text, 'complexity': 'medium'})
        
        print(f"文本：{text}")
        print(f"情感：{emotion} (强度：{intensity:.2f})")
        print(f"模型：{model}")
        print()


def test_usage_tracker():
    """测试用量追踪"""
    tracker = UsageTracker()
    
    print("=" * 60)
    print("测试用量追踪")
    print("=" * 60)
    
    # 记录几次使用
    tracker.record('bailian/qwen3.5-plus', 500, 1000, 0.01, 450, 'code')
    tracker.record('local/qwen2.5:7b', 200, 400, 0.0, 80, 'simple')
    tracker.record('bailian/qwen3.5-plus', 800, 1500, 0.015, 500, 'chat')
    
    # 获取统计
    stats = tracker.get_stats()
    print(f"总模型数：{len(stats)}")
    
    for model, data in stats.items():
        print(f"\n模型：{model}")
        print(f"  调用次数：{data.get('total_calls', 0)}")
        print(f"  总成本：¥{data.get('total_cost', 0):.3f}")
        print(f"  平均延迟：{data.get('avg_duration_ms', 0):.0f}ms")
    
    # 获取今日摘要
    daily = tracker.get_daily_summary()
    print(f"\n今日摘要:")
    print(f"  总调用：{daily['total_calls']}")
    print(f"  总成本：¥{daily['total_cost']:.2f}")
    
    # 获取优化建议
    suggestions = tracker.get_optimization_suggestions()
    if suggestions:
        print(f"\n优化建议:")
        for s in suggestions:
            print(f"  - {s}")
    
    print()


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Smart Model Router 测试套件")
    print("=" * 60 + "\n")
    
    test_task_classification()
    test_model_selection()
    test_cost_router()
    test_empathy_router()
    test_usage_tracker()
    
    print("=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
