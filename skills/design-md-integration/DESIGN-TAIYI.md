# DESIGN.md - 太一 AGI 设计系统

> 版本：v1.0  
> 创建时间：2026-04-08  
> 风格：极简黑客风

---

## 🎨 品牌色彩

| 类型 | 色彩 | 用途 |
|------|------|------|
| **主色** | `#000000` | 背景/主色调 |
| **辅色** | `#FFFFFF` | 文字/对比 |
| **强调色** | `#00FF00` | 终端绿/高亮 |
| **警告** | `#FFFF00` | 黄色警告 |
| **错误** | `#FF0000` | 红色错误 |
| **成功** | `#00FF00` | 绿色成功 |

---

## 📐 字体系统

| 用途 | 字体 | 大小 | 字重 |
|------|------|------|------|
| **代码** | JetBrains Mono | 14px | Regular |
| **标题** | Inter | 24px | Bold |
| **副标题** | Inter | 18px | SemiBold |
| **正文** | Inter | 14px | Regular |
| **辅助文字** | Inter | 12px | Light |

---

## 🧩 组件风格

### 按钮

```css
border-radius: 4px;
padding: 8px 16px;
font-family: 'Inter', sans-serif;
font-weight: 500;
transition: all 0.2s;
```

### 卡片

```css
border-radius: 8px;
border: 1px solid #333;
background: #111;
box-shadow: 0 2px 4px rgba(0,0,0,0.5);
```

### 输入框

```css
border-radius: 4px;
border: 1px solid #444;
background: #000;
color: #fff;
font-family: 'JetBrains Mono', monospace;
```

---

## 📏 间距系统

| 级别 | 大小 | 用途 |
|------|------|------|
| **XS** | 4px | 紧凑间距 |
| **SM** | 8px | 小组件间距 |
| **MD** | 16px | 标准间距 |
| **LG** | 24px | 大间距 |
| **XL** | 32px | 区块间距 |

---

## 🌗 暗色主题

```css
:root {
  --bg-primary: #000000;
  --bg-secondary: #111111;
  --bg-tertiary: #222222;
  
  --text-primary: #FFFFFF;
  --text-secondary: #CCCCCC;
  --text-tertiary: #888888;
  
  --border: #333333;
  --accent: #00FF00;
}
```

---

## 🎭 Bot 差异化

| Bot | 主色 | 强调色 | 风格 |
|-----|------|--------|------|
| **太一** | #000000 | #00FF00 | 极简黑客 |
| **知几** | #1a1a2e | #00d4ff | 金融专业 |
| **山木** | #2d1b1b | #ff6b6b | 创意艺术 |
| **素问** | #1b2d1b | #4ade80 | 学术简洁 |
| **庖丁** | #2d2b1b | #fbbf24 | 财务分析 |

---

## 📱 响应式断点

| 断点 | 宽度 | 用途 |
|------|------|------|
| **SM** | 640px | 手机 |
| **MD** | 768px | 平板 |
| **LG** | 1024px | 桌面 |
| **XL** | 1280px | 大桌面 |

---

## ✅ 设计原则

1. **极简主义** - 少即是多
2. **高对比度** - 清晰可读
3. **功能优先** - 形式追随功能
4. **一致性** - 统一设计语言
5. **可访问性** - 包容性设计

---

## 🔗 参考

- Google Material Design
- Apple Human Interface Guidelines
- GitHub Primer Design System

---

*DESIGN.md - 太一 AGI · 2026-04-08*
