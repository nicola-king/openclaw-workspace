# 📚 Taiyi NotebookLM CLI

> **版本**: v1.0 | **创建**: 2026-04-06 12:20  
> **语言**: Python 3.10+ | **许可证**: MIT  
> **特点**: 极简实现 · 太一原生集成 · 零依赖

---

## 🎯 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| **📖 笔记本管理** | `nlm notebooks` | 创建/列出/删除 |
| **📁 源文件** | `nlm sources` | PDF/URL/YouTube |
| **📝 笔记管理** | `nlm notes` | 创建/编辑/删除 |
| **🎧 音频概览** | `nlm audio` | AI 音频摘要 |
| **💬 对话** | `nlm chat` | 与笔记对话 |

---

## 📦 安装

```bash
# 克隆
cd /home/nicola/.openclaw/workspace/skills/taiyi-notebooklm

# 安装依赖
pip install -r requirements.txt

# 添加到 PATH
ln -s $(pwd)/scripts/nlm /usr/local/bin/nlm
```

---

## 🔑 认证

```bash
# 方式 1: 浏览器自动认证
nlm auth

# 方式 2: Cookie 认证
nlm config --sid "你的__Secure-1PSID"
```

---

## 💡 使用示例

```bash
# 列出笔记本
nlm notebooks list

# 创建笔记本
nlm notebooks create "我的研究"

# 上传源文件
nlm sources add "我的研究" document.pdf

# 生成音频
nlm audio generate "我的研究"

# 对话
nlm chat "我的研究" "总结核心内容"
```

---

## 🔌 太一集成

```python
from skills.taiyi_notebooklm.scripts.client import NotebookLMClient

client = NotebookLMClient()
notebooks = client.list_notebooks()
```

---

*创建：太一 AGI | 2026-04-06 12:20*
