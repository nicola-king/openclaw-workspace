---
name: markitdown-converter
version: 1.0.0
description: 'MarkItDown 文件转 Markdown 工具 — PDF/Word/Excel/PPT/HTML/图片/音频 → Markdown'
category: utility
tags: ['converter', 'markdown', 'pdf', 'document', 'preprocessing']
status: active
---

# MarkItDown Converter — 文件转 Markdown

微软 MarkItDown 的封装，专为 LLM 数据预处理设计。

## 触发规则

| 用户说 | 路由 |
|--------|------|
| "把 xxx.pdf 转成 md" | `md2md xxx.pdf -o xxx.md` |
| "转换这个文件" | 根据后缀自动选择格式 |
| "有什么格式支持" | `md2md --list-formats` |

## 支持的格式

| 格式 | 后缀 | 说明 |
|------|------|------|
| PDF | `.pdf` | 含排版/表格/图片提取 |
| Word | `.docx` | 含样式/目录 |
| Excel | `.xlsx` | 每 sheet 转一个表格 |
| PPT | `.pptx` | 每页幻灯片转标题+正文 |
| HTML | `.html` | 清理标签，保留结构 |
| 文本 | `.txt .csv .json .xml .yaml` | 原样输出 |
| Markdown | `.md` | 复制不做处理 |
| URL | 网页地址 | 自动抓取后转 md |
| 图片描述 | `.jpg .png .gif .webp` | 需 `--llm-desc` + 配置 LLM |
| 音频转写 | `.mp3 .wav .m4a` | 需 Whisper |

## 用法

```bash
# CLI
md2md 文档.pdf -o 文档.md
md2md 文档.docx 表格.xlsx        # 批量
md2md https://example.com        # 网页
md2md --list-formats             # 格式列表
```

## Python 调用

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("文档.pdf")
print(result.text_content)
```

## 依赖

- `~/.local/venvs/markitdown` — 微软 MarkItDown
- `scripts/scraper.sh` — 网页抓取（可选）
