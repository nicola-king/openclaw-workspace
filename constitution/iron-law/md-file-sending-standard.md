# 📜 太一铁律：MD 文件发送标准

> **创建时间**: 2026-04-14 19:08  
> **铁律等级**: Tier 1 (永久核心)  
> **适用范围**: 所有 MD 文件发送

---

## 🎯 铁律内容

### 核心原则
```
✅ 所有 MD 文件的说明必须从文件内容动态提取（提炼总结）
✅ 所有 MD 文件必须带时间戳（避免 Telegram 缓存）
✅ 禁止硬编码任何说明内容
✅ 说明内容必须与 MD 文件内容完全一致
```

---

## 📋 执行标准

### 1. 动态提取内容
```python
# ✅ 正确：从 MD 文件动态提取
content = extract_content_from_md(md_file_path)
title = content['title']
version = content['version']
achievements = content['achievements']

# ❌ 错误：硬编码内容
caption = """🏠 钢结构折叠式房屋需求报告"""
```

### 2. 带时间戳
```python
# ✅ 正确：带时间戳
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
caption = f"{title}\n\n生成时间：{timestamp}"

# 或使用带时间戳的文件名
filename = f"{project}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
```

### 3. 内容一致性
```
✅ 标题：从 MD 文件提取
✅ 版本：从 MD 文件提取
✅ 状态：从 MD 文件提取
✅ 功能：从 MD 文件提取
✅ 成就：从 MD 文件提取
✅ 测试结果：从 MD 文件提取
```

---

## 🔧 技术实现

### extract_content_from_md() 函数
```python
def extract_content_from_md(md_file_path):
    """从 MD 文件动态提取内容"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # 提取标题
    title = ""
    for line in lines[:20]:
        if line.startswith('#'):
            title = line.replace('#', '').strip()
            break
    
    # 提取版本信息
    version = ""
    status = ""
    for line in lines[:20]:
        if '> **版本**:' in line or '> Version:' in line:
            version = line.split(':')[1].strip()
        if '> **状态**:' in line or '> Status:' in line:
            status = line.split(':')[1].strip()
    
    # 提取核心功能数量
    features = ""
    for line in lines[20:50]:
        if '核心功能' in line or 'Core Features' in line:
            if '18' in line:
                features = '18 个核心功能'
            elif '18+' in line:
                features = '18+ 核心功能'
            break
    
    # 提取关键成就
    achievements = []
    for line in lines[20:80]:
        if '✅' in line and ('功能' in line or '能力' in line or 'CLI' in line):
            achievements.append(line.strip())
            if len(achievements) >= 5:
                break
    
    return {
        'title': title,
        'version': version,
        'status': status,
        'features': features,
        'achievements': achievements,
    }
```

### 发送函数
```python
def send_md_file(md_file_path, chat_id=TELEGRAM_CHAT_ID):
    """发送 MD 文件到 Telegram"""
    # 从 MD 文件动态提取内容
    content = extract_content_from_md(md_file_path)
    
    # 构建文件 caption（从 MD 文件内容提取，带时间戳）
    caption = f"""{content['title']}

{content['version']}
{content['status']}
{content['features']}

📄 点击文件直接打开查看

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 构建预览消息（从 MD 文件内容提取，带时间戳）
    achievements_text = '\n'.join(content['achievements'][:5])
    
    message = f"""{content['title']}

{content['version']}
{content['status']}
{content['features']}

📋 核心成就:
{achievements_text}

📄 点击文件直接打开查看

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 发送预览消息
    send_message(chat_id, message)
    
    # 发送 MD 文件
    send_document(chat_id, md_file_path, caption)
```

---

## ⚠️ 违宪行为

### 禁止的行为
```
❌ 硬编码任何说明内容
❌ 使用固定的 caption 模板
❌ 不带时间戳发送文件
❌ 说明内容与 MD 文件内容不一致
❌ 手动编写说明而不是从文件提取
```

### 违宪后果
```
⚠️ 信息不一致
⚠️ 用户困惑
⚠️ 信任度降低
⚠️ 违反太一铁律
```

---

## ✅ 合宪行为

### 正确的做法
```
✅ 使用 extract_content_from_md() 函数
✅ 动态提取标题/版本/状态/功能/成就
✅ 添加时间戳到 caption 和预览消息
✅ 使用带时间戳的文件名（可选）
✅ 确保说明内容与 MD 文件完全一致
```

### 合宪示例
```python
# ✅ 正确示例
content = extract_content_from_md(md_file_path)
caption = f"{content['title']}\n\n生成时间：{timestamp}"
send_document(chat_id, md_file_path, caption)

# ❌ 错误示例
caption = "🏠 钢结构折叠式房屋需求报告"
send_document(chat_id, md_file_path, caption)
```

---

## 📊 质量检查

### 发送前检查清单
```
☑️ 是否使用了 extract_content_from_md() 函数？
☑️ 说明内容是否从 MD 文件动态提取？
☑️ 是否添加了时间戳？
☑️ 说明内容是否与 MD 文件内容一致？
☑️ 是否避免了硬编码内容？
```

### 发送后验证
```
☑️ Telegram 显示的标题是否正确？
☑️ Telegram 显示的版本是否正确？
☑️ Telegram 显示的功能数量是否正确？
☑️ Telegram 显示的成就是否正确？
☑️ 时间戳是否显示？
```

---

## 📜 铁律历史

| 时间 | 事件 | 说明 |
|------|------|------|
| 2026-04-14 19:08 | 铁律创建 | 基于钢结构房屋内容错误事件 |
| 2026-04-14 19:08 | 脚本更新 | send-md-to-telegram.py 重写了动态提取功能 |

---

## 🎯 适用范围

**适用于**:
```
✅ 所有太一系统发送的 MD 文件
✅ 所有 Telegram 推送的文档
✅ 所有微信推送的文档
✅ 所有其他平台推送的 MD 文件
```

**不适用于**:
```
❌ 临时测试文件（可豁免）
❌ 内部开发文档（可豁免）
```

---

## 🔐 铁律等级

**等级**: Tier 1 (永久核心)

**优先级**: 
```
🔴 最高优先级
🔴 不可违反
🔴 必须遵守
```

**违反后果**:
```
⚠️ 信息不一致
⚠️ 用户信任度降低
⚠️ 系统可靠性受损
```

---

*太一铁律 · 太一 AGI · 2026-04-14 19:08*

**📜 此铁律已锚定，永久生效！**
