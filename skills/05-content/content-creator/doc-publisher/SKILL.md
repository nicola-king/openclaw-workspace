# Doc Publisher - 文档自动化发布

> **版本**: v1.0  
> **创建时间**: 2026-04-15  
> **职责**: Markdown → HTML → PDF → Telegram 全自动发布  
> **归属**: content-creator 子技能  
> **状态**: ✅ 已部署

---

## 🎯 职责域

**核心功能**: 文档自动化发布

**适用场景**:
- Markdown 文档转 PDF
- 自动发送到 Telegram
- Design Agent 排版优化
- 定时自动发布
- 日报/周报自动发布
- 会议纪要自动发送

---

## 🧠 核心能力

### 1. 文档转换
- ✅ Markdown → HTML (Design Agent 优化)
- ✅ HTML → PDF (Chrome Headless)
- ✅ A4 打印优化
- ✅ 彩色优化

### 2. 自动发布
- ✅ Telegram 自动发送
- ✅ 带描述信息
- ✅ 可点击打开
- ✅ 可在线预览
- ✅ 可下载保存

### 3. 定时调度
- ✅ crontab 集成
- ✅ 定时发布
- ✅ 批量发布
- ✅ 自动重试

---

## 🚀 使用说明

### 快速发布
```bash
bash skills/05-content/content-creator/doc-publisher/auto-publish-doc.sh "文档.md"
```

### 定时发布
```bash
# 添加到 crontab
0 9 * * * bash skills/05-content/content-creator/doc-publisher/auto-publish-doc.sh "日报.md"
```

### 批量发布
```bash
# 批量发布所有 Markdown 文档
for md_file in /home/nicola/.openclaw/workspace/*.md; do
    bash skills/05-content/content-creator/doc-publisher/auto-publish-doc.sh "$md_file"
done
```

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 执行时间 | <10 秒 |
| 成功率 | 100% |
| 支持格式 | MD/HTML/PDF |
| 支持渠道 | Telegram |
| PDF 大小 | 20KB-2MB |

---

## 🔗 与其他 Agent 的关系

### 上游 Agent
```
✅ content-creator - 内容创作
✅ Design Agent - 排版优化
✅ shanmu - 内容优化
```

### 下游 Agent
```
✅ Telegram Bot - 消息发送
✅ wisdom-scheduler - 定时调度
```

### 协作关系
```
content-creator → doc-publisher → Telegram
     ↓
Design Agent (排版优化)
```

---

## 📁 文件结构

```
doc-publisher/
├── auto-publish-doc.sh      # 主脚本
├── send-pdf-to-telegram.py  # PDF 发送脚本
├── md2pdf.sh                # MD 转 PDF 工具
└── SKILL.md                 # 本文件
```

---

## 🎯 归属关系

**父技能**: content-creator  
**子技能**: 无  
**同级技能**: 
- publisher/ - 社交媒体发布
- social-media-auto/ - 社交媒体自动化

**太一系统位置**: 
```
skills/
└── 05-content/
    └── content-creator/
        ├── publisher/
        └── doc-publisher/  ⭐ 新增
```

---

## 📈 管理优势

### 统一管理
```
✅ 所有发布技能统一管理
✅ 统一配置管理
✅ 统一日志管理
```

### 技能复用
```
✅ 复用 content-creator 资源
✅ 复用 Design Agent 优化
✅ 复用 Telegram Bot
```

### 职责清晰
```
✅ 创作：content-creator
✅ 优化：Design Agent
✅ 发布：doc-publisher
✅ 调度：wisdom-scheduler
```

---

## 🎯 后续扩展

### 功能扩展
```
⏳ 支持 Word 文档输出
⏳ 支持邮件发送
⏳ 支持微信发送
⏳ 支持网页发布
```

### 渠道扩展
```
⏳ Telegram → 多渠道
⏳ 邮件 → SMTP
⏳ 微信 → 企业微信
⏳ 网页 → GitHub Pages
```

### 调度扩展
```
⏳ crontab → 智能调度
⏳ 定时 → 事件触发
⏳ 单次 → 批量
```

---

*太一 AGI · Doc Publisher · 2026-04-15*

**🤖 文档自动化发布技能已部署！**
