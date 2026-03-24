# 📝 太一 Git 提交规范

**参考：** Victor Wu 原子化提交原则
**目标：** 最小单位 Commit，利于回滚

---

## 🎯 提交原则

### 1. 原子化提交 ✅

**每个 Commit 只做一件事：**
```bash
# ✅ 好的提交
git commit -m "feat: 添加知几-E 风控参数"
git commit -m "fix: 修复策略计算错误"
git commit -m "docs: 更新配置文档"

# ❌ 坏的提交
git commit -m "更新了很多东西"
```

---

### 2. 提交类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **feat** | 新功能 | feat: 添加日损熔断 |
| **fix** | Bug 修复 | fix: 修复滑点计算 |
| **docs** | 文档更新 | docs: 更新 README |
| **style** | 代码格式 | style: 格式化代码 |
| **refactor** | 重构 | refactor: 重构策略引擎 |
| **test** | 测试 | test: 添加单元测试 |
| **chore** | 构建/工具 | chore: 更新依赖 |

---

### 3. 提交模板

```bash
<type>: <subject>

<body>

<footer>
```

**示例：**
```bash
feat: 添加日损熔断机制

- 实现每日 10% 亏损熔断
- 添加熔断日志记录
- 添加用户通知功能

Closes #123
```

---

## 📋 提交流程

### 1. 创建工作分支

```bash
git checkout -b feature/zhiji-risk-control
```

### 2. 小步提交

```bash
# 添加风控参数
git add skills/zhiji/strategy_v21.py
git commit -m "feat: 添加风控参数配置"

# 添加熔断逻辑
git add skills/zhiji/strategy_v21.py
git commit -m "feat: 实现日损熔断逻辑"

# 添加测试
git add tests/test_risk_control.py
git commit -m "test: 添加风控测试"
```

### 3. 合并到主分支

```bash
git checkout main
git merge feature/zhiji-risk-control
```

---

## ⚠️ 避免的陷阱

| 陷阱 | 问题 | 正确做法 |
|------|------|----------|
| **大提交** | 难以审查/回滚 | 小步原子提交 |
| **混合类型** | 难以理解意图 | 一个提交一个类型 |
| **模糊信息** | 难以追溯 | 清晰的提交信息 |
| **多分支开发** | 并发冲突 | 单分支 + 功能分支 |

---

## ✅ 最佳实践

**1. 频繁提交**
```bash
# 每完成一个小功能就提交
git commit -am "feat: xxx"
```

**2. 提交前自检**
```bash
# 这个提交是否原子？
# 是否能清晰描述意图？
# 是否易于回滚？
```

**3. 使用功能分支**
```bash
# 功能开发在独立分支
git checkout -b feature/xxx
```

---

*创建时间：2026-03-24 08:20*
*下次更新：根据实践优化*
