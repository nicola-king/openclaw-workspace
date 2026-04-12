---
name: markitdown-integration
version: 1.0.0
description: Microsoft MarkItDown 集成 - 文档转 Markdown 工具
category: tools
tags: ['markdown', 'document', 'conversion', 'microsoft', 'pdf', 'word', 'excel', 'pptx']
author: 太一 AGI
created: 2026-04-09
status: active
priority: P1
---

# 📄 MarkItDown 集成 - 微软文档转换工具 v1.0

> **版本**: 1.0.0 | **创建**: 2026-04-09  
> **灵感**: [Microsoft MarkItDown](https://github.com/microsoft/markitdown)  
> **定位**: 将任何格式文档转换为 Markdown (AI 最青睐的格式)  
> **核心优势**: 干净、结构化、无损坏布局

---

## 🎯 核心功能

### 1. 多格式支持 ✅

**支持的格式**:
| 类型 | 格式 | 说明 |
|------|------|------|
| **文档** | PDF, Word (DOCX) | 保留标题/列表/表格 |
| **表格** | Excel (XLSX), CSV | 保留表格结构 |
| **演示** | PowerPoint (PPTX) | 保留幻灯片结构 |
| **图片** | JPG, PNG, GIF | EXIF 元数据 + OCR |
| **音频** | WAV, MP3 | EXIF + 语音转录 |
| **网页** | HTML, YouTube URL | 提取正文内容 |
| **其他** | JSON, XML, ZIP, EPUB | 结构化文本 |

### 2. 高质量转换 ✅

**特点**:
- ✅ 保留文档结构 (标题/列表/表格/链接)
- ✅ 无自定义解析器
- ✅ 无损坏的布局
- ✅ 无混乱的文本
- ✅ 干净、结构化的 Markdown

### 3. LLM 优化 ✅

**为什么 Markdown**:
- LLM 原生"说"Markdown
- GPT-4o 等模型训练于大量 Markdown 数据
- Token 效率高
- 最小标记，最大信息密度

---

## 🚀 使用方式

### CLI 用法

```bash
# 安装
pip install 'markitdown[all]'

# 转换单个文件
markitdown document.pdf > document.md

# 指定输出文件
markitdown document.pdf -o document.md

# 管道输入
cat document.pdf | markitdown

# 使用插件
markitdown --use-plugins document.pdf
```

### Python API

```python
from markitdown import MarkItDown

# 初始化
md = MarkItDown()

# 转换文件
result = md.convert("document.pdf")
print(result.text_content)

# 使用 LLM 描述图片
from openai import OpenAI
client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("image.jpg")
print(result.text_content)
```

---

## 📦 安装步骤

### 基础安装

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装完整功能
pip install 'markitdown[all]'
```

### 按需安装

```bash
# 只安装文档格式支持
pip install 'markitdown[pdf,docx,pptx,xlsx]'

# 添加 OCR 插件
pip install markitdown-ocr

# 添加语音转录
pip install 'markitdown[audio-transcription]'
```

---

## 🔗 与太一体系集成

### 技能创建流程

```
上传文档 (PDF/Word/PPTX)
    ↓
MarkItDown 转换
    ↓
Markdown 文件
    ↓
存入 skills/ 目录
    ↓
自动创建 SKILL.md 框架
```

### 知识库构建

```
批量文档上传
    ↓
MarkItDown 批量转换
    ↓
Markdown 知识库
    ↓
FTS5 索引
    ↓
语义搜索可用
```

---

## ⚠️ 注意事项

### 版本变更

- 依赖分组安装 (`[all]` / `[pdf]` / `[docx]` 等)
- `convert_stream()` 需要二进制文件对象
- 不再创建临时文件

### 插件支持

- 默认禁用插件
- 使用 `--use-plugins` 启用
- 查看已安装：`markitdown --list-plugins`

### OCR 插件

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o"
)
result = md.convert("document_with_images.pdf")
print(result.text_content)
```

---

## 📊 使用场景

| 场景 | 输入 | 输出 | 用途 |
|------|------|------|------|
| **技能创建** | PDF 文档 | Markdown | 快速创建 Skill |
| **知识库** | Word/Excel | Markdown | 构建可搜索知识库 |
| **会议记录** | PPTX + 音频 | Markdown | 整理会议内容 |
| **学习笔记** | EPUB/PDF | Markdown | 读书笔记/学习总结 |
| **网页存档** | YouTube/HTML | Markdown | 内容存档/引用 |

---

## 🎯 与太一技能结合

### 场景 1: 快速创建技能

```bash
# 上传产品文档
markitdown product-spec.pdf > product-spec.md

# 移动到技能目录
mv product-spec.md skills/product-skill/

# 创建 SKILL.md
# (手动补充技能元数据)
```

### 场景 2: 构建知识库

```bash
# 批量转换
for file in docs/*.pdf; do
    markitdown "$file" -o "knowledge/${file%.pdf}.md"
done

# 建立索引
python3 skills/hermes-learning-loop/search/fts5_index.py rebuild
```

---

## 📋 变更日志

### v1.0.0 (2026-04-09)
- ✅ 初始集成
- ✅ 支持所有主要格式
- ✅ CLI + Python API
- ✅ 插件支持
- ✅ OCR 集成

---

*创建：2026-04-09 23:30 | 太一 AGI | 灵感：Microsoft MarkItDown*
