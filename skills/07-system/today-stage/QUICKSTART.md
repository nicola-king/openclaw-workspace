# 今日情景 Agent · 快速启动指南

> 创建时间：2026-03-29 20:54
> 版本：1.0.0
> 目标：5 分钟内完成首次测试

---

## 🚀 5 分钟快速启动

### Step 1: 环境准备 (1 分钟)

```bash
# 确认工作目录
cd /home/nicola/.openclaw/workspace/skills/today-stage

# 检查文件结构
ls -la skills/
# 应显示 64 个状态目录
```

### Step 2: 测试单个 Skill (1 分钟)

```bash
# 测试起势期 - 初始阶段
cd skills/state-001-qishi
python3 stage-01.py
```

**预期输出**:
```
状态：起势期
阶段：初始阶段
洞察：潜力大于结果
```

### Step 3: 测试 Agent 主程序 (2 分钟)

```bash
# 返回主目录
cd /home/nicola/.openclaw/workspace/skills/today-stage

# 运行 Agent 测试
python3 agent/today-stage-agent.py
```

**预期输出**:
```
用户输入：我最近真的很努力，但就是没结果
状态：起势期
阶段：强化阶段
洞察：潜力大于结果
爆点句：我最近真的很努力，但就是没结果
```

### Step 4: 测试全部 384 Skills (1 分钟)

```bash
# 运行批量测试脚本
python3 scripts/test-all-skills.py
```

**预期输出**:
```
测试进度：384/384 ✅
通过率：100%
```

---

## 📁 核心文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| **384 Skills** | `skills/state-*/stage-*.py` | 情景状态解读 |
| **Agent 主程序** | `agent/today-stage-agent.py` | 总管调度 |
| **数据文件** | `data/stages-64-final.json` | 64 状态数据 |
| **测试脚本** | `scripts/test-all-skills.py` | 批量测试 |

---

## 🧪 常用测试命令

### 测试单个状态

```bash
# 测试状态 001 起势期
python3 skills/state-001-qishi/stage-01.py
python3 skills/state-001-qishi/stage-02.py
# ... 阶段 03-06
```

### 测试特定状态 + 阶段

```python
# Python 交互式测试
from skills.state-001-qishi.stage-03 import State001Stage03Skill
skill = State001Stage03Skill()
result = skill.get_interpretation()
print(result)
```

### 批量测试

```bash
# 测试所有 384 Skills
python3 scripts/test-all-skills.py

# 测试前 10 个状态
python3 scripts/test-first-10-states.py
```

---

## 🔧 常见问题排查

### 问题 1: 找不到 Skill 文件

```bash
# 检查目录结构
ls skills/state-001-qishi/

# 应包含:
# stage-01.py ~ stage-06.py
```

### 问题 2: 导入错误

```bash
# 确认在正确目录
cd /home/nicola/.openclaw/workspace/skills/today-stage

# 添加 Python 路径
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### 问题 3: 输出为空

```bash
# 检查 Skill 文件内容
cat skills/state-001-qishi/stage-01.py | head -20

# 应包含 class State001Stage01Skill 定义
```

---

## 📊 384 Skills 快速索引

### State 001-010 (前 10 个状态)

| 状态 | 目录 | 阶段文件 |
|------|------|---------|
| 001 起势期 | `state-001-qishi/` | stage-01~06.py |
| 002 承载期 | `state-002-chengzai/` | stage-01~06.py |
| 003 启动混乱期 | `state-003-hunduan/` | stage-01~06.py |
| 004 认知盲区期 | `state-004-mangqu/` | stage-01~06.py |
| 005 等待窗口期 | `state-005-dengdai/` | stage-01~06.py |
| 006 冲突边缘期 | `state-006-chongtu/` | stage-01~06.py |
| 007 结构协同期 | `state-007-xietong/` | stage-01~06.py |
| 008 资源整合期 | `state-008-zhenghe/` | stage-01~06.py |
| 009 小幅增长期 | `state-009-zengzhang/` | stage-01~06.py |
| 010 规则适应期 | `state-010-guze/` | stage-01~06.py |

### 快速查找状态

```bash
# 按状态名查找
ls skills/ | grep "qishi"  # 起势期

# 按状态编号查找
ls skills/ | grep "state-001"  # 状态 001
```

---

## 🎯 下一步行动

### 立即测试 (5 分钟)

- [ ] 完成 Step 1-4 快速启动
- [ ] 确认 384 Skills 全部可用
- [ ] 记录测试结果

### 今日完成 (1 小时)

- [ ] 测试所有 64 个状态
- [ ] 验证心理学框架输出
- [ ] 验证爆点句输出

### 本周完成

- [ ] 集成到小程序
- [ ] 搭建后端 API
- [ ] 准备上线审核

---

## 📞 获取帮助

| 问题类型 | 解决方案 |
|---------|---------|
| Skill 加载失败 | 检查文件路径和类名 |
| 输出格式错误 | 检查 get_interpretation() 方法 |
| 性能问题 | 使用缓存机制 |
| 审核问题 | 参考合规设计文档 |

---

## 📚 相关文档

| 文档 | 用途 |
|------|------|
| `ARCHITECTURE-V9.md` | 完整架构说明 |
| `DEVELOPMENT-CHECKLIST.md` | 开发清单 |
| `LEARNING-INTEGRATION-V11.md` | 学习整合 |
| `384-SKILLS-ARCHITECTURE.md` | Skills 架构 |

---

*创建时间：2026-03-29 20:54*
*今日情景 Agent · 快速启动指南 v1.0*
