# Agent Skills - 生产级工程工作流

> 状态：🟡 调研完成，待集成  
> 学习日期：2026-04-08  
> 来源：SAYELF 分享

---

## 📦 工具信息

| 项目 | 详情 |
|------|------|
| **名称** | Agent Skills |
| **开源** | [GitHub - addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| **开发者** | Addy Osmani（Google Chrome 工程师） |
| **Stars** | 10K+ |
| **技能数** | 19 个生产级技能 |
| **斜杠命令** | 7 个 |

---

## 🎯 核心能力

**Agent Skills** 为 AI 编码 Agent 提供生产级工程工作流：

- ✅ **7 个斜杠命令** - 对应开发全生命周期
- ✅ **19 个生产技能** - 覆盖完整开发流程
- ✅ **3 个 Agent 角色** - code-reviewer / test-engineer / security-auditor
- ✅ **4 个检查清单** - testing / security / performance / accessibility
- ✅ **质量门禁** - 强制执行工程最佳实践

---

## 🔄 开发工作流

```
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
  ↓       ↓       ↓       ↓       ↓      ↓
/spec   /plan   /build  /test   /review /ship
```

---

## 📋 7 个斜杠命令

| 命令 | 用途 | 关键原则 | 触发时机 |
|------|------|---------|---------|
| **`/spec`** | 明确要构建什么 | 规范先于代码 | 项目启动 |
| **`/plan`** | 计划如何建造 | 小的、原子性任务 | 设计阶段 |
| **`/build`** | 逐步构建 | 一次切一片 | 编码阶段 |
| **`/test`** | 证明它有效 | 测试就是证明 | 测试阶段 |
| **`/review`** | 合并前审核 | 改善代码健康 | PR 阶段 |
| **`/code-simplify`** | 简化代码 | 清晰胜于巧妙 | 重构阶段 |
| **`/ship`** | 交付生产 | 速度越快越安全 | 部署阶段 |

---

## 🤖 3 个 Agent 角色

| 角色 | 职责 | 技能 |
|------|------|------|
| **code-reviewer** | 员工级工程师审查 | 代码质量/架构/模式 |
| **test-engineer** | QA 工程师 | 测试覆盖/边界条件 |
| **security-auditor** | 安全审计 | 漏洞扫描/最佳实践 |

---

## 📝 4 个参考检查清单

| 清单 | 内容 |
|------|------|
| **Testing** | 单元测试/集成测试/E2E 测试 |
| **Security** | 输入验证/认证授权/加密 |
| **Performance** | 时间复杂度/空间复杂度/缓存 |
| **Accessibility** | ARIA/键盘导航/对比度 |

---

## 🔧 使用方法

```bash
# 安装（以 Claude Code 为例）
claude install addyosmani/agent-skills

# 项目启动
/spec "构建一个用户认证系统"

# 计划阶段
/plan "拆分为登录/注册/密码重置三个模块"

# 编码阶段
/build "实现登录功能"

# 测试阶段
/test "运行单元测试，覆盖率>80%"

# 代码审查
/review "检查代码质量和安全问题"

# 简化代码
/code-simplify "重构这个函数，提高可读性"

# 交付生产
/ship "部署到生产环境"
```

---

## 💡 太一集成场景

### 场景 1：Skill 开发标准化

```
新 Skill 开发 → /spec → /plan → /build → /test → /review → /ship
```

**价值**：
- ✅ 确保代码质量
- ✅ 强制执行测试
- ✅ 安全审查自动化

### 场景 2：素问代码生成

```
用户请求 → 素问 → Agent Skills 工作流 → 生产级代码
```

### 场景 3：知几策略开发

```
交易策略 → /spec → /test(回测) → /review(风险评估) → /ship(实盘)
```

### 场景 4：代码审查自动化

```
Git PR → Agent Skills(code-reviewer) → 自动审查 → 改进建议
```

---

## 📋 集成 Checklist

### P0 - 立即执行（今日）
- [x] ✅ 调研完成
- [ ] ⏳ 安装 Agent Skills
- [ ] ⏳ 测试 7 个命令
- [ ] ⏳ 编写集成文档

### P1 - 本周执行
- [ ] ⏳ 与素问集成
- [ ] ⏳ 与知几集成
- [ ] ⏳ 配置自动审查

### P2 - 按需执行
- [ ] ⏳ 自定义技能扩展
- [ ] ⏳ 团队工作流标准化
- [ ] ⏳ 质量门禁优化

---

## ⚠️ 注意事项

### 适用场景
- ✅ 生产级代码开发
- ✅ 团队协作项目
- ✅ 需要质量保证的场景

### 不适用场景
- 🔴 快速原型/实验性代码
- 🔴 一次性脚本
- 🔴 学习/测试用途

### 最佳实践
- ✅ `/spec` 先于编码
- ✅ `/test` 覆盖率>80%
- ✅ `/review` 必须通过
- ✅ `/ship` 前确保所有检查通过

---

## 🔗 相关链接

- GitHub: https://github.com/addyosmani/agent-skills
- Dev.to 教程：https://dev.to/_46ea277e677b888e0cd13/agent-skills-19-production-grade-skills-that-make-ai-coding-agents-work-like-senior-engineers-5bi9

---

*创建时间：2026-04-08 22:30*  
*创建人：太一 AGI*  
*状态：🟡 调研完成，待集成*
