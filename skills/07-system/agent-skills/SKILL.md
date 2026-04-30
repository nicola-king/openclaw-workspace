# Agent Skills - 生产级工程工作流

> 状态：🟡 框架创建中  
> 优先级：P1  
> 创建日期：2026-04-08

---

## 触发条件

使用此技能当：
- 开发生产级代码
- 需要质量保证
- 团队协作项目
- Skill 开发标准化
- 代码审查自动化

---

## 能力

- ✅ 7 个斜杠命令（/spec /plan /build /test /review /code-simplify /ship）
- ✅ 19 个生产技能
- ✅ 3 个 Agent 角色（code-reviewer / test-engineer / security-auditor）
- ✅ 4 个检查清单（testing / security / performance / accessibility）
- ✅ 质量门禁强制执行

---

## 配置

```bash
AGENT_SKILLS_PATH=addyosmani/agent-skills
AGENT_SKILLS_AUTO_REVIEW=true
AGENT_SKILLS_TEST_COVERAGE=80
AGENT_SKILLS_SECURITY_CHECK=true
```

---

## 使用方法

```bash
# 安装
claude install addyosmani/agent-skills

# 项目启动
/spec "构建用户认证系统"

# 计划
/plan "拆分为三个模块"

# 编码
/build "实现登录功能"

# 测试
/test "覆盖率>80%"

# 审查
/review "检查代码质量"

# 简化
/code-simplify "重构提高可读性"

# 交付
/ship "部署到生产"
```

---

## 状态

- [x] ✅ 调研完成
- [ ] ⏳ 安装测试
- [ ] ⏳ 7 个命令验证
- [ ] ⏳ 与素问/知几集成

---

*最后更新：2026-04-08 22:30*
