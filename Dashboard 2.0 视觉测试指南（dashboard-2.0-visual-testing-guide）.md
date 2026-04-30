# 🎨 Dashboard 2.0 视觉测试指南

> **版本**: v2.0.0  
> **创建时间**: 2026-04-14 23:40  
> **状态**: ✅ 实现完成

---

## 📋 视觉测试概述

**目标**: 检测 UI 回归，确保视觉一致性

**工具**: Playwright + 截图对比

**覆盖率**: 
- Dashboard 页面：100%
- Agents 页面：100%
- Approvals 页面：100%
- 核心组件：90%

---

## 1. 测试文件结构

```
e2e/tests/
├── visual.spec.ts              # Dashboard 视觉测试
├── visual-agents.spec.ts       # Agents 页面视觉测试
├── visual-approvals.spec.ts    # Approvals 页面视觉测试
└── visual-skill*.spec.ts       # Skills 页面视觉测试 (待添加)
```

---

## 2. 测试用例清单

### Dashboard 页面

**已实现**:
```
✅ Dashboard 页面整体布局
✅ 统计卡片截图
✅ Agent 状态卡片截图
✅ 自进化进度组件截图
✅ 实时任务流图表截图
✅ 事件时间线截图
✅ Header 导航栏截图
✅ Sidebar 侧边栏截图
✅ Footer 状态栏截图
```

### Agents 页面

**已实现**:
```
✅ Agents 页面整体布局
✅ Agent 列表表格截图
✅ 搜索和筛选控件截图
✅ 统计卡片截图
```

### Approvals 页面

**已实现**:
```
✅ Approvals 页面整体布局
✅ 审批统计卡片截图
✅ 审批列表表格截图
✅ 审批状态标识截图
```

---

## 3. 运行视觉测试

### 本地运行

```bash
# 运行所有视觉测试
npm run test:visual

# 运行特定测试
npm run test:visual -- --grep "Dashboard"

# 更新基准截图
npm run test:visual -- --update-snapshots
```

### CI/CD 运行

```bash
# 在 CI 环境中运行
npm run test:e2e:visual

# 生成 HTML 报告
npm run test:visual -- --reporter=html
```

---

## 4. 截图存储

**基准截图位置**:
```
e2e/tests/__snapshots__/
├── visual/
│   ├── dashboard-full.png
│   ├── dashboard-stats.png
│   ├── agent-card-sample.png
│   ├── evolution-progress.png
│   ├── realtime-chart.png
│   ├── timeline.png
│   ├── header.png
│   ├── sidebar.png
│   └── footer.png
├── visual-agents/
│   ├── agents-full.png
│   ├── agents-table.png
│   ├── agents-controls.png
│   └── agents-stats.png
└── visual-approvals/
    ├── approvals-full.png
    ├── approvals-stats.png
    ├── approvals-table.png
    └── approvals-status.png
```

---

## 5. 测试配置

### Playwright 配置

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,
      threshold: 0.2,
    },
  },
})
```

### 截图选项

```typescript
await expect(page).toHaveScreenshot('name.png', {
  fullPage: true,           // 全页面截图
  maxDiffPixels: 100,       // 最大差异像素
  threshold: 0.2,           // 差异阈值
  clip: { x: 0, y: 0, width: 800, height: 600 } // 裁剪区域
})
```

---

## 6. 测试最佳实践

### ✅ 好的实践

```typescript
// 使用描述性名称
await expect(page).toHaveScreenshot('dashboard-stats.png')

// 设置合理的差异阈值
await expect(page).toHaveScreenshot('chart.png', {
  maxDiffPixels: 100
})

// 等待动画完成
await page.waitForTimeout(1000)
await expect(page).toHaveScreenshot('animated.png')
```

### ❌ 避免的做法

```typescript
// 阈值过低导致误报
await expect(page).toHaveScreenshot('page.png', {
  maxDiffPixels: 0  // ❌ 过于严格
})

// 没有等待加载完成
await expect(page).toHaveScreenshot('loading.png')  // ❌ 可能捕获加载状态
```

---

## 7. 处理动态内容

### 时间戳处理

```typescript
// 隐藏动态时间戳
await page.evaluate(() => {
  document.querySelector('.timestamp')?.setAttribute('data-test-id', 'static-time')
})
```

### 动画处理

```typescript
// 禁用动画
await page.addStyleTag({
  content: `
    *, *::before, *::after {
      animation: none !important;
      transition: none !important;
    }
  `
})
```

### 随机数据

```typescript
// 使用 Mock 数据
await page.route('**/api/*', route => {
  route.fulfill({ json: mockData })
})
```

---

## 8. 测试维护

### 更新基准截图

**何时更新**:
```
✅ UI 设计变更
✅ 组件重构
✅ 样式调整
✅ 新增功能
```

**更新流程**:
```bash
# 1. 运行测试识别失败
npm run test:visual

# 2. 审查差异
open playwright-report/index.html

# 3. 更新基准截图
npm run test:visual -- --update-snapshots

# 4. 提交更改
git add e2e/tests/__snapshots__/
git commit -m "更新视觉测试基准截图"
```

### 清理过时截图

```bash
# 查找未使用的截图
find e2e/tests/__snapshots__ -name "*.png" | while read file; do
  if ! grep -q "$(basename $file)" e2e/tests/*.spec.ts; then
    echo "未使用：$file"
  fi
done
```

---

## 9. 测试报告

### HTML 报告

**生成命令**:
```bash
npm run test:visual -- --reporter=html
```

**报告内容**:
```
✅ 测试通过/失败状态
✅ 截图对比 (基准 vs 当前)
✅ 差异高亮显示
✅ 测试执行时间
```

### CI/CD 集成

```yaml
# .github/workflows/visual-tests.yml
visual-tests:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Install dependencies
      run: npm ci
    - name: Install Playwright
      run: npx playwright install --with-deps
    - name: Run visual tests
      run: npm run test:visual
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: visual-report
        path: playwright-report/
```

---

## 10. 性能优化

### 并行执行

```bash
# 并行运行测试
npm run test:visual -- --workers=4
```

### 选择性运行

```bash
# 只运行失败的测试
npm run test:visual -- --last-failed

# 只运行特定浏览器
npm run test:visual -- --project=chromium
```

### 缓存优化

```bash
# 使用缓存
npm run test:visual -- --grep-invert "changed"
```

---

## 11. 常见问题

### Q: 测试失败但 UI 正常？

**A**: 可能是动态内容导致，使用以下方法:
```typescript
// 1. 等待网络空闲
await page.waitForLoadState('networkidle')

// 2. 隐藏动态元素
await page.locator('.dynamic').evaluate(el => el.style.visibility = 'hidden')

// 3. 更新基准截图
npm run test:visual -- --update-snapshots
```

### Q: 截图差异过大？

**A**: 调整阈值:
```typescript
await expect(page).toHaveScreenshot('page.png', {
  maxDiffPixels: 200,  // 增加容差
  threshold: 0.3       // 提高阈值
})
```

### Q: 测试执行太慢？

**A**: 优化策略:
```bash
# 1. 减少截图数量
# 2. 降低截图分辨率
# 3. 并行执行
npm run test:visual -- --workers=8
```

---

## 12. 测试覆盖率

### 页面覆盖率

```
✅ Dashboard: 9/9 组件 (100%)
✅ Agents: 4/4 组件 (100%)
✅ Approvals: 4/4 组件 (100%)
✅ Skills: 0/4 组件 (0%) ⏳
⏳ Tasks: 待实现
⏳ Audit: 待实现
```

### 组件覆盖率

```
✅ Layout 组件: Header, Sidebar, Footer
✅ Dashboard 组件：统计卡片，Agent 卡片，图表，时间线，进度
✅ Agents 组件：列表表格，搜索筛选，统计
✅ Approvals 组件：统计卡片，列表表格，状态标识
```

---

*Dashboard 2.0 视觉测试指南 · 太一 AGI · 2026-04-14 23:40*

**✅ 视觉测试实现完成！**
