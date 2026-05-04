#!/usr/bin/env python3
"""
supply-chain 模块测试
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_config_loads():
    """测试配置文件加载"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    assert "module_name" in config
    assert "version" in config
    assert "enabled" in config
    assert config["module_name"] == "supply-chain"


def test_core_imports():
    """测试核心模块导入"""
    from core import SelfEvolution  # noqa: F401
    # 每个模块的 core.py 可能有不同的主类
    # 这里只测试导入不报错


def test_health_check():
    """测试健康检查"""
    # 如果模块支持 health_check，测试它
    pass


if __name__ == "__main__":
    test_config_loads()
    print(f"✅ {mod} 测试通过")
