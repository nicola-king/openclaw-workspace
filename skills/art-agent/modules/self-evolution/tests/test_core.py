#!/usr/bin/env python3
"""
self-evolution 模块测试
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_config_loads():
    """测试配置文件加载"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config.json"
    )
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    assert "module_name" in config
    assert "version" in config
    assert "enabled" in config
    assert config["module_name"] == "self-evolution"


def test_constitution_learning():
    """测试宪法学习循环"""
    from constitution_learning import ConstitutionLearning
    cl = ConstitutionLearning()
    result = cl.run_learning_cycle("aesthetic-filter")
    assert "cycle_id" in result
    assert "elon_analysis" in result
    assert "metrics_updated" in result


def test_self_evolution_execute():
    """测试自进化执行"""
    from core import SelfEvolution
    agent = SelfEvolution()
    result = agent.execute(task="constitution_learning", module_name="all")
    assert "cycle_id" in result
    assert "elon_analysis" in result


def test_health_check():
    """测试健康检查"""
    from core import SelfEvolution
    agent = SelfEvolution()
    result = agent.health_check()
    assert result["status"] == "healthy"
    assert "evolution_metrics" in result


if __name__ == "__main__":
    test_config_loads()
    test_constitution_learning()
    test_self_evolution_execute()
    test_health_check()
    print("✅ self-evolution 测试通过")
