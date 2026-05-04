# 贡献指南

欢迎！太一跨境贸易 Agent 是一个社区驱动的开源项目。

## 🌱 如何开始

1. **Fork** 本仓库
2. 阅读文档理解架构
3. 找一个 `good first issue`
4. 开始编码

## 📋 贡献类型

### 🐛 Bug 报告
- 在 Issues 中创建新 issue
- 描述：环境/步骤/期望/实际
- 附上日志和截图

### 💡 功能建议
- 描述清楚使用场景
- 说明解决了什么问题
- 最好附带实现思路

### 🔧 代码贡献
- 遵循现有代码风格
- 每个 PR 一个功能
- 添加测试
- 更新文档

## 🧪 测试

```bash
# 测试单一模块
python3 modules/intelligence-hub/tests/test_core.py

# 测试完整流程
python3 -c "from modules.cross-border-core.core import CrossBorderAgent; a = CrossBorderAgent(); print(a.health_check())"
```

## 📝 Commit 规范

```
[类型] 简短描述

类型:
- [修复] Bug fix
- [增强] New feature
- [文档] Documentation
- [重构] Code refactoring
- [测试] Tests
- [性能] Performance
```

---

**感恩每一份贡献。这个系统因你而进化。**
