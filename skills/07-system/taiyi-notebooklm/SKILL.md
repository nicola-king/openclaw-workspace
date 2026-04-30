---
name: taiyi-notebooklm
version: 1.0.0
description: taiyi-notebooklm skill
category: cli
tags: []
author: 太一 AGI
created: 2026-04-07
---


# 📚 Taiyi NotebookLM CLI Skill

> **版本**: v1.0 | **创建**: 2026-04-06 12:20  
> **语言**: Python 3.10+ | **许可证**: MIT  
> **特点**: 零依赖 · 太一原生 · 极简代码 (~300 行)

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
# 进入目录
cd /home/nicola/.openclaw/workspace/skills/taiyi-notebooklm

# 添加执行权限
chmod +x scripts/nlm

# 创建软链接
ln -s $(pwd)/scripts/nlm /usr/local/bin/nlm

# 验证
nlm help
```

---

## 🔑 认证

### 方式 1: 交互式认证

```bash
nlm auth
```

### 方式 2: Cookie 认证

```bash
# 获取 Cookie
# 1. 访问 https://notebooklm.google.com
# 2. F12 → Application → Cookies
# 3. 复制 __Secure-1PSID

# 设置环境变量
export NLM_SID="你的__Secure-1PSID"

# 或保存到配置文件
echo '{"sid": "你的__Secure-1PSID"}' > ~/.taiyi_nlm/config.json
```

---

## 💡 使用示例

### 笔记本管理

```bash
# 列出所有笔记本
nlm notebooks list

# 创建笔记本
nlm notebooks create "我的研究项目"

# 删除笔记本
nlm notebooks rm <笔记本 ID>
```

### 源文件管理

```bash
# 列出源文件
nlm sources <笔记本 ID>

# 添加 PDF
nlm sources <ID> add document.pdf

# 添加 URL
nlm sources <ID> add https://example.com

# 添加 YouTube
nlm sources <ID> add https://youtube.com/watch?v=xxx
```

### 对话

```bash
# 与笔记对话
nlm chat <笔记本 ID> "总结核心内容"
```

### 音频概览

```bash
# 生成音频
nlm audio generate <笔记本 ID>

# 下载音频
nlm audio download <音频 ID> output.mp3
```

---

## 🔌 太一集成

### Python API

```python
from skills.taiyi_notebooklm.scripts.client import NotebookLMClient

# 初始化客户端
client = NotebookLMClient()

# 列出笔记本
notebooks = client.list_notebooks()
for nb in notebooks:
    print(f"{nb.id}: {nb.title}")

# 创建笔记本
nb = client.create_notebook("新项目")

# 添加源文件
client.add_source_pdf(nb.id, "document.pdf")
client.add_source_url(nb.id, "https://example.com")

# 对话
response = client.chat(nb.id, "总结核心内容")
print(response)

# 生成音频
audio_id = client.generate_audio(nb.id)
client.download_audio(audio_id, "output.mp3")
```

### 知几-E 集成

```python
# skills/zhiji-e/notebooklm_integration.py

from skills.taiyi_notebooklm.scripts.client import NotebookLMClient

class NotebookLMAssistant:
    """NotebookLM 助手 - 太一原生实现"""
    
    def __init__(self):
        self.client = NotebookLMClient()
    
    def research_summary(self, notebook_title: str) -> str:
        """研究生成摘要"""
        notebooks = self.client.list_notebooks()
        target = next(nb for nb in notebooks if nb.title == notebook_title)
        return self.client.chat(target.id, "请用中文总结核心发现")
    
    def create_learning_material(self, notebook_title: str) -> str:
        """创建学习材料"""
        notebooks = self.client.list_notebooks()
        target = next(nb for nb in notebooks if nb.title == notebook_title)
        return self.client.chat(target.id, "生成学习指南")
    
    def audio_briefing(self, notebook_title: str) -> str:
        """生成音频简报"""
        notebooks = self.client.list_notebooks()
        target = next(nb for nb in notebooks if nb.title == notebook_title)
        audio_id = self.client.generate_audio(target.id)
        self.client.download_audio(audio_id, f"/tmp/{notebook_title}.mp3")
        return f"/tmp/{notebook_title}.mp3"
```

---

## 🏗️ 架构设计

### 目录结构

```
skills/taiyi-notebooklm/
├── README.md              # 使用说明
├── requirements.txt       # 依赖（零依赖）
├── scripts/
│   ├── nlm               # CLI 主程序 (~300 行)
│   └── client.py         # API 客户端封装
└── tests/
    └── test_client.py    # 单元测试
```

### 核心模块

| 模块 | 文件 | 说明 |
|------|------|------|
| **CLI** | `scripts/nlm` | 命令行接口 |
| **Client** | `scripts/client.py` | API 客户端 |
| **Config** | `~/.taiyi_nlm/config.json` | 配置存储 |

### API 协议

基于 Google NotebookLM 内部 API:
- 认证：Cookie (`__Secure-1PSID`)
- 协议：HTTPS + JSON
- 端点：`https://notebooklm.google.com/*`

---

## 📊 与 tmc/nlm 对比

| 维度 | tmc/nlm (Go) | Taiyi/nlm (Python) |
|------|-------------|-------------------|
| **语言** | Go | Python 3.10+ |
| **代码量** | ~10,000 行 | ~300 行 |
| **依赖** | 多个 Go 模块 | 零依赖（标准库） |
| **二进制大小** | 27MB | N/A (脚本) |
| **安装** | go build | chmod +x |
| **可维护性** | 中 | 高 |
| **扩展性** | 中 | 高 |
| **太一集成** | 外部 | 原生 |

**优势**:
- ✅ 极简代码 (~300 行 vs ~10,000 行)
- ✅ 零依赖 (标准库)
- ✅ 易于理解和修改
- ✅ 太一原生集成
- ✅ 快速迭代

**劣势**:
- ⚠️ 功能完整度待提升
- ⚠️ 需要逐步实现真实 API 调用

---

## 🎯 开发路线图

### Phase 1: 基础框架 (✅ 完成)
- [x] CLI 框架
- [x] 配置管理
- [x] 基础命令

### Phase 2: API 实现 (P0)
- [ ] 真实 NotebookLM API 调用
- [ ] 笔记本管理完整实现
- [ ] 源文件上传
- [ ] 对话功能

### Phase 3: 高级功能 (P1)
- [ ] 音频生成/下载
- [ ] 批量操作
- [ ] MCP 集成

### Phase 4: 优化 (P2)
- [ ] 性能优化
- [ ] 错误处理增强
- [ ] 日志系统

---

## ⚠️  注意事项

### ✅ 推荐做法
- 使用独立 Google 账号
- 不上传敏感数据
- 定期备份配置
- 关注 API 变更

### ❌ 避免做法
- 使用主账号
- 上传敏感信息
- 高频调用
- 商业用途

---

## 🔗 相关链接

- **参考项目**: https://github.com/tmc/nlm
- **官方 NotebookLM**: https://notebooklm.google.com
- **太一文档**: `/home/nicola/.openclaw/workspace/skills/taiyi-notebooklm/README.md`

---

## 📝 快速参考

```bash
# 安装
cd skills/taiyi-notebooklm
chmod +x scripts/nlm
ln -s $(pwd)/scripts/nlm /usr/local/bin/nlm

# 认证
nlm auth

# 使用
nlm notebooks list
nlm notebooks create "我的研究"
nlm chat "我的研究" "总结核心内容"
nlm audio generate "我的研究"
```

---

*创建：太一 AGI | 2026-04-06 12:20*  
**状态**: ✅ 框架完成，待 API 实现
