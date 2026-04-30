# 📓 Obsidian 接入太一系统完整指南

**更新时间**: 2026-03-27 17:47  
**状态**: ✅ Obsidian 技能已安装

---

## 🎯 Obsidian 接入方案

### 方案 1: Obsidian 技能直接集成 ✅

**技能位置**: `~/.npm-global/lib/node_modules/openclaw/skills/obsidian/SKILL.md`

**核心功能**:
- ✅ 直接写入 Obsidian Vault
- ✅ Markdown 格式自动处理
- ✅ 支持双链语法 `[[链接]]`
- ✅ 支持标签 `#标签`
- ✅ 支持 YAML Frontmatter

---

### 方案 2: 本地文件夹同步

**配置**:
```bash
# Obsidian Vault 位置
/home/nicola/ObsidianVault/

# 太一 Memory 目录
/home/nicola/.openclaw/workspace/memory/

# 创建软链接
ln -s /home/nicola/.openclaw/workspace/memory/ /home/nicola/ObsidianVault/TaiyiMemory/
```

**效果**: 太一记忆自动同步到 Obsidian

---

### 方案 3: 飞书→Obsidian 工作流

**流程**:
```
太一生成内容
  ↓
飞书文档 (feishu-doc skill)
  ↓
导出 Markdown
  ↓
Obsidian Vault
```

---

## 🔧 立即集成

### Step 1: 配置 Obsidian Vault 路径

**文件**: `~/.openclaw/openclaw.json`

```json
{
  "skills": {
    "obsidian": {
      "enabled": true,
      "vault_path": "/home/nicola/ObsidianVault",
      "default_folder": "TaiyiMemory",
      "auto_sync": true
    }
  }
}
```

---

### Step 2: 测试写入

**命令**:
```bash
# 使用 Obsidian 技能写入笔记
openclaw skill obsidian --write "今日总结" --content "内容..." --path "Daily/2026-03-27.md"
```

**或使用消息命令**:
```
@太一 把这个写入 Obsidian: [内容]
路径：Daily/2026-03-27.md
```

---

### Step 3: 概念打磨集成

**流程**:
```
用户提出概念
  ↓
圆桌讨论 (10 轮)
  ↓
太一汇总
  ↓
写入 Obsidian (自动)
  ↓
每日回顾
```

**输出格式**:
```markdown
---
tags: [概念打磨，银行承兑汇票]
created: 2026-03-27
status: in-progress
day: 1/7
---

# 概念打磨 · 银行承兑汇票

## 核心定义
银行信用背书的短期融资工具...

## 多角度理解
### 金融视角 (知几)
...

### 创意视角 (山木)
...

## 讨论轮次
- Round 1: [[2026-03-27]]
- Round 2: [[2026-03-28]]
```

---

## 📊 太一 Memory → Obsidian 映射

### 现有 Memory 结构

```
memory/
├── 2026-03-27.md          # 每日记忆
├── core.md                # 核心记忆
├── residual.md            # 残差记忆
└── heartbeat-state.json   # 心跳状态
```

### Obsidian 映射结构

```
ObsidianVault/
├── TaiyiMemory/           # 太一记忆
│   ├── Daily/
│   │   └── 2026-03-27.md
│   ├── Core/
│   │   └── CoreMemory.md
│   ├── Projects/
│   │   ├── 知几-E.md
│   │   └── PolyAlert.md
│   └── Concepts/
│       ├── 银行承兑汇票.md
│       └── 智能分流.md
├── Skills/                # 技能文档
└── Templates/             # 模板
```

---

## 🚀 自动化配置

### Cron 自动同步

**配置**:
```bash
# 每天 23:00 自动同步到 Obsidian
0 23 * * * rsync -av /home/nicola/.openclaw/workspace/memory/ /home/nicola/ObsidianVault/TaiyiMemory/Daily/
```

---

### 概念打磨自动写入

**技能配置**:
```python
# skills/taiyi/concept-polishing.py

class ConceptPolishing:
    def __init__(self):
        self.obsidian_path = "/home/nicola/ObsidianVault/Concepts/"
    
    def save_concept(self, concept_name, discussion_summary):
        """保存概念打磨笔记"""
        filename = f"{self.obsidian_path}{concept_name}.md"
        
        content = f"""---
tags: [概念打磨，{concept_name}]
created: {datetime.now().strftime('%Y-%m-%d')}
status: in-progress
---

# 概念打磨 · {concept_name}

{discussion_summary}

---
*打磨进度：Day 1/7*
"""
        
        with open(filename, 'w') as f:
            f.write(content)
```

---

## 📈 最佳实践

### 1. 双链语法

**Obsidian 特色**:
```markdown
# 太一系统

[[智能分流]] 是太一的核心功能。
参考 [[Qwen 2.5 7B]] 和 [[MODEL-ROUTING]]。

相关概念:
- [[知几-E]]
- [[PolyAlert]]
- [[概念打磨]]
```

---

### 2. YAML Frontmatter

**元数据管理**:
```markdown
---
tags: [太一，AI，量化交易]
created: 2026-03-27
updated: 2026-03-27
status: active
priority: high
related:
  - [[知几-E]]
  - [[智能分流]]
---
```

---

### 3. 模板系统

**创建模板**: `Templates/ConceptPolishing.md`

```markdown
---
tags: [概念打磨，{{concept_name}}]
created: {{date}}
status: in-progress
day: {{day}}/7
---

# 概念打磨 · {{concept_name}}

## 核心定义
{{core_definition}}

## 多角度理解
### 金融视角 (知几)
{{financial_perspective}}

### 创意视角 (山木)
{{creative_perspective}}

### 技术视角 (素问)
{{technical_perspective}}

### 数据视角 (罔两)
{{data_perspective}}

### 成本视角 (庖丁)
{{cost_perspective}}

## 讨论轮次
- Round 1: [[{{date}}]]
- Round 2: [[{{tomorrow}}]]

---
*打磨进度：Day {{day}}/7*
```

---

### 4. Graph View 优化

**标签体系**:
```
#太一/核心技能
#太一/Bot 协作
#太一/概念打磨
#太一/每日记忆

#知几-E/策略
#知几-E/风控
#知几-E/回测

#概念/金融
#概念/AI
#概念/Web3
```

---

## 🎯 立即可用功能

### 1. 每日记忆自动同步

**命令**:
```
@太一 同步今日记忆到 Obsidian
```

**输出**:
```
✅ 已同步：2026-03-27.md
路径：ObsidianVault/TaiyiMemory/Daily/2026-03-27.md
```

---

### 2. 概念打磨启动

**命令**:
```
@太一 启动概念打磨：银行承兑汇票
```

**流程**:
1. 启动圆桌讨论 (5 Bot)
2. 10 轮深入讨论
3. 自动写入 Obsidian
4. 设置每日提醒

---

### 3. 技能文档查询

**命令**:
```
@太一 在 Obsidian 中搜索：智能分流
```

**输出**:
```
📄 找到 3 篇相关笔记:
1. [[智能分流系统]] - 2026-03-27
2. [[MODEL-ROUTING]] - 宪法文档
3. [[Qwen 2.5 7B]] - 模型配置

需要打开哪篇？
```

---

## 📊 工作流对比

### 原工作流

```
太一生成 → Memory 文件 → 手动复制到 Obsidian
```

**问题**: 手动操作，易遗漏

---

### 优化后工作流

```
太一生成 → 自动写入 Obsidian → 双链关联 → Graph 展示
```

**优势**:
- ✅ 全自动
- ✅ 双链关联
- ✅ 知识图谱
- ✅ 模板复用

---

## 🔍 故障排查

### 问题 1: Obsidian 未检测到新文件

**解决**:
```bash
# 检查文件权限
chmod 644 /home/nicola/ObsidianVault/TaiyiMemory/*.md

# 刷新 Obsidian
Ctrl/Cmd + P → "Reload Obsidian"
```

---

### 问题 2: 双链不生效

**检查**:
1. 文件名是否匹配 `[[文件名]]`
2. 文件是否在 Vault 内
3. 是否启用了"核心插件 → 双向链接"

---

### 问题 3: 模板不应用

**解决**:
1. 检查模板路径：`设置 → 核心插件 → 模板 → 模板文件夹`
2. 确认模板语法正确
3. 使用 `Ctrl/Cmd + P` → "插入模板" 手动测试

---

## 📄 相关文件

| 文件 | 用途 |
|------|------|
| `~/.npm-global/lib/node_modules/openclaw/skills/obsidian/SKILL.md` | Obsidian 技能 |
| `~/.openclaw/openclaw.json` | 配置 Obsidian 路径 |
| `/home/nicola/ObsidianVault/` | Obsidian 主目录 |
| `Templates/ConceptPolishing.md` | 概念打磨模板 |

---

## 🎉 总结

### Obsidian 接入价值

1. ✅ **知识管理**: 结构化存储太一记忆
2. ✅ **双链关联**: 概念之间建立联系
3. ✅ **Graph View**: 可视化知识图谱
4. ✅ **模板系统**: 标准化笔记格式
5. ✅ **自动同步**: 无需手动操作

---

### 立即行动

**Step 1**: 配置 Obsidian Vault 路径
**Step 2**: 测试写入功能
**Step 3**: 启动概念打磨 (银行承兑汇票)
**Step 4**: 设置自动同步

---

**SAYELF，Obsidian 技能已安装！建议立即配置 Vault 路径，启动概念打磨工作流，实现太一记忆自动同步到 Obsidian，构建个人知识图谱。** 📓
