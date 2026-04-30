# 🎨 Taiyi-Artisan Design Systems

> 大厂设计风格蒸馏库  
> 融合原则：**苹果 80% + 东方 15% + 中国 5%**  
> 来源：awesome-design-systems (19k+ stars) + 太一宪法设计规范

---

## 📊 设计系统矩阵

| 品牌 | 核心特点 | 融合比例 | 应用场景 |
|------|---------|---------|---------|
| **Apple** | 简约/克制/和谐 | 80% | 主导风格 |
| **Spotify** | 大胆用色/圆形元素 | 借鉴 | 强调色 |
| **IBM** | 网格系统/设计令牌 | 借鉴 | 企业级 |
| **Google** | Material Design | 待整合 | 移动端 |
| **Ant Design** | 企业级组件 | 待整合 | B 端产品 |
| **日本** | 间/侘寂/渋い | 10% | 禅意场景 |
| **中国** | 传统色彩/纹样 | 5% | 文化场景 |

---

## 🎨 配色系统

### 主色调（苹果 80%）

| 变量 | 色值 | 来源 | 用途 |
|------|------|------|------|
| `--taiyi-primary` | #8E8E93 | 苹果灰 | 次要文字 |
| `--taiyi-background` | #FFFFFF | 苹果白 | 背景色 |
| `--taiyi-text` | #1D1D1F | 苹果黑 | 主要文字 |
| `--taiyi-accent` | #007AFF | 苹果蓝 | 强调/链接 |
| `--taiyi-success` | #34C759 | 苹果绿 | 成功状态 |
| `--taiyi-warning` | #FF9500 | 苹果橙 | 警告状态 |
| `--taiyi-error` | #FF3B30 | 苹果红 | 错误状态 |

### 东方色（15%）

| 变量 | 色值 | 来源 | 意境 |
|------|------|------|------|
| `--taiyi-zen` | #7D8447 | 日本抹茶绿 | 宁静致远 |
| `--taiyi-sakura` | #FFB7C5 | 日本樱花粉 | 春日浪漫 |
| `--taiyi-indigo` | #1E3A5F | 日本靛蓝 | 深邃优雅 |
| `--taiyi-wabi` | #8B7355 | 侘寂色 | 朴素自然 |

### 中国色（5%）

| 变量 | 色值 | 朝代 | 意境 |
|------|------|------|------|
| `--taiyi-skyblue` | #87CEEB | 宋 | 雨过天青 |
| `--taiyi-cinnabar` | #E60000 | 汉 | 朱砂热烈 |
| `--taiyi-dailan` | #4A5C8C | 唐 | 黛蓝沉静 |
| `--taiyi-moonwhite` | #D6ECF0 | 明 | 月白素雅 |
| `--taiyi-ink` | #2C2C2C | 先秦 | 墨色内敛 |

---

## 📐 设计令牌

### 字体系统

```css
:root {
  /* 主字体 - Apple */
  --taiyi-font-primary: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  
  /* 代码字体 */
  --taiyi-font-mono: "SF Mono", "JetBrains Mono", "Fira Code", monospace;
  
  /* 字号系统 (1.5 倍率) */
  --taiyi-text-xs: 12px;
  --taiyi-text-sm: 16px;
  --taiyi-text-base: 24px;
  --taiyi-text-lg: 32px;
  --taiyi-text-xl: 48px;
  --taiyi-text-2xl: 72px;
}
```

### 间距系统（4px 基准）

```css
:root {
  --taiyi-spacing-1: 4px;
  --taiyi-spacing-2: 8px;
  --taiyi-spacing-3: 16px;
  --taiyi-spacing-4: 24px;
  --taiyi-spacing-5: 32px;
  --taiyi-spacing-6: 48px;
  --taiyi-spacing-8: 64px;
}
```

### 圆角系统

```css
:root {
  --taiyi-radius-sm: 8px;    /* 小圆角 */
  --taiyi-radius-md: 12px;   /* 中圆角 */
  --taiyi-radius-lg: 20px;   /* 大圆角 */
  --taiyi-radius-xl: 32px;   /* 超大圆角 */
  --taiyi-radius-full: 9999px; /* 圆形 */
}
```

### 阴影系统（轻量化）

```css
:root {
  --taiyi-shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --taiyi-shadow-md: 0 4px 8px rgba(0,0,0,0.1);
  --taiyi-shadow-lg: 0 8px 16px rgba(0,0,0,0.15);
  --taiyi-shadow-xl: 0 12px 24px rgba(0,0,0,0.2);
}
```

### 动画系统

```css
:root {
  --taiyi-transition-fast: 200ms ease-out;
  --taiyi-transition-base: 300ms ease-out;
  --taiyi-transition-slow: 500ms ease-out;
}
```

---

## 🎯 设计原则

### Apple 三原则（主导 80%）

| 原则 | Apple 定义 | 太一诠释 |
|------|-----------|---------|
| **Deference** | 内容优先，UI 退后 | 信息密度 > 装饰元素 |
| **Clarity** | 清晰易懂，无歧义 | 废话=不输出 |
| **Depth** | 层次感，视觉深度 | 功能美学，美服务于用 |

### 东方哲学（15%）

| 概念 | 来源 | 设计应用 |
|------|------|---------|
| **间 (Ma)** | 日本 | 留白的艺术 |
| **侘寂 (Wabi-Sabi)** | 日本 | 不完美之美 |
| **渋い (Shibui)** | 日本 | 低调的优雅 |

### 中国美学（5%）

| 概念 | 来源 | 设计应用 |
|------|------|---------|
| **天青** | 宋瓷 | 雨过天青云破处 |
| **留白** | 国画 | 计白当黑 |
| **气韵** | 书法 | 生动流畅 |

---

## 📋 设计审查清单

### 自动审查（AI 执行）

- [ ] 配色是否符合太一规范
- [ ] 字体大小是否遵循 1.5 倍率
- [ ] 间距是否为 4px 倍数
- [ ] 圆角是否符合规范
- [ ] 阴影是否适度（轻量化）
- [ ] 动画时长是否 200-300ms
- [ ] 苹果设计是否主导（80%）
- [ ] 东方元素是否适度（15%）
- [ ] 中国元素是否点睛（5%）

### 手动审查（SAYELF）

- [ ] 整体视觉是否和谐
- [ ] 是否避免 AI 味设计
- [ ] 是否体现太一风格
- [ ] 功能是否被美学增强

---

## 🛠️ 使用方法

### 方式 1: CSS 变量

```css
.button {
  background: var(--taiyi-primary);
  color: var(--taiyi-text);
  padding: var(--taiyi-spacing-3);
  border-radius: var(--taiyi-radius-md);
  font-size: var(--taiyi-text-base);
}
```

### 方式 2: Tailwind CSS

```jsx
<button className="bg-[#8E8E93] text-[#1D1D1F] px-4 py-3 rounded-lg">
  点击
</button>
```

### 方式 3: 组件库（待创建）

```jsx
import { Button } from '@taiyi/design-system'

<Button variant="primary">点击</Button>
```

---

## 📚 参考资源

### 设计系统集合
- [awesome-design-systems](https://github.com/alexpate/awesome-design-systems) ⭐ 19k+
- [design-systems-repo](https://github.com/alexpate/design-systems-repo)

### 品牌设计
- [Apple Design Resources](https://www.apple.com/design-resources/)
- [Spotify Design](https://spotify.design/)
- [IBM Carbon Design](https://carbondesignsystem.com/)
- [Google Material Design](https://material.io/)
- [Ant Design](https://ant.design/)

### 东方美学
- [日本传统色](https://nipponcolors.com/)
- [中国色](http://zhongguose.com/)
- [传统色](https://github.com/zeroscalers/chinese-colors)

---

## 🔄 与 Taiyi-Artisan 集成

### 美学审核标准

```python
from skills.taiyi_artisan import Artisan

artisan = Artisan()

# 设计审核
review = artisan.review_design(ui_component)
if not review.passed:
    print(f"设计评分：{review.score}")
    print(f"改进建议：{review.suggestions}")
```

### 自动生成

```python
# 生成符合设计规范的 UI
ui = artisan.generate_ui(
    type='card',
    style='taiyi-zen',  # taiyi-apple / taiyi-oriental / taiyi-chinese
    content={'title': '...', 'body': '...'}
)
```

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-13 | 初始融合（Apple 80% + 东方 15% + 中国 5%） |

---

*太一 AGI 设计系统 · Taiyi-Artisan*  
*创建时间：2026-04-13*  
*融合原则：苹果 80% + 东方 15% + 中国 5%*
