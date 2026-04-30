---
name: meta-skill-creator
version: 1.0.0
description: meta-skill-creator skill
category: general
tags: []
author: 太一 AGI
created: 2026-04-07
---


# Meta-Skill-Creator · 元技能创建器 v1.0

> 创建时间：2026-04-06 | 灵感来源：yao-meta-skill (Claude Code) | 状态：✅ 激活

---

## 🎯 核心功能

**输入**：技能需求描述（自然语言）
**输出**：完整的 Skill 目录结构 + SKILL.md + 脚本框架

### 标准目录结构

```
~/.openclaw/workspace/skills/{skill-name}/
├── SKILL.md           # 技能定义文件（必须）
├── scripts/           # 执行脚本
├── references/        # 参考资料
├── agents/            # Agent 配置（可选）
└── README.md          # 使用说明
```

---

## 🎬 触发场景

- "创建 XX skill"
- "生成 XX 技能"
- "把这些 Markdown 做成 EPUB"
- "生成带封面的电子书"
- "新建一个 XX 工具"

---

## 📋 创建流程（6 阶段）

### 阶段 1：需求理解
```
- 技能名称：{skill-name}
- 核心功能：[用一句话描述]
- 触发关键词：[列出 3-5 个]
- 输入/输出：[数据格式]
```

### 阶段 2：目录结构创建
```bash
mkdir -p ~/.openclaw/workspace/skills/{skill-name}/{scripts,references,agents}
```

### 阶段 3：SKILL.md 生成
包含以下章节：
- 核心功能
- 触发场景
- 使用示例
- 配置说明
- 依赖项

### 阶段 4：脚本框架生成
根据技能类型选择模板：
- **CLI 工具** → Bash/Python 脚本
- **API 集成** → HTTP 客户端 + 封装
- **自动化** → Playwright/Selenium 脚本
- **数据处理** → Pandas/NumPy 脚本

### 阶段 5：测试验证
```bash
# 检查文件结构
ls -la ~/.openclaw/workspace/skills/{skill-name}/

# 验证 SKILL.md 语法
cat ~/.openclaw/workspace/skills/{skill-name}/SKILL.md
```

### 阶段 6：Git 提交
```bash
cd ~/.openclaw/workspace
git add skills/{skill-name}/
git commit -m "feat: 创建 {skill-name} skill"
git push
```

---

## 🛠️ 技能模板库

### 模板 1：数据采集类

```markdown
# {Skill-Name} - 数据采集

## 核心功能
- 从 {数据源} 采集 {数据类型}
- 支持定时任务/手动触发
- 输出格式：JSON/CSV/数据库

## 触发场景
- "采集 {数据源} 数据"
- "抓取 {网站} 内容"
- "监控 {目标} 变化"
```

### 模板 2：内容生成类

```markdown
# {Skill-Name} - 内容生成

## 核心功能
- 输入：{输入格式}
- 输出：{输出格式}
- 支持：{特性 1/特性 2/特性 3}

## 触发场景
- "生成 {内容类型}"
- "制作 {输出格式}"
- "把 {输入} 做成 {输出}"
```

### 模板 3：工具集成类

```markdown
# {Skill-Name} - 工具集成

## 核心功能
- 封装 {工具/API} 功能
- 提供简化接口
- 支持 {平台/环境}

## 触发场景
- "使用 {工具名}"
- "调用 {API 名}"
- "执行 {操作名}"
```

---

## 📦 依赖管理

### Python 技能
```
requirements.txt
- requests
- beautifulsoup4
- pandas
- playwright
```

### Node.js 技能
```
package.json
- axios
- cheerio
- puppeteer
```

### Bash 技能
```
依赖工具：
- curl
- jq
- ffmpeg
```

---

## 🔧 配置说明

### 环境变量
```bash
# ~/.openclaw/workspace/skills/{skill-name}/.env.example
API_KEY=your_api_key_here
BASE_URL=https://api.example.com
```

### OpenClaw 集成
```yaml
# 在 SKILL.md 中添加
openclaw:
  triggers:
    - "触发词 1"
    - "触发词 2"
  permissions:
    - exec
    - network
    - filesystem
```

---

## ✅ 质量门禁

创建完成后检查：
- [ ] SKILL.md 包含所有必需章节
- [ ] 目录结构符合标准
- [ ] 脚本有 shebang 和执行权限
- [ ] README.md 有使用示例
- [ ] .env.example 包含所有配置项
- [ ] Git 提交信息规范

---

## 📝 使用示例

### 示例 1：创建 EPUB 生成器

**用户**：「创建一个 epub-book-generator skill」

**Meta-Skill-Creator**：
1. 理解需求：Markdown → EPUB 转换
2. 创建目录：`skills/epub-book-generator/`
3. 生成 SKILL.md（包含核心功能/触发场景）
4. 创建脚本：`scripts/generate-epub.py`
5. 添加依赖：`requirements.txt` (pypandoc, ebooklib)
6. Git 提交并推送

### 示例 2：创建天气查询工具

**用户**：「生成一个 weather-query skill」

**Meta-Skill-Creator**：
1. 理解需求：查询天气预报
2. 创建目录：`skills/weather-query/`
3. 生成 SKILL.md（集成 Open-Meteo API）
4. 创建脚本：`scripts/query-weather.py`
5. 添加配置：`.env.example` (城市坐标)
6. Git 提交并推送

---

## 🚀 快速启动

```bash
# 1. 创建技能
太一，创建一个 {skill-name} skill，功能是 {功能描述}

# 2. 验证结构
ls -la ~/.openclaw/workspace/skills/{skill-name}/

# 3. 测试运行
cd ~/.openclaw/workspace/skills/{skill-name}/
./scripts/{main-script}.sh

# 4. Git 提交
git add skills/{skill-name}/
git commit -m "feat: 创建 {skill-name}"
```

---

## 📊 与 yao-meta-skill 对比

| 特性 | yao-meta-skill | Meta-Skill-Creator | 优势 |
|------|---------------|-------------------|------|
| **目录结构** | ~/.claude/skills/ | ~/.openclaw/workspace/skills/ | OpenClaw 原生 |
| **触发方式** | 自然语言 | 自然语言 + 模板库 | 更灵活 |
| **模板系统** | 基础 | 3 类模板（数据/内容/工具） | 更丰富 |
| **质量门禁** | 手动检查 | 自动检查清单 | 更可靠 |
| **Git 集成** | 手动 | 自动提交推送 | 更高效 |

---

## 🔮 未来扩展

- [ ] 技能模板市场（从 ClawHub 下载）
- [ ] 技能依赖自动解析
- [ ] 技能测试框架集成
- [ ] 技能版本管理（语义化版本）
- [ ] 技能发布到 ClawHub

---

*创建时间：2026-04-06 | 版本：v1.0 | 状态：✅ 激活*
