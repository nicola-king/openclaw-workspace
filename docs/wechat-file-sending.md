# 微信文件发送规范

> 版本：v1.0 | 创建：2026-04-09 00:18  
> 状态：✅ 立即生效

---

## 🎯 核心原则

**生成 .md 文件后，必须自动发送内容到微信**

```
❌ 错误：只回复文件路径
✅ 正确：发送内容预览 + 文件信息
```

---

## 📋 执行流程

### 1. 生成文件

```python
write(path, content)  # 生成 .md 文件
```

### 2. 读取内容

```python
from pathlib import Path
content = Path(path).read_text(encoding='utf-8')
```

### 3. 发送微信

```python
# 文件信息
file_info = f"""📄 文件已生成

文件名：{path.name}
大小：{len(content)}字
路径：{path}

"""

# 内容预览（前 2000 字）
preview = content[:2000]
if len(content) > 2000:
    preview += "\n\n...（内容过长，查看完整文件：cat {path}）"

# 发送
sessions_send(file_info + preview)
```

---

## 📝 示例

### 生成报告后

**❌ 错误回复：**
```
文件已保存：reports/2026-04-09-p1-complete.md
```

**✅ 正确回复：**
```
📄 文件已生成

文件名：2026-04-09-p1-complete.md
大小：3128 字
路径：/home/nicola/.openclaw/workspace/reports/2026-04-09-p1-complete.md

# P1 任务执行报告 · 全部完成

> 执行时间：2026-04-09 00:10-00:25...

（内容预览前 2000 字）

...（内容过长，查看完整文件：cat 路径）
```

---

## 🔧 立即执行

**从此刻开始，所有 .md 文件生成后：**

1. ✅ 自动读取内容
2. ✅ 微信发送预览（前 2000 字）
3. ✅ 告知完整路径
4. ✅ 提供查看指令

---

**状态：✅ 立即生效**

*太一 AGI · 2026-04-09 00:18*
