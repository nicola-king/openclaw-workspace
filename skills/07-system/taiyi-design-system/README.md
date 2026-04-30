# @taiyi/design-system

> 太一 AGI 设计系统  
> 版本：1.0.0  
> 融合原则：苹果 80% + 东方 15% + 中国 5%

---

##  设计理念

**核心原则**:
- 简约是终极的复杂
- 形式追随功能
- 克制即优雅
- 一致性和谐

**融合比例**:
```
苹果设计 80% + 东方设计 15% + 中国设计 5%
```

---

## 📦 安装

```bash
npm install @taiyi/design-system
```

或从本地引用:

```bash
cd /home/nicola/.openclaw/workspace/skills/taiyi-design-system
npm link
```

---

## 🚀 快速开始

### 方式 1: CSS 引入

```jsx
import '@taiyi/design-system/src/styles.css'
```

### 方式 2: 组件引入

```jsx
import { Button, Card, Input } from '@taiyi/design-system'

function App() {
  return (
    <div>
      <Button variant="primary">点击</Button>
      <Card title="卡片标题">内容</Card>
      <Input placeholder="请输入..." />
    </div>
  )
}
```

### 方式 3: CSS 变量

```css
.button {
  background: var(--taiyi-primary);
  border-radius: var(--taiyi-radius-md);
  padding: var(--taiyi-spacing-3);
}
```

---

## 📋 组件文档

### Button 按钮

```jsx
<Button 
  variant="primary"    // primary | secondary | danger | ghost | zen | skyblue
  size="md"            // sm | md | lg
  disabled={false}
  loading={false}
  onClick={handleClick}
>
  点击
</Button>
```

### Card 卡片

```jsx
<Card 
  title="标题"
  variant="default"    // default | elevated | bordered | zen | skyblue
  hoverable={false}
  onClick={handleClick}
>
  内容
</Card>
```

### Input 输入框

```jsx
<Input 
  type="text"          // text | password | email | number
  placeholder="请输入"
  value={value}
  onChange={handleChange}
  label="标签"
  error={false}
  disabled={false}
/>
```

---

## 🎨 设计令牌

### 色彩系统

| 变量 | 色值 | 用途 |
|------|------|------|
| `--taiyi-primary` | #8E8E93 | 主色 (苹果灰) |
| `--taiyi-accent` | #007AFF | 强调色 (苹果蓝) |
| `--taiyi-zen` | #7D8447 | 禅意绿 |
| `--taiyi-skyblue` | #87CEEB | 天青色 |

### 间距系统

| 变量 | 值 | 用途 |
|------|-----|------|
| `--taiyi-spacing-1` | 4px | 最小间距 |
| `--taiyi-spacing-2` | 8px | 小间距 |
| `--taiyi-spacing-3` | 16px | 中间距 |
| `--taiyi-spacing-4` | 24px | 大间距 |

### 圆角系统

| 变量 | 值 | 用途 |
|------|-----|------|
| `--taiyi-radius-sm` | 8px | 小圆角 |
| `--taiyi-radius-md` | 12px | 中圆角 |
| `--taiyi-radius-lg` | 20px | 大圆角 |

---

## 📁 文件结构

```
taiyi-design-system/
├── src/
│   ├── styles.css          # 样式变量
│   ├── index.js            # 入口文件
│   └── components/
│       ├── Button.jsx      # 按钮组件
│       ├── Card.jsx        # 卡片组件
│       └── Input.jsx       # 输入框组件
├── package.json
└── README.md
```

---

## 🎯 使用场景

### Bot Dashboard

```jsx
import { Button, Card } from '@taiyi/design-system'

<Card title="Bot 状态">
  <Button variant="primary">刷新</Button>
</Card>
```

### Skill Dashboard

```jsx
import { Card, Input } from '@taiyi/design-system'

<Card title="搜索技能">
  <Input placeholder="输入技能名称..." />
</Card>
```

### 市政工程造价

```jsx
import { Button, Card, Input } from '@taiyi/design-system'

<Card title="造价计算">
  <Input label="道路长度" type="number" />
  <Button variant="skyblue">计算</Button>
</Card>
```

---

## 📚 参考资源

- [awesome-design-systems](https://github.com/alexpate/awesome-design-systems) ⭐ 19k+
- [Apple Design Resources](https://www.apple.com/design-resources/)
- [IBM Carbon Design](https://carbondesignsystem.com/)

---

## 📝 更新日志

### v1.0.0 (2026-04-10)

- ✅ 初始版本
- ✅ Button 组件
- ✅ Card 组件
- ✅ Input 组件
- ✅ CSS 变量系统
- ✅ 设计令牌

---

*太一 AGI 设计系统 v1.0*  
*创建时间：2026-04-10*  
*融合原则：苹果 80% + 东方 15% + 中国 5%*
