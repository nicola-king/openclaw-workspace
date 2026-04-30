# 🔧 Hack 太一指南

> 版本：v1.0 | 创建时间：2026-04-17 | 灵感：Karpathy 哲学

---

## 一、为什么 Hack 太一？

> "你 fork 它，不是在抄作业，而是在和大师一起递归自我改进。"

太一不是黑箱，是**极简、可读、可 hack 的骨架**。

### 你能 Hack 什么？

| 内容 | 难度 | 时间 | 收获 |
|------|------|------|------|
| 修改 Agent 配置 | ⭐ | 5 分钟 | 理解 Agent 机制 |
| 创建自定义 Agent | ⭐⭐ | 30 分钟 | 掌握 Agent 创建 |
| 添加新技能 | ⭐⭐ | 1 小时 | 理解技能系统 |
| 优化协作流程 | ⭐⭐⭐ | 2 小时 | 掌握多 Bot 协作 |
| 创建新模块 | ⭐⭐⭐⭐ | 1 天 | 掌握系统架构 |

---

## 二、快速开始

### 2.1 5 分钟小 Hack

**目标**：修改 Agent 配置

```bash
# 1. Fork 项目
git clone https://github.com/nicola-king/taiyi-agents.git

# 2. 找到配置文件
cd taiyi-agents
nano .env

# 3. 修改配置
OPENAI_API_KEY=your_key
QWEN_API_KEY=your_key

# 4. 测试
python3 main.py
```

**收获**：理解配置机制

### 2.2 30 分钟中 Hack

**目标**：创建自定义 Agent

```bash
# 1. 复制模板
cp skills/template-agent/SKILL.md skills/my-custom-agent/SKILL.md

# 2. 修改内容
# 编辑 SKILL.md，填入你的 Agent 信息

# 3. 注册 Agent
# 添加到 skills/registry.py

# 4. 测试
python3 main.py --agent my-custom-agent
```

**收获**：掌握 Agent 创建流程

### 2.3 1 小时大 Hack

**目标**：添加新技能

```bash
# 1. 创建技能文件
mkdir -p skills/my-skill
nano skills/my-skill/SKILL.md

# 2. 实现技能逻辑
nano skills/my-skill/skill.py

# 3. 添加测试
nano skills/my-skill/test_skill.py

# 4. 运行测试
python3 skills/my-skill/test_skill.py
```

**收获**：掌握技能系统

---

## 三、代码哲学

### 3.1 极简主义

```python
# ❌ 坏代码 - 复杂黑箱
def process(data, config=None, **kwargs):
    # 100 行复杂逻辑
    return result

# ✅ 好代码 - 极简透明
def process_user_inquiry(data):
    """处理用户询问"""
    intent = parse_intent(data)      # 1. 解析意图
    agent = route_to_agent(intent)   # 2. 路由 Agent
    result = agent.execute(data)     # 3. 执行任务
    return format_output(result)     # 4. 格式化输出
```

### 3.2 教育注释

```python
# ❌ 无注释
result = model.generate(prompt)

# ✅ 教育注释
# 使用模型生成回复
# 温度参数控制创造性：
#   0.3 = 保守模式 (事实性回答)
#   0.7 = 平衡模式 (默认)
#   0.9 = 创造模式 (头脑风暴)
result = model.generate(prompt, temperature=0.7)
```

### 3.3 可修改性

```python
# ❌ 硬编码 - 难修改
config = {"model": "gpt-4", "temperature": 0.7}

# ✅ 配置化 - 易修改
# 用户可以在 config.yaml 中轻松修改
config = load_config("config.yaml")
```

---

## 四、Hack 项目清单

### 4.1 新手级 (⭐)

- [ ] 修改 `.env` 配置文件
- [ ] 修改 Agent 提示词
- [ ] 添加自定义问候语
- [ ] 修改输出格式
- [ ] 添加日志级别

### 4.2 进阶级 (⭐⭐)

- [ ] 创建自定义 Agent
- [ ] 添加新技能
- [ ] 修改协作流程
- [ ] 添加新的数据源
- [ ] 创建自定义报告

### 4.3 专家级 (⭐⭐⭐)

- [ ] 优化性能瓶颈
- [ ] 添加新的记忆层
- [ ] 实现新的协作机制
- [ ] 创建管理工具
- [ ] 建立 Benchmark 测试

### 4.4 大师级 (⭐⭐⭐⭐)

- [ ] 重构核心架构
- [ ] 实现分布式部署
- [ ] 创建插件系统
- [ ] 建立生态系统
- [ ] 领导社区项目

---

## 五、常见问题

### Q1: 我没有编程经验，能 Hack 吗？

**能！** 从最简单的配置修改开始：

```bash
# 修改配置文件
nano .env

# 修改提示词
nano agents/taiyi/prompt.md
```

### Q2: 我 Hack 坏了怎么办？

**不会坏！** Git 可以恢复：

```bash
# 查看修改
git status

# 恢复原状
git checkout .

# 或者回滚到之前版本
git reset --hard HEAD
```

### Q3: 如何分享我的 Hack？

**提交 PR！**

```bash
# 提交代码
git add .
git commit -m "添加我的自定义功能"
git push

# 然后到 GitHub 创建 Pull Request
```

### Q4: 太一会审查我的 PR 吗？

**会！** 太一亲自审查每个 PR：

- ✅ 24 小时内响应
- ✅ 建设性反馈
- ✅ 技术指导
- ✅ 合并后感谢

---

## 六、Hack 展示

### 6.1 优秀 Hack 案例

| 贡献者 | Hack 内容 | 影响 |
|--------|---------|------|
| @user1 | 添加了微信推送 | 100+ 用户受益 |
| @user2 | 优化了记忆压缩 | 性能提升 50% |
| @user3 | 创建了教程系列 | 1000+ 阅读 |
| @user4 | 添加了新 Agent | 社区广泛使用 |

### 6.2 你的 Hack 可以是什么？

```
想法 1: 添加新的数据源
想法 2: 优化某个流程
想法 3: 创建管理工具
想法 4: 编写教程文档
想法 5: 设计视觉效果
...
```

---

## 七、成长路径

```
新手 (0-1 个月)
    │
    ├── 修改配置
    ├── 修改提示词
    └── 提交第一个 PR
    │
    ↓
贡献者 (1-3 个月)
    │
    ├── 创建 Agent
    ├── 添加技能
    └── 帮助新手
    │
    ↓
维护者 (3-6 个月)
    │
    ├── 审查 PR
    ├── 回答问题
    └── 规划功能
    │
    ↓
核心成员 (6-12 个月)
    │
    ├── 架构决策
    ├── 社区领导
    └── 生态建设
```

---

## 八、资源

### 8.1 学习资源

- [快速开始指南](docs/quickstart.md)
- [Agent 创建教程](docs/create-agent.md)
- [技能开发指南](docs/develop-skill.md)
- [API 文档](docs/api.md)

### 8.2 社区资源

- [GitHub Issues](https://github.com/nicola-king/taiyi-agents/issues)
- [讨论区](https://github.com/nicola-king/taiyi-agents/discussions)
- [微信群](docs/wechat-group.md)
- [Telegram](https://t.me/taiyi_agents)

### 8.3 联系太一

- 📧 Email: taiyi@openclaw.ai
- 💬 Telegram: @taiyi_bot
- 🐦 Twitter: @taiyi_agents
- 📕 小红书：太一 AGI

---

## 九、宣言

```
在这里，
没有黑箱，只有透明。
没有抄袭，只有学习。
没有消费，只有创造。
没有终点，只有进化。

欢迎来到太一进化树，
你的每一个 Hack，
都是一个新的分支。

开始 Hack 吧！
```

---

*太一 AGI · Hack 指南 · v1.0*  
*创建时间：2026-04-17*  
*灵感：Karpathy 开源哲学*
