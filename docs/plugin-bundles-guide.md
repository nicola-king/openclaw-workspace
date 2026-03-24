# 🔌 太一插件包兼容性指南

**创建时间：** 2026-03-24 12:15
**参考：** OpenClaw Plugin Bundles
**目标：** 兼容 Codex/Claude/Cursor 生态

---

## 📊 插件包格式支持

### 1. Codex 插件包

**目录结构：**
```
.my-codex-plugin/
├── .codex-plugin/
│   └── manifest.json
├── skills/
│   └── my-skill/
│       └── SKILL.md
├── commands/
│   └── my-command.md
└── hooks/
    └── handler.ts
```

**太一兼容：**
- ✅ skills/目录已支持
- 🟡 commands/可创建
- 🟡 hooks/可创建

---

### 2. Claude 插件包

**目录结构：**
```
.my-claude-plugin/
├── .claude-plugin/
│   └── manifest.json
├── skills/
│   └── my-skill/
│       └── SKILL.md
└── settings.json
```

**太一兼容：**
- ✅ skills/目录已支持
- ✅ settings.json 已支持（.taiyi/settings.json）
- 🟡 manifest.json 可创建

---

### 3. Cursor 插件包

**目录结构：**
```
.my-cursor-plugin/
├── .cursor-plugin/
│   └── manifest.json
├── .cursor/
│   └── commands/
│       └── my-command.md
└── skills/
    └── my-skill/
        └── SKILL.md
```

**太一兼容：**
- ✅ skills/目录已支持
- 🟡 .cursor/commands/可创建
- 🟡 manifest.json 可创建

---

## 🔧 安装流程

### 从目录安装

```bash
openclaw plugins install ./my-plugin
```

**太一兼容：**
```bash
# 太一技能安装
cd /home/nicola/.openclaw/workspace
cp -r ./my-plugin/skills/* ./skills/
openclaw gateway reload
```

---

### 从存档安装

```bash
openclaw plugins install ./my-plugin.tgz
```

**太一兼容：**
```bash
# 太一技能安装
cd /home/nicola/.openclaw/workspace
tar -xzf ./my-plugin.tgz
cp -r ./my-plugin/skills/* ./skills/
openclaw gateway reload
```

---

### 从市场安装

```bash
openclaw plugins marketplace list
openclaw plugins install <插件名称>
```

**太一兼容：**
```bash
# ClawHub 技能安装
clawhub install <skill-name>
openclaw gateway reload
```

---

## ✅ 验证流程

### 1. 验证检测

```bash
openclaw plugins list
openclaw plugins inspect <id>
```

**太一兼容：**
```bash
# 太一技能列表
ls -la /home/nicola/.openclaw/workspace/skills/

# 太一技能详情
cat /home/nicola/.openclaw/workspace/skills/<skill>/SKILL.md
```

---

### 2. 重启并使用

```bash
openclaw gateway restart
```

**太一兼容：**
```bash
# 太一重载
openclaw gateway reload
```

---

## 📊 检测优先级

```
原生插件优先
    ↓
插件包标记
    ↓
冲突解决（如果两者都包含，优先使用原生路径）
```

**太一实现：**
```python
# 技能加载优先级
1. 原生技能（skills/直接创建）
2. 插件包技能（从外部导入）
3. 冲突时优先原生路径
```

---

## 🚀 太一优化计划

### 立即执行（今日）

**1. 创建插件包目录结构**
```bash
mkdir -p /home/nicola/.openclaw/workspace/plugins/
```

**2. 创建 manifest.json 模板**
```json
{
  "name": "taiyi-plugin",
  "version": "1.0.0",
  "description": "太一插件包",
  "author": "SAYELF",
  "skills": ["zhiji", "shanmu", "suwen", "wangliang", "paoding"],
  "commands": [],
  "hooks": []
}
```

**3. 支持外部技能导入**
```bash
# 从 Codex/Claude/Cursor 导入技能
cp -r ./external-plugin/skills/* ./skills/
openclaw gateway reload
```

---

### 中期建设（本周）

**1. 创建 ClawHub 技能包**
- 打包太一核心技能
- 发布到 ClawHub
- 社区共享

**2. 集成 MCP 工具**
- MCP 配置合并
- 启动支持的服务器
- 扩展技能来源

**3. 优化冲突解决**
- 检测技能冲突
- 优先使用原生路径
- 防止部分安装

---

## 📈 兼容性评估

| 功能 | OpenClaw | 太一现状 | 优化方向 |
|------|----------|----------|----------|
| **技能兼容** | ✅ Codex/Claude/Cursor | ✅ 已支持 | 🟡 增加 manifest |
| **命令兼容** | ✅ commands/ | 🟡 部分支持 | 🟡 创建 commands/ |
| **挂钩兼容** | ✅ hooks/ | 🟡 部分支持 | 🟡 创建 hooks/ |
| **MCP 工具** | ✅ MCP 配置 | ❌ 未支持 | 🟡 可集成 |
| **设置兼容** | ✅ settings.json | ✅ 已支持 | ✅ 已完成 |

**综合兼容性：** 🟡 70%（可优化到 90%）

---

*创建时间：2026-03-24 12:15*
*下次更新：插件包导入后*
