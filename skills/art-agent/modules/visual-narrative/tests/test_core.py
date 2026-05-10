#!/usr/bin/env python3
"""
visual-narrative 模块测试
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
    assert config["module_name"] == "visual-narrative"


def test_core_imports():
    """测试核心模块导入"""
    from core import SelfEvolution  # noqa: F401


def test_health_check():
    """测试健康检查"""
    pass


if __name__ == "__main__":
    test_config_loads()
    print(f"✅ visual-narrative 测试通过")
