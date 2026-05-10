# ✍️ UX Writer - UX 写作助手

> **版本**: 1.0.0  
> **创建时间**: 2026-04-25  
> **作者**: 太一 AGI  
> **定位**: 太一系统 UX 写作引擎

---

## 🎯 核心使命

提供太一系统 UX 写作能力，生成清晰、简洁、一致的用户界面文案。

### 写作原则

| 原则 | 说明 |
|------|------|
| **清晰** | 表达准确，无歧义 |
| **简洁** | 用最少的词表达最多的信息 |
| **一致** | 术语和风格统一 |
| **友好** | 用户友好的语气 |

---

## 📦 模块功能

### 文案生成

```python
from ux_writer import UXWriter

writer = UXWriter()
copy = writer.generate("button", text="提交")
```

### 文案优化

```python
optimized = writer.optimize(copy, tone="friendly")
```

---

## 🚀 使用方式

### 1. 独立运行

```bash
python core.py --generate button --text "提交"
```

### 2. 太一系统集成

```python
from ux_writer import UXWriter

writer = UXWriter()
copy = writer.generate("heading", text="数据面板")
```

---

## 📋 自进化

- **版本**: 1.0.0
- **进化日志**: `memory/evolution/ux-writer.json`
- **反馈收集**: 文案评分 → 写作优化

---

*太一 UX Writer v1.0 · UX 写作助手*  
*创建时间：2026-04-25*
