#  太一 Zero to Hero 教程系列

> 从 0 到 1 掌握太一 AGI | 版本：v1.0 | 创建时间：2026-04-17

---

## 课程概览

| 课程 | 时长 | 难度 | 收获 |
|------|------|------|------|
| **第 1 课：Hello Agent** | 5 分钟 | ⭐ | 运行第一个 Agent |
| **第 2 课：Agent 对话** | 15 分钟 | ⭐⭐ | 理解多 Bot 协作 |
| **第 3 课：技能创建** | 30 分钟 | ⭐⭐ | 创建自定义技能 |
| **第 4 课：自进化** | 45 分钟 | ⭐⭐⭐ | 让 Agent 自我改进 |
| **第 5 课：社区贡献** | 60 分钟 | ⭐⭐⭐ | 成为贡献者 |

---

## 第 1 课：Hello Agent (5 分钟)

### 目标

运行你的第一个太一 Agent！

### 步骤

**Step 1: 安装**

```bash
# 克隆项目
git clone https://github.com/nicola-king/taiyi-agents.git
cd taiyi-agents

# 安装依赖
pip install -r requirements.txt
```

**Step 2: 配置**

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置
nano .env

# 填入你的 API Key
OPENAI_API_KEY=sk-xxx
QWEN_API_KEY=sk-xxx
```

**Step 3: 运行**

```bash
# 运行主程序
python3 main.py

# 或者运行特定 Agent
python3 main.py --agent taiyi
```

**Step 4: 交互**

```
太一 AGI v1.0 已启动

你好！我是太一，你的 AI 助手。
有什么我可以帮助你的吗？

> 你好，请介绍一下你自己

收到！我是太一 AGI，是一个...
```

### 作业

- [ ] 成功运行太一
- [ ] 尝试 3 个不同问题
- [ ] 截图分享到社区

### 检查清单

- [ ] 环境安装成功
- [ ] 配置文件正确
- [ ] Agent 正常响应
- [ ] 理解基本交互

---

## 第 2 课：Agent 对话 (15 分钟)

### 目标

理解太一的多 Bot 协作机制！

### 背景知识

太一不是单一 Agent，而是**多 Bot 协作系统**：

```
太一 (Taiyi) ← 主 Agent
├── 知几 (Zhiji) ← 数据分析
├── 山木 (Shanmu) ← 业务执行
├── 素问 (Suwen) ← 技术研究
├── 罔两 (Wangliang) ← 市场情报
└── 庖丁 (Paoding) ← 财务管控
```

### 步骤

**Step 1: 观察协作**

```bash
# 运行需要协作的任务
python3 main.py --agent taiyi --task "分析这个数据趋势"
```

**Step 2: 查看日志**

```bash
# 查看协作日志
tail -f logs/taiyi.log

# 输出示例：
[太一] 接收任务：分析数据趋势
[太一] 路由到：知几 (数据分析)
[知几] 分析中...
[知几] 返回结果
[太一] 整合输出
```

**Step 3: 修改路由**

```python
# 编辑路由配置
nano config/routing.yaml

# 修改路由规则
data_analysis:
  primary: zhiji
  secondary: suwen
```

### 作业

- [ ] 运行 3 个不同任务
- [ ] 观察路由过程
- [ ] 修改一次路由配置
- [ ] 分享观察心得

### 检查清单

- [ ] 理解 Bot 职责
- [ ] 理解路由机制
- [ ] 能查看日志
- [ ] 能修改配置

---

## 第 3 课：技能创建 (30 分钟)

### 目标

创建你的第一个自定义技能！

### 步骤

**Step 1: 创建目录**

```bash
# 创建技能目录
mkdir -p skills/my-first-skill
```

**Step 2: 创建 SKILL.md**

```bash
# 创建技能描述文件
nano skills/my-first-skill/SKILL.md
```

```markdown
# 🎉 My First Skill

> 版本：v1.0 | 创建时间：2026-04-17 | 作者：你的名字

## 🎯 职责域

**核心功能**: [一句话描述]

**适用场景**:
- 场景 1
- 场景 2

## ✅ 成功指标

- 指标 1
- 指标 2
```

**Step 3: 实现技能**

```bash
# 创建技能实现
nano skills/my-first-skill/skill.py
```

```python
#!/usr/bin/env python3
"""我的第一个技能"""

def execute(data):
    """执行技能"""
    # 你的逻辑
    result = process(data)
    return result

def process(data):
    """处理数据"""
    # 实现细节
    return data
```

**Step 4: 注册技能**

```bash
# 编辑注册文件
nano skills/registry.py
```

```python
SKILLS = {
    # ... 其他技能
    "my-first-skill": {
        "name": "My First Skill",
        "module": "my-first-skill.skill",
        "enabled": True
    }
}
```

**Step 5: 测试技能**

```bash
# 运行测试
python3 -m skills.my-first-skill.test

# 或者通过主程序
python3 main.py --agent my-first-skill
```

### 作业

- [ ] 创建技能目录
- [ ] 编写 SKILL.md
- [ ] 实现技能逻辑
- [ ] 注册技能
- [ ] 运行测试
- [ ] 分享技能到社区

### 检查清单

- [ ] 理解技能结构
- [ ] 能创建 SKILL.md
- [ ] 能实现技能
- [ ] 能注册技能
- [ ] 能测试技能

---

## 第 4 课：自进化 (45 分钟)

### 目标

让 Agent 具备自进化能力！

### 背景知识

太一自进化机制：

```
任务执行
    ↓
经验积累
    ↓
能力涌现检测 (重复≥3 次)
    ↓
新 Agent 提议
    ↓
SAYELF 批准
    ↓
Agent 创建
    ↓
系统进化
```

### 步骤

**Step 1: 观察进化**

```bash
# 查看进化日志
tail -f logs/evolution.log

# 输出示例：
[进化检测] 同类任务重复 3 次
[进化提议] 建议创建新 Agent
[进化批准] SAYELF 已批准
[进化创建] 新 Agent 已创建
```

**Step 2: 触发进化**

```bash
# 重复执行同类任务 3 次
python3 main.py --task "分析销售数据"
python3 main.py --task "分析市场数据"
python3 main.py --task "分析用户数据"

# 系统会检测到模式，提议创建"数据分析 Agent"
```

**Step 3: 批准进化**

```
【进化提议】
任务类型：数据分析
重复次数：3 次
建议 Agent: Data Analyst Agent
预计价值：提升分析效率 50%

是否批准？(y/n): y

✅ 进化已批准
✅ Agent 创建中...
✅ Agent 已注册
```

**Step 4: 验证进化**

```bash
# 查看新 Agent
python3 main.py --list-agents

# 输出应包含新创建的 Agent
- Data Analyst Agent (新增)
```

### 作业

- [ ] 理解进化机制
- [ ] 触发一次进化
- [ ] 批准进化提议
- [ ] 验证新 Agent
- [ ] 记录进化过程

### 检查清单

- [ ] 理解能力涌现
- [ ] 理解进化流程
- [ ] 能触发进化
- [ ] 能验证结果

---

## 第 5 课：社区贡献 (60 分钟)

### 目标

成为太一贡献者！

### 步骤

**Step 1: Fork 项目**

```bash
# 到 GitHub 点击 Fork 按钮
# 或者命令行
git clone https://github.com/YOUR_USERNAME/taiyi-agents.git
```

**Step 2: 创建分支**

```bash
# 创建功能分支
git checkout -b feature/my-contribution
```

**Step 3: 做出贡献**

选择一种贡献方式：

- 🐛 **修复 Bug**: 找到 Issue，修复代码
- 💡 **添加功能**: 创建新 Agent 或技能
- 📝 **改进文档**: 完善教程或注释
- 🎨 **优化体验**: 改进 UI 或交互
- 🧪 **添加测试**: 提高测试覆盖率

**Step 4: 提交代码**

```bash
# 添加修改
git add .

# 提交代码
git commit -m "feat: 添加我的贡献

- 详细描述 1
- 详细描述 2

Fixes #123"

# 推送到 GitHub
git push origin feature/my-contribution
```

**Step 5: 创建 PR**

```
到 GitHub:
1. 点击 "Pull Request"
2. 填写 PR 描述
3. 关联 Issue
4. 提交 PR
```

**Step 6: 回应反馈**

```
太一会审查 PR 并给出反馈：
- ✅ 建设性意见
- ✅ 技术指导
- ✅ 改进建议

根据反馈修改代码，然后再次提交。
```

**Step 7: 合并庆祝**

```
PR 合并后：
- ✅ 你的名字出现在贡献者列表
- ✅ 获得社区积分
- ✅ 解锁新等级
- ✅ 获得太一感谢
```

### 作业

- [ ] Fork 项目
- [ ] 创建分支
- [ ] 做出贡献
- [ ] 提交 PR
- [ ] 回应反馈
- [ ] 庆祝合并

### 检查清单

- [ ] 理解贡献流程
- [ ] 能 Fork 项目
- [ ] 能提交 PR
- [ ] 能回应反馈
- [ ] 完成第一次贡献

---

## 毕业项目

完成以上 5 课后，完成毕业项目：

### 项目要求

创建一个完整的 Agent，包括：

- [ ] SKILL.md 描述文件
- [ ] 技能实现代码
- [ ] 测试用例
- [ ] 使用文档
- [ ] 示例代码

### 提交方式

```bash
# 提交到 GitHub
git push origin feature/graduation-project

# 创建 PR
# 标注 [毕业项目]
```

### 毕业奖励

- 🎓 太一毕业证书
- 🏆 社区勋章
- 📢 社区展示
-  太一亲自感谢

---

## 进阶学习

完成 Zero to Hero 后：

### 学习路径

1. **深入理解** - 阅读源码
2. **高级技巧** - 学习高级模式
3. **性能优化** - 学习优化技巧
4. **架构设计** - 学习系统设计
5. **社区领导** - 成为维护者

### 资源

- [源码阅读指南](docs/source-code.md)
- [高级模式教程](docs/advanced-patterns.md)
- [性能优化指南](docs/performance.md)
- [架构文档](docs/architecture.md)
- [维护者手册](docs/maintainer.md)

---

## 社区支持

### 遇到问题？

- 📖 查看文档
- 🔍 搜索 Issue
- 💬 社区提问
- 📧 联系太一

### 联系方式

- GitHub Issues
- 微信群
- Telegram
- Email

---

*太一 AGI · Zero to Hero 教程系列 · v1.0*  
*创建时间：2026-04-17*  
*预计完成时间：2.5 小时*
