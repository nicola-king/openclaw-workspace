# 🎨 Dashboard 2.0 详细设计文档

> **版本**: v2.0.0  
> **创建时间**: 2026-04-14 23:05  
> **更新时间**: 2026-04-14 23:25  
> **状态**: ✅ 设计完成

---

## 📋 执行摘要

**本报告包含**:
1. Dashboard 2.0 详细设计
2. 融合方案细化 (OpenMCT + Mission Control)
3. 测试体系详细设计
4. 实施路线图

---

## 1. Dashboard 2.0 详细设计

### 1.1 架构设计

**技术栈**:
```
前端:
- React 18.3.1
- TypeScript 5.3.3
- Tailwind CSS 3.4.1
- Recharts 2.12.0 (图表)
- @xyflow/react 12.0.0 (流程图)
- Axios 1.6.7 (HTTP 客户端)
- React Router 6.22.0 (路由)

后端:
- Node.js 22+
- Express 4.18.2
- WebSocket (ws 8.16.0)
- SQL.js 1.10.3 (数据库)
- TypeScript 5.3.3

部署:
- Docker 20+
- Docker Compose v2
- Nginx (反向代理)
```

**组件架构**:
```
Dashboard 2.0
├── 布局系统 (Layout)
│   ├── Header - 全局导航栏
│   ├── Sidebar - 侧边菜单
│   ├── Footer - 状态栏
│   └── Main - 主内容区
├── 仪表盘模块 (Dashboard)
│   ├── AgentCard - Agent 状态卡片
│   ├── SkillChart - Skill 统计图
│   ├── TaskProgress - 任务进度条
│   └── SystemHealth - 系统健康度
├── 可视化模块 (Visualization)
│   ├── RealtimeChart - 实时数据流
│   ├── Timeline - 事件时间线
│   ├── EvolutionProgress - 自进化进度
│   └── NetworkTopology - 网络拓扑图
├── 管理模块 (Management)
│   ├── AgentManager - Agent 管理
│   ├── SkillManager - Skill 管理
│   ├── ApprovalQueue - 审批队列
│   └── GatewayManager - 网关管理
└── 审计模块 (Audit)
    ├── OperationLogs - 操作日志
    ├── DecisionTrail - 决策追踪
    └── EventTimeline - 事件时间线
```

### 1.2 配色方案

**太一主题色**:
```css
主色调:
- 太一蓝：#1E88E5
- 科技蓝：#0D47A1
- 成功绿：#43A047
- 警告黄：#FFB300
- 错误红：#E53935

背景色:
- 深色背景：#1A1A2E
- 卡片背景：#16213E
- 边框色：#0F3460

文字色:
- 主文字：#FFFFFF
- 次文字：#B0B0B0
- 链接色：#64B5F6
```

### 1.3 响应式布局

**断点设计**:
```css
sm: 640px   (手机横屏)
md: 768px   (平板)
lg: 1024px  (桌面)
xl: 1280px  (大桌面)
2xl: 1536px (超大桌面)
```

**网格系统**:
```
手机 (sm):   1 列
平板 (md):   2 列
桌面 (lg):   4 列
```

---

## 2. 融合方案细化

### 2.1 NASA OpenMCT 融合

**借鉴点**:
```
1. 数据可视化框架
   - 实时数据流展示
   - 历史数据图表
   - 时间线组件
   - 仪表盘定制

2. 插件化架构
   - 可插拔设计
   - 独立功能单元
   - 统一 API 接口

3. 测试体系
   - 单元测试 (Jasmine)
   - E2E 测试 (Playwright)
   - 视觉测试
   - 性能测试
   - 安全测试 (CodeQL)
```

**融合实现**:
```
✅ 实时数据流图表 → Recharts 实现
✅ 时间线组件 → Timeline 组件
✅ 仪表盘定制 → Dashboard 页面
✅ 插件化 → React 组件系统
✅ 测试体系 → Vitest + Playwright
```

### 2.2 OpenClaw Mission Control 融合

**借鉴点**:
```
1. 运营界面设计
   - 统一运营界面
   - 多团队管理
   - 活动可见性
   - 审计追踪

2. 审批流程
   - 敏感操作审批
   - 明确审批流
   - 决策追踪

3. 网关管理
   - 网关集成连接
   - 分布式环境操作
   - 远程执行环境
```

**融合实现**:
```
✅ 统一运营界面 → Dashboard 2.0
✅ 多 Agent 管理 → Agent 管理页面
✅ 审批流程 → ApprovalQueue 组件
✅ 网关管理 → GatewayManager 组件
✅ 审计追踪 → Audit 模块
```

### 2.3 太一现有系统融合

**保留特性**:
```
✅ 9 大 Agent 矩阵
✅ 自进化系统 (Level 3, 92%)
✅ 记忆系统 v3.0
✅ 学习循环
✅ 宪法框架
✅ 多通道支持
```

**优化点**:
```
⏳ Dashboard 1.0 → 2.0 升级
⏳ 实时监控增强
⏳ 可视化增强
⏳ 用户体验优化
```

---

## 3. 测试体系详细设计

### 3.1 测试架构

**测试金字塔**:
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

### 3.2 单元测试

**框架**: Vitest
**覆盖率目标**: >80%

**测试文件结构**:
```
src/
├── components/
│   ├── Layout/
│   │   ├── Header.test.tsx
│   │   ├── Sidebar.test.tsx
│   │   └── Footer.test.tsx
│   ├── Dashboard/
│   │   ├── AgentCard.test.tsx
│   │   └── ...
│   └── Visualization/
│       ├── RealtimeChart.test.tsx
│       ├── Timeline.test.tsx
│       └── EvolutionProgress.test.tsx
├── hooks/
│   ├── useAgents.test.ts
│   ├── useSkills.test.ts
│   └── useWebSocket.test.ts
└── utils/
    ├── api.test.ts
    └── helpers.test.ts
```

**测试示例**:
```typescript
// AgentCard.test.tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import AgentCard from './AgentCard'

describe('AgentCard', () => {
  it('渲染 Agent 名称', () => {
    render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
    expect(screen.getByText('太一')).toBeInTheDocument()
  })

  it('显示正确状态', () => {
    render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
    expect(screen.getByText('运行中')).toBeInTheDocument()
  })

  it('显示健康度', () => {
    render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
    expect(screen.getByText('98%')).toBeInTheDocument()
  })
})
```

### 3.3 E2E 测试

**框架**: Playwright
**覆盖流程**: 关键用户流程

**测试文件结构**:
```
e2e/
├── tests/
│   ├── dashboard.spec.ts
│   ├── agents.spec.ts
│   ├── skills.spec.ts
│   ├── approvals.spec.ts
│   └── audit.spec.ts
├── fixtures/
│   └── test-data.ts
└── utils/
    └── helpers.ts
```

**测试示例**:
```typescript
// e2e/tests/dashboard.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Dashboard', () => {
  test('加载仪表盘页面', async ({ page }) => {
    await page.goto('http://localhost:3000')
    
    // 验证统计卡片
    await expect(page.getByText('Agent 数量')).toBeVisible()
    await expect(page.getByText('9')).toBeVisible()
    
    // 验证 Agent 状态卡片
    await expect(page.getByText('太一')).toBeVisible()
    await expect(page.getByText('运行中')).toBeVisible()
    
    // 验证自进化进度
    await expect(page.getByText('Level 3')).toBeVisible()
  })

  test('导航到 Agent 页面', async ({ page }) => {
    await page.goto('http://localhost:3000')
    await page.getByText('Agent').click()
    await expect(page).toHaveURL('http://localhost:3000/agents')
  })
})
```

### 3.4 视觉测试

**框架**: Playwright + Percy/Loki
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

### 3.5 性能测试

**工具**: Lighthouse + WebPageTest
**目标**:
```
✅ 首屏加载 < 2 秒
✅ 可交互时间 < 3 秒
✅ Lighthouse 评分 > 90
✅ Core Web Vitals 全部绿色
```

**测试脚本**:
```bash
# Lighthouse CI
npm run test:performance

# 生成报告
lighthouse http://localhost:3000 --output html --output-path ./reports/performance.html
```

### 3.6 安全测试

**工具**:
```
✅ npm audit - 依赖漏洞扫描
✅ CodeQL - 代码安全分析
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
    - name: CodeQL
      uses: github/codeql-action/analyze@v3
```

---

## 4. 实施路线图

### 阶段 1: 基础架构 (Week 1) ✅

```
Day 1-2: 项目初始化 ✅
- [x] 创建项目结构
- [x] 配置 TypeScript
- [x] 配置 Tailwind CSS
- [x] 配置 Docker

Day 3-4: 布局系统 ✅
- [x] Header 组件
- [x] Sidebar 组件
- [x] Footer 组件
- [x] 响应式布局

Day 5-7: 基础组件 ✅
- [x] AgentCard 组件
- [x] SkillChart 组件
- [x] TaskProgress 组件
- [x] SystemHealth 组件
```

**状态**: ✅ **完成** (2026-04-14 23:20)

### 阶段 2: 可视化模块 (Week 2)

```
Day 8-9: 图表组件
- [ ] RealtimeChart 组件增强
- [ ] WebSocket 实时数据
- [ ] 数据更新逻辑

Day 10-11: 时间线组件
- [ ] Timeline 组件增强
- [ ] 事件数据模型
- [ ] 滚动加载
- [ ] 筛选功能

Day 12-14: 进度可视化
- [ ] EvolutionProgress 组件增强
- [ ] NetworkTopology 组件
- [ ] 动画效果
```

**状态**: 🟡 **进行中** (预计 2026-04-21 完成)

### 阶段 3: 管理模块 (Week 3)

```
Day 15-16: Agent 管理
- [ ] AgentManager 组件
- [ ] CRUD 操作
- [ ] 状态管理
- [ ] 批量操作

Day 17-18: Skill 管理
- [ ] SkillManager 组件
- [ ] 分类过滤
- [ ] 搜索功能
- [ ] 批量操作

Day 19-21: 审批和网关
- [ ] ApprovalQueue 组件
- [ ] GatewayManager 组件
- [ ] 审批流程
- [ ] 网关配置
```

**状态**: ⏳ **待开始** (预计 2026-04-28 完成)

### 阶段 4: 审计模块 (Week 4)

```
Day 22-23: 操作日志
- [ ] OperationLogs 组件
- [ ] 日志查询
- [ ] 导出功能
- [ ] 筛选排序

Day 24-25: 决策追踪
- [ ] DecisionTrail 组件
- [ ] 关联分析
- [ ] 可视化展示
- [ ] 时间线集成

Day 26-28: 集成测试
- [ ] 单元测试
- [ ] E2E 测试
- [ ] 视觉测试
- [ ] 性能优化
```

**状态**: ⏳ **待开始** (预计 2026-05-05 完成)

---

## 5. 成功指标

### 功能指标
```
✅ 所有核心组件实现
✅ API 接口完整
✅ WebSocket 实时通信
✅ 响应式布局
✅ 多浏览器支持
```

### 性能指标
```
✅ 首屏加载 < 2 秒
✅ 数据更新 < 100ms
✅ WebSocket 延迟 < 50ms
✅ Lighthouse 评分 > 90
✅ Core Web Vitals 全部绿色
```

### 质量指标
```
✅ 测试覆盖率 > 80%
✅ TypeScript 类型完整
✅ 代码规范符合
✅ 文档完整
✅ 无严重安全漏洞
```

### 用户体验指标
```
✅ 页面加载流畅
✅ 交互响应及时
✅ 视觉设计统一
✅ 无障碍访问支持
✅ 多语言支持 (中文/英文)
```

---

## 6. 风险管理

### 技术风险
```
风险：WebSocket 连接稳定性
影响：中
概率：低
缓解：实现重连机制 + 心跳检测

风险：大数据量渲染性能
影响：中
概率：中
缓解：虚拟滚动 + 数据分页 + 懒加载
```

### 进度风险
```
风险：开发时间超出预期
影响：高
概率：中
缓解：优先级排序 + MVP 先行 + 迭代开发

风险：依赖库兼容性问题
影响：低
概率：低
缓解：锁定版本 + 充分测试
```

---

## 7. 交付物清单

### 代码交付
```
✅ frontend/ - 前端源代码
✅ backend/ - 后端源代码
✅ docker/ - Docker 配置
✅ docker-compose.yml - 编排配置
```

### 文档交付
```
✅ README.md - 项目说明
✅ API.md - API 文档
✅ DEPLOYMENT.md - 部署指南
✅ TESTING.md - 测试指南
✅ CONTRIBUTING.md - 贡献指南
```

### 测试交付
```
✅ 单元测试套件
✅ E2E 测试套件
✅ 视觉测试套件
✅ 性能测试报告
✅ 安全扫描报告
```

---

*Dashboard 2.0 详细设计文档 · 太一 AGI · 2026-04-14 23:25*

**✅ 设计完成！开始实施！**
