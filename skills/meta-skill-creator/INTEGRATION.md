# Meta-Skill-Creator · 太一集成文档

> 创建时间：2026-04-06 | 版本：v1.0 | 状态：✅ 已集成

---

## 🎯 自然语言触发器

### 直接触发（用户说）

| 用户输入 | 识别结果 | 执行动作 |
|---------|---------|---------|
| "创建一个 XX skill" | 技能创建 | `create-skill.py XX "功能描述"` |
| "生成一个 XX 技能" | 技能创建 | `create-skill.py XX "功能描述"` |
| "新建一个 XX 工具" | 技能创建 | `create-skill.py XX "功能描述"` |
| "把这些 Markdown 做成 EPUB" | EPUB 生成 | `epub-book-generator.py input.md` |
| "制作一个视频处理工具" | 视频技能 | `create-skill.py video-processor "视频处理"` |
| "生成图片的 skill" | 图片技能 | `create-skill.py image-generator "图片生成"` |

---

## 🤖 太一集成协议

### 步骤 1：意图识别

太一收到用户消息后，检查是否包含以下关键词：

```python
CREATE_SKILL_TRIGGERS = [
    "创建", "生成", "新建", "做一个", "写一个",
    "skill", "技能", "工具", "插件"
]

SKILL_TYPE_KEYWORDS = {
    "data": ["采集", "抓取", "监控", "数据", "crawl", "scrape"],
    "video": ["视频", "剪辑", "ffmpeg"],
    "image": ["图片", "图像", "封面", "image"],
    "workflow": ["工作流", "自动化", "批量"],
    "content": ["生成", "制作", "转换", "电子书", "epub"],
}
```

### 步骤 2：参数提取

从用户输入中提取：
- **技能名称**：英文或拼音，自动转换为 kebab-case
- **功能描述**：中文描述，用于 SKILL.md

**示例**：
```
用户："创建一个 epub-book-generator skill，功能是 Markdown 转 EPUB 电子书"
→ skill_name: epub-book-generator
→ description: Markdown 转 EPUB 电子书
```

### 步骤 3：执行创建

```bash
cd ~/.openclaw/workspace/skills/meta-skill-creator
python3 scripts/create-skill.py {skill_name} "{description}"
```

### 步骤 4：结果汇报

```
✅ 技能创建成功！

📁 {skill_path}
📋 类型：{template_type}
📦 依赖：{dependencies}

📝 下一步:
1. 编辑 SKILL.md 完善功能
2. 实现核心逻辑
3. 测试运行
```

---

## 📋 完整工作流示例

### 示例 1：创建 EPUB 生成器

**用户**：「太一，创建一个 epub-book-generator skill，功能是 Markdown 转 EPUB 电子书」

**太一**：
1. 识别意图：技能创建
2. 提取参数：
   - skill_name: epub-book-generator
   - description: Markdown 转 EPUB 电子书
3. 执行：`python3 create-skill.py epub-book-generator "Markdown 转 EPUB 电子书"`
4. 汇报结果 + 目录结构

### 示例 2：创建视频工具

**用户**：「生成一个视频处理工具」

**太一**：
1. 识别意图：技能创建（视频类）
2. 提取参数：
   - skill_name: video-processor
   - description: 视频剪辑/转换/压缩工具
3. 执行：`python3 create-skill.py video-processor "视频剪辑/转换/压缩工具"`
4. 汇报结果

### 示例 3：直接使用已有技能

**用户**：「把这个 Markdown 文件做成 EPUB」

**太一**：
1. 识别意图：使用已有技能
2. 检查技能：epub-book-generator 是否存在
3. 执行：`python3 epub-book-generator.py {input.md}`
4. 交付 EPUB 文件

---

## 🔧 CLI 快捷命令

在 `~/.openclaw/workspace/scripts/` 创建快捷脚本：

### create-skill CLI

```bash
#!/bin/bash
# ~/.openclaw/workspace/scripts/create-skill

SKILLS_DIR="$HOME/.openclaw/workspace/skills/meta-skill-creator"
python3 "$SKILLS_DIR/scripts/create-skill.py" "$@"
```

**用法**：
```bash
create-skill my-skill "功能描述"
```

### epub CLI

```bash
#!/bin/bash
# ~/.openclaw/workspace/scripts/epub

SKILLS_DIR="$HOME/.openclaw/workspace/skills/epub-book-generator"
python3 "$SKILLS_DIR/scripts/epub-book-generator.py" "$@"
```

**用法**：
```bash
epub book.md -o book.epub --title "我的书" --author "作者"
```

---

## 🧪 测试用例

### 测试 1：创建内容生成类技能

```bash
python3 scripts/create-skill.py content-creator "内容创作工具"
# 预期：识别为 content 类型，依赖 jinja2/markdown/pypandoc
```

### 测试 2：创建视频处理类技能

```bash
python3 scripts/create-skill.py video-editor "视频编辑工具"
# 预期：识别为 video 类型，依赖 ffmpeg-python
```

### 测试 3：创建图片处理类技能

```bash
python3 scripts/create-skill.py image-optimizer "图片优化工具"
# 预期：识别为 image 类型，依赖 Pillow
```

---

## 📊 模板库（6 类）

| 类型 | 关键词 | 依赖 | 示例技能 |
|------|--------|------|---------|
| **data** | 采集/抓取/监控/数据 | requests, bs4, pandas | github-crawler, weather-scraper |
| **content** | 生成/制作/转换/电子书 | jinja2, markdown, pypandoc | epub-generator, html-converter |
| **video** | 视频/剪辑/ffmpeg | ffmpeg-python | video-processor, clip-maker |
| **image** | 图片/图像/封面 | Pillow | image-generator, cover-maker |
| **workflow** | 工作流/自动化/批量 | pyyaml | batch-processor, auto-workflow |
| **tool** | 其他工具/API | requests, click | api-wrapper, cli-tool |

---

## 🚀 未来扩展

- [ ] 技能模板市场（从 ClawHub 下载）
- [ ] 技能依赖自动安装
- [ ] 技能测试框架集成
- [ ] 技能版本管理（语义化版本）
- [ ] 技能发布到 ClawHub
- [ ] 语音触发（"小魔力，创建一个 XX 技能"）

---

*集成时间：2026-04-06 | 太一版本：v4.0*
