# DESIGN.md 集成 - AI 设计系统文档

> 状态：🟡 调研完成，待集成  
> 学习日期：2026-04-08  
> 来源：SAYELF 分享

---

## 📦 工具信息

| 项目 | 详情 |
|------|------|
| **名称** | DESIGN.md / Awesome DESIGN.md |
| **概念来源** | Google Stitch |
| **中文合集** | [GitHub - bbylw/awesome-design-md-cn](https://github.com/bbylw/awesome-design-md-cn) |
| **格式** | Markdown |
| **用途** | AI 可读的设计系统规范 |

---

## 🎯 核心概念

**DESIGN.md** 是 Google Stitch 引入的新概念：

> 一个纯文本的设计系统文档，AI 代理通过阅读它来生成一致的 UI。

**特点**：
- 📄 纯 Markdown 格式 - LLM 原生友好
- 🎨 无需 Figma/JSON/特殊工具
- 🤖 AI 可直接读取并生成匹配 UI
- 📦 包含 AGENTS.md（编码规范）+ DESIGN.md（设计规范）

---

## 📐 文件结构

```
project/
├── AGENTS.md      # 编码代理规范
├── DESIGN.md      # 设计代理规范
└── src/           # 代码
```

### AGENTS.md 示例

```markdown
# AGENTS.md

| 文件 | 谁会读它 | 它的定义 |
|------|---------|---------|
| AGENTS.md | 编码代理 | 如何构建项目 |
| DESIGN.md | 设计代理 | 项目应该呈现怎样的外观和感觉 |
```

### DESIGN.md 示例

```markdown
# DESIGN.md

## 品牌色彩
- 主色：#007AFF（科技蓝）
- 辅色：#34C759（成功绿）
- 警告：#FF9500

## 字体
- 标题：Inter Bold
- 正文：Inter Regular

## 组件风格
- 圆角：8px
- 阴影：轻微
- 动画：流畅过渡
```

---

## 💡 太一集成场景

### 场景 1：前端项目快速启动

```
新前端项目 → 复制 DESIGN.md → AI 生成一致 UI
```

**价值**：
- 无需从零设计
- 保持品牌一致性
- AI 生成代码符合规范

### 场景 2：55+ 大厂设计语言参考

Awesome DESIGN.md 合集包含：
- Apple Human Interface Guidelines
- Google Material Design
- Microsoft Fluent Design
- Ant Design
- ...等 55+ 大厂设计系统

**用法**：
```
选择设计语言 → 复制对应 DESIGN.md → AI 按此风格生成
```

### 场景 3：Bot Dashboard 统一 UI

为太一各 Bot 创建统一 DESIGN.md：
- 知几：金融专业风格
- 山木：创意艺术风格
- 素问：学术简洁风格
- 太一：极简黑客风

---

## 📋 集成 Checklist

### P0 - 立即执行（今日）
- [x] ✅ 调研完成
- [ ] ⏳ 创建太一 DESIGN.md 模板
- [ ] ⏳ 创建 AGENTS.md 模板
- [ ] ⏳ 编写使用文档

### P1 - 本周执行
- [ ] ⏳ 应用到 Bot Dashboard
- [ ] ⏳ 应用到新前端项目
- [ ] ⏳ 收集 55+ 大厂设计语言

### P2 - 按需执行
- [ ] ⏳ 设计语言切换器
- [ ] ⏳ AI 设计审查工具

---

## 🔗 相关链接

- Awesome DESIGN.md 中文合集：https://github.com/bbylw/awesome-design-md-cn
- Google Stitch 官方文档：https://stitch.withgoogle.com/docs/design-md/overview/
- 知乎教程：https://zhuanlan.zhihu.com/p/2024386480110404702

---

*创建时间：2026-04-08 22:15*  
*创建人：太一 AGI*  
*状态：🟡 调研完成，待集成*
