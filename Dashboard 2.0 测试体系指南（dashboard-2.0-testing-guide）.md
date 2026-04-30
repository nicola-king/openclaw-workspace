# 🧪 Dashboard 2.0 测试体系文档

> **版本**: v2.0.0  
> **创建时间**: 2026-04-14 23:30  
> **状态**: ✅ 设计完成

---

## 📋 测试架构

### 测试金字塔

```
        /\
       /  \      E2E 测试 (10%)
      /----\     - Playwright
     /      \    - 关键用户流程
    /--------\
   /          \   集成测试 (20%)
  /------------\  - 组件测试
 /              \ - API 测试
/----------------\
单元测试 (70%)     - 函数测试
- 工具函数        - 钩子测试
- 组件逻辑
```

---

## 1. 单元测试

### 框架配置

**工具**: Vitest  
**环境**: jsdom  
**覆盖率目标**: >80%

**配置**:
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      threshold: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      }
    }
  }
})
```

### 测试文件

**已创建**:
```
✅ src/components/Dashboard/AgentCard.test.tsx
✅ src/components/Layout/Header.test.tsx
✅ src/components/Visualization/Timeline.test.tsx
```

**待创建**:
```
⏳ src/components/Layout/Sidebar.test.tsx
⏳ src/components/Layout/Footer.test.tsx
⏳ src/components/Visualization/RealtimeChart.test.tsx
⏳ src/components/Visualization/EvolutionProgress.test.tsx
⏳ src/pages/Dashboard.test.tsx
⏳ src/hooks/*.test.ts
⏳ src/utils/*.test.ts
```

### 运行测试

```bash
# 运行所有单元测试
npm test

# 运行单个测试文件
npm test -- AgentCard.test.tsx

# 运行测试并生成覆盖率报告
npm run test:coverage

# 打开测试 UI
npm run test:ui
```

---

## 2. E2E 测试

### 框架配置

**工具**: Playwright  
**浏览器**: Chromium, Firefox, WebKit  
**覆盖流程**: 关键用户流程

**配置**:
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e/tests',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
})
```

### 测试文件

**已创建**:
```
✅ e2e/tests/dashboard.spec.ts
```

**待创建**:
```
⏳ e2e/tests/agents.spec.ts
⏳ e2e/tests/skills.spec.ts
⏳ e2e/tests/tasks.spec.ts
⏳ e2e/tests/approvals.spec.ts
⏳ e2e/tests/audit.spec.ts
```

### 运行测试

```bash
# 运行所有 E2E 测试
npm run test:e2e

# 运行特定浏览器测试
npm run test:e2e -- --project=chromium

# 生成 HTML 报告
npm run test:e2e -- --reporter=html
```

---

## 3. 视觉测试

### 框架配置

**工具**: Playwright + 截图对比  
**目标**: 检测 UI 回归

**测试示例**:
```typescript
// e2e/tests/visual.spec.ts
import { test, expect } from '@playwright/test'

test.describe('视觉回归测试', () => {
  test('Dashboard 页面截图', async ({ page }) => {
    await page.goto('http://localhost:3000')
    await expect(page).toHaveScreenshot('dashboard.png', {
      fullPage: true,
      maxDiffPixels: 100
    })
  })

  test('Agent 卡片截图', async ({ page }) => {
    await page.goto('http://localhost:3000')
    const agentCard = page.locator('[data-testid="agent-card"]').first()
    await expect(agentCard).toHaveScreenshot('agent-card.png')
  })
})
```

### 运行测试

```bash
# 运行视觉测试
npm run test:visual

# 更新基准截图
npm run test:visual -- --update-snapshots
```

---

## 4. 性能测试

### 工具配置

**工具**: Lighthouse  
**目标**:
```
✅ 首屏加载 < 2 秒
✅ 可交互时间 < 3 秒
✅ Lighthouse 评分 > 90
✅ Core Web Vitals 全部绿色
```

### 测试脚本

```bash
# 运行 Lighthouse
lighthouse http://localhost:3000 --output html --output-path ./reports/performance.html

# 批量测试
lighthouse http://localhost:3000 --output json --output-path ./reports/lighthouse.json
```

### 性能指标

**Core Web Vitals**:
```
✅ Largest Contentful Paint (LCP) < 2.5s
✅ First Input Delay (FID) < 100ms
✅ Cumulative Layout Shift (CLS) < 0.1
```

---

## 5. 安全测试

### 工具配置

**工具**:
```
✅ npm audit - 依赖漏洞扫描
✅ ESLint security - 代码规范检查
```

**CI/CD 集成**:
```yaml
# .github/workflows/security.yml
security-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: npm audit
      run: npm audit --audit-level=moderate
```

### 运行测试

```bash
# 依赖漏洞扫描
npm audit

# 自动修复
npm audit fix

# 强制修复 (可能破坏)
npm audit fix --force
```

---

## 6. CI/CD 集成

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: npm ci
        working-directory: ./frontend
      
      - name: Run unit tests
        run: npm test -- --coverage
        working-directory: ./frontend
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json
      
      - name: Install Playwright
        run: npx playwright install --with-deps
        working-directory: ./frontend
      
      - name: Run E2E tests
        run: npm run test:e2e
        working-directory: ./frontend
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

---

## 7. 测试覆盖率

### 覆盖率报告

**生成命令**:
```bash
npm run test:coverage
```

**报告位置**:
```
frontend/coverage/
├── index.html          # HTML 报告
├── coverage-final.json # JSON 报告
└── lcov.info           # LCOV 格式
```

### 覆盖率目标

```
✅ Lines: >80%
✅ Functions: >80%
✅ Branches: >80%
✅ Statements: >80%
```

### 覆盖率检查

**CI 检查**:
```yaml
- name: Check coverage
  run: |
    coverage=$(cat coverage/coverage-final.json | jq '.total.lines.pct')
    if (( $(echo "$coverage < 80" | bc -l) )); then
      echo "Coverage $coverage% is below 80%"
      exit 1
    fi
```

---

## 8. 测试最佳实践

### 单元测试

```typescript
// ✅ 好的测试
it('显示正确状态', () => {
  render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
  expect(screen.getByText('运行中')).toBeInTheDocument()
})

// ❌ 坏的测试
it('测试组件', () => {
  // 测试名称不明确
  // 没有断言
})
```

### E2E 测试

```typescript
// ✅ 好的测试
test('导航到 Agent 页面', async ({ page }) => {
  await page.getByText('Agent').click()
  await expect(page).toHaveURL('http://localhost:3000/agents')
})

// ❌ 坏的测试
test('点击测试', async ({ page }) => {
  // 没有明确的用户场景
  // 没有验证结果
})
```

### 测试数据

```typescript
// ✅ 好的测试数据
const mockAgents = [
  { id: 'taiyi', name: '太一', status: 'running', tasks: 12, health: 98 },
  { id: 'zhiji', name: '知几', status: 'running', tasks: 8, health: 95 },
]

// ❌ 坏的测试数据
const data = [{ id: 1, name: 'test' }] // 不真实
```

---

## 9. 测试维护

### 测试更新

**何时更新**:
```
✅ 功能变更时
✅ UI 重构时
✅ Bug 修复后
✅ 性能优化后
```

**更新流程**:
```
1. 运行测试套件
2. 识别失败测试
3. 分析失败原因
4. 更新测试或代码
5. 重新运行测试
6. 提交更改
```

### 测试清理

**定期清理**:
```
✅ 删除过时测试
✅ 合并重复测试
✅ 优化慢测试
✅ 更新测试数据
```

---

## 10. 测试指标

### 质量指标

```
✅ 测试覆盖率：>80%
✅ 测试通过率：100%
✅ 测试执行时间：<5 分钟
✅ 测试稳定性：>99%
```

### 过程指标

```
✅ 测试编写时间：< 开发时间 30%
✅ Bug 检出率：>90%
✅ 回归测试覆盖率：100%
```

---

*Dashboard 2.0 测试体系文档 · 太一 AGI · 2026-04-14 23:30*

**✅ 测试体系设计完成！开始实施！**
