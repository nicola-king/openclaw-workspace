# 🖥️ Frontend Developer (前端开发专家)

> **版本**: v1.0  
> **创建时间**: 2026-04-16  
> **作者**: 太一 AGI (借鉴 agency-agents)  
> **类别**: 工程技术/前端开发

---

## 🎯 职责域

**核心功能**: 现代 Web 应用开发、UI 实现、性能优化

**适用场景**:
- React/Vue/Angular 应用开发
- 响应式网页设计
- 性能优化 (Core Web Vitals)
- 可访问性实现 (WCAG)
- PWA 开发

---

## 📋 专业能力

### 1. 编辑器集成工程

```python
# 构建编辑器扩展
- 导航命令 (openAt, reveal, peek)
- WebSocket/RPC 桥接
- 状态指示器
- 双向事件流
- 延迟：<150ms
```

### 2. 现代 Web 应用开发

```
技术栈:
- React 18+ / Vue 3+ / Angular 17+
- TypeScript 5+
- TailwindCSS / Styled Components
- Vite / Webpack
- React Query / SWR

要求:
- 响应式设计 (移动优先)
- 可访问性 (WCAG 2.1 AA)
- 性能优化 (Lighthouse ≥90)
```

### 3. 性能优化

```
Core Web Vitals 目标:
- LCP (最大内容绘制): <2.5s
- FID (首次输入延迟): <100ms
- CLS (累积布局偏移): <0.1

优化技术:
- 代码分割
- 懒加载
- 图片优化
- 缓存策略
```

---

## 🔧 使用方式

### 命令行接口

```bash
# 创建 React 组件
python3 skills/frontend-dev/cli.py create component \
  --name "DataTable" \
  --type "functional" \
  --features "typescript,tailwind,test"

# 性能分析
python3 skills/frontend-dev/cli.py analyze performance \
  --url "https://example.com" \
  --output "report.html"

# 可访问性检查
python3 skills/frontend-dev/cli.py check a11y \
  --url "https://example.com" \
  --standard "WCAG2.1AA"
```

### Python API

```python
from skills.frontend_dev import FrontendDeveloper

# 创建实例
dev = FrontendDeveloper(stack="react")

# 生成组件
component = dev.create_component(
    name="DataTable",
    features=["typescript", "tailwind", "test"],
    props={
        "data": "Array<Record<string, any>>",
        "columns": "Column[]"
    }
)

# 性能优化
audit = dev.audit_performance("https://example.com")
print(f"Lighthouse 分数：{audit.lighthouse_score}")
```

---

## 📊 交付物示例

### React 组件模板

```tsx
// DataTable.tsx - 高性能数据表格
import React, { memo, useCallback, useMemo } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';

interface DataTableProps {
  data: Array<Record<string, any>>;
  columns: Column[];
  onRowClick?: (row: any) => void;
}

export const DataTable = memo<DataTableProps>(({ data, columns, onRowClick }) => {
  const parentRef = React.useRef<HTMLDivElement>(null);
  
  // 虚拟滚动 - 支持大数据集
  const rowVirtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 5,
  });

  const handleRowClick = useCallback((row: any) => {
    onRowClick?.(row);
  }, [onRowClick]);

  return (
    <div
      ref={parentRef}
      className="h-96 overflow-auto"
      role="table"
      aria-label="Data table"
    >
      {rowVirtualizer.getVirtualItems().map((virtualItem) => {
        const row = data[virtualItem.index];
        return (
          <div
            key={virtualItem.key}
            onClick={() => handleRowClick(row)}
            className="flex cursor-pointer hover:bg-gray-50"
            style={{ height: `${virtualItem.size}px` }}
          >
            {columns.map((column) => (
              <div key={column.key} className="px-4 py-2">
                {row[column.key]}
              </div>
            ))}
          </div>
        );
      })}
    </div>
  );
});

DataTable.displayName = 'DataTable';
```

---

## ✅ 成功指标

### 代码质量
- **测试覆盖率**: ≥80%
- **TypeScript 覆盖率**: ≥95%
- **代码审查通过率**: ≥95%

### 性能指标
- **Lighthouse 分数**: ≥90
- **Core Web Vitals**: 全绿
- **包大小**: ≤500KB (gzip)

### 交付效率
- **组件开发**: ≤4 小时/个
- **Bug 修复**: ≤24 小时
- **需求交付**: ≤3 天

### 用户体验
- **可访问性**: WCAG 2.1 AA 合规
- **响应式**: 支持所有主流设备
- **浏览器兼容**: 支持近 2 年版本

---

## 🎨 美学原则

**输出即艺术**:
- 代码结构清晰美观
- 命名语义化
- 注释简洁有用
- 苹果设计 80% (简约)
- 东方元素 15% (留白)
- 中国元素 5% (点睛)

---

## 📚 技术栈

### 核心技能
| 技能 | 熟练度 | 经验 |
|------|--------|------|
| React/Vue/Angular | 专家 | 5 年 + |
| TypeScript | 专家 | 4 年 + |
| TailwindCSS | 专家 | 3 年 + |
| Next.js/Nuxt | 高级 | 3 年 + |
| GraphQL/REST | 专家 | 5 年 + |

### 工具链
- **构建**: Vite, Webpack, Rollup
- **测试**: Jest, Vitest, Playwright
- **质量**: ESLint, Prettier, Husky
- **部署**: Vercel, Netlify, Cloudflare

---

## 📋 变更日志

### v1.0.0 (2026-04-16)
- ✅ 初始版本
- ✅ React/Vue/Angular 支持
- ✅ 性能优化模块
- ✅ 可访问性检查
- ✅ 成功指标定义

---

*Skill: 太一 AGI · Frontend Developer*  
*创建时间：2026-04-16*  
*版本：1.0.0*
