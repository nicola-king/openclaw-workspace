# 太一 AGI 设计规范系统

> **创建时间**: 2026-04-10  
> **灵感来源**: alexpate/awesome-design-systems  
> **GitHub**: https://github.com/alexpate/awesome-design-systems (19k+ stars)  
> **融合原则**: 苹果 80% + 东方 15% + 中国 5%

---

## 🎯 核心设计理念

### 1. 设计下限保障

**目标**: 几乎很难再出 AI 味的前端

**方法**:
- ✅ 参考顶级品牌设计规范
- ✅ 建立太一专属设计系统
- ✅ AI 自动生成符合规范

---

## 🎨 品牌设计规范参考

### 苹果设计 (Apple Design) - 80%

**核心原则**:
```
- 简约是终极的复杂
- 形式追随功能
- 克制即优雅
- 一致性和谐
```

**配色系统**:
| 颜色 | 色值 | 用途 |
|------|------|------|
| 苹果灰 | #8E8E93 | 次要文字 |
| 苹果白 | #FFFFFF | 背景色 |
| 苹果银 | #C0C0C0 | 边框/分隔 |
| 苹果黑 | #1D1D1F | 主要文字 |
| 苹果蓝 | #007AFF | 强调/链接 |

**字体系统**:
```
- 主字体：SF Pro Display (英文) / 苹方 (中文)
- 代码字体：SF Mono / JetBrains Mono
- 字号比例：8/12/16/24/32/48 (1.5 倍率)
```

**组件规范**:
```
- 圆角：8px (小) / 12px (中) / 20px (大)
- 阴影：0 2px 8px rgba(0,0,0,0.1)
- 间距：4/8/16/24/32px (4px 基准)
- 动画：200-300ms ease-out
```

---

### Spotify 设计 - 借鉴

**核心特点**:
```
- 大胆用色 (品牌绿 #1DB954)
- 圆形元素 (播放按钮)
- 卡片式布局
- 渐变背景
```

**配色参考**:
| 颜色 | 色值 | 用途 |
|------|------|------|
| Spotify 绿 | #1DB954 | 强调色 |
| 深空黑 | #191414 | 深色背景 |
| 纯白 | #FFFFFF | 浅色文字 |

---

### IBM 设计 (Carbon Design) - 借鉴

**核心特点**:
```
- 网格系统 (12 列网格)
- 组件库完整
- 企业级规范
- 可访问性强
```

**设计令牌**:
```
- 色彩令牌：--cds-text-primary, --cds-background
- 间距令牌：--cds-spacing-01 (4px), --cds-spacing-02 (8px)
- 字体令牌：--cds-font-family, --cds-font-size-01
```

---

## 🇨🇳 东方设计元素 - 15%

### 日本设计 (禅意/侘寂)

**核心原则**:
```
- 间 (Ma): 留白的艺术
- 侘寂 (Wabi-Sabi): 不完美之美
- 渋い (Shibui): 低调的优雅
```

**配色参考**:
| 颜色 | 色值 | 意境 |
|------|------|------|
| 樱花粉 | #FFB7C5 | 春日浪漫 |
| 抹茶绿 | #7D8447 | 宁静致远 |
| 靛蓝 | #1E3A5F | 深邃优雅 |
| 侘寂色 | #8B7355 | 朴素自然 |

---

### 台湾/香港/新加坡设计

**核心特点**:
```
- 街头文化活力
- 霓虹色彩
- 多元融合
- 现代都市感
```

---

## 🇨🇳 中国经典设计 - 5%

### 传统色彩

| 颜色 | 色值 | 朝代 | 意境 |
|------|------|------|------|
| 天青 | #87CEEB | 宋 | 雨过天青云破处 |
| 朱砂 | #E60000 | 汉 | 热烈吉祥 |
| 黛蓝 | #4A5C8C | 唐 | 深邃沉静 |
| 月白 | #D6ECF0 | 明 | 洁净素雅 |
| 墨色 | #2C2C2C | 先秦 | 深邃内敛 |

### 传统纹样

```
- 云纹 ☁️ - 高升如意 (章节分隔)
- 莲花 🪷 - 清廉高洁 (文人主题)
- 竹子 🎋 - 气节高尚 (品格主题)
- 山峦 ⛰️ - 稳重厚实 (结尾装饰)
```

---

## 🎯 太一设计系统实施

### 1. 色彩系统

```css
:root {
  /* 主色调 - 苹果 80% */
  --taiyi-primary: #8E8E93;
  --taiyi-background: #FFFFFF;
  --taiyi-text: #1D1D1F;
  --taiyi-accent: #007AFF;
  
  /* 东方元素 15% */
  --taiyi-zen: #7D8447;
  --taiyi-sakura: #FFB7C5;
  
  /* 中国元素 5% */
  --taiyi-skyblue: #87CEEB;
  --taiyi-ink: #2C2C2C;
}
```

### 2. 字体系统

```css
:root {
  /* 主字体 */
  --taiyi-font-primary: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  
  /* 代码字体 */
  --taiyi-font-mono: "SF Mono", "JetBrains Mono", "Fira Code", monospace;
  
  /* 字号系统 (1.5 倍率) */
  --taiyi-text-xs: 12px;
  --taiyi-text-sm: 16px;
  --taiyi-text-base: 24px;
  --taiyi-text-lg: 32px;
  --taiyi-text-xl: 48px;
}
```

### 3. 间距系统

```css
:root {
  /* 4px 基准 */
  --taiyi-spacing-1: 4px;
  --taiyi-spacing-2: 8px;
  --taiyi-spacing-3: 16px;
  --taiyi-spacing-4: 24px;
  --taiyi-spacing-5: 32px;
  --taiyi-spacing-6: 48px;
}
```

### 4. 圆角系统

```css
:root {
  --taiyi-radius-sm: 8px;
  --taiyi-radius-md: 12px;
  --taiyi-radius-lg: 20px;
  --taiyi-radius-full: 9999px;
}
```

### 5. 阴影系统

```css
:root {
  --taiyi-shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --taiyi-shadow-md: 0 4px 8px rgba(0,0,0,0.1);
  --taiyi-shadow-lg: 0 8px 16px rgba(0,0,0,0.15);
}
```

---

## 🎨 组件设计规范

### 按钮组件

```jsx
// 主按钮 - 苹果风格
<button className="bg-[#007AFF] text-white px-6 py-3 rounded-lg hover:bg-[#0056CC] transition">
  主要操作
</button>

// 次要按钮
<button className="bg-gray-100 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-200 transition">
  取消
</button>

// 危险按钮
<button className="bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 transition">
  删除
</button>
```

### 卡片组件

```jsx
<div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
  <h3 className="text-xl font-bold text-gray-800 mb-4">卡片标题</h3>
  <p className="text-gray-600">卡片内容...</p>
</div>
```

### 输入框组件

```jsx
<input 
  type="text" 
  className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-[#007AFF] focus:border-transparent"
  placeholder="请输入..."
/>
```

---

## 📋 设计审查清单

### 自动审查 (AI 执行)

- [ ] 配色是否符合太一规范
- [ ] 字体大小是否遵循 1.5 倍率
- [ ] 间距是否为 4px 倍数
- [ ] 圆角是否符合规范
- [ ] 阴影是否适度
- [ ] 动画时长是否 200-300ms
- [ ] 是否避免 AI 味设计

### 手动审查 (SAYELF)

- [ ] 整体视觉是否和谐
- [ ] 东方元素是否适度 (15%)
- [ ] 中国元素是否点睛 (5%)
- [ ] 苹果设计是否主导 (80%)

---

## 🛠️ 使用方法

### 方式 1: AI 自动生成

```
让 AI 参考这份设计规范生成前端代码
```

### 方式 2: 组件库调用

```jsx
import { Button, Card, Input } from '@taiyi/design-system'

<Button variant="primary">点击</Button>
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

## 📚 参考资源

### 设计规范

- [Apple Design Resources](https://www.apple.com/design-resources/)
- [Spotify Design](https://spotify.design/)
- [IBM Carbon Design](https://carbondesignsystem.com/)
- [Google Material Design](https://material.io/)

### 设计系统集合

- [awesome-design-systems](https://github.com/alexpate/awesome-design-systems) ⭐ 19k+
- [design-systems-repo](https://github.com/alexpate/design-systems-repo)

### 中国传统色彩

- [中国色](http://zhongguose.com/)
- [传统色](https://github.com/zeroscalers/chinese-colors)

---

## 🎯 持续更新

**每周审查**:
- 新增设计规范
- 优化现有规范
- 收集设计反馈

**每月更新**:
- 更新配色系统
- 新增组件规范
- 优化设计令牌

---

*太一 AGI 设计规范系统 v1.0*  
*创建时间：2026-04-10*  
*融合原则：苹果 80% + 东方 15% + 中国 5%*
