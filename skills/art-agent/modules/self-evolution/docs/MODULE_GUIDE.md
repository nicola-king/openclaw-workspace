# self-evolution 模块指南

## 简介
Art Agent v1.0 的自进化模块，集成太一宪法原则，驱动美学引擎持续优化。

## 快速开始

```bash
# 独立运行
python3 core.py

# 执行宪法学习循环
python3 core.py --task constitution_learning --module-name aesthetic-filter

# 获取进化指标
python3 core.py --task get_metrics
```

## 配置

编辑 `config.json` 设置模块参数。

## 测试

```bash
pytest tests/test_core.py
```

## 依赖
- Python 3.8+
- aesthetic-filter

## 状态
✅ v1.0.0 - 已蒸馏太一系统
