# 🎨 太一 Dashboard 2.0 详细设计

> **设计时间**: 2026-04-14 23:05  
> **版本**: v2.0.0  
> **状态**: 🟢 设计中

---

## 📊 设计目标

### 核心目标
```
✅ 统一运营界面
✅ 多 Agent 状态实时监控
✅ 自进化进度可视化
✅ 实时数据流展示
✅ 时间线组件
✅ 审计日志
✅ 审批流程管理
✅ 网关状态监控
```

### 参考设计
```
✅ NASA OpenMCT - 数据可视化框架
✅ OpenClaw Mission Control - 运营平台
✅ 太一现有 Dashboard - 继承优化
```

---

## 🏗️ 架构设计

### 技术栈
```
前端:
- React 18
- TypeScript
- Tailwind CSS
- Recharts (图表)
- React Flow (流程图)
- WebSocket (实时数据)

后端:
- Node.js + Express
- WebSocket Server
- RESTful API
- SQLite (本地存储)

部署:
- Docker Compose
- Nginx (反向代理)
```

### 组件架构
```
Dashboard 2.0
├── 布局系统
│   ├── Header (全局导航)
│   ├── Sidebar (侧边栏)
│   ├── Main (主内容区)
│   └── Footer (状态栏)
├── 仪表盘模块
│   ├── Agent 状态卡片
│   ├── Skill 统计图表
│   ├── 任务进度条
│   └── 系统健康度
├── 可视化模块
│   ├── 实时数据流图表
│   ├── 时间线组件
│   ├── 自进化进度图
│   └── 网络拓扑图
├── 管理模块
│   ├── Agent 管理面板
│   ├── Skill 管理面板
│   ├── 审批队列
│   └── 网关管理
└── 审计模块
    ├── 操作日志
    ├── 决策追踪
    └── 事件时间线
```

---

## 🎨 UI/UX 设计

### 配色方案
```
主色调:
- 太一蓝：#1E88E5
- 科技蓝：#0D47A1
- 成功绿：#43A047
- 警告黄：#FFB300
- 错误红：#E53935

背景色:
- 深色模式：#1A1A2E
- 卡片背景：#16213E
- 边框色：#0F3460

文字色:
- 主文字：#FFFFFF
- 次文字：#B0B0B0
```

### 布局设计
```
┌────────────────────────────────────────────┐
│  Header (Logo + 全局导航 + 用户信息)        │
├──────────┬─────────────────────────────────┤
│ Sidebar  │                                 │
│          │         Main Content            │
│ - 仪表盘 │                                 │
│ - Agent  │    [多列网格布局]               │
│ - Skill  │                                 │
│ - 任务   │    - Agent 状态卡片             │
│ - 审批   │    - 实时数据图表               │
│ - 审计   │    - 时间线组件                 │
│ - 设置   │    - 自进化进度                 │
│          │                                 │
├──────────┴─────────────────────────────────┤
│  Footer (系统状态 + Gateway 信息 + 时间)    │
└────────────────────────────────────────────┘
```

---

## 📈 核心组件设计

### 1. Agent 状态卡片
```
┌─────────────────────────────┐
│ 🤖 Agent 名称               │
│ 状态：🟢 运行中             │
│ ─────────────────────────── │
│ 任务：12 进行中 / 156 完成  │
│ 响应：~55 秒                │
│ 健康：98%                   │
│ ─────────────────────────── │
│ [详情] [日志] [管理]        │
└─────────────────────────────┘
```

### 2. 实时数据流图表
```
┌─────────────────────────────┐
│ 📊 实时任务流               │
│                             │
│    ╱╲   ╱╲     ╱╲           │
│   ╱  ╲ ╱  ╲   ╱  ╲          │
│  ╱    ╱    ╲ ╱    ╲         │
│ ╱    ╱      ╱      ╲        │
│───────────────────────────  │
│ 00:00    12:00    23:59     │
│                             │
│ 任务数：342 | 峰值：45/min  │
└─────────────────────────────┘
```

### 3. 自进化进度图
```
┌─────────────────────────────┐
│ 🧬 自进化程度               │
│                             │
│ Level 3 (90-95%)           │
│ ████████████████████░░░░   │
│                             │
│ 本周技能：+50 个            │
│ 优化技能：+23 个            │
│ 新增洞察：+15 条            │
│                             │
│ 下一级：Level 4 (95-100%)  │
│ 进度：████░░░░░░░░ 40%     │
└─────────────────────────────┘
```

### 4. 时间线组件
```
┌─────────────────────────────┐
│ ⏱️ 事件时间线               │
│                             │
│ ● 23:05 - Dashboard 2.0 设计 │
│ ● 22:52 - 任务成果汇报      │
│ ● 22:44 - 进度汇报          │
│ ● 22:38 - Mission Control   │
│ ● 22:35 - NASA OpenMCT      │
│ ● 22:29 - OpenClaw 升级     │
│                             │
│ [查看更多...]               │
└─────────────────────────────┘
```

### 5. 审批队列
```
┌─────────────────────────────┐
│ ✅ 待审批操作               │
│                             │
│ 1. Agent 创建               │
│    请求：创建新 Skill       │
│    时间：23:00              │
│    [批准] [拒绝] [详情]     │
│                             │
│ 2. 敏感操作                 │
│    请求：删除旧配置         │
│    时间：22:45              │
│    [批准] [拒绝] [详情]     │
│                             │
└─────────────────────────────┘
```

---

## 🔌 API 设计

### RESTful API
```
# Agent 相关
GET    /api/v1/agents              # 获取所有 Agent
GET    /api/v1/agents/:id          # 获取 Agent 详情
POST   /api/v1/agents              # 创建 Agent
PUT    /api/v1/agents/:id          # 更新 Agent
DELETE /api/v1/agents/:id          # 删除 Agent

# Skill 相关
GET    /api/v1/skills              # 获取所有 Skill
GET    /api/v1/skills/:id          # 获取 Skill 详情
POST   /api/v1/skills              # 创建 Skill
PUT    /api/v1/skills/:id          # 更新 Skill

# 任务相关
GET    /api/v1/tasks               # 获取任务列表
GET    /api/v1/tasks/:id           # 获取任务详情
POST   /api/v1/tasks               # 创建任务
PUT    /api/v1/tasks/:id/status    # 更新任务状态

# 审批相关
GET    /api/v1/approvals           # 获取审批队列
POST   /api/v1/approvals/:id       # 审批操作
GET    /api/v1/approvals/history   # 审批历史

# 审计相关
GET    /api/v1/audit/logs          # 获取操作日志
GET    /api/v1/audit/timeline      # 获取时间线

# 系统相关
GET    /api/v1/system/health       # 系统健康状态
GET    /api/v1/system/gateway      # Gateway 状态
GET    /api/v1/system/stats        # 系统统计
```

### WebSocket API
```
# 连接
ws://localhost:3000/ws

# 订阅频道
{ "action": "subscribe", "channel": "agents" }
{ "action": "subscribe", "channel": "tasks" }
{ "action": "subscribe", "channel": "approvals" }

# 接收数据
{
  "channel": "agents",
  "type": "status_update",
  "data": {
    "agentId": "taiyi",
    "status": "running",
    "health": 98,
    "timestamp": "2026-04-14T23:05:00Z"
  }
}
```

---

## 📁 文件结构

```
dashboard-2.0/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── index.ts
│   │   │   ├── Dashboard/
│   │   │   │   ├── AgentCard.tsx
│   │   │   │   ├── SkillChart.tsx
│   │   │   │   ├── TaskProgress.tsx
│   │   │   │   └── SystemHealth.tsx
│   │   │   ├── Visualization/
│   │   │   │   ├── RealtimeChart.tsx
│   │   │   │   ├── Timeline.tsx
│   │   │   │   ├── EvolutionProgress.tsx
│   │   │   │   └── NetworkTopology.tsx
│   │   │   ├── Management/
│   │   │   │   ├── AgentManager.tsx
│   │   │   │   ├── SkillManager.tsx
│   │   │   │   ├── ApprovalQueue.tsx
│   │   │   │   └── GatewayManager.tsx
│   │   │   └── Audit/
│   │   │       ├── OperationLogs.tsx
│   │   │       ├── DecisionTrail.tsx
│   │   │       └── EventTimeline.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Agents.tsx
│   │   │   ├── Skills.tsx
│   │   │   ├── Tasks.tsx
│   │   │   ├── Approvals.tsx
│   │   │   ├── Audit.tsx
│   │   │   └── Settings.tsx
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── styles/
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── websocket/
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── nginx.conf
├── docker-compose.yml
├── README.md
└── .env.example
```

---

## 🚀 实施计划

### 阶段 1: 基础架构 (Week 1)
```
Day 1-2: 项目初始化
- [ ] 创建项目结构
- [ ] 配置 TypeScript
- [ ] 配置 Tailwind CSS
- [ ] 配置 Docker

Day 3-4: 布局系统
- [ ] Header 组件
- [ ] Sidebar 组件
- [ ] Footer 组件
- [ ] 响应式布局

Day 5-7: 基础组件
- [ ] AgentCard 组件
- [ ] SkillChart 组件
- [ ] TaskProgress 组件
- [ ] SystemHealth 组件
```

### 阶段 2: 可视化模块 (Week 2)
```
Day 8-9: 图表组件
- [ ] RealtimeChart 组件
- [ ] Recharts 集成
- [ ] WebSocket 连接

Day 10-11: 时间线组件
- [ ] Timeline 组件
- [ ] 事件数据模型
- [ ] 滚动加载

Day 12-14: 进度可视化
- [ ] EvolutionProgress 组件
- [ ] NetworkTopology 组件
- [ ] 数据更新逻辑
```

### 阶段 3: 管理模块 (Week 3)
```
Day 15-16: Agent 管理
- [ ] AgentManager 组件
- [ ] CRUD 操作
- [ ] 状态管理

Day 17-18: Skill 管理
- [ ] SkillManager 组件
- [ ] 分类过滤
- [ ] 批量操作

Day 19-21: 审批和网关
- [ ] ApprovalQueue 组件
- [ ] GatewayManager 组件
- [ ] 审批流程
```

### 阶段 4: 审计模块 (Week 4)
```
Day 22-23: 操作日志
- [ ] OperationLogs 组件
- [ ] 日志查询
- [ ] 导出功能

Day 24-25: 决策追踪
- [ ] DecisionTrail 组件
- [ ] 关联分析
- [ ] 可视化展示

Day 26-28: 集成测试
- [ ] 单元测试
- [ ] E2E 测试
- [ ] 性能优化
```

---

## 📊 成功指标

### 功能指标
```
✅ 所有核心组件实现
✅ API 接口完整
✅ WebSocket 实时通信
✅ 响应式布局
```

### 性能指标
```
✅ 首屏加载 < 2 秒
✅ 数据更新 < 100ms
✅ WebSocket 延迟 < 50ms
✅ Lighthouse 评分 > 90
```

### 质量指标
```
✅ 测试覆盖率 > 80%
✅ TypeScript 类型完整
✅ 代码规范符合
✅ 文档完整
```

---

## 🔗 快速链接

**设计参考**:
- NASA OpenMCT: https://github.com/nasa/openmct
- OpenClaw Mission Control: https://github.com/abhi1693/openclaw-mission-control

**技术文档**:
- React: https://react.dev
- TypeScript: https://www.typescriptlang.org
- Tailwind CSS: https://tailwindcss.com
- Recharts: https://recharts.org

---

*太一 Dashboard 2.0 详细设计 · 太一 AGI · 2026-04-14 23:05*

**🎨 设计完成！准备开始实施！**
