# 📄 太一系统 MD 文件输出标准

> **创建时间**: 2026-04-19 11:28  
> **版本**: v1.0  
> **优先级**: Tier 1 (永久执行)  
> **SAYELF 指令**: "所有文件输出均按照 MD 文件形式，文件名称中文（英文）"

---

## 🎯 核心原则

**默认格式**: Markdown (.md)

**发送方式**: Telegram 文档发送

**文件命名**: 中文（英文）.md

**打开方式**: 点击文件直接打开查看内容

---

## 📄 文件格式标准

### 文件命名

| 要素 | 标准 | 示例 |
|------|------|------|
| **语言** | 中文（英文） | `市场调研报告.md` 或 `market_research.md` |
| **扩展名** | .md | 固定 |
| **长度** | <100 字符 | 简洁明了 |
| **字符** | 字母/数字/下划线/中文 | 避免特殊字符 |

### 文件大小

| 类型 | 大小范围 | 说明 |
|------|---------|------|
| 简报 | <1KB | 每日智慧/简报 |
| 报告 | 1KB-50KB | 调研报告/分析报告 |
| 完整报告 | 50KB-10MB | 综合报告/标准文档 |

### 文件编码

| 要素 | 标准 |
|------|------|
| **编码** | UTF-8 |
| **换行** | LF (Unix) |
| **BOM** | 无 BOM |

---

## 📤 Telegram 发送标准

### 发送方法

```python
def send_md_file(file_path: str, caption: str = ""):
    """
    发送 MD 文件到 Telegram
    """
    # 获取文件大小
    file_size = Path(file_path).stat().st_size
    
    # 格式化大小
    if file_size < 1024:
        size_str = f"{file_size} B"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size/1024:.1f} KB"
    else:
        size_str = f"{file_size/(1024*1024):.1f} MB"
    
    # 完整 Caption
    full_caption = f"{caption}\n\n📄 {file.name}\n💾 {size_str}"
    
    # 发送 (MIME: text/markdown)
    send_document(
        chat_id=CHAT_ID,
        file=file_path,
        caption=full_caption,
        mime_type='text/markdown'
    )
```

### Caption 格式

**标准格式**:
```
{主题描述}

📄 {文件名}
💾 {文件大小}
```

**示例**:
```
📝 测试 MD 文件

📄 test_md_file.md
💾 193 B
```

**或者**:
```
🌐 7 大数据源验证模块集成

📄 7 大数据源验证模块集成报告.md
💾 6.5 KB
```

### MIME 类型

| 文件类型 | MIME 类型 |
|---------|----------|
| .md | text/markdown |
| .txt | text/plain |

---

## ✅ 质量检查清单

### 发送前检查

- [ ] MD 文件格式正确
- [ ] UTF-8 编码
- [ ] 文件名简洁（中文或英文）
- [ ] 文件大小 <50MB
- [ ] Caption 包含文件名 + 大小
- [ ] MIME 类型：text/markdown

### 发送后检查

- [ ] Telegram 显示文件大小
- [ ] 点击可以打开
- [ ] 内容可以看见
- [ ] Git 提交归档

---

## 📊 文件输出统计

### 格式分布

| 格式 | 占比 | 说明 |
|------|------|------|
| .md | 100% | 默认格式 |
| 其他 | 0% | 需客户明确要求 |

### 命名分布

| 命名方式 | 占比 | 示例 |
|---------|------|------|
| 中文.md | 50% | 市场调研报告.md |
| 英文.md | 50% | market_research.md |
| 中文（英文）.md | 可选 | 市场调研报告 (market_research).md |

---

## 📁 文件示例

### 简报类

```
📄 temp_dao_card.md
   328 B MD

🌿 道 Agent · 每日智慧
```

### 报告类

```
📄 7 大数据源验证模块集成报告.md
   6.5 KB MD

🌐 7 大数据源验证模块集成
```

### 分析类

```
📄 market_research.md
   5.2 KB MD

📊 医疗器械市场调研
```

---

## 🔄 执行流程

```
生成内容
    ↓
格式化为 MD (UTF-8)
    ↓
保存到本地
    ↓
获取文件大小
    ↓
生成 Caption (含文件名 + 大小)
    ↓
Telegram 发送 (MIME: text/markdown)
    ↓
确认发送成功
    ↓
Git 提交归档
```

---

## ⚠️ 禁止行为

- ❌ 发送纯文本消息代替 MD 文件
- ❌ 使用非.md 格式（除非客户明确要求）
- ❌ Caption 不包含文件名和大小
- ❌ 使用错误的 MIME 类型
- ❌ 文件编码不是 UTF-8
- ❌ 文件名过长或包含特殊字符

---

## ✅ 必须行为

- ✅ 默认使用.md 格式
- ✅ Caption 包含文件名 + 大小
- ✅ MIME 类型：text/markdown
- ✅ UTF-8 编码
- ✅ 文件可点击打开
- ✅ Git 归档保存

---

## 📜 宪法地位

**优先级**: Tier 1 (永久执行)

**加载顺序**:
1. CONST-ROUTER.md
2. VALUE-FOUNDATION.md
3. NEGENTROPY.md
4. AGI-TIMELINE.md
5. SELF-EVOLUTION-EMERGENCE.md
6. AUTO-EXECUTION-PRINCIPLE.md
7. **FILE_OUTPUT_MD_STANDARD.md** ← 本文件
8. OBSERVER.md
9. SELF-LOOP.md

**适用范围**: 所有太一系统文件输出

---

## 🎯 与现有宪法关系

### 文件输出格式标准 (FILE_OUTPUT_STANDARDS.md)
- MD 文件输出标准 = 文件输出格式的具体实现
- 默认.md 格式
- Telegram 文档发送

### AGI 时间线法则 (AGI-TIMELINE.md)
- MD 文件输出 = AGI 时间线的一次性交付体现
- 完整 MD 文件 → 点击打开 → 查看内容

### 自动执行原则 (AUTO-EXECUTION-PRINCIPLE.md)
- MD 文件输出 = 自动执行的交付方式
- 执行完成后 → 生成 MD 文件 → Telegram 发送

---

## 📋 实施时间

**立即生效**: 2026-04-19 11:28 起

**适用范围**:
- ✅ 跨境贸易 Agent 所有报告
- ✅ AI 搜索 Agent 所有结果
- ✅ 太一系统所有文件输出
- ✅ 所有 Telegram 发送文件

---

## 📤 Telegram 显示效果

```
┌─────────────────────────────────┐
│ 📄 7 大数据源验证模块集成报告.md  │
│    6.5 KB MD                    │
│                                 │
│ 🌐 7 大数据源验证模块集成          │
│ 📄 7 大数据源验证模块集成报告.md  │
│ 💾 6.5 KB                       │
└─────────────────────────────────┘
        ↓ 点击
┌─────────────────────────────────┐
│ # 🌐 7 大数据源验证模块集成报告    │
│                                 │
│ > 执行时间：2026-04-19 11:05    │
│ > 执行状态：✅ 100% 完成         │
│ ...                             │
│                                 │
│ [完整 MD 内容]                   │
└─────────────────────────────────┘
```

---

*太一 AGI · MD 文件输出标准 v1.0*  
*创建时间：2026-04-19 11:28*  
*立即生效 · 永久执行*  
*SAYELF 指令固化*
