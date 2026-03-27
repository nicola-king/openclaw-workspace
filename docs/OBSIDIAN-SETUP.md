# Obsidian 接入方案

> 将太一工作区设置为 Obsidian Vault，实现双向实时同步

---

## 🎯 方案概述

**推荐方案**: 工作区即 Vault

```
Obsidian Vault = ~/.openclaw/workspace/

优势:
✅ 无需同步脚本
✅ 实时双向访问
✅ 零配置成本
✅ 版本控制可选
```

---

## 📋 实施步骤

### 步骤 1：打开 Obsidian

```
1. 启动 Obsidian
2. 点击 "Open folder as vault"
3. 选择：/home/nicola/.openclaw/workspace/
4. 点击 "Open"
```

### 步骤 2：配置插件（可选）

推荐插件:
- [ ] Dataview - 数据查询
- [ ] Templater - 模板引擎
- [ ] Calendar - 日历视图
- [ ] Kanban - 看板管理
- [ ] Excalidraw - 绘图工具

### 步骤 3：创建快捷方式

```bash
# 创建桌面快捷方式
ln -s ~/.openclaw/workspace/ ~/Desktop/太一知识库
```

---

## 📁 目录映射

| Obsidian 目录 | 太一目录 | 说明 |
|--------------|---------|------|
| 01-Daily | memory/ | 每日日志 |
| 02-Knowledge | constitution/ | 知识库 |
| 03-Reports | reports/ | 报告 |
| 04-Skills | skills/ | 技能 |
| 05-Templates | templates/ | 模板 (新建) |
| 06-Archives | archives/ | 归档 (新建) |

---

## 🔗 双向访问示例

### 太一 → Obsidian

```
太一生成报告 → 保存到 reports/
→ Obsidian 自动显示
→ 可在 Obsidian 中查看/编辑/链接
```

### Obsidian → 太一

```
Obsidian 创建笔记 → 保存到 workspace/
→ 太一立即可读取
→ 可用于后续任务
```

---

## 📊 数据流

```
┌─────────────┐
│   Obsidian  │
│   (人工编辑) │
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│ ~/.openclaw/    │
│ workspace/      │ ←─── 共享目录
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   太一 AGI   │
│  (自动生成)  │
└─────────────┘
```

---

## 🎯 使用场景

### 场景 1：人工笔记 + AI 增强

```
1. 在 Obsidian 记录想法
2. 太一读取并扩展
3. 生成报告/执行任务
4. 结果保存回 Obsidian
```

### 场景 2：AI 报告 + 人工整理

```
1. 太一生成分析报告
2. 在 Obsidian 中查看
3. 人工整理/添加链接
4. 形成知识库
```

### 场景 3：双向链接知识网

```
1. 太一生成每日日志
2. Obsidian 自动创建双向链接
3. 形成知识网络
4. 太一可查询关联知识
```

---

## 📋 最佳实践

### 文件命名

```
✅ 推荐:
- YYYY-MM-DD 标题.md (每日日志)
- 主题 - 子主题.md (知识)
- 报告 - 日期 - 主题.md (报告)

❌ 避免:
- 未命名.md
- 临时.md
- 新建文档.md
```

### 标签使用

```
#太一/记忆
#太一/报告
#太一/技能
#项目/Polymarket
#项目/跨境贸易
#状态/进行中
#状态/已完成
```

### 模板示例

```markdown
---
创建日期：{{date}}
标签：#太一/报告
状态：草稿
---

# {{title}}

## 概述

## 核心内容

## 结论

## 后续行动
```

---

## 🚀 进阶功能

### Dataview 查询

```dataview
TABLE file.ctime as 创建时间
FROM #太一/报告
WHERE file.cday >= date(2026-03-01)
SORT file.ctime DESC
```

### 自动备份

```bash
# 每日备份到 Git
cd ~/.openclaw/workspace
git add .
git commit -m "Daily backup $(date +%Y-%m-%d)"
git push
```

---

## 📞 故障排查

### 问题 1：Obsidian 找不到文件

**解决**:
```
1. 检查目录路径是否正确
2. 重启 Obsidian
3. 检查文件权限
```

### 问题 2：太一读取不到 Obsidian 文件

**解决**:
```
1. 确认文件保存在 workspace/ 目录
2. 检查文件扩展名 (.md)
3. 刷新太一记忆
```

---

## 📄 相关文件

- [[OBSIDIAN-README.md]] - Obsidian 知识库说明
- [[MEMORY.md]] - 长期记忆
- [[HEARTBEAT.md]] - 核心待办

---

*创建时间：2026-03-26 | 太一 AGI*
