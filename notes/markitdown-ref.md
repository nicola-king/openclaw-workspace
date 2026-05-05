# MarkItDown - 微软开源文件转 Markdown 工具

> 记录时间：2026-05-05 | 来源：github.com/microsoft/markitdown

## 核心定位

轻量级 Python 工具，把 PDF/Word/Excel/PPT/图片/音频/HTML 等转换成 Markdown，**专为 LLM 数据预处理设计**。

## 安装

```bash
pip install 'markitdown[all]'
# 或按需：pip install 'markitdown[pdf, docx, pptx, xlsx]'
```

## CLI 用法

```bash
markitdown document.pdf -o output.md
cat document.pdf | markitdown  # 管道输入
```

## Python 用法

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)
```

## LLM 图片描述

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("example.jpg")
print(result.text_content)
```

## OCR 插件

```bash
pip install markitdown-ocr
```

自动用 LLM Vision 从 PDF/DOCX/PPTX/XLSX 的嵌入图片中提取文字。

## 对我方场景的价值

| 场景 | 用途 |
|------|------|
| 外贸社媒优化 | Word/PDF/Excel 稿件转纯文本喂给 SEO 模型 |
| GEO 审计 | HTML 竞品页面 → 结构化 Markdown → 对比分析 |
| 量化研究 | PDF 研报 → Markdown → 关键信号提取 |
| 公众号运营 | 多格式素材统一转 Markdown 正文 |
