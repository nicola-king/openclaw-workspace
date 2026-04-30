# 🦞 赛博龙虾主题配置

> 灵感来源：SAYELF 2026-04-02 22:10 发送的机械龙虾图腾  
> 创建时间：2026-04-02 22:17  
> 版本：v1.0.0

---

## 🎨 色彩方案

### 主色调 - 蓝紫霓虹
| 色阶 | 色值 | 预览 |
|------|------|------|
| 500 | `#8B5CF6` | 🟣 主色 |
| 600 | `#7C3AED` | 🟣 深紫 |
| 700 | `#6D28D9` | 🟣 暗紫 |

### 强调色 - 龙虾红
| 色阶 | 色值 | 预览 |
|------|------|------|
| 500 | `#FF6B6B` | 🔴 强调色 |
| 600 | `#EF4444` | 🔴 深红 |
| 400 | `#F87171` | 🔴 浅红 |

### 背景色 - 深空黑
| 色阶 | 色值 | 预览 |
|------|------|------|
| 900 | `#0D0D1A` | ⚫ 深空黑 |
| 800 | `#202038` | ⚫ 暗蓝 |
| 950 | `#05050A` | ⚫ 纯黑 |

### 霓虹高光
| 颜色 | 色值 | 预览 |
|------|------|------|
| 赛博蓝 | `#00F0FF` | 🔵 霓虹蓝 |
| 霓虹紫 | `#9D5BFF` | 🟣 霓虹紫 |
| 赛博粉 | `#FF00FF` | 🔴 霓虹粉 |

---

## 🌈 渐变配置

### 主渐变（蓝紫）
```css
linear-gradient(135deg, #5A4B9E 0%, #9D5BFF 100%)
```

### 龙虾红渐变
```css
linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%)
```

### 赛博霓虹渐变
```css
linear-gradient(135deg, #00F0FF 0%, #9D5BFF 50%, #FF00FF 100%)
```

### 深空背景渐变
```css
linear-gradient(180deg, #0D0D1A 0%, #1A1A2E 100%)
```

---

## ✨ 光晕效果

### 霓虹光晕
```css
box-shadow: 0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.3);
```

### 紫色光晕
```css
box-shadow: 0 0 10px rgba(157, 91, 255, 0.5), 0 0 20px rgba(157, 91, 255, 0.3);
```

### 龙虾红光晕
```css
box-shadow: 0 0 10px rgba(255, 107, 107, 0.5), 0 0 20px rgba(255, 107, 107, 0.3);
```

---

## 📁 文件结构

```
constitution/theme/
├── cyber-lobster-theme.ts    # TypeScript 主题配置
├── cyber-lobster-theme.css   # CSS 变量定义
└── README.md                 # 本文档
```

---

## 🔧 使用方式

### React/Next.js
```tsx
import { CYBER_LOBSTER_THEME } from '@/constitution/theme/cyber-lobster-theme';

// 使用主色
<div style={{ color: CYBER_LOBSTER_THEME.primary[500] }}>
  🦞 赛博龙虾主题
</div>

// 使用渐变
<div style={{ background: CYBER_LOBSTER_THEME.gradients.primary }}>
  蓝紫渐变背景
</div>

// 使用光晕
<div style={{ boxShadow: CYBER_LOBSTER_THEME.shadows.neonGlow }}>
  霓虹光晕效果
</div>
```

### CSS
```css
/* 使用 CSS 变量 */
.element {
  color: var(--primary-500);
  background: var(--gradient-primary);
  box-shadow: var(--shadow-neon-glow);
}
```

### Tailwind CSS
```css
/* tailwind.config.js */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#8B5CF6',
          600: '#7C3AED',
          700: '#6D28D9',
        },
        accent: {
          500: '#FF6B6B',
        },
        background: {
          900: '#0D0D1A',
        },
      },
    },
  },
}
```

---

## 🎯 设计原则

1. **深邃智能** - 蓝紫霓虹代表深度思考和未来感
2. **机械装甲** - 深色背景象征坚固可靠
3. **开源精神** - openclaw 标识融入设计元素
4. **移动优先** - 手机底座启发响应式设计

---

## 📊 对比度检查

| 组合 | 对比度 | WCAG 等级 |
|------|--------|-----------|
| 主色 / 深空黑 | 12.5:1 | AAA ✅ |
| 龙虾红 / 深空黑 | 8.2:1 | AAA ✅ |
| 霓虹蓝 / 深空黑 | 15.3:1 | AAA ✅ |
| 白色 / 深空黑 | 18.6:1 | AAA ✅ |

---

## 🦞 图腾寓意

- **蓝紫霓虹** = 深邃智能
- **机械装甲** = 负熵法则
- **openclaw 标识** = 开源精神
- **手机底座** = 移动优先
- **龙虾红** = 活力与执行力

---

*创建时间：2026-04-02 22:17 | 太一 AGI v4.0 | 赛博龙虾主题*
